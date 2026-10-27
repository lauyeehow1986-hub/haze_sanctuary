#!/usr/bin/env python3
"""
FastMCP Server: mcp-sg-haze-nea
Exposes tools for querying Singapore NEA Real-Time & Historical PSI, 1-hr PM2.5,
MSS Wind Direction/Speed, Rainfall, Relative Humidity, and Historical 1997-2026 Episode Benchmarks.
"""
import json
import urllib.request
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-sg-haze-nea")

@mcp.tool()
def get_realtime_psi_and_pm25(date: str = "") -> str:
    """Fetch Singapore NEA 24-hr PSI and 1-hr PM2.5 across North, South, East, West, Central."""
    psi_url = "https://api-open.data.gov.sg/v2/real-time/api/psi" + (f"?date={date}" if date else "")
    pm25_url = "https://api-open.data.gov.sg/v2/real-time/api/pm25" + (f"?date={date}" if date else "")
    out = {}
    for key, url in [("psi", psi_url), ("pm25", pm25_url)]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MCP-SG-Haze/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                out[key] = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            out[key] = {"error": str(e)}
    return json.dumps(out, indent=2)

@mcp.tool()
def get_mss_wind_and_weather(date: str = "") -> str:
    """Fetch MSS wind direction, wind speed, rainfall, and relative humidity across Singapore stations."""
    endpoints = {
        "wind_direction": "https://api-open.data.gov.sg/v2/real-time/api/wind-direction",
        "wind_speed": "https://api-open.data.gov.sg/v2/real-time/api/wind-speed",
        "rainfall": "https://api-open.data.gov.sg/v2/real-time/api/rainfall",
        "relative_humidity": "https://api-open.data.gov.sg/v2/real-time/api/relative-humidity"
    }
    res = {}
    for k, base in endpoints.items():
        url = base + (f"?date={date}" if date else "")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MCP-SG-Haze/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                res[k] = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            res[k] = {"error": str(e)}
    return json.dumps(res, indent=2)

@mcp.tool()
def get_historical_haze_episodes_since_1997() -> str:
    """Return canonical summary of major unhealthy PSI episodes in Singapore since 18 Sep 1997."""
    episodes = [
        {"episode": "1997 El Nino Crisis", "first_unhealthy_date": "1997-09-18", "peak_psi": 226, "dominant_wind": "SE/SSE (Kalimantan & S. Sumatra)", "worst_region": "Central & South", "safest_subzone": "Pulau Ubin & Changi Point (D17)"},
        {"episode": "2013 Sumatra Riau Crisis", "first_unhealthy_date": "2013-06-17", "peak_psi_3hr": 401, "peak_psi_24hr": 246, "dominant_wind": "SW/WSW (Central Sumatra)", "worst_region": "West (Tuas/Jurong D22) & Central", "safest_subzone": "Changi Point, Loyang West & Pasir Ris (D17/D18)"},
        {"episode": "2015 Super El Nino Crisis", "first_unhealthy_date": "2015-09-10", "peak_psi_3hr": 471, "peak_psi_24hr": 341, "dominant_wind": "SE/S (South Sumatra & Kalimantan)", "worst_region": "South, Central & East Coast (D01/D04/D15)", "safest_subzone": "Pulau Ubin, Changi Point & Sembawang Straits (D17/D27)"},
        {"episode": "2019 Dry IOD Episode", "first_unhealthy_date": "2019-09-14", "peak_psi_24hr": 154, "dominant_wind": "SE/SSE", "worst_region": "South & Central", "safest_subzone": "Changi Point, Coney Island & Loyang (D17/D19)"},
        {"episode": "2023 October Episode", "first_unhealthy_date": "2023-10-07", "peak_psi_24hr": 123, "dominant_wind": "SE", "worst_region": "East Coast & Central", "safest_subzone": "Sembawang Straits, Kranji & Pulau Ubin (D27/D17)"},
        {"episode": "2026 Sep-Oct Prolonged Haze", "first_unhealthy_date": "2026-09-04", "peak_psi_24hr": 203, "dominant_wind": "Variable SW/SE Inter-Monsoon", "worst_region": "West (Oct 14-18) & Central (Sep 4-26)", "safest_subzone": "Pulau Ubin, Changi Point & Loyang West (D17)"}
    ]
    return json.dumps(episodes, indent=2)

if __name__ == "__main__":
    mcp.run()
