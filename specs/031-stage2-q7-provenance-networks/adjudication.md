# Spec 031 — Adjudication Record

> ## ADJUDICATED INPUT — 2026-10-13
>
> This spec has two adjudication inputs, recorded
> here so the freeze's basis is inspectable:
>
> 1. **The Stage 2 / Q7 adjudication of 2026-10-12**
>    (`specs/027-movement-culture-language/
>    stage2-q7-adjudication.md`): the owner's
>    instruction **"Freeze it"** (2026-10-12), read
>    under his established block-ratification pattern
>    and confirmed by him the same day (verbatim:
>    **"correct, do it"**, 2026-10-12 13:30 EDT),
>    adopted the Q7 packet's six recommendations as a
>    block: **1B, 2B, 3A, 4A, 5A, 6A**. That record is
>    the adjudication input to this design; its
>    operative text is reproduced verbatim in §1
>    below. It authorised the D8 audit (step 1 of its
>    cascade, since completed) and prescribed this
>    freeze (step 2) as a separate later act.
> 2. **The owner's order of 2026-10-13** (program
>    chat): design and freeze Spec 027 Stage 2 / Q7
>    from the D8 margins. Execution was not ordered.

## 1. The adopted asks (verbatim operative text)

From `stage2-q7-adjudication.md` (2026-10-12):

**Ask 1 — D8 audit scope and order → 1B.** "The D8
source/licence audit runs sequenced, with a stop rule
and a reported outcome after each stage: Law (2011)
first, Kenoyer/Vidale second, Meluhha compilations
last." — *Discharged:* the audit ran and closed
2026-10-12 with no rights failure
(`stage2-d8-audit.md`).

**Ask 2 — What counts as a provenance link → 2B.**
"Two-tier links. Instrumental methods (petrography,
INAA, LA-ICP-MS, Pb isotopes) form the primary link
set; visual-only links appear only in a separately
labelled sensitivity. The primary estimand is defined
on strong links: if the D8 audit shows strong links
too sparse for the Ask 5 minimum-support rule, Q7 is
NOT-YET-TESTABLE on the primary — it is not quietly
re-based on visual links." — *Implemented in spec
§3, claims F031-C02, C03, C08.*

**Ask 3 — Response operationalisation → 3A.** "Each
response is modelled on its own eligible site set:
ceramic similarity from published fabric/typology
classifications; bead/craft similarity from published
technique classifications; a site enters an arm if
that arm's frozen minimum-support rule is met; the
arms are never pooled into one score (§8.1).
Minimum-support and frequency rules are fixed in the
Q7 freeze from margins only, with provenance method
and classification source recorded per link and per
similarity cell." — *Implemented in spec §4, claims
F031-C05, C06.*

**Ask 4 — Dependence on Spec 030 → 4A.** "Q7 proceeds
independently of the Spec 030 chronology-spine
extension, on the Stage 0 gazetteer and published
period labels (`period_label_as_published`)." What
stays untestable was recorded with the decision: "any
Q7 variant needing within-Mature chronological
resolution finer than published period labels would
be a new question with its own design." —
*Implemented in spec §§4.4, 6; claim F031-C10.*

**Ask 5 — Null model, controls, support rules → 5A.**
"The Spec 026/027 discipline is inherited wholesale:
MRM / partial-Mantel null (geography and river
distance explain all shared variance); the §8.1
falsifier (source-sharing adds no predictive power,
or its effect is not robust to the frozen site
jackknife); discriminating positive and negative
controls (a control that cannot differentially fail
makes a run INVALID); the INVALID / INCONCLUSIVE /
CONTRADICTED / SUPPORTED verdict taxonomy. The
minimum eligible site-pair and per-arm support rules
are fixed in the Q7 freeze from margins only, after
the D8 audit reports the eligible-link counts and
before any response is computed." — *Implemented in
spec §§4.3, 5; claims F031-C08, C09, C12. The specific
thresholds the margins force are the design
decisions of §2 below.*

**Ask 6 — Publication posture and registration →
6A.** "Stage 1's posture is mirrored: D8-derived link
data are published only at their audited posture
(verified_open-derived rows may go CC BY 4.0 through
the release gate; read-only-derived rows are never
released, per §5.1); the frozen Q7 contract is
registered on OSF before execution; the Q7 outcome
is recorded under Spec 027 and never written into
Stage 1's or Spec 028's records." — *Implemented in
spec §§7, 8; claim F031-C11. The registration is
filed with this freeze; execution remains a separate
owner order.*

## 2. Design decisions taken under the 5A mandate

Adopted 5A fixes the support rules in the freeze
from margins only; it does not enumerate their
values. The following decisions were forced by the
D8 margins and are taken under that mandate. Each is
stated with its recommendation and reasoning in spec
§10 and summarised here so the freeze record carries
them in one place. They are **design decisions of
this freeze, not owner adjudications**: an owner
change to any of them is a new adjudication and,
after the freeze merges, a new freeze.

- **DD-1** — Link support: site link-eligible at ≥ 3
  primary-tier determinations; pair linked on ≥ 1
  shared named source area (identity as published,
  no program-side merging).
- **DD-2** — Arm site-support floors: ceramic ≥ 20
  published classified items per site; bead/craft
  ≥ 10 published classified beads per site.
- **DD-3** — Arm viability: ≥ 8 eligible sites and
  ≥ 10 linked pairs; analysis pair set = all pairs
  among eligible sites.
- **DD-4** — Practical margin: partial R² = 0.02 for
  the shared-source term (Stage 1's 0.01 governed a
  far larger estimand; the pair-level estimand's
  effective N is at most C(30, 2) pairs).
- **DD-5** — Verdict rules operationalised on the
  Stage 1 pattern (§7.6 → spec §5.2), with
  NOT-YET-TESTABLE as a margins-step registration
  status and non-estimable LOSO cells capping
  SUPPORTED.
- **DD-6** — Controls: R = 199 synthetic replicates
  of the identical pipeline per arm; negative control
  passes iff the SUPPORTED rule fires in ≤ 5% of
  replicates, positive (planted ≈ 2× margin) iff
  ≥ 95%.
- **DD-7** — Ceramic arm declared **conditionally
  estimable** with a pre-registered NOT ESTIMABLE
  closure at the execution margins step (its source
  basis was never audited as a set — D8 residual
  (i)); dose-response declared sensitivity-only.
- **DD-8** — River-network distance: along-network
  distance on a drainage network pinned by name and
  hash at execution; 25 km snap tolerance;
  unsnappable sites excluded and reported.

## 3. What this adjudication does not cover

- **Execution.** Phase-395 runs only on a separate
  owner order after this freeze merges and the OSF
  registration verifies public (adopted 6A's
  registration-before-execution order).
- **Any Spec 027, 028, 029, or 030 record.** This
  spec references them; it alters none of them.
- **Q6.** Stage 2's other question is untouched;
  Ask 4A's independence ruling is the only
  cross-reference.
- **Rights-holder contact.** None is authorised; a
  permission request, if ever needed, is a separate
  owner decision (adjudication non-goals, standing).

AI disclosure: recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI. The adopted-ask texts in §1 are the
2026-10-12 adjudication record's own words; the
design decisions in §2 are the program's, taken under
the 5A mandate that record created.
