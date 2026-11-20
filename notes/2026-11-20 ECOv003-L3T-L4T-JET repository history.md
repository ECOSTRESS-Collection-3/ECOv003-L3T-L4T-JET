# `ECOv003-L3T-L4T-JET` Repository History (`v1.0.1` – `v1.22.1`)

The `ECOv003-L3T-L4T-JET` repository evolved from `v1.0.1` (May 2025) through `v1.22.1` (November 2026), transforming from an initial port of the ECOSTRESS Collection 2 evapotranspiration Product Generating Executable (PGE) into a modularized, containerized Collection 3 operational pipeline backed by the standalone `JET3` science library.

---

## Operational Context: Collection 3 Deployment & the Suomi NPP → JPSS Transition

The release cadence of `ECOv003-L3T-L4T-JET` directly reflects the operational lifecycle of the ECOSTRESS Collection 3 forward-processing system (`ecostress-level-2-3-4`):

1. **Late-2025 Forward-Processing Baseline (`v1.13.0` – `v1.16.0`):**
   * In late 2025, ECOSTRESS Collection 3 entered operational forward processing (`ecostress-level-2-3-4 v1.7.0` / `v1.7.1`, pairing `ECOv003-L3T-L4T-JET>=1.13.0` with `ECOv003-L2T-STARS>=1.11.0`).
   * Operational requirements mandated that maintained PGEs remain output-consistent with that late-2025 baseline. Following validation updates in `v1.16.0` (January 2026), the production baseline ran stably for nearly 11 months without requiring container rebuilds—explaining why `ECOv003-L3T-L4T-JET` saw only documentation and metadata updates (`v1.17.0`–`v1.18.0`) between February and October 2026.
2. **Suomi NPP VIIRS Decommissioning & JPSS Transition (`v1.19.0` – `v1.22.1`, November 2026):**
   * On **November 2, 2026**, Suomi NPP VIIRS was decommissioned, cutting off upstream `VNP43NRT` coarse surface reflectance and albedo inputs required by `L2T_STARS`.
   * Transitioning `ECOv003-L2T-STARS` to JPSS (`VCD43NRT`) inputs (`v1.14.0` → `v1.18.0`) while preserving Collection 3 algorithmic consistency required rebuilding the shared `ecostress-level-2-3-4` application container around Python 3.12 and a `conda-forge` geospatial/scientific toolchain (`v1.9.0` → `v1.13.0`).
   * `ECOv003-L3T-L4T-JET` was aligned in lockstep across `v1.19.0`–`v1.22.1` so both PGEs share compatible dependency pins (`GEOS5FP~=2.24.0`, `JET3~=3.1.1`, `numpy~=2.5.4`, `pandas~=3.1.1`, `rasterio~=1.5.2`) and automated container smoke tests inside `ecostress-level-2-3-4`.

---

## Phase 1: Collection 2 Port & Initial Release (`v1.0.1` – `v1.1.0`, May – June 2025)

* **`v1.0.1` (2025-05-21) — Initial Collection 3 Port:**
  * Duplicated the ECOSTRESS Collection 2 `ECOv002-L3T-L4T-JET` codebase and re-targeted it for Collection 3 (`ECOv003-L3T-L4T-JET v1.0.1`).
  * Replaced inline evapotranspiration sub-modules with standalone pip dependencies: `BESS-JPL>=1.9.2`, `PM-JPL>=1.4.0`, `STIC-JPL`, `PTJPLSM>=1.2.0`, `FLiESANN`, `FLiESLUT`, `verma-net-radiation`, `ECOv002-granules>=1.1.1`, `ECOv003-granules>=1.3.0`, `NASADEM>=1.2.0`, `rasters>=1.5.0`, `GEOS5FP`, `koppengeiger`, `MCD12C1-2019-v006`, `check-distribution`, `colored-logging`, `solar-apparent-time`, and `sun-angles`.
  * Consolidated the three separate Collection 2 auxiliary products (`L3T SEB`, `L3T SM`, and `L3T MET`) into a single unified **`L3T ETAUX`** product (`Ta`, `RH`, `SM`, `Rg`, `Rn`) and switched product serialization to `ECOv003-granules>=1.3.0`.
  * Added individual model daily ET outputs alongside the ensemble daily median (`ETdaily`) and established the `ECOv003-L3T-L4T-JET` CLI entry point.

* **`v1.1.0` (2025-06-24) — Exit Codes & Downscaling Modularization:**
  * Replaced local exit code definitions with the external `ECOv003-exit-codes` package and removed legacy `SEB`/`SM`/`MET` product writer stubs.
  * Extracted meteorological and soil-moisture regression downscaling out of `ECOv003_L3T_L4T_JET.py` into dedicated modules (`sharpen_meteorology_data.py` and `sharpen_soil_moisture_data.py`), introducing direct `GEOS5FP_connection.Td_C(...)` calls.
  * Removed obsolete `downscale_*` helper modules and added a working granule-download example script using `ECOv002-CMR`.

---

## Phase 2: Ancillary Data Wiring & Resilience (`v1.2.0` – `v1.9.0`, July – September 2025)

* **`v1.2.0` – `v1.2.1` (2025-07-01 to 2025-07-03):**
  * Added Python 3.11 support, bumped `BESS-JPL>=1.12.0` to fix soil heat flux return values (`v1.2.0`), and passed `GEOS5FP_connection` into `FLiESANN` so GEOS-5 FP downloads respected the configured download directory (`v1.2.1`).

* **`v1.3.0` (2025-07-03):**
  * Reverted XML run-config parsing in `L3TL4TJETConfig.py` and `L3T_L4T_JET.xml` from `StaticAuxiliaryFileGroup` back to `StaticAncillaryFileGroup` to match Science Data System (SDS) run-config conventions.

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

---

## Phase 3: Open-Water Evaporation & SI/Daylight Standardization (`v1.10.0` – `v1.11.0`, October – November 2025)

* **`v1.10.0` (2025-10-01) — `AquaSEBS` Open-Water Integration & Dual-Collection Support:**
  * Added support for ingesting both `ECOv002` (`ECOv002-granules~=1.2.1`) and `ECOv003` (`ECOv003-granules~=1.10.0`) `L2T_LSTE` and `L2T_STARS` input granules.
  * Integrated `AquaSEBS` to compute open-water latent heat flux over SRTM/NASADEM water-mask pixels, introducing `GEOS5FP_connection.wind_speed(...)`, and added `rasterio`.
  * Fixed the `L3T_JET` instantaneous `PTJPLSM` layer (`LE_PTJPLSM`) and compiled initial Markdown/PDF versions of the Collection 3 ATBD and User Guide.

* **`v1.11.0` (2025-11-12) — Daylight Upscaling & SI Unit Naming:**
  * Standardized internal variable names to explicit SI unit suffixes (`SZA_deg`, `elevation_m`, `SWin_Wm2`, `LE_BESS_Wm2`, `LE_STIC_Wm2`, `LE_PTJPLSM_Wm2`, `LE_PMJPL_Wm2`, `Rn_Wm2`) across updated model interfaces (`AquaSEBS~=1.1.0`, `BESS-JPL~=1.20.0`, `FLiESANN~=2.1.0`, `GEOS5FP~=1.3.0`, `PM-JPL~=1.7.0`, `PTJPLSM~=1.9.0`, `STIC-JPL~=1.4.0`, `verma-net-radiation~=1.8.0`, `rasters~=1.14.0`, `NASADEM~=1.4.0`, `check-distribution~=1.1.0`, and `koppengeiger~=1.1.0`).
  * Switched to raw `FLiESANN~=2.1.0` solar radiation without GEOS-5 FP bias correction (`SWin_Wm2`) and enabled `upscale_to_daylight=True` across all constituent models.
  * Updated `ETdaily` to aggregate the model-specific daylight ET estimates (`ET_daylight_*_kg`), converted `ETuncertainty` to daily units (`mm day⁻¹`), added proportional flux partitioning layers (`LE_canopy_fraction_*`, `LE_soil_fraction_PTJPLSM`, `LE_interception_fraction_PTJPLSM`), and added the `--overwrite` CLI flag.

---

## Phase 4: Modular Architecture, `JET3` Extraction & Collection 3 Deployment (`v1.13.0` – `v1.18.0`, November 2025 – October 2026)

* **`v1.13.0` (2025-11-18) — Full Pipeline Modularization & Forward-Processing Deployment:**
  * Decomposed `ECOv003_L3T_L4T_JET.py` into focused modules: `read_ECOv003_configuration.py`, `read_ECOv003_inputs.py`, `JET.py`, `process_JET_table.py`, and `write_ECOv003_products.py`.
  * Added tabular/point processing (`process_JET_table`), bundled the ECOSTRESS Collection 2 Cal/Val reference input dataset, and delivered the package into the initial Collection 3 forward-processing container baseline (`ecostress-level-2-3-4 v1.7.0` / `v1.7.1`).

* **`v1.14.0` – `v1.16.0` (2026-01-24 to 2026-01-30) — `JET3` Extraction & Collection 3 Validation:**
  * Extracted the core `JET` science engine, `process_JET_table`, meteorological/soil-moisture sharpening modules, and Cal/Val tables (`ECOv002-calval-tables~=1.13.0`) out of `ECOv003-L3T-L4T-JET` into the standalone **`JET3`** package, leaving `ECOv003-L3T-L4T-JET` as a PGE wrapper around `JET3`.
  * Added performance benchmarking tools (`performance/analyze_table_processing.py`) and updated model dependencies and accuracy assessments for Collection 3 deployment (`v1.16.0`), establishing the reference output baseline maintained through the 11-month Suomi NPP operational run.

* **`v1.17.0` – `v1.18.0` (2026-04-29 to 2026-10-12) — Documentation & Metadata Fixes:**
  * Separated PGE and Science Algorithm Software (SAS) documentation, corrected layer names/sizes and uncertainty timesteps in `README.md` and the User Guide (`v1.17.0`–`v1.17.1`), and fixed `StandardMetadata/InputPointer` formatting (`v1.18.0`) ahead of the `ecostress-level-2-3-4 v1.8.0` container refresh.

---

## Phase 5: JPSS Transition, Containerization & `GEOS5FP` Remediation (`v1.19.0` – `v1.22.1`, November 2026)

* **`v1.19.0` – `v1.20.3` (2026-11-11 to 2026-11-17) — Coordinated JPSS Transition & Python 3.12/3.13 Alignment:**
  * Following the November 2, 2026 decommissioning of Suomi NPP VIIRS, aligned dependency pins with `ECOv003-L2T-STARS` (`v1.14.0`–`v1.18.0`, transitioning from `VNP43NRT` to JPSS `VCD43NRT`) across Python 3.13 (`v1.19.0`) and Python 3.12 (`v1.20.0`), culminating in `GEOS5FP~=2.24.0`, `JET3~=3.0.1`, `AquaSEBS~=1.3.0`, `BESS-JPL~=1.28.0`, `FLiESANN~=2.13.1`, `PM-JPL~=1.11.0`, `PTJPLSM~=1.10.0`, `STIC-JPL~=1.6.0`, `verma-net-radiation~=1.11.0`, `ECOv003-granules~=1.14.0`, `ECOv003-exit-codes~=1.2.0`, `rasters~=1.21.0`, `numpy~=2.5.4`, `pandas~=3.1.1`, `rasterio~=1.5.2`, `scikit-learn~=1.9.1`, `onnx~=1.23.2`, and `onnxruntime~=1.31.1` (`v1.20.2`–`v1.20.3`) for `ecostress-level-2-3-4 v1.9.0`–`v1.12.0`.

* **`v1.21.0` – `v1.22.0` (2026-11-19) — CLI Refactor & Multi-Stage Docker Runtime:**
  * Replaced manual `sys.argv` parsing with `argparse` (`build_parser`), added `--save-diagnostics` (deprecating `--save-intermediate`), introduced `smoke_test.py` (`ECOv003-L3T-L4T-JET test`), bumped `JET3~=3.1.0`, and added a multi-stage `micromamba` + `pip` `Dockerfile` (`linux/amd64`, Python 3.12) with container smoke tests (`tests/test_docker_smoke.py`), enabling end-to-end CLI smoke testing in `ecostress-level-2-3-4 v1.13.0`.

* **`v1.22.1` (In Progress on `geos5fp_mismatch`, 2026-11-20) — `GEOS5FP` API Contract Hardening:**
  * Isolated a regression where `JET3 v3.1.0` eagerly called legacy `GEOS5FP_connection.wind_speed(...)` (carried over from `ECOv003-L3T-L4T-JET v1.10.0`) after `GEOS5FP>=2.24.0` renamed the method to `wind_speed_mps(...)`.
  * Updated `ECOv003-L3T-L4T-JET v1.22.1` `pyproject.toml` to require `JET3~=3.1.1` alongside `GEOS5FP~=2.24.0`, and expanded `smoke_test.py` and `test_docker_smoke.py` to assert `GEOS5FPConnection` SI method availability (`wind_speed_mps`, `Td_K`, `Ta_C`, `RH`, `SM`) and verify `JET3` API compatibility prior to building `ecostress-level-2-3-4 v1.13.1`.