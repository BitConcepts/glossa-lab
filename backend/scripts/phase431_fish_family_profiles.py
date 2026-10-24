#!/usr/bin/env python3
"""Phase-431 — Spec 072 execution: Parpola's fish-sign
family, sign by sign, in ICIT numbering on the Shakti
corpus (the Spec 048 question, re-designed).

Frozen contract: specs/072-fish-family-profiles-redesign/
(spec.md as frozen 2026-10-22; freeze digest
3925f365bdc452031bb7356f9b357c6d5068da4a835afcfd75b0e9ffa3a69e92;
OSF contract registration filed at the freeze under
OPEN-072-7) under the runnable-experiments campaign.
Execution commissioned in the same owner tasking as
the freeze (2026-10-22).

Step 0 runs in the frozen order (spec section 3),
before any member's ending-follower fraction is
computed:

  0.1 Shakti intake assertion (P-F1 S1/S2) - the
      corpus and row-grades files (restricted-local,
      never committed) are recomputed against the
      merged intake record's pins and the census is
      reproduced; failure closes SHAKTI INTAKE NOT
      REPRODUCED.
  0.2 Asset F digest assertion - recomputed under
      Spec 044 section 4.2's exclusion rule against
      the frozen pin; absence closes ASSET F NOT
      AVAILABLE, mismatch ASSET F DIGEST MISMATCH.
  0.3 Concordance assertion - the freeze-pinned
      concordance (freeze.md section 4) is exhibited
      from the frozen record: five members identified
      (M048=243, M050=220, M060=235, M145=032,
      M147=033), two UNIDENTIFIED IN ICIT (M047,
      M052) under the confirmed DD-072-5 disposition.
  0.4 Positional classes and census (margins only) -
      per population under the carried cascade; if no
      identified member clears the carried supported
      floor in the primary population the run closes
      TOO THIN.
  0.5 Verdict-line assertion - the freeze-fixed
      L = 0.765 and its reference record
      (reference-distribution.json, sha256
      55d266b3...) are exhibited from the freeze
      record; absence closes INVALID.

Then the primary run (spec section 5) on the
documented-lineage population and the mandatory
sensitivity on documented + corroborated rows,
against the same L; grade-flips are findings
(section 5.4); the family word follows the frozen
majority partition (section 6). Outputs:
reports/phase431_results.json and
reports/phase431_report.md, under spec section 9's
headline rules. This record is internal under the
Roif gate (spec section 7, limit 1; claim
F072-C14); it is not a publication. The script is
deterministic: a second run reproduces both output
files byte-identically.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SPEC = _REPO / "specs/072-fish-family-profiles-redesign"
_HOME = Path.home()
_CORPUS = (
    _HOME / "workspace/research_notes/indus-data-deep-sweep-20261008"
    / "downloads/shaktiosindia-indus-sign-regimes-deposit/sanitized_corpus.json"
)
_GRADES = (
    _HOME / "workspace/research_notes/indus-data-deep-sweep-20261008"
    / "downloads/shakti_row_grades_2026-10-22.csv"
)

FREEZE_DIGEST = "3925f365bdc452031bb7356f9b357c6d5068da4a835afcfd75b0e9ffa3a69e92"
PIN_CORPUS = "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
PIN_GRADES = "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
PIN_ASSET_F = "ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3"
PIN_REF_DIST = "55d266b39969caf9ec020a3a941ec451760b05d983da3c6a419903addc73f4f5"
PIN_REGISTRY = "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
PIN_YAJNADEVAM = "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
VERDICT_LINE = 0.765

IDENTIFIED = {"M048": "243", "M050": "220", "M060": "235", "M145": "032", "M147": "033"}
UNIDENTIFIED = ["M047", "M052"]
MEMBER_ORDER = ["M047", "M048", "M050", "M052", "M060", "M145", "M147"]

S3_STATEMENT = (
    "This corpus is an ICIT-lineage corpus. Agreement between it and the "
    "program's earlier ICIT-lineage layer is consistency within one "
    "tradition, not independent corroboration."
)
ROIF_SENTENCE = "This record is internal under the Roif gate; it is not a publication."


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _gated(row) -> list:
    return [s for s in row["symbols"] if s != "000"]


def _classes(rows):
    pos = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        seq = _gated(r)
        if len(seq) < 2:
            continue
        for i, s in enumerate(seq):
            if i == 0:
                pos[s][0] += 1
            elif i == len(seq) - 1:
                pos[s][2] += 1
            else:
                pos[s][1] += 1
    totals = {s: sum(v) for s, v in pos.items()}
    classes = {}
    for s, (i, m, t) in pos.items():
        tot = i + m + t
        if tot < 5:
            classes[s] = None
            continue
        ir, mr, tr = i / tot, m / tot, t / tot
        if tr >= 0.60:
            c = "TERMINAL_STRONG"
        elif ir >= 0.55:
            c = "INITIAL_STRONG"
        elif mr >= 0.65:
            c = "MEDIAL_STRONG"
        elif tr >= 0.40:
            c = "TERMINAL_MODERATE"
        elif ir >= 0.40:
            c = "INITIAL_MODERATE"
        else:
            c = "MIXED"
        classes[s] = c
    return totals, classes


def _fraction(code, rows, classes):
    num = den = 0
    for r in rows:
        seq = _gated(r)
        for a, b in zip(seq, seq[1:]):
            if a == code:
                den += 1
                if classes.get(b) in ("TERMINAL_STRONG", "TERMINAL_MODERATE"):
                    num += 1
    return num, den


def _floor_class(total: int) -> str:
    if total < 10:
        return "NOT SCANNED"
    if total < 20:
        return "SCANNED - BELOW SUPPORTED FLOOR"
    return "TESTABLE"


def _population_test(rows, classes, totals):
    members = {}
    for key in MEMBER_ORDER:
        if key in UNIDENTIFIED:
            members[key] = {"disposition": "UNIDENTIFIED IN ICIT", "icit_code": None}
            continue
        code = IDENTIFIED[key]
        total = totals.get(code, 0)
        num, den = _fraction(code, rows, classes)
        frac = (num / den) if den else None
        scanned = total >= 10
        carried_supported = bool(scanned and total >= 20 and frac is not None and frac > 0.15)
        tested = total >= 20
        passes = bool(tested and frac is not None and frac >= VERDICT_LINE)
        members[key] = {
            "icit_code": code,
            "total": total,
            "floor_class": _floor_class(total),
            "bigrams": den,
            "ending_followers": num,
            "fraction": frac,
            "carried_label": (
                "supported" if carried_supported else "not supported"
            ) if scanned else "not scanned",
            "tested": tested,
            "pass": passes if tested else None,
        }
    tested = {k: m for k, m in members.items() if m.get("tested")}
    passing = {k: m for k, m in tested.items() if m["pass"]}
    tested_total = sum(m["total"] for m in tested.values())
    passing_total = sum(m["total"] for m in passing.values())
    w = (passing_total / tested_total) if tested_total else None
    identified_total = sum(
        m["total"] for m in members.values() if m.get("icit_code")
    )
    untested_total = identified_total - tested_total
    coverage_fires = bool(tested_total and untested_total > tested_total)
    if not tested:
        word = None
    elif coverage_fires or w == 0.5:
        word = "INCONCLUSIVE"
    elif w > 0.5:
        word = "FAMILY SUPPORTED"
    else:
        word = "FAMILY NOT SUPPORTED"
    return {
        "members": members,
        "tested_total": tested_total,
        "passing_total": passing_total,
        "w": w,
        "identified_family_total": identified_total,
        "untested_identified_total": untested_total,
        "coverage_condition_fires": coverage_fires,
        "family_word": word,
    }


def main() -> int:
    results = {
        "phase": "Phase-431",
        "spec": "specs/072-fish-family-profiles-redesign/spec.md",
        "title": "Parpola's fish-sign family, sign by sign, in ICIT numbering on the Shakti corpus",
        "lineage_label": "Shakti corpus (ICIT-lineage), cited through the adopted intake record",
        "lineage_sentence": S3_STATEMENT,
        "claim_under_test": "parpola_2010_dravidian_solution_manual_002",
        "freeze_digest": FREEZE_DIGEST,
        "execution_date": "2026-10-22",
        "verdict_line": VERDICT_LINE,
        "restricted_local_products": (
            "none: the corpus and row-grades files are inputs held "
            "restricted-local; no row-level product is produced or committed"
        ),
    }
    gates = {}

    # ── Gate 0.1 — Shakti intake assertion (P-F1 S1/S2) ──
    if not _CORPUS.exists() or not _GRADES.exists():
        gates["0.1"] = {"gate": "shakti_intake", "verdict": "FAIL",
                        "closure": "SHAKTI INTAKE NOT REPRODUCED",
                        "detail": "restricted-local corpus or row-grades file absent"}
        results["gates"] = gates
        results["outcome"] = "SHAKTI INTAKE NOT REPRODUCED"
        _write(results)
        return 0
    corpus_sha = _sha(_CORPUS)
    grades_sha = _sha(_GRADES)
    corpus = json.loads(_CORPUS.read_text(encoding="utf-8"))
    with open(_GRADES, encoding="utf-8") as fh:
        grades = {r["shakti_id"]: r["grade"] for r in csv.DictReader(fh)}
    analyzable = [r for r in corpus if not all(s == "000" for s in r["symbols"])]
    gc = Counter(grades[r["id"]] for r in corpus)
    cisi = sum(
        1 for r in analyzable if (r.get("cisi") or "").strip() not in ("", "-")
    )
    census = {
        "rows": len(corpus),
        "analyzable": len(analyzable),
        "documented": gc["documented-lineage"],
        "corroborated": gc["undocumented-corroborated"],
        "uncorroborated": gc["undocumented-uncorroborated"],
        "cisi_on_analyzable": cisi,
        "true_sign_tokens": sum(
            1 for r in corpus for s in r["symbols"] if s != "000"
        ),
        "distinct_signs": len(
            {s for r in corpus for s in r["symbols"] if s != "000"}
        ),
        "sites": len({r["site"] for r in corpus}),
    }
    s1_ok = corpus_sha == PIN_CORPUS and grades_sha == PIN_GRADES
    s2_ok = (
        census["rows"] == 5704 and census["analyzable"] == 5536
        and census["documented"] == 3212 and census["corroborated"] == 2087
        and census["uncorroborated"] == 405 and census["cisi_on_analyzable"] == 4904
        and census["true_sign_tokens"] == 18065 and census["distinct_signs"] == 713
        and census["sites"] == 77
    )
    gates["0.1"] = {
        "gate": "shakti_intake", "verdict": "PASS" if (s1_ok and s2_ok) else "FAIL",
        "corpus_sha256": corpus_sha, "row_grades_sha256": grades_sha,
        "census": census,
    }
    if not (s1_ok and s2_ok):
        gates["0.1"]["closure"] = "SHAKTI INTAKE NOT REPRODUCED"
        results["gates"] = gates
        results["outcome"] = "SHAKTI INTAKE NOT REPRODUCED"
        _write(results)
        return 0

    # ── Gate 0.2 — Asset F digest assertion ──
    asset_path = _SPEC.parent / "044-fish-sign-coastal-residue/asset-f-fish-family.json"
    if not asset_path.exists():
        gates["0.2"] = {"gate": "asset_f_digest", "verdict": "FAIL",
                        "closure": "ASSET F NOT AVAILABLE"}
        results["gates"] = gates
        results["outcome"] = "ASSET F NOT AVAILABLE"
        _write(results)
        return 0
    asset = json.loads(asset_path.read_text(encoding="utf-8"))
    body = {k: v for k, v in asset.items() if k != "digest"}
    canonical = json.dumps(body, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    asset_digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    gates["0.2"] = {
        "gate": "asset_f_digest",
        "verdict": "PASS" if asset_digest == PIN_ASSET_F else "FAIL",
        "recomputed_digest": asset_digest,
        "member_count": asset["member_count"],
    }
    if asset_digest != PIN_ASSET_F:
        gates["0.2"]["closure"] = "ASSET F DIGEST MISMATCH"
        results["gates"] = gates
        results["outcome"] = "ASSET F DIGEST MISMATCH"
        _write(results)
        return 0

    # ── Gate 0.3 — concordance assertion (freeze-pinned act exhibited) ──
    registry_sha = _sha(_REPO / "data/crosswalks/canonical_sign_registry.csv")
    yajna_sha = _sha(_REPO / "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv")
    freeze_record = json.loads((_SPEC / "freeze.json").read_text(encoding="utf-8"))
    conc = freeze_record["definition"]["design"]["concordance"]
    conc_ok = (
        registry_sha == PIN_REGISTRY and yajna_sha == PIN_YAJNADEVAM
        and conc["identified"] == IDENTIFIED
        and conc["unidentified"] == UNIDENTIFIED
        and freeze_record["digest"] == FREEZE_DIGEST
    )
    gates["0.3"] = {
        "gate": "concordance", "verdict": "PASS" if conc_ok else "FAIL",
        "basis_sha256": {"registry": registry_sha, "yajnadevam_crosswalk": yajna_sha},
        "identified": IDENTIFIED, "unidentified": UNIDENTIFIED,
    }
    if not conc_ok:
        gates["0.3"]["closure"] = "INVALID"
        results["gates"] = gates
        results["outcome"] = "INVALID"
        _write(results)
        return 0

    # populations
    primary_rows = [r for r in corpus if grades[r["id"]] == "documented-lineage"]
    sensitivity_rows = [
        r for r in corpus
        if grades[r["id"]] in ("documented-lineage", "undocumented-corroborated")
    ]

    # ── Gate 0.4 — classes and census (margins only) ──
    prim_totals, prim_classes = _classes(primary_rows)
    sens_totals, sens_classes = _classes(sensitivity_rows)
    member_census = {}
    for key in MEMBER_ORDER:
        if key in UNIDENTIFIED:
            member_census[key] = {"disposition": "UNIDENTIFIED IN ICIT"}
        else:
            code = IDENTIFIED[key]
            member_census[key] = {
                "icit_code": code,
                "primary_total": prim_totals.get(code, 0),
                "primary_floor_class": _floor_class(prim_totals.get(code, 0)),
                "sensitivity_total": sens_totals.get(code, 0),
                "sensitivity_floor_class": _floor_class(sens_totals.get(code, 0)),
            }
    any_testable = any(
        v.get("primary_total", 0) >= 20 for v in member_census.values()
    )
    gates["0.4"] = {
        "gate": "classes_and_census",
        "verdict": "PASS" if any_testable else "FAIL",
        "member_census": member_census,
    }
    if not any_testable:
        gates["0.4"]["closure"] = "TOO THIN"
        results["gates"] = gates
        results["outcome"] = "TOO THIN"
        _write(results)
        return 0

    # ── Gate 0.5 — verdict-line assertion ──
    ref_sha = _sha(_SPEC / "reference-distribution.json")
    line_def = freeze_record["definition"]["design"]["verdict_line"]
    line_ok = (
        ref_sha == PIN_REF_DIST and line_def["L"] == VERDICT_LINE
        and line_def["reference_record"]["sha256"] == PIN_REF_DIST
    )
    gates["0.5"] = {
        "gate": "verdict_line", "verdict": "PASS" if line_ok else "FAIL",
        "L": VERDICT_LINE, "reference_record_sha256": ref_sha,
    }
    if not line_ok:
        gates["0.5"]["closure"] = "INVALID"
        results["gates"] = gates
        results["outcome"] = "INVALID"
        _write(results)
        return 0
    results["gates"] = gates

    # ── Primary run + sensitivity ──
    primary = _population_test(primary_rows, prim_classes, prim_totals)
    sensitivity = _population_test(sensitivity_rows, sens_classes, sens_totals)
    results["primary"] = primary
    results["sensitivity"] = sensitivity

    flips = []
    for key in MEMBER_ORDER:
        pm = primary["members"].get(key, {})
        sm = sensitivity["members"].get(key, {})
        if not pm.get("icit_code"):
            continue
        for field, label in (("carried_label", "carried supported label"),
                             ("pass", "PASS word")):
            if pm.get(field) != sm.get(field):
                flips.append({
                    "member": key, "icit_code": pm["icit_code"], "field": label,
                    "primary_value": pm.get(field),
                    "sensitivity_value": sm.get(field),
                    "primary_fraction": pm.get("fraction"),
                    "sensitivity_fraction": sm.get("fraction"),
                    "primary_total": pm.get("total"),
                    "sensitivity_total": sm.get("total"),
                })
    family_flip = primary["family_word"] != sensitivity["family_word"]
    results["grade_flips"] = flips
    results["family_grade_sensitive"] = family_flip
    results["outcome"] = primary["family_word"]
    _write(results)
    return 0


def _fmt_frac(f) -> str:
    return "—" if f is None else f"{f:.4f}"


def _member_table(test) -> str:
    lines = [
        "| Member | ICIT | Total | Bigrams | Ending followers | Fraction | Carried label | PASS (vs L = 0.765) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for key in MEMBER_ORDER:
        m = test["members"][key]
        if not m.get("icit_code"):
            lines.append(f"| {key} | UNIDENTIFIED IN ICIT | — | — | — | — | — | — |")
            continue
        lines.append(
            f"| {key} | {m['icit_code']} | {m['total']} | {m['bigrams']} | "
            f"{m['ending_followers']} | {_fmt_frac(m['fraction'])} | "
            f"{m['carried_label']} | "
            f"{'PASS' if m['pass'] else ('does not pass' if m['tested'] else 'not tested')} |"
        )
    return "\n".join(lines)


def _write(results: dict) -> None:
    out_json = _REPO / "reports/phase431_results.json"
    out_json.write_text(
        json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    outcome = results["outcome"]
    primary = results.get("primary")
    sensitivity = results.get("sensitivity")
    flips = results.get("grade_flips", [])
    lines = []
    lines.append("# Phase-431 report — Spec 072 (fish-sign family, ICIT numbering, Shakti corpus)")
    lines.append("")
    lines.append("## Headline block")
    lines.append("")
    lines.append(f"1. {S3_STATEMENT}")
    lines.append(
        "2. Asset F digest `ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3`, "
        "7 members; dispositions: M048 identified as ICIT 243; M050 as 220; M060 as 235; "
        "M145 as 032; M147 as 033; M047 and M052 UNIDENTIFIED IN ICIT (excluded from both "
        "populations' weighting under the freeze-ruled disposition; their occurrence share "
        "in ICIT space cannot be measured). Gate-0.3 cross-check: Asset F holds none of the "
        "claim record's trio (72, 64, 70) and, of the Phase-43 six (267, 72, 65, 59, 60, 70), "
        "only 60, as M060. Named divergence: the concordance basis's depiction notes for "
        "P145, P147 and P047 differ from Asset F's depiction notes for the same Parpola "
        "numbers (freeze.md section 4)."
    )
    lines.append(
        "3. Corpus: the Shakti corpus as pinned at gate 0.1 (SHA-256 345241b1…), cited "
        "through the intake record docs/decisions/2026-10-22-shakti-corpus-intake-record.md. "
        "Populations: primary = documented-lineage rows only; sensitivity = documented + "
        "undocumented-corroborated rows."
    )
    lines.append(
        "4. Verdict line L = 0.765 — derived at the freeze as the 95th percentile "
        "(nearest-rank, rank 82 of 86) of the reference distribution of 86 non-fish signs "
        "on the primary population (reference record: specs/072-fish-family-profiles-"
        "redesign/reference-distribution.json, SHA-256 55d266b39969caf9ec020a3a941ec4517"
        "60b05d983da3c6a419903addc73f4f5)."
    )
    if primary and sensitivity:
        lines.append("5. Per-member tables, both populations: below.")
        w_pct = f"{primary['w'] * 100:.1f}" if primary["w"] is not None else "—"
        if outcome == "FAMILY SUPPORTED":
            head = (
                f"6. FAMILY SUPPORTED: \"Tested sign by sign across the fish family fixed "
                f"in advance by Asset F (digest ca5fb1b5…), in ICIT numbering on the "
                f"Shakti corpus (documented-lineage rows only), members carrying {w_pct}% "
                f"of the family's tested occurrences pass the freeze-fixed ending-follower "
                f"criterion (line L = 0.765, derived at the freeze from the reference "
                f"distribution of 86 non-fish signs on this corpus). The family behaves, "
                f"in its token-weighted majority, the way the 'meen' reading predicts. "
                + ("The documented + corroborated sensitivity returns the same family "
                   "verdict." if not results["family_grade_sensitive"] else
                   f"GRADE-SENSITIVE: the documented + corroborated sensitivity returns "
                   f"{sensitivity['family_word']} — see the grade-flip findings in the "
                   f"first section.")
                + " This does not establish that any fish sign was pronounced 'meen': "
                "positional behaviour is a necessary shadow of the reading, not the reading.\""
            )
        elif outcome == "FAMILY NOT SUPPORTED":
            head = (
                f"6. FAMILY NOT SUPPORTED: \"Tested sign by sign across the fish family "
                f"fixed in advance by Asset F (digest ca5fb1b5…), in ICIT numbering on "
                f"the Shakti corpus (documented-lineage rows only), members carrying only "
                f"{w_pct}% of the family's tested occurrences pass the freeze-fixed "
                f"ending-follower criterion (line L = 0.765). The family's token-weighted "
                f"majority is not followed by text-ending behaviour at the rate the "
                f"freeze-fixed line requires, and the claim "
                f"parpola_2010_dravidian_solution_manual_002 is recorded as not supported "
                f"as a family claim on this corpus. "
                + ("The documented + corroborated sensitivity returns the same family "
                   "verdict." if not results["family_grade_sensitive"] else
                   f"GRADE-SENSITIVE: the documented + corroborated sensitivity returns "
                   f"{sensitivity['family_word']} — see the grade-flip findings in the "
                   f"first section.")
                + " This does not establish what any fish sign meant or was pronounced, "
                "and it is not a verdict on the Phase-43 or Spec 048 records, which stand "
                "exactly as recorded.\""
            )
        else:
            reason = (
                "the passing members carry exactly 50% of tested occurrences"
                if primary["w"] == 0.5 else
                f"the coverage condition fired — untested identified members carry "
                f"{primary['untested_identified_total']} of the identified family's "
                f"occurrences, more than the tested members' {primary['tested_total']}"
            )
            head = (
                f"6. INCONCLUSIVE: \"Tested sign by sign across the fish family fixed in "
                f"advance by Asset F (digest ca5fb1b5…), in ICIT numbering on the Shakti "
                f"corpus, the result is inconclusive: {reason}. The claim stands exactly "
                f"as recorded — partially supported, family split unresolved.\""
            )
        lines.append(head)
    else:
        lines.append(f"6. Outcome: {outcome} (step-0 closure; see the results JSON gates).")
    lines.append(f"7. {ROIF_SENTENCE}")
    lines.append("")
    lines.append("## Grade-flip findings (first section)")
    lines.append("")
    if flips:
        for f in flips:
            lines.append(
                f"- **{f['member']}** (ICIT {f['icit_code']}): {f['field']} flips — "
                f"primary {f['primary_value']} (fraction {_fmt_frac(f['primary_fraction'])}, "
                f"total {f['primary_total']}) → sensitivity {f['sensitivity_value']} "
                f"(fraction {_fmt_frac(f['sensitivity_fraction'])}, total {f['sensitivity_total']})."
            )
    else:
        lines.append("- No member's carried label or PASS word changes between the two populations.")
    if results.get("family_grade_sensitive"):
        lines.append(
            f"- **Family-level flip:** primary {primary['family_word']} vs sensitivity "
            f"{sensitivity['family_word']} — the headline is GRADE-SENSITIVE."
        )
    lines.append("")
    if primary and sensitivity:
        lines.append("## Primary population (documented-lineage rows only)")
        lines.append("")
        lines.append(_member_table(primary))
        lines.append("")
        lines.append(
            f"Tested members carry {primary['tested_total']} occurrences; passing members "
            f"carry {primary['passing_total']} (w = {_fmt_frac(primary['w'])}). Family word: "
            f"**{primary['family_word']}**."
        )
        lines.append("")
        lines.append("## Sensitivity population (documented + undocumented-corroborated)")
        lines.append("")
        lines.append(_member_table(sensitivity))
        lines.append("")
        lines.append(
            f"Tested members carry {sensitivity['tested_total']} occurrences; passing members "
            f"carry {sensitivity['passing_total']} (w = {_fmt_frac(sensitivity['w'])}). Family word: "
            f"**{sensitivity['family_word']}**."
        )
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*AI disclosure: executed by an AI agent (Muse, via Muse) at the "
                 "direction of Tristen Pierson, per constitution §VI.*")
    lines.append("")
    (_REPO / "reports/phase431_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


if __name__ == "__main__":
    sys.exit(main())
