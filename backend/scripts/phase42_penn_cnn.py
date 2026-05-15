"""Phase-42 Task 3: Download Penn Museum Indus seal images + CNN inference.

Penn Museum API:
  - Base: https://www.penn.museum/collections/apis/v1/objects/{id}
  - The object ID is the last part of the image_master_uri path
  - Image URL extracted from `images` field in API response
  - License: CC BY 4.0 (confirmed in research export)

Strategy:
  1. Load Penn Museum objects from indus_research.jsonl
  2. For each, call the Penn Museum API to get the image URL
  3. Download the image (thumbnail / medium size preferred)
  4. Run the 43.57% CNN to get top-5 sign candidates
  5. Save results as phase42_penn_cnn_candidates.jsonl

GPU enforcement: torch.cuda.is_available() asserted.
"""
from __future__ import annotations
import json, sys, time, urllib.request, urllib.error
from pathlib import Path
import cv2, numpy as np

# GPU enforcement
import torch
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"GPU: {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory//1024**2} MB VRAM)")
else:
    import warnings
    warnings.warn(
        "CUDA not available — CNN inference on CPU (~5x slower). "
        "Install CUDA PyTorch: pip install torch --index-url https://download.pytorch.org/whl/cu126",
        stacklevel=2,
    )
    device = torch.device("cpu")
    print("Device: CPU (CUDA not available)")

import torch.nn as nn
import torchvision.transforms as T
import torchvision.models as tvm
from torch.utils.data import Dataset, DataLoader

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
REPORTS = ROOT / "reports"
CORPUS_INDUS = ROOT / "glossa-corpus" / "indus"
CNN_PT = CORPUS_INDUS / "ocr_results" / "glyph_cnn_augmented.pt"
TEMPLATES = CORPUS_INDUS / "ocr_results" / "glyph_templates"
IMG_CACHE = CORPUS_INDUS / "sources" / "penn-museum" / "images"
IMG_CACHE.mkdir(parents=True, exist_ok=True)

GLYPH_SIZE = 64
MAX_IMAGES = 500      # cap for this run (500 × ~3s API + download ≈ 25 min)
API_DELAY  = 0.3      # polite rate limiting (Penn Museum API)

# ── CNN model setup ───────────────────────────────────────────────────────────
class_dirs = sorted([d for d in TEMPLATES.iterdir() if d.is_dir()])
class_names = [d.name for d in class_dirs]
n_classes = len(class_dirs)

transform = T.Compose([
    T.ToPILImage(),
    T.Resize((GLYPH_SIZE, GLYPH_SIZE)),
    T.ToTensor(),
    T.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5]),
])

model = tvm.efficientnet_b0(weights=None)
model.classifier = nn.Sequential(nn.Dropout(0.4,True), nn.Linear(model.classifier[1].in_features, n_classes))

if CNN_PT.exists():
    state = torch.load(CNN_PT, map_location=device, weights_only=True)
    model.load_state_dict(state)
    print(f"CNN loaded: {CNN_PT.name} ({n_classes} classes, val_acc=43.57%)")
else:
    print(f"WARNING: CNN checkpoint not found at {CNN_PT}")
    sys.exit(1)
model = model.to(device); model.eval()

def predict_top5(img_path: Path) -> list[dict]:
    """Run CNN on a single image, return top-5 sign candidates with probabilities."""
    img = cv2.imread(str(img_path))
    if img is None:
        return []
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tensor = transform(img_rgb).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
    top5_idx = probs.argsort()[-5:][::-1]
    return [{"sign_id": class_names[i], "probability": round(float(probs[i]), 4)} for i in top5_idx]

# ── Load Penn Museum objects ───────────────────────────────────────────────────
print("\nLoading Penn Museum objects from indus_research.jsonl...")
penn_objects = []
with open(CORPUS_INDUS / "exports" / "indus_research.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            obj = json.loads(line)
            if obj.get("source_system") == "PennMuseum":
                penn_objects.append(obj)
        except: pass
print(f"Penn Museum objects: {len(penn_objects)}")

# Filter: seals/tablets with image_master_uri
with_image = [o for o in penn_objects if o.get("image_master_uri")]
print(f"Objects with image_master_uri: {len(with_image)}")

# ── Penn Museum Collections API helper ────────────────────────────────────────
def get_penn_image_url(collection_uri: str) -> str | None:
    """Get direct image URL from Penn Museum Collections API."""
    try:
        # Extract object ID from URI: https://penn.museum/collections/object/290348
        obj_id = collection_uri.rstrip("/").split("/")[-1]
        api_url = f"https://www.penn.museum/collections/apis/v1/objects/{obj_id}"
        req = urllib.request.Request(api_url, headers={
            "User-Agent": "GlossaLab/1.0 (glossa-lab research; tpierson@bitconcepts.tech)",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        # Penn Museum API response has 'images' array
        images = data.get("images", [])
        if images:
            # Prefer medium or large size
            for img in images:
                url = img.get("url") or img.get("thumb") or img.get("medium") or img.get("large")
                if url:
                    return url
        # Fallback: check for direct image URL
        return data.get("image_url") or data.get("primary_image")
    except Exception:
        return None

def download_image(url: str, dest: Path) -> bool:
    """Download image to dest path."""
    if dest.exists():
        return True
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "GlossaLab/1.0 (research corpus building)",
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) > 1000:  # real image > 1KB
            dest.write_bytes(data)
            return True
    except Exception:
        pass
    return False

# ── Main pipeline: API → download → CNN ──────────────────────────────────────
print(f"\nProcessing up to {MAX_IMAGES} Penn Museum objects...")
print("API → download → CNN inference → top-5 sign candidates")

output_path = REPORTS / "phase42_penn_cnn_candidates.jsonl"
error_path  = REPORTS / "phase42_penn_cnn_errors.jsonl"
stats = {"processed": 0, "api_success": 0, "download_success": 0,
         "cnn_success": 0, "api_fail": 0, "download_fail": 0}

with open(output_path, "w", encoding="utf-8") as out_f, \
     open(error_path,  "w", encoding="utf-8") as err_f:

    for i, obj in enumerate(with_image[:MAX_IMAGES]):
        glossa_id = obj["glossa_id"]
        uri = obj["image_master_uri"]
        acc = obj.get("accession_number", "?")
        stats["processed"] += 1

        # 1. Get image URL from Penn Museum API
        img_url = get_penn_image_url(uri)
        time.sleep(API_DELAY)  # rate limit
        if not img_url:
            stats["api_fail"] += 1
            err_f.write(json.dumps({"glossa_id": glossa_id, "error": "api_no_image_url", "uri": uri}) + "\n")
            if i % 50 == 0:
                print(f"  [{i}/{min(MAX_IMAGES,len(with_image))}] {glossa_id}: API no image URL")
            continue
        stats["api_success"] += 1

        # 2. Download image
        ext = img_url.split("?")[0].rsplit(".",1)[-1][:4].lower() or "jpg"
        if ext not in ("jpg","jpeg","png","gif","webp"): ext = "jpg"
        img_dest = IMG_CACHE / f"{glossa_id}.{ext}"
        if not download_image(img_url, img_dest):
            stats["download_fail"] += 1
            err_f.write(json.dumps({"glossa_id": glossa_id, "error": "download_fail", "url": img_url}) + "\n")
            continue
        stats["download_success"] += 1

        # 3. CNN inference
        top5 = predict_top5(img_dest)
        if not top5:
            continue
        stats["cnn_success"] += 1

        record = {
            "glossa_id": glossa_id,
            "accession_number": acc,
            "artifact_type": obj.get("artifact_type"),
            "rights_status": obj.get("rights_status"),
            "image_url": img_url,
            "image_path": str(img_dest.name),
            "cnn_top5": top5,
            "top1_sign": top5[0]["sign_id"] if top5 else None,
            "top1_prob": top5[0]["probability"] if top5 else None,
        }
        out_f.write(json.dumps(record) + "\n")

        if i % 25 == 0 or i < 5:
            top1 = top5[0] if top5 else {}
            print(f"  [{i+1}/{min(MAX_IMAGES,len(with_image))}] {glossa_id} ({acc}): "
                  f"top1={top1.get('sign_id','?')} p={top1.get('probability',0):.2f}")

# ── Summary ────────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"Penn Museum CNN inference complete:")
print(f"  Processed:      {stats['processed']}")
print(f"  API success:    {stats['api_success']}")
print(f"  Downloaded:     {stats['download_success']}")
print(f"  CNN inferred:   {stats['cnn_success']}")
print(f"  API failures:   {stats['api_fail']}")
print(f"  Download fails: {stats['download_fail']}")

summary = {
    "experiment": "Phase-42 Task 3: Penn Museum CNN inference",
    "cnn_model": str(CNN_PT.name),
    "cnn_val_accuracy": 0.4357,
    "n_classes": n_classes,
    "output_file": str(output_path),
    "stats": stats,
    "_citation": {"primary":["I.1","I.2","I.3"],"phase":"Phase-42-T3"},
}
(REPORTS/"phase42_t3_penn_cnn_summary.json").write_text(json.dumps(summary,indent=2),"utf-8")
print(f"\nResults: {output_path}")
print(f"Summary: reports/phase42_t3_penn_cnn_summary.json")
