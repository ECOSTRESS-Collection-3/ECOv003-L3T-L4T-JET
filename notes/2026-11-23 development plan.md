# `ECOv003-L3T-L4T-JET` Comprehensive Development Plan (`v1.0.1` – `v1.23.0`)

- **Repository:** [`ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET`](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET)
- **Current Version:** `v1.23.0` (branch: `geos5fp_mismatch`)
- **Last Updated:** November 23, 2026

---

## 1. Executive Summary & Architectural Trajectory

`ECOv003-L3T-L4T-JET` is the Product Generating Executable (PGE) responsible for producing ECOSTRESS Collection 3 Level-3 and Level-4 terrestrial and open-water ecosystem data products (`L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, and `L4T_WUE`). Across 23 releases, the repository has evolved through five distinct architectural phases:

1. **Collection 2 Port & Product Consolidation (`v1.0.1` – `v1.1.0`):** Ported the Collection 2 JET pipeline to Collection 3, extracted inline science sub-modules into standalone pip packages, and consolidated `L3T SEB`, `L3T SM`, and `L3T MET` into a single **`L3T ETAUX`** product.
2. **Ancillary Data Integration & Resilience (`v1.2.0` – `v1.9.0`):** Wired local download directories for static datasets (`GEDI`, `MODISCI`, `MCD12C1`, `SoilGrids`, `SRTM`), aligned XML run-configs (`StaticAncillaryFileGroup`), and wrapped meteorological/soil-moisture downscaling in resilient fallback handlers.
3. **Open-Water Evaporation & SI/Daylight Standardization (`v1.10.0` – `v1.11.0`):** Integrated `AquaSEBS` for open-water latent heat flux, enabled dual-collection (`ECOv002` / `ECOv003`) granule ingestion, standardized internal variables to explicit SI unit suffixes, and added per-model daylight ET and flux-partitioning layers.
4. **Pipeline Modularization & `JET3` Science Extraction (`v1.13.0` – `v1.18.0`):** Decomposed the monolithic PGE script into focused I/O, configuration, and product-writer modules, extracted the core science ensemble into the standalone **`JET3`** package, and established the Collection 3 forward-processing baseline (`BuildID` `0700`).
5. **Post-Suomi NPP JPSS Transition, Containerization & Solar Radiation Parity (`v1.19.0` – `v1.23.0`):** Coordinated dependency alignment following the November 2, 2026 decommissioning of Suomi NPP VIIRS (`VNP43NRT` -> JPSS `VCD43NRT`), introduced a multi-stage `micromamba` + `pip` `Dockerfile` (`linux/amd64`, Python 3.12), hardened `GEOS5FP` SI method and unit-transformation contracts (`GEOS5FP~=2.27.0`, `JET3~=3.3.0`, `BESS-JPL~=1.29.0`), and restored top-level package exports for **`v1.23.0`**.

---

## 2. Summary of `v1.23.0` Deliverables & Root-Cause Resolutions

1. **Top-Level Package Export Restoration (`ECOv003_L3T_L4T_JET/__init__.py`):**
   - Explicitly re-exported `from .generate_L3T_L4T_JET_runconfig import generate_L3T_L4T_JET_runconfig` so top-level imports resolve to the callable function rather than the submodule.
2. **`BESS-JPL` / `GEOS5FP` `CO2SC` Raster Query Fix (`pyproject.toml`):**
   - Pinned `BESS-JPL~=1.29.0` and `GEOS5FP~=2.27.0` to resolve the `ValueError: Multiple variables can only be queried for point geometries` crash when querying `["CO2SC"]` on a `RasterGrid`.
3. **Solar Radiation (`Rg`) Parity & Unit-Conversion Hardening (`constants.py`, `smoke_test.py`, `tests/test_docker_smoke.py`):**
   - Root-caused the `+74.35 W/m²` `L3T_ETAUX` `Rg` discrepancy on `orbit=44841, scene=001, tile=11SPS` (`2026-06-02`) to missing unit-scaling factors on gridded rasters in `GEOS5FP v2.24.0`–`v2.26.0` (`vapor_gccm` returning raw `TQV` in kg/m² instead of `TQV / 10` in g/cm², and `ozone_cm` returning raw `TO3` in Dobson Units instead of `TO3 / 1000` in cm).
   - Updated to `GEOS5FP~=2.27.0` and `JET3~=3.3.0`, set `BIAS_CORRECT_FLIES_ANN = False` in `ECOv003_L3T_L4T_JET/constants.py` to match the Collection 3 operational baseline (`BuildID 0700`), and added unit-transformation assertions to `smoke_test.py` and `tests/test_docker_smoke.py`.

---

## 3. Verification & Release Checklist (`v1.23.0`)

- [x] `ECOv003_L3T_L4T_JET/__init__.py` re-exports `generate_L3T_L4T_JET_runconfig`.
- [x] Upstream `BESS-JPL v1.29.0`, `GEOS5FP v2.27.0`, and `JET3 v3.3.0` released on PyPI.
- [x] `pyproject.toml` updated to `1.23.0` with `BESS-JPL~=1.29.0`, `GEOS5FP~=2.27.0`, and `JET3~=3.3.0`.
- [x] `ECOv003_L3T_L4T_JET/constants.py` sets `BIAS_CORRECT_FLIES_ANN = False` and `ZERO_COT_CORRECTION = True`.
- [x] `smoke_test.py` and `tests/test_docker_smoke.py` verify `BIAS_CORRECT_FLIES_ANN is False` and `GEOS5FP` `vapor_gccm` / `ozone_cm` unit transformations.
- [ ] Run `make test`, `make smoke-test`, and `python examples/example_L3T_L4T_JET_run_with_download.py` to confirm full `MATCH` across `L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, and `L4T_WUE`.
- [ ] Run `make docker-smoke-test` on `linux/amd64`, tag `v1.23.0`, publish to PyPI, and update `ecostress-level-2-3-4`.
