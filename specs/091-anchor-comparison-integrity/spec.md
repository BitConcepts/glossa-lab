# Feature Specification: Anchor and Comparison Integrity — Wave 1 of the Spec 088 Gap Register (GR-088-01, GR-088-02, GR-088-03)

**Feature Branch**: `091-anchor-comparison-integrity` (build stages); this
package lands on `docs/091-wave1-draft`
**Created**: 2026-11-05
**Status**: Draft package — awaiting the owner's block approval (Stage 0, T003)
**Input**: The owner's commission in this chat, 2026-11-05: "Commission
wave 1: GR-01, 02, 03" — the first execution wave commissioned from the
ratified Spec 088 gap register v1 (ratified as a block, 2026-11-04;
closeout PR #511), executed as one spec with three workstreams. The
register's ratification commissioned nothing by itself; this spec is
the commissioning act for its three strongest entries.
**Evidence of record**: the grounding census in
`records/commission-and-grounding-2026-11-05.md`, counted and read
first-hand from the repo on 2026-11-05: the gap register entries
GR-088-01/02/03/04 in full (`glossa-indus/map/gap-register.md`); the
repair brief record (PR #421, 2026-10-26; `docs/repair-2026-10-26/` —
README, baseline-and-dispositions, anchor-support-audit.json); the WP4
provenance classification
(`backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_provenance.json`:
184 entries — 0 independently sourced, 6 used during candidate
construction, 116 project-derived, 7 unverified, 55 ineligible; eligible
for independent validation: 0); the WP5 anchor-support audit
(strict core 94 = 6 independently supported / 46 internal-only / 37
requires-revalidation / 2 insufficient / 3 expert-pending; the Phase-48
subset of 30 = 28 requires-revalidation + 2 insufficient).
**Predecessors**: Spec 088 (the gap register this spec executes from;
its honesty rule C088-12 is GR-088-01's standing instance), the
2026-10-26 repair brief (PR #421: WP4's provenance classification, WP5's
anchor audit, the corrected v2 checkers `phonotactics_v2` /
`site_stats_v2`, and the standing rule that corrections land as new
versioned artifacts with history preserved byte-for-byte), Spec 089
(run-scoped results: every re-run this spec produces is a run under
run-defs v1, cited by run id, and comparable divergences junction),
Spec 086 (the ledger, the gate, gated publication; the foundation-check
gate of constitution §III / rule H21 guards anchor data).

## Problem statement

The strict core's support is thinner than its size, and the program's
flagship external comparison is circular. The program's own audit
established both findings; this spec is the work that answers them.

- **The comparison that validates nothing (GR-088-01).** The
  Mahadevan–Parpola crosswalk holds 184 comparisons. WP4's provenance
  classification is total: **zero** are eligible as independent
  validation. 116 entries carry the project's own readings copied under
  a "Parpola 1994" source label (the Phase-96 mechanism); the staged
  citations are file-level, and per-entry primary-source locators for
  the readings have never been recorded. Every "Parpola agrees"
  relation in the lineage therefore shares the derivation it would
  confirm — the edge from the anchor claims to the field's standard
  comparator carries no weight, and no locator pass has ever tested
  whether an independent comparison exists to be had from this
  crosswalk at all.
- **The strict core's real mass is 6, not 94 (GR-088-02).** Of the 94
  strict anchors, 46 rest on internal-only support — every support line
  produced inside this program (audit derivation categories for the 46:
  GRAMMAR 20 / DEDR 17 / ICONOGRAPHIC 4 / MIXED 2 / CROSSWALK_CORPUS 2 /
  LITERATURE 1). Under the honesty rule their standings cannot be cited
  as confirmed; the independently supported mass is 6 (M044, M047,
  M124, M202, M329, M330), and every downstream claim inheriting anchor
  support inherits the thinness. No outside-reproduction pass over the
  46 has ever been run.
- **37 strict anchors hold a status the audit cannot defend
  (GR-088-03).** 28 are Phase-48 promotions: the promoting battery
  carried pass-by-default paths and promoted 30 of 30 tested (the
  remaining 2 of the 30 are the insufficient-evidence pair, GR-088-27,
  outside this spec). 5 rest on a single line (M042, M046, M108 under
  rule R5b; M176, M342 under R5c). 4 rest solely on a crosswalk or
  literature import (R5d: M087, M165, M264, M311). None of the 37 has
  been revalidated under the corrected machinery the repair brief
  built.

## Scope — what this spec builds

Three workstreams, one per register entry, sharing one disposition
discipline (append-only reclassification over frozen records) and one
honesty rule (a support class changes only when the evidence that
defines it actually lands).

- **W1 — The eligible set (GR-088-01).** (a) The locator pass:
  entry-level primary-source locators for the reading fields of all 184
  crosswalk entries, or a recorded locator-not-found outcome per entry
  after a documented search — the pass is total, no entry unexamined.
  (b) Independent coding: the readings coded from those primary sources
  by a coder who did not derive the project readings, under a recorded
  blinding protocol (D-091-1, D-091-2 — an owner act; the in-house legs
  do not wait for it). (c) The eligible set recomputed mechanically
  from locators + coding under WP4's classification rules, and reported
  as produced — including zero, in which case the gap re-registers as
  structural on the register's own falsifier. (d) The citation
  consequence: no "Parpola agrees" relation is citable as independent
  validation for an entry outside the eligible set (C091-4).
- **W2 — Outside reproduction over the 46 (GR-088-02).** A recorded
  protocol pass over the 46 internal-only strict anchors: independent
  attestation, or blind re-derivation by readers who did not produce
  the original derivations (D-091-1 — an owner act). Outcomes recorded
  per anchor, including failures. An anchor's class changes only when
  an external line actually lands; until then, citations of the 46
  carry their internal-only status and the core's independently
  supported mass is stated as the measured number (C091-6, C091-7).
- **W3 — Revalidation of the 37 (GR-088-03).** (a) Candidate 1: a
  corrected Phase-48 battery — a new versioned battery with every
  pass-by-default path removed (D-091-4) — re-run over the 28
  promotions, whose dispositions then follow the new run; the
  historical battery output is retired as evidence. (b) Candidate 2:
  corrected-checker revalidation of the 5 single-line anchors over the
  checker arms that can run (the site-statistics lineage); the
  phonotactic arm is explicitly gated on GR-088-04's linguist leg
  (D-091-6) — noted as a dependency, not absorbed: GR-088-04 is not
  part of this spec, and no phonotactic verdict is produced under
  uncertified rules. (c) Candidate 3: an independent support line for
  the 4 R5d anchors sourced outside the crosswalk lineage (an owner
  act for external sourcing), or a recorded structural outcome where
  no outside source attests the readings.
- **Dispositions.** Every status change lands as an append-only
  reclassification act and in a new versioned anchor-support audit
  (audit v2, D-091-3); the WP5 audit and the historical battery output
  are never edited. At each workstream's end, its register entry is
  amended (append-only) to its measured end state: closed,
  re-registered structural, or still open with the blocking fact named.

## Non-goals (explicit)

- **No decipherment claim of any kind.** No stage changes any anchor's
  proposed reading, any claim's verdict, or the program's standing
  position: the Indus script is not deciphered, and no outcome of this
  spec changes that. Support classes and validation statuses are the
  only quantities that move (C091-15).
- **GR-088-04 is not absorbed.** The linguist certification leg is a
  separate register entry and a separate owner act (a shortlist was
  authorized 2026-11-05; engagement and certification are later acts).
  This spec names the dependency where it binds (W3 candidate 2's
  phonotactic arm) and proceeds everywhere else.
- **Neighboring register entries are out of scope.** GR-088-12 (no
  strict anchor record states a falsifier), GR-088-14 (the 3
  expert-pending anchors M222/M362/M398), GR-088-19 (anchor trails not
  citing the corpus), GR-088-27 (the 2 insufficient-evidence anchors)
  are separate entries with their own candidates; this spec does not
  take them, and its counts never silently include them.
- **No ledger verdicts move.** Beyond the adoption intake append
  (Stage 0), this spec writes no claim verdicts; anchor dispositions
  live in the anchor audit line, not the claims ledger. Where a
  disposition change forces generated-layer regeneration, it goes
  through gated publication as usual.
- **No contact without the owner's act.** The outside coder, the
  external readers, and candidate 3's external sourcing are named-human
  engagements under the program's contact rules; no stage initiates
  contact (D-091-1).
- **The historical record is not edited.** The WP4 provenance file is
  extended by new versioned artifacts, not rewritten; the WP5 audit,
  the Phase-48 battery script, and its historical output stay
  byte-for-byte as the repair brief left them.

## Decisions

- **D-091-1 — The independence legs' humans are an owner act; the
  in-house legs do not wait.** W1's independent coding, W2's external
  readers, and W3 candidate 3's external sourcing count as independent
  only if the humans are outside the derivation lineage, and engaging
  them is the owner's act. Options: (a) the owner names and engages
  them directly; (b) the owner authorizes a shortlist (credentials,
  rates) prepared in Stage 1, contact only on his pick — the pattern
  he set for the GR-088-04 linguist on 2026-11-05; (c) wave 1 runs
  in-house legs only and the independence legs are deferred wholesale.
  *Recommendation: (b).* The locator pass, the corrected battery, and
  the site-statistics arm are months of in-house work that should start
  at adoption; the independence legs start the day he picks names, and
  a shortlist is the prepared form that makes that a one-tap act.
- **D-091-2 — The blinding protocol is full blind, filed before coding
  starts.** Options: (a) full blind — the coder sees the primary
  sources and the sign list, never the project readings or the WP4
  classifications, until their coding is filed; (b) blind to readings
  only, classifications visible. *Recommendation: (a).* A coder who can
  see which entries the project derived cannot unsee the suggestion;
  (b) would let the eligibility recomputation inherit the very
  circularity W1 exists to test. Any deviation from the filed protocol
  voids the coding it touches (C091-2).
- **D-091-3 — Dispositions land in a new versioned audit (audit v2),
  generated, with the WP5 audit frozen.** Options: (a) audit v2 — a
  versioned generator produces a new anchor-support audit carrying
  every disposition change with its act reference, WP5's audit
  untouched; (b) a free-standing overlay file of changes only.
  *Recommendation: (a).* It is the repair brief's own rule (corrections
  land as new versioned artifacts; history preserved), and a complete
  v2 census is what the register amendment and any reader needs — an
  overlay forces every consumer to fold two files forever.
- **D-091-4 — The corrected Phase-48 battery is a new versioned
  battery; the original script is frozen.** Options: (a) battery v2
  alongside the historical `phase48_medium_validation.py`, with the
  removed paths enumerated against the original; (b) edit the original
  in place. *Recommendation: (a).* Same rule as D-091-3: the historical
  battery's output is evidence about the promotions; the instrument
  that produced it must stay inspectable as it was.
- **D-091-5 — Honesty labels land per workstream, not at spec
  closeout.** The citation consequences (C091-4's eligibility classes,
  C091-7's internal-only labels, the measured supported mass) apply to
  published layers as each workstream's counts land. Options: (a) per
  workstream, through gated publication as each lands; (b) once, at
  closeout. *Recommendation: (a).* The slowest workstream is gated on
  external humans; the program's public surfaces should not carry
  unqualified "Parpola agrees" or 94-as-confirmed statements for the
  duration. (Any preprint or site *text* change still goes through the
  owner's approval of the actual text, as always; this decision covers
  the labeling obligation and its timing, not any text.)
- **D-091-6 — Candidate 2's phonotactic arm is dependency-gated, not
  blocking.** Options: (a) W3 proceeds on every arm that can run; any
  of the 5 whose revalidation requires the phonotactic checker stays at
  requires-revalidation with the GR-088-04 dependency named on its
  record, and the spec can close with that arm named-open; (b) all of
  candidate 2 waits for the linguist. *Recommendation: (a).* One
  external dependency should not hold 32 other anchors hostage; the
  register's own framing gates only "the phonotactic arm," and an
  honestly named open arm is a better end state than an untested
  blanket hold.
- **D-091-7 — Eligible entries become citable at W1's close, with
  their class attached; no extra adjudication act.** If the pass
  produces eligible entries, options: (a) their "Parpola agrees"
  relations are citable as independent validation from W1's closeout,
  every citation carrying the entry's eligibility class; (b) citability
  additionally requires a separate owner adjudication per entry.
  *Recommendation: (a).* The classification record — locators plus
  blind coding plus mechanical recomputation — is the evidence; a
  per-entry owner act would re-introduce the human bottleneck this
  spec mechanizes, and the class-on-citation rule keeps the evidence
  attached wherever the relation is used.

## Requirements (summary; the claims in claims.md are the normative text)

- **FR-091-01 — The locator pass is total** (W1; C091-1). All 184
  entries carry an entry-level primary-source locator for their reading
  fields, or a recorded locator-not-found outcome from a documented
  search.
- **FR-091-02 — Independent coding is independent in fact** (W1;
  C091-2). Coding is produced under the filed blinding protocol by a
  coder outside the derivation lineage; deviations void the coding.
- **FR-091-03 — The eligible set is recomputed, not asserted** (W1;
  C091-3). Eligibility is recomputed mechanically from the locator and
  coding records under WP4's classification rules; zero is a
  reportable, register-changing outcome.
- **FR-091-04 — Crosswalk agreement is citable only at its class**
  (W1; C091-4). No published layer cites a crosswalk agreement as
  independent validation for an entry outside the eligible set.
- **FR-091-05 — Every one of the 46 gets its outside attempt** (W2;
  C091-5). The reproduction pass covers all 46 under a recorded
  protocol, outcomes per anchor including failures.
- **FR-091-06 — Classes change only when external lines land** (W2;
  C091-6). The independently supported count is 6 plus the anchors with
  landed external lines; same-lineage re-examination moves nothing.
- **FR-091-07 — The interim labels are honest from adoption** (W2;
  C091-7). The 46 are cited as internal-only, and the core's supported
  mass as the measured number, in every published layer from adoption
  onward.
- **FR-091-08 — The corrected battery has no pass-by-default path**
  (W3; C091-8). Every credit is earned by an executed check over
  present inputs; absent inputs are not-run or fail, never credit.
- **FR-091-09 — The 28 follow the corrected run** (W3; C091-9). The
  corrected battery re-runs over the 28; dispositions follow the run;
  the historical output is retired as evidence.
- **FR-091-10 — The 5 are revalidated on the arms that can run** (W3;
  C091-10, C091-11). Corrected-checker revalidation of M042, M046,
  M108, M176, M342; insufficient support moves an anchor to
  insufficient evidence, never back to supported; the phonotactic arm
  stays dependency-gated on GR-088-04 with the dependency named.
- **FR-091-11 — The 4 get an outside line or a structural record**
  (W3; C091-12). M087, M165, M264, M311 are sourced outside the
  crosswalk lineage or recorded permanently requires-revalidation.
- **FR-091-12 — Dispositions are append-only, in audit v2** (all
  workstreams; C091-13). Frozen records are never edited; every change
  carries its act.
- **FR-091-13 — Register entries close only on their falsifiers'
  terms** (closeout; C091-14). GR-088-01/02/03 are amended to measured
  end states; spec completion alone closes nothing.
- **FR-091-14 — Nothing here is a decipherment result** (all stages;
  C091-15). Readings, claim verdicts, and the standing position do not
  move.

## Governance

Claims first (this package's `claims.md` / `aee-claims.json`,
C091-1..15), assessed under the pinned AEE before any build task starts
(Stage 0, T002 — the assessment is in `records/t002-aee-assessment.json`,
its invocation and verbatim outcome in `records/t002-note.md`).
Verdicts and citations follow program doctrine: numbers only from
records read first-hand; assessments by actually running the assessor;
CI green or the work is not done. Every execution this spec produces
(the locator pass, the battery re-run, the checker revalidations, the
recomputations) is a run under Spec 089's run-defs v1, cited by run id
in its stage record. Any change touching anchor data passes the
foundation check (constitution §III) before it lands. The owner's block
approval of this package (T003) is the ratification act for the spec,
the claims, and decisions D-091-1..7; the named-human engagements of
D-091-1 remain separate owner acts whenever they occur. The spec ends
with its closeout record (T601); a workstream left dependency-gated at
closeout (W3's phonotactic arm, if the linguist leg has not landed) is
named open there, with its register entry carrying the same state.
