# Spec 056 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign plan approved AS WRITTEN on
> 2026-10-21 — D-17 is campaign member 12 —
> and the portfolio triage of the same date,
> drafting only). The freeze and the
> execution of Spec 056 are separate later
> acts under the campaign.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-17 recovery of this one fragment),
      H13 (epistemic boundaries stated in spec
      §10), H15/H23 (execution shape is
      graph-first, spec §13), H16 (data from
      the registered sources of record: the
      pinned held source document, claim
      record, Phase-104 evaluation, and
      crosswalk registry), H24 (no private
      correspondence in the repo), H26 (no
      semantic-anchoring machinery is used as
      a gate for anything in this spec — the
      recovery test is quotation against a
      pinned passage).
- [x] **L2 — Claims-first register.**
      `claims.json` (F056-C01…C15) drafted in
      the Spec 042/046 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-056-8). Acceptance
      tests were derived twice independently;
      disagreements and resolutions are
      recorded in `adjudication.md` §5. The
      AEE lifecycle hooks have **not** run on
      this register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      freeze decision, CI state reported from
      the run's own conclusions.
- [ ] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the freeze
      act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register; the
      gate is **pass**, and a stricter outcome
      blocks the freeze until its named
      recovery is complete and recorded.
      Deliberate ordering (the Spec 035/038
      record): any recovery round changes
      claim text, and the freeze digest is
      computed over the recovered register
      exactly once, at freeze. Freeze
      mechanics are re-checked against the
      adopted 1.5.x engine at the freeze
      rather than assumed from pre-adoption
      habit (campaign plan, Wave 2).
- [ ] **L5 — Freeze-decision items.** The
      freeze decides OPEN-1 (passage digest
      re-computed and bounds confirmed),
      OPEN-2 (the IDENTIFICATION FAILED
      closure), OPEN-3 (the recovered claim's
      placement), OPEN-4 (Figure 6.13 and the
      glyph slots), OPEN-5 (the two-pass
      mechanics), OPEN-6 (the retirement's
      reach across program surfaces), OPEN-7
      (dry-run of the recovery test), and
      OPEN-8 (the test-design note's depth),
      and confirms or openly overturns
      DD-056-1, DD-056-2, DD-056-3, and
      DD-056-5.
- [ ] **L6 — Freeze.** On the owner's freeze
      order under the campaign, with L4 passed
      and L5 decided: hooks recorded,
      `freeze.md` finalised, `freeze.json`
      recomputed over the recovered register
      and finalised texts, every spec §2 pin
      re-asserted against the merged record,
      the passage digest pinned byte-exactly,
      the execution phase number allocated
      (DD-056-7), and the spec's OSF contract
      registration filed under campaign
      decision E-1.
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and the campaign's execution pass

Campaign order (plan Part 4, Wave 3):
**Spec 056 executes in group 2, the
independent executions.** It consumes no
shared asset and no member's output, and no
member consumes its output inside the pass.

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0** (spec §3 gates
      0.1–0.3): input integrity against the
      freeze pins; passage produced from the
      held copy with both anchor lines and
      the anchor sentence located verbatim;
      passage slice recomputed to its
      freeze-pinned digest. Any failure
      closes the run as CLOSED AT STEP 0 in
      the named class, produces the outcome
      record with the gate record, and ends
      the execution here. A passage that is
      not producible and pinnable is never
      approximated.
- [ ] **E3 — Step 1, re-extraction** (spec
      §4): two independent extraction passes
      over the pinned passage only, each
      producing its extraction sheet with
      verbatim quotes and locators; the
      reconciliation building the union
      candidate set, settling disagreements
      by quotation or recording them as
      unsettled (unsettled resolves against
      recovery).
- [ ] **E4 — Step 2, the recovery test**
      (spec §5): each reconciled candidate
      checked against R-1…R-5 with the
      failing condition named; the R-3
      identification routes (registry by drawn
      form, or the source list's own entry —
      never a number match) run only for
      candidates that reach them. The outcome
      word assigned by spec §6's mapping
      alone. On RECOVERED, the test-design
      note drafted for the recovered claim —
      designed, not run.
- [ ] **E5 — Outcome** (spec §§6–8): the
      outcome record under the §6.1 wording
      for the outcome reached, carrying the
      §8 reporting set (passage identification
      in full, both sheets and the
      reconciliation or the gate record, the
      per-candidate checklists, the fence
      sentence); the §7 append — on RECOVERED
      the restatement entry on the fragment's
      claim record (stage created, status
      untested), on RETIREMENT RECOMMENDED the
      disposition entry recording the
      retirement in exactly §7's form, on
      IDENTIFICATION FAILED the closure entry
      naming the gap and the unblocking act;
      the LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.
      No prior record is edited or deleted
      at any point.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
