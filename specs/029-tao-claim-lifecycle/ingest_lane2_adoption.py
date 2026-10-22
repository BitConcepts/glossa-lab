#!/usr/bin/env python3
"""Spec 029 lane-2 adoption ingestion (2026-10-13, owner order).

The lane-2 drafts for the 35 live claims in scope
(``lane2-drafts/drafts.json``, PR #190) were AI-drafted on
2026-10-13, shown to the owner in full, and adopted by him as
authored by him the same day — verbatim: "Adopt all 35 lane-2
drafts as authored by me" (2026-10-13 06:12 EDT). PR #190
completed the OD-2 authoring fields on every record. This script
is the ingestion act of the same owner order: it writes the
adopted records into the live stores.

What it writes, per claim (append-only discipline throughout):

* ``not_understood`` — the adopted text, on all 35 records;
* ``explanation_record`` — the completed Phase B record (author
  Tristen Pierson; the drafting AI recorded as ``drafter`` only),
  on all 35 records;
* a stage transition ``checked`` → ``explained`` for the 20
  records standing at ``checked``, applied ONLY through the
  Phase B gate layer (:func:`glossa_lab.claim_bundle.
  gated_transition_stage`), which delegates the write to the
  Phase A transition service — the single writer of stage
  changes. The 15 records at ``created`` keep their stage:
  explanation cannot precede checking, so their records sit as
  authored-pending on a ``created`` claim;
* ``verified_unexplained`` cleared (the stored Phase D stamp)
  exactly on the records whose explanation takes effect and
  whose stamped flag was set — the flag's own computation
  (FR-029-03) also stops firing at ``explained``; the two agree.

The three Phase-104 fragment claims in scope are ingested for
their texts only and are NEVER transitioned by this script, at
any stage: their evaluation state belongs to the Phase-104
carry-over correction, a separate act.

Fail-closed, throughout: the script refuses to run unless the
drafts file is the ADOPTED one (status + author on every
record); every explanation record must pass
:func:`glossa_lab.claim_bundle.validate_explanation_record` and
its ``content_hash`` must equal the SHA-256 of its explanation
text; a record already carrying an ``explanation_record`` or a
``not_understood`` is a conflict, not a no-op; an unexpected
stage is a conflict. Nothing is written unless every record
passes — the stores are written only after the full population
validates in memory.

Usage (venv python, from anywhere):

    python3 specs/029-tao-claim-lifecycle/ingest_lane2_adoption.py
    python3 specs/029-tao-claim-lifecycle/ingest_lane2_adoption.py --verify

``--verify`` re-reads the live stores and asserts the ingested
state: all 35 texts + records present and valid, the 20 stage
advances exactly as recorded, the 9 flag clearings, and no other
record's stage or flag disturbed (checked against the frozen
reclassification ledger).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from glossa_lab.claim_bundle import (  # noqa: E402
    gated_transition_stage,
    validate_explanation_record,
)

SPEC_DIR = REPO_ROOT / "specs" / "029-tao-claim-lifecycle"
DRAFTS_PATH = SPEC_DIR / "lane2-drafts" / "drafts.json"
CLAIMS_DIR = REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
SIDECAR_PATH = SPEC_DIR / "phase-d-stamped-records.json"
LEDGER_PATH = SPEC_DIR / "reclassification-ledger.json"

AUTHOR = "Tristen Pierson"
#: The owner act: 2026-10-13 06:12 EDT = 10:12 UTC.
ACT_TIMESTAMP = "2026-10-13T10:12:00+00:00"
TRANSITION_REASON = (
    "Lane-2 adoption (owner act, 2026-10-13): the explanation record "
    "authored by Tristen Pierson — adopted from the AI-drafted texts of "
    "PR #190, drafting disclosed in the record — is ingested; the stage "
    "advances checked -> explained through the transition service (OD-2)."
)

#: The Phase-104 fragment claims: texts ingested, evaluation state
#: (including stage) owned by the carry-over correction, never by
#: this script.
PHASE104_HOLD = {
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001",
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001",
}

EXPLANATION_FIELDS = (
    "author", "author_kind", "drafter", "artifact_uri", "content_hash",
    "challenge_venue", "ai_assistance_disclosure", "explanation_text",
)


class IngestionError(RuntimeError):
    """The ingestion refuses to proceed (fail-closed)."""


def canonical(data: Any, *, trailing_newline: bool) -> str:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    return text + "\n" if trailing_newline else text


def load_drafts() -> dict[str, Any]:
    doc = json.loads(DRAFTS_PATH.read_text("utf-8"))
    if not str(doc.get("status") or "").startswith("ADOPTED"):
        raise IngestionError(
            "drafts.json is not the adopted record (status does not "
            "start with ADOPTED) — PR #190 must land first")
    if len(doc.get("drafts") or []) != 35:
        raise IngestionError("expected exactly 35 adopted drafts")
    for draft in doc["drafts"]:
        record = draft["explanation_record"]
        validate_explanation_record(record)  # raises on any defect
        if record.get("author") != AUTHOR or record.get("author_kind") != "human":
            raise IngestionError(
                f"{draft['claim_id']}: author is not the adopting human")
        digest = hashlib.sha256(
            record["explanation_text"].encode("utf-8")).hexdigest()
        if digest != record.get("content_hash"):
            raise IngestionError(
                f"{draft['claim_id']}: content_hash does not match the "
                "SHA-256 of the explanation text")
        if not str(draft.get("not_understood") or "").strip():
            raise IngestionError(f"{draft['claim_id']}: empty not_understood")
    return doc


def explanation_payload(draft: dict[str, Any]) -> dict[str, Any]:
    record = draft["explanation_record"]
    return {field: record[field] for field in EXPLANATION_FIELDS}


def locate_records(doc: dict[str, Any]):
    """Map every draft to its live record (in-memory objects).

    Returns (targets, writers): targets maps claim_id ->
    (draft, record); writers is a list of (path, data,
    trailing_newline) to persist after a successful apply.
    """
    targets: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    writers: list[tuple[Path, Any, bool]] = []

    sidecar = json.loads(SIDECAR_PATH.read_text("utf-8"))
    sidecar_by_id = {r["item_id"]: r for r in sidecar["records"]}
    writers.append((SIDECAR_PATH, sidecar, True))

    claim_files: dict[str, dict[str, Any]] = {}
    for path in sorted(CLAIMS_DIR.glob("*.json")):
        claim_files[path.name] = json.loads(path.read_text("utf-8"))
        writers.append((path, claim_files[path.name], False))
    claims_by_id: dict[str, dict[str, Any]] = {}
    for data in claim_files.values():
        for claim in data.get("claims", []):
            claims_by_id[str(claim.get("claim_id"))] = claim

    for draft in doc["drafts"]:
        claim_id = draft["claim_id"]
        if draft["record_kind"] == "extracted_claim":
            record = claims_by_id.get(claim_id)
        else:  # study_headline_claim | registered_prediction
            record = sidecar_by_id.get(claim_id)
        if record is None:
            raise IngestionError(f"{claim_id}: live record not found")
        targets[claim_id] = (draft, record)
    return targets, writers


def check_preconditions(targets) -> None:
    for claim_id, (draft, record) in targets.items():
        if "explanation_record" in record or "not_understood" in record:
            raise IngestionError(
                f"{claim_id}: record already carries lane-2 text — "
                "the adoption is a one-shot act, not a re-run")
        if record.get("stage") not in ("created", "checked"):
            raise IngestionError(
                f"{claim_id}: unexpected stage {record.get('stage')!r}")


def apply(targets) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {
        "explained": [], "authored_pending": [], "phase104_hold": []}
    for claim_id, (draft, record) in targets.items():
        record["not_understood"] = draft["not_understood"]
        record["explanation_record"] = explanation_payload(draft)
        if claim_id in PHASE104_HOLD:
            groups["phase104_hold"].append(claim_id)
            continue
        if record.get("stage") == "checked":
            gated_transition_stage(
                record, "explained",
                actor=AUTHOR, actor_kind="human",
                reason=TRANSITION_REASON,
                evidence_refs=[draft["explanation_record"]["artifact_uri"]],
                timestamp=ACT_TIMESTAMP,
            )
            if record.get("verified_unexplained") is True:
                record["verified_unexplained"] = False
            groups["explained"].append(claim_id)
        else:  # created: explanation cannot precede checking
            groups["authored_pending"].append(claim_id)
    return groups


def verify(doc: dict[str, Any]) -> dict[str, Any]:
    targets, _writers = locate_records(doc)
    ledger = json.loads(LEDGER_PATH.read_text("utf-8"))
    ledger_by_id = {e["item_id"]: e for e in ledger["entries"]}
    problems: list[str] = []
    explained, pending, hold, flags_cleared = [], [], [], []
    for claim_id, (draft, record) in targets.items():
        if record.get("not_understood") != draft["not_understood"]:
            problems.append(f"{claim_id}: not_understood mismatch")
        if record.get("explanation_record") != explanation_payload(draft):
            problems.append(f"{claim_id}: explanation_record mismatch")
        else:
            validate_explanation_record(record["explanation_record"])
        entry = ledger_by_id[claim_id]
        ledger_flag = "verified_unexplained" in (entry.get("flags") or [])
        if claim_id in PHASE104_HOLD:
            hold.append(claim_id)
            if record.get("stage") != entry["honest_stage"]:
                problems.append(f"{claim_id}: hold record's stage disturbed")
        elif entry["honest_stage"] == "checked":
            explained.append(claim_id)
            if record.get("stage") != "explained":
                problems.append(f"{claim_id}: stage is not explained")
            history = record.get("stage_history") or []
            if len(history) != 2:
                problems.append(f"{claim_id}: stage_history length != 2")
            else:
                tail = history[-1]
                if (tail.get("to_stage") != "explained"
                        or tail.get("actor") != AUTHOR
                        or tail.get("timestamp") != ACT_TIMESTAMP):
                    problems.append(f"{claim_id}: history tail is not the adoption entry")
            if record.get("stage_source") != "transition-service:stage_history[1]":
                problems.append(f"{claim_id}: stage_source is not the transition service")
            # Every explained record's flag reads False: the nine
            # stamped-true records were cleared by the act, and the
            # rest were stamped False by Phase D already.
            if record.get("verified_unexplained") is not False:
                problems.append(f"{claim_id}: explained record's flag is not False")
            if ledger_flag:
                flags_cleared.append(claim_id)
        else:
            pending.append(claim_id)
            if record.get("stage") != entry["honest_stage"]:
                problems.append(f"{claim_id}: created record's stage disturbed")
            if record.get("verified_unexplained") is not ledger_flag:
                problems.append(f"{claim_id}: created record's flag disturbed")
    return {
        "problems": problems,
        "explained": sorted(explained),
        "authored_pending": sorted(pending),
        "phase104_hold": sorted(hold),
        "flags_cleared": sorted(flags_cleared),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true",
                        help="assert the ingested state; write nothing")
    args = parser.parse_args()

    doc = load_drafts()
    if args.verify:
        report = verify(doc)
        print(json.dumps(report, indent=2))
        if report["problems"]:
            print("VERIFY FAILED", file=sys.stderr)
            return 1
        print("VERIFY OK: 35 records ingested; "
              f"{len(report['explained'])} explained, "
              f"{len(report['authored_pending'])} authored-pending, "
              f"{len(report['phase104_hold'])} Phase-104 hold; "
              f"{len(report['flags_cleared'])} flags cleared")
        return 0

    targets, writers = locate_records(doc)
    check_preconditions(targets)
    groups = apply(targets)
    for path, data, trailing in writers:
        path.write_text(canonical(data, trailing_newline=trailing), "utf-8")
    print(json.dumps({k: sorted(v) for k, v in groups.items()}, indent=2))
    print("INGESTED: texts on 35 records; "
          f"{len(groups['explained'])} advanced to explained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
