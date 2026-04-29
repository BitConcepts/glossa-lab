# SIGNAL_STATUS
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / Layer1Labs Silicon, Inc.  
**Confidentiality**: INTERNAL

---

## 1. Current Signal Level

**SIGNAL LEVEL: MODERATE**  
**Assessed**: 2026-04-23  
**Previous level**: LOW (before multi-site corpus expansion, 2026-04-22)

---

## 2. Signal Threshold Definitions (Per Section 7 of Operating Instructions)

| Level | Definition |
|-------|-----------|
| LOW | Interesting structure, repeatable clustering, stronger-than-baseline regularities |
| **MODERATE** | Candidate grammar-like regularity, reproducible decomposition, stable sign-role assignments, multiple independent experiments converge |
| HIGH | Held-out predictions succeed, broad corpus explanatory power, internal consistency, alternative explanations less plausible |
| CRITICAL | Strong held-out success + stable cross-subset hypothesis + deterministic reproducibility + external expert confirms non-trivial + explanatory power clearly exceeds chance |

---

## 3. Evidence Supporting MODERATE Rating

| Evidence | Details |
|---------|---------|
| Cross-site stability 85.3% | Full stability rate over 52 sites; Phase 9 gate passed (threshold: 70%) |
| 40 reproducible structural clusters | Agglomerative clustering is deterministic; reproduced on re-run |
| 21.6% entropy reduction | Class-label space reduces sequence entropy by 2.31 bits vs random clustering baseline |
| holdatllc cross-validation | Two independent INITIAL signs (P086↔M077, P001↔M001) confirmed by completely independent dataset |
| Nair (2026) scorecard | 4/4 metrics in linguistic-consistent range |
| Formulaic template coverage | 86.0% of inscriptions contain a recurrent template |
| SA convergence: Dravidian > Pali, Sanskrit (control) | mean_consistency higher for Dravidian LM in multiple runs |
| Phase 9 gate explicitly passed | Review gate from CGSA Phase 6 cleared 2026-04-22 |

---

## 4. Evidence Pending for HIGH Signal

| Required Signal | Current Status |
|----------------|---------------|
| Held-out prediction success (structural) | PENDING — registered in PREDICTION_REGISTER.md, not yet tested |
| Held-out prediction success (linguistic) | PENDING — requires phonetic framework, not yet established |
| Broad corpus explanatory power | PARTIAL — 2,722 inscriptions, 40% of known corpus |
| SA convergence replicated | PENDING — needs replication with fixed model version |
| Alternative explanations tested and rejected | PARTIAL — heraldic/administrative addressed; Proto-Elamite not yet compared |

---

## 5. Blockers for HIGH Signal

1. **No held-out prediction has been formally tested** — predictions exist in PREDICTION_REGISTER.md but withheld data not yet evaluated.
2. **No external expert confirmation** — Dr. Fuls contacted (April 1, 2026); no reply received.
3. **Image-backed crosswalk incomplete** — sign identity unconfirmed visually.
4. **Corpus at 40% of known CISI/ICIT** — broader corpus may change results.

---

## 6. Blockers for CRITICAL Signal

All MODERATE→HIGH blockers, plus:
- External domain expert (Dr. Fuls or equivalent) must confirm a finding as non-trivial
- Cross-subset stability must be demonstrated with formal held-out test
- Deterministic reproducibility must be documented with matched SHA256 hashes

---

## 7. Actions That Would Upgrade Signal Level

| Action | Signal upgrade |
|--------|---------------|
| Run held-out prediction on withheld corpus subset | LOW→MODERATE already done; MODERATE→HIGH if prediction confirmed |
| Acquire ICIT data and re-run | Potential HIGH if 85%+ stability maintained |
| Dr. Fuls replies with non-trivial confirmation | Contributes to CRITICAL pathway |
| Bilingual text or IVC-Brahmi evolutionary link found | Would unlock phonetic testing pathway |

---

## 8. Disclosure Lock Status

**Disclosure lock: ACTIVE**  
No public claims, press releases, or unrestricted expert sharing until HIGH signal is achieved and the Section 8 protocol is executed. Only controlled communication with Dr. Fuls is authorized (logged in DISCLOSURE_LOG.md).

---

## 9. Change History

| Date | From | To | Reason |
|------|------|----|--------|
| 2026-04-22 | LOW | MODERATE | Multi-site corpus expansion (52 sites), cross-site stability 85.3%, Phase 9 gate passed |
