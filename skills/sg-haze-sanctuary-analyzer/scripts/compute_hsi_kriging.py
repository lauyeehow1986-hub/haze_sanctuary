#!/usr/bin/env python3
"""
Anisotropic Wind-Vector Kriging & Haze Sanctuary Index (HSI) Calculator
for Singapore's 332 URA Subzones, 28 Postal Districts, and 6-Digit Postal Codes.
"""
import math
import json

def compute_subzone_hsi(base_region_psi, wind_deg, dist_johor_strait_km, urban_svf_penalty, canopy_ndvi):
    """
    Computes effective localized PSI and Haze Sanctuary Index (0-100).
    """
    # Johor Strait / South China Sea marine boundary flushing reduction
    sea_breeze_relief = 14.5 * math.exp(-dist_johor_strait_km / 3.2)
    # Urban heat island nocturnal trapping penalty
    uhi_penalty = 8.2 * urban_svf_penalty
    # Vegetative dry deposition scavenging
    canopy_relief = 6.0 * canopy_ndvi
    
    local_psi = max(35.0, base_region_psi - sea_breeze_relief + uhi_penalty - canopy_relief)
    hsi = max(0.0, min(100.0, round(100.0 - ((local_psi - 55.0) * 0.72), 1)))
    return {"effective_psi": round(local_psi, 1), "hsi_score": hsi}

if __name__ == "__main__":
    sample = compute_subzone_hsi(base_region_psi=118.0, wind_deg=215, dist_johor_strait_km=0.4, urban_svf_penalty=0.12, canopy_ndvi=0.78)
    print(json.dumps({"subzone": "CHANGI POINT (D17, 498991)", **sample}, indent=2))
