# METRIC_AUDIT.md — Preprint v2 Internal Consistency Audit

**Canonical values (Phase-133 corrected, Phase-170 verified):**

| Metric | Canonical Value | Source |
|---|---|---|
| H+M anchors | 161 (75 HIGH + 86 MEDIUM) | INDUS_FINAL_ANCHORS.json |
| PROVISIONAL_MEDIUM | 4 (M330, M165, M202, M198) | Phase-163/166 |
| LOW signs | 236 | INDUS_FINAL_ANCHORS.json |
| Token coverage (genuine) | 90.96% | Phase-133/170 |
| Seals fully covered (genuine) | 69.8% (1,165/1,670) | Phase-133 resolution |
| Foundation checks passing | 59 | foundation_check.py (Phases 1–170) |
| Irresolvable signs | 18 (M198 removed, M223 deduplicated) | Phase-166 |

---

## Global Occurrence Table

| Location (tex line) | Flagged Text | Problem | Corrected Text | Status |
|---|---|---|---|---|
| L65–67 (Title) | "268 Anchors, 96.2% Token Coverage" | Inflated pre-Phase-133 count | "161 H+M Anchors, 90.96% Token Coverage" | **FIXED in v1.tex** |
| L69 (Label) | `268-anchors-96.2-token-coverage` | LaTeX label contains stale metrics | Should be updated to match new title | COSMETIC — label not displayed |
| L82–86 (Abstract) | "268 sign anchors… 96.2% token coverage… 1,165/1,670 (69.8%)" | Abstract now contains 69.8% but still references prior 268 inflated count as context | Abstract correctly explains Phase-133 correction | **FIXED in v1.tex** |
| L247 (§2.2) | `MEDIUM (193 signs)` | Pre-Phase-133 count | `MEDIUM (86 signs)` | **FIXED in v1.tex** |
| L253 (§2.2) | `LOW (129 signs)` | Pre-Phase-133 count | `LOW (236 signs)` | **FIXED in v1.tex** |
| L308–310 (§3.1 table) | MEDIUM=193, LOW=129, H+M=268, 96.2% | All pre-Phase-133 | MEDIUM=86, LOW=236, H+M=161, 90.96% | **FIXED in v1.tex** |
| L314 (§3.1 prose) | "268 H+M anchors cover 6,733 of 7,002" | Stale calculation | "161 H+M (75 HIGH + 86 MEDIUM) cover 6,363 of 7,002… prior count of 268 included placeholders" | **FIXED in v1.tex** |
| L505 (§3.6 table) | `1,429 (85.6%)` fully decoded | Pre-Phase-133 count (included heuristic placeholders) | `1,165 (69.8%)` | **FIXED in v1.tex** |
| L506 (§3.6 table) | `241 (14.4%)` blocked | Complementary to 85.6% — also wrong | `505 (30.2%)` | **FIXED in v1.tex** |
| L585 (§3.9) | "The 30.9% undecoded ceiling" | Phase-133 gives 30.2% blocked; 30.9% is close but inconsistent | "The 30.2% not yet covered" | **FIXED in v1.tex** |
| L983–984 (§4.3 header) | "The 20 Irresolvable Signs" | M198 promoted to PROVISIONAL_MEDIUM; M223 was duplicated → 18 irresolvable | "The 18 Irresolvable Signs" | **FIXED in v1.tex** |
| L1005 (§4.4) | "the irresolvable 20" | Same | "the irresolvable 18" | **FIXED in v1.tex** |
| L1041–1042 (§5 Conclusion) | "268 sign anchors… 96.2% token coverage, 85.6% of seals" | All pre-Phase-133 inflated | "161 genuine sign anchors… 90.96%… 69.8% fully covered" | **FIXED in v1.tex** |
| L1048 (§5 Conclusion) | "The remaining 14.4% of seals" | Complement of 85.6% — wrong | "The remaining 30.2% of seals" | **FIXED in v1.tex** |
| L1189–1190 (Appendix B header) | "The 20 Irresolvable Signs" | Count wrong after Phase-166 | "The 18 Irresolvable Signs" | **FIXED in v1.tex** |
| L1195 (Appendix B prose) | "and 14.4% of undecoded seals" | Stale | Updated as part of Appendix B fix | **FIXED in v1.tex** |
| L1197–1198 (Appendix B list) | M198 listed as irresolvable; M223 listed twice | M198 = PROVISIONAL_MEDIUM (Phase-166); M223 duplicate | Remove M198, deduplicate M223 → 18 signs | **FIXED in v1.tex** |
| L1210 (Appendix C) | "45 independent checks" | Now 59 checks (Phases 1–170) | "59 independent checks (Phases 1–170)" | **FIXED in v1.tex** |
| L1125 (References) | `178--193` | Page range for Parpola 2010 — coincidental match to 193, NOT a sign count | Valid reference page range — no change needed | VALID |

---

## Remaining Warnings (not errors)

| Issue | Location | Action Required |
|---|---|---|
| LaTeX label `268-anchors-96.2` in section header | L69 | Cosmetic — does not affect compiled output; update in v2 |
| `96.2\%` appears in compiled LaTeX label string | L69 | LaTeX auto-generated from old section title; updating title (done) leaves label stale but harmless |
| §3.6 still references "+35 seals (Phase-128/129 net gain)" | L508 | Still valid historical annotation; retain but clarify it applies to the older counting methodology |
| `96.2%` removed from body but still in some compiled cross-references | L69 label | Will auto-resolve on xelatex compile once label is updated in v2 |

---

## Summary

**Fixed in v1.tex:** 17 occurrences across title, abstract, §2.2, §3.1 table, §3.6 table, §3.9, §4.3, §4.4, §5 conclusion, Appendix B, Appendix C.

**No action needed:** 2 (reference page range, LaTeX internal label).

**Canonical state after fixes:**
- Headline: 161 H+M (75 HIGH, 86 MEDIUM) + 4 PROVISIONAL_MEDIUM
- Coverage: 90.96% token, 69.8% seals (1,165/1,670)  
- Checks: 59/59
- Irresolvable list: 18 signs
