# Spec 040 — AEE note (draft)

The AEE lifecycle hooks (after_specify /
after_plan / after_tasks) have **not run** on
this draft's claim register (F040-C01…C15),
deliberately: the hooks are a **freeze gate**,
not a drafting step (tasks L4). Any recovery
round at the freeze act changes claim text, so
the freeze digest is computed over the
recovered register exactly once, at freeze —
the ordering Spec 035 established and Specs
036/037 carried. At this draft the register
carries only the draft-stage self-checks
pinned by `backend/tests/test_spec040_freeze.py`
(dependency integrity; the definition
constants; the cited-record facts: the
Phase-140 and Phase-385 quantities, the spine
and covariate pins, and the Spec 025 rider).

The freeze act for this spec has a second gate
in front of the hooks (tasks L5): spec §1's
dependency gate on the executed Spec 039
record. The hooks run only when that gate is
satisfied; a hook pass over a register whose
dependency has failed would freeze a contract
that cannot execute.

At the freeze act, the hook outputs and any
recovery rounds are recorded in this directory
(`aee/`), and this note is completed by append
with their record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
