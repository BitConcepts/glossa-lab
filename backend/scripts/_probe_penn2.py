"""Probe: (1) Get Penn CSV headers, (2) Test Wikimedia Commons for Penn Museum images."""
import urllib.request, urllib.error, json, re

UA_BROWSER = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
UA_BOT = "GlossaLab/1.0 (Indus research; tpierson@bitconcepts.tech)"

print("=" * 60)
print("PROBE 1: Penn Museum CSV — first 2KB (column headers)")
print("=" * 60)
CSV_URL = "https://www.penn.museum/collections/assets/data/Penn_Museum_Collections_Data.csv"
try:
    req = urllib.request.Request(
        CSV_URL,
        headers={"User-Agent": UA_BROWSER, "Range": "bytes=0-2047"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        chunk = r.read(2048).decode("utf-8", errors="replace")
        # Extract header row (first line)
        header = chunk.split("\n")[0]
        cols = header.split(",")
        print(f"  HTTP status: {r.status}")
        print(f"  Columns ({len(cols)}):")
        for i, c in enumerate(cols):
            print(f"    [{i:2d}] {c.strip()}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}: {e.reason}")
except Exception as e:
    print(f"  Error: {e}")

print()
print("=" * 60)
print("PROBE 2: Wikimedia Commons API — Penn Museum Indus seals")
print("=" * 60)
# Sample Penn Museum accession numbers from known Indus objects
SAMPLE_ACCS = ["29-70-164", "29-70-165", "29-70-166", "CBS 14896"]  # typical Penn acc numbers

# Search Wikimedia Commons for Penn Museum Indus seals
wmc_url = (
    "https://commons.wikimedia.org/w/api.php"
    "?action=query&list=search"
    "&srsearch=Penn+Museum+Indus+seal+steatite"
    "&srnamespace=6"  # File namespace
    "&srlimit=10"
    "&format=json"
)
try:
    req = urllib.request.Request(wmc_url, headers={"User-Agent": UA_BOT})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    hits = data.get("query", {}).get("search", [])
    print(f"  Commons search hits: {len(hits)}")
    for h in hits[:10]:
        print(f"    {h['title']}")
except Exception as e:
    print(f"  Commons search error: {e}")

print()
print("=" * 60)
print("PROBE 3: Penn Museum search.php (HTML scrape for image URLs)")
print("=" * 60)
search_url = (
    "https://www.penn.museum/collections/search.php"
    "?q=indus+seal&type%5B%5D=1&images%5B%5D=yes&submit_term=Submit+Query"
)
try:
    req = urllib.request.Request(
        search_url,
        headers={"User-Agent": UA_BROWSER, "Accept": "text/html"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", errors="replace")
        print(f"  HTTP {r.status}, {len(html)} bytes")
        # Find any image URLs in search results
        imgs = re.findall(r'["\']([^"\']+\.(?:jpg|jpeg|png)[^"\']*)["\']', html, re.I)
        uniq = sorted(set(u for u in imgs if "penn" in u.lower()))
        for u in uniq[:15]:
            print(f"  IMG: {u}")
        # Find object IDs linked
        obj_ids = re.findall(r'/collections/object/(\d+)', html)
        print(f"  Object IDs found: {len(obj_ids)} — sample: {obj_ids[:5]}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}: {e.reason}")
except Exception as e:
    print(f"  Error: {e}")

print()
print("=" * 60)
print("PROBE 4: Internet Archive — Penn Museum Indus objects")
print("=" * 60)
# Try IA search for Penn Museum Indus content
ia_url = (
    "https://archive.org/advancedsearch.php"
    "?q=penn+museum+indus+seal"
    "&fl[]=identifier,title,mediatype"
    "&output=json&rows=10"
)
try:
    req = urllib.request.Request(ia_url, headers={"User-Agent": UA_BOT})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    docs = data.get("response", {}).get("docs", [])
    print(f"  IA results: {len(docs)}")
    for d in docs:
        print(f"    {d.get('identifier')} — {d.get('title','?')} ({d.get('mediatype','?')})")
except Exception as e:
    print(f"  IA search error: {e}")
