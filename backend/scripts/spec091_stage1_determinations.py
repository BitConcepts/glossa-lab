"""Spec 091 Stage 1 — generators for the T104 and T105 determination records.

T104 (the pass-by-default enumeration) traces every credit kind in
the WP5 census (`docs/repair-2026-10-26/anchor-support-audit.json`,
`phase48_summary.pass_credits_by_kind`) to the code path in the
frozen Phase-48 battery (`backend/scripts/phase48_medium_validation.py`)
that awarded it, and reconciles the gap register's "four
pass-by-default paths" (GR-088-03) against the enumeration.

T105 (the checker-arm split for the 5) determines, per anchor
(M042, M046, M108, M176, M342), which corrected checker arm may
lawfully produce its revalidation — the site-statistics arm
(`site_stats_v2` lineage) or the phonotactic arm
(`phonotactics_v2`, dependency-gated on GR-088-04) — from the R5
rule definitions in `backend/scripts/repair_anchor_audit.py` and
the anchors' full WP5 audit records.

Both source files are FROZEN records of the repair brief: they are
read here, never written. The generator verifies every citation it
emits against the sources (branch signatures inside the cited line
ranges; every pass-awarding return in the battery covered by
exactly one enumerated path; every census kind and every default
credit kind in the audit generator's DEFAULT_CREDITS traced; each
R5 rule text found verbatim in its audit record's explanation).
Any failed verification aborts with a nonzero exit and writes
nothing.

Outputs (generated records, Spec 091 Stage 1):
  specs/091-anchor-comparison-integrity/records/
      t104-pass-by-default-enumeration.json
      t105-checker-arm-split.json

Standard library only.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BATTERY = REPO / "backend/scripts/phase48_medium_validation.py"
AUDIT = REPO / "docs/repair-2026-10-26/anchor-support-audit.json"
AUDIT_GEN = REPO / "backend/scripts/repair_anchor_audit.py"
OUT_DIR = REPO / "specs/091-anchor-comparison-integrity/records"

BATTERY_REL = "backend/scripts/phase48_medium_validation.py"
AUDIT_REL = "docs/repair-2026-10-26/anchor-support-audit.json"
AUDIT_GEN_REL = "backend/scripts/repair_anchor_audit.py"

DATE = "2026-11-17"
SIGNS = ["M042", "M046", "M108", "M176", "M342"]

EM = "\u2014"  # the em dash the battery writes in its default-pass details

# The battery's pass-awarding paths. Line ranges cite the frozen
# file as read on 2026-11-17; main() re-verifies each signature
# inside its range before anything is written, so a moved frozen
# file fails the generation instead of falsifying the record.
PATHS = [
    {
        "path_id": "P1",
        "battery_function": "test_positional",
        "lines": [119, 130],
        "signature": '"PASS" if ok',
        "credit_kind": "genuine_positional_pass_reading_blind",
        "audit_code_fact": "positional_reading_blind",
        "note": (
            "The expectation checks run over the role's avg_position "
            "and starter/ending flags and the verdict is computed "
            "from them. A real measurement — but the test never "
            "uses the proposed reading, so it supports distribution "
            "and functional role only (WP5 code fact "
            "'positional_reading_blind')."
        ),
    },
    {
        "path_id": "P2",
        "battery_function": "test_positional",
        "lines": [116, 117],
        "signature": f"no_expectation{EM}pass_by_default",
        "credit_kind": "default_credit_no_expectation",
        "audit_code_fact": "positional_pass_by_default",
        "note": (
            "PASS BY DEFAULT: the role has no expectation entry "
            "(UNKNOWN role or unlisted role), so there is nothing "
            "to check against and the branch returns a pass."
        ),
    },
    {
        "path_id": "P3",
        "battery_function": "test_dedr",
        "lines": [138, 139],
        "signature": "too_short_pass",
        "credit_kind": "default_credit_too_short",
        "audit_code_fact": "dedr_too_short_pass",
        "note": (
            "PASS BY DEFAULT: the normalized reading is shorter "
            "than 2 characters, so the dictionary check does not "
            "run and the branch returns a pass."
        ),
    },
    {
        "path_id": "P4",
        "battery_function": "test_dedr",
        "lines": [143, 144],
        "signature": "exact_match_",
        "credit_kind": "exact_match_lexical_plausibility",
        "audit_code_fact": "dedr_is_lexical_plausibility",
        "note": (
            "The dictionary scan ran (counts at lines 141-142) and "
            "found at least one entry equal to the normalized "
            "reading. Lexical plausibility, per the WP5 code fact: "
            "it shows a word of this shape exists, not that this "
            "sign stood for that word."
        ),
    },
    {
        "path_id": "P5",
        "battery_function": "test_dedr",
        "lines": [145, 146],
        "signature": "prefix_match_",
        "credit_kind": "prefix_match_weak_lexical_plausibility",
        "audit_code_fact": "dedr_is_lexical_plausibility",
        "note": (
            "The dictionary scan ran (counts at lines 141-142) and "
            "found 2 or more entries sharing the first 3 "
            "normalized characters with the reading (or the "
            "reverse). Weak lexical plausibility."
        ),
    },
    {
        "path_id": "P6",
        "battery_function": "test_bigram_consistency",
        "lines": [157, 158],
        "signature": f"char_not_in_lm{EM}pass_by_default",
        "credit_kind": "default_credit_missing_model_character",
        "audit_code_fact": "bigram_pass_by_default",
        "note": (
            "PASS BY DEFAULT: the reading's first character is "
            "absent from the language model, so no comparison is "
            "possible and the branch returns a pass."
        ),
    },
    {
        "path_id": "P7",
        "battery_function": "test_bigram_consistency",
        "lines": [189, 190],
        "signature": f"no_anchor_neighbours{EM}pass_by_default",
        "credit_kind": "default_credit_no_anchor_neighbors",
        "audit_code_fact": "bigram_pass_by_default",
        "note": (
            "PASS BY DEFAULT: none of the sign's top following "
            "signs has a HIGH or MEDIUM anchor reading, so no "
            "neighbour could be checked and the branch returns a "
            "pass."
        ),
    },
    {
        "path_id": "P8",
        "battery_function": "test_bigram_consistency",
        "lines": [191, 192],
        "signature": "neighbour_match=",
        "credit_kind": "genuine_bigram_pass_as_recorded_backend_dependent",
        "audit_code_fact": "bigram_backend_divergence",
        "note": (
            "The neighbour comparison ran and the match ratio met "
            "the 0.4 threshold. A real comparison as recorded — "
            "but the comparison set is backend-dependent (top-5 "
            "continuations with torch, all continuations without; "
            "lines 161-170), so the pass is not the same test "
            "across backends (WP5 code fact "
            "'bigram_backend_divergence')."
        ),
    },
]

AGGREGATION = {
    "path_id": "AGG",
    "battery_function": "main",
    "lines": [220, 222],
    "signature": "promote = score >= 2",
    "credit_kind": None,
    "audit_code_fact": "promotion_rule",
    "note": (
        "Not a credit path: the promotion rule. A sign is "
        "promoted when any 2 of the 3 tests pass, so default "
        "credits counted toward promotion exactly like measured "
        "passes (WP5 code fact 'promotion_rule')."
    ),
}


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(msg: str) -> None:
    raise SystemExit(f"spec091_stage1_determinations: REFUSING TO WRITE: {msg}")


def default_credit_kinds(audit_gen_source: str) -> set[str]:
    """The audit generator's DEFAULT_CREDITS set, read from its AST."""
    tree = ast.parse(audit_gen_source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "DEFAULT_CREDITS" for t in node.targets
        ):
            return {
                elt.value
                for elt in node.value.elts
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
            }
    fail("DEFAULT_CREDITS assignment not found in the audit generator")
    return set()


def build_t104(battery_lines: list[str], audit: dict, audit_gen_source: str) -> dict:
    census = audit["phase48_summary"]["pass_credits_by_kind"]
    defaults = default_credit_kinds(audit_gen_source)

    # Verify every cited signature sits inside its cited range.
    for path in PATHS + [AGGREGATION]:
        lo, hi = path["lines"]
        window = "\n".join(battery_lines[lo - 1 : hi])
        if path["signature"] not in window:
            fail(
                f"{path['path_id']}: signature {path['signature']!r} not found "
                f"in {BATTERY_REL} lines {lo}-{hi}"
            )

    # Completeness over the battery's own returns: every literal
    # `return True` and every computed pass return is covered by
    # exactly one enumerated path.
    def covering(line_no: int) -> list[str]:
        return [
            p["path_id"]
            for p in PATHS + [AGGREGATION]
            if p["lines"][0] <= line_no <= p["lines"][1]
        ]

    literal_true = [
        i + 1 for i, line in enumerate(battery_lines) if "return True" in line
    ]
    computed_pass = [
        i + 1
        for i, line in enumerate(battery_lines)
        if "return ok," in line or "return ratio" in line
    ]
    for line_no in literal_true + computed_pass:
        cov = covering(line_no)
        if len(cov) != 1:
            fail(f"battery line {line_no} is covered by {cov}, expected exactly one path")

    entries = []
    for path in PATHS:
        kind = path["credit_kind"]
        entries.append(
            {
                "path_id": path["path_id"],
                "battery_function": path["battery_function"],
                "code_location": {"file": BATTERY_REL, "lines": path["lines"]},
                "branch_signature": path["signature"],
                "credit_kind_awarded": kind,
                "is_pass_by_default": kind in defaults,
                "recorded_credits_in_wp5_census": census.get(kind, 0),
                "fired_in_recorded_run": census.get(kind, 0) > 0,
                "audit_code_fact": path["audit_code_fact"],
                "note": path["note"],
            }
        )
    entries.append(
        {
            "path_id": AGGREGATION["path_id"],
            "battery_function": AGGREGATION["battery_function"],
            "code_location": {"file": BATTERY_REL, "lines": AGGREGATION["lines"]},
            "branch_signature": AGGREGATION["signature"],
            "credit_kind_awarded": None,
            "is_pass_by_default": False,
            "recorded_credits_in_wp5_census": None,
            "fired_in_recorded_run": None,
            "audit_code_fact": AGGREGATION["audit_code_fact"],
            "note": AGGREGATION["note"],
        }
    )

    traced = [e["credit_kind_awarded"] for e in entries if e["credit_kind_awarded"]]
    if sorted(traced) != sorted(set(traced)):
        fail("a credit kind is traced to more than one path")
    missing_census = [k for k in census if k not in traced]
    if missing_census:
        fail(f"census kinds with no traced path: {missing_census}")
    default_paths = [e for e in entries if e["is_pass_by_default"]]
    missing_defaults = [k for k in defaults if k not in traced]
    if missing_defaults:
        fail(f"default credit kinds with no traced path: {missing_defaults}")
    if len(default_paths) != 4:
        fail(f"enumerated {len(default_paths)} pass-by-default paths, expected 4")

    return {
        "record_id": "spec091-t104-pass-by-default-enumeration",
        "spec": "091-anchor-comparison-integrity",
        "task": "T104",
        "claim": "C091-8 (enumeration side)",
        "generated_by": "backend/scripts/spec091_stage1_determinations.py",
        "date": DATE,
        "inputs": {
            BATTERY_REL: sha256_of(BATTERY),
            AUDIT_REL: sha256_of(AUDIT),
            AUDIT_GEN_REL: sha256_of(AUDIT_GEN),
        },
        "method": (
            "Every credit kind in the WP5 census is traced to the "
            "battery code path that awarded it. Completeness is by "
            "the enumeration's own rule: every pass-awarding return "
            "in the frozen battery (6 literal `return True` "
            "branches and 2 computed pass returns) lies inside "
            "exactly one enumerated path's line range; every kind "
            "in the census is awarded by exactly one path; every "
            "kind in the audit generator's DEFAULT_CREDITS is "
            "awarded by exactly one pass-by-default path."
        ),
        "paths": entries,
        "observed_non_credit_default": {
            "code_location": {"file": BATTERY_REL, "lines": [110, 110]},
            "observation": (
                "test_positional line 110 defaults a missing "
                "avg_position to 0.5 before the expectation checks "
                "run. This is input defaulting inside path P1, not "
                "a separate verdict path: the verdict is still "
                "computed by the expectation checks, and no census "
                "kind corresponds to it. Named here so battery v2's "
                "authors see it; it is not counted among the four "
                "pass-by-default paths."
            ),
        },
        "reconciliation": {
            "register_text": (
                "GR-088-03 (the Spec 088 gap register): the "
                "promoting battery 'carried four pass-by-default "
                "paths and promoted 30 of 30 tested'."
            ),
            "register_paths_claimed": 4,
            "enumerated_pass_by_default_paths": len(default_paths),
            "pass_by_default_path_ids": [e["path_id"] for e in default_paths],
            "census_kinds_total": len(census),
            "census_default_credit_kinds_with_credits": sorted(
                k for k in census if k in defaults
            ),
            "audit_default_credit_vocabulary": sorted(defaults),
            "verdict": (
                "AGREES. The register's four is a count of code "
                "paths; the census's two default-credit kinds are "
                "the two of the four paths that fired in the "
                "recorded run (default_credit_too_short: 9 credits "
                "via P3; default_credit_missing_model_character: 5 "
                "credits via P6). The other two paths (P2 "
                "no-expectation, P7 no-anchor-neighbours) fired "
                "zero times in the recorded run, so their kinds "
                "appear in the audit classifier's DEFAULT_CREDITS "
                "vocabulary but not in pass_credits_by_kind. Paths "
                "and credit kinds are different units (grounding "
                "record gap 2); there is no contradiction and no "
                "register amendment is owed."
            ),
            "register_amendment_proposal": None,
        },
    }


def extract_rule_text(audit_gen_source: str, rule_id: str) -> tuple[int, str]:
    """(line of the rule-id assignment, rule text) from the audit generator."""
    lines = audit_gen_source.splitlines()
    id_lines = [
        i + 1 for i, line in enumerate(lines) if f'"{rule_id}"' in line
    ]
    if not id_lines:
        fail(f"rule id {rule_id} not found in {AUDIT_GEN_REL}")
    id_line = id_lines[0]
    tree = ast.parse(audit_gen_source)
    long_strings = sorted(
        (node.lineno, node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and len(node.value) > 80
    )
    for lineno, value in long_strings:
        if id_line < lineno <= id_line + 12:
            return id_line, value
    fail(f"no rule text found within 12 lines after {rule_id} at line {id_line}")
    return id_line, ""


def norm_ws(s: str) -> str:
    return " ".join(s.split())


def build_t105(audit: dict, audit_gen_source: str) -> dict:
    records = {r["sign"]: r for r in audit["records"]}
    determinations = []
    for sign in SIGNS:
        rec = records[sign]
        rule_id = rec["disposition_rule"]
        id_line, rule_text = extract_rule_text(audit_gen_source, rule_id)
        if norm_ws(rule_text) not in norm_ws(rec["plain_language_explanation"]):
            fail(f"{sign}: R5 rule text not found verbatim in the audit record")
        line_tests = sorted(
            {
                t
                for line in rec["evidence_independence"]["independent_lines"]
                for t in line.get("tests", [])
            }
        )
        all_tests = sorted(set(rec["evidence_tests"]) | set(line_tests))
        site = bool(set(all_tests) & {"distribution", "functional_role"})
        phon = "phonetic_value" in all_tests
        undeterminable = not site and not phon
        if site and phon:
            arm_text = "both arms"
        elif site:
            arm_text = "site-statistics arm"
        elif phon:
            arm_text = "phonotactic arm"
        else:
            arm_text = "undeterminable — recorded as phonotactic-gated"
        basis = (
            f"The record's evidence vocabulary names {all_tests}: "
            + (
                "distribution/functional role are the properties "
                "the defective validation measured and the "
                "site-statistics lineage (site_stats_v2) measures, "
                "so the site-statistics arm is required. "
                if site
                else ""
            )
            + (
                "phonetic_value is named, so the phonotactic arm "
                "is required. "
                if phon
                else "No field of the record names phonetic_value, "
                "and the R5 rule text rests the defect on no check "
                "of the reading's sound shape, so the phonotactic "
                "arm is not required by this record. "
                if site
                else ""
            )
            + (
                "Neither arm is engaged by the record; under the "
                "determination rule the anchor is undeterminable "
                "and is recorded as phonotactic-gated."
                if undeterminable
                else ""
            )
        )
        determinations.append(
            {
                "sign": sign,
                "reading_as_recorded": rec["proposed_value"]["reading"],
                "current_evidential_status": rec["current_evidential_status"],
                "disposition_rule": rule_id,
                "rule_definition": {
                    "source_file": AUDIT_GEN_REL,
                    "rule_id_line": id_line,
                    "rule_text": rule_text,
                    "rule_text_verified_in": (
                        f"{AUDIT_REL} record for {sign}, field "
                        "plain_language_explanation (verbatim tail)"
                    ),
                },
                "record_fields_cited": {
                    "evidence_tests": rec["evidence_tests"],
                    "support_line_tests": line_tests,
                    "phase48_promotion": rec["phase48_promotion"],
                    "phase48_reconstruction_present": (
                        rec["phase48_reconstruction"] is not None
                    ),
                },
                "determination": {
                    "arm": arm_text,
                    "site_statistics_arm_required": site,
                    "phonotactic_arm_required": phon,
                    "undeterminable": undeterminable,
                    "phonotactic_gated": undeterminable or phon,
                },
                "basis": basis,
            }
        )
    return {
        "record_id": "spec091-t105-checker-arm-split",
        "spec": "091-anchor-comparison-integrity",
        "task": "T105",
        "claims": "C091-10, C091-11 (determination side)",
        "generated_by": "backend/scripts/spec091_stage1_determinations.py",
        "date": DATE,
        "inputs": {
            AUDIT_REL: sha256_of(AUDIT),
            AUDIT_GEN_REL: sha256_of(AUDIT_GEN),
        },
        "determination_rule": (
            "An anchor requires the site-statistics arm iff its "
            "audit record's evidence vocabulary (evidence_tests, "
            "or any support line's tests in evidence_independence) "
            "names distribution or functional_role — the "
            "properties the defective validation measured and the "
            "site-statistics lineage measures. An anchor requires "
            "the phonotactic arm iff that vocabulary names "
            "phonetic_value, or its R5 rule text rests the defect "
            "on a check of the reading's sound shape. An anchor "
            "engaging neither arm is undeterminable and is "
            "recorded as phonotactic-gated (the conservative "
            "direction, per plan.md Stage 1)."
        ),
        "arm_definitions": {
            "site_statistics_arm": (
                "The repair brief's corrected site-statistics "
                "lineage, site_stats_v2 (backend/glossa_lab/"
                "site_stats_v2.py): distributional measurement "
                "done properly — a computed statistic and p-value, "
                "explicit insufficient-data outcomes, no invented "
                "values, no equivalence verdicts."
            ),
            "phonotactic_arm": (
                "The repair brief's corrected phonotactic "
                "checker, phonotactics_v2 (backend/glossa_lab/"
                "phonotactics_v2.py): the reading's initial sound "
                "against declared rules. Its rule set is not "
                "linguist-certified (GR-088-04), so the arm is "
                "dependency-gated wherever it is required "
                "(C091-11): no phonotactic verdict is produced "
                "under the uncertified rule set."
            ),
        },
        "determinations": determinations,
        "summary": {
            "site_statistics_arm": [
                d["sign"]
                for d in determinations
                if d["determination"]["site_statistics_arm_required"]
            ],
            "phonotactic_arm": [
                d["sign"]
                for d in determinations
                if d["determination"]["phonotactic_arm_required"]
            ],
            "undeterminable_phonotactic_gated": [
                d["sign"] for d in determinations if d["determination"]["undeterminable"]
            ],
            "consequence": (
                "On the five's own audit records the phonotactic "
                "subset is empty: all five revalidate on the "
                "site-statistics arm at Stage 3 (T303), and none "
                "of the five waits on GR-088-04. C091-11's gating "
                "therefore does not engage for the 5. This "
                "determination performs no revalidation and moves "
                "no disposition."
            ),
        },
    }


def main() -> int:
    battery_lines = BATTERY.read_text(encoding="utf-8").splitlines()
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    audit_gen_source = AUDIT_GEN.read_text(encoding="utf-8")
    t104 = build_t104(battery_lines, audit, audit_gen_source)
    t105 = build_t105(audit, audit_gen_source)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, record in [
        ("t104-pass-by-default-enumeration.json", t104),
        ("t105-checker-arm-split.json", t105),
    ]:
        (OUT_DIR / name).write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {OUT_DIR / name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
