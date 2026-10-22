# Spec 065 — Tasks

> ## PLAN — FROZEN 2026-10-21 (successor recovery act for Spec 057's S-1/S-5 rows)
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's approval of
> 2026-10-21, amendment package Item 6; the
> amendment-queue commission Item 6, whose
> §3 this spec follows). **The freeze, the
> OSF filing, and the execution of Spec 065
> are separate acts. The freeze and the OSF
> filing were taken on 2026-10-21 under the
> owner's approval (amendment package Item 6;
> L4/L5/E1 below); execution remains a
> separate later act.**
> Spec 057's directory is untouched by every
> act in this plan. **No text layer is
> searched by any act in this plan except
> execution (E2–E5).**

## Drafting (this draft)

- [x] **D1 — Predecessor record verified
      against the frozen record.** Spec
      057's spec (§5 heading rule, §4 step 4),
      outcome (class C; §§4.1–4.2), adjudication
      (incl. defect D-2), freeze record, and
      registration record read in full; its
      freeze digest and the two rows' pins
      recomputed from `main` at 7e483e74 —
      `adjudication.md` §2.
- [x] **D2 — Acquisition posture verified
      first-hand.** The acquired S-5 file
      asserted locally (657,863 bytes; SHA-256
      `77f10f32…`; MD5 `36616e20…` matching the
      Zenodo record), its CC-BY-4.0 licence and
      established edition relationship read
      from PROVENANCE.md entry 23 and
      `edition-comparison.md`; S-1's blocker
      read from `BLOCKED.md` and the
      PROVENANCE.md blocked section. No §5
      search was run on any document.
- [x] **D3 — This draft.** `spec.md`,
      `claims.json` (register 0.5-draft,
      F065-C01…C15), `adjudication.md`,
      `tasks.md`, opened as a PR for the
      freeze decision. Spec 057's directory
      untouched.

## Lifecycle (freeze gate)

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance
      H2, H6 (no scope beyond the two rows'
      document-layer resolution), H13
      (epistemic boundaries stated in spec
      §9), H15/H23 (execution shape is
      graph-first, spec §12), H16 (data from
      the registered sources of record: the
      pinned §2 set), H24 (no private
      correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F065-C01…C15) drafted in
      the Spec 057 register shape, with
      `observed_at` carried on evidence items
      from this draft. The AEE lifecycle hooks
      ran at L4.
- [x] **L3 — Design PR.** This draft, opened
      as a PR for the freeze; CI state, when
      reported, is reported from the run's
      own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE
      GATE).** DONE 2026-10-21 at the freeze
      act: `aee assess` (lenient load) run
      after_specify, after_plan, and
      after_tasks over the claim register;
      pass requires zero correctness failure
      modes and no claim below the 0.70
      threshold at every hook (the DD-038-10
      reading). Record in
      `aee/freeze-aee-note.md`.
- [x] **L5 — Freeze-decision items.** DONE
      2026-10-21:
      OPEN-1…OPEN-4 decided on the record
      (`adjudication.md` §7 at the freeze):
      the S-1 frozen contract's form, the
      aggregate partition and disposition
      forms, the execution phase number
      (Phase-427 allocated, verified genuinely
      free — DD-065-13), and the OSF registration
      under E-1 (DD-065-15). DD-065-10…DD-065-15
      recorded; DD-065-1…DD-065-9 stand as
      drafted, none overturned.

## Execution (NOT authorised by this draft; every step OWNER-APPROVAL)

- [x] **E1 — Freeze + OSF.** DONE
      2026-10-21: This contract
      frozen (digest computed over the
      recovered register exactly once, at
      freeze; `freeze.md` / `freeze.json`),
      and this spec's own OSF contract
      registration filed under campaign
      decision E-1 (filing record
      `osf-spec-registration.md`). The
      registration stands pending approval;
      execution (E2–E5) awaits its approval
      act and a separate execution order.
- [x] **E2 — Graph-first build** (H15/H23) —
      script, graph node, registration,
      verification. **OWNER-APPROVAL** (as
      part of the execution order).
- [x] **E3 — Step 0** (spec §3) — input
      integrity, acquired-file assertion
      (S-5), S-1 intake determination, order.
      **OWNER-APPROVAL** (the execution
      order).
- [x] **E4 — Searches + accounting** (spec
      §§4–6) — the S-5 text-layer search; the
      S-1 search on the search arm only, else
      the frozen blocked outcome; exactly one
      outcome per source; recovered claims
      through normal intake at the created
      stage. **OWNER-APPROVAL** (the execution
      order).
- [x] **E5 — Outcome** (spec §§7–8) —
      headline class, disposition append,
      LEDGER entry; anchors asserted
      byte-identical; foundation check
      reported as measured. Spec 057's
      records untouched.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
