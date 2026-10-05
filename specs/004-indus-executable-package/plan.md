# Plan 004 — Indus executable package

## Branch / commits

Branch `feat/indus-executable-package` from main (d9613595). One commit
per workstream, plus this proposal commit and a closing
verification/ledger commit. PR to main via `gh pr create`; NOT merged
(owner review; PR #58 also still open).

## WS1 — Phase-52 run

1. Confirm `IndusConstrainedSA` registration in
   `glossa_lab.experiment_graph.ATOMIC_NODES` (H23 step 4 pattern; the
   node and its script `backend/scripts/phase52_syllabic_sa.py` already
   exist — no new node is created).
2. Execute the node's function through the experiment-graph machinery
   (the node subprocess-runs the phase script and parses its report).
   Timeout-bounded (H9/H11): the SA is 5 seeds × 10 restarts × 30k
   iterations of a ~100µs NumPy score → allow 30 min hard timeout.
3. Verify `reports/phase52_syllabic_sa.json` +
   `reports/phase52_full_decipherment_table.json` exist; re-run
   `backend/scripts/foundation_check.py` and confirm CHECK NEW-F passes
   (z ≥ 4) and the warning is gone.
4. Ledger the execution as Phase-106 in `glossa-indus/LEDGER.md` with the
   actual findings.

## WS2 — Crosswalk expansion

1. Audit script (scratch, not committed): load v2 crosswalk; classify
   each entry's evidence basis from its `source` field and provenance
   (Phase-28 v1 curated / literature synthesis / Phase-96 identity table).
2. Mine in-repo equivalence sources not yet fully reflected in v2:
   - `outputs/phase51_parpola_crosswalk.json` (parpola_to_m_crosswalk)
   - `outputs/phase56_parpola_expansion.json` (master_crosswalk)
   - `backend/scripts/phase65_crosswalk_top100.py` SUPPLEMENTARY_MAP
   - `backend/scripts/phase71_crosswalk_complete.py` EXTENDED_MAP
     (entries carrying a named source + iconographic note)
   - `backend/glossa_lab/data/mahadevan_parpola_crosswalk.json` (v1:
     iconic descriptions, allograph families, Wells IDs)
   - `backend/glossa_lab/data/iconographic_anchors.json`
   - `outputs/phase220_parpola_cisi_crossref.json`
   - Yajnadevam bridge if a Y→M table exists in-repo
     (`data/crosswalks/yajnadevam_to_parpola_crosswalk_extended.csv` is
     Y→P; requires a Y→M counterpart to bridge).
   Considered and rejected as evidence: Holdat↔CISI inscription
   alignment — the two corpora share no inscription IDs (Holdat
   `H-0001`/`M-0001` style vs CISI JSON `M-1A` style), so positional
   equivalence is not demonstrable.
3. Build additions: for each sourced M↔P pair not already in v2, add an
   entry in v2 format plus an `evidence` field naming the in-repo source
   (and its stated published source where given). Identity-only pairs
   encountered are written to
   `backend/glossa_lab/data/mahadevan_parpola_crosswalk_candidates.json`
   with `basis: number_identity_inference` — never into the mapping.
4. Regenerate v2 `stats` from actual contents; bump `version` note.
5. Cross-check the 5 Phase-104 blocked claims (from spec 003 /
   `reports/phase104_claims_evaluation.json`): which cite signs whose
   numbering becomes resolvable via the expanded crosswalk. Report only.
6. Sanity: `indus_sign_crosswalk.py` still loads; API foundation check
   §10 count reflects the new total.

## WS3 — Anchors reconciliation

1. Snapshot sha256 of the canonical JSON of `anchors` mapping.
2. Regenerate: `total` (entry count), `by_confidence` (count per
   confidence value present), `n_high`, `total_all_entries`, and
   `metadata` counts (total_count / high_count / medium_count /
   low_count) — plus a `metadata.counts_note` defining each quantity and
   the Phase-170 "161" subset definition.
3. Re-hash the `anchors` mapping; must be byte-identical canonical form.
4. Run `backend/scripts/foundation_check.py`; anchors checks pass.

## WS4 — Discovery triage

1. Read `glossa_lab/discovery/` and the research-loop/discovery API
   processing code to use the pipeline's own status vocabulary and
   disposition mechanisms.
2. Restart the local backend from this branch if needed; pull the queue
   via `GET /api/v1/discovery/items?status=new` (expect 78).
3. Disposition each item via the API (status update endpoint / pipeline
   triage path): kept/relevant, dismissed with the pipeline's reason
   categories, or flagged for review — per each item's content.
4. Report counts by topic × disposition; list unprocessable items with
   reasons.

## Verification

- Full backend pytest suite in `~/workspace/venvs/glossa-lab`: exact
  pass/skip/fail counts recorded.
- `backend/scripts/foundation_check.py`: full run recorded (expect
  Phase-52 warning gone; anchors checks green).
- `ruff check` on changed Python files (expected: data files + this
  spec only; any script written for WS1/WS2 execution is scratch unless
  it becomes a maintained artifact — if committed, it is ruffed).
- Root `LEDGER.md` summary entry + `glossa-indus/LEDGER.md` phase
  entries, AI disclosure in each (H1, constitution §II/§VI).
