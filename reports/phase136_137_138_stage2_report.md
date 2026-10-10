# Phases 136–138 — Spec 024 Stage 2 Combined Report

**Spec:** 024 — Evidence Integration, Stage 2 (spec
§5). **Arms executed:** (a) terminal-class × object
type (Phase-136), (c) site repertoire
differentiation (Phase-137, two layers), (d)
graffiti descriptive protocol (Phase-138). **Arm
(b) was not touched** — it is CLOSED as run per
`specs/024-evidence-integration/motif-arm-closure.md`.
**Owner instruction of record:** Tristen Pierson,
2026-10-09 — "Do all next things". **Freezes**
(each committed and merged before its arm's code
ran): `stage2a-freeze.md` (PR #117, merge
`8a8a106a`), `stage2c-freeze.md` (PR #118, merge
`9484f54d`), `stage2d-freeze.md` (PR #119, merge
`ad665b05`). **Executions:** Phase-136 PR #121
(merge `e7d17f6a`); Phase-137 PR #122 (merge
`75943a7f`); Phase-138 PR #120 (merge `4069bcb1`)
with corrective PR #123 (merge `1c2a5fd2`, §7).
**Date:** 2026-10-09.

**AI disclosure:** Stage 2 was executed by AI
agents (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI. Every quantity below is computed by script
from the data files and recorded in the phase
results JSONs; nothing is copied from a worker's
self-report.

**Scope, stated once and binding (spec §8):**
associations describe **use, not meaning**. No
result in this report can mint, promote, demote,
or validate any sign reading, change any anchor's
status, or move PRED-2026 in either direction
(spec §7). Anchors are byte-identical throughout
(sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`,
asserted in every phase's tests). Hypotheses these
findings suggest are **hypothesis-grade**; they
enter the program's ordinary queue and acquire no
informal credibility by being reported here.

---

## 1. The declared family and its correction (spec §5.1)

The family declared in `stage2a-freeze.md` §1 has
exactly three members. All three executed and were
estimable under their frozen rules, so the
Benjamini–Hochberg correction at **q = 0.05** is
applied across all three raw p-values, once, here:

| Member | Test | Raw p | BH q | Verdict |
|---|---|---:|---:|---|
| **F1** | Terminal-class × object type, within-site stratified permutation (ICIT-lineage layer) | 0.0001 | 0.00015 | **SUPPORTED** |
| **F2** | Site repertoire differentiation, composition-controlled permutation (Holdat layer) | 0.7354 | 0.7354 | **NOT SUPPORTED** |
| **F3** | Site repertoire differentiation, composition-controlled permutation (ICIT-lineage layer) | 0.0001 | 0.00015 | **SUPPORTED** |

(BH computation, m = 3: sorted p (0.0001, 0.0001,
0.7354) → q-values (0.00015, 0.00015, 0.7354) by
the standard step-up rule; both small p-values are
the minimum the frozen formula returns at
B = 9,999 permutations — 0 of 9,999 permutations
reached the observed statistic in each case.)
Arm (d) computed no test and is not a family
member. Nothing outside this family was tested;
all other quantities in the phase reports are the
freezes' pre-declared descriptive outputs.

## 2. F1 — Terminal-class × object type (ICIT-lineage layer; Phase-136)

*Headline label: ICIT-lineage derivative layer —
not an independent witness; results describe this
layer's joined subset, not the Indus corpus in
general.*

**Flow as run** (freeze §3; every audit number
reproduced, no drift): 5,679 layer rows → 2,895
joined by the audited exact-string key (2
ambiguous, 2,782 unmatched; 49.0% of the layer is
unjoinable or ambiguous and is excluded) → 2,752
with a catalogue object type → 2,676 in the
pre-declared {Seals, Tablets} restriction
(Graffiti 69 and Objects 7 excluded, boundary 4) →
2,195 with a mapped terminal sign (481
UNK-terminal excluded) → **2,062** in the three
eligible site strata (Mohenjo-daro, Harappa,
Kalibangan).

**Result as found.** Observed CMH statistic
**47.0047** against a permutation distribution
with median 0.455 and 95th percentile 3.991; raw
p = **0.0001**. Mantel–Haenszel common odds ratio
**2.384** (95% CI 1.847–3.077): within sites, a
seal's terminal sign is substantially more likely
to belong to the frozen TERMINAL class than a
tablet's. Observed TERMINAL shares — Mohenjo-daro:
seals 30.0% (258/859) vs tablets 16.4% (48/292);
Harappa: 24.6% (69/281) vs 10.5% (61/579);
Kalibangan: 12.5% (5/40) vs 9.1% (1/11); pooled
eligible: seals 28.1%, tablets 12.5%. The crude
(uncontrolled) OR is 2.748 — the within-site
control attenuates the association but does not
remove it. **Verdict: SUPPORTED** (family q =
0.00015) — the functional-split hypothesis for
terminal signs is supported on this data: in this
layer, closing-sign behaviour differs by object
class, within sites.

**Standing caveat (from the freeze, §7):** the
strongest alternative explanation is
compilation-internal — the lineage's transcriptions
and the catalogue's object typing were both made
within one scholarly tradition — so this is a
finding about the recorded layer's organization of
use, stated with its lineage label, and nothing
more. It is not a PRED-2026 evaluation in either
direction (freeze §2).

## 3. F2 — Site repertoire differentiation, Holdat layer (Phase-137)

**Population as run:** all 1,670 inscriptions; all
9 sites eligible under the frozen rule; strata =
length class only (the layer has no object-type
field; the type control degenerates, as the freeze
states). Profile table 9 × 98 (97 signs with
layer-wide count ≥ 10 plus OTHER = 911 tokens,
13.01% of 7,002). Sparsity, as mandated: 607/882
cells (68.8%) with expected count < 5; minimum
expected 0.214.

**Result as found.** Observed χ² = **745.95** —
**below** its own composition-controlled
permutation median (770.32; 95th percentile
838.45); 7,353 of 9,999 permutations reached or
exceeded it; raw p = **0.7354**. Cramér's V
(descriptive) 0.1154. **Verdict: NOT SUPPORTED**
(family q = 0.7354). Per the §5.4 falsifier, stated
in advance: site repertoire differentiation in the
Holdat layer does not exceed what length
composition explains — on this layer, per-site
"dialects" of the repertoire are recorded as an
artifact of what each site happens to preserve,
not a finding. The null stands as found; the
observed statistic sitting below the null median
is reported as a description of the permutation
distribution, not as evidence of
anti-differentiation.

## 4. F3 — Site repertoire differentiation, ICIT-lineage layer (Phase-137)

*Headline label: ICIT-lineage derivative layer —
not an independent witness; results describe this
layer, not the Indus corpus in general.*

**Population as run:** 5,410 inscriptions at the 7
eligible sites (Harappa, Mohenjo-daro, Dholavira,
Kalibangan, Lothal, Chanhu-daro, Nausharo; 70 site
labels excluded under the frozen rule and named in
the phase report, including `Unknown`). Strata =
type class × length class (16). Profile table
7 × 187 (186 signs ≥ 10 plus OTHER = 1,387 tokens,
8.04% of 17,257 profile tokens). Sparsity:
887/1,309 cells (67.8%) expected < 5; minimum
expected 0.075.

**Result as found.** Observed χ² = **4,966.36**
against a permutation median of 2,667.87 (95th
percentile 2,844.61); 0 of 9,999 permutations
reached it; raw p = **0.0001**. Cramér's V
(descriptive) 0.2190. **Verdict: SUPPORTED**
(family q = 0.00015) — in this layer, per-site sign
repertoires differ beyond what object-type mix and
text-length mix explain.

**Mandatory confounder statement (freeze §6 B2):**
period, preservation, and excavation history are
not available in this layer and are **not**
controlled; a positive result here is a statement
about the layer's recorded distributions, with
those confounders open. **Cross-layer note
(freeze §6 B3):** F2's null and F3's positive are
reported side by side descriptively; their
contrast is not itself a test. The two layers are
different compilations with different site records
and different sign lists — the contrast describes
the layers; it does not adjudicate the sites.

## 5. Arm (d) — Graffiti, descriptive only (Phase-138)

Population as run: **417 catalogue photo rows over
395 distinct objects** (Vol. 1: 119 rows / 100
objects; Vol. 2: 298 / 295), exactly the freeze
§1 audit. Headline descriptives, as found:

- **Objects by site:** Harappa 262, Lothal 44,
  Mohenjo-Daro 42, Kalibangan 26, no site recorded
  8, the remainder across smaller sites — the
  graffiti subset's catalogue centre of mass is
  Harappa, the reverse of the seal/tablet mass.
  (The catalogue is a publication selection, not
  the excavated population; freeze §5 D2.)
- **Photo rows per object:** mode 1 — 374 of 395
  objects carry a single photographed side/view.
- **`motif_chapter` filled on 0 of 417 rows
  (0.0%)**: the CISI editors' chapter organization
  assigns no depiction chapter to any graffiti row,
  against 26.0% of catalogue rows overall. The
  graffiti subset carries no depiction coding in
  the catalogue at all.
- `caption_ocr_score` median 0.943 (IQR 0.029) —
  the catalogue's extraction quality on this subset
  matches the corpus norm.

**Comparative strand (qualitative only):** the
Kodumanal volume's Graffiti Marks section
describes marks by ware and vessel position in a
trench-organized excavation report; its printed
tallies are internally inconsistent (subtotals
summing to 225 against a stated 175) and are used
as no counts. The Tamil Nadu graffiti corpus is
**not in hand — 0 records** (access requested
2026-10-08; no reply on record). **Dating-gap
caveat:** that material is separated from the
Indus material by ≥ 1,000 years on the published
rebuttal of the continuity claims; any resemblance
is formal resemblance across a millennium-plus
gap. No overlap statistic against the seal-text
repertoire was computed — no machine-readable
sign-form repertoire of the catalogue graffiti
objects exists in hand (freeze §4) — and no
continuity, descent, or survival claim is made or
implied. No test of any kind was computed in this
arm.

## 6. What Stage 2 leaves standing

- A measured, controlled association (F1) between
  closing-sign class and object class in one
  labeled lineage layer — a Tier-(ii) fact about
  the writing system's functional organization as
  recorded there, and a hypothesis-grade pointer
  for future work on genuinely independent data.
- A disciplined split outcome on site repertoires
  (F2 null, F3 positive): site differentiation is
  **not** a layer-free fact; it appears in the
  ICIT-lineage record beyond composition controls
  and does not appear in the Holdat record beyond
  its (length-only) control. Both halves are
  reported with their layers named.
- A complete descriptive record of the catalogue
  graffiti subset, including the measured absence
  of any depiction coding for it (arm (d)).
- Nothing about what any sign means, sounds like,
  or refers to (spec §8). Decipherment was not a
  deliverable and is not advanced by any line of
  this report.

## 7. Process record (deviations and corrections, as they happened)

- **Phase-136:** no deviation from the freeze. One
  implementation note: two descriptive ineligible
  strata have a zero cell, so their per-stratum OR
  is recorded as `null` with an explanatory note in
  the results JSON rather than a non-finite value;
  no eligible stratum, statistic, or effect size is
  affected.
- **Phase-137:** no deviation from the freeze.
  Three recorded interpretations (phase report):
  the inclusion rule's token arm counted on parsed
  tokens (the freeze's own audit basis; the
  eligible set is identical under either basis);
  the Holdat quote-strip is a measured no-op on
  the file in hand; F3 length classes counted on
  parsed tokens per the freeze's wording while
  profiles exclude placeholders (142
  all-placeholder inscriptions at eligible sites,
  disclosed in the flow).
- **Phase-138:** the phase's descriptive numbers
  were never in question, but its PR #120 merged on
  a CI readout that did not match the run's actual
  conclusion: the backend job had in fact failed on
  two test pins in the phase's own test file
  (a field-class string pin and a line-wrap pin —
  both in test code, neither touching a descriptive
  quantity). The discrepancy was caught by the
  executing worker's own verification against the
  run's API record and job log, and corrected in
  PR #123 (merge `1c2a5fd2`), whose CI was verified
  green from the run's own conclusion and job log
  (1,044 passed / 14 skipped / 0 failed) before
  merging. The correction is recorded here and in
  the ledgers rather than left in a PR thread,
  because the merged-on-red interval is part of
  this program's record. Phase-137's first CI run
  also failed on the same Phase-138 pin (a file it
  did not touch) during the parallel execution;
  it proceeded only after PR #123 landed.
- Parallel execution produced one merge conflict
  in `experiment_graph.py` (registration-block
  adjacency across the phase PRs), resolved by
  keeping both blocks; all three nodes verified
  registered on final main.

## 8. Deliverables

Per phase (all merged): analysis script
(`backend/scripts/phase136_terminal_type.py`,
`phase137_site_repertoire.py`,
`phase138_graffiti_descriptive.py`); graph module
+ registration (nodes `IndusPhase136TerminalType`,
`IndusPhase137SiteRepertoire`,
`IndusPhase138GraffitiDescriptive`); tests
(`backend/tests/test_phase13{6,7,8}_*.py`); results
JSON (`reports/phase136_results.json`,
`phase137_results.json`, `phase138_results.json`);
phase report (`reports/phase136_report.md`,
`phase137_report.md`, `phase138_report.md`). This
combined report is the family's single BH
application point. The Stage 2 record is published
as Zenodo v4.8.0 (program note + the three phase
results JSONs) through the mandatory release gate;
the deposit record is
`outputs/RELEASE_VALIDATION.json`, entry
`release_v4_8_0`.
