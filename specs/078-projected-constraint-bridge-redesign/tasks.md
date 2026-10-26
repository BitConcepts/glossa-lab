# Spec 078 — Tasks

Freeze and pilot tasks, in execution order. The
pilot tasks (T6–T9) run only after the freeze PR
has merged on genuine CI (FF-078-5).

- [x] T1 — Freeze-prep review of the M13 design
      (bars, NC-1…NC-8 completeness, A-FACE-2's
      falsifier, counted-population arithmetic,
      base rates against slot totals); record the
      outcome in the adjudication (no amendments
      required; no bar moved).
- [x] T2 — Draft the spec from the M13 design
      (design carried as written; freeze-fixed
      completions FF-078-1…FF-078-5 in §0; the S4
      note as §13), the claims register
      (F078-C01…F078-C10, 0.7 form), and this
      adjudication.
- [x] T3 — Verify every pin first-hand from repo
      main (export, anchors, Registry v2) and
      re-derive the inherited census; confirm every
      pre-named figure reproduces (step-0 figures:
      11,507 tokens; 5,883 strict; slot totals;
      finals partition; 677 / 178 / 13; base rates;
      counted population 86 under FF-078-2).
- [x] T4 — Run the AEE lifecycle hooks
      (after_specify / after_plan / after_tasks)
      under the pinned evaluator (aee 1.5.3) in the
      freeze configuration; file the artifacts and
      the freeze AEE note.
- [x] T5 — File the strengthened-gate records:
      C1 kill-test battery, C2 independent
      spot-check, C3 evidence sample (verification
      on); run the C4 checker locally on the
      assembled directory.
- [x] T6 — Compute the freeze digest
      (build_freeze.py, framework026) over the
      final texts; write freeze.md; regenerate the
      gate statistics (C5); the coordinator opens
      the freeze PR (branch spec-078-freeze);
      merge only on genuine CI green including the
      required C4 check.
- [ ] T7 — OSF registration (DD-078-5): filed at
      this freeze under the owner's express order;
      the coordinator performs the filing after
      merge via the ORCID/token-link route, and the
      registration identifier is recorded with the
      pilot record.
- [ ] T8 — Pilot step 0: re-derive the inherited
      census from the merged record; assert every
      pre-named figure; any mismatch closes the
      pilot CANNOT BE RUN AS WRITTEN and voids the
      inherited step-2 standing in the same record.
      (Step 2 is not re-run: inherited standing,
      §7.2.)
- [ ] T9 — Pilot step 3′: blind-code the 94 strict
      signs under NC-1…NC-8 and the FF-078-3
      blindness protocol (coder blind to census
      rows, to the 076 pilot's per-sign rows, and
      to §6 codings); judge the distributional line
      against the census rows and the functional
      line by anchor share against the base rates
      from the re-verified census; report the
      summary line and the worked-example and
      frame-absent lines separately.
- [ ] T10 — Verdict and filing: per the §7.4 bands
      — on PILOT PASSES, file F078-C02 (the §8
      licence to draft a production-register freeze
      opens; no register is produced by the pilot
      itself); on a bar or pattern failure, close
      BRIDGE DOES NOT HOLD with A-FACE-2 fallen; on
      an administrability failure, close CANNOT BE
      ADMINISTERED — THE CORE MAKES TOO FEW
      CHECKABLE CLAIMS. Either way the pilot record
      lands in this directory and in the programme
      goal record, with the coding file preserved.
