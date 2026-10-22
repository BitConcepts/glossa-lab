# Spec 024 — Stage 2(a) Freeze Record (Phase-136)

> ## FROZEN 2026-10-09 — Stage 2 family declaration + test (a)
>
> Frozen under spec 024 §5 / §12 on the owner's
> instruction of record: **Tristen Pierson,
> 2026-10-09 — "Do all next things"** (the remaining
> Stage 2 arms, (a), (c), and (d); arm (b) is CLOSED
> per `motif-arm-closure.md` and is not touched by
> anything in this freeze). This freeze is committed
> and merged **before** any Phase-136 analysis code
> runs (spec-before-code). It operationalizes the
> §5.2 sketch on the Phase-133 Stage 0 numbers; it
> narrows the sketch for feasibility in the places
> stated below and widens it nowhere.

**Phase:** 136 · **Spec:** 024 §5.2 (test (a)) ·
**Family role:** family member **F1** (declaration
in §1 below) · **Date:** 2026-10-09.

**AI disclosure:** this freeze, and the execution it
governs, are produced by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution §VI.

---

## 0. Recorded interpretation — the text substrate (binding on all Stage 2 freezes)

Phase-133 graded every layer's sign-sequence field
Class I with the reason stated verbatim in the
inventory: for horus84 `text`, *"Sign sequence
transcribed under the ICIT sign identifiers:
text-internal transcription, not context"*; for
Holdat `letters`, *"Sign identity (M-number)
assigned under the compilation's sign list:
text-internal transcription, not observational
context."* The Class I exclusion of spec §3.4 /
boundary 2 is an exclusion from **context
evidence**: interpretive material must not
masquerade as context. The §5 tests are defined
over a **text layer joined to context fields** —
§5.2's variable is a property of the inscription's
own sequence; §5.4's profiles are the text layers'
own sign distributions. Without the layers'
transcriptions those sketches are vacuous, and the
owner's Stage 2 instruction defines arm (a)'s
classes "from the layer's sequence data".

This freeze therefore records, explicitly: the
sequence fields (`text` in the ICIT-lineage layer;
`letters` with `position` in Holdat) are used
**only as the text substrate** — the inscriptions
themselves, exactly as transcribed by their
compilers, with the lineage label attached. They
are never used as context evidence and never enter
any context variable. Every genuinely interpretive
field enters **nothing at all**: horus84 `class`,
`sanskrit`, `translation`, `notes`; Holdat
`letter_label_encoded`, `FormWithoutLemma`,
`MorphemeSeparated`, `morpheme boundary`, `noun`,
`verb`, `prefix`, `prefix_label_encoded`, `vowel`,
`upos`, `xpos`; and the Holdat semantic-roles table
in full. All context variables in this test come
from Class O fields only (catalogue `object_type`;
horus84 `site`).

## 1. Family declaration (spec §5.1; tasks T10)

All confirmatory tests frozen under Spec 024
Stage 2 form one declared family, **F**:

| Member | Test | Layer | Freeze |
|---|---|---|---|
| **F1** | Terminal-class × object type, within-site stratified permutation test | ICIT-lineage (horus84) joined subset — **lineage label mandatory** | this freeze (Stage 2(a), Phase-136) |
| **F2** | Site repertoire differentiation, composition-controlled permutation test | Holdat | `stage2c-freeze.md` (Phase-137) |
| **F3** | Site repertoire differentiation, composition-controlled permutation test | ICIT-lineage (horus84) — **lineage label mandatory** | `stage2c-freeze.md` (Phase-137) |

- **Correction:** Benjamini–Hochberg at **q = 0.05**
  across the raw p-values of the family members
  that execute and are estimable, applied once, in
  the combined Stage 2 report. A member judged
  NOT ESTIMABLE under its frozen rule contributes
  no p-value and is reported NOT ESTIMABLE with its
  cell counts shown (spec §5.1).
- **Permutation parameters (all members):**
  B = 9,999 permutations; seed 20261009;
  p = (1 + #{statistic_perm ≥ statistic_obs}) /
  (1 + B); Python stdlib `random.Random(20261009)`,
  Fisher–Yates shuffles within strata. No asymptotic
  p-value is reported as a result anywhere (an
  asymptotic value may appear only as a labeled
  computational cross-check in a results JSON).
- Arm (d) (Phase-138) is **descriptive only** and is
  not a family member; it computes no test and no
  p-value.
- Anything computed outside this declaration is
  EXPLORATORY, labeled as such in every artifact,
  and excluded from the family (spec §5.1).

## 2. Question and falsifier (spec §5.2, restated)

**Question.** In the ICIT-lineage layer's
catalogue-joined subset, does the closing-sign
behaviour of inscriptions differ between seals and
tablets — measured as membership of the terminal
sign in the frozen spec-018 TERMINAL set — once
site composition is controlled within site strata?
A fact about **use**, prior to any reading (spec
§8 governs all reporting language).

**Falsifier (the null, stated in advance).** If the
association does not survive the within-site control
at the family threshold (BH-adjusted q > 0.05 in
the combined report), the functional-split
hypothesis for terminal signs is recorded as
**NOT SUPPORTED on this data**. A raw p reported in
the phase report is an intermediate quantity; the
verdict word is assigned only after the family
correction, in the combined report.

**Not this test:** this is not a PRED-2026-001/002
evaluation in any direction (spec §7). The
TERMINAL set is used as a frozen descriptive class
definition; no register criterion is applied, no
dedup-for-PRED protocol runs, and no output of
Phase-136 is an input to the PRED harness.

## 3. Population (frozen flow; design-audit counts recorded)

Computed at freeze time from the files as a design
audit (margins and flow counts only; no joint
outcome × type cell was inspected). Execution
recomputes every step and reports the flow as run.

1. ICIT-lineage layer rows: **5,679**.
2. Join on the Stage-0-audited key, Phase-133 §3.2
   rule (exact string; a row joins iff its `cisi`
   value is a printed catalogue ID in **exactly
   one** volume): matched **2,895**; ambiguous
   **2** (the value `H-311`); unmatched **2,782**.
   Ambiguous and unmatched rows are excluded and
   counted. (The v4.6.0 clarification stands: three
   `cisi` values carry trailing whitespace;
   exact-string matching is the frozen rule, so
   those rows fall where the rule puts them.)
3. The joined object's catalogue `object_type`
   (Class O; an object's type is the filled value
   on its catalogue rows — the audit found **no**
   joined object with conflicting filled types):
   filled **2,752** (Seals 1,588; Tablets 1,088;
   Graffiti 69; Objects 7); unfilled **143** —
   excluded, counted.
4. **Pre-declared restriction (narrowing, stated):**
   the test population is object types
   **{Seals, Tablets}** — **2,676** rows. Graffiti
   (69) and Objects (7) are excluded from the test:
   boundary 4 (graffiti material is never pooled
   into a test over seal/tablet texts) and the
   Objects cell (7) is below any statable minimum.
   Both are reported descriptively in the combined
   report. The sketch's "other inscribed objects"
   category is thereby **not** tested; the estimand
   is the seal-vs-tablet contrast, which is the
   sketch's substantive question.
5. Sequence parse, established convention for this
   lineage (Phase-115): `re.findall(r"\d{3}", text)`
   in recorded (reading) order; the terminal sign
   is the **last** parsed code. All 2,676 rows
   parse to ≥1 code.
6. Terminal mapping by the **frozen spec-018 §3
   canonical map** (Wells → Parpola), executed by
   the frozen machinery itself
   (`glossa_lab.pred_harness.build_sign_maps` /
   `SignMapper.map_w` over
   `data/crosswalks/canonical_sign_registry.csv`;
   conflict rule of §3: highest `corpus_freq`,
   tie → lowest P, residual tie → AMBIGUOUS → UNK;
   placeholder codes `000`/`999` → UNK per the
   lineage adapter convention). Rows whose terminal
   code maps to UNK carry no terminal class and are
   excluded, counted: audit flow — mapped **2,195**,
   UNK-terminal **481**.
7. **Stratum eligibility (frozen rule, applied
   mechanically to the step-6 population):** a site
   stratum enters iff its analysis-population
   N ≥ 20 and it contains ≥5 Seals and ≥5 Tablets.
   Audit-observed strata expected to qualify:
   Mohenjo-daro, Harappa, Kalibangan (their
   pre-mapping step-4 margins are 1,367 / 1,074 /
   68 rows).

## 4. Variables (all definitions frozen)

- **Outcome:** terminal mapped P sign ∈ TERMINAL14
  (spec 018 §3, end_rate ≥ 0.55 class) vs ∉.
  TERMINAL14 = {P020, P076, P095, P099, P108, P125,
  P210, P226, P256, P346, P359, P378, P384, P385}
  (verified at audit against
  `pred_harness.load_sign_classes`).
- **Predictor:** catalogue `object_type` ∈
  {Seals, Tablets} (Class O).
- **Stratum:** horus84 `site` (Class O; filled on
  all rows; the layer's own findspot record).
  Catalogue-site concordance for joined rows is
  reported descriptively in the results JSON; it is
  not a variable.
- No other variable enters the test. In particular
  no Class I field (§0) and no depiction field
  enters anything.

## 5. Estimability rule (frozen; spec §5.1)

The test executes iff, on the §3 analysis
population restricted to eligible strata: (i) ≥2
eligible strata; (ii) the pooled 2×2 table's
expected counts (from the pooled margins) are ≥5
in **at least 80%** of its 4 cells — the §5.1
default, unmodified for this test. Audit margins
(outcome margin among mapped step-6 rows: 475 of
2,195 in TERMINAL14; type margins 1,588 / 1,088 at
step 4) make failure unlikely; the rule is applied
mechanically regardless. Failure → **NOT
ESTIMABLE**, cell counts shown, no p-value, F1
contributes nothing to the BH correction.

## 6. Test and effect sizes (frozen)

- **Statistic:** Cochran–Mantel–Haenszel chi-square
  (no continuity correction) over the eligible
  strata's 2×2 (type × outcome) tables.
- **Null distribution:** permutation — within each
  stratum, object-type labels are shuffled across
  the stratum's rows (outcome vector and stratum
  sizes fixed); the statistic is recomputed per
  permutation; §1 parameters (B, seed, p formula).
- **Effect sizes (reported regardless of verdict):**
  Mantel–Haenszel common odds ratio with 95% CI
  (Robins–Breslow–Greenland variance on the log
  scale); the crude (unstratified) odds ratio,
  labeled uncontrolled and reported only so the
  control's effect is visible; per-stratum odds
  ratios (descriptive); observed TERMINAL14 shares
  by type within each stratum and pooled
  (descriptive counts and proportions).
- **Reported alongside every statistic:** the
  ICIT-lineage label; the join flow (step counts of
  §3); the 49.0% unjoinable-or-ambiguous share of
  the layer (2,784 of 5,679 rows); and the sentence:
  results describe this lineage layer's joined
  subset, not the Indus corpus in general.

## 7. Assumptions and epistemic boundaries (H13)

- **Assumptions:** (A1) the lineage layer's
  recorded reading order is the transcription's
  token order, per the established adapter
  convention for this lineage (Phases 107/115);
  the terminal sign is defined on that order.
  (A2) Catalogue `object_type` and horus84 `site`
  are observational records whose errors are not
  differential by terminal class in a way the test
  could detect; no correction is attempted.
  (A3) Rows are independent units for permutation
  purposes; duplicate inscriptions within the layer
  are a property of the layer as acquired and are
  **not** deduplicated (the PRED dedup protocol
  does not apply here — §2 fence); the flow counts
  state the population as acquired.
- **Boundaries:** §8 of spec 024 governs verbatim:
  associations describe use, not meaning; nothing
  here can mint, promote, demote, or validate a
  reading, change an anchor, or move PRED-2026.
  The layer is an ICIT-lineage derivative — not an
  independent witness — and every output carries
  that label in its headline.
- **Adversarial note:** the strongest alternative
  explanation for any association found is
  compilation-internal (the lineage's transcription
  and the catalogue's typing were both made within
  one scholarly tradition); the report must state
  this rather than let the within-site control
  imply more independence than exists.

## 8. Deliverables (Phase-136)

Per governance H15/H23 (graph-first, 5-step gate):
script `backend/scripts/phase136_terminal_type.py`;
graph module
`backend/glossa_lab/experiment_graph_phase136.py`
(node `IndusPhase136TerminalType`), registered in
`experiment_graph.py` and verified before the run;
tests `backend/tests/test_phase136_terminal_type.py`;
results `reports/phase136_results.json`; report
`reports/phase136_report.md`. Foundation check
(H21) after the run: 0 failures required. Anchors
asserted byte-identical (sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`).

## 9. Deviations

None at freeze. Any deviation discovered in
execution is recorded in the phase report as a
deviation with the rule that resolved it — never
silently adopted.
