# Spec 027 — Stage 2 / Q7 Adjudication Packet

> ## PACKET FOR OWNER ADJUDICATION — NOT ADJUDICATED (2026-10-12)
>
> Prepared at the owner's direction (2026-10-12: "Do all
> we can do today, no reaching out yet"). This packet
> frames the decisions a Q7 freeze requires; it decides
> none of them, freezes nothing, and authorises no
> work. The recommendations are the program's, with
> reasoning, for the owner to accept, amend, or reject
> per ask — the same division of labour as Spec 027's
> §13 asks and Spec 028's adjudication record.
>
> Basis (merged record only): Spec 027 spec §8.1 (the
> bounded Q7 question), §5/D8 (provenance source
> candidates and licensing posture), §8.3 (Stage 2
> separation from Q1), claim F027-C15 ("Q7 verdicts
> concern craft evidence only"); Stage 0 completed
> (Phase-391); Stage 1 completed INCONCLUSIVE
> (Phase-392) and its robustness follow-up completed
> (Spec 028, Phase-393). Spec 027's adjudication record
> states: "Stage 2 (Q7/Q6) is not authorized by this
> record beyond its conditional design status; each
> Stage 2 question requires its own freeze."

## The question, and what gates it

**Q7 (spec §8.1):** Do site pairs that share provenanced
material sources show greater ceramic or bead/craft-technique
similarity than expected from geographic and river-network
distance alone? Unit: site pair. Responses are modelled
separately (ceramics; bead/craft technique) and never pooled
into one "culture" score. Null: geography and river distance
explain all shared variance. Licensed conclusion: a statement
about objects, materials, and techniques only — never about
people migrating, workshops moving, or language spreading.

**The gate is not chronology.** Q7 may be frozen only after
Stage 0 (done) **and after the D8 source/licence audit**
establishes which provenance links are lawfully and traceably
usable (spec §8.1, FR-027-8). That audit has never been run:
D8's posture in the spec is "catalogue and rights-clear
before digitisation; bulk-open status not verified" for all
three components — Law (2011), Kenoyer/Vidale craft studies,
and the Meluhha compilations. Until it runs, Q7 has no lawful
link set at all, and every ask below is downstream of that
fact.

## Ask 1 — D8 audit scope and order

**Options:**

- **1A — Audit all three components as one exercise.**
  Complete picture in one pass; spends equal effort on the
  least central source (Meluhha compilations are
  Mesopotamian-side and support context, not the site-pair
  link set's core).
- **1B — Sequenced audit with a stop rule after each:**
  Law (2011) first, Kenoyer/Vidale second, Meluhha last.
- **1C — Audit only a minimum viable link set** (the
  components a first network could be built from), deferring
  the rest indefinitely.

**Program recommendation: 1B.** Law (2011) is the largest
structured provenance dataset in D8 — stone-source
attributions with site linkage — and its rights outcome
likely decides Q7's fate on its own: if Law's data cannot be
lawfully digitised, the link set may fall below viability
and Q7 closes negatively *cheaply*, before effort is spent
elsewhere. Kenoyer/Vidale second, because the bead/craft
response (Ask 3) depends on their technique classifications.
Meluhha last: it contextualises exchange but the bounded
question is about Indus-side site pairs. 1C is rejected
because "minimum viable" cannot be known before any audit
returns — it would bake an unaudited guess into the design.
1A is rejected on effort-ordering only, not on substance.

*Testability consequence:* under 1B, each stage's outcome is
reported before the next begins; a rights failure at any
stage is a reportable negative closure for the affected
response arm, not a prompt to substitute a weaker source.

## Ask 2 — What counts as a provenance link

Spec §8.1 admits a link with its method recorded (visual,
petrography, INAA, LA-ICP-MS, Pb isotopes, or another named
method). The movement report's D8 caveat stands: provenance
is often geological *compatibility*, not a unique
fingerprint, and visual attribution is the weakest form.

**Options:**

- **2A — All recorded methods pooled**, method as a covariate.
- **2B — Two-tier links:** instrumental methods
  (petrography, INAA, LA-ICP-MS, Pb isotopes) form the
  primary link set; visual-only links appear only in a
  separately labelled sensitivity.
- **2C — Instrumental only;** visual links excluded entirely.

**Program recommendation: 2B.** It mirrors the program's
existing discipline for exactly this shape of problem
(M77 governing with Parpola as a labelled sensitivity in
Stage 1; the Spec 030 design's CONTESTED sensitivity). 2A
lets the weakest method silently carry the estimand; 2C
discards real information and could make Q7 untestable for
purity's sake when a labelled sensitivity would have
preserved the honest reading.

*Testability consequence:* the primary estimand is defined
on strong links. If the D8 audit shows strong links too
sparse for the Ask 5 minimum-support rule, Q7 is
NOT-YET-TESTABLE on the primary — it is not quietly
re-based on visual links.

## Ask 3 — Response operationalisation and eligibility

The program generates no primary laboratory data; both
responses must be built from published classifications as
recorded, with method fields preserved.

**Options:**

- **3A — Each response modelled on its own eligible site
  set:** ceramic similarity from published fabric/typology
  classifications; bead/craft similarity from published
  technique classifications (e.g. drilling-technique
  classes); a site enters an arm if that arm's frozen
  minimum-support rule is met; arms never share a pooled
  score (§8.1 already forbids the pooling).
- **3B — Intersection only:** both arms restricted to sites
  eligible for both responses. Cleaner comparison, much
  smaller site set — likely below viability given the
  gazetteer's 30 clusters.
- **3C — One combined craft-similarity response.**
  Rejected outright: §8.1 forbids pooling into a single
  score.

**Program recommendation: 3A**, with minimum-support and
frequency rules fixed in the Q7 freeze from margins only
(the Stage 1 freeze discipline), and with provenance-method
and classification-source recorded per link and per
similarity cell.

*Testability consequence:* under 3A the two arms can return
different verdicts — that is a feature of the bounded
question, not an inconsistency to be harmonised.

## Ask 4 — Does Q7 depend on the chronology-spine extension (Spec 030)?

**Analysis.** Q7's controls are geographic distance,
river-network distance, period eligibility, site sample size,
and publication/excavation intensity. None requires a dated
first appearance. Period eligibility can be served by the
Stage 0 gazetteer's period labels as published
(`period_label_as_published`); Q7's site identities and
coordinates come from Stage 0, which is complete. The
Spec 030 extension exists to serve Q6's timing criteria —
a different question with different evidence (spec §8:
"Stage 2 is not a package").

**Options:**

- **4A — Q7 proceeds independently of Spec 030**, on the
  Stage 0 gazetteer and published period labels.
- **4B — Q7 waits for Spec 030**, in case the extension
  incidentally enriches the gazetteer or site-period data.

**Program recommendation: 4A.** Q7's actual blocker is D8
rights, not chronology; coupling Q7 to a spine it does not
use would delay it behind an unrelated study and blur the
Stage 2 separation the spec mandates.

*What stays untestable under 4A:* any Q7 variant needing
within-Mature chronological resolution finer than published
period labels (e.g. period-sliced networks at sub-period
resolution). If such a variant is ever wanted, it is a new
question with its own design — not a reason to hold this
one.

## Ask 5 — Null model, controls, and the freeze's minimum-support rule

**Options:**

- **5A — Inherit the Spec 026/027 discipline wholesale:**
  MRM / partial-Mantel null (geography + river distance
  explain all shared variance), the §8.1 falsifier
  (source-sharing adds no predictive power, or its effect is
  not robust to the frozen site jackknife), discriminating
  positive and negative controls (a control that cannot
  differentially fail makes a run INVALID), and the
  INVALID / INCONCLUSIVE / CONTRADICTED / SUPPORTED verdict
  taxonomy. Minimum eligible site-pair and per-arm support
  rules are fixed in the freeze **from margins only**,
  after the D8 audit reports the eligible-link counts and
  before any response is computed.
- **5B — A lighter design** (single Mantel test, no control
  pair, no jackknife clause). Rejected: it would reintroduce
  exactly the failure mode Spec 028 exists because of — a
  headline effect whose robustness was never made a verdict
  condition.

**Program recommendation: 5A**, unchanged. The Stage 1 /
Spec 028 sequence is the program's own evidence for why:
Phase-392's primary cleared its margin and its detection
unanimously, and only the pre-committed jackknife clause
kept the verdict honest at INCONCLUSIVE.

## Ask 6 — Publication posture and registration

**Options:**

- **6A — Mirror Stage 1 exactly:** D8-derived link data are
  published only at their audited posture (verified_open-
  derived rows may go CC BY 4.0 through the release gate;
  read-only-derived rows are never released, per Spec 027
  §5.1); the frozen Q7 contract is registered on OSF before
  execution; the Q7 outcome is recorded under Spec 027 and
  never written into Stage 1's or Spec 028's records.
- **6B — Decide publication after the verdict.** Rejected:
  posture follows the licence audit, not the result;
  deciding after outcomes invites result-dependent
  disclosure choices.

**Program recommendation: 6A.**

## Dependencies — summary

| Dependency | Status | Needed for Q7? |
|---|---|---|
| Spec 027 Stage 0 (gazetteer + spine) | Complete (Phase-391) | Yes — site identities, coordinates, period labels |
| D8 source/licence audit | **Never run — the gate** | Yes — no lawful link set exists without it |
| Stage 1 (Phase-392) + Spec 028 (Phase-393) | Complete | No data dependency; machinery and discipline precedent only |
| Spec 030 spine extension (Q6) | Design draft only | **No** (Ask 4) |
| Q6 freeze or outcome | Not freezable today | No — Stage 2 questions are separate (spec §8) |

## Explicit non-goals

- **No people, migration, workshop-population, or language
  conclusion** from any Q7 outcome (spec §8.1 licensed
  conclusion; F027-C15). A Q7 result is not the mobility arm
  of Q1 and does not upgrade Q1 (spec §8.3).
- **No digitisation before rights clearance**, and no
  contact with any rights holder under this packet — a
  permission request, if the audit ever shows one is
  needed, is a separate owner decision.
- **No new primary data generation** (no laboratory
  provenance work, no new fieldwork data).
- **No PRED-2026 or anchor contact**, and nothing here
  enters a sign-reading model (movement report §9, rule 5).

## What adjudication would set in motion (for the owner's awareness)

Adjudicating these asks does not freeze Q7. It would
authorise, in order: (1) the D8 audit under Ask 1's scope —
a desk audit of published sources and their terms, no
external contact; (2) a Q7 freeze designed from the audit's
margins (eligible links, sites, pairs) under Asks 2/3/5,
with its own freeze record and OSF registration; (3)
execution only after that freeze merges. Each step remains
separately reportable, and a negative D8 outcome closes the
line honestly at step 1.

AI disclosure: prepared by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution §VI. Nothing in this packet is a decision;
the decisions are the owner's.
