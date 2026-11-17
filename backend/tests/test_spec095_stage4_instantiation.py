"""Spec 095 Stage 4 (T401/T402) — the multi-script model and its
Indus instantiation.

The specification (docs/MULTISCRIPT_MODEL.md) covers every entity
in C095-11's enumeration of record — eighteen names under the
claim's "seventeen entities" wording; the enumeration governs —
each with its own claim (ME-nn) and falsifier. The Indus record
instantiates the model with zero changed facts, counts, or
standings: this test re-derives the instantiation census from the
record itself, so a silent change to the ledger, the anchors
register, the matrix, or the corpus registry fails here.
"""

from __future__ import annotations

import json
from pathlib import Path

from glossa_lab.data import corpus_identity as ci

ROOT = Path(__file__).resolve().parents[2]

# C095-11's enumeration of record, in order (counted from the
# claim text at Stage 4: eighteen names).
ENTITIES = [
    "WritingSystem",
    "LanguageHypothesis",
    "Corpus",
    "Artifact",
    "Inscription",
    "Sign",
    "SignVariant",
    "Transcription",
    "ReadingHypothesis",
    "TranslationHypothesis",
    "Context",
    "Evidence",
    "Claim",
    "Falsifier",
    "Experiment",
    "Execution",
    "Result",
    "Adjudication",
]


def _model_text() -> str:
    return (ROOT / "docs" / "MULTISCRIPT_MODEL.md").read_text(encoding="utf-8")


def _ledger_rows() -> list[dict]:
    path = ROOT / "glossa-indus" / "ledger" / "claims.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_model_spec_covers_every_enumerated_entity_with_claim_and_falsifier():
    text = _model_text()
    for i, name in enumerate(ENTITIES, start=1):
        assert f"### 3.{i} {name}" in text, name
        assert f"ME-{i:02d}" in text, name
    # Each entity block states a falsifier.
    assert text.count("*Falsifier:*") >= len(ENTITIES)


def test_model_generic_layer_names_no_script_specific_assumption():
    text = _model_text()
    # The separation contract: shape carries no value or meaning.
    assert "carries no phonetic value" in text
    # The generic rules are stated as rules of the layer (G1-G6).
    for rule in ("G1", "G2", "G3", "G4", "G5", "G6"):
        assert f"**{rule} " in text, rule


def test_indus_claims_census_unchanged():
    rows = _ledger_rows()
    claims = [r for r in rows if r.get("kind") == "claim"]
    assert len(rows) == 1025
    assert len(claims) == 994
    assert len(rows) - len(claims) == 31
    # Falsifier coverage: 985 of 994; the 9 without are GR-088-21.
    assert sum(1 for r in claims if r.get("falsifier")) == 985
    # Claim -> Sign linkage: exactly one claim carries sign_refs
    # (3 references) — the GR-088-07 gap, stated in the mapping.
    with_refs = [r for r in claims if r.get("sign_refs")]
    assert len(with_refs) == 1
    assert sum(len(r["sign_refs"]) for r in with_refs) == 3


def test_indus_anchors_census_unchanged():
    data = json.loads((ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json").read_text(encoding="utf-8"))
    assert data["total"] == 287
    assert len(data["anchors"]) == 287
    assert data["by_confidence"] == {"HIGH": 166, "MEDIUM": 5, "LOW": 3, "CANDIDATE": 113}
    # The separation contract in the realization: a reading lives on
    # the anchor (hypothesis) entry with its basis and confidence —
    # the sign's identity is its key, not a value stored as shape.
    for sign, entry in data["anchors"].items():
        assert "reading" in entry and "confidence" in entry and "basis" in entry, sign


def test_indus_corpus_registry_unchanged():
    assert len(ci.CORPUS_IDENTITIES) == 8
    for key, ident in ci.CORPUS_IDENTITIES.items():
        # Every identity of record is complete (C095-3's shape).
        assert ident.version and ident.source and ident.licensing, key
        assert ident.census_basis and ident.normalization, key
        assert ident.orientation_basis, key


def test_indus_matrix_census_unchanged():
    matrix = json.loads((ROOT / "glossa-indus" / "matrix" / "matrix.json").read_text(encoding="utf-8"))
    assert len(matrix["rows"]) == 994
    assert len(matrix["columns"]) == 644


def test_translation_hypothesis_emptiness_is_stated_not_papered():
    # The mapping states the empty entity plainly (§6): the program
    # holds no translation of any Indus sequence.
    text = _model_text()
    assert "TranslationHypothesis | **No instance.**" in text
