# Spec 076 — Tasks

Freeze and pilot tasks, in execution order. The
pilot tasks (T6–T9) run only after the freeze PR
has merged on genuine CI (FF-5).

- [ ] T1 — Draft the spec from the M12 design
      (design carried as written; freeze-fixed
      completions in §0), the claims register
      (F076-C01…F076-C10, 0.7 form), and this
      adjudication.
- [ ] T2 — Verify every pin first-hand from repo
      main (export, anchors, Registry v2) and
      re-derive the §7 census; confirm every
      pre-named figure reproduces.
- [ ] T3 — Run the AEE lifecycle hooks
      (after_specify / after_plan / after_tasks)
      under the pinned evaluator (aee 1.5.3) in the
      freeze configuration; file the artifacts and
      the freeze AEE note.
- [ ] T4 — File the strengthened-gate records:
      C1 kill-test battery, C2 independent
      spot-check, C3 evidence sample (verification
      on); run the C4 checker locally on the
      assembled directory.
- [ ] T5 — Compute the freeze digest
      (build_freeze.py, framework026) over the
      final texts; write freeze.md; regenerate the
      gate statistics (C5); open the freeze PR;
      merge only on genuine CI green including the
      required C4 check.
- [ ] T6 — Pilot step 0 + step 1: re-run the frozen
      derivation from the merged record; assert the
      census and the pre-named headline numbers
      (677 / 178 / 13); any mismatch closes the
      pilot CANNOT BE RUN AS WRITTEN.
- [ ] T7 — Pilot step 2: the marginals-preserving
      shuffle null (B = 999, seed 20261026);
      report the residual's and the solo-only
      count's percentiles against their frozen bars.
- [ ] T8 — Pilot step 3: blind-code the 94 strict
      signs' claimed types under CR-1…CR-7 (coder
      blind to census rows); count exclusions
      against the ≤5 bar (frame-absent strict signs
      on their own line, CR-7).
- [ ] T9 — Verdict and filing: on PASS, file
      F076-C02 and produce the pilot-frame register
      (pilot-register.json + pilot-register.md)
      exactly as §6 specifies; on FAIL, file the
      failure record with the design's closure word
      and no register. Either way the pilot record
      lands in this directory and in the programme
      goal record.
