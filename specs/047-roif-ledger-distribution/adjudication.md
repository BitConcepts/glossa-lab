# Spec 047 — Adjudication Record

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
>    Design D-09 is campaign member 8. The plan's
>    embedded decisions govern this draft: **E-6**
>    (shared assets live inside their builder
>    specifications — Asset B is built and frozen
>    inside this spec), **E-2 / R-7 / Part 8**
>    (the Roif experiments execute; their results
>    are computed and held, never surfaced, until
>    the owner's separate publication act).
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-09 found **RIPE** — "The Spec 027
>    gazetteer exists as the site spine it hangs
>    on, and the missing site-function
>    classification is buildable from the
>    published excavation literature as cited
>    data under the design's two-source agreement
>    rule. Corpus layers with site attribution
>    are in hand."
> 3. **The Roif preprint verification of
>    2026-10-21**
>    (`~/workspace/research_notes/roif-preprint-check-2026-10-21.md`):
>    Avishai Roif's work is publicly posted on
>    Academia.edu in two 2025 versions, full
>    text, citable by URL. This satisfies the
>    Roif gate's evidence condition; under the
>    campaign plan it does **not** clear
>    publication, which remains the owner's
>    separate GATE act (spec §10, claim
>    F047-C18).
>
> These inputs commission this **draft**. They
> are not a freeze order and not an execution
> order for Spec 047: both remain separate
> owner decisions.

## 1. The adopted basis (operative substance)

- **The design.** D-09 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
  §D-09): step 1 builds the site-function
  classification from the published excavation
  literature as cited data, on the Spec 027
  gazetteer spine, under a two-source agreement
  rule with disagreed sites listed and excluded
  by rule; step 2 tests whether inscription
  shares and the shares of the sign classes
  Roif's text names as ledger notation
  concentrate at administrative/trade/gateway
  sites, size controlled by shares, against
  criteria fixed in advance (ratio 1.5,
  permutation test 9,999 shuffles at the 5%
  level, 12-testable-site floor).
- **The claim.**
  `indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`
  — Roif's ledger thesis, decomposed per the
  design into three components of which only
  the distribution component is tested here
  (claim F047-C05).
- **The shared asset.** Asset B, the
  site-function classification, is built by
  this spec (campaign E-6) and consumed by
  design D-10 (its specification) by digest pin
  (campaign R-2). Spec §4 is the asset's
  contract; §4 below records the decisions
  that fix it.
- **The hold.** Campaign R-7: this member's
  records are internal; reporting names it
  only as "executed — held under the Roif
  gate"; no result content leaves the
  program's internal records until the owner's
  publication act (spec §10).

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
against `main` at `82b29490` (the current head
when drafting began; re-read at the start of
the drafting act, per instructions). The
branch as pushed sits on `83b6a563` — PR #241
merged while drafting was in flight — and
every pin in spec §2 was re-verified identical
at both heads (the intervening commits touch
Spec 030's record only):

- **Design D-09** — read in full: the bundled
  thesis and its decomposition ("only the first
  makes a prediction this program can test");
  the hypothesis and the falsifier as the
  claim's own record states it; step 1's data
  (every gazetteer site classed from the
  published excavation literature, two
  independent published sources per site where
  they exist, entry only on agreement, disagreed
  sites listed and excluded by rule); the six
  classes (gateway/border, administrative,
  port/trade, domestic, ritual, mixed/unknown);
  step 2's data (corpus layers with site
  attribution, as held); the two pre-registered
  measures; the criteria verbatim (SUPPORTED at
  ratio ≥ 1.5 with permutation at 5% and the
  ledger classes in the same direction; NOT
  SUPPORTED at ratio ≤ 1.0 or permutation
  non-rejection; INCONCLUSIVE between, or below
  12 testable sites, the classification then
  being the finding); and the named confounders
  (excavation/publication bias with the
  five-largest sensitivity; classification
  contestability with the each-source-alone
  rerun; circularity bar).
- **The claim's record** — read in the
  Phase-104 evaluation (pin in spec §2):
  `manual_001` stays untested, rule RULE-SITE,
  reason quoted in spec §1. The same file's
  `manual_003` entry (design D-10's claim)
  confirms the shared missing input.
- **The gazetteer spine** — the pinned file
  recomputes to `5ac76a30…`; its 36 rows carry
  exactly **30 distinct `program_site_id`
  clusters** (counted at this draft). Spec 027's
  spec was read for the gazetteer discipline
  Asset B inherits: source rows preserved,
  clustering by `program_site_id`, §6.3's bar
  on resolving conflicts by majority vote,
  §6.5's competing-assertions rule.
- **The primary layer** — the pinned CSV
  recomputes to `c02e3d7b…` from its git blob
  (the contents API returns no body for a file
  of this size; the blob route was used and the
  hash matches the pin Spec 042's draft carries
  for the same file). Its header carries `site`
  and sign-sequence columns, as spec §2 states.
  **No per-site count was computed at this
  draft** (see "Not done" below).
- **Spine-versus-corpus observation, recorded
  as a limitation, not repaired.** The spine's
  30 clusters and the corpus's site set are
  different universes: corpus sites of record
  elsewhere in the program (Chanhu-daro and
  Dholavira appear in Spec 028's population and
  in D-10's recorded counts) are **not** spine
  clusters, and several spine clusters are
  extra-regional XRONOS rows. The design hangs
  the test on the spine, so the draft does too:
  non-spine corpus sites are out-of-population
  by rule and counted in gate 0.3's census
  (spec §§3, 6.1, 8). The freeze is asked to
  confirm this reading (§5, item 4).
- **Roif source of record** — the verification
  note was read in full. Two consequences are
  built into the draft: the §5 extraction
  sources are the two Academia.edu postings
  (citations in spec §2.1), because the held
  manuscript PDF does not survive (2026-10-08
  purge scope; no copy in any checkout or
  preserved backup); and the gate's evidence
  condition is recorded as met while its
  owner-act condition remains open (spec §10).
  The program's citation of record was also
  read: `seed_citations.py`, key
  `roif_indus_ledger`, carries "Roif, A.",
  Academia.edu, year field empty, DOI empty,
  URL field carrying only the Academia.edu
  root — no document-level identifier, which
  is consistent with the verification's
  findings (the document-level URLs come from
  the verification, not from this record).
- **Defect found at draft (recorded in spec
  §2.2).** The hypothesis-model file
  `glossa-indus/hypotheses/models/roif_guild_ledger.yaml`
  carries unreliable source metadata: a
  malformed `document_id` (stray quotation
  mark) and a `doi` field matching neither
  Academia.edu posting (which have no DOIs).
  The draft cites that file for nothing but the
  existence of the program's earlier planned
  tests, and §5 never reads it. Repairing the
  file is outside this spec.
- **Phase-147 posture.** The internal
  validation record (SHA-256 `cf9dd60d…`) was
  located and its scope confirmed: it scored
  other renderings of Roif's model, on a
  different corpus description, and did not run
  this distribution test. Spec §11 limit 5 and
  claim F047-C19 bar citing it in this spec's
  outputs. It is not pinned as an input,
  deliberately.
- **Phase-number state** — Phase-403 (Spec
  039) is the latest execution phase allocated
  on the merged record; Specs 040–043 allocated
  none at draft. Spec 047 allocates none at
  draft (DD-047-6).
- **Not done at draft, by design** — no site
  has been classified; no excavation literature
  has been extracted; the ledger-sign list has
  not been extracted; no per-site inscription
  count, share, ratio, or permutation quantity
  has been computed; no code was written or run;
  the AEE hooks have not run; nothing was filed
  with OSF. The gate-0.3 join census is an
  execution act, not a drafting act: computing
  per-site record counts at draft would put the
  classification worker one step from the very
  figures §4.5 keeps from them.

- **Pin correction — 2026-10-21, same day,
  before any freeze.** The first drafting pass
  carried four wrong pins, produced by a
  hash-computation run whose outputs did not
  survive re-computation: the Phase-104
  evaluation (carried `b299905a…`, correct
  `2d0b83e8…`), the citation record (carried
  `38f252e9…`, correct `39d28112…`), the sign
  crosswalk (carried `d94a62e0…`, correct
  `e44b8b55…`), and Spec 027's spec (carried
  `9c2b0c57…`, correct `7fff5d5a…`). Each
  correct value was re-verified by **two
  independent routes at the branch's base
  commits** (`82b29490`, and `83b6a563`, the
  head the branch as pushed sits on): the git-blob route
  through the commit's tree, and the contents
  raw route — the two agree byte-for-byte on
  every file checked, including the pins that
  were right (gazetteer `5ac76a30…`, corpus
  `c02e3d7b…`, anchors `df0cf620…`, model file
  `c5f08461…`, Phase-147 record `cf9dd60d…`).
  The error reached only the hash strings and
  one description detail (the citation record's
  year/URL fields, corrected in §2 above and
  spec §2); the quoted claim record itself was
  re-read from the correctly pinned file and is
  **identical** to what §2 and spec §1 state —
  verdict, rule, and reason verbatim. The
  correction is this note plus the corrected
  values, in a follow-up commit on the draft
  branch; the freeze re-asserts every pin in
  any case (tasks L6), and the Spec 040
  stale-pin precedent is exactly why it does.

## 3. Acceptance tests derived twice, independently

Per the doctrine, the acceptance test for each
claim was derived **twice, independently, from
the requirement alone**: Derivation A worked
from the design text (D-09) and the claim's
Phase-104 record only; Derivation B worked
from the approved campaign plan (Parts 2–5,
8, 12) and the triage entry only. The two
derivations agreed on the tests for 15 of the
19 claims as drafted. The four disagreements,
and their resolutions, are recorded here; the
register's `falsification_tests` carry the
resolved form.

1. **The sub-12 floor: verdict or build
   failure?** A (from the design) read "fewer
   than 12 sites survive" as an INCONCLUSIVE
   outcome in which the classification is the
   finding — a test gate. B (from the campaign
   plan's cluster tripwire: "Asset B fails its
   construction gates → dependents close as
   not-run") read a thin asset as a failed
   asset. **Resolution:** the design governs
   substance. Build gates (§4.7) are integrity
   gates — coverage, citation completeness,
   verification, circularity. Thinness is
   adjudicated at §6.3 as INCONCLUSIVE with
   Asset B frozen and published as the finding
   (claims F047-C12, F047-C15). Whether D-10
   proceeds against a frozen-but-thin Asset B
   is D-10's own gate question, flagged for
   its draft (§5, item 3).
2. **Permutation non-rejection with a high
   ratio.** A first derived the partition as
   "ratio ≥ 1.5 but p ≥ 0.05 → INCONCLUSIVE
   (measures incomplete)". B derived from the
   design's NOT SUPPORTED clause — "the ratio
   at or below 1.0 **or the permutation test
   does not reject**" — that the same case is
   NOT SUPPORTED. **Resolution:** B; the
   design's clause is explicit and governs
   (claim F047-C16, spec §6.3). The
   INCONCLUSIVE-measures case is thereby
   narrowed to 1.0 < R < 1.5 (with p < 0.05)
   and to the measures-disagree case.
3. **The ledger list's source document.** A's
   derivation named "the source document the
   program holds" (the design's phrase,
   "extracted from the source document"). B's
   derivation, working from the verification
   record, named the Academia.edu postings.
   The held document does not exist.
   **Resolution:** B, on the verification's
   evidence: posting A is the identical-titled
   public version of the held manuscript, and
   citing both postings (2025a/b) is the form
   the program's internal records already use
   (DD-047-3; claim F047-C13). The
   substitution is stated openly in spec §2.1
   rather than inherited silently.
4. **One corpus layer or two?** A read the
   design's "corpus layers with site
   attribution" as plural and co-primary. B
   read the campaign's comparability rule (R-2
   / R-3 discipline: one frozen contract per
   member) as requiring a single verdict-bearing
   layer named in the draft. **Resolution:** a
   single primary — the pinned layer of Specs
   027/028 — is named at draft (DD-047-4), and
   the status of any second site-attributed
   layer (co-primary, sensitivity, or unused)
   is an explicit OPEN item for the freeze
   (§5, item 1), not a drafting improvisation.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-047-1 — Thinness is a test gate, not a
  build gate.** Asset B's build gates (§4.7)
  are integrity-only. A honestly built,
  honestly thin asset freezes; §6.3 then
  returns INCONCLUSIVE with the classification
  as the finding (claims F047-C12, F047-C15).
  Rationale recorded in §3, disagreement 1.
- **DD-047-2 — An empty side closes the test
  at the same gate.** The design fixes the
  12-site floor but does not state the case
  where one side of the comparison is empty.
  With an empty pooled or contrast side the
  §6.2 ratio is undefined, so the draft reads
  the case into the same classification gate:
  INCONCLUSIVE, no quantity computed (claim
  F047-C15). The freeze may replace this with
  a stated alternative openly.
- **DD-047-3 — The public postings are the
  extraction source of record.** Grounds in
  §3, disagreement 3 (claim F047-C13, spec
  §2.1). The program's unreliable model file
  (spec §2.2) is never an extraction source.
- **DD-047-4 — One primary corpus layer.**
  The pinned Yajnadevam-compiled layer is the
  verdict-bearing corpus; any second layer's
  role is the freeze's to fix (§5, item 1).
- **DD-047-5 — The pooled grouping is part of
  the contract.** `ADMIN-TRADE-GATEWAY` =
  {gateway/border, administrative, port/trade}
  against {domestic, ritual}, with
  `mixed/unknown` in neither, is fixed in spec
  §4.2 so D-10's draft reads the same groupings
  this test uses. The design names the three
  pooled classes in its hypothesis and
  criteria; the grouping merely writes that
  down as asset contract.
- **DD-047-6 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-047-7 — Evidence carries `observed_at`
  from the draft.** The cited facts were
  verified first-hand today; Spec 038's freeze
  had to retrofit this field as a factual
  completion. Including it now is the same
  completion, done at the act that actually
  observed the records.

## 5. OPEN — what the freeze decision is asked to decide

1. **The second corpus layer's role** (§3,
   disagreement 4): co-primary, stated
   sensitivity, or unused — and if used, which
   layer, pinned how.
2. **The permutation seed.** Spec §6.2 fixes
   the shuffle count (9,999) and the level
   (5%); the seed value is set at the freeze
   and recorded in the freeze record, before
   any count exists.
3. **D-10 against a thin Asset B.** If §6.3's
   classification gate fires here (Asset B
   frozen but fewer than 12 testable sites),
   does the D-10 specification proceed under its own floors,
   or does the cluster close? This draft takes
   no position; the question belongs to the
   freeze of this spec and the drafting of
   the D-10 specification, in that order.
4. **Spine-only population, confirmed?** §2's
   verification record notes the spine excludes
   corpus sites of record elsewhere (Chanhu-daro,
   Dholavira). The draft follows the design
   (spine governs); the freeze confirms or
   records the exception it intends.
5. **The all-UNMAPPED ledger case.** If §5's
   extraction maps no entry, measure (b) cannot
   run. Draft position: the case is not
   silently absorbed — the freeze rules whether
   the execution then proceeds on measure (a)
   alone (with the SUPPORTED criterion's
   ledger clause amended openly in the frozen
   text) or closes at step 1.
6. **DD-047-8 (proposal): whether the frozen
   spec files its own OSF registration** —
   proposal: yes, under campaign decision E-1
   (every specification in the pass registers
   at its freeze, following the Specs 036–039
   pattern), so the classification contract,
   gates, and criteria are timestamped outside
   the repo before execution. Nothing is filed
   at draft. Note the Roif gate: an OSF
   registration files this spec's frozen
   *contract* (a design text), not results;
   the freeze confirms that reading against
   R-7 before filing.
7. **Whether execution requires a separate
   classification audit.** The §4.3
   verification pass is internal to the build.
   Proposal: it suffices, with its record
   published in the step-1 outcome; the freeze
   confirms or requires an independent re-check
   of a sample of AGREED rows.

## 6. What the freeze decision is asked to decide (summary)

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   §2 pin re-asserted against the merged
   record, the OPEN items of §5 decided, and
   DD-047-2 confirmed or openly overturned —
   or decline, leaving
   `indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`
   UNTESTED with the classification unbuilt and
   design D-10 still blocked on the same missing
   input its record names.
2. Under the campaign, this spec's freeze
   precedes the D-10 specification's freeze in dependency
   order (builders before dependents), and
   the D-10 specification's freeze pins Asset B's frozen
   digest from item 1.

## 7. Freeze decisions (DD-047) — 2026-10-21

The freeze act of 2026-10-21, taken in the
campaign's Wave 2 freeze wave under the
runnable-experiments campaign plan approved by
the owner as written on 2026-10-21. The header
of this record commissions the draft; this
section is the freeze's own record. Every §2
pin was re-asserted at the freeze by two
independent routes — the contents-API raw route
and the git-blob route, both at the merged
record (`main` at `83b6a563`) — and the two
routes agree byte-for-byte on every file, with
every hash equal to its pin (the full record is
in `freeze.md` §2). The AEE lifecycle hooks ran
over the register before the digest was
computed (rounds and artifacts in
`aee/freeze-aee-note.md`; the register stands
recovered at 0.7-draft).

### DD-047-8 — The spec's own OSF contract registration (OPEN item 6)

**DECIDED at freeze: yes** — file this frozen
spec's own OSF contract registration, under
campaign decision E-1 (every specification in
the pass registers at its freeze, following the
Specs 036–039 pattern). The Roif-gate reading
the draft asked the freeze to confirm is
**confirmed**: the registration files this
spec's frozen *contract* — a design text — and
no result; no result exists at the freeze, and
the filing surfaces nothing derived from any
result. Campaign R-7 stands untouched: this
spec's records are internal, and publication of
results remains the owner's separate GATE act
(spec §10, F047-C18). The registration's record
is kept in `osf-spec-registration.md` in this
directory, completed by append after filing;
execution awaits the registration's approval
act, which is the parent's approval click on
OSF's admin notification, and a separate
execution order.

### DD-047-9 — The second corpus layer's role (OPEN item 1)

**DECIDED at freeze: unused.** No second
site-attributed layer runs under this contract —
not as a co-primary and not as a sensitivity.
The pinned primary layer of spec §2 (the
Yajnadevam-compiled layer of Specs 027/028) is
the sole verdict-bearing corpus (DD-047-4
stands). No second layer is pinned in §2, and
the freeze adds none: a layer without a pin
could not enter a frozen contract, and a
comparison against one is a successor act
outside this campaign. Spec §8 carries the
ruling in the frozen text.

### DD-047-10 — The permutation seed (OPEN item 2)

**DECIDED at freeze: the seed is 20261021.**
Spec §6.2 fixes the shuffle count (9,999) and
the level (5%); the seed value is fixed here,
recorded in the freeze record (`freeze.json`),
and carried into the frozen §6.2 text and
F047-C16's boundary — before any count exists.
The value is the freeze date as an integer; any
fixed value would serve, and this one is now
the value of record.

### DD-047-11 — D-10 against a thin Asset B (OPEN item 3)

**DECIDED at freeze: D-10 proceeds under its own
gates.** If this spec's classification gate
fires (§6.3: Asset B frozen, fewer than 12
testable sites), the frozen Asset B still stands
as the identical classification campaign R-2
requires, and the D-10 specification is drafted
and frozen against it, adjudicating its own
population and floors in its own record. D-10
closes not-run by dependency closure only if
Asset B itself fails to build (a §4.7 gate) or
is later found unsound (§4.6) — the cases
DD-047-1 and F047-C12 already govern. This
spec's thin outcome closes this spec's test; it
does not close the dependent's.

### DD-047-12 — Spine-only population (OPEN item 4)

**CONFIRMED at freeze: the spine governs.** The
test population is the gazetteer spine's
testable clusters, exactly as drafted (§§3, 6.1,
8). Corpus sites of record elsewhere in the
program that are not spine clusters —
Chanhu-daro and Dholavira are the named cases in
§2's verification record — remain
out-of-population by rule and are accounted for
in gate 0.3's census, by name, with their record
counts. The freeze records no exception.

### DD-047-13 — The all-UNMAPPED ledger case (OPEN item 5)

**DECIDED at freeze: the execution proceeds on
measure (a) alone.** If the §5 extraction maps
no entry, measure (b) cannot run; the ledger
list still freezes with its extraction census,
and the distribution test runs on the
inscription share alone under the amended
partition frozen in spec §6.3 (SUPPORTED iff
R ≥ 1.5 and p < 0.05; NOT SUPPORTED iff R ≤ 1.0
or p ≥ 0.05; INCONCLUSIVE otherwise). The
SUPPORTED criterion's ledger clause is vacated
for that run only, and the outcome record states
the vacated clause openly beside the verdict,
with the extraction census as the reason. The
case is never silently absorbed, and no other
criterion changes. F047-C13's and F047-C16's
boundaries carry the ruling in the register.

### DD-047-14 — Classification audit (OPEN item 7)

**DECIDED at freeze: the §4.3 verification pass
suffices.** No separate classification audit is
required. The pass is internal to the build by
design — a second worker, or a second pass by a
worker who has not seen the first mapping,
verifying every AGREED row's citations against
its mapped class, with demotions recorded under
§4.4 — and its record is published in full in
the step-1 outcome record, where any reader can
re-check any row from the asset alone
(F047-C08's falsifier). An audit that re-read
the same citations more favourably would be the
repair §4.3 forbids.

### DD-047-15 — Execution phase number (per DD-047-6)

**DECIDED at freeze: Phase-406.** The merged
record allocates Phase-400 to Spec 036,
Phase-401 to Spec 038, Phase-402 to Spec 037,
and Phase-403 to Spec 039; this spec allocates
the next number in the campaign's freeze-wave
sequence as Phase-406. Nothing substantive turns
on the number.

### DD-047-16 — The AEE gate reading

**DECIDED at freeze: the Spec 038 DD-038-10 /
Spec 037 DD-037-9 reading governs.** At every
lifecycle hook the aee 1.5.0 assessment carries
zero correctness failure modes and no claim
below the 0.70 threshold; its outcome word
reads "iterate" solely because each of the 19
claims carries an FR-2.3 draft-cap record. That
cap is a lifecycle fact about a freeze-time
register, not a correctness failure and not a
bar to freezing. The rounds (a loadability
recovery, then 67 failure modes over the
recovered text, then draft-cap records only)
and artifacts are recorded in
`aee/freeze-aee-note.md`.

### Confirmations

- **DD-047-1 is CONFIRMED as drafted:** thinness
  is a test gate (§6.3), not a build gate
  (§4.7). A honestly built, honestly thin asset
  freezes.
- **DD-047-2 is CONFIRMED as drafted:** an empty
  pooled or contrast side closes the test at the
  same classification gate — INCONCLUSIVE, no
  quantity computed.

## 8. What the freeze decision decided (summary)

1. This contract is frozen (digest in
   `freeze.md` / `freeze.json`), with every §2
   pin re-asserted by the two-route verification
   and the execution phase allocated as
   Phase-406.
2. The §5 OPEN items are decided as DD-047-8 to
   DD-047-14 above; DD-047-15 allocates the
   phase; DD-047-16 records the AEE gate reading;
   DD-047-1 and DD-047-2 are confirmed.
3. Nothing else: the claim
   `indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`
   stands UNTESTED, Asset B is unbuilt, no
   ledger-sign list exists, and nothing has been
   counted. Execution is a separate act, gated
   on this freeze merging, the OSF registration's
   approval act, and a separate execution order.
   Under the campaign, this spec's freeze
   precedes the D-10 specification's freeze in
   dependency order (builders before dependents).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
