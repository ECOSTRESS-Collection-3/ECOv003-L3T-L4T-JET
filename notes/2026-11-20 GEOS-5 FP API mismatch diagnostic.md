# Diagnostic Report: `GEOS5FPConnection.wind_speed` `AttributeError` in `JET3 v3.1.0`

* **Date:** November 20, 2026
* **Affected Repositories:** `JET3` (`v3.1.0`), `ECOv003-L3T-L4T-JET` (`v1.22.0`), `ecostress-level-2-3-4` (`v1.13.0`)
* **Symptom:** `AttributeError: 'GEOS5FPConnection' object has no attribute 'wind_speed'` during L3T/L4T JET processing when `wind_speed_mps` is not pre-supplied.
* **Status:** Root cause isolated; remediation plan defined across upstream and downstream packages.

---

## 1. Executive Summary

During execution of the ECOSTRESS Collection 3 Level-3T/Level-4T Jet Propulsion Laboratory Evapotranspiration (`ECOv003-L3T-L4T-JET`) pipeline, runs fail immediately when `JET3` attempts to retrieve missing meteorological forcing data from `GEOS5FPConnection`. Specifically, `JET3` invokes `GEOS5FP_connection.wind_speed(...)`, whereas modern versions of `GEOS5FP` (`>=2.24.0`) expose this method exclusively as `wind_speed_mps(...)`.

This regression was introduced in `JET3 v3.1.0` when meteorological variable retrieval was refactored out of an optional conditional branch into eager top-level initialization inside `JET3/JET.py`, and subsequently surfaced in `ECOv003-L3T-L4T-JET v1.22.0` when the dependency constraint was bumped from `JET3~=3.0.1` to `JET3~=3.1.0`.

---

## 2. Root Cause & Regression Timeline

### Dependency & Release Chain
1. **`GEOS5FP` (`>=2.24.0`):** Standardized method naming with explicit SI unit suffixes, renaming `wind_speed` to `wind_speed_mps` (and exposing dewpoint temperature in Kelvin via `Td_K`).
2. **`JET3 v3.0.1`:** `JET3/JET.py` only called `GEOS5FP_connection.wind_speed(...)` inside the optional `if include_water_surface:` block. Standard land-surface L3T/L4T runs bypassed this call path entirely.
3. **`JET3 v3.1.0`:**
   * Refactored `JET3/JET.py` to eagerly resolve `wind_speed_mps`, `SZA_deg`, `elevation_m`, and `canopy_height_meters` up front prior to model execution.
   * Placed `GEOS5FP_connection.wind_speed(...)` directly in the default execution path (line 283), while newly added calibration and uncertainty quantification (UQ) modules in the same release consistently called `wind_speed_mps`.
4. **`ECOv003-L3T-L4T-JET v1.22.0` & `ecostress-level-2-3-4 v1.13.0`:**
   * Updated dependency specification from `JET3~=3.0.1` to `JET3~=3.1.0`, exposing every L3T/L4T JET production and test run (where `wind_speed_mps` is dynamically queried from GEOS-5 FP) to the `AttributeError`.

---

## 3. Secondary Latent API Mismatches Identified in `JET3 v3.1.0`

An audit of all `GEOS5FP_connection` invocations across `JET3 v3.1.0` revealed three additional latent defects that either mask degradation or will trigger secondary `AttributeError` failures once `wind_speed_mps` is resolved:

| File | Line(s) | Current Call in `JET3 v3.1.0` | Issue / `GEOS5FPConnection` Reality | Impact |
| :--- | :--- | :--- | :--- | :--- |
| `JET3/JET.py` | `283` | `GEOS5FP_connection.wind_speed(...)` | Method renamed to `wind_speed_mps(...)` | **Immediate crash** (`AttributeError`) on all standard runs without pre-supplied wind speed. |
| `JET3/JET.py` | `279` | `GEOS5FP_connection.elevation(...)` | `GEOS5FPConnection` does not implement `.elevation()` | **Secondary crash** (`AttributeError`) on standalone `JET()` invocations where `elevation_m` is `None`. |
| `JET3/sharpen_meteorology_data.py` | `57`, `156` | `GEOS5FP_connection.Td_C(...)` | `GEOS5FPConnection` only implements `Td_K(...)` | **Silent degradation:** Exception is caught and falls back to unsharpened coarse meteorology on every scene. |
| `JET3/constants.py` | `63` | `SHARPEN_METEOROLOGY = True` | Duplicate constant assignment | Code hygiene / configuration ambiguity. |

---

## 4. Remediation Plan

### 4.1 Upstream Fix: `JET3` (`v3.1.1`)
1. **`JET3/JET.py` (line 283):**
   * Replace `GEOS5FP_connection.wind_speed(...)` with `GEOS5FP_connection.wind_speed_mps(...)` (or guard with `hasattr(GEOS5FP_connection, "wind_speed_mps")` for backward compatibility).
2. **`JET3/JET.py` (line 279):**
   * Replace or guard `GEOS5FP_connection.elevation(...)` with `hasattr` checks / valid DEM elevation source lookup so standalone `JET()` calls do not fail when `elevation_m` is omitted.
3. **`JET3/sharpen_meteorology_data.py` (lines 57 & 156):**
   * Replace `GEOS5FP_connection.Td_C(...)` with `GEOS5FP_connection.Td_K(...) - 273.15` so meteorological sharpening executes rather than silently hitting the unsharpened fallback path.
4. **`JET3/constants.py` (line 63):**
   * Remove the duplicate `SHARPEN_METEOROLOGY = True` definition.
5. **`JET3/pyproject.toml`:**
   * Bump version to `3.1.1`.
   * Explicitly declare `"GEOS5FP>=2.24.0"` in `dependencies`.

### 4.2 Midstream Fix: `ECOv003-L3T-L4T-JET` (`v1.22.1`)
1. **`pyproject.toml`:**
   * Update dependency constraint from `"JET3~=3.1.0"` to `"JET3>=3.1.1"`.
   * Bump package version to `1.22.1`.
2. **`ECOv003_L3T_L4T_JET/smoke_test.py`:**
   * Add explicit interface assertions verifying that `GEOS5FPConnection` exposes `wind_speed_mps` and `Td_K`, and execute a lightweight mock/dry-run check of `JET` parameter resolution so `ECOv003-L3T-L4T-JET test` catches upstream API drift prior to container builds.

### 4.3 Downstream Container & Pipeline Update: `ecostress-level-2-3-4` (`v1.13.1`)
1. **`pyproject.toml`:**
   * Update dependency constraint from `"ECOv003-L3T-L4T-JET>=1.22.0"` to `"ECOv003-L3T-L4T-JET>=1.22.1"`.
   * Bump version to `1.13.1`.
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
- [ ] `ECOv003-L3T-L4T-JET v1.22.1` updated with `"JET3>=3.1.1"` and expanded `smoke_test.py`.
- [ ] `ecostress-level-2-3-4 v1.13.1` runtime image rebuilt and validated end-to-end with `make smoke-test`.