# C1 — the kill-test battery

Four fixed defective designs. The current evaluator is run over
them (at every evaluator release and at every freeze, via
`../run_battery.py`), and any case it passes without a finding
that addresses the defect is recorded as a **named blind spot**
— never smoothed over. The determination is strict on purpose:
hygiene-class findings (independence modelling, boundary form)
fire on sound registers too, so they never count as catches;
only a finding whose name addresses the case's defect does. The
exact criteria live in `cases.json` beside each case's
`DEFECT.md`, which states the defect in plain words.

| Case | The defect | Source |
|---|---|---|
| (i) | A real design whose instrument could not discriminate its target property — found by the programme only in execution | `case-i-spec026-era/` — Spec 012 / Phase-114, byte-identical to `specs/012-phase113-blind-affiliation/spec.md` on main |
| (ii) | A headline claim whose falsifier is present in form and empty in substance | `case-ii-unfalsifiable/` — planted |
| (iii) | A pinned total of 52 against a cited source summing to 47 | `case-iii-wrong-pin/` — planted |
| (iv) | Claims stating the opposite of the real records they cite | `case-iv-unsupported-citation/` — planted |

Results: `results/battery-result.md` (human) and
`results/battery-result.json` (machine; the file C4 reads),
with raw evaluator outputs under `results/raw/`.

**This battery does not establish** that the evaluator catches
any class of defect beyond these four, and — as the current
results show — it does not establish that it catches these.
