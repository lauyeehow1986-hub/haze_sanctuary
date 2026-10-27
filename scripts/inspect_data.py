import re

with open("dist/index.html", "r", encoding="utf-8") as f:
    text = f.read()

subzones_match = re.search(r"const SUBZONES_DATA = \[(.*?)\];\s*const", text, re.DOTALL)
if subzones_match:
    block = subzones_match.group(1)
    ids = re.findall(r'id:\s*"([^"]+)"', block)
    names = re.findall(r'subzone:\s*"([^"]+)"', block)
    ranks = re.findall(r'rank:\s*(\d+)', block)
    districts = re.findall(r'district:\s*"([^"]+)"', block)
    hsis = re.findall(r'hsi:\s*([\d\.]+)', block)
    for r, i, n, d, h in zip(ranks, ids, names, districts, hsis):
        print(f"Rank {r}: {n} (ID: {i}, District: {d}, HSI: {h})")
