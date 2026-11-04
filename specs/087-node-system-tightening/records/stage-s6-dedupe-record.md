# Spec 087 — Stage S6 record (anchor-set dedupe, live DB, via API)

- Stage: S6 — anchor-set dedupe (tasks T601–T603)
- Branch: `feat/087-s6-dedupe`, base main `7131a43a`
- Date: 2026-11-03 (execution evening EST; evidence timestamps UTC as returned)
- Seat: execution worker (parent gates and merges)
- Claims answered: C087-12; the S6 leg of C087-14 (stage touched anchor sets only)

## 1. Execution summary

The live anchor-set population was deduplicated exactly as
decision D4 and claim C087-12 specify: through the API only,
exact duplicates only, earliest copy of each distinct content
kept, every removed id recorded here. No database file was
touched; no deletion path other than `DELETE /anchor-sets/{id}`
was used; no refusal occurred, so D4's stop-and-return fallback
was never invoked.

- Population read live through the API: **104** anchor sets
- Distinct (name, language, pairs-content) groups: **8**
- Removed as later exact duplicates: **96**
- Surviving sets: **8** (the 8 kept canonicals, §3)
- Distinct content before = after: 8 = 8 (identical set, §5)

Access note (infrastructure, stated plainly): this VM had been
replaced, so the Spec 080 tailnet forwarder unit was absent and
port 8001 refused connections. It was restored with the
standing post-replacement procedure
(`hidden_files/spec080-migration/install-forwarder.sh`, wave
probe CLEAR first), and backend identity was verified BY
PAYLOAD before any data was read: `GET /api/v1/health` through
the forwarder returned the DESKTOP payload
`{"status":"healthy","version":"0.1.0","component":
"glossa-lab-backend","build":"dev","auth":"token"}` with a
desktop uptime of ~5.6 h. All reads and deletions below went
to that backend, authenticated with the Spec 082 install token
(`Authorization: Bearer`, token value never recorded).

## 2. Grouping rule and population (T601)

All 104 sets were read through the API (list + per-set detail)
into a pre-deletion snapshot (§6). Each set's pairs content was
hashed canonically: each pair serialized as JSON with sorted
keys and compact separators, the pair strings sorted, joined
as a JSON array, CRLF→LF normalized, SHA-256 over UTF-8
(canonicalize-before-you-hash). Sets group by
**(name, language, canonical pairs-content hash)**; the kept
canonical is the earliest `created_at` in the group
(tie-break, unused in the event: smallest id). The population
fell into 13 creation waves; within each (name, language) all
13 copies carry ONE identical content hash, and descriptions
and corpus ids agree within every group — so the grouping is
exact under the rule's three elements and under every other
recorded field as well. Placeholder content that is distinct
survives by design (C087-12's stated bound): five of the eight
surviving contents are empty pair lists under distinct names.

Reference check before any deletion: all 104 ids were grepped
against the full repository working tree (7,340 files) and
against the Spec 087 audit's live-graph artifacts (27 graph
JSONs + censuses). **Zero references to any id.** No id was
stopped on reference grounds.

## 3. Groups: kept canonicals

| # | Name | Language | Pairs | Content SHA-256 | Kept id | Kept created_at (UTC) |
|---|------|----------|-------|-----------------|---------|-----------------------|
| 1 | Add Pairs | ugaritic | 1 | `45bb9faef7b1cffa7889923b3324217e7224fc78aee9aa2fca8cbfe2d1b3fce3` | `8db495856656` | 2026-10-05T16:13:46.913565+00:00 |
| 2 | Fuls 6 | ugaritic | 2 | `954c8c3e7462c0051a9c38edd068e919722f300530d65164636b3582b79f7151` | `5388a725e038` | 2026-10-05T16:13:46.867029+00:00 |
| 3 | Get By ID | ugaritic | 0 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `511c9cf6297f` | 2026-10-05T16:13:46.895479+00:00 |
| 4 | Listed | ugaritic | 0 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `f087d9af1884` | 2026-10-05T16:13:46.874743+00:00 |
| 5 | Minimal Set | (empty) | 0 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `ef2b303e3e6f` | 2026-10-05T16:13:46.767010+00:00 |
| 6 | New | ugaritic | 0 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `cab53975f7ea` | 2026-10-05T16:13:46.904683+00:00 |
| 7 | Set A | ugaritic | 0 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `7e0509beb7df` | 2026-10-05T16:13:46.886225+00:00 |
| 8 | Set B | ugaritic | 0 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `ba44a794693c` | 2026-10-05T16:13:46.889106+00:00 |

Pairs content of the non-empty groups (from the kept sets):

- **Add Pairs** (1 pairs): `[{"cipher": "X", "confidence": "low", "note": "", "target": "y"}]`
- **Fuls 6** (2 pairs): `[{"cipher": "004", "confidence": "high", "note": "Fuls verified", "target": "T"}, {"cipher": "066", "confidence": "high", "note": "Fuls verified", "target": "m"}]`

The other six groups' pairs lists are empty (`[]`, content hash
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`);
they are distinct groups because their names (and, for
'Minimal Set', the language) differ.

## 4. Removed ids (T602)

Every deletion: `DELETE /api/v1/anchor-sets/{id}` → HTTP 200
`{"deleted": true, "id": <id>}`, then verified absent by
`GET /api/v1/anchor-sets/{id}` → HTTP 404, per id, in plan
order. Per-id API responses are on file (§6). 96 of 96
completed; no refusal, no verification failure, no stop.

### Group: Add Pairs (language ugaritic) — kept `8db495856656`

| Removed id | Created_at (UTC) |
|------------|------------------|
| `2cdcb4383f9c` | 2026-10-05T18:30:59.486725+00:00 |
| `2f20ddf08954` | 2026-10-05T21:35:20.342039+00:00 |
| `f77fc948f118` | 2026-10-05T21:40:54.585648+00:00 |
| `8368d6bee323` | 2026-10-06T01:23:20.922193+00:00 |
| `da55b5927343` | 2026-10-06T10:11:29.590437+00:00 |
| `a3b916b25dca` | 2026-10-06T10:42:05.023088+00:00 |
| `146df6e5cb74` | 2026-10-06T11:42:09.413614+00:00 |
| `d5871e2b57db` | 2026-10-07T20:40:09.770646+00:00 |
| `ed10a5480327` | 2026-10-07T21:52:09.261905+00:00 |
| `98a796dca5e2` | 2026-10-08T21:04:55.482858+00:00 |
| `9a8c1018c22f` | 2026-10-08T21:24:22.434265+00:00 |
| `1c6a83bae131` | 2026-10-09T19:07:11.944671+00:00 |

### Group: Fuls 6 (language ugaritic) — kept `5388a725e038`

| Removed id | Created_at (UTC) |
|------------|------------------|
| `da76b58cccd2` | 2026-10-05T18:30:59.440546+00:00 |
| `c639e2b7df29` | 2026-10-05T21:35:20.208955+00:00 |
| `36251a5bf503` | 2026-10-05T21:40:54.503060+00:00 |
| `4a2da252215b` | 2026-10-06T01:23:20.886081+00:00 |
| `d1ba27376c7c` | 2026-10-06T10:11:29.522059+00:00 |
| `a0fea008370c` | 2026-10-06T10:42:04.976503+00:00 |
| `007ec74b04ab` | 2026-10-06T11:42:09.292469+00:00 |
| `3520fb1b016e` | 2026-10-07T20:40:09.698724+00:00 |
| `a52f20562d83` | 2026-10-07T21:52:09.052183+00:00 |
| `a968e138c208` | 2026-10-08T21:04:55.346160+00:00 |
| `627319bfe692` | 2026-10-08T21:24:22.042423+00:00 |
| `dfa973bb68cd` | 2026-10-09T19:07:11.886035+00:00 |

### Group: Get By ID (language ugaritic) — kept `511c9cf6297f`

| Removed id | Created_at (UTC) |
|------------|------------------|
| `12a6a109db37` | 2026-10-05T18:30:59.468040+00:00 |
| `1595b87e42e2` | 2026-10-05T21:35:20.290079+00:00 |
| `efad40039f95` | 2026-10-05T21:40:54.545427+00:00 |
| `3199fb752728` | 2026-10-06T01:23:20.905648+00:00 |
| `dcda48f1915e` | 2026-10-06T10:11:29.555505+00:00 |
| `fa6972c9aaeb` | 2026-10-06T10:42:05.003371+00:00 |
| `ba8072d8bf0b` | 2026-10-06T11:42:09.385136+00:00 |
| `c1f55004a20c` | 2026-10-07T20:40:09.742550+00:00 |
| `543f95474711` | 2026-10-07T21:52:09.232189+00:00 |
| `493fd45f5afd` | 2026-10-08T21:04:55.416819+00:00 |
| `1856fefa6339` | 2026-10-08T21:24:22.271652+00:00 |
| `2de0b15a92f7` | 2026-10-09T19:07:11.915274+00:00 |

### Group: Listed (language ugaritic) — kept `f087d9af1884`

| Removed id | Created_at (UTC) |
|------------|------------------|
| `e96eb6d65abe` | 2026-10-05T18:30:59.446494+00:00 |
| `651567fc1f79` | 2026-10-05T21:35:20.228016+00:00 |
| `4ca18ae7f786` | 2026-10-05T21:40:54.513333+00:00 |
| `b2ad41ec8752` | 2026-10-06T01:23:20.890372+00:00 |
| `53a04dcc45f9` | 2026-10-06T10:11:29.528717+00:00 |
| `83155e1d0df7` | 2026-10-06T10:42:04.984148+00:00 |
| `f189b7c70a15` | 2026-10-06T11:42:09.316000+00:00 |
| `c09d6c5a64bd` | 2026-10-07T20:40:09.708983+00:00 |
| `823a21380a90` | 2026-10-07T21:52:09.105676+00:00 |
| `b9eeff84966e` | 2026-10-08T21:04:55.357731+00:00 |
| `354a27786b39` | 2026-10-08T21:24:22.089211+00:00 |
| `f9f3c3fc86eb` | 2026-10-09T19:07:11.895751+00:00 |

### Group: Minimal Set (language (empty)) — kept `ef2b303e3e6f`

| Removed id | Created_at (UTC) |
|------------|------------------|
| `328405437975` | 2026-10-05T18:30:59.367143+00:00 |
| `f44a4adf1197` | 2026-10-05T21:35:19.990641+00:00 |
| `fd45e1d9e56b` | 2026-10-05T21:40:54.349319+00:00 |
| `412cb05fe1f5` | 2026-10-06T01:23:20.814737+00:00 |
| `a2f28cd55573` | 2026-10-06T10:11:29.438115+00:00 |
| `45a4b982e46f` | 2026-10-06T10:42:04.893332+00:00 |
| `9d25974b5fbb` | 2026-10-06T11:42:09.129215+00:00 |
| `c8824bc02f06` | 2026-10-07T20:40:09.615922+00:00 |
| `10bfd96fb276` | 2026-10-07T21:52:08.458206+00:00 |
| `aba0b9ff30c4` | 2026-10-08T21:04:54.997343+00:00 |
| `47c5caeab1cd` | 2026-10-08T21:24:21.273036+00:00 |
| `25bb579d5420` | 2026-10-09T19:07:11.759560+00:00 |

### Group: New (language ugaritic) — kept `cab53975f7ea`

| Removed id | Created_at (UTC) |
|------------|------------------|
| `35b5c09eac4d` | 2026-10-05T18:30:59.479763+00:00 |
| `0991562c153e` | 2026-10-05T21:35:20.324206+00:00 |
| `4820efe0913e` | 2026-10-05T21:40:54.566672+00:00 |
| `c38a5c51258c` | 2026-10-06T01:23:20.915230+00:00 |
| `d464df67fa51` | 2026-10-06T10:11:29.572805+00:00 |
| `7d3aa6d6f139` | 2026-10-06T10:42:05.012138+00:00 |
| `b045c550e5de` | 2026-10-06T11:42:09.402069+00:00 |
| `f1c6b8b81086` | 2026-10-07T20:40:09.755963+00:00 |
| `8c8ce5d381fa` | 2026-10-07T21:52:09.251795+00:00 |
| `558a6e6a6f5d` | 2026-10-08T21:04:55.451942+00:00 |
| `caf157e7fbb1` | 2026-10-08T21:24:22.381824+00:00 |
| `cf3dacea0c92` | 2026-10-09T19:07:11.928902+00:00 |

### Group: Set A (language ugaritic) — kept `7e0509beb7df`

| Removed id | Created_at (UTC) |
|------------|------------------|
| `7297b4b55c58` | 2026-10-05T18:30:59.453465+00:00 |
| `8f75d17b157b` | 2026-10-05T21:35:20.258882+00:00 |
| `d835de656e8d` | 2026-10-05T21:40:54.524574+00:00 |
| `93bc127a263c` | 2026-10-06T01:23:20.897250+00:00 |
| `6bed0a36638f` | 2026-10-06T10:11:29.538079+00:00 |
| `dbcdb43d100b` | 2026-10-06T10:42:04.991776+00:00 |
| `bed31674155c` | 2026-10-06T11:42:09.357456+00:00 |
| `ef480f7f3f40` | 2026-10-07T20:40:09.723403+00:00 |
| `d44e340551b5` | 2026-10-07T21:52:09.171165+00:00 |
| `20fd9ecb2620` | 2026-10-08T21:04:55.375955+00:00 |
| `3a1b5a1648a6` | 2026-10-08T21:24:22.179065+00:00 |
| `7a03f953fb7a` | 2026-10-09T19:07:11.902990+00:00 |

### Group: Set B (language ugaritic) — kept `ba44a794693c`

| Removed id | Created_at (UTC) |
|------------|------------------|
| `7f6e9cfcd598` | 2026-10-05T18:30:59.457194+00:00 |
| `fe87ffc2e68c` | 2026-10-05T21:35:20.268471+00:00 |
| `249f6edd8e95` | 2026-10-05T21:40:54.530684+00:00 |
| `f6fa3190e05d` | 2026-10-06T01:23:20.899756+00:00 |
| `e509b716dd4c` | 2026-10-06T10:11:29.546206+00:00 |
| `13698a9ed95d` | 2026-10-06T10:42:04.995519+00:00 |
| `cf2c0cdfbb47` | 2026-10-06T11:42:09.369957+00:00 |
| `f0e302efe24f` | 2026-10-07T20:40:09.730769+00:00 |
| `1814b00ebd10` | 2026-10-07T21:52:09.201937+00:00 |
| `fefbde2f157c` | 2026-10-08T21:04:55.392581+00:00 |
| `ffd223719c58` | 2026-10-08T21:24:22.211139+00:00 |
| `fb245e315473` | 2026-10-09T19:07:11.907399+00:00 |

## 5. Post-pass verification (T603)

A post-deletion snapshot was read the same way (list + detail)
and reconciled against the plan and the pre-snapshot:

- Total: 104 → **8**; reduction **96**, exactly the recorded removals.
- Post population id set == kept id set, exactly (no extras, no losses).
- Every kept set present with canonical content hash identical
  to its pre-deletion value and to the plan; name, language,
  description, corpus_id and created_at all unchanged.
- Every removed id absent from the post population (and each
  was individually verified 404 immediately after its DELETE).
- Distinct (name, language, content) set: 8 before, 8 after, identical.
- Delete-results file ids == plan removed ids, set-equal; all
  96 DELETE bodies `{"deleted": true}` with HTTP 200, all
  verification GETs 404.

Foundation check re-run (T603), through the MCP tools against
the same live backend, reported exactly as returned. Before
the re-run, `get_foundation_status` reported the on-disk
report of 2026-10-26: verdict READY WITH CAVEATS, 39 ok /
0 fail / 9 warn (source `on_disk_report`). `run_foundation_check`
was then executed; `get_foundation_status` afterwards:
verdict **PASS**, 17 ok / 0 fail / 0 warn, last_checked_at
2026-11-04T02:36:02Z, source `research_api`, running false,
dirty false. The two reads are different surfaces (an October
on-disk report vs a fresh research-API run with its own check
population); this record states both and does not equate their
counts. The T603 fact: after the dedupe, a fresh foundation
check completes with zero failures.

## 6. Evidence files (goal workspace, `hidden_files/system-coupling-2026-11-02/`)

- `s6-anchor-sets-presnapshot.json` — all 104 sets in full, read before any deletion. SHA-256 `5311cbaf101fba6cf59cab0f4c65fe0b11caaf5e2779f44423d416f7835a0b54` (34,161 bytes). This is the restore record: any removed set can be re-created from it through the API.
- `s6-dedupe-plan.json` — the grouping: kept + removed ids per group with content hashes, computed and saved before any deletion. SHA-256 `2fcff7162e12c5ec09f013d278777e392c433d199623b1759af0411ec1d59837`.
- `s6-delete-results.json` — per-id DELETE responses + verification results (96 entries). SHA-256 `7516cc7a9ee8d0fd6d1e251f135a2cacc954a4055ae0f3a06cc3e83d2cd4709f`. The worker's streaming per-id log (intent + result lines, fsynced) is retained with the execution scratch.
- `s6-anchor-sets-postsnapshot.json` — the surviving 8 sets in full. SHA-256 `d7dd3281ce7f706c1a13af273fbc24d6cd62f125124ab0848e333b8acd07efab`.

## 7. Claim assessment

- **C087-12 — SUPPORTED AS SPECIFIED.** Stage S6 deleted an
  anchor set only when another set with identical (name,
  language, pairs content) was kept (§2–§3); the earliest
  canonical copy of each distinct content survives (§3, §5);
  every deletion went through `DELETE /anchor-sets/{id}`
  (§4, per-id responses on file); every removed id, with its
  group's kept id, is recorded here (§4). None of the
  falsifiers is met: no deleted set differs from its kept
  set in any rule element (hashes, §3); no distinct content
  lacks a surviving copy (§5); no deletion was performed by
  direct database write (API only, §1/§4); no removed id is
  absent from this record (§4).
- **C087-14 (S6 leg) — SUPPORTED AS SPECIFIED.** This stage
  touched anchor sets only: no claim status, stage or score,
  no ledger content, and no frozen record was read for
  modification or written. Its evidence is the execution
  surface itself: the only mutating calls issued were the 96
  DELETEs of §4 (plus the T603 foundation check re-run, a
  read-computation the task itself orders).

## 8. Departures and notes

1. **Forwarder restore preceded execution** (§1): the VM
   replacement had removed the Spec 080 forwarder unit; it
   was reinstalled by the standing procedure and identity-
   verified by payload before use. No data path was improvised.
2. **The parent session's first full clone of the repo did
   not survive the VM replacement** (its directory vanished
   mid-transfer; the transfer process is gone and no result
   was ever delivered from it). The reference check and this
   record PR instead used a fresh shallow clone
   (`s6-clone2`, depth 1, main tip `7131a43a` verified against
   the PR #500 merge). Kept per instructions.
3. **Tasks pointer vs this file's name:** tasks.md's S6 header
   names the record PR `records/087-s6-stage-record`; this
   record follows the stage-record naming of S1/S2/S4
   (`records/stage-s6-dedupe-record.md`) per the executing
   brief. The tasks.md tick notes point here.
4. **T601's acceptance is human-as-oracle** (the group list is
   reviewed before execution). The grouping was computed and
   saved to the plan file before any deletion (§2, §6) and
   the deletions executed exactly that plan; the oracle read
   itself belongs to the parent's gate of this PR, where the
   full group list is on the record (§3–§4).
5. Nothing was deleted from the VM or the desktop in this
   stage beyond the 96 API deletions: cleanup determination —
   the shallow clone (kept, per instructions) and /tmp
   scratch (ephemeral) are the only creations.

