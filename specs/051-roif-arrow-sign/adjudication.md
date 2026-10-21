# Spec 051 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign plan,
>    approved by the owner as written on
>    2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`).
>    Design D-10 is campaign member 9. The plan's
>    embedded decisions govern this draft: **E-6**
>    (shared assets live inside their builder
>    specifications — Asset B is built and frozen
>    inside Spec 047; this spec consumes it),
>    **E-2 / R-7 / Part 8** (the Roif experiments
>    execute; their results are computed and held,
>    never surfaced, until the owner's separate
>    publication act), and **R-2** (assets are
>    built once and consumed by identical digest).
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-10 found **RIPE** — "Sign 391's
>    per-site counts are on record, and its one
>    shared input (D-09's site-function
>    classification) is cited-data desk work
>    buildable in the same programme — not a
>    missing dataset."
> 3. **The Roif preprint verification of
>    2026-10-21**
>    (`~/workspace/research_notes/roif-preprint-check-2026-10-21.md`):
>    Avishai Roif's work is publicly posted on
>    Academia.edu in two 2025 versions, full
>    text, citable by URL. This satisfies the
>    Roif gate's evidence condition; under the
>    campaign plan it does **not** clear
>    publication, which remains the owner's
>    separate GATE act (spec §9, claim
>    F051-C19).
>
> These inputs commission this **draft**. They
> are not a freeze order and not an execution
> order for Spec 051: both remain separate
> owner decisions. In the campaign's dependency
> order this spec's freeze follows Spec 047's
> freeze, because its freeze takes Asset B's
> digest as its pin (claim F051-C10).

## 1. The adopted basis (operative substance)

- **The design.** D-10 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
  §D-10): per-site arrow-sign shares (M391
  occurrences over site inscriptions) compared
  across the frozen site-function classes, with
  an exact test and a permutation control, and
  the same shares regressed on site size alone
  to score the case-ending rival; criteria fixed
  in advance (SUPPORTED at gateway/border share
  over the great-city share by a ratio of at
  least 1.5 at the 5% level, with class adding
  predictive power beyond size; NOT SUPPORTED at
  ratio at or below 1.0, or size alone explaining
  the pattern; INCONCLUSIVE between, or fewer
  than 3 gateway/border sites carrying the sign);
  the two readings scored separately because both
  roles could coexist.
- **The claim.**
  `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003`
  — the arrow sign (tīr) as border enforcement
  or guild authority, standing UNTESTED under
  Phase-104's RULE-SITE (spec §1, claims
  F051-C02, F051-C03).
- **The shared asset.** Asset B, the
  site-function classification, is built by
  Spec 047 (campaign E-6) and consumed here by
  digest pin (campaign R-2). Spec §4 restates
  the consumed contract; §4 below records the
  consumer-side decisions, and §3 records where
  the design's wording and the contract's
  groupings differ and how the draft carries
  the difference — as a stated boundary, never
  as a silent re-mapping.
- **The hold.** Campaign R-7: this member's
  records are internal; reporting names it
  only as "executed — held under the Roif
  gate"; no result content leaves the program's
  internal records until the owner's publication
  act (spec §9).

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
against `main` at `83b6a563` (re-read at the
start of the drafting act, per instructions;
the current head, a merge of PR #241 recording
Spec 030's Ask 2 ruling):

- **Design D-10** — read in full: the question,
  the claim's hypothesis, the falsifier as the
  design states it (gateway/border share at or
  below the great-city share once totals are
  controlled), the data (the frozen
  classification; sign 391 counts per site
  re-derived from the database at run time under
  H16; site totals as the exposure control; the
  case-ending rival measured in the same run),
  the method, the criteria verbatim, the named
  confounders, and the limits (no meaning
  conclusion; both roles could coexist; the two
  scores reported separately).
- **The claim's record** — read in the pinned
  claim file (SHA-256 `bc22d6f0…`): `manual_003`
  carries normalised claim, proposed value
  *tīr* (enforcement at borders), falsification
  condition "If arrow sign does not cluster at
  gateway/border sites", status untested, and a
  not-understood text naming the missing
  classification and the counts' great-city
  lean. The same document's `manual_001` entry
  is Spec 047's claim; the two are distinct and
  this draft touches only `manual_003`.
- **Phase-104** — read in the pinned evaluation
  (SHA-256 `2d0b83e8…`, matching Spec 047's
  corrected pin for the same file): `manual_003`
  stays untested, rule RULE-SITE, with the
  nine-site M391 Holdat distribution and the
  CASE_MARKER_SUFFIX role note as its evidence
  (spec §1). The nine counts sum to **193**.
- **The roles file** — read in the pinned file
  (SHA-256 `3f1c24ed…`): M391 is
  CASE_MARKER_SUFFIX, mapped to TERMINAL,
  `is_ending` true, count **193** — agreeing
  with the Phase-104 distribution total. Two
  independent records therefore carry the
  census total; gate 0.4 puts both at risk
  against a fresh derivation.
- **The gazetteer spine** — the pinned file
  recomputes to `5ac76a30…`; its 36 rows carry
  exactly **30 distinct `program_site_id`
  clusters** (counted at this draft). The
  cluster list was read in full: it contains
  Mohenjo-daro, Harappa, Lothal, Surkotada,
  Kalibangan, and Banawali — six of the nine
  census sites — and **no** cluster for
  Dholavira, Chanhu-daro, or Rakhigarhi. On the
  recorded counts, 28 of 193 M391 occurrences
  therefore sit outside Asset B's universe by
  rule (spec §5.1, claim F051-C11). Spec 047's
  adjudication records the same spine
  observation from its side (Chanhu-daro and
  Dholavira named there).
- **Asset B's contract** — Spec 047's `spec.md`
  §4 read in full on its draft branch
  (`spec-047-roif-ledger-distribution-draft`,
  PR #246), with §5 for the ledger-list context
  this spec does not consume: the file form
  (§4.1: path, exactly 30 rows, the seven
  fields, the `source_a`/`source_b` shape), the
  six classes and the §4.2 groupings fixed
  "for the test and for D-10's use" (pooled
  `ADMIN-TRADE-GATEWAY` = {gateway/border,
  administrative, port/trade}; contrast =
  {domestic, ritual}; `mixed/unknown` in
  neither), the two-source agreement rule and
  the testable definition (§4.3: AGREED and
  class ≠ `mixed/unknown`), the dispute statuses
  (§4.4: DISAGREED, SINGLE-SOURCE, NO-SOURCE,
  AGREED-`mixed/unknown`), the freeze point and
  digest pinning with the §4.6 consumer rule
  (dependents name the digest in their §2,
  re-assert it at step 0, mismatch stops the
  consumer as INVALID; a status/class change
  makes the asset unsound and closes dependents
  as not-run), and the build gates (§4.7).
  Spec 047 is itself a draft at this writing:
  its freeze may change its own text, and this
  spec's freeze must re-read the merged §4
  before taking the pin (§5, item 6).
- **Input pins** — recomputed at this draft from
  `main` at `83b6a563…`, each by **two
  independent routes** (the contents raw route
  and the git-blob route through the commit's
  tree), agreeing byte-for-byte on every file:
  claim file `bc22d6f0…`, Phase-104 evaluation
  `2d0b83e8…`, gazetteer `5ac76a30…`, roles file
  `3f1c24ed…`, anchors `df0cf620…`. The
  two-route discipline is deliberate: Spec 047's
  first drafting pass carried four single-route
  pins that did not survive re-computation, and
  its correction note is the precedent this
  draft follows rather than repeats.
- **Defect 1 found at draft (recorded, not
  repaired).** The one per-symbol site-distribution
  file on `main` that a drafter would reach for
  first — `data/raw/other_sites/holdatllc_core_symbol_site_distribution.csv`
  (SHA-256 `fc05e552…`, read at this draft) —
  covers five sites only (Chanhu-daro, Harappa,
  Kalibangan, Lothal, Mohenjo-daro) and its
  symbol rows run M390, M392 with **no M391 row
  at all**. It therefore cannot reproduce the
  §1 census and is not the counting layer; spec
  §2 says so explicitly and claim F051-C12
  registers the consequence (layer identified,
  exported, and pinned at step 0 under a
  reproduction gate, following the Specs
  044/048 database-posture precedent).
  Repairing or extending that file is not part
  of this spec.
- **Defect 2 found at draft (a design/contract
  difference, carried as a boundary).** The
  design states its comparison as gateway/border
  against "the great-city sites" and its
  hypothesis as gateway/border against
  "elsewhere"; Asset B's fixed vocabulary has
  neither a great-city class nor an elsewhere
  class. The draft does not silently re-map
  (spec §4.2, claim F051-C08, DD-051-1): the
  primary ratio runs on §4.2's fixed groupings,
  "great-city" is operationalised as the
  administrative class with the translation
  stated wherever the comparison is stated,
  size never defines a class, and the literal
  border-versus-city discrimination survives as
  the R_city verdict clause. If either freeze
  judges the translation wrong, it overturns it
  openly; neither the design nor the asset is
  amended to fit.
- **Phase-number state** — Phase-403 (Spec 039)
  is the latest execution phase allocated on the
  merged record; Specs 040–048 allocated none at
  draft. Spec 051 allocates none at draft
  (DD-051-6).
- **Not done at draft, by design** — no site
  class has been read for a test (Asset B does
  not exist yet); no share, ratio, regression,
  or permutation quantity has been computed; the
  counting layer has not been exported; no code
  was written or run; the AEE hooks have not
  run; nothing was filed with OSF. The §1 census
  is quoted from the pinned records, not
  re-derived — re-derivation is gate 0.4's
  execution act.

## 3. Acceptance tests derived twice, independently

Per the doctrine, the acceptance test for each
claim was derived **twice, independently, from
the requirement alone**: Derivation A worked
from the design text (D-10) and the claim's
Phase-104 record only; Derivation B worked
from the approved campaign plan (Parts 2–5, 8,
12), the triage entry, and Spec 047's §4
contract only. The two derivations agreed on
the tests for 15 of the 20 claims as drafted.
The five disagreements, and their resolutions,
are recorded here; the register's
`falsification_tests` carry the resolved form.

1. **The comparison grouping.** A (from the
   design) derived the primary test as
   gateway/border sites alone against the
   great-city sites — the design's literal
   words. B (from Spec 047 §4.2, which fixes
   the groupings "for the test and for D-10's
   use") derived the pooled
   `ADMIN-TRADE-GATEWAY` against {domestic,
   ritual} comparison. **Resolution:** B for the
   primary ratio, A preserved as a verdict
   clause. The contract governs consumption
   (campaign R-2: dependents test against the
   identical asset, groupings included; a
   consumer that re-groups has a different
   asset in effect), so R runs on §4.2's
   groupings — but the design's falsifier is the
   claim's own, so R_city (gateway/border over
   administrative) is a clause of the §5.4
   partition: R_city ≤ 1.0 returns NOT SUPPORTED
   even when the pooled ratio is high, because
   a pooled excess driven by the great cities
   fits the rival reading, not the border one.
   The difference is stated as a boundary in
   spec §4.2 and claim F051-C08 (DD-051-1).
2. **What "great-city sites" means.** A read the
   phrase as a size-defined set (in effect, the
   largest sites — the design's own gloss is
   "mostly the great cities" over raw counts).
   B read it as the administrative class, the
   only centre-like class the asset contains.
   **Resolution:** B for the verdict. A
   size-defined verdict class would be circular
   — site size is the rival explanation §5.3
   tests, and a class defined by size cannot
   then beat size in a fair comparison. The
   five largest test-population sites are
   reported descriptively as a sensitivity
   (claims F051-C08, F051-C18; DD-051-2).
3. **Permutation non-rejection at a high
   ratio.** A, following the sibling Spec 047's
   partition, derived "R ≥ 1.5 but p ≥ 0.05 →
   NOT SUPPORTED" (D-09's text states that
   clause). B, from D-10's text alone, derived
   INCONCLUSIVE: D-10 fixes NOT SUPPORTED as
   ratio at or below 1.0, or size alone
   explaining the pattern, and non-rejection is
   neither. **Resolution:** B; the design
   governs substance, and the divergence from
   the sibling partition is recorded in spec
   §5.4 and claim F051-C16 rather than smoothed
   over (DD-051-3).
4. **The counting layer.** A (from Spec 047's
   precedent) named the pinned Yajnadevam-compiled
   layer as primary. B (from the Phase-104
   record) named the Holdat corpus: the census
   of record is a Holdat distribution, its total
   (193) matches the Holdat roles file, and the
   design says the counts are "re-derived from
   the database at run time." **Resolution:** B.
   The Yajnadevam layer's numbering is not the
   M-numbering the census is stated in; counting
   it would test a crosswalked reconstruction,
   not the recorded census. The Holdat layer is
   the layer of record, pinned at step 0 under
   an exact-reproduction gate (claim F051-C12;
   DD-051-4), and the second layer's role is
   OPEN for the freeze (§5, item 5) — the same
   posture Spec 047 took for its own second
   layer, not a silent pluralisation.
5. **Whose thinness floor binds.** A read Spec
   047's adjudication (§5, item 3 — which leaves
   "D-10 against a thin Asset B" open) together
   with its §6.3 gate as importing the 12-testable-
   site floor into D-10: below 12 testable sites,
   both tests close on the classification. B
   read D-10's own floors as complete: the
   design fixes exactly one floor (fewer than 3
   gateway/border sites carrying the sign →
   INCONCLUSIVE) and the empty-side rule this
   draft adds by Spec 047's DD-047-2 precedent.
   **Resolution:** B (DD-051-5). Spec 047's
   DD-047-1 already decides that a thin asset
   still freezes; the 12-site figure is a
   property of D-09's test (a 30-site share
   ratio), not of the asset, and D-10's test —
   one sign's shares — states its own floor.
   This draft therefore answers Spec 047's open
   item from the consumer side: D-10 proceeds
   under its own floors against a frozen Asset B
   of any testable count. Both freezes are asked
   to confirm or overturn openly (§5, item 3).

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-051-1 — The §4.2 groupings carry the
  primary; the design's literal comparison
  carries a verdict clause.** R runs pooled
  against contrast exactly as Spec 047 §4.2
  fixes them for D-10's use; R_city
  (gateway/border over administrative) is
  pre-registered in §5.2 and clauses §5.4 in
  both directions (R_city > 1.0 required for
  SUPPORTED; R_city ≤ 1.0 returns NOT
  SUPPORTED). Grounds in §3, disagreement 1
  (claims F051-C08, F051-C13, F051-C16; spec
  §4.2 boundary note).
- **DD-051-2 — "Great-city" is the
  administrative class, never a size set.**
  Grounds in §3, disagreement 2 (claim
  F051-C08). The five-largest description is a
  sensitivity, not a class.
- **DD-051-3 — Non-rejection is INCONCLUSIVE
  here.** D-10's NOT SUPPORTED clauses are
  exhaustive as the design states them; Spec
  047's stricter clause is not imported.
  Grounds in §3, disagreement 3 (claim
  F051-C16, spec §5.4).
- **DD-051-4 — The Holdat layer is the counting
  layer of record, pinned at step 0.** No file
  pin at draft; gate 0.4's exact census
  reproduction is the identity test. Grounds in
  §3, disagreement 4 and §2, defect 1 (claim
  F051-C12).
- **DD-051-5 — This spec's floors are its own.**
  The gate-0.6 floors (≥3 gateway/border
  carriers; both sides non-empty) are the whole
  thinness rule for this test; Spec 047's
  12-site gate is not imported. Grounds in §3,
  disagreement 5 (claim F051-C17). This is the
  consumer-side answer to Spec 047's
  adjudication §5, item 3.
- **DD-051-6 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-051-7 — Evidence carries `observed_at`
  from the draft.** The cited facts were
  verified first-hand today; Spec 038's freeze
  had to retrofit this field as a factual
  completion. Including it now is the same
  completion, done at the act that actually
  observed the records.
- **DD-051-8 — The rival regressions weight
  sites equally.** Sites are the units of the
  design's comparison ("relative to each site's
  total inscriptions"), and equal weighting
  keeps a large site's share from counting as
  many observations. The freeze may substitute
  inscription weighting openly, with the
  verdict partition re-stated if it does (claim
  F051-C15, spec §5.3).

## 5. OPEN — what the freeze decision is asked to decide

1. **DD-051-9 (proposal): whether the frozen
   spec files its own OSF registration** —
   proposal: yes, under campaign decision E-1
   (every specification in the pass registers
   at its freeze, following the Specs 036–039
   pattern), so the shares definitions, the
   groupings translation, and the verdict
   partition are timestamped outside the repo
   before execution. Nothing is filed at draft.
   Note the Roif gate: an OSF registration files
   this spec's frozen *contract* (a design
   text), not results; the freeze confirms that
   reading against R-7 before filing, as Spec
   047's freeze is asked to.
2. **The permutation and class-addition seeds.**
   Spec §5 fixes the shuffle counts (9,999) and
   the level (5%) for both permutation tests;
   the seed values are set at the freeze and
   recorded in the freeze record, before any
   share exists.
3. **The thin-asset reading, confirmed at both
   freezes (DD-051-5).** Spec 047's freeze is
   asked the same question from the builder
   side (its adjudication §5, item 3). The two
   freezes must land on one answer, recorded in
   both records; a disagreement between them
   blocks this spec's freeze, not its draft.
4. **The Fisher exact test's status.** Draft
   position: computed and reported, not
   verdict-bearing (claim F051-C14). The freeze
   confirms, or makes it a stated co-condition
   of SUPPORTED with the partition re-stated
   openly in the frozen text.
5. **The second corpus layer's role.** Draft
   position: the Yajnadevam-compiled layer is
   not consumed (spec §2). The freeze rules
   whether a crosswalked second run is a stated
   sensitivity — and if so, names the crosswalk
   and the numbering rule in the frozen text —
   or the layer stays unused.
6. **Contract-drift check against Spec 047's
   freeze.** Spec 047 is a draft at this
   writing. This spec's freeze re-reads Spec
   047's merged §4 as frozen; if the frozen
   contract differs from the draft contract
   restated in spec §4 (fields, classes,
   groupings, testable rule, or the §4.6
   consumer rule), the difference is decided
   openly at this spec's freeze — adopted with
   the partition re-checked, or the draft is
   withdrawn for re-drafting. It is never
   absorbed silently.
7. **The counting-layer export form.** Gate 0.4
   pins whatever export the execution produces.
   Proposal: the freeze names the canonical
   export form (the database export's file form
   and sort order) so the step-0 digest is
   reproducible by a later reader, rather than
   leaving the form to the execution act.

## 6. What the freeze decision is asked to decide (summary)

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every §2
   pin re-asserted against the merged record,
   Asset B's digest taken as this spec's pin
   from Spec 047's freeze and step-1 outcome
   records, the OPEN items of §5 decided, and
   DD-051-1, DD-051-3, and DD-051-5 confirmed or
   openly overturned — or decline, leaving
   `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003`
   UNTESTED with the classification built for
   its sibling test and this claim's own test
   unrun against it.
2. Under the campaign, this spec's freeze
   follows Spec 047's freeze in dependency
   order (builders before dependents), and its
   execution follows Spec 047's step-1 asset
   freeze in execution order (asset builds,
   then dependent executions).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
