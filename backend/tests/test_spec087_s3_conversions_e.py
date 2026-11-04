"""Spec 087 Stage S3, PR-E (family F9): equivalence proofs.

The fixtures in tests/fixtures/spec087_s3_conv_e/expected.json were
captured from the PRE-change implementations (the capture commit
precedes any conversion in this PR). Each case replays its node's
registered fn against the recorded inputs/params and compares the
entire result by canonical-JSON equality ("full" mode — every case
in this batch).

Canonical form matches the capture: json.dumps(sort_keys=True,
ensure_ascii=False), UTF-8.

All eight nodes are pure functions of (inputs, params) over
synthetic inputs — no corpus files, no DB — so the inputs are built
deterministically (dedicated Random instances) to exercise every
branch the conversion could move: the detector's significance cuts
and top_k slicing; all three HED regime branches; the length_bin
bucketing and all three association verdict branches plus the
misalignment error; the DoF renaming table incl. partial inputs;
the comparator's candidate classification (target equality /
"indus" literal / "candidate" substring), the negative-tag set, the
refs fallback and all three verdict bands; the detector-verdict
evidence rule table branch by branch incl. both CAS threshold
params and the unfed shape test_spec086_stub_disposition.py pins;
the positional classifier's five classes, the length-1 I+T path,
min_count exclusion, and a custom-threshold run; the null test's
z bands and its three error returns. Every capture case asserted
its intended branch at capture time.

One hand check is pinned in the fixture bundle's capture record:
for the locked-block detector corpus, count(a1)=count(a2)=30 of 270
unigrams and bigram (a1,a2)=30 of 180, so PMI = log(13.5) = 2.6027.

Placement rationale per case lives in
specs/087-node-system-tightening/records/stage-s3-conversions.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossa_lab import experiment_graph as eg

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "spec087_s3_conv_e" / "expected.json"
BUNDLE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
CASES = BUNDLE["cases"]

CONVERTED_IDS = {
    "EpistaticInteractionDetector": "glossa_lab.experiment_graph_phase14",
    "EpistaticOrderProfile": "glossa_lab.experiment_graph_phase14",
    "SignContextAssociation": "glossa_lab.experiment_graph_phase14",
    "DoFExtractor": "glossa_lab.experiment_graph_phase14",
    "LanguageSignatureComparator": "glossa_lab.experiment_graph_phase14",
    "LanguageDetectorVerdict": "glossa_lab.experiment_graph_phase14",
    "FulsPositionalClassifier": "glossa_lab.experiment_graph_phase20",
    "IndusNullModelTest": "glossa_lab.experiment_graph_indus_evidence",
}

PRIMITIVE_IDS = [
    "InteractionSurplusProfile",
    "OrderInformationProfile",
    "TokenContextAssociation",
    "MetricFieldExtractor",
    "SignatureComparator",
    "EvidenceRuleAggregator",
    "PositionalClassClassifier",
    "SignPositionNullTest",
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
    assert set(data["s3_additions"]["PR-E (F9)"]) == set(CONVERTED_IDS)
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
