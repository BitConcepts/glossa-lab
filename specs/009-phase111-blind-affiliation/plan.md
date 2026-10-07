# Plan — Spec 009 / Phase-111

1. **Spec first (pre-registration).** Spec 009 written and committed
   ALONE, before any pipeline code output, panel statistic, or result
   exists. Ledger entries (root + glossa-indus) recording the freeze,
   with AI disclosure, ride in the same commit.
2. **Acquisition.** Inventory in-repo corpora; download only the
   openly-licensed sources named in spec §13 (DCS, ORACC, CDLI,
   Open Khipu Repository, Project Gutenberg) into the gitignored
   `glossa-corpus/indus/sources/phase111/`. Every corpus — obtained,
   in-repo, restricted-local, or gap — gets an entry in
   `reports/phase111_acquisition_log.json` (Phase-107 format) with
   source, license, token/text counts, unit and text rules as
   applied. Gaps (Elamite; SCA heraldry; any failed download) are
   logged before any run. No raw downloaded text is committed.
3. **Machinery (H23).** Create
   `backend/glossa_lab/experiment_graph_phase111.py` with nodes
   `IndusPhase111BlindGate` / `IndusPhase111BlindClassify`, register
   in `backend/glossa_lab/experiment_graph.py`, verify both IDs in
   `ATOMIC_NODES` — all before running the pipeline.
4. **Pipeline.** `phase111_custodian.py` (panel build, token remap,
   synthetics S1–S4, anonymized panel file + key in gitignored
   runtime state), `phase111_features.py` (the frozen 28-feature
   extractor of spec §4), `phase111_analyst.py` (LDA, gate,
   classification, verdict logic of spec §§6–10; imports nothing
   from the custodian), `phase111_run.py` (orchestrator).
5. **Unit tests** (`backend/tests/test_phase111_blind.py`):
   hand-computed feature values on toy corpora; blinding invariant
   (analyst artifacts contain no corpus names or source IDs);
   resampling exactness (exactly N tokens per draw; chunk-length
   distribution vs. target); gate logic on synthetic feature
   matrices (pass and fail branches); generator determinism; LDA
   determinism. Full suite must stay green (609 baseline + new).
6. **Gate run.** Orchestrator runs the gate on known corpora only.
   Gate failure → STOP: inconclusive results + summary written,
   ledgered, PR opened. No tuning, no Indus classification.
7. **Classification (only if the gate passes).** Final model trained
   on all known draws; anonymized targets + synthetics classified;
   control validity checked; unblinding logged; verdict computed
   strictly by spec §9 (V1–V6 vocabulary).
8. **Reports.** `reports/phase111_blind_affiliation_results.json` +
   `reports/phase111_blind_affiliation_summary.md` per spec §14.5.
9. **Gates before PR.** Foundation check (H21, 0 failures); full
   backend suite; ruff clean on new Python.
10. **Record.** Ledger entries (root + glossa-indus) with the gate
    outcome and the verdict verbatim; tasks ticked; branch pushed;
    ONE PR opened (spec + code + reports), NOT merged.
