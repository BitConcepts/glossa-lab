# Spec 059 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The approved runnable-experiments
>    campaign** (owner approval 2026-10-21 of
>    the campaign plan as written,
>    `~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`):
>    Spec 059 is campaign member 16 of 20,
>    drafting design D-22 in the campaign's
>    Wave 1. Per the plan's Part 7, D-22's
>    join gate is a named per-experiment
>    tripwire: a gate failure closes this
>    experiment with its pre-written wording
>    and the pass continues.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-22 found **RIPE** — "Its step-0
>    gate (does an object-identifier join beat
>    the original 51% joined share by 10
>    points?) is a real test on routes now
>    proven in hand: Spec 034 joined 5,018
>    ICIT inscriptions to CISI object
>    references through the Phase-130 schema.
>    Spec 037's census warns that
>    identity-by-*string*-matching conflicts
>    at 49% (mostly object type) — this design
>    already specifies object identifiers, so
>    the warning sharpens the gate rather
>    than blocking it."
> 3. **Design D-22 itself** (PR #195 packet,
>    `docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
>    §D-22), which governs this draft's
>    substance.
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 059: both remain
> separate acts under the campaign's freeze
> wave (Wave 2) and execution pass (Wave 3).

## 1. The adopted basis (operative substance)

- **The design.** D-22: Spec 024 F1's
  seal/tablet TERMINAL14 test, re-run on a
  corpus joined through object identifiers
  rather than catalogue concordance — gated at
  step 0 on whether the object-ID join beats
  the original 51.0% joined share by 10 points.
  The F1 test is specified for the gate-passed
  case only.
- **The claim.** `STUDY-SPEC-024/F1`:
  SETTLED — SUPPORTED on its joined subset
  (OR 2.384, CI [1.847, 3.077], family
  q = 0.00015, Phase-141 LOSO-stable). The
  claim's not-understood text names the
  silent 49.0% as its open point; this spec
  is that open point's registered answer.
- **The join route.** Object identifiers
  carried as cited provenance data through
  the Phase-130 intake schema (Spec 021),
  joined to the CISI catalogue layer's object
  IDs. Proven at scale by Spec 034 route (b):
  5,018 ICIT inscriptions admitted through
  the schema (validation verdict pass),
  joined on `provenance.object_id` only.
- **The boundary.** Object IDs, never string
  identity (Spec 037's census: 693
  exact-string matches — 269 VERIFIED / 341
  CONFLICT (49.21%) / 83 UNRESOLVED). Stated
  as spec §7.1 and claim F059-C06.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
against `main` at `83b6a563402b02809ab1143848e4dd2c0cfd9de3`
(re-read at the start of this drafting act):

- **Design D-22** — read in full in the local
  campaign designs copy (identical packet
  text): the open point, step-0 gate text
  ("at least 10 points (to 61% or more)"),
  hypothesis, falsifier ("interval includes
  1.0, or the point estimate falls below
  1.5"), method ("the identical test as
  Phase-136 … same family correction across
  the Spec 024 family"), criteria
  (REPLICATED / WEAKENED / NOT REPLICATED),
  controls, and the not-established line.
- **Phase-136 record** — read on `main`:
  `reports/phase136_results.json` (flow,
  parameters, strata), the Phase-136 report,
  and the Stage 2(a) freeze in full (§§0–8:
  the concordance join rule, the flow audit
  counts, TERMINAL14's 14 signs, eligibility
  N ≥ 20 / ≥5 / ≥5, the 80%-of-cells
  estimability rule, B = 9,999, seed
  20261009, the language fences). The
  original joined share is 2,895 / 5,679 =
  50.977% — the design's "51.0%".
- **The verdict of record** — the combined
  Stage 2 report's family table: F1 raw p
  0.0001 → BH q 0.00015 → SUPPORTED; F2 NOT
  SUPPORTED; F3 SUPPORTED.
- **Phase-141** — LOSO report read: F1
  STABLE, all three dropped-site intervals
  excluding 1, and its explicit rule that
  LOSO mints no verdicts.
- **Spec 034 outcome** — read on `main`:
  route (b)'s 5,018-inscription Phase-130
  admission and `provenance.object_id` join;
  route (a)'s catalogue layer (7,705 rows,
  3,493 distinct objects); its gate census
  published as a finding (the pattern §3.5
  follows for this spec's closure).
- **Spec 037 outcome** — read on `main`: the
  693-candidate census (269 / 341 / 83;
  CONFLICT 49.21%, almost all on object
  type); the spine halted by its own rule.
- **Spec 021 (Phase-130)** — read on `main`:
  schema v1 fields (per-inscription
  `provenance` with `source_reference`
  required; declared `object_type`), the
  validator's hard license gate, and
  duplicate-ID rejects.
- **Gate arithmetic** — computed at this
  draft: 0.61 × 5,679 = 3,464.19, so ≥ 61.0%
  is ≥ 3,465 rows (3,464 rows = 60.997%,
  fails); the exact-points reading
  (50.977% + 10) is 60.977%, ≥ 3,463 rows;
  the relative reading (51.0% × 1.10) is
  56.1%, ≥ 3,186 rows (≥ 3,185 on the
  unrounded base).
- **Input pins** — recomputed at this draft
  from `main` and stated in spec §2:
  phase136_results.json `11a07413…`,
  stage2a-freeze.md `c65a4b9b…`,
  phase136_terminal_type.py `d5ceec46…`,
  phase141_report.md `d442f8d2…`,
  combined Stage 2 report `6a4f5d26…`,
  canonical_sign_registry.csv `8a0b2a82…`
  (equal to the value Phase-136 recorded for
  it), Spec 034 outcome `c0cc615d…`, Spec 037
  outcome `28e444f2…`, anchors `df0cf620…`
  (fresh recompute, per the Spec 040
  stale-pin precedent). The local-store pins
  (horus84 layer `c368f290…`; catalogue vols
  `e0d698f9…` / `e751244e…`) are carried **as
  recorded in the Phase-136 results**, and
  spec §2 says so; they are re-asserted by
  recompute at the freeze.
- **Not done at draft, by design** — the
  object-ID join census has **not** been
  computed: no row of this layer has been
  joined by object ID under this spec, no
  joined share exists, and no F1 quantity on
  any enlarged set was calculated. No code
  was written or run, the AEE hooks have not
  run, and nothing was filed with OSF.

## 3. The doubled derivation of acceptance tests (doctrine record)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived **twice,
independently, from the requirement alone**:
Derivation A worked from the design text
(D-22) alone; Derivation B worked from the
frozen record alone (Spec 024's Stage 2(a)
freeze, the Phase-136/141 records, Specs
034/037/021). Where the two derivations
disagreed, the disagreement and its
resolution are recorded here; the register
carries the resolved form.

| Claim | Derivation A (from D-22) | Derivation B (from the frozen record) | Agree? |
|---|---|---|---|
| C01 scope | Inspection of outputs against the design's question | Inspection against the freeze §8 language fences | Yes |
| C02 record | Design header's recorded OR/CI/q | Direct read of the three record files + hash pins | Yes (B adds the hash test; adopted) |
| C03 baseline | Design's "51%" + "49.0% could not be joined" | Freeze §3 / results flow: 2,895 matched of 5,679 = 50.977% | Yes, after B fixed the exact counts A lacked |
| C04 gate | Design text: "≥ 61%", else closure | (Record is silent — the gate is the design's, not the record's) | **Disagreed — see D-1** |
| C05 join construction | "CISI catalogue object IDs + Phase-130 route" | Spec 034 route (b): `provenance.object_id` only; per-row provenance; resolution classes | Yes, B supplied the mechanism |
| C06 string boundary | Design says "object identifiers rather than concordance" | Spec 037 census grades string identity at 49.21% CONFLICT | Yes; B quantified the boundary |
| C07 fail-closed | Gate-first structure of the design | Program gate pattern (Specs 034/042 §§3/9) | Yes |
| C08 hypothesis | Design step 1, verbatim | No record counterpart (the hypothesis is new) | Yes (A governs) |
| C09 falsifier | Design falsifier, verbatim | Freeze §2's family falsifier form (q-based) | **Disagreed in form — see D-4** |
| C10 machinery | "Identical test as Phase-136" | Freeze §§3–6 parameter-by-parameter | Yes; B's enumeration adopted |
| C11 verdict words | Design criteria block | — (new words; the record has only SUPPORTED) | **Disagreed internally — see D-2** |
| C12 NOT ESTIMABLE | Design does not name it | Freeze §5 names it, with its rule | Yes (B governs; class adopted) |
| C13 correction | Design: "same family correction across the Spec 024 family" | Combined report: that family was corrected once and closed | **Disagreed — see D-3** |
| C14 LOSO + covariates | Design: LOSO "as in Phase-141"; covariate comparison | Phase-141: LOSO mints no verdicts, qualifies language only | Yes; B's no-verdict rule adopted |
| C15 append-only | Design: "the original verdict is not edited in any case" | Program append-only rule | Yes |

**Disagreements and resolutions.**

- **D-1 (C04 — the gate bar).** Derivation A
  reads the design's "by at least 10 points
  (to 61% or more)" as fixing the bar at
  61.0%. Derivation B notes the phrase "10
  points" is not self-interpreting: on the
  unrounded baseline the points reading gives
  60.977% (≥ 3,463 rows), and a relative
  reading gives 56.1% (≥ 3,186 rows). The
  design's own parenthetical states 61% —
  the points reading on the rounded baseline.
  **Resolution:** the draft carries the
  design's stated 61.0% (≥ 3,465 rows) as
  operative — it is also the strictest
  reading, so no reading the freeze might
  adopt can make a passed gate retroactively
  failed — and records all three readings as
  OPEN item OF-059-1 for the freeze to
  confirm or replace openly. Nothing is
  silently picked: every reading, with its
  row count, is in spec §3.4 and claim
  F059-C04's boundary.
- **D-2 (C11 — verdict precedence).** The
  design's criteria, read literally, overlap:
  with q < 0.05 and an interval including
  1.0, both WEAKENED ("interval reaches below
  1.5") and NOT REPLICATED ("interval
  includes 1.0") apply. **Resolution
  (DD-059-3):** NOT REPLICATED governs where
  the interval includes 1.0, because the
  design's falsifier names inclusion of 1.0
  first; WEAKENED is reserved for intervals
  that exclude 1.0 but reach below 1.5. The
  freeze may overturn this openly.
- **D-3 (C13 — the correction family).**
  Derivation A carries the design's words
  (correct across the Spec 024 family).
  Derivation B objects: that family's
  correction was computed once, in the
  combined report, over F1/F2/F3, and is a
  closed record; re-running it with a new p
  would re-adjudicate F2's and F3's closed
  q-values. **Resolution (DD-059-4):** the
  draft proposes a single-test family under
  this spec (BH over one p; q = p), recorded
  as OPEN item OF-059-2. The freeze decides;
  the verdict wordings are stated in q so
  they stand under either ruling.
- **D-4 (C09 — falsifier form).** The
  design's falsifier is stated on the odds
  ratio (interval / point estimate) while its
  criteria are stated on q and the interval
  jointly. **Resolution:** claim F059-C09
  carries the falsifier's clauses and maps
  them onto the verdict words through
  F059-C11, so the falsifier and the criteria
  are one rule, not two.

## 4. Draft-fixed readings (DECIDED-BY-DRAFT; stand unless the freeze overturns them openly)

- **DD-059-1 — The variant appends; the
  frozen verdict is untouched.** The claim
  under test is `STUDY-SPEC-024/F1`; this
  spec's outcome appends to its record as a
  dated replication record. Spec 024's files
  and verdict are never edited (claim
  F059-C15).
- **DD-059-2 — The census unit is the layer
  row.** The gate compares joined *shares of
  layer rows*, like-for-like with the
  original 51.0%; two rows resolving to one
  catalogue object both count, and the
  distinct-object count is reported
  descriptively. A distinct-object share
  would be a different gate from the one the
  design fixed.
- **DD-059-3 — Verdict precedence.** An
  odds-ratio interval including 1.0 is NOT
  REPLICATED even when q < 0.05 (§3, D-2;
  claim F059-C11).
- **DD-059-4 — Single-test correction
  family, proposed.** §3, D-3 (claim
  F059-C13). Labelled a proposal, not a
  settled reading: it is also OPEN item
  OF-059-2.
- **DD-059-5 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today
  (§2); the Spec 038/042 precedent is
  followed.
- **DD-059-6 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.

## 5. OPEN for the freeze (not decided by this draft)

- **OF-059-1 — The gate bar's reading.**
  Confirm the operative bar — the design's
  stated 61.0% (≥ 3,465 of 5,679 rows) — or
  adopt the exact-points reading (60.977%,
  ≥ 3,463 rows) or the relative reading
  (56.1%, ≥ 3,186 rows) by open ruling,
  recorded in the freeze record. Until the
  freeze rules, 61.0% governs (§3, D-1).
- **OF-059-2 — The correction family.**
  Confirm the single-test family proposed in
  DD-059-4, or declare a wider family with
  its membership recorded before execution
  (§3, D-3).
- **OF-059-3 — The object-ID source.** Name
  and pin the exact held source (or sources)
  from which each lineage row's object
  identifier is taken, and pin the Phase-130
  intake schema file (`data/intake/intake_dataset_schema_v1.json`)
  by hash. The draft asserts the route (Spec
  034 route (b)) and the counting rules; it
  does not invent the source. If no held
  source supplies identifiers for this
  layer, that is a freeze-stage finding to
  report — never a licence to substitute a
  string join.
- **OF-059-4 — OSF registration.** Proposal:
  yes — the frozen spec files its own OSF
  contract registration at its freeze,
  following the program's standing pattern
  (campaign decision E-1: every specification
  in the pass registers at its freeze).
  Nothing is filed at draft.
- **OF-059-5 — Whether a separate join audit
  is required.** Proposal: the gate census
  (§3.3), published either way, suffices as
  the join's audit; the freeze confirms or
  requires a fuller audit of identifier
  provenance before execution.

## 6. Defects and weaknesses found at drafting

1. **The gate bar's wording is genuinely
   ambiguous in isolation** ("by 10 points"),
   and the readings differ by up to 280 rows
   of consequence (3,185 vs 3,465 would both
   be "10 points" under some reading).
   The design's parenthetical "(to 61% or
   more)" rescues the intent, but a frozen
   spec cannot rest on a parenthetical: this
   is OF-059-1, and it is the draft's
   principal open item.
2. **The design's "same family correction"
   cannot be executed as written** — the
   Spec 024 family is closed. Recorded as
   D-3 / OF-059-2 rather than silently
   reinterpreted.
3. **The design's criteria overlap** at
   (q < 0.05, interval includes 1.0).
   Resolved by DD-059-3; the overlap itself
   is a defect of the design text the freeze
   should note.
4. **No single pinned artifact yet carries
   this layer's object identifiers** in the
   record this draft could cite: Spec 034's
   route (b) proves the mechanism on ICIT
   inscriptions, but the freeze must name
   the source for *this* layer (OF-059-3).
   The draft flags this rather than asserting
   coverage it did not verify.
5. **No defect was found in the underlying
   records**: every quantity the design
   cites (51.0%, 49.0%, OR 2.384, CI,
   q = 0.00015, LOSO stability) recomputes
   or reads back exactly from the pinned
   files on current `main`.

## 7. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest
   in `freeze.md` / `freeze.json`), with
   every §2 pin re-asserted against the
   merged record and the local-store pins
   recomputed — or decline, leaving
   `STUDY-SPEC-024/F1` with its joined-subset
   SUPPORTED record and its silent 49.0% as
   the program's word: unasked by any
   registered design.
2. Rule on OF-059-1 (the gate bar), OF-059-2
   (the correction family), and OF-059-3 (the
   object-ID source and schema pin); decide
   OF-059-4 (OSF) and OF-059-5 (join audit);
   and confirm or openly overturn DD-059-3
   and DD-059-4.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
