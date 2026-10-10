# Phase-137 Report — Spec 024 Stage 2(c): Site Repertoire Differentiation

**Phase:** 137 · **Spec:** 024 §5.4 (test (c)) ·
**Freeze:** `specs/024-evidence-integration/stage2c-freeze.md`
(merged before any analysis code ran, PR #118) ·
**Family members:** F2 (Holdat compilation layer) and
F3 (ICIT-lineage layer), tested **separately, never pooled** ·
**Results:** `reports/phase137_results.json` (computed by
`backend/scripts/phase137_site_repertoire.py`, never
hand-written) · **Graph node:** `IndusPhase137SiteRepertoire`.

**AI disclosure:** this phase, and the execution it records,
were produced by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.

**Verdict discipline (family declaration, Stage 2(a) freeze
§1):** this report states **raw p-values only**. The verdict
words for F2 and F3 are assigned only after the
Benjamini–Hochberg correction at q = 0.05 across the family,
applied once in the combined Stage 2 report. Nothing below
is a verdict.

**Common design (as frozen).** Unit = the inscription. Profile
table = site × sign token counts over the layer's analysis
population; sign columns = signs with layer-wide count ≥ 10
within the analysis population, rarer signs pooled into one
`OTHER` column; placeholder tokens excluded from profiles
entirely. Statistic = Pearson chi-square of the table, used
as a divergence statistic only — all inference is by
permutation of site labels at inscription level **within
composition strata**, B = 9,999, seed 20261009,
p = (1 + #{χ²_perm ≥ χ²_obs}) / (1 + B), stdlib
`random.Random(20261009)`. Site inclusion: ≥ 30 inscriptions
AND ≥ 100 tokens. Estimability (freeze §3): a layer executes
iff ≥ 2 eligible sites and ≥ 2 sign columns; the sparsity
disclosure is mandatory. Effects (descriptive): Cramér's V,
observed statistic vs permutation median / 95th percentile,
per-site total-variation (TV) distance to the pooled profile
for **all** eligible sites. Class I interpretive fields
entered nothing in either layer (Holdat:
`letter_label_encoded`, `FormWithoutLemma`,
`MorphemeSeparated`, `morpheme boundary`, `noun`, `verb`,
`prefix`, `prefix_label_encoded`, `vowel`, `upos`, `xpos`;
ICIT-lineage: `class`, `sanskrit`, `translation`, `notes`).

---

## F2 — Holdat compilation layer: site repertoire differentiation

The layer is named in every output: its transcription is one
compilation's work, and the result describes that layer's
recorded repertoires.

**Population flow (as run).** 7,002 token rows read; grouped
by `seal_id` (tokens ordered by int(`position`)) into **1,670
inscriptions**, lengths 2–8 tokens, 390 distinct native
M-codes, no placeholder tokens, no seal with more than one
recorded site. All **9 sites pass the inclusion rule**; none
excluded:

| Site | Inscriptions | Tokens |
|---|---|---|
| Mohenjo-daro | 606 | 2,534 |
| Harappa | 492 | 2,079 |
| Lothal | 124 | 507 |
| Kalibangan | 110 | 485 |
| Dholavira | 106 | 439 |
| Chanhu-daro | 78 | 310 |
| Surkotada | 61 | 257 |
| Banawali | 60 | 255 |
| Rakhigarhi | 33 | 136 |

**Strata as applied.** Length class only — {2-3: 599,
4-5: 745, 6-8: 326}. Object-type control degenerates, as the
freeze states: the layer carries no object-type field and its
inscriptions are seal texts, so the type mix is a constant
and length is the only composition control this layer admits.
This is a property of the layer, recorded — not patched.

**Profile table.** 9 sites × **98 columns** (97 signs with
layer-wide count ≥ 10, plus `OTHER` holding 911 tokens =
13.01% of the 7,002 profile tokens). Grand total 7,002 =
the analysis token total; all margins reconcile in the
committed JSON.

**Estimability.** ESTIMABLE AND EXECUTED (≥ 2 sites, ≥ 2
columns). **Mandatory sparsity disclosure:** 882 cells;
**607 cells (68.8%) have expected count < 5**; minimum
expected count **0.214**; per-site token counts as in the
table above. The table is sparse — stated openly per the
freeze §3 substitution: inference is permutation-based and
uses no asymptotic approximation, so sparsity qualifies how
the divergence statistic behaves, not whether the test may
run.

**Result as found.** Observed χ² = **745.95**. Permutation
distribution: median **770.32**, 95th percentile **838.45**;
7,353 of 9,999 permutations met or exceeded the observed
statistic → **raw p = 0.7354**. Cramér's V (descriptive) =
0.1154. The observed differentiation sits **below the median
of its own composition-controlled null** — on this layer,
per-site repertoires differ by no more than the sites'
different length mixes already explain. (The BH verdict word
is deferred to the combined report, per the family
declaration above.)

Per-site TV distance to the pooled profile (descriptive,
all sites): Mohenjo-daro 0.044, Harappa 0.049, Lothal 0.120,
Dholavira 0.124, Kalibangan 0.130, Banawali 0.168,
Chanhu-daro 0.190, Surkotada 0.194, Rakhigarhi 0.288. The
largest distances belong to the smallest sites, the pattern
sampling noise alone produces; the permutation result above
is the test of that, and it does not separate the observed
table from its null.

---

## F3 — ICIT-lineage layer (horus84): site repertoire differentiation

**ICIT-lineage label (mandatory, spec §2.4 / §5.1):** this
layer is a derivative of the ICIT database in open file
form, **not an independent witness**; its results describe
this layer, not the Indus corpus in general.

**Population flow (as run).** **5,679 rows** read; all 5,679
parse to ≥ 1 code under `re.findall(r"\d{3}", text)`. Full
layer: 19,946 parsed tokens, of which 1,899 are placeholders
(`000`/`999`, excluded from profiles), leaving 18,047
non-placeholder tokens over 713 distinct native W-codes.
**7 sites pass the inclusion rule** (5,410 inscriptions);
**70 site labels are excluded and named**: Alamgirpur,
Allahdino, Altyn Depe, Amri, Bakkar Buthi, Bala-kot,
Banawali, Baror, Bhirrana, Chandigarh, Daimabad, Derawar
Ther, Desalpur, Failaka, Farmana, Ganweriwala, Gharo Bhiro,
Girsu, Gola Dhoro (Bagasra), Gonur Depe, Guddal A, Gumla,
Hajar, Hissam-dheri, Hulas, Janabiyah, Jhukar, Juna Khatiya,
Kalba, Kanmer, Karanpura, Karzakan, Khirsara, Kish, Kot-Diji,
Lakhanjo-daro, Lohumjo-daro, Luristan, Miri Qalat, Murda
Sang, Naru-Waro-dharo, Nindowari-damb, Nippur, Nuhato,
Ornach area, Pabumath, Pirak, Qala'at al-Bahrain,
Ra's al-Junayz, Rahman-deri, Rajanpur, Rakhigarhi,
Rappwala Ther, Rodji, Rupar, Saar, Salut, Shikarpur,
Shortughai, Sibri, Surkotada, Susa, Tarkhanewala-dera,
Tell Umma, Tello, Tepe Yahya, Tigrana, **Unknown** (a
missing-value label, not a site; 28 inscriptions / 136
parsed tokens — it fails the inscription arm of the rule),
Ur, Wattoowala. Excluded labels together carry 269
inscriptions.

Eligible sites (inscriptions / parsed tokens / profile
(non-placeholder) tokens):

| Site | Inscriptions | Parsed tokens | Profile tokens |
|---|---|---|---|
| Harappa | 2,717 | 7,975 | 7,168 |
| Mohenjo-daro | 1,923 | 8,330 | 7,809 |
| Dholavira | 238 | 808 | 637 |
| Kalibangan | 212 | 624 | 508 |
| Lothal | 208 | 818 | 681 |
| Chanhu-daro | 74 | 352 | 325 |
| Nausharo | 38 | 144 | 129 |

Analysis population: **5,410 inscriptions**, 19,051 parsed
tokens, **17,257 profile tokens** (1,794 placeholder tokens
at eligible sites excluded from profiles). 142 eligible-site
inscriptions consist solely of placeholder codes: they
remain in the population and in their strata (the freeze's
population rule is ≥ 1 *parsed* token) and contribute an
empty token multiset to the table.

**Strata as applied.** Type class × length class, 16 strata
all populated: SEAL {1: 108, 2-3: 701, 4-5: 735, 6+: 610};
TAB {1: 220, 2-3: 1,322, 4-5: 563, 6+: 170}; POT {1: 235,
2-3: 255, 4-5: 55, 6+: 12}; OTHER {1: 86, 2-3: 169, 4-5:
116, 6+: 53}. Type class = `type` prefix before ':' in
{SEAL, TAB, POT, OTHER}, OTHER pooling {TAG, MISC, BNGL,
ROD, IMPL, BEAD, MDLN, Unknown}; length class {1, 2-3, 4-5,
6+} **parsed** tokens. Length is counted on parsed tokens
(placeholders included), exactly as the freeze words it;
profile tokens exclude placeholders.

**Profile table.** 7 sites × **187 columns** (186 signs with
layer-wide count ≥ 10 within the analysis population, plus
`OTHER` holding 1,387 tokens = 8.04% of the 17,257 profile
tokens). Grand total 17,257; all margins reconcile in the
committed JSON.

**Estimability.** ESTIMABLE AND EXECUTED. **Mandatory
sparsity disclosure:** 1,309 cells; **887 cells (67.8%) have
expected count < 5**; minimum expected count **0.075**;
per-site profile token counts as in the table above. As
with F2, the table is sparse and that is disclosed, not
hidden; inference is permutation-based throughout.

**Result as found.** Observed χ² = **4,966.36**. Permutation
distribution: median **2,667.87**, 95th percentile
**2,844.61**; **0 of 9,999** permutations met or exceeded the
observed statistic → **raw p = 0.0001**, the minimum value
the frozen formula can return at B = 9,999. Cramér's V
(descriptive) = 0.2190.

**Uncontrolled confounders (freeze §6 B2 — stated wherever
this positive result is stated):** the composition strata
capture the confounders spec §5.1 names (object-type mix,
text-length mix) and nothing else. Other confounders —
period, preservation, excavation history — are not
available in this layer and are **not controlled**. The
raw association above is a fact about this layer's recorded
distribution after type/length control only; it is not
evidence that the uncontrolled factors could not produce
it. (The BH verdict word is deferred to the combined
report.)

Per-site TV distance to the pooled profile (descriptive,
all sites): Mohenjo-daro 0.127, Harappa 0.165, Dholavira
0.240, Lothal 0.292, Kalibangan 0.301, Chanhu-daro 0.349,
Nausharo 0.426.

---

## Cross-layer note (descriptive only, freeze §6 B3)

F2 and F3 point in different directions on their own layers
(F2's observed statistic below its null median; F3's far
above its null). The two layers are tested independently;
agreement or disagreement between them is **not itself a
test**, and no pooled analysis was performed or is implied.
The layers are different compilations' transcriptions —
a pooled table would test the compilations, not the sites.

## Deviations

**Deviations from the freeze: none.** Every frozen parameter
(B, seed, p formula, inclusion rule, collapse rule, strata,
column rule, estimability rule) was applied as written.
Recorded interpretations, where the freeze's wording admits
exactly one reading consistent with its own audit numbers:

1. **Site-inclusion token arm** is counted on *parsed*
   tokens, matching the freeze §5 audit counts (Nausharo
   shown as 144 tokens = its parsed total). The eligible set
   is identical under the non-placeholder count (Nausharo
   129 ≥ 100; no other label crosses either threshold), so
   the choice has no effect on any result.
2. **Holdat single-quote stripping:** the brief and prior
   loaders describe this compilation's values as
   single-quoted; the file in hand contains no single quotes
   (measured: 0 in the raw file), so the implemented strip
   (strip one surrounding pair, exactly as prior loaders do)
   changed no value. The flow counts above are the file's
   own.
3. **F3 length class** is computed on parsed tokens
   including placeholders, per the freeze §5 wording
   ("length class {1, 2-3, 4-5, 6+} parsed tokens"), while
   profiles exclude placeholders per §2 — both rules applied
   as written; the 142 all-placeholder inscriptions this
   produces are disclosed in the F3 flow above.

Execution note (not a deviation): the full run — both
layers, 2 × 9,999 permutations — completed in ~7 minutes
wall on a heavily loaded machine, inside the script's
per-layer deadline (3,300 s) with progress prints every
500 permutations.

## §8 fences (spec 024 §8, governing verbatim)

> Associations describe **use, not meaning**. A finding
> that a sign class clusters on tablets, or that a motif
> travels with a sequence class, is a fact about how the
> writing system was deployed — it is not evidence for what
> any sign sounds like, means, or refers to. **No result
> obtainable under this spec can mint, promote, demote, or
> validate any sign reading, change any anchor's status, or
> move PRED-2026 in either direction.**

Applied here: repertoire differentiation, where found, is a
fact about the recorded distribution of sign use across
sites in a named layer — it is not evidence for regional
"dialects" as linguistic entities beyond that statement,
for any reading, or for any anchor or PRED movement
(freeze §6). Anchors asserted byte-identical before the
run: sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`.

## Verification

- H23 gate, in order: script written → graph module created
  → registered in `experiment_graph.py` → registration
  asserted (`IndusPhase137SiteRepertoire` in `ATOMIC_NODES`)
  → script run.
- Phase tests: `backend/tests/test_phase137_site_repertoire.py`
  — **22 passed**, including the recomputation test, which
  re-ran the full script from the local store and reproduced
  the committed JSON's profile tables, observed statistics,
  permutation summaries, and raw p-values exactly.
- Foundation check (H21): **40 checks passed, 0 failed**,
  8 warnings.
