# Phase-391 — Spec 027 Stage 0 Report (gazetteer + chronology spine)

Descriptive infrastructure only (Spec 027 §6, FR-027-4). This stage mints no movement, culture, language, or repertoire verdict.

## Coverage

- XRONOS export: 314030 rows total; 144 inside the frozen region filter (lat 22.0-37.5, lng 60.5-79.0).
- Gazetteer rows: 36 ({'CISI Vol. 1 catalogue (Phase-124 layer)': 11, 'CISI Vol. 2 catalogue (Phase-124 layer)': 4, 'XRONOS': 21}); program site clusters: 30, of which 5 are asserted by more than one source.
- Gazetteer licence states: {'open_access_read_only': 15, 'verified_open': 21}; coordinate states: {'unknown': 15, 'exact_published': 21}.
- CISI non-site catalogue rows excluded (empty site / section headers): 526.
- Chronology rows: 177 ({'XRONOS': 144, 'Mutin et al. 2025 SI Table S2': 33}); context grades: {'unassessed': 108, 'associated': 36, 'direct': 33}; material classes: {'long_lived': 105, 'unknown': 15, 'short_lived': 57}; CONTESTED-scenario rows: 33.

## Coverage bias (statements, not findings)

- CISI rows are inscribed-object findspots from museum collections (Vols 1-2): they cover only sites whose objects entered those collections, dominated by Mohenjo-Daro and Harappa. A site absent here is not absent from the Indus world.
- XRONOS rows cover only sites with published radiocarbon-dated contexts in the export; the filtered export contains no Mohenjo-Daro, Harappa, Mehrgarh, Rakhigarhi, Dholavira, Kalibangan, or Lothal dates. The chronology spine is therefore a dated-site skeleton, not an Indus chronology.
- Possehl, Law, and TwoRains site lists are catalogued, not built (source_register.json): the comprehensive settlement universe remains untranscribed, and every downstream design must treat gazetteer coverage as partial.

## Q6 timing-support assessment (frozen criteria, stage0-freeze.md §4)

- c1_regions_with_2plus_sites: value 1 vs threshold 3 — FAIL
- c2_window_sites_direct_or_associated: value 5 vs threshold 10 — FAIL
- c3_window_short_lived_share: value 0.0 vs threshold 0.5 — FAIL
- c4_window_median_std_bp: value 70 vs threshold 80 — PASS
- **Status: NOT-YET-TESTABLE** (window direct/associated rows: 31).

## Fitness for question (descriptive, Spec 027 §6.6)

- Q1 (mobility arm): unchanged blocker — the spine adds no site-period mobility data; NOT-YET-TESTABLE stands.
- Q2 (Stage 1 gate): the gazetteer supplies program site clusters for corpus sites; Stage 1 proceeds under its own freeze.
- Q3/Q4/Q5/Q8/Q9: unchanged blockers (spec §9); Stage 0 changes none of their data conditions. The Mutin et al. 2025 series is now traced in the spine as CONTESTED rows; Q5's replication blocker is unaffected.
- Q6: see the assessment above.
- Q7: Stage 0 supplies site identities and coordinates for the dated-site subset only; the D8 provenance/licence audit remains a separate precondition.

## Release package (Ask 4)

- `stage0-release/` holds derived CC BY 4.0 CSVs of verified_open rows only (gazetteer 21 rows; chronology 177 rows) plus the source register. CISI-derived rows (open_access_read_only) are excluded. The repo release gate was run against the package in this stage; **no external deposit was made**.

