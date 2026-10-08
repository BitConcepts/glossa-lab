"""Phase-126 — Wells-split descriptive analysis of the 113
CANDIDATE anchors: pure machinery.

Ledger-sequence Phase-126 (2026-10-08). DESCRIPTIVE ONLY.

Inputs (both read-only, both already on main):

  * ``backend/reports/INDUS_FINAL_ANCHORS.json`` — the anchor
    file. The analysis set is exactly the anchors whose
    ``confidence`` field is ``"CANDIDATE"`` (113 signs). The
    44 anchors carrying ``validation_status ==
    "pending_non_sa_validation"`` are a different set
    (verified disjoint) and are not analysed here.
  * ``data/crosswalks/wells_segmentation_witness_v1.json`` —
    the Phase-123 Wells segmentation witness table (157 rows;
    classification semantics per
    ``reports/phase123_wells_segmentation_witness.md``:
    SAME / SPLIT / MERGE / NOT-COVERED / INDETERMINATE).

For each CANDIDATE sign this module records its Wells
treatment, in this phase's vocabulary:

  * ``split``        — witness treatment SPLIT: Wells segments
                       what the program's signary treats as
                       one sign into multiple graphemes
                       (compound-suspect). The split components
                       (Wells grapheme numbers) are recorded
                       from the witness table's
                       ``wells_graphemes`` field.
  * ``merge``        — witness treatment MERGE: the sign's one
                       Wells grapheme is shared with other
                       Mahadevan signs.
  * ``unit-same``    — witness treatment SAME: Wells carries
                       exactly one grapheme for the sign,
                       unshared (unit-confirmed under Wells).
  * ``not-covered``  — witness treatment NOT-COVERED, or the
                       sign is absent from the witness table
                       (recorded, never silently dropped).
  * ``indeterminate``— witness treatment INDETERMINATE: the
                       witness states no determinable
                       treatment, with its reason recorded.

Cross-tabulations are computed against the evidence features
actually recorded in the anchors file for these 113 signs,
named by their exact field names: ``basis`` (from which the
attestation count ``freq=`` and the positional profile
``I=/T=/M=`` are parsed — every CANDIDATE ``basis`` string
carries both), ``source``, ``validation_status``,
``phase109_annotation`` (presence), ``phase110_annotation``
(presence), ``_phase132_note`` (presence), ``dedr`` /
``dedr_source`` / ``phase_upgraded`` / ``upgrade_basis``
(the Phase-252 cohort fields), and ``reading_direction``
(presence). No field is invented and no value is imputed:
a field absent from a sign's anchor entry is counted as
absent.

This module changes no anchor, asserts no implication for
any anchor's status, and phrases nothing as an adjudication:
its output is a design input — facts a future battery spec
may use, nothing more.
"""
from __future__ import annotations

import re
from collections import Counter

# ── Treatment vocabulary ──────────────────────────────────
# Phase-123 witness treatment -> Phase-126 label.
TREATMENT_MAP = {
    "SPLIT": "split",
    "MERGE": "merge",
    "SAME": "unit-same",
    "NOT-COVERED": "not-covered",
    "INDETERMINATE": "indeterminate",
}
TREATMENT_ORDER = ("split", "merge", "unit-same",
                   "not-covered", "indeterminate")

_FREQ_RE = re.compile(r"freq=(\d+)")
_PROFILE_RE = re.compile(
    r"I=(\d+\.\d+)\s+T=(\d+\.\d+)\s+M=(\d+\.\d+)")


def parse_basis(basis: str) -> dict:
    """Parse the attestation count and positional profile
    recorded in an anchor entry's ``basis`` string.

    Returns {"freq": int|None, "profile": (I, T, M)|None}.
    Values are read from the string, never imputed.
    """
    freq_match = _FREQ_RE.search(basis or "")
    profile_match = _PROFILE_RE.search(basis or "")
    profile = None
    if profile_match:
        profile = tuple(float(x) for x in profile_match.groups())
    return {
        "freq": int(freq_match.group(1)) if freq_match else None,
        "profile": profile,
    }


def candidate_signs(anchors_doc: dict) -> dict:
    """The anchors whose ``confidence`` field is CANDIDATE,
    as {sign: entry}, sorted by sign."""
    anchors = anchors_doc["anchors"]
    return {sign: anchors[sign] for sign in sorted(anchors)
            if anchors[sign].get("confidence") == "CANDIDATE"}


def pending_signs(anchors_doc: dict) -> set:
    """Signs carrying ``validation_status ==
    "pending_non_sa_validation"`` (the non-CANDIDATE set the
    Phase-123 witness also covered; not analysed here)."""
    return {sign for sign, entry in anchors_doc["anchors"].items()
            if entry.get("validation_status")
            == "pending_non_sa_validation"}


def _graphemes(raw: str) -> list[str]:
    if not raw:
        return []
    return [g.strip() for g in raw.split(";") if g.strip()]


def build_records(candidates: dict, witness_rows: list[dict]) -> list[dict]:
    """One record per CANDIDATE sign, sorted by sign.

    A CANDIDATE sign absent from the witness table is
    recorded with treatment ``not-covered`` and
    ``witness_present`` False — counted and listed, never
    silently dropped.
    """
    witness = {r["sign"]: r for r in witness_rows}
    records = []
    for sign, entry in candidates.items():
        row = witness.get(sign)
        parsed = parse_basis(entry.get("basis", ""))
        if row is None:
            treatment = "not-covered"
            raw_treatment = None
            graphemes: list[str] = []
            method = None
            thesis_source = None
            verification = None
            witness_note = ("Sign absent from the Phase-123 "
                            "witness table.")
            implication_note = None
        else:
            raw_treatment = row["treatment"]
            treatment = TREATMENT_MAP[raw_treatment]
            graphemes = _graphemes(row.get("wells_graphemes", ""))
            method = row.get("correspondence_method") or None
            thesis_source = row.get("thesis_source") or None
            verification = row.get("verification") or None
            witness_note = row.get("note") or None
            implication_note = row.get("implication_note") or None
        records.append({
            "sign": sign,
            "wells_treatment": treatment,
            "witness_treatment_raw": raw_treatment,
            "witness_present": row is not None,
            "wells_graphemes": graphemes,
            "n_wells_graphemes": len(graphemes),
            "correspondence_method": method,
            "thesis_source": thesis_source,
            "verification": verification,
            "witness_note": witness_note,
            "implication_note": implication_note,
            # Anchor evidence features, exact field names.
            "reading": entry.get("reading"),
            "confidence": entry.get("confidence"),
            "source": entry.get("source"),
            "validation_status": entry.get("validation_status"),
            "basis_freq": parsed["freq"],
            "basis_profile": (list(parsed["profile"])
                              if parsed["profile"] else None),
            "has_phase109_annotation":
                bool(entry.get("phase109_annotation")),
            "has_phase110_annotation":
                bool(entry.get("phase110_annotation")),
            "has_phase132_note": bool(entry.get("_phase132_note")),
            "has_dedr": bool(entry.get("dedr")),
            "dedr_source": entry.get("dedr_source"),
            "phase_upgraded": entry.get("phase_upgraded"),
            "has_upgrade_basis": bool(entry.get("upgrade_basis")),
            "has_reading_direction":
                bool(entry.get("reading_direction")),
        })
    return records


def cross_tab(records: list[dict], key_fn) -> dict:
    """{key: {treatment: count}} with keys sorted by their
    string form and every treatment present (zero-filled),
    in TREATMENT_ORDER."""
    table: dict[str, Counter] = {}
    for rec in records:
        key = str(key_fn(rec))
        table.setdefault(key, Counter())[rec["wells_treatment"]] += 1
    return {key: {t: table[key].get(t, 0) for t in TREATMENT_ORDER}
            for key in sorted(table)}


def build_cross_tabs(records: list[dict]) -> dict:
    """All cross-tabulations of Wells treatment against the
    anchor evidence features present for the 113 signs.
    Counts only."""
    return {
        "by_basis_freq": cross_tab(
            records, lambda r: r["basis_freq"]),
        "by_basis_profile": cross_tab(
            records,
            lambda r: (tuple(r["basis_profile"])
                       if r["basis_profile"] else None)),
        "by_source_field": cross_tab(
            records, lambda r: r["source"]),
        "by_validation_status_field": cross_tab(
            records, lambda r: r["validation_status"]),
        "by_phase132_note_presence": cross_tab(
            records, lambda r: r["has_phase132_note"]),
        "by_phase109_annotation_presence": cross_tab(
            records, lambda r: r["has_phase109_annotation"]),
        "by_phase252_cohort": cross_tab(
            records, lambda r: bool(r["phase_upgraded"])),
        "by_dedr_presence": cross_tab(
            records, lambda r: r["has_dedr"]),
        "by_reading_direction_presence": cross_tab(
            records, lambda r: r["has_reading_direction"]),
        "by_correspondence_method": cross_tab(
            records, lambda r: r["correspondence_method"]),
        "by_verification": cross_tab(
            records, lambda r: r["verification"]),
    }


def headline_counts(records: list[dict]) -> dict:
    counts = Counter(r["wells_treatment"] for r in records)
    return {t: counts.get(t, 0) for t in TREATMENT_ORDER}


def split_size_distribution(records: list[dict]) -> dict:
    sizes = Counter(r["n_wells_graphemes"] for r in records
                    if r["wells_treatment"] == "split")
    return {str(k): sizes[k] for k in sorted(sizes)}


def shared_split_components(records: list[dict]) -> dict:
    """Descriptive: Wells graphemes that appear in the split
    component sets of more than one CANDIDATE sign, as
    {grapheme: sorted [signs]}. Recorded because it states,
    in the witness's own terms, that the split sets of these
    signs are not disjoint."""
    by_grapheme: dict[str, list[str]] = {}
    for rec in records:
        if rec["wells_treatment"] != "split":
            continue
        for grapheme in rec["wells_graphemes"]:
            by_grapheme.setdefault(grapheme, []).append(rec["sign"])
    return {g: sorted(signs) for g, signs in sorted(by_grapheme.items())
            if len(signs) > 1}
