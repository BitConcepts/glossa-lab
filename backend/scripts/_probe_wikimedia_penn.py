"""Probe Wikimedia Commons for Penn Museum Indus seal images.

Penn Museum has contributed images to Wikimedia Commons under CC BY 4.0.
Strategy:
  1. Search Commons category: Category:Objects_from_the_Penn_Museum
  2. Search by Penn Museum accession numbers from indus_research.jsonl
  3. Verify image URLs are directly downloadable
"""
import json, urllib.request, urllib.error, time
from pathlib import Path

UA = "GlossaLab/1.0 (Indus research; tpierson@bitconcepts.tech)"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
ROOT = Path(__file__).parents[2]

def wmc_api(**params):
    params.setdefault("format", "json")
    url = COMMONS_API + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  API error: {e}")
        return {}

print("=" * 60)
print("PROBE 1: Wikimedia Commons — Penn Museum categories")
print("=" * 60)
# Try to list members of Penn Museum-related categories
for cat in [
    "Objects_from_the_Penn_Museum",
    "Penn_Museum_collections",
    "Images_from_the_Penn_Museum",
    "Indus_Valley_seals_in_the_Penn_Museum",
    "Indus_Valley_Civilization_artifacts_in_the_United_States",
    "Indus_script_seals",
    "Harappan_seals",
]:
    data = wmc_api(
        action="query",
        list="categorymembers",
        cmtitle=f"Category:{cat}",
        cmtype="file",
        cmlimit="10",
        cmnamespace="6",
    )
    members = data.get("query", {}).get("categorymembers", [])
    print(f"\n  Category:{cat}")
    print(f"    Members (files): {len(members)}")
    for m in members[:5]:
        print(f"      {m['title']}")
    time.sleep(0.3)

print()
print("=" * 60)
print("PROBE 2: Search Commons for Indus seals (various queries)")
print("=" * 60)
queries = [
    "Indus Valley seal Penn Museum",
    "Harappan seal Philadelphia",
    "steatite seal Mohenjo-daro Penn",
    "indus script stamp seal United States",
]
for q in queries:
    data = wmc_api(
        action="query",
        list="search",
        srsearch=q.replace(" ", "+"),
        srnamespace="6",
        srlimit="5",
    )
    hits = data.get("query", {}).get("search", [])
    print(f"\n  Query: '{q}'")
    for h in hits:
        print(f"    {h['title']}")
    time.sleep(0.3)

print()
print("=" * 60)
print("PROBE 3: Sample Penn accession numbers → Commons search")
print("=" * 60)
# Load some Penn accession numbers from indus_research.jsonl
jl = ROOT / "glossa-corpus" / "indus" / "exports" / "indus_research.jsonl"
accs = []
with open(jl, encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        if obj.get("source_system") == "PennMuseum" and obj.get("accession_number"):
            accs.append(obj["accession_number"])
        if len(accs) >= 10:
            break

print(f"  Sample accession numbers: {accs}")
for acc in accs[:5]:
    data = wmc_api(
        action="query",
        list="search",
        srsearch=acc.replace(" ", "+"),
        srnamespace="6",
        srlimit="3",
    )
    hits = data.get("query", {}).get("search", [])
    if hits:
        print(f"  {acc}: {[h['title'] for h in hits]}")
    else:
        print(f"  {acc}: no results")
    time.sleep(0.3)

print()
print("=" * 60)
print("PROBE 4: Direct Wikimedia Commons image URL test")
print("=" * 60)
# If any file is found, get its actual image URL
test_file = "Indus_script_stamp_seal.jpg"  # known file if it exists
data = wmc_api(
    action="query",
    titles=f"File:{test_file}",
    prop="imageinfo",
    iiprop="url|size|mime",
)
pages = data.get("query", {}).get("pages", {})
for pid, page in pages.items():
    ii = page.get("imageinfo", [])
    if ii:
        print(f"  {test_file}: {ii[0].get('url')}")
    else:
        print(f"  {test_file}: not found or no imageinfo")
