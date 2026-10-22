# Spec 067 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has one adjudication input, recorded
> here so the draft's basis is inspectable:
>
> 1. **The owner's approval of 2026-10-21**:
>    the amendment package Item 7 — the
>    Phase-130 catalogue-extension intake —
>    approved, and with it Item 7 §6, which
>    names this successor: a new spec number, a
>    new freeze, and a new OSF registration of
>    its own, re-running Spec 059's design
>    (Phase-136 machinery unchanged) on the
>    enlarged joined set produced by the
>    Spec 066 intake, with its own step-0 gate
>    census against the pinned merged layer and
>    its own gate bar adopted openly at its
>    freeze (the DD-059-7 form), and with a
>    mandatory step-0 census of type fill on
>    the newly joined objects before any F1
>    quantity exists. The authoritative draft
>    is
>    `~/workspace/research_notes/amendment-queue-2026-10-21/item-7-phase130-catalogue.md`
>    §6 (research notes, 2026-10-21). That
>    approval authorises this freeze and the
>    OSF filing at it. It authorises **no
>    execution**: the join and the F1 run wait
>    for the registration's approval act and a
>    separate execution order.

## 1. The adopted basis (operative substance)

- **The design.** Spec 059's frozen design
  (design D-22), carried unchanged in its test
  machinery: Spec 024 F1's seal/tablet
  TERMINAL14 test, re-run on a corpus joined
  through object identifiers rather than
  catalogue concordance — gated at step 0 on
  whether the better join is in fact better.
  The F1 test is specified for the gate-passed
  case only.
- **The claim.** `STUDY-SPEC-024/F1`:
  SETTLED — SUPPORTED on its joined subset
  (OR 2.384, CI [1.847, 3.077], family
  q = 0.00015, Phase-141 LOSO-stable). Its
  standing is not pre-judged by this spec.
- **The predecessor closure.** Spec 059
  (Phase-421) closed at step 0, JOIN GATE NOT
  MET: 2,899 of 5,679 joined (51.05%) against
  the ≥ 3,465 bar, on the vols. 1–2 catalogue
  layer. Its record is cited, never patched.
  The unblocking act its frozen outcome named
  — a more complete published object catalogue
  entering through Phase-130 intake — is the
  act Spec 066 executed.
- **The enlarged catalogue.** Spec 066
  (Phase-428; freeze digest `0b81d842…`)
  graded the CISI 3.1 portion's 2,101 numbers
  (VERIFIED 2,089 / CONFLICT 12 / UNRESOLVED
  0) and pinned the merged catalogue layer v2
  (9,741 rows, 5,529 distinct objects) in the
  restricted local store. This spec's join
  resolves against that pinned layer, in the
  DD-059-9 pin form (DD-067-9).
- **The one addition.** Item 7 §6's mandatory
  step-0 type-fill census (spec §3.4): type
  fill on the newly joined objects, and the
  resulting eligible seal/tablet strata under
  the frozen Phase-136 eligibility mapping,
  censused before any F1 quantity exists.
- **The boundary.** Object IDs, never string
  identity (Spec 037's census: 693
  exact-string matches — 269 VERIFIED / 341
  CONFLICT (49.21%) / 83 UNRESOLVED). Stated
  as spec §7.1 and claim F067-C06. The
  restricted discipline of spec §7.3 governs
  every product of the merged layer.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
against `main` at
`d195e2d1c5230e919a14ae7d6e9e20a165cab27f`
(re-read at the start of this act; the head is
the Spec 066 outcome merge, PR #317):

- **Item 7 §6** — read in full: the successor's
  terms (new spec, new freeze, new OSF
  registration; Spec 059's design re-run;
  step-0 gate census against the pinned merged
  layer; gate bar adopted openly at the freeze
  in the DD-059-7 form; the mandatory type-fill
  census; the §5 re-statement rule reserved
  exactly as Spec 059 left it; Spec 059's
  record never patched).
- **Spec 059's record** — read on `main` in
  full: spec, adjudication (DD-059-1…14),
  freeze record (digest `bba1caca…`), claims
  register, and the Phase-421 outcome (gate
  0.2 reproduced exactly 2,895 / 2 / 2,782;
  gate 0.3 census 2,899 joined / 661 no
  identifier / 2,119 zero-resolution / 0
  ambiguous, 2,479 distinct objects; joined
  set's type mix Seals 1,590 / Tablets 1,090 /
  Graffiti 69 / Objects 7 / unfilled 143;
  gate 0.4 failed, shortfall 566 rows).
- **Spec 066's record** — read on `main` in
  full: spec, adjudication, freeze record
  (digest `0b81d842…`), outcome, and the
  Phase-428 machine record
  (`reports/phase428_results.json`, SHA-256
  `a0b98dfb…`): census VERIFIED 2,089 /
  CONFLICT 12 / UNRESOLVED 0; halt evaluation
  NO HALT (0.57% against the 20% cap; stratum
  true-non-identity 0); the merged layer built
  with 53 collisions recorded, the existing
  object standing; its §7 projection (4,676
  rows, 82.34%) labelled a projection.
- **Layer v2 pin, asserted on the local file.**
  The restricted-local file
  `cisi_catalogue_layer_v2.csv` was recomputed
  at this draft: SHA-256 `cd0c2ba8…` and
  2,655,958 bytes, equal to Spec 066's outcome
  pin; its rows counted from the file: 9,741
  rows, 5,529 distinct `cisi_id` objects —
  the outcome's counts. (Counts only; no row
  left the local computation.)
- **Extension index pin, two routes.** The
  committed index
  `data/intake/cisi31_extension_index.csv`
  recomputed from the merged record by the
  contents-API route and the git-blob route:
  SHA-256 `be20439a…`, 78,531 bytes, 2,101
  data rows (VERIFIED 2,089 / CONFLICT 12) —
  both routes agree.
- **Carried pins.** Every Spec 059 §2 pin
  carried into spec §2 was re-derived at this
  draft from the merged record (the Phase-136
  record and its flow, the Stage 2(a) freeze,
  the builder, the Phase-141 report, the
  combined report, the registry, the
  Phase-130 schema and validator, the
  Phase-398 construction, the converted keyed
  layer, the horus84 layer pin
  `c368f290…`), together with the Phase-421
  census (`95282931…`) and results
  (`3948cd01…`) pins from Spec 066's record.
  The freeze re-asserts them all (§8).
- **Phase allocation.** Code search over
  `main` at the head above returns no
  reference to Phase-429 (and none to
  Phase-430); Phase-428 is Spec 066's, and
  Phases 424–427 belong to Specs 062–065's
  line as recorded on `main`. Phase-429 is
  genuinely free (DD-067-13).
- **Gate arithmetic** — computed at this
  draft: the carried bar is 0.61 × 5,679 =
  3,464.19, so ≥ 61.0% is ≥ 3,465 rows (3,464
  rows = 60.997%, fails) — DD-059-7's
  arithmetic, unchanged because the layer and
  the denominator are unchanged.
- **Not done at draft, by design** — no join
  against layer v2 has been run: no row of
  this layer has been joined under this spec,
  no joined share on the enlarged catalogue
  exists, the type-fill census has not been
  taken, and no F1 quantity on any enlarged
  set was calculated. Spec 066's projection
  is not a substitute for any of these, and
  this draft does not treat it as one.

## 3. The doubled derivation of acceptance tests (doctrine record)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived **twice,
independently, from the requirement alone**:
Derivation A worked from Item 7 §6 and
Spec 059's frozen design alone; Derivation B
worked from the executed record alone
(Spec 059's Phase-421 outcome, Spec 066's
Phase-428 outcome and machine record, the
Phase-136/141 records). Where the two
derivations disagreed, the disagreement and
its resolution are recorded here; the register
carries the resolved form. The register itself
is carried from Spec 059's recovered freeze
register (0.8-draft), so claims whose
substance is unchanged carry their recovered
heads and boundaries; the successor's changes
are the ones this section derives.

| Claim | Derivation A (from Item 7 §6 + D-22) | Derivation B (from the executed record) | Agree? |
|---|---|---|---|
| C01 scope | Inspection of outputs against §6's question | Inspection against Spec 059 §7's fences, carried | Yes |
| C02 record | §6: F1 stands as recorded | Direct read of the Phase-136 / combined / Phase-141 records + hash pins | Yes |
| C03 baseline | §6: Spec 059's design re-run — its gate 0.2 reproduction is part of the design | Phase-421 outcome: gate 0.2 reproduced exactly | Yes |
| C04 gate | §6: "its own gate bar adopted openly at its freeze (the DD-059-7 form)" | Spec 059's bar is the design's standard on the same layer and denominator | **Disagreed in route — see D-1** |
| C05 join construction | §6: join through the pinned route against the pinned merged layer | Spec 066 outcome: layer v2's pin, shape, and fences; Spec 034 route (b) as executed by 059 | Yes, B supplied the pins |
| C06 string boundary | §6 carries Spec 059's design, boundary included | Spec 037 census, as in 059 | Yes |
| C07 fail-closed + type-fill | §6: step-0 gate census **and** the mandatory type-fill census, before any F1 quantity | Spec 059 §3's gate order, with §3.4 inserted as its own gate | **Extended — see D-2** |
| C08 hypothesis | D-22 step 1 via 059, verbatim | No record counterpart (the hypothesis is the design's) | Yes (A governs) |
| C09 falsifier | D-22 falsifier via 059, verbatim | Spec 059's recovered mapping (DD-059-3 precedence) | Yes |
| C10 machinery | §6: "Phase-136 machinery unchanged: TERMINAL14, eligibility, CMH, B = 9,999, seed 20261009" | Freeze §§3–6 parameter-by-parameter, as in 059 | Yes; B's enumeration adopted |
| C11 verdict words | D-22 criteria via 059 | Spec 059's recovered mapping with DD-059-12 precedence | Yes |
| C12 NOT ESTIMABLE | §6: "a gate-passed join with too few typed seals/tablets in eligible strata closes as NOT ESTIMABLE under the frozen mapping (Spec 059 §5's provision, carried)" | Spec 024 freeze §5's class, as in 059 | Yes; §6 names the type-fill route explicitly |
| C13 correction | §6 is silent; 059's DD-059-8 is part of the carried design | Combined report: the Spec 024 family is closed | Yes (carried) |
| C14 LOSO + covariates | D-22 method via 059 | Phase-141: LOSO mints no verdicts | Yes |
| C15 append-only | §6: "Spec 059's record is cited, never patched; F1 stands as recorded unless a gate-passed execution earns the §5 re-statement" | Program append-only rule; 059 §7.2 | Yes; B adds the 059 record itself to the protected set |

**Disagreements and resolutions.**

- **D-1 (C04 — the gate bar's route).**
  Derivation A reads §6 as requiring a fresh
  adoption act at this freeze ("its own gate
  bar adopted openly at its freeze"), which
  could in principle set a new number.
  Derivation B notes the design's bar was
  fixed against this layer and this
  denominator, and that Spec 066's outcome
  supplies a projection (4,676 rows) that a
  fresh adoption might be tempted to fit the
  bar to — which would not be a gate.
  **Resolution (DD-067-7):** the adoption act
  is performed openly at this freeze, and what
  it adopts is Spec 059's bar carried
  unchanged — ≥ 61.0% (≥ 3,465 rows) — with
  the basis stated on the record (spec §3.5):
  same design, same layer, same denominator,
  same baseline; the strictest of DD-059-7's
  three readings; and no bar derived from the
  projection, which has no standing. A
  different bar would have required its own
  stated basis before freezing; none is
  offered, because none survives the
  projection-fitting objection.
- **D-2 (C07 — the type-fill census's
  place).** Derivation A places the type-fill
  census inside step 0 as §6 words it
  ("before any F1 quantity exists").
  Derivation B notes Spec 059's step 0 had
  four gates and its §4.1 flow already counts
  type fill as its first step — in the
  gate-passed case. **Resolution:** the census
  is a step-0 gate of this spec (gate 0.4,
  spec §3.4), taken on the newly joined
  objects and the whole joined set whichever
  way the gate falls, and its NOT ESTIMABLE
  consequence is the frozen mapping's
  (F067-C12). §4.1's flow steps are unchanged;
  the census is their step-0 shadow, not a
  new test step.

## 4. Draft-fixed readings (DECIDED-BY-DRAFT; stand unless the freeze overturns them openly)

- **DD-067-1 — The variant appends; the
  frozen verdicts are untouched.** The claim
  under test is `STUDY-SPEC-024/F1`; this
  spec's outcome appends to its record as a
  dated replication record. Spec 024's and
  Spec 059's files and verdicts are never
  edited (claim F067-C15).
- **DD-067-2 — The census unit is the layer
  row.** Carried from DD-059-2: the gate
  compares joined *shares of layer rows*,
  like-for-like with the original 51.0%; two
  rows resolving to one catalogue object both
  count, and the distinct-object count is
  reported descriptively.
- **DD-067-3 — Verdict precedence.** Carried
  from DD-059-3, confirmed at DD-059-12: an
  odds-ratio interval including 1.0 is NOT
  REPLICATED even when q < 0.05; WEAKENED is
  reserved for intervals that exclude 1.0 but
  reach below 1.5 (claim F067-C11).
- **DD-067-4 — Single-test correction
  family, carried.** DD-059-8's ruling is
  part of the carried design (claim
  F067-C13); the freeze confirms it as
  DD-067-8.
- **DD-067-5 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today (§2);
  the Spec 038/042/059 precedent is followed.
- **DD-067-6 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.

## 5. OPEN for the freeze (not decided by this draft)

- **OF-067-1 — The gate bar.** Adopt the
  carried bar — ≥ 61.0% (≥ 3,465 of 5,679
  rows), DD-059-7's reading — openly at the
  freeze with its basis on the record (§3,
  D-1), or adopt a different bar with its
  basis stated on the record before freezing.
  Until the freeze rules, the carried bar
  governs.
- **OF-067-2 — The execution phase.** Allocate
  the next genuinely free phase number from
  the merged record at the freeze.
- **OF-067-3 — OSF registration.** Proposal:
  yes — the frozen spec files its own OSF
  contract registration at its freeze, under
  campaign decision E-1 and Item 7 §6's own
  terms ("a new OSF registration of its own").
  Nothing is filed at draft.
- **OF-067-4 — Whether a separate join audit
  is required.** Proposal: the gate census
  and the type-fill census (§§3.3–3.4),
  published either way, suffice as the join's
  audit (the DD-059-11 form); the freeze
  confirms or requires a fuller audit.

## 6. Defects and weaknesses found at drafting

1. **The projection temptation is this
   draft's principal hazard.** Spec 066's
   outcome projects 4,676 joined rows — far
   above the bar — and a successor drafted in
   its shadow could quietly treat the gate as
   already passed, or fit its bar to the
   projection. Both are refused on the record
   (§3, D-1; spec §§3.5, 7.4): the projection
   has no standing, the bar is carried, and
   the gate is judged on this execution's own
   census, which does not exist yet.
2. **Layer v2's type vocabulary is wider
   than the vols. 1–2 layer's.** The merged
   layer records Seal impressions as a type
   (23 objects) alongside Seals / Tablets /
   Graffiti / Objects / unfilled. The frozen
   flow restricts to {Seals, Tablets} and
   excludes every other recorded type
   descriptively (spec §4.1 step 2); no
   re-mapping of Seal impressions into Seals
   is licensed — that would be a machinery
   change, and machinery identity is what
   makes this a replication.
3. **The type-fill expectation is an
   expectation.** The 126 unfilled-heading
   overlap numbers and the 143 previously
   unfilled objects are intake-record figures;
   the gate-0.4 census measures the joined
   set's actual fill, and the draft asserts
   neither that the census will match them
   nor any eligible-strata count.
4. **No defect was found in the underlying
   records**: every quantity this draft cites
   (51.0% baseline, 2,899 joined at Phase-421,
   the 566-row shortfall, the 2,101-number
   intake census, layer v2's pin and shape,
   F1's OR / CI / q, LOSO stability)
   recomputes or reads back exactly from the
   pinned files on current `main`.

## 7. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   §2 pin re-asserted against the merged
   record and the layer v2 pin asserted on
   the local file — or decline, leaving
   `STUDY-SPEC-024/F1` with its joined-subset
   SUPPORTED record, Spec 059's gate closure,
   and a pinned enlarged catalogue no
   registered design has yet resolved against.
2. Rule on OF-067-1 (the gate bar, with its
   basis on the record), OF-067-2 (the phase),
   OF-067-3 (OSF), and OF-067-4 (join audit);
   and confirm or openly overturn DD-067-3
   and DD-067-4.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 8. Freeze decisions (2026-10-21)

> ## FREEZE ACT — DECIDED — 2026-10-21
>
> The freeze act of 2026-10-21, under the
> owner's approval of 2026-10-21 (amendment
> package Item 7 §6), decided the items §5
> left open. Each resolution is recorded here
> on the record; the register rulings were
> carried into `claims.json` before the AEE
> hooks ran, and the hooks passed over the
> carried register (0.8-draft;
> `aee/freeze-aee-note.md`). Every committed
> pin below was re-derived in the foreground
> by two independent routes — the contents-API
> raw route and the git-blob route — both at
> the merged record (`main` at
> `d195e2d1c5230e919a14ae7d6e9e20a165cab27f`),
> agreeing byte-for-byte, and the local-store
> pins by two further routes (Python `hashlib`
> and `sha256sum`), agreeing. The layer v2 pin
> was asserted on the local file itself:
> SHA-256 and byte count equal to Spec 066's
> outcome pin, with 9,741 rows and 5,529
> distinct objects counted from the file.
> Phase-429 was verified unallocated in the
> merged record (no reference anywhere on
> `main`, by code search at the freeze head)
> before it was allocated here.

- **DD-067-7 — OF-067-1 resolved: the gate
  bar is ADOPTED OPENLY at this freeze as
  Spec 059's bar carried unchanged — joined
  share ≥ 61.0%, i.e. ≥ 3,465 of 5,679 joined
  rows.** This ruling is in the DD-059-7
  form: the bar and its basis are stated on
  the record. Arithmetic, shown in full: the
  baseline is 2,895 / 5,679 = 50.977% (the
  design's rounded 51.0%); 0.61 × 5,679 =
  3,464.19, so ≥ 61.0% is ≥ 3,465 rows, and
  3,464 rows = 60.997% fails. Basis: this
  spec re-runs Spec 059's design on the same
  lineage layer, the same denominator, and
  the same original baseline; the enlargement
  standard the design fixed at DD-059-7 —
  the design's own stated reading, the
  strictest of the three readings recorded
  there (exact-points 60.977% / ≥ 3,463 rows;
  relative 56.1% / ≥ 3,186 rows, or 56.075% /
  ≥ 3,185 on the unrounded base, both refused
  there and refused again here) — is the
  standard the enlarged set must meet for the
  re-test to be the re-test the design
  required. No different bar is adopted, and
  the reason no different bar is adopted is
  also on the record: the only candidate
  source for a new number in the record is
  Spec 066's projection (4,676 rows, 82.34%),
  and a bar derived from a projection would
  be fitted to the expected result — the
  projection is recorded as a projection with
  no standing, and the gate is judged on the
  execution's own census against the carried
  bar. No execution under this spec may
  re-read the bar after the census is known
  (the bar-shopping rival named in F067-C04).
- **DD-067-8 — The single-test family is
  CONFIRMED.** DD-067-4 stands as the freeze's
  ruling, carrying DD-059-8: the confirmatory
  family under this spec is its single primary
  test; the Benjamini–Hochberg adjustment at
  q = 0.05 is over one p-value and the adjusted
  q equals the raw permutation p. The Spec 024
  family (F1/F2/F3) was corrected once, in its
  combined report, and is closed. No wider
  family is declared.
- **DD-067-9 — The sources are NAMED AND
  PINNED, in the DD-059-9 form.** No source is
  invented; every artifact below is on the
  record of record, and its pin was
  re-derived at this freeze as above.
  (a) *Lineage side:* the pinned ICIT-lineage
  (horus84) inscription layer itself — local
  store, SHA-256
  `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`,
  1,190,884 bytes, as recorded in
  `reports/phase136_results.json`. Each row's
  published CISI object reference is its
  `cisi` field, carried as `provenance.object_id`
  under the Phase-130 schema exactly as Spec
  034's route-(b) construction carried it:
  `build_intake_dataset` in
  `backend/glossa_lab/phase398_matched_object.py`,
  SHA-256
  `278f16b0ae8b02b77412cc925ac9e767110f5d5461729b73e8c122a9ff7673f0`
  (40,104 bytes). The converted keyed layer v2
  (`bbfdbcd5…`, 1,586,137 bytes) carries the
  same rows and the same `cisi` values: the
  same source in converted form, not a second
  source. (b) *Catalogue side:* the pinned
  **merged catalogue layer v2** —
  `cisi_catalogue_layer_v2.csv`, restricted
  local store, SHA-256
  `cd0c2ba8823678be9f7573616528ae0b6be2fe579dc7e34c93add421c80886ad`,
  2,655,958 bytes, 9,741 rows, 5,529 distinct
  objects — **pinned here as a definition
  constant** and asserted on the local file at
  this freeze (above) and again at gate 0.1,
  before any join work. Its object key is its
  `cisi_id` column. Also pinned: the Spec 066
  extension index
  (`data/intake/cisi31_extension_index.csv`,
  SHA-256
  `be20439a094d4196352bd8c31fd8eeee3f92cd81d8443786a1c520d8355f2540`,
  78,531 bytes, 2,101 rows), the Spec 066
  freeze digest
  `0b81d8421c8fe66b486b2c729bb7e978faa6327c74b8f1bff7984128a31aa355`,
  the Phase-421 census (SHA-256
  `952829317a7b8e48e809da4353cdf5f6b6f872180920bc349aaf747595b99bb8`)
  and results (SHA-256
  `3948cd01f960842b963061d96ddeabd5ee0b5cdeb572d786976d476d84ff0c7f`)
  pins from Spec 059's executed record, and
  the vols. 1–2 catalogue pins the gate-0.2
  reproduction resolves against (`e0d698f9…` /
  `e751244e…`, as recorded in the Phase-136
  results). (c) *Schema and validator:*
  `data/intake/intake_dataset_schema_v1.json`,
  SHA-256
  `b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b`
  (6,197 bytes), validated by
  `backend/glossa_lab/intake.py`, SHA-256
  `02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03`
  (18,867 bytes). Gate 0.1 asserts every one
  of these pins. What this ruling does NOT
  do: it does not assert the join's outcome.
  Whether the named identifiers, resolving
  against layer v2, reach the carried bar is
  exactly what the gate census measures at
  execution, and a closure at step 0 remains
  a realistic, pre-registered outcome (spec
  §§3.6, 8). The string-identity boundary
  (F067-C06, spec §7.1) and the restricted
  discipline (spec §7.3) are unchanged.
- **DD-067-10 — OF-067-3 resolved: OSF
  registration at the freeze (E-1).** This
  spec files its own OSF contract registration
  at the freeze, under campaign decision E-1
  and Item 7 §6's own terms. The filing record
  is `osf-spec-registration.md`. Execution
  awaits the registration's approval act and
  a separate execution order; no mail is
  handled by the freeze.
- **DD-067-11 — OF-067-4 resolved: the gate
  census and the type-fill census suffice as
  the join's audit.** The §3.3 census and the
  §3.4 type-fill census, published either way
  (the per-row census itself held under the
  restricted discipline of spec §7.3, its
  aggregates committed), are the join's audit.
  No separate join audit is required before
  execution.
- **DD-067-12 — DD-067-3 confirmed; the
  verdict precedence stands.** An odds-ratio
  interval including 1.0 is NOT REPLICATED
  even when q < 0.05, and WEAKENED is
  reserved for intervals excluding 1.0 but
  reaching below 1.5 (carrying DD-059-12).
- **DD-067-13 — Phase-429 allocated.** The
  execution phase is **Phase-429** (completing
  DD-067-6), verified unallocated in the
  merged record before allocation (above).
- **DD-067-14 — The DD-038-10 AEE gate
  reading is adopted.** The lifecycle hooks
  PASS at the freeze when every hook carries
  zero correctness failure modes and no claim
  below the 0.70 threshold; FR-2.3 draft-cap
  records (one per claim) are recorded openly
  and are not edited away — they cap a draft
  bundle's outcome word ("iterate") and are
  lifted only by human ratification, not by
  any freeze act. The hooks' full record is
  `aee/freeze-aee-note.md`.

**Draft decisions confirmed.** DD-067-1
(the outcome appends; the frozen verdicts
are untouched), DD-067-2 (the census unit is
the layer row), and DD-067-5 (`observed_at`
carried from the draft) are confirmed as
drafted. DD-067-4 is confirmed as DD-067-8;
DD-067-3 is confirmed as DD-067-12; DD-067-6
is completed by DD-067-13. No draft decision
is overturned.

**What the freeze does not do.** It runs no
join against layer v2, computes no census,
no type fill, and no F1 quantity; it does not
decide the gate in advance — the census at
execution decides it against the bar
DD-067-7 adopts, and CLOSED AT STEP 0 —
JOIN GATE NOT MET remains a pre-registered
outcome of the frozen contract, not a defect
in it. It edits no Spec 024 or Spec 059
record, moves no anchor, and authorises no
execution by itself.
