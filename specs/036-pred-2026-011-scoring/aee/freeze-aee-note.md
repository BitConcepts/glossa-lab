# Spec 036 — AEE note

> ## DRAFT — HOOKS NOT RUN — 2026-10-20
>
> The AEE lifecycle hooks (after_specify /
> after_plan / after_tasks) have **not** run on
> this draft register (0.5-draft). That is a
> deliberate ordering, not an omission: the hook
> pass is a **freeze gate** (the Spec 035
> record). Any recovery round at after_specify
> changes claim text, and the freeze digest must
> be computed over the recovered register exactly
> once, at the freeze act — so no hook output
> exists for this draft, and none is claimed.

## At the freeze act

1. Run the hooks over the register in lifecycle
   order (after_specify, after_plan, after_tasks)
   with the Glossa venv's AEE package first on
   PATH (pinned `>=1.0.4,<1.5` per PR #181).
2. The gate is **pass**: a stricter outcome
   blocks the freeze until its named recovery is
   complete. Recovery rounds — however many the
   register needs — are recorded here by append,
   with their artifacts, and advance the register
   version (the Spec 035 record: 30, then 9, then
   8, then 0 failure modes at after_specify, over
   register versions 0.6-draft → 0.8-draft).
3. Only after the gate passes is `freeze.json`
   recomputed, once, over the recovered register
   and the finalised freeze texts, and
   `freeze.md` finalised.

## Draft-stage self-checks (not hook output)

In place of hook output, this draft carries the
mechanical self-checks the house draft pattern
pins in tests (`backend/tests/test_spec036_freeze.py`):
the draft freeze record replays exactly
(framework026 `verify_freeze` over every covered
source), the definition carries the registered
criterion, trained set, screen, step-0 closures,
and unmappable cap as registered, the claim
register is integrity-clean (dependency
integrity: no cycles, no missing dependencies,
no forbidden-assumption inheritance), and the
cited records still carry the facts the design
rests on. These checks score nothing, open no
withheld content, and compute no start rate.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
