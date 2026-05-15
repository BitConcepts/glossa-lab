"""One-off probe: fetch a Penn Museum object page and look for image URLs."""
import urllib.request, urllib.error, re

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

for obj_id in [290348, 32524, 32525]:
    url = f"https://www.penn.museum/collections/object/{obj_id}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", errors="replace")
            print(f"\n=== {url} (HTTP {r.status}) ===")
            # Any .jpg/.png/.gif URLs
            imgs = re.findall(r'["\']([^"\']*\.(?:jpg|jpeg|png|gif)[^"\']*)["\']', html, re.I)
            unique_imgs = sorted(set(u for u in imgs if "penn" in u.lower() or u.startswith("http")))
            for u in unique_imgs[:20]:
                print("  IMG:", u)
            # Look for CDN/media patterns
            cdn = re.findall(r'["\']([^"\']*(?:media|image|photo|thumb)[^"\']*)["\']', html, re.I)
            cdn_uniq = sorted(set(u for u in cdn if "penn" in u.lower() and len(u) > 20))
            for u in cdn_uniq[:10]:
                print("  CDN:", u)
            # Look for manifest/IIIF
            iiif = re.findall(r'["\']([^"\']*iiif[^"\']*)["\']', html, re.I)
            for u in iiif[:5]:
                print("  IIIF:", u)
    except urllib.error.HTTPError as e:
        print(f"\n=== {url} ===")
        print(f"  HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"\n=== {url} ===")
        print(f"  Error: {e}")
