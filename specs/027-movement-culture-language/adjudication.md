# Spec 027 — Owner Adjudication Record

> ## ADJUDICATED AND FROZEN — 2026-10-11
>
> Owner decision (Tristen Pierson, 2026-10-11 08:26 EDT,
> verbatim): **"Approve Spec 027 with the recommended answers
> and freeze it."**
>
> This record answers spec §13 Asks 1–5. The answers below are
> the owner's; the "recommended" values the owner approved are
> the draft's recommendations for Asks 1, 2, 4, and 5 and the
> draft's proposed rules for Ask 3, as presented with draft
> PR #147. No answer is paraphrased into a different rule.

## Ask 1 — Stage order and Stage 0 scope → **0A**

Order **Stage 0 → Stage 1 gate → conditional Stage 2** is
approved. Stage 0 scope is **0A**: the gazetteer and the
chronology spine are built in one Stage 0, because Q6 and any
defensible site-period work need both.

## Ask 2 — Q2 governing sign list → **M77**

**M77 (Mahadevan numbering) governs** the Stage 1 primary
test. Parpola/CISI numbering may appear **only** as a
separately labelled sensitivity with a sign-by-sign crosswalk
rule (crosswalk v1). Wells/ICIT-native numbering does **not**
govern. `sign_list_version` remains a field on every Stage 1
record; sign lists are never silently pooled.

## Ask 3 — Q2 corpus inclusion rules → **APPROVED AS DRAFTED**

- provenanced records only;
- pottery graffiti **not pooled** with seals/tablets in the
  primary test;
- damaged and multi-line objects included only when the frozen
  minimum legible-token rule is met, with their flags retained;
- duplicate records removed under the named program
  deduplication artifact, while duplicate texts on distinct
  objects are retained as distinct objects;
- unmapped signs retained as `UNMAPPED` under one frozen
  pooling rule;
- site/stratum minimum-support and frequency rules fixed in
  the Stage 1 freeze before outcomes are examined.

## Ask 4 — Gazetteer licensing and publication posture → **CC BY 4.0 via the release gate**

The completed Stage 0 gazetteer is published **CC BY 4.0
through the program release gate**, limited to lawfully
reusable rows. Restricted coordinates are never published more
precisely than their source state allows. Catalogue-only and
permission-required sources are excluded from publication
under all circumstances.

## Ask 5 — Stage 1 execution timing → **Executes on the adjudicated design**

After adjudication and completion of Stage 0, **Stage 1
executes on the adjudicated design once its own freeze is
committed and merged**. No separate owner go is required after
the Stage 0 report.

## Freeze consequences

- Spec 027 is frozen at this record. Stage 0 is **Phase-391**;
  Stage 1 is **Phase-392** (numbering: the repository's
  registered phase space ends at Phase-386 (Spec 026);
  387–390 are claimed by the docstring of the legacy
  unregistered script `backend/scripts/phase382_390_actionable.py`,
  which produced no registered artifacts — 391/392 are the
  first numbers free of both).
- Each stage still requires its own freeze record before
  execution (spec §3.1, FR-027-12). A changed gate is a new
  version and a new freeze.
- Stage 2 (Q7/Q6) is **not** authorized by this record beyond
  its conditional design status; each Stage 2 question
  requires its own freeze, and Q6 additionally requires the
  Stage 0 timing-support assessment.
- Publication of the gazetteer under Ask 4 is executed as a
  release-gate package prepared in Stage 0; the external
  deposit itself is a separate step (no deposit is made by the
  Stage 0 program that prepared the package).

AI disclosure: recorded by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution §VI. The decision text above is the owner's,
given in the program chat on 2026-10-11.
