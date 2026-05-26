# FINAL RELEASE CHECK — Indus Script Preprint v2
**Generated**: 2026-05-21  
**Branch**: preprint-last-mechanical-polish  
**File checked**: `glossa-corpus/indus/preprint.tex`  
**PDF artifact**: `preprint.pdf` (105,829 bytes)

---

## A. MANUSCRIPT INTEGRITY CHECKS

### A1. Forbidden / Overreach Language
- [x] `proven` — **0 hits** (PASS)
- [x] `definitive` — **0 hits** (PASS)
- [x] `establishes` — **0 hits** (PASS)
- [x] Bare `p = 0.x` p-value form — **0 hits** (PASS)

### A2. Stale Sign Reference Audit
- [x] `M372` mention — **0 hits** (PASS; removed in prior passes)

### A3. Arrow Formatting
- [x] Raw `->` (not preceded by `\`) — **0 hits** after fixing `<-->` on line 226 (PASS)
- [x] All arrows in body text use `\textgreater{}` or `$\to$` (PASS)

### A4. Third-Party Emails
- [x] No third-party email addresses — **0 hits** (PASS; only `tpierson@bitconcepts.tech` author email present)

### A5. Peer-Review Status
- [x] "Not peer-reviewed" disclaimer present in header (line 80) — **PASS** (intentional, correct)
- [x] No false claim of peer review anywhere — confirmed

---

## B. REQUIRED CONTENT CHECKS

### B1. Core Statistics
- [x] `z = 10.3` present — **3 occurrences** (Abstract, §3.10, §5 Conclusion)
- [x] `0/2000 permutations` present — **3 occurrences**
- [x] `0/140` fish-sign result present — **5 occurrences**

### B2. Anchor Model Numbers
- [x] `161` H+M readings — **22 occurrences** (PASS)
- [x] `90.96%` token coverage — **6 occurrences** (PASS)
- [x] `69.8%` seal coverage — **4 occurrences** (PASS)

### B3. Section Structure
- [x] Abstract present and complete
- [x] §1.3 "This Work" opens with `computational grammar and candidate anchor model` — **1 hit** (PASS)
- [x] §2.1 Corpus — present
- [x] §2.2 Evidence Hierarchy — present, PROVISIONAL_MEDIUM flagged
- [x] §3.1 Sign Anchor Summary table — present
- [x] §3.4 M267 correction — present
- [x] §3.5 Fish Sign Polysemy Test — present
- [x] §4.4 Limitations (6 items including language-family baseline) — present
- [x] §5 Conclusion with Tier 1/2/3 framing — present
- [x] §6 Data Availability — **present** with draft caveat
- [x] §7 Acknowledgments — present
- [x] §8 References — present
- [x] Appendix A (Phase-128/129 anchors) — present
- [x] Appendix B (18 irresolvable signs) — present
- [x] Appendix C (59 foundation checks) — present

### B4. Data Availability & Draft Caveat
- [x] "not yet public" or "review draft" caveat in §6 — **3 occurrences** (PASS)
- [x] Holdat corpus availability caveat present — confirmed

### B5. External Replication
- [x] Nair 2026 / arXiv:2604.17828 citation — **8 occurrences** (PASS)

---

## C. ACKNOWLEDGMENTS & THIRD-PARTY SOURCE CHECKS

### C1. Supplementary Sources List
- [x] Martini absent from Supplementary sources block — **PASS** (removed; private/unpublished source)
- [x] Roif absent from Supplementary sources block — **PASS** (removed; private/unpublished source)

### C2. Acknowledgments (informal, OK to retain)
- [x] Martini acknowledged in §7 as "discussion of later South Asian administrative vocabulary" — **1 hit** (INFO; appropriate personal thanks, not cited as source)
- [x] Roif acknowledged in §7 as "correspondence on fish-sign polysemy" — **1 hit** (INFO; appropriate personal thanks, not cited as source)
- [x] Nair acknowledged for independent replication — present

---

## D. LATEX COMPILATION

### D1. Compile Result
- [x] XeLaTeX pass 1 — **exit 0**, no fatal errors
- [x] XeLaTeX pass 2 — **exit 0**, no LaTeX errors or undefined references
- [x] PDF produced: `preprint.pdf` (105,829 bytes)
- [x] Font: Noto Serif (text) + Latin Modern Math (math) — active in preamble
- [x] Overfull hboxes — **3 minor overflows** (≤60pt in §1.3 list, ≤8pt in tables; non-critical for review draft)
- [ ] Longtable width warnings — **6 longtable warnings** (column widths converged on 2nd pass; standard behaviour, non-blocking)

### D2. Unicode / Glyph Coverage
- [x] All Dravidian diacritics use Noto Serif — no missing glyph warnings in compile log
- [x] Math symbols use Latin Modern Math — no math font errors

---

## E. REPOSITORY GATING

### E1. Repository Status
- [ ] Repository is currently **private** — arXiv posting BLOCKED until made public
- [x] Data Availability section acknowledges private repository status
- [x] Anchor table, scripts, and phase reports flagged for pre-posting release

**Pre-arXiv checklist — do before making repo public:**
- [ ] Populate repository with: anchor table, confidence labels, DEDR citations, basis statements, scripts, phase reports, and a README explaining the Holdat corpus access limitation
- [ ] Once repo is live and populated, change `"will be released"` → `"are available"` in **§6 Data Availability** and **AI Disclosure** (both instances in `preprint.tex`)

### E2. Holdat Corpus
- [x] Holdat corpus availability caveat in Data Availability and AI Disclosure
- [x] Miller (2025) reference entry includes "Not publicly released at time of writing"

### E3. Reference List Completeness
- [x] All in-text citations have reference entries: Burrow & Emeneau (DEDR), Crawford, Farmer/Sproat/Witzel, Hojlund & Abu-Laban, Krishnamurti, Laursen, Lubotsky, Mahadevan (1977), McAlpin, Miller (2025), Nair (2026), Parpola (1994, 2010), Rao et al. (2009), Southworth, Wells (2011), Witzel (1999)
- [ ] Martini (2025) PhD dissertation — **NOT in reference list** (appropriate: acknowledged informally, not cited as a source)
- [ ] Roif (2025) — **NOT in reference list** (appropriate: acknowledged informally, not cited as a source)
- [ ] Mitchell (1986) mentioned in §3.19 text but **not in reference list** — GATING ISSUE (minor; resolve before arXiv posting)
- [ ] Steinkeller (1982), Potts (1994), Reade (2001), Kjaerum (1983), Parpola (1975) — cited in §3.28 but not in reference list — GATING ISSUE (minor; full citations needed before arXiv posting)

---

## F. CLAIM TIER INTEGRITY

### F1. Tier 1 (Structural — High Confidence)
- [x] Positional structure z=10.3, 0/2000 permutations — stated as high confidence
- [x] Three-slot grammar model — stated as empirically derived
- [x] Fish-sign compound-only 0/140 — stated as factual result
- [x] M267 correction — stated as factual correction

### F2. Tier 2 (Candidate Readings — Supported but Unreviewed)
- [x] 161 H+M readings at 90.96% token coverage — framed as candidate, not final
- [x] PROVISIONAL_MEDIUM signs flagged explicitly
- [x] Coverage figures defined as anchor-model assignment, not phonetic transcription

### F3. Tier 3 (Speculative — Caveated)
- [x] Guild-identity interpretation — marked speculative in §4.1 and §5
- [x] Arthaśāstra continuity — marked speculative in §4.1
- [x] Munda substrate readings — marked "candidate" in §4.2

### F4. Language-Family Baseline Limitation
- [x] §4.4 Limitation 6: formal comparison against Proto-Munda and early Indo-Aryan explicitly flagged as not yet done

---

## G. OVERALL READINESS VERDICT

| Gate | Status |
|------|--------|
| Manuscript text | **READY** for friendly expert review |
| PDF renders cleanly | **READY** |
| Forbidden language | **CLEAR** |
| Core stats present | **CLEAR** |
| Draft caveats present | **CLEAR** |
| Repository private | **BLOCKING arXiv** — must be made public first |
| Minor reference gaps (Mitchell, §3.28 citations) | **BLOCKING arXiv** — add before posting |
| Holdat corpus unreleased | **NOTED** — caveat in place |

**VERDICT: READY FOR FRIENDLY EXPERT REVIEW.**  
**NOT YET READY FOR arXiv POSTING** (repository must be public; 5 missing reference entries must be added).

---

## H. MACHINE-READABLE JSON SUMMARY

```json
{
  "check_date": "2026-05-21",
  "branch": "preprint-last-mechanical-polish",
  "tex_file": "glossa-corpus/indus/preprint.tex",
  "pdf_artifact": "glossa-corpus/indus/preprint.pdf",
  "pdf_bytes": 105829,
  "compile_passes": 2,
  "compile_errors": 0,
  "compile_warnings": ["6 longtable width warnings (non-blocking)", "3 minor overfull hbox"],
  "forbidden_language_hits": 0,
  "stale_sign_hits": 0,
  "broken_arrow_hits": 0,
  "third_party_email_hits": 0,
  "required_stats": {
    "z_10_3": true,
    "perm_0_2000": true,
    "fish_0_140": true,
    "hm_161": true,
    "token_coverage_90_96": true,
    "seal_coverage_69_8": true
  },
  "sections_present": {
    "abstract": true,
    "introduction": true,
    "data_methods": true,
    "results": true,
    "discussion": true,
    "conclusion": true,
    "data_availability": true,
    "acknowledgments": true,
    "references": true,
    "appendix_a": true,
    "appendix_b": true,
    "appendix_c": true
  },
  "third_party_sources_in_supplementary": false,
  "martini_roif_in_supplementary": false,
  "draft_caveat_present": true,
  "holdat_corpus_caveat_present": true,
  "nair_2026_cited": true,
  "gating_issues": [
    "Repository is private — must be public before arXiv posting",
    "Mitchell (1986) mentioned in §3.19 but not in reference list",
    "Steinkeller (1982), Potts (1994), Reade (2001), Kjaerum (1983), Parpola (1975) in §3.28 text but not in reference list"
  ],
  "verdict": {
    "friendly_review_ready": true,
    "arxiv_ready": false,
    "arxiv_blocking_reasons": [
      "Repository not yet public",
      "5 missing reference list entries"
    ]
  }
}
```
