# ECOSTRESS Level 3 and 4 Evapotranspiration, Evaporative Stress Index, Water Use Efficiency

[![CI](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/actions/workflows/ci.yml/badge.svg)](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/actions/workflows/ci.yml)

This is the main repository for the ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) collection 3 level 3/4 evapotranspiration data products algorithm.

The ECOSTRESS collection 3 level 3/4 evapotranspiration data products algorithm is the pre-cursor to the [Surface Biology and Geology (SBG) collection 1 level 4 evapotranspiration data products algorithm](https://github.com/sbg-tir/SBG-TIR-L4-JET).

[Gregory H. Halverson](https://github.com/gregory-halverson-jpl) (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 321H

[Kerry Cawse-Nicholson](https://github.com/kcawse) (she/her)<br>
[kerry-anne.cawse-nicholson@jpl.nasa.gov](mailto:kerry-anne.cawse-nicholson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 321H

[Madeleine Pascolini-Campbell](https://github.com/madeleinepc) (she/her)<br>
[madeleine.a.pascolini-campbell@jpl.nasa.gov](mailto:madeleine.a.pascolini-campbell@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 321E

### Citing This Package

If you use this software in your research, please cite it using the following BibTeX entry:

```bibtex
@software{halverson_2026_ecov003_l3t_l4t_jet,
  author       = {Halverson, Gregory H. and Cawse-Nicholson, Kerry and Pascolini-Campbell, Madeleine},
  title        = {{ECOv003-L3T-L4T-JET}: {ECOSTRESS} Collection 3 Level 3 and 4 Evapotranspiration ({JET}) Product Generating Executable},
  year         = {2026},
  version      = {1.23.0},
  publisher    = {Zenodo / NASA Jet Propulsion Laboratory},
  url          = {https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET}
}
```

The code for the ECOSTRESS level 3 JET PGE has been developed using open-science practices based on the [ECOSTRESS Collection 2 JET PGE](https://github.com/ECOSTRESS-Collection-2/ECOv002-L3T-L4T-JET) with New Technology Report (NTR) and open-source license from NASA Jet Propulsion Laboratory.

The repositories for the evapotranspiration algorithms are located in the [JPL-Evapotranspiration-Algorithms](https://github.com/JPL-Evapotranspiration-Algorithms) organization.

## 1. Introduction 

This software produces estimates of:
- evapotranspiration (ET)
- evaporative stress index (ESI)
- water use efficiency (WUE)

Evapotranspiration (ET) is one of the main science outputs from the ECOSTRESS mission. ET is a Level-3 (L3) product constructed from a combination of the ECOSTRESS Level-2 (L2) Land Surface Temperature & Emissivity (LSTE) product and auxiliary data sources. Accurate modelling of ET requires consideration of many environmental and biological controls including: solar radiation, the atmospheric water vapor deficit, soil water availability, vegetation physiology and phenology (Brutsaert, 1982; Monteith, 1965; Penman, 1948). Scientists develop models that ingest global satellite observations to capture these environmental and biological controls on ET. LST holds the unique ability to capture when and where plants experience stress, as observed by elevated temperatures which can idenitfy areas that have a reduced capacity to evaporate or transpire water to the atmosphere (Allen et al., 2007). The ECOSTRESS evapotranspiration product combines the [surface temperature and emissivity observations from the ECOSTRESS sensor](https://github.com/ECOSTRESS-Collection-3/ECOv003-L2-LSTE) with the [NDVI and albedo estimated by STARS](https://github.com/ECOSTRESS-Collection-3/ECOv003-L2-STARS), estimates near-surface meteorology by downscaling GEOS-5 FP to these three high resolution images, and runs these variables through a set of surface energy balance models.

The repositories for the evapotranspiration algorithms are located in the [JPL-Evapotranspiration-Algorithms](https://github.com/JPL-Evapotranspiration-Algorithms) organization.

## 2. Data Products 

### 2.1. Metadata

Metadata for the ECOSTRESS Collection 3 tiled products is provided in JSON format:
```json
{
  "StandardMetadata": {
    "AuxiliaryInputPointer": "AuxiliaryNWP",
    "AutomaticQualityFlag": "PASS",
    "AutomaticQualityFlagExplanation": "Image matching performed to correct orbit ephemeris/attitude",
    "BuildID": "0700",
    "CRS": "+proj=utm +zone=11 +datum=WGS84 +units=m +no_defs +type=crs",
    "CampaignShortName": "Primary",
    "CollectionLabel": "ECOv003",
    "DataFormatType": "COG",
    "DayNightFlag": "Day",
    "EastBoundingCoordinate": -114.74406148409601,
    "ImageLineSpacing": 70.0,
    "ImageLines": 1568,
    "ImagePixelSpacing": 70.0,
    "ImagePixels": 1568,
    "InputPointer": "ECOv003_L2T_LSTE_21485_013_11SPS_20220420T211350_0700_01.zip,ECOv003_L2T_STARS_21485_013_11SPS_20220420T211350_0700_01.zip",
    "InstrumentShortName": "ECOSTRESS",
    "LocalGranuleID": "ECOv003_L3T_JET_21485_013_11SPS_20220420T211350_0700_01.zip",
    "LongName": "ECOSTRESS Tiled Evapotranspiration Ensemble Instantaneous and Daytime L3 Global 70 m",
    "NorthBoundingCoordinate": 33.43490918842431,
    "PGEName": "L3T_L4T_JET",
    "PGEVersion": "1.23.0",
    "PlatformLongName": "ISS",
    "PlatformShortName": "ISS",
    "PlatformType": "Spacecraft",
    "ProcessingEnvironment": "Linux eco-p44.tir 3.10.0-1160.45.1.el7.x86_64 #1 SMP Wed Oct 13 17:20:51 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux",
    "ProcessingLevelDescription": "Level 3 Tiled Evapotranspiration Ensemble",
    "ProcessingLevelID": "L3T",
    "ProducerAgency": "JPL",
    "ProducerInstitution": "Caltech",
    "ProductionDateTime": "2022-04-22T10:47:36.452Z",
    "ProductionLocation": "ECOSTRESS Science Computing Facility",
    "RangeBeginningDate": "2022-04-20",
    "RangeBeginningTime": "21:13:51.290937",
    "RangeEndingDate": "2022-04-20",
    "RangeEndingTime": "21:18:51.290937",
    "RegionID": "11SPS",
    "SISName": "Level 3 Product Specification Document",
    "SISVersion": "Preliminary",
    "SceneBoundaryLatLonWKT": "POLYGON ((-118.30553175600564 30.910805591562212, -115.4606649798732 33.891051544444885, -112.80123658401774 31.518067522267156, -115.65618262396845 28.61321628442961, -118.30553175600564 30.910805591562212))",
    "SceneID": "13",
    "ShortName": "ECO_L3T_JET",
    "SouthBoundingCoordinate": 32.42972726825087,
    "StartOrbitNumber": "21485",
    "StopOrbitNumber": "21485",
    "WestBoundingCoordinate": -115.9361545299493
  },
  "ProductMetadata": {
    "BandSpecification": [
      0.0,
      0.0,
      8.779999732971191,
      0.0,
      10.520000457763672,
      12.0
    ],
    "NumberOfBands": 3,
    "OrbitCorrectionPerformed": "True",
    "QAPercentCloudCover": 0.009151460329029571,
    "QAPercentGoodQuality": 98.34781568877551,
    "AuxiliaryNWP": "GEOS.fp.asm.inst3_2d_asm_Nx.20220420_2100.V01.nc4,GEOS.fp.asm.inst3_2d_asm_Nx.20220421_0000.V01.nc4,GEOS.fp.asm.tavg1_2d_lnd_Nx.20220420_2030.V01.nc4,GEOS.fp.asm.tavg1_2d_lnd_Nx.20220420_2130.V01.nc4,GEOS.fp.asm.tavg1_2d_rad_Nx.20220420_2030.V01.nc4,GEOS.fp.asm.tavg1_2d_rad_Nx.20220420_2130.V01.nc4,GEOS.fp.asm.tavg1_2d_slv_Nx.20220420_2030.V01.nc4,GEOS.fp.asm.tavg1_2d_slv_Nx.20220420_2130.V01.nc4,GEOS.fp.asm.tavg3_2d_aer_Nx.20220420_1930.V01.nc4,GEOS.fp.asm.tavg3_2d_aer_Nx.20220420_2230.V01.nc4,GEOS.fp.asm.tavg3_2d_chm_Nx.20220420_1930.V01.nc4,GEOS.fp.asm.tavg3_2d_chm_Nx.20220420_2230.V01.nc4"
  }
}
```

#### 2.1.1. Standard Metadata
Information on the `StandardMetadata` is included on the [ECOSTRESS GitHub landing page](https://github.com/ECOSTRESS-Collection-3)

#### 2.1.2. Product Metadata

| **Name** | **Type** |
| --- | --- |
| BandSpecification | float |
| NumberOfBands | integer |
| OrbitCorrectionPerformed | string |
| QAPercentCloudCover | float |
| QAPercentGoodQuality | float |
| AuxiliaryNWP | string |

*Table 9. Name and type of metadata fields contained in the common ProductMetadata group in each L2T/L3T/L4T product.*

| **Product Long Name** | **Product Short Name** |
| --- | --- |
| STARS NDVI/Albedo | L2T STARS |
| Ecosystem Auxiliary Inputs | L3T ETAUX |
| Evapotranspiration | L3T JET |
| Evaporative Stress Index | L4T ESI |
| Water Use Efficiency | L4T WUE |

*Table 1. Listing of ECOSTRESS ecosystem products long names and short names.*

### 2.2. Quality Flags

Two high-level quality flags are provided in all gridded and tiled products as thematic/binary masks encoded to zero and one in unsigned 8-bit integer layers. The cloud layer represents the final cloud test from L2 CLOUD. The water layer represents the surface water body in the Shuttle Radar Topography Mission (SRTM) Digital Elevation Model. For both layers, zero means absence, and one means presence. Pixels with the value 1 in the cloud layer represent detection of cloud in that pixel. Pixels with the value 1 in the water layer represent open water surface in that pixel. All tiled product data layers written in `float32` contain a standard not-a-number (`NaN`) value at each pixel that could not be retrieved. The cloud and water layers are provided to explain these missing values.

### 2.3. L3T ETAUX Ecosystem Auxiliary Inputs Product

The ECOSTRESS ecosystem processing chain is designed to be independently reproducible. To facilitate open science, the auxiliary data inputs that are produced for evapotranspiration processing are distributed as a data product, such that the end user has the ability to run their own evapotranspiration model using ECOSTRESS data. The data layers of the L3T ETAUX product are described in Table 2.

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** | **Size** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ta | Near-surface air temperature | float32 | Celsius | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| RH | Relative Humidity | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| SM | Soil Moisture | float32 | m³/m³ | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| Rg | Global Radiation | float32 | W/m^2 | NaN | N/A | 0 | N/A | N/A | 9.83 MB |
| Rn | Net Radiation | float32 | W/m^2 | NaN | N/A | 0 | N/A | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

*Table 2. Listing of the L3T ETAUX data layers.*

### 2.4. Downscaled Meteorology & Soil Moisture

Coarse resolution near-surface air temperature (Ta) and relative humidity (RH) are taken from the GEOS-5 FP `tavg1_2d_slv_Nx` product. Ta and RH are down-scaled using a linear regression between up-sampled ST, NDVI, and albedo as predictor variables to Ta or RH from GEOS-5 FP as a response variable, within each Sentinel tile. These regression coefficients are then applied to the 70 m ST, NDVI, and albedo, and this first-pass estimate is then bias-corrected to the coarse image from GEOS-5 FP. These downscaled meteorology estimates are recorded in the L3T ETAUX product listed in Table 2. Areas of cloud are filled in with bilinearly resampled GEOS-5 FP (`downsampling = "linear"`). This same down-scaling procedure is applied to soil moisture (SM) from the GEOS-5 FP `tavg1_2d_lnd_Nx` product, which is recorded in the L3T ETAUX product listed in Table 2.

### 2.5. Surface Energy Balance

The surface energy balance processing for ECOSTRESS begins with an artificial neural network (ANN) implementation of the Forest Light Environmental Simulator (FLiES) radiative transfer algorithm, following the workflow established by Dr. Hideki Kobayashi and Dr. Youngryel Ryu. GEOS-5 FP provides sub-daily Cloud Optical Thickness (COT) in the `tavg1_2d_rad_Nx` product and Aerosol Optical Thickness (AOT) from `tavg3_2d_aer_Nx`. Together with STARS albedo, water vapor (`vapor_gccm` in g cm⁻²), and ozone (`ozone_cm` in cm), these variables are run through the ANN implementation of FLiES to estimate incoming shortwave radiation (`Rg`).

Net radiation (`Rn`) is computed using the Verma net radiation model (`RN_MODEL_NAME = "verma"`) and recorded in the L3T ETAUX product listed in Table 2. The Breathing Earth System Simulator-Jet Propulsion Laboratory (BESS-JPL) algorithm, contributed by Dr. Youngryel Ryu, iteratively calculates ET and Gross Primary Production (GPP) estimates for inclusion in the ensemble and WUE products.

## 3. ECOSTRESS Collection 3 Forward Processing Deployment

In operational production at the NASA JPL ECOSTRESS Science Data System (SDS), `ECOv003-L3T-L4T-JET` is deployed alongside `ECOv003-L2T-STARS` inside a unified `linux/amd64` container image (`artifactory.jpl.nasa.gov:16001/gov/nasa/jpl/ecostress/sds/pge-v3/eco-level-2-3-4-application`, maintained in the [`ecostress-level-2-3-4`](https://github.com/ECOSTRESS-Collection-3/ecostress-level-2-3-4) repository).

### 3.1. Operational Deployment Epochs & Version Matrix

Collection 3 forward processing spans two primary operational baselines:

1. **Epoch 1 — Late-2025 Forward-Processing Baseline (November 2025 – November 2, 2026):**
   - Deployed in late 2025 (`eco-level-2-3-4-application` `v1.7.0` / `v1.7.1`) using Suomi NPP VIIRS (`VNP43NRT`) coarse surface reflectance and albedo inputs in `L2T_STARS`.
   - Under SDS operational requirements, maintained PGEs were held output-consistent with this baseline. Following science model and accuracy validation updates in `ECOv003-L3T-L4T-JET v1.16.0` (January 2026), the forward-processing container operated continuously for **~11 months** without container rebuilds.
2. **Epoch 2 — Post-Suomi NPP Decommissioning JPSS Baseline (November 2026 – Present):**
   - On **November 2, 2026**, Suomi NPP VIIRS was decommissioned, terminating upstream `VNP43NRT` inputs required by `L2T_STARS`.
   - `ECOv003-L2T-STARS` transitioned to JPSS (`VCD43NRT`) coarse inputs (`v1.14.0` → `v1.18.0`, migrating its data-fusion core from Julia to compiled Rust `_stars_rust`), while `ECOv003-L3T-L4T-JET` was co-updated (`v1.19.0` → `v1.23.0`) on a unified Python 3.12 + `conda-forge` geospatial toolchain (`GDAL` NetCDF4/HDF5 plugins, `GEOS5FP~=2.27.0`, `JET3~=3.3.0`, `BESS-JPL~=1.29.0`) to preserve Collection 3 algorithmic consistency.

| Operational Epoch | Dates | Container Image (`eco-level-2-3-4-application`) | `ECOv003-L3T-L4T-JET` | `JET3` Core Engine | `ECOv003-L2T-STARS` | Upstream Coarse VIIRS Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Epoch 1: Initial C3 Deployment** | Nov 2025 – Jan 2026 | `v1.7.0` / `v1.7.1` | `v1.13.0` (`>=1.13.0`) | Inline (`JET.py` in repo) | `>=1.11.0` | Suomi NPP (`VNP43NRT`) |
| **Epoch 1: C3 Reference Baseline** | Jan 2026 – Nov 2, 2026 | `v1.7.1` (11-month stable run) | `v1.16.0` – `v1.18.0` | Extracted to standalone `JET3` | `>=1.11.0` – `1.12.1` | Suomi NPP (`VNP43NRT`) |
| **Epoch 2: JPSS Transition & Rust Migration** | Nov 13 – Nov 19, 2026 | `v1.9.0` → `v1.13.0` | `v1.20.0` → `v1.22.0` | `JET3~=3.0.1` → `3.1.0` | `1.16.0` → `1.18.0` (Rust) | JPSS (`VCD43NRT`) |
| **Epoch 2: GEOS-5 FP & Solar Radiation Parity** | Nov 20 – Nov 23, 2026 | `v1.13.1` → `v1.14.0` | `v1.22.1` → `v1.23.0` | `JET3~=3.1.1` → `3.3.0` | `1.18.0` | JPSS (`VCD43NRT`) |

### 3.2. Container Runtime & Granule Versioning Conventions

* **PGE Entrypoint Wrapper (`/pge/L3T_L4T_JET.sh`):** Inside the production container, SDS invokes `/pge/L3T_L4T_JET.sh <RunConfig.xml>`, which pins `GDAL_DRIVER_PATH="/opt/venv/lib/gdalplugins"`, `GDAL_DATA="/opt/venv/share/gdal"`, and `PROJ_DATA="/opt/venv/share/proj"` (preventing host environment leakage under Apptainer/Singularity) and executes `ECOv003-L3T-L4T-JET "$@" --strip-console`.
* **Product Filename `BuildID` vs. `StandardMetadata.PGEVersion`:** All Collection 3 output granule filenames (e.g., `ECOv003_L3T_JET_21485_013_11SPS_20220420T211350_0700_01.zip`) carry the Collection 3 static **`BuildID` `0700`** (`DEFAULT_BUILD = "0700"`), while the exact semantic version of `ECOv003-L3T-L4T-JET` that produced the granule is recorded inside each granule's `.json` metadata file under `StandardMetadata.PGEVersion`.
* **Automated Deployment Verification:** Both `ECOv003-L3T-L4T-JET test` (CLI smoke test) and `pytest` container smoke tests (`tests/test_docker_smoke.py`) validate Python 3.12 compatibility, ONNX/GDAL/rasterio imports, and the `GEOS5FPConnection` / `JET3` SI-unit and physical unit-transformation contracts (`wind_speed_mps`, `Td_K`, `Ta_C`, `RH`, `SM`, `vapor_gccm`, `ozone_cm`) prior to Artifactory image publication.

## 4. Known Issues & Operational Troubleshooting

The table below tracks known runtime issues affecting `ECOv003-L3T-L4T-JET` and its `JET3` / `BESS-JPL` / `GEOS5FP` science dependencies, identified from forward-processing DAG log triage (`EcostressDAG_Col3.46000.0802.20261116T001911117`) and end-to-end example execution:

| Severity | Log Signature | Affected Versions | Root Cause | Resolution / Operational Guidance |
| :--- | :--- | :--- | :--- | :--- |
| **Degraded Output (`+74.35 W/m²` `Rg` Bias)** | Elevated `L3T_ETAUX` `Rg` (`+74.35 W/m²` bias, $r = 0.389$) propagating into `Rn`, `PET`, and `ETdaily` | `ECOv003-L3T-L4T-JET v1.20.0` – `v1.22.1` with `GEOS5FP v2.24.0` – `v2.26.0` | `GEOS5FPConnection.vapor_gccm()` returned raw `TQV` ($\text{kg m}^{-2}$) without dividing by `10.0` ($\text{g cm}^{-2}$) and `ozone_cm()` returned raw `TO3` ($\text{DU}$) without dividing by `1000.0` ($\text{cm}$) on gridded rasters, saturating `FLiES-ANN` inputs. | **Fixed in `GEOS5FP v2.27.0`, `JET3 v3.3.0`, and `ECOv003-L3T-L4T-JET v1.23.0`** (`GEOS5FP~=2.27.0`, `JET3~=3.3.0`, `BIAS_CORRECT_FLIES_ANN = False`), restoring `Rg` parity (`Bias = -0.023 W/m²`, `r = 0.9986`). |
| **FATAL (`ValueError`)** | `ValueError: Multiple variables can only be queried for point geometries` (`BESS_JPL/retrieve_BESS_JPL_GEOS5FP_inputs.py:189` -> `GEOS5FP/query.py:378`) | `ECOv003-L3T-L4T-JET <=1.22.1` + `BESS-JPL ~=1.28.0` with `GEOS5FP >=2.24.0` | `BESS-JPL` passes a single-element list `["CO2SC"]` to `GEOS5FP_connection.query(..., geometry=RasterGrid)`, which `GEOS5FP >=2.24.0` rejects as a multi-variable point-only query. | **Fixed in `BESS-JPL v1.29.0`, `GEOS5FP >=2.25.0`, and `ECOv003-L3T-L4T-JET v1.23.0`** (`BESS-JPL~=1.29.0`, `GEOS5FP~=2.27.0`). |
| **Bug (`TypeError`)** | `TypeError: 'module' object is not callable` on `from ECOv003_L3T_L4T_JET import generate_L3T_L4T_JET_runconfig` | `ECOv003-L3T-L4T-JET v1.13.0` – `v1.22.1` | `generate_L3T_L4T_JET_runconfig` was extracted into a submodule in `v1.13.0` without being re-exported in `ECOv003_L3T_L4T_JET/__init__.py`, causing top-level imports to resolve to the submodule object. | **Fixed in `v1.23.0`:** Re-exported `generate_L3T_L4T_JET_runconfig` in `ECOv003_L3T_L4T_JET/__init__.py`. |
| **FATAL (`ERROR`)** | `AttributeError: 'GEOS5FPConnection' object has no attribute 'wind_speed'` | `ECOv003-L3T-L4T-JET v1.22.0` + `JET3 v3.1.0` with `GEOS5FP >=2.24.0` | `GEOS5FP >=2.24.0` renamed `.wind_speed(...)` to `.wind_speed_mps(...)`, while `JET3 v3.1.0` (`JET3/JET.py:283`) eagerly called `.wind_speed(...)` when `wind_speed_mps` was omitted. | **Fixed in `JET3 v3.1.1` / `ECOv003-L3T-L4T-JET v1.22.1`** (`JET3~=3.1.1` pinned in `pyproject.toml`, verified by `ECOv003-L3T-L4T-JET test`). |
| **Degraded Output (`ERROR` + `WARNING`)** | `'GEOS5FPConnection' object has no attribute 'Td_C'` followed by `unable to sharpen meteorology` | `ECOv003-L3T-L4T-JET <=1.22.0` + `JET3 <=3.1.0` with `GEOS5FP >=2.24.0` | `JET3/sharpen_meteorology_data.py` called `.Td_C(...)`, removed in `GEOS5FP >=2.24.0` in favor of `.Td_K(...)`. Caught in `read_ECOv003_inputs.py`, silently falling back to unsharpened coarse GEOS-5 FP `Ta_C` and `RH`. | **Fixed in `JET3 v3.1.1` / `ECOv003-L3T-L4T-JET v1.22.1`**, which computes Celsius dew-point temperature via `Td_K(...) - 273.15`. |
| **Non-Fatal (`WARNING`)** | `netrc credentials not found for daac.ornl.gov` / `urs.earthdata.nasa.gov` | All containerized versions | Stateless runtime containers do not ship with `/root/.netrc` credentials for ORNL DAAC or NASA Earthdata Login. | **Benign** when `StaticAncillaryFileGroup/L3T_L4T_STATIC` (`GEDI_download`, `MODISCI_download`, `MCD12C1_download`, `SoilGrids_download`) is pre-populated. Bind-mount a read-only `.netrc` if on-demand static ancillary downloads are required. |
| **Upstream Dependency** | Missing `L2T_STARS` granule due to `GDAL_DRIVER_PATH` / `gdal_HDF5.so` or `VCD43NRT` errors | Upstream `ECOv003-L2T-STARS` | `L3T_L4T_JET` requires `InputFileGroup/L2T_STARS`; upstream `L2T_STARS` failures prevent downstream `L3T_L4T_JET` scheduling in DAG workflows. | Ensure `/pge/L2T_STARS.sh` exports `GDAL_DRIVER_PATH="/opt/venv/lib/gdalplugins"` and runs `ECOv003-L2T-STARS >=1.18.0` before re-driving failed DAG tiles. |

## 5. Release History

The `ECOv003-L3T-L4T-JET` repository evolved from `v1.0.1` (May 2025) through `v1.23.0` (November 2026), transforming from an initial port of the ECOSTRESS Collection 2 evapotranspiration Product Generating Executable (PGE) into a modularized, containerized Collection 3 operational pipeline backed by the standalone `JET3` science library.

### Phase 1: Collection 2 Port & Initial Release (`v1.0.1` – `v1.1.0`, May – June 2025)
* **`v1.0.1` (2025-05-21) — Initial Collection 3 Port:**
  * Duplicated the ECOSTRESS Collection 2 `ECOv002-L3T-L4T-JET` codebase and re-targeted it for Collection 3 (`ECOv003-L3T-L4T-JET v1.0.1`).
  * Replaced inline evapotranspiration sub-modules with standalone pip dependencies: `BESS-JPL>=1.9.2`, `PM-JPL>=1.4.0`, `STIC-JPL`, `PTJPLSM>=1.2.0`, `FLiESANN`, `FLiESLUT`, `verma-net-radiation`, `ECOv002-granules>=1.1.1`, `ECOv003-granules>=1.3.0`, `NASADEM>=1.2.0`, `rasters>=1.5.0`, `GEOS5FP`, `koppengeiger`, `MCD12C1-2019-v006`, `check-distribution`, `colored-logging`, `solar-apparent-time`, and `sun-angles`.
  * Consolidated the three separate Collection 2 auxiliary products (`L3T SEB`, `L3T SM`, and `L3T MET`) into a single unified **`L3T ETAUX`** product (`Ta`, `RH`, `SM`, `Rg`, `Rn`) and switched product serialization to `ECOv003-granules>=1.3.0`.
  * Added individual model daily ET outputs alongside the ensemble daily median (`ETdaily`) and established the `ECOv003-L3T-L4T-JET` CLI entry point.
* **`v1.1.0` (2025-06-24) — Exit Codes & Downscaling Modularization:**
  * Replaced local exit code definitions with the external `ECOv003-exit-codes` package and removed legacy `SEB`/`SM`/`MET` product writer stubs.
  * Extracted meteorological and soil-moisture regression downscaling out of `ECOv003_L3T_L4T_JET.py` into dedicated modules (`sharpen_meteorology_data.py` and `sharpen_soil_moisture_data.py`), introducing direct `GEOS5FP_connection.Td_C(...)` calls.
  * Removed obsolete `downscale_*` helper modules and added a working granule-download example script using `ECOv002-CMR`.

### Phase 2: Ancillary Data Wiring & Resilience (`v1.2.0` – `v1.9.0`, July – September 2025)
* **`v1.2.0` – `v1.2.1` (2025-07-01 to 2025-07-03):** Added Python 3.11 support, bumped `BESS-JPL>=1.12.0` to fix soil heat flux return values (`v1.2.0`), and passed `GEOS5FP_connection` into `FLiESANN` so GEOS-5 FP downloads respected the configured download directory (`v1.2.1`).
* **`v1.3.0` (2025-07-03):** Reverted XML run-config parsing in `L3TL4TJETConfig.py` and `L3T_L4T_JET.xml` from `StaticAuxiliaryFileGroup` back to `StaticAncillaryFileGroup` to match Science Data System (SDS) run-config conventions.
* **`v1.4.0` – `v1.6.1` (2025-07-03 to 2025-07-28):**
  * Wired local download directories for static and ancillary datasets: `GEDI` canopy height into `BESS-JPL>=1.13.0` (`v1.4.0`), `MODISCI` clumping index into `BESS-JPL>=1.15.0` alongside `FLiESLUT>=1.0.3` and Python 3.12 CI support (`v1.5.0`), and `SoilGrids` field capacity/wilting point plus `GEDI` into `PTJPLSM>=1.3.0` (`v1.6.0`).
  * Updated the `verma-net-radiation` function interface and bumped `PM-JPL>=1.4.1` and `PTJPLSM>=1.5.3` (`v1.6.1`).
* **`v1.6.2` – `v1.6.6` (2025-07-28 to 2025-07-30):**
  * Fixed exception catching for `BlankOutputError` from `check-distribution` (`v1.6.2`), corrected `AUXILIARY_SERVER_UNREACHABLE` exit code casing and `daylight_Rn_integration_verma` argument names (`v1.6.3`–`v1.6.4`), consolidated package version resolution to `importlib.metadata` while pinning upper bounds (`BESS-JPL>=1.15.0,<1.16.0`, `ECOv003-granules>=1.5.0,<1.6.0`, `GEOS5FP>=1.2.2,<1.3.0`, `rasters>=1.8.0,<1.9.0`, `verma-net-radiation>=1.3.0,<1.4.0` in `v1.6.5`), and passed `GEOS5FP_connection` into `PM-JPL>=1.4.1,<1.5.0` (`v1.6.6`).
* **`v1.7.0` – `v1.7.4` (2025-08-11 to 2025-09-08):**
  * Wrapped `sharpen_meteorology_data` and `sharpen_soil_moisture_data` in `try/except` fallback blocks (`v1.7.0`, bumping `FLiESANN>=1.6.0,<1.7.0`, `GEOS5FP>=1.2.3,<1.3.0`, `PTJPLSM>=1.7.0,<1.8.0`, and `rasters>=1.9.0,<1.10.0`) so scenes lacking sufficient valid coarse pixels gracefully fall back to unsharpened `GEOS5FP` meteorology instead of crashing.
  * Adopted tilde (`~=`) dependency constraints across `pyproject.toml` and bumped `BESS-JPL~=1.16.0` (`v1.7.1`), removed the deprecated `working_directory` parameter from `GEOS5FP~=1.2.3` with `BESS-JPL~=1.17.0` (`v1.7.2`), bumped `PM-JPL~=1.5.0` and `PTJPLSM~=1.8.0` while removing the direct `sun-angles` pin (`v1.7.3`), and bumped `ECOv003-granules~=1.6.0` (`v1.7.4`).
* **`v1.8.0` – `v1.9.0` (2025-09-11 to 2025-09-12):**
  * Removed remaining legacy `L3T_BESS`/`MET`/`SEB`/`SM` config attributes, refactored granule ID generation to use `ECOv003-granules~=1.7.0` `.generate_granule_name(...)` class methods, and masked sharpened meteorology arrays to valid ECOSTRESS LST swath pixels (`v1.8.0`), followed by `ECOv003-granules~=1.8.0` in `v1.9.0`.

### Phase 3: Open-Water Evaporation & SI/Daylight Standardization (`v1.10.0` – `v1.11.0`, October – November 2025)
* **`v1.10.0` (2025-10-01) — `AquaSEBS` Open-Water Integration & Dual-Collection Support:**
  * Added support for ingesting both `ECOv002` (`ECOv002-granules~=1.2.1`) and `ECOv003` (`ECOv003-granules~=1.10.0`) `L2T_LSTE` and `L2T_STARS` input granules.
  * Integrated `AquaSEBS` to compute open-water latent heat flux over SRTM/NASADEM water-mask pixels, introducing `GEOS5FP_connection.wind_speed(...)`, and added `rasterio`.
  * Fixed the `L3T_JET` instantaneous `PTJPLSM` layer (`LE_PTJPLSM`) and compiled initial Markdown/PDF versions of the Collection 3 ATBD and User Guide.
* **`v1.11.0` (2025-11-12) — Daylight Upscaling & SI Unit Naming:**
  * Standardized internal variable names to explicit SI unit suffixes (`SZA_deg`, `elevation_m`, `SWin_Wm2`, `LE_BESS_Wm2`, `LE_STIC_Wm2`, `LE_PTJPLSM_Wm2`, `LE_PMJPL_Wm2`, `Rn_Wm2`) across updated model interfaces (`AquaSEBS~=1.1.0`, `BESS-JPL~=1.20.0`, `FLiESANN~=2.1.0`, `GEOS5FP~=1.3.0`, `PM-JPL~=1.7.0`, `PTJPLSM~=1.9.0`, `STIC-JPL~=1.4.0`, `verma-net-radiation~=1.8.0`, `rasters~=1.14.0`, `NASADEM~=1.4.0`, `check-distribution~=1.1.0`, and `koppengeiger~=1.1.0`).
  * Switched to raw `FLiESANN~=2.1.0` solar radiation without GEOS-5 FP bias correction (`SWin_Wm2`) and enabled `upscale_to_daylight=True` across all constituent models.
  * Updated `ETdaily` to aggregate the model-specific daylight ET estimates (`ET_daylight_*_kg`), converted `ETuncertainty` to daily units (`mm day⁻¹`), added proportional flux partitioning layers (`LE_canopy_fraction_*`, `LE_soil_fraction_PTJPLSM`, `LE_interception_fraction_PTJPLSM`), and added the `--overwrite` CLI flag.

### Phase 4: Modular Architecture, `JET3` Extraction & Collection 3 Deployment (`v1.13.0` – `v1.18.0`, November 2025 – October 2026)
* **`v1.13.0` (2025-11-18) — Full Pipeline Modularization & Forward-Processing Deployment:**
  * Decomposed `ECOv003_L3T_L4T_JET.py` into focused modules: `read_ECOv003_configuration.py`, `read_ECOv003_inputs.py`, `JET.py`, `process_JET_table.py`, and `write_ECOv003_products.py`.
  * Added tabular/point processing (`process_JET_table`), bundled the ECOSTRESS Collection 2 Cal/Val reference input dataset, and delivered the package into the initial Collection 3 forward-processing container baseline (`ecostress-level-2-3-4 v1.7.0` / `v1.7.1`).
* **`v1.14.0` – `v1.16.0` (2026-01-24 to 2026-01-30) — `JET3` Extraction & Collection 3 Validation:**
  * Extracted the core `JET` science engine, `process_JET_table`, meteorological/soil-moisture sharpening modules, and Cal/Val tables (`ECOv002-calval-tables~=1.13.0`) out of `ECOv003-L3T-L4T-JET` into the standalone **`JET3`** package, leaving `ECOv003-L3T-L4T-JET` as a PGE wrapper around `JET3`.
  * Added performance benchmarking tools (`performance/analyze_table_processing.py`) and updated model dependencies and accuracy assessments for Collection 3 deployment (`v1.16.0`), establishing the reference output baseline maintained through the 11-month Suomi NPP operational run.
* **`v1.17.0` – `v1.18.0` (2026-04-29 to 2026-10-12) — Documentation & Metadata Fixes:**
  * Separated PGE and Science Algorithm Software (SAS) documentation, corrected layer names/sizes and uncertainty timesteps in `README.md` and the User Guide (`v1.17.0`–`v1.17.1`), and fixed `StandardMetadata/InputPointer` formatting (`v1.18.0`) ahead of the `ecostress-level-2-3-4 v1.8.0` container refresh.

### Phase 5: JPSS Transition, Containerization & `GEOS5FP` Remediation (`v1.19.0` – `v1.23.0`, November 2026)
* **`v1.19.0` – `v1.20.3` (2026-11-11 to 2026-11-17) — Coordinated JPSS Transition & Python 3.12/3.13 Alignment:**
  * Following the November 2, 2026 decommissioning of Suomi NPP VIIRS, aligned dependency pins with `ECOv003-L2T-STARS` (`v1.14.0`–`v1.18.0`, transitioning from `VNP43NRT` to JPSS `VCD43NRT`) across Python 3.13 (`v1.19.0`) and Python 3.12 (`v1.20.0`), culminating in `GEOS5FP~=2.24.0`, `JET3~=3.0.1`, `AquaSEBS~=1.3.0`, `BESS-JPL~=1.28.0`, `FLiESANN~=2.13.1`, `PM-JPL~=1.11.0`, `PTJPLSM~=1.10.0`, `STIC-JPL~=1.6.0`, `verma-net-radiation~=1.11.0`, `ECOv003-granules~=1.14.0`, `ECOv003-exit-codes~=1.2.0`, `rasters~=1.21.0`, `numpy~=2.5.4`, `pandas~=3.1.1`, `rasterio~=1.5.2`, `scikit-learn~=1.9.1`, `onnx~=1.23.2`, and `onnxruntime~=1.31.1` (`v1.20.2`–`v1.20.3`) for `ecostress-level-2-3-4 v1.9.0`–`v1.12.0`.
* **`v1.21.0` – `v1.22.0` (2026-11-19) — CLI Refactor & Multi-Stage Docker Runtime:**
  * Replaced manual `sys.argv` parsing with `argparse` (`build_parser`), added `--save-diagnostics` (deprecating `--save-intermediate`), introduced `smoke_test.py` (`ECOv003-L3T-L4T-JET test`), bumped `JET3~=3.1.0`, and added a multi-stage `micromamba` + `pip` `Dockerfile` (`linux/amd64`, Python 3.12) with container smoke tests (`tests/test_docker_smoke.py`), enabling end-to-end CLI smoke testing in `ecostress-level-2-3-4 v1.13.0`.
* **`v1.22.1` (2026-11-20) — `GEOS5FP` API Contract Hardening:**
  * Isolated a regression where `JET3 v3.1.0` eagerly called legacy `GEOS5FP_connection.wind_speed(...)` (carried over from `ECOv003-L3T-L4T-JET v1.10.0`) after `GEOS5FP>=2.24.0` renamed the method to `wind_speed_mps(...)`.
  * Updated `ECOv003-L3T-L4T-JET v1.22.1` `pyproject.toml` to require `JET3~=3.1.1` alongside `GEOS5FP~=2.24.0`, and expanded `smoke_test.py` and `test_docker_smoke.py` to assert `GEOS5FPConnection` SI method availability (`wind_speed_mps`, `Td_K`, `Ta_C`, `RH`, `SM`) and verify `JET3` API compatibility prior to building `ecostress-level-2-3-4 v1.13.1`.
* **`v1.23.0` (2026-11-23) — Solar Radiation Unit Parity, Export Restoration & `CO2SC` Raster Query Fix:**
  * Re-exported `generate_L3T_L4T_JET_runconfig` in `ECOv003_L3T_L4T_JET/__init__.py` so top-level imports resolve to the callable function rather than the submodule.
  * Updated dependencies to `GEOS5FP~=2.27.0`, `JET3~=3.3.0`, and `BESS-JPL~=1.29.0`, resolving both the `BESS-JPL` `CO2SC` raster list query `ValueError` and the `GEOS5FP` `vapor_gccm` (`/10`) and `ozone_cm` (`/1000`) raster unit-conversion regression that had shifted `FLiES-ANN` `Rg` by `+74.35 W/m²`.
  * Retained `BIAS_CORRECT_FLIES_ANN = False` and `ZERO_COT_CORRECTION = True` in `ECOv003_L3T_L4T_JET/constants.py` to preserve strict consistency with the Collection 3 operational baseline (`BuildID 0700`), and added unit-transformation assertions to `smoke_test.py` and `tests/test_docker_smoke.py`.

## 6. Acknowledgements

We thank [Evan Davis](https://github.com/evandjpl) (he/him, [evan.w.davis@jpl.nasa.gov](mailto:evan.w.davis@jpl.nasa.gov)) for assistance with code maintenance and deployment, and [Claire Villanueva-Weeks](https://github.com/clairesvw) (she/her) for assistance with open-source preparation.