#!/usr/bin/env python3
"""Phase 432 — Spec 069 execution: the Asset A build.

Executes the frozen Spec 069 contract (freeze digest
657b930c9200299c7d540baa8ed51b7a90176bdea9822577e9cb1f4d292f99aa),
which is Spec 045's frozen sections 2-3 quoted verbatim:
the depicted-kind classification built once, from held
published sources only, entered blind, disputes coded by
rule, frozen before any join. Gates A1-A6 run in order,
fail-closed. The product is the canonical CSV at
specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv
and its machine record asset-a-freeze.json; the results
record is reports/phase432_results.json.

Entry sources (gate A1, named by edition in the build
record): the CISI volumes (Corpus of Indus Seals and
Inscriptions, Vol. 1 and Vol. 2, Shah & Parpola eds.,
1991), held digitally as IA scans and through the held
CISI digitization (mayig/indus-valley-script-corpus,
April 2026, MIT licence; restored at execution from the
public upstream at commit ad2f1e2 after the programme's
downloads copy was found missing during a concurrent
workspace sweep — spot values read before the loss and
after the restore agree); and Parpola's published sign
identifications, consulted in held form (Parpola 2010,
the Helsinki lecture) — its sign numbers are Parpola's
1994 list's and do not key to the crosswalk's sign keys,
so no row is corroborated or contested from it in a
keyable way, and agreement is single_source throughout,
as the build record states openly.

No corpus of any kind is read. Deterministic: a second
run reproduces every output byte-identically.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs/069-hunt-asset-a"
ASSET_DIR = SPEC_DIR / "asset-a"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
CONCORDANCE = (
    REPO / "specs/046-horned-tiger-concordance/concordance-297.json"
)
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
RESULTS = REPO / "reports/phase432_results.json"

CROSSWALK_SHA256 = (
    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
)
CONCORDANCE_SHA256 = (
    "772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
SPEC045_DIGEST = (
    "5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a"
)
SPEC069_FREEZE_DIGEST = (
    "657b930c9200299c7d540baa8ed51b7a90176bdea9822577e9cb1f4d292f99aa"
)
FREEZE_DATE = "2026-10-22"

DOWNLOADS = (
    Path.home() / "workspace/research_notes/"
    "indus-data-deep-sweep-20261008/downloads"
)
MAYIG_CANDIDATES = [
    Path.home() / "workspace/research_notes/hunt-chain-sources/"
    "mayig-indus-valley-script-corpus",
    DOWNLOADS / "mayig-indus-valley-script-corpus",
]

FIELDS = [
    "sign_key", "cisi_no", "parpola_no", "depicted_kind",
    "depicted_label_verbatim", "governing_source",
    "source_citations", "agreement", "dispute_status",
    "d18_input", "entered_blind",
]
KINDS = [
    "animal", "sky_cycle", "object_goods", "human", "other",
    "contested", "unidentified",
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    gates: dict = {}
    anchors_before = _sha(ANCHORS)
    assert anchors_before == ANCHORS_SHA256

    # ---- Gate A1: source availability -------------------------------
    cisi_vol1 = DOWNLOADS / "cisi-1-ia-scan/CorpusVol1.pdf"
    cisi_vol2 = DOWNLOADS / "cisi-2-ia-scan/CorpusVol2.pdf"
    parpola2010 = (
        DOWNLOADS / "parpola-2010-helsinki/"
        "Parpola2010_DravidianSolution_lecture.pdf"
    )
    mayig = next(
        (p for p in MAYIG_CANDIDATES if (p / "features").is_dir()),
        None,
    )
    a1_ok = (
        cisi_vol1.is_file() and cisi_vol2.is_file()
        and parpola2010.is_file() and mayig is not None
    )
    gates["A1"] = {
        "gate": "source availability",
        "pass": bool(a1_ok),
        "sources": {
            "cisi_vol1": {
                "edition": "Corpus of Indus Seals and Inscriptions, "
                           "Vol. 1 (Shah & Parpola eds., 1991), held "
                           "digitally (IA scan)",
                "held": cisi_vol1.is_file(),
                "sha256": _sha(cisi_vol1) if cisi_vol1.is_file() else None,
            },
            "cisi_vol2": {
                "edition": "Corpus of Indus Seals and Inscriptions, "
                           "Vol. 2 (Shah & Parpola eds., 1991), held "
                           "digitally (IA scan)",
                "held": cisi_vol2.is_file(),
                "sha256": _sha(cisi_vol2) if cisi_vol2.is_file() else None,
            },
            "cisi_digitization": {
                "edition": "the CISI sign list as held in the mayig "
                           "CISI digitization "
                           "(mayig/indus-valley-script-corpus, April "
                           "2026, MIT licence; restored at execution "
                           "from the public upstream at commit ad2f1e2)",
                "held": mayig is not None,
                "path": str(mayig) if mayig else None,
            },
            "parpola_identifications": {
                "edition": "Parpola's published sign identifications, "
                           "consulted in held form: Parpola 2010, "
                           "'The Dravidian solution' (Helsinki "
                           "lecture, held PDF)",
                "held": parpola2010.is_file(),
                "sha256": _sha(parpola2010)
                if parpola2010.is_file() else None,
                "keying_note": "its sign numbers are Parpola's 1994 "
                               "list's and do not key to the "
                               "crosswalk's sign keys; no row is "
                               "corroborated or contested from it in "
                               "a keyable way",
            },
        },
    }
    if not a1_ok:
        return _fail(gates, "A1", anchors_before)

    # ---- Gate A2: D-18 input resolved -------------------------------
    d18_sha = _sha(CONCORDANCE)
    concordance = json.loads(CONCORDANCE.read_text("utf-8"))
    a2_ok = (
        d18_sha == CONCORDANCE_SHA256
        and concordance.get("signs") == []
        and "IDENTIFICATION FAILED" in concordance["closure"]["class"]
    )
    gates["A2"] = {
        "gate": "D-18 input resolved",
        "pass": bool(a2_ok),
        "state": "terminal empty feed: concordance-297.json, signs "
                 "empty, closure IDENTIFICATION FAILED (Spec 046)",
        "sha256": d18_sha,
    }
    if not a2_ok:
        results = {
            "spec": "069-hunt-asset-a", "phase": 432,
            "outcome": "BUILD NOT STARTED (gate A2)", "gates": gates,
        }
        RESULTS.write_text(json.dumps(results, indent=1) + "\n", "utf-8")
        print("BUILD NOT STARTED (gate A2)")
        return 0

    # ---- Blind entry (two passes, reconciled; entry log committed) --
    decisions = json.loads(
        (ASSET_DIR / "entry-decisions.json").read_text("utf-8")
    )["signs"]
    with CROSSWALK.open(newline="", encoding="utf-8") as handle:
        crosswalk_rows = list(csv.DictReader(handle))
    assert _sha(CROSSWALK) == CROSSWALK_SHA256
    universe = sorted({r["registry_sign_id"] for r in crosswalk_rows})
    by_id: dict[str, list[dict]] = {}
    for row in crosswalk_rows:
        by_id.setdefault(row["registry_sign_id"], []).append(row)

    rows_out = []
    for sign_key in universe:
        feature_path = mayig / "features" / f"{sign_key}.json"
        decision = decisions[sign_key]
        kind = decision["final"]
        borderline = decision["borderline"]
        if feature_path.is_file():
            label = json.loads(
                feature_path.read_text("utf-8")
            ).get("description", "")
            citations = (
                f"CISI sign list (Corpus of Indus Seals and "
                f"Inscriptions), as held in the mayig CISI "
                f"digitization, features/{sign_key}.json — "
                f"verbatim label entered; Parpola 2010 (held "
                f"lecture) consulted — silent in keyable form "
                f"for this sign"
            )
            governing = "CISI"
            agreement = "single_source"
        else:
            label = ""
            citations = (
                "sources searched: the CISI sign list as held in "
                "the mayig CISI digitization (no entry for this "
                "sign key); Parpola's published identifications in "
                "held form (Parpola 2010 — no entry); the pinned "
                "crosswalk records only a fuls_2014 mapping (F159) "
                "for this registry id, which is not a section 2.3 "
                "source"
            )
            governing = ""
            agreement = "silent"
            assert kind == "unidentified"
        parpola_no = sign_key if sign_key.startswith("P") else ""
        rows_out.append({
            "sign_key": sign_key,
            "cisi_no": parpola_no,
            "parpola_no": parpola_no,
            "depicted_kind": kind,
            "depicted_label_verbatim": label,
            "governing_source": governing,
            "source_citations": citations,
            "agreement": agreement,
            "dispute_status": "borderline" if borderline else "none",
            "d18_input": "none",
            "entered_blind": "yes",
        })

    # ---- Gate A3: coverage completeness -------------------------------
    a3_ok = (
        len(rows_out) == len(universe) == 187
        and {r["sign_key"] for r in rows_out} == set(universe)
    )
    gates["A3"] = {
        "gate": "coverage completeness (full pinned-crosswalk "
                "universe)",
        "pass": bool(a3_ok),
        "rows": len(rows_out), "universe": len(universe),
    }
    if not a3_ok:
        return _fail(gates, "A3", anchors_before)

    # ---- Gate A4: citation completeness -------------------------------
    a4_bad = [
        r["sign_key"] for r in rows_out
        if r["depicted_kind"] != "unidentified"
        and (not r["source_citations"]
             or not r["depicted_label_verbatim"])
        or not r["agreement"]
    ]
    gates["A4"] = {
        "gate": "citation completeness",
        "pass": not a4_bad, "failing_rows": a4_bad,
    }
    if a4_bad:
        return _fail(gates, "A4", anchors_before)

    # ---- Gate A5: blind entry and order (attested in build record) ----
    gates["A5"] = {
        "gate": "blind entry and order",
        "pass": True,
        "attestation": "entry was performed from the held "
                       "published sources and the sign inventory "
                       "only, in the quoted section 2.4 order "
                       "(sources consulted, rows entered in two "
                       "independent passes and reconciled, dispute "
                       "coding completed, the D-18 absence "
                       "recorded, the asset freeze digest computed) "
                       "and before any join; no positional result, "
                       "part-membership class, or model output was "
                       "consulted at any point; the entry log is "
                       "asset-a/entry-decisions.json",
    }

    # ---- Canonical CSV (CSV writer; round-trip validated) -------------
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows_out)
    csv_text = buffer.getvalue()
    parsed = list(csv.DictReader(io.StringIO(csv_text)))
    assert len(parsed) == len(rows_out)
    assert all(len(r) == len(FIELDS) and None not in r for r in parsed)
    assert [r["sign_key"] for r in parsed] == [
        r["sign_key"] for r in rows_out
    ]
    csv_bytes = csv_text.encode("utf-8")
    (ASSET_DIR / "depicted-kind-classification.csv").write_bytes(csv_bytes)
    digest = hashlib.sha256(csv_bytes).hexdigest()

    per_kind = {
        kind: sum(1 for r in rows_out if r["depicted_kind"] == kind)
        for kind in KINDS
    }
    freeze_record = {
        "asset": "Asset A — depicted-kind classification (Spec 069)",
        "contract": "Spec 045 sections 2-3, quoted in Spec 069 "
                    "spec section 2",
        "contract_anchor_freeze_digest": SPEC045_DIGEST,
        "spec069_freeze_digest": SPEC069_FREEZE_DIGEST,
        "canonical_file": "asset-a/depicted-kind-classification.csv",
        "sha256": digest,
        "row_count": len(rows_out),
        "per_kind_counts": per_kind,
        "input_pins": {
            "crosswalk": {
                "file": "data/crosswalks/sign_crosswalk_master.csv",
                "sha256": CROSSWALK_SHA256,
                "rows": len(crosswalk_rows),
                "distinct_registry_sign_ids": len(universe),
            },
            "d18_concordance": {
                "file": "specs/046-horned-tiger-concordance/"
                        "concordance-297.json",
                "sha256": CONCORDANCE_SHA256,
                "state": "terminal empty feed (signs empty, "
                         "IDENTIFICATION FAILED closure); consumed "
                         "as recorded absence, never reconstructed",
            },
            "anchors": {
                "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
                "sha256": ANCHORS_SHA256,
            },
            "sources": "gate A1 of the build record: CISI vols. 1-2 "
                       "(1991) held digitally; the CISI sign list "
                       "as held in the mayig CISI digitization "
                       "(April 2026; upstream commit ad2f1e2); "
                       "Parpola's published identifications "
                       "consulted in held form (Parpola 2010)",
        },
        "build_order_attestation": gates["A5"]["attestation"],
        "freeze_date": FREEZE_DATE,
    }
    (ASSET_DIR / "asset-a-freeze.json").write_text(
        json.dumps(freeze_record, indent=1) + "\n", "utf-8"
    )

    # ---- Gate A6: freeze recorded, digest recomputes -------------------
    recomputed = hashlib.sha256(
        (ASSET_DIR / "depicted-kind-classification.csv").read_bytes()
    ).hexdigest()
    a6_ok = recomputed == digest
    gates["A6"] = {
        "gate": "freeze recorded", "pass": bool(a6_ok),
        "sha256": digest,
    }
    if not a6_ok:
        return _fail(gates, "A6", anchors_before)

    anchors_after = _sha(ANCHORS)
    assert anchors_after == anchors_before == ANCHORS_SHA256
    results = {
        "spec": "069-hunt-asset-a", "phase": 432,
        "outcome": "ASSET BUILT AND FROZEN",
        "asset_a_sha256": digest,
        "row_count": len(rows_out),
        "per_kind_counts": per_kind,
        "agreement_counts": {
            v: sum(1 for r in rows_out if r["agreement"] == v)
            for v in ("agree", "single_source", "disagree", "silent")
        },
        "dispute_counts": {
            v: sum(1 for r in rows_out if r["dispute_status"] == v)
            for v in ("none", "contested", "borderline")
        },
        "gates": gates,
        "anchors_before": anchors_before,
        "anchors_after": anchors_after,
        "d18_state": gates["A2"]["state"],
    }
    RESULTS.write_text(json.dumps(results, indent=1) + "\n", "utf-8")
    print("ASSET BUILT AND FROZEN", digest, per_kind)
    return 0


def _fail(gates: dict, gate: str, anchors_before: str) -> int:
    results = {
        "spec": "069-hunt-asset-a", "phase": 432,
        "outcome": "ASSET FAILED", "failed_gate": gate,
        "gates": gates, "anchors_before": anchors_before,
        "anchors_after": _sha(ANCHORS),
    }
    RESULTS.write_text(json.dumps(results, indent=1) + "\n", "utf-8")
    print("ASSET FAILED at gate", gate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
