# Stage 0 record — live store inventory and the carried probe verdict (2026-11-13)

**Scope:** tasks.md Stage 0 runs T010–T011, executed on
branch `spec/094-stage0-inventory` from main `4d08788f`
(the T004 intake merge). This record is Stage 0's acceptance
artifact (plan.md: "Gate — the record itself: inventory
counts and the probe verdict stated from reads, not
inference"). **Claims discharged: none** — Stage 0 grounds
C094-12's inventory clause and D-094-5's gate; the claims
discharge at their build stages. Every count below was read
on 2026-11-13 between ~17:16 and ~17:20 EST from the stores
themselves: the live stores read-only on the mini-server
(`/home/tpierson/glossa-lab`, via `ms-ssh`; no write, no
restart, no loop start/stop, no acceptance action of any
kind), the repo copies read from a fresh clone at `4d08788f`,
and the live loop state through the MCP read tools (§5).
Nothing live was written at any point in this stage.

## 1. The three stores — live vs repo

| Store | Live (mini-server) | Repo (main `4d08788f`) | Relation |
|---|---|---|---|
| `outputs/anchor_staging.json` | 2 B · sha256 `4f53cda1…` · **0 items** | 17,143 B · sha256 `42456ef9…` · **52 items** | **DIVERGENT** (§3) |
| `outputs/anchor_staging_archive.json` | 555,415 B · sha256 `c719c60e…` · **1,107 entries** | 525,391 B · sha256 `5450df76…` · **1,047 entries** | **DIVERGENT** (§4) |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | 570,344 B · sha256 `df0cf620…` · **287 anchors** | 570,344 B · sha256 `df0cf620…` · **287 anchors** | **IDENTICAL**, byte for byte |

Provenance of the live copies, read the same hour: the
mini-server checkout stands at `a165746c` (2026-11-11, PR
#557), and its working tree carries the staging and archive
files as locally modified against that HEAD; the anchors
file is unmodified. Two consequences are stated plainly
because later stages depend on them. First, the live
archive's 60 entries beyond the repo copy (§4) exist **only**
in that working tree — they were never committed anywhere —
so any future refresh of the mini-server checkout must
preserve the working-tree stores or those entries are lost.
Second, the live backend reads the live files, not the repo
copies: where the two diverge, the live file is the operative
store and the repo copy is the last committed state.

## 2. Anchors census (live file; the repo copy is identical)

- **287 anchors**, and the file's own `total` field agrees
  (287). Stored `corpus_token_coverage`: 0.921879.
- **By confidence:** HIGH 166 · MEDIUM 5 · LOW 3 ·
  CANDIDATE 113. The LOW/CANDIDATE class — the class the
  2026-11-13 test found overwriteable at promotion (defect
  4, closed in the bug lane by PR #565) — is **116 of 287**.
- **By name form:** 286 keys are M-prefixed (`M\d+`); none is
  a bare digit string; the single remaining key is `H003`.

## 3. Staging

- **Live: 0 items.** The file is an empty JSON list (2 bytes;
  its sha256 is the hash of `[]`).
- **Repo: 52 items, every one `review_status` = `staged`.**
  The staged-candidate schema on those records is 10 keys
  (`sign`, `proposed_reading`, `evidence_type`,
  `evidence_score`, `dedr_support`, `neighbor_count`,
  `neighbor_reading`, `conflict`, `review_status`,
  `source_experiment`). **Falsifier: 0 of 52 carry one** —
  there is no `falsifier` key in the schema. Evidence refs:
  **0 of 52** carry an `evidence_ref`.

The divergence is the re-stand-up's shape, stated as read:
the restored live backend's working staging was emptied,
while the committed repo copy still carries 52 pre-gate
staged candidates the live backend does not hold. Those 52
are pre-gate stock in C094-12's posture: should any later
stage load them into the live store, they enter as records
lacking the Stage 1 fields — unapprovable until they carry
them, per plan.md Stage 1's legacy rule. Nothing in this
stage moves, loads, or re-adjudicates them.

## 4. Archive census — the stock D-094-6 prices

Entries by `review_status`, the records' own field:

| Status | Live (1,107) | Repo (1,047) |
|---|---|---|
| `verified` | 1,025 | 965 |
| `approved` | 58 | 58 |
| `promoted` | 24 | 24 |

**The divergence, exactly.** Comparing per sign × status,
the live archive dominates the repo archive everywhere: no
sign is missing on either side, no sign × status cell is
smaller live than in the repo, and the entire difference is
**+60 `verified` entries on 8 signs already present** —
M101 +9, M197 +9, M214 +9, M250 +3, M312 +9, M324 +3,
M378 +9, M406 +9. (This is a sign × status granularity
comparison; an entry-identity multiset comparison was not
performed and is not claimed.)

**The eligible pool** (the pre-gate promotion filter in
`promote_to_anchors` — `review_status` in {approved,
verified}, read at `25bcbe9a`): live **1,083 entries**
(58 approved + 1,025 verified); repo 1,023 (58 + 965).
Deduplicated per sign as the endpoint deduplicates
(verified beats approved, then higher `evidence_score`
wins): **108 distinct signs on both sides**. Of those 108,
**4 already sit at HIGH/MEDIUM** in the anchors file —
M042, M046, M108, M222 — and promotion skips those by rule.
**The endpoint's own promotable pool is therefore 104
distinct signs, identical on the live and repo copies**;
the +60 live entries duplicate signs already in the pool
and do not enlarge it.

**Evidence and falsifier census, verified not assumed.**
The archive schema is 17 keys (`sign`, `proposed_reading`,
`evidence_type`, `evidence_score`, `dedr_support`,
`neighbor_count`, `neighbor_reading`, `partner_reading`,
`conflict`, `review_status`, `source_experiment`,
`approved_at`, `verified_at`, `promoted_at`, `archived_at`,
`archived_reason`, `sa_delta`). **`evidence_ref` is not
among them: 0 of 1,107 live entries (0 of 1,047 repo
entries) carry a recorded evidence reference.** The
evidence-adjacent fields every entry does carry —
`evidence_type`, `evidence_score`, `dedr_support` — are not
what the H26 gate reads. **Falsifier: 0 entries carry a
`falsifier` key, at any status, on either side** — the key
does not exist in the schema, as the spec's grounding
expected and this census confirms from the records.

**What the 104 could do under the pre-gate rules.** Read
against `promote_to_anchors` as it stood at `25bcbe9a`: a
promotion call supplying no request refs would promote
**0 of the 104** — every best-per-sign entry falls to
`blocked_no_evidence`, because none carries a recorded ref
that resolves (there are no recorded refs at all). The pool
was reachable only through request-supplied `evidence_refs`
— defect 2's hole, demonstrated end-to-end by probe (b) and
closed in the bug lane by PR #565. **The re-evidencing
backlog D-094-6 prices is therefore 104 distinct signs
(1,083 live eligible entries): every one of them keeps its
recorded status as history, none is deleted, demoted, or
re-adjudicated, and none can promote until re-evidenced onto
the new record fields.** The 24 `promoted` entries are
history, not backlog: their signs all stand in the current
anchors file (24 of 24, read against the repo copy; the live
anchors file is byte-identical, so the reading carries).

## 5. Live loop state (C094-13's bar, observed intact)

The first MCP attempt returned connection-refused on two of
three calls (the staging call returned its shape error,
below). The VM tailnet forwarder was restored with the
standing forwarder-mini installer and the backend verified
**by identity** before retrying — the six-key health payload
`{status: healthy, version: 0.1.0, uptime_seconds:
175688 → 175690 across two reads, component:
glossa-lab-backend, build: dev, auth: token}`. On retry:

- `get_research_loop_status`: `running: false`,
  `cycles_completed: 0`, `total_papers: 0`,
  `total_insights: 0`, `n_candidates: 0`, `history: []`.
- `get_research_loop_results`: protocol
  `integrated_research_loop_v3`, `cycles_run: 0`,
  `candidate_counts: {total: 0, staged: 0, blocked: 0}`,
  `anchor_candidates: []`, `history: []`.
- `get_anchor_staging`: `{"error": "'list' object has no
  attribute 'get'", "type": "AttributeError"}` — the known
  tool-shape defect against the live list-shaped staging
  file, reproduced verbatim and carried in the bug lane;
  the staging census in §3 was read from the file instead,
  per this record's method.

The loop is off and has run 0 cycles on the live backend.
C094-13's bar is intact, and nothing in this stage tested
it: no start or stop call was made.

## 6. Probe verdict carried (T011)

The claim-record storage-edit probe's observed verdict
(parent supplement, 2026-11-13; ratification record, carried
verbatim there; method and counts in the grounding record
§5; full record `~/workspace/glossa-run/loop-test-2026-11-13/
REPORT.md` with its supplement): a bare storage edit
flipping one ledger claim from stage `created` to `digested`
(no `stage_history`, no named human, no evidence) is
**DETECTED by the ledger gate — full mode 18 PASS / 10 FAIL
/ 2 NOT-RUN against the standing 29 / 0 / 1; `--regen` mode
18 PASS / 13 FAIL / 1 NOT-RUN — but every failure is a
cross-store consistency check** (ledger vs the independently
recomputed matrix, map, and settling artifacts). **No check
validates the transition itself.** That verdict is entered
here as C094-10's grounding, per T011: for the claims ledger
the protection is post-hoc divergence detection, and the
anchor path has no equivalent recomputation net at all.
The probe was **not** re-run in this stage — there is no
built shape to re-run it against. Its re-run is registered
as Stage 4's exit evidence (tasks.md T403; D-094-5 as
adjusted).

## 7. Stage 0 exit

Stage 0's conditions, per plan.md and D-094-5 as adjusted —
the live store inventory (§§1–5, read from the stores at a
named time) plus the probe verdict of record with its re-run
staged (§6) — are **met on this record, and Stage 0 is
complete**. The forward obligations this stage creates, and
the only ones: (i) the storage-edit probe's re-run against
the built shape stands as Stage 4's exit gate (T403);
(ii) D-094-6's suspension binds the 104-sign backlog of §4
until each sign is re-evidenced onto the new record fields;
(iii) Stage 1 inherits the staging posture of §3 (live store
empty; 52 pre-gate candidates in the repo copy only).
Claims discharged by this stage: **none**, by the plan's own
statement.

*This does not establish:* anything about the inventoried
entries' soundness — they were counted and classified by
their own recorded fields, not examined (T010's own cap);
that the live archive contains the repo archive entry for
entry — the domination of §4 is proven at sign × status
granularity, not entry identity; that the loop remains off
after the read time in §5 — the bar is C094-13's standing
rule, and this record observes it intact at a named time
rather than guaranteeing it forward; or that any claim
C094-1..13 stands discharged — the build stages discharge
them, each on its own evidence.
