#!/usr/bin/env python3
"""
Comprehensive Automated Verification Test for Singapore Haze Sanctuary WebGIS
==============================================================================
Verifies:
1. All 82 postal sectors (01 through 82) are represented across SUBZONES_DATA in index.html & dist/index.html.
2. 2-digit queries ("01" - "82") resolve strictly without false positives.
3. Key 6-digit postal codes resolve accurately.
4. Arbitrary 6-digit postal codes for all 82 sectors (e.g. XX1234) resolve via prefix matching.
5. Text searches (subzone name, planning area, district) resolve properly.
6. GeoJSON dataset rankings and metrics reflect multi-episode composite HSI.
7. Generated PNG charts and hero banners exist with non-zero size in both dist/assets and assets.
"""

import os
import re
import json
import pytest

import subprocess

def extract_subzones_data_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"const SUBZONES_DATA = (\[.*?\]);\s*\n\s*let selectedSubzoneId", content, re.DOTALL)
    assert match is not None, f"Could not find SUBZONES_DATA in {html_path}"
    raw_js = match.group(1)

    node_cmd = ["node", "-e", "eval('var data = ' + process.argv[1]); console.log(JSON.stringify(data));", raw_js]
    output = subprocess.check_output(node_cmd, encoding="utf-8")
    return json.loads(output)

def simulate_handle_search(subzones_data, query):
    q = query.strip().lower()
    if not q:
        return None

    match = None
    if re.match(r"^\d{2}$", q):
        # 2-digit sector query
        for item in subzones_data:
            sectors = [s.strip() for s in item["sectors"].split(",")]
            if q in sectors:
                match = item
                break
    elif re.match(r"^\d{6}$", q):
        # Priority 1: exact postal code match across all subzones
        for item in subzones_data:
            if q in item["postalCodes"]:
                match = item
                break
        # Priority 2: 2-digit sector prefix match
        if not match:
            prefix = q[:2]
            for item in subzones_data:
                sectors = [s.strip() for s in item["sectors"].split(",")]
                if prefix in sectors:
                    match = item
                    break
    else:
        # Match normalized postal district queries (e.g. "d1", "d01", "district 1", "district 01", "d17")
        dist_match = re.match(r"^(?:d|district\s*)(\d{1,2})$", q, re.I)
        if dist_match:
            target_dist = f"D{int(dist_match.group(1)):02d}"
            for item in subzones_data:
                districts = [d.strip().upper() for d in item["district"].split("/")]
                if target_dist in districts:
                    match = item
                    break
        if not match:
            for item in subzones_data:
                if (q in item["subzone"].lower() or
                    q in item["planningArea"].lower() or
                    q in item["district"].lower() or
                    (item.get("refugeSpot") and q in item["refugeSpot"].lower())):
                    match = item
                    break

    if not match:
        match = subzones_data[1] # fallback to Changi Point
    return match

# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_all_82_sectors_represented(html_file):
    """Ensure all 82 postal sectors (01-82) are present in SUBZONES_DATA."""
    subzones = extract_subzones_data_from_html(html_file)
    all_sectors = set()
    for item in subzones:
        sectors = [s.strip() for s in item["sectors"].split(",")]
        for s in sectors:
            assert re.match(r"^\d{2}$", s), f"Invalid sector format: '{s}' in {item['id']}"
            all_sectors.add(s)

    expected_sectors = {f"{i:02d}" for i in range(1, 83)}
    missing = expected_sectors - all_sectors
    assert not missing, f"Missing sectors in {html_file}: {sorted(missing)}"
    assert len(all_sectors) >= 82, f"Total sectors count {len(all_sectors)} < 82"

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_all_82_sectors_search_resolution(html_file):
    """Ensure each 2-digit query from 01 to 82 resolves strictly to a subzone that owns it."""
    subzones = extract_subzones_data_from_html(html_file)
    for sec_int in range(1, 83):
        sec = f"{sec_int:02d}"
        result = simulate_handle_search(subzones, sec)
        assert result is not None, f"Sector {sec} failed to resolve"
        sectors = [s.strip() for s in result["sectors"].split(",")]
        assert sec in sectors, f"Sector {sec} resolved to {result['id']} which only has sectors: {sectors}"

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_key_6_digit_postal_codes(html_file):
    """Ensure known landmark 6-digit postal codes resolve accurately."""
    subzones = extract_subzones_data_from_html(html_file)
    test_cases = [
        ("498991", "changi_point"),
        ("508329", "pulau_ubin"),
        ("519914", "loyang_pasir_ris"),
        ("829325", "coney_punggol"),
        ("759819", "sembawang_straits"),
        ("787130", "springleaf_mandai"),
        ("718925", "kranji_lim_chu_kang"),
        ("529653", "tampines_bedok"),
        ("534013", "serangoon_hougang"),
        ("449876", "marine_parade_east_coast"),
        ("018989", "central_cbd_orchard"),
        ("238801", "central_cbd_orchard"),
        ("098585", "harbourfront_sentosa_south"),
        ("608532", "jurong_east_bukit_batok"),
        ("639940", "tuas_pioneer_jurong_island")
    ]
    for code, expected_id in test_cases:
        res = simulate_handle_search(subzones, code)
        assert res["id"] == expected_id, f"Postal code {code} resolved to {res['id']}, expected {expected_id}"

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_all_82_sectors_with_arbitrary_postal_codes(html_file):
    """Ensure arbitrary 6-digit postal codes with prefix 01-82 resolve via prefix matching."""
    subzones = extract_subzones_data_from_html(html_file)
    for sec_int in range(1, 83):
        postal_code = f"{sec_int:02d}1234"
        res = simulate_handle_search(subzones, postal_code)
        sectors = [s.strip() for s in res["sectors"].split(",")]
        assert f"{sec_int:02d}" in sectors, f"Postal code {postal_code} resolved to {res['id']} without sector {sec_int:02d}"

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_text_queries(html_file):
    """Ensure subzone, planning area, and district text searches work."""
    subzones = extract_subzones_data_from_html(html_file)
    test_queries = [
        ("Changi", "changi_point"),
        ("Ubin", "pulau_ubin"),
        ("Pasir Ris", "loyang_pasir_ris"),
        ("Coney Island", "coney_punggol"),
        ("Sembawang", "sembawang_straits"),
        ("Springleaf", "springleaf_mandai"),
        ("Kranji", "kranji_lim_chu_kang"),
        ("Tampines", "tampines_bedok"),
        ("Serangoon", "serangoon_hougang"),
        ("Marine Parade", "marine_parade_east_coast"),
        ("Downtown Core", "central_cbd_orchard"),
        ("Sentosa", "harbourfront_sentosa_south"),
        ("Jurong East", "jurong_east_bukit_batok"),
        ("Tuas", "tuas_pioneer_jurong_island"),
        ("d17", "pulau_ubin") # D17 matches Pulau Ubin first
    ]
    for q, expected_id in test_queries:
        res = simulate_handle_search(subzones, q)
        assert res["id"] == expected_id, f"Query '{q}' resolved to {res['id']}, expected {expected_id}"

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_exact_all_postal_codes_including_shared_sectors(html_file):
    """Ensure EVERY listed postal code across all 14 subzones resolves to its exact owner,
    verifying specifically that shared sector prefixes (e.g. 508783 in loyang_pasir_ris)
    are not shadowed by earlier subzones (pulau_ubin)."""
    subzones = extract_subzones_data_from_html(html_file)
    for item in subzones:
        for code in item["postalCodes"]:
            res = simulate_handle_search(subzones, code)
            assert res is not None, f"Postal code {code} returned None"
            assert res["id"] == item["id"], (
                f"Postal code {code} in {html_file} resolved to {res['id']}, expected {item['id']}"
            )

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_normalized_district_queries(html_file):
    """Ensure district queries format (d1, d01, district 1, district 01, etc.) resolve accurately."""
    subzones = extract_subzones_data_from_html(html_file)
    district_test_map = {
        1: "central_cbd_orchard",
        2: "central_cbd_orchard",
        3: "harbourfront_sentosa_south",
        4: "harbourfront_sentosa_south",
        5: "jurong_east_bukit_batok",
        6: "central_cbd_orchard",
        7: "central_cbd_orchard",
        8: "central_cbd_orchard",
        9: "central_cbd_orchard",
        10: "central_cbd_orchard",
        11: "central_cbd_orchard",
        15: "marine_parade_east_coast",
        16: "tampines_bedok",
        17: "pulau_ubin",
        18: "loyang_pasir_ris",
        19: "coney_punggol",
        21: "jurong_east_bukit_batok",
        22: "jurong_east_bukit_batok",
        23: "jurong_east_bukit_batok",
        24: "kranji_lim_chu_kang",
        25: "kranji_lim_chu_kang",
        26: "springleaf_mandai",
        27: "sembawang_straits",
        28: "serangoon_hougang"
    }
    for d_num, exp_id in district_test_map.items():
        variants = [f"d{d_num}", f"d{d_num:02d}", f"district {d_num}", f"district {d_num:02d}"]
        for q in variants:
            res = simulate_handle_search(subzones, q)
            assert res["id"] == exp_id, f"District query '{q}' in {html_file} resolved to {res['id']}, expected {exp_id}"

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_landmark_refuge_queries(html_file):
    """Ensure prominent landmark names resolve to their enclosing subzone sanctuary."""
    subzones = extract_subzones_data_from_html(html_file)
    landmark_cases = [
        ("Chek Jawa", "pulau_ubin"),
        ("Changi Beach", "changi_point"),
        ("Pasir Ris Park", "loyang_pasir_ris"),
        ("Coney Island Park", "coney_punggol"),
        ("Sembawang Park", "sembawang_straits"),
        ("Springleaf Nature Park", "springleaf_mandai"),
        ("Sungei Buloh", "kranji_lim_chu_kang"),
        ("Our Tampines Hub", "tampines_bedok"),
        ("NEX", "serangoon_hougang"),
        ("Parkway Parade", "marine_parade_east_coast"),
        ("Marina Bay Sands", "central_cbd_orchard"),
        ("VivoCity", "harbourfront_sentosa_south"),
        ("Westgate", "jurong_east_bukit_batok"),
        ("Boon Lay", "tuas_pioneer_jurong_island")
    ]
    for lm, exp_id in landmark_cases:
        res = simulate_handle_search(subzones, lm)
        assert res["id"] == exp_id, f"Landmark query '{lm}' in {html_file} resolved to {res['id']}, expected {exp_id}"

def test_geojson_rankings_and_composite_hsi():
    """Ensure GeoJSON features have composite HSI and are sorted descending by HSI."""
    geojson_path = "data/processed/sg_subzone_haze_1997_2026.geojson"
    assert os.path.exists(geojson_path), "GeoJSON file does not exist"
    with open(geojson_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    features = data["features"]
    assert len(features) >= 14, f"Expected at least 14 subzone features, found {len(features)}"

    # Check rank order and HSI descending
    previous_hsi = 101.0
    for idx, feat in enumerate(features, start=1):
        props = feat["properties"]
        hsi = props["haze_sanctuary_index"]
        rank = props["sanctuary_rank"]
        assert rank == idx, f"Feature {props['subzone']} has rank {rank}, expected {idx}"
        assert hsi <= previous_hsi, f"Feature {props['subzone']} has HSI {hsi} > previous {previous_hsi}"
        assert props["unhealthy_hours_since_1997"] > 0
        assert props["effective_psi_baseline"] > 0
        assert "episodes" in props
        assert len(props["episodes"]) == 6
        previous_hsi = hsi

def test_static_infographic_and_hero_banner_assets():
    """Ensure all required static PNG charts and banners exist and are non-empty in both locations."""
    required_charts = [
        "sg_haze_sanctuary_ranking_atlas.png",
        "sg_haze_diurnal_microclimate_atlas.png",
        "sg_postal_district_hsi_heatmap.png",
        "sg_haze_synoptic_wind_plumes.png",
        "linkedin_hero_banner.png"
    ]
    for c in required_charts:
        dist_path = os.path.join("dist", "assets", c)
        root_path = os.path.join("assets", c)
        assert os.path.exists(dist_path), f"Missing in dist/assets: {dist_path}"
        assert os.path.exists(root_path), f"Missing in assets: {root_path}"
        assert os.path.getsize(dist_path) > 10000, f"File {dist_path} too small: {os.path.getsize(dist_path)} bytes"
        assert os.path.getsize(root_path) > 10000, f"File {root_path} too small: {os.path.getsize(root_path)} bytes"

@pytest.mark.parametrize("html_file", ["index.html", "dist/index.html"])
def test_native_javascript_engine_execution(html_file):
    """Verify that the raw JavaScript handleSearch() function embedded in the HTML file
    executes inside Node.js without errors and produces correct results for all query archetypes."""
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    m_data = re.search(r"const SUBZONES_DATA = (\[.*?\]);\s*\n\s*let selectedSubzoneId", html, re.DOTALL)
    m_func = re.search(r"function handleSearch\(\) \{(.*?)\n    \}", html, re.DOTALL)
    assert m_data is not None and m_func is not None

    def execute_js_search(query):
        js_code = f"""
        const SUBZONES_DATA = {m_data.group(1)};
        let selectedSubzoneId = null;
        let feedbackTextContent = '';
        const document = {{
            getElementById: function(id) {{
                if (id === 'postalSearchInput') return {{ value: {json.dumps(query)} }};
                if (id === 'searchFeedback') return {{ classList: {{ remove: function() {{}} }} }};
                if (id === 'searchFeedbackText') return {{ set textContent(val) {{ feedbackTextContent = val; }} }};
                return {{}};
            }}
        }};
        function renderMap() {{}}
        function updateInspector() {{}}
        function handleSearch() {{{m_func.group(1)}}}
        handleSearch();
        console.log(JSON.stringify({{ selectedSubzoneId, feedbackTextContent }}));
        """
        output = subprocess.check_output(["node", "-e", js_code], encoding="utf-8")
        return json.loads(output)

    # 1. Exact postal code including previously shadowed code 508783
    res_loyang = execute_js_search("508783")
    assert res_loyang["selectedSubzoneId"] == "loyang_pasir_ris", f"JS engine failed on 508783: {res_loyang}"

    # 2. Strict 2-digit sector query
    res_sec_01 = execute_js_search("01")
    assert res_sec_01["selectedSubzoneId"] == "central_cbd_orchard", f"JS engine failed on 01: {res_sec_01}"

    # 3. Arbitrary 6-digit prefix query
    res_pref = execute_js_search("751234")
    assert res_pref["selectedSubzoneId"] == "sembawang_straits", f"JS engine failed on 751234: {res_pref}"

    # 4. Normalized district queries
    res_d1 = execute_js_search("d1")
    assert res_d1["selectedSubzoneId"] == "central_cbd_orchard", f"JS engine failed on d1: {res_d1}"
    res_dist5 = execute_js_search("district 5")
    assert res_dist5["selectedSubzoneId"] == "jurong_east_bukit_batok", f"JS engine failed on district 5: {res_dist5}"

    # 5. Landmark query
    res_mbs = execute_js_search("Marina Bay Sands")
    assert res_mbs["selectedSubzoneId"] == "central_cbd_orchard", f"JS engine failed on MBS: {res_mbs}"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
