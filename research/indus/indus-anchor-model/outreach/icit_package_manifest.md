# ICIT Validation Package Manifest
## Materials to send with initial contact to ICIT/Fuls

Send these items as attachments to the initial email. Do NOT send the full project ZIP on first contact.

---

## Required items (7)

| # | File | Description |
|---|---|---|
| 1 | `docs/two_page_summary.md` (as PDF) | 2-page technical summary of the model and the ICIT ask |
| 2 | `data/public/anchor_table_397.csv` | All 397 Mahadevan signs with candidate readings and confidence tiers |
| 3 | `data/public/formula_bigrams.csv` | Top-30 directed H+M bigrams with counts and PMI |
| 4 | `docs/icit_validation_plan.md` (as PDF) | Full 8-test plan with falsification criteria and output specs |
| 5 | `manuscript/pierson_2026_indus_preprint.pdf` | Preprint PDF |
| 6 | GitHub repository link | https://github.com/BitConcepts/glossa-lab |
| 7 | Zenodo DOI | (to be generated — see Phase 6 instructions) |

---

## Do NOT send on first contact

- The full project ZIP
- The Holdat corpus data (it is not ours to share)
- Detailed requests for Fuls's unpublished data
- Claims of decipherment or language-family proof

---

## Narrow ask in the email

The first email should ask only:

> Is a Mahadevan-to-ICIT crosswalk already available, and is there a preferred format for running corpus-level positional and bigram tests on ICIT?

A partial crosswalk covering the top-50 signs by frequency is sufficient for Tests T1–T3. The full 161-anchor crosswalk would be required for the complete validation suite (Tests T1–T8).

---

## Follow-up (7–10 days after first email, if no reply)

Send a brief follow-up with only items 1 and 2 (two-page summary + anchor table). Ask only the narrow crosswalk question. Do not resend the full package.

---

## After crosswalk agreement

If Fuls or the ICIT team agrees to advise on the crosswalk:
- Send scripts from `scripts/` along with input schema docs
- Confirm which ICIT export format their system produces
- Run Tests T1–T3 first; report back before proceeding to T4–T8
