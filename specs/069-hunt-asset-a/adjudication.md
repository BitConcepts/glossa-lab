# Spec 069 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-22
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The owner's readiness decisions of
>    2026-10-22, decision 3** (the Hunt
>    programme, re-scoped). The owner
>    commissioned three new specs in
>    dependency order — this Asset A build
>    first (Spec 069), then the opening-signs
>    successor (Spec 070), then the
>    sky-signs successor (Spec 071). That
>    decision commissions this **draft**.
>    It is not a freeze order, not a
>    registration order, and not an execution
>    order: the freeze, the OSF registration,
>    and the execution of Spec 069 remain
>    separate later owner acts.
> 2. **The Shakti readiness assessment of
>    2026-10-22**
>    (`~/workspace/research_notes/shakti-readiness-proposals-2026-10-22.md`,
>    §1.5 Spec 045 and §3 Family 4), read
>    first-hand at this draft. Its finding
>    for this spec: Spec 045's corpus gate
>    0.2 does not transfer and 045 stands
>    closed, but "Asset A's build is
>    corpus-independent and transfers as
>    written" — a depicted-kind
>    classification built from held published
>    sources (CISI volumes, Parpola's
>    identifications), entered blind, frozen
>    before any join, under 045 §§2–3 and
>    gates A1–A6; nothing in that contract
>    names any corpus.
> 3. **Spec 045's frozen record on `main`** —
>    its spec.md §§2–3 (the contract, quoted
>    in full in this draft's spec §2), its
>    freeze.json (freeze digest
>    `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`),
>    and its outcome.md (execution of
>    2026-10-21: **INVALID at gate 0.2**,
>    positional reproduction; step 0 ran
>    before the step-1 Asset A build, so the
>    build gates never ran and no Asset A
>    digest exists).
>
> No AEE lifecycle hooks have run on this
> draft; they are a freeze gate. Nothing in
> this draft has been run, frozen,
> registered, joined, or computed.

## 1. The adopted basis (operative substance)

- **The contract.** Spec 045 §§2–3, verbatim.
  This draft invents no part of the asset's
  contract: the form and location, the
  classification fields, the source
  hierarchy, the blind-entry rule, the
  dispute rule, the D-18 consumption form,
  the freeze point and digest pinning, and
  the build gates A1–A6 are the frozen
  words, quoted between markers in spec §2
  and verified character for character at
  drafting (see §2).
- **The build only.** Spec 045's own test
  (its §§5–6: the two models, the closing
  comparison, the step-0 gates including
  the failed gate 0.2) is **not** part of
  this spec. Spec 045 closed INVALID and
  stands closed; this spec neither reopens
  it nor produces a verdict under it. The
  readiness assessment's split — build
  transfers, corpus gate does not — is the
  drafting rule of this spec.
- **The product and its consumers.** The
  classification and its digest, published
  as the first product. Spec 070 step 0 and
  Spec 071 step 0 assert that digest from
  this spec's executed record
  (`asset-a/asset-a-freeze.json` in this
  spec's directory). Dependency order as
  commissioned: **Spec 069 → Spec 070 →
  Spec 071.**

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-22,
against `origin/main` at
`2a0eb854982f52453bcd76fd4a5bcbb088eb21e8`
(the local checkout was not used; the draft
was built in a fresh tree from that commit):

- **Spec 045 spec.md** — read in full.
  §§2–3 extracted mechanically from the
  frozen file and embedded in spec §2 of
  this draft; the embedded text was then
  compared programmatically against the
  source span and matched exactly.
- **Spec 045 freeze.json** — the freeze
  digest `5d8254dd…` read from the file's
  `digest` field; the register and design
  blocks confirm Asset A was **not** built
  at the freeze ("NOT built at this freeze";
  execution gate not satisfied at the
  freeze).
- **Spec 045 outcome.md** — read in full:
  gate 0.1 PASS; gate 0.2 FAIL on three
  observed grounds (the pinned corpus
  carries 3,463 inscriptions of length ≥ 3
  against the recorded 2,267; the 40/61/20
  classes are exhibited by no record of
  record; the quantities belong to the
  absent Firestore V3 corpus); gates 0.3
  and 0.4 not reached; Asset A not built,
  gates A1–A6 never ran, no digest exists;
  the D-18 delivery re-verified as the
  empty feed, SHA-256 `772db4df…`, under
  its IDENTIFICATION FAILED closure.
- **Spec 049 draft** (branch
  `spec-049-hunt-opening-animal-signs-draft`,
  PR #250) and **Spec 050 spec.md** on
  `main` — read for the consumption forms
  the successors restate: both consume
  Asset A by digest and neither builds it;
  neither can proceed without the product
  of this spec.
- **The readiness assessment** — §1.5
  (045/049/050) and §3 Family 4 read in
  full; its Asset A finding is input 2
  above.

## 3. Double derivation of acceptance tests (doctrine requirement)

Each claim's acceptance test was derived
twice independently; disagreements and their
resolutions are recorded. Summary of the
points where the derivations diverged:

| Claim | Derivation A | Derivation B | Resolution |
|---|---|---|---|
| C02 | The freeze checks the quotation by re-reading Spec 045 at freeze time | The freeze checks the quotation against the freeze digest's frozen file bytes as pinned on main | **Agree in substance, both recorded.** The check is character-for-character against Spec 045 §§2–3 as frozen on main; the freeze digest is the anchor and the file on main at the freeze is the text. |
| C07 | The D-18 input is absent, because Spec 046 identified no sign | The D-18 input is present as a terminal delivery: the frozen closure form, an empty feed | **Disagreement, resolved (DD-069-1).** B governs, on Spec 045's own execution record: the concordance file exists, is pinned by its digest, and carries the closure block; §2.6 states expressly that an empty feed is a stated state, never an absent file. The draft therefore records the input as a terminal empty feed, and gate A2 re-asserts it. |
| C08 | Coverage is the signs the dependents need | Coverage is the full pinned-crosswalk universe (gate A3 as restated by DD-045-18) | **Disagreement, resolved.** The quoted contract governs: gate A3's scope is the full universe — 187 distinct sign keys at the freeze census. A narrower scope would contradict the quoted text this spec exists to execute. |
| C11 | The build should pin the positional record, as Spec 045 §4 did | The build pins no corpus-side record at all | **Disagreement, resolved (DD-069-2).** B governs. Spec 045 §4 pinned the positional record for its *test*; the build's inputs are the sources, the crosswalk, and the D-18 state. Pinning a corpus record would import the coupling that left the asset unbuilt, without serving any build gate. |

All other claims: the two derivations
agreed, with the operative check being the
gate or inspection named in the claim.

## 4. What the freeze decision is asked to decide

1. **OPEN-069-1 (asset location).** Confirm
   spec §2.1's reading: the canonical file
   and `asset-a-freeze.json` live in **this**
   spec's directory
   (`specs/069-hunt-asset-a/asset-a/`), since
   Spec 045's directory is a frozen, closed
   record and is not edited. The successors'
   step-0 pins name this location.
2. **OPEN-069-2 (the D-18 state).** Confirm
   DD-069-1: the D-18 input stands resolved
   as the terminal empty feed on record, and
   gate A2 at execution re-asserts that
   state rather than re-opening Spec 046.
3. **OPEN-069-3 (jurisdiction coding).**
   Spec 045's frozen §5.2(b) jurisdiction
   coding rule (its DD-045-14) belongs to
   Spec 045's own closing test, which this
   spec does not run. Decide whether the
   build record nevertheless states the
   per-row jurisdiction coding at entry (so
   a future closing test need not re-enter
   the asset), or whether the build records
   the verbatim labels only and coding is a
   later act outside the frozen asset. The
   draft takes no position; the asset's
   fields (quoted §2.2) are unaffected
   either way.
4. **OPEN-069-4 (second-enterer spot
   check).** Spec 045's freeze decided
   (DD-045-16) that no second-enterer spot
   check is added. Decide whether that
   decision carries to this build or
   whether the freeze adds a stated spot
   check. The quoted gates do not require
   one.
5. **OPEN-069-5 (OSF).** Whether this spec
   files its own OSF contract registration
   at its freeze, and in what form, given
   that it is a build whose product is an
   asset rather than a verdict. No
   registration is filed by this draft.
6. **OPEN-069-6 (phase number).** Allocate
   the execution phase number at the
   freeze, from the merged record as it
   then stands (DD-069-3).

## 5. Draft-fixed readings (stand unless the freeze overturns them openly)

- **DD-069-1 — The D-18 input is a terminal
  empty feed, on record.** See §3, C07.
  The build proceeds without the feed and
  records its absence; the feed is never
  reconstructed from the asset's labels.
- **DD-069-2 — No corpus-side pin.** The
  build's input table (spec §4) contains no
  corpus, positional, Phase-43, or Shakti
  pin. See §3, C11.
- **DD-069-3 — No execution phase number at
  draft.** The phase number is allocated at
  the freeze act (OPEN-069-6).
- **DD-069-4 — Evidence carries
  `observed_at` of this draft** (2026-10-22),
  because the cited facts were verified
  first-hand at drafting, per the Spec
  042–054 convention.
- **DD-069-5 — The freeze gate is the AEE
  lifecycle hooks in the substantive form
  of DD-038-10:** at after_specify,
  after_plan, and after_tasks, zero
  correctness failure modes and no claim
  below the 0.70 threshold; the FR-2.3
  draft-cap records a draft register
  carries are not a freeze failure. No
  hooks run at draft.

## 6. Design defects and ambiguities found at drafting

1. **The quoted §2.1 names Spec 045's
   directory as the asset's home.** That
   directory is a frozen, closed record;
   building the file there would edit a
   closed spec's tree at execution. The
   draft resolves the tension openly in
   spec §2.1 (the asset lives in this
   spec's directory; form and contents
   unchanged) and puts the reading to the
   freeze as OPEN-069-1. The quoted text
   itself is **not** altered to hide the
   tension.
2. **The quoted contract speaks of Spec
   045's own test population and step-0
   gates,** which closed INVALID and will
   never run. Those references are read as
   record, per spec §2.1; no reading is
   allowed to turn them into acts of this
   spec. Recorded here so the freeze can
   overturn the reading openly if it
   disagrees.
3. **No Asset A digest can be stated in
   any successor draft as a value.** Both
   successors pin the digest by source
   (this spec's `asset-a-freeze.json`)
   exactly as Spec 050 pinned Spec 045's;
   any draft found carrying an asserted
   digest value before this build executes
   is defective on its face.

## 7. Bottom line

Spec 069 is a build under a frozen contract,
quoted in full, with fail-closed gates and a
single product — the classification and its
digest — on which the commissioned
dependency order (Spec 069 → Spec 070 →
Spec 071) stands. It has no corpus gate and
no Shakti input, and it adjudicates no Hunt
claim. The freeze is asked to decide the
six OPEN items of §4.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
