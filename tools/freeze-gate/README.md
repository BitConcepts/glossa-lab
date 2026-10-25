# The correctness-bearing freeze gate (C1–C5)

Built 2026-10-25 under the realignment plan's item 3.1, on the
design in the programme's goal record
(`2026-10-25-correctness-bearing-gate-design.md`) and the build
decision in `docs/decisions/2026-10-25-freeze-gate-build-decision.md`.

**Why this exists, in one paragraph.** Across 38 freezes, the AEE
gate's recorded output was register hygiene (FR-2.3 draft-cap
records); it blocked no freeze, and its confidences are graded by
the pipeline that drafted the claims (red-team finding RT-01).
That gate stays, described as what it is — register discipline.
This directory is the correctness layer beside it: machinery that
has demonstrated, on recorded examples, that it can fail
something real.

## The components

- **C1 — Kill-test battery** (`battery/`, `run_battery.py`). Four
  fixed defective designs; the current evaluator is run over them
  and the results filed. **Current result (aee 1.5.3,
  2026-10-25): the evaluator flags none of the four.** Each miss
  is a named blind spot, in plain words, in
  `battery/results/battery-result.md` — including that the
  planted unfalsifiable claim's falsifiability component scored
  a perfect 1.0, because the evaluator grades a falsifier's
  presence, not its content. That is not a failure of this
  build; it is the measurement the design asked for, and it is
  why C2 and C3 exist.
- **C2 — Independent recomputation spot-checks**
  (`freeze_records.py scaffold-c2`, template in `templates/`).
  A worker who did not draft the spec recomputes every
  gate-turning quantity plus 25% (minimum 3) of the rest, from
  the spec text and pinned inputs only. *Catches:* the
  wrong-pin class (battery case iii) and any arithmetic or
  transcription slip in a frozen quantity. *Does not establish:*
  full recomputation — it is a sample, and the record states
  its coverage.
- **C3 — Evidence verification on a sample** (`scaffold-c3`).
  Verification switched on for every verdict-bearing claim plus
  at least 20% of the remainder; the verifier reads the cited
  text against the claim (the engine resolves refs and hashes;
  support is judged by the verifier — battery case iv shows the
  engine alone does not catch an inverted citation). *Catches:*
  citations that resolve but do not support. *Does not
  establish:* that unsampled claims' evidence is sound.
- **C4 — One mechanical block** (`check_freeze_gate.py`, CI job
  "Freeze gate records check (C4)"). A freeze PR fails unless
  its tree carries a current-evaluator C1 result, a C2 record
  with no unresolved mismatch on a gate-turning quantity, and a
  C3 record with no unverified verdict-bearing claim. The check
  reads files, not attestations. **Enforcement state, stated
  honestly: the CI job exists and is demonstrated able to fail,
  but it is NOT a required check in branch protection.** The
  first strengthened freeze (the endings atlas) is a shadow
  freeze — the gate runs in full and is reported — and the
  check becomes required with the freeze after it (build
  decision, choice 3). *Does not establish:* that the records
  are truthful — only that they exist, are current, and are
  internally complete; C1–C3 are what make them hard to fake
  cheaply.
- **C5 — Published gate statistics** (`gate_statistics.py` →
  `docs/freeze-gate/gate-statistics.md`). Findings by kind,
  freezes blocked by component, and the battery's named blind
  spots, generated from the records. The first strengthened
  freeze record carries the table.

## Running it

```
python tools/freeze-gate/run_battery.py            # C1 (needs the aee evaluator)
python tools/freeze-gate/freeze_records.py scaffold-c2 <spec-dir> --drafter X --recomputer Y --quantities qs.json
python tools/freeze-gate/freeze_records.py scaffold-c3 <spec-dir> --verdict-bearing ID [ID ...]
python tools/freeze-gate/freeze_records.py validate <record.json> [...]
python tools/freeze-gate/check_freeze_gate.py <spec-dir> [...]   # C4, one spec
python tools/freeze-gate/check_freeze_gate.py --all              # every spec carrying gate-records/
python tools/freeze-gate/gate_statistics.py                      # C5
python -m pytest tools/freeze-gate/tests/ -q                     # machinery tests
```

The evaluator version the gate is calibrated to lives in
`evaluator-version.txt`; a freeze's C1 record for any other
version fails C4 until the battery is re-run.
