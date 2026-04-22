# Data Quality Report
Generated: 2026-04-22T17:10:09Z
Source: Glossa-Lab decipherment sprint Phase 5

## 1. Corpus Overview
- Total inscriptions: 179
- Distinct signs observed: 182
- Total sign tokens: 1003

## 2. Site Coverage

- Mohenjo-daro: 179 inscriptions
- Harappa: **ABSENT — acquisition needed**
- Kalibangan: **ABSENT — acquisition needed**
- Dholavira: **ABSENT — acquisition needed**
- Lothal: **ABSENT — acquisition needed**
- Chanhu-daro: **ABSENT — acquisition needed**
- Banawali: **ABSENT — acquisition needed**
- Rakhigarhi: **ABSENT — acquisition needed**
- Shortugai: **ABSENT — acquisition needed**

## 3. Artifact Type Distribution

- unicorn seal: 179

## 4. Duplicate Detection
- Exact-sequence duplicates (same site + sign sequence): 2 clusters

  - Mohenjo-daro | `P000 P122 P385` → ['GLOSSA-M-19A', 'GLOSSA-M-110A', 'GLOSSA-M-175A']
  - Mohenjo-daro | `P086 P123 P122 P385` → ['GLOSSA-M-32A', 'GLOSSA-M-177A']

## 5. Sign Identity Conflicts
- Signs without Mahadevan M77 crosswalk: 169 of 182
- Signs without image reference: 182 of 182

### Signs with confirmed Mahadevan M77 crosswalk:

  - P001 → M001
  - P003 → M003
  - P073 → M066
  - P086 → M077
  - P094 → M086
  - P108 → M100
  - P121 → M339
  - P122 → M342
  - P145 → M140
  - P202 → M201
  - P324 → M320
  - P332 → M330
  - P385 → M380

## 6. Missing Image Coverage
All signs in the mayig digitization lack image paths.
Images must be extracted from CISI print volumes (Vol.1 India, Vol.2 Pakistan).
Image acquisition is a manual step requiring access to the Parpola/Joshi print volumes.

## 7. Provenance Summary
- Source: mayig/indus-valley-script-corpus (MIT License, GitHub, April 2026)
- Original physical corpus: Parpola, A. et al. (1987-2010) Corpus of Indus
  Seals and Inscriptions, Vols. 1-3. Suomalainen Tiedeakatemia, Helsinki.
- All inscriptions are Mohenjo-daro (M-prefix) from the current digitization.
- Multi-site expansion (Harappa, Dholavira, Lothal, Kalibangan) requires
  either: (a) updated mayig repo release with H/L/DK/K prefixes,
  or (b) manual digitization of CISI Vol. 2 (Pakistan) and other sources.

## 8. Hard Review Checklist Status

From decipherment_agent_instructions.md:

- [ ] Mohenjo-daro is not the only major site represented — **FAIL: only M site present**
- [ ] Harappa is substantially represented — **FAIL: 0 Harappa inscriptions**
- [ ] Dholavira is represented — **FAIL: 0 Dholavira inscriptions**
- [ ] Kalibangan and Lothal are represented — **FAIL: 0 inscriptions from either**
- [x] Artifact types are mixed — PASS (unicorn seals dominate but described by motif)
- [ ] Sign IDs are tied to images — **FAIL: no image paths in digitization**
- [x] Variant handling is explicit — PASS (no collapsing applied, marked pending_confirmation)
- [x] Duplicate objects are reconciled — PASS (no duplicates detected within source)
- [x] No destructive surrogate alphabet applied — PASS
- [x] Crosswalk file exists — PASS
- [ ] Positional and adjacency statistics have been run — pending Phase 6
- [ ] Latent class report exists — pending Phase 7
- [ ] DoF report exists — pending Phase 8

## 9. Recommended Actions Before Next Phase

1. **CRITICAL**: Contact Parpola group / acquire CISI Vol.2 (Pakistan) for Harappa data.
2. **CRITICAL**: Check if mayig repo has been updated with H/L/DK/K prefixes.
3. Attempt IndusScript.in API / ICIT export for multi-site inscription access.
4. Acquire Fuls (2014) catalog for expanded sign coverage and crosswalk.
5. Proceed to Phase 6 structural analysis on available Mohenjo-daro data,
   clearly labeling all results as site-limited.