# Spec 037 — AEE note (draft)

The AEE lifecycle hooks (after_specify /
after_plan / after_tasks) have **not run** on
this draft's claim register (F037-C01…C15),
deliberately: the hooks are a **freeze gate**,
not a drafting step (tasks L3). Any recovery
round at the freeze act changes claim text, so
the freeze digest is computed over the
recovered register exactly once, at freeze —
the ordering Spec 035 established and Spec 036
carried. At this draft the register carries
only the draft-stage self-checks pinned by
`backend/tests/test_spec037_freeze.py`
(dependency integrity; the definition
constants; the cited-record facts: the
corpus_master pin, the Spec 031 fence figures,
and the design constants in `freeze.json`).

At the freeze act, the hook outputs and any
recovery rounds are recorded in this directory
(`aee/`), and this note is completed by append
with their record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
