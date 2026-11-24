# ECOv003-L3T-L4T-JET Known Issues & Operational Triage Report

- **Repository:** [`ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET`](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET)
- **Current Release:** `v1.23.0` (`BuildID 0700`)
- **Container Runtime:** `eco-level-2-3-4-application:v1.14.0`
- **Report Date:** November 24, 2026
- **Triage Source:** ECOSTRESS Collection 3 Forward-Processing DAG Logs (`EcostressDAG_Col3.46000.0802.20261116T001911117` and `EcostressDAG_Col3.47400.0802.20261115T235815542`)

---

## 1. Executive Summary

Following the November 2, 2026 decommissioning of Suomi NPP VIIRS (`VNP43NRT` $\rightarrow$ JPSS `VCD43NRT`) and the deployment of `ECOv003-L3T-L4T-JET v1.23.0` (`GEOS5FP~=2.27.0`, `JET3~=3.3.0`, `BESS-JPL~=1.29.0`) in `eco-level-2-3-4-application:v1.14.0`, all core `GEOS5FP` API, `CO2SC` raster query, and `FLiES-ANN` solar radiation unit regressions have been resolved.

Triage of **762 scanned log files** from DAG `EcostressDAG_Col3.47400.0802.20261115T235815542` confirms **three open operational issues** (`#92`, `#91`, `#85`) remaining for `v1.23.1`, alongside upstream/environmental log signatures observed during re-drives.

---

## 2. Open Issues (`ECOv003-L3T-L4T-JET`)

### 2.1. Issue `#92` — `AquaSEBS` Aborts Terrestrial ET When No Valid Unmasked Water Pixels Exist

- **GitHub Issue:** [`#92`](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/issues/92)
- **Severity:** High / Degraded Coverage (`EXPECTED_SKIP` in DAG log scraper — 19 occurrences across 17 tiles on 2026-11-24)
- **Affected Versions:** `ECOv003-L3T-L4T-JET <= v1.23.0` with `JET3 <= v3.3.0`
- **Affected Tiles (`EcostressDAG_Col3.47400`):** `50JPQ`, `50KRC`, `51KVB`, `51KVV`, `51KWU`, `51KYT`, `51KYU`, `51KZB`, `51KZT`, `51LYC`, `51LZC`, `52KBD`, `52KBF`, `52KBG`, `52KCE`, `52KCF`, `52KCG`
- **Log Signature & Traceback:**
  ```text
    File "/opt/venv/lib/python3.12/site-packages/JET3/JET.py", line 933, in JET
      AquaSEBS_results = AquaSEBS(
    File "/opt/venv/lib/python3.12/site-packages/AquaSEBS/AquaSEBS.py", line 120, in AquaSEBS
      water_heat_flux_results = water_heat_flux(
    File "/opt/venv/lib/python3.12/site-packages/AquaSEBS/water_heat_flux.py", line 153, in water_heat_flux
      check_distribution(Tn, "Tn")
    File "/opt/venv/lib/python3.12/site-packages/check_distribution/check_distribution.py", line 89, in check_distribution
      raise BlankOutputError(f"variable {variable}{date_message}{target_message} is a blank image")
  check_distribution.check_distribution.BlankOutputError: variable Tn is a blank image
  ```
- **Root Cause:** In `JET3/JET.py` (line 933), `AquaSEBS(...)` is called unconditionally regardless of whether any unmasked open-water pixels exist (`(water_mask == 1) & np.isfinite(ST_C)`). On land-only tiles or coastal tiles where clouds mask out open-water pixels, `AquaSEBS` fails `check_distribution(Tn, "Tn")` and raises `BlankOutputError`, aborting the entire `JET()` execution even when valid land pixels are present.
- **Remediation Plan:** Guard `AquaSEBS(...)` in `JET3` (and/or handle `BlankOutputError` inside `AquaSEBS` integration) so open-water processing is skipped when no valid unmasked water pixels exist, allowing terrestrial `L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, and `L4T_WUE` outputs to be generated normally whenever valid land pixels are present.

---

### 2.2. Issue `#91` — Uncaught `check_distribution.BlankOutputError` Exits with Status `1` Instead of `BLANK_OUTPUT`

- **GitHub Issue:** [`#91`](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/issues/91)
- **Severity:** Medium / Incorrect Exit Code (`run_pge::docker_status= 1` — 19 occurrences across 17 tiles on 2026-11-24)
- **Affected Versions:** `ECOv003-L3T-L4T-JET v1.13.0` – `v1.23.0`
- **Log Signature:**
  ```text
  check_distribution.check_distribution.BlankOutputError: variable Tn is a blank image
  run_pge::docker_status= 1
  ```
- **Root Cause:** `ECOv003_L3T_L4T_JET/ECOv003_L3T_L4T_JET.py` catches `JET3.BlankOutput`, whereas `check_distribution` raises `check_distribution.BlankOutputError`. Because `BlankOutputError` is uncaught at the PGE entrypoint, Python terminates with generic exit code `1` instead of the designated `ECOv003_exit_codes.BLANK_OUTPUT` skip code.
- **Remediation Plan:** Import `BlankOutputError` from `check_distribution` in `ECOv003_L3T_L4T_JET/ECOv003_L3T_L4T_JET.py` and catch `(BlankOutput, BlankOutputError)` to map blank scenes cleanly to `BLANK_OUTPUT`.

---

### 2.3. Issue `#85` — Missing `.netrc` Credential Warnings in Stateless Container Runs

- **GitHub Issue:** [`#85`](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/issues/85)
- **Severity:** Low / Informational Warning (38 occurrences across 17 tiles on 2026-11-24)
- **Affected Versions:** All containerized versions (`v1.21.0` – `v1.23.0`)
- **Log Signatures:**
  ```text
  [WARNING] netrc credentials not found for daac.ornl.gov
  [WARNING] netrc credentials not found for urs.earthdata.nasa.gov
  ```
- **Root Cause:** Stateless runtime containers do not ship with `/root/.netrc` credentials for ORNL DAAC or NASA Earthdata Login. Downstream static ancillary clients (`GEDI`, `SoilGrids`, `MODISCI`) check `.netrc` during initialization even when target static files already exist locally under `StaticAncillaryFileGroup/L3T_L4T_STATIC` (`/runtime_ancillary`).
- **Operational Impact & Remediation:**
  - **Non-blocking** when `L3T_L4T_STATIC` is pre-populated on shared runtime storage; **blocking** only if a tile attempts an on-the-fly download of missing static ancillary files.
  - Add a logging filter in `configure_pge_logging` (`read_ECOv003_configuration.py`) to suppress non-fatal `netrc credentials not found` warnings in container runs and document `.netrc` mount requirements for on-demand downloads.

---

## 3. Summary Matrix of All Operational & Historical Log Signatures

| ID / Tracking | Severity | Status | Log Signature | Root Cause & Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **`#92`** | High (`EXPECTED_SKIP`) | **Open** (`v1.23.1`) | `BlankOutputError: variable Tn is a blank image` (`JET3/JET.py:933`) | `AquaSEBS` runs unconditionally even when no unmasked water pixels exist, aborting valid land pixels. Guard `AquaSEBS` in `JET3`. |
| **`#91`** | Medium (`Exit Code 1`) | **Open** (`v1.23.1`) | `BlankOutputError` uncaught (`run_pge::docker_status= 1`) | PGE catches `JET3.BlankOutput` but not `check_distribution.BlankOutputError`. Catch both and return `BLANK_OUTPUT`. |
| **`#85`** | Low (`WARNING`) | **Open** (`v1.23.1`) | `netrc credentials not found for daac.ornl.gov` / `urs.earthdata.nasa.gov` | Benign when `L3T_L4T_STATIC` is pre-staged; filter warning in PGE logging and document `.netrc` mount. |
| **Upstream (`L2T_STARS`)** | `ERROR` (4 logs, tile `51KTS`) | External (`L2T_STARS`) | `STARS_NDVI_51KTS_70m.tif: MissingRequired: TIFF directory is missing required "ImageLength" field` | Truncated/corrupt cached `STARS_NDVI_51KTS_70m.tif` from an interrupted earlier run; clear cached intermediate file for tile `51KTS` and re-drive. |
| **GDAL Info** | `WARNING` (19 logs) | Benign | `CPLE_NotSupported in driver GTiff does not support open option FILL` | Harmless GDAL driver option warning when opening GeoTIFFs; no impact on output data. |
| **Resolved (`v1.23.0`)** | Degraded Output | **Fixed** (`v1.23.0`) | `+74.35 W/m²` `Rg` bias in `L3T_ETAUX` (`r = 0.389`) | `GEOS5FP` `v2.24.0`–`v2.26.0` omitted `/10` on `vapor_gccm` and `/1000` on `ozone_cm`. Fixed in `GEOS5FP~=2.27.0` and `JET3~=3.3.0`. |
| **Resolved (`v1.23.0`)** | `FATAL` (`ValueError`) | **Fixed** (`v1.23.0`) | `ValueError: Multiple variables can only be queried for point geometries` (`CO2SC`) | `BESS-JPL` passed `["CO2SC"]` list to raster query. Fixed in `BESS-JPL~=1.29.0` and `GEOS5FP~=2.27.0`. |
| **Resolved (`v1.23.0`)** | Bug (`TypeError`) | **Fixed** (`v1.23.0`) | `TypeError: 'module' object is not callable` on `generate_L3T_L4T_JET_runconfig` | Re-exported `generate_L3T_L4T_JET_runconfig` in `ECOv003_L3T_L4T_JET/__init__.py`. |
| **Resolved (`v1.22.1`)** | `FATAL` (`AttributeError`) | **Fixed** (`v1.22.1`) | `'GEOS5FPConnection' object has no attribute 'wind_speed'` / `'Td_C'` | Updated `JET3~=3.1.1` to use `wind_speed_mps()` and `Td_K() - 273.15` for `GEOS5FP>=2.24.0`. |