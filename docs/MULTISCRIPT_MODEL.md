# The Multi-Script Data Model — Specification

**Status:** specified under Spec 095 Stage 4 (T401), discharging the
specification half of C095-11. The Indus instantiation is §6 of this
document, proven by the census in the Stage 4 record and by
`backend/tests/test_spec095_stage4_instantiation.py`.

**Provenance.** The external red-team review of 2026-11-15 (register
rows RT-24 and RT-26) required a shared abstraction supporting
multiple ancient scripts and languages, with sign shape separated
from phonetic interpretation and semantic interpretation, and no
Proto-Dravidian assumption embedded in generic platform
infrastructure. C095-11 fixes the entity set of record. This
document is that specification.

**A note on the entity count.** C095-11 and the Stage 4 task text
say "seventeen entities"; the enumeration of record in C095-11 names
eighteen (WritingSystem, LanguageHypothesis, Corpus, Artifact,
Inscription, Sign, SignVariant, Transcription, ReadingHypothesis,
TranslationHypothesis, Context, Evidence, Claim, Falsifier,
Experiment, Execution, Result, Adjudication — counted from the
claim text at Stage 4). The enumeration governs: this specification
covers every enumerated entity, each with its own claim and
falsifier (§3). The numeral in the claim text is recorded as a
package inconsistency in the Stage 4 record; no enumerated entity
is dropped to make the numeral true, and none is invented.

**Placement.** This specification lives at
`docs/MULTISCRIPT_MODEL.md`. It is not a new `specs/` directory: a
new spec directory is an adoption act (program-map assignment and
claims intake), which would change the ledger census the Indus
instantiation must prove unchanged. It is not under `glossa-indus/`:
the generic layer is platform-level, and filing it inside one
script's tree would embed exactly the single-script assumption the
model exists to remove.

## 1. Purpose

The platform studies undeciphered and partially deciphered writing
systems. Today every script's record is held in script-shaped
structures, so a second target is a fork. This model states the
script-neutral entities, their relations, and the rules any
script's record must satisfy to instantiate the model, so that a
second script's record is new data under one model, not new
machinery.

The model is a specification of record, not a database migration.
Instantiating it (§5) is a mapping with a census proof; it changes
no fact, count, or standing in the record instantiated.

## 2. Generic-layer rules

- **G1 — No script-specific assumption.** No rule, field, default,
  or vocabulary in the generic layer names a particular writing
  system, language, or language family. A rule that only makes
  sense for one script belongs to that script's instantiation,
  never to this layer. (Falsifier for the layer as a whole: a
  generic rule is found that names an Indus or Proto-Dravidian
  assumption.)
- **G2 — Shape, value, and meaning are separate entities.** A
  sign's shape (Sign, SignVariant) carries no phonetic value and no
  meaning. A phonetic value exists only as a ReadingHypothesis. A
  meaning exists only as a TranslationHypothesis. No field on a
  shape entity may hold a value or a gloss.
- **G3 — Namespaces are per writing system.** Sign identifiers,
  corpus identifiers, and transcription identifiers are unique only
  inside their WritingSystem namespace. Cross-system statements
  (crosswalks) are Evidence-bearing relations between namespaced
  entities, never silent merges of identifier spaces.
- **G4 — Uncertainty is carried as data.** Damage, ambiguity,
  ligature, missing signs, disputed segmentation, and reading
  direction are recorded on the entities they describe (per
  C095-10, orientation basis is data, never a silent
  canonicalization). An unknown is a stated unknown, not a default.
- **G5 — Every assertion is a Claim with a Falsifier.** Anything
  the platform asserts about a script — a reading, a translation, a
  structural regularity, an identification — is a Claim entity
  carrying its Falsifier, its Evidence, and its standing under
  Adjudication. Presentation surfaces render Claims; they do not
  mint them.
- **G6 — Lineage is typed.** Evidence records its lineage (source,
  derivation, independence class) in the vocabulary of the
  program's standards of record (`glossa-indus/STANDARDS.md` until
  a platform-level standards document supersedes it, and the
  corpus identity standard for corpora). A derived result is never
  typed as independent confirmation (the C095-7 contamination
  shapes are the negative catalogue for this rule).

## 3. The entities

Each entity states: its definition, its key attributes, its
relations, the claim the model makes for it (ME-nn), and that
claim's falsifier. Attributes are the minimum the generic layer
requires; an instantiation may carry more, never fewer, and may
not repurpose a required attribute.

### 3.1 WritingSystem

The outermost namespace: one attested writing system (e.g. the
Indus script), identified independently of any hypothesis about
the language it writes.

- *Attributes:* identifier; attestation basis (what objects attest
  it); sign-inventory frames of record (competing inventories are
  carried as frames, not silently chosen between — G4).
- *Relations:* owns Sign, SignVariant, Corpus, Artifact,
  Inscription, Transcription instances under its namespace.
- **ME-01.** Every script-level entity belongs to exactly one
  WritingSystem namespace. *Falsifier:* an entity instance is found
  belonging to two namespaces, or to none.

### 3.2 LanguageHypothesis

A hypothesis that a WritingSystem writes a particular language or
language family (or that it does not write language at all — the
nonlinguistic hypothesis is a LanguageHypothesis with the same
standing machinery as any other).

- *Attributes:* the language or family proposed (or the explicit
  nonlinguistic position); its basis; its standing.
- *Relations:* is supported or contradicted by Evidence; motivates
  ReadingHypotheses and TranslationHypotheses, which must name it.
- **ME-02.** Every ReadingHypothesis and TranslationHypothesis
  names the LanguageHypothesis it is made under, or is recorded as
  language-neutral (a structural statement). *Falsifier:* a reading
  or translation is found whose language basis is unstated.

### 3.3 Corpus

A delimited, identity-bearing collection of Inscriptions (or of
transcriptions of them) used as evidence: the unit a study's
reproducibility statement names.

- *Attributes:* the immutable identity of record — version,
  content hash, source, licensing terms, object / inscription /
  sign counts under a named counting basis, normalization rules,
  orientation basis (per C095-3 and C095-10).
- *Relations:* contains Inscriptions; is cited by Experiments;
  its identity is verified by loaders, which fail closed on
  mismatch.
- **ME-03.** No computation runs against a Corpus whose identity
  is missing or differs from its identity of record. *Falsifier:*
  a loader or study is found executing against a corpus with a
  mismatched or absent identity, without refusing.

### 3.4 Artifact

A physical object bearing writing (a seal, tablet, sherd, or
other carrier), as an archaeological object distinct from any
transcription of it.

- *Attributes:* catalogue identity; material and object class;
  find Context; imaging references where held.
- *Relations:* bears one or more Inscriptions; is described by
  Context; is distinct from every Transcription of it (a
  transcription is a scholarly act about the Artifact, not the
  Artifact).
- **ME-04.** Objects and their transcriptions are never the same
  entity, and duplicate representations of one object in multiple
  sources resolve to one Artifact with multiple Transcriptions.
  *Falsifier:* a count of inscriptions is found that double-counts
  one object because two sources' transcriptions were treated as
  two artifacts.

### 3.5 Inscription

One contiguous written act on one Artifact: the ordered sign
sequence as attested, before any transcription choice is applied.

- *Attributes:* the Artifact it belongs to; its extent on the
  object; damage and completeness state; orientation basis (G4).
- *Relations:* is carried by one Artifact; is rendered by one or
  more Transcriptions; belongs to Corpora.
- **ME-05.** An Inscription's attested sequence and its damage
  state are recorded independently of any Transcription's reading
  of them. *Falsifier:* an inscription record is found whose
  sequence silently incorporates a transcription decision (a
  supplied sign, a resolved ligature, a chosen variant) without
  that decision being recorded as the Transcription's.

### 3.6 Sign

A grapheme identity inside one WritingSystem: the shape-class the
system distinguishes, held entirely apart from any value or
meaning (G2).

- *Attributes:* namespaced identifier; inventory frame(s) it
  belongs to; shape description or reference.
- *Relations:* has SignVariants; occurs in Inscriptions (through
  Transcriptions); is the subject of ReadingHypotheses.
- **ME-06.** A Sign carries no phonetic value and no gloss in the
  generic layer. *Falsifier:* a sign record is found with a value
  or meaning stored on the sign itself rather than on a
  ReadingHypothesis or TranslationHypothesis.

### 3.7 SignVariant

A attested shape variant of a Sign: the allograph-level unit at
which inventories disagree.

- *Attributes:* the Sign it varies; the shape distinction that
  defines it; the sources attesting it.
- *Relations:* variant-of one Sign; the disagreement between
  inventory frames is expressed as variant groupings, preserved,
  never silently resolved (G4).
- **ME-07.** Competing sign inventories are representable as
  different Sign/SignVariant groupings over the same attested
  shapes, without altering any Inscription. *Falsifier:* adopting
  a different inventory frame is found to require editing
  inscription records.

### 3.8 Transcription

A scholarly rendering of an Inscription into a sign sequence: an
act with an author, a date, a basis (edition, catalogue, imaging),
and a method, distinct from the Inscription it renders.

- *Attributes:* transcriber or source edition; the inventory frame
  used; uncertainty markings (damaged, ambiguous, supplied signs
  are marked, per G4); orientation as recorded by the
  transcription.
- *Relations:* renders one Inscription; uses Signs and
  SignVariants; may be superseded by a later Transcription without
  the earlier one being deleted (history is append-only).
- **ME-08.** Every sign sequence used by any computation traces to
  a named Transcription with a named basis. *Falsifier:* a
  sequence in a claim-bearing path is found with no transcription
  provenance.

### 3.9 ReadingHypothesis

A proposed phonetic (or other functional) value for a Sign or a
sign sequence, made under a named LanguageHypothesis or recorded
as language-neutral.

- *Attributes:* the Sign(s) it values; the value proposed; the
  LanguageHypothesis basis (ME-02); its standing (candidate,
  supported at a stated strength, contradicted, not identifiable —
  in the outcome vocabulary of record, including NOT IDENTIFIABLE
  per C095-9).
- *Relations:* is a Claim (it carries a Falsifier and Evidence);
  competes with rival ReadingHypotheses over the same Sign, which
  are carried as rivals, not deleted.
- **ME-09.** A reading's standing is a property of its
  Adjudication under its Falsifier, never of its frequency of
  assertion or its agreement with other hypotheses derived from
  the same evidence. *Falsifier:* a reading is found scored
  SUPPORTED with no rival-construction record where the
  identifiability protocol applies, or promoted on agreement with
  a same-lineage hypothesis typed as independent.

### 3.10 TranslationHypothesis

A proposed meaning for a sign sequence (an inscription, a formula,
a word-form), made under a named LanguageHypothesis and resting on
named ReadingHypotheses.

- *Attributes:* the sequence translated; the meaning proposed;
  the ReadingHypotheses it depends on; its standing.
- *Relations:* depends on ReadingHypotheses (a translation whose
  readings fall is re-stated, not silently retained); is a Claim.
- **ME-10.** No TranslationHypothesis stands stronger than the
  weakest ReadingHypothesis it depends on. *Falsifier:* a
  translation is found presented at a strength exceeding the
  standing of a reading it rests on.

### 3.11 Context

The archaeological and documentary setting of an Artifact or
Inscription: site, stratum or period, object association, and the
provenance chain by which the record reached the platform.

- *Attributes:* site and period as recorded by the source;
  provenance chain; uncertainty in attribution, stated.
- *Relations:* describes Artifacts and Inscriptions; is cited by
  Claims that use distribution over sites or periods as evidence.
- **ME-11.** A distributional claim (over sites, periods, or
  object classes) names the Context records it ranges over.
  *Falsifier:* a site- or period-level result is found whose
  context basis is unstated or whose contexts were silently
  re-attributed.

### 3.12 Evidence

A traceable item bearing on a Claim: a source record, an
observation, a computation result, or an expert statement, with
its lineage typed (G6).

- *Attributes:* what it is; its source; its transformation lineage
  from the source; its independence class relative to the Claim
  it bears on; what it does not establish.
- *Relations:* bears on Claims (supporting, contradicting, or
  bounding); is produced by Executions or held as source records.
- **ME-12.** Every Evidence item's lineage walks back to a named
  source in a finite number of recorded steps. *Falsifier:* an
  evidence item is found whose lineage contains an unrecorded
  transformation, or whose independence class is a bare boolean.

### 3.13 Claim

One assertion the platform makes or entertains, in the program's
claim form: a statement, its Falsifier, its Evidence, its
does-not-establish bound, and its standing under Adjudication.

- *Attributes:* identifier; statement; falsifier; evidence
  references; does-not-establish; stage and status in the
  lifecycle of record.
- *Relations:* is adjudicated by Adjudications; is tested by
  Experiments; rests on Evidence; may supersede or be superseded
  by other Claims, append-only.
- **ME-13.** A statement presented by the platform as established
  is a Claim whose standing supports that presentation, at the
  strength presented. *Falsifier:* a surface is found presenting a
  statement stronger than its claim's adjudicated standing (the
  RT-03 shape is this falsifier's historical instance).

### 3.14 Falsifier

The recorded condition under which a Claim would be withdrawn or
re-stated: fixed when the Claim is made, not after its test is
seen.

- *Attributes:* the condition, stated so a third party can check
  whether it occurred; the time of its fixing relative to the
  Claim's tests.
- *Relations:* belongs to exactly one Claim (or one
  ReadingHypothesis / TranslationHypothesis in their Claim
  capacity); is applied by Adjudications.
- **ME-14.** Every Claim carries a Falsifier fixed before its
  first adjudication. *Falsifier:* a claim is found adjudicated
  with no falsifier, or with a falsifier whose fixing postdates
  the result it judges.

### 3.15 Experiment

A designed test of one or more Claims: its question, its
procedure, its controls, its data (Corpora by identity), and its
acceptance shape, stated before execution.

- *Attributes:* the Claims addressed; the procedure; the controls
  (including nonlanguage and permutation controls where the
  question requires them); the Corpora cited by identity (ME-03).
- *Relations:* tests Claims; is realized by Executions; produces
  Results.
- **ME-15.** An Experiment's design record exists before its first
  Execution, and names its controls before their outcomes are
  known. *Falsifier:* an execution is found whose design was
  recorded after it ran, or whose controls were chosen after the
  result was seen.

### 3.16 Execution

One run of an Experiment: the immutable record of what actually
ran — inputs by hash, environment, seeds, code identity, and the
full attempt accounting (including rejected and negative trials).

- *Attributes:* run identity; input hashes; environment and seed
  record; the attempt lineage (every attempt, not only the
  surviving one).
- *Relations:* realizes one Experiment; produces Results; is the
  unit results are lumped by (results are never pooled across
  Executions silently).
- **ME-16.** Every Result traces to exactly the Execution that
  produced it, and every Execution of an Experiment is accounted
  for, including failures. *Falsifier:* a result is found with no
  producing execution, or an execution exists that the record
  omits because its outcome was negative.

### 3.17 Result

The recorded outcome of an Execution: the quantities computed,
their uncertainty statement (per the reporting standard of
record: effect size, interval, multiplicity handling, power or
precision basis — never a bare p-value), and what the result does
not establish.

- *Attributes:* the quantities; the uncertainty companions; the
  does-not-establish bound; the orientation assumption where the
  result is positional (C095-10).
- *Relations:* is produced by one Execution; bears on Claims as
  Evidence; is re-issued, never edited, when its assumptions are
  re-stated.
- **ME-17.** A Result's reported strength never exceeds what its
  design and uncertainty statement support. *Falsifier:* a result
  is found reported as an equivalence from a non-significant
  difference, or with a p-value standing alone.

### 3.18 Adjudication

The recorded act that sets or changes a Claim's standing: who or
what adjudicated, under which Falsifier, on which Evidence, with
what outcome — including the NOT IDENTIFIABLE outcome where the
identifiability protocol applies.

- *Attributes:* the Claim; the adjudicator (a named human, or a
  named mechanical gate — automated actors never approve in their
  own right, per the program's standing rules); the evidence
  considered; the outcome and its date.
- *Relations:* sets the standing of Claims, ReadingHypotheses, and
  TranslationHypotheses; is itself a record that later
  Adjudications may supersede, append-only.
- **ME-18.** No standing changes without an Adjudication record.
  *Falsifier:* a claim's standing is found different between two
  points in the record with no adjudication between them.

## 4. The separation contract (G2 in operational form)

For any sign S in any instantiation:

1. The Sign record for S states shape facts only: identifier,
   inventory frames, variant groupings, attestation counts.
2. Every phonetic statement about S is a ReadingHypothesis whose
   subject is S, carrying its own Claim machinery.
3. Every semantic statement about a sequence containing S is a
   TranslationHypothesis resting on named ReadingHypotheses.
4. A query that asks "what does S mean" is answered by walking
   2 and 3 and reporting their standings — including when the
   answer is that no reading is identifiable. The Sign record
   itself never answers it.

## 5. The instantiation contract

A writing system's record instantiates this model when:

1. A mapping table names, for every entity in §3, where that
   entity lives in the system's record (store, file, or registry),
   or states plainly that the system holds no instance of it yet.
2. The mapping is proven by a census: the counts and identities
   the mapping claims are recomputed from the record itself, and
   the instantiation changes no fact, count, or standing —
   proven by before/after census of the record's canonical
   stores.
3. Every gap the mapping exposes (an entity with no instance, a
   relation the record does not yet carry) is stated in the
   mapping as a gap, not papered over. A gap is a finding about
   the record, not a failure of the instantiation.

## 6. The Indus instantiation (T402)

The Indus record instantiates the model as follows. Locations are
paths in this repository at the Stage 4 base (`cf7fac12`); counts
are the census of record, recomputed at Stage 4 and proven
unchanged by the before/after census in the Stage 4 record.

| Entity | Indus realization | State at Stage 4 |
|---|---|---|
| WritingSystem | The Indus script record as a whole; inventory frames of record: 557 (Shakti), 527 (M77), 584 (Nair) signs — frame-dependent size is a program finding, carried as frames per §3.1 | Instantiated; frames carried, not chosen between |
| LanguageHypothesis | `glossa-indus/hypotheses/` (models, model_claims, model_predictions, model_scores) plus the spec record's language-comparison line (Specs 033, 052, 076, 093); the nonlinguistic position is carried as a hypothesis of the same form | Instantiated |
| Corpus | The corpus identity registry, `backend/glossa_lab/data/corpus_identity.py` (8 identities of record, C095-3), stated in `glossa-indus/CORPUS_IDENTITY_STANDARD.md` | Instantiated; 6 of 8 identities verify in a fresh checkout, 2 absent by design (the V3 strict file is placed read-only, never committed; the Holdat downloads layer is restricted-local) |
| Artifact | The canonical inscription store's object records (Spec 093 Stage 1 census: 19,925 canonical records) and the CISI catalogue concordance | Instantiated at record level; object/transcription separation is the store's keying discipline |
| Inscription | Corpus inscription records (V3 strict census: 3,916 records / 3,137 sequences; V1 export; CISI compilation) with damage and gap markers carried in the transcription layers | Instantiated |
| Sign | The anchors register's sign entries, `backend/reports/INDUS_FINAL_ANCHORS.json` (287 recorded signs), and the inventory frames above | Instantiated; sign entries carry readings as hypotheses (§4), not as sign fields |
| SignVariant | Variant groupings in the corpus layers and the cross-frame inventory differences (557/527/584) | Instantiated at layer level; no single variant registry exists — stated as a gap |
| Transcription | The keyed transcription layers (Spec 023), the mayig/CISI transcription layer, and the V3 loader's reconstruction, each with its basis named in the corpus identity records | Instantiated |
| ReadingHypothesis | The 287 anchor readings, each with basis, confidence, stage, and validation status in the anchors register; standings re-stated under the identifiability protocol at Spec 095 Stage 3 (all six independently supported anchors NOT IDENTIFIABLE) | Instantiated |
| TranslationHypothesis | **No instance.** The program holds no translation of any Indus sequence; its standing position is that the script is not deciphered | Empty by the record's own standing; stated, not papered over |
| Context | Site and period attribution in the site-attributed corpus layer and the canonical store's metadata (Spec 093's material register) | Instantiated |
| Evidence | Claims' `evidence_refs` and the generated evidence matrix, `glossa-indus/matrix/` (994 rows × 644 columns) | Instantiated; lineage typing is the ledger's field discipline |
| Claim | `glossa-indus/ledger/claims.jsonl`: 994 claims (+31 annotations), append-only | Instantiated |
| Falsifier | The `falsifier` field on claims: present on 985 of 994; the 9 without are the registered gap GR-088-21 | Instantiated with a named gap |
| Experiment | The experiment-graph node registry (556 nodes, Spec 087 census of record) and the spec corpus (each spec's design record) | Instantiated |
| Execution | Run records under the Spec 089 run discipline (run index; results lumped by run) | Instantiated |
| Result | Study outputs and reports (`outputs/`, `reports/`, spec records), each with its does-not-establish bound in the claim form | Instantiated |
| Adjudication | Adjudication and settling records (spec adjudications; `glossa-indus/ledger/settling-canonical.json` and the act chain) | Instantiated |

Two relation-level gaps the mapping exposes, both already
registered and neither changed by this instantiation:

- **Claim → Sign linkage is nearly empty.** Only 1 of 994 claims
  carries `sign_refs` (GR-088-07: no claim bears a recorded
  relation to any anchor). The model requires the relation; the
  Indus record does not yet carry it. The instantiation states
  the gap; closing it is the owning gap entry's work, not this
  stage's.
- **No SignVariant registry.** Variants live inside corpus layers
  and cross-frame differences, not in a registry of their own.
  Stated as a gap under §5 rule 3.

The instantiation changes no Indus fact, count, or standing: the
before/after census (claims ledger, anchors register, evidence
matrix, program map — hashes and counts) is filed in the Stage 4
record, and `test_spec095_stage4_instantiation.py` re-derives the
counts above from the record itself.
