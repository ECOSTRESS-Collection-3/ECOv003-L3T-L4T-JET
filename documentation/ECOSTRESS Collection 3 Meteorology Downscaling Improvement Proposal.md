# Technical Proposal: Physics-Informed, Structurally Constrained Meteorology and Soil Moisture Downscaling for the ECOSTRESS JET Processing Chain

---

## 1. Executive Summary

This proposal outlines a technical upgrade to the operational meteorology downscaling subsystem within the ECOSTRESS Collection 3 Level-3 Evapotranspiration (JET) processing chain[cite: 1, 2]. 

The current Collection 3 operational pipeline derives 70 m near-surface air temperature (Ta), relative humidity (RH), and soil moisture (SM) auxiliary fields by fitting independent, tile-wise Ordinary Least Squares (OLS) linear regressions on coarse GEOS-5 FP model states using ECOSTRESS surface temperature (ST), NDVI, and surface albedo as spatial predictors. While computationally efficient, this empirical approach introduces systemic physical and spatial errors that propagate directly into downstream Level-3 evapotranspiration models[cite: 1, 2]:

* Spaceborne radiometric skin temperature (Tskin) is treated as a direct linear proxy for 2 m ambient air temperature (Ta) without accounting for aerodynamic resistance (ra), surface roughness, or canopy structural decoupling.
* Linear downscaling of relative humidity violates non-linear Clausius-Clapeyron thermodynamics, resulting in unphysical vapor pressure deficits (VPD) and out-of-bounds humidity values.
* Low degrees of freedom across coarse GEOS pixels within individual Sentinel tiles induce collinear instability and seamline discontinuities along tile borders.
* Downscaled soil moisture relies on optical proxies that cannot distinguish shallow topsoil desiccation from deep root-zone transpirational cooling.

We propose a **Physics-Informed, Structurally Constrained Downscaling Pipeline** that:
1. Integrates Global Ecosystem Dynamics Investigation (GEDI) canopy height to parameterize aerodynamic resistance (ra), aerodynamic roughness length (z0m), and sub-canopy microclimates.
2. Reformulates humidity downscaling around conservative actual vapor pressure (ea) with psychrometric recovery of RH.
3. Implements continuous spatially regularized regression (Ridge/GWR) with overlapping tile blending to eliminate edge seamlines.
4. Uses multi-scale Laplacian pyramid blending to replace abrupt bicubic cloud fills with seamless background transitions.

These enhancements will directly improve input meteorological fidelity for the PT-JPL-SM, STIC-JPL, PM-JPL, and BESS-JPL ensemble, supporting the mission's daily ET accuracy requirement of 1.0 mm/day.

---

## 2. Baseline Architecture and Key Deficiencies

The ECOSTRESS Collection 3 L3T ETAUX auxiliary product ingests GEOS-5 FP hourly fields (Ta and RH from `tavg1_2d_slv_Nx`; SM from `tavg1_2d_lnd_Nx`) and downscales them to 70 m using ECOSTRESS L2T LSTE surface temperature (ST) and L2T STARS surface reflectance (NDVI and albedo).