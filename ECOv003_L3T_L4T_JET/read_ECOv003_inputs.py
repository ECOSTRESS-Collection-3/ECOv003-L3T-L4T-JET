"""
Module for reading and processing ECOv003 input data and meteorological variables.

This module contains the read_ECOv003_inputs function which loads and processes
input granules (L2T LSTE and L2T STARS), retrieves meteorological data from GEOS-5 FP,
runs FLiES-ANN for solar radiation, and optionally sharpens meteorological and soil
moisture data.
"""

import logging
from datetime import datetime
from os.path import basename, exists

import numpy as np
import rasters as rt
from rasters import Raster, RasterGeometry

from check_distribution import check_distribution

import colored_logging as cl
from solar_apparent_time import solar_hour_of_day_for_area, solar_day_of_year_for_area
from koppengeiger import load_koppen_geiger
from FLiESANN import FLiESANN
from GEOS5FP import GEOS5FP
from sun_angles import calculate_SZA_from_DOY_and_hour
from MODISCI import MODISCI

from ECOv003_granules import L2TLSTE, L2TSTARS
from ECOv002_granules import L2TLSTE as ECOv002L2TLSTE
from ECOv002_granules import L2TSTARS as ECOv002L2TSTARS

from JET3 import InputFilesInaccessible, DaytimeFilter, BlankOutput
from JET3 import sharpen_meteorology_data
from JET3 import sharpen_soil_moisture_data

from .version import __version__
from .constants import SZA_DEGREE_CUTOFF, GEOS_IN_SENTINEL_COARSE_CELL_SIZE

logger = logging.getLogger(__name__)


def read_ECOv003_inputs(
        L2T_LSTE_filename: str,
        L2T_STARS_filename: str,
        orbit: int,
        scene: int,
        tile: str,
        GEOS5FP_directory: str,
        MODISCI_directory: str,
        time_UTC: datetime,
        date_UTC,
        geometry: RasterGeometry,
        zero_COT_correction: bool,
        sharpen_meteorology: bool,
        sharpen_soil_moisture: bool,
        upsampling: str,
        downsampling: str) -> dict:
    """
    Read and process ECOv003 input data from L2T LSTE and L2T STARS granules.
    
    This function loads input granules, retrieves meteorological data from GEOS-5 FP,
    sharpens meteorology and soil moisture (if enabled), and prepares all necessary 
    inputs for FLiES-ANN solar radiation modeling.
    Note: FLiES-ANN is called in the main L3T_L4T_JET function, not here.
    
    Args:
        L2T_LSTE_filename: Path to the L2T LSTE input file.
        L2T_STARS_filename: Path to the L2T STARS input file.
        orbit: Orbit number.
        scene: Scene number.
        tile: Tile identifier.
        GEOS5FP_directory: Directory containing GEOS-5 FP data.
        MODISCI_directory: Directory containing MODIS clumping index data.
        time_UTC: UTC time of the overpass.
        date_UTC: UTC date of the overpass.
        geometry: Raster geometry for the tile.
        zero_COT_correction: Whether to set Cloud Optical Thickness to zero.
        sharpen_meteorology: Whether to sharpen meteorological variables.
        sharpen_soil_moisture: Whether to sharpen soil moisture.
        upsampling: Upsampling method for spatial resampling.
        downsampling: Downsampling method for spatial resampling.
    
    Returns:
        A dictionary containing input variables and metadata needed for FLiES-ANN and subsequent processing:
        - metadata: Product metadata dictionary
        - ST_K, ST_C: Surface temperature in Kelvin and Celsius
        - elevation_km: Elevation in kilometers
        - elevation_m: Elevation in meters
        - emissivity: Surface emissivity
        - water_mask: Water mask
        - cloud_mask: Cloud mask
        - NDVI: Normalized Difference Vegetation Index
        - albedo: Surface albedo
        - GEOS5FP_connection: GEOS-5 FP connection object
        - MODISCI_connection: MODIS CI connection object
        - SZA_deg: Solar zenith angle in degrees
        - AOT: Aerosol optical thickness
        - COT: Cloud optical thickness (corrected if zero_COT_correction=True)
        - vapor_gccm: Water vapor in g/cm²
        - ozone_cm: Ozone in cm
        - hour_of_day: Solar hour of day
        - day_of_year: Solar day of year
        - time_solar: Solar time
        - KG_climate: Köppen-Geiger climate classification
        - coarse_geometry: Coarse resolution geometry
        - Ta_C: Air temperature in Celsius (sharpened if enabled)
        - Ta_C_smooth: Smoothed air temperature in Celsius
        - RH: Relative humidity (sharpened if enabled)
        - SM: Soil moisture (sharpened if enabled)
        - SVP_Pa: Saturated vapor pressure in Pa
        - Ea_Pa: Actual vapor pressure in Pa
        - Ea_kPa: Actual vapor pressure in kPa
        - Ta_K: Air temperature in Kelvin
    """
    # Check L2T LSTE file existence
    if not exists(L2T_LSTE_filename):
        raise InputFilesInaccessible(f"L2T LSTE file does not exist: {L2T_LSTE_filename}")

    # Load L2T LSTE granule based on collection version
    L2T_LSTE_basename = basename(L2T_LSTE_filename)
    if "ECOv003" in L2T_LSTE_basename:
        L2T_LSTE_granule = L2TLSTE(L2T_LSTE_filename)
    elif "ECOv002" in L2T_LSTE_basename:
        L2T_LSTE_granule = ECOv002L2TLSTE(L2T_LSTE_filename)
    else:
        raise ValueError(f"collection not recognized in L2T LSTE filename: {L2T_LSTE_filename}")

    # Check L2T STARS file existence
    if not exists(L2T_STARS_filename):
        raise InputFilesInaccessible(f"L2T STARS file does not exist: {L2T_STARS_filename}")

    # Load L2T STARS granule based on collection version
    L2T_STARS_basename = basename(L2T_STARS_filename)
    if "ECOv003" in L2T_STARS_basename:
        L2T_STARS_granule = L2TSTARS(L2T_STARS_filename)
    elif "ECOv002" in L2T_STARS_basename:
        L2T_STARS_granule = ECOv002L2TSTARS(L2T_STARS_filename)
    else:
        raise ValueError(f"collection not recognized in L2T STARS filename: {L2T_STARS_filename}")

    # Prepare metadata
    metadata = L2T_STARS_granule.metadata_dict
    metadata["StandardMetadata"]["PGEVersion"] = __version__
    metadata["StandardMetadata"]["PGEName"] = "L3T_L4T_JET"
    metadata["StandardMetadata"]["ProcessingLevelID"] = "L3T"
    metadata["StandardMetadata"]["SISName"] = "Level 3 Product Specification Document"
    metadata["StandardMetadata"]["SISVersion"] = "Preliminary"
    metadata["StandardMetadata"]["AuxiliaryInputPointer"] = "AuxiliaryNWP"

    # Extract time information
    time_solar = L2T_LSTE_granule.time_solar
    logger.info(
        f"orbit {cl.val(orbit)} scene {cl.val(scene)} tile {cl.place(tile)} overpass time: {cl.time(time_UTC)} UTC ({cl.time(time_solar)} solar)")
    
    # Calculate solar time variables
    hour_of_day = solar_hour_of_day_for_area(time_UTC=time_UTC, geometry=geometry)
    day_of_year = solar_day_of_year_for_area(time_UTC=time_UTC, geometry=geometry)

    # Read surface temperature from L2T LSTE
    logger.info("reading surface temperature from L2T LSTE product")
    ST_K = L2T_LSTE_granule.ST_K
    ST_C = ST_K - 273.15
    check_distribution(ST_C, "ST_C", date_UTC=date_UTC, target=tile)

    # Read elevation
    logger.info(f"reading elevation from L2T LSTE: {L2T_LSTE_granule.product_filename}")
    elevation_km = L2T_LSTE_granule.elevation_km
    check_distribution(elevation_km, "elevation_km", date_UTC=date_UTC, target=tile)

    # Read emissivity and water mask
    emissivity = L2T_LSTE_granule.emissivity
    water_mask = L2T_LSTE_granule.water

    # Read cloud mask
    logger.info("reading cloud mask from L2T LSTE product")
    cloud_mask = L2T_LSTE_granule.cloud
    check_distribution(cloud_mask, "cloud_mask", date_UTC=date_UTC, target=tile)

    # Read NDVI from L2T STARS
    logger.info("reading NDVI from L2T STARS product")
    NDVI = L2T_STARS_granule.NDVI
    check_distribution(NDVI, "NDVI", date_UTC=date_UTC, target=tile)

    # Read albedo from L2T STARS
    logger.info("reading albedo from L2T STARS product")
    albedo = L2T_STARS_granule.albedo
    check_distribution(albedo, "albedo", date_UTC=date_UTC, target=tile)

    # Calculate cloud percentage for metadata
    percent_cloud = 100 * np.count_nonzero(cloud_mask) / cloud_mask.size
    metadata["ProductMetadata"]["QAPercentCloudCover"] = percent_cloud

    # Initialize GEOS-5 FP and MODIS CI connections
    GEOS5FP_connection = GEOS5FP(download_directory=GEOS5FP_directory)
    MODISCI_connection = MODISCI(directory=MODISCI_directory)

    # Calculate solar zenith angle
    SZA_deg = calculate_SZA_from_DOY_and_hour(
        lat=geometry.lat,
        lon=geometry.lon,
        DOY=day_of_year,
        hour=hour_of_day
    )
    check_distribution(SZA_deg, "SZA", date_UTC=date_UTC, target=tile)

    # Check for nighttime conditions
    if np.all(SZA_deg >= SZA_DEGREE_CUTOFF):
        raise DaytimeFilter(
            f"solar zenith angle exceeds {SZA_DEGREE_CUTOFF} for orbit {orbit} scene {scene} tile {tile} at {time_UTC} UTC")

    # Retrieve atmospheric variables from GEOS-5 FP
    logger.info("retrieving GEOS-5 FP aerosol optical thickness raster")
    AOT = GEOS5FP_connection.AOT(time_UTC=time_UTC, geometry=geometry)
    check_distribution(AOT, "AOT", date_UTC=date_UTC, target=tile)

    logger.info("generating GEOS-5 FP cloud optical thickness raster")
    COT = GEOS5FP_connection.COT(time_UTC=time_UTC, geometry=geometry)
    check_distribution(COT, "COT", date_UTC=date_UTC, target=tile)

    logger.info("generating GEOS5-FP water vapor raster in grams per square centimeter")
    vapor_gccm = GEOS5FP_connection.vapor_gccm(time_UTC=time_UTC, geometry=geometry)
    check_distribution(vapor_gccm, "vapor_gccm", date_UTC=date_UTC, target=tile)

    logger.info("generating GEOS5-FP ozone raster in grams per square centimeter")
    ozone_cm = GEOS5FP_connection.ozone_cm(time_UTC=time_UTC, geometry=geometry)
    check_distribution(ozone_cm, "ozone_cm", date_UTC=date_UTC, target=tile)

    # Calculate derived variables needed for later processing
    KG_climate = load_koppen_geiger(albedo.geometry)
    
    # Apply COT correction if requested
    if zero_COT_correction:
        COT = COT * 0.0
    
    elevation_m = elevation_km * 1000

    # Create coarse geometry
    coarse_geometry = geometry.rescale(GEOS_IN_SENTINEL_COARSE_CELL_SIZE)

    # Sharpen meteorological variables if enabled
    if sharpen_meteorology:
        try:
            Ta_C, RH, Ta_C_smooth = sharpen_meteorology_data(
                ST_C=ST_C,
                NDVI=NDVI,
                albedo=albedo,
                geometry=geometry,
                coarse_geometry=coarse_geometry,
                time_UTC=time_UTC,
                upsampling=upsampling,
                downsampling=downsampling,
                GEOS5FP_connection=GEOS5FP_connection
            )
        except Exception as e:
            logger.error(e)
            logger.warning("unable to sharpen meteorology")
            Ta_C = GEOS5FP_connection.Ta_C(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)
            Ta_C_smooth = Ta_C
            RH = GEOS5FP_connection.RH(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)
    else:
        Ta_C = GEOS5FP_connection.Ta_C(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)
        Ta_C_smooth = Ta_C
        RH = GEOS5FP_connection.RH(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)

    # Sharpen soil moisture if enabled
    if sharpen_soil_moisture:
        try:
            SM = sharpen_soil_moisture_data(
                ST_C=ST_C,
                NDVI=NDVI,
                albedo=albedo,
                water_mask=water_mask,
                geometry=geometry,
                coarse_geometry=coarse_geometry,
                time_UTC=time_UTC,
                upsampling=upsampling,
                downsampling=downsampling,
                GEOS5FP_connection=GEOS5FP_connection
            )
        except Exception as e:
            logger.error(e)
            logger.warning("unable to sharpen soil moisture")
            SM = GEOS5FP_connection.SM(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)
    else:
        SM = GEOS5FP_connection.SM(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)

    # Calculate vapor pressure variables
    SVP_Pa = 0.6108 * np.exp((17.27 * Ta_C) / (Ta_C + 237.3)) * 1000  # [Pa]
    Ea_Pa = RH * SVP_Pa
    Ea_kPa = Ea_Pa / 1000
    Ta_K = Ta_C + 273.15

    # Return all variables as a dictionary
    return {
        'metadata': metadata,
        'ST_K': ST_K,
        'ST_C': ST_C,
        'elevation_km': elevation_km,
        'elevation_m': elevation_m,
        'emissivity': emissivity,
        'water_mask': water_mask,
        'cloud_mask': cloud_mask,
        'NDVI': NDVI,
        'albedo': albedo,
        'GEOS5FP_connection': GEOS5FP_connection,
        'MODISCI_connection': MODISCI_connection,
        'SZA_deg': SZA_deg,
        'AOT': AOT,
        'COT': COT,
        'vapor_gccm': vapor_gccm,
        'ozone_cm': ozone_cm,
        'hour_of_day': hour_of_day,
        'day_of_year': day_of_year,
        'time_solar': time_solar,
        'KG_climate': KG_climate,
        'coarse_geometry': coarse_geometry,
        'Ta_C': Ta_C,
        'Ta_C_smooth': Ta_C_smooth,
        'RH': RH,
        'SM': SM,
        'SVP_Pa': SVP_Pa,
        'Ea_Pa': Ea_Pa,
        'Ea_kPa': Ea_kPa,
        'Ta_K': Ta_K
    }
