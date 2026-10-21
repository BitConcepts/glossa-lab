# Phase-410 — Spec 043 step-0 report

Prediction: PRED-2026-012 (H4 successor: ICIT Function Alignment) — standing PENDING, unscored. Execution date: 2026-10-21. Freeze digest: `8a8a334f13577cbb704fc96e6d4c0451cb1277a3470b90c98b3f86c362475987`. OSF registration vmcra (approved and public). Execution authorized by the owner's approval of the runnable-experiments campaign plan AS WRITTEN on 2026-10-21 (Wave 3).

## Outcome: PROVENANCE - CANNOT BE RUN AS WRITTEN

## Checks, in frozen order

- **Check 0.1 — Sources and pins: PASS** — all seven frozen sources present and hashed to the freeze record's pins; the PRED-2026-012 entry located standing as registered (criterion verbatim; Outcome PENDING).
- **Check 0.2 — Enumeration, re-derivation, cross-check: PASS** — 803 rows read; census 791 uncoded, 12 coded (ITM 4, LOG 2, NUM 2, TMK 2, SHN 1, SYL 1); ITM = {P056, P324, P378, P385}; re-derivation of all 803 values from the pinned builder rule exact (zero mismatches); held records verified (P385, P378 ITM; P098 no code); cross-check read in full (611 records: 579 empty, 32 free-text glosses, no ITM, no LOG) with every disagreement recorded sign-by-sign in the step-0 record, as expected in kind.
- **Check 0.3 — Provenance gate: FAIL** — evidence set D1-D4 produced and adjudicated under DD-043-10. All three limbs FAIL. Class definition: the produced documents define the ICTM class by cluster-final behaviour — Wells classifies signs 'according to their preferred text position' and ICTM signs are those that 'mark the end of initial clusters' (Fuls 2013, s.2, s.3.7). Per-sign basis: every stated basis is positional (W740 terminal distribution; W820, W817, W861 initial distribution), and W231 has no stated basis at all. Source agreement: Wells' published ICTM class is exactly signs 060, 001, 002 (Wells 2015, ch. 3); 817, 820, 861 are published as initial signs, 820 also as a terminal marker — different functions from the builder table, and W231 omitted. The study therefore closes as PROVENANCE — CANNOT BE RUN AS WRITTEN, unscored. The LOG trace is recorded in the step-0 record and gates nothing (DD-043-12).
- **Check 0.4 — Recorded Phase 5 output verification: NOT RUN** — the frozen order reaches it only behind a passed gate. The recorded clustering and characterisation were byte-hashed at check 0.1 for integrity and never opened for assignments; the sanity anchor was not reproduced, because the check that reads it was never reached. No Phase 5 assignment was looked up for any sign.

## What was not done

No scoring ran: no share, coverage figure, or verdict exists. PRED-2026-012 remains unscored and its registered Outcome stands PENDING; PRED-2026-007's PARTIALLY CONFIRMED stands untouched as its own pre-execution record. This closure records what the classification's assignments rest on; it is not a verdict on the criterion and not a refutation.

Step-0 record: `reports/phase410_results.json` (step-0 record SHA-256 `019c65991835505c7f8ecac11e3b62f5b01b1fe825bed3c46eb23fdb2879c948`).

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.*
