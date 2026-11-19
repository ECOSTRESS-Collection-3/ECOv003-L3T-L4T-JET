# ECOSTRESS Collection 3 to Collection 4 Technical Road-Map

**Document ID:** ROADMAP-ECOSTRESS-L3T-L4T-C4  
**Target Systems:** `ECOv003-L3T-L4T-JET` (PGE & Granule Packaging), `JET3` (Core Science Algorithms), and `ECOv003_granules`  
**Status:** Proposed / Engineering Plan  

---

## 1. Executive Summary

Following the operational release of ECOSTRESS Version 3 Level-3 and Level-4 products at the NASA Land Processes Distributed Active Archive Center (LP DAAC) in May 2026, this road-map synthesizes three subsystem enhancement proposals—**Meteorology & Soil Moisture Downscaling**, **Instantaneous-to-Daily Upscaling**, and **Uncertainty Quantification**—into a unified, phased 24-month engineering plan for Collection 3+ maintenance updates and the Collection 4 baseline.

Collection 3 established Cloud-Optimized GeoTIFF (COG) packaging, unified auxiliary distribution (`L3T ETAUX`), per-model daily evapotranspiration (ET) layers (`PT-JPL-SM`, `STIC-JPL`, `PM-JPL`, `BESS-JPL`), and standardized daily units ($\text{mm day}^{-1}$) across `ETdaily`, `ETuncertainty`, and `PET`. Collection 4 transitions the science engine from empirical linear approximations, uniform daylight "boxcar" integration, and descriptive inter-model dispersion metrics to a physically constrained, energy-conserving, and probabilistically calibrated architecture.

---

## 2. Architectural Evolution: Collection 3 Baseline vs. Collection 4 Target

| Subsystem | Collection 3 Operational Baseline | Collection 4 Target Architecture | Primary Scientific & Product Impact |
| :--- | :--- | :--- | :--- |
| **Meteorology & Soil Moisture Downscaling (`L3T ETAUX`)** | Independent tile-wise Ordinary Least Squares (OLS) regression of GEOS-5 FP $T_a$, $RH$, and $SM$ against $ST$, NDVI, and albedo; coarse bias correction; bicubic cloud fill. | GEDI canopy-height aerodynamic resistance ($r_a$, $z_{0m}$) coupling; conservative actual vapor pressure ($e_a$) downscaling with psychrometric $RH$ recovery; spatially regularized regression (Ridge/GWR) with overlapping tile blending; Laplacian pyramid cloud blending. | Eliminates tile border seamlines, prevents non-physical $RH$/VPD violations via Clausius-Clapeyron consistency, and resolves sub-canopy microclimate decoupling. |
| **Instantaneous-to-Daily Upscaling (`L3T JET`)** | Uniform "boxcar" integration ($LE_{\text{inst}} \times t_{\text{daylight}} / L_v$) with fixed $L_v = 2.45 \times 10^6\,\text{J kg}^{-1}$ over astronomical daylight. | Temperature-dependent $L_v(T_{\text{surf}})$ and sublimation $L_s$; Evaporative Fraction ($EF$) scaling over diurnal available energy ($R_n - G$); afternoon VPD stomatal closure attenuation ($K_{\text{stress}}$); dual `ETdaily_daylight` and `ETdaily_24h` layers. | Removes ISS orbital-precession time-of-day bias (25–45% error at solar noon/edges), removes 1–4.5% thermal $L_v$ bias, and closes the 24-hour hydrologic budget. |
| **Ensemble Aggregation & Uncertainty (`L3T JET`)** | Unweighted pixelwise median across 4 models; `ETuncertainty` defined solely as sample standard deviation across the 4 daily outputs. | Biome- and aridity-stratified Bayesian Model Averaging (BMA); Knothe-Rosenblatt triangular transport maps for bounded non-Gaussian error propagation; Law of Total Variance decomposition (`input` + `structural` + `temporal`); exponential spatial covariance length scale ($L$). | Captures forcing/state errors (ERA5 EDA, SMAP TC, L2 LST noise), enforces physical bounds ($0 \le ET \le R_n - G$), and enables volumetric error aggregation over polygons and basins. |

---

## 3. Subsystem Synergy & Data-Flow Dependencies

The three upgrades form a coupled physical pipeline rather than independent patches, requiring sequential integration aligned with upstream-to-downstream data flow:

```text
+--------------------------------------------------------------------------------------+
| STAGE 1: Physics-Informed Downscaling (L3T ETAUX)                                    |
|  - GEDI Canopy Height -> Aerodynamic resistance (r_a) & roughness length (z_0m)      |
|  - Downscale conservative actual vapor pressure (e_a) -> Psychrometric RH & VPD      |
|  - Overlapping tile Ridge/GWR + Laplacian cloud fill -> Seam-free 70 m Ta, RH, SM    |
|  - Propagate input covariance Sigma_x (ERA5 EDA + SMAP TC + L2 LST sensor noise)     |
+------------------------------------------+-------------------------------------------+
                                           |
                                           v
+--------------------------------------------------------------------------------------+
| STAGE 2: Ensemble Energy Balance & Non-Gaussian Propagation (JET3 Models)            |
|  - Run PT-JPL-SM, STIC-JPL, PM-JPL, BESS-JPL (+ AquaSEBS over NASADEM water)         |
|  - Offline-trained Knothe-Rosenblatt Transport Maps yield per-model PDFs & sigma_in  |
|  - Biome/Aridity-stratified BMA weights combine model outputs                        |
+------------------------------------------+-------------------------------------------+
                                           |
                                           v
+--------------------------------------------------------------------------------------+
| STAGE 3: Diurnal Closure & Total Uncertainty Packaging (L3T JET / L4T Products)      |
|  - Dynamic L_v(T_surf) + Evaporative Fraction (EF) * Integral(Rn(t) - G(t)) dt       |
|  - Afternoon VPD hysteresis attenuation (K_stress) + Nocturnal LE integration        |
|  - Total Variance: sigma_total = sqrt(sigma_input^2 + sigma_structural^2 + sigma_t^2)|
|  - Serialize backward-compatible + new Collection 4 COG layers & JSON metadata       |
+--------------------------------------------------------------------------------------+
```

---

## 4. Phased Implementation Road-Map (24-Month Execution Plan)

```text
Quarter:     | Q1   Q2 | Q3   Q4 | Q5   Q6 | Q7   Q8 |
------------------------------------------------------
Phase 1:     |=========|         |         |         | Dynamic L_v, e_a Conservation & Input UQ
Phase 2:     |         |=========|         |         | Canopy Downscaling, Transport Maps & BMA
Phase 3:     |         |         |=========|         | EF/24h Closure & Total Variance Engine
Phase 4:     |         |         |         |=========| Global Cal/Val, Packaging & C4 Release
```

### Phase 1: Low-Risk Physical Fixes & Input Error Characterization (Months 1–6)
*Target Release: Collection 3.1 Maintenance Update & Offline Calibration Harness*

1. **Thermally Dynamic Latent Heat ($L_v$) & Shortwave Ratio Fallback (`JET3`):**
   - Replace constant `LATENT_VAPORIZATION_JOULES_PER_KILOGRAM = 2450000.0` with per-pixel temperature-dependent latent heat of vaporization:
     $$L_v(T_{\text{surf}}) = (2.501 - 0.002361 \, T_{\text{surf}}) \times 10^6 \quad [\text{J kg}^{-1}]$$
     and latent heat of sublimation $L_s = 2.834 \times 10^6 \text{ J kg}^{-1}$ when $T_{\text{surf}} < 0.0^\circ\text{C}$.
   - Implement shortwave solar radiation ratio ($R_{s,\text{day}} / R_{s,\text{inst}}$) scaling using hourly GEOS-5 FP radiation fields as an immediate step toward eliminating ISS overpass-timing bias.
2. **Conservative Vapor Pressure ($e_a$) Downscaling (`JET3`):**
   - Refactor `sharpen_meteorology_data` to downscale actual vapor pressure $e_a$ rather than $RH$ directly, recovering relative humidity via Clausius-Clapeyron saturation vapor pressure $RH = \text{clip}(e_a / e_s(T_a), 0, 1)$.
3. **Input Error Covariance Look-Up Tables & Benchmarking Harness:**
   - Characterize biome-stratified input error covariance matrices $\mathbf{\Sigma}_{\mathbf{x}}$ for $T_a$, $RH$, $VPD$, and $SM$ using ERA5 10-member Ensemble Data Assimilation (EDA) spreads and SMAP Triple Collocation (TC).
   - Build an automated validation harness across **75+ AmeriFlux / FLUXNET eddy covariance towers** spanning the 2018–2026 ECOSTRESS archive, stratified by overpass time bin (morning 07:00–10:00, solar noon 11:00–13:00, afternoon 14:00–17:00) and aridity index.

### Phase 2: Structural Downscaling & Surrogate UQ Training (Months 7–12)
*Target Release: `JET3` v4.0 Alpha & Pre-Trained Transport Map Library*

1. **Canopy-Coupled, Seam-Free Downscaling (`JET3`):**
   - Integrate `GEDI_directory` canopy height rasters (already wired into `L3TL4TJETConfig` and `JET()`) to parameterize aerodynamic roughness length ($z_{0m}$) and aerodynamic resistance ($r_a$) in $T_a$ downscaling.
   - Replace tile-isolated OLS with spatially regularized regression (Ridge / Geographically Weighted Regression) over buffered/overlapping MGRS tile neighborhoods and multi-scale Laplacian pyramid blending across `cloud_mask` boundaries.
2. **Offline Transport Map Training & BMA Weight Calibration:**
   - Train lower-triangular Knothe-Rosenblatt measure transport maps for `PT-JPL-SM`, `STIC-JPL`, `PM-JPL`, and `BESS-JPL` across IGBP land-cover classes and climate zones, enforcing $ET \ge 0$ and energy-balance upper bounds ($ET \le R_n - G$).
   - Verify $>500\times$ online inference speedup and quantile fidelity against $N = 10,000$ brute-force Monte Carlo simulations.
   - Fit biome- and aridity-conditioned Bayesian Model Averaging (BMA) weights $w_m(\text{IGBP}, \text{AI})$ against tower observations.

### Phase 3: Full Diurnal Closure & Total Variance Engine Integration (Months 13–18)
*Target Release: `ECOv004-L3T-L4T-JET` Integration Candidate*

1. **Evaporative Fraction ($EF$), Stomatal Hysteresis, & 24-Hour Closure (`JET3`):**
   - Transition daytime upscaling to sub-daily available energy integration:
     $$LE_{\text{daylight}} = EF_{\text{inst}} \int_{\text{sunrise}}^{\text{sunset}} \left[R_n(t) - G(t)\right] dt \cdot K_{\text{stress}}$$
     where $K_{\text{stress}}$ attenuates afternoon stomatal closure when $VPD_{\text{afternoon}} > VPD_{\text{overpass}}$.
   - Add nocturnal latent heat flux integration ($LE_{\text{night}}$) from sunset to next sunrise to produce `ETdaily_24h` alongside backward-compatible `ETdaily` (`ETdaily_daylight`).
2. **Law of Total Variance Engine (`JET3`):**
   - Compute total predictive uncertainty combining within-model propagated input variance, between-model BMA structural variance, and diurnal temporal extrapolation variance:
     $$\sigma_{\text{total}} = \sqrt{\sigma_{\text{input}}^2 + \sigma_{\text{structural}}^2 + \sigma_{\text{temporal}}^2}$$
   - Compute pixelwise exponential spatial error correlation length scales ($L$) to support polygon- and basin-scale volumetric error aggregation.
3. **PGE & Granule Writer Updates (`ECOv003-L3T-L4T-JET` / `ECOv003_granules`):**
   - Extend `ECOv003_L3T_L4T_JET.py` and `write_ECOv003_products.py` to unpack and serialize the new Collection 4 layers and standardized UQ/upscaling metadata fields while preserving existing Collection 3 layer names for downstream compatibility.

### Phase 4: Global Cal/Val, Packaging & Operational Release (Months 19–24)
*Target Release: ECOSTRESS Collection 4 Operational Production*

1. **Spread-Skill & Diurnal Bias Verification:**
   - Validate across global FLUXNET and AmeriFlux sites using Spread-Skill Reliability Diagrams and Continuous Ranked Probability Scores (CRPS).
   - Confirm achievement of quantitative performance targets:
     - Daily ET $\text{RMSE} < 0.9 \text{ mm day}^{-1}$ ($\ge 25\%$ reduction from Collection 3 baseline of $\sim 1.2 \text{ mm day}^{-1}$)
     - Diurnal overpass mean bias error $|\text{MBE}| < 0.2 \text{ mm day}^{-1}$
     - Coefficient of determination $R^2 \ge 0.85$ (up from $\sim 0.72$)
     - Calibrated $1\sigma$ empirical error containment ($\sim 68\%$)
2. **Documentation & Product Packaging:**
   - Package extended uncertainty layers into an optional auxiliary bundle (`L3T-JET-UQ`) if needed to manage standard granule storage footprint, update the ATBD and User Guide, and deliver operational Docker images to the ECOSTRESS Science Data System (SDS).

---

## 5. Target Product Schema Evolution (`L3T_JET`)

To maintain full backward compatibility with Collection 3 user pipelines while exposing the new physical capabilities, Collection 4 retains all Collection 3 layer names and appends the new fields:

| Layer Name | Status | Type | Units | Role in Collection 4 |
| :--- | :--- | :--- | :--- | :--- |
| `ETdaily` | Retained | `float32` | $\text{mm day}^{-1}$ | BMA daytime evapotranspiration (sunrise–sunset, backward compatible) |
| `ETdaily_24h` | **New** | `float32` | $\text{mm day}^{-1}$ | Full 24-hour hydrologic evapotranspiration (`ETdaily` + `ET_nocturnal`) |
| `ETuncertainty` | Upgraded | `float32` | $\text{mm day}^{-1}$ | Total $1\sigma$ uncertainty (Law of Total Variance + diurnal sampling error) |
| `ETuncertainty_input` | **New** | `float32` | $\text{mm day}^{-1}$ | Within-model propagated meteorological, soil moisture, and LST error |
| `ETuncertainty_structural` | **New** | `float32` | $\text{mm day}^{-1}$ | Between-model BMA structural disagreement |
| `ETquantile_10` / `ETquantile_90` | **New** | `float32` | $\text{mm day}^{-1}$ | Asymmetric 10th and 90th percentile bounds from transport map posterior PDF |
| `spatial_corr_length` | **New** | `float32` | $\text{km}$ | Spatial error correlation scale $L$ for polygon/basin volumetric aggregation |
| `PTJPLSMdaily`, `STICJPLdaily`, `BESSJPLdaily`, `PMJPLdaily` | Retained | `float32` | $\text{mm day}^{-1}$ | Constituent model daily ET layers (upgraded with dynamic $L_v$ & $EF$ scaling) |

---

## 6. Risk Assessment & Mitigation

| Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| Transport map training instability in extreme biomes | High | Low | Regularize polynomial coefficients; fall back to analytical First-Order Second-Moment (FOSM) Jacobians in fringe climates. |
| Memory and I/O overhead from additional raster layers | Medium | Medium | Distribute extended UQ layers as an optional auxiliary product bundle (`L3T-JET-UQ`), preserving standard granule size. |
| Inadequate tower coverage in tropical/high-latitude zones | Medium | High | Use clustered biome cross-validation and supplement with synthetic site simulations from coupled land-surface models. |
| Operational runtime increase from diurnal & UQ steps | High | Low | Pre-compile transport map evaluators into optimized C++/ONNX binaries and vectorize sub-daily GEOS-5 FP integrations. |

---

## 7. Immediate Repository Actions

1. **Add Road-Map to Documentation:** Place this document in `documentation/ECOSTRESS_Collection_3_to_4_Roadmap.md` alongside `documentation/ECOSTRESS_C2_vs_C3_Differences.md` to establish the full C2 $\rightarrow$ C3 $\rightarrow$ C4 lineage.