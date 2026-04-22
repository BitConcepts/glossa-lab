# Decipherment Readiness Report
Generated: 2026-04-22T17:35:27Z
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
  Evidence: 20 signs with start_rate >= 0.55
  Top candidates: P004, Y0156, Y0064, Y0090, P098, Y0153, Y0155, P001

### MEDIAL_SLOT
  Description: Internal signs — candidate root or modifier
  Evidence: 235 signs with internal_rate >= 0.70
  Top candidates: Y0382, Y0390, Y0337, Y0035, Y0048, Y0455, P316, Y0585

### TERMINAL_SLOT
  Description: Final sign/signs — candidate suffix or formula closure
  Evidence: 20 signs with end_rate >= 0.55
  Top candidates: Y0371, Y0098, Y0201, P385, Y0137, Y0260, Y0091, P378

### HAPAX_SLOT
  Description: Signs appearing once only — high uncertainty
  Evidence: 276 hapax signs (35.7% of sign inventory)
  Top candidates: none identified

---

## Entropy Analysis

- Sequence entropy in raw sign space: 10.6691 bits
- Sequence entropy in class-label space: 8.3636 bits
- Entropy reduction: 2.3055 bits (21.6%)

Class-label representation reduces sequence entropy, indicating that
structural classes capture real patterns in inscription structure.

## Recurrent Class Templates

  - MEDIAL_STRONG MEDIAL_STRONG: 1689 times
  - MEDIAL_STRONG MIXED: 1195 times
  - INITIAL_STRONG MEDIAL_STRONG: 1161 times
  - MIXED MEDIAL_STRONG: 1148 times
  - INITIAL_STRONG MIXED: 786 times
  - MEDIAL_STRONG TERMINAL_STRONG: 742 times
  - MIXED MIXED: 670 times
  - MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG: 616 times
  - INITIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG: 568 times
  - MEDIAL_STRONG MEDIAL_STRONG MIXED: 435 times
  - MEDIAL_STRONG MIXED MEDIAL_STRONG: 398 times
  - INITIAL_STRONG MEDIAL_STRONG MIXED: 378 times
  - INITIAL_STRONG INITIAL_STRONG: 373 times
  - MIXED MEDIAL_STRONG MEDIAL_STRONG: 362 times
  - INITIAL_STRONG MIXED MEDIAL_STRONG: 351 times
  - MEDIAL_STRONG MEDIAL_STRONG TERMINAL_STRONG: 322 times
  - MIXED MEDIAL_STRONG MIXED: 286 times
  - MIXED TERMINAL_STRONG: 279 times
  - MIXED MEDIAL_STRONG TERMINAL_STRONG: 253 times
  - MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG MEDIAL_STRONG: 219 times

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