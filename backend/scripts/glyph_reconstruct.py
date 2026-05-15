"""Glyph Reconstruct — merge inferred sign sequences into corpus staging.

Reads missing_sequences.json (output of glyph_match.py --missing) and
produces a JSONL staging file of [INFERRED] corpus records, one per
classified textnum.  The resulting file can be appended to the main
staging pipeline in the usual way.

Output schema mirrors objects_*_indusarrays.jsonl (indusscript-m77
source system) but uses source_system='indusscript-m77-inferred' and
review_state='inferred' to clearly distinguish predicted from verified.

Usage:
    shell.cmd python backend/scripts/glyph_reconstruct.py
"""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

REPO      = Path(__file__).parents[2]
MISSING_F = REPO / "glossa-corpus/indus/ocr_results/missing_sequences.json"
STAGING   = REPO / "glossa-corpus/indus/staging"

TODAY = date.today().strftime("%Y-%m-%d")
OUT_F = STAGING / f"objects_{TODAY}_inferred.jsonl"


def make_diplomatic(signs: list[str]) -> str:
    """Encode a sign list as a diplomatic text-code string.

    Examples:
        ["0", "67", "342"]   -> "+000-067-342+"
        ["_086", "55"]       -> "+_086-055+"   (sanitized ligature: * -> _)
    """
    parts = []
    for s in signs:
        if s.startswith("_") or s.startswith("*"):
            prefix = s[0]
            num = s[1:]
            try:
                parts.append(f"{prefix}{int(num):03d}")
            except ValueError:
                parts.append(s)
        else:
            try:
                parts.append(f"{int(s):03d}")
            except ValueError:
                parts.append(s)
    return "+" + "-".join(parts) + "+"


def main() -> int:
    if not MISSING_F.exists():
        print(f"ERROR: {MISSING_F} not found — run glyph_match.py --missing first")
        return 1

    data = json.loads(MISSING_F.read_text(encoding="utf-8"))
    results   = data.get("results", [])
    classified = [r for r in results if r.get("predicted_signs")]
    skipped    = len(results) - len(classified)

    print(f"Input : {len(results)} missing textnums "
          f"({len(classified)} classified, {skipped} no-crop skipped)")

    records: list[dict] = []
    for r in classified:
        tn    = int(r["textnum"])
        signs = [str(s) for s in r["predicted_signs"]]
        record = {
            "glossa_id":              f"GLI-IND-M77-{tn:05d}",
            "source_system":          "indusscript-m77-inferred",
            "source_object_id":       str(tn),
            "artifact_type":          "seal",        # default — unknown without Firestore
            "site_name":              None,
            "locus":                  None,
            "rights_status":          "rmrl-research",
            "text_code_diplomatic":   make_diplomatic(signs),
            "sign_id_scheme":         "Mahadevan1977",
            "canonical_grapheme_ids": [],
            "sign_instance_count":    len(signs),
            "raw_signs":              signs,
            "inscobj":                None,
            "direction":              None,
            "review_state":           "inferred",
            "pipeline_stage":         "inferred",
            "quarantine_reason":      None,
            "_source_extra": {
                "textnum":            tn,
                "method":             "glyph-iou-knn",
                "sign_accuracy_est":  29.8,
                "classifier_version": "glyph_match.py-v1",
            },
            "_citation": {
                "primary_sources": ["I.8", "A.1"],
                "derivation": (
                    f"[INFERRED] IM77 text {tn} sign sequence predicted by IoU k-NN "
                    f"template matching on M77 IIIF scan pages (glyph_match.py v1). "
                    f"Estimated sign-level accuracy ~29.8% on 50 known texts. "
                    f"NOT verified against CISI or RMRL official sources."
                ),
                "status": "[INFERRED] — requires verification",
            },
        }
        records.append(record)

    # Write staging JSONL
    STAGING.mkdir(parents=True, exist_ok=True)
    with open(OUT_F, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    total_signs = sum(r["sign_instance_count"] for r in records)
    sign_counts = [r["sign_instance_count"] for r in records]
    avg_signs   = total_signs / len(records) if records else 0.0

    print(f"Output: {OUT_F}")
    print(f"Records: {len(records)} [INFERRED] inscription objects")
    print(f"Total sign tokens: {total_signs}")
    if sign_counts:
        print(f"Avg signs/text : {avg_signs:.1f}  "
              f"(min {min(sign_counts)}, max {max(sign_counts)})")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
