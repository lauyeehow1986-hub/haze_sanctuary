#!/usr/bin/env python3
"""
Directional Atmospheric Dispersion & Multi-Layer Geospatial Sanctuary Index (SI) Scorer
for nested GIS administrative boundaries (Regions, Planning Areas, Subzones, Postal Districts, and Postal Codes).
Fuses regional telemetry nodes, directional wind vectors, marine boundary flushing, urban SVF, and vegetative canopy.
"""
import math
import json
import sys

def compute_sanctuary_score(
    base_station_value: float,
    wind_deg: float = 215.0,
    upwind_distance_km: float = 40.0,
    coastal_flushing_distance_km: float = 0.5,
    urban_svf_penalty: float = 0.1,
    canopy_ndvi: float = 0.75,
    sea_flush_factor: float = 0.95,
    baseline_floor: float = 40.0,
    scale_factor: float = 0.42
) -> dict:
    """
    Computes localized effective hazard intensity and Sanctuary Index (0-100, where 100 = cleanest/safest refuge).

    Mathematical Formulation:
      C_s = max(30.0, C_base + Advection(theta, d_upwind) - SeaFlush(d_coast) + UHI(SVF) - Canopy(NDVI))
      SI_s = max(0.0, min(100.0, 100.0 - (C_s - baseline_floor) * scale_factor))
    """
    theta = wind_deg % 360.0

    # Directional upwind advection penalty (plume decay)
    if 195.0 <= theta <= 255.0:
        # Southwest corridor (e.g. Sumatra SW plumes)
        advection = 45.0 * math.exp(-upwind_distance_km / 14.0)
    elif 120.0 <= theta <= 195.0:
        # Southeast corridor (e.g. Kalimantan SE plumes)
        advection = 38.0 * math.exp(-upwind_distance_km / 12.0)
    else:
        advection = 15.0

    # Coastal / marine boundary-layer sea-breeze flushing relief
    flushing_relief = 28.5 * sea_flush_factor * math.exp(-coastal_flushing_distance_km / 3.8)

    # Urban heat-island / street-canyon nocturnal trapping penalty
    canyon_penalty = 16.5 * max(0.0, min(1.0, urban_svf_penalty))

    # Vegetative canopy dry-deposition / shading relief
    canopy_relief = 12.0 * max(0.0, min(1.0, canopy_ndvi))

    effective_value = max(30.0, base_station_value + advection - flushing_relief + canyon_penalty - canopy_relief)
    sanctuary_index = max(0.0, min(100.0, round(100.0 - ((effective_value - baseline_floor) * scale_factor), 1)))

    return {
        "effective_intensity": round(effective_value, 1),
        "sanctuary_index": sanctuary_index,
        "components": {
            "advection_impact": round(advection, 2),
            "flushing_relief": round(-flushing_relief, 2),
            "canyon_penalty": round(canyon_penalty, 2),
            "canopy_relief": round(-canopy_relief, 2)
        }
    }

if __name__ == "__main__":
    demo = compute_sanctuary_score(
        base_station_value=142.0,
        wind_deg=215.0,
        upwind_distance_km=40.5,
        coastal_flushing_distance_km=0.3,
        urban_svf_penalty=0.08,
        canopy_ndvi=0.76
    )
    print("Sample Sanctuary Evaluation (Changi Point Benchmark):")
    print(json.dumps(demo, indent=2))
