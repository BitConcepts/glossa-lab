# Spec 046 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign plan approved AS WRITTEN on
> 2026-10-21 — D-18 is campaign member 13 —
> and the portfolio triage of the same date,
> drafting only). The freeze and the
> execution of Spec 046 are separate later
> acts under the campaign.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-18 identification concordance for
      this one fragment), H13 (epistemic
      boundaries stated in spec §9), H15/H23
      (execution shape is graph-first, spec
      §12), H16 (data from the registered
      sources of record: the held source
      book, the four published lists, the
      pinned crosswalk registry), H24 (no
      private correspondence in the repo),
      H26 (no semantic-anchoring machinery is
      used as a gate for anything in this
      spec — the check is concordance over
      quoted published identifications).
- [x] **L2 — Claims-first register.**
      `claims.json` (F046-C01…C15) drafted in
      the Spec 042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-046-8). Acceptance
      tests were derived twice independently;
      disagreements and resolutions are
      recorded in `adjudication.md` §5. The
      AEE lifecycle hooks have **not** run on
      this register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      freeze decision, CI state reported from
      the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).**
      Run at the freeze act of 2026-10-21 over
      the recovered register 0.7-draft under
      aee 1.5.0: PASS on the DD-046-16 reading
      (zero correctness failure modes at every
      hook, minimum propagated 0.72, draft-cap
      records only). Original gate text: At the freeze
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
- [x] **L5 — Freeze-decision items.** Decided
      at the freeze act of 2026-10-21 in
      `adjudication.md` §7 (DD-046-9 to
      DD-046-15). Original text: the
      freeze decides OPEN-1 (the PARTIAL
      CONCURRENCE word), OPEN-2 (Wells list
      of record), OPEN-3 (CISI list of
      record), OPEN-4 (Mahadevan edition of
      record), OPEN-5 (list lineage note),
      OPEN-6 (the Spec 045 delivery-form
      cross-check against spec §6), and
      OPEN-7 (dry-run check), and confirms or
      openly overturns DD-046-2, DD-046-3,
      and DD-046-6.
- [x] **L6 — Freeze.** Taken at the freeze act
      of 2026-10-21 under the campaign plan
      approved AS WRITTEN (Wave 2), with L4 passed
      and L5 decided: hooks recorded,
      `freeze.md` finalised, `freeze.json`
      recomputed over the recovered register
      and finalised texts, every spec §2 pin
      re-asserted against the merged record,
      the list editions of record fixed in
      spec §2, the execution phase number
      allocated (DD-046-7), and the spec's OSF
      contract registration filed under
      campaign decision E-1.
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and the campaign's execution pass

Campaign order (plan Part 4, Wave 3):
**Spec 046 executes in group 1, before
Asset A freezes.** Its `concordance-297.json`
— in whatever terminal state it reaches,
including an empty-feed closure — must exist
before Spec 045's step 1 build consumes it.

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [x] **E2 — Step 0** (spec §3 gates
      0.1–0.3): input integrity against the
      freeze pins; source book produced from
      the held copy with the §1 passage
      located verbatim; each of the four
      lists accounted for as HELD or CITABLE
      with citation plus locator form. Any
      failure closes the run as CLOSED AT
      STEP 0 in the named class, produces
      `concordance-297.json` with its closure
      block, and ends the execution here.
- [x] **E3 — Step 1, identification** (spec
      §4): the source's sign list named from
      the book's own apparatus; Wells's sign
      297 matched by drawn form to a
      crosswalk-registry entry or to Wells's
      published list entry, citation attached,
      match basis and reference recorded.
      Number-matching is forbidden (F046-C07).
      A failure closes the run as
      IDENTIFICATION FAILED with the reason
      named, with the closure-form delivery.
- [ ] **E4 — Step 2, concordance** (spec
      §5): the four list rows quoted verbatim
      at their locators and scored AGREE /
      DISAGREE / SILENT (with `entry_present`);
      the per-sign concurrence state computed
      by the §5.2 mapping alone — Wells scored
      as SOURCE and never counted toward
      CONSENSUS. Asset A material, D-05
      labels, and positional results are not
      consulted at any point (F046-C12).
- [ ] **E5 — Delivery and outcome** (spec
      §§6, 8): `concordance-297.json` written
      in the §6 form with its `asset_a_feed`
      block; the outcome append in this
      directory under the §5.3 wording for
      the outcome reached, carrying the §8
      reporting obligations; the appended
      first-check entry on the claim
      `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`'s
      record; the handover of the delivery
      file to Spec 045's Asset A build
      recorded (or, on a closure, the
      empty-feed state recorded for it); the
      LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.


## Execution record — 2026-10-21 (Phase-405)

Executed in Wave 3 group 1 under the frozen
contract, the OSF gate satisfied (dnts8 approved
+ public). **E1 done** (graph-first build;
registration verified by import before the run).
**E2 done** (step 0 passed in full). **E3 done**
(the list was named from the apparatus; the drawn
sign could not be matched — the execution closed
as IDENTIFICATION FAILED (sign unmatched) with
the closure-form delivery, as E3 prescribes).
**E4 not reached** (no scoring on a step-1
closure; left unchecked deliberately). **E5
substantially done** — delivery, outcome record,
claim first-check append, LEDGER entry, and the
anchors assertion are all on this record; the
foundation-check figure is appended to
`outcome.md` §7 after the record merge, in the
Spec 039 completion pattern, at which point E5
is checked. Outcome record: `outcome.md` in this
directory.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
