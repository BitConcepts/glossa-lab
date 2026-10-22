# Spec 024 — Stage 2(c) Freeze Record (Phase-137)

> ## FROZEN 2026-10-09 — test (c), site repertoire differentiation
>
> Frozen under spec 024 §5 / §12 on the owner's
> instruction of record: **Tristen Pierson,
> 2026-10-09 — "Do all next things"** (arm (b) is
> CLOSED per `motif-arm-closure.md` and is not
> touched). This freeze is committed and merged
> **before** any Phase-137 analysis code runs. It
> operationalizes the §5.4 sketch on the Phase-133
> Stage 0 numbers, under the family declaration of
> `stage2a-freeze.md` §1 (this test contributes
> family members **F2** and **F3**). It narrows
> the sketch for feasibility in the places stated
> and widens it nowhere.

**Phase:** 137 · **Spec:** 024 §5.4 (test (c)) ·
**Family roles:** **F2** (Holdat layer), **F3**
(ICIT-lineage layer) · **Date:** 2026-10-09.

**AI disclosure:** this freeze, and the execution
it governs, are produced by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

---

## 0. Recorded interpretation — the text substrate

The substrate interpretation recorded in
`stage2a-freeze.md` §0 is incorporated verbatim:
the layers' sign sequences (Holdat `letters`
ordered by `position`; the ICIT-lineage layer's
`text` parsed by the established convention) are
used only as the text substrate — the inscriptions
themselves — never as context evidence. Context
and control variables come from Class O fields
only (`site` in both layers; `type` in the
ICIT-lineage layer). Every Class I interpretive
field listed in `stage2a-freeze.md` §0 enters
nothing at all.

## 1. Question and falsifier (spec §5.4, restated)

**Question.** Do per-site sign-frequency profiles
(repertoires) differ across sites **beyond what
the sites' different composition explains** —
composition being object-type mix and text-length
mix, the standing confounders of spec §5.1,
controlled by permutation within composition
strata? Each layer is tested **separately, on its
own sign list, and is never pooled with the other**
(the layers' transcriptions are different
compilations' work; a pooled table would test the
compilations, not the sites).

**Falsifier (the null, stated in advance).** If a
layer's differentiation does not exceed the
composition-controlled permutation null at the
family threshold (BH-adjusted q > 0.05 in the
combined report), site "dialects" of the
repertoire are recorded for that layer as **NOT
SUPPORTED — an artifact of what each site happens
to preserve, not a finding** (§5.4). Phase-131's
composition share (6.1%, with 93.9% of its
positional disagreement unexplained) is the
standing warning that composition effects here are
real but small; this test measures repertoire
composition directly rather than positional
profiles.

## 2. Common design (frozen for both layers)

- **Unit:** the inscription. Site labels are
  permuted at inscription level; each inscription
  carries its full token multiset with it (tokens
  within an inscription are never treated as
  independent units).
- **Profile table:** site × sign token counts,
  aggregated over the layer's analysis population.
  Sign columns: signs whose layer-wide token count
  **within the analysis population** is ≥ 10;
  rarer signs are pooled into a single `OTHER`
  column (the only collapse; pre-declared here per
  §5.1). Placeholder / identity-less tokens are
  excluded from profiles entirely (they carry no
  sign identity): in the ICIT-lineage layer, codes
  `000` / `999` (the lineage adapter's PLACEHOLDERS,
  Phase-115); in Holdat there are none.
- **Statistic:** Pearson chi-square of the profile
  table, Σ (O − E)² / E with E from the table's
  margins — used as a divergence statistic only;
  all inference is by permutation (no asymptotic
  approximation is used or reported as a result).
- **Composition control:** site labels are
  shuffled **within composition strata only**
  (layer-specific strata, §3–§4), so every
  permutation preserves each stratum's site mix
  exactly: object-type mix and text-length mix are
  held fixed by construction.
- **Permutation parameters:** family parameters of
  `stage2a-freeze.md` §1 (B = 9,999; seed 20261009;
  p = (1 + #{χ²_perm ≥ χ²_obs}) / (1 + B)).
- **Effect sizes:** Cramér's V of the observed
  table (descriptive, labeled as such); the
  observed statistic against the permutation
  distribution (median and 95th percentile);
  per-site total-variation distance between the
  site's profile and the pooled profile
  (descriptive, all sites shown — no selection).
- **Site inclusion rule (uniform, both layers):**
  a site enters iff, in the layer's parsed
  population, it has **≥ 30 inscriptions and
  ≥ 100 tokens**. Sites failing the rule are
  excluded and counted, by name, in the report.
  (`Unknown` is a missing-value label, not a site;
  it fails the rule in any case and is named as
  excluded where it occurs.)

## 3. Estimability rule (frozen; a stated substitution for the §5.1 default)

Spec §5.1's default minimum-cell rule (expected
count ≥ 5 in ≥ 80% of cells) guards **asymptotic**
chi-square inference. This test's inference is
permutation-based and uses no asymptotic
approximation, so the freeze substitutes the rule
that matches the inferential basis, and states the
substitution openly rather than letting the default
silently veto a permutation test it was not written
for: a layer's test **executes** iff (i) ≥ 2 sites
pass the §2 inclusion rule, and (ii) the profile
table has ≥ 2 sign columns after the §2 collapse.
**Mandatory sparsity disclosure (not optional):**
the executed report states the share of profile
table cells with expected count < 5, the minimum
expected count, and the per-site token counts, so
any reader can see the table's sparsity. If (i) or
(ii) fails → **NOT ESTIMABLE**, counts shown, no
p-value, the family member contributes nothing to
the BH correction.

## 4. Holdat subdesign (family member F2)

- **Population:** all **1,670** inscriptions
  (token rows grouped by `seal_id`; tokens ordered
  by `position`; sign identity = `letters` M-code
  as recorded, substrate per §0). No exclusions at
  audit: every inscription has 2–8 tokens.
- **Sites:** all **9** pass the §2 rule (audit:
  Mohenjo-daro 606 insc / 2,534 tok; Harappa 492 /
  2,079; Lothal 124 / 507; Kalibangan 110 / 485;
  Dholavira 106 / 439; Chanhu-daro 78 / 310;
  Banawali 60 / 255; Surkotada 61 / 257;
  Rakhigarhi 33 / 136).
- **Sign space:** the layer's native Mahadevan
  numbers (audit: 390 distinct over 7,002 tokens).
- **Composition strata:** inscription length class
  only — {2–3, 4–5, 6–8 tokens} (audit counts
  599 / 745 / 326). **Object-type control
  degenerates, stated plainly:** the layer carries
  no object-type field and its inscriptions are
  seal texts (`form` = `seal_NNNN` throughout), so
  the type mix is a constant and the length control
  is the only composition control this layer
  admits. This is a property of the layer, recorded
  here — not patched by importing a type from
  another layer (no audited join exists, Phase-133
  §3.3–3.4).
- **Headline label:** Holdat compilation layer —
  the layer is named in every output; its
  transcription is one compilation's work and the
  result describes that layer's recorded
  repertoires.

## 5. ICIT-lineage subdesign (family member F3)

- **Population:** inscriptions at §2-eligible
  sites with ≥ 1 parsed token. Audit-eligible
  sites (**7**): Harappa 2,717 insc / 7,975 tok;
  Mohenjo-daro 1,923 / 8,330; Dholavira 238 / 808;
  Kalibangan 212 / 624; Lothal 208 / 818;
  Chanhu-daro 74 / 352; Nausharo 38 / 144
  (5,410 inscriptions). All 5,679 rows parse to
  ≥ 1 code under the established convention
  (`re.findall(r"\d{3}", text)`, Phase-115).
- **Sign space:** the layer's native Wells/ICIT
  codes as parsed (audit: 713 distinct
  non-placeholder codes over 18,047
  non-placeholder tokens in the full layer). No
  crosswalk to P space is applied: the test is
  within-layer, and the native list is the
  repertoire the layer itself records. (Arm (a)'s
  P-space mapping exists for its own frozen
  purpose and is not reused here.)
- **Composition strata:** object-type class ×
  length class. Type class from the layer's
  `type` field (Class O), prefix before `:` —
  {SEAL, TAB, POT, OTHER}, where OTHER pools the
  remaining recorded prefixes {TAG, MISC, BNGL,
  ROD, IMPL, BEAD, MDLN, Unknown} (audit full-layer
  counts: SEAL 2,290; TAB 2,290; POT 636; OTHER
  463 — the only type collapse, pre-declared
  here). Length class {1, 2–3, 4–5, 6+} parsed
  tokens (audit: 698 / 2,564 / 1,532 / 885).
  Strata are formed on the analysis population;
  a stratum whose members all share one site
  contributes a constant to every permutation and
  is harmless by construction.
- **Headline label:** ICIT-lineage layer —
  **mandatory in the headline of every output**,
  per spec §2.4 / §5.1: the layer is a derivative
  of the ICIT database in open file form, not an
  independent witness, and its results describe
  this layer, not the Indus corpus in general.

## 6. Assumptions and epistemic boundaries (H13)

- **Assumptions:** (B1) an inscription's site in
  each layer is its findspot as recorded by the
  compilation (Class O); transcription and
  findspot errors are the layers' own and are not
  corrected. (B2) Composition strata as frozen
  capture the confounders §5.1 names (type mix,
  length mix); other confounders (period,
  preservation, excavation history) are not
  available in these layers and are **not**
  controlled — the report must say so wherever a
  positive result is stated. (B3) The two layers
  are tested independently; agreement or
  disagreement between F2 and F3 is reported
  descriptively in the combined report and is not
  itself a test.
- **Boundaries:** spec §8 governs verbatim.
  Repertoire differentiation, if found, is a fact
  about the recorded distribution of sign use
  across sites in a named layer — it is not
  evidence for regional "dialects" as linguistic
  entities beyond that statement, for any reading,
  or for any anchor or PRED movement.

## 7. Deliverables (Phase-137)

Per governance H15/H23 (graph-first, 5-step gate):
script `backend/scripts/phase137_site_repertoire.py`
(both layer subdesigns, one run); graph module
`backend/glossa_lab/experiment_graph_phase137.py`
(node `IndusPhase137SiteRepertoire`), registered
and verified before the run; tests
`backend/tests/test_phase137_site_repertoire.py`;
results `reports/phase137_results.json`; report
`reports/phase137_report.md` (both layers, each
under its own headline label). Foundation check
(H21): 0 failures. Anchors asserted byte-identical
(sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`).

## 8. Deviations

None at freeze. Execution deviations, if any, are
recorded in the phase report with the rule that
resolved them.
