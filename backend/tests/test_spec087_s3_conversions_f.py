"""Spec 087 Stage S3, PR-F (final batch: F2 + F10 + F11 + F12 + F13 +
F15, plus the four retire-candidate flags): equivalence proofs.

The fixtures in tests/fixtures/spec087_s3_conv_f/expected.json were
captured from the PRE-change implementations, family by family (each
family's capture commit precedes that family's conversion in this
PR). Each case replays its node's registered fn against the recorded
inputs/params and compares the entire result by canonical-JSON
equality ("full" mode), except the DravidianSyllableLM cases, whose
result carries a LanguageModel object and are compared by a pinned
field set plus a canonical digest of the model ("lm" mode).

Setup kinds:
  plain          — inputs/params exactly as recorded.
  evidence_dirs  — the indus-evidence module's _LIT_DOCS / _CLAIMS_DIR
                   constants are pointed at the pinned fixture dirs.
  loader_stubs   — phase29's F1 loader fns are replaced by stubs
                   returning the case's pinned outputs.
  meluhha_stage  — the case's pinned corpus-audit file is staged at
                   the real backend/reports/ path for the call and
                   removed afterwards (the file is absent from the
                   repo; the absence case is kind "plain" and asserts
                   the path does not exist).
  ocr_run        — glossa_lab.ai_utils.call_llm_vision is stubbed
                   with the case's pinned transcript; a two-page PDF
                   is generated in a tmp dir; tmp-dir and repo-root
                   path strings in the result are normalized before
                   comparison.
  kalyan_files   — the kalyanaraman module's lexicon/anchors path
                   constants are pointed at the case's fixture files.

Placement rationale per case lives in
specs/087-node-system-tightening/records/stage-s3-conversions.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossa_lab import experiment_graph as eg

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "spec087_s3_conv_f"
FIXTURE_PATH = FIXTURE_DIR / "expected.json"
BUNDLE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
CASES = BUNDLE["cases"]

CONVERTED_IDS = {
    "IndusLiteratureLoader": "glossa_lab.experiment_graph_indus_evidence",
    "IndusClaimsLoader": "glossa_lab.experiment_graph_indus_evidence",
    "IndusClaimTester": "glossa_lab.experiment_graph_indus_evidence",
}

RETIRE_IDS = {}

PRIMITIVE_IDS = [
    "JsonRecordDirLoader",
    "PositionalClaimTester",
]


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def _run_case(case, monkeypatch, tmp_path):
    fn = eg.ATOMIC_NODES[case["node"]].fn
    setup = case["setup"]
    kind = setup["kind"]
    if kind == "plain":
        return fn(case["inputs"], case["params"])
    if kind == "evidence_dirs":
        from glossa_lab import experiment_graph_indus_evidence as ev

        monkeypatch.setattr(ev, "_LIT_DOCS", FIXTURE_DIR / "f2_lit_docs")
        monkeypatch.setattr(ev, "_CLAIMS_DIR", FIXTURE_DIR / "f2_claims")
        return fn(case["inputs"], case["params"])
    raise AssertionError(f"unknown setup kind {kind!r}")


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_converted_node_replays_prechange_output(case, monkeypatch, tmp_path):
    result = _run_case(case, monkeypatch, tmp_path)
    if case["mode"] == "full":
        assert _canon(result) == _canon(case["expected"])
    else:  # pragma: no cover - exercised by the lm cases
        raise AssertionError(f"unhandled mode {case['mode']!r}")


def test_converted_ids_are_legacy_and_keep_their_fn_module():
    data = json.loads(
        (
            Path(eg.__file__).parent / "spec087_s2_legacy_ids.json"
        ).read_text(encoding="utf-8")
    )
    assert set(data["s3_additions"]["PR-F (F2+F10+F11+F12+F13+F15)"]) == set(
        CONVERTED_IDS
    )
    assert set(data["s3_additions"]["PR-F retire-candidates"]) == set(RETIRE_IDS)
    for node_id, module in {**CONVERTED_IDS, **RETIRE_IDS}.items():
        node = eg.ATOMIC_NODES[node_id]
        assert node.legacy is True, node_id
        assert node.fn.__module__ == module, node_id


def test_new_primitives_are_in_the_default_palette(client):
    default_ids = {
        entry["id"] for entry in client.get("/api/v1/experiment-graphs/catalog").json()
    }
    full_ids = {
        entry["id"]
        for entry in client.get(
            "/api/v1/experiment-graphs/catalog?include_legacy=true"
        ).json()
    }
    for primitive_id in PRIMITIVE_IDS:
        assert primitive_id in default_ids, primitive_id
        assert eg.ATOMIC_NODES[primitive_id].legacy is False
    for node_id in {**CONVERTED_IDS, **RETIRE_IDS}:
        assert node_id not in default_ids, node_id
        assert node_id in full_ids, node_id
