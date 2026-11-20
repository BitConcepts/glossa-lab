# Spec 097 — Adoption and registration record, 2026-11-20

## The commission and the placement direction

On 2026-11-20 the owner commissioned the second-target ancient
language work in parallel ("start the other ancient language
decoding work"), the Meroitic benchmark among it, and then
directed that the benchmark be set up as its own separate program
in Glossa-Lab rather than as a deliverable inside Spec 095's
package. That direction is the adoption act for this package
(T003). It supersedes the placement under claim C095-16 (a study
scoping inside Spec 095); it does not supersede, amend, or
re-derive any part of the founding scoping's substance: the
target, the three legs, the success criteria and the falsifier
were fixed on 2026-11-17 in
`specs/095-red-team-remediation/second-targets/meroitic-benchmark-scoping-2026-11-17.md`
and are carried into this package's spec section 3 as written
there. The scoping document stays in place, unedited, as
provenance.

One step-0 PR had been opened under the old placement (PR #603,
the step-0 identity record and execution freeze filed under Spec
095's records). It was closed unmerged on the placement
direction, with the supersession stated on the PR; its substance
(the pin, the license record, the independence reading log, the
freeze) moves into this program's Stage 1 records unaltered, and
the computations already run under that freeze (Legs A and B)
stand as this program's Stage 2 work under its own records.

## The number (D-097-1) — renumbered in flight

Checked 2026-11-20 before the package was written: origin/main
at `e7e7898f8730f5a41e48c1c11d5a4ecab8f3b4c8`; the highest landed
spec directory was `095-red-team-remediation`; no `096-*`
directory, branch, or open pull request existed on origin, and
the parallel Eteocypriot worker had pushed nothing. 096 was
therefore the next free number actually free at check time, and
this package was drafted and first filed under it (setup PR
#607, with the full registration discharged on that base: ledger
at 1,031 lines / 1,000 claims, gate at the standing profile in
both modes, the pin-bearing test files passing).

The Eteocypriot program then landed 096 first (PRs #604, #605
and #606, merged 2026-11-20; main at `88ec96fa`), its intake
growing the ledger to 1,029 lines / 998 claims and the study
register to 97. Under the owner's shared-file discipline, and
the draft's own D-096-1 terms, this package renumbered to
**097** rather than colliding: PR #607 was closed unmerged with
the renumbering stated on it, and the whole registration was
re-applied cleanly on top of the landed main — ledger intake,
taxonomy entry, settling-chain refresh, generated layers, and
census pins — dropping no Eteocypriot entry. The platform
project (below) carries no spec number and stands as created.

## Registration (T001), as re-applied on the landed main

- Claims C097-1..C097-6 intaken into
  `glossa-indus/ledger/claims.jsonl` through
  `tools/ledger/import_bundle.py` (route 2), dated 2026-11-20:
  the ledger grows from 1,029 lines / 998 claims to 1,035 lines
  / 1,004 claims.
- Program-map taxonomy: one study entry,
  `097-meroitic-reproduction-benchmark`, domain "Sign inventory &
  corpus", subdomain "Signary & corpus models" (D-097-2),
  alongside the Eteocypriot program's own entry, untouched.
- The generated layers regenerated in dependency order
  (matrix, map-data, program map).
- The settling chain refreshed in the standing order against
  the grown ledger (verify-canonicals first; the T405 pair
  re-executed with byte-equal result blocks; the comparison
  re-filed; the sets re-materialized; the canonical pin
  refreshed with the re-derivation recorded; the superseded
  generation departed with its accounting).
- Census pins moved by this intake, updated in the same pull
  request from the regenerated artifacts' actuals: claims 998 to
  1,004, studies 97 to 98, and every derived count (population,
  class, falsifier coverage, matrix cells, edge census, claims
  untouched by any run, domain totals, the dashboard census, and
  the T405 run-of-record ids in the dashboard tests); each move
  is a consequence of the six new draft claims and the one new
  study, and of nothing else.

## AEE verification (T002)

The bundle's `aee validate` and `aee assess --no-ledger`
outcomes are recorded verbatim in
`records/adoption-aee-assessment.json` (the assessor's own
output) alongside this record; the summary line is quoted in the
landing pull request. The validate run reads "valid: 6
claim(s)"; the assess outcome is **iterate**, the expected
draft-stage reading for a bundle on asserted sources (the same
reading Spec 094's bundle received at adoption). The bundle was
re-validated after the renumbering (claim ids C097-1..6); the
assessment of record is the renumbered bundle's.

## Platform registration (T004)

The owner's direction of 2026-11-20 also places this program
inside the Glossa-Lab platform itself. Two acts, both verified
by read-back through the backend API (127.0.0.1:8001, token
auth; the token was read in-process from the install's token
file and is not recorded anywhere):

1. **The project.** Created through the platform's own Projects
   API (`PUT /api/v1/projects/meroitic_reproduction_benchmark`,
   HTTP 200), the same machinery the dashboard and the project
   seeder use. Read-back (`GET /api/v1/projects/meroitic_reproduction_benchmark`,
   HTTP 200) shows: id `meroitic_reproduction_benchmark`, label
   "Meroitic Reproduction Benchmark", slug
   `meroitic-reproduction-benchmark`, the program's question
   ("Is the published record of Otten & Anastasopoulos (2025)
   reproducible from its published corpus by its stated
   methods?"), its standing position (the C097-6 bound, in
   surface-neutral form), and `corpus_ids: ["cat-meroitic"]` —
   the catalogue's existing Meroitic corpus entry. The project
   list read-back shows exactly two projects, and the active
   project remains `indus_decipherment`: the Indus program's
   project, records, and stores were not disturbed, and this
   project was not activated. (Created during the 096 filing;
   the project record carries no spec number, so the
   renumbering does not touch it.)
2. **The registered work.** The platform carries a program's
   claims and studies in its record machinery, not in the
   project record: the claims ledger (this intake: claims 998
   to 1,004, visible on the ledger-driven dashboard and map
   surfaces) and the spec-study register
   (`GET /api/v1/spec-studies/{spec_id}`, which enumerates the
   serving tree's `specs/` directories). The register entry for
   097 reads back from the live API once this package lands in
   the serving tree through the normal merge-and-pull; that
   read-back is verified and recorded in Stage 1's step-0
   record, and the dashboard census figures move with the same
   landing (claims 1,004, ledger lines 1,035 — the pins updated
   in this package's pull request).

What the project model cannot carry, recorded rather than worked
around: the project record has no field linking it to a spec
package or to ledger claims (its link fields are discovery
topics, graph experiments, and corpora), so no such link was
improvised in a parallel store. `experiment_ids` is empty
because no registered graph experiment exists for this benchmark
(the platform's legacy Meroitic benchmark is not this program's
work and is not claimed as it); `topic_ids` is empty because
discovery topics are feed registrations and none exists for
Meroitic. If either is wanted, it is a platform change under its
own spec, not a setup improvisation.
