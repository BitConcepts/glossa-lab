# Tasks — Spec 024 / Evidence Integration

> ## FROZEN 2026-10-09 (Stage 0) with spec 024
>
> The build for Stage 0 is **Phase-133**. Stage 1
> tasks (T7–T9) remain gated on their separate
> post-Stage-0 owner go; Stage 2 tasks (T10–T11) on
> their own freezes.

## Pre-freeze (owner)

- **T0.** Owner adjudication of Decision Asks 1–4
  (spec §11) — **DONE 2026-10-09**: the owner
  (Tristen Pierson, "Execute the plan") answered
  (1) Stage 0 **GO**; (2) motif pilot approved **in
  principle** as drafted, separate post-Stage-0 go
  still required; (3) coder basis **blinded AI
  double-coding with the Phase-132 disclosure**;
  (4) Stage 0 inventory dataset **published CC BY 4.0
  through the release gate** at Stage 0 completion.
  Recorded verbatim in the spec §11 freeze record.
- **T0a.** Freeze commit for Stage 0 (owner values
  written in; banner flipped; committed alone —
  Spec 023 §12 pattern) — **DONE 2026-10-09** (this
  commit).

## Stage 0 — Context-field inventory (starts only after T0a)

- **T1.** Coverage-matrix builder: scripted audit
  over the layers of spec §2, emitting the
  (layer × field) matrix of §3.2 as machine-readable
  output, with counts recomputed from the files —
  never copied from prior reports. — **DONE
  2026-10-09 (Phase-133)**: builder
  `backend/scripts/phase133_stage0_inventory.py`;
  243 (layer × field) rows over 9 layers in
  `data/evidence_integration/`
  `phase133_stage0_inventory.json`.
- **T2.** Join-key audit per §3.3: volume-scoped
  catalogue keys re-derived; mayig and horus84
  candidate keys tested empirically (match /
  ambiguous / unmatched + collision rates);
  `cisi_number` documented as prohibited; museum
  cross-reference census. — **DONE 2026-10-09
  (Phase-133)**: mayig 179 matched / 0 ambiguous /
  0 unmatched; horus84 2,895 matched / 2 ambiguous /
  2,782 unmatched (NOT USABLE); museum
  cross-references 0/40.
- **T3.** Field-provenance grading per §3.4
  (O / C / I with reasons), including the explicit
  Class I exclusion list. — **DONE 2026-10-09
  (Phase-133)**: 243 fields graded (O 207 / C 7 /
  I 29); Class I list named in the Stage 0 report.
- **T4.** Non-machine-readable pass: Kodumanal
  volume and Kunal article field structure recorded
  descriptively; anomalies found during T1–T3
  (e.g. misnamed / mismatched raw files) recorded,
  not routed around. — **DONE 2026-10-09
  (Phase-133)**: Kodumanal/Kunal/Penn descriptive
  pass in the inventory JSON + report §6, incl.
  the `holdatllc_seal_catalog.csv` content
  mismatch (Ollama model-list JSON, 0 seal records).
- **T5.** Stage 0 report: what context evidence
  exists, what does not, which §5 sketches survive;
  ledger entries appended. — **DONE 2026-10-09
  (Phase-133)**: `reports/`
  `phase133_stage0_report.md` (incl. Appendix A
  drift table and arm-by-arm verdicts); entries
  appended to both ledgers.
- **T6.** Inventory dataset disposition per
  Decision Ask 4 — adjudicated 2026-10-09:
  **release-gated CC BY 4.0 publication** at Stage 0
  completion (facts only, no images). — **DONE
  2026-10-09**: published with Zenodo v4.6.0 (DOI
  10.5281/zenodo.23267995, record 23267995) through
  the mandatory release gate (PASS 13/13, recorded
  in `RELEASE_VALIDATION.json` `release_v4_6_0`);
  post-deposit checksums confirmed 13/13; OSF
  registry updated the same day.

## Stage 1 — Motif-coding pilot (separate go; designed in spec §4)

- **T7.** Stage 1 freeze (sample rule + seed,
  codebook from §4.3 categories, gates from §4.5
  with owner values, coder basis per Decision
  Ask 3). — **DONE 2026-10-09 (Phase-134)**:
  owner go given 2026-10-09 ("Approve the Stage 1
  motif-coding pilot"); freeze record at
  `stage1-freeze.md` in this directory (frame
  rule + seed `phase134-20261009`, premise
  correction of record on the sample population,
  codebook as frozen, metric definitions).
- **T8.** Blinded double coding + adjudication;
  disagreement log preserved; gold-subset drift
  measurement; AI disclosure attached if applicable.
  — **DONE 2026-10-09 (Phase-134)**: two blinded
  passes over the 100-object frame, gold third
  coding of the 20-object subset, adjudication of
  all 16 disagreements with the log preserved in
  the dataset; all roles AI-executed with the
  disclosure attached (report §3, dataset meta).
- **T9.** Pilot report with gate verdicts as found;
  motif arm proceeds, pauses, or closes exactly as
  §4.5 prescribes. — **DONE 2026-10-09
  (Phase-134)**: `reports/phase134_pilot_report.md`
  — exact agreement 0.84, Cohen's κ 0.7885;
  proceed gate NOT MET (agreement arm), stop rule
  NOT FIRED → **MIDDLE BAND** per §4.5; the
  Stage 2(b) decision is framed for the owner,
  not taken.

## Stage 1 continuation — Combined path (owner approval 2026-10-09)

- **T9b.** Codebook clarification of the ILLEGIBLE /
  SCRIPT_ONLY / GEOMETRIC boundary from the 16 adjudicated
  Phase-134 disagreements + Phase-135 re-pilot freeze
  (fresh sample, identical gates). Owner approval
  2026-10-09: "Run the combined path — clarify the
  boundary, re-pilot fresh, freeze Stage 2(b) only if
  the gates pass, publish the combined record." —
  freeze record `stage1-freeze-2.md` in this directory.
  — **DONE 2026-10-09**: Rules B1–B5 frozen in
  `stage1-freeze-2.md` §2 (freeze commit `dee4e5c2`,
  before the frame was drawn); taxonomy, precedence
  rule, and all gate thresholds unchanged.
- **T9c.** Phase-135 re-pilot execution (blinded double
  coding + gold + adjudication under the clarified
  codebook; all quantities from on-disk records) and
  pilot report with the gate verdict as found. —
  **DONE 2026-10-09 (Phase-135)**: fresh 100-object
  frame (0 overlap with Phase-134, verified), two
  blinded passes + gold + adjudication of all 22
  disagreements, no deviations;
  `reports/phase135_pilot_report.md` — exact agreement
  **0.78**, Cohen's κ **0.7129**.
- **T9d.** Branch deliverable per `stage1-freeze-2.md`
  §5: Stage 2(b) design freeze (proceed gate only) /
  motif-arm closure statement (stop rule) / framed
  owner decision (middle band again). — **DONE
  2026-10-09**: proceed gate NOT MET (both arms),
  stop rule NOT FIRED → **MIDDLE BAND for the second
  time**; no Stage 2(b) design drafted; the owner's
  decision is framed in the Phase-135 report §8.
- **T9e.** Combined motif-arm publication: Zenodo
  v4.7.0 (Phase-134 dataset + Phase-135 dataset +
  program note; codes and logs only, no images)
  through the mandatory release gate; OSF registry
  updated in step. Authorized by the same owner
  approval (T9b). — **DONE 2026-10-09**: published
  as Zenodo v4.7.0 (DOI 10.5281/zenodo.23270096,
  record 23270096) through the mandatory release
  gate (PASS 18/18 at e698cff2, recorded in
  `RELEASE_VALIDATION.json` `release_v4_7_0`;
  final gate run at the gate-record merge 52580e43
  PASS 18/18); post-deposit checksums confirmed
  18/18; OSF registry updated the same day.

## Stage 1 — Motif arm closure (owner decision 2026-10-09)

- **T9f.** Motif-arm closure record. Owner decision
  2026-10-09: paths (b) AND (c) together — the arm
  rests now on its published two-pilot record, and
  path (b) is preserved as the sole reopening
  condition. — **CLOSED 2026-10-09**: the motif arm
  is closed as run on the AI-coder basis
  (Phase-134: 0.84 / κ 0.7885, MIDDLE BAND;
  Phase-135: 0.78 / κ 0.7129, MIDDLE BAND;
  Zenodo v4.7.0, DOI 10.5281/zenodo.23270096);
  no Stage 2(b) design exists or is authorized.
  Reopening ONLY under a new owner decision AND
  human expert coders (path (b)), clarified
  codebook (`stage1-freeze-2.md`), fresh sample,
  identical frozen gates; a third AI-basis pilot is
  expressly not a reopening path. Record:
  `motif-arm-closure.md` in this directory.
  T7–T9e stand as executed above; nothing in this
  closure alters them, and Stage 2 arms (a), (c),
  (d) are unaffected.

## Stage 2 — Association tests (each its own freeze; spec §5)

- **T10.** Family declaration + first test freeze
  (default order: (a) terminal class × object type,
  (c) site repertoire; (b) only if T9 passes its
  proceed gate; (d) comparative-only, any time after
  Stage 0, under boundary 4).
- **T11.** Per-test execution and report, results as
  found, NOT ESTIMABLE where the estimability rule
  bites, lineage labels in headlines.

## Explicitly not tasks of this program (any stage)

- Any change to anchors, readings, or PRED-2026.
- Any transcription work (Spec 023's line, stopped).
- Any outreach — to libraries, researchers, or
  repositories — of any kind.
- Any acquisition; Stage designs use only material
  already in hand (spec §2.7).
- Any image handling outside the gitignored local
  store.

## Stage 2 — execution record (2026-10-09)

- **T10.** Family declaration + test freezes — **DONE 2026-10-09**: the declared family F = {F1 (a) terminal × object type, F2 (c) Holdat site repertoire, F3 (c) ICIT-lineage site repertoire} with Benjamini–Hochberg q = 0.05 across executed members is declared in `stage2a-freeze.md` §1. Arm (a) frozen in `stage2a-freeze.md` (Phase-136) on the owner instruction "Do all next things" (2026-10-09). Arm (b) CLOSED (T9f) — not in the family, not touched.
- **T10b.** Arm (c) design freeze — **DONE 2026-10-09**: `stage2c-freeze.md` (Phase-137; family members F2 + F3; layers tested separately, never pooled; §5.1 default minimum-cell rule replaced by the stated permutation-matched rule with mandatory sparsity disclosure).
- **T10c.** Arm (d) descriptive-protocol freeze — **DONE 2026-10-09**: `stage2d-freeze.md` (Phase-138; descriptive only; not a family member; boundary 4 and the ≥1,000-year dating-gap caveat frozen into every output).


## Stage 2 — execution (2026-10-09)

- **T11.** Per-test execution and reports —
  **DONE 2026-10-09**: Phase-136 (arm (a), F1;
  PR #121, merge `e7d17f6a`) — CMH 47.0047, raw
  p = 0.0001, MH common OR 2.384 (1.847–3.077);
  Phase-137 (arm (c), F2 + F3; PR #122, merge
  `75943a7f`) — F2 Holdat χ² 745.95, raw
  p = 0.7354; F3 ICIT-lineage χ² 4,966.36, raw
  p = 0.0001; Phase-138 (arm (d), descriptive
  only; PR #120, merge `4069bcb1`; corrective
  PR #123, merge `1c2a5fd2`) — 417 rows / 395
  objects, `motif_chapter` filled 0/417.
  Combined report
  `reports/phase136_137_138_stage2_report.md`
  applies the declared family's Benjamini–Hochberg
  correction once: **F1 q = 0.00015 SUPPORTED;
  F2 q = 0.7354 NOT SUPPORTED; F3 q = 0.00015
  SUPPORTED.** Arm (b) untouched (CLOSED, T9f).
- **T12.** Stage 2 publication — Zenodo v4.8.0
  (program note + the three phase results JSONs,
  CC BY 4.0) through the mandatory release gate;
  OSF registry updated in step. (Completion
  appended below on publication.)
