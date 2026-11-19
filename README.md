# ECOSTRESS Level 3 and 4 Evapotranspiration, Evaporative Stress Index, Water Use Efficiency

[![CI](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/actions/workflows/ci.yml/badge.svg)](https://github.com/ECOSTRESS-Collection-3/ECOv003-L3T-L4T-JET/actions/workflows/ci.yml)

This is the main repository for the ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) collection 3 level 3/4 evapotranspiration data products algorithm.

The ECOSTRESS collection 3 level 3/4 evapotranspiration data products algorithm is the pre-cursor to the [Surface Biology and Geology (SBG) collection 1 level 4 evapotranspiration data products algorithm](https://github.com/sbg-tir/SBG-TIR-L4-JET).

[Gregory H. Halverson](https://github.com/gregory-halverson-jpl) (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G

[Kerry Cawse-Nicholson](https://github.com/kcawse) (she/her)<br>
[kerry-anne.cawse-nicholson@jpl.nasa.gov](mailto:kerry-anne.cawse-nicholson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G

[Madeleine Pascolini-Campbell](https://github.com/madeleinepc) (she/her)<br>
[madeleine.a.pascolini-campbell@jpl.nasa.gov](mailto:madeleine.a.pascolini-campbell@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329F

[Evan Davis](https://github.com/evandjpl) (he/him)<br>
[evan.w.davis@jpl.nasa.gov](mailto:evan.w.davis@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 397K

[Claire Villanueva-Weeks](https://github.com/clairesvw) (she/her)<br>
NASA Jet Propulsion Laboratory 329G

The code for the ECOSTRESS level 3 JET PGE has been developed using open-science practices based on the [ECOSTRESS Collection 2 JET PGE](https://github.com/ECOSTRESS-Collection-2/ECOv002-L3T-L4T-JET) with New Technology Report (NTR) and open-source license from NASA Jet Propulsion Laboratory.

The repositories for the evapotranspiration algorithms are located in the [JPL-Evapotranspiration-Algorithms](https://github.com/JPL-Evapotranspiration-Algorithms) organization.

## 1. Introduction 

This software produces estimates of:
- evapotranspiration (ET)
- evaporative stress index (ESI)
- water use efficiency (WUE)

Evapotranspiration (ET) is one of the main science outputs from the ECOSTRESS mission. ET is a Level-3 (L3) product constructed from a combination of the ECOSTRESS Level-2 (L2) Land Surface Temperature & Emissivity (LSTE) product and auxiliary data sources. Accurate modelling of ET requires consideration of many environmental and biological controls including: solar radiation, the atmospheric water vapor deficit, soil water availability, vegetation physiology and phenology (Brutsaert, 1982; Monteith, 1965; Penman, 1948). Scientists develop models that ingest global satellite observations to capture these environmental and biological controls on ET. LST holds the unique ability to capture when and where plants experience stress, as observed by elevated temperatures which can idenitfy areas that have a reduced capacity to evaporate or transpire water to the atmosphere (Allen et al., 2007). The ECOSTRESS evapotranspiration product combines the [surface temperature and emissivity observations from the ECOSTRESS sensor](https://github.com/ECOSTRESS-Collection-3/ECOv003-L2-LSTE) with the [NDVI and albedo estimated by STARS](https://github.com/ECOSTRESS-Collection-3/ECOv003-L2-STARS), estimates near-surface meteorology by downscaling GEOS-5 FP to these three high resolution images, and runs these variables through a set of surface energy balance models.

The repositories for the evapotranspiration algorithms are located in the [JPL-Evapotranspiration-Algorithms](https://github.com/JPL-Evapotranspiration-Algorithms) organization.

## 2. Data Products 

### 2.1. Metadata

Metadata for the ECOSTRESS Collection 3 tiled products is provided in JSON format:
```json
{
  "StandardMetadata": {
    "AuxiliaryInputPointer": "AuxiliaryNWP",
    "AutomaticQualityFlag": "PASS",
    "AutomaticQualityFlagExplanation": "Image matching performed to correct orbit ephemeris/attitude",
    "BuildID": "0700",
    "CRS": "+proj=utm +zone=11 +datum=WGS84 +units=m +no_defs +type=crs",
    "CampaignShortName": "Primary",
    "CollectionLabel": "ECOv003",
    "DataFormatType": "COG",
    "DayNightFlag": "Day",
    "EastBoundingCoordinate": -114.74406148409601,
    "ImageLineSpacing": 70.0,
    "ImageLines": 1568,
    "ImagePixelSpacing": 70.0,
    "ImagePixels": 1568,
    "InputPointer": "ECOv003_L2T_LSTE_21485_013_11SPS_20220420T211350_0700_01.zip,ECOv003_L2T_STARS_21485_013_11SPS_20220420_0700_01.zip",
    "InstrumentShortName": "ECOSTRESS",
    "LocalGranuleID": "ECOv003_L3T_JET_21485_013_11SPS_20220420T211350_0700_01.zip",
    "LongName": "ECOSTRESS Tiled Evapotranspiration Ensemble Instantaneous and Daytime L3 Global 70 m",
    "NorthBoundingCoordinate": 33.43490918842431,
    "PGEName": "L3T_L4T_JET",
    "PGEVersion": "1.20.3",
    "PlatformLongName": "ISS",
    "PlatformShortName": "ISS",
    "PlatformType": "Spacecraft",
    "ProcessingEnvironment": "Linux eco-p44.tir 3.10.0-1160.45.1.el7.x86_64 #1 SMP Wed Oct 13 17:20:51 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux",
    "ProcessingLevelDescription": "Level 3 Tiled Evapotranspiration Ensemble",
    "ProcessingLevelID": "L3T",
    "ProducerAgency": "JPL",
    "ProducerInstitution": "Caltech",
    "ProductionDateTime": "2022-04-22T10:47:36.452Z",
    "ProductionLocation": "ECOSTRESS Science Computing Facility",
    "RangeBeginningDate": "2022-04-20",
    "RangeBeginningTime": "21:13:51.290937",
    "RangeEndingDate": "2022-04-20",
    "RangeEndingTime": "21:18:51.290937",
    "RegionID": "11SPS",
    "SISName": "Level 3 Product Specification Document",
    "SISVersion": "Preliminary",
    "SceneBoundaryLatLonWKT": "POLYGON ((-118.30553175600564 30.910805591562212, -115.4606649798732 33.891051544444885, -112.80123658401774 31.518067522267156, -115.65618262396845 28.61321628442961, -118.30553175600564 30.910805591562212))",
    "SceneID": "13",
    "ShortName": "ECO_L3T_JET",
    "SouthBoundingCoordinate": 32.42972726825087,
    "StartOrbitNumber": "21485",
    "StopOrbitNumber": "21485",
    "WestBoundingCoordinate": -115.9361545299493
  },
  "ProductMetadata": {
    "BandSpecification": [
      0.0,
      0.0,
      8.779999732971191,
      0.0,
      10.520000457763672,
      12.0
    ],
    "NumberOfBands": 3,
    "OrbitCorrectionPerformed": "True",
    "QAPercentCloudCover": 0.009151460329029571,
    "QAPercentGoodQuality": 98.34781568877551,
    "AuxiliaryNWP": "GEOS.fp.asm.inst3_2d_asm_Nx.20220420_2100.V01.nc4,GEOS.fp.asm.inst3_2d_asm_Nx.20220421_0000.V01.nc4,GEOS.fp.asm.tavg1_2d_lnd_Nx.20220420_2030.V01.nc4,GEOS.fp.asm.tavg1_2d_lnd_Nx.20220420_2130.V01.nc4,GEOS.fp.asm.tavg1_2d_rad_Nx.20220420_2030.V01.nc4,GEOS.fp.asm.tavg1_2d_rad_Nx.20220420_2130.V01.nc4,GEOS.fp.asm.tavg1_2d_slv_Nx.20220420_2030.V01.nc4,GEOS.fp.asm.tavg1_2d_slv_Nx.20220420_2130.V01.nc4,GEOS.fp.asm.tavg3_2d_aer_Nx.20220420_1930.V01.nc4,GEOS.fp.asm.tavg3_2d_aer_Nx.20220420_2230.V01.nc4,GEOS.fp.asm.tavg3_2d_chm_Nx.20220420_1930.V01.nc4,GEOS.fp.asm.tavg3_2d_chm_Nx.20220420_2230.V01.nc4"
  }
}
```

#### 2.1.1. Standard Metadata
Information on the `StandardMetadata` is included on the [ECOSTRESS GitHub landing page](https://github.com/ECOSTRESS-Collection-3)

#### 2.1.2. Product Metadata

| **Name** | **Type** |
| --- | --- |
| BandSpecification | float |
| NumberOfBands | integer |
| OrbitCorrectionPerformed | string |
| QAPercentCloudCover | float |
| QAPercentGoodQuality | float |
| AuxiliaryNWP | string |

*Table 9. Name and type of metadata fields contained in the common ProductMetadata group in each L2T/L3T/L4T product.*

| **Product Long Name** | **Product Short Name** |
| --- | --- |
| STARS NDVI/Albedo | L2T STARS |
| Ecosystem Auxiliary Inputs | L3T ETAUX |
| Evapotranspiration | L3T JET |
| Evaporative Stress Index | L4T ESI |
| Water Use Efficiency | L4T WUE |

*Table 1. Listing of ECOSTRESS ecosystem products long names and short names.*

### 2.2. Quality Flags

Two high-level quality flags are provided in all gridded and tiled products as thematic/binary masks encoded to zero and one in unsigned 8-bit integer layers. The cloud layer represents the final cloud test from L2 CLOUD. The water layer represents the surface water body in the Shuttle Radar Topography Mission (SRTM) Digital Elevation Model. For both layers, zero means absence, and one means presence. Pixels with the value 1 in the cloud layer represent detection of cloud in that pixel. Pixels with the value 1 in the water layer represent open water surface in that pixel. All tiled product data layers written in `float32` contain a standard not-a-number (`NaN`) value at each pixel that could not be retrieved. The cloud and water layers are provided to explain these missing values.

### 2.3. L3T ETAUX Ecosystem Auxiliary Inputs Product

The ECOSTRESS ecosystem processing chain is designed to be independently reproducible. To facilitate open science, the auxiliary data inputs that are produced for evapotranspiration processing are distributed as a data product, such that the end user has the ability to run their own evapotranspiration model using ECOSTRESS data. The data layers of the L3T ETAUX product are described in Table 2.

| **Name** | **Description** | **Type** | **Units** | **Fill Value** | **No Data Value** | **Valid Min** | **Valid Max** | **Scale Factor** |**Size** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -- |
| Ta | Near-surface air temperature | float32 | Celsius | NaN | N/A | N/A | N/A | N/A | 9.83 MB |
| RH | Relative Humidity | float32 | Ratio | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| SM | Soil Moisture | float32 | m³/m³ | NaN | N/A | 0 | 1 | N/A | 9.83 MB |
| Rg | Global Radiation | float32 | W/m^2 | NaN | N/A | 0 | N/A | N/A | 9.83 MB |
| Rn | Net Radiation | float32 | W/m^2 | NaN | N/A | 0 | N/A | N/A | 9.83 MB |
| cloud | Cloud mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |
| water | Water mask | uint8 | Mask | 255 | N/A | 0 | 1 | N/A | 2.46 MB |

*Table 2. Listing of the L3T ETAUX data layers.*

### 2.4. Downscaled Meteorology & Soil Moisture

Coarse resolution near-surface air temperature (Ta) and relative humidity (RH) are taken from the GEOS-5 FP `tavg1_2d_slv_Nx` product. Ta and RH are down-scaled using a linear regression between up-sampled ST, NDVI, and albedo as predictor variables to Ta or RH from GEOS-5 FP as a response variable, within each Sentinel tile. These regression coefficients are then applied to the 70 m ST, NDVI, and albedo, and this first-pass estimate is then bias-corrected to the coarse image from GEOS-5 FP. These downscaled meteorology estimates are recorded in the L3T ETAUX product listed in Table 2. Areas of cloud are filled in with bilinearly resampled GEOS-5 FP (`downsampling = "linear"`). This same down-scaling procedure is applied to soil moisture (SM) from the GEOS-5 FP `tavg1_2d_lnd_Nx` product, which is recorded in the L3T ETAUX product listed in Table 2.

### 2.5. Surface Energy Balance

The surface energy balance processing for ECOSTRESS begins with an artificial neural network (ANN) implementation of the Forest Light Environmental Simulator (FLiES) radiative transfer algorithm, following the workflow established by Dr. Hideki Kobayashi and Dr. Youngryel Ryu. GEOS-5 FP provides sub-daily Cloud Optical Thickness (COT) in the `tavg1_2d_rad_Nx` product and Aerosol Optical Thickness (AOT) from `tavg3_2d_aer_Nx`. Together with STARS albedo, these variables are run through the ANN implementation of FLiES to estimate incoming shortwave radiation (Rg), bias-corrected to Rg from the GEOS-5 FP `tavg1_2d_rad_Nx` product.

Net radiation (`Rn`) is computed using the Verma net radiation model (`RN_MODEL_NAME = "verma"`) and recorded in the L3T ETAUX product listed in Table 2. The Breathing Earth System Simulator-Jet Propulsion Laboratory (BESS-JPL) algorithm, contributed by Dr. Youngryel Ryu, iteratively calculates ET and Gross Primary Production (GPP) estimates for inclusion in the ensemble and WUE products.
