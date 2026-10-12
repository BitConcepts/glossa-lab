# Spec 029 — Phase D Run Record: OD-1 Re-staging Migration

> One dated reclassification event, executed 2026-10-12
> with `migrate_phase_d_restaging.py` from branch
> `impl/029-phase-d-restaging` (base main `028d416c`).
> Script, D1 inventory, representation decisions, and
> the D3 dry-run record: `phase-d-record.md`.

## Inputs

- Frozen ledger:
  `specs/029-tao-claim-lifecycle/reclassification-ledger.json`
  — SHA-256
  `e53a037e71439401f4114100b32495ff98adb58f8529fe83dfedde3b94d22b90`
  (asserted by the script against `freeze.json` at every
  run), 345 entries: 336 staged + 9 grouped/non-record.
- Stage stamped per record: the ledger entry's
  `honest_stage`; `stage_source` =
  `specs/029-tao-claim-lifecycle/reclassification-ledger.json:<item_id>`;
  `stage_as_of` = `2026-10-12`; one initial
  `stage_history` entry (actor
  `spec029-phase-d-restaging-migration`, timestamp
  `2026-10-12`, evidence ref = the ledger entry, reason
  citing OD-1 + the entry); `verified_unexplained` =
  `true` exactly for the ledger entries flagged
  `verified_unexplained`.

## Pre-run snapshots

Taken by the live run, before any write, to
`~/workspace/glossa-wt-029D-snapshots/phase-d-pre-run-2026-10-12/`
(mirroring repo paths; outside the repo, not committed —
the identical pre-run bytes are also the base commit
`028d416c` state of every file below). The sidecar
`specs/029-tao-claim-lifecycle/phase-d-stamped-records.json`
did not exist before the run (recorded in the snapshot
manifest).

## Before / after SHA-256 per touched store

| Store | Before | After |
|---|---|---|
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed` | `18e6f4b2caa7bc9ae1f5cc92dd96f95ce191a77c56144b95820a368d75a316d6` |
| `glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json` | `82ee15c0e70f7b6fdc4e29364990bb5955f2a27c7606292c9315bdf7a45c72e8` | `5e00dae1464a34f46f6597818db3455fc02934bda96a23cc7a6b187e169f816c` |
| `glossa-indus/claims/extracted_claims/farmer_sproat_witzel_2004.json` | `7744f2d36df56999a806457508c443814dee293dc461a00637c13faec68eb3d2` | `4779b7b5ee22f39851def2afcea28b6de23b073829430b29950a373b92b9770e` |
| `glossa-indus/claims/extracted_claims/fuls2023_catalog_of_indussigns_searchins_1dbdecdb.json` | `d560e3055b0dd3bb34bb426d8111ea34e58f8d84705b1699392c7e4cfa62c4b5` | `d4e533ef6a6dc2b048021202c0f025a91432d0b7eb6a0fa7994e3fe0b2cdabf2` |
| `glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json` | `dc413459a2b169031af6a0ade042fbfc64be3454c217a1d14e736ab448d8f548` | `0d7bb8710573a29ecb7edbb71d42e2b99da72a4ea330e5ca5a60294b057fdccc` |
| `glossa-indus/claims/extracted_claims/parpola_2010_dravidian_solution.json` | `30affafb32c4241e977cdc46a52d9d936eec756923121a86ce8b30a4bce1a1e5` | `ef0b07dd8df97b8c40c14c0972bb1826ac9c40e59dad75cca1d357ea748a746d` |
| `glossa-indus/claims/extracted_claims/positional_analysis_of_indus_signs_a2bedc93.json` | `16a09ffed1f93538e86db7aa8333ce1ed2df6b3c3e65819411c89547de4b90aa` | `9a48853d1d25e0ac232eccd8cdb06c63db26021aac4260fb28464deedba67fa9` |
| `glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json` | `08c1c87d1f7896ccc3739f2b62f33e7b1019d50e8327fb3f05da62ab0754acb6` | `8a3475b784007a5e7429af9c1feb8c569f0eaf313eda51dbfff191d52585f24f` |
| `glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json` | `aa4ed458879f891353311029ee6dfcf432d8ceba5ba63e2403c841b4e83b7da2` | `1bd02f83d4562922796ca3c3dc99896778e9947cbca690e9b7b180d91dc18f04` |
| `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json` | `2b8cd5377e1e6016096d3995a49ffdef7e1bc2f3c6e2e6c5cf6c81511d443bd4` | `3a7b9f2861ac7c88cb5bdaf4fba4ec4b9b3884215699cb871127fa850123715d` |
| `glossa-indus/claims/extracted_claims/yadav_2010_ngrams.json` | `6ad9d1839296316884dccafe82aa6fd65713e2b88d5b47f0480c6828a2866dc0` | `6e3375c34a47f050628c29d7e2286e44da80045b23cc8480f52642f6f57947bf` |
| `glossa-indus/hypotheses/models/hunt_civic_ritual.yaml` | `8d296dd46b0a8c8052ab9edb7486acbf5b51da5f6c6f46ebc5386dfc93c8c93a` | `89729db2a4dda1cda1bac751b16325fcfc119f7cf4b8b9138a315acc0e986da3` |
| `glossa-indus/hypotheses/models/parpola_proto_dravidian.yaml` | `5cb6c2cb7de45328a57549fb94a0b54091135b1ca0b19ef522acc99a9e305137` | `4e26d5101efebad921d5d61a0d11656be54fc0e4aa0373e1624132e831a0c982` |
| `glossa-indus/hypotheses/models/roif_guild_ledger.yaml` | `42b4d87917893dc450752009252191b2afb51ca38a37350f73848f7498730f20` | `c5f08461cc1a37b91cb5a17981e2e4d7c02958312e1e7b6b9a49618a154c9586` |
| `specs/029-tao-claim-lifecycle/phase-d-stamped-records.json` (sidecar, new) | — (absent) | `6b23da7e8e1bf400af263eaacc2ed72eb5186d110aa072e9d83195f50123f698` |

Untouched by the run (verified by `git status` — no
other store changed): `docs/PREDICTION_REGISTER.md`
(SHA-256
`3fb5eff1df6c4b8844bbcb8c769a8739b296c962a825557b3b1a6fe0fce75dc1`,
unchanged), the per-spec outcome records, the anchors
backups, and every digest-covered file under
`specs/029-tao-claim-lifecycle/`.

## Additive-only assertion

**Held.** Asserted inside the run, before each write:
for the anchors file and every extracted-claims file,
removing exactly the five additive keys (`stage`,
`stage_source`, `stage_as_of`, `stage_history`,
`verified_unexplained`) from the post-stamp records and
re-serializing canonically reproduces the pre-run file
bytes exactly; for each hypothesis YAML, the post-run
bytes have the pre-run bytes as a strict prefix (the
stamp is one appended top-level block; the two
parseable files still parse, with their pre-existing
keys unchanged). In the line diff, the only modified
pre-existing lines are each stamped JSON record's
former last-field line, which gains a trailing comma —
no pre-existing value changes anywhere.

## Reconciliation (from the live stores, post-run)

The live run re-read every store after writing and
reconciled via `--verify` semantics; a separate
`--verify` invocation after the run returned the same
result, as did the idempotency checks below:

| Class | Post-run (live stores) | Ledger §3 |
|---|---|---|
| anchors | 193 created / 94 checked | 193 / 94 |
| extracted claims | 21 created / 10 checked | 21 / 10 |
| PRED-2026 live (sidecar) | 3 created / 2 checked | 3 / 2 |
| hypothesis models | 3 created | 3 |
| study headlines (sidecar) | 10 checked | 10 |
| **Totals** | **220 created / 116 checked / 0 explained / 0 accepted / 0 digested** | **220 / 116 / 0 / 0 / 0** |
| `verified_unexplained` flags | **105** | **105** |
| grouped / non-record entries | 9 (unstamped, by design) | 9 |

Every stamped record (336) carries `stage_source` and
`stage_as_of` — checked per record during reconciliation
(a missing or mismatched value raises, and none did).

## Idempotency

A second `--live` run after the first reported
`no-op: every record already carries this migration's
stamp; nothing written` and wrote nothing; a post-live
`--dry-run` reported the population as 336 stamped with
the reconciliation still matched.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
