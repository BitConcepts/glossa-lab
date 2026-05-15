# Corpus Batch 2 Retry Report

**Date:** 2026-05-15  
**Result:** 3/6 OK, 484,645 files

## Results

| Source | Status | Files |
|---|---|---|
| GRETIL/DCS Sanskrit | OK | 24,312 |
| ORACC/CDLI/ETCSL | PARTIAL | 0 |
| SuttaCentral | OK | 156,882 |
| CBETA Chinese Buddhist | FAIL | 0 |
| Papyri.info | FAIL | 303,405 |
| CDLI GitHub | OK | 46 |

## Changes from Batch 1
- GRETIL: switched to shreevatsa/sanskrit mirror + DCS (OliverHellwig/sanskrit)
- ORACC: using CDLI direct downloads + ETCSL GitHub instead of ORACC API
- SuttaCentral: timeout increased to 600s + bilara-data fallback
- CBETA: using GitHub directly (no SSL API needed)
- NEW: Papyri.info Greek papyri (idp.data repo)
- NEW: CDLI GitHub (cdli-gh/data transliterations)
