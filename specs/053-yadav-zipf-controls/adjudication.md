# Spec 053 — Adjudication Record

> ## FREEZE ACT — 2026-10-21
>
> The freeze decisions are recorded in §8 of
> this record (DD-053-11 to DD-053-19),
> resolving OPEN-053-1 to OPEN-053-8 on the
> record. The central ruling is DD-053-11
> (option (a)): the §4.2 estimator is specified
> completely at the freeze and the "identical
> to Phase-43" reading is retired, on the
> re-verified evidence that no Phase-43 Zipf
> estimator exists.

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign plan,
>    approved by the owner AS WRITTEN on
>    2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
>    Parts 1–4 read in full at this draft).
>    The campaign commissions this draft:
>    member 6 (design D-07, **arm A only**),
>    Wave 1, independent members in parallel.
>    Decision **E-3** governs arm B: trigger-armed
>    arms do not auto-join; a fired trigger queues
>    a mini planning gate (§5 of this record).
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-07 found **RIPE (arm A)** — "Arm A —
>    the identical fit against named non-linguistic
>    control systems and a linguistic positive
>    control, with the subsampling and split/merge
>    sensitivities — needs only published counts
>    and the strict corpus. Arm B (the same fit on
>    an independent corpus) stays trigger-armed
>    inside the design."
> 3. **Design D-07 itself** (PR #195 packet,
>    `01-language-and-position.md`, §D-07), read
>    in full at this draft. The design governs
>    substance; where it is silent or ambiguous,
>    §3's double derivation and §6's defect list
>    record what this draft did about it.
>
> These inputs commission this **draft**. The
> freeze and the execution of Spec 053 are
> separate later acts under the campaign's
> Waves 2 and 3.

## 1. The adopted basis (operative substance)

- **The design.** D-07 arm A: fit the identical
  Zipf-Mandelbrot estimator to (a) the Indus
  strict corpus, (b) at least three published
  non-linguistic symbol inventories named at
  freeze (the design's examples: heraldic charge
  frequencies, Mesopotamian numerical-sign
  frequencies from published counts, a synthetic
  emblem inventory generated under a stated
  random process), and (c) at least one known
  linguistic corpus as a positive control; report
  the exponent's movement under subsampling
  (halving, quartering) and under the crosswalk's
  split/merge variants. The conclusion is a
  stated comparison, attached to the claim as a
  bounded finding, not a verdict change.
- **The claim.**
  `yadav_2009_arxiv_manual_001`: SETTLED,
  strongly supported — "Indus script sign
  frequencies follow a Zipf-Mandelbrot
  distribution"; Phase-43 evidence, V3 Zipf
  exponent about 1.35; stage explained. Its
  not-understood text asks for exactly this
  comparison (and, separately, arm B).
- **The falsifier.** At least one named
  non-linguistic system fits as well or better
  under the same fitting rules. Spec §4.3 states
  "as well" mechanically (NRMSE_log ≤ the Indus
  value) before any fitting.
- **Arm B.** Contingent only (§5). Not designed,
  not pre-registered, not executed here.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
via the GitHub API against `main` (head
`83b6a563…`); the local checkout was not used:

- **Design D-07** — read in full, both in the
  campaign designs copy and on the PR #195
  branch: the open point, arm A's hypothesis
  and falsifier, its method and named example
  controls, the sensitivity table "fixed in
  advance", arm B's blocked precondition, and
  the closing limit ("Arm A cannot promote the
  fit into evidence that the script encodes
  language… Its product is an honest strength
  label for a settled claim").
- **The claim record** — read on `main`:
  manual_001's normalized claim, status
  strongly_supported, stage explained, its
  falsification condition ("If frequency
  distribution deviates from Zipf-Mandelbrot
  law"), its Phase-43 evidence string, and its
  not-understood residue text (non-linguistic
  systems and random processes produce similar
  curves; the exponent moves with corpus size
  and split/merge choices; the strengthening
  acts are the control comparison and the
  independent-corpus fit). File recomputed to
  SHA-256 `90476623…` at this draft.
- **The strict sign set** — the anchors file
  recomputed to SHA-256 `df0cf620…` (matching
  the pin Specs 042/048 carry) and its census
  read: 287 anchors, **94** with validation
  status `strict_sa_independent`. Spec 033 §4
  read on `main`: the strict set and the
  "V3/Mahadevan-lineage corpus as held in the
  database" definition this draft inherits.
- **The strict-corpus pin posture** — follows
  Spec 048's verified finding: the strict
  corpus is a database posture, not a pinnable
  repository file on `main`; hence spec §2
  states no pin and gate 0.3 makes
  identification-and-pinning a fail-closed
  step-0 act (DD-053-4).
- **The crosswalk** —
  `data/crosswalks/sign_crosswalk_master.csv`
  recomputed to SHA-256 `4ace1a61…`;
  `mahadevan_parpola_crosswalk.json` to
  `9ebd7723…`. The crosswalk module's own
  header (read at this draft) records typed
  links, never silent collapses — the basis
  for S2's variant construction and its
  partial-variant honesty rule.
- **The Phase-43 Zipf record (a gap, recorded,
  not papered over)** — Phase-43's results file
  `outputs/phase43_all.json` was located on
  `main`, recomputed to SHA-256 `78a6c219…`,
  and read in full: it carries the phase's
  corpus census (3,916 records; 12,494 sign
  instances; top-20 frequencies), its SA
  scores, and its positional tables — and **no
  Zipf fit**: no exponent, no Mandelbrot
  parameters, no fitting procedure. No
  Phase-43 estimator script for the Zipf fit
  is on `main`. The recorded exponent of about
  1.35 therefore rests on the claim file's
  evidence string alone. The only Zipf results
  file in `reports/`
  (`reports/indus_phase31_t3_zipf_restored.json`)
  is an older, slope-based record (M77 slope
  0.75, TB slope 0.93), reconstructed from an
  archived result — a different measure from a
  different phase. Hence DD-053-3 (the spec
  defines its own estimator) and OPEN-053-2.
  *(Correction note, same day: the first
  drafting pass searched `reports/` and
  `backend/reports/` only and stated that no
  Phase-43 results file was pinnable; the
  `outputs/` file was found on a fuller tree
  listing minutes later and this record, spec
  §2/§4.2, and claims F053-C02/C06 were
  corrected before the draft PR was read by
  anyone. The substance is unchanged: the file
  contains no Zipf fit.)*
- **Not done at draft, by design** — no control
  count was entered, no corpus was exported, no
  fit of any system was computed, no synthetic
  inventory was generated, no code was written
  or run, the AEE hooks have not run, and
  nothing was filed with OSF.

## 3. Double derivation of acceptance tests (doctrine requirement)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived **twice,
independently, from the claim alone** —
Derivation A from the claim's operative
sentence, Derivation B from its falsifier /
outcome side — and disagreements were resolved
in the draft, here. Agreements are recorded in
one line; disagreements in full.

| Claim | Derivation A (from the claim) | Derivation B (from the falsifier/outcome side) | Result |
|---|---|---|---|
| C01 | Inspect outputs for any statement beyond the named-set comparison | Inspect outputs for the excluded statements (language, meaning, unnamed systems, arm B) appearing anywhere | **Agree** — one inspection, both directions; the claim's falsification test is that inspection. |
| C02 | Recompute the claim file's hash and read manual_001's status, evidence, falsifier | Check at close that no Spec 053 product edited the recorded status or exponent | **Agree** — both are required; the claim carries both. |
| C03 | Run §4; hypothesis supported iff every non-linguistic control is strictly worse and P1 passes | Run §4; hypothesis fails if any control is at or below the Indus error (→ C04), and is unadjudicated if P1 fails (→ C12) | **Agree** — the three routes are exhaustive by construction and each is routed to its own claim, not silently to either side. |
| C04 | Outcome record carries NOT SEPARABLE wording when the §4.3 condition holds | If every control is strictly worse, C04's condition does not arise (→ SEPARABLE) | **Agree.** |
| C05 | Inspect the claim record at close: only the dated append added | Any product restating the pooled verdict or status falsifies compliance | **Agree.** |
| C06 | One implementation exhibited for all systems, gate 0.2 self-test passed | A fit quantity from any other estimator (per-system tweaks, a library default) falsifies the record | **Disagreement, resolved (DD-053-3).** A (from the design's "identical Zipf-Mandelbrot estimator") reads it as *Phase-43's* estimator, reused. B (from the record) finds no Phase-43 Zipf estimator pinnable on `main`, and Phase-43's results file records no Zipf fit (§2 verification record) — the identity A wants cannot be exhibited. **Resolution:** identity is preserved where it matters — one estimator, defined in spec §4.2, applied to *every system including the Indus* — and Phase-43 comparability is carried by sensitivity S3 (full-inventory α reported beside the recorded ~1.35). The freeze may substitute a pinned Phase-43 estimator openly, before any fitting (OPEN-053-2); after any fit, never. |
| C07 | Verdict word derivable from the published NRMSE_log values by the ≤ rule | A near-miss control relabelled as firing (or a firing control relabelled as a near miss) falsifies the record | **Disagreement, resolved (DD-053-2).** A (from the falsifier's words "as well **or better**") fixes the rule at ε = 0: a control counts iff its error is ≤ the Indus error. B (from the outcome side) proposes a tolerance band ε = 0.02 *inside* the rule, arguing sampling and counting noise make exact ties arbitrary. **Resolution:** A's literal reading governs the verdict — the design's words carry no band, and a band chosen at draft would decide borderline outcomes by drafter's preference. B's concern is preserved where it cannot decide anything: the band survives as the reporting-only NEAR MISS rule (§4.3 rule 4), so a control 0.01 worse than the script is named in every product, not buried. OPEN-053-5 asks the freeze to confirm ε = 0 or to set a band openly, before fitting. |
| C08 | Step-0 record exhibits the frozen tables with citations before any fit | A set differing from the named set, or a fit preceding the freeze, breaks the gate (→ CONTROL SET FREEZE FAILED) | **Disagreement, resolved (DD-053-6).** A (from the design's "a synthetic emblem inventory generated under a stated random process") reads the simplest stated process: uniform-random assignment of tokens to types. B (from the residue's point) objects that a uniform process is near-flat by construction — it *cannot* fit a Zipf curve, so as a control it is vacuous: the residue's warning is that some random processes *do* produce this curve. **Resolution:** the synthetic control is a Yule–Simon process (innovation ρ = 0.10, seed and size-matching pinned in gate 0.4), the standard stated random process whose output is a power-law rank distribution; the uniform process is recorded here as the considered-and-refused alternative. OPEN-053-6 asks the freeze to confirm the process and its parameters. |
| C09 | Gate 0.3 pins the layer; the primary's V and N equal the strict census | A primary fitted on any other population (e.g. the full inventory) falsifies the record | **Disagreement, resolved (DD-053-4).** A (from Yadav's original test) reads "the Indus fit" as the full-inventory V3 distribution — the population the recorded 1.35 came from. B (from the design text and D-03/D-04 usage) reads "the Indus **strict corpus**" as the strict sign set's distribution, the population every sibling design in this file means by the phrase. **Resolution:** B governs the primary — the design and the campaign brief both name the strict corpus as arm A's input, and a draft does not override its design's named population. A's population is preserved as sensitivity S3, reported beside the recorded exponent, so the comparability A wants is in the record without changing the registered primary. The freeze confirms or overturns this openly (OPEN-053-1 includes the population question). |
| C10 | Gate verdicts precede quantities in the run record, in order | Any quantity preceding its gate falsifies compliance | **Agree** — with the floors noted as draft-fixed values (DD-053-7): neither derivation could ground 50 types / 2,000 tokens in the design (it states none); they are set from the strict set's size (94 candidate types) as the smallest census on which a rank–frequency comparison over ≥3 controls is not decided by a handful of types, and OPEN-053-4 puts them to the freeze. |
| C11 | All three sensitivity tables present at close | A headline following a sensitivity instead of the §4 primary falsifies the boundary | **Disagreement, resolved (DD-053-9).** A (from the design's "corpus subsampling (halving, quartering)") reads token-level subsampling: draw half / a quarter of the tokens. B (from the corpus's structure) objects that tokens are not independent units — token sampling fabricates inscriptions that never existed and understates the exponent's true movement. **Resolution:** inscription-level sampling (whole inscriptions drawn without replacement; their strict tokens follow), which is what "corpus subsampling" means for a corpus of texts. |
| C12 | P1's row in the per-system table is strictly below every non-linguistic row, or the headline is COMPARISON UNINFORMATIVE | A separability headline on a table where P1 fails falsifies the record | **Agree** — with one draft addition recorded: the design names no word for this case; COMPARISON UNINFORMATIVE is this draft's fail-closed completion (DD-053-5), following Spec 042's NOT ADJUDICATED precedent. |
| C13 | Headline derivable from gate record + tables alone | Headline must match §6's pre-written wording for its class | **Agree** — the step-0 closure classes (TOO THIN / STRICT CORPUS NOT PINNABLE / CONTROL SET FREEZE FAILED / INVALID) are this draft's fail-closed completion of the design's unstated outcome set (DD-053-1). |
| C14 | Inspect products: no arm B design, registration, or quantity anywhere | Any arm B execution under this spec falsifies the campaign's E-3 rule | **Agree.** |
| C15 | Inspect outputs for language/meaning/completeness claims | A separable fit presented as language evidence falsifies compliance | **Agree** — one inspection, both directions. |

## 4. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   spec §2 pin re-asserted against the merged
   record — or decline, leaving
   `yadav_2009_arxiv_manual_001` with its
   recorded fit and no strength label: the
   residue exactly as its not-understood text
   states it.
2. **OPEN-053-1 (strict corpus).** Confirm
   gate 0.3's identify-export-pin procedure
   and DD-053-4's population reading (strict
   distribution primary; full inventory as
   S3), or name the layer and its pin in the
   freeze record itself. The draft could not
   pin the layer (spec §2); the freeze must
   not proceed on an unidentified corpus.
3. **OPEN-053-2 (estimator).** Confirm spec
   §4.2's estimator (grid, refinement,
   normalisation, self-test tolerances) as the
   fitting rule of record — or substitute a
   pinned Phase-43 estimator, if the freeze
   identifies one on the record, openly and
   before any fitting (DD-053-3).
4. **OPEN-053-3 (control sources).** Confirm
   the exact published sources, editions, and
   tables for N1 (Mesopotamian numerical
   signs), N2 (heraldic charges), and P1
   (Linear B), with the per-count locator
   form gate 0.4 requires — or replace a named
   system openly, with its source, before any
   counting. The draft names systems and
   bibliographic pins; it does not invent
   tables it has not seen (§6, defect 4).
5. **OPEN-053-4 (floors).** Confirm or adjust
   DD-053-7's census floors (≥50 distinct
   strict types, ≥2,000 strict tokens), before
   any census is taken under them.
6. **OPEN-053-5 (comparison rule).** Confirm
   DD-053-2 (verdict rule ε = 0; the 0.02 band
   reporting-only) or set a band inside the
   rule, openly, before any fitting.
7. **OPEN-053-6 (synthetic process).** Confirm
   DD-053-6's Yule–Simon process and its
   parameters (ρ = 0.10, seed 20261021,
   99 replicates, token total matched at
   gate 0.5) or pin a different stated process,
   before any generation.
8. **OPEN-053-7 (OSF).** Whether the frozen
   spec files its own OSF registration — under
   campaign decision E-1, every specification
   in the pass gets its own OSF contract
   registration at its freeze, so the proposal
   is **yes**, following Specs 036–039. Nothing
   is filed at draft.
9. **OPEN-053-8 (phase number).** Allocate the
   execution phase number at the freeze act,
   from the merged record as it then stands
   (DD-053-8).

## 5. Arm B — contingent status (campaign E-3)

Arm B is the identical fit on a corpus
independent of the Mahadevan lineage, with the
sign inventory fixed in advance. Its trigger
is the campaign's shared trigger: genuinely
new, independent inscription data entering
through Phase-130 intake — the event the
weekly data watch already tests for. The
record at this draft: the 2026-10-08 sweep
found no independent corpus in hand, and the
2026-10-20 re-tests closed both newly arrived
candidate datasets as ICIT-lineage on
provenance, so the precondition stands unmet.

Under E-3, approved as written, a fired trigger
does **not** enlarge this pass and does **not**
attach arm B to this spec: it queues a mini
planning gate of its own. This draft therefore
records the contingency (here and in claim
F053-C14) and does nothing more with arm B —
no design, no registration, no execution
shape. Any future arm B spec starts from that
gate, not from this draft.

## 6. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-053-1 — The outcome set is completed
  fail-closed.** Design D-07 names its
  conclusion only as "a stated comparison."
  The draft fixes the adjudicated words
  (SEPARABLE / NOT SEPARABLE / COMPARISON
  UNINFORMATIVE) and the step-0 closure classes
  (TOO THIN / STRICT CORPUS NOT PINNABLE /
  CONTROL SET FREEZE FAILED / INVALID) with
  §6 wordings — the Spec 042 DD-042-3 /
  Spec 044 DD-044-1 precedent.
- **DD-053-2 — "Fits as well" carries no
  tolerance band in the verdict rule.** ε = 0;
  the 0.02 band is reporting-only (NEAR MISS).
  (§3 derivation C07; OPEN-053-5.)
- **DD-053-3 — The spec defines its own
  estimator.** §4.2's deterministic
  grid estimator is the fitting rule of record
  for every system; Phase-43's estimator is
  not pinnable at draft. (§3 derivation C06;
  OPEN-053-2.)
- **DD-053-4 — "Strict corpus" means the
  strict sign set's distribution.** Primary
  population per D-03/D-04 usage; the full
  inventory is sensitivity S3. No file pin is
  stated for the corpus layer at draft; gate
  0.3 pins it fail-closed (Spec 048
  precedent). (§3 derivation C09; OPEN-053-1.)
- **DD-053-5 — COMPARISON UNINFORMATIVE is
  the positive-control-failure class.** A
  measures finding, never folded into a
  separability word. (§3 derivation C12.)
- **DD-053-6 — The synthetic control is a
  pinned Yule–Simon process.** ρ = 0.10, seed
  20261021, 99 replicates, token total matched
  to the Indus strict total; its fit quantity
  is the replicate median, with the full
  distribution and the as-well share reported.
  (§3 derivation C08; OPEN-053-6.)
- **DD-053-7 — Census floors are draft-fixed
  at 50 types / 2,000 tokens.** The design
  states no floors; these are the smallest
  census the draft will let a rank–frequency
  comparison stand on. (OPEN-053-4.)
- **DD-053-8 — No execution phase number at
  draft.** Allocated at the freeze act.
- **DD-053-9 — Subsampling is at inscription
  level.** (§3 derivation C11.)
- **DD-053-10 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today (the
  Spec 042 DD-042-4 precedent).

## 7. Design defects and ambiguities found at drafting

Recorded per the campaign rule that a defect
is reported, never repaired silently:

1. **The design never defines "fits as well."**
   No fit-quality measure, no margin, and no
   tie rule is stated anywhere in D-07 — the
   falsifier cannot fire mechanically until a
   draft supplies all three. Supplied at spec
   §4 (NRMSE_log; ε = 0; the synthetic median
   rule); DD-053-2; OPEN-053-5 puts the margin
   question to the freeze explicitly.
2. **"The identical Zipf-Mandelbrot estimator"
   has no pinnable referent on the record.**
   Phase-43's results file exists and is
   pinned (spec §2), but it records no Zipf
   fit, and no Phase-43 Zipf estimator is on
   `main` to be identical *to* (§2
   verification record); the only Zipf results
   file in `reports/` is Phase-31's older
   slope record. A draft that claimed
   Phase-43 identity would be claiming a
   fitting rule it cannot exhibit. Handled by
   DD-053-3 and OPEN-053-2; if the freeze
   also cannot pin Phase-43's estimator,
   §4.2's estimator stands and the recorded
   ~1.35 remains context, exactly as spec
   §4.2 states.
3. **"The Indus strict corpus" is ambiguous
   against Yadav's population.** The original
   fit (and the recorded exponent) is over the
   full V3 inventory; the design's phrase, in
   its own file's usage, means the strict
   subset. The two populations give different
   curves, and the design does not acknowledge
   the difference. Handled by DD-053-4 (strict
   primary, full inventory as S3) so both
   numbers are in the record and neither is
   quoted as the other.
4. **The example controls name systems, not
   sources.** "Heraldic charge frequencies"
   and "Mesopotamian numerical-sign frequencies
   from published counts" cite no roll, no
   edition, and no table; the counts therefore
   cannot be pinned at draft without inventing
   citations. Handled by gate 0.4's cited-data
   freeze, the CONTROL SET FREEZE FAILED
   closure, and OPEN-053-3. If the freeze finds
   a named system has no complete published
   count set the program can lawfully enter,
   the honest outcomes are an openly replaced
   system at freeze or that closure at
   execution — never a quietly reduced set.
5. **The design's synthetic example ("a stated
   random process") does not say which
   process, and the choice decides the
   control's force.** A uniform process is
   vacuous; a Yule–Simon process is the
   residue's actual warning. Handled by
   DD-053-6 with the refused alternative on
   the record (§3, C08); OPEN-053-6.
6. **The design states no census floors and
   no positive-control failure mode.** Both
   had to be supplied at draft (DD-053-7,
   DD-053-5) so the run can close honestly
   instead of improvising at execution;
   OPEN-053-4 and §4 of this record put both
   to the freeze.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 8. Freeze decisions (2026-10-21)

Decided at the freeze act under the
runnable-experiments campaign plan approved by
the owner AS WRITTEN on 2026-10-21 (Wave 2
freeze wave; decision E-1 governs the OSF
filing). Every §2 pin was re-asserted in the
foreground by two independent routes — the
contents-API raw route and the git-blob route,
agreeing byte-for-byte — at `main` head
`3af269f660a9368e898cdece41132200d31b87cc`:
claim file SHA-256 `90476623…` (13,230 bytes),
anchors `df0cf620…` (570,344 bytes; census
re-read: 287 anchors, 94
`strict_sa_independent`), crosswalk
`4ace1a61…`, Mahadevan–Parpola crosswalk
`9ebd7723…`, and Phase-43 results
`78a6c219…` (15,047 bytes). The claim file's
hash is carried as a freeze definition
constant in the Spec 038 form: the
extracted-claims store is regenerated by the
backend suite, so the freeze tests assert the
constant plus the `manual_001` facts on the
live file, never a live-file hash on that
store.

- **DD-053-11 — The estimator ruling
  (OPEN-053-2): option (a) adopted; the
  Phase-43 identity reading is RETIRED.**
  Reasoning, on the record. (1) The freeze
  re-verified the draft's central finding
  first-hand: `outputs/phase43_all.json`
  (SHA-256
  `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4`)
  was re-read in full and contains no Zipf fit
  at all — no exponent, no Mandelbrot
  parameters, no fitting procedure, not even
  the word "Zipf" — and no Phase-43 Zipf
  estimator script is on `main`. Yadav's
  recorded value of about 1.35 rests on the
  claim file's evidence string alone
  ("Phase-43: V3 Zipf exponent ~1.35
  (super-Zipfian)"), verified on the pinned
  claim file at this freeze. There is
  therefore no Phase-43 estimator for this
  spec to be identical *to*; a freeze that
  claimed that identity would be claiming a
  fitting rule it cannot exhibit. (2) The
  falsifier does not need one: it fires iff a
  named non-linguistic control fits **as well
  as or better than the Indus strict corpus**
  under §4's one estimator (§1.2, §4.3) — a
  comparison internal to this spec, between
  systems fitted by the same code in the same
  run. It never compared anything against a
  Phase-43 fit, and the recorded 1.35 enters
  only as context (spec §4.2, §5 S3, limit 4).
  Option (b) — freeze failure — therefore does
  not arise: the central comparison is fully
  defined without the retired identity.
  (3) The freeze accordingly **specifies the
  estimator completely as a freeze-stage
  design decision**: the Zipf-Mandelbrot model
  f̂(r) = C / (r + q)^α with C fixed by
  normalisation (Σ f̂(r) = N, not a free
  parameter); fitting by minimising the sum of
  squared log residuals over the deterministic
  grid α 0.00–3.00 in steps of 0.01 and
  q 0.0–20.0 in steps of 0.1, then one
  refinement pass at one-tenth steps in α and
  q around the best grid cell; types ranked by
  count descending, ties by type identifier
  ascending; the primary quantity NRMSE_log =
  √(SSE / V), with log-space R² and the fitted
  α and q reported and never decisive; the
  gate 0.2 self-test on synthetic data
  generated from α = 1.20, q = 2.0, V = 200,
  N = 50,000, seed 20261021, by the stated
  multinomial procedure, passing iff the fit
  recovers α within ±0.10 and q within ±1.0;
  the synthetic control N3 as a Yule–Simon
  process (ρ = 0.10, seed 20261021, 99
  replicates, token total size-matched at gate
  0.5, replicate median as its fit quantity);
  and the sensitivities' seeds and replicate
  counts as stated in §5 (S1: 99 replicates per
  level, seed 20261021, inscription-level).
  The spec's claims and falsifier are restated
  to say exactly this — the spec tests Yadav's
  recorded 1.35 value under this named
  estimator, as context, not as a reproduction
  target (F053-C02, C06, C11 as edited at this
  freeze, before the digest; claim IDs
  stable). No estimator substitution is
  possible after any fitting.
- **DD-053-12 — Strict corpus and population
  (OPEN-053-1): confirmed as drafted.**
  Gate 0.3's identify-export-pin procedure
  stands, and DD-053-4's population reading
  stands: the strict sign set's distribution
  is the primary; the full inventory is
  sensitivity S3 only. The freeze names no
  file pin for the corpus layer, deliberately
  (the Spec 048 precedent): the layer is a
  database posture, and gate 0.3 closes the
  run STRICT CORPUS NOT PINNABLE if it cannot
  be uniquely identified, exported whole, and
  shown to be the Phase-43 framework's corpus
  family. The freeze does not proceed on an
  unidentified corpus — gate 0.3 is exactly
  that guarantee, at execution, before any
  fit.
- **DD-053-13 — Control sources (OPEN-053-3):
  the named systems and bibliographic pins
  stand; gate 0.4 is the fixed pin source for
  the control tables.** N1 Mesopotamian
  numerical signs from Nissen, Damerow &
  Englund, *Archaic Bookkeeping* (1993) and
  the published archaic sign counts it
  reports; N2 heraldic charges from a
  published roll of arms; P1 Linear B syllabic
  sign frequencies from published corpus
  counts; N3 as pinned in DD-053-11 /
  DD-053-16. No second positive control is
  added. The exact tables, editions, and
  per-count locators are entered as cited data
  at gate 0.4 — before any fit, the Indus
  included — and a system that cannot be
  entered whole there closes the run CONTROL
  SET FREEZE FAILED. The freeze invents no
  table it has not seen (§7, defect 4): what
  the freeze fixes is the systems, the
  sources, the counting units (gate 0.4 as
  drafted), and the fail-closed gate that is
  the tables' pin source.
- **DD-053-14 — Census floors (OPEN-053-4):
  confirmed.** ≥ 50 distinct strict types
  present and ≥ 2,000 strict tokens
  (DD-053-7 as drafted).
- **DD-053-15 — Comparison rule (OPEN-053-5):
  confirmed.** DD-053-2 stands: the verdict
  rule carries no tolerance band (ε = 0;
  a control fits as well iff its NRMSE_log is
  at or below the Indus value, the synthetic
  control by its replicate median); the 0.02
  band is reporting-only (NEAR MISS).
- **DD-053-16 — Synthetic process
  (OPEN-053-6): confirmed.** DD-053-6 stands:
  Yule–Simon, ρ = 0.10, seed 20261021, 99
  replicates, token total matched to the
  Indus strict total at gate 0.5; the uniform
  process stays refused on the record (§3,
  C08).
- **DD-053-17 — OSF (OPEN-053-7): yes.**
  Under campaign decision E-1, this spec files
  its own OSF contract registration at its
  freeze, following Specs 036–039 and 042–051
  (`osf-spec-registration.md`, completed by
  append after filing). Nothing was filed at
  draft.
- **DD-053-18 — Phase number (OPEN-053-8):
  Phase-413 allocated** at this freeze, from
  the merged record as it stands.
- **DD-053-19 — The AEE gate reading.**
  The DD-038-10 / DD-037-9 reading is adopted:
  the lifecycle hooks pass at a freeze when,
  at every hook, there are zero correctness
  failure modes and no claim below the 0.70
  threshold; the engine's "iterate" outcome
  word, driven solely by the FR-2.3 draft-cap
  records a draft register necessarily
  carries, does not block the freeze. The
  hooks' record for this spec is in
  `aee/freeze-aee-note.md`. The one
  negation-conflict challenge raised over the
  recovered register (F053-C01 / F053-C04) was
  adjudicated at the freeze as no
  contradiction — C04 is the NOT SEPARABLE
  branch of C01's scope statement; the two
  share a boundary by design — and is
  recorded in C04's boundary and the AEE note.
  COMPARISON UNINFORMATIVE (DD-053-5) is also
  confirmed at this freeze as the
  positive-control-failure class.

DD-053-1 (fail-closed outcome set), DD-053-3
(the spec defines its own estimator — now
ruled completely in DD-053-11), DD-053-8 (phase
allocated at freeze — discharged by
DD-053-18), DD-053-9 (inscription-level
subsampling), and DD-053-10 (`observed_at`
from the draft) stand as drafted and are not
re-asked.
