# Spec 029 — Owner Adjudication Record

> ## ADJUDICATED — 2026-10-12
>
> Owner decision (Tristen Pierson, 2026-10-12, verbatim):
> **"ratify all of these as a block and do it"** — in
> response to the program's recommendations for the six
> open owner decisions in `spec.md` §8 (OD-1 through
> OD-6), presented with their reasoning in the program
> chat on 2026-10-12.
>
> All six decisions are ratified **as a block**, adopting
> the recommendations exactly as presented. There is no
> separate per-decision adjudication round: the block
> ratification is the adjudication record for OD-1
> through OD-6. The retroactive realignment audit
> (`audit.md` in this directory, with its reclassification
> ledger) had been commissioned before ratification; its
> findings are the evidence base the OD-1 and OD-3
> decisions below rest on, and its ledger is the
> instrument OD-1 names.

## What the owner decided

1. **OD-1 — Retroactivity: immediate re-staging.** All
   existing governed claims — the 287 anchors and the
   extracted claims — are re-staged immediately when the
   lifecycle is implemented, as **one dated
   reclassification event**, not at next touch of each
   record. The retroactive audit's reclassification ledger
   serves as the re-staging record. A claim's stage is the
   highest stage whose evidence exists in the record, so
   later refinements of the stage definitions do not cause
   churn: records move only when evidence is added. Known
   non-conforming displays (the audit found live machinery,
   not archived text) are corrected in the same
   implementation, prioritised by public visibility.
2. **OD-2 — Digestion authority: named accountable human;
   independence required at `digested`.** The explanation
   gate accepts a named, accountable human author —
   program-internal or external — whose account is a
   durable, public, citable artifact. AI systems may draft
   but may **never** be the named human. The `digested`
   stage additionally requires engagement by at least one
   scholar independent of the program (not an author of
   the claim, not program staff). Internal and external
   explanations carry the same weight at the `accepted`
   gate; independence is spent at the top stage.
3. **OD-3 — Contested-attribution cap: `checked`.** While
   a claim's attribution sub-claim is contested, the
   parent claim's stage is capped at `checked`. This is
   the bundle rule (parent stage = minimum of sub-claim
   stages, F029-C03) applied consistently: a contested
   attribution sub-claim is itself only at created/checked,
   because its explanation is precisely what is in
   dispute. **Contested** means an active, evidenced
   dispute, and the cap applies. **Unexamined** (the
   attribution sub-claim not yet assessed) carries no
   special cap; the bundle minimum rule handles it.
4. **OD-4 — Stage naming: Tao's five names verbatim.**
   The stage names — created, checked, explained,
   accepted, digested — are adopted verbatim in data and
   on all displays. There is no display-level synonym
   mapping: a translation layer drifts toward warmer words
   and quietly re-introduces acceptance language for
   checking-stage states, which is the failure this spec
   exists to prevent. Reader unfamiliarity is handled by a
   one-line legend, not by renaming.
5. **OD-5 — Digestion threshold: any one of three
   qualifying events.** A digestion record qualifies on
   **any one** of: (i) independent scholarly **reuse** of
   the reading or explanation in work not authored by the
   program; (ii) a published substantive **challenge**
   that the account has answered in a durable record —
   the exchange itself is the digestion record; or (iii)
   an independent **citation that engages the mechanism**
   (not a passing mention), judged by a named reviewer at
   intake with the rationale recorded. Symmetrically, an
   **unanswered refutation is adverse digestion**: the
   claim is flagged contested and pulled back under the
   bundle rule.
6. **OD-6 — Priority register: public at intake, content
   sealed by hash.** The external priority/credit register
   is **public at intake**: the registration record —
   claimant, timestamp, and a hash of the reading — is
   published immediately, proving priority and
   content-at-time without revealing the content. The
   reading itself stays sealed until the claimant
   publishes, or at a claimant-chosen date (default
   24 months, extendable once). Registration issues on
   record completeness alone; no score, stage, or verdict
   is required or implied (F029-C08, FR-029-11).

## Scope note

This record adjudicates OD-1 through OD-6 only. The
additional items the retroactive audit raised in its §9
(D-A through D-E) are **not** decided by this ratification
and remain open for the owner.

## Freeze consequences

- Spec 029's §8 decisions are now disposed; `spec.md` §8
  is annotated DECIDED 2026-10-12 under each item, with
  the original question text preserved.
- The governed claims (F029-C01…C10) remain `draft`: this
  record adjudicates the §8 decisions, it does not freeze
  the claims. Plan and tasks may now be written against
  the adjudicated decisions, under §6(d) — a future plan
  disposes of each decision by citing this record, never
  by default.
- The freeze merge of PR #164 happens **after** the
  retroactive audit has landed on the same branch (it
  has: `audit.md` + `reclassification-ledger.json`), and
  remains an owner-gated merge. Nothing in this record
  merges anything.
- OD-1's re-staging is executed by the implementation,
  using the audit's ledger as its record; no existing
  claim, anchor, verdict, or display is changed by this
  adjudication record itself (F029-C10 stands for the
  drafting stage).

AI disclosure: recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI. The decision text above is the owner's,
given in the program chat on 2026-10-12; the decision
substance is the program's recommendations as presented
to and ratified by him.

---

## Addendum — D-A through D-E ratified as a block (2026-10-12)

> Owner decision (Tristen Pierson, 2026-10-12, verbatim):
> **"do all this"** — in response to the program's
> recommendations for the five further decisions the
> retroactive realignment audit raised in `audit.md` §9
> (D-A through D-E), presented with their reasoning in
> the program chat on 2026-10-12.
>
> The scope note in the record above — D-A through D-E
> "are **not** decided by this ratification and remain
> open" — is superseded by this addendum: all five are
> now decided, as a block, adopting the recommendations
> exactly as presented.

1. **D-A — The 33 chained HIGH anchors: annotate in
   place, additively; pin the schema.** Every anchor
   record gains a total, explicit `validation_status`
   (no absent fields — 130 anchors currently carry none)
   and a computed `strict_set` flag with the governing
   rule's version recorded, so the canonical anchors
   file becomes self-describing and strict-set membership
   is inspectable from the file alone. There is **no
   demotion of the display tier**: the confidence tier is
   a lane-1 extraction judgment, validation provenance is
   a separate axis, and conflating the two axes is the
   failure that produced the flat status. No existing
   field is altered. The same pass pins a declared schema
   for the anchors file, enforced by a CI validator — the
   file has accreted 56 distinct field shapes, and without
   a schema gate the annotation decays back into drift.
2. **D-B — Duplicate extracted claims: deduplicate by
   proposition — merge, never delete; guard the intake.**
   One canonical claim per proposition; every source
   document that stated it is preserved as an evidence
   instance of that claim, with evidence counted **once
   per origin group** (Spec 026's evidence-counting rule
   applied to the store). Stage and score attach to the
   proposition, not to an instance. A proposition
   fingerprint (normalised-text hash) is checked at
   extraction intake, so a future wholesale re-extraction
   collides loudly instead of silently regenerating a
   doubled set — the failure mode that produced the
   duplicates in the 2026-10-09 batch.
3. **D-C — README factual errata: correct immediately,
   as errata.** Executed by the pull request carrying
   this addendum, on its own track, not bundled into the
   implementation. Two statements misstated the canonical
   record (`backend/reports/INDUS_FINAL_ANCHORS.json`,
   recomputed from the entries: HIGH 166 / MEDIUM 5 /
   LOW 3 / CANDIDATE 113; `pending_non_sa_validation`
   = 44 = 43 HIGH + 1 MEDIUM) and are corrected in place,
   with a dated errata note in the README: (i) the tier
   split in the Indus Script Decipherment section,
   previously "112 LOW + 4 CANDIDATE"; (ii) the
   pending-validation set described as "44 HIGH" in the
   status banner, the metrics table, and the
   research-status list — now "43 HIGH + 1 MEDIUM" in
   each. The re-base note's past-tense account of the
   Phase-108 classification ("44 HIGH anchors were
   SA-derived or SA-confirmed-only") is **not** altered:
   it records what Phase-108 found, and the one MEDIUM
   anchor, M293, was HIGH at classification and was
   re-reviewed HIGH → MEDIUM by Phase-109 — a demotion
   the same note already records.
4. **D-D — Foundation report annotations: as-of label
   now; generated annotations as the structural fix.**
   Interim: the embedded `solid_claims` /
   `caveated_claims` prose carries a dated as-of label,
   so stale figures no longer ride unflagged in a live
   report (a prose refresh was rejected as the primary
   remedy: it asserts a currency the process cannot yet
   guarantee, and re-drifts at the next anchor change).
   Structural: the report's claim annotations are
   **computed from the canonical data at report time**,
   stamped with the anchor file's hash, never hand-typed;
   and the foundation status endpoint is repaired to
   serve the on-disk report or fail loudly — an endpoint
   returning nulls beside a healthy report file is how
   the stale prose went unflagged.
5. **D-E — Where the stages live: the audit ledger is
   the source of truth until the plan's re-staging
   migration.** No stage fields are stamped onto live
   records before the machinery exists to maintain them:
   unmaintained stage fields would begin rotting at the
   first claim edit, rebuilding the flat-status problem
   in better vocabulary. OD-1's immediate re-staging is
   executed by the Spec 029 implementation as an **early,
   gated migration task**, run mechanically from
   `reclassification-ledger.json`, stamping each record
   with `stage`, `stage_source`, and `stage_as_of`. The
   governing invariant: **a stage is always recomputable
   from the record's evidence — the stored value is a
   cache with provenance, never an assertion.**

**Plan-scope consequences.** D-A, D-B, and D-E enter
the Spec 029 plan scope; D-D's structural half likewise
(its interim as-of label is a standing instruction to
the plan). D-C is executed by the pull request carrying
this addendum and does not enter the plan. Nothing in
this addendum changes any claim, anchor, verdict, or
display beyond the D-C errata it executes (F029-C10
stands for the drafting stage).

AI disclosure: recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI. The decision text above is the owner's,
given in the program chat on 2026-10-12; the decision
substance is the program's recommendations as presented
to and ratified by him.
