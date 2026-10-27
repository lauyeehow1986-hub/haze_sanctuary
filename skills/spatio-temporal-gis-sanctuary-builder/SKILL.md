---
name: spatio-temporal-gis-sanctuary-builder
description: Fuse historical and real-time environmental telemetry (air quality, haze, urban heat, flood risk, noise, weather vectors), satellite Earth observation (AOD, thermal, NDVI), and GIS administrative boundaries (regions, planning areas, subzones, postal districts, postal codes) into a ranked Sanctuary/Exposure Index, interactive GitHub-Pages WebGIS app, and downloadable Antigravity IDE Skills + MCP Server kit. Use whenever the user asks to find the safest, cleanest, coolest, or least-affected microclimate or location over time, map environmental/climate hazards against GIS subzones or postal codes, or package a geospatial/telemetry project into an Antigravity master prompt and MCP bundle.
allowed-tools: google default_api image_gen skills
---

# Spatio-Temporal GIS Sanctuary & Antigravity Kit Builder

End-to-end workflow for fusing multi-decade environmental sensor time-series, directional wind/flow vectors, satellite remote sensing layers, and granular GIS polygons (down to subzone, postal district, and postal code) to identify microclimate refuges ("sanctuaries") and package the results into an interactive GitHub-ready WebGIS application plus an importable Antigravity IDE Skills & MCP Server kit.

## When to Use

- Finding the least-affected or safest microclimate/refuge across any city, island, or country for environmental hazards such as transboundary haze/PM2.5, urban heat islands (UHI), pluvial/coastal flooding, wildfire smoke, pollen, or industrial emissions
- Overlapping hourly, diurnal, and multi-year historical telemetry with nested GIS hierarchies (Regions -> Planning Areas -> Subzones -> Postal Districts -> Postal Sectors -> Building Postal Codes)
- Generating a complete **Antigravity IDE Kit** containing a high-effort Master Prompt, custom FastMCP servers, sub-skills, dependency manifests (`requirements.txt`, `package.json`, `environment.yml`, `mcp_config.json`, `setup.sh`), and a zero-backend GitHub Pages WebGIS explorer

## Step-by-Step Workflow

### Step 1: Establish the Temporal Baseline & Regime Segmentation

1. **Anchor First Historical Threshold Date ($t_0$)**:
   - Identify the exact historical date when the hazard first crossed the critical threshold in official records (e.g., 18 Sep 1997 for Singapore Unhealthy PSI >100) and collect all major episodes from $t_0$ to present.
2. **Segment by Advection / Synoptic Regimes**:
   - Partition hourly and daily time-series by directional transport vectors (e.g., Southwest Monsoon vs. Southeast Inter-Monsoon plumes, coastal sea-breeze inflows, or nocturnal calm thermal inversions) rather than using flat annual averages that obscure directional shelters.
3. **Harmonize Sensor Revisions**:
   - Account for historical methodology shifts across multi-decade datasets (for example, pre-2014 vs. post-2014 PSI/AQI sub-index definitions) using validated conversion ratios before computing cumulative exceedance hours.

### Step 2: Execute Multi-Layer GIS & Satellite Downscaling

1. **Build the Nested Spatial Crosswalk**:
   - Map coarse monitoring station regions onto fine administrative polygons (Planning Areas, Subzones, Census Tracts) and postal geometries (Postal Districts, 2-digit Sectors, 6-digit building centroids) in a metric local projection (e.g., `EPSG:3414` SVY21 or local UTM zone).
2. **Compute the Composite Sanctuary Index ($	ext{SI}_s \in [0, 100]$)**:
   - Run `scripts/anisotropic_sanctuary_scorer.py` to combine:
     - **Anisotropic Upwind Kriging ($w_{	ext{IDW}}$)**: Interpolate ground station readings along the prevailing wind/flow vector $ec{u}(t)$.
     - **Satellite Aerosol / Thermal / Canopy Layer ($	ext{Sat}_s$)**: Fuse 1km MAIAC AOD (`MCD19A2`), Sentinel-5P TROPOMI, or Landsat/MODIS land-surface temperature and vegetative NDVI dry-deposition buffers.
     - **Boundary-Layer Flushing Bonus ($V_{	ext{coast}}$)**: Reward upwind maritime channels or valley breeze corridors that undercut and flush ground-level pollutants during afternoon sea-breeze reversals.
     - **Urban Canyon / Topographic Trapping Penalty ($	ext{SVF}_s$)**: Penalize high-density street canyons (low Sky-View Factor) or topographic basins where nocturnal thermal inversions trap pollutants between 01:00 and 08:30 local time.

### Step 3: Build the Self-Contained GitHub-Pages WebGIS Application

1. **Generate Visual Telemetry Assets**:
   - Call `image_gen:generate_image` (`aspect_ratio="16:9"`, `"clean composition, text-free, no labels, no watermarks"`) to create a dark-mode satellite/GIS dispersion banner and inline it as a base64 data URI.
2. **Include Mandatory Interactive Controls**:
   - **Interactive SVG/Canvas Choropleth + Streamline Map**: Clickable subzone/district polygons with animated wind/plume vector streamlines.
   - **Temporal Time-Machine & Diurnal Slider**: Filter by historical crisis episode, wind regime, and hour of day (00:00-23:00) with instantaneous recalculation of subzone scores.
   - **Postal Code / District / Subzone Search**: Instant lookup that resolves any postal code or district to its sanctuary rank, historical peak exposure, and nearest recommended refuge spot.
   - **Copy-Paste Antigravity Drawer**: Built-in tab allowing users to copy the Master Prompt and `mcp_config.json` with one click.
3. **Validate Zero-Backend Readiness**:
   - Run `check_web_app.py` to verify zero broken handlers, zero external local file dependencies, and full responsiveness across mobile, tablet, and desktop viewports.

### Step 4: Package the Antigravity IDE Skills & MCP ZIP Archive

1. **Generate the Antigravity Kit Directory (`scripts/scaffold_antigravity_kit.py`)**:
   - `ANTIGRAVITY_MASTER_PROMPT.md`: Copy-pasteable prompt engineered for high-effort reasoning (`gemini-3.8-flash` high effort) containing the exact mathematical equations, data endpoints, ground-truth validation benchmarks, and execution steps.
   - `skills/`: Modular sub-skills (`*-telemetry-ingestor`, `*-gis-subzone-interpolator`, `*-satellite-plume-tracker`, `browser-computer-use-scraper`, `github-pages-publisher`) with runnable Python helper scripts.
   - `mcp-servers/`: Ready-to-run `FastMCP` Python servers for live telemetry APIs, geocoding/GIS spatial queries, satellite Earth Engine extraction, and Playwright computer-use scraping.
   - `mcp_config.json`, `requirements.txt`, `package.json`, `environment.yml`, `setup.sh`, `.github/workflows/deploy-pages.yml`, and `dist/index.html`.
2. **Present Deliverables**:
   - Call `google:show_file` on the interactive HTML WebGIS app, the standalone `ANTIGRAVITY_MASTER_PROMPT.md`, and the packaged `.zip` archive.

## Gotchas

- **Never rely on regional averages alone**: Coarse 5-region or city-wide averages hide 15-30% microclimate differences caused by coastal boundary-layer flushing, vegetative scavenging, and urban heat-island nocturnal inversions.
- **Always separate directional wind regimes**: A subzone that is a top sanctuary during Southwest Monsoon plumes can be moderately exposed during Southeast plumes unless it sits along a sheltered lee channel with active sea-breeze flushing.
- **Keep the WebGIS 100% client-side**: GitHub Pages does not run Python/Node backends; always pre-compute and embed the spatial crosswalk and episode matrix inside the HTML bundle while providing the Python/MCP pipeline inside the ZIP kit for live refreshes.
