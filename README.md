# ECOSTRESS Level 3 and 4 Evapotranspiration, Evaporative Stress Index, Water Use Efficiency

[![CI](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/actions/workflows/ci.yml/badge.svg)](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/actions/workflows/ci.yml)

This is the main repository for the ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) collection 3 level 3/4 evapotranspiration data products algorithm.

The ECOSTRESS collection 3 level 3/4 evapotranspiration data products algorithm is the pre-cursor to the [Surface Biology and Geology (SBG) collection 1 level 4 evapotranspiration data products algorithm](https://github.com/sbg-tir/SBG-TIR-L4-JET).

[Gregory H. Halverson](https://github.com/gregory-halverson-jpl) (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G

[Kerry Cawse-Nicholson](https://github.com/kcawse) (she/her)<br>
[kerry-anne.cawse-nicholson@jpl.nasa.gov](mailto:kerry-anne.cawse-nicholson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G

[Madeleine Pascolini-Campbell](https://github.com/madeleinepc) (she/her)<br>
[madeleine.a.pascolini-campbell@jpl.nasa.gov](mailto:madeleine.a.pascolini-campbell@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329F

[Evan Davis](https://github.com/evandjpl) (he/him)<br>
[evan.w.davis@jpl.nasa.gov](mailto:evan.w.davis@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 397K

[Claire Villanueva-Weeks](https://github.com/clairesvw) (she/her)<br>
NASA Jet Propulsion Laboratory 329G

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
    "PGEVersion": "1.20.3",
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

The surface energy balance processing for ECOSTRESS begins with an artificial neural network (ANN) implementation of the Forest Light Environmental Simulator (FLiES) radiative transfer algorithm, following the workflow established by Dr. Hideki Kobayashi and Dr. Youngryel Ryu. GEOS-5 FP provides sub-daily Cloud Optical Thickness (COT) in the `tavg1_2d_rad_Nx` product and Aerosol Optical Thickness (AOT) from `tavg3_2d_aer_Nx`. Together with STARS albedo, these variables are run through the ANN implementation of FLiES to estimate incoming shortwave radiation (Rg), bias-corrected to Rg from the GEOS-5 FP `tavg1_2d_rad_Nx` product.

Net radiation (`Rn`) is computed using the Verma net radiation model (`RN_MODEL_NAME = "verma"`) and recorded in the L3T ETAUX product listed in Table 2. The Breathing Earth System Simulator-Jet Propulsion Laboratory (BESS-JPL) algorithm, contributed by Dr. Youngryel Ryu, iteratively calculates ET and Gross Primary Production (GPP) estimates for inclusion in the ensemble and WUE products.

## 3. Release History & Collection 3 Forward-Processing Timeline

The `ECOv003-L3T-L4T-JET` repository evolved from `v1.0.1` (May 2025) through `v1.22.1` (November 2026), transforming from an initial port of the ECOSTRESS Collection 2 evapotranspiration Product Generating Executable (PGE) into a modularized, containerized Collection 3 operational pipeline backed by the standalone `JET3` science library.

### Operational Context: Collection 3 Deployment & the Suomi NPP → JPSS Transition

The release cadence of `ECOv003-L3T-L4T-JET` directly reflects the operational lifecycle of the ECOSTRESS Collection 3 forward-processing system (`ecostress-level-2-3-4`):

1. **Late-2025 Forward-Processing Baseline (`v1.13.0` – `v1.16.0`):**
   * In late 2025, ECOSTRESS Collection 3 entered operational forward processing (`ecostress-level-2-3-4 v1.7.0` / `v1.7.1`, pairing `ECOv003-L3T-L4T-JET>=1.13.0` with `ECOv003-L2T-STARS>=1.11.0`).
   * Operational requirements mandated that maintained PGEs remain output-consistent with that late-2025 baseline. Following validation updates in `v1.16.0` (January 2026), the production baseline ran stably for nearly 11 months without requiring container rebuilds—explaining why `ECOv003-L3T-L4T-JET` saw only documentation and metadata updates (`v1.17.0`–`v1.18.0`) between February and October 2026.
2. **Suomi NPP VIIRS Decommissioning & JPSS Transition (`v1.19.0` – `v1.22.1`, November 2026):**
   * On **November 2, 2026**, Suomi NPP VIIRS was decommissioned, cutting off upstream `VNP43NRT` coarse surface reflectance and albedo inputs required by `L2T_STARS`.
   * Transitioning `ECOv003-L2T-STARS` to JPSS (`VCD43NRT`) inputs (`v1.14.0` → `v1.18.0`) while preserving Collection 3 algorithmic consistency required rebuilding the shared `ecostress-level-2-3-4` application container around Python 3.12 and a `conda-forge` geospatial/scientific toolchain (`v1.9.0` → `v1.13.0`).
   * `ECOv003-L3T-L4T-JET` was aligned in lockstep across `v1.19.0`–`v1.22.1` so both PGEs share compatible dependency pins (`GEOS5FP~=2.24.0`, `JET3~=3.1.1`, `numpy~=2.5.4`, `pandas~=3.1.1`, `rasterio~=1.5.2`) and automated container smoke tests inside `ecostress-level-2-3-4`.

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

### Phase 5: JPSS Transition, Containerization & `GEOS5FP` Remediation (`v1.19.0` – `v1.22.1`, November 2026)
* **`v1.19.0` – `v1.20.3` (2026-11-11 to 2026-11-17) — Coordinated JPSS Transition & Python 3.12/3.13 Alignment:**
  * Following the November 2, 2026 decommissioning of Suomi NPP VIIRS, aligned dependency pins with `ECOv003-L2T-STARS` (`v1.14.0`–`v1.18.0`, transitioning from `VNP43NRT` to JPSS `VCD43NRT`) across Python 3.13 (`v1.19.0`) and Python 3.12 (`v1.20.0`), culminating in `GEOS5FP~=2.24.0`, `JET3~=3.0.1`, `AquaSEBS~=1.3.0`, `BESS-JPL~=1.28.0`, `FLiESANN~=2.13.1`, `PM-JPL~=1.11.0`, `PTJPLSM~=1.10.0`, `STIC-JPL~=1.6.0`, `verma-net-radiation~=1.11.0`, `ECOv003-granules~=1.14.0`, `ECOv003-exit-codes~=1.2.0`, `rasters~=1.21.0`, `numpy~=2.5.4`, `pandas~=3.1.1`, `rasterio~=1.5.2`, `scikit-learn~=1.9.1`, `onnx~=1.23.2`, and `onnxruntime~=1.31.1` (`v1.20.2`–`v1.20.3`) for `ecostress-level-2-3-4 v1.9.0`–`v1.12.0`.
* **`v1.21.0` – `v1.22.0` (2026-11-19) — CLI Refactor & Multi-Stage Docker Runtime:**
  * Replaced manual `sys.argv` parsing with `argparse` (`build_parser`), added `--save-diagnostics` (deprecating `--save-intermediate`), introduced `smoke_test.py` (`ECOv003-L3T-L4T-JET test`), bumped `JET3~=3.1.0`, and added a multi-stage `micromamba` + `pip` `Dockerfile` (`linux/amd64`, Python 3.12) with container smoke tests (`tests/test_docker_smoke.py`), enabling end-to-end CLI smoke testing in `ecostress-level-2-3-4 v1.13.0`.
* **`v1.22.1` (In Progress on `geos5fp_mismatch`, 2026-11-20) — `GEOS5FP` API Contract Hardening:**
  * Isolated a regression where `JET3 v3.1.0` eagerly called legacy `GEOS5FP_connection.wind_speed(...)` (carried over from `ECOv003-L3T-L4T-JET v1.10.0`) after `GEOS5FP>=2.24.0` renamed the method to `wind_speed_mps(...)`.
  * Updated `ECOv003-L3T-L4T-JET v1.22.1` `pyproject.toml` to require `JET3~=3.1.1` alongside `GEOS5FP~=2.24.0`, and expanded `smoke_test.py` and `test_docker_smoke.py` to assert `GEOS5FPConnection` SI method availability (`wind_speed_mps`, `Td_K`, `Ta_C`, `RH`, `SM`) and verify `JET3` API compatibility prior to building `ecostress-level-2-3-4 v1.13.1`.