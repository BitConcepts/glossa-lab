# Plan — Spec 014 / Phase-115

1. **Diagnosis (pre-freeze, corpus-level only).** Decompose the
   Phase-107 layer loss token-by-token against the canonical
   registry and crosswalk v2 (spec §1): the dominant loss is a
   leading-zero key mismatch (4,014 tokens), followed by the
   all-or-nothing inscription rule discarding legible signs
   around placeholders/unmapped codes. Other in-repo crosswalks
   checked; none extend Wells coverage deterministically.
2. **Spec first (pre-registration).** Spec 014 committed ALONE,
   before any battery-v2 code runs against any anchor and
   before any calibration statistic exists under it. It freezes:
   the v2 layer build policy (§2, with prototype-measured
   corpus-level stats as run-time assertions), T1 v2 with the
   opportunity-scaled floor (§4), T2/T3 verbatim from spec 011,
   the calibration gates (§5), the decision rule (§6).
3. **Layer build.** `phase115_build_layer_v2.py` implements §2;
   the built layer's stats are asserted against §2; byte-
   identical reproducibility is verified by building twice and
   comparing hashes. Layer + meta stay gitignored; the v1
   layer is untouched.
4. **Machinery (pure, deterministic).** `phase115_battery.py`:
   T1 v2 (opportunity, floor, stability guard) on top of the
   spec-011 machinery (`phase113_battery`: profiles, modal
   class, TV, canon syllabifier, T2, T3, decision rule) — reused,
   not reimplemented, so T2/T3 cannot drift from the frozen
   originals. No SA artifact is imported or read.
5. **Unit tests.** `test_phase115_battery.py`: floor-band
   boundaries, opportunity arithmetic, T1 v2 state machine
   (NOT_ATTESTED paths incl. `sign_absent_holdat` and
   `below_stability_floor`; FAIL requires ≥ 3 tokens; PASS at
   scaled floor), sentinel-position profile geometry on toy
   corpora, layer-builder policy on a toy CSV (normalization,
   placeholders, partial retention, both dedupe rules), and the
   H23 registration assertion.
6. **H23 gate.** Graph module `experiment_graph_phase115.py`
   (node `IndusPhase115NonSaValidation`), registration in
   `experiment_graph.py`, ATOMIC_NODES assertion — all before
   the runner executes.
7. **Calibration.** Runner executes §5: battery v2 over
   STRICT94 (leave-one-out) and KUR113. Gates: strict VALIDATED
   ≥ 57/94; kur VALIDATED ≤ 5/113. Failure → battery rejected;
   reports + ledgers written; phase stops with the anchors
   file untouched and FLAGGED44 never run.
8. **Main run (only if calibration passes).** Battery v2 over
   FLAGGED44; §6 applied mechanically; anchors updated;
   change register (one record per flagged anchor, including
   UNRESOLVED non-actions); bookkeeping regenerated and
   asserted against the register (Phase-113 pattern).
9. **Verification.** Full backend suite (baseline 673 passed /
   11 skipped) and `foundation_check.py` (H21; baseline
   40 / 0 / 8) in the worktree venv; ruff over all new/changed
   Python before push.
10. **Record + PR.** Results JSON + summary MD (diagnosis and
    layer coverage first, calibration outcomes verbatim,
    per-anchor tallies if the main run executes, final tier
    counts / coverage if changed); ledger entries in both
    ledgers with AI disclosure; one PR from
    `phase/nonsa44-validation-v2`. No merge — the owner merges
    science PRs on explicit say-so.
