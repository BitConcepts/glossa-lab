#!/usr/bin/env python3
"""C5 — published gate statistics, generated from the freeze records.

Regenerates docs/freeze-gate/gate-statistics.md from:
  - the canonical C1 battery result
    (tools/freeze-gate/battery/results/battery-result.json),
  - every specs/*/gate-records/ record on main (C2/C3 outcomes),
  - the count of legacy freeze-aee-note.md files (the register-
    discipline gate's freezes; counted, not parsed — their prose
    is not machine-read here, and the table says so).

Run it whenever a freeze lands or the battery is re-run:
  python tools/freeze-gate/gate_statistics.py
The first strengthened freeze record carries this table; until one
exists the table states that plainly.
"""

import datetime
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
OUT = REPO_ROOT / "docs" / "freeze-gate" / "gate-statistics.md"


def main():
    battery_path = HERE / "battery" / "results" / "battery-result.json"
    battery = json.loads(battery_path.read_text(encoding="utf-8")) if battery_path.exists() else None

    record_dirs = sorted((REPO_ROOT / "specs").glob("*/gate-records"))
    legacy_notes = sorted((REPO_ROOT / "specs").glob("*/aee/freeze-aee-note.md"))

    blocked = {"C1": 0, "C2": 0, "C3": 0}
    c2_mismatches = 0
    c3_unverified = 0
    strengthened = []
    for rd in record_dirs:
        spec = rd.parent.name
        strengthened.append(spec)
        c2p, c3p = rd / "c2-spotcheck.json", rd / "c3-evidence-sample.json"
        if c2p.exists():
            c2 = json.loads(c2p.read_text(encoding="utf-8"))
            if c2.get("outcome") != "PASS":
                blocked["C2"] += 1
            c2_mismatches += sum(
                1 for q in c2.get("quantities", [])
                if str(q.get("status", "")).startswith("mismatch")
            )
        if c3p.exists():
            c3 = json.loads(c3p.read_text(encoding="utf-8"))
            if c3.get("outcome") != "PASS":
                blocked["C3"] += 1
            c3_unverified += sum(
                1 for c in c3.get("claims", []) if c.get("verification") == "unverified"
            )

    today = datetime.date.today().isoformat()
    lines = [
        "# Freeze-gate statistics (C5)",
        "",
        f"Generated {today} by `tools/freeze-gate/gate_statistics.py` from the",
        "records on main. Do not edit by hand; regenerate.",
        "",
        "## The strengthened gate (C1–C4)",
        "",
        f"- Freezes carrying gate records so far: **{len(strengthened)}**"
        + (f" ({', '.join(strengthened)})" if strengthened else " — none yet."),
    ]
    if not strengthened:
        lines.append(
            "- The first strengthened freeze is the endings atlas, designated a "
            "SHADOW freeze in its design: the gate runs in full and is reported; "
            "the C4 check becomes a required branch-protection check with the "
            "freeze after it. Until then this table is the machinery's own "
            "readiness record, not a freeze record."
        )
    lines += [
        f"- Freezes blocked by C2 (spot-check outcome not PASS): **{blocked['C2']}**",
        f"- Freezes blocked by C3 (evidence-sample outcome not PASS): **{blocked['C3']}**",
        f"- C2 mismatches recorded (resolved + unresolved): **{c2_mismatches}**",
        f"- C3 unverified sampled claims recorded: **{c3_unverified}**",
        "",
        "## C1 battery (current evaluator)",
        "",
    ]
    if battery:
        lines.append(
            f"Evaluator `aee` {battery['evaluator_version']}, run {battery['run_at']} "
            f"({battery['configuration']})."
        )
        lines.append("")
        lines.append("| Case | Defect class | Result |")
        lines.append("|---|---|---|")
        for c in battery["cases"]:
            result = "flagged" if c["flagged"] else "NOT flagged — named blind spot"
            lines.append(f"| ({c['case_id']}) {c['name']} | {c['defect_class']} | {result} |")
        lines.append("")
        lines.append("Named blind spots, in plain words:")
        lines.append("")
        for b in battery["blind_spots"]:
            lines.append(f"- Case ({b['case_id']}), {b['defect_class']}: {b['blind_spot']}")
    else:
        lines.append("No battery result is filed yet.")
    lines += [
        "",
        "## The register-discipline gate (for scale)",
        "",
        f"- Freezes with an AEE freeze note on main: **{len(legacy_notes)}** "
        "(counted from `specs/*/aee/freeze-aee-note.md`; the notes are prose "
        "and are not parsed by this generator). Across those freezes the "
        "gate's recorded findings were FR-2.3 draft-cap hygiene records; it "
        "blocked no freeze. That is the finding (RT-01) this machinery answers.",
        "",
        "## What these statistics do and do not establish",
        "",
        "They summarise the gate's own records, arithmetically. They do not",
        "establish anything about past freezes, whose verdicts stand on their",
        "own records, and a quiet table (few blocks) does not by itself show",
        "the gate is weak or strong — the battery's blind spots above are the",
        "honest measure of what the evaluator, as operated, cannot see.",
        "",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
