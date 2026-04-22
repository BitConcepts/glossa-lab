"""
Apply confirmed Y→P crosswalk to re-label Yajnadevam inscriptions.

Takes the 184 confirmed Yajnadevam GLYPHID → Parpola P-number mappings
(confidence ≥ 0.80, from sequence alignment on shared Mohenjo-daro inscriptions)
and re-labels every Yajnadevam inscription's sign sequence:
  - Y-signs with a confirmed P-mapping → replaced with P-number
  - Y-signs without a confirmed mapping → retained as Yunmapped_NNNN

This produces a unified sign namespace for cross-site analysis.

Run from glossa-lab root:
    python scripts/apply_yp_crosswalk.py

Outputs:
    data_raw/other_sites/yajnadevam_inscriptions_pnumbered.json
    logs/yp_crosswalk_application_log.md
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSSWALK_PATH = ROOT / "crosswalks" / "yajnadevam_to_parpola_crosswalk.csv"
YJ_PATH = ROOT / "data_raw" / "other_sites" / "yajnadevam_inscriptions.json"
OUT_PATH = ROOT / "data_raw" / "other_sites" / "yajnadevam_inscriptions_pnumbered.json"
LOGS = ROOT / "logs"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

MIN_CONFIDENCE = 0.80  # only apply mappings at or above this threshold


def load_crosswalk() -> dict[str, str]:
    """Load Y→P mapping: {Y0xxx → P-number} for confirmed entries."""
    mapping: dict[str, str] = {}
    with open(CROSSWALK_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if float(row["match_confidence"]) >= MIN_CONFIDENCE:
                y_id = row["registry_sign_id_yajnadevam"]  # e.g. Y0017
                p_id = row["best_parpola_match"]            # e.g. P122
                mapping[y_id] = p_id
    return mapping


def translate_sequence(sign_ids: list[str], mapping: dict[str, str]) -> tuple[list[str], int, int]:
    """
    Translate a sign sequence using the Y→P mapping.
    Returns (translated_signs, n_mapped, n_unmapped).
    """
    translated = []
    n_mapped = 0
    n_unmapped = 0
    for sign_id in sign_ids:
        if sign_id in mapping:
            translated.append(mapping[sign_id])
            n_mapped += 1
        else:
            # Keep Y-sign with a clear prefix indicating unmapped status
            glyph_num = sign_id[1:]  # strip Y prefix
            translated.append(f"Yunmapped_{glyph_num}")
            n_unmapped += 1
    return translated, n_mapped, n_unmapped


def main() -> None:
    print("=" * 60)
    print("Apply Y→P Crosswalk to Yajnadevam Corpus")
    print("=" * 60)

    print(f"\nLoading crosswalk (min confidence {MIN_CONFIDENCE})...")
    mapping = load_crosswalk()
    print(f"  {len(mapping)} confirmed Y→P mappings loaded")
    print(f"  Sample: {list(mapping.items())[:5]}")

    print("\nLoading Yajnadevam inscriptions...")
    records = json.loads(YJ_PATH.read_text("utf-8"))
    print(f"  {len(records)} inscriptions")

    print("\nApplying crosswalk...")
    total_tokens = 0
    total_mapped = 0
    total_unmapped = 0
    translated_records = []

    for rec in records:
        original_seq = rec["sign_sequence_raw"].split()
        translated_seq, n_mapped, n_unmapped = translate_sequence(original_seq, mapping)
        total_tokens += len(original_seq)
        total_mapped += n_mapped
        total_unmapped += n_unmapped

        # Build updated record
        new_rec = dict(rec)
        new_seq_str = " ".join(translated_seq)
        new_rec["sign_sequence_raw"] = new_seq_str
        new_rec["sequence_source_exact"] = new_seq_str  # preserve original in notes
        new_rec["sequence_registry_ids"] = new_seq_str
        new_rec["sequence_variant_sensitive"] = new_seq_str
        new_rec["sequence_variant_collapsed_light"] = new_seq_str
        new_rec["notes"] = (
            rec.get("notes", "") +
            f" | original_y_seq={rec['sign_sequence_raw']}"
        )
        new_rec["sign_numbering_system"] = (
            "Parpola (1982) P-numbers [via Y→P crosswalk, conf≥0.80] "
            "+ Yunmapped_NNNN for unmapped signs"
        )
        new_rec["crosswalk_applied"] = "yes"
        new_rec["crosswalk_map_rate"] = round(n_mapped / len(original_seq), 4) if original_seq else 0
        translated_records.append(new_rec)

    map_rate = round(total_mapped / total_tokens, 4) if total_tokens else 0
    print(f"  Total tokens: {total_tokens}")
    print(f"  Mapped (Y→P): {total_mapped} ({round(100*map_rate,1)}%)")
    print(f"  Unmapped (Yunmapped_*): {total_unmapped} ({round(100*(1-map_rate),1)}%)")

    # Distinct P-signs now visible in Yajnadevam corpus
    all_p_signs = set()
    all_y_unmapped = set()
    for rec in translated_records:
        for sign in rec["sign_sequence_raw"].split():
            if sign.startswith("P"):
                all_p_signs.add(sign)
            elif sign.startswith("Yunmapped_"):
                all_y_unmapped.add(sign)
    print(f"  Distinct P-signs now in Yajnadevam corpus: {len(all_p_signs)}")
    print(f"  Distinct unmapped Yunmapped_ signs: {len(all_y_unmapped)}")

    # Save output
    OUT_PATH.write_text(
        json.dumps(translated_records, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"\nSaved: {OUT_PATH}")

    # Write log
    log_lines = [
        "# Y→P Crosswalk Application Log",
        f"Applied: {NOW}",
        f"Min confidence threshold: {MIN_CONFIDENCE}",
        "",
        "## Statistics",
        f"- Confirmed mappings applied: {len(mapping)}",
        f"- Inscriptions processed: {len(records)}",
        f"- Total sign tokens: {total_tokens}",
        f"- Tokens mapped (Y→P): {total_mapped} ({round(100*map_rate,1)}%)",
        f"- Tokens unmapped (Yunmapped_*): {total_unmapped} ({round(100*(1-map_rate),1)}%)",
        f"- Distinct P-signs in translated corpus: {len(all_p_signs)}",
        f"- Distinct unmapped Y-signs: {len(all_y_unmapped)}",
        "",
        "## Interpretation",
        f"A {round(100*map_rate,1)}% mapping rate means approximately that proportion",
        "of Yajnadevam sign tokens can now be compared directly against the",
        "CISI (Parpola) corpus. Unmapped signs (Yunmapped_*) represent GLYPHIDs",
        "with no confident Parpola equivalent — likely rare signs, composite signs,",
        "or signs where Yajnadevam's sign-splitting decision differs from Parpola's.",
        "",
        "## Next step",
        "Update build_corpus_pipeline.py to use yajnadevam_inscriptions_pnumbered.json",
        "instead of yajnadevam_inscriptions.json, then re-run cross-site analysis.",
    ]
    (LOGS / "yp_crosswalk_application_log.md").write_text(
        "\n".join(log_lines), encoding="utf-8"
    )
    print("Log written.")
    print("=" * 60)
    print(f"Map rate: {round(100*map_rate,1)}% of Yajnadevam tokens now use P-numbers")
    print("Run build_corpus_pipeline.py + cross_site_analysis.py next.")
    print("=" * 60)


if __name__ == "__main__":
    main()
