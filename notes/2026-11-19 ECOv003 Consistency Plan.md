# ECOSTRESS Collection 3 (`ECOv003-L3T-L4T-JET`) Internal Consistency Plan

**Date:** November 19, 2026  
**Target Repository:** `ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET` (v1.20.3)  
**Operational Constraint:** Collection 3 Science & Output Schema Freeze  

---

## 1. Executive Summary & Guiding Principle

Because ECOSTRESS Collection 3 is currently in operational production at the NASA Land Processes Distributed Active Archive Center (LP DAAC), any modification that alters pixel values, raster layer names, units, or file formats risks introducing temporal discontinuities into the archive or breaking downstream user pipelines.

Accordingly, this plan enforces a **Science & Output Schema Freeze** for Collection 3:
- **Preserve operational product outputs** (`RN_MODEL_NAME = "verma"`, `downsampling = "linear"`, existing COG layer names/units, and `.png` browse previews).
- **Fix non-breaking runtime bugs** (template placeholder substitution, path ordering, collection dispatch, and redundant disk I/O).
- **Align documentation and metadata** (`README.md`, ATBD, User Guide, and Road-Map) so they accurately reflect the operational Collection 3 software.
- **Add automated CI guardrails** to prevent future drift between code, configuration templates, dependencies, and documentation.
- **Defer algorithm changes** (`verma` $\rightarrow$ `BESS` net radiation unification, advanced cloud filling) to Collection 4.

---

## 2. Inventory of Identified Inconsistencies

### 2.1 Code, Configuration & Packaging Issues
1. **`SRTM_directory` handling mismatch:** `ECOv003_L3T_L4T_JET/L3T_L4T_JET.xml` defines `<scalar name="L3T_L4T_SRTM">SRTM_directory</scalar>`, and `generate_L3T_L4T_JET_runconfig.py` accepts `SRTM_directory` as an argument, but never performs `.replace("SRTM_directory", SRTM_directory)`. Meanwhile, `L3TL4TJETConfig.py` and `read_ECOv003_configuration.py` ignore `L3T_L4T_SRTM` entirely because the water mask is read from `L2T_LSTE`.
2. **Broken `ECOv003` dispatch & path order in `generate_L3T_L4T_JET_runconfig.py`:**
   - Imports `L2TLSTE` exclusively from `ECOv002_granules`, failing on `ECOv003` input filenames (unlike `read_ECOv003_configuration.py` and `read_ECOv003_inputs.py`, which check `"ECOv003"` vs. `"ECOv002"`).
   - Evaluates `runconfig_filename = join(working_directory, ...)` *before* defaulting `working_directory = granule_ID` when `working_directory is None`, causing a `TypeError`.
3. **Triple disk reads of `L2T_LSTE`:** `L2T_LSTE_filename` is opened three separate times during a single scene execution (`L3TL4TJETConfig.__init__`, `read_ECOv003_configuration`, and `read_ECOv003_inputs`).
4. **Dead CLI/API parameter (`save_intermediate`):** Defined in `L3T_L4T_JET()` and `--save-intermediate` in `build_parser()`, but never referenced in the function body.
5. **Packaging & test drift:**
   - `pyproject.toml` lists `"pytest"` twice under `[project.optional-dependencies].dev`.
   - `Dockerfile` runs `COPY pyproject.toml /app/pyproject.toml` immediately after `COPY . /app/`.
   - `tests/test_import_dependencies.py` omits five runtime dependencies declared in `pyproject.toml` (`monte_carlo_sensitivity`, `skl2onnx`, `solar_apparent_time`, `pytictoc`, `ECOv002_calval_tables`), and `smoke_test.py` checks only a 6-package subset.

### 2.2 Documentation & Product Specification Discrepancies
1. **Net radiation (`Rn`) model:** `constants.py` sets `RN_MODEL_NAME = "verma"`, whereas `README.md`, `ECOv003_L3_L4_JET_ATBD.md`, `ECOv003_L3_L4_JET_User_Guide.md`, and `ECOSTRESS Collection 2 to 3 Changes.md` state that `Rn` is computed by `BESS-JPL`.
2. **Cloud-fill resampling method:** Documentation states that cloudy pixels in downscaled `Ta`, `RH`, and `SM` are filled via **bicubic** resampling, whereas `ECOv003_L3T_L4T_JET.py` defaults to `downsampling = "linear"`.
3. **Missing layer in ATBD Table 3 (`L3T JET`):** `ECOv003_L3_L4_JET_User_Guide.md` Table 4 lists 14 layers including `STICJPLinst` ($\text{W m}^{-2}$), and `write_ECOv003_products.py` passes `LE_instantaneous_STICJPL_Wm2` to `write_L3T_JET`, but `ECOv003_L3_L4_JET_ATBD.md` Table 3 omits `STICJPLinst`.
4. **Incorrect units/bounds in documentation tables:**
   - `README.md` Table 2 (`L3T ETAUX`) lists `Rn` units as `Ratio` instead of `W/m^2`.
   - `ATBD` Table 5 and `User Guide` Table 6 (`L4T WUE`) list `Valid Max = 1` for `WUE` ($\text{g C kg}^{-1}\text{ H}_2\text{O}$), a copy-paste error from `ESI`.
5. **Browse image format & metadata examples:** `L3TL4TJETConfig.py` outputs `.png` granule browse previews (`DEFAULT_BUILD = "0700"`), while docs reference `.jpeg` browse images and sample JSON metadata with `"BuildID": "0800"` and `"PGEVersion": "v1.10.12"`.
6. **Document structure & filename drift:**
   - `ECOv003_L3_L4_JET_User_Guide.md` TOC lists `2. L2T STARS NDVI & Albedo Product`, while the body heading uses `and` and has no content.
   - `ECOSTRESS Collection 3 to 4 Road-Map.md` (Section 7) references underscored filenames (`ECOSTRESS_Collection_3_to_4_Roadmap.md` and `ECOSTRESS_C2_vs_C3_Differences.md`) rather than the actual space-separated filenames in `documentation/`.

---

## 3. Phased Implementation Plan

### Phase 1: Non-Breaking Bug Fixes & Code Hygiene (Zero Product Impact)
*Goal: Resolve runtime defects and packaging redundancies without altering output rasters or filenames.*

| Task | Target File(s) | Action |
| :--- | :--- | :--- |
| **1.1 Fix runconfig generator path order** | `ECOv003_L3T_L4T_JET/generate_L3T_L4T_JET_runconfig.py` | Initialize `working_directory = granule_ID` *before* constructing `runconfig_filename`, `output_directory`, `sources_directory`, `static_directory`, and `log_filename`. |
| **1.2 Support `ECOv003` & `ECOv002` in runconfig generator** | `ECOv003_L3T_L4T_JET/generate_L3T_L4T_JET_runconfig.py` | Dispatch `L2TLSTE` loading based on `"ECOv003"` vs. `"ECOv002"` in `basename(L2T_LSTE_filename)`, matching `read_ECOv003_configuration.py`. |
| **1.3 Reconcile `SRTM_directory`** | `generate_L3T_L4T_JET_runconfig.py`, `L3TL4TJETConfig.py`, `L3T_L4T_JET.xml` | Either add `template = template.replace("SRTM_directory", SRTM_directory)` and parse/log `L3T_L4T_SRTM` in `L3TL4TJETConfig` for SDS schema compatibility, or deprecate it cleanly if unused by SDS workflows. |
| **1.4 Reuse loaded `L2T_LSTE_granule`** | `L3TL4TJETConfig.py`, `read_ECOv003_configuration.py`, `read_ECOv003_inputs.py` | Store `self.L2T_LSTE_granule` on `L3TL4TJETConfig` and pass it into `read_ECOv003_inputs()` so the granule is opened once per run instead of three times. |
| **1.5 Deprecate or wire `save_intermediate`** | `ECOv003_L3T_L4T_JET/ECOv003_L3T_L4T_JET.py` | Map `save_intermediate=True` to `save_diagnostics=True` with a `DeprecationWarning` log message so existing CLI calls remain backward compatible without silently doing nothing. |
| **1.6 Deduplicate `pyproject.toml` & `Dockerfile`** | `pyproject.toml`, `Dockerfile` | Remove the duplicate `"pytest"` entry in `[project.optional-dependencies].dev` and remove the redundant `COPY pyproject.toml /app/pyproject.toml` line in `Dockerfile`. |
| **1.7 Synchronize dependency tests** | `tests/test_import_dependencies.py`, `ECOv003_L3T_L4T_JET/smoke_test.py` | Update `dependencies` in `test_import_dependencies.py` to cover all packages in `pyproject.toml` (`monte_carlo_sensitivity`, `skl2onnx`, `solar_apparent_time`, `pytictoc`, `ECOv002_calval_tables`). |

---

### Phase 2: Documentation & Specification Alignment
*Goal: Update all documentation to accurately reflect the deployed Collection 3 behavior.*

| Task | Target File(s) | Action |
| :--- | :--- | :--- |
| **2.1 Document operational `Rn` model** | `README.md`, `ECOv003_L3_L4_JET_ATBD.md`, `ECOv003_L3_L4_JET_User_Guide.md`, `ECOSTRESS Collection 2 to 3 Changes.md` | Clarify that Collection 3 operational `Rn` is computed by the **Verma net radiation model** (`RN_MODEL_NAME = "verma"`), while BESS-JPL produces GPP and its constituent ET estimate. |
| **2.2 Document operational cloud-fill resampling** | `README.md`, `ECOv003_L3_L4_JET_User_Guide.md` | Update cloud-fill descriptions for downscaled `Ta`, `RH`, and `SM` from "bi-cubically resampled" to **bilinearly resampled** (`downsampling = "linear"`) GEOS-5 FP. |
| **2.3 Fix `L3T ETAUX` `Rn` units** | `README.md` (Table 2) | Change `Rn` units from `Ratio` to `W/m^2` to match `ECOv003_L3_L4_JET_User_Guide.md` Table 3. |
| **2.4 Add `STICJPLinst` to ATBD** | `ECOv003_L3_L4_JET_ATBD.md` (Table 3) | Add `STICJPLinst` (`float32`, `W/m^2`) to the `L3T JET` layer table so all 14 layers written by `write_ECOv003_products.py` match `User Guide` Table 4. |
| **2.5 Fix `L4T WUE` valid range** | `ECOv003_L3_L4_JET_ATBD.md` (Table 5), `ECOv003_L3_L4_JET_User_Guide.md` (Table 6) | Change `Valid Max` for `WUE` from `1` to `N/A` (or its physical upper limit). |
| **2.6 Align browse format & metadata examples** | `README.md`, `ECOv003_L3_L4_JET_User_Guide.md`, `ECOSTRESS Collection 2 to 3 Changes.md` | Clarify that granule-level browse previews are `.png` while per-layer COG browse renderings are `.jpeg` (per `ECOv003_granules`), and align `README.md` JSON example fields (`BuildID`, `PGEVersion`, `SISName`) with `constants.py` and `read_ECOv003_inputs.py`. |
| **2.7 Resolve User Guide stub & Road-Map filenames** | `ECOv003_L3_L4_JET_User_Guide.md`, `ECOSTRESS Collection 3 to 4 Road-Map.md` | Populate or remove the empty Section 2 (`L2T STARS NDVI & Albedo Product`) in the User Guide so TOC and headings match, and update Section 7 of the Road-Map to match actual filenames in `documentation/`. |

---

### Phase 3: Automated Consistency Guardrails in CI
*Goal: Add automated tests so code, templates, and docs cannot drift apart in future commits.*

1. **Create `tests/test_consistency.py`:**
   - **Template round-trip test:** Call `generate_L3T_L4T_JET_runconfig()` with mock `ECOv002` and `ECOv003` granule filenames (including `working_directory=None`), parse the generated XML with `L3TL4TJETConfig`, and assert zero unsubstituted placeholder tokens remain.
   - **Dependency parity test:** Parse `[project].dependencies` from `pyproject.toml` and verify every runtime dependency is represented in `tests/test_import_dependencies.py`.
   - **Documentation & constant parity test:** Assert that `DEFAULT_BUILD`, `RN_MODEL_NAME`, and the product layers passed in `write_ECOv003_products.py` are consistent with the layer tables in `ECOv003_L3_L4_JET_ATBD.md` and `ECOv003_L3_L4_JET_User_Guide.md`.
2. **Verify PDF build assets:** Ensure `documentation/pandoc_table_header.tex` is tracked in git so `make compile-documentation` executes cleanly.

---

### Phase 4: Defer Science Changes to Collection 4
*Goal: Keep Collection 3 science deterministic while tracking algorithm unifications for Collection 4.*

- Retain `RN_MODEL_NAME = "verma"` and `downsampling = "linear"` as frozen Collection 3 defaults.
- Log the `verma` $\rightarrow$ `BESS-JPL` net radiation switch and bicubic/Laplacian cloud-fill upgrades in `documentation/ECOSTRESS Collection 3 to 4 Road-Map.md` under Phase 1/Phase 2 so they are calibrated and validated alongside the Collection 4 ensemble and uncertainty upgrades.

---

## 4. Verification Checklist

- [ ] `pytest -vv` passes all existing and new `test_consistency.py` checks on Python 3.12 and 3.13.
- [ ] `ECOv003-L3T-L4T-JET test` and `docker build --target smoke-test` succeed cleanly.
- [ ] Regression run on a reference `ECOv003` tile confirms bit-for-bit identical output GeoTIFFs, JSON metadata, and filenames compared to pre-cleanup `v1.20.3`.
- [ ] `make compile-documentation` renders both the ATBD and User Guide PDFs without missing headers or broken links.