# Addendum to Preprint v4 — Post–Phase-107/108 Headline Re-Base

> **DRAFT — NOT SUBMITTED.** This addendum was drafted in-repo on
> 2026-10-06 as part of Phase-109 (spec
> `specs/007-phase109-follow-through/`) at the direction of the
> author. It has **not** been submitted to Zenodo, SSRN, or any
> other venue, and it does not modify the published v4 preprint
> (`pierson_2026_indus_decipherment_preprint_v4.pdf`, DOI
> 10.5281/zenodo.20414696), which remains the citation of record.
> It records what a v5 revision would state, and the exact edits
> that revision would require.

**Parent document:** Pierson, T.K. (2026). *A Falsifiable
Computational Decipherment Hypothesis for the Indus Valley
Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot
Positional Grammar.* Preprint v4, Zenodo.
DOI: 10.5281/zenodo.20414696. SSRN submission ID 6827038.

---

## 1. Why this addendum exists

Three results obtained after v4 was published change the
evidential basis of the preprint's headline numbers:

1. **Phase-107 — the SA validation failed its falsification
   test.** The project's simulated-annealing (SA) machinery —
   historically the source of many anchor readings and of the
   "SA agrees 55%"-style support claims — was subjected to a
   pre-registered held-out test (spec 005). Under every lever
   (constraint terms removed, corpus pooled +32%, a 10× scaled
   run), held-out anchor agreement was **0.000** (0/115 folds;
   0/275 stability-supported signs at scale). Controls were
   non-discriminating: a Sanskrit language model (z=60.87) and a
   scrambled null (z=16.48) also recovered 0.000 held-out. The SA
   objective therefore carries no information about sign values,
   and no SA-derived or SA-confirmed reading can be cited as
   evidenced by SA. (Artifacts: `reports/phase107_*.json`,
   `reports/phase107_sa_validation_summary.md`.)
2. **Phase-108 — provenance audit of all 287 anchors.** Each
   anchor's chain of custody was classified from in-repo records.
   Headline findings: **210/287 anchors are strictly SA-free**;
   **44 HIGH anchors are SA load-bearing** (24 SA_DERIVED + 20
   SA_CONFIRMED_ONLY); and a **116-anchor cohort** traced to
   research-loop heuristic tables (bulk gloss assignments)
   promoted in June 2026 through an endpoint named
   `/staging/verify-sa` that performs no SA test. (Artifacts:
   `reports/phase108_provenance_summary.md`,
   `reports/phase108_provenance_register.json`,
   `reports/phase108_impact_map.json`.)
3. **Phase-109 — follow-through (this package).** Under
   pre-registered rules (spec 007): the 116-anchor staging cohort
   was re-reviewed — **112 prior sourced readings restored**
   (109 `kur`/LOW from Phase-111 allograph resolution; M042
   `vaN`, M046 `kaL`, M108 `kaL` at HIGH from Phase-89 DEDR),
   **1 kept** on independent Parpola crosswalk support (M222),
   **3 demoted** (H003; M231, M252 — whose overwritten priors
   were themselves SA-modal readings). The 44 SA-lineage HIGH
   anchors were flagged `validation_status:
   pending_non_sa_validation` (values and tiers unchanged).
   M293 `ta`, M362 `aṇi`, and M398 `kuṟi` were individually
   re-reviewed and each set HIGH → MEDIUM (M293: the Phase-101
   adjudication's own outcome, its HIGH having rested on an
   SA-only recalibration gate; M362/M398: the latest adjudication,
   Phase-105, is INCONCLUSIVE and was never superseded). A new
   governance rule (**H26**) prohibits SA-sufficient promotion
   gates, and promotion now requires a recorded non-SA evidence
   reference. (Artifacts: `reports/phase109_change_register.json`,
   `reports/phase109_step1_decisions.json`,
   `reports/phase109_dossier_M293.json` / `_M362.json` /
   `_M398.json`.)

## 2. Re-based headline numbers

Recomputed fresh on the post-Phase-109 anchor table with the
Phase-108 methods (`reports/phase109_rebase.json`):

| Quantity | v4 headline (retired) | Re-based (Phase-109) |
|---|---|---|
| Headline anchor set | 161 H+M (75 HIGH + 86 MEDIUM) | **94 strict SA-independent H+M (90 HIGH + 4 MEDIUM)** |
| Token coverage (Holdat, 7,002 tokens) | 90.96% (of the 161 set) | **73.68% (5,159/7,002)** for the strict set; 92.19% (6,455/7,002) for the full post-review H+M set (171) |
| Parpola agreement | 59% (Phase-170-era, 44-sign set, 45.5% SA-lineage) | Crosswalk-v2.1 comparison on the strict set: 81/81 compared signs — **partially tautological** (identity-only crosswalk entries) and **not** a like-for-like replacement for the 59% figure; reported only with this caveat |
| Phonotactic violations | 0 (Phase-58/61) | 0 on both the strict set and the full H+M set |
| Grammar site-invariance | 90/90 (Phase-69/170 framing) | 65/65 tested signs (strict set); 90/90 (full H+M) — survives the re-base |
| SA-lineage HIGH anchors | not distinguished | 44 flagged `pending_non_sa_validation`, excluded from the strict set |

The full post-review anchor table holds 287 entries:
166 HIGH + 5 MEDIUM + 112 LOW + 4 CANDIDATE.

**Claims that stand unchanged:** the structural results that do
not depend on SA or on the retired anchor counts — the three-slot
positional grammar (z=10.3, 0/2000 permutations), the fish-sign
isolation test (0/140), the M267 genitive reclassification, and
the grammar's site-invariance — per the Phase-108 impact map's
per-claim assessment (`reports/phase108_impact_map.json`).

## 3. Exact edits a v5 revision would make

Per `docs/research/PREPRINT_VERSIONING.md` (the published v4
`.tex`/PDF are **not** edited by this draft):

1. **Title block / § heading (`.tex` line ~74):** the title's
   "161 Candidate Proto-Dravidian Anchors" becomes "94 Strictly
   SA-Independent Candidate Proto-Dravidian Anchors" (author to
   confirm final wording); the same change applies to the title
   as recorded in `docs/research/PREPRINT_VERSIONING.md` and
   `AGENTS.md` at bump time.
2. **Version line (`.tex` line ~81):** `Version: Preprint v4`
   → `Version: Preprint v5`; date line → `Date: May 2026
   (revised October 2026)`.
3. **Abstract / headline figures (`.tex` lines ~98, ~165, ~176,
   ~206, §3.1 table line ~317 and prose line ~323, and the
   remaining "161" occurrences — 21 in total):** replace the
   161 / 90.96% / 59% set with the re-based table in §2 above,
   including the Parpola caveat verbatim in substance.
4. **New section** summarising Phase-107 (SA falsification),
   Phase-108 (provenance audit), and Phase-109 (re-review,
   flags, H26), citing the in-repo artifacts.
5. **End-of-document line:** `\emph{End of Preprint v4}` →
   `\emph{End of Preprint v5}`.
6. **PDF rename:** `pierson_2026_indus_decipherment_preprint_
   v4.pdf` → `..._v5.pdf`; Zenodo new version + SSRN revision
   **only on the author's explicit instruction** — neither is
   authorised by this draft.

## 4. Status

Draft only. Prepared by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI. The
accompanying Phase-109 pull request is opened unmerged for the
author's review of all scientific changes recorded here.
