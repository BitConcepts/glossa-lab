# CORPUS_DEFINITION
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / BitConcepts LLC  
**Confidentiality**: INTERNAL

---

## 1. Purpose

This document defines the exact corpus used in all Glossa-Lab Indus decipherment experiments. It is a primary provenance document and must be updated whenever corpus composition changes.

---

## 2. Corpus Components

### 2.1 CISI / mayig Corpus (Component A)

| Field | Value |
|-------|-------|
| Source name | CISI Vol. 1 — Mohenjo-daro (Parpola et al., 1987) |
| Digitization | mayig project (MIT License, GitHub: NottsDigitalHumanities/mayig) |
| Number of inscriptions | 179 |
| Site coverage | Mohenjo-daro only |
| Sign numbering system | Parpola P-numbers (P001–P390+) |
| Format | JSON (data_raw/cisi_vol1_india/indus_cisi_corpus.json) |
| Download date | 2026-04-22 |
| License | MIT (mayig digitization) |
| Artifact hash | See MASTER_LEDGER.md |

**Notes**: Inscriptions cover seals, sealings, tablets, and miniature objects from Mohenjo-daro. Variant and damage markers preserved; no normalization beyond whitespace. 179 unique inscription sides.

### 2.2 Yajnadevam Corpus (Component B)

| Field | Value |
|-------|-------|
| Source name | Yajnadevam Indus Corpus SQL dump |
| Digitization | Yajnadevam project (GPL-3.0) |
| Number of inscriptions | 2,543 |
| Site coverage | 52 sites including Harappa, Lothal, Dholavira, Kalibangan, Chanhu-daro, Surkotada |
| Sign numbering system | Y-numbers (Y0001–Y1000+, custom scheme) |
| Format | Parsed JSON (data_raw/other_sites/yajnadevam_inscriptions.json) |
| Download date | 2026-04-22 |
| License | GPL-3.0 |
| Artifact hash | See MASTER_LEDGER.md |

**Notes**: Multi-site coverage critical for cross-site stability validation. Y-numbers partially crosswalked to P-numbers (82.8% token mapping achieved via extended crosswalk). Site-level breakdown in analysis/cross_site_stats.json.

### 2.3 Combined Corpus (Active Analysis Dataset)

| Field | Value |
|-------|-------|
| Total inscriptions | 2,722 (179 CISI + 2,543 Yajnadevam) |
| Total tokens | ~12,300 (estimated from structural_stats.json) |
| Distinct signs (P-system) | 160 classified; 803 in full inventory |
| Distinct signs (Y-system) | ~600+ Y-numbers |
| Master file | data_normalized/corpus_master.csv |
| Sites represented | 52 (via Yajnadevam) + Mohenjo-daro (CISI) |

---

## 3. Excluded / Pending Corpora

| Corpus | Status | Reason |
|--------|--------|--------|
| CISI Vol. 2 (Harappa, Pakistan) | NOT ACQUIRED | Physical volume; no digital access |
| ICIT database (Wells/Fuls, ~6,800 inscriptions) | PENDING | Awaiting Dr. Fuls response to collaboration request |
| holdatllc corpus | VALIDATION ONLY | Used for cross-validation of sign roles, not in main analysis corpus |
| ASI digital archives | PENDING | See internet search results in SIGNAL_STATUS.md |

---

## 4. Corpus Integrity Rules

1. No sign collapsing — every sign ID is preserved as-is in all analysis files.
2. Damage markers (typically `?` or `~` in the source) are retained in the normalized form.
3. Duplicate object reconciliation: inscriptions from the same physical object (both sides) are tracked separately.
4. Any corpus addition requires a new MASTER_LEDGER.md entry with `entry_type: dataset_change`.
5. The corpus_master.csv is the single source of truth for all analysis. All scripts read from it.

---

## 5. Change History

| Date | Version | Change | Ledger ID |
|------|---------|--------|-----------|
| 2026-04-22 | 0.1 | Initial CISI ingestion (179 inscriptions) | H1-CORPUS-001 |
| 2026-04-22 | 0.2 | Yajnadevam ingestion (2,543 inscriptions, 52 sites) | H1-CORPUS-002 |
| 2026-04-22 | 0.3 | Y→P crosswalk applied (82.8% token mapping) | H1-CORPUS-003 |
| 2026-04-23 | 1.0 | This document created | H1-DOC-001 |
