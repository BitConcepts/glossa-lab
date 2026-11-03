"""Spec 087 Stage S3, PR-D (families F7 + F6): equivalence proofs.

The fixtures in tests/fixtures/spec087_s3_conv_d/expected.json were
captured from the PRE-change implementations (the capture commit
precedes any conversion in this PR). Each case replays its node's
registered fn against the recorded inputs/params and compares the
entire result by canonical-JSON equality ("full" mode — every case
in this batch).

Canonical form matches the capture: json.dumps(sort_keys=True,
ensure_ascii=False), UTF-8.

The fixture inputs are synthetic records in exactly the
mesopotamian_contact shapes: the loaders behind the historical
graphs read corpus files that live in the gitignored corpora/
download tree and are absent from this repository, so — following
PR-A's/PR-C's precedent — the equivalence proof runs over synthetic
inputs in the data module's shapes, chosen to exercise every branch
the conversion could move (the keyword gate on and off, the direct
vs expanded rendering scans, substring vs token-exact matching, the
allograph expansion and its absence, both -me-luh-ha penalties, the
ePSD2 segmenter with determinatives and subscript digits,
min_icount filtering, cohort binning incl. empty and out-of-range
cohorts, known-name confirmation by set vs by upstream flag, the
three example-line truncation rules, and insufficient inputs).

One cross-check is pinned explicitly: RefinedMeluhhanPersonsExtractorV2
runs V1's fixture rows, and its captured output differs from V1's
only in the verdict wording and the example_line[:120] truncation —
the triage's "near-verbatim copy" account, proven on the captures.

Placement rationale per case lives in
specs/087-node-system-tightening/records/stage-s3-conversions.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossa_lab import experiment_graph as eg

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "spec087_s3_conv_d" / "expected.json"
BUNDLE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
CASES = BUNDLE["cases"]

CONVERTED_IDS = {
    "JanabiyahPhoneticReadout": "glossa_lab.experiment_graph_phase25",
    "JanabiyahPhoneticReadoutV2": "glossa_lab.experiment_graph_phase26",
    "ReverseJanabiyahSearch": "glossa_lab.experiment_graph_phase27",
    "ReverseJanabiyahSearchV2": "glossa_lab.experiment_graph_phase28",
    "M77ReverseJanabiyahSearchV3": "glossa_lab.experiment_graph_phase29",
    "LengthCohortReverseJanabiyahSearch": "glossa_lab.experiment_graph_phase30",
    "MeluhhanPersonsExtractor": "glossa_lab.experiment_graph_phase22",
    "RefinedMeluhhanPersonsExtractor": "glossa_lab.experiment_graph_phase23",
    "RefinedMeluhhanPersonsExtractorV2": "glossa_lab.experiment_graph_phase24",
    "Persons_v3_Extractor": "glossa_lab.experiment_graph_phase25",
}

PRIMITIVE_IDS = [
    "SkeletonTabletSearch",
    "ReverseSkeletonSearch",
    "PersonsAggregator",
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


def test_refined_v2_matches_v1_except_verdict_and_line_truncation():
    by_id = {c["id"]: c for c in CASES}
    v1 = by_id["persons_refined_default"]["expected"]
    v2 = by_id["persons_refined_v2_same_rows"]["expected"]
    assert v1["verdict"] != v2["verdict"]
    for key in v1:
        if key == "verdict":
            continue
        a, b = v1[key], v2[key]
        if isinstance(a, list):
            assert len(a) == len(b)
            for row_a, row_b in zip(a, b):
                for field in row_a:
                    if field == "example_line":
                        assert row_b[field] == row_a[field][:120]
                    else:
                        assert row_a[field] == row_b[field]
        else:
            assert a == b


def test_converted_ids_are_legacy_and_keep_their_fn_module():
    data = json.loads(
        (
            Path(eg.__file__).parent / "spec087_s2_legacy_ids.json"
        ).read_text(encoding="utf-8")
    )
    assert set(data["s3_additions"]["PR-D (F7+F6)"]) == set(CONVERTED_IDS)
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
