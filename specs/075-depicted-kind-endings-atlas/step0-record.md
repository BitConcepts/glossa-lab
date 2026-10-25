# Spec 075 — Step-0 record

**Date:** 2026-10-25 (execution day)
**Executor:** Phase-441 instrument, run under the owner's execution order of
2026-10-25 (12:03 EDT) after OSF registration jv74f was approved and public.
**Contract:** freeze digest
`aa06726f545218c5bcee4b3a5df94c920828fead4e06e2ccec1eeffce44ac5cf`;
all six gates of spec section 6 ran fail-closed, in the frozen order. A gate
failure closes the execution with the frozen consequence and no count is
computed past it; no gate failed. Full gate details are in the machine record
(`reports/phase441_results.json`, field `gates`) and in
`reports/phase441_report.md`.

## Gate results (in order)

- **Gate 0.1 — PASS.** The asset pins of section 3, asserted against Spec
  073's executed record: both v2 freeze records are present, and the live
  products hash to the freeze's pins — Registry v2
  `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`
  (1,013 rows) and Asset A v2
  `681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`
  (552 rows). Asset A v2's per-kind counts, counted from the file at this
  gate: other 246, unidentified 211, human 43, animal 30, object_goods 22,
  sky_cycle 0; dispute counts none 548, borderline 4, contested 0 — matching
  the freeze record. (Had this gate failed, this execution would have closed
  ASSET NOT FROZEN or ASSET PIN MISMATCH with no counts; it did not fail.)
- **Gate 0.2 — PASS.** The Shakti intake (P-F1 S1/S2): the corpus
  (restricted local, never in git) hashes to
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68` and
  the row-grade file to
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`.
  The census reproduces exactly: 5,704 rows; 5,536 analyzable; grades
  3,212 documented-lineage / 2,087 undocumented-corroborated / 405
  undocumented-uncorroborated.
- **Gate 0.3 — PASS.** The input-integrity pins of section 3: the sign
  crosswalk of record hashes to
  `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf`;
  Registry v1 to
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`;
  the anchors file to
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at
  both the before and after readings (byte-identical across the run).
- **Gate 0.4 — PASS (the reproduction assertion held; keying complete).**
  The primary population, enumerated under section 3's construction
  (documented-lineage rows only; sequences with `000` tokens dropped),
  reproduces the frozen figures exactly: **3,045 analyzable rows, 557
  distinct signs, 550 in sequences of length ≥ 2**. As the spec flags, this
  is a replay/drift gate over quantities verified at the freeze. Every
  enumerated sign was then keyed to exactly one Asset A v2 row under the
  two-leg route (DD-075-5): 423 signs under leg 1 (Registry v2's
  parpola_1982 rows' wells_ids), 133 under leg 2 (Registry v2's icit_wells
  rows) — 556 signs keyed, to 424 distinct Asset A v2 rows (the frozen
  route is many-to-one: more than one population sign can key to the same
  asset row, each to exactly one). Token **999** stands as the named
  exclusion of section 4.3: 2 primary rows, 2 occurrences — counted, never
  keyed or classed. No POPULATION NOT REPRODUCED and no POPULATION NOT
  KEYED closure applied. The keying publication hash (the keyed population,
  published in the machine record before any rate was computed) is
  `0a732022828db1bf…`.
- **Gate 0.5 — PASS (the census, published before any kind rate).** The
  class census on the primary population, with the floors of section 4.5
  applied to it in this record: **other — 307 member signs, 7,006 pooled
  occurrences; human — 53 signs, 978 occurrences; animal — 39 signs, 1,179
  occurrences; object_goods — 24 signs, 2,159 occurrences.** (Member signs
  are population signs keyed to a row of the kind — hence they can
  outnumber the kind's Asset A v2 rows, gate 0.4's many-to-one note.)
  Unidentified: 133 signs, 481 pooled occurrences — counted as context,
  members of no class and no comparison class (DD-075-4). Token 999: 2
  occurrences. The corpus-wide final-position rate, published as
  descriptive context, is 3,045 final occurrences of 11,805 total =
  **0.2579**. **No kind is TOO THIN**: every kind clears both floors
  (20 signs, 30 occurrences). The borderline signs sensitivity S1 removes
  are named here, as section 5.4 directs: **255** (P073, animal), **256**
  (P074, animal), **520** (P217, object_goods), **716** (P320, other),
  **717** (P320, other) — five population signs standing on the asset's
  four borderline rows.
- **Gate 0.6 — PASS (the freeze-order proof, from the external records).**
  This spec's freeze digest, recomputed from the frozen sources through
  the freeze's own machinery, is
  `aa06726f545218c5bcee4b3a5df94c920828fead4e06e2ccec1eeffce44ac5cf` —
  equal to the frozen digest and to freeze.json's. The freeze PR's merge
  state, read from the repository record: PR #389 closed and merged,
  merge commit `fd9bd448…`. This spec's OSF registration, read from the
  OSF record: jv74f `public: true`,
  `pending_registration_approval: false`, `reviews_state: accepted` —
  DOI 10.17605/OSF.IO/JV74F. Each assertion is cited to its external
  record, never to this spec's own outcome.

## The run

- Instrument: `backend/scripts/phase441_depicted_kind_endings_atlas.py`,
  experiment graph node `IndusPhase441DepictedKindEndingsAtlas`
  (`backend/glossa_lab/experiment_graph_phase441.py`), registered in
  `backend/glossa_lab/experiment_graph.py`.
- Runs: two, on 2026-10-25; `reports/phase441_results.json` byte-identical
  across both (SHA-256
  `f55ae91124e1ac74268f79035d862586a81a2f2e9596fd2318f3741c6e39ea29`).
- Restricted inputs stayed restricted-local (corpus and grades read from
  their local paths; nothing restricted entered git).
- Outcome: **PER-KIND VERDICTS** — other INCONCLUSIVE (ratio 1.0796,
  Fisher two-sided p = 0.0295); human NOT SUPPORTED (0.7785, p = 6.93e-06);
  animal NOT SUPPORTED (0.8912, p = 0.0200); object_goods NOT SUPPORTED
  (0.4055, p = 2.34e-67). No pooled verdict exists. See `outcome.md` and
  `reports/phase441_report.md`.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.*
