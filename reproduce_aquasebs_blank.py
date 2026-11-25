"""
Download the ECOSTRESS Collection 3 L2T_LSTE granule from the I&T Slack log
(tile=52KBF, orbit=47400, scene=030, acquisition_date=2026-11-14) via ECOv003-CMR,
fetch L2T_STARS from CMR or generate it locally via ECOv003-L2T-STARS, and run
L3T_L4T_JET to reproduce the AquaSEBS BlankOutputError ('variable Tn is a blank image').
"""

from datetime import date, timedelta
import glob
import logging
import os

import numpy as np
import pandas as pd
from ECOv003_CMR import (
    ECOSTRESS_CMR_search,
    download_ECOSTRESS_granule,
    setup_earthdata_session,
)
from ECOv003_granules import L2TLSTE, L2TSTARS
from ECOv003_L3T_L4T_JET import generate_L3T_L4T_JET_runconfig, L3T_L4T_JET

logging.raiseExceptions = False
logging.getLogger().handlers = []

working_directory = os.path.expanduser(os.path.join("~", "data", "ECOv003_52KBF_repro"))
static_directory = os.path.expanduser(os.path.join("~", "data", "L3T_L4T_static"))

tile = "52KBF"
orbit = 47400
scene = 30
acquisition_date = "2026-11-14"


def latest_granule_listing(df: pd.DataFrame, **filters) -> pd.DataFrame:
    """Filter a CMR search DataFrame and keep only the latest build's rows."""
    sub = df.copy()
    for col, val in filters.items():
        sub = sub[sub[col] == val]
    if sub.empty:
        raise FileNotFoundError(f"No matching granules found for filters: {filters}")
    latest_gid = sorted(sub["granule"].unique())[-1]
    return sub[sub["granule"] == latest_gid]


def generate_stars_locally(l2t_lste_filename: str, work_dir: str) -> str:
    """Generate the L2T_STARS granule locally using ECOv003-L2T-STARS."""
    from ECOv003_L2T_STARS import L2T_STARS, generate_L2T_STARS_runconfig

    stars_work_dir = os.path.join(work_dir, "L2T_STARS_work")

    for stale_rc in glob.glob(os.path.join(stars_work_dir, "runconfig", f"ECOv003_L2T_STARS_{tile}_*_*.xml")):
        os.remove(stale_rc)

    stars_runconfig = generate_L2T_STARS_runconfig(
        L2T_LSTE_filename=l2t_lste_filename,
        working_directory=stars_work_dir,
    )
    print(f"Generated L2T_STARS runconfig: {stars_runconfig}")

    stars_exit = L2T_STARS(
        runconfig_filename=stars_runconfig,
        backend="rust",
        num_workers=8,
        overwrite=True,
    )
    if stars_exit != 0:
        raise RuntimeError(f"ECOv003-L2T-STARS failed with exit code {stars_exit}")

    stars_zips = sorted(
        glob.glob(os.path.join(stars_work_dir, "L2T_STARS_output", f"ECOv003_L2T_STARS_{tile}_*.zip"))
    )
    if not stars_zips:
        raise FileNotFoundError(f"No generated ECOv003_L2T_STARS zip found in {stars_work_dir}/L2T_STARS_output")
    return stars_zips[-1]


session = setup_earthdata_session()

# 1. Search and download L2T_LSTE for tile=52KBF, orbit=47400, scene=030
acq_dt = date.fromisoformat(acquisition_date)
lste_listing = ECOSTRESS_CMR_search(
    product="L2T_LSTE",
    tile=tile,
    start_date=acq_dt,
    end_date=acq_dt + timedelta(days=1),
    session=session,
)
lste_granule_df = latest_granule_listing(lste_listing, orbit=orbit, scene=scene)
ts_str = lste_granule_df["granule"].iloc[0].split("_")[6]
lste_acquisition_date = f"{ts_str[:4]}-{ts_str[4:6]}-{ts_str[6:8]}"

L2T_LSTE_granule = download_ECOSTRESS_granule(
    product="L2T_LSTE",
    orbit=orbit,
    scene=scene,
    tile=tile,
    acquisition_date=lste_acquisition_date,
    parent_directory=working_directory,
    CMR_file_listing_df=lste_granule_df,
    session=session,
)
L2T_LSTE_filename = L2T_LSTE_granule.product_filename
print(f"Downloaded L2T_LSTE: {L2T_LSTE_filename}")

# 2. Search CMR for L2T_STARS; if not yet published to CMR, generate it via ECOv003-L2T-STARS
stars_listing = ECOSTRESS_CMR_search(
    product="L2T_STARS",
    tile=tile,
    start_date=acq_dt - timedelta(days=7),
    end_date=acq_dt + timedelta(days=1),
    session=session,
)
stars_tifs = stars_listing[stars_listing["type"] == "GeoTIFF Data"] if not stars_listing.empty else pd.DataFrame()

if not stars_tifs.empty:
    latest_stars_gid = sorted(stars_tifs["granule"].unique())[-1]
    stars_ts = latest_stars_gid.split("_")[4]
    stars_acquisition_date = f"{stars_ts[:4]}-{stars_ts[4:6]}-{stars_ts[6:8]}"
    stars_granule_df = latest_granule_listing(stars_listing, granule=latest_stars_gid)
    L2T_STARS_granule = download_ECOSTRESS_granule(
        product="L2T_STARS",
        tile=tile,
        acquisition_date=stars_acquisition_date,
        parent_directory=working_directory,
        CMR_file_listing_df=stars_granule_df,
        session=session,
    )
    L2T_STARS_filename = L2T_STARS_granule.product_filename
    print(f"Downloaded L2T_STARS from CMR: {L2T_STARS_filename}")
else:
    print(f"No L2T_STARS granule on CMR for {tile} around {acquisition_date}; generating via ECOv003-L2T-STARS...")
    L2T_STARS_filename = generate_stars_locally(
        l2t_lste_filename=L2T_LSTE_filename,
        work_dir=working_directory,
    )
    print(f"Generated L2T_STARS locally: {L2T_STARS_filename}")

# 3. Inspect pixel counts in L2T_LSTE and L2T_STARS
lste_obj = L2TLSTE(L2T_LSTE_filename)
stars_obj = L2TSTARS(L2T_STARS_filename)
st_c = np.asarray(lste_obj.ST_K) - 273.15
water = np.asarray(lste_obj.water)
cloud = np.asarray(lste_obj.cloud)
ndvi = np.asarray(stars_obj.NDVI)

valid_st = np.isfinite(st_c)
print(
    f"\nGranule Pixel Diagnostics ({tile}):\n"
    f"  Total pixels               : {st_c.size}\n"
    f"  Water mask == 1 pixels     : {int(np.sum(water == 1))}\n"
    f"  Cloud mask == 1 pixels     : {int(np.sum(cloud == 1))}\n"
    f"  Valid ST_C pixels          : {int(np.sum(valid_st))}\n"
    f"  Valid NDVI pixels          : {int(np.sum(np.isfinite(ndvi)))}\n"
    f"  Valid LAND pixels          : {int(np.sum((water == 0) & valid_st))}\n"
    f"  Valid UNMASKED WATER pixels: {int(np.sum((water == 1) & valid_st))}\n"
)

# 4. Generate runconfig and run L3T_L4T_JET
runconfig_filename = generate_L3T_L4T_JET_runconfig(
    L2T_LSTE_filename=L2T_LSTE_filename,
    L2T_STARS_filename=L2T_STARS_filename,
    working_directory=working_directory,
    static_directory=static_directory,
)
exit_code = L3T_L4T_JET(
    runconfig_filename=runconfig_filename,
    overwrite=True,
    strip_console=False,
    save_diagnostics=False,
)
print(f"L3T/L4T JET PGE exited with code: {exit_code}")