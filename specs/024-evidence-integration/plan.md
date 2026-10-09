# Plan — Spec 024 / Evidence Integration

> ## DRAFT — PROPOSAL FOR OWNER ADJUDICATION — NOT FROZEN
>
> Companion plan to `spec.md`. Nothing in this plan
> is authorized until the owner answers §11 of the
> spec and a stage is frozen under §12.

## Approach (proposed)

**Stage 0 first, and alone.** The inventory is a
measurement exercise over files already local —
the same discipline Spec 023 applied to
transcription: measure coverage and joinability
before designing anything that depends on them.
Three work products, in dependency order:

1. **Coverage matrix** (§3.2): scripted field audit
   over the Phase-124 catalogue CSVs, the Holdat
   corpus file, the mayig layer + source corpus, the
   horus84 inscriptions table, the museum open-data
   records, and a documented pass over the
   non-machine-readable material (Kodumanal volume,
   Kunal article) that records their field structure
   without pretending to counts it cannot support.
2. **Join-key audit** (§3.3): every candidate key is
   tested empirically against the volume-scoped
   catalogue keys; match / ambiguous / unmatched
   counts and collision rates are the output. The
   prohibited key (`cisi_number`) is documented as
   inventoried-and-never-joined.
3. **Field-provenance grading** (§3.4): O / C / I
   grade per field with reasons; Class I fields are
   listed precisely so their exclusion is auditable.

Stage 0's report then states which §5 sketches
survive. No Stage 1 design work begins inside
Stage 0 beyond that statement.

**Stage 1, if separately approved,** follows the
Phase-132 machinery deliberately: frozen sample
draw with recorded seed, blinded independent
coders, adjudication with a preserved disagreement
log, gold subset, gates and a stop-rule frozen
*before* any image is coded, and the AI-disclosure
carried verbatim if AI coders are used. The pilot's
product is a measurement of codability — the codes
themselves are secondary.

**Stage 2, if ever,** is one freeze per test
family, with the family declared before the first
freeze, so the multiple-comparison discipline of
§5.1 has a fixed denominator.

## Principal risks the staging is designed to retire

- **Phantom joins.** The Phase-131 failure mode: a
  key that *looks* shared and is not. Retired by the
  §3.3 audit before any join is used, with collision
  rates on the record.
- **Theory in context costume.** A compilation's
  interpretive annotations (noun / verb / morpheme /
  "translation") silently treated as independent
  context. Retired by the §3.4 grading and the
  Class I exclusion.
- **Coder-dependent evidence treated as fact.**
  Motif labels are someone else's coding until
  Stage 1 measures whether coding can agree with
  itself. Retired by gating Stage 2(b) on Stage 1's
  proceed gate.
- **Fishing.** Dozens of context × text crossings
  computed and the significant ones reported.
  Retired by the declared family + BH-FDR discipline
  and the EXPLORATORY label rule (§5.1).
- **Composition masquerading as pattern.** Site and
  object-type mixes differ across every layer.
  Retired by mandatory within-stratum controls in
  every Stage 2 freeze (§5.1), with Phase-131's
  composition measurement as the standing warning.
- **Lineage laundering.** ICIT-lineage results
  reported as if independent. Retired by the
  headline-label rule (§5.1) and §2.4's standing
  determination.

## What this plan never does

Mint or move a reading; feed PRED-2026; pool
graffiti with seal texts; back-fill a field a source
does not print; move an image into git; or contact
anyone. (Spec §8 and the epistemic boundaries govern;
this list is a reminder, not a substitute.)
