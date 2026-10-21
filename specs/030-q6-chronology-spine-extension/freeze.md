# Spec 030 — Freeze Record (Q6 Chronology-Spine Extension)

> ## FROZEN at the Spec 030 freeze merge (2026-10-12)
>
> Basis: Spec 030 as adjudicated by the owner
> (`adjudication.md` — §9 Asks 1, 3, 4, and 5 adopted
> as proposed under the owner's instruction "Freeze
> it"; Ask 2 expressly not covered). The governed
> claim register enters this freeze as recovered at
> the freeze AEE pass (`aee/recovery-specify.md`) —
> the freeze digest below covers the recovered
> register, never the pre-recovery one. The machine
> freeze record is `freeze.json` (framework026
> digest, built by `build_freeze.py`).

## 1. What is frozen

- **The design.** `spec.md` as adjudicated: the
  spine extension that could let the frozen Stage 0
  criteria (Spec 027 `stage0-freeze.md` §4 —
  thresholds, 5250–3850 BP window, grade and material
  vocabularies, unchanged per F030-C01) pass on
  re-test, or could show on margins only that they
  still cannot pass from lawfully usable sources.
  Routes in stop-point order **R5 → R1 → R2 → R4 →
  R3** (adopted Ask 4), tracing selectivity
  short-lived-first (adopted Ask 3), coordinate-less
  rows admitted for gazetteer-established sites with
  coordinate state inherited-from-cluster (adopted
  Ask 1), the §5 integrity rules, and the §6 re-test:
  the Stage 0 §4 assessment verbatim, margins only,
  with SUPPORTED-FOR-FREEZE-DESIGN or
  NOT-YET-TESTABLE as its only outcomes and a
  negative extension outcome as a valid closure
  (F030-C07).
- **The governed claim register.** `claims.json`,
  register_version `0.2-draft`: 7 claims
  (F030-C01…C07), recovered at the freeze AEE pass —
  the AEE hook pass over this register returns
  **pass** at after_specify, after_plan, and
  after_tasks (7 claims, 0 failure modes, 0 below
  the 0.70 threshold; `aee/` artifacts).
- **The measured gap the design rests on**, pinned
  by the freeze tests from the Stage 0 record
  (`reports/phase391_results.json`): Q6
  timing-support NOT-YET-TESTABLE — C1 = 1 region
  (threshold 3), C2 = 5 window d/a sites (threshold
  10), C3 = 0.0 short-lived share (threshold 0.5),
  C4 = 70 BP median σ (threshold 80, pass), over 31
  window d/a rows.
- **The phase assignment.** The extension build is
  **Phase-394** (adopted Ask 5; first free number
  after Phase-393).

## 2. Bookkeeping rule for the frozen bytes

The design sources (`spec.md`, `claims.json`,
`adjudication.md`) are digest-covered as frozen and
are not bookkeeping: any change to them after this
freeze is a design change requiring a new owner
adjudication. Phase-394's build and outcome records,
when they exist, are recorded in this directory and
in the program ledgers (root `LEDGER.md`), never by
editing the frozen files. The freeze itself is never
regenerated (Spec 026 §4.7).

## 3. Tooling pins

- AEE package **1.0.4** (Glossa venv, PATH-pinned for
  every AEE run); AEE extension v1.1.0; evaluator
  extension v1.0.0; specify CLI 1.0.10; Python 3.12.3.
- Freeze machinery: `glossa_lab.framework026`
  (`build_freeze` / `verify_freeze` /
  `check_dependency_integrity`).

## 4. What this freeze does not do

- **It does not execute the build.** Adopted Ask 5
  makes OSF registration of this frozen contract a
  precondition of any execution, mirroring Spec 027
  Stage 1. The registration is prescribed, not
  performed, by the adjudication and this freeze;
  execution follows registration under its own go.
- **It does not decide Ask 2.** Whether the
  CONTESTED sensitivity binds a future Q6 freeze is
  expressly not covered by the adjudication; the
  re-test reports both computations (integrity
  rule 5), and bindingness is reserved to a future
  Q6 freeze's adjudication under Spec 027 §8.2.
- **It changes no Spec 027 record and no Q6
  status.** Q6 remains registered-blocked under
  F027-C16; a Q6 freeze, if the re-test ever
  supports one, is a separate later act under
  Spec 027 §8.2 with its own freeze and owner gate.
- **It loosens no criterion.** The frozen Stage 0
  thresholds, window, grade rule, and material
  mapping apply verbatim (F030-C01); a negative
  extension outcome is never grounds to loosen them
  (F030-C07).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## Addendum — freeze-test amendment (2026-10-21)

Owner-ordered on 2026-10-21, verbatim: **"Amend
the freeze test (Spec 038 precedent)"**; recorded
in full in `adjudication.md` (freeze-test
amendment section) and in the LEDGER entry of the
same date.

The Ask 2 ruling of 2026-10-21 is recorded by
dated append in `adjudication.md`, a
digest-covered source of this freeze, so the
freeze replay fence
(`backend/tests/test_spec030_freeze.py::test_freeze_record_replays`)
failed by construction on the ruling record
(PR #241): `verify_freeze` reported the single
backend failure `frozen source changed:
specs/030-q6-chronology-spine-extension/adjudication.md`
in an otherwise 1,366 passed / 20 skipped suite,
although no frozen byte was altered — the frozen
bytes remain an exact prefix of the live file.
The amendment narrows that single assertion for
`adjudication.md` to prefix-integrity: the
freeze-time bytes (5,867 bytes, SHA-256
`f962f910d81cb63f44abb4db0e1be2ee0fb9fca45f5242f23656113ddd609738`)
are pinned in `freeze.json` (`prefix_pins`) and
must remain an exact prefix of the live file;
dated appends after them are permitted. Every
other covered source keeps its live whole-file
hash assertion; no other assertion changes, and
no production code changes. `freeze.json` is
recomputed once over the amended state by
`build_freeze.py` (framework026), in the freeze
environment (python 3.12.3, aee 1.0.4), after the
pre-amendment builder reproduced the freeze-act
digest from the original bytes exactly; the
successor digest is the `digest` recorded in the
amended `freeze.json`, carried in the LEDGER
entry of 2026-10-21.

The freeze-act digest
`3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3db00e9`
stands as the digest of the freeze act in every
record that cites it — the OSF contract
registration (bge3k), `osf-registration.md`,
`outcome.md` — and is edited nowhere.

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
