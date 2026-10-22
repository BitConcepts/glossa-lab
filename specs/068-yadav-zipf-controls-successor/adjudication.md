# Spec 068 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-22
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The Shakti readiness assessment**
>    (`~/workspace/research_notes/shakti-readiness-proposals-2026-10-22.md`,
>    §§1.5–1.6 read first-hand at this draft).
>    Section 1.5 finds Spec 053 the one
>    transferable member of the Item-1 successor
>    chain, with named amendment, and drafts
>    the amendment's wording (Amendment S-053,
>    quoted in full in spec §2.1); §1.6 drafts
>    the corpus's own intake gates (Proposal
>    P-F1, gates S1–S4). The assessment is
>    proposals only; what makes its §1.5/§1.6
>    proposals operative for this draft is
>    input 2.
> 2. **The owner's 2026-10-22 readiness
>    decisions, decision 2.** Decision 2
>    approves drafting a successor to Spec 053
>    on the Shakti corpus under Amendment
>    S-053: a new spec with a new OSF
>    registration, a documented-lineage-only
>    primary fit with the documented +
>    corroborated fit reported as a sensitivity,
>    the strict-sign-set choice ruled at the
>    successor's freeze, and — decision 2c,
>    accepted on the record — the result stated
>    as a new baseline that neither confirms
>    nor corrects Phase-43. Drafts are
>    pre-approved standing in this program; the
>    freeze, the execution, and the OSF
>    registration are separate later owner
>    acts.
> 3. **Spec 053's frozen record**
>    (`specs/053-yadav-zipf-controls/spec.md`
>    and `adjudication.md` on `main`, read
>    first-hand at this draft). Spec 053 froze
>    on 2026-10-21 under the runnable-experiments
>    campaign (freeze decisions DD-053-11 to
>    DD-053-19), executed as Phase-413, and
>    closed at its step-0 gate 0.3 as STRICT
>    CORPUS NOT PINNABLE, with no fit computed.
>    Its DD-053-11 estimator ruling is this
>    successor's estimator authority (§1). Its
>    record and its closure stand; this
>    successor does not re-open them.
>
> These inputs commission this **draft**. The
> freeze and the execution of Spec 068 are
> separate later owner acts. No AEE lifecycle
> hooks have run on this draft; they are a
> freeze gate, on the DD-038-10 posture for
> draft registers.

## 1. The adopted basis (operative substance)

- **The question.** Spec 053's, unchanged
  (design D-07, arm A): what is a
  Zipf-Mandelbrot curve fit worth — the same
  frozen estimator fitted to the Indus
  distribution and to named non-linguistic
  controls plus a linguistic positive control.
  The product is a strength label for the
  settled claim `yadav_2009_arxiv_manual_001`,
  not a new verdict on it.
- **The estimator.** Spec 053's, as frozen.
  DD-053-11 specified it completely at that
  freeze as a freeze-stage design decision —
  model f̂(r) = C / (r + q)^α with C fixed by
  normalisation (Σ f̂(r) = N); objective the
  sum of squared log residuals; grid α
  0.00–3.00 in steps of 0.01, q 0.0–20.0 in
  steps of 0.1; one refinement pass at
  one-tenth steps in α and q around the best
  grid cell; ranking by count descending, ties
  by type identifier ascending; primary
  quantity NRMSE_log = √(SSE / V); the gate
  0.2 self-test on synthetic data generated
  from α = 1.20, q = 2.0, V = 200, N = 50,000,
  seed 20261021, passing iff α is recovered
  within ±0.10 and q within ±1.0 — and
  honestly **RETIRED** the "identical to
  Phase-43" reading, because the Phase-43
  results file contains no Zipf fit at all and
  no Phase-43 Zipf estimator exists on the
  record. This successor's estimator identity
  is identity with that freeze (claim
  F068-C07), and with nothing else.
- **The controls.** Spec 053 gate 0.4's set,
  as frozen and confirmed at DD-053-13: N1
  Mesopotamian numerical signs (Nissen,
  Damerow & Englund, *Archaic Bookkeeping*
  (1993)); N2 heraldic charges from a published
  roll of arms; N3 the synthetic emblem
  inventory (Yule–Simon, ρ = 0.10, seed
  20261021, 99 replicates, size-matched,
  replicate median — DD-053-6, confirmed
  DD-053-16); P1 Linear B syllabic sign
  frequencies. No system is new, added,
  substituted, or dropped in this draft.
- **The comparison rule and outcome words.**
  Spec 053 §§4.3–4.5, confirmed at DD-053-15
  (ε = 0; the 0.02 band reporting-only as
  NEAR MISS) and DD-053-19 (COMPARISON
  UNINFORMATIVE as the positive-control-failure
  class): SEPARABLE / NOT SEPARABLE /
  COMPARISON UNINFORMATIVE, with pre-written
  wordings carried into spec §7 and re-pointed
  at this spec's corpus and fence.
- **The floors.** Spec 053 gate 0.5's: at
  least 50 distinct types and at least 2,000
  tokens (DD-053-7, confirmed DD-053-14),
  carried by Amendment S-053 and measured on
  this successor's restricted set (spec §4,
  gate 0.7).
- **The corpus substitution.** Amendment
  S-053 (spec §2.1, quoted in full): the
  Indus distribution of record is the
  ShaktiOSindia corpus as graded in the
  provenance audit of 2026-10-22, restricted
  to documented-lineage rows for the primary
  fit, with the documented + corroborated fit
  as a reported sensitivity, the
  undocumented-uncorroborated rows in no fit,
  and the strict-sign-set bracket carried open
  to the freeze (OPEN-068-1).
- **The intake gates.** Proposal P-F1's S1–S4
  (spec §§2.1, 4, 6.1, 10): both SHA-256 pins
  recompute (S1); the audit census reproduces
  (S2); every product carries the lineage
  statement in its headline block (S3); grade
  discipline, with a difference between the
  grade sets reported as grade-sensitivity
  (S4). Failure of S1 or S2 closes the citing
  spec at step 0 as SHAKTI INTAKE NOT
  REPRODUCED.
- **The falsifier.** Spec 053's, unchanged in
  substance: at least one named non-linguistic
  control fits as well as or better than the
  Indus primary fit under the one estimator —
  "as well" mechanical at ε = 0 on NRMSE_log.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-22,
via the GitHub API against `main` and from the
research-notes files named; the local checkout
at `~/workspace/glossa-lab` was **not** used
(it is behind and dirty, and this draft was
built in a fresh worktree from `origin/main`):

- **`origin/main` head** —
  `2a0eb854982f52453bcd76fd4a5bcbb088eb21e8`,
  verified through the GitHub API at this
  draft and matching the drafting commission's
  stated head. Spec 053's directory and the
  Spec 054 draft branch (below) were read
  against this record.
- **Spec 053's frozen spec** — read in full
  from `main`: the claim and its residue (§1),
  the inputs and their pins (§2), the step-0
  gates 0.1–0.5 (§3), the estimator (§4.2: the
  grid, objective, normalisation, ranking, and
  primary quantity stated in claim F068-C07),
  the comparison rule (§4.3: ε = 0, the median
  rule for N3, the NEAR MISS reporting band),
  the positive-control condition (§4.4), the
  headline rule (§4.5), the sensitivities
  (§5), the pre-written outcome wordings (§6),
  the limits (§7), the reporting obligations
  (§9), and the arm-B exclusion (§12).
- **Spec 053's adjudication, including
  DD-053-11** — read in full from `main`: the
  draft-stage decisions DD-053-1 to DD-053-10
  (including DD-053-2's ε = 0 reading,
  DD-053-4's strict-population reading,
  DD-053-6's Yule–Simon ruling, and DD-053-7's
  floors) and the freeze decisions §8,
  DD-053-11 to DD-053-19 — DD-053-11's
  estimator ruling in its full reasoning (no
  Phase-43 Zipf fit exists in the Phase-43
  results file `outputs/phase43_all.json`,
  SHA-256 `78a6c219…`, read in full at that
  freeze; Yadav's recorded value of about 1.35
  rests on the claim file's evidence string
  alone), DD-053-12 (gate 0.3 and the strict
  population), DD-053-13 (control sources;
  gate 0.4 as the control tables' pin source),
  DD-053-14 (floors), DD-053-15 (ε = 0),
  DD-053-16 (Yule–Simon), DD-053-17 (OSF),
  DD-053-18 (Phase-413), and DD-053-19 (the
  AEE gate reading adopting DD-038-10).
  Spec 053's execution record (its tasks file
  and outcome, on `main`): gate 0.3 FAILED —
  STRICT CORPUS NOT PINNABLE — gate 0.4 not
  reached, no control count entered, no fit
  computed.
- **The readiness assessment §§1.5–1.6** —
  read first-hand in full: §1.5's Spec 053
  entry (the frozen gate 0.3 quoted; the three
  facts that make 053 the one transferable
  member; what does not transfer — the strict
  sign set's keying and the Phase-43 exponent;
  Amendment S-053's full draft wording,
  quoted verbatim in spec §2.1, including its
  row arithmetic note: 3,212 + 2,087 = 5,299;
  analyzable 3,045 + 2,086 = 5,131, the one
  all-`000` corroborated row H-986 being in the
  2,087 but not the analyzable subset) and
  §1.6's Proposal P-F1 in full (the corpus pin
  stated in full there; S1–S4 as spec §2.1
  states them; the SHAKTI INTAKE NOT
  REPRODUCED closure).
- **The provenance audit** — read first-hand:
  the corpus file and its verified pin
  (`sanitized_corpus.json`, SHA-256
  `345241b1…` in full at spec §2.1); the
  documented figure reproduced exactly under
  the deposit's stated rule (3,212 of 5,704 =
  56.31%; 3,045 of the 5,536 analyzable); the
  unmatched stratum's systematic differences
  (§2 of the audit — the basis of spec §9's
  grade-composition confounder); the §3
  lineage-layer census and its caveat (the
  source of P-F1 S3's statement); the grades
  and per-grade verdicts (§4: documented
  cleared for working use; corroborated usable
  with the caveat carried; uncorroborated not
  usable), including the 167 entirely-`000`
  documented rows and the all-`000`
  corroborated row H-986, both excluded from
  sign analysis.
- **The draft form mirrored** — Spec 054's
  draft (`specs/054-yadav-opening-closing/` on
  branch `spec-054-yadav-opening-closing-draft`,
  PR #260, still open and unmerged), read
  first-hand at this draft: file set (spec.md,
  claims.json, adjudication.md, tasks.md —
  exactly this draft's file set), the DESIGN
  DRAFT banner posture (commissioning authority
  quoted; drafts pre-approved standing; freeze
  and execution as separate later owner acts;
  no AEE hooks run, as a freeze gate; execution
  phase number unassigned at draft), the
  register form (`register_version`
  `0.5-draft`, claims at status `draft`,
  `observed_at` carried on evidence), and the
  adjudication/tasks structure this record and
  `tasks.md` follow. Spec 054's later freeze
  failure is its own record and has no bearing
  on this draft's substance; only its draft
  form is mirrored.
- **The intake record — NOT YET ON `main`.**
  `docs/decisions/2026-10-22-shakti-corpus-intake-record.md`
  does not exist on `main` at head `2a0eb854…`
  (checked at this draft; the `docs/decisions`
  path is absent). It is being created in
  parallel. This draft therefore cites it by
  that path as the standing record the freeze
  will assert against (spec §3), states both
  pins in full in spec §2.1 — the corpus pin
  from P-F1 §1.6 and the audit, the row-grades
  pin `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`
  as recorded for that intake record — and
  makes the intake record's presence on the
  merged record a freeze condition
  (OPEN-068-2). Nothing in this draft asserts
  the intake record exists yet.
- **Not done at draft, by design** — no corpus
  file was opened or counted by this draft, no
  census was computed, no mapping was stated,
  no control count was entered, no fit of any
  system was computed, no synthetic inventory
  was generated, no code was written or run,
  the strict-set limb was **not** chosen, the
  AEE hooks have not run, and nothing was
  filed with OSF.

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
| C01 | Inspect outputs for any statement beyond the named-set comparison on the restricted corpus | Inspect outputs for the excluded statements (language, meaning, unnamed systems, V3 population, Phase-43 quantities) appearing anywhere | **Agree** — one inspection, both directions; the claim's falsification test is that inspection. |
| C02 | The freeze record states one limb; step 0 exhibits the population that limb defines | A fit measured on a population following neither limb, or on a limb chosen after the census, is not a fit under this spec (→ gate 0.5 closes the run) | **Disagreement, resolved (DD-068-1).** A initially read Amendment S-053's bracket as a step-0 choice, since the amendment says the mapping is "pinned at step 0" under the retained limb. B, from the amendment's own closing sentence ("the successor's freeze must choose one and record the choice; it may not proceed with the choice unstated") and the owner's decision 2 (the choice is "ruled at its freeze"), read the *choice* as the freeze's and only the *mapping act* as step 0's. **Resolution:** B governs. The freeze chooses and records the limb (and, under limb A, names the mapping's basis source); step 0 performs and pins the act the chosen limb requires; a freeze record stating no limb closes any execution at gate 0.5 as INVALID. Both limbs are drafted in full (spec §2.2) so the freeze is choosing between complete texts, not commissioning one. |
| C03 | Recompute the claim file's hash and read manual_001's status and evidence | Check at close that no Spec 068 product edited the recorded status or exponent, and that a step-0 closure added no label | **Agree** — both are required; the claim carries both. |
| C04 | Run §5; hypothesis supported iff every non-linguistic control is strictly worse on the primary and P1 passes | Run §5; hypothesis fails if any control is at or below the Indus primary error (→ C10), and is unadjudicated if P1 fails (→ C10) | **Agree** — the three routes are exhaustive by construction and each is routed to the verdict claim, not silently to either side. The sensitivity fit is not a fourth route: its ordering is reported under C11 and adjudicates nothing here. |
| C05 | Recompute both digests at step 0 against the intake record | A run proceeding on a file whose digest differs in any digit has fitted a corpus the audit did not grade (→ SHAKTI INTAKE NOT REPRODUCED) | **Agree.** One sharpening from B is carried: the gate is asserted *against the intake record*, not against this draft — so the freeze must first assert the draft's pins against the intake record standing on the merged record (OPEN-068-2). |
| C06 | Gate 0.4 reproduces the audit census and states the successor's own restricted census | Derived draft figures quoted as the measurement would let a population difference between the audit's corpus and the executed corpus pass silently (→ census governs over derived figures, stated in the claim) | **Agree** — with DD-068-2 recorded: neither derivation could ground the floors on any population but the restricted set's fit population, since Amendment S-053 carries Spec 053's floors "measured on the restricted set"; under limb A that is the mapped-strict population over the documented rows, under limb B the full inventory of the documented rows. The gate states both the restricted census and the fit-population counts, so the measurement the floors turn on is exhibited either way. |
| C07 | One implementation exhibited for all systems, gate 0.2 self-test passed, its constants equal to DD-053-11's statement | A fit quantity from any other estimator (per-system tweaks, a re-derived rule for the ICIT population, a library default) falsifies the record | **Disagreement, resolved (DD-068-3).** A read "the same frozen estimator" in Amendment S-053's question statement as identity with the estimator of record for the *claim* — and went looking, as Spec 053's draft did, for a Phase-43 estimator to be identical to. B found DD-053-11 already settled that search: no Phase-43 estimator exists, the identity reading was retired at Spec 053's freeze, and the estimator was specified completely there as the fitting rule of record. **Resolution:** B governs, and it is not a close call — identity in this successor is identity with Spec 053's freeze, stated constant by constant in the claim; the retired Phase-43 reading is not revived by the substitution, and §6 defect 2 records why a draft that claimed it would be claiming a rule it cannot exhibit. |
| C08 | Step-0 record exhibits the frozen tables with citations before any fit | A set differing from the named set, or a fit preceding the freeze of the tables, breaks the gate (→ CONTROL SET FREEZE FAILED) | **Agree** — with the Spec 053 posture carried whole (DD-053-13): gate 0.6 is the fixed pin source for the tables; the draft names systems, sources, and counting units and invents no table. |
| C09 | Gate verdicts precede quantities in the run record, in order | Any quantity preceding its gate falsifies compliance | **Agree.** |
| C10 | Headline derivable from the published primary NRMSE_log values by the ≤ rule and the P1 condition alone | A headline following the sensitivity fit, or a near-miss control relabelled either way, falsifies the record | **Disagreement, resolved (DD-068-4).** A (from P-F1 S4's both-ways reporting) at first read a differing sensitivity ordering as changing the headline — the result "changes between the two", so arguably the headline should be the combined fit's, or no headline should stand. B (from Amendment S-053's own sentence: the sensitivity "is reported alongside the primary fit") read the primary as the verdict population throughout: the amendment makes the documented fit primary in terms, and S4's remedy for a difference is *reporting* — both fits, neither suppressed, the difference named grade-sensitivity wherever cited — not a verdict transfer. **Resolution:** B governs. The headline is the primary's (spec §5.5); a differing sensitivity ordering attaches the grade-sensitivity statement to the headline in every product (§6.1 rule 3), with the same prominence, and both orderings are exhibited in full. Either of A's readings would leave the verdict population undecided until after the fits exist, which is the discretion the gates exist to refuse. |
| C11 | Both fits reported in full, both orderings exhibited, the 405 rows in no fit | A product quoting only the fit that supports its reading, or quoting the headline without the grade-sensitivity statement where the orderings differ, falsifies compliance | **Agree** — with the audit's stratum finding carried as the reason the claim's boundary states the combined fit is a different population, not a larger sample of the same one. |
| C12 | Inspect every product's headline block for the statement, verbatim | A Shakti result quoted anywhere as independent corroboration of an ICIT-lineage result is the failure this gate exists to prevent (→ the statement's absence is an integrity finding, not a formatting defect) | **Agree** — one inspection, judged character-for-character against the text quoted in the claim, which is P-F1 S3's text as read at this draft. |
| C13 | Inspect every input list, gate, and product for Phase-43 quantities in operative positions | Any Shakti quantity quoted as confirming or correcting Phase-43 falsifies the fence, including by juxtaposition (→ no fit reported beside the recorded exponent) | **Agree** — with one point both derivations flagged and the draft states openly: Spec 053 *did* report a fit beside the recorded exponent (its S3 bridge). That was honest there, where the corpus was the V3 population the exponent came from. Here the corpus, the population, and the numbering all differ, so the bridge form itself would misstate what the number is; §6.3 carries the full-inventory fit with no Phase-43 juxtaposition (see §6, defect 3). |
| C14 | File inspection at close: prior content unchanged, appends dated and enumerated | A language claim in any output, or a status restated in place, falsifies compliance | **Agree** — one inspection, both directions. |

## 4. What the freeze decision is asked to decide

1. **OPEN-068-1 (the strict-sign-set limb —
   the principal item).** Choose **limb A**
   (retained: the strict restriction keyed to
   ICIT space by the mapping act of spec §2.2,
   with the mapping's basis source named in
   the freeze record so gate 0.5 has a stated
   basis to pin against) or **limb B**
   (dropped: the population stated as the full
   ICIT sign inventory of the restricted
   corpus) — and record the choice and its
   reasons in the freeze record, in spec
   §2.2's terms. **The draft may not proceed
   past freeze with the choice unstated**;
   there is no third limb and no execution-time
   choice. (Claim F068-C02.)
2. **OPEN-068-2 (the intake record and the
   pins).** Assert, against the merged record
   as it then stands: the intake record
   (`docs/decisions/2026-10-22-shakti-corpus-intake-record.md`)
   stands on it, carrying the P-F1 gates
   S1–S4 in their adopted form and both
   SHA-256 pins exactly as spec §2.1 states
   them — corpus
   `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`,
   row-grades
   `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`
   — and every other spec §3 pin re-asserts
   against the merged record. If the intake
   record does not stand, or carries different
   pins, the freeze does not happen on this
   draft's terms; the discrepancy is reported,
   not adjusted silently.
3. **OPEN-068-3 (the contract as drafted).**
   Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with
   DD-068-1 to DD-068-6 confirmed or openly
   overturned — or decline, leaving Spec 053's
   comparison unrun on any corpus, its
   strength label unwritten, and Spec 053's
   record exactly as it stands.
4. **OPEN-068-4 (AEE lifecycle hooks).** Run
   the hooks as the freeze gate (tasks L4) on
   the DD-038-10 posture for draft registers
   adopted in DD-053-19 — the gate is pass on
   that reading — with any recovery round
   completed and recorded before the freeze
   digest is computed, exactly once, over the
   recovered register.
5. **OPEN-068-5 (control tables).** Confirm
   the DD-053-13 posture carried in claim
   F068-C08: the named systems stand, no
   second positive control is added, and gate
   0.6 is the fixed pin source for the exact
   tables and per-count locators — or replace
   a named system openly, with its source,
   before any counting.
6. **OPEN-068-6 (OSF).** File this spec's own
   OSF contract registration at the freeze —
   the owner's decision 2 commissions the
   successor "as a new spec with a new OSF
   registration", so the proposal is **yes**, a
   new registration for Spec 068, not an
   amendment of Spec 053's. Nothing is filed
   at draft; the registration's approval act
   remains a separate owner act after the
   freeze.
7. **OPEN-068-7 (phase number).** Allocate
   the execution phase number at the freeze
   act, from the merged record as it then
   stands (DD-068-6).

## 5. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-068-1 — The limb choice is the
  freeze's; the mapping act is step 0's.**
  (§3 derivation C02; claim F068-C02;
  OPEN-068-1.)
- **DD-068-2 — The floors are measured on
  the restricted set's fit population.**
  Gate 0.7's population is the one the
  freeze's limb defines over the
  documented-lineage rows; the gate exhibits
  both the restricted census and the
  fit-population counts. (§3 derivation C06;
  claim F068-C06.)
- **DD-068-3 — Estimator identity is identity
  with Spec 053's freeze.** DD-053-11's ruling
  is inherited whole; the retired Phase-43
  identity reading is not revived. (§3
  derivation C07; claim F068-C07.)
- **DD-068-4 — The headline is the primary
  fit's; a differing sensitivity ordering is
  reported as grade-sensitivity beside it.**
  (§3 derivation C10; claims F068-C10,
  F068-C11; spec §§5.5, 6.1.)
- **DD-068-5 — The outcome set is completed
  fail-closed for the new corpus.** To Spec
  053's closure classes (TOO THIN / CONTROL
  SET FREEZE FAILED / INVALID) the successor
  adds the two its own gates require:
  SHAKTI INTAKE NOT REPRODUCED (P-F1's own
  closure word) and STRICT MAPPING NOT
  PINNABLE (limb A's gate 0.5, in the form of
  Spec 053's gate-0.3 closure). STRICT CORPUS
  NOT PINNABLE does not carry over: it named
  the V3 layer's failure, and this spec has
  no V3 gate.
- **DD-068-6 — No execution phase number at
  draft; evidence carries `observed_at` from
  the draft.** The phase number is allocated
  at the freeze act (OPEN-068-7); the cited
  facts were verified first-hand today (the
  Spec 042 DD-042-4 / Spec 054 DD-054-8
  precedent).

## 6. Design defects and ambiguities found at drafting

Recorded per the program rule that a defect is
reported, never repaired silently:

1. **Amendment S-053 leaves its central
   bracket unresolved — by design, and the
   draft must not resolve it.** The
   amendment's closing bracket offers two
   populations that give different curves, in
   different inventories, and the readiness
   assessment and the owner's decision both
   assign the choice to the freeze. A draft
   that picked a limb would be spending an
   owner decision it does not hold; a draft
   that drafted only the limb it expected
   would make the freeze's other choice
   undrafted. Handled by drafting both limbs
   in full (spec §2.2), registering the item
   as a claim with its dependency stated
   (F068-C02), and gating execution on the
   freeze record's stating the choice (gate
   0.5). Recorded here so the freeze package
   cannot mistake the openness for an
   oversight.
2. **"The same frozen estimator" has two
   candidate referents, and only one exists.**
   Read against the claim's history, the
   phrase can point at Phase-43's estimator;
   read against the successor chain, at Spec
   053's freeze. DD-053-11 settled the matter
   on the evidence — no Phase-43 estimator
   exists — but a drafter who read only the
   amendment and the claim record could revive
   the retired reading in good faith. Handled
   by DD-068-3 and claim F068-C07, which state
   the identity constant by constant against
   Spec 053's freeze and name the retired
   reading as retired.
3. **Spec 053's S3 bridge form does not
   transfer, although its estimator does.**
   Spec 053 reported its full-inventory fit
   beside the recorded exponent of about 1.35
   as a comparability bridge to Yadav's
   population. Amendment S-053's fence ("no
   quantity in it is a reproduction of a
   Phase-43 quantity") and decision 2c exclude
   that form here: the bridge would invite
   exactly the reading the fence forbids.
   Handled in spec §6.3: the full-inventory
   fit is carried (limb A only; under limb B
   it *is* the primary) with its exponent
   reported on its own, and the difference
   from Spec 053's S3 is stated in the spec
   text, not left for a reader to miss.
4. **Spec 053's split/merge sensitivity (its
   S2) has no ICIT-space source on the
   record.** S2 built its variants from the
   pinned Mahadevan-space crosswalk's variant
   structure. Amendment S-053 names no
   ICIT-space variant source, and none is
   pinned in this draft; inventing one (or
   carrying Mahadevan variant links across
   numbering spaces by sign number) would
   repeat, inside a sensitivity, the
   number-identity error OPEN-068-1 exists to
   refuse for the primary. The successor
   therefore carries the grade sensitivity
   (§6.1, the amendment's own) and subsampling
   (§6.2, corpus-internal and
   numbering-independent), and does **not**
   carry a split/merge variant fit. If the
   freeze wants one, it must name and pin an
   ICIT-space variant source as a freeze act;
   the absence is recorded here as a stated
   scope limit of the draft, not discovered
   later as a missing deliverable.
5. **The intake record the gates assert
   against does not yet stand on `main`.**
   The amendment quotes the row-grades pin
   only as "as recorded in the successor's
   intake record", and P-F1's adoption itself
   is effected through that record. At this
   draft the record is being created in
   parallel and the `docs/decisions` path is
   absent from `main` (§2 verification
   record). Handled by citing the record by
   its path as the standing record the freeze
   will assert against, stating both pins in
   full from the sources the draft *can* read,
   and making the record's presence and pins
   a freeze condition (OPEN-068-2). If the
   record lands with different pins, this
   draft's gates are wrong on their face and
   the freeze must say so — the draft does not
   quietly become right by the record's
   arrival.
6. **Derived grade arithmetic is one row
   easy to misstate.** The sensitivity set's
   analyzable count is 5,131, not 5,132:
   2,087 corroborated rows include one
   all-`000` row (H-986) that is not
   analyzable, so the analyzable sum is
   3,045 + 2,086. The readiness memo states
   the arithmetic correctly; the draft repeats
   it correctly (§2.1, claim F068-C06) and
   records it here because a reader checking
   3,212 + 2,087 and 3,045 + 2,087 in
   parallel will find the one-row difference
   unexplained anywhere else. The successor's
   own step-0 census governs over all of it.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
