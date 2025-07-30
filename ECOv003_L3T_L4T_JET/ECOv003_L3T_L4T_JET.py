import logging  # Used for logging messages and tracking execution.
import posixpath  # For manipulating POSIX-style paths (e.g., for file operations).
import shutil  # For high-level file operations, like zipping directories.
import socket  # For network-related operations, potentially for checking server reachability.
import sys  # Provides access to system-specific parameters and functions, used for command-line arguments and exit.
import warnings  # For issuing warnings.
from datetime import datetime  # For working with dates and times.
from os import makedirs  # For creating directories.
from os.path import join, abspath, dirname, expanduser, exists, basename  # For path manipulation (joining, absolute paths, directory names, user home, existence check, base name).
from shutil import which  # For finding the path to an executable.
from uuid import uuid4  # For generating unique identifiers.
from pytictoc import TicToc  # A simple timer for measuring code execution time.
import numpy as np  # Fundamental package for numerical computation, especially with arrays.
import pandas as pd  # For data manipulation and analysis, especially with tabular data (DataFrames).
import sklearn  # Scikit-learn, a machine learning library.
import sklearn.linear_model  # Specifically for linear regression models.
from dateutil import parser  # For parsing dates and times from various formats.

import colored_logging as cl  # Custom module for colored console logging.

import rasters as rt  # Custom or external library for raster data processing.
from rasters import Raster, RasterGrid, RasterGeometry  # Specific classes from the rasters library for handling raster data, grids, and geometries.
from rasters import linear_downscale, bias_correct  # Functions for downscaling and bias correction of rasters.

from check_distribution import check_distribution  # Custom module for checking and potentially visualizing data distributions.

from solar_apparent_time import UTC_offset_hours_for_area, solar_hour_of_day_for_area, solar_day_of_year_for_area  # Custom modules for solar time calculations.

from koppengeiger import load_koppen_geiger  # Custom module for loading Köppen-Geiger climate data.
import FLiESANN  # Custom module for the FLiES-ANN (Forest Light Environmental Simulator - Artificial Neural Network) model.
from GEOS5FP import GEOS5FP, FailedGEOS5FPDownload  # Custom module for interacting with GEOS-5 FP atmospheric data, including an exception for download failures.
from sun_angles import calculate_SZA_from_DOY_and_hour  # Custom module for calculating Solar Zenith Angle (SZA).

from MCD12C1_2019_v006 import load_MCD12C1_IGBP  # Custom module for loading MODIS Land Cover Type (IGBP classification) data.
from FLiESLUT import process_FLiES_LUT_raster  # Custom module for processing FLiES Look-Up Table (LUT) rasters.
from FLiESANN import FLiESANN  # Re-importing FLiESANN, potentially the main class.

from MODISCI import MODISCI
from BESS_JPL import BESS_JPL  # Custom module for the BESS-JPL (Breathing Earth System Simulator - Jet Propulsion Laboratory) model.
from PMJPL import PMJPL  # Custom module for the PMJPL (Penman-Monteith Jet Propulsion Laboratory) model.
from STIC_JPL import STIC_JPL  # Custom module for the STIC-JPL (Surface Temperature Initiated Closure - Jet Propulsion Laboratory) model.
from PTJPLSM import PTJPLSM  # Custom module for the PTJPLSM (Priestley-Taylor Jet Propulsion Laboratory - Soil Moisture) model.
from verma_net_radiation import verma_net_radiation, daily_Rn_integration_verma  # Custom modules for net radiation calculation using Verma's model and daily integration.
from sun_angles import SHA_deg_from_DOY_lat, sunrise_from_SHA, daylight_from_SHA  # Additional solar angle calculations.

from ECOv003_granules import write_L3T_JET  # Functions for writing ECOSTRESS Level 3/4 products.
from ECOv003_granules import write_L3T_ETAUX
from ECOv003_granules import write_L4T_ESI
from ECOv003_granules import write_L4T_WUE

from ECOv003_granules import L2TLSTE, L2TSTARS, L3TJET, L3TSM, L3TSEB, L3TMET, L4TESI, L4TWUE  # Product classes or constants from ECOv003_granules.
from ECOv003_granules import ET_COLORMAP, SM_COLORMAP, WATER_COLORMAP, CLOUD_COLORMAP, RH_COLORMAP, GPP_COLORMAP  # Colormaps for visualization.

from ECOv003_exit_codes import * # Import all custom exit codes.

from .version import __version__  # Import the package version.
from .constants import * # Import all constants used in the package.
from .runconfig import read_runconfig, ECOSTRESSRunConfig  # Modules for reading and handling run configuration.

from .generate_L3T_L4T_JET_runconfig import generate_L3T_L4T_JET_runconfig  # Module for generating run configuration files.
from .L3TL4TJETConfig import L3TL4TJETConfig  # Specific run configuration class for L3T/L4T JET.

from .NDVI_to_FVC import NDVI_to_FVC  # Module for converting NDVI to Fractional Vegetation Cover.

from .sharpen_meteorology_data import sharpen_meteorology_data  # Module for sharpening meteorological data.
from .sharpen_soil_moisture_data import sharpen_soil_moisture_data  # Module for sharpening soil moisture data.

from .exceptions import *

from .version import __version__

logger = logging.getLogger(__name__)  # Get a logger instance for this module.

def L3T_L4T_JET(
        runconfig_filename: str,
        upsampling: str = None,
        downsampling: str = None,
        SWin_model_name: str = SWIN_MODEL_NAME,
        Rn_model_name: str = RN_MODEL_NAME,
        include_SEB_diagnostics: bool = INCLUDE_SEB_DIAGNOSTICS,
        include_JET_diagnostics: bool = INCLUDE_JET_DIAGNOSTICS,
        bias_correct_FLiES_ANN: bool = BIAS_CORRECT_FLIES_ANN,
        zero_COT_correction: bool = ZERO_COT_CORRECTION,
        sharpen_meteorology: bool = SHARPEN_METEOROLOGY,
        sharpen_soil_moisture: bool = SHARPEN_SOIL_MOISTURE,
        strip_console: bool = STRIP_CONSOLE,
        save_intermediate: bool = SAVE_INTERMEDIATE,
        show_distribution: bool = SHOW_DISTRIBUTION,
        floor_Topt: bool = FLOOR_TOPT) -> int:
    """
    Processes ECOSTRESS L2T LSTE and L2T STARS granules to produce L3T and L4T JET products (ECOSTRESS Collection 3).

    This function orchestrates the entire processing workflow, including reading run configuration,
    loading input data, performing meteorological and soil moisture sharpening, running
    evapotranspiration and gross primary productivity models (FLiES-ANN, BESS-JPL, STIC-JPL, PMJPL, PTJPLSM),
    calculating daily integrated products, and writing the output granules.

    Args:
        runconfig_filename: Path to the XML run configuration file.
        upsampling: Upsampling method for spatial resampling (e.g., 'average', 'linear'). Defaults to 'average'.
        downsampling: Downsampling method for spatial resampling (e.g., 'linear', 'average'). Defaults to 'linear'.
        SWin_model_name: Model to use for incoming shortwave radiation ('GEOS5FP', 'FLiES-ANN', 'FLiES-LUT'). Defaults to SWIN_MODEL_NAME.
        Rn_model_name: Model to use for net radiation ('verma', 'BESS'). Defaults to RN_MODEL_NAME.
        include_SEB_diagnostics: Whether to include Surface Energy Balance diagnostics in the output. Defaults to INCLUDE_SEB_DIAGNOSTICS.
        include_JET_diagnostics: Whether to include JET diagnostics in the output. Defaults to INCLUDE_JET_DIAGNOSTICS.
        bias_correct_FLiES_ANN: Whether to bias correct the FLiES-ANN shortwave radiation output. Defaults to BIAS_CORRECT_FLIES_ANN.
        zero_COT_correction: Whether to set Cloud Optical Thickness to zero for correction. Defaults to ZERO_COT_CORRECTION.
        sharpen_meteorology: Whether to sharpen meteorological variables using a regression model. Defaults to SHARPEN_METEOROLOGY.
        sharpen_soil_moisture: Whether to sharpen soil moisture using a regression model. Defaults to SHARPEN_SOIL_MOISTURE.
        strip_console: Whether to strip console output from the logger. Defaults to STRIP_CONSOLE.
        save_intermediate: Whether to save intermediate processing steps. Defaults to SAVE_INTERMEDIATE.
        show_distribution: Whether to show distribution plots of intermediate and final products. Defaults to SHOW_DISTRIBUTION.
        floor_Topt: Whether to floor the optimal temperature (Topt) in the models. Defaults to FLOOR_TOPT.

    Returns:
        An integer representing the exit code of the process.
    """
    exit_code = SUCCESS_EXIT_CODE

    if upsampling is None:
        upsampling = "average"

    if downsampling is None:
        downsampling = "linear"

    try:
        runconfig = L3TL4TJETConfig(runconfig_filename)
        working_directory = runconfig.working_directory
        granule_ID = runconfig.granule_ID
        log_filename = join(working_directory, "log", f"{granule_ID}.log")
        cl.configure(filename=log_filename, strip_console=strip_console)
        timer = TicToc()
        timer.tic()
        logger.info(f"started L3T L4T JET run at {cl.time(datetime.utcnow())} UTC")
        logger.info(f"L3T_L4T_JET PGE ({cl.val(runconfig.PGE_version)})")
        logger.info(f"L3T_L4T_JET run-config: {cl.file(runconfig_filename)}")

        L3T_JET_granule_ID = runconfig.L3T_JET_granule_ID
        logger.info(f"L3T JET granule ID: {cl.val(L3T_JET_granule_ID)}")

        L3T_JET_directory = runconfig.L3T_JET_directory
        logger.info(f"L3T JET granule directory: {cl.dir(L3T_JET_directory)}")
        L3T_JET_zip_filename = runconfig.L3T_JET_zip_filename
        logger.info(f"L3T JET zip file: {cl.file(L3T_JET_zip_filename)}")
        L3T_JET_browse_filename = runconfig.L3T_JET_browse_filename
        logger.info(f"L3T JET preview: {cl.file(L3T_JET_browse_filename)}")

        L3T_ETAUX_directory = runconfig.L3T_ETAUX_directory
        logger.info(f"L3T ETAUX granule directory: {cl.dir(L3T_ETAUX_directory)}")
        L3T_ETAUX_zip_filename = runconfig.L3T_ETAUX_zip_filename
        logger.info(f"L3T ETAUX zip file: {cl.file(L3T_ETAUX_zip_filename)}")
        L3T_ETAUX_browse_filename = runconfig.L3T_ETAUX_browse_filename
        logger.info(f"L3T ETAUX preview: {cl.file(L3T_ETAUX_browse_filename)}")

        L3T_BESS_directory = runconfig.L3T_BESS_directory
        logger.info(f"L3T BESS granule directory: {cl.dir(L3T_BESS_directory)}")
        L3T_BESS_zip_filename = runconfig.L3T_BESS_zip_filename
        logger.info(f"L3T BESS zip file: {cl.file(L3T_BESS_zip_filename)}")
        L3T_BESS_browse_filename = runconfig.L3T_BESS_browse_filename
        logger.info(f"L3T BESS preview: {cl.file(L3T_BESS_browse_filename)}")

        L3T_MET_directory = runconfig.L3T_MET_directory
        logger.info(f"L3T MET granule directory: {cl.dir(L3T_MET_directory)}")
        L3T_MET_zip_filename = runconfig.L3T_MET_zip_filename
        logger.info(f"L3T MET zip file: {cl.file(L3T_MET_zip_filename)}")
        L3T_MET_browse_filename = runconfig.L3T_MET_browse_filename
        logger.info(f"L3T MET preview: {cl.file(L3T_MET_browse_filename)}")

        L3T_SEB_directory = runconfig.L3T_SEB_directory
        logger.info(f"L3T SEB granule directory: {cl.dir(L3T_SEB_directory)}")
        L3T_SEB_zip_filename = runconfig.L3T_SEB_zip_filename
        logger.info(f"L3T SEB zip file: {cl.file(L3T_SEB_zip_filename)}")
        L3T_SEB_browse_filename = runconfig.L3T_SEB_browse_filename
        logger.info(f"L3T SEB preview: {cl.file(L3T_SEB_browse_filename)}")

        L3T_SM_directory = runconfig.L3T_SM_directory
        logger.info(f"L3T SM granule directory: {cl.dir(L3T_SM_directory)}")
        L3T_SM_zip_filename = runconfig.L3T_SM_zip_filename
        logger.info(f"L3T SM zip file: {cl.file(L3T_SM_zip_filename)}")
        L3T_SM_browse_filename = runconfig.L3T_SM_browse_filename
        logger.info(f"L3T SM preview: {cl.file(L3T_SM_browse_filename)}")

        L4T_ESI_granule_ID = runconfig.L4T_ESI_granule_ID
        logger.info(f"L4T ESI PT-JPL granule ID: {cl.val(L4T_ESI_granule_ID)}")
        L4T_ESI_directory = runconfig.L4T_ESI_directory
        logger.info(f"L4T ESI PT-JPL granule directory: {cl.dir(L4T_ESI_directory)}")
        L4T_ESI_zip_filename = runconfig.L4T_ESI_zip_filename
        logger.info(f"L4T ESI PT-JPL zip file: {cl.file(L4T_ESI_zip_filename)}")
        L4T_ESI_browse_filename = runconfig.L4T_ESI_browse_filename
        logger.info(f"L4T ESI PT-JPL preview: {cl.file(L4T_ESI_browse_filename)}")

        L4T_WUE_granule_ID = runconfig.L4T_WUE_granule_ID
        logger.info(f"L4T WUE granule ID: {cl.val(L4T_WUE_granule_ID)}")
        L4T_WUE_directory = runconfig.L4T_WUE_directory
        logger.info(f"L4T WUE granule directory: {cl.dir(L4T_WUE_directory)}")
        L4T_WUE_zip_filename = runconfig.L4T_WUE_zip_filename
        logger.info(f"L4T WUE zip file: {cl.file(L4T_WUE_zip_filename)}")
        L4T_WUE_browse_filename = runconfig.L4T_WUE_browse_filename
        logger.info(f"L4T WUE preview: {cl.file(L4T_WUE_browse_filename)}")

        required_files = [
            L3T_JET_zip_filename,
            L3T_JET_browse_filename,
            L3T_MET_zip_filename,
            L3T_MET_browse_filename,
            L3T_SEB_zip_filename,
            L3T_SEB_browse_filename,
            L3T_SM_zip_filename,
            L3T_SM_browse_filename,
            L4T_ESI_zip_filename,
            L4T_ESI_browse_filename,
            L4T_WUE_zip_filename,
            L4T_WUE_browse_filename
        ]

        some_files_missing = False

        for filename in required_files:
            if exists(filename):
                logger.info(f"found product file: {cl.file(filename)}")
            else:
                logger.info(f"product file not found: {cl.file(filename)}")
                some_files_missing = True

        if not some_files_missing:
            logger.info("L3T_L4T_JET output already found")
            return SUCCESS_EXIT_CODE

        logger.info(f"working_directory: {cl.dir(working_directory)}")
        output_directory = runconfig.output_directory
        logger.info(f"output directory: {cl.dir(output_directory)}")
        sources_directory = runconfig.sources_directory
        logger.info(f"sources directory: {cl.dir(sources_directory)}")
        GEOS5FP_directory = runconfig.GEOS5FP_directory
        logger.info(f"GEOS-5 FP directory: {cl.dir(GEOS5FP_directory)}")
        static_directory = runconfig.static_directory
        logger.info(f"static directory: {cl.dir(static_directory)}")
        GEDI_directory = runconfig.GEDI_directory
        logger.info(f"GEDI directory: {cl.dir(GEDI_directory)}")
        MODISCI_directory = runconfig.MODISCI_directory
        logger.info(f"MODIS CI directory: {cl.dir(MODISCI_directory)}")
        MCD12_directory = runconfig.MCD12_directory
        logger.info(f"MCD12C1 IGBP directory: {cl.dir(MCD12_directory)}")
        soil_grids_directory = runconfig.soil_grids_directory
        logger.info(f"SoilGrids directory: {cl.dir(soil_grids_directory)}")
        logger.info(f"log: {cl.file(log_filename)}")
        orbit = runconfig.orbit
        logger.info(f"orbit: {cl.val(orbit)}")
        scene = runconfig.scene
        logger.info(f"scene: {cl.val(scene)}")
        tile = runconfig.tile
        logger.info(f"tile: {cl.val(tile)}")
        build = runconfig.build
        logger.info(f"build: {cl.val(build)}")
        product_counter = runconfig.product_counter
        logger.info(f"product counter: {cl.val(product_counter)}")
        L2T_LSTE_filename = runconfig.L2T_LSTE_filename
        logger.info(f"L2T_LSTE file: {cl.file(L2T_LSTE_filename)}")
        L2T_STARS_filename = runconfig.L2T_STARS_filename
        logger.info(f"L2T_STARS file: {cl.file(L2T_STARS_filename)}")

        if not exists(L2T_LSTE_filename):
            raise InputFilesInaccessible(f"L2T LSTE file does not exist: {L2T_LSTE_filename}")

        L2T_LSTE_granule = L2TLSTE(L2T_LSTE_filename)

        if not exists(L2T_STARS_filename):
            raise InputFilesInaccessible(f"L2T STARS file does not exist: {L2T_STARS_filename}")

        L2T_STARS_granule = L2TSTARS(L2T_STARS_filename)

        metadata = L2T_STARS_granule.metadata_dict
        metadata["StandardMetadata"]["PGEVersion"] = __version__
        metadata["StandardMetadata"]["PGEName"] = "L3T_L4T_JET"
        metadata["StandardMetadata"]["ProcessingLevelID"] = "L3T"
        metadata["StandardMetadata"]["SISName"] = "Level 3 Product Specification Document"
        metadata["StandardMetadata"]["SISVersion"] = "Preliminary"
        metadata["StandardMetadata"]["AuxiliaryInputPointer"] = "AuxiliaryNWP"

        geometry = L2T_LSTE_granule.geometry
        time_UTC = L2T_LSTE_granule.time_UTC
        date_UTC = time_UTC.date()
        time_solar = L2T_LSTE_granule.time_solar
        logger.info(
            f"orbit {cl.val(orbit)} scene {cl.val(scene)} tile {cl.place(tile)} overpass time: {cl.time(time_UTC)} UTC ({cl.time(time_solar)} solar)")
        timestamp = f"{time_UTC:%Y%m%dT%H%M%S}"

        hour_of_day = solar_hour_of_day_for_area(time_UTC=time_UTC, geometry=geometry)
        day_of_year = solar_day_of_year_for_area(time_UTC=time_UTC, geometry=geometry)

        ST_K = L2T_LSTE_granule.ST_K

        logger.info(f"reading elevation from L2T LSTE: {L2T_LSTE_granule.product_filename}")
        elevation_km = L2T_LSTE_granule.elevation_km
        check_distribution(elevation_km, "elevation_km", date_UTC=date_UTC, target=tile)

        emissivity = L2T_LSTE_granule.emissivity
        water_mask = L2T_LSTE_granule.water
        cloud_mask = L2T_LSTE_granule.cloud
        NDVI = L2T_STARS_granule.NDVI
        albedo = L2T_STARS_granule.albedo

        percent_cloud = 100 * np.count_nonzero(cloud_mask) / cloud_mask.size
        metadata["ProductMetadata"]["QAPercentCloudCover"] = percent_cloud

        GEOS5FP_connection = GEOS5FP(
            download_directory=GEOS5FP_directory
        )

        MODISCI_connection = MODISCI(directory=MODISCI_directory)

        SZA = calculate_SZA_from_DOY_and_hour(
            lat=geometry.lat,
            lon=geometry.lon,
            DOY=day_of_year,
            hour=hour_of_day
        )

        check_distribution(SZA, "SZA", date_UTC=date_UTC, target=tile)

        if np.all(SZA >= SZA_DEGREE_CUTOFF):
            raise DaytimeFilter(f"solar zenith angle exceeds {SZA_DEGREE_CUTOFF} for orbit {orbit} scene {scene} tile {tile} at {time_UTC} UTC")

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

        logger.info(f"running Forest Light Environmental Simulator for {cl.place(tile)} at {cl.time(time_UTC)} UTC")

        doy_solar = time_solar.timetuple().tm_yday
        KG_climate = load_koppen_geiger(albedo.geometry)

        if zero_COT_correction:
            COT = COT * 0.0

        FLiES_results = FLiESANN(
            albedo=albedo,
            geometry=geometry,
            time_UTC=time_UTC,
            day_of_year=doy_solar,
            hour_of_day=hour_of_day,
            COT=COT,
            AOT=AOT,
            vapor_gccm=vapor_gccm,
            ozone_cm=ozone_cm,
            elevation_km=elevation_km,
            SZA=SZA,
            KG_climate=KG_climate,
            GEOS5FP_connection=GEOS5FP_connection,
        )

        Ra = FLiES_results["Ra"]
        SWin_FLiES_ANN_raw = FLiES_results["Rg"]
        UV = FLiES_results["UV"]
        VIS = FLiES_results["VIS"]
        NIR = FLiES_results["NIR"]
        VISdiff = FLiES_results["VISdiff"]
        NIRdiff = FLiES_results["NIRdiff"]
        VISdir = FLiES_results["VISdir"]
        NIRdir = FLiES_results["NIRdir"]

        albedo_NWP = GEOS5FP_connection.ALBEDO(time_UTC=time_UTC, geometry=geometry)
        RVIS_NWP = GEOS5FP_connection.ALBVISDR(time_UTC=time_UTC, geometry=geometry)
        albedo_visible = rt.clip(albedo * (RVIS_NWP / albedo_NWP), 0, 1)
        check_distribution(albedo_visible, "RVIS")
        RNIR_NWP = GEOS5FP_connection.ALBNIRDR(time_UTC=time_UTC, geometry=geometry)
        albedo_NIR = rt.clip(albedo * (RNIR_NWP / albedo_NWP), 0, 1)
        check_distribution(albedo_NIR, "RNIR")
        PARDir = VISdir
        check_distribution(PARDir, "PARDir")

        SWin_FLiES_LUT= process_FLiES_LUT_raster(
            geometry=geometry,
            time_UTC=time_UTC,
            cloud_mask=cloud_mask,
            COT=COT,
            koppen_geiger=KG_climate,
            albedo=albedo,
            SZA=SZA,
            GEOS5FP_connection=GEOS5FP_connection
        )

        coarse_geometry = geometry.rescale(GEOS_IN_SENTINEL_COARSE_CELL_SIZE)

        SWin_coarse = GEOS5FP_connection.SWin(
            time_UTC=time_UTC,
            geometry=coarse_geometry,
            resampling=downsampling
        )

        if bias_correct_FLiES_ANN:
            SWin_FLiES_ANN = bias_correct(
                coarse_image=SWin_coarse,
                fine_image=SWin_FLiES_ANN_raw,
                upsampling=upsampling,
                downsampling=downsampling
            )
        else:
            SWin_FLiES_ANN = SWin_FLiES_ANN_raw

        check_distribution(SWin_FLiES_ANN, "SWin_FLiES_ANN", date_UTC=date_UTC, target=tile)

        SWin_GEOS5FP = GEOS5FP_connection.SWin(
            time_UTC=time_UTC,
            geometry=geometry,
            resampling=downsampling
        )

        check_distribution(SWin_GEOS5FP, "SWin_GEOS5FP", date_UTC=date_UTC, target=tile)

        if SWin_model_name == "GEOS5FP":
            SWin = SWin_GEOS5FP
        elif SWin_model_name == "FLiES-ANN":
            SWin = SWin_FLiES_ANN
        elif SWin_model_name == "FLiES-LUT":
            SWin = SWin_FLiES_LUT
        else:
            raise ValueError(f"unrecognized solar radiation model: {SWin_model_name}")

        SWin = rt.where(np.isnan(ST_K), np.nan, SWin)

        if np.all(np.isnan(SWin)) or np.all(SWin == 0):
            raise BlankOutput(f"blank solar radiation output for orbit {orbit} scene {scene} tile {tile} at {time_UTC} UTC")

        ST_C = ST_K - 273.15

        # Sharpen meteorological variables if enabled.
        if sharpen_meteorology:
            Ta_C, RH, Ta_C_smooth = sharpen_meteorology_data(
                ST_C=ST_C,
                NDVI=NDVI,
                albedo=albedo,
                geometry=geometry,
                coarse_geometry=coarse_geometry,
                time_UTC=time_UTC,
                date_UTC=date_UTC,
                tile=tile,
                orbit=orbit,
                scene=scene,
                upsampling=upsampling,
                downsampling=downsampling,
                GEOS5FP_connection=GEOS5FP_connection
            )
        else:
            Ta_C = GEOS5FP_connection.Ta_C(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)
            Ta_C_smooth = Ta_C
            RH = GEOS5FP_connection.RH(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)

        # Sharpen soil moisture if enabled.
        if sharpen_soil_moisture:
            SM = sharpen_soil_moisture_data(
                ST_C=ST_C,
                NDVI=NDVI,
                albedo=albedo,
                water_mask=water_mask,
                geometry=geometry,
                coarse_geometry=coarse_geometry,
                time_UTC=time_UTC,
                date_UTC=date_UTC,
                tile=tile,
                orbit=orbit,
                scene=scene,
                upsampling=upsampling,
                downsampling=downsampling,
                GEOS5FP_connection=GEOS5FP_connection
            )
        else:
            SM = GEOS5FP_connection.SM(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)

        # Calculate Saturated Vapor Pressure (SVP_Pa) and Actual Vapor Pressure (Ea_Pa, Ea_kPa).
        SVP_Pa = 0.6108 * np.exp((17.27 * Ta_C) / (Ta_C + 237.3)) * 1000  # [Pa]
        Ea_Pa = RH * SVP_Pa
        Ea_kPa = Ea_Pa / 1000
        Ta_K = Ta_C + 273.15

        logger.info(f"running Breathing Earth System Simulator for {cl.place(tile)} at {cl.time(time_UTC)} UTC")

        BESS_results = BESS_JPL(
            ST_C=ST_C,
            NDVI=NDVI,
            albedo=albedo,
            elevation_km=elevation_km,
            geometry=geometry,
            time_UTC=time_UTC,
            hour_of_day=hour_of_day,
            day_of_year=day_of_year,
            GEOS5FP_connection=GEOS5FP_connection,
            MODISCI_connection=MODISCI_connection,
            Ta_C=Ta_C,
            RH=RH,
            Rg=SWin_FLiES_ANN,
            VISdiff=VISdiff,
            VISdir=VISdir,
            NIRdiff=NIRdiff,
            NIRdir=NIRdir,
            UV=UV,
            albedo_visible=albedo_visible,
            albedo_NIR=albedo_NIR,
            vapor_gccm=vapor_gccm,
            ozone_cm=ozone_cm,
            KG_climate=KG_climate,
            SZA=SZA,
            GEDI_download_directory=GEDI_directory
        )

        Rn_BESS = BESS_results["Rn"]
        G_BESS = BESS_results["G"]
        check_distribution(Rn_BESS, "Rn_BESS", date_UTC=date_UTC, target=tile)
        
        LE_BESS = BESS_results["LE"]

        ## an need to revise evaporative fraction to take soil heat flux into account
        EF_BESS = rt.where((LE_BESS == 0) | ((Rn_BESS - G_BESS) == 0), 0, LE_BESS / (Rn_BESS - G_BESS))
        
        Rn_daily_BESS = daily_Rn_integration_verma(
            Rn=Rn_BESS,
            hour_of_day=hour_of_day,
            DOY=day_of_year,
            lat=geometry.lat,
        )

        LE_daily_BESS = rt.clip(EF_BESS * Rn_daily_BESS, 0, None)

        if water_mask is not None:
            LE_BESS = rt.where(water_mask, np.nan, LE_BESS)

        check_distribution(LE_BESS, "LE_BESS", date_UTC=date_UTC, target=tile)
        
        GPP_inst_umol_m2_s = BESS_results["GPP"]
        
        if water_mask is not None:
            GPP_inst_umol_m2_s = rt.where(water_mask, np.nan, GPP_inst_umol_m2_s)

        check_distribution(GPP_inst_umol_m2_s, "GPP", date_UTC=date_UTC, target=tile)

        if np.all(np.isnan(GPP_inst_umol_m2_s)):
            raise BlankOutput(f"blank GPP output for orbit {orbit} scene {scene} tile {tile} at {time_UTC} UTC")

        NWP_filenames = sorted([posixpath.basename(filename) for filename in GEOS5FP_connection.filenames])
        AuxiliaryNWP = ",".join(NWP_filenames)
        metadata["ProductMetadata"]["AuxiliaryNWP"] = AuxiliaryNWP

        verma_results = verma_net_radiation(
            SWin=SWin,
            albedo=albedo,
            ST_C=ST_C,
            emissivity=emissivity,
            Ta_C=Ta_C,
            RH=RH
        )

        Rn_verma = verma_results["Rn"]

        if Rn_model_name == "verma":
            Rn = Rn_verma
        elif Rn_model_name == "BESS":
            Rn = Rn_BESS
        else:
            raise ValueError(f"unrecognized net radiation model: {Rn_model_name}")

        if np.all(np.isnan(Rn)) or np.all(Rn == 0):
            raise BlankOutput(f"blank net radiation output for orbit {orbit} scene {scene} tile {tile} at {time_UTC} UTC")

        STIC_results = STIC_JPL(
            geometry=geometry,
            time_UTC=time_UTC,
            Rn_Wm2=Rn,
            RH=RH,
            Ta_C=Ta_C_smooth,
            ST_C=ST_C,
            albedo=albedo,
            emissivity=emissivity,
            NDVI=NDVI,
            max_iterations=3
        )

        LE_STIC = STIC_results["LE"]
        LEt_STIC = STIC_results["LEt"]
        G_STIC = STIC_results["G"]

        STICJPLcanopy = rt.clip(rt.where((LEt_STIC == 0) | (LE_STIC == 0), 0, LEt_STIC / LE_STIC), 0, 1)

        ## FIXME need to revise evaporative fraction to take soil heat flux into account
        EF_STIC = rt.where((LE_STIC == 0) | ((Rn - G_STIC) == 0), 0, LE_STIC / (Rn - G_STIC))

        PTJPLSM_results = PTJPLSM(
            geometry=geometry,
            time_UTC=time_UTC,
            ST_C=ST_C,
            emissivity=emissivity,
            NDVI=NDVI,
            albedo=albedo,
            Rn_Wm2=Rn,
            Ta_C=Ta_C,
            RH=RH,
            soil_moisture=SM,
            field_capacity_directory=soil_grids_directory,
            wilting_point_directory=soil_grids_directory,
            canopy_height_directory=GEDI_directory
        )

        LE_PTJPLSM = rt.clip(PTJPLSM_results["LE"], 0, None)
        G_PTJPLSM = PTJPLSM_results["G"]

        EF_PTJPLSM = rt.where((LE_PTJPLSM == 0) | ((Rn - G_PTJPLSM) == 0), 0, LE_PTJPLSM / (Rn - G_PTJPLSM))

        if np.all(np.isnan(LE_PTJPLSM)):
            raise BlankOutput(
                f"blank PT-JPL-SM instantaneous ET output for orbit {orbit} scene {scene} tile {tile} at {time_UTC} UTC")

        if np.all(np.isnan(LE_PTJPLSM)):
            raise BlankOutput(
                f"blank daily ET output for orbit {orbit} scene {scene} tile {tile} at {time_UTC} UTC")

        LE_canopy_PTJPLSM_Wm2 = rt.clip(PTJPLSM_results["LE_canopy"], 0, None)

        PTJPLSMcanopy = rt.clip(LE_canopy_PTJPLSM_Wm2 / LE_PTJPLSM, 0, 1)

        if water_mask is not None:
            PTJPLSMcanopy = rt.where(water_mask, np.nan, PTJPLSMcanopy)
        
        LE_soil_PTJPLSM = rt.clip(PTJPLSM_results["LE_soil"], 0, None)

        PTJPLSMsoil = rt.clip(LE_soil_PTJPLSM / LE_PTJPLSM, 0, 1)

        if water_mask is not None:
            PTJPLSMsoil = rt.where(water_mask, np.nan, PTJPLSMsoil)
        
        LE_interception_PTJPLSM = rt.clip(PTJPLSM_results["LE_interception"], 0, None)

        PTJPLSMinterception = rt.clip(LE_interception_PTJPLSM / LE_PTJPLSM, 0, 1)

        if water_mask is not None:
            PTJPLSMinterception = rt.where(water_mask, np.nan, PTJPLSMinterception)
        
        PET_PTJPLSM = rt.clip(PTJPLSM_results["PET"], 0, None)

        ESI_PTJPLSM = rt.clip(LE_PTJPLSM / PET_PTJPLSM, 0, 1)

        if water_mask is not None:
            ESI_PTJPLSM = rt.where(water_mask, np.nan, ESI_PTJPLSM)

        if np.all(np.isnan(ESI_PTJPLSM)):
            raise BlankOutput(f"blank ESI output for orbit {orbit} scene {scene} tile {tile} at {time_UTC} UTC")

        PMJPL_results = PMJPL(
            geometry=geometry,
            time_UTC=time_UTC,
            ST_C=ST_C,
            emissivity=emissivity,
            NDVI=NDVI,
            albedo=albedo,
            Ta_C=Ta_C,
            RH=RH,
            elevation_km=elevation_km,
            Rn=Rn,
            GEOS5FP_connection=GEOS5FP_connection,
        )

        LE_PMJPL = PMJPL_results["LE"]
        G_PMJPL = PMJPL_results["G"]

        ETinst = rt.Raster(
            np.nanmedian([np.array(LE_PTJPLSM), np.array(LE_BESS), np.array(LE_PMJPL), np.array(LE_STIC)], axis=0),
            geometry=geometry)

        ## FIXME need to revise evaporative fraction to take soil heat flux into account
        EF_PMJPL = rt.where((LE_PMJPL == 0) | ((Rn - G_PMJPL) == 0), 0, LE_PMJPL / (Rn - G_PMJPL))

        ## FIXME need to revise evaporative fraction to take soil heat flux into account
        EF = rt.where((ETinst == 0) | (Rn == 0), 0, ETinst / Rn)

        SHA = SHA_deg_from_DOY_lat(day_of_year, geometry.lat)
        sunrise_hour = sunrise_from_SHA(SHA)
        daylight_hours = daylight_from_SHA(SHA)

        Rn_daily = daily_Rn_integration_verma(
            Rn=Rn,
            hour_of_day=hour_of_day,
            DOY=day_of_year,
            lat=geometry.lat,
        )

        Rn_daily = rt.clip(Rn_daily, 0, None)
        LE_daily = rt.clip(EF * Rn_daily, 0, None)

        daylight_seconds = daylight_hours * 3600.0

        ET_daily_kg = np.clip(LE_daily * daylight_seconds / LATENT_VAPORIZATION_JOULES_PER_KILOGRAM, 0, None)

        ET_daily_kg_BESS = np.clip(LE_daily_BESS * daylight_seconds / LATENT_VAPORIZATION_JOULES_PER_KILOGRAM, 0, None)
        LE_daily_STIC = rt.clip(EF_STIC * Rn_daily, 0, None)
        ET_daily_kg_STIC = np.clip(LE_daily_STIC * daylight_seconds / LATENT_VAPORIZATION_JOULES_PER_KILOGRAM, 0, None)
        LE_daily_PTJPLSM = rt.clip(EF_PTJPLSM * Rn_daily, 0, None)
        ET_daily_kg_PTJPLSM = np.clip(LE_daily_PTJPLSM * daylight_seconds / LATENT_VAPORIZATION_JOULES_PER_KILOGRAM, 0, None)
        LE_daily_PMJPL = rt.clip(EF_PMJPL * Rn_daily, 0, None)
        ET_daily_kg_PMJPL = np.clip(LE_daily_PMJPL * daylight_seconds / LATENT_VAPORIZATION_JOULES_PER_KILOGRAM, 0, None)

        ETinstUncertainty = rt.Raster(
            np.nanstd([np.array(LE_PTJPLSM), np.array(LE_BESS), np.array(LE_PMJPL), np.array(LE_STIC)], axis=0),
            geometry=geometry).mask(~water_mask)

        GPP_inst_g_m2_s = GPP_inst_umol_m2_s / 1000000 * 12.011
        ETt_inst_kg_m2_s = LE_canopy_PTJPLSM_Wm2 / LATENT_VAPORIZATION_JOULES_PER_KILOGRAM
        WUE = GPP_inst_g_m2_s / ETt_inst_kg_m2_s
        WUE = rt.where(np.isinf(WUE), np.nan, WUE)
        WUE = rt.clip(WUE, 0, 10)

        metadata["StandardMetadata"]["CollectionLabel"] = "ECOv003"

        write_L3T_JET(
            L3T_JET_zip_filename=L3T_JET_zip_filename,
            L3T_JET_browse_filename=L3T_JET_browse_filename,
            L3T_JET_directory=L3T_JET_directory,
            orbit=orbit,
            scene=scene,
            tile=tile,
            time_UTC=time_UTC,
            build=build,
            product_counter=product_counter,
            LE_PTJPLSM=ET_daily_kg_PTJPLSM,
            ET_PTJPLSM=ET_daily_kg_PTJPLSM,
            ET_STICJPL=ET_daily_kg_STIC,
            ET_BESSJPL=ET_daily_kg_BESS,
            ET_PMJPL=ET_daily_kg_PMJPL,
            ET_daily_kg=ET_daily_kg,
            ETinstUncertainty=ETinstUncertainty,
            PTJPLSMcanopy=PTJPLSMcanopy,
            STICJPLcanopy=STICJPLcanopy,
            PTJPLSMsoil=PTJPLSMsoil,
            PTJPLSMinterception=PTJPLSMinterception,
            water_mask=water_mask,
            cloud_mask=cloud_mask,
            metadata=metadata
        )

        write_L3T_ETAUX(
            L3T_ETAUX_zip_filename=L3T_ETAUX_zip_filename,
            L3T_ETAUX_browse_filename=L3T_ETAUX_browse_filename,
            L3T_ETAUX_directory=L3T_ETAUX_directory,
            orbit=orbit,
            scene=scene,
            tile=tile,
            time_UTC=time_UTC,
            build=build,
            product_counter=product_counter,
            Ta_C=Ta_C,
            RH=RH,
            Rn=Rn,
            Rg=SWin,
            SM=SM,
            water_mask=water_mask,
            cloud_mask=cloud_mask,
            metadata=metadata
        )

        write_L4T_ESI(
            L4T_ESI_zip_filename=L4T_ESI_zip_filename,
            L4T_ESI_browse_filename=L4T_ESI_browse_filename,
            L4T_ESI_directory=L4T_ESI_directory,
            orbit=orbit,
            scene=scene,
            tile=tile,
            time_UTC=time_UTC,
            build=build,
            product_counter=product_counter,
            ESI=ESI_PTJPLSM,
            PET=PET_PTJPLSM,
            water_mask=water_mask,
            cloud_mask=cloud_mask,
            metadata=metadata
        )

        write_L4T_WUE(
            L4T_WUE_zip_filename=L4T_WUE_zip_filename,
            L4T_WUE_browse_filename=L4T_WUE_browse_filename,
            L4T_WUE_directory=L4T_WUE_directory,
            orbit=orbit,
            scene=scene,
            tile=tile,
            time_UTC=time_UTC,
            build=build,
            product_counter=product_counter,
            WUE=WUE,
            GPP=GPP_inst_g_m2_s,
            water_mask=water_mask,
            cloud_mask=cloud_mask,
            metadata=metadata
        )

        logger.info(f"finished L3T L4T JET run in {cl.time(timer.tocvalue())} seconds")

    except (BlankOutput, BlankOutputError) as exception:
        logger.exception(exception)
        exit_code = BLANK_OUTPUT

    except (FailedGEOS5FPDownload, ConnectionError, LPDAACServerUnreachable) as exception:
        logger.exception(exception)
        exit_code = AUXILIARY_SERVER_UNREACHABLE

    except ECOSTRESSExitCodeException as exception:
        logger.exception(exception)
        exit_code = exception.exit_code

    return exit_code


def main(argv=sys.argv):
    """
    Main function to parse command line arguments and run the L3T_L4T_JET process.

    Args:
        argv: Command line arguments. Defaults to sys.argv.

    Returns:
        An integer representing the exit code.
    """
    if len(argv) == 1 or "--version" in argv:
        print(f"L3T/L4T JET PGE ({__version__})")
        print(f"usage: ECOv003-L3T-L4T-JET RunConfig.xml")

        if "--version" in argv:
            return SUCCESS_EXIT_CODE
        else:
            return RUNCONFIG_FILENAME_NOT_SUPPLIED

    strip_console = "--strip-console" in argv
    save_intermediate = "--save-intermediate" in argv
    show_distribution = "--show-distribution" in argv
    runconfig_filename = str(argv[1])

    exit_code = L3T_L4T_JET(
        runconfig_filename=runconfig_filename,
        strip_console=strip_console,
        save_intermediate=save_intermediate,
        show_distribution=show_distribution
    )

    logger.info(f"L3T/L4T JET exit code: {exit_code}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main(argv=sys.argv))
