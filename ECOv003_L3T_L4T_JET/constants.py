from os.path import join, dirname, abspath

from FLiESANN import GEOS5FP_INPUTS as FLiESANN_GEOS5FP_INPUTS
from BESS_JPL import GEOS5FP_INPUTS as BESS_JPL_GEOS5FP_INPUTS
from verma_net_radiation import GEOS5FP_INPUTS as VERMA_GEOS5FP_INPUTS
from PTJPLSM import GEOS5FP_INPUTS as PTJPLSM_GEOS5FP_INPUTS
from PMJPL import GEOS5FP_INPUTS as PMJPL_GEOS5FP_INPUTS
from STIC_JPL import GEOS5FP_INPUTS as STIC_JPL_GEOS5FP_INPUTS
from AquaSEBS import GEOS5FP_INPUTS as AquaSEBS_GEOS5FP_INPUTS

from BESS_JPL import BALL_BERRY_INTERCEPT_C4

GEOS5FP_INPUTS = set(FLiESANN_GEOS5FP_INPUTS + BESS_JPL_GEOS5FP_INPUTS + VERMA_GEOS5FP_INPUTS +
                     PTJPLSM_GEOS5FP_INPUTS + PMJPL_GEOS5FP_INPUTS + STIC_JPL_GEOS5FP_INPUTS +
                     AquaSEBS_GEOS5FP_INPUTS)

UPSCALE_TO_DAYLIGHT = True

# constant latent heat of vaporization for water: the number of joules of energy it takes to evaporate one kilogram
LATENT_VAPORIZATION_JOULES_PER_KILOGRAM = 2450000.0

L3T_L4T_JET_TEMPLATE_FILENAME = join(abspath(dirname(__file__)), "L3T_L4T_JET.xml")
DEFAULT_BUILD = "0700"
DEFAULT_OUTPUT_DIRECTORY = "ECOv003_L3T_L4T_JET_output"
DEFAULT_PTJPL_SOURCES_DIRECTORY = "L3T_L4T_JET_sources"
DEFAULT_STATIC_DIRECTORY = "L3T_L4T_static"
DEFAULT_SRTM_DIRECTORY = "SRTM_directory"
DEFAULT_GEDI_DIRECTORY = "GEDI_download"
DEFAULT_MODISCI_DIRECTORY = "MODISCI_download"
DEFAULT_MCD12C1_DIRECTORY = "MCD12C1_download"
DEFAULT_SOIL_GRIDS_DIRECTORY = "SoilGrids_download"
DEFAULT_GEOS5FP_DIRECTORY = "GEOS5FP_download"
DEFULT_DIAGNOSTICS_DIRECTORY = "ECOv003_diagnostics"

L3T_SEB_SHORT_NAME = "ECO_L3T_SEB"
L3T_SEB_LONG_NAME = "ECOSTRESS Tiled Surface Energy Balance Instantaneous L3 Global 70 m"

L3T_SM_SHORT_NAME = "ECO_L3T_SM"
L3T_SM_LONG_NAME = "ECOSTRESS Tiled Downscaled Soil Moisture Instantaneous L3 Global 70 m"

L3T_MET_SHORT_NAME = "ECO_L3T_MET"
L3T_MET_LONG_NAME = "ECOSTRESS Tiled Downscaled Meteorology Instantaneous L3 Global 70 m"

L3T_JET_SHORT_NAME = "ECO_L3T_JET"
L3T_JET_LONG_NAME = "ECOSTRESS Tiled Evapotranspiration Ensemble Instantaneous and Daytime L3 Global 70 m"

L4T_ESI_SHORT_NAME = "ECO_L4T_ESI"
L4T_ESI_LONG_NAME = "ECOSTRESS Tiled Evaporative Stress Index Instantaneous L4 Global 70 m"

L4T_WUE_SHORT_NAME = "ECO_L4T_WUE"
L4T_WUE_LONG_NAME = "ECOSTRESS Tiled Water Use Efficiency Instantaneous L4 Global 70 m"

GEOS_IN_SENTINEL_COARSE_CELL_SIZE = 13720

STRIP_CONSOLE = False
SAVE_INTERMEDIATE = False
SHOW_DISTRIBUTION = True
INCLUDE_SEB_DIAGNOSTICS = False
INCLUDE_JET_DIAGNOSTICS = False
BIAS_CORRECT_FLIES_ANN = True
ZERO_COT_CORRECTION = True
SHARPEN_METEOROLOGY = True
SHARPEN_SOIL_MOISTURE = True

# SWIN_MODEL_NAME = "FLiES-ANN"
SWIN_MODEL_NAME = "GEOS5FP"
RN_MODEL_NAME = "verma"
FLOOR_TOPT = True

SZA_DEGREE_CUTOFF = 90

INPUT_VARIABLES = [
    "AOT",
    "C4_fraction",
    "Ca",
    "CI",
    "COT",
    "IGBP",
    "KG_climate",
    "NDVI",
    "NDVI_maximum",
    "NDVI_minimum",
    "NIR_albedo",
    "PAR_albedo",
    "RH",
    "ST_C",
    "SZA_deg",
    "Ta_C",
    "Tmin_C",
    "Topt_C",
    "albedo",
    "ball_berry_intercept_C3",
    "ball_berry_intercept_C4",
    "ball_berry_slope_C3",
    "ball_berry_slope_C4",
    "canopy_height_meters",
    "canopy_temperature_C",
    "carbon_uptake_efficiency",
    "elevation_m",
    "emissivity",
    "fAPARmax",
    "field_capacity",
    "geometry",
    "kn",
    "ozone_cm",
    "peakVCmax_C3_μmolm2s1",
    "peakVCmax_C4_μmolm2s1",
    "soil_moisture",
    "soil_temperature_C",
    "time_UTC",
    "vapor_gccm",
    "wind_speed_mps",
]
