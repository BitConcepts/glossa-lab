# Spec 093 Stage 1 — stage record (2026-11-06)

Stage 1 (Inventory, normalization, join) executed 2026-11-06
under the ratified plan. Three tasks, three records, one
outcome per task; the tasks' *this does not establish* lines
are carried verbatim in their own records and in tasks.md.
No claim's status was changed by this stage; no Stage 2 work
was started.

## T101 — Census completion: DONE

Record: `records/t101-census-completion-2026-11-06.md`;
computation: `tools/spec093/stage1_census.py` over the
pinned files. The grounding inventory is amended on seven
points (A1–A7, census record §8), the largest being the two
sources it missed: the canonical store as a population in
its own right (19,925 records, incl. the 4,417-record
MuseumsOfIndia population the research export rejected) and
the CISI data-list compilation (5,679 rows × 38 fields — the
only in-repo per-object material/site/period/typology source
for text-bearing objects). C093-3's disjointness re-counted
on the pinned snapshot: sequence ∧ material = 0,
sequence ∧ site = 966 (all indusscript-m77; Mohenjo-daro
839, Harappa 110, Chanhu-Daro 7, Sutkagen-Dor 6, Lothal 3,
Kalibangan 1). Confirmed as register-bound gaps, not
patched: the snapshot's artifact typology is degenerate
(seal 10,072 / unknown 5,436) and it carries no per-record
period field.

## T102 — Material normalization register: DONE

Register: `records/material-normalization-register-v1.json`
(253,354 bytes, SHA-256
`fe8d454252c12af6cd342c14f5a45ecae6dab28040f10682ef86278c95405764`)
with its document `records/material-normalization-register-v1.md`;
generator `tools/spec093/build_material_register.py`;
checker `tools/spec093/check_material_register.py`.
Coverage: all **1,122** distinct raw `material` values in
the pinned snapshot, **11,839** records — class 663 values /
10,987 records; composite 370 / 638; alternatives 15 / 29;
non-material 49 / 157 (by rule, with reason codes); unmapped
25 / 28, each named in the register with its reason.
Uncertain-flagged: 139 values, 233 records. The register is
bound to the snapshot's population; the CSV's 23 material
values are not covered (register document §1).

Acceptance check execution (2026-11-06): the checker
re-applied the rules from the artifact itself against the
pinned snapshot and **passed**: "PASS: 1122 distinct values,
11839 records; rules re-applied from the artifact agree on
every value" (full line in the checker's output; per-kind
aggregates in the register document §4). Seeded-failure
proofs, all failing as required: a copy of the register with
one value ('Steatite') dropped fails check 1 (value set
diverges); a copy with one disposition tampered
('Steatite' → classes ['stone-unspecified']) fails check 2
(disposition diverges from recomputation); a copy with one
unmapped reason removed ('Ao') fails check 4 (unmapped value
without a reason).

## T103 — Join design, freeze, precision audit: DONE (floor cleared)

Freeze: `records/t103-join-freeze-v1.md` (frozen before the
audit ran; floor 0.90 identity precision per key family;
complete-enumeration audit rule). Audit:
`tools/spec093/run_join_audit.py`; machine record
`records/t103-join-audit-v1.json` (SHA-256
`4405167610ed13c05603d7c54684761889c955cbc0c0a70fe1e4097eae7b7d9e`); record
`records/t103-join-audit-2026-11-06.md`. Outcomes:

- **K1 (cross-population exact keys): REJECTED.**
  `accession_number` produces 0 pairs (museum-side only).
  `source_object_id` produces 7 pairs, 0 correct,
  precision 0.000 < 0.90 — bare-integer collisions between
  Penn registration numbers and Mahadevan text indices; the
  seven museum records are North American and Japanese
  objects, individually listed in the audit record.
- **K2 (CISI catalogue concordance): ACCEPTED.** 179 pairs
  produced, 179 correct, precision 1.000 ≥ 0.90; the key is
  1:1 on the population; no unmatched text records.
  Diagnostics over the true pairs: token-count agreement
  150/179 (83.8%), count-field agreement 149/179, 29
  content disagreements censused (largest +6 tokens), 24
  count-field-artifact pairs (incl. 4 non-numeric CSV count
  fields, the data list's own '4+?' marks).
- **Join output:** `records/t103-join-pairs-v1.jsonl`,
  179 pairs (SHA-256 `7107f738832a4e3b04cff91d81073212bc0f3a77afed6f0ccc3cee4fce621703`). Coverage bound:
  179 of 3,085 text-bearing records (5.8%), one site
  (Mohenjo-daro); the Mahadevan population has no in-repo
  concordance. **The material arm is not stopped** — Stage 4
  may administer its material pass over this population
  under its own freeze and C093-1's standing; the joined
  material values are raw and need a successor register
  before any normalized material pass (audit record §5).

## Stage 1 outcome

All three Stage 1 tasks are complete. Stage 2 (channel
definition, T201) consumes this stage's vocabularies — the
register's classes for material, the census's populations,
the CSV's typology for the joined slice — and is not
started by this record. The two absences the plan names
(artifact typology, period per record) stand confirmed as
register-bound gaps for Stage 6, with the single bounded
exception the join creates: typology and period exist for
the 179 joined objects, from the data lists, at data-list
trust.
