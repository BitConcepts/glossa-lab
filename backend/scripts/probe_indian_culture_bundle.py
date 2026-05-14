"""Analyze Indian Culture Portal React bundle for API endpoints and ebook paths."""
import re
import urllib.request
from pathlib import Path

REPO = Path(__file__).parents[2]
IC_DIR = REPO / "glossa-corpus" / "indus" / "sources" / "indian-culture" / "raw" / "2026-05-14"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0"
BASE = "https://www.indianculture.gov.in"

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

# Find main JS URL from captured HTML
html_path = IC_DIR / "mohenjo-daro-civ.html"
if not html_path.exists():
    print("ERROR: No captured HTML found. Run acquire_indian_culture_playwright.py first.")
    exit(1)

html = html_path.read_text(encoding="utf-8", errors="replace")
m = re.search(r'/static/js/main\.([a-f0-9]+)\.js', html)
if not m:
    print("Could not find main React bundle URL in HTML")
    # Try to download based on the main.js pattern in network log
    exit(1)

main_js_url = f"{BASE}/static/js/main.{m.group(1)}.js"
print(f"Main React bundle: {main_js_url}")

# Download if not already cached
main_js_path = IC_DIR / "main_react.js"
if not main_js_path.exists():
    print("Downloading...")
    data = fetch(main_js_url)
    main_js_path.write_bytes(data)
    print(f"Saved: {len(data):,} bytes")
else:
    data = main_js_path.read_bytes()
    print(f"Using cached: {len(data):,} bytes")

text = data.decode("utf-8", errors="ignore")

# Extract useful patterns
apis = set(re.findall(r'["\'/]+(api/v\d+/[^"\' \n`]{3,100})', text))
apis2 = set(re.findall(r'["\'`](/api/[^"\'`\n]{3,100})["\'`]', text))
fetches = set(re.findall(r'fetch\(["\'](https?://[^"\']{5,150})["\']\)', text))
base_urls = set(re.findall(r'(?:baseURL|BASE_URL|apiUrl|API_URL)["\': ]+["\'](https?://[^"\']{5,100})["\']', text))
ebook_paths = set(re.findall(r'["\'`]([^"\'`\n ]{0,50}(?:ebook|pdf|rarebook|flipbook|viewer|archive|content/book)[^"\'`\n ]{0,80})["\'`]', text, re.IGNORECASE))
env_vars = set(re.findall(r'process\.env\.(\w+)', text))
cms_paths = set(re.findall(r'["\'`]([^"\'`\n ]*(?:cms|content|media|storage|s3|cdn)[^"\'`\n ]{0,100})["\'`]', text, re.IGNORECASE))

print("\n=== /api/ paths ===")
for x in sorted(apis | apis2)[:30]:
    print(f"  {x}")

print("\n=== fetch() URLs ===")
for x in sorted(fetches)[:20]:
    print(f"  {x}")

print("\n=== Base/API URLs ===")
for x in sorted(base_urls)[:15]:
    print(f"  {x}")

print("\n=== Ebook/PDF/viewer paths ===")
for x in sorted(ebook_paths)[:25]:
    print(f"  {x}")

print("\n=== Environment variables ===")
for x in sorted(env_vars)[:20]:
    print(f"  {x}")

print("\n=== CMS/media/storage paths ===")
for x in sorted(cms_paths)[:20]:
    print(f"  {x}")

# Also look for API keys/tokens that might hint at the backend
aws = set(re.findall(r'AKIA[A-Z0-9]{16}', text))  # AWS access key pattern
if aws:
    print(f"\n=== AWS patterns found ({len(aws)}) ===")
    # Don't print actual keys

# Look for common API base patterns
endpoint_candidates = []
for pattern in [r'https://[^"\'`\n ]{10,150}(?:api|backend|cms|content)\.[^"\'`\n ]{3,100}']:
    endpoint_candidates.extend(re.findall(pattern, text))
print("\n=== API-like full URLs in bundle ===")
for x in sorted(set(endpoint_candidates))[:20]:
    print(f"  {x}")
