"""Spec 087 Stage S3, PR-C (families F4 + F5): equivalence proofs.

The fixtures in tests/fixtures/spec087_s3_conv_c/expected.json were
captured from the PRE-change implementations (the capture commit
precedes any conversion in this PR). Each case replays its node's
registered fn against the recorded inputs/params and compares the
entire result by canonical-JSON equality ("full" mode — every case
in this batch; the permutation outputs are seed-determined, so
byte-equality is exact).

Canonical form matches the capture: json.dumps(sort_keys=True,
ensure_ascii=False), UTF-8.

The fixture inputs are synthetic records in exactly the
mesopotamian_contact shapes: the loaders behind the historical
graphs read corpus files that live in the gitignored corpora/
download tree and are absent from this repository, so — following
PR-A's precedent for ContactCorpusLoader — the equivalence proof
runs over synthetic inputs in the data module's shapes, chosen to
exercise every branch the conversion could move (placeholder-only
seals, compound sign ids, the allograph second pass, insufficient
inputs, the pinned divergent Meluhha falloff, and all three
stratifiers over one shared person set).

Placement rationale per case lives in
specs/087-node-system-tightening/records/stage-s3-conversions.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossa_lab import experiment_graph as eg

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "spec087_s3_conv_c" / "expected.json"
BUNDLE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
CASES = BUNDLE["cases"]

CONVERTED_IDS = {
    "IconographicAnchorScore": "glossa_lab.experiment_graph_phase27",
    "AllographAwareIconographicScore": "glossa_lab.experiment_graph_phase28",
    "BlindHeldOutTest": "glossa_lab.experiment_graph_phase25",
    "BayesianDecoder": "glossa_lab.experiment_graph_phase26",
    "BayesianDecoderV2": "glossa_lab.experiment_graph_phase27",
    "EnhancedNameMatcher": "glossa_lab.experiment_graph_phase23",
    "EnhancedNameMatcherV2": "glossa_lab.experiment_graph_phase24",
    "MeluhhaNameMatcher": "glossa_lab.experiment_graph_phase22",
    "BilingualReadoutTest": "glossa_lab.experiment_graph_phase23",
    "BilingualReadoutTestV2": "glossa_lab.experiment_graph_phase24",
    "PeriodStratifiedReadout": "glossa_lab.experiment_graph_phase25",
    "PeriodStratifiedReadout6Bucket": "glossa_lab.experiment_graph_phase27",
    "ProvenienceStratifiedReadout": "glossa_lab.experiment_graph_phase26",
}

PRIMITIVE_IDS = [
    "IconographicAnchorScorer",
    "PhonemeMapCoverage",
    "PhonemeMapPermutationTest",
    "LengthMatchScorer",
    "LengthMatchPermutationTest",
    "StratifiedPermutationTest",
]


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_converted_node_replays_prechange_output(case):
    assert case["mode"] == "full"
    assert case["setup"]["kind"] == "plain"
    fn = eg.ATOMIC_NODES[case["node"]].fn
    result = fn(case["inputs"], case["params"])
    assert _canon(result) == _canon(case["expected"])


def test_converted_ids_are_legacy_and_keep_their_fn_module():
    data = json.loads(
        (
            Path(eg.__file__).parent / "spec087_s2_legacy_ids.json"
        ).read_text(encoding="utf-8")
    )
    assert set(data["s3_additions"]["PR-C (F4+F5)"]) == set(CONVERTED_IDS)
    for node_id, module in CONVERTED_IDS.items():
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
    for node_id in CONVERTED_IDS:
        assert node_id not in default_ids, node_id
        assert node_id in full_ids, node_id
