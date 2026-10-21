# Spec 050 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign approved by the owner as written
> on 2026-10-21, and the portfolio triage of
> the same date, drafting only). The freeze
> was completed on 2026-10-21 (adjudication
> §7, DD-050-9 to DD-050-15); the execution of
> Spec 050 remains a separate later act under
> the campaign's Waves 2 and 3. This spec is a **dependent**: its
> freeze follows Spec 045's freeze and its
> execution follows Spec 045's Asset A build
> (campaign Wave 3, group 3).

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      design D-13's terminal-enrichment test
      and the Asset A consumption it
      registers), H13 (epistemic boundaries
      stated in spec §7), H15/H23 (execution
      shape is graph-first, spec §10), H16
      (data from the registered sources of
      record: the pinned corpus layer,
      positional record, Phase-43 record, and
      crosswalk; the celestial class from the
      frozen Asset A only), H24 (no private
      correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F050-C01…C15) drafted in
      the Spec 042/045 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-050-8), and each
      claim's acceptance test derived twice
      with disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR on branch
      `spec-050-hunt-sky-signs-endings-draft`
      and left unmerged for the freeze
      decision, CI state reported from the
      run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE
      GATE).** Run at the freeze act of
      2026-10-21 over the recovered register
      0.8-draft under aee 1.5.0: PASS on the
      DD-050-9 reading (zero correctness
      failure modes at every hook, no claim
      below the 0.70 threshold, draft-cap
      records only; `aee/freeze-aee-note.md`).
      Original gate text: at the freeze act,
      run `run_aee.py assess` after_specify,
      after_plan, and after_tasks over the
      claim register, read under the campaign's
      standing reading for draft-lifecycle
      registers; a correctness failure blocks
      the freeze until its named recovery is
      complete and recorded. Any recovery round
      changes claim text, and the freeze
      digest is computed over the recovered
      register exactly once, at freeze.
- [x] **L5 — Freeze-decision items.** Decided
      at the freeze act of 2026-10-21 in
      `adjudication.md` §7: the Asset A
      pin-timing ruling — contract anchor and
      fixed pin source in place of a digest
      quotation, the asset not yet existing
      (DD-050-11); the coverage question,
      resolved on Spec 045's frozen
      full-universe scope with gate 0.3
      standing as drafted (DD-050-12);
      DD-050-1…DD-050-6 confirmed, DD-050-1
      frozen (DD-050-13); the OSF filing
      (campaign E-1; DD-050-14); and the
      calibration question — none beyond gate
      0.5 (DD-050-15).
- [x] **L6 — Freeze.** Completed 2026-10-21
      under the campaign plan approved AS
      WRITTEN, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` computed over the
      recovered register and finalised texts,
      every spec §6 pin re-asserted against
      the merged record by two routes, Spec
      045's freeze digest quoted as the
      contract anchor with `asset-a-freeze.json`
      fixed as the pin source (DD-050-11; no
      Asset A digest exists at the freeze),
      and the execution phase number allocated
      as **Phase-416** (DD-050-10, resolving
      DD-050-7). Freeze order inside the
      campaign: Spec 050 freezes **after**
      Spec 045, whose freeze and asset build
      supply its pin.
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [x] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.3): **EXECUTED 2026-10-21 — gate
      0.1 fired in its absent branch: CLOSED AT
      STEP 0 — ASSET NOT FROZEN (the fixed pin
      source does not exist; `outcome.md` §2);
      gates 0.2–0.3 NOT REACHED.** Asset A digest assertion
      against the digest recorded in the fixed
      pin source, Spec 045's
      `asset-a-freeze.json` (DD-050-11) (an
      unfrozen asset closes as
      CLOSED AT STEP 0 — ASSET NOT FROZEN; a
      mismatch as CLOSED AT STEP 0 — ASSET
      PIN MISMATCH); input integrity;
      coverage and join completeness. Any
      failure stops the run before any
      counting.
- [ ] **E3 — Step 0, part 2** (gates
      0.4–0.6): class census, totals only
      (a TOO THIN closure ends the execution
      here, with the census as its finding);
      positional reproduction (805 / 2,267
      and the 40 / 61 / 20 classes);
      freeze-order proof. Any other failure
      stops the run as INVALID.
- [ ] **E4 — Primary** (spec §4): the pooled
      enrichment test against the
      frequency-matched comparison class, the
      full per-sign table, the
      half-of-occurrences condition computed
      from it, both sensitivity arms (S1
      borderline removed; S2 contested
      included under CISI-governed
      `sky_cycle` labels), and the pooled /
      per-sign reconciliation. A
      reconciliation failure records NOT
      ADJUDICATED with the counts published.
- [x] **E5 — Outcome:** **EXECUTED 2026-10-21 —
      `outcome.md` records the gate-0.1
      dependency closure in the pre-written
      §5.2 wording; the §9 headline quantities
      do not exist and the record says so.** The §9 record —
      results JSON and report under the
      headline rules (claim identifier, Asset
      A digest and class census, both pooled
      rates, the ratio, the exact test, the
      half-of-occurrences share, the verdict
      word or closure class in its pre-written
      §5.2 wording, the §7 limit in plain
      words), the appended outcome in this
      directory, and the LEDGER entry; anchors
      asserted byte-identical before and
      after; foundation check reported as
      measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
