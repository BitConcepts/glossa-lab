# Spec 088 — Stage S5, Cluster C scan: infrastructure + bookkeeping

Executed 2026-11-04 on branch `feat/088-s5-scans` off
origin/main `893a426a`. Task T503. Finds are exactly
one of the four registered kinds; every candidate
carries a one-line falsifier and an honesty-rule type
(C088-10, C088-12). Scope: Domain 5 (Program
infrastructure) plus every cross-cutting bookkeeping
item on C088-11's source lists, wherever it lives.

## Inputs (read first-hand this scan)

- `glossa-indus/map/program-map.json` coverage block:
  Domain 5: 17 studies / 150 claims (studies open 11 /
  unjudged 6; claims open 149 / closed_other 1);
  multi-spec claims 44 (C-11).
- `glossa-indus/map/program-map-finds.json`: this
  cluster's items are Domain 5's 6 `bundle_less_study`
  finds (C-03).
- `docs/governance/legc-gaps-2026-10-29.md` (the
  system-coupling audit's gap register: GAP-C07,
  GAP-C12, GAP-C13 as written there).
- `specs/086-winning-combination-adoption/stage-5-record.md`
  §T505 (the Spec 085 re-score: items 2 and 6,
  partially closed);
  `specs/086-winning-combination-adoption/stage-2-record.md`
  and `stage-4-record.md` (the mahadevan:64 routes);
  `glossa-indus/matrix/matrix.json` coverage block
  (current: dependency pairs not cells 793; sign_refs
  occurrences 1; sign_refs_without_anchor_record 3).
- `specs/084-policy-sync-conformance/spec.md` (C084-10
  HELD; the llms.txt drift statement).
- `files/2026-11-04-spec088-adoption-full-picture-map.md`
  §4 (goal-workspace adoption record: the §4 items);
  repo `LEDGER.md` (the T020 desktop settle record);
  the GitHub compare of `309ea63c…893a426a` read this
  scan (main ahead_by 118, behind_by 0).
- `records/taxonomy-v0-draft.md` §5 (numbers 049 and
  085); the live spec tree (89 directories; verified
  this scan: no `049-*`, no `085-*`).

## Finds

### C-01 — GAP-C07: the lifecycle state machine is not storage-enforced, and its spec was never written

- **Kind:** missing node.
- **Missing piece:** the cross-cutting spec the gap
  record itself calls for. The gated transitions
  (`claim_stage.transition_stage` /
  `claim_bundle.gated_transition_stage`) are sound,
  but no API endpoint or file writer is forced through
  them: claim/anchor records are plain JSON and other
  writers set `stage` / `review_status` / `confidence`
  directly. Closing it "needs its own spec so each
  writer's legitimate transitions are enumerated
  rather than guessed" — that spec does not exist.
- **Why its absence blocks convergence:** the ledger's
  lifecycle guarantees hold only where writers
  cooperate. Every generated surface downstream —
  matrix, maps, this program's standings — derives
  from fields no storage layer protects, so the whole
  chain's integrity rests on writer discipline rather
  than enforcement.
- **Evidence:** `docs/governance/legc-gaps-2026-10-29.md`
  GAP-C07 (owner as written there: backend maintainer,
  spec + implementation; the C-03 promotion-evidence
  mitigation noted as partial).
- **Candidate:** the GAP-C07 spec — a writer census,
  then routing every writer through the gated
  transitions or adding storage-layer validation.
  - **Falsifier:** the writer census shows every
    current writer already routes through the gated
    transitions → the gap closes as already-enforced
    and only the census record is new.
  - **Type:** in-house re-derivation.
  - **Owner gates:** the spec is a cross-cutting act
    (block approval like any spec); the gap record
    names the backend maintainer as its owner.

### C-02 — GAP-C12 remnant: a legacy chi-squared rule is still registered, and its live reach was never traced

- **Kind:** missing node.
- **Missing piece:** the live-caller trace and the
  disposition. `backend/glossa_lab/experiment_graph_phase20.py`
  still declares significance by `chi2 > 3.84 *
  max(1, dof)` — a statistically wrong threshold
  scaling (verified in the current tree: the rule
  stated at line 462, `critical_per_dof` 3.84 at line
  474) — and the gap record states "whether any live
  verdict flows through it is untested." The v2
  checkers can fail correctly; the legacy module was
  neither retired nor repaired.
- **Why its absence blocks convergence:** an unknown
  number of verdicts (possibly zero) rest on a rule
  the program has already judged wrong. Until the
  trace runs, no verdict inventory can certify that
  none of them are live.
- **Evidence:** `docs/governance/legc-gaps-2026-10-29.md`
  GAP-C12 (owner as written there: experiment-graph
  maintainer); `backend/glossa_lab/experiment_graph_phase20.py`
  lines 462/474 (read this scan).
- **Candidate:** run the caller trace, then the
  disposition it dictates (retire the module, or
  replace the rule with proper per-dof critical
  values).
  - **Falsifier:** the trace finds zero live callers
    and zero verdict-bearing artifacts → the module
    retires and the find closes as bookkeeping; a
    trace finding live verdicts converts it to a
    thin-evidence find over those verdicts.
  - **Type:** in-house re-derivation.
  - **Owner gates:** the disposition is the
    experiment-graph maintainer's (per the gap
    record).

### C-03 — GAP-C13: bundle-less directories and the undistinguished falsifier cases

- **Kind:** stale bookkeeping.
- **Missing piece:** a one-line disposition per
  listed spec (no-claims / claims-elsewhere /
  falsifier-required). Two instruments, recorded
  separately because they measure different things:
  (i) today's tree — 28 bundle-less directories in
  the find list, of which Domain 5's six are this
  cluster's: `001-glossa-lab-baseline`,
  `002-gdelt-ngrams-and-frontier-methods`,
  `003-mcp-and-test-gaps`,
  `025-paper-search-research-check`,
  `025-stage2-controlled-followup`,
  `026-core-research-source` (the other 22 are
  consumed by Clusters A and B); (ii) the audit-era
  instrument — at the 2026-10-29 scan of specs
  001–081, 31 specs had no `claims.json` at all and
  27 specs' `spec.md` never mentions a falsifier
  (002, 004, 013–017, 020–023, 025, 026, 030, 032,
  035–041, 043, 066, 079, 080), with the register
  unable to distinguish "no governed claims" from
  "governed claims with no falsifier."
- **Why its absence blocks convergence:** the program
  cannot tell, for a third of its historical spec
  range, whether silence means "nothing governed
  here" or "governed claims nobody gave a falsifier
  to." Every completeness claim the register makes
  inherits that ambiguity until the sweep runs.
- **Evidence:** `docs/governance/legc-gaps-2026-10-29.md`
  GAP-C13; `glossa-indus/map/program-map-finds.json`
  (the 28, per-study); `records/stage-s2-record.md`
  (the 28 enumerated).
- **Candidate:** the disposition sweep over the
  audit list, reconciled against today's bundle
  census — one line per spec, recorded against it.
  - **Falsifier:** a listed spec is found holding
    governed claims that lack falsifiers → it exits
    the sweep as a falsifier-backfill find, and the
    "bookkeeping only" framing fails for it.
  - **Type:** in-house re-derivation.
  - **Owner gates:** spec authors for their specs;
    the program owner for the sweep and any
    constitution-level rule it proposes (per the gap
    record).

### C-04 — Spec 086 residual: claim×claim dependency pairs are coverage data, not edges

- **Kind:** missing edge.
- **Missing piece:** typed claim→claim edges. The
  current matrix coverage counts
  `dependency_pairs_not_cells: 793` (790 at Spec 086
  Stage 5; +3 from the C088 intake's own pairs) —
  pairs carried in evidence_refs and expressly not
  cells under matrix-defs v1; and extracted claims
  carry no `depends_on` / `conflicts_with` fields for
  the AEE graph at all.
- **Why its absence blocks convergence:** the map
  cannot show that one claim's fall takes others with
  it. Digestion order and blast radius — the two
  things a claims program most needs from its graph —
  are invisible in the layer built to show them.
- **Evidence:**
  `specs/086-winning-combination-adoption/stage-5-record.md`
  §T505 item 2 ("Edges for the live claim population —
  partially closed");
  `glossa-indus/matrix/matrix.json` coverage block
  (793, counted this scan).
- **Candidate:** a dependency-edge promotion study —
  promote the recorded pairs to typed edges under a
  matrix-defs amendment, or record why they must stay
  coverage data.
  - **Falsifier:** the promotion analysis shows the
    pairs duplicate existing claim→evidence edges
    claim-for-claim → not-a-gap disposition, with the
    analysis as the record.
  - **Type:** in-house re-derivation.
  - **Owner gates:** a matrix-defs amendment is a
    program act under Spec 086's discipline.

### C-05 — Spec 086 residual: the two-graph-worlds join has population one

- **Kind:** missing edge.
- **Missing piece:** identifier linkage between claim
  text and the sign register at population scale.
  Exactly one claim of 876 carries sign_refs that
  resolve (one `sign_refs` occurrence in the current
  matrix artifact; Stage 5's count was 1 of 840 —
  the population did not grow with the ledger). The
  friction surface, from the same coverage block: 14
  unresolved sign mentions (prose mentions with no
  sign identity) and 3 sign_refs with no anchor
  record under the matrix key (C-06).
- **Why its absence blocks convergence:** claims and
  signs are the program's two graph worlds; joined at
  one claim, every cross-world question (which claims
  does this sign's verdict touch — Cluster A's A-04
  from the other side) is unanswerable from the
  generated layers.
- **Evidence:**
  `specs/086-winning-combination-adoption/stage-5-record.md`
  §T505 item 6 ("Join the two graph worlds —
  partially closed… The joined population is one
  claim"); `glossa-indus/matrix/matrix.json` (counted
  this scan).
- **Candidate:** a sign-mention extraction pass
  minting structured sign_refs from claim text under
  a registered rule.
  - **Falsifier:** the pass over all 876 claims finds
    structured mentions on only the same single
    claim → the join is population-one because the
    claims genuinely do not name signs in extractable
    form, and the find re-registers as a property of
    the claim corpus, not a missing build.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

### C-06 — T201: two registered routes derive mahadevan:64/70/72 differently

- **Kind:** stale bookkeeping.
- **Missing piece:** the owner's oracle ruling, and
  the losing route's amendment. Matrix-defs v1's
  literal key resolves `mahadevan:64`, `mahadevan:70`,
  `mahadevan:72` to no anchor record (the current
  matrix coverage still lists exactly these 3 as
  sign_refs_without_anchor_record, all on
  `parpola_2010_dravidian_solution_manual_002`),
  while glossa-settle-1 resolves the same references
  by number to M064/M070/M072. The divergence was
  flagged for the owner's oracle read beside T201 at
  Spec 086 Stage 2; no ruling is on record and
  matrix-defs is unamended.
- **Why its absence blocks convergence:** one claim's
  anchor relations are simultaneously "no record" and
  "M064/M070/M072" depending on which registered
  surface a reader opens. The program's two generated
  layers disagree about the same fact, by name, in
  print.
- **Evidence:**
  `specs/086-winning-combination-adoption/stage-2-record.md`
  (matrix census: the 3 refs unresolved);
  `specs/086-winning-combination-adoption/stage-4-record.md`
  (the settling key resolving mahadevan:64 → M064);
  `glossa-indus/matrix/matrix.json` coverage block
  (the 3 entries, current).
- **Candidate:** the owner's oracle ruling, then the
  amendment of the route that loses (a matrix-defs v2
  key rule, or a settle-key registration change).
  - **Falsifier:** a third registered route is found
    resolving the refs a third way → the divergence
    is wider than two routes and the entry must be
    re-scoped before any ruling.
  - **Type:** in-house re-derivation (a reconciliation
    of the program's own records).
  - **Owner gates:** OWNER — the ruling is his oracle
    act; T201's acceptance was human-as-oracle from
    the start.

### C-07 — The tracker's llms.txt still names the superseded v8 preprint as latest

- **Kind:** stale bookkeeping.
- **Missing piece:** the corrected latest-release
  line on the served `bitconcepts.tech/llms.txt`,
  which "still names the superseded v8 preprint as
  the latest release (verified live 2026-10-31) while
  v9 is the current deposit" (Spec 084's record of
  the drift). The correction is held as C084-10
  because its text is bundled with the prepared v10
  corrections package awaiting the owner's approval
  of the exact text, and the source lives outside
  this repo.
- **Why its absence blocks convergence:** llms.txt is
  the machine-facing summary of the program's public
  record; it currently directs readers to a superseded
  version as the latest — the one public surface that
  misstates the program's own headline artifact.
- **Evidence:** `specs/084-policy-sync-conformance/spec.md`
  (the drift statement; C084-10 HELD with its reason;
  C084-9's note that conformance belongs to the
  tracker publish path).
- **Candidate:** the v10-gated correction, published
  through the tracker publish path with its
  served-identity check.
  - **Falsifier:** a fresh fetch of the served
    llms.txt already names v9 (or v10) → the find is
    already closed and is removed, with the fetch as
    the record.
  - **Type:** in-house re-derivation.
  - **Owner gates:** OWNER — the correction text is
    bundled with his v10 approval act.

### C-08 — The desktop host still runs a 2026-10-31 checkout (118 commits behind main)

- **Kind:** stale bookkeeping.
- **Missing piece:** the Spec 083-sequence sync of
  the desktop checkout to main, with its post-sync
  battery. The repo's own record: the desktop
  checkout was settled from `124a1ac3` to `309ea63c`
  on 2026-10-31 (T020 acceptance, settle job run
  41164924219) and no later settle is recorded. The
  adoption record carries it as "desktop clone at
  local commit 309ea63c, unsynced (Spec 083 sequence
  owns)." Precision this scan adds: `309ea63c` is PR
  #472's merge commit and **is** in main's history —
  the GitHub compare read today shows main
  (`893a426a`) 118 commits ahead of it, 0 behind. It
  is the desktop checkout that stands still, so every
  Spec 087/088-era backend change is absent from the
  served host.
- **Why its absence blocks convergence:** the
  production Glossa backend — the one the MCP tools
  and the cloud edition are being built on — serves
  an October 31 snapshot while the ledger's home repo
  has moved through two specs. Any behavior verified
  in the repo is not thereby behavior of the served
  system.
- **Evidence:** repo `LEDGER.md` (T020 acceptance:
  the settle record); `files/2026-11-04-spec088-adoption-full-picture-map.md`
  §4; GitHub compare `309ea63c…893a426a` (ahead_by
  118, behind_by 0; read 2026-11-04).
- **Candidate:** execute the sync through the
  Syncyard gatekeeper (windowless, owner's profile)
  with the host battery re-run, as the Spec 083
  sequence prescribes.
  - **Falsifier:** a gatekeeper read shows the
    desktop checkout already at a descendant of
    current main with the battery green → the find
    is closed and only this record was stale.
  - **Type:** in-house re-derivation.
  - **Owner gates:** the sync belongs to the Spec 083
    sequence (adoption §4); desktop execution runs
    through the gatekeeper only.

### C-09 — The data-lineage question: two production datasets, no adjudication

- **Kind:** stale bookkeeping.
- **Missing piece:** the adjudication of which
  dataset is canonical where they differ, and a diff
  census bounding where they differ. Both are
  preserved: the VM-era dataset and desktop snapshot
  1 (2026-10-28, taken at the Spec 080 cutover). The
  adoption record carries it as "data-lineage
  adjudication (VM dataset vs snapshot 1) as an open
  owner question." Scope note: the VM production DB
  holds no claim state — claims of record live in the
  repo checkout — so the open question concerns the
  application's dataset, not the ledger.
- **Why its absence blocks convergence:** any
  app-level record (jobs, experiments, reports) can
  exist in two versions with no rule for which one a
  future surface should show. The ambiguity is
  bounded but unbounded-in-time: it survives every
  migration that copies either dataset forward.
- **Evidence:** `files/2026-11-04-spec088-adoption-full-picture-map.md`
  §4; `files/2026-10-28-spec-080-desktop-migration-record.md`
  §10 (goal-workspace cutover record: the snapshot's
  custody).
- **Candidate:** the lineage adjudication — a
  byte-level diff census first, then the owner's
  ruling on the census.
  - **Falsifier:** the census shows the two datasets
    identical in every claim-adjacent respect → the
    question is moot and closes as not-a-gap, with
    the census as the record.
  - **Type:** in-house re-derivation.
  - **Owner gates:** OWNER — the adjudication is his
    ruling.

### C-10 — Spec numbers 049 and 085 have no directory

- **Kind:** stale bookkeeping.
- **Missing piece:** a recorded disposition per
  number. Verified against today's tree (89
  directories; no `049-*`, no `085-*`): 049 is named
  as a predecessor in Spec 070's own title ("Successor
  to Spec 049, D-06") — a number the lineage cites
  that the tree cannot produce; 085's package (the
  graph-matrix audit) exists only in the goal
  workspace, unadopted — its six gaps were re-scored
  by Spec 086 Stage 5 without the spec ever landing.
- **Why its absence blocks convergence:** the count
  of the program's studies is citable two ways (89
  directories; numbers running to 088 with two
  holes), and a successor's title cites a predecessor
  no reader can open. Small, but exactly the class of
  discrepancy that compounds in a program whose
  defense is its records.
- **Evidence:** `records/taxonomy-v0-draft.md` §5
  (both numbers, with the 049 predecessor naming);
  the live `specs/` tree (counted this scan).
- **Candidate:** for 049, a register disposition
  (lineage reference, not a study — no directory ever
  existed in this tree); for 085, adoption or formal
  non-adoption of the package.
  - **Falsifier:** a 049 bundle or directory surfaces
    in any clone or archive → 049 converts to a
    bundle-less-study find (the A-01 pattern) and
    this disposition is wrong on the record.
  - **Type:** in-house re-derivation.
  - **Owner gates:** 085's adoption is the owner's
    act.

### C-11 — The multi-spec membership fork (44 claims) is registered one way and unruled the other

- **Kind:** stale bookkeeping.
- **Missing piece:** the ruling on the fork — or a
  recorded decision that the registered reading
  stands permanently. The taxonomy draft's premise
  ("none multi-spec today") is falsified by the
  ledger: 44 bundle claims name more than one spec
  directory across their `sources[]`, in
  non-representative roles (`bundle_aee`,
  `evidence_instance`, `promotion`); the ids are
  enumerated in every build's coverage block
  (`multi_spec_claims`, 44). Program-map-defs v1
  registered membership = the source-of-record spec
  only (stage-s1-record departure (a)), so citing
  studies' roll-ups do not count claims they cite.
  The other reading (any-source membership) would be
  a defs v2 amendment; it has not been ruled on.
- **Why its absence blocks convergence:** two
  defensible readings of "a study's claims" diverge
  on exactly these 44 claims. Any future surface that
  counts membership the other way disagrees with the
  program map by a known, enumerated set — a standing
  invitation to a future "the two records disagree"
  find with no ruling to point at.
- **Evidence:** `records/stage-s1-record.md`
  departure (a); `glossa-indus/map/program-map.json`
  coverage block (the 44 ids);
  `glossa-indus/map/PROGRAM-MAP-DEFINITIONS.md`
  (the registered rule).
- **Candidate:** the owner rules the fork at register
  ratification; if any-source membership wins, defs
  v2 and the builder amendment follow as their own
  act.
  - **Falsifier:** a recomputation under the
    any-source rule changes no study's class on
    today's ledger → the fork is presentational
    today and downgrades to a note, with the
    recomputation as its record.
  - **Type:** in-house re-derivation.
  - **Owner gates:** OWNER — the defs' semantics were
    his at T003/T101; changing or confirming them is
    his.

## Counts (this cluster)

Finds: **11** — missing node 2 (C-01, C-02); missing
edge 2 (C-04, C-05); thin evidence 0; stale
bookkeeping 7 (C-03, C-06, C-07, C-08, C-09, C-10,
C-11). Candidates: **11**. Find-list items consumed:
6 of 28 `bundle_less_study` (C-03). This cluster
records no thin-evidence find: Domain 5's claims are
the program's governance claims about itself, and no
record on this scan's source lists counts their
support as thin — their gaps are enforcement (C-01)
and bookkeeping, and the scan records what the
records support, not a symmetry.

## What this cluster did not scan

The remaining entries of the same gap register it drew
GAP-C07/C12/C13 from — GAP-C01 (no authentication
layer), GAP-C09F (frontend error reporting),
GAP-ENV (runtime venv below the engine pin) — are
outside C088-11's named source lists for this spec;
they are carried to S6 as a note, not scanned (per the
scan plan's output discipline). The `in_flight` empty
population (D-088-4) is a registered v1 limitation,
not a find. Live-system state (backend jobs, tray,
serving) is outside the scans' inputs (generated map
+ records).

*This does not establish:* that infrastructure gaps
matter less — the register ranks; the scan only
records. (T503's line.)
