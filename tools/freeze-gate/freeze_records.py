#!/usr/bin/env python3
"""C2 / C3 freeze-record tooling — correctness-bearing freeze gate.

Scaffolds and validates the two freeze-time records the C4 check
reads:

- C2 spot-check record (c2-spotcheck): an independent worker's
  recomputation of a sample of the quantities a freeze pins. Rule:
  EVERY gate-turning quantity, plus a random sample of the rest at
  fraction 25%, minimum 3 (decision record 2026-10-25).
- C3 evidence-sample record (c3-evidence-sample): evidence
  verification switched ON for a sample of the spec's claims. Rule:
  EVERY verdict-bearing claim, plus a random sample of at least
  20% of the remainder (design C3). The scaffold marks the sample;
  the verifier then reads each sampled claim's cited evidence
  against the claim and records the outcome — the engine resolves
  refs and hashes, the verifier judges support.

The scaffolder never fills in a recomputed value or a verification
outcome. Those come from the humans/processes the records name;
the validator checks structure and completeness only, which is
exactly what C4 can honestly enforce (the check reads files, not
attestations — and this tool is the files' shape).

Usage:
  freeze_records.py scaffold-c2 <spec-dir> --drafter NAME --recomputer NAME \
      --quantities quantities.json [--seed N] [--out PATH]
      (quantities.json: [{"name":..., "source_in_spec":..., "gate_turning":bool,
                          "pinned_value":...}, ...])
  freeze_records.py scaffold-c3 <spec-dir> --verdict-bearing ID [ID...] [--seed N] [--out PATH]
      (reads <spec-dir>/claims.json)
  freeze_records.py validate <record.json> [<record.json>...]
"""

import argparse
import json
import pathlib
import random
import sys

C2_FRACTION = 0.25
C2_MINIMUM = 3
C3_FRACTION = 0.20


def sample_rest(items, fraction, minimum, seed):
    """Deterministic random sample of the non-mandatory items."""
    if not items:
        return []
    k = max(minimum, -(-len(items) * int(fraction * 100) // 100))  # ceil(fraction * n)
    k = min(k, len(items))
    return random.Random(seed).sample(sorted(items), k)


def scaffold_c2(spec_dir, drafter, recomputer, quantities, seed):
    gate = [q for q in quantities if q["gate_turning"]]
    rest_names = [q["name"] for q in quantities if not q["gate_turning"]]
    sampled_rest = set(sample_rest(rest_names, C2_FRACTION, C2_MINIMUM, seed))
    entries = []
    for q in quantities:
        sampled = q["gate_turning"] or q["name"] in sampled_rest
        entries.append({
            "name": q["name"],
            "source_in_spec": q["source_in_spec"],
            "gate_turning": bool(q["gate_turning"]),
            "sampled": sampled,
            "pinned_value": q.get("pinned_value"),
            "recomputed_value": None,
            "status": "not-checked" if sampled else "not-sampled",
            "note": "",
        })
    return {
        "record_type": "c2-spotcheck",
        "schema_version": "1.0",
        "spec": spec_dir,
        "drafter": drafter,
        "recomputer": recomputer,
        "method": "Recomputed from the spec text and the pinned inputs only; the drafter's workings were not consulted.",
        "sample_rule": "every gate-turning quantity + random 25% (minimum 3) of the rest",
        "sample_seed": seed,
        "quantities": entries,
        "coverage": {
            "gate_turning_total": len(gate),
            "gate_turning_checked": 0,
            "other_total": len(rest_names),
            "other_sampled": len(sampled_rest),
            "other_checked": 0,
        },
        "outcome": "INCOMPLETE",
    }


def scaffold_c3(spec_dir, claims_path, verdict_bearing, seed):
    bundle = json.loads(pathlib.Path(claims_path).read_text(encoding="utf-8"))
    ids = [c["id"] for c in bundle["claims"]]
    vb = set(verdict_bearing)
    missing = vb - set(ids)
    if missing:
        raise SystemExit(f"verdict-bearing claim ids not in register: {sorted(missing)}")
    rest = [i for i in ids if i not in vb]
    sampled_rest = set(sample_rest(rest, C3_FRACTION, 1, seed))
    entries = []
    for cid in ids:
        sampled = cid in vb or cid in sampled_rest
        entries.append({
            "claim_id": cid,
            "verdict_bearing": cid in vb,
            "sampled": sampled,
            "verification": "pending" if sampled else "not-sampled",
            "evidence_refs_checked": [],
            "note": "",
        })
    return {
        "record_type": "c3-evidence-sample",
        "schema_version": "1.0",
        "spec": spec_dir,
        "claims_file": claims_path,
        "verification_mode": "on",
        "verifier": "",
        "sample_rule": "every verdict-bearing claim + random sample of at least 20% of the remainder",
        "sample_seed": seed,
        "claims": entries,
        "outcome": "INCOMPLETE",
    }


def validate_c2(rec):
    problems = []
    if rec.get("record_type") != "c2-spotcheck":
        return ["record_type is not c2-spotcheck"]
    qs = rec.get("quantities")
    if not qs:
        return ["quantities missing or empty"]
    for q in qs:
        for field in ("name", "source_in_spec", "gate_turning", "sampled", "pinned_value", "status"):
            if field not in q:
                problems.append(f"quantity {q.get('name', '?')}: missing field {field}")
        if q.get("gate_turning") and not q.get("sampled"):
            problems.append(f"gate-turning quantity {q.get('name')} was not sampled")
        if q.get("sampled") and q.get("status") not in ("agree", "mismatch-resolved", "mismatch-unresolved"):
            problems.append(f"quantity {q.get('name')}: sampled but status is {q.get('status')!r}")
        if q.get("status") == "mismatch-unresolved" and q.get("gate_turning"):
            problems.append(f"UNRESOLVED MISMATCH on gate-turning quantity {q.get('name')}")
    cov = rec.get("coverage") or {}
    gt = [q for q in qs if q.get("gate_turning")]
    if cov.get("gate_turning_total") != len(gt):
        problems.append("coverage.gate_turning_total does not match the quantities list")
    checked = [q for q in gt if q.get("status") in ("agree", "mismatch-resolved", "mismatch-unresolved")]
    if cov.get("gate_turning_checked") != len(checked):
        problems.append("coverage.gate_turning_checked does not match the quantities list")
    if rec.get("outcome") != "PASS":
        problems.append(f"outcome is {rec.get('outcome')!r}, not PASS")
    return problems


def validate_c3(rec):
    problems = []
    if rec.get("record_type") != "c3-evidence-sample":
        return ["record_type is not c3-evidence-sample"]
    if rec.get("verification_mode") != "on":
        problems.append("verification_mode is not 'on'")
    claims = rec.get("claims")
    if not claims:
        return problems + ["claims missing or empty"]
    for c in claims:
        for field in ("claim_id", "verdict_bearing", "sampled", "verification"):
            if field not in c:
                problems.append(f"claim {c.get('claim_id', '?')}: missing field {field}")
        if c.get("verdict_bearing") and not c.get("sampled"):
            problems.append(f"verdict-bearing claim {c.get('claim_id')} was not sampled")
        if c.get("sampled") and c.get("verification") not in ("verified", "unverified"):
            problems.append(f"claim {c.get('claim_id')}: sampled but verification is {c.get('verification')!r}")
        if c.get("verdict_bearing") and c.get("verification") == "unverified":
            problems.append(f"UNVERIFIED verdict-bearing claim {c.get('claim_id')}")
    if rec.get("outcome") != "PASS":
        problems.append(f"outcome is {rec.get('outcome')!r}, not PASS")
    return problems


def validate_record(path):
    rec = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    rt = rec.get("record_type")
    if rt == "c2-spotcheck":
        return validate_c2(rec)
    if rt == "c3-evidence-sample":
        return validate_c3(rec)
    return [f"unknown record_type {rt!r}"]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s2 = sub.add_parser("scaffold-c2")
    s2.add_argument("spec_dir")
    s2.add_argument("--drafter", required=True)
    s2.add_argument("--recomputer", required=True)
    s2.add_argument("--quantities", required=True)
    s2.add_argument("--seed", type=int, default=20261025)
    s2.add_argument("--out")

    s3 = sub.add_parser("scaffold-c3")
    s3.add_argument("spec_dir")
    s3.add_argument("--verdict-bearing", nargs="+", required=True)
    s3.add_argument("--seed", type=int, default=20261025)
    s3.add_argument("--out")

    sv = sub.add_parser("validate")
    sv.add_argument("records", nargs="+")

    args = ap.parse_args()
    if args.cmd == "scaffold-c2":
        quantities = json.loads(pathlib.Path(args.quantities).read_text(encoding="utf-8"))
        rec = scaffold_c2(args.spec_dir, args.drafter, args.recomputer, quantities, args.seed)
        out = args.out or str(pathlib.Path(args.spec_dir) / "gate-records" / "c2-spotcheck.json")
    elif args.cmd == "scaffold-c3":
        claims_path = str(pathlib.Path(args.spec_dir) / "claims.json")
        rec = scaffold_c3(args.spec_dir, claims_path, args.verdict_bearing, args.seed)
        out = args.out or str(pathlib.Path(args.spec_dir) / "gate-records" / "c3-evidence-sample.json")
    else:
        bad = 0
        for path in args.records:
            problems = validate_record(path)
            if problems:
                bad += 1
                print(f"{path}: INVALID")
                for p in problems:
                    print(f"  - {p}")
            else:
                print(f"{path}: valid")
        return 1 if bad else 0

    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(f"scaffold written: {out} (outcome INCOMPLETE until the work it records is done)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
