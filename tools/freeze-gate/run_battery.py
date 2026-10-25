#!/usr/bin/env python3
"""C1 kill-test battery runner — correctness-bearing freeze gate.

Runs the current AEE evaluator over the four fixed battery cases in
tools/freeze-gate/battery/ and files the results in
tools/freeze-gate/battery/results/ (battery-result.json +
battery-result.md, with the raw evaluator outputs under raw/).

Configuration, stated once and recorded in the result: the freeze
configuration, as the programme's freezes run the gate (lenient load,
evidence verification off, no ledger). Case (iv) is additionally run
with evidence verification on, because C3 is the component aimed at
its defect class; both runs are recorded, and the case's flagged /
blind-spot determination rests on BOTH runs together (flagged if
either run raises a correctness finding against the defect).

A claim's failure is a CORRECTNESS finding unless it is an FR-2.3
draft-cap record (the register-hygiene finding every draft register
carries). But a case is "flagged" only if a correctness finding
ADDRESSES THE CASE'S DEFECT — matching the case's catch_criteria in
cases.json (e.g. a falsifiability challenge naming the empty test).
Hygiene-class findings (independence modelling, boundary form)
fire on sound registers too (27 of them fired on Spec 074's sound
register at its freeze); counting them as catches would be exactly
the smoothing-over this battery exists to prevent. All findings
are recorded either way, marked as addressing the defect or not.
If the evaluator cannot be run against a case at all (e.g. it
extracts zero claims from a prose design), that is recorded as a
blind spot with the reason, per the design.

Usage:  python tools/freeze-gate/run_battery.py [--aee /path/to/aee]
Env:    AEE_BIN overrides the evaluator binary location.
Exit:   0 if the battery ran (whatever it found); 2 if the
        evaluator binary itself could not be located/run at all.
"""

import argparse
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
BATTERY = HERE / "battery"
RESULTS = BATTERY / "results"
REPO_ROOT = HERE.parents[1]


def find_aee(explicit=None):
    candidates = []
    if explicit:
        candidates.append(explicit)
    if os.environ.get("AEE_BIN"):
        candidates.append(os.environ["AEE_BIN"])
    candidates.append(str(pathlib.Path.home() / "workspace" / "venvs" / "glossa-aee153" / "bin" / "aee"))
    candidates.append("aee")
    for c in candidates:
        try:
            r = subprocess.run([c, "--version"], capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                return c, r.stdout.strip().split()[-1]
        except (OSError, subprocess.TimeoutExpired):
            continue
    return None, None


def is_draft_cap(failure):
    fid = failure.get("id", "")
    return fid.endswith("DRAFT-CAP") or failure.get("challenge") == "Draft outcome cap"


def assess(aee, input_path, project_root, out_dir, verify_evidence=False):
    """Run one assessment; return (parsed_output, error_string_or_None)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "aee-output.json"
    eval_json = out_dir / "evaluator-output.json"
    cmd = [
        aee, "assess",
        "--input", str(input_path),
        "--lenient", "--no-ledger",
        "--project-root", str(project_root),
        "--output", str(out_json),
        "--evaluator-output", str(eval_json),
    ]
    if verify_evidence:
        cmd.append("--verify-evidence")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if not out_json.exists():
        return None, (r.stderr or r.stdout or "evaluator produced no output")[-2000:]
    try:
        return json.loads(out_json.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"evaluator output not parseable: {e}"


def correctness_findings(parsed):
    findings = []
    for claim in parsed.get("claims", []):
        for f in claim.get("failures", []):
            if not is_draft_cap(f):
                findings.append({
                    "claim_id": claim.get("id"),
                    "id": f.get("id"),
                    "challenge": f.get("challenge"),
                    "breakpoint": (f.get("breakpoint") or "")[:400],
                })
    return findings


def addresses_defect(findings, criteria):
    """A finding counts as catching the case only if its text names the
    defect (the case's catch_criteria, from cases.json). Hygiene-class
    findings (independence modelling, boundary form) fire on sound
    registers too and never count — counting them would be exactly
    the smoothing-over this battery exists to prevent."""
    hits = []
    for f in findings:
        # Match on the finding's id + challenge name only. Breakpoint
        # prose is boilerplate that recites the whole scoring model
        # (it mentions "falsifiability" while explaining an unrelated
        # independence finding) — matching it manufactures catches.
        text = f"{f.get('id', '')} {f.get('challenge', '')}".lower()
        if any(re.search(c, text) for c in criteria):
            hits.append(f)
    return hits


def hygiene_count(parsed):
    n = 0
    for claim in parsed.get("claims", []):
        n += sum(1 for f in claim.get("failures", []) if is_draft_cap(f))
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aee", default=None)
    args = ap.parse_args()

    aee, version = find_aee(args.aee)
    if not aee:
        print("FATAL: no runnable AEE evaluator binary found", file=sys.stderr)
        return 2

    manifest = json.loads((BATTERY / "cases.json").read_text(encoding="utf-8"))
    run_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    case_results = []

    if True:
        project_root = REPO_ROOT
        for case in manifest["cases"]:
            cdir = BATTERY / case["dir"]
            input_path = cdir / case["input"]
            entry = {
                "case_id": case["id"],
                "name": case["name"],
                "defect_class": case["defect_class"],
                "expected_catcher": case["expected_catcher"],
                "input": f"tools/freeze-gate/battery/{case['dir']}/{case['input']}",
                "ran": False,
                "flagged": False,
                "correctness_findings": [],
                "blind_spot": None,
                "run_error": None,
            }
            raw_dir = RESULTS / "raw" / case["dir"]
            parsed, err = assess(aee, input_path, project_root, raw_dir / "freeze-config")
            if parsed is None:
                entry["run_error"] = f"evaluator could not be run against this case in the freeze configuration: {err}"
                entry["blind_spot"] = (
                    "The evaluator cannot be run against this case in its current form, "
                    f"so the gate has no reading on this defect class at all. Reason recorded: {err}"
                )
                case_results.append(entry)
                continue
            entry["ran"] = True
            probe = case.get("score_probe")
            if probe:
                comp = (
                    parsed.get("scores", {}).get(probe["claim_id"], {})
                    .get("components", {}).get(probe["component"])
                )
                entry["score_probe"] = {**probe, "value": comp}
            entry["claims_assessed"] = len(parsed.get("claims", []))
            entry["assessment_outcome"] = parsed.get("outcome")
            entry["draft_cap_findings"] = hygiene_count(parsed)
            entry["determination_rule"] = case["determination_rule"]
            findings = correctness_findings(parsed)

            if case["id"] == "iv":
                parsed_v, err_v = assess(aee, input_path, project_root, raw_dir / "verify-on", verify_evidence=True)
                entry["verify_evidence_run"] = {}
                if parsed_v is None:
                    entry["verify_evidence_run"]["error"] = err_v
                else:
                    vf = correctness_findings(parsed_v)
                    entry["verify_evidence_run"] = {
                        "claims_assessed": len(parsed_v.get("claims", [])),
                        "assessment_outcome": parsed_v.get("outcome"),
                        "correctness_findings": vf,
                    }
                    findings = findings + vf

            hits = addresses_defect(findings, case["catch_criteria"])
            entry["correctness_findings"] = findings
            entry["findings_addressing_the_defect"] = hits
            entry["flagged"] = len(hits) > 0
            if not entry["flagged"]:
                entry["blind_spot"] = case["blind_spot_if_unflagged"]
            case_results.append(entry)

    result = {
        "record_type": "c1-battery-result",
        "schema_version": "1.0",
        "evaluator": "aee (applied-epistemic-engineering)",
        "evaluator_version": version,
        "configuration": "lenient load; evidence verification off (freeze configuration); case iv additionally run with evidence verification on",
        "run_at": run_at,
        "cases": case_results,
        "blind_spots": [
            {"case_id": c["case_id"], "defect_class": c["defect_class"], "blind_spot": c["blind_spot"]}
            for c in case_results if c["blind_spot"]
        ],
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "battery-result.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")

    lines = [
        "# C1 kill-test battery — results",
        "",
        f"Evaluator: `aee` **{version}** (applied-epistemic-engineering), run {run_at}.",
        "Configuration: the freeze configuration (lenient load, evidence verification off,",
        "no ledger). Case (iv) was additionally run with evidence verification on; its",
        "determination rests on both runs. A finding counts as a correctness finding",
        "unless it is an FR-2.3 draft-cap record (register hygiene, carried by every",
        "draft register). Raw evaluator outputs: `raw/` beside this file.",
        "",
    ]
    for c in case_results:
        lines.append(f"## Case ({c['case_id']}) — {c['name']}")
        lines.append("")
        lines.append(f"Defect class: {c['defect_class']}.")
        lines.append(f"Expected catcher: {c['expected_catcher']}.")
        if c["run_error"]:
            lines.append(f"**The evaluator could not be run against this case.** {c['run_error']}")
        else:
            lines.append(
                f"Assessed {c.get('claims_assessed')} claim(s); assessment outcome "
                f"`{c.get('assessment_outcome')}`; {c.get('draft_cap_findings')} draft-cap "
                f"finding(s); {len(c['correctness_findings'])} non-draft-cap finding(s), of "
                f"which {len(c['findings_addressing_the_defect'])} address this case's defect."
            )
            lines.append(f"Determination rule: {c['determination_rule']}")
            if c.get("score_probe"):
                sp = c["score_probe"]
                lines.append(
                    f"Score probe: claim {sp['claim_id']}'s {sp['component']} component "
                    f"scored {sp['value']} — the evaluator grades the falsifier's "
                    "presence, not its content."
                )
            for f in c["correctness_findings"]:
                marker = "ADDRESSES THE DEFECT" if f in c["findings_addressing_the_defect"] else "does not address the defect"
                lines.append(f"- FINDING on {f['claim_id']}: {f['challenge']} ({f['id']}) — {marker}")
            if "verify_evidence_run" in c:
                v = c["verify_evidence_run"]
                if "error" in v:
                    lines.append(f"Evidence-verification run errored: {v['error']}")
                else:
                    lines.append(
                        f"Evidence-verification run: {v['claims_assessed']} claim(s), "
                        f"outcome `{v['assessment_outcome']}`, "
                        f"{len(v['correctness_findings'])} correctness finding(s)."
                    )
        if c["flagged"]:
            lines.append("**Result: FLAGGED — the evaluator catches this case.**")
        else:
            lines.append(f"**Result: NOT FLAGGED — NAMED BLIND SPOT.** {c['blind_spot']}")
        lines.append("")
    lines.append("## What this battery does and does not establish")
    lines.append("")
    lines.append("It establishes whether the current evaluator, as the freezes run it,")
    lines.append("flags these four named defect classes — nothing more. It does not")
    lines.append("establish that the evaluator catches any other class of defect, and")
    lines.append("a flagged case does not make the gate a correctness check on its own:")
    lines.append("C2 and C3 carry the classes the evaluator is blind to, and C4 is what")
    lines.append("makes any of it mechanical.")
    lines.append("")
    (RESULTS / "battery-result.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"battery run complete: aee {version}; "
          f"flagged: {[c['case_id'] for c in case_results if c['flagged']]}; "
          f"blind spots: {[c['case_id'] for c in case_results if c['blind_spot']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
