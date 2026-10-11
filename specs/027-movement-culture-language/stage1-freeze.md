# Spec 027 — Stage 1 Freeze Record (Phase-392, Q2 repertoire gate)

> ## FROZEN at the Stage 1 freeze merge (2026-10-11)
>
> Basis: Spec 027 as frozen 2026-10-11 (PR #147) with the
> owner's adjudication (`adjudication.md`): Ask 2 → **M77 governs**;
> Ask 3 → corpus rules approved as drafted; Ask 5 →
> Stage 1 executes on the adjudicated design once this freeze
> is committed and merged. Stage 0 (Phase-391) is complete
> (PR #151). This record pins every Stage 1 quantity BEFORE
> any repertoire outcome is computed. The margins it relies on
> come from the margins-only audit
> (`stage1/margins-audit.json`, produced by
> `stage1/build_margins_audit.py`); the audit computes no
> site-by-sign association, divergence, or permutation
> statistic, and a test pins the absence of outcome fields.
> The machine freeze record is `stage1-freeze.json`
> (framework026 digest).

## 1. Bounded claim and estimand (spec §7.1, §7.3)

**Claim (bounded):** in the named corpus below, under M77,
after rarefaction to a common cell size and stratification by
object type, site explains more recorded sign-repertoire
variation than expected under permuted site labels, at the
declared practical margin. The claim is about *recorded
repertoires in this corpus*; it is not a claim about dialects,
languages, ethnic groups, political units, or workshops as
peoples (spec §7.1).

- **Response:** per-inscription sign composition (proportions
  over the frozen sign columns) under **M77**.
- **Grouping:** site (6 analysis sites, §3).
- **Distance:** Bray–Curtis on proportions.
- **Estimand:** PERMANOVA R² for site, rarefaction-averaged
  (§4).
- **Practical margin:** R² = **0.01**. Declared convention
  (spec §12): a site share of repertoire dispersion below 1%
  is not a regional repertoire pattern for program purposes.
  A p-value alone cannot produce SUPPORTED (§7.3).

## 2. Corpus (Ask 2 + Ask 3, operationalised)

- **Substrate:** the program's M77-keyed layer,
  `icit_converted_v2_keyed.json` (sha256
  `bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8`),
  built by the Phase-115/116 layer build from the ICIT-lineage
  export — ICIT/Wells codes converted to M-signs via the
  canonical registry + crosswalk chain, with per-token
  provenance (`direct` / `chain` / `unmapped` / `placeholder`)
  and dedup status per record. This layer **is** the named
  program deduplication artifact for Ask 3: its `status`
  field already applies the program dedup (intra-corpus exact
  duplicates and Holdat-corpus duplicates removed as records;
  duplicate *texts* on distinct objects retained as distinct
  objects, per the build's recorded rules).
- **Metadata join:** horus84 `inscriptions.csv` (sha256
  `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`,
  the Spec 025 frozen layer file) joined on `id` for
  completeness/preservation fields. Audit: 5,678 of 5,679
  records join; site agreement 5,678/5,678 joined. The one
  unjoined record (id `2294.1`) carries UNRECORDED metadata
  and is retained with that flag.
- **Token rules:** `sign_list_version` = **M77** on every
  record. Composition tokens = kinds `direct` + `chain`
  (mapped M-signs) + `unmapped` pooled into the single
  **UNMAPPED** column (Ask 3's frozen pooling rule).
  `placeholder` positions (ICIT `000`, illegible) are **not
  signs**: excluded from composition, counted as a per-object
  damage flag.
- **Legible-token rule (Ask 3):** an object is eligible only
  if its legible-token count (direct + chain + unmapped) is
  **≥ 2**. Flags (placeholder count, completeness,
  preservation) are retained on every record.
- **Multi-line note (Ask 3):** the ICIT-lineage layer records
  no line-structure field, so multi-line status cannot be
  flagged from this substrate; eligibility is governed solely
  by the legible-token rule. This is a stated boundary of the
  bounded claim (recorded repertoires *as recorded in this
  layer*), not a silent omission.
- **Object inclusion (Ask 3):** provenanced records only —
  site present and not the recorded value `Unknown`
  (26 records excluded by the audit under this rule);
  object classes **SEAL + TAB** in the primary test (type
  class = prefix of the layer `type` field, the Phase-137
  convention). Pottery is excluded from the primary test;
  pottery graffiti (`POT:T:g`, 473 kept records) is excluded
  from **every** Stage 1 population (never pooled — Ask 3);
  non-graffiti pottery is likewise outside the primary test
  and is not run as a sensitivity in this freeze.

## 3. Populations (from the margins audit; execution must reproduce exactly)

Flow: 5,679 layer records → dedup-kept 4,531 → site-`Unknown`
excluded 26 → provenanced 4,505 → SEAL/TAB 3,605 → legible
≥ 2 → **eligible 3,144** (52 sites).

**Analysis population:** eligible records at sites with
≥ 20 eligible inscriptions — 6 sites, **3,030 inscriptions**:

| Site | SEAL | TAB | Total |
|---|---|---|---|
| Harappa | 361 | 1,076 | 1,437 |
| Mohenjo-daro | 1,138 | 164 | 1,302 |
| Dholavira | 96 | 15 | 111 |
| Lothal | 72 | 2 | 74 |
| Chanhu-daro | 52 | 2 | 54 |
| Kalibangan | 49 | 3 | 52 |

Eligible-but-not-analysis records (small sites) are reported
in the execution flow and excluded from the test; they are
not pooled into a composite "other" site.

**Sign columns:** M-signs with ≥ 10 mapped tokens in the
eligible population (123 signs per the audit) + `UNMAPPED` +
`OTHER` (mapped signs below 10 pooled) = 125 columns.

## 4. Frozen statistics

- **Rarefaction:** within each site × type-class cell of the
  analysis population, sample without replacement to the
  common cell size **n_cell = 15** (the largest size keeping
  ≥ 10 cells; cells below 15 are excluded from the rarefied
  population and reported: Lothal TAB 2, Chanhu-daro TAB 2,
  Kalibangan TAB 3). Included cells (10): Harappa SEAL/TAB,
  Mohenjo-daro SEAL/TAB, Dholavira SEAL/TAB, Lothal SEAL,
  Chanhu-daro SEAL, Kalibangan SEAL → 150 inscriptions per
  draw. **R = 199 draws.**
- **Per draw:** Bray–Curtis PERMANOVA for site on the
  rarefied inscriptions' proportions; permutation p from
  **B = 499** permutations of site labels **within type-class
  strata** (labels exchangeable only within a stratum);
  p = (1 + #{F_perm ≥ F_obs}) / (1 + B).
- **Summaries:** draw-level R² distribution → median R² and
  percentile interval [2.5%, 97.5%]; share of draws with
  p ≤ 0.05.
- **Seed:** `20261011` for rarefaction, permutation, controls,
  and jackknife (one seed, named here so no later choice
  exists). α = 0.05.
- **Jackknife:** leave-one-site-out over the 6 analysis
  sites; per dropped site, the rarefaction-averaged median
  R² recomputed identically (no permutation). Reported as a
  range.
- **Sensitivity (labelled, no verdict):** S-complete —
  exclude records whose joined `complete` field is `N`;
  recompute median R² and the share of draws rejecting.
  Period is **not** a stratum or sensitivity: the layer's
  period field is 59.2% uninformative (Phase-139 audit of
  this layer), recorded here as a limitation of the bounded
  claim. Inscription length enters through proportions
  (composition is length-normalised by construction); no
  length-class stratum is used, per spec §7.3's "where the
  frozen design states it" — this freeze states it is not
  used, with that reason.

## 5. Discriminating controls (spec §7.5; failure = INVALID)

Both controls run the **identical** pipeline (same cells,
rarefaction, PERMANOVA, permutation, summaries) on synthetic
populations with the analysis population's cell sizes and
per-inscription legible lengths:

- **Negative control:** each synthetic inscription's tokens
  drawn from the pooled eligible composition (no site
  structure). PASS iff its median R² < 0.01 **and** ≥ 95% of
  its draws have p > 0.05.
- **Positive control:** each site's composition = pooled
  composition perturbed toward a site-specific set of 10
  signs (probability × 3, renormalised; sets drawn with the
  frozen seed), calibrated to a true site R² of roughly
  2–3× the margin. PASS iff ≥ 95% of its draws have p ≤ 0.05
  **and** its R² interval lies entirely above 0.01.

If either control fails, the run is **INVALID** (the
instrument cannot discriminate at the declared margin), the
verdict is recorded as INVALID, and no primary verdict is
issued from the primary numbers.

## 6. Verdict rules (spec §7.6, operationalised)

Population reproduction is a precondition: if the executed
population differs from §3's frozen margins in any count, the
run is INVALID (population not reproduced) and stops.

- **SUPPORTED** iff controls pass AND ≥ 95% of primary draws
  reject (p ≤ 0.05) AND the R² percentile interval lies
  entirely above 0.01 AND every LOSO median R² > 0.01.
- **CONTRADICTED** iff controls pass AND (≥ 95% of primary
  draws fail to reject OR the R² percentile interval lies
  entirely at or below 0.01). The bounded claim is defeated;
  spec §7.2's negative closure applies automatically: all
  downstream repertoire-geography work under Spec 027 stops.
- **INCONCLUSIVE** iff controls pass and neither rule fires
  (including a jackknife range crossing the margin while the
  primary interval does not).
- **INVALID** iff a control fails, the population is not
  reproduced, or a frozen rule was changed after outcome
  inspection.

No outcome identifies a dialect or a language (§7.6).

## 7. Parpola/CISI sensitivity — assessed on margins, NOT ESTIMABLE

Ask 2 permits Parpola/CISI only as a separately labelled
sensitivity with a sign-by-sign crosswalk rule. The frozen
rule for any such sensitivity is: map only tokens whose M
sign has **exactly one** high-confidence P partner in
crosswalk v1 (`data/crosswalks/parpola_mahadevan_crosswalk_v1.csv`,
sha256 `3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823`)
with no conflict flag on the pair. The margins audit measures
that coverage at **17.57%** of mapped tokens (any-high-
confidence coverage is 99.94%, but the pairs are dominated by
many-to-many and conflict-flagged mappings that the rule may
not silently resolve). At 17.57% coverage the sensitivity
cannot carry the §1 estimand on a comparable population.
**Recorded at this freeze, before any outcome: the Parpola
sensitivity is NOT ESTIMABLE under the frozen rule and is not
run.** This is a margins determination, not a result.

## 8. Execution shape

- Phase-392 script + graph node (H23 order: script → graph
  module addition → registration → verification → run).
- Outputs: `reports/phase392_results.json`,
  `reports/phase392_report.md`; outcome + closure record in
  `stage1-outcome.md`; ledgers appended.
- No anchor or PRED contact (FR-027-15). If the result
  appears to bear on an anchor, it is recorded as a
  historical assessment and flagged for owner adjudication —
  never actioned here.
