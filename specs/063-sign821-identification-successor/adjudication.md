# Spec 063 — Adjudication Record

> ## ADJUDICATION — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The owner's approval of 2026-10-21
>    (amendment package Item 5)**: build the
>    successor to Spec 056 (sign 821
>    recovery) through freeze and OSF
>    filing. This is the freeze-and-filing
>    approval for this spec. It is not an
>    execution order: execution remains a
>    separate later act (DD-063-13).
> 2. **The authoritative draft: Amendment
>    Queue Item 5** — "Drawn-Form References
>    for Wells's Signs 821 and 297"
>    (investigation and draft, 2026-10-21) —
>    followed exactly in its §6.1 (the
>    reference record), §7 (the
>    identification protocol), and §8 (what
>    the successor is). Its §5.1 finds that
>    a lawful inspectable form for sign 821
>    exists by two independent text routes;
>    its §9.1 names the preservation act,
>    performed inside this spec (DD-063-4).
> 3. **Spec 056's frozen and executed
>    record** (`specs/056-sign821-recovery/`):
>    freeze digest `64c28ce1…`, executed
>    at Phase-418, outcome IDENTIFICATION
>    FAILED at R-3, with candidate K-1
>    passing R-1, R-2, R-4 and R-5 on the
>    pinned passage. That record is this
>    spec's predecessor record: cited, never
>    edited (DD-063-1).
>
> Under campaign decision E-1, OSF
> registration at freeze is settled policy,
> not an open proposal — see §3, OP-063-2,
> decided at the freeze as DD-063-9.

## 1. The adopted basis (operative substance)

- **The predecessor.** Spec 056 re-extracted
  the pinned passage of Wells (2015) under
  a two-pass protocol, recovered a specific
  argument (candidate K-1: sign 821, in the
  Dholavira signboard contexts, has a
  meaning of 'city', either as a
  determinative or as a word; Wells 2015,
  printed p. 92), and closed IDENTIFICATION
  FAILED because the drawn sign could not
  be identified by either of the two routes
  its frozen R-3 allowed: the registry
  carries no W821 entry, and Figure 2.6's
  entry is graphic-only in the held text
  (captions only). Its outcome named the
  unblocking act: preservation, as a
  committed and hashed record, of an
  inspectable drawn-form reference for
  Wells's sign 821.
- **The draft that supplies it.** Amendment
  Queue Item 5 investigated every form a
  reference could take against three tests
  — inspectable by a second party,
  committable under the no-images rule,
  lawful under the applicable license
  position — and found for 821: route 1
  (composition: the book's own formation
  text, held text lines 3691–3704, plus the
  registry's drawn description of the base
  sign, P378 / W820, "Wheel with 6 spokes
  with even angles") composes a complete
  drawn-form descriptor from committed,
  hash-pinned records alone; route 2 (a
  feature descriptor derived by glyph
  inspection of Figure 3.2 in the held
  Wells 2006 PhD thesis, thesis p. 92)
  confirms it independently from an open
  deposit; route 3 (citation) pins Wells
  2015 Figure 2.6 (printed pp. 19–22) and
  Figure 6.13 (printed p. 93) for any
  checker with lawful access to the book.
  Its license position (§4 ¶¶1, 2, 4) is
  argued, not assumed, and is carried in
  the preserved record.
- **What the successor is (draft §8).** A
  new spec re-running Spec 056's recovery
  test for candidate K-1 with R-3 now
  satisfiable through the §6.1 record and
  the §7 protocol. Its outcomes are its own
  (RECOVERED / IDENTIFICATION FAILED on the
  new record / CLOSED AT STEP 0), frozen by
  itself; if RECOVERED, the claim enters at
  created/untested with a designed-never-run
  test note, exactly as DD-056-6/DD-056-17
  fixed for the original. Spec 056's
  outcome stands unedited as the record of
  why the first run could not finish.
- **No other sign, no other successor.**
  The same draft's §6.2 record and §8
  successor for sign 297 (Spec 046's
  successor) are outside this spec
  entirely; nothing here touches them.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
by two independent routes (git-blob and
contents-API raw), both at `main` at
`e03f7832f99463d3496241676e21bf85e62fb9cc`,
the routes agreeing byte-for-byte:

- **Spec 056's record** — read in full:
  `spec.md`, `claims.json`,
  `adjudication.md`, `tasks.md`,
  `freeze.json` (digest
  `64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e`),
  `osf-spec-registration.md` (registration
  3eygs, later approved + public), and
  `outcome.md` (SHA-256 `ff16184a…`) with
  its extraction record (SHA-256
  `ad4a3f74…`): K-1's checklists, the
  R-3 record, and the named unblocking act.
- **Input pins** — recomputed and equalling
  their pins on both routes: held Wells
  text `62acf855…` (268,195 bytes);
  registry `8a0b2a82…` (803 rows);
  witness `ecbc37a4…` (157 rows);
  Phase-104 evaluation `2d0b83e8…`;
  lane-2 drafts `3f645c9a…`; anchors
  `df0cf620…`.
- **Registry facts re-derived by parse:**
  no W821 value in any row, sole or inside a
  multi-value cell; W820 solely on P378
  ("Wheel with 6 spokes with even angles",
  M391); `Yunmapped_0821` is
  `yajnadevam_glyphid` with empty
  `wells_ids` and corpus frequency 10.
- **Witness facts re-derived by exact field
  parse:** no grapheme 821 in any row's
  `wells_graphemes` field.
- **Held-text locators re-derived:** list-
  naming statements at lines 414 and 665;
  Figure 2.6 captions at lines 868, 872,
  876, 880; K-1 suggestion at lines
  2835–2836 (printed p. 92); sign 861
  passage at lines 2848–2853; Figure 6.13
  caption at line 2860 and in the list of
  figures at line 176; the 'Doubled Signs'
  passage at lines 3691–3704 with the Table
  AII.4 caption at lines 3705–3706; the
  passage-of-record slice (lines 2783–2871)
  is Spec 056's freeze-pinned digest
  `51d6fb3a…` (5,354 bytes).
- **Thesis PDF asserted on the local
  file:** `Wells2006_PhD_EpigraphicApproachesToIndusWriting.pdf`,
  19,313,853 bytes, SHA-256
  `4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e`
  — equalling the amendment draft's §6.1
  plate-confirmation pin. The freeze's
  step-0 gate 0.2 states this assertion as
  an execution-time check, before any plate
  is read (spec §3).
- **The preserved reference** — written from
  the draft's §6.1 contents exactly;
  SHA-256 computed at commitment:
  `695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999`
  (5,689 bytes). No image is committed
  anywhere in this spec.
- **Phase allocation check** — Phase-425
  verified genuinely free from the repo
  phase records at this draft: the frozen
  freeze records allocate Phase-419…
  Phase-424 to Specs 057… 062 in freeze
  order; a repository code search for
  "Phase-425" and for "phase425" returns no
  record; the root LEDGER allocates no
  Phase-425; no phase425 report, script, or
  graph module exists in the tree. (Decided
  at the freeze as DD-063-10.)
- **The fragment's live record** — asserted
  in the Spec 038 form: the _0001 entry is
  present with wording, UNTESTED status and
  created stage as the frozen record states,
  and carries the appended `spec056_closure`
  entry (Phase-418) naming the closure and
  the unblocking act.
- **Not done at draft, by design** — no
  derivation was performed, no plate was
  read under this spec, the §5 protocol was
  not run, R-3 was not scored, no test for
  the recovered claim was designed, the AEE
  hooks had not run at drafting, and nothing
  had been filed with OSF. Those are freeze
  and execution acts, in that order.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest
   in `freeze.md` / `freeze.json`), with
   every §2 pin re-asserted against the
   merged record — or decline, leaving
   Spec 056's IDENTIFICATION FAILED as the
   standing record, with its named
   unblocking act unperformed.
2. **OP-063-1 — Execution phase number.**
   Not allocated by this draft. Phase-425 is
   verified free (§2); the freeze allocates
   it or the next free number, on the same
   verification.
3. **OP-063-2 — OSF registration (settled,
   not open).** Campaign decision E-1
   settles that every specification in the
   pass files its own OSF contract
   registration at its freeze. The freeze of
   Spec 063 therefore files one, following
   the Specs 036–039 and 056/062 pattern.
   Nothing is filed at draft.
4. **OP-063-3 — Route 3 (composition).**
   Spec 056's frozen R-3 admitted two
   routes; the composition route is new and
   exists only if this successor freezes it
   (draft §3.3, §7). The freeze adopts it
   with the §7 justification carried into
   spec §5 step M verbatim in substance —
   or declines it, leaving routes 1 and 2.
5. **OP-063-4 — The step-0 class names for
   the new gates.** This draft names three
   classes (INPUT PIN MISMATCH; THESIS FILE
   PIN MISMATCH; REFERENCE NOT PRODUCIBLE).
   The freeze confirms the names, or renames
   openly before any execution.
6. **OP-063-5 — The freeze and execution
   acts.** The freeze, and any later
   execution order, are the owner's acts.
   **OWNER-APPROVAL** for each: freeze,
   OSF filing, execution.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-063-1 — Successor, not patch.** Spec
  056's record (spec, freeze, extraction
  record, outcome) is cited, never edited.
  Its IDENTIFICATION FAILED stands until a
  successor execution under this spec
  replaces the outcome with its own
  appended outcome record (claim F063-C15).
- **DD-063-2 — Candidate of record is K-1;
  the argument conditions are of record.**
  R-1, R-2, R-4 and R-5 stand as Spec 056's
  execution adjudicated them on the pinned
  passage; no new extraction pass runs
  under this spec; the open condition is
  R-3 alone (claim F063-C02, F063-C08).
  Ground: the passage, its extraction, and
  its checklists are of record at pinned
  digests asserted at gate 0.1; re-running
  them would manufacture a second,
  competing record of the same passage.
- **DD-063-3 — The outcome set is exactly
  three.** RECOVERED / IDENTIFICATION
  FAILED (on the new record) / CLOSED AT
  STEP 0 (draft §8). No retirement outcome
  exists: K-1 passed the argument
  conditions, so the retirement wording
  (an extraction artefact stating no
  proposition) is false of it, and the
  DD-056-2 logic that created the closure
  class governs here too (claim F063-C04).
- **DD-063-4 — The preservation act is
  inside this spec.** `drawn-form-reference-821.json`
  is committed in this spec's directory
  with exactly the draft §6.1 contents, in
  text form under the no-images rule; its
  SHA-256 is computed at commitment and
  pinned in the freeze (claim F063-C05).
  Ground: draft §9.1 names the preservation
  act, and the owner's Item 5 approval
  commissions this successor; a separate
  records act would split the reference
  from the contract that freezes its use.
- **DD-063-5 — The identification protocol
  is the draft's §7, as it applies to 821.**
  Step 0 gates (§3); step D double
  derivation (without sight of each other
  or of the drafted descriptor wording;
  unsettled disagreement resolves against
  identification); step C continuity by
  anchors; step M routes 1–3, route 3
  (composition) new with its justification
  (claims F063-C06, C07, C09).
- **DD-063-6 — Step C for 821 passes on the
  anchors' agreement.** The formation
  passage, the P378 registry anchor, and
  the plate agreement (draft §3.2): the
  check is the agreement of those records,
  stated on the run record; the plate
  number alone anchors nothing.
- **DD-063-7 — No execution phase number at
  draft.** Allocated at the freeze act,
  from the repo phase records as they then
  stand (OP-063-1).
- **DD-063-8 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today; the
  completion Spec 038's freeze had to
  retrofit is done here at the act that
  actually observed the records.

## 5. Double derivation of the acceptance tests (doctrine record)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived twice,
independently, from the requirement alone,
before the register was written:

- **Derivation A** worked from the
  requirement text forward: for each claim,
  what observable record, produced by the
  run itself, would show the requirement
  held?
- **Derivation B** worked from the falsifier
  and the pre-written outcome wordings
  backward: for each claim, what would a
  hostile reader check in the outcome record
  to show the requirement had *not* held?

The two derivations agreed on the gate,
derivation-sheet, checklist, and inspection
tests for F063-C02, C05, C06, C10, C12, C13,
and C15 without amendment: in each case A's
"record produced in order" and B's "absence
or disorder of that record falsifies" are the
same check read from the two directions, and
the register states it once.

Disagreements, and their resolutions:

- **X-1 — Re-extract the passage, or take
  K-1 as of record?** A proposed a fresh
  two-pass extraction under this spec, for
  symmetry with Spec 056. B held that the
  extraction is an executed act of record on
  the pinned passage: re-extracting would
  manufacture a second record of the same
  passage, and any difference between the
  two records — even a checklist wording —
  would itself become a dispute the
  successor exists to avoid. The open
  condition is identification alone.
  **Resolution:** B governs (DD-063-2): the
  argument conditions are of record at
  pinned digests; this spec runs R-3 only.
- **X-2 — Keep a retirement outcome for
  symmetry?** A carried Spec 056's four-word
  outcome set forward for family symmetry.
  B quoted the retirement wording against A:
  it asserts the fragment states no
  proposition, which Spec 056's executed
  record refutes for K-1 — a retirement
  outcome in this spec could never honestly
  fire, and a word that cannot fire is not
  an outcome but a decoration. The draft
  (§8) fixes the successor's outcomes as
  three. **Resolution:** B governs
  (DD-063-3).
- **X-3 — Is route 3 a number match in
  disguise?** A's hostile reading: the
  formation passage names 820 and 821 by
  number, so composing 821 from 820 is
  arithmetic on numbers, not a drawn form.
  B answered from the records: every step
  of the composition is a drawn form — the
  base sign enters by its registry *drawn
  description* ("Wheel with 6 spokes with
  even angles"), the operation is the
  source's own stated *doubling of the
  drawn sign*, and the result is checked
  against the plate's *drawn pair*; the
  numbers locate those drawn forms in the
  source and do no identifying work
  themselves. That is the draft §7
  justification, and it is carried into
  spec §5 step M in the freeze.
  **Resolution:** B governs, and A's reading
  is answered on the record here and in
  spec §9 (the base-sign trap) rather than
  left implicit (OP-063-3 for the freeze).
- **X-4 — Inherit the drafted descriptor, or
  check it?** A proposed that the §6.1
  descriptor, already derived by two routes
  at drafting of the amendment (§3.2, §3.3),
  be adopted as the identification's basis
  directly. B held that a descriptor no
  execution-time derivation has checked is
  the draft's expected reading with standing
  — the exact position Spec 055's record
  refuses. **Resolution:** B governs (draft
  §7 step D, spec §5): two derivations
  without sight of the drafted wording, and
  a material difference closes the run as
  IDENTIFICATION FAILED (reference not
  sustained).
- **X-5 — Is P378 a route-1 match?** A
  proposed that the composition descriptor
  matches the registry through P378 (the
  only wheel row), making route 1 satisfiable
  by construction. B distinguished the base
  from the target: P378's description is a
  *single* six-spoke wheel — sign 820 — and
  crediting it as the match for the *doubled*
  form would identify the wrong sign, the
  family's standing error in a new costume.
  **Resolution:** B governs (spec §5 step M):
  route 1 matches only a row carrying the
  doubled drawn form; there is no fallback
  to P378, and its misuse is a named trap.

## 6. Defects found at drafting

- **D-1 — Spec 056's named unblocking act
  mentions the image form.** Its headline
  act names "the Figure 2.6 sign-list pages
  … or the Figure 6.13 examples as images
  tied to the list entry". The program's
  no-images rule bars committing those
  images. Resolved at draft per the
  amendment draft's §5.1: the act's purpose
  ("from which the drawn sign can be matched
  by drawn form through the crosswalk
  registry or quoted as the source list's
  own entry") is met by the preserved text
  record — descriptor, composition, and
  citation — and the image form is not
  used. Spec 056's record is not edited;
  the resolution is recorded here.
- **D-2 — Spec 056's frozen R-3 cannot be
  re-read to admit the composition route.**
  Its two routes are frozen text. Treating
  the Doubled Signs passage as already
  inside them would rewrite a frozen
  contract by interpretation — the appendix
  text was noted in Spec 056's outcome and
  set aside precisely because the frozen
  routes did not include the use this
  successor proposes for it. Repaired by
  succession, not reinterpretation: route 3
  is frozen openly in this spec (§5,
  OP-063-3), and Spec 056's closure stands
  as the correct outcome under its own
  contract.
- **D-3 — The thesis list is an earlier
  state of the author's list.** The 2006
  plates print 676 signs under the 2006
  numbering; the fragments' numbering is
  the 2011 form as given in 2015 (694
  signs). A plate number is therefore not
  self-evidently the 2015 number. Carried
  as a stated limit (spec §11) and repaired
  structurally by step C: continuity for
  821 is anchored from the 2015 side by the
  formation passage and the registry
  cross-match agreeing with the plate, and
  step C's failure is a pre-registered
  closure. Not repaired by assertion.
- **D-4 — The reference record did not
  exist in the repository before this
  spec.** The unblocking act names a
  committed, hashed record; until this
  draft, the program held the descriptor
  only in the amendment draft outside the
  repo. Repaired by DD-063-4: the record is
  committed inside this spec, hashed at
  commitment, and pinned in the freeze, so
  the reference the execution checks is the
  reference the freeze froze.

No defect was found that prevents stating
the falsifier, the step-0 gates, the
identification protocol, or the pre-written
wordings for the full outcome set; the draft
therefore advances to the freeze.

## 7. Freeze decisions (2026-10-21)

> ## FREEZE ACT — DECIDED — 2026-10-21
>
> The freeze act of 2026-10-21, under the
> owner's approval of the same date
> (amendment package Item 5). Each
> resolution is recorded here on the record;
> the register rulings were carried into
> `claims.json` before the AEE hooks ran,
> and the hooks passed over the recovered
> register (0.6-draft;
> `aee/freeze-aee-note.md`).

- **DD-063-9 — OSF registration at the
  freeze (E-1).** This spec files its own
  OSF contract registration at the freeze,
  under campaign decision E-1, following
  the Specs 036–039 and 056/062 pattern.
  The filing record is
  `osf-spec-registration.md`. Execution
  awaits the registration's approval act
  and a separate execution order; no mail
  is handled by the freeze.
- **DD-063-10 — OP-063-1 resolved:
  Phase-425 allocated.** The execution
  phase number (DD-063-7) is allocated at
  this freeze as **Phase-425**, on the §2
  verification: Phase-424 was Spec 062's;
  no repo record allocated Phase-425 before
  this act.
- **DD-063-11 — OP-063-3 resolved: route 3
  (composition) adopted, with its
  justification.** The freeze adopts route
  3 as spec §5 step M states it, carrying
  the amendment draft §7's justification
  verbatim in substance: every step is a
  drawn form — the base sign's registry
  description ("Wheel with 6 spokes with
  even angles", P378), the doubling
  operation from the source's own appendix
  (the 'Doubled Signs' formation passage),
  the plate's drawn pair (thesis p. 92) —
  and the number is used only to locate
  them. Routes 1 and 2 stand as drafted.
- **DD-063-12 — OP-063-4 resolved: the
  step-0 class names confirmed.** CLOSED AT
  STEP 0 — INPUT PIN MISMATCH; CLOSED AT
  STEP 0 — THESIS FILE PIN MISMATCH (the
  thesis digest asserted on the local file
  before any plate is read); CLOSED AT
  STEP 0 — REFERENCE NOT PRODUCIBLE. No
  substitute artefact is admitted under any
  class.
- **DD-063-13 — OP-063-5 resolved: the
  freeze and filing acts are taken; the
  execution is not authorised.** The freeze
  act and the OSF filing act are taken
  under the owner's Item 5 approval.
  Execution (Phase-425) is a separate later
  act: it begins only after this freeze has
  merged, the OSF registration's approval
  act has completed, and a separate
  execution order is given.
- **DD-063-14 — Pins and the reference
  digest confirmed at the freeze.** Every
  spec §2 pin was re-verified two routes at
  `main` `e03f7832…` before freezing
  (§2), and the preserved reference's
  digest `695dd35d…` is pinned in the
  freeze record as computed at commitment.
- **DD-063-15 — The DD-038-10 AEE gate
  reading adopted.** The gate is: at every
  lifecycle hook, zero correctness failure
  modes and no claim below the 0.70
  threshold; FR-2.3 draft-cap records alone
  do not block a freeze, because they are
  lifted only by human ratification (a
  status change), not by any recovery
  available at a freeze. The hooks passed
  on that reading (`aee/freeze-aee-note.md`).

DD-063-1 to DD-063-8 are **confirmed** as
drafted, including DD-063-3's three-word
outcome set, DD-063-4's preservation act
inside this spec, and DD-063-5's protocol
with step C passing on the anchors'
agreement for 821 (DD-063-6).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
