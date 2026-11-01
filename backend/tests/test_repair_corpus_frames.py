"""Tests for the gap-aware corpus representation (repair WP6).

Covers: leading unknowns, trailing unknowns, internal gaps, marked
signs, singleton-after-filtering, boundary-semantics naming, the
repeated-identifier cross-scheme join block, and within-scheme
analysis being unaffected by join repeats.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from glossa_lab.corpus_frames import (
    BoundarySemantics,
    GapAwareFrame,
    InscriptionRecord,
    RecordKind,
    TokenState,
    analyze_within_scheme,
    classify_positions,
    damaged,
    final_token,
    initial_token,
    join_on_mahadevan,
    legible,
    marked,
    unknown_gap,
)

ORIG = BoundarySemantics.ORIGINAL_BOUNDARY
FIRST = BoundarySemantics.FIRST_LEGIBLE


def rec(tokens, **kw):
    kw.setdefault("object_id", "OBJ-1")
    return InscriptionRecord(tokens=tuple(tokens), **kw)


def slots(record, boundary):
    return {t.sign_id: s for t, s in classify_positions(record, boundary=boundary)}


# --- leading unknowns -------------------------------------------------------

def test_leading_unknown_original_boundary():
    r = rec([unknown_gap(), legible("A"), legible("B")])
    # The gap occupies place 0, so no legible sign is initial; A is medial.
    assert initial_token(r, boundary=ORIG).sign_id is None
    assert slots(r, ORIG) == {"A": "medial", "B": "final"}


def test_leading_unknown_first_legible():
    r = rec([unknown_gap(), legible("A"), legible("B")])
    assert initial_token(r, boundary=FIRST).sign_id == "A"
    assert slots(r, FIRST) == {"A": "initial", "B": "final"}


# --- trailing unknowns ------------------------------------------------------

def test_trailing_unknown_original_boundary():
    r = rec([legible("A"), legible("B"), unknown_gap()])
    assert final_token(r, boundary=ORIG).sign_id is None
    assert slots(r, ORIG) == {"A": "initial", "B": "medial"}


def test_trailing_unknown_first_legible():
    r = rec([legible("A"), legible("B"), unknown_gap()])
    assert final_token(r, boundary=FIRST).sign_id == "B"
    assert slots(r, FIRST) == {"A": "initial", "B": "final"}


# --- internal gaps ----------------------------------------------------------

def test_internal_gap_both_semantics_agree_on_boundaries():
    r = rec([legible("A"), unknown_gap(), legible("B")])
    for b in (ORIG, FIRST):
        assert slots(r, b) == {"A": "initial", "B": "final"}
    # The gap itself is a real place: 3 places, 2 legible tokens.
    assert len(r.tokens) == 3
    assert len(r.legible_tokens) == 2
    assert r.compressed_sign_ids() == ["A", "B"]


def test_damaged_token_keeps_its_place():
    r = rec([legible("A"), damaged("B"), legible("C")])
    assert [t.state for t in r.tokens] == [
        TokenState.LEGIBLE, TokenState.DAMAGED, TokenState.LEGIBLE]
    assert len(r.tokens) == 3
    # A damaged token is not legible, so it holds no slot; its place is
    # still counted in the original length (see census in frame test).
    assert r.compressed_sign_ids() == ["A", "C"]


# --- marked signs -----------------------------------------------------------

def test_marked_sign_is_kept_and_named():
    r = rec([legible("A"), marked("B", raw="*B")])
    assert r.tokens[1].state is TokenState.MARKED
    assert r.tokens[1].sign_id == "B"
    # The historical compressed view drops marked tokens (the Spec 076
    # pilot dropped 452 of them); the gap-aware view keeps the place.
    assert r.compressed_sign_ids() == ["A"]
    assert len(r.tokens) == 2


# --- singleton after filtering ----------------------------------------------

def test_singleton_after_filtering():
    r = rec([unknown_gap(), legible("A"), unknown_gap()])
    # Compressed view: one token, so A looks like a solo inscription.
    assert slots(r, FIRST) == {"A": "solo"}
    # Original inscription: A is in the middle place of three.
    assert slots(r, ORIG) == {"A": "medial"}


def test_true_singleton_is_solo_under_both():
    r = rec([legible("A")])
    assert slots(r, FIRST) == {"A": "solo"}
    assert slots(r, ORIG) == {"A": "solo"}


# --- boundary semantics must be chosen and named ------------------------------

def test_boundary_semantics_is_forced():
    r = rec([legible("A"), legible("B")])
    with pytest.raises(ValueError):
        initial_token(r)  # no default
    with pytest.raises(ValueError):
        initial_token(r, boundary=None)
    with pytest.raises(ValueError):
        GapAwareFrame(records=[r]).positional_counts()


def test_positional_results_name_the_semantics_used():
    r = rec([unknown_gap(), legible("A"), legible("B")])
    res_first = initial_token(r, boundary=FIRST)
    res_orig = initial_token(r, boundary=ORIG)
    assert res_first.boundary_semantics is FIRST
    assert res_orig.boundary_semantics is ORIG
    assert "FIRST_LEGIBLE" in res_first.describe()
    assert "ORIGINAL_BOUNDARY" in res_orig.describe()
    frame = GapAwareFrame(records=[r])
    counts = frame.positional_counts(boundary=FIRST)
    assert counts.to_dict()["boundary_semantics"] == "FIRST_LEGIBLE"
    counts_orig = frame.positional_counts(boundary=ORIG)
    assert counts_orig.to_dict()["boundary_semantics"] == "ORIGINAL_BOUNDARY"
    # And the counts themselves differ, which is the point.
    assert (counts.init, counts.fin, counts.med) == (1, 1, 0)
    assert (counts_orig.init, counts_orig.fin, counts_orig.med) == (0, 1, 1)


# --- record kinds are distinct, never silently merged -------------------------

def test_record_kinds_stay_distinct():
    base = dict(tokens=(legible("A"),))
    frame = GapAwareFrame(records=[
        InscriptionRecord(object_id="OBJ-1", record_kind=RecordKind.ORIGINAL_ARTIFACT, **base),
        InscriptionRecord(object_id="OBJ-1-copy", record_kind=RecordKind.REPEAT_IMPRESSION,
                          related_object_id="OBJ-1", **base),
        InscriptionRecord(object_id="OBJ-1-pub2", record_kind=RecordKind.DUPLICATE_PUBLICATION,
                          related_object_id="OBJ-1", **base),
        InscriptionRecord(object_id="OBJ-1-tr2", record_kind=RecordKind.DUPLICATE_TRANSCRIPTION,
                          related_object_id="OBJ-1", **base),
    ])
    census = frame.census()
    assert census["records"] == 4
    assert census["records_by_kind"] == {
        "original_artifact": 1, "repeat_impression": 1,
        "duplicate_publication": 1, "duplicate_transcription": 1}


def test_stable_identifiers_round_trip():
    r = InscriptionRecord(
        object_id="M-123", face="A", catalog_id="CISI-123",
        source_lineage="CISI vol.1 / M-123", scheme="mahadevan",
        tokens=(unknown_gap(), legible("047")),
        direction="rtl", direction_uncertain=True)
    d = r.to_dict()
    assert InscriptionRecord.from_dict(d) == r
    assert d["face"] == "A" and d["catalog_id"] == "CISI-123"
    assert d["direction_uncertain"] is True


# --- cross-scheme join: repeated identifier blocks -----------------------------

def test_repeated_mahadevan_id_blocks_join():
    left = [{"mahadevan_id": "M002", "scheme": "mahadevan"},
            {"mahadevan_id": "M076", "scheme": "mahadevan"}]
    right = [{"mahadevan_id": "M002", "parpola_id": "P002"},
             {"mahadevan_id": "M076", "parpola_id": "P076a"},
             {"mahadevan_id": "M076", "parpola_id": "P076b"}]  # repeated
    result = join_on_mahadevan(left, right)
    joined_ids = [a["mahadevan_id"] for a, _ in result.joined]
    assert joined_ids == ["M002"]            # unambiguous pair still joins
    assert result.blocked_ids == ["M076"]     # repeated sign is blocked
    blocked = result.blocked[0]
    assert blocked.left_count == 1 and blocked.right_count == 2
    assert "repeated" in blocked.reason


def test_repeated_id_on_left_also_blocks():
    left = [{"mahadevan_id": "M050"}, {"mahadevan_id": "M050"}]
    right = [{"mahadevan_id": "M050"}]
    result = join_on_mahadevan(left, right)
    assert result.joined == ()
    assert result.blocked_ids == ["M050"]


def test_join_never_silently_takes_first_match():
    left = [{"mahadevan_id": "M001", "v": "only"}]
    right = [{"mahadevan_id": "M001", "v": "first"},
             {"mahadevan_id": "M001", "v": "second"}]
    result = join_on_mahadevan(left, right)
    assert result.joined == ()
    assert result.blocked_ids == ["M001"]


def test_within_scheme_analysis_unaffected_by_join_repeats():
    records = [
        rec([legible("076"), legible("002")], object_id="O1", scheme="mahadevan"),
        rec([legible("076")], object_id="O2", scheme="mahadevan"),
        rec([legible("076")], object_id="O3", scheme="parpola"),
    ]
    out = analyze_within_scheme(records, "mahadevan")
    assert out["join_used"] is False
    assert out["records"] == 2
    assert out["sign_counts"] == {"002": 1, "076": 2}
