# Spec 038 — Freeze Record (PRED-2026-007: full-population ITM census and scoring, D-31)

> ## FROZEN at the Spec 038 freeze merge (2026-10-20)
>
> Basis: the owner's freeze-and-execute order of
> 2026-10-20, verbatim **"Freeze D-31 for
> execution"** (`adjudication.md` §6), which
> freezes this contract and orders Phase-401
> execution in the same act. The governed claim
> register passed the AEE lifecycle gate at
> after_specify, after_plan, and after_tasks
> under **aee 1.5.0** (DD-038-7), after three
> recorded rounds at after_specify (24, then 20,
> then 14 failure modes — the final 14 all
> FR-2.3 draft-cap records; 0 correctness
> failure modes and 0 claims below the 0.70
> threshold from round 2 on;
> `aee/recovery-specify.md`; the gate reading
> under aee 1.5.0 is recorded as DD-038-10) —
> the freeze digest recorded in `freeze.json`
> (framework026 digest, built by
> `build_freeze.py` from the DEFINITION and
> SOURCES it carries) covers the recovered
> register (0.7-draft), never the pre-recovery
> draft.

## 1. Basis

The contract implemented is design **D-31**
(PR #195 portfolio) for the PRED-2026-007
registration of 2026-04-22
(`docs/PREDICTION_REGISTER.md`): enumerate the
full ITM population, then score the registered
criterion over it, reading only the recorded
CGSA Phase 5 output.

Three design-integrity flags from the freeze
coordinator's Stage-0 preparation are disposed
of in `adjudication.md` §3 and are part of this
basis: the verdict rule is mechanical and **no
outcome is pre-written for any branch**
(DD-038-1 — the register's recorded 67% is a
pre-execution figure whose denominator mixed in
a non-ITM sign); the cluster-class rule is a
disclosed operationalisation, a deterministic
lookup in a named record (DD-038-9); and the
function-code sources are named — primary,
cross-check, conflict rule — before any
enumeration (DD-038-5).

The freeze also decides the open design
proposal: **DD-038-6 is decided YES** — this
frozen spec files its own OSF contract
registration, following the Spec 032–036 house
pattern (PRED-2026-007 itself has no
preregistration of its own,
`osf-registration.md`). The phase number is
confirmed at the same act (DD-038-8):
**Phase-401 is allocated to Spec 038** on the
merged record (`adjudication.md` §6).

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/038-pred-2026-007-full-population/freeze.md` (this
  document)
- `specs/038-pred-2026-007-full-population/spec.md`
- `specs/038-pred-2026-007-full-population/claims.json`
- `specs/038-pred-2026-007-full-population/adjudication.md`
- `specs/038-pred-2026-007-full-population/osf-registration.md`
- `specs/038-pred-2026-007-full-population/aee/freeze-aee-note.md`
- `specs/038-pred-2026-007-full-population/build_freeze.py`
- `backend/tests/test_spec038_freeze.py`

`plan.md`, `tasks.md`, and `outcome.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds).

## 3. What the freeze fixes

- **The criterion** (spec §6 / F038-C02): at
  least 70% of ITM-coded signs are TERMINAL or
  cluster in TERMINAL clusters, carried
  verbatim; CONFIRMED / NOT CONFIRMED are the
  only verdicts; the verdict rule is mechanical
  and no band is added.
- **The population frame** (spec §2 /
  F038-C03): every distinct sign the named
  primary source codes exactly ITM; the
  cross-check and conflict rule fixed before
  enumeration (DD-038-5); P098 (LOG) excluded
  by rule.
- **Step 0, fail-closed, in a fixed order**
  (spec §3): sources and provenance;
  enumeration with completeness checks, written
  and hashed before any Phase 5 lookup; Phase 5
  output verification. The census branch
  completes rather than closes (§6).
- **The scoring inputs** (spec §5 / F038-C06):
  the recorded Phase 5 output only, cluster
  classes per DD-038-9; no re-clustering.
- **The coverage rule** (spec §6 / F038-C07):
  the design's rule, fixed in advance.
- **Register handling at execution** (spec
  §7): dated appends only — the outcome entry
  and the provenance reconciliation note; the
  registered §3 text is never edited; every
  other prediction stays byte-identical.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
