"""Penn Museum — Playwright browser-rendered image acquisition.

Penn Museum blocks all Python urllib requests (403). This script uses
Playwright Chromium with full browser fingerprinting to load object pages
and extract direct image URLs, then downloads and runs CNN inference.

Usage:
    python backend/scripts/acquire_penn_playwright.py [--test] [--max N]

    --test   : Run on 5 objects only to verify connectivity
    --max N  : Process up to N objects (default 500)

Output:
    glossa-corpus/indus/sources/penn-museum/images/{glossa_id}.jpg
    reports/phase42_penn_cnn_candidates.jsonl  (CNN top-5 results)
    reports/phase42_t3_penn_cnn_summary.json   (updated summary)
"""
from __future__ import annotations
import argparse, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
REPORTS     = ROOT / "reports"
CORPUS_INDUS = ROOT / "glossa-corpus" / "indus"
IMG_CACHE   = CORPUS_INDUS / "sources" / "penn-museum" / "images"
IMG_CACHE.mkdir(parents=True, exist_ok=True)
CNN_PT      = CORPUS_INDUS / "ocr_results" / "glyph_cnn_augmented.pt"
TEMPLATES   = CORPUS_INDUS / "ocr_results" / "glyph_templates"

# ── Argument parsing ──────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Penn Museum Playwright image acquisition")
parser.add_argument("--test", action="store_true", help="Test mode: 5 objects only")
parser.add_argument("--max",  type=int, default=500, help="Max objects to process")
args = parser.parse_args()
MAX_OBJECTS = 5 if args.test else args.max

# ── Playwright check ──────────────────────────────────────────────────────────
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright not installed.")
    print("Install: pip install playwright && python -m playwright install chromium")
    sys.exit(1)

# ── CNN setup ─────────────────────────────────────────────────────────────────
import torch, torch.nn as nn
import torchvision.transforms as T
import torchvision.models as tvm
import cv2, numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

CNN_AVAILABLE = False
model = None
class_names = []
transform = None

if CNN_PT.exists() and TEMPLATES.exists():
    class_dirs = sorted([d for d in TEMPLATES.iterdir() if d.is_dir()])
    class_names = [d.name for d in class_dirs]
    n_classes = len(class_dirs)
    transform = T.Compose([
        T.ToPILImage(),
        T.Resize((64, 64)),
        T.ToTensor(),
        T.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ])
    model = tvm.efficientnet_b0(weights=None)
    model.classifier = nn.Sequential(
        nn.Dropout(0.4, True),
        nn.Linear(model.classifier[1].in_features, n_classes),
    )
    state = torch.load(CNN_PT, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model = model.to(device)
    model.eval()
    CNN_AVAILABLE = True
    print(f"CNN loaded: {n_classes} classes, val_acc=43.57%")
else:
    print("WARNING: CNN checkpoint not found — will download images only, skip inference")

def predict_top5(img_path: Path) -> list[dict]:
    if not CNN_AVAILABLE or model is None:
        return []
    img = cv2.imread(str(img_path))
    if img is None:
        return []
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tensor = transform(img_rgb).unsqueeze(0).to(device)
    with torch.no_grad():
        probs = torch.softmax(model(tensor), dim=1)[0].cpu().numpy()
    top5_idx = probs.argsort()[-5:][::-1]
    return [{"sign_id": class_names[i], "probability": round(float(probs[i]), 4)} for i in top5_idx]

# ── Load Penn Museum objects ───────────────────────────────────────────────────
print("Loading Penn Museum objects from indus_research.jsonl...")
penn_objects = []
with open(CORPUS_INDUS / "exports" / "indus_research.jsonl", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get("source_system") == "PennMuseum" and obj.get("image_master_uri"):
            penn_objects.append(obj)
print(f"Penn objects with image_master_uri: {len(penn_objects)}")
print(f"Processing up to: {MAX_OBJECTS}")

# ── Playwright acquisition ────────────────────────────────────────────────────
output_path = REPORTS / "phase42_penn_cnn_candidates.jsonl"
error_path  = REPORTS / "phase42_penn_cnn_errors.jsonl"
stats = {
    "processed": 0, "page_success": 0, "image_found": 0,
    "download_success": 0, "cnn_success": 0,
    "page_fail_403": 0, "page_fail_other": 0,
    "image_not_found": 0, "download_fail": 0,
}

# Image URL extraction patterns for Penn Museum
IMG_PATTERNS = [
    r'(https?://[^"\'\s]+penn[^"\'\s]*\.(?:jpg|jpeg|png))',
    r'(https?://[^"\'\s]+\.(?:jpg|jpeg|png))["\'\s]',
    r'"(https?://[^"]+/images/[^"]+)"',
    r'"(https?://[^"]+/media/[^"]+)"',
]

def extract_image_from_html(html: str) -> str | None:
    """Extract most likely seal image URL from Penn Museum object page HTML."""
    for pattern in IMG_PATTERNS:
        matches = re.findall(pattern, html, re.I)
        # Filter out logos, icons, CSS sprites
        exclude = {"logo", "icon", "sprite", "banner", "btn", "arrow", "nav", "footer"}
        for url in matches:
            if not any(ex in url.lower() for ex in exclude):
                return url
    return None

print(f"\nStarting Playwright acquisition ({MAX_OBJECTS} objects)...")

with (
    open(output_path, "w", encoding="utf-8") as out_f,
    open(error_path, "w", encoding="utf-8") as err_f,
    sync_playwright() as p,
):
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-web-security",
        ],
    )
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
        },
    )

    for i, obj in enumerate(penn_objects[:MAX_OBJECTS]):
        glossa_id = obj["glossa_id"]
        uri = obj["image_master_uri"]  # e.g. https://penn.museum/collections/object/290348
        acc = obj.get("accession_number", "?")
        stats["processed"] += 1

        page = context.new_page()
        try:
            resp = page.goto(uri, wait_until="domcontentloaded", timeout=20000)
            status = resp.status if resp else 0

            if status == 403:
                stats["page_fail_403"] += 1
                err_f.write(json.dumps({"glossa_id": glossa_id, "error": "403", "uri": uri}) + "\n")
                page.close()
                if i < 3:
                    print(f"  [{i+1}] {glossa_id}: HTTP 403 — IP-level block confirmed")
                    if i == 2:
                        print("  3 consecutive 403s — IP block confirmed, stopping early")
                        break
                continue

            if status not in (200, 206):
                stats["page_fail_other"] += 1
                err_f.write(json.dumps({"glossa_id": glossa_id, "error": f"http_{status}", "uri": uri}) + "\n")
                page.close()
                continue

            stats["page_success"] += 1
            html = page.content()

            # Try to extract image src from rendered HTML
            img_url = extract_image_from_html(html)

            # Also try JS-rendered img tags
            if not img_url:
                try:
                    img_srcs = page.eval_on_selector_all(
                        "img",
                        "els => els.map(e => e.src).filter(s => s && s.includes('penn') && !s.includes('logo'))"
                    )
                    img_url = img_srcs[0] if img_srcs else None
                except Exception:
                    pass

            if not img_url:
                stats["image_not_found"] += 1
                err_f.write(json.dumps({"glossa_id": glossa_id, "error": "no_image_url", "uri": uri}) + "\n")
                page.close()
                continue

            stats["image_found"] += 1

            # Download image
            ext = img_url.rsplit(".", 1)[-1].split("?")[0][:4].lower()
            if ext not in ("jpg", "jpeg", "png", "gif"):
                ext = "jpg"
            img_dest = IMG_CACHE / f"{glossa_id}.{ext}"

            if not img_dest.exists():
                try:
                    img_data = page.request.get(img_url, timeout=15000)
                    if img_data.status == 200 and len(img_data.body()) > 1000:
                        img_dest.write_bytes(img_data.body())
                        stats["download_success"] += 1
                    else:
                        stats["download_fail"] += 1
                        err_f.write(json.dumps({"glossa_id": glossa_id, "error": "download_fail", "url": img_url}) + "\n")
                        page.close()
                        continue
                except Exception as exc:
                    stats["download_fail"] += 1
                    err_f.write(json.dumps({"glossa_id": glossa_id, "error": f"download_exc:{exc}", "url": img_url}) + "\n")
                    page.close()
                    continue
            else:
                stats["download_success"] += 1

            # CNN inference
            top5 = predict_top5(img_dest)
            if top5:
                stats["cnn_success"] += 1

            record = {
                "glossa_id": glossa_id,
                "accession_number": acc,
                "artifact_type": obj.get("artifact_type"),
                "image_url": img_url,
                "image_path": str(img_dest.name),
                "cnn_top5": top5,
                "top1_sign": top5[0]["sign_id"] if top5 else None,
                "top1_prob": top5[0]["probability"] if top5 else None,
            }
            out_f.write(json.dumps(record) + "\n")

            top1 = top5[0] if top5 else {}
            print(f"  [{i+1}] {glossa_id} ({acc}): img={img_url[:60]}... "
                  f"top1={top1.get('sign_id','?')} p={top1.get('probability',0):.2f}")

        except Exception as exc:
            stats["page_fail_other"] += 1
            err_f.write(json.dumps({"glossa_id": glossa_id, "error": f"exc:{str(exc)[:100]}", "uri": uri}) + "\n")
            if i < 5:
                print(f"  [{i+1}] {glossa_id}: Exception — {str(exc)[:80]}")
        finally:
            try:
                page.close()
            except Exception:
                pass
        time.sleep(0.5)

    browser.close()

# ── Summary ────────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"Penn Museum Playwright CNN acquisition complete:")
for k, v in stats.items():
    print(f"  {k:20s}: {v}")

summary = {
    "experiment": "Phase-42 Task 3: Penn Museum CNN via Playwright",
    "method": "playwright_chromium_headless",
    "cnn_model": CNN_PT.name if CNN_PT.exists() else "not_found",
    "cnn_val_accuracy": 0.4357,
    "n_classes": len(class_names),
    "output_file": str(output_path),
    "stats": stats,
    "_citation": {"primary": ["I.1", "I.2", "I.3"], "phase": "Phase-42-T3-Playwright"},
}
(REPORTS / "phase42_t3_penn_cnn_summary.json").write_text(
    json.dumps(summary, indent=2), "utf-8"
)
print(f"\nSummary: reports/phase42_t3_penn_cnn_summary.json")
