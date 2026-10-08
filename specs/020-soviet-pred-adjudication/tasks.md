# Tasks — Spec 020 / Soviet Dataset Adjudication for PRED-2026-001/002

## Adjudication (owner-authorized 2026-10-08)

- [x] T1 Source texts read in full: `docs/PREDICTION_REGISTER.md` §2 (PRED-2026-001/002 verbatim), spec 018 §§3–6 (sign sets, six source classes + frozen evaluability matrix, dedup protocol, scoring/gating rules), Phase-121 dataset (`data/soviet_positional/` CSVs + JSON) and memo (`reports/phase121_soviet_positional_dataset.md`).
- [x] T2 Criteria derived mechanically from the registered texts and stated before application (spec §2: C1 class/matrix, C2 identity/substitute, C3 per-sign rate computability, C4 dedup applicability, C5 sign-space/ingestibility, C6 independence), each citing its source text.
- [x] T3 Established facts of the dataset recorded (spec §3: aggregate published tables; no inscription-level records; T4 a restricted Marshall-numbered pair × final co-occurrence matrix; no Marshall↔P map).
- [x] T4 Criteria applied one by one (spec §4): C1 FAIL, C2 FAIL, C3 FAIL, C4 FAIL, C5 FAIL, C6 PASS (narrow, lineage only).
- [x] T5 Verdict recorded (spec §5): **NO** — the dataset does not qualify for PRED-2026-001/002; predictions remain PENDING.
- [x] T6 Append-only adjudication note added to `docs/PREDICTION_REGISTER.md` (registered entries unmodified; Tested/Outcome remain PENDING).
- [x] T7 Full backend suite + foundation check (H21): 867 passed / 12 skipped / 0 failed (baseline 867/12); foundation check 40 passed / 0 failed / 8 warnings; anchors sha256 asserted unchanged; branding sweep over changed files clean.
- [ ] T8 Ledger entries (both files; AI disclosure) and one PR; merge only when complete + CI green (standing auto-merge rule); post-merge verification on main (suite counts, anchors hash). (Ledger entries written with this task list; PR/merge/post-merge verification complete the item.)

## Conditional scoring branch (executes ONLY on a YES verdict)

- [ ] S1 Ingest via `backend/glossa_lab/pred_harness.py` under the adjudicated source class, with §5 dedup and §6 scoring per spec 018. — **Not executed: verdict is NO.**
- [ ] S2 Record PRED-2026-001/002 verdicts in the register append-only, with tested date, outcome, and caveat C1 verbatim where required. — **Not executed: verdict is NO; no PRED verdict exists to record.**

## Explicitly not tasks of this spec

- Running the harness scorers in evaluation mode — or a labelled dry run — on the adjudicated non-qualifying dataset.
- Inventing a new source class, amending spec 018's frozen evaluability matrix, creating a Marshall→P sign map, or re-registering either prediction.
- Any anchor, claim, registry, or language-model change; any change to PRED-2026-003 or PRED-2026-004–009.
