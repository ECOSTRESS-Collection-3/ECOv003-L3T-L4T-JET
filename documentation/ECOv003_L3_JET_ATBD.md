# ECOv003 L3 JET Algorithm Theoretical Basis Document

**Jet Propulsion Laboratory**

**Authors:** Gregory H. Halverson, Kerry Cawse-Nicholson, Madeleine Pascolini-Campbell, Evan Davis, Claire Villanueva-Weeks, Simon Hook, AJ Purdy, Maggie Johnson, Munish Sikka

**Affiliation:** ECOSTRESS Science Team, Jet Propulsion Laboratory, California Institute of Technology

**Date:** August 2024

**Document Number:** ECOSTRESS Science Document no. D-1001467

---

## Table of Contents

1. [Introduction](#introduction)
   - [Purpose](#purpose)
   - [Scope and Objectives](#scope-and-objectives)
2. [Parameter Description and Requirements](#parameter-description-and-requirements)
3. [Evapotranspiration Retrieval](#evapotranspiration-retrieval)
   - [PT-JPL~SM~: General Form](#pt-jplsm-general-form)
   - [STIC: General Form](#stic-general-form)
   - [MOD16: General Form](#mod16-general-form)
   - [BESS: General Form](#bess-general-form)
4. [Calibration/Validation](#calibrationvalidation)
5. [Acknowledgements](#acknowledgements)
6. [References](#references)

---

## Introduction

### Purpose

Evapotranspiration (ET) is one of the main science outputs from the ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS). ET is a Level-3 (L-3) product constructed from a combination of the ECOSTRESS Level-2 (L-2) Land Surface Temperature & Emissivity (LSTE) product and auxiliary data sources. 

The ECOSTRESS Collection 3 L3T JET product uses an ensemble of four evapotranspiration models (PT-JPL-SM, STIC-JPL, PM-JPL, and BESS-JPL) to produce robust evapotranspiration estimates. This ensemble approach combines outputs from four distinct models, each with different strengths and theoretical foundations, to reduce uncertainty and improve overall accuracy.

Accurate modelling of ET requires consideration of many environmental and biological controls including: solar radiation, the atmospheric water vapor deficit, soil water availability, vegetation physiology and phenology. LST holds the unique ability to capture when and where plants experience stress, as observed by elevated temperatures which can identify areas that have a reduced capacity to evaporate or transpire water to the atmosphere.

The rate of ET is controlled by many environmental and biological factors, including:

- Incoming radiation
- Atmospheric water vapor deficit
- Soil water availability
- Vegetation physiology and phenology

### Scope and Objectives

This document provides:

1. A description of the ET parameter characteristics and requirements.
2. An overview of the general form of the ET algorithms in the JET ensemble.
3. Algorithm-specific adaptations for the ECOSTRESS mission.
4. Required auxiliary data products and their sources.
5. A plan for calibration and validation (Cal/Val) of the ET retrieval.

---

## Parameter Description and Requirements

### Attributes of ET Data

- **Spatial resolution:** 70 m x 70 m
- **Temporal resolution:** Diurnally varying to match ISS overpass characteristics
- **Latency:** As required by the ECOSTRESS Science Data System (SDS)

### Auxiliary Variables

| Auxiliary Variable       | Product Layer        | Source                          |
|--------------------------|----------------------|---------------------------------|
| Near-surface air temp.   | Ta                  | GEOS-5 FP tavg1_2d_slv_Nx      |
| Relative humidity (RH)   | RH                  | GEOS-5 FP tavg1_2d_slv_Nx      |
| Soil moisture (SM)       | SM                  | GEOS-5 FP tavg1_2d_lnd_Nx      |
| Global radiation         | Rg                  | GEOS-5 FP tavg1_2d_rad_Nx      |
| Net radiation            | Rn                  | BESS-JPL calculation            |
| Cloud mask               | cloud               | L2 CLOUD product                |
| Water mask               | water               | NASADEM Surface Water Bodies    |

---

## Evapotranspiration Retrieval

The ensemble incorporates ET data from four algorithms: Priestley Taylor-Jet Propulsion Laboratory model with soil moisture (PT-JPL-SM), the Penman Monteith-Jet Propulsion Laboratory model (PM-JPL), Surface Temperature Initiated Closure-Jet Propulsion Laboratory model (STIC-JPL), and the Breathing Earth System Simulator-Jet Propulsion Laboratory model (BESS-JPL).

### PT-JPL-SM: General Form

The PT-JPL~SM~ model relies on the Priestley-Taylor equation to resolve potential ET (PET):

$$
PT = \alpha \frac{\Delta}{\Delta + \gamma} R_N - G
$$

Where:
- $\Delta$: Slope of the saturation-to-vapor pressure curve
- $\gamma$: Psychrometric constant
- $R_N$: Net radiation (W/m²)
- $G$: Ground heat flux (W/m²)

To reduce PET to actual ET (AET), ecophysiological constraint functions are applied based on atmospheric moisture and vegetation indices.

---

### STIC-JPL: General Form

The Surface Temperature Initiated Closure-Jet Propulsion Laboratory (STIC-JPL) model, contributed by Dr. Kaniska Mallick, was designed as a surface temperature-sensitive ET model, adopted by ECOSTRESS and SBG for improved estimates of ET reflecting mid-day heat stress. The STIC-JPL model integrates LST into the Penman-Monteith Shuttleworth-Wallace system of ET equations and estimates total latent heat flux directly using thermal remote sensing observations.

The general approach involves:

1. Solving state equations to find analytical solutions for aerodynamic temperature ($T_0$) and conductances ($g_a$, $g_{cs}$).
2. Iteratively estimating unknowns using Penman-Monteith and Shuttleworth-Wallace equations.

---

### PM-JPL: General Form

The Penman-Monteith-Jet Propulsion Laboratory (PM-JPL) algorithm is a derivation of the MOD16 algorithm that was originally designed as the ET product for the Moderate Resolution Imaging Spectroradiometer (MODIS) and continued as a Visible Infrared Imaging Radiometer Suite (VIIRS) product. PM-JPL uses a similar approach to PT-JPL and PT-JPL-SM to independently estimate vegetation and soil components of instantaneous ET, but using the Penman-Monteith formula instead of the Priestley-Taylor.

The algorithm is based on the Penman-Monteith equation with environmental constraints from vegetation cover, temperature, and atmospheric moisture deficits. It resolves evaporative fluxes from the soil, canopy, and intercepted water separately. The PM-JPL latent heat flux partitions are summed to total latent heat flux for the ensemble estimate.

---

### BESS-JPL: General Form

The Breathing Earth System Simulator-Jet-Jet Propulsion Laboratory Propulsion Laboratory (BESS-JPL) model is a coupled surface energy balance and photosynthesis model contributed by Dr. Youngryel Ryu. The model iteratively calculates net radiation, ET, and Gross Primary Production (GPP-JPL) estimates. The latent heat flux component of BESS-JPL is included in the ensemble estimate, while the BESS-JPL net radiation is used as input to the other ET models.

The BESS-JPL model is a coupled surface energy balance and photosynthesis model contributed by Dr. Youngryel Ryu. The model iteratively calculates net radiation, ET, and Gross Primary Production (GPP) estimates. The latent heat flux component of BESS-JPL is included in the ensemble estimate, while the BESS-JPL net radiation is used as input to the other ET models.

The BESS-JPL couples atmospheric and canopy radiative transfer processes with photosynthesis, stomatal conductance, and transpiration. It uses a quadratic representation of the Penman-Monteith model to estimate transpiration.

### AquaSEBS Water Surface Evaporation

For water surface pixels identified using the NASADEM Surface Water Body extent, the ECOSTRESS Collection 3 processing chain implements the AquaSEBS (Aquatic Surface Energy Balance System) model developed by Abdelrady et al. (2016) and validated by Fisher et al. (2023). Water surface evaporation is calculated using a physics-based approach that combines the equilibrium temperature model for water heat flux with the Priestley-Taylor equation for evaporation estimation.

The AquaSEBS model implements the surface energy balance equation specifically adapted for water bodies:

$$R_n = LE + H + W$$

Where the water heat flux (W) is calculated using the equilibrium temperature model:

$$W = \beta \times (T_e - WST)$$

Latent heat flux is then calculated using the Priestley-Taylor equation with α = 1.26 for water surfaces:

$$LE = \alpha \times \frac{\Delta}{\Delta + \gamma} \times (R_n - W)$$

The AquaSEBS methodology has been extensively validated against 19 in situ open water evaporation sites worldwide spanning multiple climate zones, with daily evaporation estimates showing r² = 0.47-0.56 and RMSE = 1.2-1.5 mm/day.

### Ensemble Processing

The median of total latent heat flux in watts per square meter from the PT-JPL-SM, STIC-JPL, PM-JPL, and BESS-JPL models is upscaled to a daily ET estimate in millimeters per day and recorded in the L3T JET product as `ETdaily`. The standard deviation between these multiple estimates of ET is considered the uncertainty for the evapotranspiration product, as `ETinstUncertainty`. The ETdaily product represents the integrated ET between sunrise and sunset.

---

---

## Calibration/Validation

### ET Evaluation

Eddy covariance (EC) towers provide year-round observations at frequencies (~30 minutes) and spatial scales (10s-100s m) necessary to evaluate the JET ensemble. This analysis uses EC data from the Ameriflux network.

### Error Budget

The ECOSTRESS ET products target an error value of 1 mm/day, consistent with established literature. For example:

- PT-JPL ET: RMSE of 6%, $R^2 = 0.88$
- MOD16: RMSE of 0.84 mm/day

---

## Acknowledgements

We thank Gregory Halverson, Laura Jewell, Gregory Moore, Caroline Famiglietti, Munish Sikka, Manish Verma, Kevin Tu, Alexandre Guillaume, Kaniska Mallick, Youngryel Ryu, and Hideki Kobayashi for their contributions.

---

## Algorithm Repositories

The evapotranspiration algorithms are located in the [JPL-Evapotranspiration-Algorithms](https://github.com/JPL-Evapotranspiration-Algorithms) organization:

- **PT-JPL-SM**: [https://github.com/JPL-Evapotranspiration-Algorithms/PT-JPL-SM](https://github.com/JPL-Evapotranspiration-Algorithms/PT-JPL-SM)
- **STIC-JPL**: [https://github.com/JPL-Evapotranspiration-Algorithms/STIC-JPL](https://github.com/JPL-Evapotranspiration-Algorithms/STIC-JPL)
- **PM-JPL**: [https://github.com/JPL-Evapotranspiration-Algorithms/PM-JPL](https://github.com/JPL-Evapotranspiration-Algorithms/PM-JPL)
- **BESS-JPL**: [https://github.com/JPL-Evapotranspiration-Algorithms/BESS-JPL](https://github.com/JPL-Evapotranspiration-Algorithms/BESS-JPL)
- **AquaSEBS**: [https://github.com/JPL-Evapotranspiration-Algorithms/AquaSEBS](https://github.com/JPL-Evapotranspiration-Algorithms/AquaSEBS)

---

## References

Allen, R. G., M. Tasumi, and R. Trezza (2007), Satellite-based energy balance for mapping evapotranspiration with internalized calibration (METRIC)-model, *J. Irrig. Drain. E.*, *133*, 380-394. doi: [https://doi.org/10.1061/(ASCE)0733-9437(2007)133:4(380)](https://doi.org/10.1061/(ASCE)0733-9437(2007)133:4(380))

Anderson, M. C., J. M. Norman, J. R. Mecikalski, J. A. Otkin, and W. P. Kustas (2007), A climatological study of evapotranspiration and moisture stress across the continental United States based on thermal remote sensing: 1. Model formulation, *J. Geophys. Res.*, *112*(D10), D10117. doi: [https://doi.org/10.1029/2006JD007506](https://doi.org/10.1029/2006JD007506)

Anderson, M. C., W. P. Kustas, C. R. Hain, C. Cammalleri, F. Gao, M. Yilmaz, I. Mladenova, J. Otkin, M. Schull, and R. Houborg (2013), Mapping surface fluxes and moisture conditions from field to global scales using ALEXI/DisALEXI, *Remote Sensing of Energy Fluxes and Soil Moisture Content*, 207-232. doi: [https://doi.org/10.3390/rs13040773](https://doi.org/10.3390/rs13040773)

Baldocchi, D. (2008), 'Breathing' of the terrestrial biosphere: lessons learned from a global network of carbon dioxide flux measurement systems, *Australian Journal of Botany*, *56*, 1-26. doi: [https://doi.org/10.1071/BT07151](https://doi.org/10.1071/BT07151)

Baldocchi, D., E. Falge, L. H. Gu, R. J. Olson, D. Hollinger, S. W. Running, P. M. Anthoni, C. Bernhofer, K. Davis, R. Evans, J. Fuentes, A. Goldstein, G. Katul, B. E. Law, X. H. Lee, Y. Malhi, T. Meyers, W. Munger, W. Oechel, K. T. P. U, K. Pilegaard, H. P. Schmid, R. Valentini, S. Verma, T. Vesala, K. Wilson, and S. C. Wofsy (2001), FLUXNET: A new tool to study the temporal and spatial variability of ecosystem-scale carbon dioxide, water vapor, and energy flux densities, *Bulletin of the American Meteorological Society*, *82*(11), 2415-2434. doi: [https://doi.org/10.1175/1520-0477(2001)082<2415:FANTTS>2.3.CO;2](https://doi.org/10.1175/1520-0477(2001)082<2415:FANTTS>2.3.CO;2)

Bi, L., P. Yang, G. W. Kattawar, Y.-X. Hu, and B. A. Baum (2011), Diffraction and external reflection by dielectric faceted particles, *J. Quant. Spectrosc. Radiant. Transfer*, *112*, 163-173. doi: [https://doi.org/10.1016/j.jqsrt.2010.02.007](https://doi.org/10.1016/j.jqsrt.2010.02.007)

Bisht, G., V. Venturini, S. Islam, and L. Jiang (2005), Estimation of the net radiation using MODIS (Moderate Resolution Imaging Spectroradiometer), *Remote Sensing of Environment*, *97*, 52-67. doi: [https://doi.org/10.1016/j.rse.2005.03.014](https://doi.org/10.1016/j.rse.2005.03.014)

Bouchet, R. J. (1963), Evapotranspiration réelle evapotranspiration potentielle, signification climatique *Rep. Publ. 62*, 134-142 pp, Int. Assoc. Sci. Hydrol., Berkeley, California.

Chen, X., H. Wei, P. Yang, and B. A. Baum (2011), An efficient method for computing atmospheric radiances in clear-sky and cloudy conditions, *J. Quant. Spectrosc. Radiant. Transfer*, *112*, 109-118. doi: [https://doi.org/10.1016/j.jqsrt.2010.08.013](https://doi.org/10.1016/j.jqsrt.2010.08.013)

Chen, Y., J. Xia, S. Liang, J. Feng, J. B. Fisher, X. Li, X. Li, S. Liu, Z. Ma, and A. Miyata (2014), Comparison of satellite-based evapotranspiration models over terrestrial ecosystems in China, *Remote Sensing of Environment*, *140*, 279-293. doi: [https://doi.org/10.1016/j.rse.2013.08.045](https://doi.org/10.1016/j.rse.2013.08.045)

Coll, C., Z. Wan, and J. M. Galve (2009), Temperature-based and radiance-based validations of the V5 MODIS land surface temperature product, *Journal of Geophysical Research*, *114*(D20102), doi: [https://doi.org/10.1029/2009JD012038](https://doi.org/10.1029/2009JD012038).
