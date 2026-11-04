# Spec 088 — Stage S5 record (gap scans, three clusters)

Executed 2026-11-04 on branch `feat/088-s5-scans` off
origin/main `893a426a` (the PR #508 S4 merge; main had
not advanced). Tasks T501–T504. All counts below are
from the scan records' own mechanical pass, the
artifacts' coverage blocks, or the records cited —
read first-hand this session. The stage wrote no code
and touched no generated artifact; its outputs are the
three scan records and these ticks.

## What landed

- **T501** — `records/scan-corpus-anchors.md`
  (Cluster A: Domains 1 + 2).
- **T502** — `records/scan-families-contact.md`
  (Cluster B: Domains 3 + 4).
- **T503** — `records/scan-infra-bookkeeping.md`
  (Cluster C: Domain 5 + cross-cutting bookkeeping).
- **T504** — the consolidation check (below).

## Consolidated counts (per cluster, per kind — from the records)

| Cluster | Missing node | Missing edge | Thin evidence | Stale bookkeeping | Finds | Candidates |
|---|---|---|---|---|---|---|
| A — corpus + anchors | 2 | 3 | 5 | 2 | 12 | 14 |
| B — families + contact | 3 | 3 | 3 | 3 | 12 | 12 |
| C — infra + bookkeeping | 2 | 2 | 0 | 7 | 11 | 11 |
| **Total** | **7** | **8** | **8** | **12** | **35** | **37** |

Candidates exceed finds only in Cluster A, where A-06
carries three candidates (one per revalidation route
the audit's own fields define: 28 Phase-48 promotions
/ 5 single-line / 4 sole crosswalk-literature imports).

## T504 mechanical pass (output, quoted)

The pass (a script run over the three records + the
find list, this stage) reports:

- 35 finds; every find carries exactly one `Kind:`
  line, and every kind is one of the four registered
  kinds — no fifth kind anywhere (per-cluster kind
  counts as the table above).
- Every candidate carries both a falsifier line and
  an honesty-rule type line; the counts are equal per
  cluster (A 14/14, B 12/12, C 11/11; total 37/37).
- Find-list consumption: all 28 `bundle_less_study`
  subjects are named in a scan record (A consumes 20:
  Domain 2's 13 + Domain 1's 7; B consumes 2: `024`,
  `013`; C consumes 6: Domain 5's six); all 9
  `extracted_null_falsifier` claims' source documents
  are covered by B-05; the 1 `restricted_node` item
  (`072-fish-family-profiles-redesign`) is explicitly
  carried to S6 — the restriction is a standing owner
  order, by design, not a gap, and T504's terms allow
  the explicit carry; 0 `judgment_call` items exist
  to consume (the live population is empty, per the
  S2 record). Total: 37 consumed + 1 carried = the
  find list's 38.

## Verifications executed this stage (not carried)

- **WP5 census verified against its record** (the
  brief's "verify, do not copy blindly" instruction):
  `docs/repair-2026-10-26/anchor-support-audit.json`
  summary_counts read directly — 94 strict: 6
  supported_independent / 46 supported_internal_only
  / 37 requires_revalidation / 3
  expert_adjudication_pending (M222, M362, M398) / 2
  insufficient_evidence (M367, M048). The audit's
  per-record fields additionally give: 94/94 records
  with no falsifier recorded and no distinguishing
  observation recorded (A-09); 52 records with no
  ledger passage in trail (A-10).
- **WP4 verified against its record:** the repair
  README's provenance result — 0 of 184 eligible, 116
  entries carrying project readings under a "Parpola
  1994" label (B-01).
- **Matrix facts recounted from the current
  artifact** (post-adoption regeneration, not the
  Spec 086-era numbers): cells by class anchors 0 /
  research_checks 0 / studies 7 / documents 1,392;
  unused study columns 6 of 10; empty rows 14;
  dependency pairs not cells **793** (was 790 at Spec
  086 Stage 5; +3 from the C088 intake's own pairs);
  `sign_refs` occurrences in the artifact: 1 (C-05);
  sign_refs_without_anchor_record: the same 3
  (mahadevan:64/70/72, C-06).
- **GAP-C12's rule verified in the current tree:**
  `experiment_graph_phase20.py` line 462 (the rule),
  line 474 (`critical_per_dof` 3.84) (C-02).
- **Desktop-sync precision (C-08):** `309ea63c` is PR
  #472's merge commit (GitHub PR record) and main's
  descendant-compare read this scan shows main
  (`893a426a`) ahead_by 118 / behind_by 0 — the commit
  is in main's history; the stale surface is the
  desktop **checkout**, per the repo LEDGER's T020
  settle record and adoption §4. (A local shallow
  clone's initial object check suggested the commit
  was absent from origin; the GitHub compare disproved
  that reading, and the scan records the compare.)
- **Laursen absence counted, not assumed (B-10):**
  `claims.jsonl` contains zero entries mentioning
  laursen, gulf, dilmun, janabiyah, or arabia
  (full-text count over the ledger, this scan).
- **Spec tree verified:** 89 directories; no `049-*`,
  no `085-*` (C-10).

## The ledger did not move (C088-15)

`glossa-indus/ledger/claims.jsonl` SHA-256 before the
stage's work and after its completion, identical:
`9f8144c3fa73d7cfa4ffd02d3b6c23c3ea9e0c1e164e9497232dd2842e0a022c`
(907 lines; the raw `sha256sum` equals the canonical
hash — the file is LF-clean). No stage-5 act writes to
the ledger; no claim's status, stage, or score changed
anywhere. The generated artifacts are likewise
untouched (their hashes stand as the S4 record states
them; the gate below recomputes them).

## Gate, both modes (run before and after the stage's writing; identical)

```
full:    summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

The working tree at commit time carries only the
intended paths (tasks.md ticks; the three scan
records; this record) — no in-tree regeneration
residue to restore.

## Departures, stated plainly

(a) **Branch shape.** The plan stages S5 as three PRs
(`feat/088-s5a/s5b/s5c`); the executing brief for this
stage directed one branch (`feat/088-s5-scans`) and
one PR, and the brief governs. The three records are
separately complete and separately countable, so the
consolidation loses nothing by landing together.

(b) **The scan plan's WP2 gloss.** The plan's Cluster
B text names "the five template families" for WP2's
linguist certification; no record this scan could
read carries that phrase — the repair record states
the leg as a linguist-reviewed rule set (baseline
§2.4). B-02 cites the record's own statement and does
not repeat the gloss.

(c) **The Holdat block is cited, not re-derived
(A-12).** The adoption record names the Holdat CSV as
a WP3 blocker; the repo also contains Holdat-adjacent
data files (an M77 test fixture, holdatllc extracts),
and this scan did not establish which artifact the
block refers to. A-12 records the block on the
adoption record's authority and says so on its face;
its falsifier is designed to settle the question
empirically.

(d) **Cluster C records no thin-evidence find.** The
count is 0, stated rather than padded: Domain 5's
gaps on the named source lists are enforcement and
bookkeeping, and no source-list record counts the
governance claims' support as thin.

(e) **Two counts moved since their source records,
and are stated as counted today:** dependency pairs
793 (not 790) and the two-graph-worlds join at 1 of
876 (not 1 of 840). Both movements are the T004
adoption intake's arithmetic, not drift.

## Carried to S6 (explicit, per T504)

- The `restricted_node` find for Spec 072 (owner
  restriction by design; not a gap).
- A note, not a find: the legc-gaps entries outside
  C088-11's named source lists (GAP-C01, GAP-C09F,
  GAP-ENV) — Cluster C's did-not-scan line records
  them for the register stage's awareness; the
  completeness check (T602) is against the named
  lists, and these are not on them.
- Every scan find above is S6's input: the register
  consolidates and ranks; the scans did not rank, and
  no wave is proposed or commissioned by this stage.

*This record does not establish:* scan quality —
shape only; quality is the oracle's and, finally, the
owner's at ratification (T504's line). Nor that the
35 finds are all the gaps there are (T501's line),
nor that infrastructure gaps matter less (T503's
line), nor that thin evidence means wrong (T502's
line).
