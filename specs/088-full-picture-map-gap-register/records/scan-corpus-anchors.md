# Spec 088 — Stage S5, Cluster A scan: corpus + anchors

Executed 2026-11-04 on branch `feat/088-s5-scans` off
origin/main `893a426a`. Task T501. Finds are exactly one of
the four registered kinds (missing node / missing edge /
thin evidence / stale bookkeeping); every candidate carries
a one-line falsifier and an honesty-rule type (C088-10,
C088-12). Nothing in this record is a standing: where a
study's standing exists only in prose, that is recorded as
a find, never used as data (C2, C088-17).

## Inputs (read first-hand this scan)

- `glossa-indus/map/program-map.json` coverage block:
  Domain 1 (Sign inventory & corpus) 17 studies / 125
  claims, studies open 10 / unjudged 7; Domain 2 (Anchors
  & readings) 13 studies / 0 claims, studies unjudged 13.
  Ledger 907 lines, canonical SHA-256 `9f8144c3…` (the
  S2–S4 stamp); falsifier coverage 867/876 (bundle
  853/853, extracted 14/23).
- `glossa-indus/map/program-map-finds.json`: this
  cluster's find-list items are the 20 `bundle_less_study`
  finds in Domains 1–2 (enumerated in A-01/A-02).
- `glossa-indus/matrix/matrix.json` coverage block
  (current artifact): columns studies 10 / documents 316
  / research_checks 31 / anchors 287; cells by class
  documents 1,392 / studies 7 / anchors 0 /
  research_checks 0; unresolved sign mentions 14.
- `docs/repair-2026-10-26/anchor-support-audit.json`
  (WP5): summary counts over the 94 strict anchors —
  6 supported_independent / 46 supported_internal_only /
  37 requires_revalidation / 3 expert_adjudication_pending
  (M222, M362, M398) / 2 insufficient_evidence (M367,
  M048); the Phase-48 promotion subset (n=30) splits
  0 supported / 28 requires_revalidation / 2
  insufficient_evidence.
- Pre-answered legs, cited not re-derived (scan plan):
  the WP5 census above; the falsifier census — consumed
  here as context for A-09: ledger-claim falsifiers are
  complete for the bundle population (853/853), so
  thinness in this cluster is support class and
  anchor-record completeness, not claim-falsifier
  absence.

## Finds

### A-01 — Domain 2's thirteen studies carry no ledger claims

- **Kind:** stale bookkeeping.
- **Missing piece:** claims bundles for the anchor
  provenance and validation era. The 13 study nodes —
  `004-indus-executable-package`, `005-phase52-v2`,
  `006-anchor-provenance-audit`,
  `007-phase109-follow-through`, `008-m222-adjudication`,
  `009-phase111-blind-affiliation`,
  `010-phase112-blind-affiliation`,
  `011-phase113-nonsa44-validation`,
  `012-phase113-blind-affiliation`,
  `014-phase115-nonsa44-validation-v2`,
  `016-phase117-within-compilation-validation`,
  `017-phase118-within-compilation-validation-v2`,
  `018-phase119-pred2026-readiness` — are all class
  unjudged; their standings exist only in phase records
  and prose. Consumes 13 `bundle_less_study` finds.
- **Why its absence blocks convergence:** the anchor
  layer is the program's core evidence, and its entire
  validation era (Phases 111–119, the batteries the 44
  SA-lineage anchors were tested by) is invisible to the
  ledger → matrix → map chain. No generated surface can
  weigh it; WP5 had to audit the anchors from trails
  outside the ledger (A-10).
- **Evidence:** program-map coverage block (Domain 2:
  13 studies, 0 claims, 13 unjudged);
  `program-map-finds.json` (13 finds named above);
  `records/taxonomy-v0-draft.md` §3 Domain 2.
- **Candidate:** bundle backfill — extract claims
  bundles for the 13 studies from their phase records
  through the sanctioned ledger intake.
  - **Falsifier:** a study whose phase record contains
    no falsifiable claim-shaped statements (pure battery
    run logs) dispositions as pre-ledger history instead
    of receiving a bundle — the backfill claim fails for
    that study on its own record.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none for the intake (the program's
    own act); per-study dispositions settle at the
    register's ratification (T603).

### A-02 — Domain 1's seven bundle-less studies

- **Kind:** stale bookkeeping.
- **Missing piece:** claims bundles for
  `015-phase116-corpus-harmonization`,
  `019-phase125-cross-compilation-positional`,
  `020-soviet-pred-adjudication`,
  `021-phase127-cross-compilation-diagnostic`,
  `021-phase130-intake-pack`,
  `022-phase131-attribution`,
  `023-keyed-transcription-layer` — all unjudged, all
  concentrated in the cross-compilation line and the
  keyed transcription build. Consumes 7
  `bundle_less_study` finds.
- **Why its absence blocks convergence:** Domain 1's
  other ten studies carry 125 claims; the seven without
  bundles include the corpus-harmonization study and
  the transcription layer the later corpus work stands
  on, so the corpus's own foundations are the part of
  the domain the picture cannot weigh.
- **Evidence:** program-map coverage block (Domain 1:
  studies unjudged 7); `program-map-finds.json`.
- **Candidate:** bundle backfill from the phase
  records, as A-01.
  - **Falsifier:** as A-01 — a record with no
    claim-shaped statements dispositions as pre-ledger
    history, not backfill.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

### A-03 — The cross-compilation attribution line's early legs are unledgered

- **Kind:** missing edge.
- **Missing piece:** the claim-level edge from the
  Phase-125/127 disagreement result to its attribution
  successors. Studies `019`, `021-phase127`, `022`
  (the diagnostic legs) carry no claims (A-02), while
  `034-matched-object-attribution` and
  `058-transcription-disagreement-mechanism` carry the
  attribution forward with bundles. The successor
  relation exists in titles and prose only; at claim
  level there is nothing for an edge to attach to.
- **Why its absence blocks convergence:** the program's
  central corpus disagreement — why the Holdat and ICIT
  positional profiles disagree — has its evidentiary
  root outside the generated graph. A reader of the map
  cannot trace what the attributions attribute.
- **Evidence:** `records/taxonomy-v0-draft.md` §3
  Domain 1 (Cross-compilation comparisons, 8 studies);
  program-map coverage block; A-02's find consumption.
- **Candidate:** the A-02 backfill for `019`,
  `021-phase127`, `022`, sequenced first — it creates
  the nodes this edge needs, in the disagreement
  result's own terms.
  - **Falsifier:** extraction shows the phase records'
    stated result contradicts the premise `034`
    attributes (a different disagreement mechanism) →
    the edge is recorded as contested, not supportive,
    and the attribution line re-opens.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

### A-04 — No claim bears a recorded relation to any anchor

- **Kind:** missing edge.
- **Missing piece:** claim→anchor edges. The matrix
  carries 287 anchor columns and zero anchor cells
  (cells by class: anchors 0, counted from the current
  `matrix.json`); under matrix-defs v1 anchors
  contribute no cells, so the relation was never built.
  On the claim side, 14 sign mentions in claim text
  resolve to no sign identity (the coverage block's
  unresolved-sign-mentions list), so those mentions
  cannot become edges either.
- **Why its absence blocks convergence:** which claims
  stand on which anchors is the most decision-relevant
  relation in a decipherment program — it is the blast
  radius of every anchor verdict in A-05/A-06 — and it
  is absent from the evidence graph. The settling
  layer's identifier join exists but has population one
  (Cluster C, C-05).
- **Evidence:** `glossa-indus/matrix/matrix.json`
  coverage block (columns by class; cells by class;
  unused columns: anchors 287 of 287);
  `specs/086-winning-combination-adoption/stage-2-record.md`
  (the registered choices, T201).
- **Candidate:** an edge-construction study under a
  matrix-defs amendment, building anchor cells from
  structured sign references and the WP5 trails.
  - **Falsifier:** the construction pass finds
    structured sign references on too few claims to
    populate the relation (today exactly 1 claim
    carries sign_refs) → the find converts to a
    missing-node find (structured sign-mention
    extraction) rather than closing.
  - **Type:** in-house re-derivation.
  - **Owner gates:** a matrix-defs amendment is a
    program act under Spec 086's amendment discipline.

### A-05 — 46 of the 94 strict anchors rest on internal-only support

- **Kind:** thin evidence.
- **Missing piece:** for 46 strict anchors, any support
  line originating outside the program's own derivation
  lineage. The audit's derivation categories for the 46:
  GRAMMAR 20 / DEDR 17 / ICONOGRAPHIC 4 / MIXED 2 /
  CROSSWALK_CORPUS 2 / LITERATURE 1 — every line
  produced inside this program.
- **Why its absence blocks convergence:** under the
  honesty rule (C088-12) these standings cannot be
  cited as confirmed. The strict core's independently
  supported mass is 6, not 94, and every downstream
  claim inheriting anchor support inherits the
  thinness.
- **Evidence:**
  `docs/repair-2026-10-26/anchor-support-audit.json`
  summary_counts (supported_internal_only 46;
  supported_independent 6: M044, M047, M124, M202,
  M329, M330).
- **Candidate:** an outside-reproduction pass over the
  46 — independent attestation, or blind re-derivation
  by readers who did not produce the original
  derivations.
  - **Falsifier:** an anchor whose only producible
    support after the pass remains same-lineage stays
    internal-only and the count stands — the find
    closes per-anchor only as external lines actually
    land.
  - **Type:** independent confirmation.
  - **Owner gates:** external readers are an owner act
    (named humans; the program's contact rules apply).

### A-06 — 37 strict anchors require revalidation (routed: 28 / 5 / 4)

- **Kind:** thin evidence.
- **Missing piece:** a validation that survives the
  repair brief's findings, for 37 anchors. The scan
  plan's routing duty, executed from the audit's own
  fields:
  - **28 are Phase-48 promotions** (node-shaped): the
    battery that promoted them carried four
    pass-by-default paths (`too_short_pass`,
    `char_not_in_lm—pass_by_default`,
    `no_anchor_neighbours—pass_by_default`,
    `no_expectation—pass_by_default`; baseline §5.7),
    and 30 tested produced 30 promoted. The missing
    piece is a corrected validation run.
  - **5 rest on a single line** (3 restored readings
    under disposition rule R5b: M042, M046, M108;
    2 citing Phase-48 as support without being
    promotions, R5c: M176, M342). The missing piece is
    revalidation under the corrected checkers.
  - **4 rest solely on a crosswalk/literature import**
    (R5d: M087, M165, M264, M311 — edge-shaped): their
    only support is an attribution edge of the kind
    Cluster B's B-01 shows to be compromised (0 of 184
    eligible). The missing piece is an independent
    line.
- **Why its absence blocks convergence:** 37 of the 94
  strict anchors — including 28 of the 30 Phase-48
  promotions (the other 2 are A-08's pair; none of the
  30 is supported in any class) — hold a status the
  program's own audit says it cannot currently defend.
  Until they are revalidated or fall, the strict core's
  size is nominal.
- **Evidence:**
  `docs/repair-2026-10-26/anchor-support-audit.json`
  (summary_counts; phase48_promotion_subset; per-record
  disposition_rule / phase48_promotion fields, counted
  this scan); `docs/repair-2026-10-26/baseline-and-dispositions.md`
  §5.7, §5.A.
- **Candidates (one per route):**
  1. Corrected Phase-48 battery re-run over the 28,
     with the pass-by-default paths removed.
     - **Falsifier:** the re-run promotes a materially
       different set → the original promotions
       reclassify per the new run, and the battery's
       historical output is retired as evidence.
     - **Type:** in-house re-derivation.
     - **Owner gates:** none.
  2. Corrected-checker revalidation of the 5
     single-line anchors (phonotactics_v2 /
     site_stats_v2 lineage).
     - **Falsifier:** the v2 checkers judge the support
       insufficient → the 5 move to insufficient
       evidence, not back to supported.
     - **Type:** in-house re-derivation.
     - **Owner gates:** gated on Cluster B's B-02
       linguist leg for the phonotactic arm.
  3. An independent support line for the 4 R5d
     anchors, sourced outside the crosswalk lineage.
     - **Falsifier:** no source outside the crosswalk
       lineage attests the readings → the 4 stay
       requires-revalidation permanently, recorded as
       structural rather than pending.
     - **Type:** independent confirmation.
     - **Owner gates:** external sourcing is an owner
       act.

### A-07 — Three strict anchors await expert adjudication (M222, M362, M398)

- **Kind:** thin evidence.
- **Missing piece:** expert adjudication verdicts for
  M222, M362, M398. M222's adjudication study exists
  (`008-m222-adjudication`) but is itself bundle-less
  (A-01), so even its partial record is outside the
  ledger.
- **Why its absence blocks convergence:** the audit's
  acceptance rule (baseline §5.A) marks expert
  adjudication pending where required — never forced
  complete. Three anchors sit in that pending state
  with no verdict and no schedule.
- **Evidence:**
  `docs/repair-2026-10-26/anchor-support-audit.json`
  summary_counts (expert_adjudication_pending_signs);
  `docs/repair-2026-10-26/README.md` ("three anchor
  entries await expert adjudication").
- **Candidate:** complete the expert adjudications on
  the M222 pattern (named expert, registered protocol).
  - **Falsifier:** an expert returns "cannot adjudicate
    on this evidence" → the anchor moves to
    insufficient evidence, closing the pending state
    honestly rather than by default.
  - **Type:** independent confirmation.
  - **Owner gates:** owner act (named experts; contact
    rules).

### A-08 — Two strict anchors are recorded as insufficient evidence (M367, M048)

- **Kind:** thin evidence.
- **Missing piece:** evidence itself. Both are
  Phase-48 promotions (the promotion subset's 2
  insufficient of 30); the audit's verdict is that the
  trails do not carry enough to judge them either way.
- **Why its absence blocks convergence:** two members
  of the strict core are known-empty: they count in
  the 94 and support nothing. Unlike A-06, no method
  repair changes this — the record is the gap.
- **Evidence:**
  `docs/repair-2026-10-26/anchor-support-audit.json`
  summary_counts (insufficient_evidence 2;
  phase48_promotion_subset).
- **Candidate:** targeted evidence assembly over the
  widest trails (Phase-108 register, crosswalk,
  corpus frames) with a stop rule.
  - **Falsifier:** assembly over the full trails still
    yields no second line → the pair is recorded as
    permanently insufficient and exits the strict
    core's working mass by disposition.
  - **Type:** in-house re-derivation (assembly of
    existing records; only external evidence could
    change the outcome if it fails — noted, not
    claimed).
  - **Owner gates:** none.

### A-09 — No strict anchor record states a falsifier or a distinguishing observation

- **Kind:** thin evidence.
- **Missing piece:** per-anchor falsifiers. Counted
  from the audit's records this scan: all 94 strict
  records carry `falsifier: "no falsifier recorded"`
  and `distinguishing_observation: "not recorded"`
  (94/94, both fields). The ledger's claims are
  falsifier-complete for the bundle population
  (853/853) — the absence is at the anchor-record
  level, a different instrument (WP5 element 5.5,
  unexecuted at this completeness).
- **Why its absence blocks convergence:** an anchor
  whose record states no observation that would
  distinguish its reading from the runner-up
  alternative cannot be falsified as held; A-05/A-06's
  revalidations have no per-anchor test to run against.
- **Evidence:**
  `docs/repair-2026-10-26/anchor-support-audit.json`
  records (fields counted this scan);
  `docs/repair-2026-10-26/baseline-and-dispositions.md`
  §5.5.
- **Candidate:** falsifier backfill per anchor from
  its derivation trail (the distinguishing observation
  the trail's own tests imply), executed as WP5
  element 5.5 at record level.
  - **Falsifier:** an anchor whose trail contains no
    distinguishing observation even in prose is
    recorded as unfalsifiable-as-held and routed to
    A-07/A-08's dispositions — the backfill claim
    fails for it on its own record.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

### A-10 — 52 of 94 strict-anchor trails never cite the ledger

- **Kind:** missing edge.
- **Missing piece:** trail→ledger citation edges. The
  audit's summary counts `records_with_no_ledger_passage_in_trail:
  52` — for over half the strict core, the provenance
  trail records no ledger passage the standing rests
  on.
- **Why its absence blocks convergence:** the anchor
  layer's provenance and the claim layer's record do
  not meet. A reader cannot walk from an anchor's
  standing to the ledger entry that carries it, which
  is why A-01's era had to be audited from trails at
  all.
- **Evidence:**
  `docs/repair-2026-10-26/anchor-support-audit.json`
  summary_counts.
- **Candidate:** a trail completion pass over the
  Phase-108 register trails, adding the ledger passage
  citation where the passage exists.
  - **Falsifier:** a trail whose underlying passage
    does not exist in the ledger corpus → that
    anchor's standing is recorded as resting on an
    uncitable passage (a worse, named state), not
    silently passed over.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

### A-11 — The 44 pending readings have no adjudication route

- **Kind:** missing node.
- **Missing piece:** any validated route — instrument
  or panel — that may score the 44 pending anchor
  readings. The Step 0-G instrument line closed by
  owner decision OD-1 (2026-10-28) after its final
  run: "M4 remains GATED — DRAFT ONLY, permanently
  under its current gate. The 44 pending readings
  remain pending indefinitely, carrying no weight —
  neither validated nor falsified; this run scored
  none of them." Phase-120 gave them a descriptive
  triage (Bhaskar 2024), not an adjudication.
- **Why its absence blocks convergence:** 44 candidate
  readings — against 287 recorded anchors and a strict
  core of 94 — sit outside every verdict. The core can
  neither grow from them nor formally exclude them,
  and "pending" has no exit condition on any current
  record.
- **Evidence:** `LEDGER.md` §9 endgame entry (Step 0-G
  closure, OD-1); `LEDGER.md` Phase-120 entry (Bhaskar
  2024 triage of the 44);
  `docs/repair-2026-10-26/wp8-exposure-and-controls.md`
  (Step 0-G status: unsatisfied; M4 gated);
  `docs/repair-2026-10-26/baseline-and-dispositions.md`
  §5.1 (the 44 maintained without new weight).
- **Candidate:** an expert adjudication panel for the
  44 on the M222 pattern (A-07) — the instrument route
  is closed by the owner's own decision, so the panel
  is the route that does not require reopening it.
  - **Falsifier:** the panel's agreement on a
    planted-control subset falls below the registered
    bar → the panel route closes too, and the 44 stay
    pending by a second, independent failure.
  - **Type:** independent confirmation.
  - **Owner gates:** OWNER — OD-1 was his decision;
    any route (panel, or a new instrument design)
    opens only on his act.

### A-12 — The Holdat positional corpus exists as profiles, not as a keyed dataset

- **Kind:** missing node.
- **Missing piece:** the Holdat dataset itself in
  keyed, pinned, citable form — a corpus node. The
  adoption record names "WP3 Holdat CSV + GPU
  environment" as blocked legs; Specs 015/019 studied
  the Holdat–ICIT disagreement from positional
  profiles, and the cross-compilation line (A-03) has
  only ever adjudicated profiles. This scan did not
  independently verify which artifact is absent; the
  adoption record is the citation for the block.
- **Why its absence blocks convergence:** two legs
  wait on it — Cluster B's WP3 re-evaluation (B-03)
  and any ground-truth check of the profile
  disagreement. A disagreement between profiles of a
  corpus nobody can cite cannot be settled at the
  level of the corpus.
- **Evidence:**
  `files/2026-11-04-spec088-adoption-full-picture-map.md`
  §4 (goal-workspace adoption record: WP3 blocked
  legs); `records/taxonomy-v0-draft.md` §3 Domain 1
  (015/019 titles).
- **Candidate:** acquisition and keying of the Holdat
  corpus with a pin, under the program's corpus
  discipline.
  - **Falsifier:** keyed and pinned, the corpus
    reproduces the 015/019 profile disagreement
    identically → the disagreement lives in profile
    construction, not the data; this find closes as
    not-the-blocker and B-03's block stands on the GPU
    environment alone.
  - **Type:** in-house re-derivation.
  - **Owner gates:** lawful access to the dataset, if
    it is not already in program hands, is an owner
    matter.

## Counts (this cluster)

Finds: **12** — missing node 2 (A-11, A-12); missing
edge 3 (A-03, A-04, A-10); thin evidence 5 (A-05,
A-06, A-07, A-08, A-09); stale bookkeeping 2 (A-01,
A-02). Candidates: **14** (A-06 carries three, one per
route). Find-list items consumed: 20 of 28
`bundle_less_study` (A-01: 13; A-02: 7).

## What this cluster did not scan

Per-study prose outcomes of the 20 bundle-less studies
(C2: the register's oracle reads them at disposition
time; the scan does not convert them into standings).
The signary frame-size disagreement across compilations
(a documented frame dependence carried by registered
frame choices, not one of the four kinds on this
scan's inputs). WP5's per-anchor detail beyond the
audit JSON's own fields.

*This does not establish:* that these are all the gaps
in those domains — only that every find recorded is in
the registered shape. (T501's line.)
