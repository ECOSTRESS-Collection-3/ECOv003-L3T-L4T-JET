# ECOSTRESS Collection‑3 — Evapotranspiration (ET) Uncertainty Procedure

Version: 1.0  
Date: 2026-10-14  
Author: Generated from ECOSTRESS Collection‑3 documentation and code (ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET)

---

## Summary (one-line)
ETuncertainty in ECOSTRESS Collection‑3 is the inter‑model standard deviation across the ET estimates from the ensemble models (PT‑JPL‑SM, STIC‑JPL, PM‑JPL, BESS‑JPL), expressed in daily integrated units (mm day⁻¹) and stored as `ETuncertainty` in the L3T JET product.

---

## 1. Purpose and Rationale
- The Collection‑3 L3T JET product uses an ensemble of four evapotranspiration (ET) models to produce robust ET estimates.  
- The ensemble median (not mean) is used for the central ET estimate (`ETdaily`).  
- The standard deviation across the ensemble members is used as a pixelwise measure of uncertainty and is provided as `ETuncertainty` (units: mm day⁻¹).  
- This inter‑model spread is a descriptive metric of ensemble disagreement; it is not a full, propagated measurement error that accounts for all possible error sources (biases, correlated input errors, sampling error, etc.).

---

## 2. Inputs and component models
- Ensemble members (as used in Collection‑3):  
  - PT‑JPL‑SM (Priestley‑Taylor with soil moisture adjustments)  
  - STIC‑JPL  
  - PM‑JPL (MOD16‑style Penman–Monteith)  
  - BESS‑JPL (surface energy balance + photosynthesis)  
- Each model produces instantaneous latent heat flux (LE) in W m⁻² (and/or daily ET in mm day⁻¹ after upscaling).
- The pipeline upscales instantaneous latent heat fluxes (W m⁻²) to daily integrated ET (mm day⁻¹) for the `ETdaily` product; `ETuncertainty` is reported in the same daily units.

---

## 3. Central estimate: median and upscaling
- Central value used in product: the median of total latent heat flux across the ensemble models. The median is upscaled to daily ET and recorded as `ETdaily` (mm day⁻¹).  
- Upscaling formula (conceptual):
  - ET_daily (kg m⁻² day⁻¹ = mm day⁻¹) = (1 / λ) × ∫_sunrise^sunset LE(t) dt  
    - LE(t): latent heat flux [J s⁻¹ m⁻² = W m⁻²]  
    - λ: latent heat of vaporization for water ≈ 2.45 × 10^6 J kg⁻¹ (value depends slightly on temperature)
- Note: Because integration and linear conversion are linear operators, converting instantaneous LE to daily ET then taking medians or taking medians then integrating yields similar results up to differences introduced by nonlinearity in intermediate steps or if different models have different temporal structures. The product documentation indicates the median of latent heat fluxes is upscaled to produce the daily ET.

---

## 4. ETuncertainty: exact computation and formula
- Definition (as stated in the ATBD and User Guide):  
  "The standard deviation between these multiple estimates of ET is considered the uncertainty for the ECOSTRESS evapotranspiration product, as `ETuncertainty`."
- Practical pixelwise computation (per pixel):
  1. For pixel p, obtain ET_i(p) for each model i ∈ {1..n} expressed in mm day⁻¹ (either after per‑model integration or by converting instantaneous LE_i to daily ET_i). In Collection‑3 n = 4.
  2. Compute the sample standard deviation across the n values:
     - Sample standard deviation (unbiased estimator):
       σ(p) = sqrt( (1 / (n − 1)) * Σ_{i=1..n} (ET_i(p) − μ(p))² )
       where μ(p) = (1/n) Σ_{i=1..n} ET_i(p) (the ensemble mean).
     - Documentation uses the term "standard deviation" but does not explicitly state sample (n−1) vs population (n) normalization. With small ensembles, use of sample standard deviation (ddof=1) is conventional; the product team should confirm which variant is stored.
  3. Store σ(p) as `ETuncertainty(p)` (float32) in mm day⁻¹.
- Implementation note: in NumPy, the sample standard deviation is `np.std(values, ddof=1)`; the population version is `np.std(values, ddof=0)`.

---

## 5. Units and conversion (LE W m⁻² → ET mm day⁻¹)
- Instantaneous LE units: W m⁻² = J s⁻¹ m⁻².
- Integrate over daytime in seconds to obtain energy per m² per day: ∫ LE(t) dt [J m⁻² day⁻¹].
- Convert to mass of water (kg m⁻²) by dividing by λ (J kg⁻¹):
  ET_kg_m2_day = (1 / λ) × ∫_sunrise^sunset LE(t) dt
- Expressed in mm day⁻¹: 1 kg m⁻² = 1 mm, so:
  ET_mm_day = (1 / λ) × ∫_sunrise^sunset LE(t) dt
- If LE values are constant or if daytime seconds S_day is used with an average LĒ:
  ET_mm_day = (LĒ × S_day) / λ
  where S_day is the number of seconds between sunrise and sunset for that pixel and date.
- Latent heat of vaporization λ typical value: ≈ 2.45 × 10^6 J kg⁻¹ (weakly temperature dependent).

---

## 6. Interpretation of ETuncertainty
- ETuncertainty measures inter‑model spread (ensemble disagreement) at each pixel:
  - Small σ → models agree; larger σ → models disagree.
  - It is a descriptive metric and indicates reliability of the ensemble estimate insofar as model spread correlates with truth uncertainty.
- ETuncertainty does NOT:
  - Fully capture common systemic bias that all models share (all models could be wrong in the same direction with small σ).
  - Replace empirical validation (comparison to flux towers) for absolute error assessment.
  - Provide direct probabilistic confidence intervals for the true ET without assumptions about model error distributions and independence.

---

## 7. Relation to validation and performance metrics
- The Collection‑3 documentation reports ensemble validation against eddy covariance (EC) towers (AmeriFlux): typical daily RMSE ≤ 1.5 mm day⁻¹ and instantaneous RMSE ≤ ~60 W m⁻², with R² > 0.7 across many biomes.
- Product error target: ~1 mm day⁻¹ (target for water resource management applications). This target is an end‑to‑end accuracy objective, not the same as the ensemble spread `ETuncertainty`.
- Users should use ETuncertainty together with independent validation for site‑specific bias and absolute error quantification.

---

## 8. Practical product details (storage & metadata)
- Layer name: `ETuncertainty`
- Data type: float32
- Units: mm day⁻¹
- Location: L3T JET product bundle (see product table in README/User Guide)
- Complementary layers available in product:
  - `ETdaily` (ensemble median daily ET)  
  - Per‑model layers (e.g., `PTJPLSMdaily`, `STICJPLdaily`, `BESSJPLdaily`, `PMJPLdaily`) so users can inspect the component estimates directly
  - Quality masks: `cloud`, `water` (8‑bit)
- Recommended metadata fields to include (if not present):
  - `uncertainty.method` = "inter-model standard deviation"
  - `uncertainty.n_members` = 4
  - `uncertainty.units` = "mm day^-1"
  - `uncertainty.std_type` = "sample" or "population" (clarify which was used)
  - `uncertainty.latent_heat_lambda` = value used (J kg^-1)
  - `uncertainty.integration_window` = description (sunrise–sunset; how sunrise/sunset determined)

---

## 9. Limitations and caveats (users & data scientists)
- Small ensemble size (n=4) means the sample standard deviation has limited degrees of freedom; interpret pixelwise σ with caution.
- Common-mode errors (shared biases or input errors) can produce small σ but large absolute error versus truth.
- Sampling mismatches: flux towers measure over different footprints and times; therefore, validation RMSEs reflect additional scale/temporal mismatch uncertainties.
- Spatial/temporal correlation of errors is not represented; ETuncertainty is per pixel and does not provide spatial covariance or temporal persistence.
- ETuncertainty should be used as a relative indicator of reliability, not a complete uncertainty budget.

---

## 10. Recommended user practices
- Screen pixels by `ETuncertainty` to flag locations where models disagree, e.g., filter or weight analyses by σ threshold.
- Inspect per‑model layers to identify which model(s) cause high disagreement — remove or downweight outlier models if warranted for a particular biome or application.
- Combine ETuncertainty with validation comparisons to in‑situ flux towers for site-specific bias correction and calibration.
- For assimilation or formal uncertainty propagation, augment ETuncertainty with other error sources (input data errors, representativeness errors) and, if possible, use a statistical model that treats ensemble spread as one component of a hierarchical error model.

---

## 11. Implementation pseudocode (Python, conceptual)
```python
# ET_values: array-like of shape (n_models,) for a single pixel, in mm/day
import numpy as np

ET_values = np.array([ET_ptjplsm, ET_stic, ET_pmjpl, ET_bess])  # mm/day
n = ET_values.size

# 1) compute median daily ET (product ETdaily)
ETdaily = np.median(ET_values)

# 2) compute uncertainty as sample standard deviation (recommended for small n)
ETuncertainty_sample_std = np.std(ET_values, ddof=1)  # ddof=1 -> sample std

# 3) alternative: population std (ddof=0)
ETuncertainty_population_std = np.std(ET_values, ddof=0)

# store ETdaily and ETuncertainty_sample_std as float32 in product