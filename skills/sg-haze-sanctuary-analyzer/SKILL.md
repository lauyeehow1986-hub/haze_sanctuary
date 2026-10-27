---
name: sg-haze-sanctuary-analyzer
description: Compute Singapore spatio-temporal Haze Sanctuary Index (HSI) across all 332 URA Subzones, 55 Planning Areas, 28 Postal Districts (D01-D28), and 6-digit Postal Codes from 18 Sep 1997 to present by fusing NEA PSI/PM2.5, MSS wind vectors, ASMC satellite AOD, and OneMap GIS layers. Use when analyzing Singapore air quality, haze refuges, microclimates, or subzone pollution exposure.
---
# Singapore Haze Sanctuary Analyzer

Compute high-resolution spatio-temporal air quality and haze exposure scores across Singapore's 332 URA Subzones, 55 Planning Areas, 28 Postal Districts (D01-D28), and 6-digit Postal Codes from the first unhealthy PSI reading on 18 September 1997 to the present.

## When to Use

- Analyzing historical or real-time Singapore PSI and 1-hr PM2.5 readings across regions, planning areas, subzones, or postal codes
- Finding the cleanest microclimate or "haze sanctuary" during Southwest Monsoon (Sumatra) or Inter-Monsoon/Southeast (Kalimantan) haze episodes
- Fusing NEA ground sensors, MSS wind vector fields, ASMC satellite hotspot/aerosol plumes, and URA Master Plan GIS polygons
- Building interactive maps or educational dashboards for Singapore environmental resilience

## Core Workflow

1. **Ingest Temporal Baseline (1997-Present)**:
   - Query NEA real-time and historical APIs (`https://api-open.data.gov.sg/v2/real-time/api/psi` and `pm25`) and merge with archival haze crisis datasets (18 Sep 1997, Jun 2013, Sep-Oct 2015, Sep 2019, Sep-Oct 2026).
   - Segment hourly records by prevailing MSS 10m wind direction:
     - **Sumatra SW Plume ($200^\circ\text{--}250^\circ$)**: Direct advection into Tuas, Jurong Island, and Western Catchment (D22).
     - **Kalimantan SE/S Plume ($130^\circ\text{--}190^\circ$)**: Advection into Southern Islands, Marina South, Downtown Core, and East Coast (D01, D02, D04, D15).
     - **Johor Strait / NE Sea-Breeze Flushing ($040^\circ\text{--}080^\circ$)**: Clean marine boundary-layer inflow across Changi Point, Loyang, Pasir Ris, Pulau Ubin, Coney Island, and Sembawang (D17, D18, D19, D27).

2. **Spatial Downscaling to 332 URA Subzones & Postal Codes**:
   - Run `scripts/compute_hsi_kriging.py` to apply wind-aligned anisotropic kriging between NEA's 5 regional reporting nodes (North, South, East, West, Central), satellite MAIAC 1km Aerosol Optical Depth (AOD), urban sky-view factor (SVF) heat-island penalties, and coastal sea-breeze flushing coefficients.
   - Map each subzone polygon to its intersecting 2-digit Postal Sectors (01-82), Postal Districts (D01-D28), and SLA OneMap 6-digit building centroids.

3. **Verify Output Metrics**:
   - Confirm that every subzone record includes: `subzone_name`, `planning_area`, `region`, `postal_district`, `postal_sectors`, `sample_postal_codes`, `mean_haze_psi_all_episodes`, `sumatra_regime_psi`, `kalimantan_regime_psi`, `unhealthy_hours_since_1997`, and `haze_sanctuary_index` (0-100).

## Gotchas

- Never treat NEA's 5 regional numbers as uniform flat blocks; coastal boundary-layer flushing along the Johor Strait reduces ground-level PM2.5 by 14-28% in Changi Point (D17) and Pulau Ubin compared to inland Tampines or Bedok within the same East Region.
- Account for diurnal boundary-layer collapse between 02:00 and 08:00 SGT, when urban heat retention traps smoke in high-density Central/South canyons (D01/D02/D09).
