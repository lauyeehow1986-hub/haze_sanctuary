#!/usr/bin/env python3
"""
Canonical Singapore 2-Digit Postal Sector to Postal District (D01-D28) & URA Planning Area Lookup.
Covers all 28 Postal Districts (D01–D28) and all 82 Postal Sectors (01–82).
"""

POSTAL_DISTRICTS = {
    "D01": {"sectors": ["01", "02", "03", "04", "05", "06"], "areas": "Raffles Place, Cecil, Marina, People's Park", "region": "Central"},
    "D02": {"sectors": ["07", "08"], "areas": "Anson, Tanjong Pagar", "region": "Central"},
    "D03": {"sectors": ["14", "15", "16"], "areas": "Queenstown, Tiong Bahru, Alexandra", "region": "Central"},
    "D04": {"sectors": ["09", "10"], "areas": "Telok Blangah, Harbourfront, Sentosa", "region": "South"},
    "D05": {"sectors": ["11", "12", "13"], "areas": "Pasir Panjang, Hong Leong Garden, Clementi New Town", "region": "West"},
    "D06": {"sectors": ["17"], "areas": "City Hall, High Street, Beach Road", "region": "Central"},
    "D07": {"sectors": ["18", "19"], "areas": "Middle Road, Golden Mile, Bugis", "region": "Central"},
    "D08": {"sectors": ["20", "21"], "areas": "Little India, Farrer Park, Serangoon Road", "region": "Central"},
    "D09": {"sectors": ["22", "23"], "areas": "Orchard, Cairnhill, River Valley", "region": "Central"},
    "D10": {"sectors": ["24", "25", "26", "27"], "areas": "Ardmore, Bukit Timah, Holland Road, Tanglin", "region": "Central"},
    "D11": {"sectors": ["28", "29", "30"], "areas": "Watten Estate, Novena, Thomson", "region": "Central"},
    "D12": {"sectors": ["31", "32", "33"], "areas": "Balestier, Toa Payoh, Serangoon", "region": "Central"},
    "D13": {"sectors": ["34", "35", "36", "37"], "areas": "Macpherson, Braddell", "region": "Central"},
    "D14": {"sectors": ["38", "39", "40", "41"], "areas": "Geylang, Eunos, Paya Lebar", "region": "East"},
    "D15": {"sectors": ["42", "43", "44", "45"], "areas": "Katong, Joo Chiat, Amber Road, Marine Parade, East Coast", "region": "East"},
    "D16": {"sectors": ["46", "47", "48"], "areas": "Bedok, Upper East Coast, Eastwood, Kew Drive", "region": "East"},
    "D17": {"sectors": ["49", "50", "81"], "areas": "Loyang, Changi, Changi Point, Pulau Ubin", "region": "East (Sanctuary Core)"},
    "D18": {"sectors": ["51", "52"], "areas": "Tampines, Pasir Ris", "region": "East (Sanctuary Core)"},
    "D19": {"sectors": ["53", "54", "55", "82"], "areas": "Serangoon Garden, Hougang, Punggol, Sengkang, Coney Island", "region": "North-East (Sanctuary Core)"},
    "D20": {"sectors": ["56", "57"], "areas": "Bishan, Ang Mo Kio", "region": "North-East"},
    "D21": {"sectors": ["58", "59"], "areas": "Upper Bukit Timah, Ulu Pandan, Clementi Park", "region": "West"},
    "D22": {"sectors": ["60", "61", "62", "63", "64"], "areas": "Jurong, Tuas, Boon Lay, Pioneer", "region": "West (Acute Hazard Corridor)"},
    "D23": {"sectors": ["65", "66", "67", "68"], "areas": "Hillview, Dairy Farm, Bukit Panjang, Choa Chu Kang", "region": "West"},
    "D24": {"sectors": ["69", "70", "71"], "areas": "Lim Chu Kang, Tengah", "region": "West/North"},
    "D25": {"sectors": ["72", "73"], "areas": "Kranji, Woodgrove, Woodlands", "region": "North"},
    "D26": {"sectors": ["77", "78"], "areas": "Upper Thomson, Springleaf, Mandai", "region": "North (Sanctuary Core)"},
    "D27": {"sectors": ["75", "76"], "areas": "Yishun, Sembawang, Sembawang Straits", "region": "North (Sanctuary Core)"},
    "D28": {"sectors": ["79", "80"], "areas": "Seletar, Yio Chu Kang", "region": "North-East"}
}

# Reverse lookup table for O(1) resolution
SECTOR_TO_DISTRICT = {
    sec: dist for dist, info in POSTAL_DISTRICTS.items() for sec in info["sectors"]
}

def lookup_postal_code(postal_code: str) -> dict:
    clean_code = str(postal_code).strip()
    sector = clean_code[:2] if len(clean_code) >= 2 else clean_code.zfill(2)
    dist = SECTOR_TO_DISTRICT.get(sector)
    if dist:
        info = POSTAL_DISTRICTS[dist]
        return {
            "postal_code": clean_code,
            "sector": sector,
            "district": dist,
            "areas": info["areas"],
            "region": info["region"],
            "matched": True
        }
    return {
        "postal_code": clean_code,
        "sector": sector,
        "district": "Unknown",
        "areas": "Unknown",
        "region": "Unknown",
        "matched": False
    }

if __name__ == "__main__":
    test_codes = ["498991", "508329", "018989", "608532", "639841", "787130", "556083", "759819"]
    for tc in test_codes:
        print(lookup_postal_code(tc))
