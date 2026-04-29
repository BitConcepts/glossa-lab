# SIGN_INVENTORY
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / Layer1Labs Silicon, Inc.  
**Confidentiality**: INTERNAL

---

## 1. Purpose

This document describes the canonical sign inventory used in Glossa-Lab Indus decipherment research. It summarizes the registry, sign systems, crosswalk status, and key observations about sign distribution.

---

## 2. Canonical Sign Registry

**Primary file**: `crosswalks/canonical_sign_registry.csv`  
**Created**: 2026-04-22 (CGSA Phase 3)  
**Total signs**: 803 (unique sign IDs with stable UUID assigned)  
**File size**: 112,387 bytes  
**Artifact hash**: See MASTER_LEDGER.md

### 2.1 Registry Fields

Each row in canonical_sign_registry.csv contains:
- `sign_uuid` — stable UUID assigned during CGSA Phase 3
- `p_number` — Parpola number (P001–P400+), if known
- `y_number` — Yajnadevam Y-number, if known
- `wells_number` — Wells concordance number, if known
- `mahadevan_number` — Mahadevan M-number, if known
- `global_freq` — frequency in combined corpus
- `global_class` — INITIAL / MEDIAL / TERMINAL / MIXED / INSUFFICIENT_DATA
- `cluster_id` — CGSA Phase 5 cluster assignment (0–39)
- `icit_function` — ICIT function code if present (ITM, LOG, SYL, TMK, NUM, SHN)
- `description` — Parpola sign description

---

## 3. Sign Inventory by Numbering System

| System | Signs in Registry | Source |
|--------|------------------|--------|
| Parpola P-numbers | 160 classified; ~390 known | CISI / Parpola (1994) |
| Yajnadevam Y-numbers | ~600+ | Yajnadevam project |
| Mahadevan M-numbers | 417 (Mahadevan 1977) | CISI Vol. 1 concordance |
| Wells numbers | Partial crosswalk | Wells (2011) |
| ICIT numbers | Partial (via mayig features) | Fuls ICIT database |

---

## 4. Sign Distribution in Combined Corpus

| Metric | Value |
|--------|-------|
| Total distinct sign IDs | 803 |
| Signs with global_freq ≥ 10 | 105 |
| Hapax signs (freq = 1) | 276 |
| Hapax rate | 35.7% |
| Most frequent sign | P324 (1,366 tokens) — Classic jar symbol |
| Second most frequent | P098/P217 cluster (583 tokens) — Vertical lines |
| Top terminal sign | P385 (349 tokens) — Diamond/leaf shape |

---

## 5. Structural Classifications (CGSA Phase 5)

Based on positional analysis (start_rate, internal_rate, end_rate) across 2,722 inscriptions:

| Class | Signs Classified | Description |
|-------|-----------------|-------------|
| INITIAL | 12 signs | start_rate ≥ 0.55; candidate determinatives/titles |
| MEDIAL | 46 signs | internal_rate ≥ 0.70; candidate roots/stems |
| TERMINAL | 14 signs | end_rate ≥ 0.55; candidate suffixes/case markers |
| MIXED | 33 signs | flexible position; candidate phonetic syllabics |
| INSUFFICIENT_DATA | 77 signs | freq < 10; cannot classify reliably |

---

## 6. High-Confidence Sign Assignments

Signs with multiple independent lines of evidence (CGSA cluster, holdatllc validation, SA anchor):

| Sign | Slot | Confidence | Evidence Sources |
|------|------|-----------|-----------------|
| P385 | TERMINAL | HIGH | SA (0.8591), CAS TERMINAL, holdatllc M380≈TERMINAL, ICIT ITM |
| P324 | INITIAL | HIGH | SA anchor, CAS INITIAL, start_rate=0.690, ICIT ITM |
| P122 | MEDIAL | MED | SA anchor, CAS MEDIAL, internal_rate=1.0, ICIT SHN |
| P086 | INITIAL | MED | SA anchor, CAS INITIAL, M077 holdatllc confirmed |
| P332 | MEDIAL | MED | SA anchor, follows P324 in 91% of occurrences |
| P378 | TERMINAL | MED | end_rate=0.753, ICIT ITM, cluster 39 |

---

## 7. Known Crosswalk Issues

| Issue | Signs Affected | Status |
|-------|---------------|--------|
| P122↔M342 wrong mapping | P122, M342 | CRITICAL — remove from sign_crosswalk_master.csv |
| M342 (jar sign, 584 occurrences) has no P-number | M342 | Pending visual comparison against Parpola plates |
| 77 signs with INSUFFICIENT_DATA | — | Corpus expansion required |
| Y-numbers without P-mapping | ~400 Y-numbers | Ongoing crosswalk extension |

---

## 8. Related Files

| File | Purpose |
|------|---------|
| `crosswalks/canonical_sign_registry.csv` | Master sign registry with UUIDs |
| `crosswalks/sign_crosswalk_master.csv` | Multi-system crosswalk (P, Y, M, Wells) |
| `crosswalks/sign_inventory.csv` | Full sign inventory with positional stats |
| `crosswalks/yajnadevam_to_parpola_crosswalk_extended.csv` | Y→P mapping |
| `analysis/sign_clusters.json` | CGSA Phase 5 cluster assignments |
| `reports/cluster_characterization.md` | Detailed cluster report |
