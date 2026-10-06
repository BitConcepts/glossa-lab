# Plan — Spec 008 / Phase-110

1. **Machinery first (H23).** Write
   `backend/scripts/phase110_m222_dossier.py` (evidence assembly,
   decide-only) and `backend/scripts/phase110_m222_apply.py`
   (applies the spec-008 disposition, writes the change register,
   regenerates bookkeeping). Create
   `backend/glossa_lab/experiment_graph_phase110.py` with nodes
   `IndusPhase110M222Dossier` / `IndusPhase110M222Apply`, register
   in `backend/glossa_lab/experiment_graph.py` (try/except block
   after the Phase-109 block), verify both IDs in `ATOMIC_NODES`
   — all before running either script.
2. **Dossier.** Run the dossier node/script; inspect the verdict
   predicates (all mechanical): every Cohort-A basis cites M222
   ('kur'); the Phase-111 run artifact's match distribution; the
   profile recomputation; M222's standing record. Write the MD
   summary from the dossier JSON.
3. **Apply.** Run the apply script (it re-derives the cohorts,
   asserts the register set equality, applies the branch
   disposition, regenerates bookkeeping, and self-verifies that
   the anchors diff equals the register). Inspect the diff.
4. **Part C.** README.md + CITATIONS.md pointer lines.
5. **Gates.** Foundation check (H21); full backend suite; ruff on
   the new Python files.
6. **Record.** Ledger entries (root + glossa-indus) with AI
   disclosure; tick tasks; commit per step; push; open PR
   (not merged).
