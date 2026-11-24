# `ECOv003-L3T-L4T-JET` Consolidated Development Plan (`v1.0.1` – `v1.23.0`)

- **Repository:** [`ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET`](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET)
- **Target Release:** `v1.23.0` (branch: `geos5fp_mismatch`)
- **Last Updated:** November 23, 2026
- **Status:** Core fixes implemented and verified end-to-end against public LP DAAC Collection 3 granules (`BuildID 0700`); ready for final CI/Docker smoke testing, release tagging, and `ecostress-level-2-3-4` container deployment.

---

## 1. Executive Summary & Architectural Trajectory

`ECOv003-L3T-L4T-JET` is the Product Generating Executable (PGE) responsible for producing ECOSTRESS Collection 3 Level-3 and Level-4 terrestrial and open-water ecosystem data products (`L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, and `L4T_WUE`). Across 23 releases, the repository has evolved through five distinct architectural phases:

1. **Collection 2 Port & Product Consolidation (`v1.0.1` – `v1.1.0`):** Ported the Collection 2 JET pipeline to Collection 3, extracted inline science sub-modules into standalone pip packages, and consolidated `L3T SEB`, `L3T SM`, and `L3T MET` into a single **`L3T ETAUX`** product.
2. **Ancillary Data Integration & Resilience (`v1.2.0` – `v1.9.0`):** Wired local download directories for static datasets (`GEDI`, `MODISCI`, `MCD12C1`, `SoilGrids`, `SRTM`), aligned XML run-configs (`StaticAncillaryFileGroup`), and wrapped meteorological/soil-moisture downscaling in resilient fallback handlers.
3. **Open-Water Evaporation & SI/Daylight Standardization (`v1.10.0` – `v1.11.0`):** Integrated `AquaSEBS` for open-water latent heat flux, enabled dual-collection (`ECOv002` / `ECOv003`) granule ingestion, standardized internal variables to explicit SI unit suffixes, and added per-model daylight ET and flux-partitioning layers.
4. **Pipeline Modularization & `JET3` Science Extraction (`v1.13.0` – `v1.18.0`):** Decomposed the monolithic PGE script into focused I/O, configuration, and product-writer modules, extracted the core science ensemble into the standalone **`JET3`** package, and established the Collection 3 forward-processing baseline (`BuildID 0700`).
5. **Post-Suomi NPP JPSS Transition, Containerization & Solar Radiation Parity (`v1.19.0` – `v1.23.0`):** Coordinated dependency alignment following the November 2, 2026 decommissioning of Suomi NPP VIIRS (`VNP43NRT` $\rightarrow$ JPSS `VCD43NRT`), introduced a multi-stage `micromamba` + `pip` `Dockerfile` (`linux/amd64`, Python 3.12), hardened `GEOS5FP` SI method and unit-transformation contracts (`GEOS5FP~=2.27.0`, `JET3~=3.3.0`, `BESS-JPL~=1.29.0`), and restored top-level package exports for **`v1.23.0`**.

---

## 2. Operational Context & Cross-Stack Forward-Processing Matrix

In operational production at the NASA JPL ECOSTRESS Science Data System (SDS), `ECOv003-L3T-L4T-JET` is deployed alongside `ECOv003-L2T-STARS` inside a unified `linux/amd64` container image (`artifactory.jpl.nasa.gov:16001/gov/nasa/jpl/ecostress/sds/pge-v3/eco-level-2-3-4-application`, maintained in `ecostress-level-2-3-4`):

- **Algorithmic & Output Consistency Governance:** All Collection 3 output granule filenames carry the static **`BuildID 0700`** (`DEFAULT_BUILD = "0700"`), while exact software provenance is recorded in `StandardMetadata.PGEVersion` inside each granule's `.json` metadata. All maintained PGE updates must produce outputs scientifically consistent with the late-2025 Collection 3 baseline across the mission data record.
- **November 2, 2026 Suomi NPP $\rightarrow$ JPSS Cutover:** Following Suomi NPP VIIRS decommissioning (`VNP43NRT` termination), `ECOv003-L2T-STARS` migrated to JPSS (`VCD43NRT`) inputs and a compiled Rust fusion core (`_stars_rust`), while `ECOv003-L3T-L4T-JET` was co-updated on a unified Python 3.12 + `conda-forge` geospatial toolchain (`GDAL` NetCDF4/HDF5 plugins, `numpy~=2.5.4`, `pandas~=3.1.1`, `rasterio~=1.5.2`, `scikit-learn~=1.9.1`).

| Operational Epoch | Dates | Container Image (`eco-level-2-3-4-application`) | `ECOv003-L3T-L4T-JET` | `JET3` Core Engine | `GEOS5FP` | `ECOv003-L2T-STARS` | Upstream VIIRS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Epoch 1: Initial C3 Deployment** | Nov 2025 – Jan 2026 | `v1.7.0` / `v1.7.1` | `v1.13.0` (`>=1.13.0`) | Inline (`JET.py` in repo) | `~=1.3.0` | `>=1.11.0` | Suomi NPP (`VNP43NRT`) |
| **Epoch 1: C3 Reference Baseline** | Jan 2026 – Nov 2, 2026 | `v1.7.1` (11-month stable run) | `v1.16.0` – `v1.18.0` | `v3.0.0` – `v3.1.0` (extracted Feb 2026) | `~=2.19.0` | `>=1.11.0` – `1.12.1` | Suomi NPP (`VNP43NRT`) |
| **Epoch 2: JPSS Transition & Rust Migration** | Nov 13 – Nov 19, 2026 | `v1.9.0` $\rightarrow$ `v1.13.0` | `v1.20.0` $\rightarrow$ `v1.22.0` | `JET3~=3.0.1` $\rightarrow$ `3.1.0` | `~=2.24.0` | `1.16.0` $\rightarrow$ `1.18.0` (Rust) | JPSS (`VCD43NRT`) |
| **Epoch 2: GEOS-5 FP SI Method Hardening** | Nov 20, 2026 | `v1.13.1` | `v1.22.1` | `JET3~=3.1.1` | `~=2.24.0` | `1.18.0` | JPSS (`VCD43NRT`) |
| **Epoch 2: Solar Radiation & Query Parity** | Nov 23, 2026 | `v1.13.2` *(target)* | **`v1.23.0`** | **`JET3~=3.3.0`** | **`~=2.27.0`** | `1.18.0` | JPSS (`VCD43NRT`) |

---

## 3. Complete Chronological Release History (`Oct 2024 – Nov 2026`)

### Pre-Release Prototype & Collection 2 Duplication (`Oct – Dec 2024`)
- **2024-10-22 (`334153b` – `785b0f2`):** Repository initialized as a YAML run-config prototype (`ECOv001_L4T_JET.py` / `SBGv001_L4T_JET`), renamed the same day to `ECOv001_L3T_JET.py`.
- **2024-10-29 (`9101281` – `4e9fc17`):** Renamed to `ECOv003_L3T_L4T_JET.py` for ECOSTRESS Collection 3 Level 3/4, reverting from YAML back to ECOSTRESS XML run-configs.
- **2024-12-02 (`c3a3a70`):** Duplicated the Collection 2 `ECOv002_L3T_L4T_JET` codebase—initially bundling inline `BESS`, `FLiES`, `FLiESLUT`, `LPDAAC`, `MCD12`, `MOD16`, `PTJPL`, `PTJPLSM`, `SRTM`, `STIC`, and `downscaling` modules prior to externalizing them into pip packages.

### Phase 1: Collection 2 Port & Initial Release (`v1.0.1` – `v1.1.0`, May – June 2025)
- **`v1.0.1` (2025-05-21) — Initial Collection 3 Port:** Replaced inline sub-modules with standalone packages (`BESS-JPL>=1.9.2`, `PM-JPL>=1.4.0`, `STIC-JPL`, `PTJPLSM>=1.2.0`, `FLiESANN`, `FLiESLUT`, `verma-net-radiation`, `ECOv002-granules>=1.1.1`, `ECOv003-granules>=1.3.0`, `NASADEM>=1.2.0`, `rasters>=1.5.0`, `GEOS5FP`); consolidated Collection 2 `L3T SEB`, `L3T SM`, and `L3T MET` into **`L3T ETAUX`** (`Ta`, `RH`, `SM`, `Rg`, `Rn`); and added per-model daily ET layers alongside `ETdaily`.
- **`v1.1.0` (2025-06-24) — Exit Codes & Downscaling Modularization:** Adopted `ECOv003-exit-codes`, removed legacy `SEB`/`SM`/`MET` writer stubs, extracted regression downscaling into `sharpen_meteorology_data.py` and `sharpen_soil_moisture_data.py`, and added `examples/example_L3T_L4T_JET_run_with_download.py`.

### Phase 2: Ancillary Data Wiring & Resilience (`v1.2.0` – `v1.9.0`, July – September 2025)
- **`v1.2.0` – `v1.3.0` (2025-07-01 to 2025-07-03):** Added Python 3.11 support, bumped `BESS-JPL>=1.12.0` for soil heat flux fixes, passed `GEOS5FP_connection` into `FLiESANN`, and reverted XML run-config group naming to `StaticAncillaryFileGroup`.
- **`v1.4.0` – `v1.6.6` (2025-07-03 to 2025-07-30):** Wired `GEDI`, `MODISCI`, and `SoilGrids` download directories into `BESS-JPL` and `PTJPLSM`; updated `verma-net-radiation`; fixed `BlankOutputError` and `AUXILIARY_SERVER_UNREACHABLE` exit code handling; consolidated package versioning via `importlib.metadata`; and passed `GEOS5FP_connection` into `PM-JPL`.
- **`v1.7.0` – `v1.9.0` (2025-08-11 to 2025-09-12):** Wrapped meteorology and soil-moisture sharpening in `try/except` fallback blocks so scenes lacking valid coarse pixels fall back to unsharpened `GEOS5FP` meteorology; standardized on tilde (`~=`) dependency pins; refactored granule ID creation to `ECOv003-granules~=1.7.0` `.generate_granule_name(...)` methods; and masked sharpened meteorology arrays to valid ECOSTRESS LST swath pixels.

### Phase 3: Open-Water Evaporation & SI/Daylight Standardization (`v1.10.0` – `v1.11.0`, October – November 2025)
- **`v1.10.0` (2025-10-01) — `AquaSEBS` & Dual-Collection Support:** Added support for both `ECOv002` and `ECOv003` `L2T_LSTE` / `L2T_STARS` inputs, integrated `AquaSEBS` for open-water evaporation over SRTM/NASADEM water masks, fixed the `L3T_JET` instantaneous `PTJPLSM` layer, and compiled the initial Collection 3 ATBD and User Guide.
- **`v1.11.0` (2025-11-12) — Daylight Upscaling & SI Unit Naming:** Standardized internal variable names to explicit SI unit suffixes (`SZA_deg`, `elevation_m`, `SWin_Wm2`, `LE_*_Wm2`, `Rn_Wm2`), removed `GEOS5FP.SWin` bias correction (`91478687`) so `FLiESANN~=2.1.0` `SWin_Wm2` is used directly, enabled `upscale_to_daylight=True` across all four constituent ET models, aligned `ETdaily` and `ETuncertainty` to $\text{mm day}^{-1}$, added flux partitioning layers (`*canopy`, `*soil`, `*interception`), and added `--overwrite`.

### Phase 4: Modular Architecture, `JET3` Extraction & Collection 3 Baseline (`v1.13.0` – `v1.18.0`, November 2025 – October 2026)
- **`v1.13.0` (2025-11-18):** Decomposed `ECOv003_L3T_L4T_JET.py` into `read_ECOv003_configuration.py`, `read_ECOv003_inputs.py`, `JET.py`, `process_JET_table.py`, and `write_ECOv003_products.py`; entered initial Collection 3 forward processing (`eco-level-2-3-4-application` `v1.7.0` / `v1.7.1`).
- **`v1.14.0` – `v1.16.0` (2026-01-24 to 2026-01-30):** Extracted the core `JET` science engine, `process_JET_table`, sharpening modules, OLS error calibration/UQ, and Cal/Val verification suite into the standalone **`JET3`** package (`v3.0.0`–`v3.1.0`), establishing the reference baseline maintained across the 11-month Suomi NPP operational run.
- **`v1.17.0` – `v1.18.0` (2026-04-29 to 2026-10-12):** Separated PGE and SAS documentation, corrected layer names/sizes and uncertainty timesteps in `README.md` and the User Guide, and fixed comma-delimited `StandardMetadata/InputPointer` formatting.

### Phase 5: JPSS Transition, Containerization & API/Unit Hardening (`v1.19.0` – `v1.23.0`, November 2026)
- **`v1.19.0` – `v1.20.3` (2026-11-11 to 2026-11-17):** Co-aligned Python 3.12/3.13 dependency pins with `ECOv003-L2T-STARS` (`v1.14.0`–`v1.18.0`, JPSS `VCD43NRT` + Rust fusion core).
- **`v1.21.0` – `v1.22.0` (2026-11-19):** Consolidated the PGE entrypoint in `ECOv003_L3T_L4T_JET.py`, replaced manual `sys.argv` parsing with `argparse`, added `--save-diagnostics` and `smoke_test.py` (`ECOv003-L3T-L4T-JET test`), and added the multi-stage `micromamba` + `pip` `Dockerfile` (`linux/amd64`, Python 3.12) with `tests/test_docker_smoke.py`.
- **`v1.22.1` (2026-11-20):** Remediated DAG run `EcostressDAG_Col3.46000.0802.20261116T001911117` failures (Issues `#4` and `#34`) where `JET3 v3.1.0` called deprecated `GEOS5FPConnection.wind_speed()` and `Td_C()` after `GEOS5FP >=2.24.0` standardized on `wind_speed_mps()` and `Td_K()`; bumped `JET3~=3.1.1` and added API contract checks to `smoke_test.py` and `tests/test_docker_smoke.py`.

---

## 4. Consolidated `v1.23.0` Issues Resolved & Verification Results

Following `v1.22.1`, end-to-end validation against public Collection 3 granules (`orbit=44841`, `scene=001`, `tile=11SPS`, `2026-06-02T18:00:12Z`) uncovered and resolved three additional integration defects:

| Issue / Defect | Affected Versions | Root Cause | Resolution Implemented in `v1.23.0` |
| :--- | :--- | :--- | :--- |
| **1. Top-Level Export Shadowing (`TypeError: 'module' object is not callable`)** | `v1.13.0` – `v1.22.1` | `generate_L3T_L4T_JET_runconfig` was extracted into a submodule without being re-exported in `ECOv003_L3T_L4T_JET/__init__.py`. | Re-exported `generate_L3T_L4T_JET_runconfig` in `ECOv003_L3T_L4T_JET/__init__.py` and added callable checks in `tests/test_import_ECOv003_L3T_L4T_JET.py`, `smoke_test.py`, and `tests/test_docker_smoke.py`. |
| **2. `BESS-JPL` / `GEOS5FP` `CO2SC` Raster Query Crash (`ValueError`)** | `<=1.22.1` (`BESS-JPL~=1.28.0` + `GEOS5FP~=2.24.0`) | `BESS_JPL` passed a 1-element list `["CO2SC"]` to `GEOS5FP.query(..., geometry=RasterGrid)`, rejected by `GEOS5FP v2.24.0` as a multi-variable point-only query. | Updated `pyproject.toml` to require **`BESS-JPL~=1.29.0`** and **`GEOS5FP~=2.27.0`**, which resolve single-element list and scalar raster queries cleanly. |
| **3. `GEOS5FP` Gridded Unit Regression (`+74.35 W/m²` `Rg` Bias)** | `v1.22.0` – `v1.22.1` (`GEOS5FP v2.24.0`–`v2.26.0`) | `GEOS5FP v2.24.0`–`v2.26.0` dropped unit scaling on gridded rasters: `vapor_gccm()` returned raw `TQV` in $\text{kg m}^{-2}$ (`10.72`, $10\times$ too high) instead of $\text{g cm}^{-2}$ (`TQV / 10.0`), and `ozone_cm()` returned raw `TO3` in Dobson Units (`334.44`, $1000\times$ too high) instead of $\text{cm}$ (`TO3 / 1000.0`), saturating `FLiES-ANN` inputs. | Updated to **`GEOS5FP~=2.27.0`** and **`JET3~=3.3.0`**; set `BIAS_CORRECT_FLIES_ANN = False` in `ECOv003_L3T_L4T_JET/constants.py` to match the Collection 3 baseline (`BuildID 0700`); and added unit-transformation checks to `smoke_test.py` and `tests/test_docker_smoke.py`. |

### 4.1. End-to-End Granule Validation Results (`orbit=44841`, `scene=001`, `tile=11SPS`, `2026-06-02`)

Re-running `examples/example_L3T_L4T_JET_run_with_download.py` with `ECOv003-L3T-L4T-JET v1.23.0` (`GEOS5FP 2.27.0`, `JET3 3.3.0`, `BESS-JPL 1.29.0`) confirmed full parity across all four Collection 3 products (`AuxiliaryNWP match : True`):

- **`L3T_ETAUX`:** `Ta` (`MATCH`, $r = 1.00000$), `SM` (`MATCH`, $r = 1.00000$), `RH` (`RMSE = 0.00008`, $r = 1.00000$), **`Rg`** (`Mean = 989.80 W/m²` vs. `989.83 W/m²` public, **`Bias = -0.02331 W/m²`**, **`RMSE = 0.52714 W/m²`**, **`r = 0.99859`**), and `Rn` (`Bias = -0.25869 W/m²`, `RMSE = 0.46232 W/m²`, `r = 0.99999`).
- **`L3T_JET`:** `ETdaily` (`Bias = -0.00056 mm/day`, `RMSE = 0.00150 mm/day`, `r = 1.00000`), `ETuncertainty` (`Bias = -0.00064 mm/day`, `RMSE = 0.00192 mm/day`, `r = 0.99996`), and all constituent daily & partitioning layers (`r = 0.99996` – `1.00000`).
- **`L4T_ESI` & `L4T_WUE`:** `GPP` (`MATCH`, `RMSE = 0.00000`, `r = 1.00000`), `ESI` (`RMSE = 0.00003`, `r = 1.00000`), `WUE` (`RMSE = 0.00046`, `r = 1.00000`), and `PET` (`Bias = -0.20329 W/m²`, `RMSE = 0.36346 W/m²`, `r = 0.99999`).

*(Note: Sub-watt/sub-millimeter residuals reflect minor input build differences between `L2T_LSTE` `_05` / `L2T_STARS` `_02` used locally and `_02` / `_01` ingested during forward processing of the public `_02` granules. Operational environment warnings for absent `/root/.netrc` on `daac.ornl.gov` and `urs.earthdata.nasa.gov` remain non-fatal when `L3T_L4T_STATIC` is pre-populated on shared runtime storage.)*

---

## 5. Final Verification & Release Checklist (`v1.23.0`)

- [x] `ECOv003_L3T_L4T_JET/__init__.py` re-exports `generate_L3T_L4T_JET_runconfig`.
- [x] Upstream `BESS-JPL v1.29.0`, `GEOS5FP v2.27.0`, and `JET3 v3.3.0` released on PyPI.
- [x] `pyproject.toml` updated to `1.23.0` with `BESS-JPL~=1.29.0`, `GEOS5FP~=2.27.0`, and `JET3~=3.3.0`.
- [x] `ECOv003_L3T_L4T_JET/constants.py` sets `BIAS_CORRECT_FLIES_ANN = False` and `ZERO_COT_CORRECTION = True`.
- [x] `smoke_test.py` and `tests/test_docker_smoke.py` verify `BIAS_CORRECT_FLIES_ANN is False` and `GEOS5FP` `vapor_gccm` / `ozone_cm` unit transformations.
- [x] End-to-end validation (`examples/example_L3T_L4T_JET_run_with_download.py`) completed with exit code `0` and verified across `L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, and `L4T_WUE`.
- [ ] Run `make test`, `make smoke-test`, `make smoke-test-cli`, and `make docker-smoke-test` (`linux/amd64`).
- [ ] Merge `geos5fp_mismatch` $\rightarrow$ `main`, tag `v1.23.0`, publish to PyPI, and update `ecostress-level-2-3-4` (`ECOv003-L3T-L4T-JET>=1.23.0`) to re-drive failed DAG tiles.