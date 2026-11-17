# Standards of Record — Glossa-Lab Indus Program

Adopted 2026-11-16 (Spec 095 Stage 3: T302 states Parts I and II
under claim C095-8; T303 states Part III under claim C095-9).

These standards are stated once, here, program-wide. A study
adopted after this date cites the part it applies ("Standards of
Record, Part I") instead of restating a local rule; a local
restatement in a post-adoption record is a defect against C095-8's
falsifier. Results frozen before adoption keep the rules they were
frozen under: the standards do not retroactively re-judge them
(C095-8, does-not-establish). Divergences between the standards and
past practice are noted where they exist, in the open, below.

This document changes only by a recorded amendment: a dated
amendment section appended to the part it changes, in the same
change that adopts the new rule. A silent edit to a standard is a
violation of the standard.

## Part I — Equivalence

1. Equivalence between two quantities, distributions, or
   procedures may be claimed only against a margin registered
   before the comparison is run, by an equivalence test: a
   two-one-sided-tests procedure, or an interval rule stated in
   the freeze under which the uncertainty interval for the
   difference must fall inside the registered margin.
2. A non-significant difference test never establishes
   equivalence. It licenses exactly one statement: a difference
   was not detected, at the precision the study achieved (which
   Part II then requires the report to state).
3. The margin is part of the claim. An equivalence claim that
   does not name its margin, its test, and its registration point
   is not reportable.

Practice of record, and the divergence. The program's frozen
studies state numeric verdict bounds in advance and judge against
them (for example the Phase-125 pattern, spec 019 section 6:
median TV PASS at or below 0.35, FAIL at or above 0.50, with the
null bound stated alongside). Those are decision thresholds for a
difference claim, and this standard keeps them. No frozen study
of record runs an equivalence test, and no frozen text claims
equivalence in so many words; what the record does contain is
null results reported without the precision statement rule 2 now
requires (Part II names the instances). The standard governs the
prospective case: from adoption, "no difference was found" is not
an available paraphrase of "the two are equivalent."

## Part II — Statistical reporting

A statistical result is reportable only with all four of:

1. an effect size, in the units of the quantity compared;
2. an uncertainty interval, with its construction named (for
   example, inscription-level bootstrap, B and seed stated);
3. its multiplicity handling: the family of comparisons the
   result belongs to and the rule the family was judged under
   (pre-registered arms and a single verdict pattern are a
   handling; an unregistered search reported as a single result
   is not);
4. its achieved power or precision basis: what difference the
   study, at its actual sizes, could have detected (a power grid,
   a matched-size null, or the interval width itself read as the
   precision statement).

A p-value alone is never a reportable result.

Practice of record, and the divergence. The standard's four
elements are the program's own best frozen practice, stated once:
the Phase-127 diagnostic (spec 021) reports effect sizes as TV
distances, inscription-bootstrap intervals with B and seed, its
arms pre-registered under spec 019/021 as the multiplicity
handling, and a power grid (its section 8) giving the
tokens-per-sign at which its gate clears its own noise criterion.
Against that, parts of the older record report bare tallies and
bare p-values: the Phase-48 battery's pass counts (tests passed,
of six) carry no effect size or interval, and pipeline node
outputs have formatted a lone p-value into result text (named in
the Spec 095 Stage 2 census of the v1 validator family). Those
results stand as frozen; from adoption, a report that omits any
of the four elements is incomplete on its face.

## Part III — Identifiability of reading claims

1. A reading claim (a sign's proposed function, or its proposed
   phonetic value where the claim is phonetic) is *identifiable*
   on a body of evidence only if rival constructions are excluded
   by named evidence: observations in the record that the claim
   fits and the rivals do not.
2. A *rival construction* assigns the same evidence a different
   sign function and, where the claim is phonetic, a different
   value, drawn where possible from a named unrelated language
   family. The rival machinery of record is the WP8 control
   families (docs/repair-2026-10-26/wp8-exposure-and-controls.md,
   section 3): meaning permutations (C1), frequency- and
   position-matched wrong mappings (C2), plausible wrong
   morphology (C3), matched homophony and polyphony flexibility
   (C4), wrong-language candidates (C5), and structured
   non-language corpora (C6), run under WP8's fairness conditions
   (matched tuning budget, matched available evidence, the whole
   procedure challenged, section 3.3).
3. The program's non-identifiability rule, carried from WP8
   section 3.6: if two or more readings are observationally
   equivalent under the available evidence — every observation
   the procedure can make is equally consistent with each of
   them — the result is reported as non-identifiability. The
   procedure does not pick the best-looking one.
4. No reading claim is scored SUPPORTED at any strength without
   a rival-construction record. Where a rival construction fits
   the recorded evidence comparably, the outcome is recorded as
   NOT IDENTIFIABLE.
5. NOT IDENTIFIABLE bounds what the evidence can distinguish. It
   does not disprove a reading, and it does not move any other
   disposition a record carries: a support-lineage classification
   (for example, the WP5 audit's dispositions) answers who
   produced the support; identifiability answers whether the
   support excludes rivals. The two vocabularies are not
   interchangeable, and neither is silently converted into the
   other.

### Recorded amendment, 2026-11-16 — the outcome vocabulary

By this amendment the program's outcome vocabulary gains the
verdict **NOT IDENTIFIABLE**, with the meaning in rules 3 and 4
above, available to any study adopted after this date and to any
re-statement filed under this protocol. This amendment is the
recorded amendment C095-9 requires. The protocol's first
application — rival constructions against the six independently
supported anchors of record (M044, M047, M124, M202, M329, M330),
with per-sign outcomes and the six standings re-stated under
them — is filed at
specs/095-red-team-remediation/records/t303-identifiability-application-2026-11-16.md.
