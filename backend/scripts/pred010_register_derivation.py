"""PRED-2026-010 — registration derivation (2026-10-13).

Successor to PRED-2026-006, which Spec 032 / Phase-396
closed at step 0 as CANNOT BE RUN AS WRITTEN (unscored):
the recorded `global_class_stability` classification had
been trained on the combined corpus
(`data/normalized/corpus_master.csv` — 179 CISI
Mohenjo-daro inscriptions plus 2,543 Yajnadevam), so the
"withheld" Harappa Yajnadevam data sat inside the
training pool (step-0 record:
`reports/phase396_results.json`, sha256
`26781336c8c34b006e62474448b17be4d895c1d7ea06d5c24418d49a38e7c4e7`).

This script performs the registration derivation for the
successor, and nothing else:

  * the classification logic is the recorded logic,
    imported unchanged from the frozen Phase-396 build
    (`backend/scripts/phase396_pred006_step0.py`), which
    carries it verbatim from
    `scripts/global_class_stability.py` and proved the
    carry by exact reproduction in Phase-396 check 3.1;
  * the training pool is that same corpus file, filtered
    to its CISI component only — source "Corpus of
    Indus Seals and Inscriptions (mayig digitization)",
    179 inscriptions, all Mohenjo-daro, zero Yajnadevam
    rows. No Yajnadevam sequence is tokenised anywhere
    in this derivation;
  * the input file's SHA-256 must equal the hash the
    Phase-396 step-0 record pinned for it — byte
    identity with the input Phase-396 verified is what
    carries the "verbatim" claim here, so a changed
    corpus fails this derivation closed;
  * the withheld file
    (`backend/glossa_lab/data/yajnadevam_inscriptions.csv`)
    and the crosswalk
    (`data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`)
    are byte-hashed only — fixed by reference for the
    future scoring. Neither is opened for content, and
    no Harappa start rate is computed for any sign.

Output: `reports/pred010_derivation_record.json` — the
derived trained INITIAL set, the pool identity (file
hash + filtered-pool manifest hash), and the comparison
against PRED-2026-006's recorded 12 signs. Registration
work only: no scoring runs here, now or later; scoring
is a separate, future, owner-ordered act under the
registered contract.
"""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# The frozen Phase-396 build carries the recorded
# classification logic verbatim; import it unchanged so
# this derivation runs the very code Phase-396 verified.
_spec = importlib.util.spec_from_file_location(
    "phase396_pred006_step0",
    REPO / "backend" / "scripts" / "phase396_pred006_step0.py",
)
p396 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p396)

CORPUS_MASTER = REPO / "data" / "normalized" / "corpus_master.csv"
CROSSWALK_CSV = REPO / "data" / "crosswalks" / "yajnadevam_to_parpola_crosswalk.csv"
WITHHELD_CSV = (
    REPO / "backend" / "glossa_lab" / "data" / "yajnadevam_inscriptions.csv"
)
RECORDED_SCRIPT = REPO / "scripts" / "global_class_stability.py"
DERIVATION_RECORD = REPO / "reports" / "pred010_derivation_record.json"

CISI_SOURCE = "Corpus of Indus Seals and Inscriptions (mayig digitization)"

# Hashes pinned by the Phase-396 step-0 record
# (reports/phase396_results.json). Byte identity with
# those inputs is a precondition of this derivation.
PINNED_CORPUS_SHA256 = (
    "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
)
PINNED_CROSSWALK_SHA256 = (
    "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
)
PINNED_WITHHELD_SHA256 = (
    "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
)

# PRED-2026-006's trained INITIAL set, as frozen by
# Phase-396 check 3.1 — comparison material only.
PRED006_TRAINED_INITIAL = [
    "P000", "P001", "P004", "P013", "P051", "P098",
    "P217", "P238", "P265", "P301", "P310", "P324",
]


def derive() -> dict:
    corpus_sha256 = p396.sha256_file(CORPUS_MASTER)
    if corpus_sha256 != PINNED_CORPUS_SHA256:
        raise SystemExit(
            "corpus_master.csv hash differs from the Phase-396 "
            "step-0 pin; the verbatim carry cannot be asserted. "
            "Derivation closed."
        )
    records = p396.load_corpus_master()
    pool = [r for r in records if r["source_name"] == CISI_SOURCE]
    if not pool:
        raise SystemExit("CISI pool is empty; derivation closed.")
    if any(r["source_name"].startswith("Yajnadevam") for r in pool):
        raise SystemExit("Yajnadevam row inside the pool; derivation closed.")
    pool_sites = Counter(r["site"] for r in pool)
    if set(pool_sites) != {"Mohenjo-daro"}:
        raise SystemExit(
            f"CISI pool is not Mohenjo-daro only: {dict(pool_sites)}; "
            "derivation closed."
        )
    classes = p396.recompute_global_classes(pool)
    initial = sorted(s for s, c in classes.items() if c == "INITIAL")
    class_counts = Counter(classes.values())
    return {
        "prediction": "PRED-2026-010",
        "derivation_date": "2026-10-13",
        "purpose": (
            "Registration derivation only: derive and freeze the "
            "trained INITIAL set for PRED-2026-010 from a training "
            "pool that excludes the withheld corpus by construction. "
            "No scoring; no Harappa start rate computed for any sign."
        ),
        "logic": {
            "source": (
                "scripts/global_class_stability.py (recorded run of "
                "2026-04-22T18:16:22Z), carried verbatim in "
                "backend/scripts/phase396_pred006_step0.py and "
                "imported unchanged from that frozen build"
            ),
            "recorded_script_sha256": p396.sha256_file(RECORDED_SCRIPT),
            "min_freq_global": p396.MIN_FREQ_GLOBAL,
            "rule": (
                "INSUFFICIENT_DATA if freq < 10; TERMINAL if end_rate "
                ">= 0.55; INITIAL if start_rate >= 0.55; MEDIAL if "
                "internal_rate >= 0.70; BIMODAL if start_rate >= 0.30 "
                "and end_rate >= 0.30 and internal_rate < 0.30; "
                "otherwise MIXED"
            ),
            "verbatim_carry_basis": (
                "Phase-396 check 3.1 recomputed the recorded "
                "classification with this code over the recorded "
                "training corpus and reproduced the recorded output "
                "exactly (105 classifiable signs, no differences). "
                "This derivation runs the same code object on the "
                "same input file, whose SHA-256 equals the Phase-396 "
                "step-0 pin."
            ),
        },
        "training_pool": {
            "file": "data/normalized/corpus_master.csv",
            "file_sha256": corpus_sha256,
            "filter": f'source_name == "{CISI_SOURCE}"',
            "corpus_rows_total": len(records),
            "pool_rows": len(pool),
            "pool_sites": dict(pool_sites),
            "yajnadevam_rows_in_pool": 0,
            "pool_manifest_sha256": p396.sha256_json(pool),
        },
        "withheld_data_fixed_by_reference": {
            "file": "backend/glossa_lab/data/yajnadevam_inscriptions.csv",
            "file_sha256": p396.sha256_file(WITHHELD_CSV),
            "treatment": (
                "byte-hashed only; not opened for content in this "
                "derivation; the Harappa subset is the scoring pool "
                "under the registered contract"
            ),
        },
        "crosswalk_fixed_by_reference": {
            "file": "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv",
            "file_sha256": p396.sha256_file(CROSSWALK_CSV),
        },
        "result": {
            "classifiable_signs": len(classes),
            "class_counts": dict(sorted(class_counts.items())),
            "classes": dict(sorted(classes.items())),
            "trained_initial_set": initial,
            "trained_initial_set_size": len(initial),
        },
        "comparison_to_pred_2026_006": {
            "pred006_trained_initial_set": PRED006_TRAINED_INITIAL,
            "pred006_trained_initial_set_size": len(PRED006_TRAINED_INITIAL),
            "shared": sorted(set(initial) & set(PRED006_TRAINED_INITIAL)),
            "only_in_pred010_pool": sorted(
                set(initial) - set(PRED006_TRAINED_INITIAL)
            ),
            "only_in_pred006_combined_pool": sorted(
                set(PRED006_TRAINED_INITIAL) - set(initial)
            ),
        },
        "attestation": (
            "No Harappa counting ran in this derivation: the "
            "withheld file was byte-hashed only, the crosswalk was "
            "byte-hashed only, and the only sequences tokenised "
            "were the 179 CISI Mohenjo-daro inscriptions of the "
            "training pool."
        ),
    }


def main() -> int:
    record = derive()
    DERIVATION_RECORD.write_text(
        json.dumps(record, indent=2, sort_keys=True), encoding="utf-8"
    )
    result = record["result"]
    print(f"PRED-2026-010 registration derivation: {DERIVATION_RECORD}")
    print(
        f"Pool: {record['training_pool']['pool_rows']} CISI rows, "
        f"sites {record['training_pool']['pool_sites']}"
    )
    print(
        f"Classifiable: {result['classifiable_signs']}; "
        f"class counts {result['class_counts']}"
    )
    print(
        f"Trained INITIAL set ({result['trained_initial_set_size']}): "
        f"{result['trained_initial_set']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
