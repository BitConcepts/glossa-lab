# Spec 088 — Stage S5, Cluster B scan: claim families + contact zone

Executed 2026-11-04 on branch `feat/088-s5-scans` off
origin/main `893a426a`. Task T502. Finds are exactly one
of the four registered kinds; every candidate carries a
one-line falsifier and an honesty-rule type (C088-10,
C088-12). No prose-only standing is used as data
anywhere in this record (C2, C088-17).

## Inputs (read first-hand this scan)

- `glossa-indus/map/program-map.json` coverage block:
  Domain 3 (Claim families by study line) 40 studies /
  568 claims (studies open 38 / unjudged 1 / restricted
  1; claims positive 2 / negative 6 / open 560);
  Domain 4 (Contact zone & external corpora) 2 studies
  / 33 claims (studies open 1 / unjudged 1).
- `glossa-indus/map/program-map-finds.json`: this
  cluster's items are the 9 `extracted_null_falsifier`
  finds (B-05), 2 `bundle_less_study` finds in these
  domains (B-08, B-12), and the 1 `restricted_node`
  find (not scanned — carried to S6, see the counts
  section).
- `glossa-indus/matrix/matrix.json` coverage block
  (current artifact): rows 876, rows with cells 862,
  empty rows 14; unused study columns 6 of 10 (046,
  047, 051, 056, 063, 064); study outcome blocks not
  bearing 7; cells by study class 7.
- Repair records: `docs/repair-2026-10-26/README.md`
  and `docs/repair-2026-10-26/baseline-and-dispositions.md`
  (§2 WP2, §3 WP3, §4 WP4);
  `docs/repair-2026-10-26/wp9-study-preparations.md`
  (contact-zone preparation, Study A).
- `records/taxonomy-v0-draft.md` §3–§4 (D-design table
  with successor edges in titles; extracted-document
  assignments).
- Pre-answered legs, cited not re-derived (scan plan):
  WP4's count (0 of 184); the extracted-claim falsifier
  split (14/23); the WP5 census where it touches claim
  families (B-01's containment cross-reference).

## Classification of Domain 4's thinness (per the scan plan's instruction)

The domain holds 2 study nodes for the whole contact
zone. That smallness is **not** honest smallness, on
the records: its one substantive literature line (the
Laursen/Gulf catalog work) has no ledger claims at all
(B-10); its one discriminating study is prepared but
gated on a dataset that does not exist in program
hands (B-09); and its one independent-attestation
study is bundle-less (B-12). The domain is thin
because its content was never ledgered, not because
the contact zone was worked and found small. The three
finds named carry the classification; no separate
"domain size" find is recorded.

## Finds

### B-01 — WP4: zero of 184 Parpola comparisons are eligible as independent validation

- **Kind:** missing edge.
- **Missing piece:** a single comparison, of the 184
  in the Mahadevan–Parpola crosswalk, whose reading is
  independently sourced. The provenance classification
  is total: **0 eligible**; 116 entries carry the
  project's own readings copied under a "Parpola 1994"
  source label (the Phase-96 mechanism, baseline §4.3).
  Per-entry primary-source locators have never been
  recorded (baseline §4.2), and the file's own partial
  counts (113 entries attested by an independent
  in-repo source) attest sign pairings, not readings —
  they are not the eligible count (baseline §4.4).
- **Why its absence blocks convergence:** this is the
  program's flagship outside-reproduction hole, the
  honesty rule's standing instance (C088-12). Every
  "Parpola agrees" relation in the lineage is circular
  — it shares the derivation it would confirm — so the
  edge from the anchor claims to the field's standard
  comparator carries no weight, and "independent
  Parpola validation" was one of the four advertisings
  the repair brief contained (baseline §1.5).
- **Evidence:** `docs/repair-2026-10-26/README.md`
  (crosswalk_provenance result: 0 eligible of 184; 116
  copied); `docs/repair-2026-10-26/baseline-and-dispositions.md`
  §4.2, §4.3, §4.4, §4.A; `claims.md` C088-12.
- **Candidate:** build the eligible set — entry-level
  primary-source locators for all 184 entries, and
  independent coding of the readings from those
  primary sources by a coder who did not derive the
  project readings.
  - **Falsifier:** the locator pass finds every
    entry's reading traceable to the project's own
    derivation → the eligible count stays 0 and the
    gap re-registers as structural (no independent
    Parpola comparison exists to be had from this
    crosswalk), not as an unfinished task.
  - **Type:** independent confirmation.
  - **Owner gates:** the locator pass is in-house work,
    but its product counts as independent only if the
    coding is independent — an outside coder is an
    owner act. The register must not mistake the pass
    for the confirmation.

### B-02 — WP2: the phonotactic certification leg was never supplied

- **Kind:** thin evidence.
- **Missing piece:** the linguist-reviewed rule set,
  and with it the corrected re-run. The corrected
  checker exists (`phonotactics_v2`); what does not
  exist is (a) the linguist's establishment of which
  restrictions belong to the proposed historical
  language vs later Tamil (baseline §2.4 — "WP2's
  certification wording stays gated on it"), and
  (b) any certified run of the corrected checker over
  the dependent population. The repair record's
  position: "Dependent corpus claims remain
  unvalidated until a corrected analysis is run under
  a linguist-reviewed rule set," and the "zero
  violations" quantity was withdrawn, not replaced
  (baseline §2.10's containment; the overlay holds the
  dependent claims at `invalid_method`, §2.A).
- **Why its absence blocks convergence:** every claim
  whose support passes through the Phase-58 checker
  lineage — including Cluster A's A-06 route 2 — stands
  on an uncertified arm. The program cannot state a
  phonotactic violation count in either direction:
  the old count is withdrawn and no corrected count
  exists.
- **Evidence:**
  `docs/repair-2026-10-26/baseline-and-dispositions.md`
  §2.4, §2.A, §2.10; `docs/repair-2026-10-26/README.md`
  (phonotactics_v2; "What this patch does not do").
- **Candidate:** linguist certification of the rule
  set, then the v2 re-run over the strict core and the
  dependent claims.
  - **Falsifier:** under certified rules the v2
    checker returns violations > 0 for the strict
    core → the dependent claims reclassify downward
    and the thinness converts to measured
    contradiction for the affected family; a zero
    count under certified rules is what closes it.
  - **Type:** in-house re-derivation (the closing
    study is the program's own re-run; its gating
    input is external — typed by the study, not the
    input).
  - **Owner gates:** the linguist engagement is an
    owner act (a named human; DATA-BLOCKED in the
    repair brief's terms until supplied).

### B-03 — WP3: the corrected site-statistics re-evaluation was never run

- **Kind:** thin evidence.
- **Missing piece:** the re-evaluation of the
  site-statistics population under the corrected
  implementation. The Phase-69 routine could emit
  only p ∈ {0.0, 0.5, 1.0} (baseline §3.1);
  `site_stats_v2` exists with a real p-value and
  reference values on record ([[13,7],[7,13]] →
  χ² 3.6, p ≈ 0.0578 — §3.3). No equivalence design
  exists (no prespecified margin, §3.5), the
  invariance language was contained rather than
  established (README: "no site-invariance equivalence
  has been established"), and current displays hide
  the insufficient-data remainder — 29 of 94 strict,
  81 of 171 full — outside the tested denominator
  (§3.A). The adoption record names the run's blocked
  legs: a Holdat CSV and a GPU environment (§4;
  the Holdat dependency is Cluster A's A-12).
- **Why its absence blocks convergence:** the
  site-effect family of standings (the "no site
  effect" line that Specs 028/040/060 work in) rests
  on outputs the staged routine cannot reproduce.
  Nobody can say which historical site verdicts
  survive correction, so the family can neither be
  relied on nor retired.
- **Evidence:**
  `docs/repair-2026-10-26/baseline-and-dispositions.md`
  §3.1, §3.3, §3.5, §3.A; `docs/repair-2026-10-26/README.md`
  (site_stats_v2); `files/2026-11-04-spec088-adoption-full-picture-map.md`
  §4 (blocked legs).
- **Candidate:** the corrected re-evaluation over the
  full population — remainder inside the denominator —
  with the equivalence margin prespecified before
  outcomes are seen.
  - **Falsifier:** v2 disagrees with the historical
    outputs beyond the declared tolerance on the
    reference tables → the historical site verdicts
    reclassify wholesale, and the find converts from
    thin evidence to contradicted for the affected
    family.
  - **Type:** in-house re-derivation.
  - **Owner gates:** the full-population arm waits on
    A-12's Holdat leg and a GPU environment (program
    infrastructure; the Syncyard/desktop route is the
    program's own act).

### B-04 — Three extracted documents have no testing line (12 claims)

- **Kind:** missing node.
- **Missing piece:** a study line that takes up the
  claims of `ancient_writing_and_modern_technologies`
  (4 claims), `the_archaeology_and_epigraphy_of_indus_writing`
  (2), and `indus_valley_script_deciphered_from_myth`
  (6). The taxonomy assigns all three to the
  Extracted literature claims subdomain expressly
  because no testing line exists, and records that
  the fact "is itself a scan input." Of the 12 claims,
  9 sit at status untested; 3 (all in the myth
  document) carry negative standings from their
  extraction records that no study has ever re-tested.
- **Why its absence blocks convergence:** extracted
  claims are the program's picture of what the
  literature asserts. Twelve of the 23 were never
  connected to the testing machinery at all, so the
  picture holds assertions the program has neither
  confirmed nor refuted with its own instruments —
  including sign-validation claims of exactly the kind
  the D-designs exist to test for other documents.
- **Evidence:** `records/taxonomy-v0-draft.md` §4
  (assignments and the no-testing-line note);
  program-map claim nodes by document (statuses
  counted this scan).
- **Candidate:** one testing-line study per document
  (or a single study with three arms), taking each
  claim to a registered corpus test where a test
  exists.
  - **Falsifier:** the claim-by-claim pass finds
    claims admitting no corpus test (purely
    historiographical assertions) → those claims
    disposition as not-testable and the node shrinks
    to the testable subset; the falsifier is expected
    to fire for at least the myth document's framing
    claims.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

### B-05 — Nine extracted claims carry no falsifier

- **Kind:** thin evidence. (The template's named
  thin-evidence case: falsifiers absent.)
- **Missing piece:** a falsifier — or a recorded
  disposition — for each of the 9 claims enumerated
  in the find list (4 in
  `ancient_writing_and_modern_technologies`, 2 in
  `indus_valley_script_deciphered_from_myth`, 2 in
  `the_archaeology_and_epigraphy_of_indus_writing`,
  1 in `without_kings_or_conquests`). Falsifier
  coverage stands at 867/876 with the extracted
  population at 14/23; the bundle population is
  complete (853/853). Consumes all 9
  `extracted_null_falsifier` finds. Per the scan
  plan, this is a disposition item, not a measurement
  item.
- **Why its absence blocks convergence:** a claim with
  no falsifier cannot move by evidence in either
  direction; nine of the program's 23 literature
  claims are structurally stuck at their extraction
  standings.
- **Evidence:** `glossa-indus/map/program-map-finds.json`
  (9 finds, enumerated); program-map coverage block
  (null_extracted_claims list; falsifier coverage);
  `records/stage-s2-record.md` (enumeration);
  `files/2026-11-04-spec088-adoption-full-picture-map.md`
  §4 (the disposition framing).
- **Candidate:** falsifier backfill by re-derivation
  from each claim's source document, claim by claim.
  - **Falsifier:** a claim whose source text states
    no observation that would count against it →
    backfill is impossible for that claim; it remains
    a counted null by disposition, and the find
    closes only when all 9 are filled or
    dispositioned.
  - **Type:** in-house re-derivation.
  - **Owner gates:** the accept-and-record
    disposition, where backfill fails, is an owner
    act at ratification (T603).

### B-06 — D-design outcomes are unconsumed in the generated layer; successor structure is unrecorded at claim level

- **Kind:** missing edge.
- **Missing piece:** the consumption/residue record
  for the D-design line. Two faces, both from the
  generated layer: (a) of the matrix's 10 study
  columns, 6 are unused (046, 047, 051, 056, 063,
  064), 7 study outcome blocks are recorded as not
  bearing, and study-class cells total 7 — study
  outcomes exist that no claim cell consumes under
  matrix-defs v1; (b) the taxonomy's title record
  carries successor edges for 045→069, 046→064,
  050→071, 053→068, 056→063, 057→065, 070→074, but
  D-designs 044 (D-02), 047 (D-09), 051 (D-10), 052
  (D-01), 054 (D-08), 055 (D-15) carry no successor
  edge, and whether each closed cleanly or left an
  open residue is recorded nowhere at claim level.
- **Why its absence blocks convergence:** a closed
  design's residue can drop out of the program
  silently. The map shows the D-design studies as
  open bundles of draft claims; it cannot show that a
  question was finished, abandoned, or inherited —
  the successor structure is the program's memory of
  its own source-thesis tests.
- **Evidence:** `glossa-indus/matrix/matrix.json`
  coverage block (unused columns; outcome blocks not
  bearing; cells by class);
  `records/taxonomy-v0-draft.md` §3 Domain 3 table
  (successor edges in titles).
- **Candidate:** a D-design residue census over the
  six no-successor designs' outcome records and the
  seven non-bearing outcome blocks, recorded as
  claim-level edges or explicit terminal dispositions.
  - **Falsifier:** every one of the six records
    states a terminal verdict with no named residue
    → the find downgrades to a bookkeeping note and
    closes.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

### B-07 — Fourteen extracted claims are isolated rows in the evidence matrix

- **Kind:** missing edge.
- **Missing piece:** any edge at all for 14 extracted
  claims — rows with zero cells (rows with cells 862
  of 876): `ancient_writing…sign_val_0002/0003`,
  `indus_valley_script_deciphered_from_myth…manual_001–004`,
  `parpola_2010_dravidian_solution…manual_001/002`,
  `the_archaeology_and_epigraphy…sign_val_0001/0002`,
  `without_kings…manual_001/002/004/005`. They have
  program-map nodes but no recorded relation to any
  document, study, or anchor column — including the
  Parpola document's own two claims, the subject of
  B-01.
- **Why its absence blocks convergence:** the matrix
  layer cannot weigh what it cannot reach. Fourteen
  literature claims — over half the extracted
  population — are invisible to the program's
  evidence machinery while remaining visible on the
  map.
- **Evidence:** `glossa-indus/matrix/matrix.json`
  coverage block (empty_rows, enumerated);
  `specs/086-winning-combination-adoption/stage-2-record.md`
  (the same 14 at generation).
- **Candidate:** a cell-construction pass deciding,
  per claim under the defs, whether its isolation is
  a registered defs consequence (non-bearing
  outcomes, the R-rules) or a construction gap.
  - **Falsifier:** the pass shows every empty row's
    isolation follows from a registered matrix-defs
    rule → the find downgrades to a defs note for
    the register, not a gap.
  - **Type:** in-house re-derivation.
  - **Owner gates:** a matrix-defs amendment, if the
    pass recommends one, is a program act.

### B-08 — Spec 024, root of the F1/F2 lineage, is bundle-less

- **Kind:** stale bookkeeping.
- **Missing piece:** `024-evidence-integration`'s
  claims bundle — or a recorded disposition that it
  is pre-ledger history. Its successors carry
  bundles: `059` is "Spec 024 F1 Rebuilt", `060` is
  "Residue of Spec 024 F2", `067` re-runs `059`. The
  lineage's root is the one member the ledger cannot
  weigh. Consumes 1 `bundle_less_study` find (the
  Domain 3 member of the 28).
- **Why its absence blocks convergence:** the F1/F2
  object-join line is one of Domain 3's live lines;
  its origin study's findings enter the successors'
  premises without ever having been ledgered
  themselves.
- **Evidence:** `program-map-finds.json`;
  `records/taxonomy-v0-draft.md` §3 Domain 3 table
  (059/060/067 titles); program-map coverage block
  (Domain 3 studies unjudged 1).
- **Candidate:** bundle backfill from 024's record.
  - **Falsifier:** 024's record contains no
    claim-shaped statements beyond what 059/060
    already ledger → disposition as history, with the
    lineage root marked superseded-by-successors.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

### B-09 — The contact-zone sequence study is prepared and gated on a transcription that does not exist

- **Kind:** missing node.
- **Missing piece:** a transcription of the CISI
  Vol. 3 inscription material — the sign sequences of
  the Gulf inscribed material, with per-sequence
  provenance — lawfully accessible under the
  program's restricted-material custody. The WP9
  preparation names it "the precise missing
  dependency," records the stop rule ("no further
  sequence-leg work until the CISI Vol. 3
  transcription exists and is lawfully accessible"),
  and carries the design condition that any future
  freeze must name the wider Dilmun corpus
  (approximately 800 seals) as its held-out arm or
  state why its design does not need one.
- **Why its absence blocks convergence:** the
  sequence leg is the contact zone's only
  discriminating test — sequence-level comparison of
  the Gulf INDUS material against the Indus corpus.
  Until the transcription exists the study cannot be
  frozen, let alone run, and Domain 4's thinness
  (the classification above) cannot change.
- **Evidence:**
  `docs/repair-2026-10-26/wp9-study-preparations.md`
  §1.2, §1.3 inputs table, Study A summary row;
  `docs/repair-2026-10-26/README.md` ("the
  contact-zone sequence study remains gated on the
  CISI Volume 3 transcription").
- **Candidate:** produce the transcription under the
  custody arrangement the program already uses for
  restricted material, pinned as the study's input.
  - **Falsifier:** the transcription is produced and
    pinned → the gate lifts and the find closes at
    the study's freeze; if lawful access is refused
    on the record, the leg dispositions as
    abandoned-by-access and the find closes as a
    recorded dead end instead.
  - **Type:** in-house re-derivation (the work
    product is the program's own transcription of an
    external corpus).
  - **Owner gates:** OWNER-GATED — CISI material is
    restricted (statistics publishable; scans never
    redistributed; custody on the owner's machines).
    The access route is the owner's; no agent route
    exists.

### B-10 — The completed Laursen catalog leg has no ledger claims

- **Kind:** missing node.
- **Missing piece:** an extraction bundle carrying
  the catalog leg's claims. The leg is complete and
  verified on its record: the Laursen 2010 Table 1
  catalog in program hands is **121 seals = 92 Gulf
  Type + 28 Gulf INDUS + 1 Gulf Linear-Elamite,
  across 29 named sites** (WP9 §1.1). But this scan's
  count over `claims.jsonl` finds zero entries
  mentioning laursen, gulf, dilmun, janabiyah, or
  arabia — the program's one completed contact-zone
  measurement exists only in preparation and
  goal-workspace records, so the map shows nothing of
  it.
- **Why its absence blocks convergence:** the
  catalog leg is the contact zone's strongest
  completed result (its negative bearing on
  contact-mechanism claims is the line's current
  standing). Unledgered, it cannot be cited by the
  matrix, weighed by the map, or inherited by any
  successor study — the completed work is invisible
  to the system it belongs to.
- **Evidence:**
  `docs/repair-2026-10-26/wp9-study-preparations.md`
  §1.1 (catalog leg verified as already run);
  `glossa-indus/ledger/claims.jsonl` (zero hits on the
  five search terms, counted this scan, 2026-11-04);
  `files/2026-10-26-laursen-table1-rebuild-completion.md`
  (goal-workspace completion record).
- **Candidate:** extraction of the catalog leg into
  the ledger through the sanctioned intake, from the
  completed rebuild record.
  - **Falsifier:** the extracted claims fail the
    research-check reproduction of the catalog counts
    (121 = 92 + 28 + 1 across 29 sites) → the bundle
    is rejected and the catalog leg's standing
    re-opens instead of entering.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none (the intake is the
    program's own act; the underlying catalog is
    published literature).

### B-11 — The taxonomy's Domain-4 note describes claim nodes the map does not contain

- **Kind:** stale bookkeeping.
- **Missing piece:** a taxonomy note that matches the
  generated picture. The v0 draft's Domain-4 note
  asserts the Gulf/Laursen line "enter[s] the map as
  claim nodes under their testing studies in Domain 3
  and as extracted claims (§4)" — but §4's table
  assigns no Gulf/Laursen document, and the map,
  derived only from the ledger, contains no such
  nodes (B-10's count). The prose expectation and the
  generated picture disagree; under C2 the map
  governs, and the prose is the find.
- **Why its absence blocks convergence:** the
  taxonomy is a builder input; a note in it that
  misdescribes the population teaches every future
  reader (and every future taxonomy amendment) a
  wrong starting picture of the program's thinnest
  domain.
- **Evidence:** `records/taxonomy-v0-draft.md` §3
  Domain-4 note and §4 table; B-10's ledger count.
- **Candidate:** correct the note at the next
  taxonomy version, recording which of B-09/B-10
  changed the picture by then.
  - **Falsifier:** a Gulf/Laursen claim is located in
    the ledger under a naming this scan's search
    missed → the find closes as a scan error,
    recorded as such in the register.
  - **Type:** in-house re-derivation.
  - **Owner gates:** a taxonomy amendment is a
    stage-record act (C088-9).

### B-12 — Spec 013, Domain 4's attestation study, is bundle-less

- **Kind:** stale bookkeeping.
- **Missing piece:** `013-tn-graffiti-crosswalk`'s
  claims bundle, or its pre-ledger-history
  disposition. It is Domain 4's only
  independent-attestation study (the CANDIDATE-tier
  sign tail's external context) and one of the 28
  bundle-less directories; its standing lives in
  prose. Consumes 1 `bundle_less_study` find.
- **Why its absence blocks convergence:** Domain 4's
  classification (above) rests partly on this: the
  domain's one study whose evidence originates
  outside the Indus corpus proper is the one the
  ledger cannot weigh.
- **Evidence:** `program-map-finds.json`;
  `records/taxonomy-v0-draft.md` §3 Domain 4 table;
  program-map coverage block (Domain 4 studies
  unjudged 1).
- **Candidate:** bundle backfill from 013's record.
  - **Falsifier:** as B-08 — no claim-shaped
    statements beyond what later records already
    ledger → disposition as pre-ledger history.
  - **Type:** in-house re-derivation.
  - **Owner gates:** none.

## Counts (this cluster)

Finds: **12** — missing node 3 (B-04, B-09, B-10);
missing edge 3 (B-01, B-06, B-07); thin evidence 3
(B-02, B-03, B-05); stale bookkeeping 3 (B-08, B-11,
B-12). Candidates: **12**. Find-list items consumed:
11 (9 `extracted_null_falsifier` in B-05; 2
`bundle_less_study` in B-08/B-12). The remaining
find-list item in these domains, the `restricted_node`
find for `072-fish-family-profiles-redesign`, is
**not scanned**: Spec 072 is name-only under a
standing owner restriction, and the restriction is by
design, not a gap. It is explicitly carried to S6
(T504's allowed disposition).

## What this cluster did not scan

Per-design prose outcomes beyond the taxonomy and
matrix records used in B-06 (C2: outcome-chasing in
prose is the register stage's oracle work, not the
scan's). The restricted study 072 (name-only by owner
order — carried to S6, above). Standings inside
Domain 3's bundles claim by claim (draft by
construction under the derivation table; the family's
thinness is scanned at the WP2/WP3/WP4 level, where
the records put it).

*This does not establish:* that thin evidence means
wrong — the census counts support classes; what they
mean is the register's judgment, reviewed by the
owner at T603. (T502's line.)
