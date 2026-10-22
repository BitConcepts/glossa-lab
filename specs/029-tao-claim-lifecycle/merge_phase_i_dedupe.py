"""Spec 029 Phase I — D-B proposition deduplication (plan §2.6, tasks I1–I3).

Run from the repo root with the Glossa venv:

    # dry run (writes nothing; emits the merge plan + reconciliation)
    python specs/029-tao-claim-lifecycle/merge_phase_i_dedupe.py --dry-run

    # live run (snapshots the store first, then merges)
    python specs/029-tao-claim-lifecycle/merge_phase_i_dedupe.py \
        --live --snapshot-dir /path/to/snapshots

    # post-run verification (read-only; checks the merged store)
    python specs/029-tao-claim-lifecycle/merge_phase_i_dedupe.py --verify

D-B (ratified 2026-10-12): deduplicate by PROPOSITION — merge,
never delete. This tool is the merge's only writer. Its rules:

* The proposition fingerprint is
  ``glossa_lab.proposition_fingerprint.claim_fingerprint``
  (SHA-256 over the normalised claim text; rules frozen in that
  module, version ``spec029-phase-i-v1``). Records sharing a
  fingerprint are one proposition.
* One canonical claim per proposition: the record with the
  fuller trail wins (count of populated trail fields — see
  ``TRAIL_FIELDS``); ties break by store scan order (sorted
  file name, then position in the file), which for every group
  in the 2026-10-09 batch agrees with the frozen
  reclassification ledger (the ledger flags the non-canonical
  records ``duplicate_record`` and never the canonical ones).
* Merge, never delete: every record stays in its own file with
  every pre-existing field byte-preserved. The canonical record
  gains ``proposition_fingerprint`` and an
  ``evidence_instances`` list holding a full copy of each merged
  instance record (as stamped by this merge, pointer included).
  Each instance record gains ``proposition_fingerprint`` and a
  ``merged_into`` pointer to the canonical claim id. Records in
  no duplicate group gain only ``proposition_fingerprint``.
* Phase D stage stamps are never touched: stage, stage_source,
  stage_as_of, stage_history and verified_unexplained are not
  merge keys, and the additive-only assertion (below) proves no
  pre-existing field of any record changed.
* Additive-only, asserted before writing: removing exactly the
  Phase I keys (``proposition_fingerprint``, ``merged_into``,
  ``evidence_instances``) from the merged data must reproduce
  each file's pre-merge canonical bytes.
* Idempotent: a store already merged exactly per plan is a
  no-op and says so; a partially merged store stops the run.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from glossa_lab.proposition_fingerprint import (  # noqa: E402
    FINGERPRINT_RULES_VERSION,
    claim_fingerprint,
)

STORE_DIR = REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
PHASE_I_KEYS = ("proposition_fingerprint", "merged_into", "evidence_instances")
MERGE_DATE = "2026-10-12"

#: Fields that make one record's trail "fuller" than another's
#: (tasks I2: the fuller trail wins the canonical slot).
TRAIL_FIELDS = (
    "falsification_condition", "glossa_lab_evidence",
    "contradicting_evidence", "quote_fragment", "author",
    "signs_involved", "sign_ids", "proposed_value",
    "proposed_language", "required_data",
)


def _canonical_bytes(data: dict) -> bytes:
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")


def load_store() -> list[tuple[Path, dict]]:
    files = []
    for path in sorted(STORE_DIR.glob("*.json")):
        files.append((path, json.loads(path.read_text("utf-8"))))
    return files


def all_records(files: list[tuple[Path, dict]]) -> list[tuple[str, dict]]:
    """(source_file_stem, record) pairs in store scan order."""
    out = []
    for path, data in files:
        for record in data.get("claims", []):
            out.append((path.stem, record))
    return out


def trail_richness(record: dict) -> int:
    return sum(1 for k in TRAIL_FIELDS if record.get(k) not in (None, "", []))


def plan_merges(files: list[tuple[Path, dict]]) -> list[dict]:
    """The exact duplicate set: fingerprint groups with >1 record."""
    groups: dict[str, list[tuple[str, dict]]] = {}
    for stem, record in all_records(files):
        groups.setdefault(claim_fingerprint(record), []).append((stem, record))
    plan = []
    for fingerprint, members in groups.items():
        if len(members) < 2:
            continue
        ranked = sorted(
            range(len(members)),
            key=lambda i: (-trail_richness(members[i][1]), i),
        )
        canonical_idx = ranked[0]
        canonical_stem, canonical = members[canonical_idx]
        instances = [m for i, m in enumerate(members) if i != canonical_idx]
        plan.append({
            "fingerprint": fingerprint,
            "canonical_claim_id": canonical["claim_id"],
            "canonical_source_file": canonical_stem,
            "canonical_trail_richness": trail_richness(canonical),
            "instance_claim_ids": [r["claim_id"] for _, r in instances],
            "instance_source_files": [s for s, _ in instances],
        })
    plan.sort(key=lambda p: p["canonical_claim_id"])
    return plan


def store_state(files: list[tuple[Path, dict]], plan: list[dict]) -> str:
    """'unmerged' | 'merged' | 'partial' for the live store."""
    records = [r for _, r in all_records(files)]
    stamped = [r for r in records if "proposition_fingerprint" in r]
    if not stamped:
        return "unmerged"
    if len(stamped) != len(records):
        return "partial"
    by_id = {r["claim_id"]: r for r in records}
    for group in plan:
        canonical = by_id[group["canonical_claim_id"]]
        embedded = canonical.get("evidence_instances") or []
        if [e.get("claim_id") for e in embedded] != group["instance_claim_ids"]:
            return "partial"
        for cid in group["instance_claim_ids"]:
            if by_id[cid].get("merged_into") != group["canonical_claim_id"]:
                return "partial"
    return "merged"


def apply_merges(files: list[tuple[Path, dict]], plan: list[dict]) -> None:
    """Apply the merge in memory (callers assert, then write)."""
    records = all_records(files)
    by_id = {r["claim_id"]: r for _, r in records}
    stem_of = {r["claim_id"]: s for s, r in records}
    # 1. Every record gains its proposition fingerprint.
    for _, record in records:
        record["proposition_fingerprint"] = claim_fingerprint(record)
    # 2. Instances gain the merged_into pointer.
    for group in plan:
        for cid in group["instance_claim_ids"]:
            by_id[cid]["merged_into"] = group["canonical_claim_id"]
    # 3. Canonical records gain the preserved evidence instances:
    #    a full copy of each instance record as stamped by this
    #    merge (fingerprint + pointer included), in scan order.
    for group in plan:
        canonical = by_id[group["canonical_claim_id"]]
        canonical["evidence_instances"] = [
            {
                "claim_id": cid,
                "source_document_id": by_id[cid].get("source_document_id"),
                "source_file": stem_of[cid],
                "record": copy.deepcopy(by_id[cid]),
            }
            for cid in group["instance_claim_ids"]
        ]


def additive_only_check(before: list[tuple[Path, dict]],
                        after: list[tuple[Path, dict]]) -> list[str]:
    """Removing exactly the Phase I keys from `after` must reproduce
    `before`'s canonical bytes, file by file."""
    problems = []
    before_map = {p.name: _canonical_bytes(d) for p, d in before}
    for path, data in after:
        stripped = copy.deepcopy(data)
        for record in stripped.get("claims", []):
            for key in PHASE_I_KEYS:
                record.pop(key, None)
        if _canonical_bytes(stripped) != before_map[path.name]:
            problems.append(f"{path.name}: pre-existing content changed")
    return problems


def verify_store(files: list[tuple[Path, dict]], plan: list[dict]) -> dict:
    records = all_records(files)
    problems = []
    by_id = {r["claim_id"]: r for _, r in records}
    for _, record in records:
        if record.get("proposition_fingerprint") != claim_fingerprint(record):
            problems.append(f"{record['claim_id']}: fingerprint mismatch")
    canonical_count = 0
    for _, record in records:
        if record.get("merged_into"):
            target = by_id.get(record["merged_into"])
            if target is None:
                problems.append(f"{record['claim_id']}: merged_into dangles")
            else:
                embedded = {
                    e.get("claim_id"): e
                    for e in target.get("evidence_instances") or []
                }
                entry = embedded.get(record["claim_id"])
                # The embedded copy is the record as merged; the
                # store's one volatile field, ``extracted_at``, is
                # refreshed by later extraction regenerations on
                # the live instance record (pre-existing store
                # behaviour, Phases A/D) and is excluded from the
                # comparison. Every other field must match exactly.
                live = {k: v for k, v in record.items() if k != "extracted_at"}
                kept = {k: v for k, v in (entry.get("record") or {}).items()
                        if k != "extracted_at"} if entry else None
                if entry is None or kept != live:
                    problems.append(
                        f"{record['claim_id']}: not preserved verbatim "
                        f"on canonical {record['merged_into']}")
        else:
            canonical_count += 1
    return {
        "records_in_store": len(records),
        "canonical_claims": canonical_count,
        "evidence_instances": len(records) - canonical_count,
        "merge_groups": len(plan),
        "problems": problems,
        "ok": not problems,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--snapshot-dir", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    files = load_store()
    plan = plan_merges(files)
    state = store_state(files, plan)
    report: dict = {
        "tool": "merge_phase_i_dedupe",
        "date": MERGE_DATE,
        "fingerprint_rules_version": FINGERPRINT_RULES_VERSION,
        "store_state_before": state,
        "records_in_store": len(all_records(files)),
        "merge_groups": plan,
    }

    if args.verify:
        report["verification"] = verify_store(files, plan)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["verification"]["ok"] else 1

    if state == "merged":
        report["result"] = "no-op: store already merged per plan; nothing written"
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    if state == "partial":
        report["result"] = "STOP: store is partially merged; not smoothed"
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1

    before = copy.deepcopy(files)
    apply_merges(files, plan)
    problems = additive_only_check(before, files)
    if problems:
        report["result"] = "STOP: additive-only assertion failed"
        report["problems"] = problems
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1
    report["verification_after_apply"] = verify_store(files, plan)

    if args.dry_run:
        report["result"] = "dry run: nothing written"
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    # Live: snapshot first, then write exactly the merged bytes.
    if args.snapshot_dir is None:
        print("ERROR: --live requires --snapshot-dir", file=sys.stderr)
        return 2
    args.snapshot_dir.mkdir(parents=True, exist_ok=True)
    for path, _ in files:
        shutil.copy2(path, args.snapshot_dir / path.name)
    report["snapshot_dir"] = str(args.snapshot_dir)
    hashes = {}
    for path, data in files:
        raw = _canonical_bytes(data)
        path.write_bytes(raw)
        hashes[path.name] = hashlib.sha256(raw).hexdigest()
    report["post_merge_sha256"] = hashes
    report["result"] = "live run complete: store merged, nothing deleted"
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.report:
        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False), "utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
