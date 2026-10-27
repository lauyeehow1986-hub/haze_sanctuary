#!/usr/bin/env python3
"""Canonical Singapore 2-Digit Postal Sector to Postal District (D01-D28) & URA Planning Area Lookup."""

POSTAL_DISTRICTS = {
    "D01": {"sectors": ["01", "02", "03", "04", "05", "06"], "areas": "Raffles Place, Cecil, Marina, People's Park", "region": "Central"},
    "D02": {"sectors": ["07", "08"], "areas": "Anson, Tanjong Pagar", "region": "Central"},
    "D03": {"sectors": ["14", "15", "16"], "areas": "Queenstown, Tiong Bahru, Alexandra", "region": "Central/South"},
    "D04": {"sectors": ["09", "10"], "areas": "Telok Blangah, Harbourfront, Sentosa", "region": "South"},
    "D05": {"sectors": ["11", "12", "13"], "areas": "Pasir Panjang, Hong Leong Garden, Clementi New Town", "region": "West/South"},
    "D15": {"sectors": ["42", "43", "44", "45"], "areas": "Katong, Joo Chiat, Amber Road, Marine Parade, East Coast", "region": "East"},
    "D16": {"sectors": ["46", "47", "48"], "areas": "Bedok, Upper East Coast, Eastwood, Kew Drive", "region": "East"},
    "D17": {"sectors": ["49", "50", "81"], "areas": "Loyang, Changi, Changi Point, Pulau Ubin", "region": "East (Sanctuary Core)"},
    "D18": {"sectors": ["51", "52"], "areas": "Tampines, Pasir Ris", "region": "East (Sanctuary Core)"},
    "D19": {"sectors": ["53", "54", "55", "82"], "areas": "Serangoon Garden, Hougang, Punggol, Sengkang, Coney Island", "region": "North-East"},
    "D22": {"sectors": ["60", "61", "62", "63", "64"], "areas": "Jurong, Tuas, Boon Lay, Pioneer", "region": "West"},
    "D25": {"sectors": ["72", "73"], "areas": "Kranji, Woodgrove, Woodlands", "region": "North"},
    "D26": {"sectors": ["77", "78"], "areas": "Upper Thomson, Springleaf, Mandai", "region": "North/Central"},
    "D27": {"sectors": ["75", "76"], "areas": "Yishun, Sembawang, Sembawang Straits", "region": "North"},
    "D28": {"sectors": ["79", "80"], "areas": "Seletar, Yio Chu Kang", "region": "North-East"},
}

def lookup_postal_code(postal_code: str):
    sector = str(postal_code).strip()[:2]
    for dist, info in POSTAL_DISTRICTS.items():
        if sector in info["sectors"]:
            return {"postal_code": postal_code, "sector": sector, "district": dist, **info}
    return {"postal_code": postal_code, "sector": sector, "district": "Other"}

if __name__ == "__main__":
    print(lookup_postal_code("498991"))
