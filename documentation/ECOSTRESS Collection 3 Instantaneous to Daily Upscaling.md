# ECOSTRESS Collection 3: Instantaneous-to-Daily Upscaling Procedure

This document describes the procedure used in ECOSTRESS Collection 3 to convert instantaneous latent heat flux estimates (W m^-2) from evapotranspiration models into daily evapotranspiration totals (mm day^-1), as implemented in the L3T JET product.

## 1. Scope

The ECOSTRESS Collection 3 L3T JET product is built from an ensemble of four evapotranspiration models:

- PT-JPL-SM
- STIC-JPL
- PM-JPL
- BESS-JPL

Each model produces an instantaneous latent heat flux estimate, LE, in W m^-2. The product then upscales these values to a daytime daily ET estimate for each pixel. The output daily product is designated as:

- ETdaily: daily evapotranspiration, mm day^-1
- ETuncertainty: uncertainty in daily ET, mm day^-1

The repository documentation states that:

> The median of total latent heat flux in watts per square meter from the PT-JPL-SM, STIC-JPL, PM-JPL, and BESS-JPL models is upscaled to a daily ET estimate in millimeters per day and recorded in the L3T JET product as ETdaily.

It further states that:

> The ETdaily product represents the integrated ET between sunrise and sunset.

This is reinforced in the repository constants, where:

- `UPSCALE_TO_DAYLIGHT = True`
- `LATENT_VAPORIZATION_JOULES_PER_KILOGRAM = 2450000.0`

---

## 2. Physical Basis

The instantaneous ET models estimate latent heat flux, LE, which is the energy used to evaporate water:

- LE is reported in W m^-2
- 1 W m^-2 = 1 J s^-1 m^-2

To convert an instantaneous flux to a daily water depth, the energy must be integrated over the daylight period and then converted to equivalent water mass using the latent heat of vaporization.

The relevant conversion is:

- Energy per unit area over the daylight interval:
  
  E_day = LE_inst × t_daylight

- Convert energy to water depth:
  
  ET_daily = E_day / L_v

where:

- `E_day` = integrated energy over the daylight period (J m^-2)
- `LE_inst` = instantaneous latent heat flux (W m^-2)
- `t_daylight` = daylight duration in seconds
- `L_v` = latent heat of vaporization of water (J kg^-1)
- `ET_daily` = daily ET expressed as water depth (mm day^-1)

Since 1 kg m^-2 of evaporated water corresponds to 1 mm depth, the final formula is:

```text
ET_daily (mm day^-1) = LE_inst (W m^-2) × daylight_seconds / 2450000.0
```

This produces a daily ET equivalent integrated over the daylight interval from sunrise to sunset.

---

## 3. Ensemble Construction

For each pixel and acquisition date, the ET processing chain first collects the valid instantaneous latent heat flux estimates from the constituent models:

- PT-JPL-SM: LE_PTJPLSM
- STIC-JPL: LE_STICJPL
- PM-JPL: LE_PMJPL
- BESS-JPL: LE_BESSJPL

The ensemble instantaneous estimate is formed as the median across available valid model estimates:

```text
LE_ensemble_inst = median(LE_PTJPLSM, LE_STICJPL, LE_PMJPL, LE_BESSJPL)
```

This median-based approach reduces sensitivity to outliers and model-specific biases.

The daily ensemble estimate is then computed from the model-level daily values or from the mean/median of model instantaneous estimates scaled over the daylight interval. In the product documentation, the ensemble daily value is described as the median of the model-based ET outputs, with uncertainty defined as the standard deviation between the multiple estimates.

---

## 4. Daylight Upscaling Procedure

### 4.1 Determine daylight interval

For each pixel, date, and solar geometry, compute the daylight duration between sunrise and sunset:

```text
t_daylight = sunset_time - sunrise_time
```

This interval is expressed in seconds.

The repository includes the constant:

```python
UPSCALE_TO_DAYLIGHT = True
```

which indicates the product is scaled over daylight rather than over a full 24-hour period.

### 4.2 Integrate the latent heat flux over daylight

The instantaneous latent heat flux is an energy rate. To estimate total energy used for evapotranspiration during the daylight window:

```text
E_day = LE_inst × t_daylight
```

where:

- `LE_inst` is in W m^-2 = J s^-1 m^-2
- `t_daylight` is in seconds
- `E_day` is in J m^-2

### 4.3 Convert energy to water equivalent

To convert the energy to an equivalent water depth:

```text
ET_daily = E_day / L_v
```

Using the repository constant:

```text
L_v = 2450000.0 J kg^-1
```

Therefore:

```text
ET_daily = LE_inst × t_daylight / 2450000.0
```

This yields the daily ET in units of kg m^-2 or, equivalently, mm day^-1.

---

## 5. Final Daily ET Output

For the ECOSTRESS Collection 3 L3T JET product, the daily ET output is:

```text
ETdaily = daily evapotranspiration integrated from sunrise to sunset
```

and is reported in:

```text
mm day^-1
```

The daily ET product is not a 24-hour total; it is a daylight-integrated total. This is explicitly stated in the documentation:

> The ETdaily product represents the integrated ET between sunrise and sunset.

---

## 6. Uncertainty

The documentation defines the ET uncertainty as the standard deviation among the ensemble model estimates:

```text
ETuncertainty = stddev(ET_model_1, ET_model_2, ET_model_3, ET_model_4)
```

This calculation is performed in daily ET units, aligning with the ETdaily product:

- ETdaily: mm day^-1
- ETuncertainty: mm day^-1

This differs from older collection versions, where uncertainty was often reported in instantaneous W m^-2 units. Collection 3 standardizes the uncertainty to the same daily units as ETdaily.

---

## 7. Model-by-Model Daily Layers

Collection 3 produces daily layers for each model:

- PTJPLSMdaily
- STICJPLdaily
- PMJPLdaily
- BESSJPLdaily

These are created by applying the same daylight scaling to each model’s instantaneous estimate.

In other words, for each model:

```text
ET_model_daily = LE_model_inst × t_daylight / L_v
```

and the ensemble daily estimate is then derived from these model-based daily values.

This is an important Collection 3 enhancement: not only does the product provide an ensemble estimate, but it also includes the individual daily ET layers for each constituent model.

---

## 8. Water Pixels and AquaSEBS

For water surface pixels, ECOSTRESS uses a separate water evaporation model:

- AquaSEBS

Water pixels are identified using the NASADEM water-body extent. AquaSEBS computes evaporation using a physics-based energy-balance approach with a Priestley-Taylor formulation.

The simplified water energy balance is:

```text
Rn = LE + H + W
```

where:

- Rn = net radiation
- LE = latent heat flux
- H = sensible heat flux
- W = water heat flux

For water, AquaSEBS estimates latent heat flux as:

```text
LE = α × (Δ / (Δ + γ)) × (Rn - W)
```

with:

```text
α = 1.26
```

for water surfaces.

This AquaSEBS-based latent heat flux is then scaled to a daily value using the same daylight integration logic described above.

---

## 9. Practical Implementation Logic

The overall algorithm can be summarized in pseudocode as follows:

```python
# Inputs per pixel/date:
#   LE_PTJPLSM, LE_STICJPL, LE_PMJPL, LE_BESSJPL  (W/m^2)
#   sunrise, sunset
#   latent heat constant: 2450000.0 J/kg

daylight_seconds = (sunset - sunrise).total_seconds()

# Compute daily ET for each model
ET_PTJPLSM_daily = LE_PTJPLSM * daylight_seconds / 2450000.0
ET_STICJPL_daily = LE_STICJPL * daylight_seconds / 2450000.0
ET_PMJPL_daily = LE_PMJPL * daylight_seconds / 2450000.0
ET_BESSJPL_daily = LE_BESSJPL * daylight_seconds / 2450000.0

# Ensemble daily ET is median of valid model ETs
ETdaily = median([
    ET_PTJPLSM_daily,
    ET_STICJPL_daily,
    ET_PMJPL_daily,
    ET_BESSJPL_daily
])

# Daily uncertainty is standard deviation across model ETs
ETuncertainty = stddev([
    ET_PTJPLSM_daily,
    ET_STICJPL_daily,
    ET_PMJPL_daily,
    ET_BESSJPL_daily
])
```

This is the essential daily scaling step used in the ECOSTRESS Collection 3 processing chain.

---

## 10. Summary of the Procedure

The ECOSTRESS Collection 3 instantaneous-to-daily ET upscaling procedure is:

1. Compute instantaneous latent heat flux estimates from the model ensemble:
   - PT-JPL-SM
   - STIC-JPL
   - PM-JPL
   - BESS-JPL

2. Form the ensemble instantaneous estimate using the median.

3. Determine the pixel-specific daylight length from sunrise to sunset.

4. Convert the instantaneous latent heat flux to daily ET by integrating over daylight:
   
   ```text
   ET_daily = LE_inst × daylight_seconds / 2450000.0
   ```

5. Produce daily ET outputs for each model and for the ensemble.

6. Compute daily uncertainty as the standard deviation across the model estimates.

7. For water pixels, apply AquaSEBS and scale its output using the same daylight integration logic.

This yields the final L3T JET daily ET product, ETdaily, in mm day^-1, representing the total evapotranspiration integrated between sunrise and sunset.

---

## 11. Key Repository References

- Repository constants:
  - `UPSCALE_TO_DAYLIGHT = True`
  - `LATENT_VAPORIZATION_JOULES_PER_KILOGRAM = 2450000.0`

- Documentation:
  - `documentation/ECOv003_L3_L4_JET_ATBD.md`
  - `documentation/ECOv003_L3_L4_JET_User_Guide.md`

- Product description:
  - `README.md`

These sources collectively describe the ensemble concept, daylight scaling, and the conversion of instantaneous latent heat flux to daily ET in mm day^-1.

---

## 12. Final equation

The key conversion used in Collection 3 is:

```text
ETdaily (mm day^-1) = LE_inst (W m^-2) × t_daylight (s) / 2450000.0
```

where:

- `LE_inst` is the instantaneous latent heat flux from one model or from the ensemble median
- `t_daylight` is the daytime duration from sunrise to sunset
- `2450000.0` J kg^-1 is the latent heat of vaporization used for water

This equation encapsulates the instantaneous-to-daily upscaling procedure used in ECOSTRESS Collection 3.
```