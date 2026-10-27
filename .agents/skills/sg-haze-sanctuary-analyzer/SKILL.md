---
name: sg-haze-sanctuary-analyzer
description: Compute Singapore spatio-temporal Haze Sanctuary Index (HSI) across all 332 URA Subzones, 55 Planning Areas, 28 Postal Districts (D01-D28), and 6-digit Postal Codes from 18 Sep 1997 to present by fusing NEA PSI/PM2.5, MSS wind vectors, ASMC satellite AOD, and OneMap GIS layers. Use when analyzing Singapore air quality, haze refuges, microclimates, or subzone pollution exposure.
---
# Singapore Haze Sanctuary Analyzer

Compute high-resolution spatio-temporal air quality and haze exposure scores across Singapore's 332 URA Subzones, 55 Planning Areas, 28 Postal Districts (D01-D28), 82 Postal Sectors (01-82), and 6-digit Postal Codes from the first unhealthy PSI reading on 18 September 1997 to the present.

## When to Use

- Analyzing historical or real-time Singapore PSI and 1-hr PM2.5 readings across regions, planning areas, subzones, or postal codes
- Determining the cleanest microclimates and empirical "haze sanctuaries" during Southwest Monsoon (Sumatra) or Inter-Monsoon/Southeast (Kalimantan) haze episodes
- Fusing NEA ground telemetry, MSS wind vector fields, ASMC satellite hotspot/aerosol optical depth (AOD), and URA Master Plan GIS boundaries
- Building client-side WebGIS choropleths or educational dashboards with robust search and sanctuary routing

## Core Workflow

### 1. Ingest Temporal Baseline (1997–Present)
- Query NEA real-time and historical endpoints (`https://api-open.data.gov.sg/v2/real-time/api/psi` and `pm25`) and merge with archival crisis records (18 Sep 1997, Jun 2013, Sep–Oct 2015, Sep 2019, Oct 2023, Sep–Oct 2026).
- Segment records by prevailing synoptic wind transport regimes:
  - **Sumatra SW Plume Corridor ($195^\circ\text{–}255^\circ$)**: Direct advection into Tuas View, Pioneer, Jurong Island, and Boon Lay (D22). Overland fetch across the 42 km island axis dilutes smoke by >90% before reaching District 17.
  - **Kalimantan SE/S Plume Corridor ($120^\circ\text{–}195^\circ$)**: Initial coastal landfall along Southern Islands, Telok Blangah, Marina South, Downtown Core, and East Coast (D01, D02, D04, D15).
  - **Johor Strait NE Marine Inflow ($040^\circ\text{–}080^\circ$)**: Clean marine boundary-layer sea breeze undercuts smoke layers along Changi Point, Loyang, Pasir Ris, Pulau Ubin, Coney Island, and Sembawang (D17, D18, D19, D27).

### 2. Physical & Meteorological Dispersion Engine
Calculate localized concentration $C_s(t)$ and normalized **Haze Sanctuary Index ($\text{HSI}_s \in [0, 100]$)**:

$$C_s(t) = C_{\text{NEA}}(r, t) + \Delta C_{\text{advection}}(s, \theta_t) - \Delta C_{\text{sea}}(s) + \Delta C_{\text{UHI}}(s) - \Delta C_{\text{canopy}}(s)$$

$$\text{HSI}_s = \max\left(0, \min\left(100, 100 - (C_s(t) - 40.0) \times 0.42\right)\right)$$

Where:
- $\Delta C_{\text{advection}}$:
  - If $195^\circ \le \theta \le 255^\circ$: $45.0 \cdot \exp(-d_{\text{west\_coast}} / 14.0)$
  - If $120^\circ \le \theta \le 195^\circ$: $38.0 \cdot \exp(-d_{\text{south\_coast}} / 12.0)$
  - Else: $15.0$
- $\Delta C_{\text{sea}}$: $28.5 \cdot f_{\text{flush}} \cdot \exp(-d_{\text{johor\_strait}} / 3.8)$ (Johor Strait marine flushing)
- $\Delta C_{\text{UHI}}$: $16.5 \cdot \text{SVF}(s)$ (Urban canyon nocturnal thermal inversion trapping between 02:00–08:30 SGT)
- $\Delta C_{\text{canopy}}$: $12.0 \cdot \text{NDVI}(s)$ (Vegetative mangrove and rainforest dry-deposition scavenging)

### 3. Spatial Crosswalk Across All 28 Postal Districts
Run `scripts/postal_subzone_crosswalk.py` to map subzones and postal codes to all 28 Postal Districts (D01–D28) and 82 Postal Sectors (01–82). Note that Subzone #13 (`jurong_east_bukit_batok`) includes Sector 60 (`608532` JEM/Westgate), which belongs to **District 22 (`D22`)**, requiring classification as `D05 / D21 / D22 / D23`.

### 4. Verified Ground-Truth Sanctuary Hierarchy
- **Tier 1 Prime Refuges (HSI ≥ 85)**:
  - **#1 Offshore Island**: Pulau Ubin (D17, Sector 50, Postal Code `508329`, HSI **96.4**)
  - **#1 Mainland Coastal**: Changi Point (D17, Sectors 49/81, Postal Code `498991`, HSI **94.8**)
  - **#2 Residential Core**: Loyang West & Pasir Ris Park (D17/D18, Sectors 50/51, Postal Code `519914`, HSI **92.1**)
  - **#3 Far-North Eco-Coastal**: Coney Island & Punggol Point (D19, Sector 82, Postal Code `829325`, HSI **90.4**)
  - **#4 North Strait Shoreline**: Sembawang Straits & Wak Hassan (D27, Sectors 75/76, Postal Code `759819`, HSI **88.9**)
  - **#1 Central Forest Buffer**: Springleaf & Central Catchment (D26, Sectors 77/78, Postal Code `787130`, HSI **85.2**)
- **Tier 2 High/Moderate Towns (HSI 75–84)**:
  - Kranji & Sungei Buloh (D24/D25, HSI **81.5**)
  - Tampines & Bedok North (D16/D18, HSI **77.8**)
  - Serangoon & Hougang (D19/D28, HSI **75.4**)
- **Tier 3 Urban Inversion & Coastal Landfall (HSI 60–74)**:
  - Marine Parade & Katong (D15, HSI **68.2**)
  - Downtown Core, Marina & Orchard (D01/D02/D09, HSI **61.5**)
- **Tier 4 Acute Hazard Corridors (HSI < 60)**:
  - Telok Blangah, HarbourFront & Sentosa (D03/D04, HSI **58.4**)
  - Jurong East, Clementi & Bukit Batok (D05/D21/D22/D23, HSI **55.8**)
  - Tuas View, Pioneer, Boon Lay & Jurong Island (D22, HSI **48.2**)

## Gotchas

1. **Avoid Single-Episode Ranking Skew**:
   Never base general subzone sanctuary rankings on a single episode. Evaluating solely on a Southwest plume episode (like 2026) artificially penalizes northern eco-sanctuaries (Coney Island, Springleaf) and boosts East inland towns (Tampines East). Always rank overall sanctuaries by their 29-year multi-episode composite mean exposure.
2. **Expand En-Dash Postal Sector Ranges in UI Search**:
   When storing sector strings with en-dashes (e.g. `"01–08"`, `"14–16"`, `"65–68"`), front-end search engines using `.includes(prefix)` will fail on intermediate sectors (e.g. `02`, `07`, `15`, `66`). Always programmatically expand dash ranges into discrete 2-digit sector arrays during indexing.
3. **Never Use Uncalibrated Regional Fallbacks in District Plots**:
   In postal district bar charts, never assign flat high fallbacks (such as `88.0`) to unmatched districts based on coarse `"East" in reg` checks, as this matches `"North-East"` and elevates non-coastal districts (D14, D20, D28) above actual sanctuaries (D17).
4. **Distinguish Peak 3-hr Spikes from 24-hr Baselines**:
   Tuas reached an official 3-hr peak PSI of 401 during the June 2013 emergency, whereas 24-hr regional baselines were ~246. Ensure dynamic chart canvases and static atlas figures explicitly declare whether they represent 3-hr peak spikes or 24-hr rolling baselines.
