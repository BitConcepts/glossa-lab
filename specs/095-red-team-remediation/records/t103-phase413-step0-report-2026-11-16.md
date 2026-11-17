# Phase-413 — Spec 053 step-0 report

Claim: `yadav_2009_arxiv_manual_001` — standing
strongly supported, stage explained, exactly as
recorded (recorded Zipf exponent about 1.35).
Execution date: 2026-10-21. Freeze digest:
`fd2d5cb86b6aed51882a945719bb747ac34f149b08a21e6485b1407c6dc6b309`. OSF registration s9yfe
(approved and public).

## Outcome: INVALID

## Gates, in frozen order

- **Gate 0.1 — Input integrity: FAIL**
  - `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json` — MISMATCH (9dd672d107c98082e12ffaeec11d710bc307322f21b7ea354e7e454ae2599804)
  - `backend/reports/INDUS_FINAL_ANCHORS.json` — match (df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569)
  - `data/crosswalks/sign_crosswalk_master.csv` — match (4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf)
  - `backend/glossa_lab/data/mahadevan_parpola_crosswalk.json` — match (9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b)
  - `outputs/phase43_all.json` — match (78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4)
  - Anchors census: 287 anchors, 94 strict_sa_independent.
- **Gate 0.2 — Estimator self-test: NOT REACHED**
- **Gate 0.3 — Strict corpus identification and pin: NOT REACHED**
- **Gate 0.4 — Control set freeze (cited data): NOT REACHED**
- **Gate 0.5 — Census and floors: NOT REACHED**

## What was not done

Gate 0.4 (control set freeze) and gate 0.5
(census and floors) were not reached: no
control count was entered, no corpus was
exported, and no system — Indus or control —
was fitted. The sensitivities S1-S3 were not
computed. No strength label is added to the
claim's record; the claim stands exactly as
recorded. This result is a strength label
for a recorded curve fit. It is not evidence
that the script encodes language, and it
changes no verdict. (Spec section 9 fence
sentence, carried here as written; this
closure adds no label, so the fence is
restated for completeness.)

Anchors asserted byte-identical before and after:
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at both readings.

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution section VI.*
