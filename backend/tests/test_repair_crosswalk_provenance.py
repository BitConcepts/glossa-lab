"""WP4 tests: crosswalk provenance classifier (repair 2026-10-26).

Covers the three acceptance properties from the repair brief's
Work Package 4 on synthetic fixtures, plus a real-data smoke test
against the generated overlay:

(i)   a synthetic source -> copied comparator -> original source
      cycle earns NO support;
(ii)  mutating the project reading does not alter the stored
      comparator value or its classification;
(iii) an independently coded source value stays fixed with its
      source revision.

The classifier module is loaded by file path from the staged patch
tree (``../glossa_lab/crosswalk_provenance.py``), so these tests run
without the package being installed.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve()
MODULE_PATH = HERE.parents[1] / "glossa_lab" / "crosswalk_provenance.py"
OVERLAY_PATH = (HERE.parents[1] / "glossa_lab" / "data"
                / "mahadevan_parpola_crosswalk_v2_provenance.json")


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "crosswalk_provenance", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cp = _load_module()


# ── Synthetic fixtures ───────────────────────────────────────────────

def _phase96_style_entry(reading: str) -> dict:
    """An entry in the exact shape the Phase-96 builder writes: the
    reading and the anchor_confidence are both taken from the anchor
    entry being processed, under the stated source of a
    sign-correspondence table."""
    return {
        "mahadevan_id": "M047",
        "parpola_id": "P047",
        "parpola_num": 47,
        "source": "Parpola 1994 Appendix B",
        "confidence": "HIGH",
        "reading": reading,
        "anchor_confidence": "MEDIUM",
    }


def _independent_entry() -> dict:
    """An entry coded directly from a primary source, carrying an
    exact locator (work + page + sign scheme) and a source revision."""
    return {
        "mahadevan_id": "M999",
        "parpola_id": "P999",
        "parpola_num": 999,
        "source": "Example, A. 2000. A Sign List.",
        "confidence": "HIGH",
        "reading": "mīn",
        "value_origin": "independent_primary_source",
        "primary_source_locator": {
            "work": "Example, A. 2000. A Sign List.",
            "page": "p. 123, table 4",
            "sign_scheme": "Mahadevan 1977 numbering",
        },
        "source_revision": "signlist-2000-printing-2",
    }


# ── Acceptance property (i): a copied cycle earns no support ─────────

def test_copied_cycle_earns_no_support_even_when_identical():
    # The primary source's value, adopted by the project anchor, then
    # copied back into the crosswalk by the builder. The comparison
    # is byte-identical — and still worth nothing as validation.
    source_value = "min/mīn"
    anchor = {"reading": source_value, "confidence": "HIGH"}
    entry = _phase96_style_entry(reading=source_value)
    rec = cp.classify_entry("M047", entry, anchor)
    assert rec["identity"]["raw_identical"] is True
    assert rec["identity"]["normalized_identical"] is True
    assert rec["comparison_classification"] == cp.PROJECT_DERIVED
    assert rec["eligible_for_independent_validation"] is False
    assert cp.earns_independent_support(rec) is False


def test_copied_cycle_stays_project_derived_when_anchor_moves_on():
    # A stale copy (the anchor was corrected after the copy) is still
    # a copy: disagreement does not launder provenance either.
    entry = _phase96_style_entry(reading="pār")
    anchor = {"reading": "nē", "confidence": "MEDIUM"}
    rec = cp.classify_entry("M024", entry, anchor)
    assert rec["identity"]["normalized_identical"] is False
    assert rec["comparison_classification"] == cp.PROJECT_DERIVED
    assert cp.earns_independent_support(rec) is False


# ── Acceptance property (ii): anchor mutation changes nothing ───────

def test_mutating_project_reading_changes_neither_value_nor_class():
    entry = _phase96_style_entry(reading="min/mīn")
    before = cp.classify_entry("M047", entry, {"reading": "min/mīn"})
    after = cp.classify_entry("M047", entry, {"reading": "kur"})
    # Stored comparator value untouched by the mutation.
    assert after["phonetic_reading"]["value"] == "min/mīn"
    assert after["phonetic_reading"]["value"] == \
        before["phonetic_reading"]["value"]
    # Classification derives from provenance fields, not agreement.
    assert after["comparison_classification"] == \
        before["comparison_classification"] == cp.PROJECT_DERIVED
    # Only the reported identity flags move.
    assert before["identity"]["raw_identical"] is True
    assert after["identity"]["raw_identical"] is False


# ── Acceptance property (iii): independent value stays fixed ────────

def test_independently_coded_value_fixed_with_source_revision():
    entry = _independent_entry()
    rec = cp.classify_entry("M999", entry, {"reading": "mīn"},
                            source_revision="signlist-2000-printing-2")
    assert rec["comparison_classification"] == cp.INDEPENDENTLY_SOURCED
    assert rec["eligible_for_independent_validation"] is True
    assert cp.earns_independent_support(rec) is True
    assert rec["phonetic_reading"]["value"] == "mīn"
    assert rec["phonetic_reading"]["source_revision"] == \
        "signlist-2000-printing-2"
    # Mutating the project reading cannot reclassify it or move the
    # stored value/revision: disagreement with an independent source
    # is a finding, not a provenance change.
    rec2 = cp.classify_entry("M999", entry, {"reading": "something else"},
                             source_revision="signlist-2000-printing-2")
    assert rec2["comparison_classification"] == cp.INDEPENDENTLY_SOURCED
    assert rec2["phonetic_reading"]["value"] == "mīn"
    assert rec2["phonetic_reading"]["source_revision"] == \
        "signlist-2000-printing-2"
    assert rec2["identity"]["raw_identical"] is False


# ── The remaining classes ────────────────────────────────────────────

def test_used_during_candidate_construction_earns_no_support():
    entry = {
        "mahadevan_id": "M175", "parpola_id": "175",
        "source": "mahadevan_parpola_crosswalk.json Phase-28",
        "iconic": "spinner's spindle", "phoneme": "katir",
        "confidence": "HIGH",
    }
    rec = cp.classify_entry("M175", entry, {"reading": "katir"},
                            used_in_candidate_construction=True)
    assert rec["comparison_classification"] == \
        cp.USED_DURING_CANDIDATE_CONSTRUCTION
    assert cp.earns_independent_support(rec) is False


def test_unlocated_external_attribution_is_unverified_at_best():
    # WS2-style entry: admitted on in-repo tables only.
    entry = {
        "parpola_id": "P222", "parpola_num": 222, "reading": "min",
        "confidence": "CANDIDATE",
        "source": "spec 004 WS2 expansion (2026-10-05)",
        "iconographic_match": False,
        "evidence": "phase71 EXTENDED_MAP: 'hook sign', source stated "
                    "as Parpola 1994 App. B. Single in-repo source.",
    }
    rec = cp.classify_entry("M222", entry, {"reading": "min"})
    assert rec["identity"]["raw_identical"] is True
    assert rec["comparison_classification"] == cp.UNVERIFIED
    assert cp.earns_independent_support(rec) is False


def test_partial_locator_does_not_make_a_source_independent():
    entry = _independent_entry()
    entry["primary_source_locator"] = {"work": "Example 2000"}
    entry.pop("value_origin")
    rec = cp.classify_entry("M999", entry, {"reading": "mīn"})
    assert rec["phonetic_reading"]["locator_present"] is False
    assert rec["comparison_classification"] == cp.UNVERIFIED


def test_ineligible_when_nothing_to_compare():
    no_value = {"mahadevan_id": "M086", "parpola_id": "P086",
                "parpola_num": 86, "source": "Parpola 1994 Appendix B",
                "confidence": "MEDIUM", "reading": "",
                "anchor_confidence": "UNREAD"}
    rec = cp.classify_entry("M086", no_value, {"reading": "oru"})
    assert rec["comparison_classification"] == cp.INELIGIBLE
    valued = _phase96_style_entry(reading="oru")
    rec2 = cp.classify_entry("M086", valued, None)
    assert rec2["comparison_classification"] == cp.INELIGIBLE
    assert cp.earns_independent_support(rec2) is False


def test_confidence_label_alone_never_earns_support():
    # An entry labeled HIGH merely because its sign pre-existed in the
    # old crosswalk carries no provenance: still a copy.
    entry = _phase96_style_entry(reading="tōḷ")
    entry["confidence"] = "HIGH"
    rec = cp.classify_entry("M001", entry, {"reading": "tōḷ"})
    assert rec["comparison_classification"] == cp.PROJECT_DERIVED
    assert cp.earns_independent_support(rec) is False


# ── Real-data smoke test ─────────────────────────────────────────────

def test_real_overlay_every_entry_classified_and_counts_agree():
    overlay = json.loads(OVERLAY_PATH.read_text(encoding="utf-8"))
    entries = overlay["entries"]
    assert len(entries) == 184
    for rec in entries:
        assert rec["comparison_classification"] in cp.CLASSIFICATIONS
        assert rec["eligible_for_independent_validation"] == (
            rec["comparison_classification"] == cp.INDEPENDENTLY_SOURCED)
        for block in ("sign_mapping", "depiction", "phonetic_reading",
                      "semantic_reading"):
            assert block in rec
            assert "source_as_stated" in rec[block]
            assert "locator_present" in rec[block]
            assert "value_origin" in rec[block]
    # The eligible count recomputed from the entries equals the
    # overlay's own stated count — whatever it is, including 0.
    recounted = sum(1 for r in entries
                    if r["eligible_for_independent_validation"])
    stated = overlay["summary"][
        "n_eligible_for_independent_validation"]
    assert recounted == stated
    for name, block in overlay["named_sets"].items():
        sub = [r for r in entries if r["sign"] in set(block["signs"])]
        assert len(sub) == block["n_entries"]
        assert sum(1 for r in sub
                   if r["eligible_for_independent_validation"]) == \
            block["n_eligible_for_independent_validation"]
