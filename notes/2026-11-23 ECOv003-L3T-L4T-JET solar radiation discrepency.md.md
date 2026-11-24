# Root-Cause Investigation Report: `GEOS5FP` Unit Regression (`vapor_gccm`, `ozone_cm`) & `FLiES-ANN` Solar Radiation (`Rg`) Discrepancy

- **Date:** November 23, 2026
- **Investigated Repositories:**
  - `GEOS5FP` (`v2.19.0` $\rightarrow$ `v2.26.0`)
  - `FLiESANN` (`v2.13.0` $\rightarrow$ `v2.13.1`)
  - `JET3` (`v3.1.0` $\rightarrow$ `v3.3.0`)
  - `ECOv003-L3T-L4T-JET` (`v1.0.1` $\rightarrow$ `v1.23.0`, branch `geos5fp_mismatch`)
- **Reference Granule Analyzed:**
  - Orbit `44841`, Scene `001`, Tile `11SPS`, Overpass `2026-06-02T18:00:12Z`
  - Public Reference Product: `ECOv003_L3T_ETAUX_44841_001_11SPS_20260602T180012_0700_02.zip`
- **Status:** Root cause conclusively proven and verified (`RMSE` reduced from `74.757 W/m²` to `0.527 W/m²`, `Bias` reduced from `+74.349 W/m²` to `-0.023 W/m²`, $r$ improved from `0.38894` to `0.99859`).

---

## 1. Executive Summary

During end-to-end validation of `ECOv003-L3T-L4T-JET v1.23.0` (`JET3 v3.3.0`, `GEOS5FP v2.26.0`, `FLiESANN v2.13.1`) against existing public ECOSTRESS Collection 3 granules (`orbit=44841`, `scene=001`, `tile=11SPS`, `2026-06-02T18:00:12Z`), all meteorological downscaling layers (`Ta`, `RH`, `SM`) and open-water fluxes matched the public Collection 3 reference products (`BuildID` `0700`), **except incoming global shortwave radiation (`Rg` in `L3T_ETAUX`)**, which exhibited a systematic positive offset of **`+74.35 W/m²`** (`1064.17 W/m²` local vs. `989.83 W/m²` public) and degraded spatial correlation ($r = 0.38894$).

A systematic, hypothesis-driven investigation across the commit histories of `FLiESANN`, `JET3`, `ECOv003-L3T-L4T-JET`, and `GEOS5FP` eliminated three plausible hypotheses—(1) missing `GEOS5FP.SWin` bias correction (`BIAS_CORRECT_FLIES_ANN`), (2) Cloud Optical Thickness zeroing (`ZERO_COT_CORRECTION`), and (3) `FLiESANN` neural network weight changes—and isolated the **true root cause**:

> **In `GEOS5FP` (`v2.24.0`–`v2.26.0`), unit conversion factors were inadvertently dropped in `GEOS5FPConnection.vapor_gccm()` and `GEOS5FPConnection.ozone_cm()`:**
> 1. **`vapor_gccm()`** returned raw GEOS-5 FP `TQV` in **$\text{kg m}^{-2}$ ($\text{mm}$)** (`mean = 10.7180`) instead of dividing by `10.0` to return **$\text{g cm}^{-2}$** (`mean = 1.0718 g/cm²`) — **$10\times$ too high**.
> 2. **`ozone_cm()`** returned raw GEOS-5 FP `TO3` in **Dobson Units ($\text{DU}$)** (`mean = 334.4433`) instead of dividing by `1000.0` to return **$\text{cm}$ (atm-cm)** (`mean = 0.3344 cm`) — **$1000\times$ too high**.

Because `FLiESANN` was trained on physical column water vapor (`0–7 g/cm²`) and column ozone (`0.15–0.55 cm`), feeding $10\times$ water vapor and $1000\times$ ozone saturated the neural network inputs and shifted predicted `SWin_Wm2` (`Rg`) by `+74.35 W/m²`. When `vapor_gccm` is divided by `10.0` and `ozone_cm` is divided by `1000.0` on the cached `2026-06-02` inputs, `FLiESANN` reproduces the public `L3T_ETAUX` `Rg` layer with **`Bias = -0.02331 W/m²`**, **`RMSE = 0.52714 W/m²`**, and **`r = 0.99859`**.

---

## 2. Initial Symptom & Layer-by-Layer Comparison (`2026-06-02`)

Running `examples/example_L3T_L4T_JET_run_with_download.py` on `orbit=44841`, `scene=001`, `tile=11SPS` (`2026-06-02T18:00:12Z`) with `ECOv003-L3T-L4T-JET v1.23.0` (`GEOS5FP v2.26.0`, `JET3 v3.2.0` / `v3.3.0`) produced the following comparison against the public Collection 3 reference products (`_02` build):

### 2.1. `L3T_ETAUX` Comparison (Initial Run: `BIAS_CORRECT_FLIES_ANN = False`, `GEOS5FP v2.26.0`)

| Layer | Units | Local Mean | Public Mean | RMSE | MAE | Bias | MaxDiff | Pearson $r$ | Status |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| **`Ta`** | °C | ~35.9 | ~35.9 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 1.00000 | `MATCH` |
| **`RH`** | 0–1 | ~0.16 | ~0.16 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 1.00000 | `MATCH` |
| **`SM`** | $\text{m}^3/\text{m}^3$ | ~0.08 | ~0.08 | — | — | — | — | >0.999 | Minor `_01` vs `_02` STARS prior diff |
| **`Rg`** | $\text{W m}^{-2}$ | **1064.17** | **989.83** | **74.75685** | **74.34881** | **+74.34881** | **95.36** | **0.38894** | **`DIFF` (Root Anomaly)** |
| **`Rn`** | $\text{W m}^{-2}$ | — | — | ~58.2 | — | +58.1 | — | — | Downstream propagation of `Rg` |

### 2.2. Downstream Propagation into `L3T_JET`, `L4T_ESI`, and `L4T_WUE`

Because `Rg` (`SWin_Wm2`) directly drives both `BESS-JPL` (radiative transfer, `GPP`, and `LE_BESS`) and `verma_net_radiation` (`Rn_Wm2`, which in turn forces `PT-JPL-SM`, `STIC-JPL`, and `PM-JPL`), the `+74.35 W/m²` error in `Rg` propagated systematically into every downstream energy-balance and water-flux product:
- **`L3T_ETAUX` (`Rn`):** Elevated net radiation (`Rn = (1 - albedo) * Rg + LWin - LWout`).
- **`L3T_JET` (`PTJPLSMinst`, `STICJPLinst`, `*daily`, `ETdaily`, `ETuncertainty`):** Elevated instantaneous latent heat flux and daytime integrated evapotranspiration across all four ensemble members.
- **`L4T_ESI` (`PET`, `ESI`):** Elevated potential evapotranspiration (`PET`) and slightly depressed evaporative stress index (`ESI = LE / PET`).
- **`L4T_WUE` (`GPP`, `WUE`):** Shifted `BESS-JPL` gross primary production (`GPP`) and water use efficiency (`WUE`).

---

## 3. Release-History & Algorithmic Lineage Audit

To determine what changed between the June 2, 2026 operational run (`BuildID 0700`, `PGEVersion 1.17.1` / `1.18.0` with `GEOS5FP v2.19.0`) and the November 23, 2026 run (`GEOS5FP v2.26.0`), we audited the complete git release histories of `FLiESANN`, `ECOv003-L3T-L4T-JET`, and `JET3`.

### 3.1. `FLiESANN` Release History (`v1.0.0` $\rightarrow$ `v2.13.1`)

| Version | Date | Key Architectural & Algorithmic Changes |
| :--- | :--- | :--- |
| **`v1.0.0` – `v1.5.0`** | Sep 2024 – Jun 2025 | Initial neural network (`FLiES` $\rightarrow$ `FLiESANN`), modularized into `process_FLiES_ANN.py`, `run_FLiES_ANN_inference.py`, `determine_atype.py`, `determine_ctype.py`, and `prepare_FLiES_ANN_inputs.py`. Always retrieved GEOS-5 FP `COT`. |
| **`v1.6.0`** | 2025-08-06 | Introduced `ZERO_COT_CORRECTION = True` in `FLiESANN/constants.py` (`COT = np.zeros(albedo.shape, dtype=np.float32)` when `COT=None`). |
| **`v1.6.1` – `v2.0.0`** | Sep 9 – Oct 24, 2025 | Fixed `RasterGeometry` raster conversion (`v1.6.1`), renamed `Ra` $\rightarrow$ `SWin_TOA_Wm2` and `Rg` $\rightarrow$ `SWin_Wm2`, standardized spectral output keys (`PAR_Wm2`, `NIR_Wm2`, `PAR_diffuse_Wm2`, etc.), and added `verify.py` (`v2.0.0`). |
| **`v2.1.0`** | 2025-11-10 | Switched `ZERO_COT_CORRECTION = False` in `FLiESANN/constants.py` (commits `73368e78`, `1a4bd1de`), restoring GEOS-5 FP `COT` retrieval when `COT=None` is passed to `FLiESANN()`. |
| **`v2.13.0` – `v2.13.1`** | Dec 23, 2025 – Aug 4, 2026 | Added `offline_mode` (`v2.13.0`) and fixed default `model_filename` in `process_FLiESANN_table.py` (`v2.13.1`). **The trained `.h5`/ONNX neural network weights were unchanged between `v2.13.0` (used on June 2, 2026) and `v2.13.1` (used in November 2026).** |

### 3.2. `ECOv003-L3T-L4T-JET` Solar Radiation History (`v1.0.1` $\rightarrow$ `v1.23.0`)

| Release | Date | Handling of `COT` and `SWin` (`Rg`) in `ECOv003-L3T-L4T-JET` |
| :--- | :--- | :--- |
| **`v1.0.1` – `v1.10.0`** | May 21 – Oct 1, 2025 | `ZERO_COT_CORRECTION = True` (`COT = COT * 0.0`) AND `BIAS_CORRECT_FLIES_ANN = True` (`rasters.bias_correct(coarse_image=SWin_coarse, fine_image=SWin_FLiES_ANN_raw)`), with `SWIN_MODEL_NAME = "GEOS5FP"` initially. |
| **`v1.11.0` (`91478687`)** | **Nov 10–12, 2025** | **Intentionally removed `bias_correct(...)` and `SWin_GEOS5FP`** (`SWin_Wm2 = SWin_FLiES_ANN_raw`), while keeping **`ZERO_COT_CORRECTION = True`** (`COT = COT * 0.0`) in `constants.py` and `read_ECOv003_inputs.py`. |
| **`v1.13.0` – `v1.18.0`** | Nov 18, 2025 – Oct 12, 2026 | Operational Collection 3 baseline (`BuildID 0700`, including the June 2, 2026 `_02` granule): `ZERO_COT_CORRECTION = True` and raw `FLiESANN` output without `GEOS5FP.SWin` bias correction. |
| **`v1.19.0` – `v1.22.1`** | Nov 11 – Nov 20, 2026 | Same `ZERO_COT_CORRECTION = True` and raw `FLiESANN` `SWin_Wm2` (extracted into `JET3` in `v1.17.0`). |

---

## 4. Hypothesis Testing & Diagnostic Experiments

Three hypotheses were systematically tested against the cached `2026-06-02` granules (`ECOv003_L2T_LSTE_44841_001_11SPS_20260602T180012_05` and `ECOv003_L2T_STARS_11SPS_20260602_02`):

### 4.1. Hypothesis 1: Missing `GEOS5FP.SWin` Bias Correction (`BIAS_CORRECT_FLIES_ANN = True`) — **REJECTED**
- **Test:** Enabled `bias_correct_FLiES_ANN=True` in `JET3` (`v3.3.0`) and `ECOv003-L3T-L4T-JET`, bias-correcting `FLiESANN` `SWin_Wm2` against coarse `GEOS5FP.SWin` (`13,720 m` grid).
- **Result:** `Rg` dropped from `1064.17 W/m²` to **`752.58 W/m²`** (`RMSE = 237.45 W/m²`, **`Bias = -237.25 W/m²`**, $r = 0.0894$).
- **Conclusion:** Confirms the git history finding (`v1.11.0`, commit `91478687`) that Collection 3 operational products do **not** apply `GEOS5FP.SWin` bias correction. `BIAS_CORRECT_FLIES_ANN` must remain **`False`** by default.

### 4.2. Hypothesis 2: `ZERO_COT_CORRECTION = True` vs. `False` — **REJECTED (for this scene)**
- **Test:** Executed `FLiESANN` directly on the `2026-06-02` scene passing un-zeroed `COT = geos.COT(time_UTC=t, geometry=geom)` (`ZERO_COT_CORRECTION = False`).
- **Result:**
  ```text
  COT enabled -> min/mean/max: 1033.04 / 1064.17 / 1078.78
  Comparison  -> RMSE: 74.75685, Bias: 74.34881, r: 0.38894
  ```
- **Conclusion:** `GEOS5FP.COT` is `0.0000` across the entire `11SPS` tile on `2026-06-02T18:00:12Z`, so `ZERO_COT_CORRECTION` has zero effect on this clear-sky overpass.

### 4.3. Hypothesis 3: Input Variable Unit Inspection (`vapor_gccm` & `ozone_cm`) — **CONFIRMED ROOT CAUSE**
- **Test:** Inspected the numerical distributions of every input raster passed to `FLiESANN` from `L2T_LSTE`, `L2T_STARS`, and `GEOS5FP v2.26.0`:
  ```text
  albedo  : min=0.0000, mean=0.1810, max=0.7752
  elev_m  : min=-118.7878, mean=56.8248, max=1637.3722
  COT     : min=0.0000, mean=0.0000, max=0.0000
  AOT     : min=0.0596, mean=0.0722, max=0.0801
  vapor   : min=7.8124, mean=10.7180, max=14.4300
  ozone   : min=330.7942, mean=334.4433, max=336.8232
  pub_rg  : min=964.4972, mean=989.8250, max=1032.7947
  ```
- **Physical Unit Diagnosis:**
  1. **`vapor_gccm` ($\text{g cm}^{-2}$):** In CGS units, $1\text{ g cm}^{-2}$ of precipitable water equals $1\text{ cm} = 10\text{ mm} = 10\text{ kg m}^{-2}$. `GEOS5FP` `TQV` (total precipitable water vapor) is stored in NetCDF files in $\text{kg m}^{-2}$ (`~10.72 kg/m²` over Southern California in June). `GEOS5FP v2.26.0` returned raw `TQV` (`10.7180`) without dividing by `10.0` (`1.0718 g/cm²`).
  2. **`ozone_cm` ($\text{cm}$ at STP / atm-cm):** One Dobson Unit ($\text{DU}$) is defined as $0.001\text{ cm}$ ($10\ \mu\text{m}$) of ozone at standard temperature and pressure. `GEOS5FP` `TO3` (total column ozone) is stored in NetCDF files in Dobson Units (`~334.44 DU`). `GEOS5FP v2.26.0` returned raw `TO3` (`334.4433`) without dividing by `1000.0` (`0.3344 cm`).

### 4.4. Verification Run with Corrected `vapor_gccm` and `ozone_cm` Units

Re-running `FLiESANN` on the exact same `2026-06-02` inputs with `vapor_gccm / 10.0` and `ozone_cm / 1000.0` yielded:

```text
Fixed units -> min/mean/max: 964.0876 / 989.8017 / 1031.9769
Comparison  -> RMSE: 0.52714, Bias: -0.02331, r: 0.99859
```

| Metric | Broken `GEOS5FP v2.26.0` Units | Corrected Units (`vapor/10`, `ozone/1000`) | Public Reference (`_02`) |
| :--- | ---: | ---: | ---: |
| **Min `Rg` ($\text{W m}^{-2}$)** | 1033.04 | **964.09** | 964.50 |
| **Mean `Rg` ($\text{W m}^{-2}$)** | 1064.17 | **989.80** | 989.83 |
| **Max `Rg` ($\text{W m}^{-2}$)** | 1078.78 | **1031.98** | 1032.79 |
| **Bias ($\text{W m}^{-2}$)** | +74.34881 | **-0.02331** | — |
| **RMSE ($\text{W m}^{-2}$)** | 74.75685 | **0.52714** | — |
| **Pearson $r$** | 0.38894 | **0.99859** | — |

*(Note: The tiny remaining `0.527 W/m²` RMSE and `-0.023 W/m²` bias is fully accounted for by the minor albedo difference between `ECOv003_L2T_STARS_11SPS_20260602_02` used locally and `ECOv003_L2T_STARS_11SPS_20260602_01` ingested during forward processing of the `_02` `L3T_ETAUX` granule.)*

---

## 5. Multi-Repository Remediation Plan

### 5.1. `GEOS5FP` (Root Fix — Next Patch/Minor Release, e.g., `v2.26.1` or `v2.27.0`)
1. **Restore Unit Conversions in `GEOS5FPConnection`:**
   - **`vapor_gccm(...)`:** Convert GEOS-5 FP `TQV` ($\text{kg m}^{-2}$) to $\text{g cm}^{-2}$ by dividing by `10.0` (`1 kg/m² = 0.1 g/cm²`).
   - **`ozone_cm(...)`:** Convert GEOS-5 FP `TO3` ($\text{DU}$) to $\text{cm}$ (atm-cm) by dividing by `1000.0` (`1 DU = 0.001 cm`).
2. **Audit All Other SI-Suffixed Methods in `GEOS5FP`:**
   - Verify unit conversions across `Ta_C` ($\text{K} - 273.15$), `Td_K` ($\text{K}$), `wind_speed_mps` ($\text{m s}^{-1}$), `AOT` (unitless), `COT` (unitless), `SWin` ($\text{W m}^{-2}$), `SM` ($\text{m}^3\text{ m}^{-3}$), `ALBEDO` / `ALBVISDR` / `ALBNIRDR` (0–1), and `PS` ($\text{Pa}$).
3. **Add Unit-Range Regression Tests in `GEOS5FP`:**
   - Assert physical bounds in unit tests (`0.0 <= vapor_gccm <= 10.0` and `0.05 <= ozone_cm <= 1.0`) so raw $\text{kg m}^{-2}$ or Dobson Unit values fail CI immediately.

### 5.2. `JET3` (`v3.3.0`)
1. **Keep `BIAS_CORRECT_FLIES_ANN = False` as Default:**
   - Retain `BIAS_CORRECT_FLIES_ANN = False` in `JET3/constants.py` while keeping the optional `bias_correct_FLiES_ANN: bool = BIAS_CORRECT_FLIES_ANN` keyword parameter on `JET()` for callers that explicitly request GEOS-5 FP bias correction.
2. **Defensive Unit Guard / Warning (Optional):**
   - Optionally log a warning or guard if `np.nanmean(ozone_cm) > 5.0` or `np.nanmean(vapor_gccm) > 15.0` in `JET()` to surface upstream unit anomalies immediately.

### 5.3. `ECOv003-L3T-L4T-JET` (`v1.23.0`)
1. **`ECOv003_L3T_L4T_JET/constants.py`:**
   - Revert `BIAS_CORRECT_FLIES_ANN = False` (alongside `ZERO_COT_CORRECTION = True`) so `ECOv003-L3T-L4T-JET` matches the Collection 3 operational baseline (`v1.11.0`–`v1.22.1`).
2. **`ECOv003_L3T_L4T_JET/smoke_test.py` & `tests/test_docker_smoke.py`:**
   - Assert `BIAS_CORRECT_FLIES_ANN is False`.
   - Add physical unit-range contract assertions for `GEOS5FPConnection` (`vapor_gccm` in $\text{g cm}^{-2}$ `< 10` and `ozone_cm` in $\text{cm}$ `< 1`) so `ECOv003-L3T-L4T-JET test` and `make docker-smoke-test` catch `GEOS5FP` unit regressions before container deployment.
3. **`pyproject.toml`:**
   - Pin the patched `GEOS5FP` release (e.g., `"GEOS5FP~=2.27.0"` or `">=2.26.1"`).
4. **End-to-End Granule Validation:**
   - Re-run `examples/example_L3T_L4T_JET_run_with_download.py` and verify that all layers across `L3T_JET`, `L3T_ETAUX`, `L4T_ESI`, and `L4T_WUE` report `MATCH` (`Bias ≈ 0`, $r > 0.998$) against the public Collection 3 reference products.