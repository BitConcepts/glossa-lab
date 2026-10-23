# Spec 073 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-22
>
> Adjudication inputs are recorded in
> `adjudication.md` (the merged outcome
> records of Specs 070 and 071; Spec 069's
> executed Asset A record; Spec 045's
> frozen §§2–3; the pinned registry,
> crosswalk, and intake record). The
> freeze, the registration, and the
> execution of Spec 073 are separate later
> owner acts.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance
      H2 (spec before code), H6 (no scope
      beyond the repair the two outcome
      records name), H13 (epistemic
      boundaries stated in spec §8), H15/H23
      (execution shape is graph-first, spec
      §12), H16 (data from the registered
      sources of record: the pinned registry,
      crosswalk, and Asset A v1 by hash; the
      Shakti corpus only through the intake
      record; depictions only from the
      published sources of spec §2), H24 (no
      private correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F073-C01…C16) drafted in
      the Spec 042–072 register shape, at
      `0.5-draft`, with `observed_at` carried
      on evidence items from this draft and
      the acceptance tests for each claim
      derived twice independently,
      disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the
      freeze act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register;
      the gate is **pass** (per DD-038-10),
      and a stricter outcome blocks the freeze
      until its named recovery is complete and
      recorded. Deliberate ordering (the
      Spec 035/038 record): any recovery
      round changes claim text, and the
      freeze digest is computed over the
      recovered register exactly once, at
      freeze.
- [x] **L5 — Freeze-decision items.** The
      freeze decides OPEN-073-1 (the governing
      source list and hierarchy, including
      Wells 1998's standing), OPEN-073-2
      (Registry v2's form and the `icit_wells`
      value), OPEN-073-3 (the attested frame),
      OPEN-073-4 (the `row_origin` field),
      OPEN-073-5 (entry checking), OPEN-073-6
      (concordance inputs vs direct entry),
      OPEN-073-7 (the OSF contract
      registration), OPEN-073-8 (the execution
      phase number), and OPEN-073-9 (every §2
      pin re-asserted against the merged
      records, including the Fuls volumes'
      bibliographic pins), and confirms or
      openly overturns DD-073-1…DD-073-7.
- [x] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` computed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted, the
      execution phase number allocated
      (OPEN-073-8), and the OSF contract
      registration filed under OPEN-073-7's
      ruling if the freeze confirms it.
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [x] **E1 — Graph-first build** (H15/H23):
      step-0 exhibits script, Registry v2
      builder, entry tooling, and coverage
      script registered as a graph, then run
      in the order below.
- [x] **E2 — Step 0** (spec §3 gates
      0.1–0.4): frozen-input integrity
      (INPUT PIN MISMATCH / SHAKTI INTAKE NOT
      REPRODUCED on failure); baseline
      reproduction, figure by figure
      (BASELINE NOT REPRODUCED on failure);
      sources in hand, each exhibited with
      its pin (SOURCE NOT IN HAND, named, on
      failure); blind-entry setup attested.
      Nothing is entered before these
      exhibits.
- [x] **E3 — Registry v2 build** (spec §4):
      v1 rows carried verbatim; Wells-map
      completions and `icit_wells` rows added
      only on cited published statements;
      change schedule emitted by machine diff
      against pinned v1; CONTESTED IDENTITY
      entries recorded, never resolved; the
      NO PUBLISHED IDENTITY schedule drafted
      for the attested frame; CSV
      writer-generated and round-trip
      validated; digest computed.
- [x] **E4 — Frame enumeration and blind
      entry** (spec §5): the attested frame
      enumerated from the pinned corpus
      (documented + corroborated rows, per
      the freeze's OPEN-073-3 ruling) and
      published with its count; new rows
      entered blind under the ruled hierarchy
      (two-pass entry with the log published
      as `asset-a-v2/entry-decisions.json`);
      disputes coded contested with both
      labels; silence coded `unidentified`
      with sources searched.
- [x] **E5 — Build gates** (spec §5.4):
      B1 universe completeness, B2 citation
      completeness, B3 carried-row fidelity,
      B4 blind-entry attestation, B5 digest
      recomputation (ASSET FAILED with the
      gate named, or ENTRY DISCIPLINE FAILED,
      on failure).
- [x] **E6 — Coverage measurement** (spec
      §6): the v2-route joins over the
      recorded populations; M1–M5 computed
      and exhibited with remainders listed
      sign by sign; the five named codes'
      dispositions stated by name; the
      celestial census stated plainly beside
      Spec 071's recorded floor of 30, as a
      comparison of numbers only.
- [x] **E7 — Outcome:** the §10 record —
      results JSON and outcome report under
      the headline rules (the P-F1 S3 lineage
      statement in the headline block, both
      product digests and censuses, the
      change schedule and the §4.3 schedule
      in full, M1–M5 with M5 in the headline),
      the appended outcome in this directory,
      the closing re-assertion of the v1 pins
      (FROZEN INPUT MUTATED voids the products
      if it fails), and the LEDGER entry.
      No append to the records of Specs 045,
      069, 070 or 071, and none to either Hunt
      claim's record.

---

*AI disclosure: executed by an AI agent (Muse,
via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
