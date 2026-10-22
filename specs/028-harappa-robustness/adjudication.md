# Spec 028 — Owner Adjudication Record (Delegated Design)

> ## ADJUDICATED BY DELEGATION — 2026-10-11
>
> Owner decision (Tristen Pierson, 2026-10-11, verbatim):
> **"Also do the Harappa robustness design follow up and
> execute it based on what you think the best way forward
> is."**
>
> Unlike Spec 027, this spec has **no separate owner
> adjudication round**: the owner's sentence authorises the
> follow-up, delegates the design judgment to the program,
> and authorises execution, in one order. This record is the
> adjudication record for Spec 028. The design decisions
> below are the program's, made under that delegation and
> recorded here so the delegation is auditable; the verdicts,
> whatever they are, are produced by the frozen rules, not by
> this record.

## What the owner decided

1. **The follow-up happens.** Spec 027 Stage 1 (Phase-392)
   closed INCONCLUSIVE because its SUPPORTED rule's
   jackknife clause failed on the Harappa drop alone. The
   question that verdict leaves open — whether the
   site-linked repertoire structure is independent of
   Harappa or a Harappa/big-corpus artefact — is to be
   designed and executed as a new spec (Spec 028, Phase-393).
2. **Design judgment is delegated.** Arm structure,
   estimands, and multiplicity handling are the program's
   choice, frozen before outcomes under the program's usual
   discipline (margins-only audit, synthetic-only
   calibration, freeze, OSF registration, execution).
3. **Execution is authorised in advance**, on the frozen
   design, without a further owner go — mirroring Spec 027's
   Ask 5 answer for its Stage 1.

## The program's design decisions under the delegation

Recorded in full in `spec.md` §5 and frozen in `freeze.md`:

- **Arm A (confirmatory, primary):** the Phase-392 analysis
  population with Harappa excluded, run through the identical
  Phase-392 machinery — the direct test of whether the
  bounded claim survives without the load-bearing site.
- **Arm B (confirmatory, secondary):** a site-equal-weight
  estimand on the full six-site population (equal per-site
  quota per draw) — the direct test of the rival explanation
  that the effect is an inscription-count artefact of the
  large corpora.
- **Arm C (exploratory, no verdict):** a descriptive
  decomposition of Harappa's own contribution (object types
  and composition components), labelled exploratory wherever
  reported.
- **Multiplicity:** hierarchical. Arm A carries the primary
  claim; Arm B is a separate bounded claim under its own
  frozen rule, labelled secondary; no pooled headline across
  arms is permitted.
- **Inherited adjudicated values (not re-decided):** M77
  governs (Spec 027 Ask 2); the Ask 3 corpus rules as frozen
  in Spec 027's Stage 1 freeze; the verdict taxonomy and the
  practical margin (adjusted R² = 0.01) from Spec 026/027.

## Freeze consequences

- Spec 028 is frozen at `freeze.md` in this directory once
  this record, the spec, the claim register, the margins
  audit, and the calibration are merged. The execution phase
  is **Phase-393** (numbering: the repository's registered
  phase space ends at Phase-392 (Spec 027); 393 is the first
  free number).
- The frozen contract is registered on OSF **before**
  execution, following the Spec 027 Stage 1 sequencing rule.
- Phase-392's record is never rewritten by this spec. If
  Spec 028 changes the reading of Phase-392's INCONCLUSIVE,
  that is recorded as a historical assessment appended under
  Spec 028, not as an edit to Spec 027.
- No anchor is touched and no PRED-2026 scoring occurs under
  this spec, whatever the verdicts.

AI disclosure: recorded by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution §VI. The decision text above is the owner's,
given in the program chat on 2026-10-11; the design
decisions are the program's under his delegation.
