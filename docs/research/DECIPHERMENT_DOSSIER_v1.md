# DECIPHERMENT_DOSSIER_v1
**Version**: 1.0 (DRAFT — MODERATE signal; not yet at Section 8 Critical Signal trigger)  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / BitConcepts, LLC  
**Confidentiality**: STRICTLY INTERNAL — DO NOT DISTRIBUTE

---

## 1. Purpose

This dossier is the comprehensive internal record of the Glossa-Lab Indus decipherment research. It is prepared in advance of Critical Signal per Section 8.2 of the Operating Instructions, so it is ready when needed. The current version reflects MODERATE signal status.

**This document MUST NOT be shared externally without explicit authorization from Tristen Pierson.**

---

## 2. Research Summary

### 2.1 Core Finding (Structural)

The Indus corpus (2,722 inscriptions, 52 sites) exhibits a robust 3-slot positional grammar — INITIAL, MEDIAL, TERMINAL — that is:

1. Reproducible from raw corpus data deterministically
2. Stable across all 52 known IVC sites (85.3% full stability)
3. Confirmed by three independent data sources (CGSA, holdatllc, Fuls prior)
4. Inconsistent with all non-linguistic generator models tested

This finding constitutes MODERATE signal. It is scientifically defensible and publishable as a structural finding.

### 2.2 Linguistic Hypothesis (Candidate)

The structural grammar matches Dravidian morphological patterns more closely than Sanskrit, Pali, or random controls, based on SA phonotactic testing. Specifically:
- INITIAL sign class matches Dravidian classifier/determinative function
- MEDIAL sign class matches Dravidian nominal root position
- TERMINAL sign class matches Dravidian case suffix (genitive/dative) position

**Status**: Structural hypothesis only. No phonemes have been confirmed.

---

## 3. Key Evidence Chain

1. **CISI corpus (Parpola 1987)**: 179 Mohenjo-daro inscriptions → baseline structural analysis
2. **Yajnadevam corpus**: 2,543 inscriptions from 52 sites → multi-site expansion
3. **CGSA Phases 1–6**: 40 structural clusters, entropy reduction 21.6%
4. **holdatllc cross-validation**: Independent confirmation of INITIAL signs P086 and P001
5. **Nair (2026) scorecard**: 4/4 linguistic-consistent metrics
6. **SA phonotactic analysis**: Dravidian > Pali > Sanskrit on Indus corpus (multiple runs)
7. **Phase 9 gate**: Cross-site stability gate passed (85.3% ≥ 70%)

---

## 4. Experiment Record

| Experiment | Result | Date | Commit |
|-----------|--------|------|--------|
| CGSA Phases 1–6 | 40 clusters, 85.3% cross-site stability | 2026-04-22 | 790ddd1 |
| Nair (2026) scorecard | 4/4 linguistic-consistent | 2026-04-22 | 98fd599 |
| holdatllc cross-validation | P086↔M077, P001↔M001 confirmed INITIAL | 2026-04-22 | 7d3e302 |
| SA Dravidian vs Pali | Dravidian higher consistency (multiple runs) | 2026-04-22 | 9a848fc |
| Phase 9 function validation | Pending full results | 2026-04-23 | TBD |
| Phase 9 Dravidian slot test | Pending full results | 2026-04-23 | TBD |
| P385 phoneme test | Pending (requires UI run) | — | — |

---

## 5. What Makes This Non-Trivial

- Previous computational analyses (Rao et al. 2009) were criticized for not addressing non-linguistic alternatives. Our approach explicitly tests against Nair (2026) non-linguistic baselines.
- Previous Dravidian hypotheses (Parpola 1994) were based on iconographic interpretation. Our approach is purely structural/statistical.
- The 85.3% cross-site stability is a new measurement not reported in prior literature.
- The holdatllc cross-validation uses a completely independent methodology and independently confirms two INITIAL signs.

---

## 6. Open Questions

1. Does the ICIT full corpus (6,800 inscriptions) show the same structural stability?
2. Does the positional grammar hold specifically for Harappa tablet sequences?
3. Can any held-out prediction succeed? (Registered, untested)
4. Is the Dravidian functional interpretation the best explanation, or could another agglutinative language match as well?

---

## 7. If This Reaches Critical Signal

Per Section 8 protocol:
1. Encrypted snapshot of all artifacts to be created
2. IP memo to be filed
3. Dr. Fuls (and potentially other experts) to be contacted with controlled disclosure
4. Patent relevance to be reviewed by IP counsel
5. Preprint to be prepared for arXiv submission

---

## 8. Narrative Timeline

| Date | Event |
|------|-------|
| 2026-04-01 | First external communication: Dr. Andreas Fuls contacted with project report |
| 2026-04-22 | Multi-site corpus expansion: Yajnadevam (52 sites, 2,543 inscriptions) |
| 2026-04-22 | CGSA Phases 1–6 completed: 40 clusters, 85.3% cross-site stability |
| 2026-04-22 | holdatllc ingestion and cross-validation |
| 2026-04-22 | Phase 9 gate passed (MODERATE signal) |
| 2026-04-23 | Governance infrastructure established (this dossier created) |
| 2026-04-23 | Phase 9 experiments re-run (results pending) |
