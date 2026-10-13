#!/usr/bin/env python3
"""Phase-104 carry-over correction — Spec 029 record correction (2026-10-13).

The defect (verified against the primary record before any change):
``glossa-indus/reports/phase104_claims_evaluation.json`` evaluated the
then-untested extracted claims and returned, for five records, the
verdict ``status_changed`` -> ``contradicted`` under RULE-DUP
("verdict carried over from an already-adjudicated identical
proposition"), each with the reason "Restates the proposition already
adjudicated as farmer_sproat_witzel_2004_manual_001 (verdict:
contradicted, with cited evidence). Verdict carries over." Three of
the five are canonical live claims:

* ``indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001``
* ``indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002``
* ``without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001``

(The other two, ``..._critique_0003`` / ``..._critique_0004``, were
merged by Phase I as evidence instances of the first two canonicals;
their preserved instance records are intentionally NOT rewritten by
this correction — see the correction record.)

The carry-over was never written into the live records: all three
still read ``claim_status: untested`` at stage ``created``. The
Spec 029 retroactive audit then honestly staged them ``created``
("no test outcome recorded") from the live state it found, and the
frozen reclassification ledger preserves that reading. The ledger is
frozen and is NOT touched; this correction supersedes the stamp on
these three records through the machinery's own append-only route:

* the lane-1 verdict is written as Phase-104 prescribed it —
  ``claim_status: contradicted`` plus Phase-104's own evidence list,
  verbatim, as ``contradicting_evidence``;
* an additive ``status_correction`` field preserves the previous
  status and names the basis, so nothing is silently overwritten;
* the stage moves ``created`` -> ``checked`` through the single
  stage writer (``glossa_lab.claim_stage.transition_stage``), which
  appends a dated ``stage_history`` entry naming this correction;
  the Phase D migration entry stays as history[0], untouched.

The canonical claim (``farmer_sproat_witzel_2004_manual_001``) does
not change. No falsification condition is added: Phase-104 carried
over a verdict and its evidence, not a falsifier, and this machinery
invents none — the fragments' falsifier gap stays on their trail,
with the proposition's falsifier reachable on the canonical record
through the cross-reference evidence item.

Usage:
    python3 correct_phase104_carryover.py            # verify pre-state (dry run)
    python3 correct_phase104_carryover.py --apply    # write the correction
    python3 correct_phase104_carryover.py --verify   # verify post-state
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from glossa_lab.claim_stage import transition_stage  # noqa: E402

CLAIMS_DIR = REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
PHASE104_REL = "glossa-indus/reports/phase104_claims_evaluation.json"
CANONICAL_ID = "farmer_sproat_witzel_2004_manual_001"
CANONICAL_REL = "glossa-indus/claims/extracted_claims/farmer_sproat_witzel_2004.json"
LEDGER_SOURCE = "specs/029-tao-claim-lifecycle/reclassification-ledger.json"
CORRECTION_DATE = "2026-10-13"
ACTOR = "spec029-phase104-carryover-migration"

TARGETS: dict[str, str] = {
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001":
        "indus_valley_script_deciphered_from_myth_65ff0a26.json",
    "indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002":
        "indus_valley_script_deciphered_from_myth_65ff0a26.json",
    "without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001":
        "without_kings_or_conquests_the_indus_scr_ce9d98cc.json",
}

REASON = (
    "Phase-104 carry-over correction (2026-10-13): the Phase-104 evaluation of "
    "untested claims found this record restates the Farmer, Sproat and Witzel "
    "thesis already judged contradicted on farmer_sproat_witzel_2004_manual_001, "
    "and recorded that the verdict carries over (rule RULE-DUP) — but the "
    "carry-over was never written into this record, which still showed untested "
    "at the created stage. This entry writes it: the claim status now reads "
    "contradicted, with the evaluation's evidence, and the stage moves to "
    "checked. The earlier stage entry in this history is unchanged."
)

NOTE = (
    "The Phase-104 evaluation judged this record a restatement of "
    "farmer_sproat_witzel_2004_manual_001 (contradicted) and recorded that "
    "the verdict carries over; the carry-over was never written into the "
    "live record. Applied 2026-10-13 on the owner's order. The previous "
    "status is preserved in this field, and the record's earlier history "
    "is unchanged."
)


class CorrectionError(RuntimeError):
    pass


def dump(data: dict) -> bytes:
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")


def load_doc(filename: str) -> tuple[Path, dict]:
    path = CLAIMS_DIR / filename
    return path, json.loads(path.read_text("utf-8"))


def find_claim(doc: dict, claim_id: str) -> dict:
    for claim in doc["claims"]:
        if claim.get("claim_id") == claim_id:
            return claim
    raise CorrectionError(f"{claim_id}: not found in its source document")


def phase104_entries() -> dict[str, dict]:
    data = json.loads((REPO_ROOT / PHASE104_REL).read_text("utf-8"))
    out = {}
    for result in data["results"]:
        if result.get("rule") == "RULE-DUP":
            out[result["claim_id"]] = result
    return out


def check_phase104_support(entries: dict[str, dict]) -> None:
    """Fail closed unless Phase-104 supports the carry-over for every target."""
    for claim_id in TARGETS:
        entry = entries.get(claim_id)
        if entry is None:
            raise CorrectionError(f"{claim_id}: no RULE-DUP entry in Phase-104 record")
        if entry.get("verdict") != "status_changed" or entry.get("new_status") != "contradicted":
            raise CorrectionError(
                f"{claim_id}: Phase-104 verdict is {entry.get('verdict')!r} -> "
                f"{entry.get('new_status')!r}, not status_changed -> contradicted")
        if CANONICAL_ID not in str(entry.get("reason") or ""):
            raise CorrectionError(f"{claim_id}: Phase-104 reason does not name {CANONICAL_ID}")
        if not entry.get("evidence"):
            raise CorrectionError(f"{claim_id}: Phase-104 entry carries no evidence list")


def assert_pre_state(claim: dict) -> None:
    cid = claim["claim_id"]
    if claim.get("claim_status") != "untested":
        raise CorrectionError(f"{cid}: claim_status is {claim.get('claim_status')!r}, not 'untested'")
    if claim.get("stage") != "created":
        raise CorrectionError(f"{cid}: stage is {claim.get('stage')!r}, not 'created'")
    if claim.get("stage_source") != f"{LEDGER_SOURCE}:{cid}":
        raise CorrectionError(f"{cid}: stage_source is not the frozen-ledger stamp")
    if claim.get("stage_as_of") != "2026-10-12" or len(claim.get("stage_history") or []) != 1:
        raise CorrectionError(f"{cid}: stage stamp is not the single Phase D entry")
    if "contradicting_evidence" in claim or "status_correction" in claim:
        raise CorrectionError(f"{cid}: correction fields already present (already applied?)")


def assert_post_state(claim: dict, entry: dict) -> None:
    cid = claim["claim_id"]
    if claim.get("claim_status") != "contradicted":
        raise CorrectionError(f"{cid}: claim_status is not 'contradicted' after correction")
    if claim.get("contradicting_evidence") != entry["evidence"]:
        raise CorrectionError(f"{cid}: contradicting_evidence differs from the Phase-104 list")
    corr = claim.get("status_correction") or {}
    if corr.get("kind") != "phase104-carryover-correction" or corr.get("date") != CORRECTION_DATE:
        raise CorrectionError(f"{cid}: status_correction note missing or malformed")
    if corr.get("previous_claim_status") != "untested":
        raise CorrectionError(f"{cid}: previous status not preserved in the correction note")
    history = claim.get("stage_history") or []
    if len(history) != 2 or history[0].get("actor") != "spec029-phase-d-restaging-migration":
        raise CorrectionError(f"{cid}: Phase D history entry not preserved as history[0]")
    tail = history[-1]
    if tail.get("from_stage") != "created" or tail.get("to_stage") != "checked":
        raise CorrectionError(f"{cid}: correction history tail is not created -> checked")
    if tail.get("actor") != ACTOR or f"{PHASE104_REL}:{cid}" not in (tail.get("evidence_refs") or []):
        raise CorrectionError(f"{cid}: correction history entry lacks actor or Phase-104 ref")
    if claim.get("stage") != "checked":
        raise CorrectionError(f"{cid}: stage is not 'checked' after correction")
    if claim.get("stage_source") != "transition-service:stage_history[1]":
        raise CorrectionError(f"{cid}: stage_source does not index the correction entry")
    if claim.get("stage_as_of") != tail.get("timestamp"):
        raise CorrectionError(f"{cid}: stage_as_of does not equal the correction timestamp")
    if claim.get("verified_unexplained") is not False:
        raise CorrectionError(f"{cid}: verified_unexplained changed (must stay false)")


def apply_correction(claim: dict, entry: dict, timestamp: str) -> None:
    """Write the Phase-104 outcome into one record (see module docstring)."""
    cid = claim["claim_id"]
    correction = {
        "kind": "phase104-carryover-correction",
        "date": CORRECTION_DATE,
        "previous_claim_status": claim["claim_status"],
        "new_claim_status": entry["new_status"],
        "basis": f"{PHASE104_REL}:{cid}",
        "rule": entry["rule"],
        "note": NOTE,
    }
    rebuilt: dict = {}
    for key, value in claim.items():
        rebuilt[key] = value
        if key == "testability":
            rebuilt["contradicting_evidence"] = list(entry["evidence"])
            rebuilt["status_correction"] = correction
    rebuilt["claim_status"] = entry["new_status"]
    claim.clear()
    claim.update(rebuilt)
    transition_stage(
        claim,
        "checked",
        actor=ACTOR,
        actor_kind="automated",
        reason=REASON,
        evidence_refs=[f"{PHASE104_REL}:{cid}", f"{CANONICAL_REL}:{CANONICAL_ID}"],
        timestamp=timestamp,
    )


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "--dry-run"
    entries = phase104_entries()
    check_phase104_support(entries)

    docs: dict[str, tuple[Path, dict]] = {}
    for filename in sorted(set(TARGETS.values())):
        docs[filename] = load_doc(filename)

    if mode == "--verify":
        for claim_id, filename in TARGETS.items():
            claim = find_claim(docs[filename][1], claim_id)
            assert_post_state(claim, entries[claim_id])
            print(f"VERIFIED post-state: {claim_id}")
        return 0

    for claim_id, filename in TARGETS.items():
        assert_pre_state(find_claim(docs[filename][1], claim_id))
    print("Pre-state verified for all three claims (untested / created / Phase D stamp).")

    if mode == "--dry-run":
        for claim_id in TARGETS:
            e = entries[claim_id]
            print(f"WOULD CORRECT {claim_id}: untested -> {e['new_status']} "
                  f"(stage created -> checked), evidence items: {len(e['evidence'])}")
        return 0

    if mode == "--apply":
        timestamp = datetime.now(timezone.utc).isoformat()
        for claim_id, filename in TARGETS.items():
            claim = find_claim(docs[filename][1], claim_id)
            apply_correction(claim, entries[claim_id], timestamp)
            assert_post_state(claim, entries[claim_id])
        for filename, (path, doc) in docs.items():
            path.write_bytes(dump(doc))
            print(f"WROTE {path.relative_to(REPO_ROOT)}")
        for claim_id in TARGETS:
            print(f"CORRECTED {claim_id}: untested/created -> contradicted/checked "
                  f"(Phase-104 carry-over, {CORRECTION_DATE})")
        return 0

    print(f"unknown mode {mode!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
