# Spec 074 — Step-0 record

**Date:** 2026-10-24 (execution day)
**Executor:** Phase-440 instrument, run under the owner's execution order of
2026-10-24 after OSF registration cfe7z was approved and public.
**Contract:** freeze digest
`5416a0d331e76fcec720746849969f2e86e9d79f2cc0fa583e1050662ffba36c`;
all six gates of spec section 5 ran fail-closed, in the frozen order. A gate
failure closes the execution with the frozen consequence and no count is
computed past it; no gate failed. Full gate details are in the machine record
(`reports/phase440_results.json`, field `gates`) and in
`reports/phase440_report.md`.

## Gate results (in order)

- **Gate 0.1 — PASS.** The freeze's predecessor-verification step (spec
  section 5, DD-074-11). Spec 073's executed record
  (`specs/073-keying-surface-repair/outcome.md`, verdict REPAIRED WITH NAMED
  SHORTFALL) shows both products frozen, and gate 0.4's disposition there is
  the successor-route sentence this spec is. The live products hash to the
  freeze's pins: Registry v2
  `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`
  (1,013 rows) and Asset A v2
  `681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`
  (552 rows). Asset A v2's per-kind counts, counted from the file at this
  gate: animal 30, sky_cycle 0, object_goods 22, human 43, other 246,
  contested 0, unidentified 211 — matching the freeze record. (Had this gate
  failed, this execution would have closed with no counts and no status
  movement; it did not fail.)
- **Gate 0.2 — PASS.** The carried inputs: the Shakti corpus (restricted
  local, never in git) hashes to
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68` and
  the row-grade file to
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`.
  The corpus census reproduces exactly: 5,704 rows serialized; 5,536
  analyzable; grades 3,212 documented-lineage / 2,087
  undocumented-corroborated / 405 undocumented-uncorroborated; 4,904 rows
  carrying a CISI number.
- **Gate 0.3 — PASS.** The carried pins: the Phase-433 results record hashes
  to `667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214`;
  Registry v1 to
  `8a0b2a82a3ba1de2c1e7fdcf3b978167667633fd6ba59d4b75935b89e437b0f3b`;
  the crosswalk to
  `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf`; this
  spec's freeze record carries the contract digest `5416a0d3…`; the anchors
  hash to
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at both
  the before and after readings.
- **Gate 0.4 — PASS (the reproduction assertion held).** The battery ran on
  the primary population (documented-lineage rows only) and the
  opening-strong set was enumerated in Wells space. The executed
  enumeration's canonical publication hash —
  `30092b6fd64f221ee0808addeedd11e1e800cf3d79716ba26b3fb971f396a93b` —
  **equals Spec 070's recorded publication hash exactly**; the enumerated
  set and per-sign I/M/T counts are equal to Spec 070's recorded 31 signs;
  the full class census (220 signs at the floor: TERMINAL_STRONG 42,
  MEDIAL_STRONG 81, TERMINAL_MODERATE 37, INITIAL_MODERATE 6, MIXED 23,
  INITIAL_STRONG 31) is equal to Spec 070's recorded census. Every sign then
  keyed to exactly one Asset A v2 row under the two-leg route (DD-074-8):
  26 under leg 1 (Registry v2's parpola_1982 rows' wells_ids); the five
  formerly unkeyable signs — **136, 298, 401, 617, 824** — under leg 2
  (Registry v2's icit_wells rows) to keys W136, W298, W401, W617, W824, each
  classified `unidentified` in Asset A v2. Disposition (DD-074-10):
  **POPULATION NOT KEYED does not apply** — the population is keyed only
  because Registry v2's wells-space rows supply the five asset rows, and
  those five stand in the counts as unidentified. Had the reproduction
  failed, the execution would have closed POPULATION NOT REPRODUCED with no
  counts and no status movement; it did not fail.
- **Gate 0.5 — PASS.** The comparison inventory U enumerated under
  DD-070-10's counting rule: 76 signs at total ≥ 30 on the primary
  population (73 classified — 6 animal, 67 non-animal; 0 contested;
  3 unidentified: 501, 585, 617). Every O and U sign carries an Asset A v2
  row. The S-B naming scan over Asset A v2's verbatim labels returns no
  sign identifying a unicorn: **S-B is not applicable**, stated here and in
  the outcome record as the frozen design directs — no alternative sign-list
  was hunted.
- **Gate 0.6 — PASS.** The order stands recorded in the machine record: the
  freeze quoted the v2 digests from Spec 073's executed record and the
  recorded enumeration from Spec 070's record (never from this execution);
  the population was hashed at gate 0.4, before the join below was computed;
  the outcome word below is section 4.3's precedence applied to the frozen
  section 4 arms and nothing else.

## The run

- Instrument: `backend/scripts/phase440_hunt_opening_signs.py`, experiment
  graph node `IndusPhase440HuntOpeningSigns`
  (`backend/glossa_lab/experiment_graph_phase440.py`), registered in
  `backend/glossa_lab/experiment_graph.py`.
- Runs: two, on 2026-10-24; `reports/phase440_results.json` byte-identical
  across both (SHA-256
  `d539519d6949d6ce73654290a49a0e629141a89082f7034e201135e9af1c3bc1`).
- Restricted inputs stayed restricted-local (corpus and grades read from
  their local paths; nothing restricted entered git).
- Outcome: **NOT SUPPORTED** — the primary table [[2, 24], [6, 58]];
  R1 = 0.8654; Fisher exact one-sided p = 0.7345 (two-sided 1.0);
  reversed arm R2 = 0.0; S-A equal to the primary; S-B not applicable;
  S-C NOT SUPPORTED (R1 = 0.8929, p = 0.7140) — the result is not
  grade-sensitive. See `outcome.md` and `reports/phase440_report.md`.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.*
