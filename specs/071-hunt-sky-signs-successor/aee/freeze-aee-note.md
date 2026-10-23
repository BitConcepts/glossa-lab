# Spec 071 — AEE freeze-gate note (2026-10-22)

The claims register (`../claims.json`) was assessed
with the AEE lifecycle hooks (run_aee.py, AEE CLI
v1.5.3) at after_specify, after_plan and after_tasks,
under the gate reading of DD-071-7 / DD-038-10 /
DD-071-14: zero correctness failure modes and no
claim below 0.70 propagated confidence.

## Loadability recovery (register 0.5-draft → 0.6)

The draft register did not load: its evidence kinds
(`design-source`, `program-record`) and the
`authoritative` source quality are not values the
installed evaluator accepts. Under the same standing
convention the earlier freezes in this programme
recovered by (recorded at Specs 069's and 070's
freezes), the evidence was restated in the
evaluator's vocabulary — kind `observed`, source
quality `artifact` where the draft carried
`program-record` or `authoritative` — and each
evidence item gained an `independent_of` list naming
the register's other sources for its claim. The
cited records themselves are unchanged.

## Freeze recovery rounds (0.6 → 0.9)

- **Round 1 (0.7):** each claim head was restated as
  a single atomic proposition; the drafted substance
  moved into the claim's boundary verbatim in
  substance, and the freeze rulings were carried
  into the boundaries of F071-C08 (Asset A digest
  and freeze order, DD-071-9) and F071-C07 (keying
  route and unkeyable-sign disposition, DD-071-10 /
  DD-071-11). Six failure modes remained: two
  negation-conflict challenges against F071-C13's
  negative head, and irreducibility challenges on
  F071-C04, C08, C11 and C13.
- **Round 2 (0.8, carried into the frozen 0.9
  register unchanged in substance):** the heads of
  F071-C04, C08 and C11 were shortened to single
  propositions, and F071-C13's head was restated in
  positive form ("Depiction under Spec 071 is the
  published identification layer"), the superseded
  heads recorded in their boundaries. **Zero
  failure modes at all three hooks; minimum
  propagated confidence 0.845.**

The frozen register is version `0.9-frozen-candidate`
in the file; the freeze digest in `../freeze.md` /
`../freeze.json` is computed over it. Final
assessment artifacts: `after_specify.json`-series
files in this directory (assessment timestamps
20261023T001133Z, 20261023T001134Z, 20261023T001134Z).

*AI disclosure: prepared by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
