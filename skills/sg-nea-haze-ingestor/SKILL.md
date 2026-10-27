---
name: sg-nea-haze-ingestor
description: Ingest, clean, and backfill Singapore NEA 24-hr PSI, 3-hr PSI, 1-hr PM2.5, wind speed, wind direction, rainfall, and relative humidity from data.gov.sg APIs and archival 1997-2026 haze records. Use when fetching Singapore air quality or meteorological time-series.
---
# Singapore NEA Haze & Meteorological Ingestor

Fetch, paginate, and harmonize hourly and daily air quality and weather telemetry from Singapore's National Environment Agency (NEA) and Meteorological Service Singapore (MSS).

## When to Use

- Pulling real-time or historical `psi`, `pm25`, `wind-direction`, `wind-speed`, `rainfall`, or `relative-humidity` from `data.gov.sg` v2 APIs
- Harmonizing pre-2014 24-hr/3-hr PSI records (where PM2.5 was folded into 24-hr PSI on 1 April 2014) with post-2014 1-hr PM2.5 bands

## Steps

1. **Query Live & Historical NEA Endpoints**:
   - Real-time 24-hr PSI & sub-indices: `GET https://api-open.data.gov.sg/v2/real-time/api/psi?date=YYYY-MM-DD`
   - Real-time 1-hr PM2.5: `GET https://api-open.data.gov.sg/v2/real-time/api/pm25?date=YYYY-MM-DD`
   - Historical PSI Collection: Query `data.gov.sg` Collection ID `2215` (`d_b4cf557f8750260d229c49fd768e11ed`).
2. **Normalize the 2014 PSI Formula Shift**:
   - Prior to 1 April 2014, NEA's 24-hr PSI was based on 5 pollutants ($	ext{PM}_{10}, 	ext{SO}_2, 	ext{CO}, 	ext{O}_3, 	ext{NO}_2$). On 1 April 2014, 24-hr $	ext{PM}_{2.5}$ was added as the 6th pollutant.
   - For 1997 and 2013 episodes, convert archival $	ext{PM}_{10}$ and visibility extinction (Changi/Paya Lebar METAR `HZ`/`FU` synoptics) using the validated NEA smoke-aerosol ratio $	ext{PM}_{2.5} / 	ext{PM}_{10} pprox 0.78$ during biomass burning episodes.
3. **Export Clean Parquet/JSON**:
   - Output standardized UTC+8 (`Asia/Singapore`) hourly frames with columns: `timestamp_sgt`, `region`, `psi_24hr`, `pm25_1hr`, `wind_dir_deg`, `wind_speed_kts`, `rainfall_mm`, `rh_pct`.

## Gotchas

- Always pass `X-Api-Key` header if querying `api-open.data.gov.sg` at high concurrency to avoid HTTP 429 rate limits.
