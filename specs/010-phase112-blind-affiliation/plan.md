# Plan — Spec 010 / Phase-112

1. **Design stage (pre-freeze, known corpora only).** Candidate
   order-carrying features implemented in `phase112_features.py`
   (17 spec-009 definitions recomputed identically + 6 new);
   mechanical toy-corpus permutation-sensitivity tests; the
   permutation-sensitivity audit
   (`backend/scripts/phase112_feature_audit.py`) run on the nine
   known panel corpora only — no Indus corpus, no synthetic
   control, no classification is touched at this stage. Audit
   output: `reports/phase112_feature_audit.json`. Candidates
   failing the frozen admission rule are dropped, and the drops
   are recorded in spec §4.
2. **Spec first (pre-registration).** Spec 010 written and
   committed ALONE (with the ledger freeze entries), after the
   audit and before any panel build, gate evaluation, or Indus
   statistic exists. Git order is the pre-registration proof.
3. **Acquisition.** No new downloads. The Phase-111 panel sources
   are staged as local copies in the gitignored
   `glossa-corpus/indus/sources/phase112/` (identical files,
   identical licenses; see `reports/phase112_acquisition_log.json`).
   Gaps inherited from spec 009 + its Addendum A stand (K6
   Akkadian, N2 proto-cuneiform, Elamite, attested SCA heraldry).
4. **Machinery (H23).** Create
   `backend/glossa_lab/experiment_graph_phase112.py` with nodes
   `IndusPhase112BlindGate` / `IndusPhase112BlindClassify`,
   register in `backend/glossa_lab/experiment_graph.py`, verify
   both IDs in `ATOMIC_NODES` — all before running the pipeline.
5. **Pipeline.** `phase112_custodian.py` (panel build reusing the
   frozen spec-009 loaders/chunking/resampling by import;
   synthetics S1–S5; anonymized panel file + key in gitignored
   runtime state `.glossa-state/phase112/`),
   `phase112_features.py` restricted to the admitted set frozen in
   spec §4 (definitions unchanged), `phase112_analyst.py` (LDA,
   gate, control validity over S1–S5, verdict logic of spec
   §§6–10; imports nothing from any custodian),
   `phase112_run.py` (orchestrator).
6. **Unit tests** (`backend/tests/test_phase112_blind.py`):
   design-stage permutation-sensitivity (already in place);
   hand-computed feature values; blinding invariant; resampling
   exactness; gate logic pass/fail branches; generator determinism
   incl. S5's positional-bigram definition; LDA determinism.
   Full suite must stay green (626 passed / 10 skipped baseline
   after Phase-111, plus new tests).
7. **Gate run.** Orchestrator runs the gate on known corpora only.
   Gate failure → STOP: inconclusive results + summary written,
   ledgered, PR opened. No tuning, no Indus classification.
8. **Classification (only if the gate passes).** Final model
   trained on all known draws + the two disclosed generator
   classes (gen_heraldic, gen_administrative — S5 has NO trained
   class); anonymized targets + synthetics S1–S5 classified;
   control validity (§8) checked over all five controls;
   unblinding logged; verdict computed strictly by spec §9
   (V1–V6 vocabulary).
9. **Close-out.** Results JSON + summary; ledger outcome entries;
   foundation check; ruff check on all new Python; ONE PR, not
   merged (owner merges on explicit say-so).
