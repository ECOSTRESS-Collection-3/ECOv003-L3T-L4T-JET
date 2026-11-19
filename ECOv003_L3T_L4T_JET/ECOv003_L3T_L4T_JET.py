import argparse
import logging
import sys
from os import makedirs
from os.path import basename, join

import colored_logging as cl

from GEOS5FP import FailedGEOS5FPDownload
from ECOv003_exit_codes import (
    AUXILIARY_SERVER_UNREACHABLE,
    BLANK_OUTPUT,
    ECOSTRESSExitCodeException,
    RUNCONFIG_FILENAME_NOT_SUPPLIED,
    SUCCESS_EXIT_CODE,
)
from JET3 import BlankOutput, JET

from .constants import (
    DEFAULT_DIAGNOSTICS_DIRECTORY,
    RN_MODEL_NAME,
    SAVE_INTERMEDIATE,
    SHARPEN_METEOROLOGY,
    SHARPEN_SOIL_MOISTURE,
    SHOW_DISTRIBUTION,
    STRIP_CONSOLE,
    ZERO_COT_CORRECTION,
)
from .read_ECOv003_configuration import read_ECOv003_configuration
from .read_ECOv003_inputs import read_ECOv003_inputs
from .smoke_test import test as run_smoke_test
from .version import __version__
from .write_ECOv003_products import write_ECOv003_products

logger = logging.getLogger(__name__)


def L3T_L4T_JET(
        runconfig_filename: str,
        upsampling: str = None,
        downsampling: str = None,
        Rn_model_name: str = RN_MODEL_NAME,
        zero_COT_correction: bool = ZERO_COT_CORRECTION,
        sharpen_meteorology: bool = SHARPEN_METEOROLOGY,
        sharpen_soil_moisture: bool = SHARPEN_SOIL_MOISTURE,
        strip_console: bool = STRIP_CONSOLE,
        save_intermediate: bool = SAVE_INTERMEDIATE,
        show_distribution: bool = SHOW_DISTRIBUTION,
        overwrite: bool = False,
        diagnostics_directory: str = None,
        save_diagnostics: bool = False) -> int:
    """
    Processes ECOSTRESS L2T LSTE and L2T STARS granules to produce L3T and L4T JET products (ECOSTRESS Collection 3).
    """
    exit_code = SUCCESS_EXIT_CODE

    if upsampling is None:
        upsampling = "average"

    if downsampling is None:
        downsampling = "linear"

    if save_intermediate and not save_diagnostics:
        logger.warning("--save-intermediate is deprecated; enabling save_diagnostics")
        save_diagnostics = True

    try:
        config = read_ECOv003_configuration(
            runconfig_filename=runconfig_filename,
            strip_console=strip_console,
            overwrite=overwrite
        )

        if config['should_exit']:
            return config['exit_code']

        runconfig = config['runconfig']
        timer = config['timer']
        working_directory = config['working_directory']
        GEOS5FP_directory = config['GEOS5FP_directory']
        GEDI_directory = config['GEDI_directory']
        MODISCI_directory = config['MODISCI_directory']
        soil_grids_directory = config['soil_grids_directory']
        orbit = config['orbit']
        scene = config['scene']
        tile = config['tile']
        L2T_LSTE_filename = config['L2T_LSTE_filename']
        L2T_LSTE_granule = config['L2T_LSTE_granule']
        L2T_STARS_filename = config['L2T_STARS_filename']
        geometry = config['geometry']
        time_UTC = config['time_UTC']
        date_UTC = config['date_UTC']

        inputs = read_ECOv003_inputs(
            L2T_LSTE_filename=L2T_LSTE_filename,
            L2T_STARS_filename=L2T_STARS_filename,
            orbit=orbit,
            scene=scene,
            tile=tile,
            GEOS5FP_directory=GEOS5FP_directory,
            MODISCI_directory=MODISCI_directory,
            time_UTC=time_UTC,
            date_UTC=date_UTC,
            geometry=geometry,
            zero_COT_correction=zero_COT_correction,
            sharpen_meteorology=sharpen_meteorology,
            sharpen_soil_moisture=sharpen_soil_moisture,
            upsampling=upsampling,
            downsampling=downsampling,
            L2T_LSTE_granule=L2T_LSTE_granule,
        )

        metadata = inputs['metadata']
        ST_C = inputs['ST_C']
        elevation_m = inputs['elevation_m']
        emissivity = inputs['emissivity']
        water_mask = inputs['water_mask']
        cloud_mask = inputs['cloud_mask']
        NDVI = inputs['NDVI']
        albedo = inputs['albedo']
        GEOS5FP_connection = inputs['GEOS5FP_connection']
        MODISCI_connection = inputs['MODISCI_connection']
        SZA_deg = inputs['SZA_deg']
        AOT = inputs['AOT']
        COT = inputs['COT']
        vapor_gccm = inputs['vapor_gccm']
        ozone_cm = inputs['ozone_cm']
        KG_climate = inputs['KG_climate']
        Ta_C = inputs['Ta_C']
        RH = inputs['RH']
        soil_moisture = inputs['SM']

        results = JET(
            ST_C=ST_C,
            NDVI=NDVI,
            emissivity=emissivity,
            albedo=albedo,
            geometry=geometry,
            time_UTC=time_UTC,
            COT=COT,
            AOT=AOT,
            vapor_gccm=vapor_gccm,
            ozone_cm=ozone_cm,
            elevation_m=elevation_m,
            SZA_deg=SZA_deg,
            KG_climate=KG_climate,
            Ta_C=Ta_C,
            RH=RH,
            soil_moisture=soil_moisture,
            water_mask=water_mask,
            Rn_model_name=Rn_model_name,
            GEOS5FP_connection=GEOS5FP_connection,
            MODISCI_connection=MODISCI_connection,
            soil_grids_directory=soil_grids_directory,
            GEDI_directory=GEDI_directory,
            downsampling=downsampling,
        )

        LE_PTJPLSM_Wm2 = results["LE_PTJPLSM_Wm2"]
        ET_daylight_PTJPLSM_kg = results["ET_daylight_PTJPLSM_kg"]
        LE_STIC_Wm2 = results["LE_STIC_Wm2"]
        ET_daylight_STIC_kg = results["ET_daylight_STIC_kg"]
        LE_BESS_Wm2 = results["LE_BESS_Wm2"]
        ET_daylight_BESS_kg = results["ET_daylight_BESS_kg"]
        LE_PMJPL_Wm2 = results["LE_PMJPL_Wm2"]
        ET_daylight_PMJPL_kg = results["ET_daylight_PMJPL_kg"]
        ET_daylight_kg = results["ET_daylight_kg"]
        ET_uncertainty = results["ET_uncertainty"]
        LE_canopy_fraction_PTJPLSM = results["LE_canopy_fraction_PTJPLSM"]
        LE_canopy_fraction_STIC = results["LE_canopy_fraction_STIC"]
        LE_soil_fraction_PTJPLSM = results["LE_soil_fraction_PTJPLSM"]
        LE_interception_fraction_PTJPLSM = results["LE_interception_fraction_PTJPLSM"]
        Rn_Wm2 = results["Rn_Wm2"]
        SWin = results["SWin_Wm2"]
        ESI_PTJPLSM = results["ESI_PTJPLSM"]
        PET_instantaneous_PTJPLSM_Wm2 = results["PET_instantaneous_PTJPLSM_Wm2"]
        WUE = results["WUE"]
        GPP_inst_g_m2_s = results["GPP_inst_g_m2_s"]
        AuxiliaryNWP = results["AuxiliaryNWP"]

        input_pointer = f"{basename(L2T_LSTE_filename)},{basename(L2T_STARS_filename)}"
        metadata["StandardMetadata"]["InputPointer"] = input_pointer
        metadata["StandardMetadata"]["CollectionLabel"] = "ECOv003"
        metadata["ProductMetadata"]["AuxiliaryNWP"] = AuxiliaryNWP

        write_ECOv003_products(
            runconfig=runconfig,
            metadata=metadata,
            LE_PTJPLSM_Wm2=LE_PTJPLSM_Wm2,
            ET_daylight_PTJPLSM_kg=ET_daylight_PTJPLSM_kg,
            LE_STIC_Wm2=LE_STIC_Wm2,
            ET_daylight_STIC_kg=ET_daylight_STIC_kg,
            LE_BESS_Wm2=LE_BESS_Wm2,
            ET_daylight_BESS_kg=ET_daylight_BESS_kg,
            LE_PMJPL_Wm2=LE_PMJPL_Wm2,
            ET_daylight_PMJPL_kg=ET_daylight_PMJPL_kg,
            ET_daylight_kg=ET_daylight_kg,
            ET_uncertainty=ET_uncertainty,
            LE_canopy_fraction_PTJPLSM=LE_canopy_fraction_PTJPLSM,
            LE_canopy_fraction_STIC=LE_canopy_fraction_STIC,
            LE_soil_fraction_PTJPLSM=LE_soil_fraction_PTJPLSM,
            LE_interception_fraction_PTJPLSM=LE_interception_fraction_PTJPLSM,
            water_mask=water_mask,
            cloud_mask=cloud_mask,
            Ta_C=Ta_C,
            RH=RH,
            Rn_Wm2=Rn_Wm2,
            SWin=SWin,
            SM=soil_moisture,
            ESI_PTJPLSM=ESI_PTJPLSM,
            PET_instantaneous_PTJPLSM_Wm2=PET_instantaneous_PTJPLSM_Wm2,
            WUE=WUE,
            GPP_inst_g_m2_s=GPP_inst_g_m2_s
        )

        if save_diagnostics:
            if diagnostics_directory is None:
                diagnostics_directory = join(working_directory, DEFAULT_DIAGNOSTICS_DIRECTORY)

            makedirs(diagnostics_directory, exist_ok=True)
            logger.info(f"saving diagnostic GeoTIFFs to: {cl.dir(diagnostics_directory)}")

            diagnostic_rasters = {**inputs, **results}

            for var_name, data_obj in diagnostic_rasters.items():
                if hasattr(data_obj, 'to_geotiff'):
                    try:
                        tif_filename = join(diagnostics_directory, f"{var_name}.tif")
                        data_obj.to_geotiff(tif_filename)
                        logger.info(f"Saved diagnostic: {cl.file(tif_filename)}")
                    except Exception as e:
                        logger.warning(f"Failed to write diagnostic {var_name} to GeoTIFF: {e}")

        logger.info(f"finished L3T L4T JET run in {cl.time(timer.tocvalue())} seconds")

    except BlankOutput as exception:
        logger.exception(exception)
        exit_code = BLANK_OUTPUT

    except (FailedGEOS5FPDownload, ConnectionError) as exception:
        logger.exception(exception)
        exit_code = AUXILIARY_SERVER_UNREACHABLE

    except ECOSTRESSExitCodeException as exception:
        logger.exception(exception)
        exit_code = exception.exit_code

    return exit_code


def build_parser() -> argparse.ArgumentParser:
    """Builds and returns the argparse parser with sub-commands."""
    parser = argparse.ArgumentParser(
        prog="ECOv003-L3T-L4T-JET",
        description="L3T/L4T JET PGE command-line interface.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit.",
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    # 'test' sub-command
    subparsers.add_parser(
        "test",
        help="Run smoke test suite from .smoke_test",
        description="Execute the test() smoke test routine.",
    )

    # Main processing arguments on root parser
    parser.add_argument(
        "runconfig_filename",
        nargs="?",
        type=str,
        help="Path to XML RunConfig file",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite existing output files if they exist",
    )
    parser.add_argument(
        "--strip-console",
        action="store_true",
        default=STRIP_CONSOLE,
        help="Strip console output from logger",
    )
    parser.add_argument(
        "--save-intermediate",
        action="store_true",
        default=SAVE_INTERMEDIATE,
        help="Deprecated alias for --save-diagnostics",
    )
    parser.add_argument(
        "--show-distribution",
        action="store_true",
        default=SHOW_DISTRIBUTION,
        help="Show distribution plots",
    )
    parser.add_argument(
        "--save-diagnostics",
        action="store_true",
        default=False,
        help="Save output rasters to disk as GeoTIFF files",
    )

    return parser


def main(argv=None):
    """
    Main function to parse command line arguments and execute the selected action.
    """
    if argv is None:
        argv = sys.argv[1:]
    elif len(argv) > 0 and argv[0] == sys.argv[0]:
        argv = argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "test":
        result = run_smoke_test()
        if isinstance(result, int):
            return result
        return SUCCESS_EXIT_CODE if result or result is None else 1

    if not args.runconfig_filename:
        parser.print_usage()
        return RUNCONFIG_FILENAME_NOT_SUPPLIED

    exit_code = L3T_L4T_JET(
        runconfig_filename=args.runconfig_filename,
        strip_console=args.strip_console,
        save_intermediate=args.save_intermediate,
        show_distribution=args.show_distribution,
        overwrite=args.overwrite,
        save_diagnostics=args.save_diagnostics,
    )

    logger.info(f"L3T/L4T JET exit code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
