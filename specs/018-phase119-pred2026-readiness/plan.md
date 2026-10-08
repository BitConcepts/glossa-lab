# Plan — Spec 018 / Phase-119 PRED-2026 Readiness Harness

Build phase (owner-authorized 2026-10-07, design + build in
one authorization; **no evaluation of any real prediction is
authorized or possible** — spec §10). The product is a
machine: when a qualifying independent dataset lands, the
evaluation of PRED-2026-001–003 is a procedure, not a
negotiation.

## Approach

1. **Register first.** The three registered criteria were
   located verbatim in `docs/PREDICTION_REGISTER.md` §2 and
   are quoted in spec §1. Everything downstream implements
   those texts; operationalizations are frozen and disclosed
   (spec A4, §6.3), never smuggled.
2. **Measure before freezing.** Design-stage statistics on
   the current expanded ICIT layer fixed the design choices:
   the §5 dedup stages (A.1: cumulative 45.51% removal —
   the short-inscription duplicate residue the layer builder
   exempted is real and large); the §3 canonical map (A.4:
   the sparse crosswalk-v2 map collapses coverage and is
   rejected with numbers); the §3 class floor (A.3: freq ≥ 10
   is the unique floor reproducing the register's 14/12).
   These numbers are the spec's Appendix A, committed with
   the freeze; the built harness must reproduce A.1/A.2
   through its own code path.
3. **Gate in code, not in vigilance.** Independence gating
   (§4/§6.1), the verdict lock (§6.5), and the dry-run
   prohibition on criterion statistics (§8) are properties
   of the code path, each pinned by a unit test.
4. **H23 order.** Script → graph module → registration →
   assertion → run. The dry run happens only after the node
   `IndusPhase119PredHarness` is asserted in `ATOMIC_NODES`.
5. **Fixtures are synthetic.** No real awaited source
   exists; each adapter is built against a hand-verifiable
   toy input in its documented schema, and the scoring path
   is proven end-to-end on a toy prediction over a toy
   independent fixture (both verdict directions).

## Verification

- Unit tests (`backend/tests/test_phase119_pred_harness.py`)
  per spec §9.5.
- Dry run reproduces Appendix A.1/A.2 numbers exactly.
- Full backend suite (main baseline measured at phase start)
  + foundation check (H21) + ruff.
- Ledgers both files (H1); one PR; no merge (owner's
  say-so).
