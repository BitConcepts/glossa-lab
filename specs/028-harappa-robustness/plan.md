# Spec 028 — Plan

> ## FROZEN UNDER DELEGATED ADJUDICATION — 2026-10-11
>
> Owner order (verbatim): "Also do the Harappa robustness
> design follow up and execute it based on what you think
> the best way forward is." Adjudication record:
> `adjudication.md`. This plan's sequence is operative under
> that delegation; execution remains gated on the freeze
> merge and the OSF registration, in that order.

**Governing documents:** `spec.md`, `claims.json`, and
`checklists/requirements.md` in this directory; Spec 027's
Stage 1 freeze and outcome records; Spec 026's framework
artifacts; the Glossa constitution; and governance rules
H2, H6, H13, H15/H23, and H21.

**Tooling record:** `working/tooling.md`. Versions pinned
for this spec's lifecycle runs: specify CLI 1.0.10; AEE
extension v1.1.0; evaluator extension v1.0.0; AEE package
1.0.4 from the Glossa venv on PATH. The spec-kit venv
carries AEE package 1.0.2, so every AEE invocation states
and pins its PATH.

## 1. Lifecycle sequence (this spec)

1. **Constitution check** — §4 below.
2. **Specify** — `spec.md` plus the structured claim
   register `claims.json`; integrity checked with Spec 026
   machinery (16 claims).
3. **Adjudication record** — the owner's delegated-design
   order recorded verbatim in `adjudication.md`; no
   separate adjudication round exists for this spec.
4. **Margins-only audit** — `build_margins_audit.py` →
   `margins-audit.json`: population flow reproducing the
   Phase-392 frozen counts, per-arm margins, quota
   feasibility, Arm C counts. No outcome field (test-pinned
   fence).
5. **Synthetic calibration** — `build_calibration.py`
   through `pipeline393.py` → `calibration.json`: both arms'
   controls on synthetic populations only. Calibration
   forced Amendment 1 (controls regenerate their synthetic
   population per draw; permutation strata refined to type
   class × legible-length value), recorded in `freeze.md`
   with its synthetic evidence and the confirming
   diagnostic — the Phase-392 Amendment 1 pattern.
6. **Plan + tasks + checklist** — this document, `tasks.md`,
   `checklists/requirements.md`.
7. **AEE hooks** — AEE assess plus evaluator-contract
   outputs saved under `aee/` after specify, plan, and
   tasks; outcomes recorded. A `fail` outcome blocks the
   freeze until its recovery record is complete.
8. **Freeze** — `freeze.md` + `freeze.json` (framework026
   digest via `build_freeze.py`) + freeze tests in
   `backend/tests/`. The freeze PR merges only on CI
   verified from the run's own conclusion and job logs.
9. **OSF registration** — the frozen contract registered
   (OSF Preregistration schema, public, no embargo) after
   the freeze merge and before execution; recorded in
   `osf-registration.md` and both ledgers.
10. **Execution (Phase-393)** — H23 order: script → graph
    module → registration in `experiment_graph.py` →
    registration verification → run, once, under the
    freeze. Outputs to `reports/phase393_results.json` and
    `reports/phase393_report.md`; outcome record, side-by-
    side statement, and (if warranted) the historical
    assessment in this directory; ledger entries in both
    program ledgers.
11. **Closeout** — full backend suite and foundation check
    on merged main; anchors byte-identical verified by
    sha256; PRED register untouched verified; deviations
    all recorded.

## 2. Design summary (from spec §5)

- **Arm A (primary):** Phase-392 population minus Harappa;
  identical cell rarefaction (n_cell 49, 6 cells, 294/draw);
  LOSO over 5 sites; S-complete sensitivity.
- **Arm B (secondary):** full population; equal per-site
  quota Q = 52 per draw (312/draw) under the frozen
  allocation rule; LOSO over 6 sites with Q held constant.
- **Arm C (exploratory):** Harappa decomposition —
  centroid distance matrix, per-column BC contributions,
  within-type distances. No verdict, no p-values.
- **Shared:** M77; 125 columns; Bray–Curtis adjusted-R²
  PERMANOVA; margin 0.01; 199 draws; 499 permutations
  within type × length-value strata; seed 20261012;
  per-arm discriminating controls (failure = that arm
  INVALID); per-arm verdict rules (spec §5.5); hierarchical
  reporting, no pooled headline.

## 3. Principal risks and mitigations

| Risk | Mitigation in design |
|---|---|
| Arm A is a foregone conclusion from Phase-392's published LOSO number | Verdict turns on quantities Phase-392 never computed for this population (rejection share, own LOSO clause, own controls, fresh seed); stated openly in spec §4 |
| Length-dispersion channel manufactures rejections | Calibration caught it pre-freeze; strata refined to type × exact length; diagnostic recorded |
| Equal-quota arm misread as "the" result | Hierarchical reporting frozen; Arm B labelled SECONDARY everywhere; no pooled headline (C06) |
| Arm C decomposition hardens into a verdict by prose drift | C05 fence: no p-values, no margin language, EXPLORATORY label in every output; generated report template carries the label |
| Freeze machinery diverges from executed machinery | Execution script copies pipeline393.py's pipeline section verbatim; identity asserted by test |
| Phase-392's record is rewritten by implication | C11 append-only rule; changed readings go in a dated historical assessment under this spec |

## 4. Constitution check

- **§I Provenance:** the corpus substrate is inherited from
  the Spec 027 freeze with hashes asserted; no new data
  enters the pipeline.
- **§II Ledger:** every step is an append-only event in
  both program ledgers (`LEDGER.md`, `glossa-indus/
  LEDGER.md`).
- **§III Foundation gate:** no anchor, language-model, or
  prior phase result changes occur; the foundation check
  runs at closeout because a new phase result file is
  added (H21).
- **§IV Falsifiable claims:** `claims.json`, §3.2 fields,
  §3.3 taxonomy, §10 boundaries, AEE as the same engine.
- **§V Public/private:** no correspondence or personal data
  anywhere in this spec.
- **§VI AI disclosure:** present in spec, plan, tasks,
  adjudication, and ledger entries.
- **§VII SDD:** sequential spec number, spec/plan/tasks,
  AEE hooks, graph-first Phase-393.
- **§VIII Verification:** JSON validity, claim integrity,
  freeze-digest replay, calibration on synthetic data,
  CI on every PR verified from run conclusions. No version
  string is introduced outside the tooling record's
  observed tool versions.

## 5. What this plan never does

Rerun or edit Phase-392; pool the arms into one headline;
give Arm C a verdict; touch an anchor; score PRED-2026;
deposit anything externally beyond the pre-execution OSF
registration; or execute Stage 2 of Spec 027.
