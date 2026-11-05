# Spec 093 — Claims

Every claim carries at least one falsifier (a concrete
observation that would show it false) and a "does not
establish" line (the over-reading it forbids), per the
program's claims discipline. The same set, normalized into
`aee-claims.json` without substantive change, is validated
under the pinned AEE (1.5.3) at drafting (T002;
`records/t002-note.md`). **These claims are drafts for
ratification: none is in the ledger, and nothing below is
a result.** The claims enter the ledger only at adoption,
through the sanctioned intake, as this spec's only ledger
diff (C093-11).

Grounding for every factual statement below:
`records/grounding-data-inventory-2026-11-05.md`, counted
and read first-hand from the repo on 2026-11-05.

**Ordering rule (the cap).** C093-1 is this spec's first
claim by design: it asserts that the material-context
channel is a different projection of the candidate state
than the sign sequences. Every downstream culture-side
claim in this spec (C093-7, C093-8, and any claim a stage
adds later) is stated under it and may not be stated
stronger than C093-1's recorded standing after its Stage 2
test. If C093-1 falls, the downstream claims fall to
bookkeeping statements about the record system, and the
spec's outcome vocabulary (§5 of spec.md) says so.

## The channel and its independence

**C093-1 — The material-context channel is a different
projection of the state, not the sequence table
re-expressed.** A candidate state in G1 §2.1's sense
determines, for each inscribed object, both its text (the
sequence the record system's coded corpora carry) and its
material-context tuple as this spec defines it at Stage 2:
the per-object recorded values of site, material class,
artifact type, holding/provenance, and find context, under
the vocabularies the Stage 1 normalization registers. The
channel claim is that this tuple is not a function of the
object's sequence table together with the record system's
bookkeeping (source system, frame, derivation): there is
no rule, statable in advance of Stage 2's freeze, that
computes the tuple from the table and the bookkeeping
alone. Stage 2 administers exactly this: a pre-registered
prediction test in which the frozen culture-side fields
are predicted from table-plus-bookkeeping features under
permutation controls, and the channel stands as
independent only at the strength the audited outcome
records (spec.md §5's vocabulary).
*Falsifier:* a statable rule or fitted predictor, frozen
before its administration, that recovers a registered
culture-side field from sequence-table-plus-bookkeeping
features at or above the freeze's stated bar on held-out
objects — the channel, for that field, is the same
information re-expressed, and C093-1 falls for that field
(the outcome record names the field).
*Does not establish:* that the channel, where independent,
carries information about any reading, sign value, or
language identification — independence is a claim about
projections of the state, not about what either projection
says. Condition 1 (Spec 090, DERIVED) is untouched: this
claim asserts a second projection exists to be tested; it
does not assert the second projection separates any pair
of states.

**C093-2 — The inventory is complete against its named
sources.** The grounding record's field census covers
every culture-side field present in its named sources
(the corpus snapshot, the M77 and ICIT flat files, the
CISI coded subset's loader, the three contact-zone
rebuild files, and the corpus-catalogue seeder): each
field a named source carries that names site, material,
artifact type or typology, holding or provenance, find
context, period, or execution medium appears in the
census with its presence count, or the census names the
field and states why it is not culture-side.
*Falsifier:* a culture-side field, in the census's sense,
present in a named source and absent from the census —
exhibited by file, key, and one record carrying it.
*Does not establish:* that the census's sources are all
the culture-side data the program holds anywhere — the
claim is bounded to the named sources, and a source
outside the list is Stage 1's to add by amendment, with
the census re-run.

**C093-3 — The snapshot's joint coverage is as counted,
and it binds every pass.** Within the corpus snapshot as
pinned, the records carrying both a recorded sequence and
a non-empty material number **0**, and the records
carrying both a recorded sequence and a non-empty
site_name number **966**, all in the indusscript-m77
subset. No Stage 4 pass may consume a joint population the
snapshot does not contain: a material-side pass over
sequences runs only on a Stage 1 join that has passed its
audit (C093-9), and a site-side pass runs only on the
populations the freeze enumerates.
*Falsifier:* one snapshot record, exhibited by
`glossa_id`, carrying a non-empty `canonical_grapheme_ids`
list and a non-empty `material`; or a Stage 4 pass whose
population includes a record pair no audited join produced.
*Does not establish:* that the underlying objects lack
materials or sites in the world — only that this record
system does not carry the joint fact, which is the
constraint the design answers to.

## Comparanda and acceptance discipline

**C093-4 — Every computed comparison answers to a
register entry frozen before it.** A cross-cultural
comparison is computed under this spec only if a
comparanda-register entry naming (i) the comparanda set,
(ii) the transmission mechanism — documented trade,
contact, or continuity, stated as a checkable historical
claim with its source, (iii) a fixed time window, and
(iv) the practice compared, was committed before the
computation's first run. Wide windows (centuries to
millennia) are admissible only where the entry's mechanism
is a continuity claim stated at that span; a window's
width is never a substitute for its mechanism.
*Falsifier:* a comparison result in any stage record whose
register entry is absent, postdates the computation, or
lacks any of (i)–(iv).
*Does not establish:* that a registered comparison is a
good comparison — only that it was fixed before it met
the data, which is what makes its outcome a test rather
than a fit.

**C093-5 — No window moves after a pattern is seen.** A
comparanda entry's window, set, mechanism, or compared
practice, once any computation under it has run, may be
changed only by a new entry that supersedes it; every
result computed under the superseded entry is voided in
the same act and may not be cited, including in the
superseding entry's rationale.
*Falsifier:* a cited result computed under an entry whose
terms differ from the terms frozen when it ran; or an
amended entry whose predecessor's results survive anywhere
in the spec's records as live.
*Does not establish:* that the original windows were well
chosen — only that the register's history is append-only,
so a reader can see every window that was ever tried.

**C093-6 — Acceptance is by the registered controls, or
the pass does not count.** A Stage 4 pass is accepted only
if its frozen design's negative controls (permutation or
shuffle of the culture-side labels within the strata the
design names) and its replication arm (held-out sites
where the design names them, and the inventory's counts
allow them) were run under Spec 089 run discipline and
the audited comparison of pass against controls meets the
freeze's bar. A pass whose controls were not run, or
whose bar was set after its first run, is recorded as NOT
YET with the obstruction named, whatever its uncontrolled
numbers look like.
*Falsifier:* an accepted pass in any stage record lacking
its registered controls' run records, or resting on a bar
absent from its freeze.
*Does not establish:* that a pass meeting its bar is true
in the world — only that it survived the controls this
program requires before a number may be cited.

**C093-7 — Culture-side regularities, where any are
accepted, are stated at channel strength.** A statement
this spec accepts about how inscription behavior
conditions on a culture-side field (for example: sequence
length or sign-choice distributions differing by site or
by material class beyond the registered controls) is
stated as a fact about the joint distribution of the two
projections over the named population, and carries
C093-1's recorded standing as a premise on its face.
*Falsifier:* an accepted statement of this form whose
population, controls, or premise citation is absent; or
one that survives in the records after C093-1's standing
for its field has fallen, unstated at the fallen strength.
*Does not establish:* anything about why the regularity
holds — no reading, function, or historical cause is
asserted by a distributional statement, and none may be
read into one.

**C093-8 — The honest stops are outcomes, not delays.**
Where a stage's frozen floors fire — a joint population
below its floor, a held-out arm the counts cannot carry
(the inventory names the standing case: four of six named
sites in the sequence-bearing subset carry 7 or fewer
records), a join that fails its audit — the stage records
NOT YET (the administration ran and did not meet its bar,
obstruction named) or CANNOT BE ADMINISTERED (the frozen
administration cannot be run, forcing counts shown) and
stops. No threshold, floor, population, or case is
adjusted under this spec to convert a stop into a pass.
*Falsifier:* a stage outcome recorded as accepted over a
fired floor; or a floor, threshold, or population in a
stage record differing from its freeze without a
superseding freeze that voids the earlier runs.
*Does not establish:* that a stopped stage was badly
designed — the floors are the price of the acceptance
machinery meaning anything, and a stop is a finding about
the record system's present contents.

## The join, the restrictions, and the one truth store

**C093-9 — A join is a claim, and it is audited before
use.** Any identification of a snapshot museum record with
a text-bearing record (by accession number, holding,
catalogue identity, or published concordance) that a
Stage 4 pass consumes was produced by a join procedure
frozen at Stage 1 and audited on a hand-checked sample
whose size and measured precision the audit record states.
A pass resting on an unaudited join, or on a join whose
measured precision falls below its freeze's floor, does
not run; the stage records the stop under C093-8.
*Falsifier:* a consumed join pair the frozen procedure
does not produce; or a pass whose join audit record is
absent, or whose stated precision is below the frozen
floor, with the pass nevertheless run.
*Does not establish:* that an audited join is correct pair
by pair — precision on a sample is the claim, and the
audit's sample and errors are part of the record a reader
judges.

**C093-10 — No restricted material enters this spec's
records, and the contact bar stands.** CISI enters this
spec only as statistics and data-list metadata lawfully
held and publishable under the standing restriction
(scans never redistributed, never in the repository); the
Laursen author copy never enters the repository (the
rebuilt Table 1 is the artifact); no stage act contacts
Andreas Fuls, and no stage act creates an account or
channel in any person's name.
*Falsifier:* a CISI scan or other restricted source
material present in the repository or in any stage output;
a redistribution of restricted content rather than
statistics or metadata; or a contact record to the barred
person attributable to this spec.
*Does not establish:* anything about the restrictions
themselves — only that this spec's design never needs to
touch them.

**C093-11 — One truth store: the ledger, and the
generated layers stay generated.** Culture-side claims
enter the system only as claims in the append-only ledger
(the family this spec adds at adoption, C093-1 onward),
entered through the sanctioned intake. The matrix rows
and the program-map layer for the material-context domain
are generated from the ledger by the registered
generators; no culture-side statement appears in the
matrix, on the map, or in any derived surface that is not
a ledger claim cited by its id; no generated file is
hand-edited. This spec's ledger diff across its whole
life is its adoption intake plus the claim appends its
later stages ratify one by one.
*Falsifier:* a matrix cell, map node, or derived statement
in the material-context layer carrying no ledger id, or
citing an id the ledger does not contain; a hand-edit to
a generated file attributable to this spec; a ledger diff
attributable to this spec beyond ratified intakes.
*Does not establish:* that the ledger's claims are true —
only that the one-way flow (ledger → matrix → map) this
program's publication discipline rests on survives the new
domain intact.

**C093-12 — Every culture-side gap entry carries its
falsifier and its acceptance test.** Each entry in this
spec's gap register (Stage 6, extending the Spec 088
register's discipline to the culture-side unknowns:
GR-093 series) states, on its face: what is not known; a
falsifier — the observation that would close or break the
entry's present statement; an acceptance test — the
administration whose outcome would discharge the entry;
and an honesty-rule type in the register's existing
vocabulary. An entry lacking any of the four is not an
entry, and the register's completeness check counts it as
a failure.
*Falsifier:* a GR-093 entry missing any of the four
elements, exhibited by entry id; or a completeness check
that passes over such an entry.
*Does not establish:* that the register enumerates all
culture-side unknowns there are — only that every entry
it carries is stated in the shape that lets it be closed
honestly.

**C093-13 — The boundary: nothing existing moves.** No
act under this spec adjudicates, reclassifies, annotates,
or scores any claim already in the ledger; no Indus claim
changes status, stage, or score citing this spec; the
program's standing position (the Indus script is not
deciphered) is untouched, and nothing in this spec is a
decipherment claim, evidence for a reading, or a step that
presupposes one.
*Falsifier:* an existing claim's status, stage, or score
changed with this spec cited as the act; or a stage
record stating a reading, a sign value, or a language
identification as supported by this spec's work.
*Does not establish:* anything about the existing claims —
only that this spec's front is additive and its boundary
is where it says it is.

**C093-14 — The outcome is recorded and reported, either
way.** The spec closes with an outcome record stating, per
stage and in the vocabulary of spec.md §5, what was
administered, what was accepted, what stopped and at what
counts; and the outcome is reported to the VEXA chat for
the improvement registry as a closeout deliverable, in the
outcome record's own words.
*Falsifier:* the spec closing with no outcome record; an
outcome stated in vocabulary §5 does not define without
mapping to its terms; or no report delivered after the
outcome record lands.
*Does not establish:* that the reported outcome settles
the channel question — later stages, later joins, and the
reader stand after it.
