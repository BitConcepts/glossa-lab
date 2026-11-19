# Spec 095 — T503 closeout record (2026-11-19)

**Stage.** The Spec 095 closeout, run 2026-11-19 on the owner's
order of that day, immediately after the dedicated T404
remediation stage passed the audit package's pre-fixed
thresholds on re-run (PR #595). T503's text: "The register
re-checked against C095-1 (no duplicate worked twice, no NEW
item lost); every claim discharged or carried as a named
remainder; the closeout record filed in this directory."

## 1. The register re-checked against C095-1

The reconciliation register of 2026-11-15 (43 rows, RT-01..RT-43)
was re-read in full for this closeout, against the stage records
of Stages 0–5, the T403 build record, and the T404 remediation
stage record.

- **Dispositions intact.** 23 DUPLICATE-OF-RECORD rows, 18 rows
  carrying the 14 NEW items of section N, 2 FACT-DISPUTED rows
  (RT-42, RT-43; the record governs both): 23 + 18 + 2 = 43.
  Every row carries exactly one disposition and names its owning
  vehicle or its section-N item. C095-1's falsifier does not
  fire.
- **No duplicate worked twice.** No Spec 095 stage task worked a
  duplicate row's item: the stages worked the NEW items and this
  spec's governance claims only. RT-06, the register's one
  security risk requiring verification, stayed under its Spec
  083 vehicle throughout and was not touched by any stage of
  this spec.
- **No NEW item lost.** Each of section N's 14 items maps to
  exactly one owning claim and one discharging stage (item 8,
  the platform commission, spans two claims by its own terms —
  the multi-script specification and the dashboard — and is
  counted once, as the register counts it):

| §N item | Claim | Discharged by |
| --- | --- | --- |
| 1. RT-03 micro-task (README banner) | inside C095-1's register | **carried** — §3, remainder 4 |
| 2. RT-04 synthetic census + pinning | C095-6 | Stage 2 |
| 3. RT-10 twelve-case battery | C095-4 | Stage 1 |
| 4. RT-14 contamination detection | C095-7 | Stage 3 |
| 5. RT-16 validator census + guards | C095-5 | Stage 2 |
| 6. RT-17/RT-32 standards | C095-8 | Stage 3 |
| 7. RT-19+RT-20 audit package | C095-13 | Stage 4 run; remediation stage re-run (PASS) |
| 8. RT-23/RT-24/RT-26 platform | C095-11, C095-12 | Stage 4; T403 build (2026-11-18) |
| 9. RT-27 orientation as data | C095-10 | Stage 3 |
| 10. RT-31 identifiability protocol | C095-9 | Stage 3 (ledger remainder — §3, remainder 3) |
| 11. RT-34 Eteocypriot | C095-15 | Stage 5 scoping |
| 12. RT-35 Meroitic benchmark | C095-16 | Stage 5 scoping |
| 13. RT-38 composed release gate | C095-14 | Stage 4 |
| 14. RT-39 derived documents | C095-17 | Stage 4 |

The two scopings were re-checked as T503 directs: T501's target
is NEW item 11 and T502's is NEW item 12; neither scoping worked
any other item, and neither produced analysis or benchmark
output under this spec (their claims' falsifiers checked at
Stage 5 and again here: neither fires).

## 2. Every claim, discharged or carried

- **C095-1** (register as scope of record) — discharged at
  adoption (Stage 0 complete at adoption, D-095-2); re-checked
  at this closeout, §1 above.
- **C095-2** (pinnability, locate-first) — discharged, Stage 1
  (T101–T103; the re-execution's outcome is filed as its own
  record and stands as that record states).
- **C095-3** (corpus identity standard) — discharged, Stage 1
  (T104; governance claim).
- **C095-4** (twelve-case battery) — discharged, Stage 1 (T105).
- **C095-5** (v1 validators guarded) — discharged, Stage 2
  (T201–T203).
- **C095-6** (synthetic containment) — discharged, Stage 2
  (T204).
- **C095-7** (contamination gate class) — discharged, Stage 3
  (T301).
- **C095-8** (equivalence and reporting standards) — discharged,
  Stage 3 (T302).
- **C095-9** (identifiability protocol) — discharged, Stage 3
  (T303), **with remainder 3 carried** (§3): the protocol ran
  and the six anchors' standings were re-stated in the
  application record; the ledger re-statement was not applied,
  because no vehicle exists that can carry anchor standings as
  acts.
- **C095-10** (orientation as data) — discharged, Stage 3
  (T304).
- **C095-11** (multi-script specification) — discharged,
  Stage 4 (T401/T402).
- **C095-12** (dashboard) — discharged in two halves as its
  records state: at wireframes, Stage 4; the build half by the
  T403 build (PR #589, merged 2026-11-18), Playwright-verified
  at desktop and mobile widths.
- **C095-13** (audit package) — discharged by the T404
  remediation stage (PR #595, merged 2026-11-19): the re-run
  passes every pre-fixed threshold, raw and corrected
  (functional 15/15 corrected; protocol 6/8 corrected on the
  legacy leg with the dashboard leg 8/8; zero axe critical and
  zero serious on both legs). **Remainder 2 carried** (§3): the
  authenticated legs.
- **C095-14** (composed release gate) — discharged, Stage 4
  (T405). Its public-claims component's standing failure is
  remainder 4's, and is recorded as such wherever the gate's
  results are stated.
- **C095-15** (Eteocypriot scoping) — discharged, Stage 5
  (T501). Execution is a separate owner decision, outside this
  spec.
- **C095-16** (Meroitic scoping) — discharged, Stage 5 (T502).
  Execution is a separately commissioned study, outside this
  spec.
- **C095-17** (derived documents) — discharged, Stage 4 (T406;
  governance claim).

All seventeen claims are discharged. Four remainders carry, by
name, in §3. No claim is left open and unnamed.

## 3. The named remainders

1. **C095-12, build half** — named in the Stage 5 scoping
   record as an open remainder; **resolved before this
   closeout** by the T403 build (PR #589) and recorded here as
   discharged, not carried. It is listed so the closeout's
   accounting against the scoping record's §4 is complete.
2. **The C095-13 authenticated legs.** The audit package ran on
   the Spec 083 acceptance vehicle as a scratch instance with
   authentication off — the scope the thresholds record fixed
   before the original run. The authenticated cloud legs remain
   with the standing Spec 083 proofs remainder, for the owner's
   sessions. Nothing in C095-13's discharge rests on them.
3. **The T303 ledger re-statement.** The six anchors' standings
   under the identifiability protocol stand as re-stated in
   `records/t303-identifiability-application-2026-11-16.md`
   (filed, not applied): no vehicle exists that can carry
   anchor standings into the ledger as acts. Carried by name to
   whichever future stage builds that vehicle; the application
   record is the governing statement until then.
4. **The RT-03 README supersession banner.** The anchor-model
   README still foregrounds the superseded figures the Stage 0
   public-surfaces pass confirmed (the "161 H+M signs" family).
   The banner is an owner-gated micro-task (D-095-5), outside
   this spec's stages; it was not done by this closeout and is
   flagged here for the owner's hand. It remains the standing
   failure of the composed release gate's public-claims
   component (C095-14), exactly as the Stage 4 record states.

## 4. Spec state at closeout

Every task in `tasks.md` is ticked: Stages 0–4, the T403 build,
the T404 remediation and re-run, and Stage 5's two scopings.
T503's own box is ticked by this record's commit. Spec 095 is
complete, subject to the four remainders above — two carried
open (remainders 3 and 4), one carried to another spec's
standing remainder (remainder 2), and one resolved and recorded
(remainder 1).

Nothing in this closeout commissions the Eteocypriot execution,
the Meroitic benchmark execution, or any second-target work;
both remain separate owner decisions, as their claims state.
