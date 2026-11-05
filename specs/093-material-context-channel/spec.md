# Feature Specification: The Material-Context Channel — a second projection for the Indus record system (Spec 093)

**Feature Branch**: `093-material-context-channel` (build stages); this
package lands on `docs/093-material-channel-draft`
**Created**: 2026-11-05
**Status**: Draft package — awaiting the owner's block ratification
(Stage 0). **Nothing in this package is a result: no pattern over
the corpus has been computed, no claim below is in the ledger, and
the study this spec designs has not been administered in any part.**
**Input**: The owner's commission in this chat, 2026-11-05, in two
parts. First: a different sort of Rosetta Stone — "perhaps one based
on culture or architecture or other aspects, perhaps even writing
style and what things had what written on them and what was common
at the time in history plus and minus at least a few centuries up to
millennia (just in case they were ahead or behind the rest of the
world for their time)". Second, in the same commission: "we need to
build a projected constraint matrix/structure/atlas for what we
know and what we don't and to analyze the gaps with falsification
and acceptance tests."
**Evidence of record**: the grounding inventory in
`records/grounding-data-inventory-2026-11-05.md`, counted and read
first-hand from the repo on 2026-11-05 (presence counts only; no
pattern computed): the corpus snapshot's 15,508 records split into
a sequence-bearing population and a metadata-bearing population
that are disjoint except for site (sequence ∧ material = 0 records;
sequence ∧ site = 966, all indusscript-m77, 6 named sites, top site
839); the Laursen Table 1 rebuild (121 rows, typology and
metrology, no sequences); the contact-zone rebuild (14 Indus seals
excavated in Mesopotamia; 1,462 Meluhha tablet hits); the corpus
catalogue's 39 world-script corpora with period and script-type
fields; the Finnish Academy's email to the owner of 2026-11-04
(no digital CISI edition exists or is planned; data-list text is
usable academically; photo reproduction needs owner/museum and
photographer/commissioner permission).
**Predecessors**: Spec 086 (the one append-only claims ledger as
sole entry point; the matrix generated from the ledger; the layered
map as primary surface citing ledger ids; truth flowing ledger →
matrix → map one way — this spec extends that machinery, it does
not build a second store); Spec 088 (the program map and the
37-entry gap register, every entry carrying a falsifier and an
honesty type — this spec extends the register's discipline to the
culture-side unknowns); Spec 089 (run-scoped results: every
computation this spec produces is a run under run-defs v1, cited by
run id, divergences junction); Spec 090 (the generalization study:
its Condition 1, DERIVED at full strength, is this spec's founding
constraint — §4, H1); Spec 090's G3 package (draft PR #523), whose
administration discipline (freeze before computation, bars stated
in advance, honest stops as first-class outcomes, claims drafted
but not appended) is this package's house template.

## 1. Problem statement

Every quantity this program has ever computed over the Indus
record system is a function of one projection of the candidate
state: the sign sequences. The positional grammar, the anchor
register, the settling semantics, the Spec 090 separator — all of
them read the text side of the records. Spec 090's Condition 1
then proved the ceiling of that projection: states with different
readings and a different language identification induce the same
sequence-side observations, so no test computed from the sequences
alone can separate them.

The records, however, carry a second side. An inscribed object
also has a site, a material, a type, a holding, a find context —
facts determined by the same historical state that determined its
text, recorded by different hands through different derivations,
and never yet treated as a channel in their own right. The
owner's commission names the intuition exactly: what things had
what written on them, in what medium, in what world, is itself
evidence — *if* it is a genuinely second projection and not the
first one wearing a costume, and *if* the comparisons it invites
are disciplined enough to be tests rather than pattern-matching
across an unbounded past.

The inventory states the problem's true shape, and it is harder
than the intuition suggests. In the snapshot as pinned, the
sequence-bearing and metadata-bearing populations are disjoint
except for site: **0** records carry both a sequence and a
material; **966** carry both a sequence and a site name, across
only 6 named sites, 839 of them one site. The material catalogue
is rich (11,839 records) but textless; the text corpus is
sequenced (3,085 records) but materially blank. The channel
exists; its joint coverage is presently one thin site arm and a
join that has never been built or audited. A spec that pretended
otherwise would compute its first "result" over a population
that does not exist.

This spec therefore designs the front in the only honest order:
inventory and normalization first; the channel-independence test
before any culture-side pattern is computed; the comparanda
register frozen before any comparison; the first passes only
over populations the record system actually contains, under
permutation controls and held-out arms; and the projected-
constraints extension (ledger family, generated matrix rows,
map layer, culture-side gap register) built as the same one-way
machinery the program already trusts, so that whatever this
front learns enters the single record of what the program knows
and what it does not.

## 2. Scope — what this spec builds

1. **A completed culture-side data inventory and a registered
   normalization** (Stage 1): the grounding inventory completed
   against any source it missed; `material` free text normalized
   to a registered material-class vocabulary with the rules
   filed; the artifact-typology and ductus gaps carried as
   register entries, not silently absorbed.
2. **A join, designed and audited** (Stage 1): the procedure
   identifying snapshot museum records with text-bearing
   records, frozen, with a hand-checked precision audit; the
   join is a claim (C093-9), not plumbing.
3. **The channel-independence administration** (Stage 2): the
   material-context projection defined formally against G1
   §2.1's state; a pre-registered prediction test with
   permutation controls; a freeze before any computation; an
   outcome recorded in §5's strength vocabulary. This stage is
   the spec's gate: no Stage 4 pass may be stated stronger than
   its outcome.
4. **A comparanda register v1** (Stage 3): entries naming
   comparanda set, transmission mechanism, fixed window, and
   compared practice, seeded from the corpus catalogue's 39
   corpora and the contact-zone records (the 14 excavated
   seals; the Meluhha documentary record; the Gulf/Dilmun
   typology population).
5. **The first computed passes** (Stage 4): site-conditioned
   sequence behavior over the populations the freeze
   enumerates (the 966, with the Harappa held-out arm where
   counts allow); a material-conditioned pass only over an
   audited join's population, if one exists; each pass a Spec
   089 run with its registered controls, adjudged against its
   frozen bar.
6. **The projected-constraints extension** (Stage 5): the
   ledger's material-context claim family (intaken at
   adoption); matrix rows for the domain generated from the
   ledger; a material-context layer on the program map citing
   ledger ids; the ledger gate extended so the culture layer's
   one-way flow is verified like every other layer's.
7. **A culture-side gap register v1 and closeout** (Stage 6):
   GR-093 entries in the Spec 088 register's discipline —
   each with what is not known, a falsifier, an acceptance
   test, and an honesty type — covering at least the gaps the
   inventory names (ductus, iconography, artifact typology,
   period-per-record, the material join's coverage), and the
   outcome record with the VEXA report (C093-14).

## 3. Non-goals (explicit)

- **No decipherment claim, no reading, no sign value.** Nothing
  in this spec asserts or presupposes any value for any sign;
  the standing position (the Indus script is not deciphered) is
  a boundary claim of the spec itself (C093-13).
- **No second truth store.** The matrix/structure/atlas the
  owner commissioned is the Spec 086 machinery extended —
  ledger → matrix → map — not a parallel database, spreadsheet,
  or document set with its own facts.
- **No computation before its freeze.** No stage computes a
  pattern, an association, or a comparison over the corpus
  before that stage's freeze record is committed. The drafting
  of this package computed presence counts only (the grounding
  record's method line), and no stage may cite drafting-time
  exploration, because there is none.
- **No contact, no accounts, no restricted material.** CISI
  enters as statistics and data-list metadata only; Andreas
  Fuls is never contacted; the Laursen author copy never
  enters the repository (C093-10).
- **No changes to existing claims.** This spec is additive:
  it appends its own family at ratified intakes and moves
  nothing that already stands (C093-13).
- **Not a convergence step.** This spec is Glossa-internal
  front-opening under the owner's commission; it does not
  advance VEXA convergence staging, and its VEXA-facing act is
  the closeout report alone (C093-14).

## 4. Hard constraints carried on the face

- **H1 — Channel independence first (Spec 090, Condition 1).**
  The package's first claim (C093-1) is that the
  material-context channel is a different projection of the
  state than the sign sequences, with a falsifier that would
  show it is the same information re-expressed. No downstream
  claim may be stated stronger than C093-1's recorded
  standing. A culture-side quantity derived from the sequence
  table (or from bookkeeping about it) is not channel data,
  however it is dressed.
- **H2 — Comparanda discipline.** Every cross-cultural
  comparison names its comparanda set and its transmission
  mechanism (documented trade, contact, or continuity) and a
  **fixed** window in advance, in the comparanda register.
  No sliding windows after patterns are seen (C093-5). The
  owner's wide window — centuries to millennia — is honored
  by letting the register carry wide-window entries whose
  mechanism is named (a continuity claim stated at that
  span), never by post-hoc matching against an unbounded
  past.
- **H3 — Controls are the acceptance machinery.** Permutation
  / shuffle negative controls within named strata, and
  held-out sites as replication arms where the counts allow,
  are how a pass is accepted; bars are stated in advance;
  honest stops (NOT YET / CANNOT BE ADMINISTERED, with the
  forcing counts shown) are first-class outcomes, in the G3
  package's pattern (C093-6, C093-8).
- **H4 — CISI discipline.** CISI material is restricted:
  statistics and data-list metadata publishable, scans never
  redistributed. The publisher's 2026-11-04 email confirms
  data-list text is usable academically and that no digital
  edition exists; nothing in this spec needs more. Andreas
  Fuls is never contacted.

## 5. Outcome vocabulary, bars, and honest stops

**C093-1's standing** (Stage 2's outcome, recorded once and
cited by every downstream statement):

- **INDEPENDENT AT FULL STRENGTH** — the frozen prediction
  test failed to recover any registered culture-side field
  from table-plus-bookkeeping at the freeze's bar, on the
  audited runs, controls behaving as registered.
- **INDEPENDENT IN PART** — the test failed for some fields
  and succeeded for others; the standing names the fields in
  each class, and downstream claims may cite only the
  surviving fields as channel data.
- **NOT INDEPENDENT** — the test recovered the registered
  fields at or above the bar: the channel, as defined, is
  the sequence projection re-expressed, and the spec's
  downstream claims fall to bookkeeping statements about the
  record system. This is a complete, publishable outcome of
  the spec, not a failure of it: it closes the front on
  evidence instead of letting it run on costume.

**Pass outcomes** (Stage 4, and any later administration):

- **ACCEPTED** — the frozen bar met in full on the audited
  runs, controls and replication arms as registered.
- **NOT YET** — the administration ran and the bar was not
  met, or could not be met as frozen, with the obstruction
  named. No re-administration under the same freeze repairs
  it; a successor attempt is a new freeze.
- **CANNOT BE ADMINISTERED** — the frozen administration
  cannot be run as specified: a joint population below its
  floor, a held-out arm the counts cannot carry, a join
  below its precision floor. The outcome record shows the
  forcing counts. (The inventory names the standing
  candidate: a six-site held-out design over the 966 cannot
  be administered as drawn — four sites carry ≤7 records —
  and a Stage 4 freeze that asks for it will record exactly
  that.)

Bars are numbers in freezes, not adjectives in outcome
records: each freeze states its prediction bar, its control
behavior, its floors, and its replication requirement
before its first run, and the outcome is adjudged against
exactly those.

## 6. Decisions

- **D-093-1 — This front's home: a new spec (093), not a
  stage of Spec 090 and not a wave of Spec 088.** Options:
  (a) new spec — the claim family, the data side, and the
  machinery extension are all new, while the governance is
  inherited; (b) a stage amendment to Spec 090 — wrong
  shape: Spec 090 tests the skeleton's instantiation, and
  its claims are about the framework, not about the Indus
  record system's second projection. *Recommendation: (a).*
- **D-093-2 — The channel's field set for Stage 2: the five
  recorded sides (site, material class, artifact type,
  holding/provenance, find context), with ductus and
  iconography excluded until data exists.** Options: (a)
  the five, as defined over the inventory's fields after
  Stage 1 normalization; (b) add a ductus arm now, coded
  from the snapshot's image URIs — rejected: the URIs point
  at museum images whose coding would be new human coding
  with its own blinding problem, and 12,423 of the records
  carrying images carry no text. *Recommendation: (a)*,
  with ductus and iconography carried as gap-register
  entries (Stage 6) whose acceptance tests name the coding
  protocol a future stage would need.
- **D-093-3 — The independence test's form: prediction
  under permutation, per field.** Options: (a) per-field
  prediction from table-plus-bookkeeping features, bar and
  controls frozen per field — a field falls alone, and the
  standing can be INDEPENDENT IN PART with the fields named;
  (b) one joint test over the whole tuple — a single weak
  field would sink the channel entire, and a single strong
  one would launder the rest. *Recommendation: (a).*
- **D-093-4 — The material arm runs only on an audited
  join.** Options: (a) Stage 4's material pass is gated on
  C093-9's audit clearing its frozen precision floor, and
  records CANNOT BE ADMINISTERED if no join clears it;
  (b) run the material pass on the museum population's
  internal structure alone (no sequences) and call it
  channel evidence — rejected: without sequences it is a
  statement about museum cataloguing, not about the joint
  state. *Recommendation: (a).*
- **D-093-5 — The gap register's form: a culture-side
  section of the existing register.** Options: (a) GR-093
  entries appended to `glossa-indus/map/gap-register.md`
  under their own section, with the register's mechanical
  completeness checks extended to count them — one
  register, one discipline, one completeness claim; (b) a
  sibling register file for culture-side gaps — a second
  surface for a reader to miss, and a second completeness
  claim to keep honest. *Recommendation: (a)*, with the
  adoption task owing the check extension in the same PR
  that lands the first entries (Stage 6), so the register
  never carries entries its checks do not count.
- **D-093-6 — The map layer's form: a generated layer, not
  a new map.** The material-context domain appears as a
  layer of the existing program map (taxonomy domain +
  generated nodes citing ledger ids), produced by the
  registered generators, with the ledger gate's checks
  extended to verify the layer's citations like every other
  layer's. Options: (a) as stated; (b) a separate atlas
  document for the culture side — rejected under C093-11:
  a surface that is not generated from the ledger is a
  second truth store with better typography.
  *Recommendation: (a).*
- **D-093-7 — Comparanda seeding: the catalogue plus the
  contact-zone records, nothing wider at v1.** The
  register's v1 entries are drawn from the corpus
  catalogue's 39 corpora (period and script type already
  carried) and the documented contact channels in-repo
  (Mesopotamian find contexts, the Meluhha documentary
  record, the Gulf/Dilmun population). Entries beyond those
  sources — Egyptian practice, later South Asian continuity
  at millennial spans — are admissible only as later
  register amendments, each with its mechanism argued from
  named sources before any computation under it.
  *Recommendation: adopt.*
- **D-093-8 — The report: the outcome goes to the VEXA
  chat either way.** Extends the program's standing
  practice (D-090-4, D-090-10) to this spec: the closeout
  outcome, in its own words, is reported for the
  improvement registry — a second-projection test, whatever
  it finds, is framework-relevant evidence.
  *Recommendation: adopt.*

## 7. Requirements (summary; the claims in claims.md are the normative text)

- **FR-093-01** — The culture-side inventory is completed
  and its normalization registered before any channel
  definition is frozen (Stage 1; C093-2).
- **FR-093-02** — The snapshot's joint coverage binds every
  population a pass may consume (Stage 1, Stage 4; C093-3).
- **FR-093-03** — The channel is defined against G1 §2.1's
  state and tested for independence per field, under a
  freeze, before any culture-side pattern is computed
  (Stage 2; C093-1).
- **FR-093-04** — No downstream statement exceeds C093-1's
  recorded standing (all stages; C093-1, C093-7).
- **FR-093-05** — Every computed comparison answers to a
  comparanda entry frozen before it, naming set, mechanism,
  fixed window, and compared practice (Stage 3; C093-4).
- **FR-093-06** — No comparanda term moves after a
  computation under it; supersession voids predecessor
  results in the same act (Stage 3 onward; C093-5).
- **FR-093-07** — Acceptance is by registered permutation
  controls and held-out replication against frozen bars
  (Stage 4; C093-6).
- **FR-093-08** — Honest stops are recorded with their
  forcing counts and are never converted by mid-course
  adjustment (all stages; C093-8).
- **FR-093-09** — Any join a pass consumes is frozen and
  precision-audited before use (Stage 1, Stage 4; C093-9).
- **FR-093-10** — Restricted material never enters the
  record; the contact bar stands (all stages; C093-10).
- **FR-093-11** — Culture-side knowledge enters only
  through the ledger; matrix and map layers for the domain
  are generated and gate-verified (Stage 0, Stage 5;
  C093-11).
- **FR-093-12** — Every culture-side gap entry carries its
  falsifier and acceptance test, and the register's
  completeness checks count the new section (Stage 6;
  C093-12).

## 8. Governance

Claims first (this package's `claims.md` / `aee-claims.json`,
C093-1..14), validated under the pinned AEE at drafting
(T002 — the invocation and verbatim reading are in
`records/t002-note.md`) and assessed again at adoption
before any build task starts. Verdicts and citations follow
program doctrine: numbers only from records read first-hand;
assessments by actually running the assessor; CI green or
the work is not done. Every computation this spec produces
is a run under Spec 089's run-defs v1, cited by run id in
its stage record; a divergence between comparable runs is a
junction, never an average. Publications flow through the
ledger gate, extended at Stage 5 to cover the culture layer
before any culture-side statement is published. The owner's
block ratification of this package is the ratification act
for the spec, the claims, and decisions D-093-1..8. One
expected draft-state note: like Specs 091/092's drafts, this
package adds a new spec directory with no program-map
assignment, so the draft PR fails the program-map assignment
gate until adoption assigns it; that failure is the gate
working as designed, not a defect in the package.
