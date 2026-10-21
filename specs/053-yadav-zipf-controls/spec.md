# Spec 053 — Yadav's Zipf Fit: What Is a Curve Fit Worth? (Design D-07, Arm A Only)

> ## FROZEN — 2026-10-21
>
> Frozen under the runnable-experiments campaign
> plan approved by the owner AS WRITTEN on
> 2026-10-21 (campaign decision E-1: this spec
> files its own OSF contract registration at
> its freeze; decision E-3 governs arm B, §12).
> This spec is campaign member 6 (design D-07,
> **arm A only**). The freeze decisions
> DD-053-11 to DD-053-19 are recorded in
> `adjudication.md` §8; DD-053-1 to DD-053-10
> stand as drafted, with DD-053-2, DD-053-4,
> DD-053-5 and DD-053-6 confirmed there.
>
> **The estimator ruling (DD-053-11, option
> (a)).** The freeze specifies the estimator of
> §4.2 completely — fitting procedure,
> parameters, grid, refinement, seeds, and the
> control constructions of §3 — as a
> freeze-stage design decision, and the
> "identical to Phase-43" reading is honestly
> **RETIRED**: no Phase-43 Zipf estimator
> exists to be identical to. Phase-43's results
> file (`outputs/phase43_all.json`, SHA-256
> `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4`,
> re-verified at this freeze by two routes)
> carries no Zipf fit — no exponent, no
> Mandelbrot parameters, no fitting procedure —
> and Yadav's recorded value of about 1.35
> rests on the claim file's evidence string
> alone. This spec therefore tests that
> recorded value under the named estimator of
> §4.2: its claims and falsifier are restated
> to say exactly that (claims edited at draft
> stage, before the digest; claim IDs stable).
> The falsifier itself never depended on a
> Phase-43 fit: it compares each named control
> against the Indus strict corpus under §4's
> one estimator (§1.2, §4.3).
>
> Execution runs as **Phase-413** (allocated at
> this freeze, DD-053-18). Nothing in this
> contract has been run, fitted, or computed:
> no control count has been entered, no corpus
> has been exported, and no fit of any system
> exists. Execution awaits this freeze merging,
> the OSF registration's approval act, and a
> separate execution order.

**Design source:** D-07 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/01-language-and-position.md`,
§D-07, read in full at this draft), with the
portfolio triage of 2026-10-21 (design D-07
found **RIPE (arm A)**: "Arm A — the identical
fit against named non-linguistic control
systems and a linguistic positive control, with
the subsampling and split/merge sensitivities —
needs only published counts and the strict
corpus. Arm B (the same fit on an independent
corpus) stays trigger-armed inside the
design.").

**Claim under test:**
`yadav_2009_arxiv_manual_001` — "Indus script
sign frequencies follow a Zipf-Mandelbrot
distribution" — standing **SETTLED, strongly
supported**: Phase-43 fitted the V3 corpus and
recorded a Zipf exponent of about 1.35, in the
range the original work reported. This spec
tests only the residue its not-understood text
names (§1). Arm B of the design is **not** a
member of this spec (§12).

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The verdict stands: on the corpus the program
fitted, the sign frequencies do follow the
Zipf-Mandelbrot curve. The claim's own
falsifier — "if frequency distribution deviates
from Zipf-Mandelbrot law" — did not fire, and
the recorded exponent (about 1.35) sits in the
range Yadav's original work reported.

The residue is what that fit is *worth*. The
claim's not-understood text states it plainly:
a Zipf-style curve is weak evidence about
meaning, because many systems that are not
language at all — and some random processes —
produce similar curves; the exponent's exact
value also moves with corpus size and with how
signs are split or merged. The text names two
strengthening acts: the fit measured against
known non-linguistic systems (this spec, arm A)
and the same fit on an independent corpus
(arm B — contingent, §12, not designed here).

### 1.1 The question, in plain words

Fit one identical curve-fitting rule to the
script and to symbol systems that are certainly
not writing. If the non-writing systems fit the
curve as well as the script does, then the
script's good fit, on its own, says almost
nothing — and the claim's record should carry
that strength label in so many words. If every
non-writing system fits strictly worse, the fit
is separable on these measures, and the record
should carry that instead. Either way the
product is an honest strength label for a
settled claim — not a new verdict on the claim
(§7, limit 2).

### 1.2 The falsifier, first

**Falsifier.** At least one named
non-linguistic control system fits the curve
**as well as or better than** the Indus strict
corpus does, under the identical fitting rules
of §4. "Fits as well" is mechanical, fixed here
before any fitting: a control fits as well iff
its primary fit error (§4.2) is less than or
equal to the Indus strict corpus's primary fit
error. No tolerance band enters the verdict
rule (DD-053-2); near misses are reported, not
verdicts (§4.3).

Everything below is written so that this
falsifier can fire: the control set is named
and frozen as cited data before any fit (§3,
gate 0.4), the estimator and the comparison
rule are fixed before any fit (§4), the step-0
gates run before any fit quantity exists (§3),
and every outcome — including the falsifier's
own word, NOT SEPARABLE — is pre-written in
§6 before any result can be known.

### 1.3 The hypothesis

**Hypothesis.** The Indus fit is
*distinguishable* from the fits of the named
non-linguistic control systems: every
non-linguistic control's primary fit error is
strictly greater than the Indus strict
corpus's, under §4's rules — and the comparison
itself is informative, in the sense §4.4 fixes:
the linguistic positive control fits strictly
better than every non-linguistic control.

## 2. Inputs (pinned where a pin exists; every pin re-asserted at the freeze)

Every pin in this section was re-derived at
the freeze of 2026-10-21 by two independent
routes — the contents-API raw route and the
git-blob route — agreeing byte-for-byte, at
`main` head `3af269f660a9368e898cdece41132200d31b87cc`:
the claim file `90476623…` (13,230 bytes), the
anchors file `df0cf620…` (570,344 bytes; census
re-read: 287 anchors, 94
`strict_sa_independent`), the crosswalk
`4ace1a61…`, the Mahadevan–Parpola crosswalk
`9ebd7723…`, and the Phase-43 results file
`78a6c219…` (15,047 bytes; re-read in full at
the freeze: it contains no occurrence of the
word "Zipf" and no Mandelbrot parameter — the
ground for DD-053-11).

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json`) | SHA-256 `904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3` (recomputed at this draft from `main`, head `83b6a563…`). manual_001: strongly supported, stage explained; evidence string "Phase-43: V3 Zipf exponent ~1.35 (super-Zipfian)"; not-understood text as §1 quotes. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) — the strict sign set's census source | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft; matches the pin Specs 042/048 carry). Census read at this draft: 287 anchors, **94** carrying validation status `strict_sa_independent` — the strict sign set of designs D-03/D-04/D-07. This spec moves no anchor; the file is asserted byte-identical before and after any execution. |
| Strict corpus (the Indus distribution of record) — the V3 / Mahadevan-lineage corpus the Phase-43 framework ran on, restricted to the strict sign set | **No file pin is stated at this draft, deliberately** (the Spec 048 precedent, DD-053-4). Spec 033 §4 states this corpus as "the program's V3/Mahadevan-lineage corpus as held in the database" — a database posture, not a pinnable repository file on `main`. The layer is therefore identified, exported, and pinned by digest at step 0, before any fitting, under gate 0.3 — and the run closes if it cannot be (OPEN-053-1). Inventing a pin at draft would repeat the stale-pin failure Spec 040's gate record documents. |
| Sign crosswalk (`data/crosswalks/sign_crosswalk_master.csv`) — the source of the §5 split/merge variants | SHA-256 `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` (recomputed at this draft). The Mahadevan–Parpola crosswalk file (`backend/glossa_lab/data/mahadevan_parpola_crosswalk.json`, SHA-256 `9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b`, recomputed at this draft) is cited alongside it for numbering questions. |
| Control counts — the named systems of §3 gate 0.4 | Bibliographic pins as drafted; the counts themselves are entered as **cited data at step 0** (gate 0.4), each count with its source locator, and frozen before any fit. **Ruled at the freeze (DD-053-13):** the named systems and bibliographic pins stand as drafted, no second positive control is added, and gate 0.4 is the fixed pin source for the control tables — the exact tables and per-count locators are entered there, and a system that cannot be entered whole closes the run CONTROL SET FREEZE FAILED. The freeze invents no table it has not seen (§7 defect 4 of the adjudication). No count is typed into a script (H16). |
| Phase-43 results file (`outputs/phase43_all.json`) | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` (recomputed at this draft). Read in full at this draft: it carries Phase-43's corpus census (3,916 records; 12,494 sign instances; top-20 sign frequencies) and its positional and SA tables — and **no Zipf fit**: no exponent, no Mandelbrot parameters, no fitting procedure. It is pinned here so the freeze works from the complete record, and it is the ground for §4.2's estimator statement. |
| Yadav's original report | Yadav et al. 2009, "Statistical analysis of the Indus script using n-grams" (arXiv preprint) — the source document of the claim record; cited for the reported exponent range only. No number is taken from it at execution; the comparison is internal to §4's rules. |

## 3. Step 0 — gates before any fit (fail-closed)

Execution runs these gates in order, before any
Zipf-Mandelbrot fit is computed for any system.
A failure stops the execution in the class
named; nothing is repaired at run time, and no
quantity produced before a gate failure is
quotable.

- **0.1 Input integrity.** Every §2 input that
  carries a pin hashes to its freeze-record
  value, and the anchors file is asserted
  byte-identical. A mismatch stops the run as
  **INVALID**.
- **0.2 Estimator self-test.** The §4 estimator,
  implemented once, is run on synthetic
  rank–frequency data generated from known
  Zipf-Mandelbrot parameters (α = 1.20,
  q = 2.0, V = 200 types, N = 50,000 tokens,
  seed 20261021, counts drawn by the stated
  multinomial procedure in the execution
  script). The gate passes iff the fit recovers
  α within ±0.10 and q within ±1.0 of the
  generating values. A failure stops the run
  as **INVALID** — the comparison does not
  proceed on machinery that cannot first
  recover parameters it planted. This gate is
  the draft's able-to-fail proof for the
  estimator (DD-053-3).
- **0.3 Strict corpus identification and pin.**
  The V3 / Mahadevan-lineage corpus layer of
  record is identified from the database as the
  layer the Phase-43 framework ran on, exported
  in full, and pinned by SHA-256 digest in the
  step-0 record. The gate states the export's
  inscription count and token count. If the
  layer cannot be uniquely identified, cannot
  be exported whole, or cannot be shown to be
  the Phase-43 framework's corpus family, the
  run closes as **STRICT CORPUS NOT PINNABLE**
  (§6 wording) and nothing is fitted.
- **0.4 Control set freeze (cited data).** The
  control set is entered and frozen in the
  step-0 record — **before any fit, including
  the Indus fit** — as follows. Each system's
  entry is a canonical count table (type
  identifier, token count) with a per-system
  source citation and per-count locators where
  the source is tabular.
  - **N1 — Mesopotamian numerical signs.**
    Token frequencies of numerical signs from
    published counts of archaic Mesopotamian
    administrative tablets (the design's named
    example; bibliographic pin: Nissen,
    Damerow & Englund, *Archaic Bookkeeping*
    (1993) and the published archaic sign
    counts it reports — exact table confirmed
    at the freeze, OPEN-053-3). Numerical
    signs only; phonetic/syllabic signs of the
    same tablets are not this system. (Freeze
    ruling DD-053-13: this source stands as
    named; its exact table is entered with its
    locator at this gate.)
  - **N2 — Heraldic charges.** Frequencies of
    charges (the devices borne on shields)
    across a published roll of arms (the
    design's named example; freeze ruling
    DD-053-13: the roll and edition are entered
    with their citation at this gate, as the
    fixed pin source for this system's table).
    The counting unit is one
    charge occurrence on one shield, as the
    roll records it.
  - **N3 — Synthetic emblem inventory.**
    Generated, not published — fully pinned
    here (DD-053-6): a Yule–Simon process with
    innovation probability ρ = 0.10, seed
    20261021, run to exactly the Indus strict
    corpus's token total N (gate 0.5's count,
    so the synthetic system is size-matched);
    99 replicates are generated, each replicate
    is a separate system instance, and N3's
    fit quantities are the medians across
    replicates (§4.3). A uniform-random
    inventory is **not** the synthetic control:
    it produces a near-flat distribution by
    construction and could not test the
    residue's point, which is that a *stated
    random process* can produce this curve
    (adjudication §3, C08).
  - **P1 — Linguistic positive control.**
    Sign frequencies of a deciphered,
    certainly-linguistic script from published
    corpus counts: **Linear B** syllabic sign
    frequencies (bibliographic pin: the
    published Linear B corpus counts; freeze
    ruling DD-053-13: the exact source is
    entered with its citation at this gate, and
    no second positive control is added). One positive control is the
    design's floor ("at least one"); a second
    may be added only at the freeze, openly.
  If any named system's counts cannot be
  entered completely as published — the whole
  inventory the source reports, not a selection
  — or any entry lacks its citation, the run
  closes as **CONTROL SET FREEZE FAILED** (§6
  wording). No system is substituted, trimmed,
  or completed from another source after this
  gate, and no fit of any kind precedes it.
- **0.5 Census and floors (counts only).** From
  the pinned strict corpus: the strict
  distribution's census — distinct strict types
  present (of the 94), strict token total N,
  inscription count — computed and stated in
  the step-0 record. **Floors:** the primary
  proceeds only if distinct strict types
  present ≥ **50** and strict tokens ≥
  **2,000** (DD-053-7; confirmed at the freeze,
  DD-053-14). Below either floor the
  execution closes as **TOO THIN** (§6
  wording) with the census as its finding; no
  fit is computed. The frozen control tables'
  type and token counts are stated alongside,
  for the record; no floor applies to a
  control — a control is the published system
  as it stands.

## 4. The estimator and the comparison rule (fixed before any fitting)

### 4.1 The distribution fitted, per system

For each system, the input is its frozen count
table (§3 gate 0.4; for the Indus, gate 0.5's
strict distribution: tokens in the pinned
corpus whose sign is in the strict sign set,
counted by sign type; signs outside the strict
set contribute neither types nor tokens —
DD-053-4). Types are ranked by count
descending; ties are broken by type identifier
ascending, so the ranking is deterministic.
The ranked counts are f(1) ≥ f(2) ≥ … ≥ f(V),
with V the number of distinct types and
N = Σ f(r) the token total.

### 4.2 The estimator (identical for every system)

The Zipf-Mandelbrot model f̂(r) = C / (r + q)^α
is fitted with C fixed by normalisation
(Σ f̂(r) = N — C is not a free parameter), by
minimising the sum of squared log residuals,
SSE = Σ_r (log f(r) − log f̂(r))², over a
deterministic grid: α from 0.00 to 3.00 in
steps of 0.01, q from 0.0 to 20.0 in steps of
0.1; then one refinement pass at one-tenth
steps in α and q around the best grid cell.
The same code, grid, and refinement run for
every system, the Indus included. Reported per
system: V, N, fitted α and q, SSE, and:

- **Primary fit error (the comparison
  quantity):** NRMSE_log = √(SSE / V) — the
  root-mean-square log residual. It is a ratio
  measure, so systems of different sizes are
  compared on the shape of the fit, not on
  raw counts.
- **Secondary (reported, never decisive):**
  R² in log space, 1 − SSE / Σ_r (log f(r) −
  mean log f)², and the fitted α itself.

This estimator is the fitting rule of record
for this spec (DD-053-3). It is not claimed to
be Phase-43's estimator: Phase-43's results
file is pinnable (§2) but records no Zipf fit
— no exponent, no Mandelbrot parameters, no
fitting procedure — and no Phase-43 estimator
script for the Zipf fit is on `main` at this
draft (adjudication §7, defect 2), so there is
no Phase-43 fitting rule to be identical to.
The recorded exponent of about 1.35, which
lives in the claim record's evidence string,
is context for the comparison, not a
reproduction target. **Freeze ruling
DD-053-11 (option (a)):** this estimator —
model, normalisation, objective, grid,
refinement, and the gate 0.2 self-test with
its planted parameters and seed — is specified
completely here as a freeze-stage design
decision and stands as the fitting rule of
record; the "identical to Phase-43" reading is
RETIRED, because the freeze re-verified that
no Phase-43 estimator exists on the record
(the Phase-43 results file carries no Zipf fit
at all). No estimator may be substituted after
any fitting.

### 4.3 The comparison rule — what counts as "fits as well"

Stated mechanically, in full, before any
fitting:

1. Compute NRMSE_log for the Indus strict
   corpus (call it E_Indus) and for each
   control: E_N1, E_N2, E_P1, and for N3 the
   **median** NRMSE_log across its 99
   replicates (E_N3), with the replicates'
   full distribution reported.
2. A non-linguistic control **fits as well**
   iff its error is less than or equal to
   E_Indus: E ≤ E_Indus. ("As well or better,"
   the design's words, with no tolerance band —
   DD-053-2; confirmed at the freeze with
   ε = 0, DD-053-15.)
3. The **falsifier fires** iff at least one of
   N1, N2, N3 fits as well under rule 2.
4. The **gap** Δ = E_control − E_Indus is
   reported for every control. A control with
   0 < Δ ≤ 0.02 is named a **NEAR MISS** in
   every product that reports the outcome: it
   did not fire the falsifier, and it is not
   buried either. The 0.02 band is a reporting
   rule only; it changes no verdict.
5. N3's replicates are also reported against
   rule 2 individually: the share of replicates
   fitting as well is stated beside the median
   rule's outcome, so a median that hides a
   split distribution is visible as one.

### 4.4 The positive-control validity condition

The comparison is **informative** only if the
estimator and measures can tell a known
language's distribution from the named
non-linguistic ones. Mechanically: P1 passes
iff E_P1 is strictly less than every
non-linguistic control's error (E_P1 < E_N1,
E_P1 < E_N2, E_P1 < E_N3). If P1 does not pass,
the headline is **COMPARISON UNINFORMATIVE**
(§6): the measures did not separate the one
system in the set that is certainly writing,
so they are not used to judge the script
either way (DD-053-5). This condition is
checked from the same frozen fits; it is not a
fit of its own and it is not adjustable after
the fits exist.

### 4.5 The headline rule

After all gates pass and §4.4 is evaluated,
the headline is exactly one of:

- **SEPARABLE** — P1 passes (§4.4) and no
  non-linguistic control fits as well (§4.3
  rule 3 does not fire).
- **NOT SEPARABLE** — P1 passes and the
  falsifier fires: at least one named
  non-linguistic system fits as well as or
  better than the script.
- **COMPARISON UNINFORMATIVE** — P1 does not
  pass, whatever the Indus comparison shows.

## 5. Sensitivities (reported alongside, never verdict-changing)

Fixed in advance by the design; all three are
computed and reported with the primary, and
none changes the §4.5 headline.

- **S1 — Subsampling.** The Indus strict
  distribution is refitted on random halves
  and random quarters of the pinned corpus's
  **inscriptions** (inscription-level sampling,
  so no fabricated texts are created —
  DD-053-9): 99 replicates per level, seed
  20261021, sampling without replacement.
  Reported per level: median and central 90%
  interval of fitted α and of NRMSE_log. The
  table states how far the exponent and the
  fit error move with corpus size — the
  movement the residue names — in numbers.
- **S2 — Split/merge variants.** The Indus
  strict distribution is refitted under the
  pinned crosswalk's variant structure:
  **merged** — strict types the crosswalk
  links as allograph/variant forms are
  collapsed into single types, counts summed;
  **split** — strict types the crosswalk
  records as composite are expanded into
  their components where the pinned corpus's
  encoding carries the components. If the
  encoding does not carry a component, that
  type is reported unexpanded, by name, and
  the variant is labelled partial with the
  affected types listed. Reported: per
  variant, V, α, q, NRMSE_log beside the
  primary's. The variant construction is
  frozen in the execution script from the
  pinned crosswalk alone; no variant is
  built from the fit results.
- **S3 — Full-inventory fit.** The same
  estimator fitted to the pinned corpus's
  **full** sign inventory (all types, not
  only the strict set), reported with its α
  beside the recorded Phase-43 exponent of
  about 1.35. This is the comparability
  bridge to Yadav's original population
  (DD-053-4); it is a sensitivity because
  the design's primary population is the
  strict corpus, and it carries no verdict.

## 6. Outcome set and pre-written verdict wordings

The execution ends in exactly one headline
outcome. The outcome record's headline
paragraph uses one of these forms, with the
bracketed quantities filled from the run.
These wordings are written before any data is
touched; no other headline wording may be
used. **Every adjudicated outcome attaches to
the claim as a dated bounded finding (a
strength label); none changes the claim's
recorded status** (§7, limit 2).

- **SEPARABLE:** "Fitted under one identical
  Zipf-Mandelbrot rule, the Indus strict corpus
  (fit error [E_Indus], exponent [α]) fits the
  curve strictly better than every named
  non-linguistic control — Mesopotamian
  numerical signs ([E_N1]), heraldic charges
  ([E_N2]), and the synthetic emblem process
  (median [E_N3]) — and the linguistic positive
  control, Linear B sign frequencies ([E_P1]),
  fits strictly better than every
  non-linguistic control, so the measures
  separate the set's one certain writing system
  from its non-writing systems. On these
  measures, and on these measures only, the
  Indus fit is separable from the
  non-linguistic controls. This is a strength
  label for the recorded fit, not new evidence
  that the script encodes language: separability
  from three named systems is not separation
  from non-language in general."
- **NOT SEPARABLE:** "Fitted under one
  identical Zipf-Mandelbrot rule, [control
  name(s)] fit(s) the curve as well as or
  better than the Indus strict corpus does
  (Indus fit error [E_Indus]; [control] [E],
  gap [Δ]). A system that is not writing
  produces this curve as well as the script
  does, so the recorded fit, on its own,
  carries no distinguishing weight: the claim's
  record gains this dated strength label —
  'the Zipf-Mandelbrot fit is not separable
  from named non-linguistic systems on these
  measures' — beside its standing verdict,
  which does not change. What the script
  encodes is not decided by this result in
  either direction."
- **COMPARISON UNINFORMATIVE:** "The
  comparison cannot judge the script: the
  linguistic positive control, Linear B sign
  frequencies (fit error [E_P1]), does not fit
  strictly better than every non-linguistic
  control ([per-control errors]), so the
  measures used here do not separate the one
  certain writing system in the set from
  systems that are not writing. The Indus
  quantities ([E_Indus], exponent [α]) are
  reported for the record and support no
  separability conclusion either way. The
  claim stands exactly as recorded, with no
  strength label added."
- **TOO THIN (step-0 closure):** "Spec 053
  closed at step 0, gate 0.5: the strict
  corpus carries [t] distinct strict types and
  [n] strict tokens in the pinned layer,
  below the frozen floors (50 types, 2,000
  tokens). No fit was computed. This closure
  is a statement about runnability, not about
  the claim; the claim stands exactly as
  recorded."
- **STRICT CORPUS NOT PINNABLE (step-0
  closure):** "Spec 053 closed at step 0, gate
  0.3: the V3 / Mahadevan-lineage corpus layer
  of record could not be uniquely identified
  and pinned as the Phase-43 framework's
  corpus ([reason]). No fit was computed.
  This closure is a statement about
  runnability, not about the claim; the claim
  stands exactly as recorded."
- **CONTROL SET FREEZE FAILED (step-0
  closure):** "Spec 053 closed at step 0, gate
  0.4: the control set could not be frozen as
  cited data as §3 requires ([system and
  reason]). No fit was computed — in
  particular, the Indus fit was not computed
  ahead of the controls. This closure is a
  statement about runnability, not about the
  claim; the claim stands exactly as
  recorded."
- **INVALID (integrity closure):** "Spec 053
  closed as INVALID: [the named §2 pin
  mismatched / the estimator self-test of gate
  0.2 failed / the anchors assertion failed /
  a fit is shown to precede its gate]. No
  result is recorded under this spec."

## 7. Epistemic limits (binding on all outputs)

1. **No promotion to language evidence.** Arm A
   cannot promote the fit into evidence that
   the script encodes language — that is
   exactly the over-reading the residue exists
   to prevent. Even SEPARABLE says only that
   three named non-linguistic systems fit
   worse on these measures; it does not say
   the script is writing, and no output may
   present it as doing so.
2. **No verdict change.** The claim
   `yadav_2009_arxiv_manual_001` stands
   strongly supported on its recorded test.
   This spec's outcome appends to its record
   as a dated bounded finding (the strength
   label of §6); the recorded status, the
   recorded exponent, and the claim's own
   falsifier text are never edited.
3. **Three systems are not all non-language.**
   The control set is the named set of §3 and
   nothing larger. A reader who needs "no
   non-linguistic system fits this well" needs
   a different, larger design; this one names
   its systems so its conclusion can be quoted
   exactly as far as it reaches.
4. **The strict population is not Yadav's
   population.** The primary fits the strict
   sign set's distribution (94 candidate
   types), not the full inventory Yadav fitted.
   The full-inventory sensitivity (S3) is the
   stated bridge; no output may quote the
   strict fit's exponent as Yadav's exponent
   reproduced or contradicted.
5. **Published counts are taken as published.**
   Each control is its source's inventory as
   the source reports it — its completeness,
   period, and counting conventions are the
   source's. The step-0 record states each
   source's conventions beside its table; a
   dispute about a source is a dispute about
   that control, recorded as such, never
   repaired by adjusting counts.
6. Negative, uninformative, thin, and
   step-0-closure outcomes are recorded with
   the same prominence as a separable finding.

## 8. Controls and named confounders

- **Corpus size.** Fit error and exponent move
  with N and V. The synthetic control is
  size-matched to the Indus token total
  (gate 0.4); every system's V and N are
  reported beside its error; and S1 measures
  the Indus quantities' own movement under
  halving and quartering, so a size artefact
  is visible in the record rather than
  asserted away.
- **Inventory-size mismatch across published
  systems.** N1, N2, and P1 come at their
  published sizes; NRMSE_log is a per-type
  average of log residuals, which is the
  draft's mitigation, and the limit is stated:
  the comparison is of fit shape under one
  rule, not of systems equated in size
  (adjudication §3, C07).
- **Counting conventions differ by source.**
  Each control's unit is stated at its entry
  (gate 0.4) and held fixed; no unit is
  harmonised across systems after entry,
  because harmonisation after seeing counts
  is a discretion the design does not grant.
- **The estimator could favour a shape.**
  That is what P1 tests (§4.4): if the rule
  cannot rank the set's certain writing system
  above its non-writing systems, the run says
  so and judges nothing.
- **Sign-inventory discretion (Indus side).**
  The strict set is the anchors file's frozen
  census, not a list chosen for this test;
  S2 reports the fit's movement under the
  crosswalk's split/merge variants, the
  movement the residue names.

## 9. Reporting obligations

Every product of an execution carries, in its
headline section:

1. the corpus label — the pinned strict corpus
   (gate 0.3 digest), its census (types
   present, strict tokens, inscriptions), and
   its lineage posture as recorded (V3 /
   Mahadevan lineage, the same lineage the
   original study used — stated, per the claim
   record, wherever the result is stated);
2. the frozen control tables' identity: per
   system, source citation, V, N, fitted α and
   q, NRMSE_log, R²_log, and the gap Δ against
   the Indus error — for **every** system, not
   only decisive ones, with N3's replicate
   distribution and NEAR MISS names (§4.3)
   included;
3. the positive-control condition's outcome
   (§4.4) stated before the headline word;
4. the headline outcome word of §6, in §6's
   pre-written wording;
5. the sensitivities S1–S3 in full tables;
6. the fence sentence: "This result is a
   strength label for a recorded curve fit. It
   is not evidence that the script encodes
   language, and it changes no verdict."

Deliverables at execution: a results JSON
(step-0 record with all pins, the frozen
control tables and their citations, census,
self-test record, per-system fits, replicate
distributions, sensitivities), a report under
these headline rules, the experiment-graph
node (H15/H23, registered and verified before
the run), the outcome append in this
directory — including the dated strength-label
append to the claim's record — and the LEDGER
entry (H1). Foundation check (H21) after the
execution phase: 0 failures, or the outcome
record says why not. Anchors asserted
byte-identical before and after.

## 10. Stop conditions and outcome classes

Execution ends in exactly one of:

- **SEPARABLE**, **NOT SEPARABLE**, or
  **COMPARISON UNINFORMATIVE** — per §4, after
  all gates pass.
- **TOO THIN** — gate 0.5 floors fail. No fit
  is computed.
- **STRICT CORPUS NOT PINNABLE** — gate 0.3.
- **CONTROL SET FREEZE FAILED** — gate 0.4.
- **INVALID** — a §2 pin mismatches, the
  estimator self-test fails (gate 0.2), the
  anchors assertion fails, or any fit is shown
  to precede its gate.

## 11. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — integrity; estimator
   self-test; strict corpus identified,
   exported, pinned; control set entered and
   frozen as cited data; census and floors.
3. **Primary fits** (§4) — every system under
   the one estimator; the comparison rule and
   the positive-control condition applied
   mechanically.
4. **Sensitivities** (§5) — subsampling,
   split/merge variants, full-inventory fit.
5. **Outcome** (§9) — appended records only;
   anchors asserted byte-identical; foundation
   check reported as measured.

## 12. What this spec is not

Not arm B. **Arm B of design D-07 — the
identical fit on a corpus independent of the
Mahadevan lineage — is trigger-armed and is
not a member of this spec or of this campaign
pass** (campaign decision E-3): its trigger is
a genuinely independent corpus entering
through Phase-130 intake (the 2026-10-08 sweep
and the 2026-10-20 re-tests found none in
hand). If the trigger fires, arm B queues for
its own mini planning gate; it does not join
this spec, and this spec neither designs nor
pre-registers its execution — the contingent
status is recorded in `adjudication.md` and
claim F053-C14, and that recording is all this
draft does with arm B.

Not a re-run of Yadav's original fit, not a
re-adjudication of the strongly supported
verdict, not a test of whether the script
encodes language, not design D-08 (the
opening/closing-sign claim, a separate member
of this campaign), not a new corpus, and not
an authorisation to execute. It is the
control-systems comparison for one settled
claim, arm A only, designed so that its honest
outcomes — including closing at its own
step 0 — are written down before any system
is fitted.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
