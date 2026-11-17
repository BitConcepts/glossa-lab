"""Spec 091 Stage 1 — the T104 and T105 determination records.

T104's acceptance (tasks.md): the generated enumeration record
names a code location and a census kind per entry; an untraced
kind or path fails it. These tests re-derive the tracing from the
frozen sources themselves — the Phase-48 battery's pass-awarding
returns, the WP5 census in the audit JSON, and the audit
generator's DEFAULT_CREDITS — and require the filed record to
agree exactly.

T105's acceptance: the determination record cites the rule text
and record fields per anchor. These tests require each
determination's cited rule text to be the R5 text the audit
generator defines and the audit record carries verbatim, its
cited record fields to match the audit record exactly, and its
arm determination to follow the record's stated rule recomputed
from those fields.
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / "specs" / "091-anchor-comparison-integrity" / "records"
BATTERY = ROOT / "backend" / "scripts" / "phase48_medium_validation.py"
AUDIT = ROOT / "docs" / "repair-2026-10-26" / "anchor-support-audit.json"
AUDIT_GEN = ROOT / "backend" / "scripts" / "repair_anchor_audit.py"

SIGNS = ["M042", "M046", "M108", "M176", "M342"]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _norm_ws(s: str) -> str:
    return " ".join(s.split())


def _default_credits() -> set[str]:
    tree = ast.parse(AUDIT_GEN.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "DEFAULT_CREDITS" for t in node.targets
        ):
            return {
                elt.value
                for elt in node.value.elts
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
            }
    raise AssertionError("DEFAULT_CREDITS not found in the audit generator")


# ── T104 — the pass-by-default enumeration ──────────────────────


def _t104() -> dict:
    return _load(RECORDS / "t104-pass-by-default-enumeration.json")


def test_t104_inputs_are_the_frozen_sources() -> None:
    rec = _t104()
    assert rec["inputs"]["backend/scripts/phase48_medium_validation.py"] == _sha256(
        BATTERY
    )
    assert rec["inputs"]["docs/repair-2026-10-26/anchor-support-audit.json"] == _sha256(
        AUDIT
    )
    assert rec["inputs"]["backend/scripts/repair_anchor_audit.py"] == _sha256(AUDIT_GEN)


def test_t104_every_census_kind_traced_to_exactly_one_path() -> None:
    rec = _t104()
    census = _load(AUDIT)["phase48_summary"]["pass_credits_by_kind"]
    traced = [p["credit_kind_awarded"] for p in rec["paths"] if p["credit_kind_awarded"]]
    assert len(traced) == len(set(traced)), "a kind is traced to two paths"
    for kind, count in census.items():
        assert kind in traced, f"census kind {kind} has no traced path"
        entry = next(p for p in rec["paths"] if p["credit_kind_awarded"] == kind)
        assert entry["recorded_credits_in_wp5_census"] == count
        assert entry["code_location"]["file"] == (
            "backend/scripts/phase48_medium_validation.py"
        )
        lo, hi = entry["code_location"]["lines"]
        assert 1 <= lo <= hi


def test_t104_four_pass_by_default_paths_reconciled() -> None:
    rec = _t104()
    defaults = _default_credits()
    default_paths = [p for p in rec["paths"] if p["is_pass_by_default"]]
    assert len(default_paths) == 4
    assert {p["credit_kind_awarded"] for p in default_paths} == defaults
    recon = rec["reconciliation"]
    assert recon["register_paths_claimed"] == 4
    assert recon["enumerated_pass_by_default_paths"] == 4
    assert recon["register_amendment_proposal"] is None
    fired = {p["credit_kind_awarded"] for p in default_paths if p["fired_in_recorded_run"]}
    assert fired == {k for k in defaults if _load(AUDIT)["phase48_summary"][
        "pass_credits_by_kind"].get(k, 0) > 0}


def test_t104_signatures_and_return_coverage() -> None:
    rec = _t104()
    lines = BATTERY.read_text(encoding="utf-8").splitlines()
    for path in rec["paths"]:
        lo, hi = path["code_location"]["lines"]
        assert path["branch_signature"] in "\n".join(lines[lo - 1 : hi]), (
            f"{path['path_id']}: signature not in cited lines"
        )

    def covering(line_no: int) -> list[str]:
        return [
            p["path_id"]
            for p in rec["paths"]
            if p["code_location"]["lines"][0] <= line_no <= p["code_location"]["lines"][1]
        ]

    pass_returns = [
        i + 1
        for i, line in enumerate(lines)
        if "return True" in line or "return ok," in line or "return ratio" in line
    ]
    assert pass_returns, "the battery's pass returns were not found"
    for line_no in pass_returns:
        assert len(covering(line_no)) == 1, (
            f"battery line {line_no} covered by {covering(line_no)}"
        )


# ── T105 — the checker-arm split for the 5 ──────────────────────


def _t105() -> dict:
    return _load(RECORDS / "t105-checker-arm-split.json")


def _rule_text_from_generator(rule_id: str) -> str:
    source = AUDIT_GEN.read_text(encoding="utf-8")
    lines = source.splitlines()
    id_line = next(
        i + 1 for i, line in enumerate(lines) if f'"{rule_id}"' in line
    )
    tree = ast.parse(source)
    long_strings = sorted(
        (node.lineno, node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and len(node.value) > 80
    )
    for lineno, value in long_strings:
        if id_line < lineno <= id_line + 12:
            return value
    raise AssertionError(f"no rule text found after {rule_id}")


def test_t105_covers_exactly_the_five() -> None:
    rec = _t105()
    assert [d["sign"] for d in rec["determinations"]] == SIGNS
    assert rec["inputs"]["docs/repair-2026-10-26/anchor-support-audit.json"] == _sha256(
        AUDIT
    )


def test_t105_citations_match_the_audit_records() -> None:
    rec = _t105()
    audit_records = {r["sign"]: r for r in _load(AUDIT)["records"]}
    for det in rec["determinations"]:
        arec = audit_records[det["sign"]]
        assert det["disposition_rule"] == arec["disposition_rule"]
        rule_text = det["rule_definition"]["rule_text"]
        # The cited text is the generator's R5 rule text …
        assert rule_text == _rule_text_from_generator(det["disposition_rule"])
        # … and the audit record carries it verbatim.
        assert _norm_ws(rule_text) in _norm_ws(arec["plain_language_explanation"])
        fields = det["record_fields_cited"]
        assert fields["evidence_tests"] == arec["evidence_tests"]
        line_tests = sorted(
            {
                t
                for line in arec["evidence_independence"]["independent_lines"]
                for t in line.get("tests", [])
            }
        )
        assert fields["support_line_tests"] == line_tests
        assert fields["phase48_promotion"] == arec["phase48_promotion"]
        assert fields["phase48_reconstruction_present"] == (
            arec["phase48_reconstruction"] is not None
        )


def test_t105_determinations_follow_the_stated_rule() -> None:
    rec = _t105()
    for det in rec["determinations"]:
        fields = det["record_fields_cited"]
        tests = set(fields["evidence_tests"]) | set(fields["support_line_tests"])
        site = bool(tests & {"distribution", "functional_role"})
        phon = "phonetic_value" in tests
        got = det["determination"]
        assert got["site_statistics_arm_required"] == site
        assert got["phonotactic_arm_required"] == phon
        assert got["undeterminable"] == (not site and not phon)
        assert got["phonotactic_gated"] == (phon or got["undeterminable"])
