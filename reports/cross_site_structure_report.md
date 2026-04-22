# Cross-Site Structural Analysis Report
Generated: 2026-04-22T18:13:02Z
**NOTE**: Classification uses RELATIVE frequency thresholds (site_min_freq = max(2, N//30)).
This avoids HAPAX inflation in small sites (45-80 inscriptions) vs large (1381).
Yajnadevam Y-unmapped signs are treated as site-unique and excluded from multi-site stability.

---

## 1. Site Coverage

Sites with ≥20 inscriptions included: 6

- **Mohenjo-daro**: 1381 inscriptions, 6830 tokens, 466 signs, H1=6.6562 bits
- **Harappa**: 970 inscriptions, 3833 tokens, 317 signs, H1=6.3504 bits
- **Lothal**: 80 inscriptions, 371 tokens, 94 signs, H1=5.6608 bits
- **Dholavira**: 74 inscriptions, 313 tokens, 110 signs, H1=6.0684 bits
- **Kalibangan**: 54 inscriptions, 236 tokens, 91 signs, H1=5.7823 bits
- **Chanhujo-daro**: 45 inscriptions, 223 tokens, 85 signs, H1=5.5752 bits

---

## 2. Per-Site Structural Profiles

### Mohenjo-daro
- Inscriptions: 1381 | Tokens: 6830 | Signs: 466
- Hapax fraction: 38.0% | Mean length: 4.95 signs
- H1: 6.6562 bits | H2: 3.3113 bits
- TERMINAL candidates: 4 | INITIAL candidates: 5
- Class distribution: {'MEDIAL': 21, 'TERMINAL': 4, 'LOW_FREQ': 251, 'HAPAX': 177, 'MIXED': 8, 'INITIAL': 5}
- Top terminal signs: P210, P378, P385, Yunmapped_0920
- Top initial signs: P004, P013, P098, P217, P324
- Top 5 signs: [('P324', 742), ('P122', 403), ('P086', 240), ('P385', 205), ('P050', 175)]

### Harappa
- Inscriptions: 970 | Tokens: 3833 | Signs: 317
- Hapax fraction: 37.2% | Mean length: 3.95 signs
- H1: 6.3504 bits | H2: 2.7904 bits
- TERMINAL candidates: 2 | INITIAL candidates: 5
- Class distribution: {'MIXED': 14, 'LOW_FREQ': 168, 'HAPAX': 118, 'MEDIAL': 10, 'INITIAL': 5, 'TERMINAL': 2}
- Top terminal signs: P123, P385
- Top initial signs: P004, P013, P098, P217, P310
- Top 5 signs: [('P324', 468), ('P098', 254), ('P122', 139), ('P086', 126), ('P062', 116)]

### Lothal
- Inscriptions: 80 | Tokens: 371 | Signs: 94
- Hapax fraction: 47.9% | Mean length: 4.64 signs
- H1: 5.6608 bits | H2: 1.4507 bits
- TERMINAL candidates: 5 | INITIAL candidates: 8
- Class distribution: {'INITIAL': 8, 'MIXED': 16, 'MEDIAL': 19, 'HAPAX': 45, 'TERMINAL': 5, 'BIMODAL': 1}
- Top terminal signs: P060, P316, P378, P385, Yunmapped_0920
- Top initial signs: P001, P004, P013, P217, P301, P324, Yunmapped_0236, Yunmapped_0409
- Top 5 signs: [('P324', 38), ('P122', 30), ('P385', 21), ('P050', 15), ('P086', 13)]

### Dholavira
- Inscriptions: 74 | Tokens: 313 | Signs: 110
- Hapax fraction: 52.7% | Mean length: 4.23 signs
- H1: 6.0684 bits | H2: 1.4934 bits
- TERMINAL candidates: 9 | INITIAL candidates: 6
- Class distribution: {'INITIAL': 6, 'MIXED': 19, 'TERMINAL': 9, 'HAPAX': 58, 'MEDIAL': 17, 'BIMODAL': 1}
- Top terminal signs: P031, P123, P145, P194, P230, P385, Yunmapped_0019, Yunmapped_0408
- Top initial signs: P001, P004, P013, P217, P324, Yunmapped_0832
- Top 5 signs: [('P324', 28), ('P122', 21), ('P086', 14), ('P385', 11), ('P121', 10)]

### Kalibangan
- Inscriptions: 54 | Tokens: 236 | Signs: 91
- Hapax fraction: 58.2% | Mean length: 4.37 signs
- H1: 5.7823 bits | H2: 1.0926 bits
- TERMINAL candidates: 5 | INITIAL candidates: 5
- Class distribution: {'MIXED': 16, 'INITIAL': 5, 'HAPAX': 53, 'MEDIAL': 12, 'TERMINAL': 5}
- Top terminal signs: P123, P154, P378, P385, Yunmapped_0091
- Top initial signs: P001, P086, P217, P324, Yunmapped_0892
- Top 5 signs: [('P122', 22), ('P324', 20), ('Yunmapped_0892', 9), ('P385', 8), ('P086', 8)]

### Chanhujo-daro
- Inscriptions: 45 | Tokens: 223 | Signs: 85
- Hapax fraction: 65.9% | Mean length: 4.96 signs
- H1: 5.5752 bits | H2: 1.4467 bits
- TERMINAL candidates: 2 | INITIAL candidates: 4
- Class distribution: {'INITIAL': 4, 'MIXED': 8, 'HAPAX': 56, 'BIMODAL': 1, 'MEDIAL': 14, 'TERMINAL': 2}
- Top terminal signs: P385, Yunmapped_0920
- Top initial signs: P001, P217, P324, Yunmapped_0161
- Top 5 signs: [('P324', 24), ('P122', 15), ('P145', 13), ('P144', 13), ('P385', 11)]

---

## 3. Cross-Site Sign Inventory Overlap

- Mohenjo-daro ↔ Harappa: Jaccard=0.4185, shared signs=231
- Mohenjo-daro ↔ Lothal: Jaccard=0.1765, shared signs=84
- Mohenjo-daro ↔ Dholavira: Jaccard=0.2203, shared signs=104
- Mohenjo-daro ↔ Kalibangan: Jaccard=0.1702, shared signs=81
- Mohenjo-daro ↔ Chanhujo-daro: Jaccard=0.1503, shared signs=72
- Harappa ↔ Lothal: Jaccard=0.238, shared signs=79
- Harappa ↔ Dholavira: Jaccard=0.2708, shared signs=91
- Harappa ↔ Kalibangan: Jaccard=0.2326, shared signs=77
- Harappa ↔ Chanhujo-daro: Jaccard=0.2145, shared signs=71
- Lothal ↔ Dholavira: Jaccard=0.351, shared signs=53
- Lothal ↔ Kalibangan: Jaccard=0.3603, shared signs=49
- Lothal ↔ Chanhujo-daro: Jaccard=0.3459, shared signs=46
- Dholavira ↔ Kalibangan: Jaccard=0.3581, shared signs=53
- Dholavira ↔ Chanhujo-daro: Jaccard=0.3, shared signs=45
- Kalibangan ↔ Chanhujo-daro: Jaccard=0.3134, shared signs=42

---

## 4. Latent Class Stability Across Sites

- Multi-site signs (appear in ≥2 sites): 275
- Signs with SAME class in all sites: 82
- **Class stability rate: 29.8%**

High stability (>70%) means latent classes are a real structural property
of the script, not a site-specific artefact.

### Stable signs (same class across all sites they appear in):

  - P385: TERMINAL
  - P205: LOW_FREQ
  - P122: MEDIAL
  - P096: LOW_FREQ
  - P120: MEDIAL

### Unstable signs (different class across sites):

  - P121: {'Mohenjo-daro': 'MEDIAL', 'Chanhujo-daro': 'MIXED', 'Dholavira': 'MEDIAL', 'Harappa': 'MEDIAL', 'Kalibangan': 'HAPAX', 'Lothal': 'MEDIAL'}
  - P202: {'Mohenjo-daro': 'MEDIAL', 'Chanhujo-daro': 'HAPAX', 'Dholavira': 'MIXED', 'Harappa': 'LOW_FREQ', 'Kalibangan': 'MIXED', 'Lothal': 'HAPAX'}
  - P073: {'Mohenjo-daro': 'MEDIAL', 'Dholavira': 'HAPAX', 'Harappa': 'MIXED', 'Kalibangan': 'MIXED', 'Lothal': 'MEDIAL'}
  - P108: {'Mohenjo-daro': 'LOW_FREQ', 'Dholavira': 'HAPAX', 'Harappa': 'HAPAX'}
  - P320: {'Mohenjo-daro': 'LOW_FREQ', 'Chanhujo-daro': 'MIXED', 'Dholavira': 'HAPAX', 'Harappa': 'LOW_FREQ', 'Kalibangan': 'MIXED'}
  - P145: {'Mohenjo-daro': 'MEDIAL', 'Chanhujo-daro': 'MIXED', 'Dholavira': 'TERMINAL', 'Harappa': 'MIXED', 'Kalibangan': 'MIXED', 'Lothal': 'MEDIAL'}
  - P094: {'Mohenjo-daro': 'LOW_FREQ', 'Chanhujo-daro': 'MEDIAL', 'Harappa': 'HAPAX'}
  - P186: {'Mohenjo-daro': 'LOW_FREQ', 'Harappa': 'HAPAX'}
  - P147: {'Mohenjo-daro': 'MEDIAL', 'Chanhujo-daro': 'HAPAX', 'Dholavira': 'MIXED', 'Harappa': 'MIXED', 'Kalibangan': 'MIXED', 'Lothal': 'HAPAX'}
  - P316: {'Mohenjo-daro': 'MEDIAL', 'Chanhujo-daro': 'HAPAX', 'Dholavira': 'MIXED', 'Harappa': 'MEDIAL', 'Lothal': 'TERMINAL'}

---

## 5. Interpretation for Review Gate

Class stability rate: 29.8%

**CAUTION**: Class stability < 50% — classes may be site-specific.
This may reflect the two different sign numbering systems (P vs Y).
Cross-system analysis requires the Y↔P crosswalk to be applied first.

NOTE: Low apparent cross-system overlap between CISI (P-numbers) and
Yajnadevam (Y-numbers) is EXPECTED because the two sign systems use
different IDs for the same signs. Apply the Y↔P crosswalk before
interpreting cross-system stability scores.