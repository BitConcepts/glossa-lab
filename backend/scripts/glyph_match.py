"""Mahadevan 1977 — Template matching classifier.

Classifies extracted glyph crops against canonical sign templates using
Normalized Cross-Correlation (NCC). No training required — the consistent
printed typeface means NCC works reliably.

Strategy:
  For each query glyph:
    1. Preprocess to binary (threshold + normalize)
    2. Compute NCC with every canonical template
    3. Return the sign_id with highest NCC score

Validation mode (--validate):
  For textnums where we KNOW the sign sequence (Firestore),
  run the classifier and report accuracy.

Usage:
    # Validate on known texts
    shell.cmd python backend/scripts/glyph_match.py --validate --n 50

    # Classify unknown textnums (the 308 missing ones)
    shell.cmd python backend/scripts/glyph_match.py --missing

    # Classify all textnums with crops
    shell.cmd python backend/scripts/glyph_match.py --all
"""
from __future__ import annotations
import json, re, sys
from datetime import datetime
from pathlib import Path
import numpy as np
import cv2

REPO = Path(__file__).parents[2]
CROPS_DIR = REPO / "glossa-corpus/indus/ocr_results/glyph_crops"
TMPL_DIR  = REPO / "glossa-corpus/indus/ocr_results/glyph_templates"
FIRESTORE = (REPO / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe"
             / "firestore_indusarrays_full.json")
MISSING_F = REPO / "glossa-corpus/indus/ocr_results/m77_textnums_missing.json"
OUT_DIR   = REPO / "glossa-corpus/indus/ocr_results"

GLYPH_SIZE = 64


def sanitize_sign(s: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', s.strip()).lstrip("0") or "0"


# ── Binary pixel similarity (IoU) ────────────────────────────────────────────
# Better than EfficientNet for printed Indus signs:
# Treats each glyph as a binary ink-mask and computes intersection-over-union.
# Also uses ALL labeled samples (k-NN), not just the canonical.

_ALL_SAMPLES: dict[str, list[np.ndarray]] = {}  # {sign_id: [binary_flat, ...]}

def binarize(img_bgr: np.ndarray) -> np.ndarray:
    """Convert glyph to normalized binary flat vector (ink=1, background=0)."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
    inv = (binary == 0).astype(np.float32)  # ink pixels = 1
    return inv.flatten()


def iou_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Intersection over Union of two binary flat vectors."""
    intersection = np.sum(a * b)
    union = np.sum(np.maximum(a, b))
    return float(intersection / (union + 1e-8))


def load_templates() -> dict[str, list[np.ndarray]]:
    """Load ALL sample images per sign class as binary vectors.
    Returns {sign_id: [binary_flat, ...]}.
    """
    global _ALL_SAMPLES
    if _ALL_SAMPLES:
        return _ALL_SAMPLES

    print("  Loading sample images for k-NN matching...")
    for d in sorted(TMPL_DIR.iterdir()):
        if not d.is_dir():
            continue
        samples = []
        # Load canonical + up to 5 samples for efficiency
        for f in [d / "canonical.png"] + sorted(d.glob("sample_*.png"))[:5]:
            if not f.exists():
                continue
            img = cv2.imread(str(f))
            if img is not None:
                samples.append(binarize(img))
        if samples:
            _ALL_SAMPLES[d.name] = samples

    print(f"  Loaded {len(_ALL_SAMPLES)} sign classes")
    return _ALL_SAMPLES


def classify_glyph(glyph: np.ndarray, templates: dict[str, list[np.ndarray]],
                    top_k: int = 3) -> list[tuple[str, float]]:
    """k-NN classification using IoU on binary glyph images.
    For each candidate sign: compute max IoU over all its samples.
    """
    q = binarize(glyph)
    scores = []
    for sid, samples in templates.items():
        best_iou = max(iou_sim(q, s) for s in samples)
        scores.append((sid, best_iou))
    scores.sort(key=lambda x: -x[1])
    return scores[:top_k]


def classify_textnum(textnum: int, templates: dict[str, np.ndarray]
                      ) -> list[str] | None:
    """Classify all glyphs for a textnum. Returns predicted sign sequence."""
    d = CROPS_DIR / str(textnum)
    if not d.exists():
        return None
    files = sorted(d.glob("glyph_*.png"))
    if not files:
        return None
    sequence = []
    for f in files:
        img = cv2.imread(str(f))
        if img is None:
            continue
        top = classify_glyph(img, templates, top_k=1)
        if top:
            sequence.append(top[0][0])
    return sequence if sequence else None


def load_firestore_known() -> dict[int, list[str]]:
    """Load best sign sequence per textnum (group all docs, pick longest).
    Uses same logic as convert_indusarrays.py best_sequence()."""
    from collections import defaultdict
    data = json.loads(FIRESTORE.read_text(encoding="utf-8"))
    # Group docs by textnum
    by_tn: dict[int, list[list[str]]] = defaultdict(list)
    for doc in data.get("documents", []):
        tn = doc.get("textnum")
        if tn is None:
            continue
        texts = doc.get("texts") or []
        signs = [sanitize_sign(str(s)) for s in texts if str(s).strip()]
        if signs:
            by_tn[int(tn)].append(signs)
    # For each textnum: pick the sequence with the most signs
    result = {}
    for tn, sequences in by_tn.items():
        best = max(sequences, key=len)
        result[tn] = best
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true",
                        help="Validate on known texts (checks accuracy)")
    parser.add_argument("--missing", action="store_true",
                        help="Classify the 308 missing textnums")
    parser.add_argument("--all", action="store_true",
                        help="Classify all textnums with crops")
    parser.add_argument("--n", type=int, default=50,
                        help="Number of texts for validation (default 50)")
    args = parser.parse_args()

    print("=== M77 Glyph Template Matcher ===")
    print("Loading templates...")
    templates = load_templates()
    print(f"Templates loaded: {len(templates)} sign classes")

    if not templates:
        print("ERROR: No templates found. Run glyph_label.py first.")
        return 1

    if args.validate:
        print(f"\n--- Validation mode (n={args.n}) ---")
        known = load_firestore_known()
        # Only validate textnums that have crops
        crop_textnums = [int(d.name) for d in CROPS_DIR.iterdir()
                         if d.is_dir() and d.name.isdigit()]
        validate_textnums = [tn for tn in sorted(known.keys())
                              if tn in set(crop_textnums)][:args.n]
        print(f"Validating on {len(validate_textnums)} texts...")

        correct_signs = 0
        total_signs = 0
        correct_seqs = 0
        results = []

        for tn in validate_textnums:
            true_signs = known[tn]
            pred_signs = classify_textnum(tn, templates)
            if pred_signs is None:
                continue
            # Compare element-wise (trim to shorter length)
            min_len = min(len(true_signs), len(pred_signs))
            matches = sum(1 for t, p in zip(true_signs[:min_len], pred_signs[:min_len]) if t == p)
            correct_signs += matches
            total_signs += len(true_signs)
            if true_signs == pred_signs:
                correct_seqs += 1
            results.append({
                "textnum": tn,
                "true": true_signs,
                "pred": pred_signs,
                "match": matches,
                "total": len(true_signs),
            })

        sign_acc = correct_signs / max(total_signs, 1) * 100
        seq_acc  = correct_seqs / max(len(results), 1) * 100
        print(f"\n=== Validation Results ===")
        print(f"  Sign-level accuracy:     {sign_acc:.1f}%  ({correct_signs}/{total_signs})")
        print(f"  Sequence-level accuracy: {seq_acc:.1f}%  ({correct_seqs}/{len(results)})")
        print(f"\nSample predictions:")
        for r in results[:5]:
            print(f"  Text {r['textnum']:>5}: true={r['true'][:5]} pred={r['pred'][:5]}")

        # Save validation report
        report = {
            "_citation": {"primary_sources": ["I.8", "A.1"]},
            "generated_at": datetime.utcnow().isoformat(),
            "sign_accuracy_pct": round(sign_acc, 1),
            "sequence_accuracy_pct": round(seq_acc, 1),
            "texts_validated": len(results),
            "results": results[:20],  # sample
        }
        (OUT_DIR / "glyph_match_validation.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        print(f"\nValidation report: {OUT_DIR / 'glyph_match_validation.json'}")

    elif args.missing:
        print("\n--- Classifying 308 missing textnums ---")
        missing_data = json.loads(MISSING_F.read_text())
        missing_tns = [int(t) for t in missing_data.get("new_not_in_firestore", [])]
        print(f"Missing textnums: {len(missing_tns)}")

        results = []
        found = 0
        for tn in missing_tns:
            pred = classify_textnum(tn, templates)
            if pred:
                results.append({"textnum": tn, "predicted_signs": pred, "sign_count": len(pred)})
                found += 1
            else:
                results.append({"textnum": tn, "predicted_signs": None, "sign_count": 0,
                                 "note": "no crops available"})

        print(f"  Classified: {found}/{len(missing_tns)}")
        out = OUT_DIR / "missing_sequences.json"
        out.write_text(json.dumps({
            "_citation": {
                "primary_sources": ["I.8", "A.1"],
                "derivation": ("Predicted sign sequences for 308 IM77 textnums missing from "
                               "indusscript.in. Method: template matching on M77 IIIF scan pages. "
                               "Confidence: requires validation against CISI/RMRL data."),
                "status": "[INFERRED] — not verified against official sources",
            },
            "generated_at": datetime.utcnow().isoformat(),
            "total_missing": len(missing_tns),
            "classified": found,
            "results": results,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  Saved: {out}")

    elif args.all:
        print("\n--- Classifying all textnums with crops ---")
        crop_textnums = sorted(int(d.name) for d in CROPS_DIR.iterdir()
                               if d.is_dir() and d.name.isdigit())
        print(f"Textnums with crops: {len(crop_textnums)}")
        results = []
        for i, tn in enumerate(crop_textnums):
            pred = classify_textnum(tn, templates)
            if pred:
                results.append({"textnum": tn, "predicted_signs": pred})
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i+1}/{len(crop_textnums)}")

        out = OUT_DIR / "all_sequences.json"
        out.write_text(json.dumps({
            "_citation": {"primary_sources": ["I.8", "A.1"]},
            "generated_at": datetime.utcnow().isoformat(),
            "total": len(results),
            "results": results,
        }, indent=2), encoding="utf-8")
        print(f"\nSaved: {out} ({len(results)} sequences)")
    else:
        print("Use --validate, --missing, or --all")

    return 0


if __name__ == "__main__":
    sys.exit(main())
