"""Phase-128 — integrated evidence dossiers for the 44
``pending_non_sa_validation`` anchors.

Joins, on sign identity (M-number), every Phase-120–127 source
that carries a per-sign record for the pending subset:

- the anchor record itself
  (``backend/reports/INDUS_FINAL_ANCHORS.json``, read-only);
- Phase-120 Bhaskar triage (``reports/phase120_bhaskar_triage_44.json``);
- Phase-123 Wells segmentation witness
  (``data/crosswalks/wells_segmentation_witness_v1.json``), with the
  Phase-126 class vocabulary applied as a pure label normalisation
  (``reports/phase126_wells_split_candidates_results.json`` records
  carry ``witness_treatment_raw`` -> ``wells_treatment``; Phase-126's
  own analysis set was the 113 CANDIDATE anchors, so no Phase-126
  record exists for a pending sign — the field is labelled as a
  normalisation, never as a Phase-126 record);
- Phase-122 Parpola<->Mahadevan crosswalk v1
  (``data/crosswalks/parpola_mahadevan_crosswalk_v1.json``), every
  row asserted for the anchor's M-sign;
- Phase-125 cross-compilation PRIMARY arm
  (``reports/phase125_cross_compilation_results.json``): per-sign
  record and judgeability;
- Phase-127 diagnostic
  (``reports/phase127_cross_compilation_diagnostic_results.json``):
  per-pair values exist only for the 16 Phase-125 PRIMARY judgeable
  pairs;
- spec 020 limitation (uniform field, not per-sign evidence): the
  Soviet positional dataset was adjudicated non-qualifying as an
  evaluation source, so no Soviet-route evaluation of these
  anchors' predictions exists or can be produced from it.

Where a join key is missing, the field is recorded as
``NOT-COVERED`` / missing — never inferred. This module is
descriptive only: it issues no status recommendation, no
adjudication, and no prediction content.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

EXPECTED_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)
PENDING_STATUS = "pending_non_sa_validation"
NOT_COVERED = "NOT-COVERED"

# Phase-126 label vocabulary (records[].wells_treatment) as a pure
# normalisation of the Phase-123 raw treatment
# (records[].witness_treatment_raw).
PHASE126_CLASS_MAP = {
    "SAME": "unit-same",
    "SPLIT": "split",
    "MERGE": "merge",
    "NOT-COVERED": "not-covered",
    "INDETERMINATE": "indeterminate",
}

WELLS_DETERMINATE = {"SAME", "SPLIT", "MERGE"}

SOVIET_LIMITATION = {
    "value": "NOT-EVALUABLE-VIA-SOVIET-DATASET",
    "note": (
        "Uniform limitation (not per-sign evidence): spec 020 "
        "adjudicated the Soviet positional dataset (Phase-121, "
        "Kondratov 1965) non-qualifying as an evaluation source "
        "for PRED-2026-001/002 (verdict NO, spec.md section 5); "
        "the Soviet route therefore cannot evaluate these "
        "anchors' predictions."
    ),
    "provenance": "specs/020-soviet-pred-adjudication/spec.md §5",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pending_anchor_ids(anchors_doc: dict) -> list[str]:
    """The dossier universe: exactly the anchors whose
    validation_status is pending_non_sa_validation, sorted."""
    return sorted(
        sign
        for sign, rec in anchors_doc["anchors"].items()
        if rec.get("validation_status") == PENDING_STATUS
    )


def phase126_class(raw_treatment: str | None) -> str | None:
    if raw_treatment is None:
        return None
    return PHASE126_CLASS_MAP.get(raw_treatment)


# ── Bucket rules ──────────────────────────────────────────────
# Deterministic predicates over dossier fields. Rules are stated
# in reports/phase128_evidence_dossiers_44.md BEFORE the
# membership lists and mirror this code exactly.
#
# Derived per-anchor predicates:
#   wells_determinate  wells treatment in {SAME, SPLIT, MERGE}
#   wells_contested    wells treatment in {SPLIT, MERGE} OR
#                      wells verification == "discrepancy"
#   cw_present         >= 1 crosswalk v1 row for the M-sign
#   cw_conflict        any crosswalk v1 row has conflict == true
#   p125_present       sign appears in Phase-125 PRIMARY records
#   p127_present       sign is the M-side of one of the 16
#                      Phase-125 PRIMARY judgeable pairs (a
#                      Phase-127 per-pair record exists)
#
# Buckets 1-4 are independent predicates: an anchor may sit in
# several of them at once. Bucket 5 (evidence-thin) is the
# defined residual: anchors in NONE of buckets 1-4. An anchor is
# therefore in evidence-thin XOR at least one of buckets 1-4.

def classify_buckets(f: dict) -> list[str]:
    """f carries the derived predicates above plus
    bhaskar_classification and wells_treatment."""
    out: list[str] = []
    if (
        f["wells_determinate"]
        and f["cw_present"]
        and f["p125_present"]
        and f["p127_present"]
    ):
        out.append("evidence-complete")
    if f["wells_contested"]:
        out.append("segmentation-contested")
    if f["cw_conflict"]:
        out.append("crosswalk-contested")
    if (
        f["bhaskar_classification"] == NOT_COVERED
        and f["wells_treatment"] in (NOT_COVERED, "INDETERMINATE")
        and not f["p125_present"]
        and not f["p127_present"]
    ):
        out.append("not-covered")
    if not out:
        out.append("evidence-thin")
    return out


def derived_predicates(dossier: dict) -> dict:
    wells = dossier["wells_phase123"]
    treatment = wells.get("treatment") if isinstance(wells, dict) else None
    verification = wells.get("verification") if isinstance(wells, dict) else None
    cw = dossier["crosswalk_phase122"]
    p125 = dossier["phase125_cross_compilation"]
    p127 = dossier["phase127_diagnostic"]
    bh = dossier["bhaskar_phase120"]
    return {
        "bhaskar_classification": bh.get("classification")
        if isinstance(bh, dict)
        else None,
        "wells_treatment": treatment,
        "wells_determinate": treatment in WELLS_DETERMINATE,
        "wells_contested": treatment in ("SPLIT", "MERGE")
        or verification == "discrepancy",
        "cw_present": isinstance(cw, dict) and cw.get("n_rows", 0) >= 1,
        "cw_conflict": isinstance(cw, dict) and bool(cw.get("any_conflict")),
        "p125_present": isinstance(p125, dict)
        and p125.get("status") == "in_primary_records",
        "p127_present": isinstance(p127, dict)
        and p127.get("status") == "in_judgeable_pair_set",
    }


# ── Source loaders / join ─────────────────────────────────────

def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_dossiers(repo: Path) -> dict:
    anchors_path = repo / "backend/reports/INDUS_FINAL_ANCHORS.json"
    sha_before = sha256_file(anchors_path)
    if sha_before != EXPECTED_ANCHORS_SHA256:
        raise AssertionError(
            f"anchors sha256 drift: {sha_before} != {EXPECTED_ANCHORS_SHA256}"
        )
    anchors_doc = _load_json(anchors_path)
    ids = pending_anchor_ids(anchors_doc)

    bhaskar = _load_json(repo / "reports/phase120_bhaskar_triage_44.json")
    bh_by_sign = {r["sign"]: r for r in bhaskar["rows"]}

    wells = _load_json(repo / "data/crosswalks/wells_segmentation_witness_v1.json")
    wells_by_sign = {
        r["sign"]: r for r in wells["rows"] if r["anchor_set"] == PENDING_STATUS
    }

    crosswalk = _load_json(
        repo / "data/crosswalks/parpola_mahadevan_crosswalk_v1.json"
    )
    cw_by_m: dict[str, list[dict]] = {}
    for row in crosswalk["rows"]:
        cw_by_m.setdefault(row["mahadevan_id"], []).append(row)

    p125 = _load_json(repo / "reports/phase125_cross_compilation_results.json")
    p125_by_m = {r["mahadevan_id"]: r for r in p125["arms"]["primary"]["records"]}

    p127 = _load_json(
        repo / "reports/phase127_cross_compilation_diagnostic_results.json"
    )
    boot = p127["arms"]["c_bootstrap"]["per_pair"]
    split_half = p127["arms"]["a_split_half"]["per_sign"]
    matched = p127["arms"]["b_matched_size"]["per_sign"]
    decomp = {
        (r["parpola_id"], r["mahadevan_id"]): r
        for r in p127["arms"]["d_crosswalk_decomposition"]["records"]
    }
    p127_by_m: dict[str, dict] = {}
    for pair_key, vals in boot.items():
        parpola_id, mahadevan_id = pair_key.split("-", 1)
        p127_by_m[mahadevan_id] = {
            "status": "in_judgeable_pair_set",
            "pair_key": pair_key,
            "parpola_id": parpola_id,
            "bootstrap_ci": vals,
            "split_half": split_half.get(pair_key),
            "matched_size_per_sign": matched.get(pair_key),
            "crosswalk_decomposition": decomp.get((parpola_id, mahadevan_id)),
            "provenance": (
                "reports/phase127_cross_compilation_diagnostic_results.json "
                f"arms.c_bootstrap.per_pair[{pair_key!r}] (+ arms a/b/d "
                "same pair key)"
            ),
        }

    dossiers: list[dict] = []
    for sign in ids:
        rec = anchors_doc["anchors"][sign]
        d: dict = {
            "anchor_id": sign,
            "sign_number": int(sign[1:]),
            "anchor": {
                **rec,
                "provenance": (
                    "backend/reports/INDUS_FINAL_ANCHORS.json "
                    f"anchors.{sign}"
                ),
            },
        }

        bh = bh_by_sign.get(sign)
        if bh is None:
            d["bhaskar_phase120"] = {
                "status": NOT_COVERED,
                "provenance": (
                    "reports/phase120_bhaskar_triage_44.json — no row "
                    f"for {sign}"
                ),
            }
        else:
            d["bhaskar_phase120"] = {
                **bh,
                "provenance": (
                    "reports/phase120_bhaskar_triage_44.json "
                    f"rows[sign={sign}]"
                ),
            }

        w = wells_by_sign.get(sign)
        if w is None:
            d["wells_phase123"] = {
                "status": NOT_COVERED,
                "provenance": (
                    "data/crosswalks/wells_segmentation_witness_v1.json "
                    f"— no pending row for {sign}"
                ),
            }
            d["wells_phase126_class"] = {
                "status": NOT_COVERED,
                "provenance": "no Phase-123 raw treatment to normalise",
            }
        else:
            d["wells_phase123"] = {
                **w,
                "verification": w.get("verification") or None,
                "note": w.get("note") or None,
                "provenance": (
                    "data/crosswalks/wells_segmentation_witness_v1.json "
                    f"rows[sign={sign}, anchor_set={PENDING_STATUS}]"
                ),
            }
            d["wells_phase126_class"] = {
                "class": phase126_class(w["treatment"]),
                "raw_treatment": w["treatment"],
                "provenance": (
                    "Phase-126 label vocabulary (reports/"
                    "phase126_wells_split_candidates_results.json "
                    "records[].wells_treatment vs witness_treatment_raw) "
                    "applied to the Phase-123 raw treatment; Phase-126's "
                    "own analysis set was the 113 CANDIDATE anchors "
                    "(pending excluded), so this is a normalisation, "
                    "not a Phase-126 record"
                ),
            }

        rows = sorted(
            cw_by_m.get(sign, []), key=lambda r: r["parpola_id"]
        )
        if not rows:
            d["crosswalk_phase122"] = {
                "status": NOT_COVERED,
                "n_rows": 0,
                "parpola_ids": [],
                "rows": [],
                "any_conflict": False,
                "provenance": (
                    "data/crosswalks/parpola_mahadevan_crosswalk_v1.json "
                    f"— no row asserts mahadevan_id={sign}"
                ),
            }
        else:
            d["crosswalk_phase122"] = {
                "status": "mapped",
                "n_rows": len(rows),
                "parpola_ids": [r["parpola_id"] for r in rows],
                "confidences": sorted({r["confidence"] for r in rows}),
                "relation_types": sorted({r["relation_type"] for r in rows}),
                "any_conflict": any(r["conflict"] for r in rows),
                "rows": rows,
                "provenance": (
                    "data/crosswalks/parpola_mahadevan_crosswalk_v1.json "
                    f"rows[mahadevan_id={sign}]"
                ),
            }

        r125 = p125_by_m.get(sign)
        if r125 is None:
            d["phase125_cross_compilation"] = {
                "status": NOT_COVERED,
                "record": None,
                "provenance": (
                    "reports/phase125_cross_compilation_results.json "
                    "arms.primary.records — no record with "
                    f"mahadevan_id={sign} (PRIMARY arm carries only "
                    "high-confidence crosswalk pairs)"
                ),
            }
        else:
            d["phase125_cross_compilation"] = {
                "status": "in_primary_records",
                "judgeable": r125["judgeable"],
                "record": r125,
                "provenance": (
                    "reports/phase125_cross_compilation_results.json "
                    f"arms.primary.records[mahadevan_id={sign}]"
                ),
            }

        d["phase127_diagnostic"] = p127_by_m.get(
            sign,
            {
                "status": NOT_COVERED,
                "provenance": (
                    "reports/phase127_cross_compilation_diagnostic_"
                    "results.json — per-pair values exist only for "
                    "the 16 Phase-125 PRIMARY judgeable pairs; "
                    f"{sign} is not the M-side of any of them"
                ),
            },
        )

        d["soviet_spec020_limitation"] = dict(SOVIET_LIMITATION)
        d["buckets"] = classify_buckets(derived_predicates(d))
        dossiers.append(d)

    buckets: dict[str, list[str]] = {}
    for d in dossiers:
        for b in d["buckets"]:
            buckets.setdefault(b, []).append(d["anchor_id"])

    sha_after = sha256_file(anchors_path)
    return {
        "phase": 128,
        "title": (
            "Integrated evidence dossiers for the 44 "
            "pending_non_sa_validation anchors"
        ),
        "date": "2026-10-08",
        "framing": (
            "Descriptive join only. No status recommendation, no "
            "adjudication, no prediction (PRED) content. Missing "
            "join keys are recorded as NOT-COVERED, never inferred."
        ),
        "anchors_file": "backend/reports/INDUS_FINAL_ANCHORS.json",
        "anchors_sha256_before": sha_before,
        "anchors_sha256_after": sha_after,
        "anchors_unchanged": sha_before == sha_after,
        "n_dossiers": len(dossiers),
        "sources": {
            "bhaskar_phase120": "reports/phase120_bhaskar_triage_44.json",
            "wells_phase123": "data/crosswalks/wells_segmentation_witness_v1.json",
            "wells_phase126_class": (
                "reports/phase126_wells_split_candidates_results.json "
                "(label vocabulary only; analysis set excluded pending)"
            ),
            "crosswalk_phase122": (
                "data/crosswalks/parpola_mahadevan_crosswalk_v1.json"
            ),
            "phase125": "reports/phase125_cross_compilation_results.json",
            "phase127": (
                "reports/phase127_cross_compilation_diagnostic_results.json"
            ),
            "soviet_spec020_limitation": (
                "specs/020-soviet-pred-adjudication/spec.md §5"
            ),
        },
        "phase127_global": {
            "matched_size_median_tv_distribution": p127["arms"][
                "b_matched_size"
            ]["median_tv_distribution"],
            "bootstrap_median_tv": p127["arms"]["c_bootstrap"]["median_tv"],
            "noise_floor_median_tv": p127["arms"]["a_split_half"][
                "noise_floor_median_tv"
            ],
            "noise_floor_fullsize_est": p127["arms"]["a_split_half"][
                "noise_floor_fullsize_est"
            ],
            "phase125_verdict_of_record": p127["phase125_verdict_of_record"],
            "provenance": (
                "reports/phase127_cross_compilation_diagnostic_results.json "
                "arms a/b/c + phase125_verdict_of_record (global values, "
                "identical for every dossier; recorded once here)"
            ),
        },
        "phase125_global": {
            "primary_stats": p125["arms"]["primary"]["stats"],
            "verdict": p125["verdict"],
            "provenance": (
                "reports/phase125_cross_compilation_results.json "
                "arms.primary.stats + verdict"
            ),
        },
        "bucket_rules": {
            "evidence-complete": (
                "wells_determinate AND cw_present AND p125_present "
                "AND p127_present"
            ),
            "segmentation-contested": (
                "wells treatment in {SPLIT, MERGE} OR wells "
                "verification == 'discrepancy'"
            ),
            "crosswalk-contested": (
                "any crosswalk v1 row for the M-sign has "
                "conflict == true"
            ),
            "not-covered": (
                "bhaskar classification == NOT-COVERED AND wells "
                "treatment in {NOT-COVERED, INDETERMINATE} AND NOT "
                "p125_present AND NOT p127_present"
            ),
            "evidence-thin": (
                "residual: in none of the four buckets above"
            ),
            "multi_membership": (
                "Buckets 1-4 are independent predicates and may "
                "overlap; evidence-thin is the defined residual and "
                "is exclusive of buckets 1-4 by construction."
            ),
        },
        "buckets": dict(sorted(buckets.items())),
        "bucket_counts": {k: len(v) for k, v in sorted(buckets.items())},
        "dossiers": dossiers,
    }
