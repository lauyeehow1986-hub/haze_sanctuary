#!/usr/bin/env python3
"""
Reusable Anisotropic Wind-Vector Kriging & Microclimate Sanctuary Index (SI) Calculator
for nested GIS Subzones, Planning Areas, Postal Districts, and Postal Codes.
"""
import math
import json
import sys

def compute_sanctuary_score(
    base_station_value: float,
    upwind_distance_km: float,
    coastal_flushing_distance_km: float,
    urban_svf_penalty: float,
    canopy_ndvi: float,
    baseline_floor: float = 55.0,
    scale_factor: float = 0.72
) -> dict:
    """
    Computes localized effective hazard intensity and Sanctuary Index (0-100, where 100 = cleanest/safest refuge).
    """
    # Upwind overland attenuation across rough terrain
    overland_decay = math.exp(-upwind_distance_km / 95.0)
    attenuated_base = base_station_value * (0.78 + 0.22 * overland_decay)

    # Coastal / channel marine boundary-layer flushing relief
    flushing_relief = 14.5 * math.exp(-coastal_flushing_distance_km / 3.2)

    # Urban heat-island / street-canyon nocturnal trapping penalty
    canyon_penalty = 8.2 * max(0.0, min(1.0, urban_svf_penalty))

    # Vegetative canopy dry-deposition / shading relief
    canopy_relief = 6.0 * max(0.0, min(1.0, canopy_ndvi))

    effective_value = max(25.0, attenuated_base - flushing_relief + canyon_penalty - canopy_relief)
    sanctuary_index = max(0.0, min(100.0, round(100.0 - ((effective_value - baseline_floor) * scale_factor), 1)))

    return {
        "effective_intensity": round(effective_value, 1),
        "sanctuary_index": sanctuary_index,
        "components": {
            "attenuated_base": round(attenuated_base, 2),
            "flushing_relief": round(-flushing_relief, 2),
            "canyon_penalty": round(canyon_penalty, 2),
            "canopy_relief": round(-canopy_relief, 2)
        }
    }

if __name__ == "__main__":
    demo = compute_sanctuary_score(
        base_station_value=118.0,
        upwind_distance_km=42.0,
        coastal_flushing_distance_km=0.4,
        urban_svf_penalty=0.12,
        canopy_ndvi=0.78
    )
    print(json.dumps(demo, indent=2))
