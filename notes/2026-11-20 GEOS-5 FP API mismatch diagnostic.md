# Diagnostic Report: `GEOS5FPConnection.wind_speed` `AttributeError` in `JET3 v3.1.0`

- **Date:** November 20, 2026
- **Affected Repositories:** `JET3` (`v3.1.0`), `ECOv003-L3T-L4T-JET` (`v1.22.0`), `ecostress-level-2-3-4` (`v1.13.0`)
- **Symptom:** `AttributeError: 'GEOS5FPConnection' object has no attribute 'wind_speed'` during L3T/L4T JET processing when `wind_speed_mps` is not pre-supplied.
- **Status:** Root cause and historical lineage isolated; remediation plan defined across upstream and downstream packages.

---

## 1. Executive Summary

During execution of the ECOSTRESS Collection 3 Level-3T/Level-4T Jet Propulsion Laboratory Evapotranspiration (`ECOv003-L3T-L4T-JET`) pipeline, runs fail immediately when `JET3` attempts to retrieve missing meteorological forcing data from `GEOS5FPConnection`. Specifically, `JET3` invokes `GEOS5FP_connection.wind_speed(...)`, whereas modern versions of `GEOS5FP` (`>=2.24.0`) expose this method exclusively as `wind_speed_mps(...)`.

A review of the `ECOv003-L3T-L4T-JET` release history (`v1.0.1` through `v1.11.0`) confirms that both the legacy `.wind_speed(...)` call and the `.Td_C(...)` call originated in early `ECOv003-L3T-L4T-JET` releases (`v1.1.0` and `v1.10.0`) before the core science algorithms were extracted into `JET3`. When `JET3 v3.1.0` refactored meteorological variable retrieval out of an optional conditional branch into eager top-level initialization inside `JET3/JET.py`, and `ECOv003-L3T-L4T-JET v1.22.0` bumped its dependency constraint from `JET3~=3.0.1` to `JET3~=3.1.0`, every standard L3T/L4T JET run became exposed to the `AttributeError`.

---

## 2. Root Cause, Historical Lineage & Regression Timeline

### Historical Origin in `ECOv003-L3T-L4T-JET` (`v1.1.0` – `v1.11.0`)
1. **`ECOv003-L3T-L4T-JET v1.1.0` (Introduction of `.Td_C(...)`):**
   - Meteorological downscaling was extracted from `ECOv003_L3T_L4T_JET.py` into `ECOv003_L3T_L4T_JET/sharpen_meteorology_data.py`, calling `GEOS5FP_connection.Td_C(...)` for coarse and fine dew-point temperature rasters.
2. **`ECOv003-L3T-L4T-JET v1.7.0` (Silent Fallback Wrapper Added):**
   - Calls to `sharpen_meteorology_data(...)` were wrapped in a broad `try ... except Exception:` handler that logs `"unable to sharpen meteorology"` and falls back to coarse `GEOS5FP_connection.Ta_C(...)` and `GEOS5FP_connection.RH(...)`.
   - When `sharpen_meteorology_data.py` and this `try/except` wrapper were later migrated into `JET3` (and retained in `ECOv003_L3T_L4T_JET/read_ECOv003_inputs.py`), `GEOS5FP`'s removal of `.Td_C(...)` in favor of `.Td_K(...)` caused meteorological sharpening to fail silently on every run instead of raising an unhandled exception.
3. **`ECOv003-L3T-L4T-JET v1.10.0` & `v1.11.0` (Introduction of `.wind_speed(...)`):**
   - In `v1.10.0`, `AquaSEBS` open-water evaporation was integrated into `ECOv003_L3T_L4T_JET.py` using `windspeed_mps = GEOS5FP_connection.wind_speed(...)`.
   - In `v1.11.0`, variable names across the pipeline were standardized to explicit SI unit suffixes (`SZA_deg`, `elevation_m`, `SWin_Wm2`, `LE_BESS_Wm2`, etc.), but `GEOS5FP_connection.wind_speed(...)` was left unrenamed when the modeling code was subsequently extracted into `JET3`.

### Dependency & Release Chain
1. **`GEOS5FP` (`>=2.24.0`):** Standardized method naming with explicit SI unit suffixes, renaming `wind_speed` to `wind_speed_mps` and exposing dew-point temperature in Kelvin via `Td_K` (removing `Td_C`).
2. **`JET3 v3.0.1`:** `JET3/JET.py` only called `GEOS5FP_connection.wind_speed(...)` inside the optional `if include_water_surface:` block (mirroring the `AquaSEBS` path from `v1.10.0`). Standard land-surface L3T/L4T runs bypassed this call path entirely.
3. **`JET3 v3.1.0`:**
   - Refactored `JET3/JET.py` to eagerly resolve `wind_speed_mps`, `SZA_deg`, `elevation_m`, and `canopy_height_meters` up front prior to model execution.
   - Placed `GEOS5FP_connection.wind_speed(...)` directly in the default execution path (line 283), while newly added calibration and uncertainty quantification (UQ) modules in the same release consistently called `wind_speed_mps`.
4. **`ECOv003-L3T-L4T-JET v1.22.0` & `ecostress-level-2-3-4 v1.13.0`:**
   - Updated dependency specification from `JET3~=3.0.1` to `JET3~=3.1.0`, exposing every L3T/L4T JET production and test run (where `wind_speed_mps` is dynamically queried from GEOS-5 FP) to the `AttributeError`.
   - *Codebase Audit Note:* Inspection of `ECOv003-L3T-L4T-JET v1.22.0` (`read_ECOv003_inputs.py` and `ECOv003_L3T_L4T_JET.py`) confirms that `ECOv003-L3T-L4T-JET` itself only invokes `.AOT()`, `.COT()`, `.vapor_gccm()`, `.ozone_cm()`, `.Ta_C()`, `.RH()`, and `.SM()` directly on `GEOS5FP_connection`—all of which remain valid in `GEOS5FP >=2.24.0`. No science or I/O logic changes are required in `ECOv003-L3T-L4T-JET`.

---

## 3. Secondary Latent API Mismatches Identified in `JET3 v3.1.0`

An audit of all `GEOS5FP_connection` invocations across `JET3 v3.1.0` revealed three additional latent defects that either mask degradation or will trigger secondary `AttributeError` failures once `wind_speed_mps` is resolved:

| File | Line(s) | Current Call in `JET3 v3.1.0` | Issue / `GEOS5FPConnection` Reality | Impact |
| :--- | :--- | :--- | :--- | :--- |
| `JET3/JET.py` | `283` | `GEOS5FP_connection.wind_speed(...)` | Method renamed to `wind_speed_mps(...)` (carried over from `ECOv003-L3T-L4T-JET v1.10.0`) | **Immediate crash** (`AttributeError`) on all standard runs without pre-supplied wind speed. |
| `JET3/JET.py` | `279` | `GEOS5FP_connection.elevation(...)` | `GEOS5FPConnection` does not implement `.elevation()` | **Secondary crash** (`AttributeError`) on standalone `JET()` invocations where `elevation_m` is `None`. |
| `JET3/sharpen_meteorology_data.py` | `57`, `156` | `GEOS5FP_connection.Td_C(...)` | `GEOS5FPConnection` only implements `Td_K(...)` (carried over from `v1.1.0`; masked by `v1.7.0` `try/except`) | **Silent degradation:** Exception is caught in `read_ECOv003_inputs.py` and falls back to unsharpened coarse meteorology on every scene. |
| `JET3/constants.py` | `63` | `SHARPEN_METEOROLOGY = True` | Duplicate constant assignment | Code hygiene / configuration ambiguity. |

---

## 4. Remediation Plan

### 4.1 Upstream Fix: `JET3` (`v3.1.1`)
1. **`JET3/JET.py` (line 283):**
   - Replace `GEOS5FP_connection.wind_speed(...)` with `GEOS5FP_connection.wind_speed_mps(...)` (or guard with `hasattr(GEOS5FP_connection, "wind_speed_mps")` for backward compatibility).
2. **`JET3/JET.py` (line 279):**
   - Replace or guard `GEOS5FP_connection.elevation(...)` with `hasattr` checks / valid DEM elevation source lookup so standalone `JET()` calls do not fail when `elevation_m` is omitted.
3. **`JET3/sharpen_meteorology_data.py` (lines 57 & 156):**
   - Replace `GEOS5FP_connection.Td_C(...)` with `GEOS5FP_connection.Td_K(...) - 273.15` so meteorological sharpening executes rather than silently hitting the unsharpened fallback path.
4. **`JET3/constants.py` (line 63):**
   - Remove the duplicate `SHARPEN_METEOROLOGY = True` definition.
5. **`JET3/pyproject.toml`:**
   - Bump version to `3.1.1`.
   - Explicitly declare `"GEOS5FP>=2.24.0"` in `dependencies`.

### 4.2 Midstream Fix: `ECOv003-L3T-L4T-JET` (`v1.22.1`)
1. **`pyproject.toml`:**
   - Update dependency constraint from `"JET3~=3.1.0"` to `"JET3~=3.1.1"` (or `"JET3>=3.1.1"`).
   - Bump package version to `1.22.1`.
2. **`ECOv003_L3T_L4T_JET/smoke_test.py` & `tests/test_docker_smoke.py`:**
   - Add explicit interface assertions verifying that `GEOS5FPConnection` exposes `wind_speed_mps` and `Td_K`, and execute a lightweight mock/dry-run check of `JET` parameter resolution so `ECOv003-L3T-L4T-JET test` catches upstream API drift prior to container builds.

### 4.3 Downstream Container & Pipeline Update: `ecostress-level-2-3-4` (`v1.13.1`)
1. **`pyproject.toml`:**
   - Update dependency constraint from `"ECOv003-L3T-L4T-JET>=1.22.0"` to `"ECOv003-L3T-L4T-JET>=1.22.1"`.
   - Bump version to `1.13.1`.
2. **Container Rebuild & Verification:**
   ```bash
   make rebuild-python-env-build
   make build-runtime
   make smoke-test
   ```

---

## 5. Verification Checklist

- [ ] `JET3 v3.1.1` tagged and published with `"GEOS5FP>=2.24.0"` pinned.
- [ ] Unit tests in `JET3` verify `JET()` execution when `wind_speed_mps=None` and `elevation_m=None`.
- [ ] `sharpen_meteorology_data` verified to produce sharpened outputs without falling back due to `Td_C`.
- [ ] `ECOv003-L3T-L4T-JET v1.22.1` updated with `"JET3~=3.1.1"` and expanded `smoke_test.py` / `test_docker_smoke.py`.
- [ ] `ecostress-level-2-3-4 v1.13.1` runtime image rebuilt and validated end-to-end with `make smoke-test`.
