# Spec 004 — Indus executable package (Phase-52 SA run, crosswalk expansion, anchors reconciliation, discovery triage)

**Status:** Proposed 2026-10-05 on `feat/indus-executable-package` (from main
d9613595). Owner-approved package of four executable workstreams from the
2026-10-05 program audit, run while PR #58's CI is blocked by a GitHub
Actions outage (that branch is not touched here).

## Context (audit findings, 2026-10-05)

- H+M anchors cover 96.5% of the 7,002 Holdat tokens; the remaining tail is
  247 tokens over 116 signs, all rare (max frequency 4). The program is
  corpus-bound; pooling CISI (Parpola P-numbers) with Holdat (Mahadevan
  M-numbers) is gated on the M↔P crosswalk.
- Foundation check: 39 passed, 0 failed, 9 warnings. Two warnings are
  actionable in-repo: the Phase-52 result file is missing, and the
  crosswalk warnings cite a stale "45/390" figure.
- `backend/reports/INDUS_FINAL_ANCHORS.json` bookkeeping fields disagree
  with its own entries (by_confidence sums to 413 vs 287 entries;
  metadata.total_count 172; total_all_entries 397).
- The discovery queue holds 78 items in status "new" (GDELT ngrams feed
  dark; no new fetching in this package).

## Workstreams

### WS1 — Phase-52 syllabic SA run (ledgered as Phase-106 execution)

Run the existing `IndusConstrainedSA` experiment-graph node
(`experiment_graph_phase48_55.py`, registered) through the established
machinery so `reports/phase52_syllabic_sa.json` exists at the path
`backend/scripts/foundation_check.py` CHECK NEW-F reads, and report the
SA's actual z-score / coverage findings honestly. The Phase-52 experiment
itself was designed in its own era; this package executes the missing run
and ledgers the execution as Phase-106 (next free phase number; phases
reached 105 in spec 003) rather than renumbering history.

### WS2 — M↔P crosswalk expansion (evidence-only additions)

Audit `backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json`
(179 raw entries) and expand it using only in-repo evidence:

- A mapping is added only when an in-repo source demonstrably states the
  equivalence (explicit cross-reference table or matching iconographic
  description/name on both sides). Every added entry records its evidence
  source.
- Number-identity alone (P_nnn = M_nnn by numeral, Phase-96 style) is
  inference, not evidence: such pairs go to a new candidates file
  (`mahadevan_parpola_crosswalk_candidates.json`), never into the mapping.
- Regenerate the file's stale `stats` block truthfully from its contents.
- Report which of the 5 Phase-104 claims blocked on "unstated numbering
  system" become addressable (addressability only; no re-adjudication).
- Foundation-check note: the API foundation check
  (`api/foundation_check.py` §10) derives its crosswalk count from the
  file, so it reflects the expansion automatically. The standalone
  script's crosswalk WARN strings are hardcoded historical snapshots and
  do not derive from the file; they are not edited here (documented
  deviation, flagged for a future check-maintenance pass).

### WS3 — Anchors file reconciliation (bookkeeping only)

Regenerate every summary field of `INDUS_FINAL_ANCHORS.json`
(by_confidence, metadata counts, n_high, total_all_entries, total) from
the entries themselves. No anchor entry (reading / confidence / basis)
is modified; a before/after hash of the `anchors` mapping must be
identical. The canonical count definitions are recorded in the file
metadata and the ledger, including: the preprint's "161 anchors" is the
Phase-170 grammar-retest subset — a distinct defined quantity, not the
file total. Foundation check (H21) must still pass its anchors checks.

### WS4 — Discovery triage of the 78 queued items

Triage every status-"new" item in the discovery queue using the pipeline's
own mechanisms and status vocabulary (API-driven; no hand-editing the
discovery DB, no new external fetching). Report disposition counts by
topic and status, plus any items the pipeline cannot process, with
reasons.

## Assumptions (H13 epistemic boundaries)

- The Phase-52 SA's published-era claim (z=16.01, ledgered as VERIFIED in
  the foundation script) rests on a run whose artifact was lost; this
  package's re-run is a fresh execution on current anchors/LM and its
  result — whatever it is — supersedes nothing in the ledger history; a
  divergent z is reported as a divergent re-run result, not edited to fit.
- Crosswalk evidence tiers: an explicit in-repo equivalence table with a
  named published source counts as evidence; bare number identity does
  not. Adversarial case: some Phase-71/Phase-96 identity entries may in
  fact be correct — they are still inference until a source states them,
  so new identity-only pairs go to candidates.
- The running backend on :8001 is used for WS4 via its public API; the
  discovery DB it writes to is runtime state, not tracked repo content.
- GPU: this VM has no CUDA GPU (foundation NEW-G warns; torch absent).
  WS1 runs the established CPU path (BigramScorer is NumPy by design) and
  the script's own GPU reporting records the device honestly.

## Out of scope

- PR #58's branch and its CI; any merge of this package's PR.
- Anchor reading/confidence changes (WS3 is bookkeeping only).
- Re-adjudication of Phase-104 claims (WS2 reports addressability only).
- New external fetching; Mistral OCR; ICIT-dependent predictions.
