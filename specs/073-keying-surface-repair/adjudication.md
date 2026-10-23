# Spec 073 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-22
>
> This spec has five adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The merged outcome record of Spec
>    070** (Phase 433; read in full at this
>    draft): closure POPULATION NOT KEYED at
>    gate 0.4; the enumerated 31-sign
>    opening-strong set; the five unkeyable
>    ICIT codes (136, 298, 401, 617, 824)
>    with their occurrence counts; the
>    verification recorded there that no
>    registry row in any numbering system
>    carries their Wells ids; and the
>    record's own statement that a successor
>    "must first repair the keying surface."
> 2. **The merged outcome record of Spec
>    071** (Phase 434; read in full at this
>    draft): closure INVALID at gate 0.3;
>    the 557-sign coverage census (285
>    keyed; 134 with no registry resolution;
>    138 resolving outside Asset A's
>    187-row universe); the recorded fact
>    that Asset A's celestial class is
>    empty against that spec's TOO THIN
>    floor of 30; and the two repairs the
>    record names.
> 3. **Spec 069's executed Asset A record**
>    (the canonical CSV, its freeze record,
>    and its entry log; read at this draft):
>    the built asset this repair carries
>    forward — 187 rows, census animal 20,
>    sky_cycle 0, object_goods 14, human
>    25, other 127, contested 0,
>    unidentified 1 — and the two-pass entry
>    structure its build used.
> 4. **Spec 045's frozen §§2–3** (read in
>    full at this draft): the Asset A
>    contract — fields, source hierarchy,
>    blind entry, dispute rule, D-18 input
>    form, build gates A1–A6 — whose
>    discipline this repair extends to new
>    material without amending.
> 5. **The pinned registry, crosswalk, and
>    intake record**, recomputed and read
>    first-hand at this draft (§2 below).
>
> These inputs commission this **draft**
> under the program's standing drafting
> authorization. The freeze, the
> registration, and the execution of Spec
> 073 are separate later owner acts. No AEE
> lifecycle hooks have run on this draft;
> they are a freeze gate (per DD-038-10).

## 1. The adopted basis (operative substance)

- **The problem.** Both Hunt successors
  closed at step 0 on the keying surface,
  not on their questions: the chain
  ICIT code → registry Wells map → Asset A
  row breaks in three recorded places —
  five opening-strong codes with no
  registry row anywhere (Spec 070); 134 of
  the primary population's 557 signs with
  no resolution in the registry's
  `parpola_1982` Wells map, and 138 more
  resolving to registry signs outside
  Asset A's 187-row universe (Spec 071) —
  and Asset A's celestial class is empty.
- **The design.** One repair study, two
  products, one measurement pass, in gated
  order: **Registry v2** (a new versioned
  file; v1's rows verbatim; Wells-map
  completions and new `icit_wells` rows
  only on cited published statements; a
  change schedule accounting for every
  difference; a NO PUBLISHED IDENTITY
  schedule naming every attested code the
  published record does not identify),
  then **Asset A v2** (a new asset with its
  own digest; v1's 187 rows carried
  verbatim and marked; new rows entered
  blind from the ruled published sources
  under Spec 045's discipline; disputes
  contested, silence coded `unidentified`,
  never pooled), then **coverage
  measurements M1–M5** against baselines
  reproduced at gate 0.2 — reported
  whatever their values.
- **The claims served.**
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
  (IN QUESTION, as Spec 070 left it) and
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
  (UNTESTED, as Specs 050/071 left it).
  This spec adjudicates neither, appends
  to neither, and computes no quantity
  under either's test.
- **The honest limit.** A repaired surface
  does not guarantee the celestial class
  reaches any floor — or one member. If
  the ruled sources identify no celestial
  depictions, the study's recorded output
  is that Spec 071's question remains
  untestable in this form. That sentence is
  in the spec (§8) and in the register
  (F073-C13) before any freeze is asked
  for, so no later reader can mistake this
  design for a promise.

## 2. Verification record at draft

Verified first-hand at this draft, against
the merged tree at `d20bc1bc`:

- Registry v1 recomputes to SHA-256
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`;
  803 rows (396 `parpola_1982`, 407
  `yajnadevam_glyphid`, the latter with no
  `wells_ids` anywhere).
- The `parpola_1982` Wells map carries
  **498 distinct Wells ids** (tokenising
  `wells_ids` on `|`), matching DD-070-9's
  freeze-time figure exactly.
- **W136, W298, W401, W617 and W824 appear
  in no row's `wells_ids`, in any numbering
  system** — Spec 070's recorded finding,
  re-verified independently at this draft.
- Crosswalk recomputes to
  `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf`;
  205 rows, 187 distinct registry sign ids.
- Asset A v1's canonical CSV recomputes to
  `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b`;
  its freeze record's census (animal 20,
  sky_cycle 0, object_goods 14, human 25,
  other 127, contested 0, unidentified 1)
  matches the CSV.
- The keying route (DD-070-9, restated as
  DD-071-10), the disposition that closed
  Spec 070 (DD-070-11), and both closures'
  exact classes and gates are as §1
  states, from the two outcome records.
- The registry carries derived positional
  columns (`corpus_freq`, `start_rate`,
  `end_rate`, `internal_rate`) — noted at
  drafting because they are a contamination
  route for blind entry; spec §2 excludes
  them as evidence and gate 0.4's inventory
  omits them.
- The next free spec number is **073**:
  `specs/` on main ends at 072, and no
  branch or open PR carries a 073 (the two
  open draft PRs are Specs 052 and 054).

## 3. Double derivation of acceptance tests (doctrine requirement)

Each claim's acceptance test was derived
twice independently at drafting — once from
the two outcome records' statements of the
failure, once from the pinned files
themselves — and the derivations agreed on
every figure used in the register (498;
803; 285/134/138; 26/31; the five codes and
their counts; sky_cycle 0 of 187). The one
surface disagreement found and resolved:
the outcome records describe the registry
gap as "no row in any numbering system,"
while DD-070-9's route reads only
`parpola_1982` rows; both are true, and the
draft keeps them distinct — Break 1 is the
stronger, any-system absence (which is why
a repair must add rows, not only complete
the `parpola_1982` map), while Break 2's
134 is the route-relative figure. Spec §1
states them separately for that reason.

## 4. What the freeze decision is asked to decide

The nine open items of spec §14
(OPEN-073-1…9). The substantive ones:

- **OPEN-073-1** — the governing source
  list and hierarchy. This is the freeze's
  real decision: ranking Fuls's 2023
  Catalog as the ICIT-native governing
  source (the drafted default) is what
  makes the repair possible at all, and it
  is a judgement about the field's
  published record that a draft should
  propose, not presume.
- **OPEN-073-3** — the attested frame
  (documented + corroborated as drafted,
  per P-F1 S4) fixes how large the new-row
  entry labour is and what M3/M5 measure.
- **OPEN-073-6** — whether Mahadevan's and
  Wells's identifications enter directly
  or through a D-18-style concordance
  input, Spec 045 §2.6's cautious form.

## 5. Draft-fixed readings (stand unless the freeze overturns them openly)

- **DD-073-1 — Two products, one study, in
  gated order.** Registry first (identity
  is upstream of depiction), asset second,
  measurement last; the order is enforced
  by the digest dependencies, not by
  convention.
- **DD-073-2 — New files, never edits.**
  Registry v2 and Asset A v2 are new files
  with their own digests; v1 files are
  consumed by hash and re-asserted at the
  close (FROZEN INPUT MUTATED voids the
  products). The crosswalk is not extended
  in place either — it is pinned by Spec
  045's contract and two freezes.
- **DD-073-3 — Yajnadevam is a locator,
  never evidence.** It is an extraction of
  ICIT itself; the corpus is ICIT-lineage;
  identities sourced from it would be the
  lineage certifying itself. The same rule
  covers the ICIT documentation PDF and
  the Fuls OCR texts (locators), and the
  registry's derived rate columns (not
  identity evidence at all).
- **DD-073-4 — Coverage is measured,
  never targeted.** No floor, quota, or
  success threshold attaches to any
  coverage figure anywhere in the design;
  the outcome classes turn on the gates
  and on whether the shortfall is named.
- **DD-073-5 — The celestial class is
  measured, never filled.** A `sky_cycle`
  row exists only where a published
  source's own words depict a sky/cycle
  object (F073-C13).
- **DD-073-6 — New rows mirror Spec 045
  §§2.2–2.5 field-for-field**, plus
  `row_origin`, so the v2 asset is
  consumable by the same reader discipline
  as v1 and the carry is visible.
- **DD-073-7 — Unresolved attested signs
  live in the schedule, not the asset.**
  An Asset A row requires a registry
  identity to key by (Spec 045 §2.1's
  form); signs without one get their named
  disposition in the §4.3 schedule instead
  of a synthetic key invented for the
  occasion.

## 6. Design defects and ambiguities found at drafting

1. **Wells 1998's text is not exhibited.**
   The thesis is resolved at record level
   (DOI 10.11575/PRISM/23641) but this
   draft could not verify an in-hand full
   text. The design therefore asserts
   nothing about its contents, ranks it
   corroborating-only in the drafted
   default, and makes gate 0.3 exhibit it
   or the freeze strike it (OPEN-073-1,
   F073-C14). If its sign list in fact
   carries depictions the default hierarchy
   would govern with, that is the freeze's
   ruling to make on the exhibited text.
2. **The `icit_wells` sign_id form**
   (`W` + zero-padded code) is a drafting
   choice, not a program convention — no
   existing registry row uses it. It is
   stated in the open (§4.2) and put to
   the freeze (OPEN-073-2) rather than
   smuggled in as if established.
3. **The route a consumer would use on v2
   is not this spec's to freeze.** Spec §6
   restates DD-070-9's route against the
   v2 files (adding the `icit_wells` rows)
   for measurement purposes; whether a
   re-frozen 070/071 successor adopts that
   route is its own freeze's act. The
   draft says so in §6 rather than letting
   the measurement route harden into a
   default by repetition.
4. **Baseline B's 138** is defined
   relative to Asset A v1's universe;
   after the repair, the analogous figure
   is an output of M3's remainder list,
   not a baseline. The draft keeps the two
   apart (§3 gate 0.2 vs §6) so the
   before/after figures are not quietly
   compared on different definitions: M3's
   remainders are classified by reason
   (no resolution / contested / no v2
   row), which is the after-state analogue
   of the 134/138 split, stated as such.
