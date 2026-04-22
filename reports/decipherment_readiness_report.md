# Decipherment Readiness Report
Generated: 2026-04-22T17:16:01Z
**Site scope**: Mohenjo-daro only (179 inscriptions).

---

## Purpose

This report assesses whether the corpus and structural analysis are
sufficient to justify moving to Phase 9 (linguistic hypothesis testing).
Per the instructions: 'Success is not a phonetic decipherment. Success is a
representation that preserves the corpus, reduces entropy, improves
predictability, remains stable across sites and artifacts, and does not
require arbitrary sign collapse.'

---

## Phase 8 Summary — Candidate DoF Schema

### INITIAL_SLOT
  Description: Opening sign/signs — candidate title or determinative
  Evidence: 10 signs with start_rate >= 0.55
  Top candidates: P000, P324, P051, P301, P001, P086, P217, P013

### MEDIAL_SLOT
  Description: Internal signs — candidate root or modifier
  Evidence: 56 signs with internal_rate >= 0.70
  Top candidates: P215, P175, P332, P276, P058, P283, P123, P120

### TERMINAL_SLOT
  Description: Final sign/signs — candidate suffix or formula closure
  Evidence: 4 signs with end_rate >= 0.55
  Top candidates: P011, P256, P385, P378

### HAPAX_SLOT
  Description: Signs appearing once only — high uncertainty
  Evidence: 77 hapax signs (42.3% of sign inventory)
  Top candidates: none identified

---

## Entropy Analysis

- Sequence entropy in raw sign space: 7.4461 bits
- Sequence entropy in class-label space: 7.0688 bits
- Entropy reduction: 0.3772 bits (5.1%)

Class-label representation reduces sequence entropy, indicating that
structural classes capture real patterns in inscription structure.

## Recurrent Class Templates

  - MEDIAL_STRONG MEDIAL_STRONG: 308 times
  - MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG: 178 times
  - MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG: 92 times
  - INITIAL_STRONG MEDIAL_STRONG: 92 times
  - INITIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG: 72 times
  - MEDIAL_STRONG TERMINAL_STRONG: 62 times
  - INITIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG: 55 times
  - MIXED MEDIAL_STRONG: 39 times
  - MEDIAL_STRONG MEDIAL_STRONG TERMINAL_STRONG: 38 times
  - MEDIAL_STRONG HAPAX: 38 times
  - LOW_FREQUENCY MEDIAL_STRONG: 32 times
  - MEDIAL_STRONG MIXED: 32 times
  - MEDIAL_STRONG MEDIAL_STRONG HAPAX: 29 times
  - MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG TERMINAL_STRONG: 27 times
  - MEDIAL_STRONG LOW_FREQUENCY: 26 times
  - HAPAX MEDIAL_STRONG: 22 times
  - MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG HAPAX: 21 times
  - INITIAL_STRONG LOW_FREQUENCY: 21 times
  - LOW_FREQUENCY MEDIAL_STRONG MEDIAL_STRONG: 19 times
  - MEDIAL_STRONG MEDIAL_STRONG MIXED: 19 times

---

## Hard Review Checklist (from decipherment_agent_instructions.md)

- [ ] Mohenjo-daro is not the only major site represented — **FAIL: only M**
- [ ] Harappa is substantially represented — **FAIL: 0 inscriptions**
- [ ] Dholavira is represented — **FAIL: 0 inscriptions**
- [ ] Kalibangan and Lothal are represented — **FAIL: 0 inscriptions**
- [x] Artifact types are mixed — PASS
- [ ] Sign IDs are tied to images — **FAIL: no image data**
- [x] Variant handling is explicit — PASS (no collapsing)
- [x] Duplicate objects reconciled — PASS
- [x] No destructive surrogate alphabet — PASS
- [x] Crosswalk file exists — PASS
- [x] Positional and adjacency statistics run — PASS
- [x] Latent class report exists — PASS
- [x] DoF report exists — PASS

---

## Decision: Is Phase 9 (Linguistic Testing) Justified?

**NO. Phase 9 is NOT justified yet.**

Blocking reasons:
1. Only Mohenjo-daro data is present. Multi-site stability of latent classes
   has not been verified. Classes may be site-specific artefacts.
2. No image-backed sign crosswalk exists. Sign identity cannot be
   confirmed across sources.
3. The structural DoF schema is derived from a 179-inscription subset.
   The full CISI/ICIT corpus has ~6,800 inscriptions — 38x more data.
4. The hapax fraction is high (>= 50%), indicating sparse sign coverage
   in the available sample.

**Minimum conditions for Phase 9:**
1. At least Harappa inscriptions added (from CISI Vol.2 or equivalent).
2. Latent class structure verified as cross-site stable.
3. Visual crosswalk for the top 30 signs confirmed against sign plates.
4. Human review gate explicitly passed.

---

## Recommended Next Actions

1. **Acquire CISI Vol.2** — Harappa and additional Mohenjo-daro coverage.
2. **Check mayig repo** for H/L/DK site data additions.
3. **Acquire Fuls 2014** catalog — 676-sign crosswalk and frequency tables.
4. **Request full ICIT export** from Wells/Fuls (~6,800 inscriptions).
5. **Contact Parpola group** for CISI digital data access.
6. After corpus expansion: re-run Phases 6-8 and re-evaluate Phase 9 gate.

The structural infrastructure (corpus_master, sign_registry, crosswalk,
analysis scripts) is now in place. The bottleneck is data volume, not tooling.