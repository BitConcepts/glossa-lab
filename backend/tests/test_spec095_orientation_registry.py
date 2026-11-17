"""Spec 095 Stage 3 (T304) — orientation basis carried as data.

Every claim-bearing corpus in the Stage 1 registry carries an
orientation basis of record, and the Corpus Identity Standard
states the requirement (its section 5): a positional result names
its orientation assumption and files its reversed variant or an
undefined-reversal statement.
"""

from __future__ import annotations

from pathlib import Path

from glossa_lab.data import corpus_identity as ci

ROOT = Path(__file__).resolve().parents[2]


def test_every_registered_corpus_carries_an_orientation_basis():
    assert len(ci.CORPUS_IDENTITIES) == 8
    for key, ident in ci.CORPUS_IDENTITIES.items():
        assert ident.orientation_basis, key
        # The basis as registered states the corpus's own position;
        # on 2026-11-16 every entry records that the corpus itself
        # records no direction, and names the standing assumption.
        assert "Not recorded" in ident.orientation_basis, key


def test_the_standard_states_the_orientation_requirement():
    text = (ROOT / "glossa-indus" / "CORPUS_IDENTITY_STANDARD.md").read_text(
        encoding="utf-8"
    )
    assert "## 5. Orientation basis" in text
    assert "orientation_basis" in text
