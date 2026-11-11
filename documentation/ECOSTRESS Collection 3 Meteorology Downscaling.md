# ECOSTRESS Collection 3 JET Meteorology Downscaling Procedure

## 1. Purpose

This document describes the meteorology downscaling approach used in the ECOSTRESS Collection 3 JET processing chain to generate high spatial resolution air temperature, humidity, and soil moisture images. The goal is to take coarse-resolution meteorological fields from GEOS-5 FP and convert them into 70 m products consistent with ECOSTRESS thermal and reflectance observations, while preserving the large-scale meteorological structure from the coarse model and adding fine-scale spatial detail from surface observations.

The procedure is applied to:
- Air temperature (Ta)
- Relative humidity (RH)
- Soil moisture (SM)

These variables are downscaled from GEOS-5 FP to the ECOSTRESS 70 m grid and are then stored in the L3T ETAUX auxiliary product and used downstream in the JET evapotranspiration model.

---

## 2. Inputs

### 2.1 Coarse meteorological forcing
The coarse-scale inputs come from GEOS-5 FP:
- Air temperature from: GEOS-5 FP `tavg1_2d_slv_Nx`
- Relative humidity from: GEOS-5 FP `tavg1_2d_slv_Nx`
- Soil moisture from: GEOS-5 FP `tavg1_2d_lnd_Nx`

These fields provide the broad-scale atmospheric and land-surface state at the native GEOS resolution.

### 2.2 Fine-scale predictors
The high-resolution predictors are drawn from ECOSTRESS/Sentinel inputs:
- Surface temperature (ST), from the L2T LSTE product
- NDVI, from the L2T STARS product
- Albedo, from the L2T STARS product

All of these are at approximately 70 m resolution and are spatially aligned to the ECOSTRESS tile footprint.

### 2.3 Ancillary masks
- Cloud mask
- Water mask
- Tile geometry and geolocation metadata

The cloud mask is important because downscaled meteorology is later replaced with GEOS-5 FP values in cloudy areas.

---

## 3. High-Level Workflow

The downscaling workflow is:

1. Load coarse GEOS-5 FP meteorological fields.
2. Load high-resolution ECOSTRESS predictors (ST, NDVI, albedo).
3. Align predictors to the GEOS grid within each Sentinel tile.
4. Fit a local linear regression relating coarse GEOS meteorology to the coarse predictor stack.
5. Apply the fitted coefficients to the full-resolution 70 m predictor fields to generate a first-pass downscaled product.
6. Bias-correct the first-pass product so that the aggregated fine field matches the original coarse GEOS field.
7. Replace cloudy pixels with bicubically resampled GEOS-5 FP values.
8. Save the final fields as L3T ETAUX products: Ta, RH, and SM.

This approach preserves the large-scale meteorological field from GEOS-5 FP and injects sub-grid variability from ECOSTRESS surface structure.

---

## 4. Mathematical Formulation

For each meteorological variable, the downscaling is represented as a tile-wise linear regression:

For a given target variable Y, where Y is either:
- Ta (air temperature)
- RH (relative humidity)
- SM (soil moisture)

the coarse data are modeled as:

Y_coarse = beta0 + beta1 * ST_coarse + beta2 * NDVI_coarse + beta3 * Albedo_coarse + error

where:
- Y_coarse is the GEOS-5 FP coarse variable
- ST_coarse is the coarse-scale surface temperature aligned to the GEOS grid
- NDVI_coarse is the coarse-scale NDVI aligned to the GEOS grid
- Albedo_coarse is the coarse-scale surface albedo aligned to the GEOS grid
- beta0, beta1, beta2, beta3 are regression coefficients estimated within each Sentinel tile

Once the coefficients are estimated, the fine-scale predictive field is computed as:

Y_70m_firstpass = beta0 + beta1 * ST_70m + beta2 * NDVI_70m + beta3 * Albedo_70m

This creates the initial high-resolution estimate.

### 4.1 Bias correction
The first-pass downscaled field is then bias-corrected so it is consistent with the original GEOS-5 FP coarse image. Conceptually:

Y_70m_corrected = Y_70m_firstpass + correction

where the correction is chosen such that when Y_70m_corrected is aggregated back to the GEOS grid, it matches the original coarse GEOS field:

aggregate(Y_70m_corrected) ≈ Y_coarse

In practice, this is typically implemented as an additive correction or a multiplicative scaling adjustment, depending on the exact code path used by the processor. The documentation emphasizes that the final field is bias-corrected to the coarse GEOS product.

### 4.2 Cloud fill
For cloudy pixels, the corrected 70 m product is not trusted. Those pixels are filled with a bicubically resampled GEOS-5 FP value. This ensures that cloud-obscured areas remain physically consistent with the model field while preserving the downscaled resolution elsewhere.

---

## 5. Detailed Procedure

### Step 1: Load coarse meteorology
For each tile and time:
- read GEOS-5 FP Ta and RH from the slv product
- read GEOS-5 FP SM from the lnd product
- store these values on the coarse GEOS-5 grid

### Step 2: Load fine predictors
Read:
- ECOSTRESS L2T LSTE surface temperature
- ECOSTRESS L2T STARS NDVI
- ECOSTRESS L2T STARS albedo

These are at 70 m spatial resolution and represent the fine-scale heterogeneity of the landscape.

### Step 3: Align to a common tile-based grid
Within each Sentinel tile:
- aggregate or resample ST, NDVI, and albedo onto the coarse GEOS pixel grid
- this creates coarse predictor arrays suitable for model fitting

The important idea is that each GEOS coarse pixel receives a corresponding set of fine-scale predictor values that describe the land surface within that pixel.

### Step 4: Estimate local regression coefficients
For each tile, fit a separate regression for:
- Ta
- RH
- SM

This makes the downscaling model local to each area rather than globally fixed across the entire image. The coefficients vary with land cover, climate, and surface heterogeneity within the tile.

### Step 5: Generate first-pass 70 m estimates
Apply the fitted coefficients to the full-resolution 70 m predictors:

- Ta_70m_firstpass = beta0_Ta + beta1_Ta * ST_70m + beta2_Ta * NDVI_70m + beta3_Ta * Albedo_70m
- RH_70m_firstpass = beta0_RH + beta1_RH * ST_70m + beta2_RH * NDVI_70m + beta3_RH * Albedo_70m
- SM_70m_firstpass = beta0_SM + beta1_SM * ST_70m + beta2_SM * NDVI_70m + beta3_SM * Albedo_70m

This step adds fine-scale spatial variability that is physically associated with temperature, vegetation vigor, and surface reflectance.

### Step 6: Bias-correct to GEOS-5 FP
Aggregate the first-pass 70 m field back to the coarse GEOS grid and compare with the original GEOS field. Apply a correction so the coarse-scale mean or distribution matches the GEOS-5 FP value.

This is critical because GEOS-5 FP remains the physically consistent large-scale reference.

### Step 7: Fill clouds using GEOS-5 FP
Mark cloud-covered pixels. For cloud pixels:
- replace the downscaled result with a bicubically resampled GEOS-5 FP value

This avoids noisy or unrealistic fine-scale values in cloud-obscured regions.

### Step 8: Save the final L3T ETAUX layers
The final product includes:
- Ta: near-surface air temperature
- RH: relative humidity
- SM: soil moisture

These are distributed in the L3T ETAUX auxiliary product used by the ECOSTRESS JET retrieval chain.

---

## 6. Why ST, NDVI, and Albedo?

The selected predictors are physically meaningful:

- Surface temperature (ST)
  - captures thermal heterogeneity due to land cover, moisture, and energy balance
- NDVI
  - captures vegetation density and vigor
  - often strongly tied to evapotranspiration and near-surface meteorology
- Albedo
  - captures radiative properties and surface energy partitioning
  - helps reflect differences in land surface reflectance and soil/vegetation exposure

Together, they encode much of the sub-grid variability that the coarse GEOS-5 FP product cannot resolve.

---

## 7. Why this approach works

This downscaling method is effective because it combines:
- large-scale consistency from GEOS-5 FP
- fine-scale detail from ECOSTRESS observations

The regression makes the fine product statistically tied to the coarse meteorological field, while the surface predictors provide the spatial structure needed to resolve local heterogeneity.

In other words:
- GEOS-5 FP tells us the broad atmospheric and land state
- ECOSTRESS ST, NDVI, and albedo tell us how that state varies within each coarse pixel

The result is a meteorology field that is both physically plausible and spatially detailed enough for 70 m evapotranspiration and ecosystem modeling.

---

## 8. Product Outputs

The final downscaled meteorology fields are recorded in the L3T ETAUX product with the following interpretation:

- Ta: near-surface air temperature, in degrees Celsius
- RH: relative humidity, as a ratio between 0 and 1
- SM: soil moisture, as a ratio between 0 and 1

These are later used in the JET energy balance and evapotranspiration calculations.

---

## 9. Implementation Notes

The repository documentation and processing code indicate that:
- downscaling is performed within each Sentinel tile
- air temperature and humidity use GEOS-5 FP `tavg1_2d_slv_Nx`
- soil moisture uses GEOS-5 FP `tavg1_2d_lnd_Nx`
- the method is a linear regression against ST, NDVI, and albedo
- the first-pass estimate is bias-corrected to the coarse GEOS data
- cloudy regions are filled using a bicubic resample of the coarse GEOS product

The repository also contains flags and processing options such as:
- `SHARPEN_METEOROLOGY = True`
- `SHARPEN_SOIL_MOISTURE = True`

These indicate that the downscaling/sharpening of meteorology and soil moisture is an intentional part of the ECOSTRESS Collection 3 pipeline.

---

## 10. Summary

The ECOSTRESS Collection 3 JET downscaling procedure uses a tile-wise linear regression to relate coarse GEOS-5 FP meteorological variables to fine-scale ECOSTRESS surface predictors (ST, NDVI, and albedo). The fitted coefficients are then applied to the native 70 m predictor fields, producing a high-resolution first-pass estimate. A bias correction step ensures compatibility with the coarse GEOS field, and cloudy pixels are filled with bicubically resampled GEOS-5 FP values. The result is a high-resolution 70 m Ta, RH, and SM dataset that preserves the large-scale meteorological structure while adding the spatial detail needed for fine-scale evapotranspiration modeling.

---

## 11. Short procedural summary

1. Use GEOS-5 FP Ta/RH/SM as coarse reference state.
2. Use ECOSTRESS ST/NDVI/albedo as fine-scale predictors.
3. Fit local linear regressions per tile.
4. Apply coefficients to 70 m predictors.
5. Bias-correct back to the coarse GEOS image.
6. Fill clouds with bi-cubic GEOS-5 FP.
7. Save the final downscaled meteorology product.

---

This document reflects the published description in the ECOSTRESS Collection 3 documentation and the repository’s processing workflow for the JET product.
