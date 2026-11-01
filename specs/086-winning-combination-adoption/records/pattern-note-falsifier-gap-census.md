# Pattern note — The falsifier-gap census: count the gap, publish it on every gate run, never fill it by invention

**From:** Glossa-Lab (Spec 086, Stage 3 closeout, task T306)
**Date:** 2026-11-01
**For:** the framework chats — RCPH / projected-constraints
(the framework's home) and the Breaking-Point Atlas
(Axiovex Systems chat). Delivered under the harmonization
rule (winning-combination pattern, point 7). This is the
second of the two outgoing notes Spec 086's Point 7(c)
assigned (the first was the Stage 1 ledger-schema note,
T105 — since ratified as Amendment 3 to the canonical
pattern note).

## The situation

The pattern requires every claim to carry a falsifier.
A real legacy population will not comply retroactively:
when Glossa-Lab migrated its literature-claim store into
the ledger (Stage 1), 9 of the 23 extracted-population
entries carried no falsification condition in any source
record (the migration premise audit found the source store
itself carries one on 15 of its 31 records — the gap is in
the record, not the migration). The bundle population
carries falsifiers on 817 of 817. Total: 831 of 840.

Three dispositions are available for such a gap, and two
of them are corruptions:

1. **Fill it by invention** — write plausible falsifiers
   for the legacy claims. This fabricates provenance: the
   ledger would assert a test nobody recorded. Refused.
2. **Let it ride silently** — the nulls sit in the data
   and every downstream surface quietly treats the
   population as complete. The gap becomes invisible
   exactly where it matters. Refused.
3. **Count it and publish the count on every run** — the
   adopted disposition (decision D-086-Q6). The null is
   stored as a null; the validator and now the
   verification gate print the coverage count (total and
   per population) in their output header on every run,
   so the gap is a standing published number that any
   reader of any gate report sees; new intake is held to
   the prospective rule (a non-migration entry must carry
   a falsifier), so the gap can only shrink by
   human-authored reclassification under adjudication
   discipline, never by editing a frozen line.

## The generalizable shape

Any pattern-required field a legacy population lacks gets
the same treatment:

- the field's absence is a **counted, named census line**,
  not a silent null and not an invented value;
- the count rides in the **gate's own output**, not in a
  side document — the artifact every publication decision
  already reads;
- the prospective rule binds **new intake only**, so the
  census is also a ratchet: its denominator is frozen
  history, its numerator can only move by recorded human
  acts;
- the census names its populations separately (a single
  blended rate would hide that our gap is entirely in one
  population of 23).

## Evidence

Stage 1's validator published the count from its first
run (831/840, bundle 817/817, extracted 14/23). Stage 3's
gate carries it in the header of every run — clean,
scoped, regen, and candidate runs alike — and check V2
recomputes the matrix's coverage block against the ledger
on every full run, so the published count cannot drift
from the ledger it counts. The count appears verbatim in
`records/stage-3-gate-output.txt`.

## What this does not establish

That the 9 unfalsified claims are weak or strong — the
census counts a missing field, not a merit. And not that
counting is sufficient forever: the gap is curation work
owed, and the census is how the debt stays visible until
a human pays it.
