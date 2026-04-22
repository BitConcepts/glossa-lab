# Consolidated Structural Grammar Report
Generated: 2026-04-22T21:40:30Z

## Evidence Sources
1. **CISI corpus (mayig digitization)** — 179 Mohenjo-daro inscriptions (Parpola P-numbers, MIT)
2. **Yajnadevam corpus** — 2,543 multi-site inscriptions from 52 sites (GPL-3.0)
3. **CGSA Phase 5-8** — 40 structural clusters, 85.3% cross-site stability
4. **CAS Phase 9** — CPSC constraint projection, 80 signs classified, 0 violations
5. **holdatllc analysis** (MIT) — 1,670 seal sequences, 151 Mahadevan signs with roles

---

## Cross-Validation Summary

- holdatllc signs with P-number mapping: 8
- **Confirmed agreements** (same role in both systems): **2**
- **Conflicts** (different role assignments): **1**

Agreement rate on mapped signs: 25.0%

---

## Conflict Analysis (Critical)

### ⚠️ M342 ↔ P122: holdatllc=TERMINAL vs ours=MEDIAL
  holdatllc: CASE_MARKER_SUFFIX (count=584, is_ending=True, is_starter=False)
  Our CAS:  MEDIAL (from Phase 9 constraint projection)

  **CRITICAL**: P122↔M342 crosswalk mapping is WRONG.
  P122 = 'Two adjacent half-height vertical strokes' (Parpola) = numeral/medial sign
  M342 = 'Jar sign' (Mahadevan) = most frequent terminal sign (584 occurrences)
  These are DIFFERENT signs. The crosswalk entry must be removed/flagged.
  M342 most likely maps to P385 or P378 (our primary TERMINAL signs).
  **Action**: Remove P122↔M342 from crosswalk_master.csv.

---

## Confirmed TERMINAL Signs (CASE_MARKER_SUFFIX)

Signs confirmed as TERMINAL by BOTH our CAS analysis AND holdatllc:


### All holdatllc CASE_MARKER_SUFFIX signs (independent validation):

| M-number | Count | avg_pos | P-number | Our role | Agreement |
|----------|-------|---------|----------|----------|-----------|
| M267 | 400 | 0.540 | — | NO_P_MAPPING | — |
| M099 | 389 | 0.598 | — | NO_P_MAPPING | — |
| M176 | 356 | 0.607 | — | NO_P_MAPPING | — |
| M211 | 249 | 0.622 | — | NO_P_MAPPING | — |
| M328 | 234 | 0.595 | — | NO_P_MAPPING | — |
| M293 | 232 | 0.621 | — | NO_P_MAPPING | — |
| M162 | 205 | 0.608 | — | NO_P_MAPPING | — |
| M391 | 193 | 0.600 | — | NO_P_MAPPING | — |
| M367 | 190 | 0.695 | — | NO_P_MAPPING | — |
| M089 | 171 | 0.684 | — | NO_P_MAPPING | — |
| M233 | 171 | 0.712 | — | NO_P_MAPPING | — |
| M051 | 163 | 0.653 | — | NO_P_MAPPING | — |
| M336 | 161 | 0.681 | — | NO_P_MAPPING | — |
| M048 | 157 | 0.627 | — | NO_P_MAPPING | — |
| M065 | 154 | 0.669 | — | NO_P_MAPPING | — |
| M012 | 143 | 0.605 | — | NO_P_MAPPING | — |
| M125 | 132 | 0.734 | — | NO_P_MAPPING | — |
| M087 | 130 | 0.678 | — | NO_P_MAPPING | — |
| M305 | 83 | 0.988 | — | NO_P_MAPPING | — |
| M249 | 73 | 0.981 | — | NO_P_MAPPING | — |
| M220 | 62 | 0.992 | — | NO_P_MAPPING | — |

---

## Confirmed INITIAL Signs (CLASSIFIER_PREFIX)

Signs confirmed as INITIAL by BOTH our CAS analysis AND holdatllc:

- **P086** ↔ M077: count=18, avg_pos=0.0
- **P001** ↔ M001: count=14, avg_pos=0.0

### Top holdatllc CLASSIFIER_PREFIX signs:

  M062: count=28 (P-mapping pending)
  M073: count=25 (P-mapping pending)
  M079: count=24 (P-mapping pending)
  M045: count=24 (P-mapping pending)
  M016: count=23 (P-mapping pending)
  M013: count=23 (P-mapping pending)
  M022: count=22 (P-mapping pending)
  M008: count=22 (P-mapping pending)
  M061: count=22 (P-mapping pending)
  M052: count=22 (P-mapping pending)
  M058: count=21 (P-mapping pending)
  M060: count=20 (P-mapping pending)
  M019: count=20 (P-mapping pending)
  M044: count=19 (P-mapping pending)
  M035: count=19 (P-mapping pending)
  M053: count=19 (P-mapping pending)
  M003: count=19 → P003
  M080: count=19 (P-mapping pending)
  M056: count=19 (P-mapping pending)
  M077: count=18 → P086

---

## M125 Boundary Operator Analysis

M125 holdatllc role: **CASE_MARKER_SUFFIX** (count=132, avg_position=0.734)

Holdatllc README identifies M125 as 'syntactic boundary operator' (75% clause-split validity). CSV classifies it as CASE_MARKER_SUFFIX. These are compatible if M125 is both a case suffix AND a clause boundary marker — consistent with Dravidian postpositional structure.

**Candidates for P-equivalent of M125** (signs with avg_position 0.60–0.85 in CISI corpus):

  - P122: freq=76, avg_pos=0.641
  - P120: freq=22, avg_pos=0.675
  - P378: freq=17, avg_pos=0.755
  - P154: freq=14, avg_pos=0.669
  - P325: freq=14, avg_pos=0.639
  - P256: freq=12, avg_pos=0.825
  - P205: freq=10, avg_pos=0.637
  - P011: freq=10, avg_pos=0.692

---

## Consolidated Dravidian Slot Assignment

Based on convergence of: structural clustering (CGSA), CAS constraint projection,
holdatllc semantic roles, and SA phonotactic evidence.

| Slot | Structural class | holdatllc role | Phoneme cands | Dravidian function |
|------|-----------------|----------------|---------------|-------------------|
| INITIAL | CLASSIFIER_PREFIX | INITIAL | /k/ /m/ /p/ /n/ | Title/determinative |
| MEDIAL | MEDIAL_STRONG | (none) | /a/ /i/ /o/ /u/ | Phonetic stem |
| TERMINAL | CASE_MARKER_SUFFIX | TERMINAL | /n/ /l/ /ku/ /al/ | Dravidian case suffix |
| BIMODAL | PERSON_OR_OWNER | BIMODAL | varies | Owner/person marker |

**Highest-confidence sign assignments:**

| Sign | Slot | Phoneme | Confidence | Sources |
|------|------|---------|------------|---------|
| P385 | TERMINAL | /n/ | HIGH | SA (0.8591) + CAS TERMINAL + holdatllc M380≈TERMINAL |
| P324 | INITIAL | /k/ | HIGH | SA anchor + CAS INITIAL + start_rate=0.690 |
| P122 | MEDIAL | /a/ | MED | SA anchor + CAS MEDIAL + internal_rate=1.0 |
| P086 | INITIAL | /m/ | MED | SA anchor + CAS INITIAL + M077 confirmed |
| P332 | MEDIAL | /o/ | MED | SA anchor + follows P324 in 91% of occurrences |
| M342→? | TERMINAL | /n/ | MED | holdatllc #1 TERMINAL (584) — needs P-mapping |

---

## Next Steps

1. **Fix P122↔M342 crosswalk** — remove the wrong entry, identify M342's correct P-number
2. **Map M342 to a P-number** — visual comparison of 'jar sign' against Parpola plates
3. **Expand crosswalk** using holdatllc's 22 TERMINAL + 77 INITIAL signs with positional data
4. **Acquire Harappa tablet sequences** — tablets likely encode phonetic sequences
5. **Send email to Dr. Fuls** for ICIT data (5,500+ inscriptions)
6. **Verify M125 equivalent** in CISI corpus as boundary/clause operator