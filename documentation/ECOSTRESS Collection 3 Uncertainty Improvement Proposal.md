# Proposal: Development Strategy for Next-Generation Uncertainty Quantification in ECOSTRESS

**Document ID:** PROP-ECOSTRESS-UQ-2026-V1  
**Target Milestone:** ECOSTRESS Collection-4 / L3T-JET Pipeline Enhancement  
**Status:** Technical Architecture & Implementation Proposal  

---

## Executive Summary

The ECOSTRESS Collection-3 L3T JET product quantifies evapotranspiration (ET) uncertainty via `ETuncertainty`, defined operationally as the pixelwise sample standard deviation across four ensemble members (PT-JPL-SM, STIC-JPL, PM-JPL, and BESS-JPL) in units of mm day⁻¹[cite: 1]. While this inter-model spread provides a descriptive diagnostic of algorithmic disagreement, it does not constitute a rigorous, propagated physical error budget[cite: 1]. It treats input meteorological drivers and soil states deterministically, omits within-model parametric variance, assumes symmetric Gaussian error on non-negative physical quantities, and lacks spatial error covariance[cite: 1].

This proposal outlines a development strategy to transition ECOSTRESS uncertainty quantification (UQ) from a four-point descriptive dispersion metric to an end-to-end, physically bounded, total uncertainty architecture. The strategy couples:
1. **Input Uncertainty Characterization:** Formulating joint, physically constrained error distributions for air temperature ($T_a$), relative humidity ($RH$), vapor pressure deficit ($VPD$), and soil moisture ($SM$).
2. **Non-Gaussian Propagation via Transport Maps:** Deploying triangular measure transport (Knothe-Rosenblatt rearrangements) to propagate bounded, nonlinearly coupled input errors to ET predictive distributions without per-pixel Monte Carlo latency.
3. **Law of Total Variance Ensemble Decomposition:** Separating within-model input/parametric uncertainty from between-model structural uncertainty within a Bayesian Model Averaging (BMA) framework.
4. **Diurnal and Spatial Error Structuring:** Incorporating diurnal upscaling bounds and spatial covariance kernels for field-to-basin aggregation.
5. **Spread-Skill Empirical Calibration:** Grounding ensemble spread against AmeriFlux and FLUXNET eddy covariance networks[cite: 1].

---

## 1. Baseline Assessment & Gap Analysis

The Collection-3 baseline architecture generates daily ET (`ETdaily`) by taking the ensemble median of instantaneous latent heat flux ($LE$, W m⁻²) across four algorithms and scaling it over the daytime integration period divided by the latent heat of vaporization ($\lambda \approx 2.45 \times 10^6\text{ J kg}^{-1}$)[cite: 1]. The accompanying uncertainty (`ETuncertainty`) is computed per pixel as[cite: 1]:

$$\sigma(p) = \sqrt{\frac{1}{n - 1} \sum_{i=1}^{n} \left(ET_i(p) - \mu(p)\right)^2}, \quad n = 4 \text{[cite: 1]}$$

### Identified Deficiencies in Collection-3 UQ
* **Neglect of Forcing and State Uncertainty:** Reanalysis meteorology (e.g., GEOS-FP, ERA5) and microwave soil moisture inputs (SMAP) carry substantial uncertainty that is ignored in the forward runs[cite: 1].
* **High Sampling Variance ($n = 4$):** Estimating standard deviation with only 3 degrees of freedom creates noisy pixelwise fields susceptible to single-model outliers[cite: 1].
* **Shared Common-Mode Failure:** If all four algorithms receive biased input drivers (e.g., underestimated $VPD$ or incorrect net radiation $R_n$), the ensemble spread can collapse to near zero while absolute error against flux towers remains severe[cite: 1].
* **Non-Gaussian and Bounded Violations:** Evapotranspiration is bounded ($ET \ge 0$, capped by available energy $R_n - G$). Assigning a symmetric standard deviation $\sigma$ produces non-physical confidence intervals in arid and hyper-arid regimes.
* **Absence of Spatial and Temporal Covariance:** `ETuncertainty` is strictly independent per pixel, preventing accurate volumetric error aggregation over agricultural management zones, sub-basins, or irrigation districts[cite: 1].

---

## 2. Technical Pillars of the Development Strategy

    +-----------------------------------------------------------------------------------+
    |                           ECOSTRESS Next-Gen UQ Architecture                      |
    +-----------------------------------------------------------------------------------+
                                              |
         +------------------------------------+-----------------------------------+
         |                                                                        |
         v                                                                        v
    [Pillar 1: Input Joint Manifolds]                           [Pillar 2: Transport Maps Propagation]
    - Ta, RH, VPD, SM Distributions                              - Lower-triangular Knothe-Rosenblatt Map
    - Thermodynamic Covariance (Clausius-Clapeyron)              - Enforces non-negative support & bounds
    - Triple Collocation & Reanalysis EDA Spreads                - Offline Training / Millisecond Online Evaluation
         |                                                                        |
         +------------------------------------+-----------------------------------+
                                              |
                                              v
                        [Pillar 3: Total Variance & Adaptive Ensemble]
                        - Law of Total Variance (Within- vs Between-Model)
                        - Biome-conditioned Bayesian Model Averaging (BMA)
                                              |
         +------------------------------------+-----------------------------------+
         |                                                                        |
         v                                                                        v
    [Pillar 4: Spatial & Diurnal Structuring]                   [Pillar 5: Empirical In-Situ Calibration]
    - Diurnal upscaling parameter bounds                         - AmeriFlux / FLUXNET tower benchmarking[cite: 1]
    - Exponential spatial covariance kernels                     - Spread-error reliability diagrams
    +-----------------------------------------------------------------------------------+

### Pillar 1: Input Uncertainty Characterization & Joint Thermodynamic Manifolds
* **Air Temperature ($T_a$) and Vapor Pressure Deficit ($VPD$):**
  * Extract pixel-level variance from reanalysis ensemble data assimilation (EDA) spreads (e.g., ERA5 10-member ensemble).
  * Couple $T_a$ and $RH$ uncertainties through saturation vapor pressure $e_s(T_a)$ to preserve relative and specific humidity bounds, preventing unphysical supersaturation.
* **Surface Soil Moisture ($SM$):**
  * Derive spatially varying error variances for downscaled microwave soil moisture products using triple collocation (TC) against in-situ sensor networks (ISMN, Cosmic-Ray Soil Moisture Observing System).
  * Enforce Dirichlet or Beta distributions bounded by residual water content $\theta_r$ and saturated porosity $\theta_s$.
* **Radiative Drivers & Level-2 LST:**
  * Propagate Level-2 LST sensor noise and atmospheric correction error directly into the available energy ($R_n - G$) boundary conditions.

### Pillar 2: Measure Transport (Transport Maps) for Nonlinear Propagation
To avoid running thousands of Monte Carlo iterations per 70 m pixel across regional swaths, non-Gaussian propagation is executed using triangular transport maps.

1. **Mathematical Structure:**
   A lower-triangular Knothe-Rosenblatt map $\mathbf{T}: \mathbb{R}^d \to \mathbb{R}^d$ pushes forward an isotropic standard normal reference $\eta(\mathbf{z}) = \mathcal{N}(\mathbf{0}, \mathbf{I})$ to the joint target density $\pi(\mathbf{x}, ET)$ where $\mathbf{x} = [T_a, RH, SM]^T$:
   $$\mathbf{T}(\mathbf{z}) = \begin{bmatrix} T_1(z_1) \\ T_2(z_1, z_2) \\ T_3(z_1, z_2, z_3) \\ T_4(z_1, z_2, z_3, z_4) \end{bmatrix} = \begin{bmatrix} T_a \\ RH \\ SM \\ ET \end{bmatrix}, \quad \frac{\partial T_i}{\partial z_i} > 0$$
2. **Enforcing Physical Constraints:**
   The output components are parameterized using integrated positive expansions (such as monotonic radial basis functions or neural operators with softplus activations), guaranteeing:
   * $ET \ge 0$ under all conditions.
   * Asymmetric tail sensitivity reflecting water-stress thresholds (stomatal shutdown under extreme $VPD$ or dry soil).
3. **Decoupled Operational Architecture:**
   * **Offline Training:** Models (PT-JPL-SM, STIC-JPL, PM-JPL, BESS-JPL) are sampled across plant functional types (PFTs) and climate zones to train map parameters[cite: 1].
   * **Online Execution:** In the production pipeline, the conditional map $T_4(z_1, z_2, z_3, \cdot)$ analytically yields the exact continuous posterior PDF $\pi(ET \mid \mathbf{x})$, quantiles ($q_{10}, q_{50}, q_{90}$), and input-induced variance $\sigma^2_{\text{input}}$ in sub-millisecond evaluation time.

### Pillar 3: Total Variance Decomposition & Biome-Adaptive Ensemble Weighting
Total uncertainty is unified under the Law of Total Variance, synthesizing within-model input/parameter error and between-model structural discrepancy:

$$\mathrm{Var}(ET) = \underbrace{\sum_{m=1}^{4} w_m \, \sigma^2_{m,\text{input}}}_{\text{Within-Model Input Variance}} + \underbrace{\sum_{m=1}^{4} w_m \left(\mu_m - \overline{ET}\right)^2}_{\text{Between-Model Structural Spread}}$$

* **Bayesian Model Averaging (BMA):** Replace equal weighting ($1/n$) with dynamic weights $w_m$ conditioned on biome type, fractional vegetation cover, and aridity index, calibrated against historical tower observations.
* **Component Tracking:** Both within-model variance and structural spread are retained as distinct layers, allowing end-users to diagnose whether uncertainty stems from poor weather drivers or model physics disagreement.

### Pillar 4: Diurnal Integration & Spatial Error Covariance
* **Diurnal Upscaling Bounds:** Replace the constant evaporative fraction (EF) assumption with upper and lower diurnal trajectory bounds parameterized by geostationary thermal observations (GOES-East/West, Meteosat) to quantify solar-to-daily integration error[cite: 1].
* **Spatial Covariance Kernels:** Define an exponential spatial covariance function $C(r) = \sigma^2 \exp(-r / L)$ where $L$ is the spatial correlation length scale of the input meteorological forcing. This allows agricultural and hydrological users to compute valid total volume uncertainty $\sigma_V$ over arbitrary polygons:
  $$\sigma_V^2 = \int_A \int_A C(\|\mathbf{u} - \mathbf{v}\|) \, d\mathbf{u} \, d\mathbf{v}$$

### Pillar 5: Spread-Skill Calibration via Eddy Covariance Networks
* Benchmark ensemble spread against Ameriflux, FLUXNET, and NEON eddy covariance tower observations[cite: 1].
* Evaluate calibration using Spread-Skill Reliability Diagrams and Continuous Ranked Probability Scores (CRPS).
* Apply empirical dispersion corrections so that an ensemble uncertainty of $1.0\text{ mm day}^{-1}$ corresponds to an empirical 68% error containment window.

---

## 3. Phased Implementation Roadmap

    +-------------------------------------------------------------------------------------------------------+
    | Milestone Schedule (24-Month Execution Plan)                                                          |
    +-------------------------------------------------------------------------------------------------------+
    Quarter:     | Q1   Q2 | Q3   Q4 | Q5   Q6 | Q7   Q8 |
    ---------------------------------------------------------------------------------------------------------
    Phase 1:     |========|          |          |          | Input UQ & Covariance Matrices
    Phase 2:     |        |==========|          |          | Transport Map Parameterization & Quadrature
    Phase 3:     |        |          |==========|          | Total Variance Integration & Upscaling UQ
    Phase 4:     |        |          |          |==========| Global Validation, Product Packaging & Release
    ---------------------------------------------------------------------------------------------------------
    Deliverable: | D1.1    | D2.1     | D3.1     | D4.1     | Operational L3T-JET Pipeline Bundle
    +-------------------------------------------------------------------------------------------------------+

### Phase 1: Input Error Formulations & Benchmark Harness (Months 1-6)
* Characterize error covariance matrices $\mathbf{\Sigma}_{\mathbf{x}}$ for $T_a$, $RH$, $VPD$, and $SM$ across global biomes using ERA5 EDA and SMAP TC datasets.
* Build automated benchmarking harness against 50+ AmeriFlux / FLUXNET tower sites[cite: 1].
* **Deliverable D1.1:** Global input error covariance look-up tables and validation baseline report.

### Phase 2: Transport Map Training & Model Emulation (Months 7-12)
* Train triangular Knothe-Rosenblatt maps for PT-JPL-SM, STIC-JPL, PM-JPL, and BESS-JPL stratified by IGBP land-cover classes[cite: 1].
* Benchmark transport map quantile outputs against brute-force Monte Carlo runs ($N = 10,000$) to verify accuracy and speedup ($> 500\times$).
* **Deliverable D2.1:** Pre-trained transport map libraries and inference module integrated with ECOv003-L3T-L4T-JET code repository[cite: 1].

### Phase 3: Total Variance Engine & Diurnal Formulation (Months 13-18)
* Integrate the Law of Total Variance decomposition module into the core operational pipeline.
* Implement BMA weighting engine and diurnal upscaling bounds module.
* Generate alpha test tiles across diverse ecoclimatic zones (cropland, closed forest, semi-arid rangeland).
* **Deliverable D3.1:** Integrated processing engine outputting total, input, and structural variance rasters.

### Phase 4: Verification, Validation, and Operational Release (Months 19-24)
* Conduct global spread-skill validation across AmeriFlux and FLUXNET networks[cite: 1].
* Finalize NetCDF4/Cloud-Optimized GeoTIFF (COG) layer definitions and metadata updates.
* Deliver complete algorithm theoretical basis document (ATBD) update and open-source verification scripts.
* **Deliverable D4.1:** Operational pipeline sign-off, validation paper, and user guide.

---

## 4. Product Delivery & Metadata Specifications

The enhanced L3T-JET product bundle will expand the current descriptive single-layer output into a comprehensive uncertainty suite[cite: 1]:

| Layer Name | Data Type | Units | Description |
| :--- | :--- | :--- | :--- |
| `ETdaily` | Float32 | mm day⁻¹ | Ensemble central estimate (BMA weighted mean/median)[cite: 1] |
| `ETuncertainty` | Float32 | mm day⁻¹ | Total standard deviation (Total Variance formulation)[cite: 1] |
| `ETuncertainty_input` | Float32 | mm day⁻¹ | Propagated input & forcing uncertainty component |
| `ETuncertainty_structural` | Float32 | mm day⁻¹ | Inter-model structural disagreement component[cite: 1] |
| `ETquantile_10` | Float32 | mm day⁻¹ | 10th percentile daily ET (from transport map PDF) |
| `ETquantile_90` | Float32 | mm day⁻¹ | 90th percentile daily ET (from transport map PDF) |
| `spatial_corr_length` | Float32 | km | Spatial error correlation length scale ($L$) |

### Standardized Metadata Attributes

    {
      "uncertainty_formulation": "Law of Total Variance via Triangular Measure Transport",
      "input_error_sources": ["ERA5-EDA", "SMAP-Triple-Collocation", "L2-LST-SensorNoise"],
      "ensemble_members": ["PT-JPL-SM", "STIC-JPL", "PM-JPL", "BESS-JPL"],
      "transport_map_architecture": "Knothe-Rosenblatt triangular polynomial expansion",
      "support_constraints": "Non-negative (ET >= 0), energy-capped (ET <= Rn - G)",
      "validation_standard": "AmeriFlux / FLUXNET spread-skill calibrated (CRPS optimized)"
    }

---

## 5. Risk Assessment and Mitigation

| Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| Transport map training instability in extreme biomes | High | Low | Regularize polynomial coefficients; fall back to analytical First-Order Second-Moment (FOSM) Jacobians in fringe climates. |
| Memory and I/O overhead from additional raster layers | Medium | Medium | Distribute advanced uncertainty layers as an optional auxiliary product bundle (`L3T-JET-UQ`), preserving standard bundle size. |
| Inadequate tower coverage in tropical/high-latitude zones | Medium | High | Utilize cross-validation over clustered biomes; incorporate synthetic site simulations using coupled land-surface models. |
| Operational latency exceeding pipeline limits | High | Low | Pre-compile transport map evaluators into optimized C++/CUDA binaries; batch-process pixels utilizing tensor parallelism. |