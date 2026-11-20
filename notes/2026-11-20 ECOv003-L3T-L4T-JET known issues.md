# `ECOv003-L3T-L4T-JET` Known Issues & DAG Log Triage Report

- **Date:** November 20, 2026
- **DAG Run Analyzed:** `EcostressDAG_Col3.46000.0802.20261116T001911117`
- **Log Scope:** 807 total DAG log files scanned; 6 log files reached `ECOv003-L3T-L4T-JET` execution (tiles `32TPS`, `32TPT`)
- **Affected Packages:** `ECOv003-L3T-L4T-JET` (`v1.22.0`), `JET3` (`v3.1.0`), `GEOS5FP` (`>=2.24.0`)

---

## 1. Executive Summary

Out of 51 unique issue signatures detected across 807 DAG log files, **47 issues originated upstream in `ECOv003_L2T_STARS` / `VCD43NRT`** (which prevented downstream `L3T_L4T_JET` jobs from being scheduled on failed tiles). Filtering exclusively to issues affecting `ECOv003-L3T-L4T-JET` isolates **4 unique issue signatures** across the 6 logs that executed the JET PGE:

1. **Fatal `GEOS5FPConnection.wind_speed` `AttributeError` (`JET3 v3.1.0`)** — Crashes every `L3T_L4T_JET` run when `wind_speed_mps` is dynamically retrieved from GEOS-5 FP (**Resolved in `JET3 v3.1.1` / `ECOv003-L3T-L4T-JET v1.22.1`**).
2. **Silent `GEOS5FPConnection.Td_C` `AttributeError` (`JET3 v3.1.0`)** — Caught during meteorological downscaling (`unable to sharpen meteorology`), forcing fallback to unsharpened coarse GEOS-5 FP air temperature and relative humidity (**Resolved in `JET3 v3.1.1` / `ECOv003-L3T-L4T-JET v1.22.1`**).
3. **Missing `.netrc` Credential Warnings (`daac.ornl.gov` & `urs.earthdata.nasa.gov`)** — Non-fatal container environment warnings emitted when `/root/.netrc` is absent; benign when `L3T_L4T_STATIC` is pre-populated on shared runtime storage.

---

## 2. JET-Specific Issues Summary

| Issue # | Severity | Log Signature | Occurrences | Affected Logs / Tiles | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **#4** | `ERROR` | `'GEOS5FPConnection' object has no attribute 'Td_C'` | 6 | 6 logs (`32TPS`, `32TPT`) | **Fixed** (`JET3 v3.1.1` / `ECOv003-L3T-L4T-JET v1.22.1`) |
| **#34** | `WARNING` / `FATAL` | `unable to sharpen meteorology` + `AttributeError: 'GEOS5FPConnection' object has no attribute 'wind_speed'` | 6 | 6 logs (`32TPS`, `32TPT`) | **Fixed** (`JET3 v3.1.1` / `ECOv003-L3T-L4T-JET v1.22.1`) |
| **#32** | `WARNING` | `netrc credentials not found for daac.ornl.gov` | 6 | 6 logs (`32TPS`, `32TPT`) | **Operational / Benign** (when static files are cached) |
| **#33** | `WARNING` | `netrc credentials not found for urs.earthdata.nasa.gov` | 6 | 6 logs (`32TPS`, `32TPT`) | **Operational / Benign** (when static files are cached) |

---

## 3. Detailed Issue Analysis

### 3.1. Issue #34 (Fatal): `AttributeError: 'GEOS5FPConnection' object has no attribute 'wind_speed'`

- **Severity:** Fatal Crash (`AttributeError` unhandled in `JET3.JET`)
- **Occurrences:** 6 across 6 log files (100% of `L3T_L4T_JET` executions in the DAG)
- **Affected Tiles:** `32TPS`, `32TPT`
- **Representative Traceback:**
  ```text
  [2026-11-20 02:18:59 WARNING] unable to sharpen meteorology
  Traceback (most recent call last):
    File "/opt/venv/bin/ECOv003-L3T-L4T-JET", line 6, in <module>
      sys.exit(main())
    File "/opt/venv/lib/python3.12/site-packages/ECOv003_L3T_L4T_JET/ECOv003_L3T_L4T_JET.py", line 338, in main
      exit_code = L3T_L4T_JET(
    File "/opt/venv/lib/python3.12/site-packages/ECOv003_L3T_L4T_JET/ECOv003_L3T_L4T_JET.py", line 133, in L3T_L4T_JET
      results = JET(
    File "/opt/venv/lib/python3.12/site-packages/JET3/JET.py", line 283, in JET
      wind_speed_mps = GEOS5FP_connection.wind_speed(time_UTC=time_UTC, geometry=geometry, resampling=downsampling)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AttributeError: 'GEOS5FPConnection' object has no attribute 'wind_speed'. Did you mean: 'wind_speed_mps'?
  ```
- **Root Cause:**
  - `GEOS5FP >=2.24.0` standardized method names with explicit SI unit suffixes, renaming `.wind_speed(...)` to `.wind_speed_mps(...)`.
  - `JET3 v3.1.0` refactored meteorological variable resolution out of an optional open-water (`AquaSEBS`) branch into top-level initialization in `JET3/JET.py:283` while retaining the legacy `.wind_speed(...)` call.
- **Resolution:**
  - Updated `JET3` (`v3.1.1`) to invoke `GEOS5FP_connection.wind_speed_mps(...)`.
  - Bumped `ECOv003-L3T-L4T-JET` (`v1.22.1`) dependency constraint to `JET3~=3.1.1` and added explicit `GEOS5FPConnection` SI-method contract checks to `ECOv003_L3T_L4T_JET/smoke_test.py` and `tests/test_docker_smoke.py`.

---

### 3.2. Issue #4 & #34 (Silent Science Degradation): `'GEOS5FPConnection' object has no attribute 'Td_C'` / `unable to sharpen meteorology`

- **Severity:** Error logged + Silent Science Degradation (falls back to unsharpened coarse meteorology)
- **Occurrences:** 6 `ERROR` entries (`Td_C`) paired with 6 `WARNING` entries (`unable to sharpen meteorology`) across 6 log files
- **Affected Tiles:** `32TPS`, `32TPT`
- **Representative Log Snippet:**
  ```text
  [2026-11-20 02:18:59 ERROR] 'GEOS5FPConnection' object has no attribute 'Td_C'
  [2026-11-20 02:18:59 WARNING] unable to sharpen meteorology
  ```
- **Root Cause:**
  - `JET3/sharpen_meteorology_data.py` called `GEOS5FP_connection.Td_C(...)` for coarse and fine dew-point temperature rasters, whereas `GEOS5FP >=2.24.0` removed `Td_C` in favor of `Td_K(...)`.
  - In `ECOv003_L3T_L4T_JET/read_ECOv003_inputs.py`, `sharpen_meteorology_data(...)` is wrapped in a `try ... except Exception:` block that logs the error, emits `"unable to sharpen meteorology"`, and falls back to coarse unsharpened `GEOS5FP_connection.Ta_C(...)` and `GEOS5FP_connection.RH(...)`.
- **Resolution:**
  - Updated `JET3` (`v3.1.1`) `sharpen_meteorology_data.py` to compute Celsius dew-point temperature via `GEOS5FP_connection.Td_K(...) - 273.15`.

---

### 3.3. Issues #32 & #33 (Environment Warnings): Missing `.netrc` Credentials for `daac.ornl.gov` and `urs.earthdata.nasa.gov`

- **Severity:** Warning (non-blocking if static ancillary datasets are pre-cached)
- **Occurrences:** 6 each across 6 log files
- **Affected Tiles:** `32TPS`, `32TPT`
- **Representative Log Snippet:**
  ```text
  [2026-11-20 02:18:18 WARNING] netrc credentials not found for daac.ornl.gov
  [2026-11-20 02:18:18 WARNING] netrc credentials not found for urs.earthdata.nasa.gov
  ```
- **Root Cause:**
  - Ancillary data connectors initialized during `read_ECOv003_inputs` / `JET` check for `/root/.netrc` credentials for ORNL DAAC (`daac.ornl.gov`, used for GEDI canopy height) and NASA Earthdata Login (`urs.earthdata.nasa.gov`).
  - Inside the stateless production container, `/root/.netrc` is not baked into the image.
- **Impact & Operational Guidance:**
  - **Benign** when `StaticAncillaryFileGroup/L3T_L4T_STATIC` (`GEDI_download`, `MODISCI_download`, `MCD12C1_download`, `SoilGrids_download`) is pre-populated on `/runtime_ancillary`.
  - If processing new tiles/regions that trigger on-demand static ancillary downloads, bind-mount a read-only `.netrc` file or set `EARTHDATA_USERNAME` / `EARTHDATA_PASSWORD` environment variables in the job runtime.

---

## 4. Upstream Dependency Note (`ECOv003_L2T_STARS`)

The remaining 47 unique issues in `EcostressDAG_Col3.46000.0802.20261116T001911117` occurred exclusively inside `ECOv003_L2T_STARS` / `VCD43NRT` (primarily missing `GDAL_DRIVER_PATH` / `gdal_HDF5.so` plugin errors when reading GEOS-5 FP `.nc4` files and legacy Julia fusion failures). Because `L2T_STARS` produces a mandatory input granule (`InputFileGroup/L2T_STARS`) for `L3T_L4T_JET`, upstream `L2T_STARS` failures prevented `L3T_L4T_JET` from being scheduled on those tiles.

---

## 5. Remediation & Verification Checklist

- [x] **`JET3 v3.1.1`:** Replace `GEOS5FP_connection.wind_speed(...)` with `wind_speed_mps(...)` and `Td_C(...)` with `Td_K(...) - 273.15`.
- [x] **`ECOv003-L3T-L4T-JET v1.22.1`:** Pin `JET3~=3.1.1` and `GEOS5FP~=2.24.0` in `pyproject.toml`, and add `GEOS5FPConnection` / `JET3` API contract assertions to `smoke_test.py` and `tests/test_docker_smoke.py`.
- [ ] **`ecostress-level-2-3-4 v1.13.1`:** Rebuild runtime container image with `ECOv003-L3T-L4T-JET>=1.22.1`, run `make smoke-test`, and re-drive failed DAG tiles.