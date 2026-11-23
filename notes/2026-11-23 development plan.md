# `ECOv003-L3T-L4T-JET` Comprehensive Development Plan (`v1.0.1` – `v1.23.0`)

- **Repository:** [`ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET`](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET)
- **Current Version:** `v1.22.1` (active branch: `geos5fp_mismatch`)
- **Target Release:** `v1.23.0`
- **Last Updated:** November 23, 2026

---

## 1. Executive Summary & Architectural Trajectory

`ECOv003-L3T-L4T-JET` is the Product Generating Executable (PGE) responsible for producing ECOSTRESS Collection 3 Level-3 and Level-4 terrestrial and open-water ecosystem data products (`L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, and `L4T_WUE`). Across 22+ releases, the repository has evolved through five distinct architectural phases:

1. **Collection 2 Port & Product Consolidation (`v1.0.1` – `v1.1.0`):** Ported the Collection 2 JET pipeline to Collection 3, extracted inline science sub-modules into standalone pip packages, and consolidated `L3T SEB`, `L3T SM`, and `L3T MET` into a single **`L3T ETAUX`** product.
2. **Ancillary Data Integration & Resilience (`v1.2.0` – `v1.9.0`):** Wired local download directories for static datasets (`GEDI`, `MODISCI`, `MCD12C1`, `SoilGrids`, `SRTM`), aligned XML run-configs (`StaticAncillaryFileGroup`), and wrapped meteorological/soil-moisture downscaling in resilient fallback handlers.
3. **Open-Water Evaporation & SI/Daylight Standardization (`v1.10.0` – `v1.11.0`):** Integrated `AquaSEBS` for open-water latent heat flux, enabled dual-collection (`ECOv002` / `ECOv003`) granule ingestion, standardized internal variables to explicit SI unit suffixes, and added per-model daylight ET and flux-partitioning layers.
4. **Pipeline Modularization & `JET3` Science Extraction (`v1.13.0` – `v1.18.0`):** Decomposed the monolithic PGE script into focused I/O, configuration, and product-writer modules, extracted the core science ensemble into the standalone **`JET3`** package, and established the Collection 3 forward-processing baseline (`BuildID` `0700`).
5. **Post-Suomi NPP JPSS Transition, Containerization & API Hardening (`v1.19.0` – `v1.23.0`):** Coordinated dependency alignment following the November 2, 2026 decommissioning of Suomi NPP VIIRS (`VNP43NRT` $\rightarrow$ JPSS `VCD43NRT`), introduced a multi-stage `micromamba` + `pip` `Dockerfile` (`linux/amd64`, Python 3.12), hardened `GEOS5FP >=2.24.0` SI method contracts, and resolved top-level package exports and upstream `BESS-JPL` / `GEOS5FP` grid query defects for **`v1.23.0`**.

---

## 2. Complete Past Development & Release History (`v1.0.1` – `v1.22.1`)

### Pre-Release Prototype & Collection 2 Duplication (`Oct – Dec 2024`)
- **2024-10-22 (`334153b` – `785b0f2`):** Initialized repository as a single-file YAML run-config prototype (`ECOv001_L4T_JET.py` / `SBGv001_L4T_JET`), renamed the same day to `ECOv001_L3T_JET.py` for ECOSTRESS Level 3.
- **2024-10-29 (`9101281` – `4e9fc17`):** Renamed to `ECOv003_L3T_L4T_JET.py` and re-targeted to ECOSTRESS Collection 3 Level 3/4, reverting from YAML back to ECOSTRESS XML run-configs.
- **2024-12-02 (`c3a3a70`):** Duplicated the full Collection 2 `ECOv002_L3T_L4T_JET` codebase—initially bundling inline `BESS`, `FLiES`, `FLiESLUT`, `LPDAAC`, `MCD12`, `MOD16`, `PTJPL`, `PTJPLSM`, `SRTM`, `STIC`, and `downscaling` modules prior to externalizing them into pip packages.

---

### Phase 1: Collection 2 Port & Initial Collection 3 Release (`v1.0.1` – `v1.1.0`, May – June 2025)

#### `v1.0.1` (2025-05-21) — Initial Collection 3 Port
- Re-targeted the Collection 2 JET PGE to Collection 3 (`ECOv003-L3T-L4T-JET v1.0.1`, `requires-python = ">=3.10"`).
- Replaced inline science sub-modules with external pip packages: `BESS-JPL>=1.9.2`, `PM-JPL>=1.4.0`, `STIC-JPL`, `PTJPLSM>=1.2.0`, `FLiESANN`, `FLiESLUT`, `verma-net-radiation`, `ECOv002-granules>=1.1.1`, `ECOv003-granules>=1.3.0`, `NASADEM>=1.2.0`, `rasters>=1.5.0`, `GEOS5FP`, `koppengeiger`, `MCD12C1-2019-v006`, `check-distribution`, `colored-logging`, `solar-apparent-time`, and `sun-angles`.
- Consolidated `L3T SEB`, `L3T SM`, and `L3T MET` into the unified **`L3T ETAUX`** product (`Ta`, `RH`, `SM`, `Rg`, `Rn`) and migrated granule serialization to `ECOv003-granules>=1.3.0`.
- Added per-model daily ET layers alongside `ETdaily` and established the `ECOv003-L3T-L4T-JET` CLI entrypoint.

#### `v1.1.0` (2025-06-24) — Exit Codes & Downscaling Modularization
- Replaced local exit code definitions with `ECOv003-exit-codes` and removed legacy `SEB`/`SM`/`MET` product writer stubs.
- Extracted meteorological and soil-moisture regression downscaling into `sharpen_meteorology_data.py` and `sharpen_soil_moisture_data.py` (introducing `GEOS5FP_connection.Td_C(...)`).
- Removed obsolete `downscale_*` helper modules (`downscale_air_temperature.py`, `downscale_relative_humidity.py`, `downscale_soil_moisture.py`, `downscale_vapor_pressure_deficit.py`) and added `examples/example_L3T_L4T_JET_run_with_download.py`.

---

### Phase 2: Ancillary Data Wiring & Resilience (`v1.2.0` – `v1.9.0`, July – September 2025)

#### `v1.2.0` – `v1.2.1` (2025-07-01 to 2025-07-03)
- **`v1.2.0`:** Added Python 3.11 support and bumped `BESS-JPL>=1.12.0` to fix soil heat flux return values.
- **`v1.2.1`:** Passed `GEOS5FP_connection` into `FLiESANN` so GEOS-5 FP downloads respected the configured `GEOS5FP_download` directory.

#### `v1.3.0` (2025-07-03)
- Reverted XML run-config group naming in `L3TL4TJETConfig.py` and `L3T_L4T_JET.xml` from `StaticAuxiliaryFileGroup` back to `StaticAncillaryFileGroup` to align with ECOSTRESS SDS run-config conventions.

#### `v1.4.0` – `v1.6.1` (2025-07-03 to 2025-07-28)
- **`v1.4.0`:** Wired `GEDI` canopy height download directory into `BESS-JPL>=1.13.0`.
- **`v1.5.0`:** Wired `MODISCI` clumping index download directory into `BESS-JPL>=1.15.0`, updated `FLiESLUT>=1.0.3`, and added Python 3.12 CI testing.
- **`v1.6.0`:** Wired `SoilGrids` (field capacity/wilting point) and `GEDI` directories into `PTJPLSM>=1.3.0`.
- **`v1.6.1`:** Updated the `verma-net-radiation` function call interface and bumped `PM-JPL>=1.4.1` and `PTJPLSM>=1.5.3`.

#### `v1.6.2` – `v1.6.6` (2025-07-28 to 2025-07-30)
- **`v1.6.2`:** Fixed exception handling for `BlankOutputError` from `check-distribution`.
- **`v1.6.3` – `v1.6.4`:** Corrected `AUXILIARY_SERVER_UNREACHABLE` exit code casing and `daylight_Rn_integration_verma` argument names.
- **`v1.6.5`:** Consolidated package version resolution to `importlib.metadata` (`version.py`) and pinned upper bounds (`BESS-JPL>=1.15.0,<1.16.0`, `ECOv003-granules>=1.5.0,<1.6.0`, `GEOS5FP>=1.2.2,<1.3.0`, `rasters>=1.8.0,<1.9.0`, `verma-net-radiation>=1.3.0,<1.4.0`).
- **`v1.6.6`:** Passed `GEOS5FP_connection` into `PM-JPL>=1.4.1,<1.5.0`.

#### `v1.7.0` – `v1.7.4` (2025-08-11 to 2025-09-08)
- **`v1.7.0`:** Wrapped `sharpen_meteorology_data` and `sharpen_soil_moisture_data` in `try/except` fallback blocks so scenes lacking sufficient valid coarse pixels fall back to unsharpened `GEOS5FP` meteorology instead of failing; bumped `FLiESANN>=1.6.0,<1.7.0`, `GEOS5FP>=1.2.3,<1.3.0`, `PTJPLSM>=1.7.0,<1.8.0`, and `rasters>=1.9.0,<1.10.0`.
- **`v1.7.1`:** Standardized `pyproject.toml` on compatible-release (`~=`) specifiers and bumped `BESS-JPL~=1.16.0`.
- **`v1.7.2`:** Removed deprecated `working_directory` parameter from `GEOS5FP~=1.2.3` initialization and bumped `BESS-JPL~=1.17.0`.
- **`v1.7.3`:** Bumped `PM-JPL~=1.5.0` and `PTJPLSM~=1.8.0` and removed direct `sun-angles` pin.
- **`v1.7.4`:** Bumped `ECOv003-granules~=1.6.0`.

#### `v1.8.0` – `v1.9.0` (2025-09-11 to 2025-09-12)
- **`v1.8.0`:** Removed remaining legacy `L3T_BESS`/`MET`/`SEB`/`SM` config attributes, refactored granule ID generation to use `ECOv003-granules~=1.7.0` `.generate_granule_name(...)` class methods, and masked sharpened meteorology arrays to valid ECOSTRESS LST swath pixels.
- **`v1.9.0`:** Bumped `ECOv003-granules~=1.8.0`.

---

### Phase 3: Open-Water Evaporation & SI/Daylight Standardization (`v1.10.0` – `v1.11.0`, October – November 2025)

#### `v1.10.0` (2025-10-01) — `AquaSEBS` Open-Water Integration & Dual-Collection Support
- Added support for ingesting both `ECOv002` (`ECOv002-granules~=1.2.1`) and `ECOv003` (`ECOv003-granules~=1.10.0`) `L2T_LSTE` and `L2T_STARS` granules.
- Integrated `AquaSEBS` for open-water evaporation over SRTM/NASADEM water-mask pixels (introducing `GEOS5FP_connection.wind_speed(...)`) and added `rasterio`.
- Fixed the `L3T_JET` instantaneous `PTJPLSM` layer (`LE_PTJPLSM`) and compiled initial Markdown/PDF versions of the Collection 3 ATBD and User Guide.

#### `v1.11.0` (2025-11-12) — Daylight Upscaling & SI Unit Naming
- Standardized internal variable names to explicit SI unit suffixes (`SZA_deg`, `elevation_m`, `SWin_Wm2`, `LE_BESS_Wm2`, `LE_STIC_Wm2`, `LE_PTJPLSM_Wm2`, `LE_PMJPL_Wm2`, `Rn_Wm2`) across updated model interfaces (`AquaSEBS~=1.1.0`, `BESS-JPL~=1.20.0`, `FLiESANN~=2.1.0`, `GEOS5FP~=1.3.0`, `PM-JPL~=1.7.0`, `PTJPLSM~=1.9.0`, `STIC-JPL~=1.4.0`, `verma-net-radiation~=1.8.0`, `rasters~=1.14.0`, `NASADEM~=1.4.0`, `check-distribution~=1.1.0`, `koppengeiger~=1.1.0`).
- Switched to raw `FLiESANN~=2.1.0` solar radiation without GEOS-5 FP bias correction (`SWin_Wm2`) and enabled `upscale_to_daylight=True` across all constituent models.
- Updated `ETdaily` to aggregate per-model daylight ET estimates (`ET_daylight_*_kg`), converted `ETuncertainty` to daily units ($\text{mm day}^{-1}$), added proportional flux-partitioning layers (`LE_canopy_fraction_*`, `LE_soil_fraction_PTJPLSM`, `LE_interception_fraction_PTJPLSM`), and added `--overwrite`.

---

### Phase 4: Modular Architecture, `JET3` Extraction & Collection 3 Baseline (`v1.13.0` – `v1.18.0`, November 2025 – October 2026)

#### `v1.13.0` (2025-11-18) — Pipeline Modularization & Initial Forward-Processing Deployment
- Decomposed `ECOv003_L3T_L4T_JET.py` into focused modules: `read_ECOv003_configuration.py`, `read_ECOv003_inputs.py`, `JET.py`, `process_JET_table.py`, and `write_ECOv003_products.py`.
- Added tabular/point processing (`process_JET_table`), bundled ECOSTRESS Collection 2 Cal/Val reference tables, and deployed into the initial Collection 3 forward-processing container (`eco-level-2-3-4-application` `v1.7.0` / `v1.7.1`, `ECOv003-L3T-L4T-JET>=1.13.0`).

#### `v1.14.0` – `v1.16.0` (2026-01-24 to 2026-01-30) — `JET3` Science Extraction & Baseline Lock
- Extracted the core `JET` science ensemble, `process_JET_table`, meteorological/soil-moisture sharpening modules, OLS error calibration, and Cal/Val tables (`ECOv002-calval-tables~=1.13.0`) into the standalone **`JET3`** package, leaving `ECOv003-L3T-L4T-JET` as a clean PGE wrapper.
- Added performance benchmarking (`performance/analyze_table_processing.py`) and updated model pins (`AquaSEBS~=1.3.0`, `BESS-JPL~=1.28.0`, `FLiESANN~=2.13.0`, `GEOS5FP~=2.19.0`, `PM-JPL~=1.11.0`, `PTJPLSM~=1.10.0`, `STIC-JPL~=1.6.0`, `verma-net-radiation~=1.11.0` in `v1.16.0`), establishing the reference baseline maintained across the 11-month Suomi NPP operational run.

#### `v1.17.0` – `v1.18.0` (2026-04-29 to 2026-10-12) — Documentation & Metadata Fixes
- **`v1.17.0` – `v1.17.1`:** Separated PGE and Science Algorithm Software (SAS) documentation and corrected layer names, file sizes, and uncertainty timesteps in `README.md` and `ECOv003_L3_L4_JET_User_Guide.md`.
- **`v1.18.0`:** Fixed `StandardMetadata/InputPointer` comma-delimited formatting ahead of the `ecostress-level-2-3-4 v1.8.0` container refresh.

---

### Phase 5: JPSS Transition, Containerization & API Hardening (`v1.19.0` – `v1.22.1`, November 2026)

#### `v1.19.0` – `v1.20.3` (2026-11-11 to 2026-11-17) — Post-Suomi NPP JPSS Alignment
- Following the November 2, 2026 decommissioning of Suomi NPP VIIRS (`VNP43NRT`), co-aligned dependency pins with `ECOv003-L2T-STARS` (`v1.14.0`–`v1.18.0`, JPSS `VCD43NRT` + Rust fusion core) across Python 3.13 (`v1.19.0`) and Python 3.12 (`v1.20.0`), settling on `GEOS5FP~=2.24.0`, `JET3~=3.0.1`, `FLiESANN~=2.13.1`, `ECOv003-granules~=1.14.0`, `ECOv003-exit-codes~=1.2.0`, `rasters~=1.21.0`, `numpy~=2.5.4`, `pandas~=3.1.1`, `rasterio~=1.5.2`, `scikit-learn~=1.9.1`, `onnx~=1.23.2`, and `onnxruntime~=1.31.1` (`v1.20.2`–`v1.20.3`).

#### `v1.21.0` – `v1.22.0` (2026-11-19) — CLI Refactor, Cleanup & Multi-Stage Docker Runtime
- Removed redundant wrapper modules (`PGE.py`, duplicate `exceptions.py`) and consolidated the PGE entrypoint in `ECOv003_L3T_L4T_JET.py`.
- Replaced manual `sys.argv` parsing with `argparse` (`build_parser`), added `--save-diagnostics` (deprecating `--save-intermediate`), introduced `smoke_test.py` (`ECOv003-L3T-L4T-JET test`), bumped `JET3~=3.1.0`, and added a multi-stage `micromamba` + `pip` `Dockerfile` (`linux/amd64`, Python 3.12) with `tests/test_docker_smoke.py`.

#### `v1.22.1` (2026-11-20) — `GEOS5FP` SI Method Contract Hardening
- Diagnosed and remediated DAG failures (`EcostressDAG_Col3.46000.0802.20261116T001911117`) caused by `JET3 v3.1.0` calling legacy `GEOS5FP_connection.wind_speed(...)` and `Td_C(...)` after `GEOS5FP >=2.24.0` standardized on `wind_speed_mps(...)` and `Td_K(...)`.
- Updated `pyproject.toml` to require `JET3~=3.1.1` alongside `GEOS5FP~=2.24.0` and added `GEOS5FPConnection` / `JET3` API contract assertions to `smoke_test.py` and `tests/test_docker_smoke.py`.

---

## 3. Current & Pending Development Plan for `v1.23.0`

During end-to-end validation of `v1.22.1` on branch `geos5fp_mismatch` (running `examples/example_L3T_L4T_JET_run_with_download.py` against orbit `35698`, scene `014`, tile `11SPS`), two additional integration defects were uncovered after `wind_speed_mps`, `Td_K` meteorological sharpening, soil moisture sharpening, and `FLiESANN` executed successfully:

1. **Top-Level Package Export Shadowing (`ECOv003_L3T_L4T_JET/__init__.py`):**
   - `from ECOv003_L3T_L4T_JET import generate_L3T_L4T_JET_runconfig` resolved to the submodule `ECOv003_L3T_L4T_JET.generate_L3T_L4T_JET_runconfig` (`TypeError: 'module' object is not callable`) instead of the function `generate_L3T_L4T_JET_runconfig`.
   - **Status:** Fixed locally in working tree (`ECOv003_L3T_L4T_JET/__init__.py` now explicitly imports `from .generate_L3T_L4T_JET_runconfig import generate_L3T_L4T_JET_runconfig`); needs regression test coverage.
2. **Upstream `BESS-JPL` / `GEOS5FP` Single-Variable List Query Crash (`CO2SC` on `RasterGrid`):**
   - Inside `BESS_JPL/retrieve_BESS_JPL_GEOS5FP_inputs.py:189`, `BESS_JPL` calls `GEOS5FP_connection.query(variables=["CO2SC"], geometry=RasterGrid, ...)` where `variables` is a 1-element `list`.
   - `GEOS5FP/query.py:378` rejects any `list` argument when `geometry` is a raster grid, raising `ValueError: Multiple variables can only be queried for point geometries`.

### 3.1. Workstream Breakdown for `v1.23.0`

#### Workstream A — Public API Exports & Smoke/Unit Test Hardening (`ECOv003-L3T-L4T-JET`)
- [x] **A1. Re-export `generate_L3T_L4T_JET_runconfig` in `ECOv003_L3T_L4T_JET/__init__.py`:**
  - Ensure `from ECOv003_L3T_L4T_JET import generate_L3T_L4T_JET_runconfig` resolves to the callable function rather than the submodule.
- [ ] **A2. Add Top-Level API Export & Run-Config Unit Tests:**
  - Update `tests/test_import_ECOv003_L3T_L4T_JET.py` and `ECOv003_L3T_L4T_JET/smoke_test.py` to assert `callable(ECOv003_L3T_L4T_JET.generate_L3T_L4T_JET_runconfig)` and `callable(ECOv003_L3T_L4T_JET.L3T_L4T_JET)`.
  - Add a fast, offline unit test for `generate_L3T_L4T_JET_runconfig` (using a lightweight mock/fixture granule) to verify XML template substitution (`orbit_number`, `scene_ID`, `tile_ID`, `L2T_LSTE_filename`, `L2T_STARS_filename`, `BuildID`, `ProductCounter`) and round-trip parsing via `L3TL4TJETConfig`.

#### Workstream B — Upstream `BESS-JPL` / `GEOS5FP` `CO2SC` Raster Query Fix
- [ ] **B1. Fix `BESS-JPL` (`retrieve_BESS_JPL_GEOS5FP_inputs.py`):**
  - Update `retrieve_BESS_JPL_GEOS5FP_inputs` so single-variable queries over raster geometries invoke `GEOS5FP_connection.CO2SC(time_UTC=time_UTC, geometry=geometry)` (or pass a scalar variable string to `.query()` rather than a `list` when querying a raster), and cut a patch release of `BESS-JPL` (e.g., `1.28.1` or `1.29.0`).
- [ ] **B2. Harden `GEOS5FP` (`GEOS5FP/query.py`):**
  - Update `GEOS5FPConnection.query()` so passing a 1-element sequence (e.g., `["CO2SC"]`) unwraps to a single-variable query rather than raising `ValueError("Multiple variables can only be queried for point geometries")`, and cut a patch release of `GEOS5FP` (e.g., `2.24.1` or `2.25.0`).
- [ ] **B3. Optional Defensive Pre-Fetch in `JET3` (`JET3/JET.py`):**
  - Evaluate pre-fetching `CO2SC = GEOS5FP_connection.CO2SC(time_UTC=time_UTC, geometry=geometry)` in `JET3` and passing `CO2SC=CO2SC` into `BESS_JPL(...)` so all GEOS-5 FP raster queries are centrally managed with explicit SI-suffixed methods.

#### Workstream C — Dependency Pinning, Smoke Test Expansion & Documentation (`ECOv003-L3T-L4T-JET v1.23.0`)
- [ ] **C1. Update `pyproject.toml` for `v1.23.0`:**
  - Bump `version` from `"1.22.1"` to `"1.23.0"`.
  - Update `BESS-JPL` and `GEOS5FP` (and `JET3`, if updated) version constraints to include the `CO2SC` raster query fix.
- [ ] **C2. Expand `smoke_test.py` & `tests/test_docker_smoke.py`:**
  - Add a mocked raster-query check for `BESS_JPL.retrieve_BESS_JPL_GEOS5FP_inputs` / `GEOS5FPConnection` (`CO2SC` on a `RasterGrid`) so `ECOv003-L3T-L4T-JET test` and `make docker-smoke-test` catch `BESS-JPL` $\leftrightarrow$ `GEOS5FP` query regressions prior to container deployment.
- [ ] **C3. Update Documentation & Known Issues Log:**
  - Update `README.md` (Section 4 Known Issues & Section 5 Release History) and `notes/` with the `v1.23.0` release summary, including the `generate_L3T_L4T_JET_runconfig` export fix and the `BESS-JPL` / `GEOS5FP` `CO2SC` query resolution.

#### Workstream D — End-to-End Verification & Downstream Container Release
- [ ] **D1. Local End-to-End Granule Validation:**
  - Re-run `python examples/example_L3T_L4T_JET_run_with_download.py` to completion and verify all four output product bundles (`L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, `L4T_WUE`), GeoTIFF layers, `.png`/`.jpeg` browse previews, and `.json` metadata (`StandardMetadata.PGEVersion == "1.23.0"`).
- [ ] **D2. Package & Container Smoke Verification:**
  - Run `make test`, `make smoke-test`, `make smoke-test-cli`, and `make docker-smoke-test`.
  - Publish `ECOv003-L3T-L4T-JET v1.23.0` to PyPI and update `ecostress-level-2-3-4` (`ECOv003-L3T-L4T-JET>=1.23.0`) for forward-processing deployment.

---

## 4. Verification & Release Checklist (`v1.23.0`)

- [x] `ECOv003_L3T_L4T_JET/__init__.py` re-exports `generate_L3T_L4T_JET_runconfig`.
- [ ] Upstream `BESS-JPL` and/or `GEOS5FP` fix released for single-variable list queries (`["CO2SC"]`) on `RasterGrid`.
- [ ] `pyproject.toml` bumped to `1.23.0` with updated `BESS-JPL` / `GEOS5FP` constraints.
- [ ] `smoke_test.py` and `tests/test_docker_smoke.py` include `generate_L3T_L4T_JET_runconfig` and `BESS-JPL` / `GEOS5FP` contract assertions.
- [ ] `examples/example_L3T_L4T_JET_run_with_download.py` completes with exit code `0` and generates valid `L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, and `L4T_WUE` granules.
- [ ] `make test` and `make docker-smoke-test` pass cleanly on `linux/amd64`.
- [ ] Git tag `v1.23.0` created and pushed; GitHub release published; `ecostress-level-2-3-4` container updated.