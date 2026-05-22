# REPRODUCIBILITY_PROTOCOL
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / BitConcepts LLC  
**Confidentiality**: INTERNAL

---

## 1. Purpose

This document describes how to reproduce all Glossa-Lab Indus decipherment results from scratch on a clean machine. It is a required component per Section 9 of the Operating Instructions.

---

## 2. System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Windows 10/11 or Linux (tested on Windows 11) |
| Python | 3.11+ |
| Node.js | 18+ (for frontend) |
| Disk space | ≥ 2 GB (corpus + analysis outputs) |
| Key Python packages | numpy, scipy, scikit-learn, networkx, pandas |

Install via: `pip install -r backend/requirements.txt`  
Frontend: `npm install` in `frontend/`

---

## 3. Data Acquisition

All raw data must be acquired from their primary sources:

| Dataset | Source | Command/URL |
|---------|--------|-------------|
| CISI / mayig | GitHub: NottsDigitalHumanities/mayig | `git clone https://github.com/NottsDigitalHumanities/mayig` |
| Yajnadevam SQL | Yajnadevam project | See data_raw/other_sites/ (SQL dump retained) |
| holdatllc | GitHub: holdatllc/indus-corpus | See scripts/ingest_holdatllc.py |
| mayig sign features | mayig GitHub (features/*.json) | Fetched by scripts/cgsa_pipeline.py |

The data files in `data_raw/` are retained in the repository. If reproducing from external sources, re-run the ingestion scripts in order.

---

## 4. Reproduction Steps (In Order)

### Step 1: CISI corpus ingestion
```
python scripts/build_corpus_pipeline.py
```
**Expected output**: `data_normalized/corpus_master.csv` (179 CISI inscriptions)

### Step 2: Yajnadevam ingestion
```
python scripts/parse_yajnadevam_sql.py
```
**Expected output**: `data_raw/other_sites/yajnadevam_inscriptions.json` (2,543 inscriptions)

### Step 3: Combined corpus structural analysis
```
python scripts/structural_analysis.py
```
**Expected outputs**: `analysis/structural_stats.json`, `analysis/structural_matrices.json`, `analysis/sign_cooccurrence_graph.json`

### Step 4: Y→P crosswalk
```
python scripts/build_yajnadevam_crosswalk.py
python scripts/extend_yp_crosswalk.py
python scripts/apply_yp_crosswalk.py
```
**Expected output**: `crosswalks/yajnadevam_to_parpola_crosswalk_extended.csv` (82.8% token coverage)

### Step 5: Cross-site structural analysis
```
python scripts/cross_site_analysis.py
python scripts/global_class_stability.py
```
**Expected outputs**: `analysis/cross_site_stats.json`, `analysis/global_class_stability.json`, `reports/global_class_stability_report.md`

### Step 6: CGSA pipeline (Phases 1–6)
```
python scripts/cgsa_pipeline.py
```
**Expected outputs**: `crosswalks/canonical_sign_registry.csv`, `analysis/sign_clusters.json`, `reports/cluster_characterization.md`, `reports/cgsa_validation_report.md`

### Step 7: Nair (2026) scorecard
```
python scripts/nair2026_scorecard.py
```
**Expected output**: `reports/nair2026_scorecard_comparison.md`

### Step 8: holdatllc ingestion and cross-validation
```
python scripts/ingest_holdatllc.py
```
**Expected outputs**: `analysis/holdatllc_sign_roles.json`, `reports/consolidated_structural_grammar.md`

### Step 9: Phase 9 hypothesis seeding (database)
```
python scripts/seed_phase9_hypotheses.py
```
**Seeds 6 hypotheses and 1 research notebook into Glossa-Lab DB**

---

## 5. Determinism Notes

- CGSA clustering uses scikit-learn AgglomerativeClustering (deterministic; no random seed required)
- SA experiments use Ollama LLM inference — **not deterministic** across runs; document model version used
- All SHA256 artifact hashes computed after each pipeline stage (see MASTER_LEDGER.md)
- Git commit hash provides version lock for code state

---

## 6. Validation Checks

After reproduction, verify:

1. `data_normalized/corpus_master.csv` has exactly 2,722 rows (or 179 for CISI-only run)
2. `crosswalks/canonical_sign_registry.csv` has 803 unique signs
3. `analysis/sign_clusters.json` has 40 clusters
4. `reports/global_class_stability_report.md` reports ≥ 85% full stability
5. `reports/nair2026_scorecard_comparison.md` shows 4/4 metrics consistent
6. Run governance lint: `shell.cmd test` — must pass 4/4 checks

---

## 7. Known Non-Reproducibility Points

| Step | Issue | Mitigation |
|------|-------|------------|
| SA phonotactic experiments | LLM inference is stochastic | Pin model version; report mean_consistency ± std |
| holdatllc ingestion | Requires external GitHub repo | Local copy retained in data_raw/ |
| Yajnadevam SQL | GPL-3.0 source; subject to upstream changes | SQL dump archived locally |
| P385 phoneme test | Requires Ollama running locally | Document model: `mistral-nemo:12b` |
