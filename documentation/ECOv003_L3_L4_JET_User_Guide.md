# ECOSTRESS Collection 3 Level-3 Evapotranspiration (JET) Data Products User Guide

**ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS)**

**May 5, 2026**

## Authors

**Gregory H. Halverson**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

**Kerry Cawse-Nicholson**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

**Madeleine Pascolini-Campbell**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

**Simon Hook**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

**AJ Purdy**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

**Margaret Johnson**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

**Evan Davis**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

**Munish Sikka**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

**Claire Villanueva-Weeks**  
ECOSTRESS Science Team  
Jet Propulsion Laboratory  
California Institute of Technology

---

*© 2026 California Institute of Technology. Government sponsorship acknowledged.*

**National Aeronautics and Space Administration**  
Jet Propulsion Laboratory  
4800 Oak Grove Drive  
Pasadena, California 91109-8099  
California Institute of Technology

This research was carried out at the Jet Propulsion Laboratory,
California Institute of Technology, under a contract with the National
Aeronautics and Space Administration.

Reference herein to any specific commercial product, process, or service
by trade name, trademark, manufacturer, or otherwise, does not
constitute or imply its endorsement by the United States Government or
the Jet Propulsion Laboratory, California Institute of Technology.

© 2026. California Institute of Technology. Government sponsorship
acknowledged.

---

The users' guide is designed to be a living document that describes the ECOSTRESS data products. The document describes the current state of the
art and is revised as progress is made in the development and assessment
of the ECOSTRESS data products. The primary purpose of the document is
to present an overview of the ECOSTRESS data products to the potential
user. For more detailed information on the physical basis and algorithms
used to produce these products, please see the Algorithm Theoretical
Basis Document (ATBD).

**Contacts**

Readers seeking additional information about this product may contact
the following:

- Gregory Halverson\
  Jet Propulsion Laboratory\
  4800 Oak Grove Dr.\
  Pasadena, CA 91109\
  Email: <gregory.h.halverson@jpl.nasa.gov>\
  Office: (626) 660-6818

<!-- -->

- Kerry Cawse-Nicholson
  MS 183-501\
  Jet Propulsion Laboratory\
  4800 Oak Grove Dr.\
  Pasadena, CA 91109\
  Email: <kerry-anne.cawse-nicholson@jpl.nasa.gov>\
  Office: (818) 354-1594

<!-- -->

- Margaret Johnson\
  Jet Propulsion Laboratory\
  4800 Oak Grove Dr.\
  Pasadena, CA 91109\
  Email: <maggie.johnson@jpl.nasa.gov>

  Office: (818) 354-8885



## Table of Contents

1. [Introduction](#introduction)
   - [Cloud-Optimized GeoTIFF Orbit/Scene/Tile Products](#cloud-optimized-geotiff-orbitscenetile-products)
   - [Quality Flags](#quality-flags)
   - [Product Availability](#product-availability)
2. [L2T STARS NDVI & Albedo Product](#l2t-stars-ndvi-and-albedo-product)
3. [L3T ETAUX Ecosystem Auxiliary Inputs Product](#l3t-etaux-ecosystem-auxiliary-inputs-product)
   - [Downscaled Meteorology](#downscaled-meteorology)
   - [Downscaled Soil Moisture](#downscaled-soil-moisture)
   - [Surface Energy Balance](#surface-energy-balance)
4. [L3T JET Evapotranspiration Product](#l3t-jet-evapotranspiration-product)
5. [L4T ESI & WUE Products](#l4t-esi-and-wue-products)
6. [Standard Metadata](#standard-metadata)
7. [Acknowledgements](#acknowledgements)
8. [Bibliography](#bibliography)

### List of Tables

- Table 1: Listing of ECOSTRESS tiled products long names and short names
- Table 2: Listing of the L2T STARS data layers  
- Table 3: Listing of the L3T ETAUX data layers
- Table 4: Listing of the L3T JET data layers
- Table 5: Listing of the L4T ESI data layers
- Table 6: Listing of the L4T WUE data layers
- Table 7: StandardMetadata fields in L2T/L3T/L4T products
- Table 8: ProductMetadata fields in L2T/L3T/L4T products

# Introduction

This is the user guide for the ECOSTRESS tiled products. ECOSTRESS
acquires data within an orbit, and this orbit path is divided into
scenes roughly 935 x 935 km in size. The ECOSTRESS orbit/scene/tile
products are distributed in Cloud-Optimized GeoTIFF (COG) format. The
tiled products are listed in Table 1.

| **Product Long Name** | **Product Short Name** |
|---|---|
| STARS NDVI/Albedo | L2T STARS |
| Ecosystem Auxiliary Inputs | L3T ETAUX |
| Evapotranspiration Ensemble | L3T JET |
| DisALEXI-JPL Evapotranspiration | L3T ET ALEXI |
| Evaporative Stress Index | L4T ESI |
| DisALEXI-JPL Evaporative Stress Index | L4T ESI ALEXI |
| Water Use Efficiency | L4T WUE |

**Table 1.** Listing of ECOSTRESS tiled products long names and short names.

## Cloud-Optimized GeoTIFF Orbit/Scene/Tile Products 

To provide an analysis-ready format, the ECOSTRESS products are
distributed in a tiled form and using the COG format. The tiled products
include the letter T in their level identifiers: L1CT, L2T, L3T, and
L4T. The tiling system used for ECOSTRESS is borrowed from the modified
Military Grid Reference System (MGRS) tiling scheme used by Sentinel 2.
These tiles divide the Universal Transverse Mercator (UTM) zones into
square tiles 109800 m across. ECOSTRESS uses a 70 m cell size with 1568
rows by 1568 columns in each tile, totaling 2.46 million pixels per
tile. This allows the end user to assume that each 70 m ECOSTRESS pixel
will remain in the same location at each timestep observed in analysis.
The COG format also facilitates end-user analysis as a universally
recognized and supported format, compatible with open-source software,
including QGIS, ArcGIS, GDAL, the Raster package in R, rioxarray in
Python, and Rasters.jl in Julia.

Each float32 data layer occupies 4 bytes of storage per pixel, which
amounts to an uncompressed size of 9.83 MB for each tiled data layer.
The uint8 quality flag layers occupy a single byte per pixel, which
amounts to an uncompressed size of 2.46 MB per tiled data quality layer.

Each .tif COG data layer in each L2T/L3T/L4T product additionally
contains a rendered browse image in GeoJPEG format with a .jpeg
extension. This image format is universally recognized and supported,
and these files are compatible with Google Earth. Each L2T/L3T/L4T tile
granule includes a .json file containing the Product Metadata and
Standard Metadata in JSON format.

## Quality Flags

Two high-level quality flags are provided in all gridded and tiled
products as thematic/binary masks encoded to zero and one in unsigned
8-bit integer layers. The cloud layer represents the final cloud test
from L2 CLOUD. The water layer represents the surface water body in the
Shuttle Radar Topography Mission (SRTM) Digital Elevation Model. For
both layers, zero means absence, and one means presence. Pixels with the
value 1 in the cloud layer represent detection of cloud in that pixel.
Pixels with the value 1 in the water layer represent open water surface
in that pixel. All tiled product data layers written in float32 contain
a standard not-a-number (NaN) value at each pixel that could not be
retrieved. The cloud and water layers are provided to explain these
missing values.

## Product Availability

The ECOSTRESS products are available at the NASA Land Processes
Distributed Active Archive Center (LP-DAAC),
https://earthdata.nasa.gov/ and can be accessed via the Earthdata search
engine.

# L2T STARS NDVI and Albedo Product

# L3T ETAUX Ecosystem Auxiliary Inputs Product

The ECOSTRESS JET processing chain is designed to be independently
reproducible. To facilitate open science, the auxiliary data inputs that
are produced for evapotranspiration processing are distributed as a data
product, such that the end user has the ability to run their own
evapotranspiration model using ECOSTRESS data. The data layers of the
L3T ETAUX product are described in Table 3.

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** | **Size** |
|:-------------------------- |:----------------------------- |:-------- |:------ |:--- |:--- |:--- |:--- |:---- |:--------- |
| Ta | Near-surface air temperature | float32 | °C | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| RH | Relative Humidity | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| Rg | Global Radiation | float32 | W m⁻² | NaN | N/A | 0 | N/A | N/A | 9.83 MB |
| Rn | Net Radiation | float32 | W m⁻² | NaN | N/A | 0 | N/A | N/A | 9.83 MB |
| SM | Soil Moisture | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

**Table 3.** Listing of the L3T ETAUX data layers.

## Downscaled Meteorology

Coarse resolution near-surface air temperature (Ta) and relative
humidity (RH) are taken from the GEOS-5 FP tavg1_2d_slv_Nx product. Ta
and RH are down-scaled using a linear regression between up-sampled ST,
NDVI, and albedo as predictor variables to Ta or RH from GEOS-5 FP as a
response variable, within each Sentinel tile. These regression
coefficients are then applied to the 70 m ST, NDVI, and albedo, and this
first-pass estimate is then bias-corrected to the coarse image from
GEOS-5 FP. These downscaled meteorology estimates are recorded in the
L3T ETAUX product listed in Table 3. Areas of cloud are filled in with
bi-cubically resampled GEOS-5 FP.

## Downscaled Soil Moisture

This same down-scaling procedure is applied to soil moisture (SM) from
the GEOS-5 FP tavg1_2d_lnd_Nx product, which is recorded in the L3T ETAUX
product listed in Table 3.

## Surface Energy Balance

The surface energy balance processing for ECOSTRESS begins with an
artificial neural network (ANN) implementation of the Forest Light
Environmental Simulator (FLiES) radiative transfer algorithm (Kobayashi & Iwabuchi, 2008), following
the workflow established by Dr. Hideki Kobayashi and Dr. Youngryel Ryu.
GEOS-5 FP provides sub-daily Cloud Optical Thickness (COT) in the
tavg1_2d_rad_Nx product and Aerosol Optical Thickness (AOT) from
tavg3_2d_aer_Nx. Together with STARS albedo, these variables are run
through the ANN implementation of FLiES to estimate incoming shortwave
radiation (Rg), bias-corrected to Rg from the GEOS-5 FP tavg1_2d_rad_Nx
product.

The Breathing Earth System Simulator (BESS-JPL) algorithm (Ryu et al., 2011; Jiang & Ryu, 2016), contributed by
Dr. Youngryel Ryu, iteratively calculates net radiation (Rn), ET, and
Gross Primary Production (GPP) estimates. The BESS-JPL Rn is used as the Rn
input to the remaining ET models and is recorded in the L3T ETAUX product
listed in Table 3.

# L3T JET Evapotranspiration Product

Following design of the L3T JET product from ECOSTRESS Collection 2, the
Collection 3 L3T JET product uses an ensemble of evapotranspiration
models to produce a daily evapotranspiration estimate.

The PT-JPL-SM model (Purdy et al., 2018), developed by Dr. Adam Purdy and Dr. Joshua Fisher
was designed as a SM-sensitive evapotranspiration product for the Soil
Moisture Active-Passive (SMAP) mission, and then reimplemented as an ET
model in the ECOSTRESS processing chain, using the downscaled
soil moisture from the L3T ETAUX product. Similar to the PT-JPL model used
in ECOSTRESS Collection 1, The PT-JPL-SM model estimates instantaneous
canopy transpiration, leaf surface evaporation, and soil moisture
evaporation using the Priestley-Taylor formula with a set of
constraints. These three partitions are combined into total latent heat
flux in watts per square meter for the ensemble estimate.

The Surface Temperature Initiated Closure (STIC-JPL) model (Mallick et al., 2018), contributed by
Dr. Kaniska Mallick, was designed as a ST-sensitive ET model, adopted by
ECOSTRESS for improved estimates of ET reflecting mid-day heat
stress. The STIC-JPL model estimates total latent heat flux directly. This
instantaneous estimate of latent heat flux is included in the ensemble
estimate.

The PM-JPL (Penman-Monteith) algorithm (Mu et al., 2011; Running et al., 2017) was designed as the ET product for the Moderate
Resolution Imaging Spectroradiometer (MODIS) and then continued as a
Visible Infrared Imaging Radiometer Suite (VIIRS) product. PM-JPL uses a
similar approach to PT-JPL and PT-JPL-SM to independently estimate
vegetation and soil components of instantaneous ET, but using the
Penman-Monteith formula instead of the Priestley-Taylor. The PM-JPL
latent heat flux partitions are summed to total latent heat flux for the
ensemble estimate.

The BESS-JPL model (Ryu et al., 2011; Jiang & Ryu, 2016) is a coupled surface energy balance and photosynthesis
model. The latent heat flux component of BESS-JPL is also included in the
ensemble estimate.

The median of total latent heat flux in watts per square meter from the
PT-JPL-SM, STIC-JPL, PM-JPL, and BESS-JPL models is upscaled to a daily ET estimate
in millimeters per day and recorded in the L3T JET product as ETdaily.
The standard deviation between these multiple estimates of ET is
considered the uncertainty for the ECOSTRESS evapotranspiration product, as
ETuncertainty. The layers for the L3T JET products are listed in
Table 4. Note that the ETdaily product represents the integrated ET
between sunrise and sunset.

| **Name** | **Description** | **Type** | **Units** | **Fill** | **No Data** | **Min** | **Max** | **Scale** | **Size** |
|:-------------------------- |:----------------------------- |:-------- |:------ |:--- |:--- |:--- |:--- |:---- |:--------- |
| PTJPLSMinst | PT-JPL-SM Instantaneous | float32 | W m⁻² | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PTJPLSMdaily | PT-JPL-SM Daily | float32 | mm day⁻¹ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| STICJPLinst | STIC-JPL Instantaneous | float32 | W m⁻² | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| STICJPLdaily | STIC-JPL Daily | float32 | mm day⁻¹ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| BESSJPLdaily | BESS-JPL Daily | float32 | mm day⁻¹ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PMJPLdaily | PM-JPL (MOD16) Daily | float32 | mm day⁻¹ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| ETdaily | Daily Evapotranspiration | float32 | mm day⁻¹ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| ETuncertainty | Daily Evapotranspiration Uncertainty | float32 | mm day⁻¹ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PTJPLSMcanopy | PT-JPL-SM Canopy | float32 | prop. | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| STICJPLcanopy | STIC-JPL Canopy | float32 | prop. | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PTJPLSMsoil | PT-JPL-SM Soil | float32 | prop. | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| PTJPLSMinterception | PT-JPL-SM Interception | float32 | prop. | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

**Table 4.** Listing of the L3T JET data layers.

# L4T ESI & WUE Products

The PT-JPL-SM model generates estimates of both actual and potential
instantaneous ET. The potential evapotranspiration (PET) estimate
represents the maximum expected ET if there were no water stress to
plants on the ground. The ratio of the actual ET estimate to the PET
estimate forms an index representing the water stress of plants, with
zero being fully stressed with no observable ET and one being
non-stressed with ET reaching PET. These ESI and PET estimates are
distributed in the L4T ESI product as listed in Table 5.

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** | **Size** |
|:-------------------------- |:----------------------------- |:-------- |:------ |:--- |:--- |:--- |:--- |:---- |:--------- |
| ESI | Evaporative Stress Index | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| PET | Potential Evapotranspiration | float32 | mm day⁻¹ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

**Table 5.** Listing of the L4T ESI data layers.

The BESS-JPL GPP estimate represents the amount of carbon that plants are
taking in. The transpiration component of PT-JPL-SM represents the
amount of water that plants are releasing. The BESS-JPL GPP is divided by
the PT-JPL-SM transpiration to estimate water use efficiency (WUE), the
ratio of grams of carbon that plants take in to kilograms of water that
plants release. These WUE and GPP estimates are distributed in the L4T
WUE product as listed in Table 6.

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** | **Size** |
|:-------------------------- |:----------------------------- |:-------- |:------ |:--- |:--- |:--- |:--- |:---- |:--------- |
| WUE | Water Use Efficiency | float32 | g C kg⁻¹ H₂O | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| GPP | Gross Primary Production | float32 | μmol m⁻² s⁻¹ | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

**Table 6.** Listing of the L4T WUE data layers.

# Standard Metadata

Each ECOSTRESS product bundle contains two sets of product metadata:

- ProductMetadata

- StandardMetadata

Each product contains a custom set of ProductMetadata attributes, as
listed in Table 7. The StandardMetadata attributes are consistent across
products at each orbit/scene, as listed in Table 8.

| **Name** | **Type** |
|---|---|
| AncillaryInputPointer | string |
| AutomaticQualityFlag | string |
| AutomaticQualityFlagExplanation | string |
| BuildID | string |
| CRS | string |
| CampaignShortName | string |
| CollectionLabel | string |
| DataFormatType | string |
| DayNightFlag | string |
| EastBoundingCoordinate | float |
| FieldOfViewObstruction | string |
| ImageLines | float |
| ImageLineSpacing | integer |
| ImagePixels | float |
| ImagePixelSpacing | integer |
| InputPointer | string |
| InstrumentShortName | string |
| LocalGranuleID | string |
| LongName | string |
| NorthBoundingCoordinate | float |
| PGEName | string |
| PGEVersion | string |
| PlatformLongName | string |
| PlatformShortName | string |
| PlatformType | string |
| ProcessingEnvironment | string |
| ProcessingLevelDescription | string |
| ProcessingLevelID | string |
| ProducerAgency | string |
| ProducerInstitution | string |
| ProductionDateTime | string |
| ProductionLocation | string |
| RangeBeginningDate | string |
| RangeBeginningTime | string |
| RangeEndingDate | string |
| RangeEndingTime | string |
| RegionID | string |
| SISName | string |
| SISVersion | string |
| SceneBoundaryLatLonWKT | string |
| SceneID | string |
| ShortName | string |
| SouthBoundingCoordinate | float |
| StartOrbitNumber | string |
| StopOrbitNumber | string |
| WestBoundingCoordinate | float |

**Table 7.** Name and type of metadata fields contained in the common StandardMetadata group in each L2T/L3T/L4T product.

| **Name** | **Type** |
|---|---|
| BandSpecification | float |
| NumberOfBands | integer |
| OrbitCorrectionPerformed | string |
| QAPercentCloudCover | float |
| QAPercentGoodQuality | float |
| AuxiliaryNWP | string |

**Table 8.** Name and type of metadata fields contained in the common ProductMetadata group in each L2T/L3T/L4T product.

# Acknowledgements

We would like to thank Joshua Fisher as the initial science lead of the
ECOSTRESS mission and PI of the ROSES project to re-design the ECOSTRESS products.

We would like to thank Adam Purdy for contributing the PT-JPL-SM model.

We would like to thank Kaniska Mallick for contributing the STIC-JPL model.

We would like to thank Youngryel Ryu for contributing the BESS-JPL model.

# Bibliography

Jiang, C., & Ryu, Y. (2016). Multi-scale evaluation of global gross primary productivity and evapotranspiration products derived from Breathing Earth System Simulator (BESS). *Remote Sensing of Environment*, 186, 528-547.

Kobayashi, H., & Iwabuchi, H. (2008). A coupled 1-D atmosphere and 3-D canopy radiative transfer model for canopy reflectance, light environment, and photosynthesis simulation in a heterogeneous landscape. *Remote Sensing of Environment*, 112(1), 173-185.

Mallick, K., Jarvis, A. J., Boegh, E., Fisher, J. B., Drewry, D. T., Tu, K. P., ... & Niyogi, D. (2018). A surface temperature initiated closure (STIC) for turbulent sensible and latent heat flux measurements. *Agricultural and Forest Meteorology*, 248, 392-410.

Mu, Q., Zhao, M., & Running, S. W. (2011). Improvements to a MODIS global terrestrial evapotranspiration algorithm. *Remote Sensing of Environment*, 115(8), 1781-1800.

Purdy, A. J., Fisher, J. B., Goulden, M. L., Colliander, A., Halverson, G., Tu, K., ... & Famiglietti, J. S. (2018). SMAP soil moisture improves global evapotranspiration. *Remote Sensing of Environment*, 219, 1-14.

Running, S., Mu, Q., Zhao, M., & Moreno, A. (2017). *MODIS Global Terrestrial Evapotranspiration (ET) Product (NASA MOD16A2/A3) NASA Earth Observing System MODIS Land Algorithm (For Collection 6)*. NASA Goddard Space Flight Center.

Ryu, Y., Baldocchi, D. D., Kobayashi, H., van Ingen, C., Li, J., Black, T. A., ... & Vargas, R. (2011). Integration of MODIS land and atmosphere products with a coupled-process model to estimate gross primary productivity and evapotranspiration from 1 km to global scales. *Global Biogeochemical Cycles*, 25(4).

Schaaf, C. (2017). *VIIRS BRDF, Albedo, and NBAR Product Algorithm Theoretical Basis Document (ATBD).* NASA Goddard Space Flight Center.