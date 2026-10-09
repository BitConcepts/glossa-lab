"""Phase-128 runner: builds the dossiers document and renders
``reports/phase128_evidence_dossiers_44.json``,
``reports/phase128_evidence_dossiers_44.csv`` and the synthesis
report ``reports/phase128_evidence_dossiers_44.md``.

Descriptive only — see glossa_lab/phase128_dossiers.py.
"""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path

from .phase128_dossiers import build_dossiers

BUCKET_ORDER = [
    "evidence-complete",
    "evidence-thin",
    "segmentation-contested",
    "crosswalk-contested",
    "not-covered",
]


def _join(vals) -> str:
    return ";".join(str(v) for v in vals)


def dossier_csv_rows(doc: dict) -> list[dict]:
    rows: list[dict] = []
    for d in doc["dossiers"]:
        bh = d["bhaskar_phase120"]
        w = d["wells_phase123"]
        cw = d["crosswalk_phase122"]
        p125 = d["phase125_cross_compilation"]
        p127 = d["phase127_diagnostic"]
        rec125 = p125.get("record") or {}
        rows.append(
            {
                "anchor_id": d["anchor_id"],
                "sign_number": d["sign_number"],
                "reading": d["anchor"].get("reading"),
                "anchor_confidence": d["anchor"].get("confidence"),
                "validation_status": d["anchor"].get("validation_status"),
                "bhaskar_classification": bh.get("classification")
                or bh.get("status"),
                "bhaskar_subflag": bh.get("subflag") or "",
                "bhaskar_case_ids": _join(bh.get("case_ids") or []),
                "wells_treatment": w.get("treatment") or w.get("status"),
                "wells_graphemes": w.get("wells_graphemes") or "",
                "wells_correspondence_method": w.get(
                    "correspondence_method"
                )
                or "",
                "wells_verification": w.get("verification") or "",
                "phase126_wells_class": d["wells_phase126_class"].get(
                    "class"
                )
                or d["wells_phase126_class"].get("status"),
                "crosswalk_status": cw.get("status"),
                "crosswalk_n_rows": cw.get("n_rows"),
                "crosswalk_parpola_ids": _join(cw.get("parpola_ids") or []),
                "crosswalk_confidences": _join(cw.get("confidences") or []),
                "crosswalk_relation_types": _join(
                    cw.get("relation_types") or []
                ),
                "crosswalk_any_conflict": cw.get("any_conflict"),
                "phase125_status": p125.get("status"),
                "phase125_parpola_id": rec125.get("parpola_id") or "",
                "phase125_judgeable": rec125.get("judgeable")
                if rec125
                else "",
                "phase125_tv": rec125.get("tv")
                if rec125.get("tv") is not None
                else "",
                "phase125_mayig_n": rec125.get("mayig_n")
                if rec125
                else "",
                "phase125_holdat_n": rec125.get("holdat_n")
                if rec125
                else "",
                "phase127_status": p127.get("status"),
                "phase127_pair_key": p127.get("pair_key") or "",
                "phase127_bootstrap_ci95_lo": (
                    p127.get("bootstrap_ci") or {}
                ).get("ci95_lo", ""),
                "phase127_bootstrap_ci95_hi": (
                    p127.get("bootstrap_ci") or {}
                ).get("ci95_hi", ""),
                "soviet_spec020_limitation": d[
                    "soviet_spec020_limitation"
                ]["value"],
                "buckets": _join(d["buckets"]),
            }
        )
    return rows


def render_csv(doc: dict) -> str:
    rows = dossier_csv_rows(doc)
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf, fieldnames=list(rows[0].keys()), lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def render_report(doc: dict) -> str:
    b = doc["buckets"]
    counts = doc["bucket_counts"]
    g127 = doc["phase127_global"]
    dist = g127["matched_size_median_tv_distribution"]
    boot = g127["bootstrap_median_tv"]
    lines: list[str] = []
    a = lines.append
    a("# Phase-128 — Integrated Evidence Dossiers for the 44 Pending Anchors")
    a("")
    a("**Status:** descriptive synthesis. **Date:** 2026-10-08. **Phase:** 128.")
    a("")
    a(
        "**Framing (hard).** This report and its companion files join, per "
        "anchor, the Phase-120–127 evidence records that exist for the 44 "
        "`pending_non_sa_validation` anchors in "
        "`backend/reports/INDUS_FINAL_ANCHORS.json` (sha256 "
        f"`{doc['anchors_sha256_before']}`, read-only, unchanged). They are "
        "**descriptive only**: they contain no status recommendation, no "
        "adjudication, and no prediction (PRED) content. Where a source has "
        "no record for a sign, the dossier records the field as "
        "NOT-COVERED/missing; nothing is inferred to fill a gap."
    )
    a("")
    a("**Artifacts.**")
    a("")
    a("- Dossiers (JSON): `reports/phase128_evidence_dossiers_44.json`")
    a("- Dossiers (CSV, flat rendering): `reports/phase128_evidence_dossiers_44.csv`")
    a("- Builder: `backend/glossa_lab/phase128_dossiers.py` + `backend/glossa_lab/phase128_run.py`; entry `backend/scripts/phase128_evidence_dossiers.py`")
    a("- Tests: `backend/tests/test_phase128_evidence_dossiers.py`")
    a("")
    a("## 1. Sources joined (per anchor, on M-number)")
    a("")
    a("| Source | Per-sign content carried into the dossier |")
    a("|---|---|")
    a("| Anchor file | reading, confidence, basis, source, validation_status |")
    a("| Phase-120 Bhaskar triage (`reports/phase120_bhaskar_triage_44.{md,json}`) | classification (CONTESTED / NOT-COVERED), subflag, detail, mention sources, case ids |")
    a("| Phase-123 Wells witness (`data/crosswalks/wells_segmentation_witness_v1.*`; memo `reports/phase123_wells_segmentation_witness.md`) | treatment (SAME / SPLIT / MERGE / NOT-COVERED / INDETERMINATE), Wells graphemes, correspondence method, thesis source, hand-verification, implication note |")
    a("| Phase-126 (`reports/phase126_wells_split_candidates*`) | class vocabulary only (unit-same / split / merge / not-covered / indeterminate), applied as a label normalisation of the Phase-123 raw treatment; Phase-126's own analysis set was the 113 CANDIDATE anchors, so no Phase-126 record exists for any pending sign |")
    a("| Phase-122 crosswalk v1 (`data/crosswalks/parpola_mahadevan_crosswalk_v1.*`; memo `reports/phase122_crosswalk_mayig.md`) | every P↔M row asserted for the M-sign: Parpola id(s), relation type, confidence, conflict flag + detail, sources |")
    a("| Phase-125 (`reports/phase125_cross_compilation_results.json`) | PRIMARY-arm record per sign (paired Parpola id, token counts, profiles, TV/W1) and judgeability |")
    a("| Phase-127 (`reports/phase127_cross_compilation_diagnostic.md` + results JSON) | per-pair diagnostic values (bootstrap CI, split-half, matched-size, crosswalk decomposition) — these exist only for the 16 PRIMARY judgeable pairs; global diagnostic values are recorded once in the JSON (§4) |")
    a("| Spec 020 (`specs/020-soviet-pred-adjudication`) | uniform limitation field on every dossier (§5) |")
    a("")
    a("Join integrity: **44 anchors in = 44 dossiers out** (asserted in code "
      "and in tests). Crosswalk coverage: 43/44 signs have ≥1 crosswalk row "
      "(M281 has none and is recorded NOT-COVERED there). Phase-125 PRIMARY "
      "records exist for 36/44 signs (the PRIMARY arm carries only "
      "high-confidence crosswalk pairs); 8 signs are recorded NOT-COVERED "
      "for Phase-125.")
    a("")
    a("## 2. Bucket rules (stated before membership)")
    a("")
    a("Derived per-anchor predicates over the dossier fields:")
    a("")
    a("- `wells_determinate` — Wells treatment ∈ {SAME, SPLIT, MERGE}")
    a("- `wells_contested` — Wells treatment ∈ {SPLIT, MERGE} OR Wells hand-verification == `discrepancy`")
    a("- `cw_present` — ≥1 crosswalk v1 row for the M-sign")
    a("- `cw_conflict` — any crosswalk v1 row for the M-sign has conflict == true")
    a("- `p125_present` — the sign appears in the Phase-125 PRIMARY records")
    a("- `p127_present` — the sign is the M-side of one of the 16 Phase-125 PRIMARY judgeable pairs (a Phase-127 per-pair record exists)")
    a("")
    a("Rules:")
    a("")
    a("1. **evidence-complete** — `wells_determinate` AND `cw_present` AND `p125_present` AND `p127_present`.")
    a("2. **segmentation-contested** — `wells_contested`.")
    a("3. **crosswalk-contested** — `cw_conflict`.")
    a("4. **not-covered** — Bhaskar classification == NOT-COVERED AND Wells treatment ∈ {NOT-COVERED, INDETERMINATE} AND NOT `p125_present` AND NOT `p127_present`.")
    a("5. **evidence-thin** — the defined residual: in none of buckets 1–4.")
    a("")
    a("**Multi-membership (explicit).** Buckets 1–4 are independent "
      "predicates: an anchor may sit in several of them at once, and §3 "
      "lists it under each. Bucket 5 is exclusive of buckets 1–4 by "
      "construction (it is exactly the residual). Every anchor is in at "
      "least one bucket.")
    a("")
    a("## 3. Bucket membership (exact)")
    a("")
    for name in BUCKET_ORDER:
        members = b.get(name, [])
        a(f"### {name} — {counts.get(name, 0)}")
        a("")
        a(", ".join(members) if members else "_(none)_")
        a("")
    a("## 4. Phase-127 diagnostic weight (global, recorded once)")
    a("")
    a(
        "The Phase-127 diagnostic is a property of the 16-pair judgeable "
        "set, not of individual pending anchors (only one pending anchor, "
        "M072, is in that set). Its global findings, carried into the JSON "
        "dossiers document verbatim: matched-size sampling at mayig token "
        f"counts gives an expected median TV of {dist['median']} "
        f"(95% {dist['ci95_lo']}–{dist['ci95_hi']}); "
        f"{dist['share_replicates_ge_observed']} of "
        f"{dist['n_replicates']} replicates reach the observed Phase-125 "
        f"median TV of {dist['observed_median_tv']} — matched-size "
        "sampling explains ~0 of the observed median TV. The inscription-"
        f"bootstrap 95% CI for the median TV is {boot['ci95_lo']}–"
        f"{boot['ci95_hi']}. The Holdat split-half noise floor is "
        f"{g127['noise_floor_median_tv']} (full-size estimate "
        f"{g127['noise_floor_fullsize_est']}). The Phase-125 verdict of "
        "record (FAIL — DISAGREEMENT) is final and unchanged by "
        "Phase-127 and by this phase."
    )
    a("")
    a("## 5. The spec-020 limitation (uniform field)")
    a("")
    a(
        "Every dossier carries the same limitation field: "
        "`NOT-EVALUABLE-VIA-SOVIET-DATASET`. Spec 020 adjudicated the "
        "Soviet positional dataset (Phase-121, Kondratov 1965) "
        "non-qualifying as an evaluation source for PRED-2026-001/002 "
        "(verdict NO, spec.md §5). The Soviet route therefore cannot "
        "evaluate these anchors' predictions. This is recorded as a "
        "uniform limitation on the dossier set, not as per-sign evidence "
        "about any anchor."
    )
    a("")
    a("## 6. What this dossier cannot do")
    a("")
    a(
        "- **Bhaskar covers 1 of 44.** The Phase-120 triage records 43 of "
        "the 44 anchors as NOT-COVERED by Bhaskar (2024); only M402 "
        "carries a documented contest (case BH-D10, a coverage gap: the "
        "left-waving frontal form on K-39 has no counterpart in any "
        "compilation's inventory of 402). For the other 43, the dossier "
        "records an absence, not a concordance — the triage never infers "
        "agreement from silent use."
    )
    a(
        "- **The Phase-125 judgeable subset is small.** Of 286 PRIMARY "
        "cross-compilation pairs, 16 are judgeable; of the 44 pending "
        "anchors, exactly one (M072, paired P058) is among them. For the "
        "other 43 anchors there is no judgeable cross-compilation "
        "measurement, and the dossier manufactures none."
    )
    a(
        "- **The Soviet route is closed.** Per spec 020 (§5 above), the "
        "one additional evaluation source examined by this program cannot "
        "evaluate these anchors' predictions."
    )
    a(
        "- **A dossier is not a verdict.** These files assemble what each "
        "source records about each sign, with provenance. They weigh "
        "nothing against anything else, and no anchor's status, reading, "
        "or confidence is changed, recommended, or implied by anything "
        "here."
    )
    a("")
    a(
        "**AI disclosure:** executed by an AI agent (Muse Spark, via "
        "Muse) at the direction of Tristen Pierson, per "
        "constitution §VI."
    )
    a("")
    return "\n".join(lines)


def run_all(repo: Path | None = None) -> dict:
    repo = repo or Path(__file__).resolve().parents[2]
    doc = build_dossiers(repo)
    assert doc["n_dossiers"] == 44, doc["n_dossiers"]
    assert doc["anchors_unchanged"]
    reports = repo / "reports"
    (reports / "phase128_evidence_dossiers_44.json").write_text(
        json.dumps(doc, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (reports / "phase128_evidence_dossiers_44.csv").write_text(
        render_csv(doc), encoding="utf-8", newline=""
    )
    (reports / "phase128_evidence_dossiers_44.md").write_text(
        render_report(doc), encoding="utf-8"
    )
    return doc
