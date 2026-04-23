# VALIDATION_PLAN
**Version**: 1.0  
**Date**: 2026-04-23  
**Owner**: Tristen Pierson / BitConcepts, LLC  
**Confidentiality**: INTERNAL

---

## 1. Purpose

This document plans the validation steps required to advance from MODERATE to HIGH signal, and from HIGH to CRITICAL signal. Each validation step has an explicit success criterion.

---

## 2. Validation Tiers

### Tier 1: Structural Validation (Active)

| Validation | Method | Success Criterion | Status |
|-----------|--------|-----------------|--------|
| Cross-site stability ≥ 70% | global_class_stability.py | ≥ 70% full stability | PASSED (85.3%) |
| Entropy reduction is non-trivial | Compare vs random clustering baseline | Reduction ≥ 10% | PASSED (21.6%) |
| Formulaic template rate consistent with linguistic system | Nair (2026) scorecard | ≥ 3/4 metrics consistent | PASSED (4/4) |
| holdatllc cross-validation on INITIAL signs | Compare against independent dataset | ≥ 2 confirmed INITIAL signs | PASSED (2 confirmed) |
| P122↔M342 crosswalk error corrected | Remove from crosswalk_master.csv | Error entry absent | PENDING |

### Tier 2: Held-Out Structural Prediction (Next)

| Validation | Method | Success Criterion | Status |
|-----------|--------|-----------------|--------|
| TERMINAL signs stable in ICIT full corpus | Apply PRED-2026-001 when ICIT available | ≥ 10/14 TERMINAL signs confirmed | PENDING |
| INITIAL signs stable in ICIT full corpus | Apply PRED-2026-002 when ICIT available | ≥ 8/12 INITIAL signs confirmed | PENDING |
| 3-slot template in new acquisition | Apply PRED-2026-003 | Coverage ≥ 70% in held-out corpus | PENDING |

### Tier 3: Linguistic Hypothesis Validation (Phase 9)

| Validation | Method | Success Criterion | Status |
|-----------|--------|-----------------|--------|
| Dravidian SA consistency vs Pali | indus_phase9_dravidian_slot_test | Dravidian mean_consistency > Pali by ≥ 0.05 | RUNNING |
| P385 phoneme test | indus_phase9_p385_phoneme_test | Dravidian terminal > random by ≥ 0.10 | PENDING (UI) |
| ICIT function alignment | indus_phase9_function_validation | ≥ 70% ITM signs in TERMINAL clusters | RUNNING |
| Template readings consistency | indus_phase9_template_readings | ≥ 70% of top-20 inscriptions parseable via slot schema | RUNNING |

### Tier 4: External Expert Validation (Future)

| Validation | Method | Success Criterion | Status |
|-----------|--------|-----------------|--------|
| Dr. Fuls review of structural findings | Controlled disclosure (Section 10 protocol) | Expert confirms findings are non-trivial | PENDING (no reply) |
| Image-backed sign identity | Physical CISI plate comparison | Top 30 signs verified against plates | PENDING |
| Independent replication | Third-party replication using REPRODUCIBILITY_PROTOCOL.md | Full pipeline replication confirmed | PENDING |

---

## 3. Validation Artifacts

All validation artifacts must be stored in `validation/` with SHA256 hashes in MASTER_LEDGER.md.

| Artifact | Location | Status |
|---------|---------|--------|
| global_class_stability.json | analysis/ | EXISTS |
| cross_site_stats.json | analysis/ | EXISTS |
| holdatllc_sign_roles.json | analysis/ | EXISTS |
| nair2026_scorecard_comparison.md | reports/ | EXISTS |
| Phase 9 experiment results | reports/phase9_*.json | PARTIAL |
| ICIT validation data | validation/ | PENDING |
| Image crosswalk validation | validation/ | PENDING |

---

## 4. Failure Protocol

If any Tier 2 or Tier 3 validation fails:
1. Log immediately in MASTER_LEDGER.md with entry_type=validation_attempt
2. Log in PREDICTION_REGISTER.md with outcome=REFUTED
3. Assess impact on SIGNAL_STATUS.md (may require downgrade)
4. Do NOT suppress or delay logging of failure
5. Investigate whether failure reveals model error, data error, or genuine falsification
