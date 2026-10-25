#!/usr/bin/env python3
"""C4 — the mechanical freeze-gate check. It reads files, not attestations.

For each spec directory it is pointed at, the check fails unless the
spec's gate-records/ directory carries, in the tree being checked:

  (a) c1-battery-result.json — a C1 battery result for the CURRENT
      evaluator version (tools/freeze-gate/evaluator-version.txt),
      covering all four battery cases, each case either flagged or
      carrying its named blind spot;
  (b) c2-spotcheck.json — a valid C2 record (freeze_records.py)
      whose gate-turning quantities all checked out;
  (c) c3-evidence-sample.json — a valid C3 record with verification
      on and no unverified verdict-bearing claim.

HARDENING (2026-10-25, programme red team finding D-1): a fully
fabricated record set passed this check end-to-end. The validators
now derive C2 status from the filed values, require the C2
recomputation to be filed, require a named C3 verifier distinct
from the drafter with evidence refs for every sampled claim,
require at least one gate-turning quantity, and match the C1
record's determinations against the canonical battery output.
Honest bound: a mechanical check enforces consistency, not
proof that work was done — that remains the human records' job.

ENFORCEMENT STATE (recorded honestly, per the build decision of
2026-10-25): this check runs in CI as a NON-REQUIRED job. The first
strengthened freeze (the endings atlas) is a shadow freeze — the
gate runs in full and is reported; branch protection starts
requiring this check with the freeze after the shadow.

Modes:
  check_freeze_gate.py <spec-dir> [<spec-dir> ...]
  check_freeze_gate.py --all                 # every specs/*/ with gate-records/
  check_freeze_gate.py --pr-scope --base REF # spec/demo dirs whose freeze.json
                                             # or gate-records/ changed vs REF
Exit 0 = every checked directory passes; 1 = at least one failure.
"""

import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from freeze_records import validate_c2, validate_c3  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
EXPECTED_CASES = {"i", "ii", "iii", "iv"}
# PR-scope watches specs/ only. The demonstration fixtures under
# tools/freeze-gate/demo/fixtures/ are the machinery tests' corpus
# (they include deliberately failing record sets, so triggering on
# them would fail any PR that touches the tooling itself);
# demonstration PRs exercise this same code path by copying a
# fixture into a scratch specs/ directory.
PR_SCOPE_ROOTS = ("specs/",)


def current_evaluator_version():
    return (HERE / "evaluator-version.txt").read_text(encoding="utf-8").strip()


def check_battery(records_dir, problems):
    path = records_dir / "c1-battery-result.json"
    if not path.exists():
        problems.append("C1: gate-records/c1-battery-result.json is missing")
        return
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        problems.append(f"C1: battery result is not valid JSON ({e})")
        return
    if rec.get("record_type") != "c1-battery-result":
        problems.append("C1: battery result record_type is not c1-battery-result")
    want = current_evaluator_version()
    if rec.get("evaluator_version") != want:
        problems.append(
            f"C1: battery result is for evaluator {rec.get('evaluator_version')!r}, "
            f"not the current evaluator {want!r} — re-run tools/freeze-gate/run_battery.py"
        )
    cases = {c.get("case_id"): c for c in rec.get("cases", [])}
    if set(cases) != EXPECTED_CASES:
        problems.append(f"C1: battery result covers cases {sorted(cases)}, expected {sorted(EXPECTED_CASES)}")
    # D-1 hardening (2026-10-25): the filed record's determinations
    # must match the canonical battery output produced by
    # run_battery.py for the current evaluator version. Before this
    # change only the version string was compared, so a record
    # claiming the opposite determinations passed.
    canonical_path = HERE / "battery" / "results" / "battery-result.json"
    if canonical_path.exists():
        try:
            canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            canonical = None
        if canonical and canonical.get("evaluator_version") == want:
            canon_cases = {c.get("case_id"): c for c in canonical.get("cases", [])}
            for cid, c in cases.items():
                cc = canon_cases.get(cid)
                if cc is not None and isinstance(c.get("flagged"), bool) and c["flagged"] != cc.get("flagged"):
                    problems.append(
                        f"C1: case {cid} claims flagged={c['flagged']} but the canonical battery result "
                        f"for evaluator {want} records flagged={cc.get('flagged')} — the filed record must "
                        f"be the battery's own output (tools/freeze-gate/run_battery.py)"
                    )
    for cid, c in cases.items():
        if not isinstance(c.get("flagged"), bool):
            problems.append(f"C1: case {cid} has no boolean flagged determination")
        elif c["flagged"] is False and not (c.get("blind_spot") or "").strip():
            problems.append(f"C1: case {cid} is unflagged but names no blind spot")


def check_record(records_dir, filename, validator, label, problems):
    path = records_dir / filename
    if not path.exists():
        problems.append(f"{label}: gate-records/{filename} is missing")
        return
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        problems.append(f"{label}: {filename} is not valid JSON ({e})")
        return
    for p in validator(rec):
        problems.append(f"{label}: {p}")


def check_spec_dir(spec_dir):
    spec_dir = pathlib.Path(spec_dir)
    records_dir = spec_dir / "gate-records"
    problems = []
    if not records_dir.is_dir():
        problems.append("gate-records/ directory is missing")
        return problems
    check_battery(records_dir, problems)
    check_record(records_dir, "c2-spotcheck.json", validate_c2, "C2", problems)
    check_record(records_dir, "c3-evidence-sample.json", validate_c3, "C3", problems)
    # D-1/D-6 hardening (2026-10-25): cross-record checks the single
    # record validators cannot make.
    def _load(name):
        try:
            return json.loads((records_dir / name).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
    c2 = _load("c2-spotcheck.json")
    c3 = _load("c3-evidence-sample.json")
    if c2 and c3:
        drafter = (c2.get("drafter") or "").strip()
        verifier = (c3.get("verifier") or "").strip()
        if drafter and verifier and (verifier == drafter or verifier.startswith(drafter)):
            problems.append("C3: verifier is the same identity as the C2 drafter — evidence verification must be by someone other than the drafter")
    claims_path = spec_dir / "claims.json"
    if c3 and claims_path.exists():
        try:
            bundle = json.loads(claims_path.read_text(encoding="utf-8"))
            register_ids = {c.get("id") for c in bundle.get("claims", [])}
        except (OSError, json.JSONDecodeError):
            register_ids = None
        if register_ids:
            record_ids = {c.get("claim_id") for c in c3.get("claims", [])}
            if record_ids != register_ids:
                missing = sorted(register_ids - record_ids)
                extra = sorted(record_ids - register_ids)
                problems.append(
                    f"C3: record covers {len(record_ids)} claims but the spec's claims.json registers {len(register_ids)}"
                    + (f"; missing from the record: {missing}" if missing else "")
                    + (f"; not in the register: {extra}" if extra else "")
                )
    return problems


def all_gate_record_dirs():
    out = []
    for d in sorted((REPO_ROOT / "specs").glob("*/gate-records")):
        out.append(d.parent)
    return out


def pr_scope_dirs(base):
    diff = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )
    if diff.returncode != 0:
        print(f"git diff failed: {diff.stderr}", file=sys.stderr)
        return None
    candidates = {}
    for line in diff.stdout.splitlines():
        path = line.strip()
        if not path.startswith(PR_SCOPE_ROOTS):
            continue
        parts = pathlib.PurePosixPath(path).parts
        # the spec/demo dir is the ancestor that holds freeze.json
        for depth in range(len(parts) - 1, 0, -1):
            cand = pathlib.Path(*parts[:depth])
            if (REPO_ROOT / cand / "freeze.json").exists():
                rel = "/".join(parts[:depth])
                trigger = parts[-1] == "freeze.json" or "gate-records" in parts
                candidates[rel] = candidates.get(rel, False) or trigger
                break
    return [REPO_ROOT / rel for rel, trig in candidates.items() if trig]


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    dirs = []
    if argv[0] == "--all":
        dirs = all_gate_record_dirs()
        if not dirs:
            print("C4: no specs carry gate-records/ yet — nothing to check (gate not yet in force for any freeze).")
            return 0
    elif argv[0] == "--pr-scope":
        base = argv[argv.index("--base") + 1] if "--base" in argv else "origin/main"
        dirs = pr_scope_dirs(base)
        if dirs is None:
            return 2
        if not dirs:
            print("C4: this change touches no freeze in scope — check passes trivially.")
            return 0
    else:
        dirs = [pathlib.Path(a) for a in argv]

    failed = 0
    for d in dirs:
        problems = check_spec_dir(d)
        label = d.relative_to(REPO_ROOT) if d.is_absolute() else d
        if problems:
            failed += 1
            print(f"C4 FAIL: {label}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"C4 PASS: {label}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
