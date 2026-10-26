# Spec 077 — Tasks

Freeze and execution tasks, in execution order. The
execution tasks (T6–T9) run only after the freeze PR
has merged on genuine CI including the required C4
check.

- [x] T1 — Draft the spec from the M7 design (design
      carried as written, with its amendment;
      freeze-fixed completions FF-1…FF-8 in §0), the
      claims register (F077-C01…F077-C10, 0.7 form),
      and this adjudication.
- [x] T2 — Verify every pin first-hand from repo main
      and the canonical store (Registry v2, Spec 075's
      machine record, both witness datasets, the
      Figure 3.6 file, the C-7 raw text) and derive
      token 999's reference behavior under Spec 075's
      frozen construction (2 occurrences, 0 finals).
- [x] T3 — Run the AEE lifecycle hooks
      (after_specify / after_plan / after_tasks) under
      the pinned evaluator (aee 1.5.3) in the freeze
      configuration; file the artifacts and the freeze
      AEE note; complete DD-077-3.
- [x] T4 — File the strengthened-gate records: C1
      kill-test battery (the canonical result for the
      current evaluator), C2 independent spot-check,
      C3 evidence sample (verification on); run the
      C4 checker locally on the assembled directory.
- [x] T5 — Compute the freeze digest (build_freeze.py,
      framework026) over the final texts; write
      freeze.md; regenerate the gate statistics (C5);
      open the freeze PR; merge only on genuine CI
      green including the required C4 check.
- [x] T6 — Execution step 0: verify every §3 pin;
      verify witness tables' actual columns and
      content; reproduce the population census and
      999's reference behavior; file the 13-id
      resolution table; verify the Table I input
      against FF-7 and record its SHA-256. Any
      failure closes the execution CANNOT BE RUN AS
      WRITTEN, naming the failed item.
- [x] T7 — Counting: per-sign witness table under
      FF-3/FF-4; raw share, ancestry-adjusted share,
      per-witness breakdown; sensitivities S1 and
      S2; the gap list.
- [x] T8 — Token 999 attack: the candidate table
      (every witness sign meeting condition 1, with
      its condition-2 reading) under FF-6/FF-7; the
      identity named or NO PUBLISHED IDENTITY.
- [x] T9 — Verdict and filing: verdicts in the frozen
      words (F077-C01, F077-C02); `step0-record.md`,
      `outcome.md` and `reports/phase443_results.json`
      filed; anchors byte-identical check; execution
      PR merged on genuine CI.
