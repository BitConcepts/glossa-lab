"""Spec 095 Stage 4 (T405) — the composed release gate.

C095-14's thirteen components composed into one gate. The
composition proofs here plant the RT-03 stale-claim shape (a
superseded claim presented as current) and show the gate blocking
its candidate; show a clean candidate with complete evidence
passing; show missing or failed evidence blocking; and show that
an exception exists only as a recorded owner-approved entry.

The heavy executed components (ledger gate subprocess, intake
validation, contamination subprocess) are replaced by stand-ins in
the composition tests — their own correctness is covered by their
own gates and suites. The corpus-identity, anchor-regression, and
public-claims components run for real here, including against the
live tree: the tree's anchor-model README still carries the RT-03
stale presentation at Stage 4 (its banner is owner-gated
micro-task MT-095-1), so the real-tree public-claims component
must FAIL. When MT-095-1 lands, that test's expectation changes
with it.
"""

from __future__ import annotations

from pathlib import Path

from glossa_lab import release_gate as rg

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "spec095_release_gate"

COMPLETE_EVIDENCE = {
    name: {
        "verdict": "pass",
        "command": f"run-{name}",
        "exit_code": 0,
        "recorded_at": "2026-11-17T00:00:00Z",
        "record_ref": f"records/{name}",
    }
    for name in rg.EVIDENCE_COMPONENTS
}


def _pass(_root):
    return rg.ComponentResult(rg.PASS, "stand-in pass")


FAST_EXECUTED = {
    "ledger_validation": _pass,
    "claim_stage_validation": _pass,
    "provenance_completeness": _pass,
}


def _gate(tmp_path: Path, surface_text: str, **kwargs):
    surface = tmp_path / "surface.md"
    surface.write_text(surface_text, encoding="utf-8")
    return rg.run_release_gate(
        ROOT,
        evidence=kwargs.pop("evidence", COMPLETE_EVIDENCE),
        exceptions=kwargs.pop("exceptions", None),
        surfaces=[str(surface)],
        executed=FAST_EXECUTED,
        **kwargs,
    )


def test_thirteen_components_of_record():
    assert rg.COMPONENTS == (
        "unit_tests",
        "integration_tests",
        "frontend_tests",
        "end_to_end_tests",
        "ledger_validation",
        "corpus_identity_verification",
        "anchor_regression",
        "claim_stage_validation",
        "provenance_completeness",
        "security_checks",
        "accessibility_checks",
        "reproducibility_smoke_test",
        "public_claims_consistency",
    )


def test_planted_stale_claim_blocks_its_candidate(tmp_path):
    planted = (FIXTURES / "planted_stale_readme.md").read_text(encoding="utf-8")
    record = _gate(tmp_path, planted)
    assert record["verdict"] == "BLOCKED"
    component = record["components"]["public_claims_consistency"]
    assert component["status"] == rg.FAIL
    assert "stale claim presented as current" in component["detail"]
    assert record["blocked_by"] == ["public_claims_consistency"]


def test_bannered_historical_values_and_clean_candidate_pass(tmp_path):
    bannered = (FIXTURES / "bannered_readme.md").read_text(encoding="utf-8")
    record = _gate(tmp_path, bannered)
    assert record["components"]["public_claims_consistency"]["status"] == rg.PASS
    assert record["verdict"] == rg.PASS
    assert record["blocked_by"] == []


def test_missing_evidence_blocks(tmp_path):
    evidence = {k: v for k, v in COMPLETE_EVIDENCE.items() if k != "frontend_tests"}
    record = _gate(tmp_path, "# clean surface\n", evidence=evidence)
    assert record["components"]["frontend_tests"]["status"] == rg.NOT_RUN
    assert record["verdict"] == "BLOCKED"


def test_failing_evidence_blocks(tmp_path):
    evidence = dict(COMPLETE_EVIDENCE)
    evidence["unit_tests"] = {**COMPLETE_EVIDENCE["unit_tests"], "exit_code": 1}
    record = _gate(tmp_path, "# clean surface\n", evidence=evidence)
    assert record["components"]["unit_tests"]["status"] == rg.FAIL
    assert record["verdict"] == "BLOCKED"


def test_exception_without_owner_approval_is_not_an_exception(tmp_path):
    evidence = dict(COMPLETE_EVIDENCE)
    evidence["security_checks"] = {**COMPLETE_EVIDENCE["security_checks"], "verdict": "fail", "exit_code": 2}
    record = _gate(
        tmp_path,
        "# clean surface\n",
        evidence=evidence,
        exceptions=[{"component": "security_checks", "scope": "fixture", "approved_by": "owner"}],
    )
    assert record["components"]["security_checks"]["status"] == rg.FAIL
    assert record["verdict"] == "BLOCKED"
    assert any("owner_approval_ref" in p for p in record["exception_problems"])


def test_recorded_owner_approved_exception_covers(tmp_path):
    evidence = dict(COMPLETE_EVIDENCE)
    evidence["security_checks"] = {**COMPLETE_EVIDENCE["security_checks"], "verdict": "fail", "exit_code": 2}
    record = _gate(
        tmp_path,
        "# clean surface\n",
        evidence=evidence,
        exceptions=[
            {
                "component": "security_checks",
                "scope": "fixture candidate only",
                "approved_by": "Tristen Pierson",
                "owner_approval_ref": "fixture-approval-2026-11-17",
                "date": "2026-11-17",
            }
        ],
    )
    assert record["components"]["security_checks"]["status"] == rg.EXCEPTED
    assert record["verdict"] == rg.PASS


def test_real_tree_anchor_and_corpus_components_pass():
    assert rg.check_anchor_regression(ROOT).status == rg.PASS
    corpus = rg.check_corpus_identity(ROOT)
    assert corpus.status == rg.PASS, corpus.detail
    assert "indus_v3_firestore_strict" in corpus.detail
    assert "holdat_downloads_layer" in corpus.detail


def test_real_tree_readme_fails_public_claims_rt03_outstanding():
    result = rg.check_public_claims(ROOT)
    assert result.status == rg.FAIL
    assert "indus-anchor-model/README.md" in result.detail
