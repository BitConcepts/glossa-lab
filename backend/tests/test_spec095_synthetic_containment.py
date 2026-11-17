"""Spec 095 Stage 2 — synthetic corpus containment tests (T204).

Claim covered:
  C095-6  The synthetic corpus is contained by census and a
          planted-fixture test: every consumer of
          indus_public_corpus is enumerated and classified, no
          claim-bearing path consumes it, a planted fixture that
          presents the synthetic corpus as a real corpus in a
          claim-bearing path fails, and the public loader's synthetic
          labelling is machine-checked, not comment-only.

Census of record (Stage 2 record, 2026-11-16) — import consumers in
backend/, pinned by test_consumer_census_is_complete below:
  * glossa_lab/corpus_seeder.py — startup seed; the corpus is seeded
    under the id "indus_synthetic" with SYNTHETIC in its name and
    metadata status. Classification: demonstration seed, labelled.
  * glossa_lab/experiment_graph.py (BuiltinCorpus node) — the "indus"
    built-in corpus IS this synthetic prototype. Classification:
    demonstration/source node; its output is labelled by the
    corpus_status key (Stage 2 containment).
  * glossa_lab/analyze_script.py — demo analysis loader; returns the
    label "Indus (Synthetic — ...)" beside the data.
    Classification: demonstration, labelled.
  * glossa_lab/experiments/_legacy/{tier5_indus_decipherment,
    progression_report, tier5_indus_readings, indus_structural_atlas,
    remaining_experiments}.py — legacy experiment modules, not wired
    into the live application. Classification: legacy demonstration.
  * tests/test_spec095_corpus_battery.py (Spec 095 Stage 1) and this
    file. Classification: test.
Reference-only consumers (no import; pinned separately below):
  * glossa_lab/corpus_catalogue_seeder.py — names the module in the
    catalogue entry's local_module field; the entry's name and
    description carry "synthetic". Classification: catalogue, labelled.
  * scripts/foundation_check.py — presence check on the module file
    only; consumes no data.
Removed at Stage 2:
  * glossa_lab/data/indus_corpus_v2.py — the claim-bearing V1 loader
    formerly named the synthetic prototype as a fallback tier. The
    tier was unreachable (it imported a load_corpus the synthetic
    module does not define) and is removed; the loader now has no
    synthetic path at all (pinned below).
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from glossa_lab import corpus_catalogue_seeder, corpus_seeder
from glossa_lab.data import corpus_identity as ci
from glossa_lab.data import indus_corpus_v2 as v2
from glossa_lab.data import indus_public_corpus

BACKEND = Path(__file__).resolve().parents[1]

EXPECTED_IMPORT_CONSUMERS = {
    "glossa_lab/corpus_seeder.py",
    "glossa_lab/experiment_graph.py",
    "glossa_lab/analyze_script.py",
    "glossa_lab/experiments/_legacy/tier5_indus_decipherment.py",
    "glossa_lab/experiments/_legacy/progression_report.py",
    "glossa_lab/experiments/_legacy/tier5_indus_readings.py",
    "glossa_lab/experiments/_legacy/indus_structural_atlas.py",
    "glossa_lab/experiments/_legacy/remaining_experiments.py",
    "tests/test_spec095_corpus_battery.py",
    "tests/test_spec095_synthetic_containment.py",
}


def _import_consumers() -> set[str]:
    """All backend/ modules that import indus_public_corpus (AST scan)."""
    found = set()
    for root in (BACKEND / "glossa_lab", BACKEND / "scripts", BACKEND / "tests"):
        for path in root.rglob("*.py"):
            if path.name == "indus_public_corpus.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                hit = False
                if isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    hit = module.endswith("indus_public_corpus") or (
                        module in ("glossa_lab.data", "data")
                        and any(a.name == "indus_public_corpus" for a in node.names)
                    )
                elif isinstance(node, ast.Import):
                    hit = any(
                        a.name.endswith("indus_public_corpus") for a in node.names
                    )
                if hit:
                    found.add(str(path.relative_to(BACKEND)))
                    break
    return found


# ── The census is complete: an unnamed consumer fails this test ────────────


def test_consumer_census_is_complete():
    assert _import_consumers() == EXPECTED_IMPORT_CONSUMERS


# ── The labelling is machine-checked, not comment-only ─────────────────────


def test_synthetic_labelling_is_machine_readable():
    assert indus_public_corpus.SYNTHETIC is True
    assert indus_public_corpus.CORPUS_KIND == "SYNTHETIC"
    assert "SYNTHETIC" in indus_public_corpus.SYNTHETIC_LABEL
    stats = indus_public_corpus.corpus_statistics()
    assert stats["corpus_kind"] == "SYNTHETIC"
    assert stats["synthetic"] is True
    assert "SYNTHETIC" in stats["status"]


def test_seeded_synthetic_corpus_is_labelled():
    assert "synthetic" in corpus_seeder._corpus_name("indus_synthetic").lower()
    loaded = corpus_seeder._load_corpus("indus_synthetic")
    assert loaded is not None
    assert "SYNTHETIC" in loaded["metadata"]["status"]
    assert "Synthetic" in loaded["metadata"]["source"]


def test_catalogue_entry_is_labelled():
    entries = [
        e for e in corpus_catalogue_seeder.CATALOGUE
        if e.get("local_module") == "indus_public_corpus"
    ]
    assert len(entries) == 1
    entry = entries[0]
    assert "synthetic" in entry["name"].lower()
    assert "synthetic" in entry["description"].lower()


def test_builtin_corpus_indus_output_is_labelled():
    """The BuiltinCorpus node's 'indus' branch serves the synthetic
    prototype; Stage 2 labels its output so the material cannot be
    mistaken for inscription data (sequences themselves unchanged)."""
    from glossa_lab import experiment_graph as eg

    result = eg.ATOMIC_NODES["BuiltinCorpus"].fn({}, {"corpus": "indus"})
    assert result["sequences"]
    assert result["total_tokens"] > 0
    assert "SYNTHETIC" in result["corpus_status"]
    assert "not inscription data" in result["corpus_status"]


# ── No claim-bearing path consumes the synthetic corpus ────────────────────


def test_v2_loader_has_no_synthetic_import():
    tree = ast.parse(
        (BACKEND / "glossa_lab" / "data" / "indus_corpus_v2.py").read_text(
            encoding="utf-8"
        )
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert "indus_public_corpus" not in (node.module or "")
        elif isinstance(node, ast.Import):
            assert all(
                "indus_public_corpus" not in a.name for a in node.names
            )


def test_v2_loader_serves_nothing_rather_than_synthetic(monkeypatch, tmp_path):
    """Planted fixture: no real corpus tier is available while the
    synthetic corpus exists and is importable — the exact condition
    under which the removed fallback tier named synthetic data as the
    last resort. The claim-bearing loader must serve nothing."""
    import glossa_lab.data.indus_cisi as cisi

    assert indus_public_corpus.get_corpus_inscriptions()  # synthetic exists
    monkeypatch.setattr(v2, "_EXPORT_PATH", tmp_path / "missing.jsonl")
    monkeypatch.setattr(v2, "_CACHE", None)
    monkeypatch.setattr(v2, "_TIER", None)
    # raising=False: indus_cisi currently defines no load_corpus (its
    # loader is _load_corpus), so the attribute is created to model
    # "CISI tier unavailable" deterministically.
    monkeypatch.setattr(cisi, "load_corpus", lambda: [], raising=False)
    assert v2.load_corpus() == []
    assert v2.corpus_status()["tier"].startswith("empty")


def test_synthetic_presented_as_strict_corpus_is_refused(tmp_path):
    """Planted fixture: synthetic inscriptions written out as a
    corpus file and presented to the identity enforcement the
    claim-bearing loaders share, under the strict corpus's identity
    of record. Enforcement refuses: the content hash differs from
    the pin."""
    synthetic = indus_public_corpus.get_corpus_inscriptions()
    planted = tmp_path / "firestore_indusarrays_full.jsonl"
    planted.write_text(
        "\n".join(
            json.dumps({"dockey": 1001 + i, "signs": seq})
            for i, seq in enumerate(synthetic[:25])
        )
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ci.CorpusIdentityError):
        ci.enforce_file_identity("indus_v3_firestore_strict", planted)
