"""Phase-392 (Spec 027 Stage 1, Q2 gate) — machinery + results.

Unit tests pin the adjusted-R^2 correction and pipeline
determinism on synthetic populations. The results test pins
the executed population against the frozen margins audit and
requires a verdict in the Spec 026 taxonomy whose rule inputs
are internally consistent (it re-derives the verdict from the
recorded quantities under stage1-freeze.md section 6).
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "backend" / "scripts" / "phase392_q2_gate.py"
RESULTS = REPO / "reports" / "phase392_results.json"
AUDIT = (REPO / "specs" / "027-movement-culture-language"
         / "stage1" / "margins-audit.json")
STORE = REPO / "corpora" / "downloads" / "spec027_stage1"


def _load():
    spec = importlib.util.spec_from_file_location("phase392", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_adjusted_r2_null_centring():
    m = _load()
    # Raw R^2 at its null expectation (g-1)/(n-1) adjusts to ~0.
    n, g = 392, 6
    assert abs(m.adjusted_r2((g - 1) / (n - 1), n, g)) < 1e-9
    assert m.adjusted_r2(0.05, n, g) > 0.03
    assert m.adjusted_r2(0.0, n, g) < 0.0  # can go negative


def test_pipeline_deterministic_under_seed():
    m = _load()
    rng = np.random.default_rng(7)
    entries, vecs = [], []
    probs = rng.dirichlet(np.ones(12))
    gen = np.random.default_rng(11)
    for site in ("A", "B", "C", "D", "E", "F"):
        for tc in ("SEAL", "TAB"):
            for _ in range(60):
                length = int(gen.integers(2, 8))
                vecs.append(np.bincount(
                    gen.choice(12, size=length, p=probs),
                    minlength=12).astype(float))
                entries.append({"site": site, "type_class": tc,
                                "n_legible": length})
    vecs = np.array(vecs)
    r1 = m.run_pipeline(entries, vecs, np.random.default_rng(5))
    r2 = m.run_pipeline(entries, vecs, np.random.default_rng(5))
    assert r1["adj_draws"] == r2["adj_draws"]
    assert r1["p_draws"] == r2["p_draws"]
    s = m.summarise(r1)
    # Homogeneous population: the instrument must not find
    # structure (share rejecting near alpha, adjusted ~ 0).
    assert s["share_draws_rejecting"] < 0.5
    assert abs(s["median_adj_r2"]) < 0.01


@pytest.mark.skipif(not STORE.is_dir(),
                    reason="stage1 input store not staged")
def test_results_population_and_verdict_consistency():
    m = _load()
    assert RESULTS.is_file(), "phase392 has not been run"
    res = json.loads(RESULTS.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert res["population_reproduced"] is True
    assert res["population_flow"] == audit["population_flow"]
    assert res["analysis_records"] == 3030
    assert res["sign_columns"] == 125
    assert res["seed"] == 20261011
    assert res["n_cell"] == 49
    assert res["verdict"] in ("SUPPORTED", "CONTRADICTED",
                              "INCONCLUSIVE", "INVALID")
    if res["verdict"] != "INVALID":
        prim = res["primary"]
        neg = res["negative_control"]
        pos = res["positive_control"]
        assert neg["pass"] and pos["pass"]
        share = prim["share_draws_rejecting"]
        lo, hi = prim["adj_r2_interval_95"]
        loso = [v for v in res["loso_median_adj_r2"].values()
                if v is not None]
        # Re-derive the verdict from the recorded quantities.
        if (share >= 0.95 and lo > 0.01
                and all(v > 0.01 for v in loso)):
            expect = "SUPPORTED"
        elif (1.0 - share) >= 0.95 or hi <= 0.01:
            expect = "CONTRADICTED"
        else:
            expect = "INCONCLUSIVE"
        assert res["verdict"] == expect
