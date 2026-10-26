"""Crosswalk provenance classifier (Glossa Lab repair WP4, 2026-10-26).

Why this module exists
----------------------
The Phase-96 crosswalk builder (``phase96_cisi_crosswalk.py``) built
most entries of ``mahadevan_parpola_crosswalk_v2.json`` by copying the
``reading`` field out of the project's own anchor table
(``anchors.get(m_id).reading``) while labeling the entry's source as
"Parpola 1994 Appendix B". Appendix B is a sign-correspondence table:
it supplies the Mahadevan <-> Parpola sign-number mapping, not
readings. The provenance audit's ``parpola_agreement`` then compared
each anchor reading against that copied value and reported the match
rate as if it were agreement with an outside scholar. Agreement
between a value and its own copy is not evidence. This module makes
that defect impossible to repeat silently: it separates the four
provenances a crosswalk entry mixes together, and it classifies every
anchor-vs-crosswalk comparison by where the crosswalk value actually
came from. Classification is derived from provenance fields only —
never from whether the two readings agree.

The four provenances (kept separate for every entry)
----------------------------------------------------
1. ``sign_mapping`` — which Mahadevan sign number corresponds to which
   Parpola sign number. A sign-correspondence table (for example
   Parpola 1994 Appendix B) is a legitimate stated source for this.
2. ``depiction`` — what the sign pictures (the entry's ``iconic``
   field, where recorded).
3. ``phonetic_reading`` — the sound value attributed to the sign (the
   entry's ``reading`` field, or its ``phoneme`` field in the older
   Phase-28 entry shape).
4. ``semantic_reading`` — the meaning attributed to the sign. No
   crosswalk entry records this separately; it is reported as not
   recorded rather than silently borrowed from the phonetic string.

Each provenance block reports: the source exactly as stated in the
data, whether an exact primary-source locator is present, and the
value's origin.

Exact primary-source locator
----------------------------
An externally attributed reading counts as located only when the entry
itself carries a locator with all three parts: the work, a page /
table / figure inside that work, and the sign scheme the locator
addresses. A bare author-year label ("Parpola 1994"), a file name, or
a pointer to another in-repo table is not a locator.

Comparison classifications (exactly one per entry)
--------------------------------------------------
Applied in this order; the first rule that matches decides:

1. ``ineligible`` — there is no comparison to classify: the crosswalk
   entry carries no phonetic value, or there is no anchor entry, or
   the anchor carries no reading.
2. ``project_derived`` — the crosswalk value was copied from the
   project's own anchor table. Detected from the builder's
   fingerprint: the entry carries an ``anchor_confidence`` field
   (a field only the Phase-96 builder writes, copied from the anchor
   entry it was reading) under the stated source "Parpola 1994
   Appendix B", or the entry explicitly declares
   ``value_origin: project_anchor_table_copy``. This rule fires
   whether or not the copied value still matches the anchor: a stale
   copy is still a copy.
3. ``used_during_candidate_construction`` — the comparator value comes
   from the same crosswalk / literature line that was used to build
   the anchor candidate in the first place (for the real data: the
   anchor's value was imported via the Phase-51 crosswalk, per the
   anchor's own source field or the Phase-108 provenance register).
   Testing a candidate against one of its own construction inputs is
   a consistency check, not validation.
4. ``independently_sourced`` — the crosswalk value is attributed to
   an external source AND carries an exact primary-source locator
   (above) AND was neither copied from the project nor used during
   candidate construction.
5. ``unverified`` — everything else: an externally attributed value
   with no exact primary-source locator (including values taken from
   secondary in-repo tables). Unverified is a ceiling, not a floor:
   such a value may be accurate, but the record does not show it.

Eligibility
-----------
``eligible_for_independent_validation`` is true only for
``independently_sourced``. Only eligible comparisons may contribute
to independent validation. Agreement alone never earns support:
source agreement does not prove a decipherment, and a comparison
classified any other way earns no support at all.

Acceptance properties (exercised by the WP4 tests)
--------------------------------------------------
(i) A synthetic cycle — primary source -> project anchor -> copied
    comparator -> comparison against the original source's value —
    earns no support: the copy fingerprint classifies it
    ``project_derived`` even when the values are byte-identical.
(ii) Mutating the project (anchor) reading does not alter the stored
    comparator value or the classification: classification reads
    provenance fields only, so the class is stable under anchor
    mutation; only the reported identity flags change.
(iii) An independently coded source value stays fixed with its source
    revision: for an ``independently_sourced`` entry the record
    carries the comparator value and its ``source_revision``
    byte-for-byte as supplied, and anchor mutation cannot reclassify
    it.

Standard library only. No file in the historical record is read or
written by this module; callers pass parsed data in and get plain
dicts out.
"""
from __future__ import annotations

import re
import unicodedata

# ── Classification labels (the complete set) ─────────────────────────

INDEPENDENTLY_SOURCED = "independently_sourced"
USED_DURING_CANDIDATE_CONSTRUCTION = "used_during_candidate_construction"
PROJECT_DERIVED = "project_derived"
UNVERIFIED = "unverified"
INELIGIBLE = "ineligible"

CLASSIFICATIONS = (
    INDEPENDENTLY_SOURCED,
    USED_DURING_CANDIDATE_CONSTRUCTION,
    PROJECT_DERIVED,
    UNVERIFIED,
    INELIGIBLE,
)

# Value origins for the phonetic-reading provenance.
ORIGIN_PROJECT_COPY = "project_anchor_table_copy"
ORIGIN_INDEPENDENT = "independent_primary_source"
ORIGIN_IN_REPO_SECONDARY = "in_repo_secondary_table"
ORIGIN_EXTERNAL_UNLOCATED = "external_attribution_unlocated"
ORIGIN_NOT_RECORDED = "not_recorded"

# The stated source the Phase-96 builder wrote on every entry it built.
_PHASE96_SOURCE = "Parpola 1994 Appendix B"


# ── Normalisation (same rule as the audit it replaces) ───────────────

def _strip_diacritics(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def normalize_reading(reading: str) -> str:
    """The audit's own match normalisation (Phase-108 / spec 006
    Step 3c): lowercase, strip diacritics, first segment before '/',
    strip parenthetical glosses, keep letters only. Used here only to
    REPORT identity under the audit's rule; classification never
    depends on it."""
    s = (reading or "").split("/")[0].strip()
    s = re.sub(r"\([^)]*\)", " ", s)
    s = _strip_diacritics(s.lower())
    s = re.sub(r"[^a-z]", "", s)
    return s


# ── Entry inspection helpers ─────────────────────────────────────────

def comparator_value(entry: dict) -> tuple[str | None, str | None]:
    """The entry's phonetic comparator value and the field it came
    from: ``reading`` in the current entry shape, ``phoneme`` in the
    Phase-28 shape. Empty strings count as absent (the Phase-96
    builder wrote "" where the anchor table had no reading)."""
    for field in ("reading", "phoneme"):
        v = entry.get(field)
        if isinstance(v, str) and v.strip():
            return v, field
    return None, None


def primary_source_locator(entry: dict) -> dict | None:
    """The entry's exact primary-source locator, or None. A locator is
    exact only with all three parts present and non-empty: ``work``,
    one of ``page`` / ``table`` / ``figure``, and ``sign_scheme``."""
    loc = entry.get("primary_source_locator")
    if not isinstance(loc, dict):
        return None
    work = str(loc.get("work") or "").strip()
    pinpoint = next((str(loc.get(k) or "").strip()
                     for k in ("page", "table", "figure")
                     if str(loc.get(k) or "").strip()), "")
    scheme = str(loc.get("sign_scheme") or "").strip()
    if work and pinpoint and scheme:
        return {"work": work, "pinpoint": pinpoint, "sign_scheme": scheme}
    return None


def _builder_copy_fingerprint(entry: dict) -> bool:
    """True when the entry bears the Phase-96 builder's fingerprint:
    an ``anchor_confidence`` field (copied by the builder from the
    anchor entry it took the reading from) under the builder's stated
    source. No transcription of an external table produces the
    project's own anchor-confidence value."""
    return ("anchor_confidence" in entry
            and entry.get("source") == _PHASE96_SOURCE)


def reading_value_origin(entry: dict) -> str:
    """Where the entry's phonetic value came from, from provenance
    fields only (never from agreement with any anchor)."""
    value, _field = comparator_value(entry)
    if value is None:
        return ORIGIN_NOT_RECORDED
    declared = entry.get("value_origin")
    if isinstance(declared, str) and declared.strip():
        return declared.strip()
    if _builder_copy_fingerprint(entry):
        return ORIGIN_PROJECT_COPY
    if primary_source_locator(entry) is not None:
        return ORIGIN_INDEPENDENT
    source = str(entry.get("source") or "")
    if source.startswith("spec 004 WS2") or "evidence" in entry:
        # Admitted on the strength of other in-repo tables (the
        # entry's own "evidence" field cites in-repo files).
        return ORIGIN_IN_REPO_SECONDARY
    return ORIGIN_EXTERNAL_UNLOCATED


def _mapping_origin(entry: dict) -> str:
    if _builder_copy_fingerprint(entry) or entry.get("source") == _PHASE96_SOURCE:
        return "phase96_builder_table_as_stated"
    source = str(entry.get("source") or "")
    if source.startswith("spec 004 WS2"):
        return ORIGIN_IN_REPO_SECONDARY
    if "Phase-28" in source:
        return "phase28_curated_in_repo_file"
    return ORIGIN_EXTERNAL_UNLOCATED


def _numeric_identity(entry: dict, sign: str) -> bool | None:
    """True when the Parpola number equals the Mahadevan number (the
    builder's assumed identity mapping). Reported as a fact about the
    pair; the classification does not depend on it."""
    p_num = entry.get("parpola_num")
    m = re.fullmatch(r"M(\d+)", sign or "")
    if isinstance(p_num, int) and m:
        return p_num == int(m.group(1))
    p_id = str(entry.get("parpola_id") or "")
    pm = re.fullmatch(r"P?(\d+)", p_id)
    if pm and m:
        return int(pm.group(1)) == int(m.group(1))
    return None


# ── Classification ───────────────────────────────────────────────────

def classify_comparison(entry: dict, anchor_reading: str | None,
                          *, used_in_candidate_construction: bool = False
                          ) -> tuple[str, list[str]]:
    """Classify the comparison between one crosswalk entry and the
    project anchor's reading. Returns (classification, reasons).
    Rules and precedence are stated in the module docstring. The
    anchor reading's CONTENT is used only for the eligibility gate
    (rule 1: a reading must exist); agreement or disagreement never
    changes the class."""
    reasons: list[str] = []
    value, field = comparator_value(entry)
    if value is None:
        return INELIGIBLE, ["crosswalk entry carries no phonetic value "
                            "(no non-empty 'reading' or 'phoneme' field)"]
    if anchor_reading is None or not str(anchor_reading).strip():
        return INELIGIBLE, ["no anchor reading to compare against "
                            "(sign absent from the anchor table or its "
                            "reading is empty)"]
    origin = reading_value_origin(entry)
    if origin == ORIGIN_PROJECT_COPY:
        return PROJECT_DERIVED, [
            f"crosswalk '{field}' value was copied from the project's "
            "own anchor table by the Phase-96 builder (builder "
            "fingerprint: 'anchor_confidence' field under stated "
            "source 'Parpola 1994 Appendix B', a sign-correspondence "
            "table that does not supply readings)"]
    if used_in_candidate_construction:
        return USED_DURING_CANDIDATE_CONSTRUCTION, [
            "the anchor value was itself imported through the "
            "crosswalk / literature line this comparator belongs to "
            "(Phase-51 crosswalk import), so the comparison tests a "
            "candidate against one of its own construction inputs"]
    if primary_source_locator(entry) is not None:
        return INDEPENDENTLY_SOURCED, [
            "externally attributed value with an exact primary-source "
            "locator (work + page/table/figure + sign scheme), not "
            "copied from the project and not a construction input"]
    reasons.append(
        "externally attributed value with no exact primary-source "
        "locator at entry level (no work + page/table + sign scheme); "
        "unverified is the highest class available")
    if origin == ORIGIN_IN_REPO_SECONDARY:
        reasons.append("value rests on secondary in-repo tables cited "
                       "in the entry's 'evidence' field, not on a "
                       "primary source")
    return UNVERIFIED, reasons


def classify_entry(sign: str, entry: dict, anchor: dict | None,
                   *, used_in_candidate_construction: bool = False,
                   source_revision: str | None = None) -> dict:
    """Build the full provenance record for one crosswalk entry.

    ``anchor`` is the project anchor entry for the sign (or None).
    ``used_in_candidate_construction`` is a provenance fact the caller
    establishes from the anchor's own records (see module docstring,
    rule 3); it is never inferred from agreement.
    ``source_revision`` identifies the revision of the file the
    comparator value was coded from, and is carried through unchanged.
    """
    value, field = comparator_value(entry)
    anchor_reading = (anchor or {}).get("reading") if anchor else None
    classification, reasons = classify_comparison(
        entry, anchor_reading,
        used_in_candidate_construction=used_in_candidate_construction)
    locator = primary_source_locator(entry)
    stated_source = entry.get("source")

    raw_identical = None
    normalized_identical = None
    if value is not None and anchor_reading:
        raw_identical = (value == anchor_reading)
        normalized_identical = (
            normalize_reading(value) == normalize_reading(anchor_reading))

    return {
        "sign": sign,
        "mahadevan_id": entry.get("mahadevan_id") or sign,
        "parpola_id": entry.get("parpola_id"),
        "sign_mapping": {
            "source_as_stated": stated_source,
            # The stated source names a work and its sign list /
            # appendix for the Phase-96 entries; that is a locator
            # for the MAPPING (the thing such a table supplies).
            "locator_present": bool(
                entry.get("source") == _PHASE96_SOURCE
                or locator is not None),
            "value_origin": _mapping_origin(entry),
            "numeric_identity": _numeric_identity(entry, sign),
            "crosswalk_confidence_as_stated": entry.get("confidence"),
        },
        "depiction": {
            "value": entry.get("iconic"),
            "source_as_stated": stated_source,
            "locator_present": locator is not None,
            "value_origin": ("recorded_in_entry" if entry.get("iconic")
                             else ORIGIN_NOT_RECORDED),
        },
        "phonetic_reading": {
            "value": value,
            "field": field,
            "source_as_stated": stated_source,
            "locator_present": locator is not None,
            "locator": locator,
            "value_origin": reading_value_origin(entry),
            "source_revision": source_revision,
        },
        "semantic_reading": {
            "value": None,
            "source_as_stated": stated_source,
            "locator_present": False,
            "value_origin": "not_recorded_separately",
            "note": "no crosswalk entry records a semantic reading "
                    "separately from the phonetic string",
        },
        "anchor_reading_as_recorded": anchor_reading,
        "identity": {
            "raw_identical": raw_identical,
            "normalized_identical": normalized_identical,
            "normalization": "audit rule (spec 006 Step 3c): "
                             "lowercase, NFD-strip diacritics, first "
                             "segment before '/', strip parenthetical "
                             "glosses, letters only",
        },
        "comparison_classification": classification,
        "eligible_for_independent_validation":
            classification == INDEPENDENTLY_SOURCED,
        "classification_reasons": reasons,
    }


def earns_independent_support(record: dict) -> bool:
    """The only route by which a comparison may support a claim:
    the record is eligible (independently sourced). Identity —
    raw or normalised — is not support."""
    return bool(record.get("eligible_for_independent_validation"))


# ── Overlay construction ─────────────────────────────────────────────

def build_overlay(crosswalk: dict, anchors: dict,
                  construction_signs: set[str] | frozenset = frozenset(),
                  *, source_revision: str | None = None,
                  named_sets: dict[str, set[str]] | None = None) -> dict:
    """Classify every entry of a parsed crosswalk file against a
    parsed anchor table. ``construction_signs`` are signs whose anchor
    value was imported through the crosswalk line (rule 3), as
    established by the caller from the anchor records. ``named_sets``
    optionally maps a set name to sign sets (for example the Phase-109
    strict set's compared signs) for per-set breakdowns."""
    entries = []
    for sign in sorted(crosswalk):
        entries.append(classify_entry(
            sign, crosswalk[sign], anchors.get(sign),
            used_in_candidate_construction=sign in construction_signs,
            source_revision=source_revision))

    def _breakdown(records: list[dict]) -> dict:
        counts = {c: 0 for c in CLASSIFICATIONS}
        for r in records:
            counts[r["comparison_classification"]] += 1
        return {
            "n_entries": len(records),
            "by_classification": counts,
            "n_eligible_for_independent_validation":
                sum(1 for r in records if earns_independent_support(r)),
        }

    overlay = {
        "generated_by": "glossa_lab/crosswalk_provenance.py "
                        "(repair WP4, 2026-10-26)",
        "method": "comparison classification from provenance fields "
                  "only; agreement never changes a class; see module "
                  "docstring for the rules",
        "source_revision": source_revision,
        "summary": _breakdown(entries),
        "named_sets": {},
        "entries": entries,
    }
    for name, signs in (named_sets or {}).items():
        subset = [r for r in entries if r["sign"] in signs]
        overlay["named_sets"][name] = {
            "signs": sorted(signs),
            **_breakdown(subset),
        }
    return overlay
