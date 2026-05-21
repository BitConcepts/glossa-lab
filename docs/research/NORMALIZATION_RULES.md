# NORMALIZATION_RULES
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / BitConcepts LLC  
**Confidentiality**: INTERNAL

---

## 1. Purpose

This document records all normalization decisions applied to the Indus corpus. A normalization rule change must be logged in MASTER_LEDGER.md with entry_type `normalization_rule_change`. Rules listed here are PERMANENT for the current corpus version.

---

## 2. General Principles

- **Non-destructive**: normalization never permanently alters the source sign IDs.
- **Marker preservation**: damage markers, variant markers, and uncertainty markers are retained.
- **No sign collapsing**: signs with different IDs are never merged unless a CROSSWALK ENTRY explicitly maps them and is itself documented.
- **Reversibility**: every normalization step can be reversed by re-running from the raw data files.

---

## 3. CISI / mayig Corpus Normalization Rules

| Rule ID | Rule | Rationale |
|---------|------|-----------|
| N-CISI-01 | Strip leading/trailing whitespace from sign sequences | Ingestion artifact |
| N-CISI-02 | Split multi-sign tokens on whitespace only | Signs are whitespace-delimited in mayig JSON |
| N-CISI-03 | Retain `?` suffix on uncertain readings | Uncertainty preserved per decipherment protocol |
| N-CISI-04 | Retain `~` damaged-sign marker | Damage preserved per decipherment protocol |
| N-CISI-05 | Map `P000` (damage/gap placeholder) to literal token `P000`; do not drop | P000 is a valid structural token representing a lost sign |
| N-CISI-06 | Preserve inscription side labels (A/B) | Required for duplicate-object reconciliation |

---

## 4. Yajnadevam Corpus Normalization Rules

| Rule ID | Rule | Rationale |
|---------|------|-----------|
| N-YD-01 | Parse SQL dump tables: Sites, Seals, Inscriptions, GlyphSequences | SQL→JSON extraction |
| N-YD-02 | Assign Y-numbers in format `Y` + zero-padded 4-digit ID | Consistent with Yajnadevam internal glyph IDs |
| N-YD-03 | Retain glyph sequence order exactly as stored in SQL | No reordering |
| N-YD-04 | Sites with null coordinates retained; site ID preserved | Provenance requires site linkage |
| N-YD-05 | Deduplicate within-site seals by unique seal ID | Prevents double-counting |

---

## 5. Crosswalk Normalization Rules

| Rule ID | Rule | Rationale |
|---------|------|-----------|
| N-CW-01 | Y→P crosswalk built from length-matched inscription pairs only | Length mismatch ≥ 20% excluded from primary crosswalk |
| N-CW-02 | Anchor-guided extension used for non-length-matched pairs | Must be flagged with confidence=extended in crosswalk CSV |
| N-CW-03 | Token mapping threshold: accept Y→P pair only if support ≥ 3 inscription pairs | Prevents noise from unique pairings |
| N-CW-04 | P122↔M342 mapping REMOVED (erroneous crosswalk) | P122=medial numeral stroke; M342=jar sign (TERMINAL); different signs |
| N-CW-05 | Signs without confirmed crosswalk retain original ID | Never substitute unconfirmed equivalents |

---

## 6. Structural Analysis Normalization

| Rule ID | Rule | Rationale |
|---------|------|-----------|
| N-SA-01 | Positional rates (start_rate, internal_rate, end_rate) computed on per-token basis, not per-inscription | Longer inscriptions would otherwise inflate terminal/initial counts |
| N-SA-02 | Global classification uses threshold: INITIAL if start_rate ≥ 0.55; TERMINAL if end_rate ≥ 0.55; MEDIAL if internal_rate ≥ 0.70; else MIXED | Thresholds based on Fuls (2014) positional analysis prior |
| N-SA-03 | INSUFFICIENT_DATA assigned if global_freq < 10 | Below-threshold signs cannot be reliably classified |
| N-SA-04 | Cross-site stability: local agreement criterion is TERMINAL→site end_rate ≥ 0.40; INITIAL→site start_rate ≥ 0.40; MEDIAL→site internal_rate ≥ 0.50 | Allows for reasonable site-level variation |

---

## 7. Things We Explicitly Did NOT Do

- Did not phonetically assign any sign IDs.
- Did not merge allographs or variant signs without explicit crosswalk evidence.
- Did not remove hapax signs from the corpus.
- Did not weight inscriptions by artifact type.
- Did not apply any language-model smoothing to n-gram counts.
