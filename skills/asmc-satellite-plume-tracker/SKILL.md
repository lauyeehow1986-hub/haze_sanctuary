---
name: asmc-satellite-plume-tracker
description: Retrieve and process satellite fire hotspots, smoke plume polygons, and Aerosol Optical Depth (AOD) over Singapore, Sumatra, and Kalimantan from ASMC, NASA FIRMS (VIIRS/MODIS), Sentinel-5P TROPOMI, and Himawari-8/9 via Google Earth Engine.
---
# ASMC & Satellite Smoke Plume Tracker

Extract transboundary fire hotspot coordinates, smoke plume trajectories, and 1km Aerosol Optical Depth (AOD) grids across Sumatra, Kalimantan, the Malacca/Singapore Straits, and Singapore Island.

## When to Use

- Overlaying satellite aerosol density (`MODIS MCD19A2` 1km MAIAC AOD or `Sentinel-5P TROPOMI` Absorbing Aerosol Index) onto Singapore URA subzones
- Tracking fire hotspot clusters in Riau, Jambi, South Sumatra, and West/Central Kalimantan via ASMC and NASA FIRMS

## Steps

1. **Query Satellite Collections in Earth Engine**:
   - `MODIS/061/MCD19A2_GRANULES` (`Optical_Depth_055` at 1km resolution) from 2000 to present
   - `COPERNICUS/S5P/OFFL/L3_AER_AI` (`absorbing_aerosol_index`) from 2018 to present
   - `TOMS/MERGED` & `COPERNICUS/CAMS/NRT` for 1997 El Niño aerosol reconstruction
2. **Compute Upwind Plume Intersection**:
   - Trace backward HYSPLIT / kinematic 850hPa–1000hPa trajectories from each Singapore subzone centroid over 24 hours.
