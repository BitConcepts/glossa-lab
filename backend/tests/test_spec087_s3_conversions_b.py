"""Spec 087 Stage S3, PR-B (families F3 + F8): equivalence proofs.

The fixtures in tests/fixtures/spec087_s3_conv_b/expected.json were
captured from the PRE-change implementations (the capture commit
precedes any conversion in this PR). Each case replays its node's
registered fn against the recorded inputs/params and compares to
the recorded output:

* "full" mode — canonical-JSON equality of the entire result;
* "hash" mode — SHA-256 of the canonical JSON + the full key set +
  the pinned verbatim fields (used where the result carries a
  multi-thousand-entry map).

Canonical form matches the capture: json.dumps(sort_keys=True,
ensure_ascii=False), UTF-8.

Database reads: the capture monkeypatched eg._sync_db_all with a
fake over two fixed tables; the replay monkeypatches the generic
engine's `_db_all` with the identical fake (the engine's helper
keeps _sync_db_all's signature and semantics), so both sides read
the same rows without a seeded database (H4 in the triage record:
the backend DB in a fresh tree holds empty CGSA tables).

One case is an exception, and says so in the bundle: ClusterMapper's
JSON-file branch reads a file at a path outside the repository
(experiment_graph.py's parents[3]); that path cannot be recreated
in CI, so the file branch is replayed through the LabelMapApplier
primitive with a temporary file carrying the same content the
capture used ({"best_k": 3, "sign_to_cluster": {"A": 0, "B": 1,
"C": 1}}) and the same source chain the domain node builds, with
the DB source emptied exactly as in the capture. The domain node's
DB, frequency, and error branches are replayed directly.

Placement rationale per case lives in
specs/087-node-system-tightening/records/stage-s3-conversions.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from glossa_lab import experiment_graph as eg
from glossa_lab import generic_primitives as gp

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "spec087_s3_conv_b" / "expected.json"
BUNDLE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
CASES = BUNDLE["cases"]

CONVERTED_IDS = {
    "CanonicalSignLoader": "glossa_lab.experiment_graph",
    "ClusterMapper": "glossa_lab.experiment_graph",
    "StructuralTemplateAnalyzer": "glossa_lab.experiment_graph",
    "ClusterArchaeology": "glossa_lab.experiment_graph_phase20",
    "IndusSignRoleClassifier": "glossa_lab.experiment_graph_ctt",
    "DefaultIndusValueRoleMap": "glossa_lab.experiment_graph_ctt",
    "IndusAnchorSetSyllable": "glossa_lab.experiment_graph_phase30",
    "DerivedAnchorSet": "glossa_lab.experiment_graph_phase14",
    "EpistaticAnchorRanker": "glossa_lab.experiment_graph_phase14",
}

PRIMITIVE_IDS = [
    "RegistryTableLoader",
    "LabelMapApplier",
    "TemplateMiner",
    "ClusterContingencyProfile",
    "SignRoleClassifier",
    "ValueRoleMapSource",
    "AnchorSyllabifier",
    "AssociationAnchorDeriver",
    "PMICentralityRanker",
]

# Identical to the capture script's fixture rows.
CANONICAL_ROWS = [
    {"sign_id": "P001", "internal_id": "uuid-1", "numbering_system": "parpola_1982",
     "in_corpus": 1, "description": "fish", "wells_ids": "[\"W10\", \"W11\"]"},
    {"sign_id": "P002", "internal_id": "uuid-2", "numbering_system": "parpola_1982",
     "in_corpus": 1, "description": "jar", "wells_ids": ""},
    {"sign_id": "P003", "internal_id": "uuid-3", "numbering_system": "parpola_1982",
     "in_corpus": 0, "description": "out of corpus", "wells_ids": ""},
    {"sign_id": "Y001", "internal_id": "uuid-4", "numbering_system": "yajnadevam_glyphid",
     "in_corpus": 1, "description": "glyph", "wells_ids": ""},
    {"sign_id": "P004", "internal_id": "uuid-5", "numbering_system": "parpola_1982",
     "in_corpus": 0, "description": "{\"note\": \"json text\"}", "wells_ids": ""},
]

ASSIGNMENT_ROWS = [
    {"sign_id": "A", "cluster_label": 0, "cluster_k": 7},
    {"sign_id": "B", "cluster_label": 0, "cluster_k": 7},
    {"sign_id": "C", "cluster_label": 1, "cluster_k": 7},
    {"sign_id": "D", "cluster_label": 2, "cluster_k": 7},
]

TABLES = {"canonical_signs": CANONICAL_ROWS, "sign_cluster_assignments": ASSIGNMENT_ROWS}
TABLES_EMPTY = {"canonical_signs": [], "sign_cluster_assignments": []}
RAISE_TABLES = {"canonical_signs", "sign_cluster_assignments"}


def _make_fake(tables, raise_on=()):
    """The capture script's fake, verbatim: same (table, where, params)
    signature as _sync_db_all / the engine's _db_all, same where-clause
    matching, same JSON-string coercion."""

    def fake(table, where="", params=()):
        if table in raise_on:
            raise RuntimeError("fixture db failure")
        rows = [dict(r) for r in tables.get(table, [])]
        if "in_corpus = 1" in where:
            rows = [r for r in rows if r.get("in_corpus") == 1]
        if "numbering_system = ?" in where:
            rows = [r for r in rows if r.get("numbering_system") == params[0]]
        out = []
        for r in rows:
            d = dict(r)
            for k, v in d.items():
                if isinstance(v, str) and v and v[0] in ("{", "["):
                    try:
                        d[k] = json.loads(v)
                    except Exception:  # noqa: BLE001
                        pass
            out.append(d)
        return out

    return fake


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def _install_fake(monkeypatch, kind: str) -> None:
    if kind == "db":
        monkeypatch.setattr(gp, "_db_all", _make_fake(TABLES))
    elif kind == "db_raise":
        monkeypatch.setattr(gp, "_db_all", _make_fake(TABLES, raise_on=RAISE_TABLES))
    else:  # db_empty, cluster_file, plain — no rows on the replay side
        monkeypatch.setattr(gp, "_db_all", _make_fake(TABLES_EMPTY))


def _assert_case(case: dict, result) -> None:
    if case["mode"] == "full":
        assert _canon(result) == _canon(case["expected"])
    else:
        digest = hashlib.sha256(_canon(result).encode("utf-8")).hexdigest()
        assert digest == case["expected_sha256"]
        assert sorted(result.keys()) == case["expected_keys"]
        for field, expected in case["expected_fields"].items():
            assert _canon(result[field]) == _canon(expected), field


_DOMAIN_CASES = [c for c in CASES if c.get("replay_via", "domain") == "domain"]


@pytest.mark.parametrize("case", _DOMAIN_CASES, ids=[c["id"] for c in _DOMAIN_CASES])
def test_converted_node_replays_prechange_output(case, monkeypatch):
    _install_fake(monkeypatch, case["setup"]["kind"])
    fn = eg.ATOMIC_NODES[case["node"]].fn
    result = fn(case["inputs"], case["params"])
    _assert_case(case, result)


def test_cluster_mapper_file_branch_via_primitive(tmp_path, monkeypatch):
    case = next(c for c in CASES if c["id"] == "cm_file")
    _install_fake(monkeypatch, "db_empty")
    file_path = tmp_path / "sign_clusters.json"
    file_path.write_text(
        json.dumps({"best_k": 3, "sign_to_cluster": {"A": 0, "B": 1, "C": 1}}),
        encoding="utf-8",
    )
    # The source chain the domain node builds, with the file source
    # pointed at the temporary file (the historical path is outside
    # the repository and cannot be recreated in CI).
    spec = {
        "sources": [
            {"kind": "db_table", "table": "sign_cluster_assignments"},
            {"kind": "json_file", "path": str(file_path)},
            {"kind": "frequency_rank", "bins": 40},
        ],
        "unmapped_label": -1,
        "unavailable_error": (
            "Cluster assignments unavailable: no DB table, no "
            "sign_clusters.json, and dataset too small for frequency fallback."
        ),
    }
    fn = eg.ATOMIC_NODES["LabelMapApplier"].fn
    result = fn(case["inputs"], {"map_spec": spec})
    _assert_case(case, result)


def test_converted_ids_are_legacy_and_keep_their_fn_module():
    data = json.loads(
        (
            Path(eg.__file__).parent / "spec087_s2_legacy_ids.json"
        ).read_text(encoding="utf-8")
    )
    assert set(data["s3_additions"]["PR-B (F3+F8)"]) == set(CONVERTED_IDS)
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
