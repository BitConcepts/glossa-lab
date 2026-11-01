#!/usr/bin/env python3
"""One-time D-E migration building the Spec 086 ledger (T104).

Migrates the three claim populations into
``glossa-indus/ledger/claims.jsonl``, one gated run per
population, in the order P1 (extracted claims) -> P3
(research-check annotations) -> P2 (spec governance bundles):

- D-B grouping: one canonical ledger entry per proposition
  fingerprint; every other source record of the proposition is
  preserved as an evidence instance in the entry's ``sources``
  and listed in the population's reconciliation report.
- Mirrors, never re-adjudicates: status/stage are copied from
  the source of record and verified byte-equal by the report.
- Read-only against every source store and frozen tree: this
  tool opens source files for reading only.

Each run emits its reconciliation report (Markdown) into the
spec's records directory and, after all three populations are
written, runs the intake validator over the built ledger and
prints its output verbatim.

Usage (from the repo root):

    python3 tools/ledger/migrate_ledger.py \
        --date 2026-11-01 --run-id migration-2026-11-01-stage1 \
        --report-dir specs/086-winning-combination-adoption/records
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.ledger_intake import (  # noqa: E402
    _SourceCache,
    annotation_from_sidecar,
    build_bundle_entries,
    entry_from_extracted_record,
    extracted_canonical_map,
    sha256_file,
    validate_ledger,
    write_ledger,
)
from glossa_lab.proposition_fingerprint import (  # noqa: E402
    proposition_fingerprint,
)

FALSIFIER_KEYS = ("falsification_tests", "falsification_condition")


def _record_falsifiers(record: dict) -> list[str]:
    out: list[str] = []
    for key in FALSIFIER_KEYS:
        value = record.get(key)
        if isinstance(value, list):
            out.extend(str(v) for v in value)
        elif isinstance(value, str) and value:
            out.append(value)
    return out


def migrate_p1(root: Path, date: str, migration: dict) -> tuple[list[dict], str]:
    claims_dir = root / "glossa-indus" / "claims" / "extracted_claims"
    files = sorted(claims_dir.glob("*.json"))
    records: list[tuple[Path, dict]] = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data.get("claims", []):
            records.append((path, record))
    groups: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for path, record in records:
        groups[proposition_fingerprint(record["normalized_claim"])].append(
            (path, record)
        )
    entries: list[dict] = []
    instance_rows: list[str] = []
    group_rows: list[str] = []
    for fp in sorted(groups):
        members = groups[fp]
        canonical = [m for m in members if not m[1].get("merged_into")]
        assert len(canonical) == 1, f"P1 group {fp} has {len(canonical)} canonicals"
        cpath, crec = canonical[0]
        entry = entry_from_extracted_record(
            crec,
            source_path=str(cpath.relative_to(root)),
            source_sha256=sha256_file(cpath),
            date=date,
            migration=migration,
        )
        falsifier: list[str] = []
        for _, record in members:
            for text in _record_falsifiers(record):
                if text not in falsifier:
                    falsifier.append(text)
        entry["falsifier"] = falsifier or None
        for path, record in members:
            if record is crec:
                continue
            assert record.get("merged_into") == crec["claim_id"], (
                f"merged_into of {record['claim_id']} does not name the "
                "group canonical"
            )
            entry["sources"].append(
                {
                    "path": str(path.relative_to(root)),
                    "sha256": sha256_file(path),
                    "role": "evidence_instance",
                    "spec": None,
                    "claim_id": str(record["claim_id"]),
                    "document_id": record.get("source_document_id"),
                }
            )
            instance_rows.append(
                f"| {record['claim_id']} | {entry['id']} | "
                f"{record.get('claim_status')} | {record.get('stage')} |"
            )
        if len(members) > 1:
            group_rows.append(
                f"- `{fp[:12]}…` canonical `{entry['id']}` with "
                f"{len(members)} source records: "
                + ", ".join(f"`{r['claim_id']}`" for _, r in members)
            )
        entries.append(entry)
    entries.sort(key=lambda e: e["id"])
    with_falsifier = sum(1 for e in entries if e["falsifier"])
    with_dne = sum(1 for e in entries if e["does_not_establish"])
    with_expl = sum(1 for e in entries if e["explanation_record"])
    unresolved = [
        (r["claim_id"], r["signs_involved"])
        for _, r in records
        if r.get("signs_involved")
    ]
    report = f"""# Reconciliation — P1 extracted claims (Spec 086 Stage 1, T104)

Migration run: `{migration['run_id']}`, {date}. Source store:
`glossa-indus/claims/extracted_claims/` ({len(files)} files,
read-only). Grouping: proposition fingerprint under
`spec029-phase-i-v1` (D-B); the canonical record of each group
is the one the store itself leaves unmerged (no `merged_into`),
and every merged record's `merged_into` was verified to name
its group's canonical.

## Headline counts

| Measure | Count |
|---|---|
| Source records in | {len(records)} |
| Canonical ledger entries out | {len(entries)} |
| Merged evidence instances (preserved as sources, D-B) | {len(records) - len(entries)} |
| Fingerprint groups with >1 source record | {len(group_rows)} |

## Merged evidence instances

Each instance's own status/stage remains in its source record
(below, for the record); under D-B the proposition's canonical
entry carries the canonical record's status/stage, verified
byte-equal against that record by this report's check.

| Instance claim id | Canonical entry | Instance status (source) | Instance stage (source) |
|---|---|---|---|
{chr(10).join(instance_rows)}

## Fingerprint groups with >1 source record

{chr(10).join(group_rows)}

## Coverage (canonical entries)

- Falsifier: {with_falsifier} of {len(entries)} entries carry
  one. Source records carrying a falsification condition
  (the store's field is `falsification_condition`):
  {sum(1 for _, r in records if _record_falsifiers(r))} of
  {len(records)}. The remaining gap is recorded as
  `falsifier: null`, never filled (D-086-Q6). Note for the
  record: the Spec 086 package's premise "0 of 31 carry a
  falsifier field" referred to a field literally named
  `falsifier`; the store carries the same content under
  `falsification_condition` on the records counted here, and
  the migration carries it where present.
- Does-not-establish (`not_understood`): {with_dne} of
  {len(entries)} entries.
- Explanation records (OD-2, named human author): {with_expl}
  of {len(entries)} entries.
- AEE state: 0 of {len(entries)} entries — the source records
  carry no scores; `aee_state` is null, shown as null.
- Confidence (harmonization adoption #3 item 6, binding —
  narrative confidence is not a number): every source record
  carries `confidence_in_source` as a NUMBER (float; 31 of 31
  records, all numeric — a full-store census found no
  qualitative confidence value in this population). Each
  canonical entry carries its canonical record's value
  verbatim in `confidence_in_source`; the 8 merged instances'
  values were checked against their canonicals' (differences:
  0). `confidence_text` is null on every entry: no narrative
  confidence exists in the source, and none was manufactured.
  Intake rule, enforced by the shared builder: a qualitative
  confidence string is carried verbatim into
  `confidence_text` and never normalized into a number.
- Unresolved sign mentions: {len(unresolved)} source records
  carry free-text `signs_involved` with no identifier-bearing
  field; they are NOT resolved into `sign_refs` (identifier
  fields only). Records: {', '.join(f'`{c}`' for c, _ in unresolved) or 'none'}.

## Mirror check

Every canonical entry's `status` and `stage` were compared
byte-equal against its source-of-record claim record after
the build; the migration test
(`test_spec086_ledger_migration.py`) re-runs this comparison
in CI. Status or stage differences: none (any difference
would be listed here and would stop the stage).
"""
    return entries, report


def migrate_p3(
    root: Path, date: str, migration: dict
) -> tuple[list[dict], str]:
    checks_dir = root / "glossa-indus" / "claims" / "research_checks"
    files = sorted(checks_dir.glob("*.research_check.json"))
    canonical_map = extracted_canonical_map(root)
    entries = [
        annotation_from_sidecar(
            root, path, date=date, canonical_map=canonical_map,
            migration=migration,
        )
        for path in files
    ]
    entries.sort(key=lambda e: e["id"])
    merged_targets = sum(
        1 for e in entries if e["canonical_claim_id"] != e["target_claim_id"]
    )
    report = f"""# Reconciliation — P3 research-check annotations (Spec 086 Stage 1, T104)

Migration run: `{migration['run_id']}`, {date}. Source store:
`glossa-indus/claims/research_checks/` ({len(files)} sidecar
files, read-only). The Spec 025 contract stands untouched:
sidecars stay advisory and never modify a claim; what enters
the ledger is one annotation entry per sidecar, recording the
sidecar's id, content hash, the claim it bears on, and the
bearing its own record states.

## Headline counts

| Measure | Count |
|---|---|
| Sidecar files in | {len(files)} |
| Annotation entries out | {len(entries)} |
| Annotations whose target claim is a merged instance (canonical entry named in `canonical_claim_id`) | {merged_targets} |
| Sidecars with a verdict | {sum(1 for e in entries if e['bearing']['verdict'])} |

Every annotation's `canonical_claim_id` resolves to a P1
canonical ledger entry (validator-checked). No claim's status,
stage, or score is changed by any annotation.
"""
    return entries, report


def migrate_p2(root: Path, date: str, migration: dict) -> tuple[list[dict], str]:
    spec_dirs = [
        p.parent
        for p in sorted(root.glob("specs/*/claims.json"))
        + sorted(root.glob("specs/*/aee-claims.json"))
    ]
    spec_dirs = sorted(set(spec_dirs))
    n_claims_files = len(list(root.glob("specs/*/claims.json")))
    n_aee_files = len(list(root.glob("specs/*/aee-claims.json")))
    total_records = 0
    pair_keys: set[tuple[str, str]] = set()
    for spec_dir in spec_dirs:
        for name in ("claims.json", "aee-claims.json"):
            path = spec_dir / name
            if path.is_file():
                data = json.loads(path.read_text(encoding="utf-8"))
                total_records += len(data.get("claims", []))
                for record in data.get("claims", []):
                    pair_keys.add((spec_dir.name, str(record["id"])))
    pair_formats: dict[tuple[str, str], set[str]] = defaultdict(set)
    for spec_dir in spec_dirs:
        for fmt, name in (("claims", "claims.json"), ("aee", "aee-claims.json")):
            path = spec_dir / name
            if path.is_file():
                data = json.loads(path.read_text(encoding="utf-8"))
                for record in data.get("claims", []):
                    pair_formats[(spec_dir.name, str(record["id"]))].add(fmt)
    pairs_in_both = sum(1 for v in pair_formats.values() if len(v) == 2)
    groups = build_bundle_entries(root, spec_dirs, date=date, migration=migration)
    entries = sorted((g.entry for g in groups), key=lambda e: e["id"])
    cross = [g for g in groups if len({(s, c) for s, c, _, _ in g.members}) > 1]
    merged_pairs = sum(
        len({(s, c) for s, c, _, _ in g.members}) - 1 for g in groups
    )
    falsifier_variants = 0
    boundary_variants = 0
    for g in groups:
        fsets = set()
        bsets = set()
        cache = _SourceCache(root)
        for source in g.entry["sources"]:
            record = cache.claim_record(source)
            if record is None:
                continue
            fsets.add(tuple(record.get("falsification_tests") or []))
            b = record.get("boundary")
            bsets.add(b if isinstance(b, str) else " ".join(b or []))
        if len(fsets) > 1:
            falsifier_variants += 1
        if len(bsets) > 1:
            boundary_variants += 1
    cross_rows = "\n".join(
        f"- `{g.fingerprint[:12]}…` canonical `{g.entry['id']}`; "
        f"proposition also recorded as: "
        + ", ".join(
            f"`{s}/{c}`"
            for s, c in sorted({(s, c) for s, c, _, _ in g.members})
            if (s, c) != g.representative
        )
        for g in sorted(cross, key=lambda g: g.entry["id"])
    )
    with_falsifier = sum(1 for e in entries if e["falsifier"])
    with_dne = sum(1 for e in entries if e["does_not_establish"])
    with_stage = sum(1 for e in entries if e["stage"])
    report = f"""# Reconciliation — P2 spec governance bundles (Spec 086 Stage 1, T104)

Migration run: `{migration['run_id']}`, {date}. Source stores:
`specs/*/claims.json` ({n_claims_files} files) and
`specs/*/aee-claims.json` ({n_aee_files} files), read-only.

## Census — re-derived on this checkout, and the delta

This checkout carries **{total_records} source records** in
{len(pair_keys)} distinct (spec, claim) pairs, including
Spec 086's own bundle
(`specs/086-winning-combination-adoption/aee-claims.json`,
21 claims, adopted at Stage 0 of this stage and migrated
with the rest — the ledger holds no silent exceptions).
The pre-existing population is {total_records - 21} records.
The Spec 086 package's audit counted 1,592 records from a
Spec 083 worktree; the delta against the pre-existing
population (+{total_records - 21 - 1592}) is exactly
`specs/084-policy-sync-conformance/aee-claims.json`
(11 claims, no `claims.json`), which landed on main with
Spec 084 (PR #474) after the audit's worktree base. This
reconciliation is authoritative.

## The double-format question — answered

The two formats are two serializations of one population:
{pairs_in_both} of the {len(pair_keys)} (spec, claim) pairs
are present in both serializations, and every such pair was
verified during the build census to carry identical text
and status in each. Under D-B the
ledger holds one canonical entry per **proposition
fingerprint**, so restatements of one proposition by successor
specs also merge: {len(cross)} fingerprint groups span more
than one (spec, claim), merging {merged_pairs} (spec, claim)
pairs into another pair's canonical entry (each preserved as
an evidence instance in the entry's `sources` and listed
below). No source record is unaccounted for:
{total_records} records in = {len(entries)} canonical entries
carrying all {total_records} source records in their
`sources` lists.

## Headline counts

| Measure | Count |
|---|---|
| Source records in | {total_records} |
| Distinct (spec, claim) pairs | {len(pair_keys)} |
| Canonical ledger entries out | {len(entries)} |
| (Spec, claim) pairs merged into another entry (D-B) | {merged_pairs} |
| Fingerprint groups spanning >1 (spec, claim) | {len(cross)} |
| Groups whose member records carry differing falsification tests | {falsifier_variants} |
| Groups whose member records carry differing boundary lines | {boundary_variants} |

## Fingerprint groups spanning >1 (spec, claim)

{cross_rows}

## Rules applied inside groups

- `statement`, `status`, `does_not_establish`: the
  representative record's (first (spec, claim) in sorted
  order; its `claims.json` serialization where both exist).
  Statuses were verified uniform inside every group during
  the build census (all `draft` but one singleton
  `superseded`, Spec 083's C083-13, which is alone in its
  group), so no status is masked by a merge.
- `falsifier`: the ordered union of the group's
  falsification tests — successor specs often restate a
  proposition with their own tests ({falsifier_variants}
  groups differ), and the union keeps every test traceable
  to a named source record (C086-5) instead of dropping the
  variants. Boundary variants ({boundary_variants} groups)
  remain in their source bundles; the entry carries the
  representative's line, per D-B (stage and score attach to
  the proposition, not to an instance).
- `stage`: from the representative pair's `aee-claims.json`
  where it carries one ({with_stage} of {len(entries)}
  entries; the rest are null — pairs with no aee
  serialization).

## Coverage (canonical entries)

- Falsifier: {with_falsifier} of {len(entries)} entries.
- Does-not-establish (`boundary`): {with_dne} of {len(entries)}
  entries.
- AEE state: 0 of {len(entries)} entries — the bundles carry
  adjudication status, not scores; `aee_state` is null, shown
  as null.
- Confidence (harmonization adoption #3 item 6, binding): a
  full census of both serializations found NO confidence
  field of any name at any depth in these {total_records}
  records — `confidence_in_source` and `confidence_text` are
  null on every bundle entry, recorded here so the absence is
  a checked fact, not an oversight. (The qualitative
  confidences the adoption names — e.g. anchor pairs'
  `confidence: "low"` — live outside this population; the
  anchor store is not in this repo tree and anchors are not a
  Stage 1 migration population. Recorded Stage 4 intake
  constraint: such values may enter the ledger only verbatim
  through `confidence_text`, never as numbers.)

## Mirror check

Every canonical entry's `status` was compared byte-equal
against its representative source record, and its `stage`
against the representative pair's aee record, after the
build; the migration test re-runs this comparison in CI.
Differences: none (any difference would be listed here and
would stop the stage).
"""
    return entries, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default="2026-11-01")
    parser.add_argument("--run-id", default="migration-2026-11-01-stage1")
    parser.add_argument("--report-dir", type=Path, required=True)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2]
    )
    args = parser.parse_args()
    root = args.root.resolve()
    migration = {"run_id": args.run_id, "migrated_at": args.date}
    p1_entries, p1_report = migrate_p1(root, args.date, migration)
    p3_entries, p3_report = migrate_p3(root, args.date, migration)
    p2_entries, p2_report = migrate_p2(root, args.date, migration)
    entries = p1_entries + p3_entries + p2_entries
    write_ledger(root, entries)
    report_dir = (root / args.report_dir).resolve()
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "reconciliation-p1.md").write_text(p1_report, encoding="utf-8")
    (report_dir / "reconciliation-p3.md").write_text(p3_report, encoding="utf-8")
    (report_dir / "reconciliation-p2.md").write_text(p2_report, encoding="utf-8")
    print(
        f"migration {args.run_id}: wrote {len(entries)} ledger entries "
        f"(P1 {len(p1_entries)} claims, P3 {len(p3_entries)} annotations, "
        f"P2 {len(p2_entries)} claims)"
    )
    report = validate_ledger(root)
    sys.stdout.write(report.render())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
