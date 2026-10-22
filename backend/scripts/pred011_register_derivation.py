"""PRED-2026-011 — draft registration derivation (2026-10-20).

This script derives the proposed trained INITIAL set for
PRED-2026-011. It does not register or score the prediction.

The derivation has two steps:

  1. Recompute PRED-2026-010's underlying classification by
     importing ``backend/scripts/pred010_register_derivation.py``
     unchanged. That derivation uses the recorded
     ``global_class_stability`` logic on the CISI Mohenjo-daro
     pool only (179 inscriptions) and byte-hashes the withheld
     file without opening its inscription content.
  2. Apply the one disclosed design change for PRED-2026-011:
     screen the resulting INITIAL signs for mappability in the
     frozen Phase-396 crosswalk. A sign is eligible only when
     at least one crosswalk row names it as
     ``best_parpola_match``. Appearances in ``top3_parpola``
     do not make a sign eligible.

The screen reads the public crosswalk. It reads no Harappa
inscription rows, sequences, occurrence counts, or start rates,
and it computes no score.
"""
from __future__ import annotations

import csv
import importlib.util
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

PRED010_SCRIPT = REPO / "backend" / "scripts" / "pred010_register_derivation.py"
PRED010_RECORD = REPO / "reports" / "pred010_derivation_record.json"
CROSSWALK_CSV = (
    REPO / "data" / "crosswalks" / "yajnadevam_to_parpola_crosswalk.csv"
)
OUTPUT = (
    REPO
    / "docs"
    / "research"
    / "pred-2026-011-registration"
    / "derivation-record.json"
)

DRAFT_DATE = "2026-10-20"
STATUS = "DRAFT_NOT_REGISTERED"


def _load_pred010():
    spec = importlib.util.spec_from_file_location(
        "pred010_register_derivation", PRED010_SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _parse_top3(value: str) -> list[str]:
    signs = []
    for item in value.split("|"):
        item = item.strip()
        if item:
            signs.append(item.rsplit(":", 1)[0].strip())
    return signs


def _screen(initial: list[str], rows: list[dict]) -> dict:
    best_matches: dict[str, list[dict]] = defaultdict(list)
    top3_appearances: dict[str, list[dict]] = defaultdict(list)

    for row in rows:
        glyph = row["registry_sign_id_yajnadevam"]
        best_sign = row["best_parpola_match"]
        best_matches[best_sign].append(
            {
                "yajnadevam_glyph": glyph,
                "match_confidence": row["match_confidence"],
                "match_count": row["match_count"],
                "total_alignments": row["total_alignments"],
                "review_status": row["review_status"],
            }
        )
        for sign in _parse_top3(row["top3_parpola"]):
            top3_appearances[sign].append(
                {
                    "yajnadevam_glyph": glyph,
                    "best_parpola_match": best_sign,
                }
            )

    counterparts = {
        sign: sorted(
            best_matches.get(sign, []),
            key=lambda match: match["yajnadevam_glyph"],
        )
        for sign in initial
    }
    trained = [sign for sign in initial if counterparts[sign]]
    excluded = []
    for sign in initial:
        if not counterparts[sign]:
            excluded.append(
                {
                    "sign": sign,
                    "reason": (
                        "No crosswalk row names this sign as "
                        "best_parpola_match. It appears only in "
                        "top3_parpola alternatives, which do not "
                        "establish a counterpart under the frozen "
                        "Phase-396 reading."
                    ),
                    "top3_only_appearances": sorted(
                        top3_appearances.get(sign, []),
                        key=lambda row: row["yajnadevam_glyph"],
                    ),
                }
            )

    return {
        "rule": (
            "A sign is eligible only if at least one row in the "
            "frozen crosswalk names it as best_parpola_match. "
            "top3_parpola appearances never establish eligibility."
        ),
        "screening_input": {
            "file": "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv",
            "file_sha256": None,  # Filled by derive() after hash check.
        },
        "counterparts_by_underlying_initial_sign": counterparts,
        "excluded_signs": excluded,
        "trained_initial_set": trained,
        "trained_initial_set_size": len(trained),
    }


def derive() -> dict:
    pred010 = _load_pred010()
    base = pred010.derive()
    committed_base = json.loads(PRED010_RECORD.read_text(encoding="utf-8"))
    if base != committed_base:
        raise SystemExit(
            "Recomputed PRED-2026-010 derivation differs from "
            "reports/pred010_derivation_record.json; "
            "PRED-2026-011 derivation closed."
        )

    crosswalk_sha256 = pred010.p396.sha256_file(CROSSWALK_CSV)
    if crosswalk_sha256 != pred010.PINNED_CROSSWALK_SHA256:
        raise SystemExit(
            "Crosswalk hash differs from the PRED-2026-010 pin; "
            "PRED-2026-011 derivation closed."
        )

    with open(CROSSWALK_CSV, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    initial = base["result"]["trained_initial_set"]
    screen = _screen(initial, rows)
    screen["screening_input"]["file_sha256"] = crosswalk_sha256

    trained_size = screen["trained_initial_set_size"]
    possible_shares = [
        float(Fraction(count, trained_size)) for count in range(trained_size + 1)
    ]
    minimum_passing = next(
        count
        for count in range(trained_size + 1)
        if Fraction(count, trained_size) >= Fraction(7, 10)
    )

    return {
        "prediction": "PRED-2026-011",
        "status": STATUS,
        "draft_date": DRAFT_DATE,
        "purpose": (
            "Draft registration derivation only: derive the proposed "
            "trained INITIAL set for PRED-2026-011 after the disclosed "
            "mappability screen. No registration, scoring, Harappa "
            "counting, or start-rate computation runs here."
        ),
        "owner_order": (
            "2026-10-20 — draft the successor under the adopted "
            "recommendation; filing awaits a separate registration order."
        ),
        "basis": {
            "predecessor": "PRED-2026-010",
            "basis_record": "reports/pred010_derivation_record.json",
            "basis_record_sha256": pred010.p396.sha256_file(PRED010_RECORD),
            "basis_script": "backend/scripts/pred010_register_derivation.py",
            "basis_script_sha256": pred010.p396.sha256_file(PRED010_SCRIPT),
            "classification_logic": base["logic"],
            "recomputation_matches_pred010_record": True,
        },
        "training_pool": base["training_pool"],
        "withheld_data_fixed_by_reference": base[
            "withheld_data_fixed_by_reference"
        ],
        "crosswalk_fixed_by_reference": base["crosswalk_fixed_by_reference"],
        "underlying_classification": {
            "classifiable_signs": base["result"]["classifiable_signs"],
            "class_counts": base["result"]["class_counts"],
            "classes": base["result"]["classes"],
            "unscreened_initial_set": initial,
            "unscreened_initial_set_size": len(initial),
        },
        "mappability_screen": screen,
        "criterion_arithmetic": {
            "denominator": trained_size,
            "share_threshold": 0.7,
            "start_rate_threshold": 0.4,
            "possible_shares": possible_shares,
            "minimum_passing_signs": minimum_passing,
            "plain_language": (
                f"With {trained_size} trained signs, the 70% bar passes "
                f"only at {minimum_passing} of {trained_size}."
            ),
        },
        "disclosures": [
            (
                "The mappability screen is a design change from "
                "PRED-2026-010 and is disclosed before registration."
            ),
            (
                "The screen used only the public, hash-pinned crosswalk. "
                "No Harappa inscription rows, sequences, occurrence "
                "counts, or start rates informed this derivation."
            ),
            (
                "Cleanliness means verified training-pool exclusion, "
                "not analyst blindness. The Harappa pool was previously "
                "inspected in aggregate during the Spec 032 closure "
                "audit, as disclosed for PRED-2026-010."
            ),
            (
                "This is a two-sign test. A pass would concern only "
                "P217 and P324 under the registered computation; it "
                "would not validate the INITIAL class as a whole."
            ),
        ],
        "attestation": (
            "No Harappa counting ran in this derivation. The withheld "
            "file was byte-hashed only by the imported PRED-2026-010 "
            "derivation; the only inscription sequences tokenised were "
            "the 179 CISI Mohenjo-daro inscriptions in the training "
            "pool. The crosswalk was opened because it is the public "
            "screening input."
        ),
    }


def main() -> int:
    record = derive()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    screen = record["mappability_screen"]
    print(f"PRED-2026-011 draft derivation: {OUTPUT}")
    print(
        "Underlying INITIAL set: "
        f"{record['underlying_classification']['unscreened_initial_set']}"
    )
    print(
        "Screened trained INITIAL set "
        f"({screen['trained_initial_set_size']}): "
        f"{screen['trained_initial_set']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
