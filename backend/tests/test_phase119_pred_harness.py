"""Tests for Phase-119 (spec 018) PRED-2026 readiness harness.

Covers: the frozen class-set reproduction (14/12/46/33) and
registry hashes (spec section 3); the canonical map conflict
rules incl. the M002 ambiguity; dedup stages A/B/C incl. the
stage-C length floor and kept-anchor (no chaining) rule; the
three ingestion adapters on synthetic fixtures; a toy
prediction evaluated end-to-end through the real gating and
scoring code in both verdict directions, plus the real
PRED-2026-003 scorer on toy future-concordance fixtures;
the section 4/6.1 gates (non-qualifying class, incomplete
provenance, unmapped-share guard, multi-site input); the
section 6.5 verdict lock; the section 8 dry-run label and
its prohibition on criterion statistics; and H23 graph
registration.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

from glossa_lab.pred_harness import (
    DRY_RUN_LABEL, PREDICTIONS, IngestedDataset, NotEvaluable,
    Prediction, SignMapper, adapt_converted_layer,
    adapt_future_concordance, adapt_image_transcription,
    adapt_rmrl_concordance, build_sign_maps, dedup, dry_run,
    evaluate, load_sign_classes,
)

BACKEND = Path(__file__).resolve().parents[1]
REPO = BACKEND.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "pred_harness"
INVENTORY = REPO / "data" / "crosswalks" / "sign_inventory.csv"
REGISTRY = REPO / "data" / "crosswalks" / "canonical_sign_registry.csv"

TOY_PRED = Prediction(
    pid="PRED-TOY-001", kind="rate", rate="start", threshold=0.5,
    pass_count=2, sign_set=("P001", "P004"),
    prediction_text="toy prediction (test only)",
    criterion_text="toy criterion (test only)")


@pytest.fixture(scope="module")
def classes():
    return load_sign_classes(INVENTORY)


@pytest.fixture(scope="module")
def mapper():
    return SignMapper(build_sign_maps(REGISTRY))


def _toy_prov(**over):
    prov = {"date": "2026-10-07", "name": "toy", "source": "fixture",
            "license": "synthetic fixture (test)",
            "status": "ingested", "input_sha256": "0" * 64,
            "text_rule": "toy", "unit_rule": "toy"}
    prov.update(over)
    return prov


# ------------------------------------------------------------ spec section 3

def test_registry_hashes_frozen():
    assert hashlib.sha256(INVENTORY.read_bytes()).hexdigest() == (
        "f9a84ff999589619a884b07afa927f0d51093f76b4ea1f8f5b5628e0e8fcb12f")
    assert hashlib.sha256(REGISTRY.read_bytes()).hexdigest() == (
        "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420")


def test_class_sets_reproduce_register_counts(classes):
    counts = Counter(classes.values())
    assert counts == {"TERMINAL": 14, "INITIAL": 12,
                      "MEDIAL": 46, "MIXED": 33}
    term = sorted(s for s, lab in classes.items() if lab == "TERMINAL")
    init = sorted(s for s, lab in classes.items() if lab == "INITIAL")
    assert term == ["P020", "P076", "P095", "P099", "P108", "P125",
                    "P210", "P226", "P256", "P346", "P359", "P378",
                    "P384", "P385"]
    assert init == ["P000", "P001", "P004", "P013", "P051", "P098",
                    "P217", "P238", "P265", "P301", "P310", "P324"]


def test_map_conflict_rules(tmp_path):
    reg = tmp_path / "reg.csv"
    reg.write_text(
        "sign_id,numbering_system,description,parpola_id,wells_ids,"
        "mahadevan_ids,parpola_allographs,icit_function,corpus_freq,"
        "start_rate,end_rate,internal_rate,in_corpus,n_feature_dims\n"
        "P900,parpola_1982,,P900,,M100,,,5,0,0,0,True,0\n"
        "P901,parpola_1982,,P901,042,M100,,,9,0,0,0,True,0\n"
        "P902,parpola_1982,,P902,,M101,,,7,0,0,0,True,0\n"
        "P903,parpola_1982,,P903,,M101,,,7,0,0,0,True,0\n",
        encoding="utf-8")
    maps = build_sign_maps(reg)
    # highest corpus_freq wins
    assert maps["m2p"]["M100"] == "P901"
    # equal-freq multi-claim is ambiguous, not silently resolved
    assert "M101" in maps["m_ambiguous"]
    assert "M101" not in maps["m2p"]
    # wells zero-padding normalized before lookup
    assert maps["w2p"]["42"] == "P901"


def test_mapper_unk_kinds(mapper):
    stats = Counter()
    assert mapper.map_m("M002", stats) == "UNK"  # ambiguous (spec A)
    assert stats["ambiguous"] == 1
    assert mapper.map_m("M9999", stats) == "UNK"  # unmapped
    assert stats["unmapped"] == 1
    assert mapper.map_w("0151", stats) == "P001"  # zero-padded Wells


# ------------------------------------------------------------ spec section 5

def _rec(tokens, site="s"):
    return {"inscription_id": "x", "site": site, "tokens": list(tokens)}


def test_dedup_stage_a_exact():
    kept, counts = dedup([_rec(["P001", "P009"]), _rec(["P001", "P009"]),
                          _rec(["P009", "P001"])])
    assert counts == {"input": 3, "stage_a_removed": 1,
                      "stage_b_removed": 0, "stage_c_removed": 0,
                      "kept": 2}
    assert len(kept) == 2


def test_dedup_stage_b_sentinel_normalized():
    kept, counts = dedup([_rec(["UNK", "P001"]), _rec(["P001", "UNK"]),
                          _rec(["P001"])])
    # stripped sequences: (P001,), (P001,), (P001,) -> two dropped
    assert counts["stage_a_removed"] == 0
    assert counts["stage_b_removed"] == 2
    assert len(kept) == 1


def test_dedup_stage_c_near_duplicate_and_floor():
    a = _rec(["P001", "P002", "P003", "P004"])
    b = _rec(["P001", "P002", "P003", "P005"])  # distance 1 from a
    short = _rec(["P001", "P002", "P003"])  # stripped len 3: exempt
    kept, counts = dedup([a, b, short])
    assert counts["stage_c_removed"] == 1
    assert kept == [a, short]


def test_dedup_stage_c_no_chaining():
    # c is distance 1 from b but distance 2 from kept anchor a;
    # comparisons run against kept anchors only, so c survives.
    a = _rec(["P001", "P002", "P003", "P004"])
    b = _rec(["P001", "P002", "P003", "P005"])
    c = _rec(["P001", "P002", "P006", "P005"])
    kept, counts = dedup([a, b, c])
    assert counts["stage_c_removed"] == 1
    assert kept == [a, c]


# ------------------------------------------------------------ spec section 7

def test_adapter_rmrl(mapper):
    ds = adapt_rmrl_concordance(FIXTURES / "toy_rmrl_confirmed.csv",
                                mapper, "toy", "synthetic", "fixture")
    assert ds.source_class == "rmrl_concordance"
    assert [r["tokens"] for r in ds.records][0] == ["P001", "P009"]
    assert ds.stats["inscriptions"] == 5
    assert ds.stats["tokens_unmapped"] == 0
    assert ds.provenance["as_built"]["inscriptions"] == 5


def test_adapter_image(mapper):
    ds = adapt_image_transcription(FIXTURES / "toy_image.csv", mapper,
                                   "toy", "synthetic", "fixture")
    assert [r["tokens"] for r in ds.records] == [["P001", "P009"],
                                                 ["P013", "P004"]]
    assert ds.provenance["records_with_confidences"] == 2


def test_adapter_converted_layer(mapper):
    ds = adapt_converted_layer(FIXTURES / "toy_layer.json", mapper, "toy")
    assert ds.source_class == "icit_lineage_derivative"
    assert ds.provenance["status"] == "dry-run-only"
    assert ds.stats["tokens_unmapped"] == 1  # M0999
    kept, counts = dedup(ds.records)
    assert counts["kept"] == 3 and counts["stage_a_removed"] == 1


# ------------------------------------------------- toy end-to-end evaluation

def test_toy_prediction_confirmed(mapper, classes):
    ds = adapt_rmrl_concordance(FIXTURES / "toy_rmrl_confirmed.csv",
                                mapper, "toy", "synthetic", "fixture")
    out = evaluate(TOY_PRED, ds, classes, set())
    assert out["verdict"] == "CONFIRMED"
    assert out["k"] == 2
    assert out["per_sign"]["P001"]["rate"] == pytest.approx(2 / 3)
    assert out["per_sign"]["P004"]["rate"] == pytest.approx(0.5)


def test_toy_prediction_refuted(mapper, classes):
    ds = adapt_rmrl_concordance(FIXTURES / "toy_rmrl_refuted.csv",
                                mapper, "toy", "synthetic", "fixture")
    out = evaluate(TOY_PRED, ds, classes, set())
    assert out["verdict"] == "REFUTED"
    assert out["k"] == 0


def test_real_template_scorer_on_toy_fixtures(mapper, classes):
    pred = PREDICTIONS["PRED-2026-003"]
    ds_ok = adapt_future_concordance(
        FIXTURES / "toy_future_confirmed.json", mapper, "toy",
        "synthetic", "fixture")
    out = evaluate(pred, ds_ok, classes, set())
    assert out["verdict"] == "CONFIRMED"
    assert out["coverage"] == pytest.approx(0.8)
    ds_no = adapt_future_concordance(
        FIXTURES / "toy_future_refuted.json", mapper, "toy",
        "synthetic", "fixture")
    out = evaluate(pred, ds_no, classes, set())
    assert out["verdict"] == "REFUTED"
    assert out["coverage"] == pytest.approx(0.4)


# ------------------------------------------------------------ spec section 6

def test_gate_refuses_nonqualifying_class(mapper, classes):
    ds = adapt_converted_layer(FIXTURES / "toy_layer.json", mapper, "toy")
    with pytest.raises(NotEvaluable) as exc:
        evaluate(PREDICTIONS["PRED-2026-001"], ds, classes, set())
    assert "does not qualify" in exc.value.reason


def test_gate_refuses_incomplete_provenance(mapper, classes):
    ds = adapt_rmrl_concordance(FIXTURES / "toy_rmrl_confirmed.csv",
                                mapper, "toy", "", "fixture")
    with pytest.raises(NotEvaluable) as exc:
        evaluate(TOY_PRED, ds, classes, set())
    assert "provenance incomplete" in exc.value.reason


def test_gate_refuses_unmapped_share(mapper, classes):
    ds = IngestedDataset(
        name="toy", source_class="rmrl_concordance",
        records=[_rec(["UNK", "UNK", "UNK", "P001"])],
        provenance=_toy_prov(),
        stats={"inscriptions": 1, "tokens": 4, "tokens_unmapped": 3,
               "tokens_ambiguous": 0, "distinct_signs": 1})
    with pytest.raises(NotEvaluable) as exc:
        evaluate(TOY_PRED, ds, classes, set())
    assert "unmapped+ambiguous" in exc.value.reason


def test_gate_multisite_for_template(mapper, classes):
    ds = adapt_future_concordance(
        FIXTURES / "toy_future_confirmed.json", mapper, "toy",
        "synthetic", "fixture")
    for r in ds.records:
        r["site"] = "only-site"
    with pytest.raises(NotEvaluable) as exc:
        evaluate(PREDICTIONS["PRED-2026-003"], ds, classes, set())
    assert "multi-site" in exc.value.reason


def test_verdict_lock(mapper, classes):
    ds = adapt_rmrl_concordance(FIXTURES / "toy_rmrl_confirmed.csv",
                                mapper, "toy", "synthetic", "fixture")
    lock: set = set()
    evaluate(TOY_PRED, ds, classes, lock)
    with pytest.raises(NotEvaluable) as exc:
        evaluate(TOY_PRED, ds, classes, lock)
    assert "verdict lock" in exc.value.reason


# ------------------------------------------------------------ spec section 8

def test_dry_run_label_and_no_criterion_statistics(mapper, classes):
    ds = adapt_converted_layer(FIXTURES / "toy_layer.json", mapper, "toy")
    out = dry_run(ds, classes)
    assert out["label"] == DRY_RUN_LABEL
    blob = json.dumps(out)
    assert "verdict" not in blob
    assert "meets_criterion" not in blob
    assert '"rate"' not in blob
    assert '"coverage":' not in blob  # no scored template coverage
    cov = out["coverage_post_dedup"]
    assert cov["TERMINAL"]["set_size"] == 14
    assert cov["TERMINAL"]["per_sign_occurrences"]["P385"] == 0


# ------------------------------------------------------------------- H23

def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase119PredHarness" in ATOMIC_NODES
