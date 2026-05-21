# EXPERT_SUMMARY_PACKAGE
**Version**: 1.0 (DRAFT — For controlled disclosure only)  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / BitConcepts LLC  
**Confidentiality**: CONTROLLED — Share only per Section 10 protocol

---

## Instructions for Use

This package is for controlled disclosure to domain experts (specifically Dr. Andreas Fuls) per Section 10 of the Operating Instructions. Before sending, confirm:
- Signal level is appropriate for disclosure (MODERATE or higher)
- Disclosure is logged in DISCLOSURE_LOG.md
- Recipient has received no IP or co-authorship rights

---

## Executive Summary

We have developed a computational methodology — Corpus-Grounded Structural Analysis (CGSA) — that identifies a reproducible positional grammar in the Indus script corpus, stable across all 52 known Indus Valley Civilization archaeological sites.

**Core finding**: The Indus corpus (2,722 inscriptions, 52 sites) exhibits a three-slot positional grammar: an INITIAL class (candidate determinative/title markers), a MEDIAL class (candidate root/stem signs), and a TERMINAL class (candidate case suffix markers). This structure:
- Is reproducible deterministically from raw corpus data
- Shows 85.3% cross-site stability across all 52 known sites
- Is inconsistent with purely heraldic or purely administrative non-linguistic generators (per Nair 2026 scorecard: 4/4 metrics)
- Is independently confirmed by two INITIAL signs (P086, P001) from the holdatllc dataset (different methodology, different researcher)

**Linguistic hypothesis** (not confirmed): The positional structure matches Dravidian morphological organization (classifier-root-case) more closely than Sanskrit or Pali controls, based on substitution analysis phonotactic experiments.

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Inscriptions analyzed | 2,722 |
| Sites covered | 52 |
| Structural clusters | 40 |
| Cross-site stability | 85.3% full / 95.1% partial |
| Entropy reduction | 21.6% (2.31 bits) |
| Nair scorecard | 4/4 linguistic-consistent |
| Formulaic template coverage | 86.0% |

---

## Specific Questions for Expert Review

1. Does the 3-slot INITIAL-MEDIAL-TERMINAL positional grammar correspond to any known structural analysis in the ICIT database?
2. Our crosswalk shows P122 (ICIT SHN function) is a pure MEDIAL sign. Does ICIT analysis confirm this?
3. The M342 (jar sign, Mahadevan) is the most frequent TERMINAL sign in holdatllc (584 occurrences). What is its P-number equivalent in the ICIT system?
4. Are there Harappa tablet inscription sequences in ICIT that differ structurally from Mohenjo-daro seals?
5. Would you be willing to supply a controlled sample from ICIT (e.g., 200 Harappa inscriptions) for independent cross-validation?

---

## Methodology Notes

- All results are derived from published, open-license datasets
- No LLM was used for corpus analysis; CGSA is deterministic clustering and positional statistics
- SA (substitution analysis) experiments use Ollama local LLM (model: mistral-nemo:12b) and are hypothesis-generating only
- All pipeline code is version-controlled (git) with SHA256-hashed artifacts

---

## What We Are NOT Claiming

- We are NOT claiming a confirmed decipherment
- We are NOT claiming confirmed phoneme assignments
- We are NOT claiming Dravidian identification (structural hypothesis only)
- Results are preliminary and require expert validation and expanded corpus

---

## Contact

Tristen Pierson  
BitConcepts LLC  
[Contact via Dr. Fuls' initial communication channel]
