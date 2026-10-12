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
