"""
Module for reading and processing ECOv003 L3T/L4T JET run configuration.

This module contains the read_ECOv003_configuration function which loads the run configuration,
extracts all necessary paths and parameters, and performs initial validation checks.
"""

import logging
from datetime import datetime
from os.path import exists, join

import colored_logging as cl
from ECOv003_exit_codes import SUCCESS_EXIT_CODE
from JET3.exceptions import InputFilesInaccessible
from pytictoc import TicToc

from .L3TL4TJETConfig import L3TL4TJETConfig

logger = logging.getLogger(__name__)


def _wrap_resilient_flush(handler: logging.Handler) -> logging.Handler:
    """Prevent transient stream/filesystem flush timeouts from printing logging tracebacks."""
    orig_flush = handler.flush

    def safe_flush():
        try:
            orig_flush()
        except OSError:
            pass

    handler.flush = safe_flush
    return handler


def configure_pge_logging(log_filename: str, strip_console: bool = False) -> None:
    """Configure colored_logging cleanly without duplicate root handlers or flush tracebacks."""
    logging.raiseExceptions = False
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass

    cl.configure(filename=log_filename, strip_console=strip_console)

    for handler in root_logger.handlers:
        _wrap_resilient_flush(handler)


def read_ECOv003_configuration(
        runconfig_filename: str,
        strip_console: bool = False,
        overwrite: bool = False) -> dict:
    """
    Read and process ECOv003 L3T/L4T JET run configuration.
    """
    runconfig = L3TL4TJETConfig(runconfig_filename)
    working_directory = runconfig.working_directory
    granule_ID = runconfig.granule_ID
    log_filename = join(working_directory, "log", f"{granule_ID}.log")

    configure_pge_logging(log_filename=log_filename, strip_console=strip_console)

    timer = TicToc()
    timer.tic()

    logger.info(f"started L3T L4T JET run at {cl.time(datetime.utcnow())} UTC")
    logger.info(f"L3T_L4T_JET PGE ({cl.val(runconfig.PGE_version)})")
    logger.info(f"L3T_L4T_JET run-config: {cl.file(runconfig_filename)}")

    # L3T JET configuration
    L3T_JET_granule_ID = runconfig.L3T_JET_granule_ID
    logger.info(f"L3T JET granule ID: {cl.val(L3T_JET_granule_ID)}")
    L3T_JET_directory = runconfig.L3T_JET_directory
    logger.info(f"L3T JET granule directory: {cl.dir(L3T_JET_directory)}")
    L3T_JET_zip_filename = runconfig.L3T_JET_zip_filename
    logger.info(f"L3T JET zip file: {cl.file(L3T_JET_zip_filename)}")
    L3T_JET_browse_filename = runconfig.L3T_JET_browse_filename
    logger.info(f"L3T JET preview: {cl.file(L3T_JET_browse_filename)}")

    # L3T ETAUX configuration
    L3T_ETAUX_directory = runconfig.L3T_ETAUX_directory
    logger.info(f"L3T ETAUX granule directory: {cl.dir(L3T_ETAUX_directory)}")
    L3T_ETAUX_zip_filename = runconfig.L3T_ETAUX_zip_filename
    logger.info(f"L3T ETAUX zip file: {cl.file(L3T_ETAUX_zip_filename)}")
    L3T_ETAUX_browse_filename = runconfig.L3T_ETAUX_browse_filename
    logger.info(f"L3T ETAUX preview: {cl.file(L3T_ETAUX_browse_filename)}")

    # L4T ESI configuration
    L4T_ESI_granule_ID = runconfig.L4T_ESI_granule_ID
    logger.info(f"L4T ESI PT-JPL granule ID: {cl.val(L4T_ESI_granule_ID)}")
    L4T_ESI_directory = runconfig.L4T_ESI_directory
    logger.info(f"L4T ESI PT-JPL granule directory: {cl.dir(L4T_ESI_directory)}")
    L4T_ESI_zip_filename = runconfig.L4T_ESI_zip_filename
    logger.info(f"L4T ESI PT-JPL zip file: {cl.file(L4T_ESI_zip_filename)}")
    L4T_ESI_browse_filename = runconfig.L4T_ESI_browse_filename
    logger.info(f"L4T ESI PT-JPL preview: {cl.file(L4T_ESI_browse_filename)}")

    # L4T WUE configuration
    L4T_WUE_granule_ID = runconfig.L4T_WUE_granule_ID
    logger.info(f"L4T WUE granule ID: {cl.val(L4T_WUE_granule_ID)}")
    L4T_WUE_directory = runconfig.L4T_WUE_directory
    logger.info(f"L4T WUE granule directory: {cl.dir(L4T_WUE_directory)}")
    L4T_WUE_zip_filename = runconfig.L4T_WUE_zip_filename
    logger.info(f"L4T WUE zip file: {cl.file(L4T_WUE_zip_filename)}")
    L4T_WUE_browse_filename = runconfig.L4T_WUE_browse_filename
    logger.info(f"L4T WUE preview: {cl.file(L4T_WUE_browse_filename)}")

    # Check if output files already exist
    required_files = [
        L3T_JET_zip_filename,
        L3T_JET_browse_filename,
        L3T_ETAUX_zip_filename,
        L3T_ETAUX_browse_filename,
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

    should_exit = False
    exit_code = SUCCESS_EXIT_CODE

    if not some_files_missing and not overwrite:
        logger.info("L3T_L4T_JET output already found (use --overwrite flag to regenerate)")
        should_exit = True
    elif not some_files_missing and overwrite:
        logger.info("L3T_L4T_JET output already found but overwrite flag is set, proceeding with processing")

    # Directory configuration
    logger.info(f"working_directory: {cl.dir(working_directory)}")
    output_directory = runconfig.output_directory
    logger.info(f"output directory: {cl.dir(output_directory)}")
    sources_directory = runconfig.sources_directory
    logger.info(f"sources directory: {cl.dir(sources_directory)}")
    GEOS5FP_directory = runconfig.GEOS5FP_directory
    logger.info(f"GEOS-5 FP directory: {cl.dir(GEOS5FP_directory)}")
    static_directory = runconfig.static_directory
    logger.info(f"static directory: {cl.dir(static_directory)}")
    SRTM_directory = runconfig.SRTM_directory
    logger.info(f"SRTM directory: {cl.dir(SRTM_directory)}")
    GEDI_directory = runconfig.GEDI_directory
    logger.info(f"GEDI directory: {cl.dir(GEDI_directory)}")
    MODISCI_directory = runconfig.MODISCI_directory
    logger.info(f"MODIS CI directory: {cl.dir(MODISCI_directory)}")
    MCD12_directory = runconfig.MCD12_directory
    logger.info(f"MCD12C1 IGBP directory: {cl.dir(MCD12_directory)}")
    soil_grids_directory = runconfig.soil_grids_directory
    logger.info(f"SoilGrids directory: {cl.dir(soil_grids_directory)}")
    logger.info(f"log: {cl.file(log_filename)}")

    # Granule parameters
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

    # Input files
    L2T_LSTE_filename = runconfig.L2T_LSTE_filename
    logger.info(f"L2T_LSTE file: {cl.file(L2T_LSTE_filename)}")
    L2T_STARS_filename = runconfig.L2T_STARS_filename
    logger.info(f"L2T_STARS file: {cl.file(L2T_STARS_filename)}")

    if not exists(L2T_LSTE_filename):
        raise InputFilesInaccessible(f"L2T LSTE file does not exist: {L2T_LSTE_filename}")

    # Reuse already-loaded L2T LSTE granule from runconfig
    L2T_LSTE_granule = runconfig.L2T_LSTE_granule
    geometry = L2T_LSTE_granule.geometry
    time_UTC = L2T_LSTE_granule.time_UTC
    logger.info(f"overpass time: {cl.time(time_UTC)} UTC")
    date_UTC = time_UTC.date()
    logger.info(f"overpass date: {cl.time(date_UTC)} UTC")
    timestamp = f"{time_UTC:%Y%m%dT%H%M%S}"

    return {
        'runconfig': runconfig,
        'timer': timer,
        'working_directory': working_directory,
        'granule_ID': granule_ID,
        'log_filename': log_filename,
        'L3T_JET_granule_ID': L3T_JET_granule_ID,
        'L3T_JET_directory': L3T_JET_directory,
        'L3T_JET_zip_filename': L3T_JET_zip_filename,
        'L3T_JET_browse_filename': L3T_JET_browse_filename,
        'L3T_ETAUX_directory': L3T_ETAUX_directory,
        'L3T_ETAUX_zip_filename': L3T_ETAUX_zip_filename,
        'L3T_ETAUX_browse_filename': L3T_ETAUX_browse_filename,
        'L4T_ESI_granule_ID': L4T_ESI_granule_ID,
        'L4T_ESI_directory': L4T_ESI_directory,
        'L4T_ESI_zip_filename': L4T_ESI_zip_filename,
        'L4T_ESI_browse_filename': L4T_ESI_browse_filename,
        'L4T_WUE_granule_ID': L4T_WUE_granule_ID,
        'L4T_WUE_directory': L4T_WUE_directory,
        'L4T_WUE_zip_filename': L4T_WUE_zip_filename,
        'L4T_WUE_browse_filename': L4T_WUE_browse_filename,
        'output_directory': output_directory,
        'sources_directory': sources_directory,
        'GEOS5FP_directory': GEOS5FP_directory,
        'static_directory': static_directory,
        'SRTM_directory': SRTM_directory,
        'GEDI_directory': GEDI_directory,
        'MODISCI_directory': MODISCI_directory,
        'MCD12_directory': MCD12_directory,
        'soil_grids_directory': soil_grids_directory,
        'orbit': orbit,
        'scene': scene,
        'tile': tile,
        'build': build,
        'product_counter': product_counter,
        'L2T_LSTE_filename': L2T_LSTE_filename,
        'L2T_STARS_filename': L2T_STARS_filename,
        'L2T_LSTE_granule': L2T_LSTE_granule,
        'geometry': geometry,
        'time_UTC': time_UTC,
        'date_UTC': date_UTC,
        'timestamp': timestamp,
        'should_exit': should_exit,
        'exit_code': exit_code
    }
