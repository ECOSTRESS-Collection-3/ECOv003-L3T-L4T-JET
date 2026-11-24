"""
Example script for downloading ECOSTRESS Collection 3 granules via ECOv003-CMR,
running the L3T/L4T JET Product Generating Executable (PGE), and comparing every
generated L3T and L4T product layer (L3T_JET, L3T_ETAUX, L4T_ESI, L4T_WUE)
against the existing public Collection 3 reference products.

Requirements:
- ECOv003-CMR package
- ECOv003-granules package
- ECOv003-L3T-L4T-JET package

Update the working and static directory paths as needed for your environment.
"""

from datetime import date, timedelta
import glob
import json
import logging
import os
import zipfile

import numpy as np
import pandas as pd
import rasters as rt
from ECOv003_CMR import (
    ECOSTRESS_CMR_search,
    download_ECOSTRESS_granule,
    setup_earthdata_session,
)
from ECOv003_L3T_L4T_JET import generate_L3T_L4T_JET_runconfig, L3T_L4T_JET

# Prevent transient stream flush timeouts from emitting logging tracebacks
logging.raiseExceptions = False
logging.getLogger().handlers = []

# Set the working, static, and reference directories
working_directory = os.path.expanduser(os.path.join("~", "data", "ECOv003_example"))
static_directory = os.path.expanduser(os.path.join("~", "data", "L3T_L4T_static"))
reference_directory = os.path.join(working_directory, "reference_products")
output_directory = os.path.join(working_directory, "ECOv003_L3T_L4T_JET_output")

tile = "11SPS"
search_start_date = "2026-06-01"
search_end_date = "2026-10-31"
output_products = ["L3T_JET", "L3T_ETAUX", "L4T_ESI", "L4T_WUE"]


def latest_granule_listing(df: pd.DataFrame, **filters) -> pd.DataFrame:
    """Filter a CMR search DataFrame and keep only the latest build's rows."""
    sub = df.copy()
    for col, val in filters.items():
        sub = sub[sub[col] == val]
    if sub.empty:
        raise FileNotFoundError(f"No matching granules found for filters: {filters}")
    latest_gid = sorted(sub["granule"].unique())[-1]
    return sub[sub["granule"] == latest_gid]


def read_granule_layers(product_path: str) -> dict[str, np.ndarray]:
    """Read all GeoTIFF layers from a granule directory or .zip archive."""
    layers = {}
    if zipfile.is_zipfile(product_path):
        with zipfile.ZipFile(product_path, "r") as zf:
            for member in sorted(zf.namelist()):
                if member.endswith(".tif"):
                    layer_name = os.path.splitext(os.path.basename(member))[0].split("_")[-1]
                    layers[layer_name] = np.asarray(
                        rt.Raster.open(f"zip://{product_path}!{member}"),
                        dtype=np.float64,
                    )
    elif os.path.isdir(product_path):
        for filename in sorted(os.listdir(product_path)):
            if filename.endswith(".tif"):
                layer_name = os.path.splitext(filename)[0].split("_")[-1]
                layers[layer_name] = np.asarray(
                    rt.Raster.open(os.path.join(product_path, filename)),
                    dtype=np.float64,
                )
    else:
        raise ValueError(f"Unsupported granule location: {product_path}")
    return layers


def read_granule_metadata(product_path: str) -> dict:
    """Read the JSON sidecar metadata from a granule directory or .zip archive."""
    if zipfile.is_zipfile(product_path):
        with zipfile.ZipFile(product_path, "r") as zf:
            for member in sorted(zf.namelist()):
                if member.endswith(".json"):
                    return json.loads(zf.read(member).decode("utf-8"))
    elif os.path.isdir(product_path):
        for filename in sorted(os.listdir(product_path)):
            if filename.endswith(".json"):
                with open(os.path.join(product_path, filename), "r", encoding="utf-8") as f:
                    return json.load(f)
    return {}


def compare_product_layers(product: str, local_path: str, public_path: str) -> None:
    """Print a layer-by-layer numerical comparison table between local and public granules."""
    print(
        f"\n{'=' * 109}\n"
        f"Product: {product}\n"
        f"  Local : {local_path}\n"
        f"  Public: {public_path}\n"
        f"{'=' * 109}"
    )

    local_meta = read_granule_metadata(local_path)
    public_meta = read_granule_metadata(public_path)
    if local_meta and public_meta:
        loc_ip = local_meta.get("StandardMetadata", {}).get("InputPointer", "")
        pub_ip = public_meta.get("StandardMetadata", {}).get("InputPointer", "")
        loc_nwp = local_meta.get("ProductMetadata", {}).get("AuxiliaryNWP", "")
        pub_nwp = public_meta.get("ProductMetadata", {}).get("AuxiliaryNWP", "")
        print(f"  InputPointer match : {loc_ip == pub_ip} (local={loc_ip} | public={pub_ip})")
        print(f"  AuxiliaryNWP match : {loc_nwp == pub_nwp}\n")

    local_layers = read_granule_layers(local_path)
    public_layers = read_granule_layers(public_path)
    all_layers = sorted(set(local_layers) | set(public_layers))

    header = (
        f"{'Layer':<22} {'Status':<12} {'RMSE':>10} {'MAE':>10} "
        f"{'Bias':>10} {'MaxDiff':>10} {'r':>8} {'LocalNaN%':>10} {'PubNaN%':>9}"
    )
    print(header)
    print("-" * len(header))

    for layer in all_layers:
        if layer not in local_layers:
            print(f"{layer:<22} {'MISSING_LOC':<12}")
            continue
        if layer not in public_layers:
            print(f"{layer:<22} {'MISSING_PUB':<12}")
            continue

        loc = local_layers[layer]
        pub = public_layers[layer]
        loc_nan_pct = 100.0 * np.isnan(loc).mean()
        pub_nan_pct = 100.0 * np.isnan(pub).mean()

        if loc.shape != pub.shape:
            print(f"{layer:<22} {'SHAPE_DIFF':<12} {str(loc.shape)} vs {str(pub.shape)}")
            continue

        valid = np.isfinite(loc) & np.isfinite(pub)
        if not np.any(valid):
            status = "ALL_NAN" if np.all(np.isnan(loc)) and np.all(np.isnan(pub)) else "NAN_MISMATCH"
            print(
                f"{layer:<22} {status:<12} {'-':>10} {'-':>10} {'-':>10} {'-':>10} "
                f"{'-':>8} {loc_nan_pct:>9.2f}% {pub_nan_pct:>8.2f}%"
            )
            continue

        diff = loc[valid] - pub[valid]
        rmse = float(np.sqrt(np.mean(diff ** 2)))
        mae = float(np.mean(np.abs(diff)))
        bias = float(np.mean(diff))
        max_diff = float(np.max(np.abs(diff)))

        if np.std(loc[valid]) > 0 and np.std(pub[valid]) > 0:
            corr = float(np.corrcoef(loc[valid], pub[valid])[0, 1])
        else:
            corr = 1.0 if max_diff == 0.0 else np.nan

        is_close = np.allclose(loc, pub, rtol=1e-4, atol=1e-5, equal_nan=True)
        status = "MATCH" if is_close else "DIFF"

        print(
            f"{layer:<22} {status:<12} {rmse:>10.5f} {mae:>10.5f} "
            f"{bias:>10.5f} {max_diff:>10.5f} {corr:>8.5f} {loc_nan_pct:>9.2f}% {pub_nan_pct:>8.2f}%"
        )


# Set up an authenticated NASA Earthdata session (reused across all searches and downloads)
session = setup_earthdata_session()

# Discover an overpass on the target tile that has L2T_LSTE, a recent L2T_STARS prior,
# and all four public L3T/L4T output products (L3T_JET, L3T_ETAUX, L4T_ESI, L4T_WUE)
product_listings = {}
for prod in ["L2T_LSTE"] + output_products:
    listing = ECOSTRESS_CMR_search(
        product=prod,
        tile=tile,
        start_date=search_start_date,
        end_date=search_end_date,
        session=session,
    )
    if listing.empty:
        raise FileNotFoundError(
            f"No public Collection 3 {prod} granules found for tile {tile} "
            f"between {search_start_date} and {search_end_date}."
        )
    product_listings[prod] = listing

common_overpasses = None
for prod, listing in product_listings.items():
    overpasses = {
        (int(r.orbit), int(r.scene))
        for r in listing[listing["type"] == "GeoTIFF Data"].itertuples()
    }
    common_overpasses = overpasses if common_overpasses is None else (common_overpasses & overpasses)

if not common_overpasses:
    raise FileNotFoundError(
        f"No common overpass across {['L2T_LSTE'] + output_products} found for tile {tile} "
        f"between {search_start_date} and {search_end_date}."
    )

orbit, scene = sorted(common_overpasses)[0]
jet_granule_df = latest_granule_listing(product_listings["L3T_JET"], orbit=orbit, scene=scene)
ts_str = jet_granule_df["granule"].iloc[0].split("_")[6]  # YYYYMMDDTHHMMSS
acquisition_date = f"{ts_str[:4]}-{ts_str[4:6]}-{ts_str[6:8]}"
acq_dt = date.fromisoformat(acquisition_date)

stars_listing = ECOSTRESS_CMR_search(
    product="L2T_STARS",
    tile=tile,
    start_date=acq_dt - timedelta(days=7),
    end_date=acq_dt,
    session=session,
)
stars_tifs = stars_listing[stars_listing["type"] == "GeoTIFF Data"] if not stars_listing.empty else pd.DataFrame()
if stars_tifs.empty:
    raise FileNotFoundError(
        f"No L2T_STARS prior found for tile {tile} within 7 days prior to {acquisition_date}."
    )

latest_stars_gid = sorted(stars_tifs["granule"].unique())[-1]
stars_ts = latest_stars_gid.split("_")[4]  # YYYYMMDD
stars_acquisition_date = f"{stars_ts[:4]}-{stars_ts[4:6]}-{stars_ts[6:8]}"

lste_granule_df = latest_granule_listing(product_listings["L2T_LSTE"], orbit=orbit, scene=scene)
stars_granule_df = latest_granule_listing(stars_listing, granule=latest_stars_gid)

print(
    f"Selected Collection 3 overpass: tile={tile}, orbit={orbit}, scene={scene}, "
    f"LSTE/JET date={acquisition_date}, STARS prior date={stars_acquisition_date}\n"
    f"  L2T_LSTE : {lste_granule_df['granule'].iloc[0]}\n"
    f"  L2T_STARS: {stars_granule_df['granule'].iloc[0]}"
)
for prod in output_products:
    prod_df = latest_granule_listing(product_listings[prod], orbit=orbit, scene=scene)
    print(f"  {prod:<9}: {prod_df['granule'].iloc[0]}")

# 1. Download the Collection 3 L2T_LSTE and L2T_STARS input granules
L2T_LSTE_granule = download_ECOSTRESS_granule(
    product="L2T_LSTE",
    orbit=orbit,
    scene=scene,
    tile=tile,
    acquisition_date=acquisition_date,
    parent_directory=working_directory,
    CMR_file_listing_df=lste_granule_df,
    session=session,
)

L2T_STARS_granule = download_ECOSTRESS_granule(
    product="L2T_STARS",
    tile=tile,
    acquisition_date=stars_acquisition_date,
    parent_directory=working_directory,
    CMR_file_listing_df=stars_granule_df,
    session=session,
)

# 2. Download all existing public Collection 3 L3T and L4T reference granules
reference_granules = {}
for prod in output_products:
    prod_df = latest_granule_listing(product_listings[prod], orbit=orbit, scene=scene)
    ref_granule = download_ECOSTRESS_granule(
        product=prod,
        orbit=orbit,
        scene=scene,
        tile=tile,
        acquisition_date=acquisition_date,
        parent_directory=os.path.join(reference_directory, prod),
        CMR_file_listing_df=prod_df,
        session=session,
    )
    reference_granules[prod] = ref_granule
    print(f"Downloaded public reference {prod}: {ref_granule.product_filename}")

# 3. Generate the XML run configuration file for the L3T/L4T JET PGE
runconfig_filename = generate_L3T_L4T_JET_runconfig(
    L2T_LSTE_filename=L2T_LSTE_granule.product_filename,
    L2T_STARS_filename=L2T_STARS_granule.product_filename,
    working_directory=working_directory,
    static_directory=static_directory,
)
print(f"Run configuration file generated: {runconfig_filename}")

with open(runconfig_filename, "r") as f:
    print(f.read())

# 4. Run the L3T/L4T JET PGE using the generated configuration file
exit_code = L3T_L4T_JET(runconfig_filename=runconfig_filename, overwrite=True, save_diagnostics=False)
print(f"L3T/L4T JET PGE exited with code: {exit_code}")

if exit_code != 0:
    raise RuntimeError(f"L3T_L4T_JET failed with exit code {exit_code}")

# 5. Compare every layer across L3T_JET, L3T_ETAUX, L4T_ESI, and L4T_WUE
for prod in output_products:
    local_matches = sorted(
        glob.glob(os.path.join(output_directory, f"ECOv003_{prod}_{orbit:05d}_{scene:03d}_{tile}_*.zip"))
    )
    if not local_matches:
        raise FileNotFoundError(f"No generated {prod} zip found in {output_directory}")

    compare_product_layers(
        product=prod,
        local_path=local_matches[-1],
        public_path=reference_granules[prod].product_filename,
    )