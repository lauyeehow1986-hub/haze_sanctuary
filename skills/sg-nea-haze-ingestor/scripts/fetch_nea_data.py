#!/usr/bin/env python3
"""Fetches NEA PSI, PM2.5, and Wind telemetry from data.gov.sg v2 API."""
import urllib.request
import json

ENDPOINTS = {
    "psi": "https://api-open.data.gov.sg/v2/real-time/api/psi",
    "pm25": "https://api-open.data.gov.sg/v2/real-time/api/pm25",
    "wind_dir": "https://api-open.data.gov.sg/v2/real-time/api/wind-direction",
    "wind_speed": "https://api-open.data.gov.sg/v2/real-time/api/wind-speed",
}

def fetch_endpoint(name, date_str=None):
    url = ENDPOINTS[name] + (f"?date={date_str}" if date_str else "")
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "SG-Haze-Sanctuary/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

if __name__ == "__main__":
    print("Configured NEA v2 endpoints:", list(ENDPOINTS.keys()))
