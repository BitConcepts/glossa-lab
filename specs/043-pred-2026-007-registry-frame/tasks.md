# Spec 043 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's successor order of
> 2026-10-21, drafting only; §6 the campaign
> ruling E-4; §7 the freeze decisions). The
> freeze was taken under the campaign plan
> approved AS WRITTEN on 2026-10-21 (Wave 2,
> delegated), which is also this member's Wave 3
> execution authorization (`adjudication.md`
> §7.6); the execution tasks run as Phase-410
> under the frozen contract, awaiting the OSF
> registration's verified approval.
>
> **Freeze repair (2026-10-21, pre-merge):** the
> freeze PR's first CI run failed on exactly one
> test — Spec 029's Phase D register pin
> (`test_pred_register_document_untouched`),
> stale since the Wave-1 PRED-2026-012 append.
> The pin was advanced an eighth time, by name,
> for that append (insertions-only verified
> against main), in the test's own recorded
> form. The repaired file is not a Spec 043
> digest-covered source, so the freeze digest
> and the OSF registration (vmcra) are
> unaffected.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and claim
      register checked against constitution §§I–VIII
      and governance H2 (spec before code), H6 (no
      scope beyond the corrected scoring the owner's
      successor order names), H13 (epistemic
      boundaries stated in spec §10 and carried in
      the claims' boundaries), H15/H23 (execution
      shape is graph-first, spec §11), H16 (data
      from the registered sources of record: the
      pinned registry, builder, parser, and recorded
      Phase 5 output; published documents D3/D4
      produced at the provenance gate with locators),
      H24 (no private correspondence in the repo).
- [x] **L2 — Claims-first register.** `claims.json`
      (F043-C01…C16) drafted in the Spec 032–042
      register shape. Draft-stage verification:
      dependency integrity over the register and the
      cited-record facts are recorded in
      `adjudication.md` §2; the AEE lifecycle hooks
      have **not** run on this register (L4).
- [x] **L3 — Design PR.** This draft, opened as a
      DRAFT PR and left unmerged for the owner's
      freeze decision, CI state reported from the
      run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).** At the freeze act, run
      `run_aee.py assess` after_specify, after_plan,
      and after_tasks over the claim register under
      the programme's adopted aee pin (1.5.x), with
      the DD-038-10 gate reading for a draft-stage
      register; a stricter outcome blocks the freeze
      until its named recovery is complete and
      recorded. Any recovery round changes claim
      text, and the freeze digest is computed over
      the recovered register exactly once, at freeze.
- [x] **L5 — Freeze-stage verification (FREEZE
      GATE).** Re-verify spec §4's pins against the
      merged record and the executing environment:
      the registry at `8a0b2a82…`, the builder at
      `4af822f1…`, the parser at `9b57f0ec…`, the
      cross-check at `8c2bd605…`, the clustering at
      `623a787d…`, the characterisation at
      `54ebf660…`, and the register at its then-current
      hash. Decide DD-043-10, DD-043-11, DD-043-12;
      DD-043-6's reading stands superseded by
      campaign ruling E-4 (`adjudication.md` §6);
      record DD-043-13's allocation (Phase-410).
      All decided at the freeze (`adjudication.md`
      §7); every pin re-asserted by two routes. Failure of any pin is
      recorded and bars the freeze; no pin is
      refreshed silently.
- [x] **L6 — Freeze.** On the owner's freeze order,
      with L4 and L5 passed: hooks recorded,
      `freeze.md` finalised, `freeze.json` computed
      over the recovered register and finalised
      texts, the execution phase number allocated
      (DD-043-13).
- [ ] **L7 — Freeze PR merged**, house gates green
      (full suite, branding sweep, foundation check
      reported as measured).

## Execution — gated on the freeze and a separate execution order

- [x] **E1 — Graph-first build** (H15/H23):
      experiment script, graph module, registration
      in the experiment graph, then run. DONE
      2026-10-21 (Phase-410): script
      `backend/scripts/phase410_pred012_step0.py`,
      graph module
      `backend/glossa_lab/experiment_graph_phase410.py`
      (node `IndusPhase410Pred012Step0`), registration
      verified by import before the run.
- [x] **E2 — Step 0, check 0.1: sources and pins.**
      Every source of spec §4 present and hashed at
      the frozen commit; a missing source or a hash
      differing from the frozen pin closes the study
      as CANNOT BE RUN AS WRITTEN. DONE 2026-10-21:
      PASS — all seven pins matched, re-derived by
      two independent routes.
- [x] **E3 — Step 0, check 0.2: enumeration,
      re-derivation, cross-check.** Mechanical read
      of the registry's `icit_function` over all 803
      rows; re-derivation of all 803 values from the
      pinned builder rule; reconciliation against the
      draft census (ITM = {P056, P324, P378, P385});
      held-record verification (P385, P378 present
      as ITM; P098 not ITM); the cross-check read
      over the whole CGSA analysis file with every
      disagreement written sign-by-sign into the
      step-0 record. Any census, re-derivation, or
      within-primary ambiguity failure closes the
      study as CANNOT BE RUN AS WRITTEN. DONE
      2026-10-21: PASS — census reproduced exactly;
      re-derivation exact (zero mismatches);
      cross-check disagreements all of the expected
      kind, recorded sign-by-sign.
- [x] **E4 — Step 0, check 0.3: the provenance
      gate.** Produce D3 (Fuls 2013) and D4 (Wells'
      published sign list, as transmitted by the
      ICIT documentation) with locators; determine
      the three limbs (class definition; per-sign
      basis for P056, P324, P378, P385; source
      agreement) under the standard the freeze fixed
      (DD-043-10); trace the LOG assignments in the
      same form. Any failure closes the study as
      **PROVENANCE — CANNOT BE RUN AS WRITTEN**,
      unscored, with the quoted basis statements (or
      their absence) in the step-0 record. **No
      Phase 5 read of any kind precedes this check's
      determination.** DONE 2026-10-21: the gate ran
      and FAILED on all three limbs — the class
      definition the produced documents state is
      positional, every stated per-sign basis is
      positional (and W231 has none), and the
      published lists assign different functions
      (the published ICTM class is signs 060, 001,
      002). The study closed as **PROVENANCE —
      CANNOT BE RUN AS WRITTEN**, unscored; the LOG
      trace is recorded and gates nothing. Record:
      `outcome.md`.
- [ ] **E5 — Step 0, check 0.4: recorded Phase 5
      output verification.** The recorded clustering
      and characterisation survive in sign-assignable
      form; the sanity anchor reproduces (P385 →
      Cluster 21 TERMINAL, P378 → Cluster 39
      TERMINAL, P098 → Cluster 10 INITIAL). Failure
      closes the study as CANNOT BE RUN AS WRITTEN.
      The step-0 record is written and hashed before
      any scoring. NOT REACHED 2026-10-21 — closed
      in substance by the check-0.3 PROVENANCE
      closure: the frozen order reaches this check
      only behind a passed gate, and no Phase 5
      assignment was looked up for any sign.
- [ ] **E6 — Scoring** (spec §6): the registered
      computation only, over the enumerated
      population, under the coverage rule (spec §7);
      the per-sign table produced with it (and, if
      the freeze so ruled under DD-043-12, the LOG
      control's descriptive share). NOT REACHED
      2026-10-21 — closed in substance by the
      check-0.3 PROVENANCE closure; no share,
      coverage, or verdict exists.
- [x] **E7 — Outcome.** The verdict, the
      partial-scope record, or the closure under its
      own name, in spec §7's pre-written wordings —
      appended to the PRED register as a dated §6
      entry (spec §8; the Phase D pin advanced by
      name), recorded in this spec's directory and
      the root LEDGER; the foundation check (H21)
      run after the claim consequence lands; nothing
      written into any frozen record. DONE 2026-10-21:
      the PROVENANCE closure is recorded in
      `outcome.md` in spec §7's pre-written wording,
      appended to the register as a dated §6 entry
      (the Phase D pin advanced by name a ninth
      time), and entered in the root LEDGER; the
      foundation check runs at the record's merge
      commit.

## Not done by this draft (by design)

- No AEE hooks run; no freeze digest computed; no
  OSF filed (DD-043-11 open).
- The provenance gate is designed, not run: no
  D3/D4 document produced or adjudicated.
- No Phase 5 assignment looked up for any sign
  beyond the register's three named signs (P056,
  P324, P310 untouched); no share, coverage figure,
  or verdict computed.
- The only computations performed are the registry
  census and the re-derivation check — population-
  side design inputs the corrected frame requires,
  disclosed in `adjudication.md` §2.
- The PRED register is not edited; PRED-2026-007
  stands PARTIALLY CONFIRMED, unscored at full
  population, exactly as Spec 038 left it.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
