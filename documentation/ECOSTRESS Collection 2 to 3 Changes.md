# ECOSTRESS L3/L4 Data Products: Collection 2 vs. Collection 3 Comparison

The transition of ECOSTRESS Level-3 (L3) and Level-4 (L4) data products from Collection 2 (C2) to Collection 3 (C3) introduces structural consolidation, expanded model outputs, standardized daily integrated units, and enhanced metadata.

## 1. Consolidation of Auxiliary Inputs (`L3T ETAUX`)

* **Collection 2 Architecture**: Distributed auxiliary processing inputs across three separate gridded and tiled products: Surface Energy Balance (`L3G/L3T SEB`), Soil Moisture (`L3G/L3T SM`), and Meteorology (`L3G/L3T MET`).
* **Collection 3 Streamlining**: Consolidated these separate inputs into a single, unified product named **Ecosystem Auxiliary Inputs (`L3T ETAUX`)** to facilitate open science and allow users to independently reproduce ET processing chains.
* **`L3T ETAUX` Data Layers**:
  * **`Ta`**: Downscaled near-surface air temperature (°C).
  * **`RH`**: Downscaled relative humidity (ratio 0–1).
  * **`SM`**: Downscaled soil moisture (ratio 0–1).
  * **`Rg`**: Incoming shortwave global radiation (W m⁻²) estimated via an Artificial Neural Network (ANN) implementation of FLiES.
  * **`Rn`**: Net radiation (W m⁻²) calculated via BESS-JPL.

## 2. Expanded Evapotranspiration Ensemble (`L3T JET`)

The Evapotranspiration Ensemble product underwent significant expansions in component outputs, model daily scaling, and flux partitioning:

* **Individual Daily ET Layers**: While Collection 2 only provided instantaneous values for constituent models (`PTJPLSMinst`, `STICinst`, `MOD16inst`, `BESSinst`) alongside integrated daily ensemble ET (`ETdaily`), Collection 3 adds individual integrated daily ET layers (mm day⁻¹) for each constituent model:
  * `PTJPLSMdaily` (Priestley-Taylor JPL Soil Moisture)
  * `STICJPLdaily` (Surface Temperature Initiated Closure)
  * `BESSJPLdaily` (Breathing Earth System Simulator)
  * `PMJPLdaily` (Penman-Monteith JPL, replacing MOD16)
* **Evapotranspiration Partitioning Layers**: Collection 3 introduces proportional flux breakdown layers to isolate canopy, soil, and interception components:
  * `PTJPLSMcanopy` & `STICJPLcanopy` (proportions)
  * `PTJPLSMsoil` (proportion)
  * `PTJPLSMinterception` (proportion)
* **Uncertainty Alignment**: In Collection 2, uncertainty was provided as instantaneous latent heat flux standard deviation (`ETinstUncertainty` in W m⁻²). In Collection 3, `ETuncertainty` is expressed directly in daily integrated units (mm day⁻¹) to match `ETdaily`.

## 3. Level 4 Product Updates (`L4T ESI` & `L4T WUE`)

* **Unit Alignment for Potential Evapotranspiration (`PET`)**:
  * **Collection 2**: Potential Evapotranspiration (`PET`) in `L4T ESI` was distributed in instantaneous rate units of W m⁻².
  * **Collection 3**: `PET` units are converted to mm day⁻¹, directly aligning with daily actual ET metrics.
* **Methodological Clarity for Water Use Efficiency (`WUE`)**:
  * In Collection 3, `WUE` (g C kg⁻¹ H₂O) is explicitly defined as the ratio of BESS-JPL Gross Primary Production (`GPP`, μmol m⁻² s⁻¹) to PT-JPL-SM canopy transpiration.

## 4. Standardized Quality Masks, Format & Metadata

* **Explicit Granule Quality Masks**: Every tiled granule layer in Collection 3 (`L3T ETAUX`, `L3T JET`, `L4T ESI`, `L4T WUE`) incorporates two standardized 8-bit uint8 binary mask layers: `cloud` (1 = cloud present) and `water` (1 = open water present).
* **JSON Metadata Granules**: Each Collection 3 tile granule bundle adds a dedicated `.json` metadata file containing both `StandardMetadata` (common orbit/scene/tile attributes) and `ProductMetadata` (specific dataset parameters).
* **Embedded GeoJPEG Browse Images**: Collection 3 tile granules provide a Google Earth-compatible GeoJPEG (`.jpeg`) browse rendering for each GeoTIFF (`.tif`) raster layer.

## 5. Side-by-Side L3/L4 Product Comparison

| Category / Product | Collection 2 | Collection 3 |
| :--- | :--- | :--- |
| **Auxiliary Products** | Distributed across three separate products (`L3T SEB`, `L3T SM`, `L3T MET`). | Consolidated into a single **`L3T ETAUX`** product (`Ta`, `RH`, `SM`, `Rg`, `Rn`). |
| **Ensemble Model Inputs** | PT-JPL-SM, STIC, MOD16, BESS. | PT-JPL-SM, STIC-JPL, PM-JPL, BESS-JPL. |
| **Constituent Model ET Layers** | Instantaneous estimates (W m⁻²). | Daily estimates (mm day⁻¹) and instantaneous estimates (W m⁻²). |
| **ET Partitioning** | Not provided in JET product. | Added canopy, soil, and interception proportion layers. |
| **ET Uncertainty Units** | W m⁻² (`ETinstUncertainty`). | mm day⁻¹ (`ETuncertainty`). |
| **`L4T ESI` PET Units** | W m⁻². | mm day⁻¹. |
| **Quality Flags & Metadata** | Basic quality layers. | Standardized uint8 `cloud`/`water` masks, embedded GeoJPEG browse images, and JSON metadata (`StandardMetadata` & `ProductMetadata`). |
