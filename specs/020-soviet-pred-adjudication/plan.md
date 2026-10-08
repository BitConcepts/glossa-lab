# Plan — Spec 020 / Soviet Dataset Adjudication for PRED-2026-001/002

Owner-authorized 2026-10-08 (STEP 2 of the Glossa-Lab
program): adjudicate, as a paper decided mechanically from
pre-stated criteria, whether the Phase-121 Soviet
positional dataset qualifies as an evaluation source for
PRED-2026-001/002; run the registered scoring **only** if
the verdict is YES; otherwise record the adjudication and
stop.

## Approach

1. **Criteria before application.** The adjudication
   criteria (§2 of the spec) are derived mechanically from
   the registered texts — the register §2 and spec 018
   §§3–7 — and are written, with their pass conditions and
   textual citations, before any criterion is applied to
   the dataset (§4). No criterion is invented from the
   dataset's properties; every property of the dataset
   enters only through §3's established facts.
2. **Texts read in full, quoted where load-bearing.**
   Register §2 entries for 001/002, spec 018 §§3–6, and
   the Phase-121 memo + dataset JSON + CSVs are read in
   full; verbatim extracts that carry a criterion are
   reproduced in spec §1 so the derivation is auditable
   from the paper alone.
3. **Facts before verdicts.** §3 establishes what the
   dataset is (published aggregate tables from the 1965
   Soviet report via Zide & Zvelebil 1976; per-table form;
   Marshall numbering; no inscription-level records) from
   the committed Phase-121 artifacts only.
4. **Conjunctive verdict.** YES requires all six criteria
   to pass for both predictions. A NO verdict triggers the
   spec §5 consequences and nothing else: an append-only
   register note, ledger entries, and this PR. The harness
   is not invoked — neither in evaluation mode nor as a
   dry run — on a non-qualifying dataset.
5. **No code changes.** The expected product is documents
   only (spec, register note, ledgers). If the adjudication
   had come out YES, the plan's scoring branch would have
   been: ingest via `backend/glossa_lab/pred_harness.py`
   under the adjudicated source class, apply §5 dedup and
   §6 scoring exactly as spec 018 prescribes, and record
   verdicts in the register append-only with tested date,
   outcome, and caveat C1 verbatim where §4 requires it.
   That branch is conditional on the verdict and is not
   executed on a NO.
6. **Anchors untouched.** The anchors file sha256 is
   asserted before and after; no anchor, claim, registry,
   or language-model file is modified.

## Verification

- Branding / contamination sweep over all new and changed
  files (no other project's names, material, or
  references; no secrets; no third-party personal data —
  H24).
- Full backend suite + foundation check (H21) in the
  dedicated worktree, and again post-merge on main.
- Ledgers in both files (H1), AI disclosure; one PR;
  merge only when complete and CI green (standing
  auto-merge rule). If CI is not green, pause and report.
