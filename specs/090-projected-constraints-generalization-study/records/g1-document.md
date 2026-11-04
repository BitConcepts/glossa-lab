# G1 document — the decipherment domain (the Indus script)

**What this document is.** This is the G1 document of Spec 090
(projected-constraints generalization study), answering items 1–3
of Appendix B of the skeleton document (*The Projected
Constraints skeleton*, generalization program document 1;
AXIOVEX/vexa commit 88839493; the copy of record is
`records/GENERALIZATION-SKELETON-2026-11-04.md` in this spec's
records, SHA-256 a66ffe4f…). It states, for the decipherment
domain: the record system (skeleton definition D1), the
projection rule (D2) with its cannot-distinguish account, and
the primitive-absolute disposition (D3) reached by audit. It is
written for the judging protocol's reader, who receives only
the skeleton, this document, and the domain's records. It
therefore contains definitions, provenance rules, counted
populations, and audit dispositions — and nothing else: no
verdict on any skeleton element, no necessary condition, no
outcome language. Terms D1–D6 are used exactly as the skeleton
defines them; this document does not redefine them.

**Version.** v1, 2026-11-04. Under decision D-090-1 of Spec
090, this document is versioned only by recorded amendment
acts: an amendment produces a new version of this file, with
the act recorded in this spec's records; the text of a
superseded version is never silently edited. The SHA-256 of
this version, as committed, is recorded in
`records/stage-s1-record.md` (a document cannot carry its own
hash; the stage record is where the hash lives).

**State of the records.** Every count and hash below was
counted or read from the records at the repository state
BitConcepts/glossa-lab commit
a7db3cfb60bf84eeb87bd9f690050543c2ebb01c (origin/main,
2026-11-04), and is reproducible from the artifacts named.
Where a population is cited from a frozen record instead of
re-counted, the frozen record is named.

---

## 1. The record system (D1)

**Definition.** The domain's state — the Indus script as it
was used: its sign inventory, its writing conventions, the
language it encoded — is known only through the records of
five classes. Together they are the record system R. A record
is a discrete, inspectable item with a provenance; no record
is the script, and no class below is complete.

### 1.1 Class I — inscription records

*What a record is.* One published record of one inscribed
object (seal, tablet, or other inscribed artifact) or of one
inscription text, as carried in the program's corpus sources:
the published concordances and corpora the program holds —
principally Mahadevan (1977), *The Indus Script: Texts,
Concordance and Tables* (Memoirs of the Archaeological Survey
of India No. 77), and the Corpus of Indus Seals and
Inscriptions (CISI) volumes — and the object-level corpus
snapshot (§1.5), whose rows are object records carrying,
where their sources state them, site, material, artifact
type, holding institution, and a diplomatic text code.

*Provenance rule.* An inscription record enters the system
only as a row or entry of a named published source or of the
snapshot's named source systems; its provenance is that
source, and object attributions (site, period, material) are
content of the record as its source states them — including
their absence: in the snapshot, 12,423 of 15,508 rows state
no sign-id scheme and many state null site or material, and
the record stands with those nulls on its face.

*Custody.* The snapshot is a file in the repository
(§1.5). CISI page scans are restricted material: held only
on the program owner's machines, never redistributed; the
statistics computed from them are publishable, the scans are
not records this document hands to a reader.

### 1.2 Class II — coded corpus records

*What a record is.* One inscription rendered as a sequence
of sign codes under a named frame (a sign inventory with a
segmentation and identity rule, §2.1). The class's principal
members are two flat files and one coded subset:

- **The M77 coded corpus** (`reports/mahadevan_corpus_flat.txt`,
  SHA-256 878fd2231929f2105cb5c7fb37507ee7eceb7d83f355f1fa4d8e793926785c18):
  1,669 inscriptions, 5,361 sign tokens, 64 distinct codes;
  mean inscription length 3.21 tokens; 564 of the 1,669
  inscriptions are a single token long; one code occurs
  exactly once in the file and three codes occur three times
  or fewer; the most frequent code accounts for 541 of 5,361
  tokens. The file's codes run numerically from 3 to 920.
- **The ICIT coded corpus** (`reports/icit_corpus_flat.txt`,
  SHA-256 c8839fd3bb98abb734bc3531ccbc451c96969cb2e38ce2bcd0713b8bed048ab3):
  4,410 inscriptions, 14,213 tokens, 713 distinct codes —
  a different frame's coding, of a differently bounded
  object set.
- **The CISI coded subset** (loader of record
  `backend/glossa_lab/data/indus_cisi.py`): 179 multi-sign
  inscriptions, Mohenjo-daro only, coded in Parpola P-codes.

*Provenance rule.* A coded corpus record is a derived
record: it exists only with its derivation named. The M77
file's derivation is stated by its loader of record
(`backend/glossa_lab/data/indus_m77.py`): produced from
Mahadevan's 1977 concordance by OCR and a sign-rank-
correlation glyph mapping; one inscription per line, signs
space-separated as 3-digit codes. The counted file governs
over its documentation where they differ: the loader's
header states an inscription-length range of 1–14 (April
2026), and the pinned file as counted contains 25 lines
longer than 14 tokens. Sequence order in a coded record
follows the transcription conventions of its derivation;
the anchor register (§1.3) records a reading direction per
anchor (the value carried is `rtl`).

*Frame note.* The M77 file's code space is not the
Mahadevan sign list's number space: the list's numbers, as
the anchor register's keys show, run from 1 to 416, while
the file attests codes above 900. Which file code, if any,
answers to which list number is a cross-frame identity
question, decided where the system decides it by crosswalk
records (§2.4, item ε) — not by the coded files themselves.

### 1.3 Class III — anchor records

*What a record is.* One assertion, keyed by sign, that a
sign carries a proposed reading. The register of record is
`backend/reports/INDUS_FINAL_ANCHORS.json` (SHA-256
df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569;
570,344 bytes; pinned in the settling canonicals, §1.5).
Each record carries: the reading; a confidence tier; a
basis text stating the grounds asserted for the reading; a
reading direction; a lifecycle stage with a stage history
(each transition naming its actor, its timestamp, its
evidence references, and its reason); a validation status;
and a strict-set flag.

*Provenance rule.* An anchor record's provenance is its
stage history and its basis text: where the reading came
from and on what grounds, as recorded. A reading enters the
strict set only under the register's strict rule (of record
in the settling canonicals' pin block, applying the
Phase-108 strict definition): confidence HIGH or MEDIUM,
register category neither SA_DERIVED nor SA_CONFIRMED_ONLY,
and not in the SA chain — that is, the strict set is defined
by independence from the program's own SA derivation and
confirmation procedure.

*Population, counted at the state named in the header.*
287 records: 286 keyed in the Mahadevan frame (keys M001–
M416) and one keyed in another frame (H003). Confidence
tiers: HIGH 166, MEDIUM 5, LOW 3, CANDIDATE 113.
Validation statuses: `strict_sa_independent` 94 (the strict
set; by confidence, HIGH 90 and MEDIUM 4),
`sa_in_provenance_chain` 33, `pending_non_sa_validation`
44, `no_validation_record` 3, `premise_superseded` 113.
Lifecycle stages: `checked` 94, `created` 193.

*Exception classes, accounted.* (i) The 3
`no_validation_record` records carry no validation record:
the register's provenance expectation (a validation chain
behind every reading) is unmet for them, and they are named
here as the exception they are, not absorbed. (ii) The 193
records at stage `created` have never advanced through a
stage transition; their stage histories record their
creation only. (iii) The 113 `premise_superseded` records
stand with the premise their reading rested on recorded as
superseded; they remain records of the system, with that
status on their face.

*Support census of the strict set (from a frozen record).*
The anchor-support audit of record
(`docs/repair-2026-10-26/anchor-support-audit.json`, audit
id repair-2026-10-26-wp5-anchor-support-audit, executed
against this register at the same SHA-256 it carries today)
disposes of the 94 strict records as: supported by evidence
independent of the program 6; supported by internal evidence
only 46; requires revalidation 37; insufficient evidence 2;
expert adjudication pending 3 (signs M222, M362, M398). It
also records that 81 of the 94 carry a crosswalk identity
entry (§2.4, item ε).

### 1.4 Class IV — ledger claim lines

*What a record is.* One line of the claims ledger
(`glossa-indus/ledger/claims.jsonl`, canonical SHA-256
15a5fbad24f400631ace1ebc88bfb7712c9bf6f68fae23e56fedbcac5fd5a794),
stating one claim about the domain (or one annotation on a
claim), with its sources, its governing status and stage,
its falsifier, and its does-not-establish bound.

*Provenance rule.* The ledger is append-only. A claim line
enters only through the sanctioned intake
(`tools/ledger/import_bundle.py`), which validates schema,
recomputes the line's fingerprint, checks provenance, and
refuses duplicates; corrections are appended annotation
lines, never edits. Each line's provenance is its source of
record and its intake act.

*Population, counted at the state named in the header.*
943 lines: 912 claim lines (by population: bundle 889,
extracted 23) and 31 annotation lines. Governing statuses:
draft 888, untested 12, partially_supported 3,
strongly_supported 2, contradicted 4, partially_falsified
1, unsupported 1, superseded 1. A falsifier is present on
903 of 912 claim lines.

*Exception class, accounted.* The 9 claim lines carrying
no falsifier are all in the extracted population (14 of 23
extracted lines carry one). They are a source gap in the
extraction the population came from, counted here as the
program's records count them; no falsifier has been
supplied for them by anyone.

*The ledger's generated layers (standing fact).* The
ledger is the sole entry point of the program's executable
matrix: the matrix (`glossa-indus/matrix/matrix.json`;
912 rows × 644 columns, 1,435 cells at this state) and the
maps are generated from the ledger by script, and claim
statuses settle mechanically under the registered semantics
glossa-settle-1. A verification gate (classes V1–V10,
`backend/glossa_lab/ledger_gate.py`) recomputes every
downstream layer by an independent route under its own
registered copies of the definitions; the gate never
writes, and publication replaces published artifacts only
on ALL PASS. This machinery is the program's standing
substrate, stated here because the ledger's provenance
includes it; no part of it is a product of the study this
document serves.

### 1.5 Class V — snapshots and frozen records

*What a record is.* A record whose content is fixed by a
pin — a hash, a freeze digest, or a filed comparison — so
that later work cites exactly the bytes that stood.

- **The corpus snapshot**
  (`glossa-corpus/indus/exports/indus_research.jsonl`,
  canonical SHA-256 08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e):
  15,508 object records. Source systems: PennMuseum 7,515;
  MetOpenAccess 4,904; indusscript-m77 2,906; mayig-cisi
  179; ClevelandArtOpenAccess 4. Sign-id schemes stated:
  Mahadevan1977 on 2,906 records, Parpola1982 on 179, none
  stated on 12,423. Diplomatic text codes appear across the
  file in 535 distinct values; a crosswalk coverage above
  zero is recorded on 3,021 records and zero on 12,487.
- **The settling canonicals**
  (`glossa-indus/ledger/settling-canonical.json`): the
  registered canonical scenarios of the settling semantics
  (named: null-over-subset, incumbent-over-subset,
  full-register-over-subset, seeded-conflict-over-subset,
  untouched-sign, incumbent-vs-full-register-over-subset),
  with a pin block naming the exact ledger, anchor-register,
  and corpus-snapshot bytes they govern. Re-run against the
  records at the state named in the header, all six
  reproduce (6/6).
- **Frozen study records.** Studies in this program freeze
  before they execute, and their frozen bars and closures
  are records of this class: for example the signary
  triangulation study's frozen record (Spec 077; freeze
  digest a9d10a2ba4f8e03fe77f7815a9fbd9a8860270f3a7a56801f02458507250f55f;
  its population, bars, and outcome stand as recorded there
  and are cited by this document in §2.4 only as counted
  grounding). Citation does not re-open a frozen record.

---

## 2. The projection rule (D2)

### 2.1 The candidate system state

A **candidate state** of this domain is a complete
hypothesis about the script as it was used, given as a
four-tuple s = (Σ, γ, ρ, λ):

- **Σ — the sign inventory:** a finite set of sign types.
- **γ — the glyph classification:** a rule that assigns, to
  every glyph token on every inscribed object, a member of
  Σ or the value *not-a-sign*; applied to an object o's
  glyph stream (its marks in their recorded order), γ
  yields o's text as a sequence over Σ. γ thus fixes both
  the segmentation of glyph streams into signs and the
  identity of signs across objects: two glyph tokens are
  the same sign exactly when γ assigns them the same member
  of Σ.
- **ρ — the reading assignment:** a partial mapping from
  signs (and, where the hypothesis states them, from sign
  sequences) to values — sound values, word values, or
  semantic values — in the language λ names. ρ is partial
  by definition: a hypothesis may leave signs unread.
- **λ — the language identification:** the language, or
  language hypothesis, whose values ρ assigns; λ may be
  the value *no identification proposed*, in which case ρ
  assigns no language-bound values.

A state is **named** in this system's sense when its γ is
presented as an explicit assignment over the object set O
(§2.2), or as a total rule the system can execute over the
recorded glyph data to obtain that assignment. The frames
of §1.2 are named states' (Σ, γ) components, presented as
coded corpora.

### 2.2 The projection π

Let O be the object set of the record system: the objects
for which the system holds inscription records (§1.1, §1.5)
— operatively, the line sets of the coded corpora (1,669
inscriptions in the M77 frame; 4,410 in the ICIT frame) and
the snapshot's object records carrying text codes. The
projection is the rule:

> **π(s) = T(s)**, the sequence table assigning to each
> object o in O the sequence γ(o) over Σ that s's glyph
> classification produces for o's glyph stream.

Every further record the state determines — token counts,
sign frequencies, co-occurrence and positional statistics —
is a function of T(s) and therefore of π(s), not an
addition to the projection. The projection does not depend
on ρ or on λ: readings and language identifications are no
part of what a state projects onto the inscription records.
Anchor records (§1.3) and claim lines (§1.4) are not
outputs of π: they are assertions about states, produced by
scholars and by the program, and the record system holds
them as assertions with provenance — their content is what
is at issue between candidate states, never a projection of
any one of them.

The actual coded corpora of §1.2 are the record system's
recorded codings of the surviving objects under their named
frames: each is T computed under that frame's (Σ, γ), by
that file's stated derivation, over that file's bounded
object set. Comparing a candidate state to the records is
therefore always a comparison under §2.3.

### 2.3 Projection-equivalence

Two candidate states s and s′ are **projection-equivalent**,
s ~ s′, exactly when there exists a bijection β : Σ → Σ′
with β(γ(o)) = γ′(o) for every object o in O (β applied
elementwise to the sequences). Sign names are labels; the
projection sees the segmentation of every surviving glyph
stream and the identity structure over its tokens, up to
relabeling — nothing else.

**Decidability.** For two named states, whether s ~ s′ is
decidable from this rule alone, by a finite check: compute
both sequence tables over O and test whether a label
bijection making them identical exists. No judgment about
either state's plausibility enters the check.

*Illustration of the rule (definitions only).* Let A's
(Σ, γ) be the coding of the M77 file itself. (i) Let B be
identical to A except that B's γ splits one code's tokens
into two sign types by a stated rule over the recorded
sequences (say, by the token's position in its
inscription). B's identity structure over the surviving
tokens differs from A's — tokens A identifies, B separates
— no label bijection exists, and π distinguishes A from B.
(ii) Let C be A with one code relabeled throughout. The
relabeling is a β, and A ~ C: π does not distinguish them.

### 2.4 The cannot-distinguish account

Everything the record system can ever know is a property of
the equivalence classes of π. What follows is what the
records of §1 cannot distinguish, each item grounded in the
records named. Equivalence under π is a fact about the
records; this account assigns no plausibility, likelihood,
or standing to any state inside a class.

**α. The inventory and the classification are not fixed by
the records.** States whose (Σ, γ) induce the same identity
structure over the surviving tokens are equivalent, however
their inventories differ in distinctions no surviving token
exercises — a split of one sign into two whose token sets
are separated only by stipulation, or a merger of two signs
no surviving context separates. That the records leave the
inventory open is measured inside the system itself: the
frames of §1.2 attest 64 distinct codes (M77 file) and 713
(ICIT file) for the same script; the program's signary
registry (Registry v2, Wells/ICIT-keyed) freezes a
population of 557 signs, of which 399 are witnessed under
the frozen match rules — a population sign is witnessed
exactly when the registry's crosswalk gives it at least one
Mahadevan number — and 158 carry no Mahadevan counterpart
(Spec 077's frozen outcome record: 399 of 557 witnessed,
71.63%, against a frozen bar of 502). Much of the surviving
material exercises little of any inventory: 564 of the
1,669 M77 inscriptions are one token long, and one code
supplies 541 of the file's 5,361 tokens.

**β. Readings and language identifications are invisible
to the projection.** For fixed (Σ, γ), every (ρ, λ) variant
of a state lies in one equivalence class: π does not depend
on them (§2.2). The ground in the records is their format:
the coded corpora carry codes only — no coded record
carries a reading — and readings exist in the system only
as anchor records (§1.3), assertions whose provenance is
the scholarship and program work their basis texts and
stage histories name. No inscription record distinguishes
one reading assignment from another over the same
classification; whatever distinguishes readings enters the
system as assertion content and its stated grounds, which
§3 audits as content.

**γ. Signs whose readings stand unvalidated on the
register's own face.** States differing only in the reading
assigned to a sign whose anchor record stands at
`pending_non_sa_validation` are distinguished by no
completed validation record in the system: 44 readings
stand in that status, their validation chains incomplete
on the register's face. The same holds, with their own
grounds, for the 3 `no_validation_record` signs (no
validation record exists) and the 113 `premise_superseded`
signs (the premise a reading rested on is recorded as
superseded, and no superseding validation is recorded).
Populations counted in §1.3 from the register at its
pinned SHA-256.

**δ. Completions differing only outside the surviving
objects.** States that agree on every object in O but
differ on objects outside O — inscriptions lost,
unexcavated, unpublished, or written on media that did not
survive — are equivalent, by the definition of π over O
(§2.2). O is a survival subset: the system holds 15,508
snapshot object records and the coded corpora's bounded
line sets, and no record of any class enumerates what did
not survive to be recorded. Any property of the script
that only lost texts would exercise — the grammar of long
documents, the inventory distinctions only rare genres
draw — is therefore not a property the records can decide.

**ε. Identity across frames is crosswalk-mediated.**
Whether a sign under one frame is the same sign as a sign
under another is decided, where the system decides it at
all, by crosswalk records — the registry crosswalk behind
item α's witnessed count, the Fuls–Mahadevan crosswalk
file in the program's reports (`reports/fuls_mahadevan_
crosswalk.txt`: Fuls 2023 ICIT codes against Mahadevan
1977 codes) — which are records with provenance of their
own, and partial ones: 158 of the registry's 557
population signs have no Mahadevan counterpart under the
registry crosswalk (item α), and the snapshot records a
crosswalk coverage of zero on 12,487 of its 15,508 object
records (§1.5). A distinction that exists in one frame and
has no crosswalk counterpart in another is not
distinguishable *as the same or as different* from the
coded corpora alone.

---

## 3. The primitive absolute (D3), by audit

### 3.1 The audit and its test

D3 permits at most one primitive absolute: a quantity the
framework takes as given in absolute terms, not relative to
the records — and requires it to be named, or none to be
proved needed. This section reaches the disposition by
audit, not by selection. The candidate absolutes are the
quantities the program's practice actually uses that could
function as absolutes; each is tested against the same
rule:

> A quantity X functions as a primitive absolute in this
> system exactly when (i) the system's reasoning about
> candidate states uses X as given; (ii) X is not a record,
> nor the content of a record with provenance in R; and
> (iii) X is not derived from R by a stated rule.

A candidate failing any clause is disposed of with the
evidence for the failure. The audit covers the candidates
the practice demonstrably uses; it does not claim to
enumerate every conceivable absolute.

### 3.2 Candidate: the corpus frame

*The candidate.* That a corpus file's codes answer to one
fixed sign inventory — the frame the file is read under —
taken as given before any record is read.

*Disposition: record-relative.* The frame varies with the
records, and the variation is exhibited inside the system:
the same script is coded at 64 distinct codes in the M77
file and 713 in the ICIT file (§1.2); the signary registry
freezes a 557-sign population in a third frame; the anchor
register's keys occupy a fourth numbering (M001–M416, with
one key, H003, from a fifth). No verdict of the program
takes any one frame as given: frames enter verdicts as the
named derivations of Class II records, and frame-dependent
results are recorded as frame-dependent (§2.4, item α).
Clause (ii) fails: each frame is itself a record — a coded
corpus with its derivation stated.

### 3.3 Candidate: the surviving corpus's extent

*The candidate.* That the record set is *the* record set —
what counts as an Indus inscription, and which objects
belong to the corpus — taken as given.

*Disposition: the record system's own definition, stated
ostensively.* R is defined by the pinned artifacts of §1
(named files, at named hashes); §2.2 defines the projection
over exactly that object set O, and every statement made
under the projection is thereby relativized to O. The
extent is not a quantity the system uses in reasoning
about candidate states — no derivation takes a corpus size
or a corpus boundary as a premise about the script — it is
the boundary of the system itself, and its consequences
are carried openly in §2.4, item δ. Object attributions
that compose the extent (that this object is an inscribed
Indus artifact, from this site) are content of Class I and
Class V records, present with their provenance and, where
their sources state none, with nulls on their face (§1.1).

### 3.4 Candidate: the anchor readings' external identifications

*The candidate.* The readings imported from named
scholarship — identifications argued from material outside
the inscription records: Dravidian comparanda, contact-zone
and bilingual material, later epigraphy — taken as given,
as the ground on which other readings are validated.

*Disposition: assertion content with provenance, not a
given.* The candidate decomposes on the register's face.
(i) *Distributional content:* a basis asserting positional
or frequency grounds ("INITIAL position (freq=16),
distributional assignment," as one pending record's basis
reads) is a function of the coded corpora — derived from R
by the counting the basis itself cites. (ii) *Imported
identifications:* a basis asserting an external
identification ("Terminal marker, Dravidian case suffix,"
as the strict record M342's basis reads) is the content of
an anchor record: an assertion with provenance (§1.3),
whose standing in the system is its recorded validation
status and stage — claim standing, not given standing.
The practice exhibits the distinction rather than assuming
it: the strict set is defined by independence from the
program's own derivation chain (§1.3); the audit of record
finds only 6 of the 94 strict readings supported by
evidence independent of the program, 46 supported by
internal evidence only, 37 requiring revalidation, and the
program records those findings as findings about its own
anchors (§1.3) — an instrument treated as given is not
audited against itself this way; and the 44 readings whose
validation is incomplete stand in the register as pending,
used as settled by no completed record (§2.4, item γ).
Clause (i) fails: no reasoning in the system takes an
imported identification as a premise that is not itself a
record under test.

### 3.5 Candidate: object-level imported identifications

*The candidate.* The archaeological scaffolding imported
with the objects: site attributions, artifact typologies,
material identifications, and the chronological brackets
(period labels and their date ranges) that claims in the
program condition on — taken as given in absolute terms,
as dates and places that are simply so.

*Disposition: record content with provenance.* Site,
material, and artifact type are fields of Class I and
Class V records, carried from their named sources and null
where unstated (§1.1, §1.5); period assignments exist in
the system as claim content in Class IV (assertions about
objects, settled like other assertions) and as the frozen
design parameters of the studies that condition on them —
in either form, records with provenance, open to the same
correction-by-append discipline as any record. A candidate
state (§2.1) does not vary over them, and the projection
does not use them: π is computed from glyph streams alone.
Clause (ii) fails.

### 3.6 Candidate: cross-frame sign identity

*The candidate.* That a sign in one frame *is* a sign in
another — the identity relation the crosswalks assert —
taken as given whenever records from two frames are used
together.

*Disposition: records, and partial ones.* Identity across
frames is asserted by crosswalk records with provenance
(§2.4, item ε) and by nothing else; the coded corpora
themselves assert no cross-frame identity (their code
spaces are not even mutually bounded: §1.2's frame note).
The crosswalks' partiality is on their face — 158 of 557
registry signs without a Mahadevan counterpart — and is
carried in the cannot-distinguish account rather than
assumed away. Clause (ii) fails.

### 3.7 Candidate: the framework's registered constants

*The candidate.* The fixed numbers and rules the machinery
runs on: frozen verdict bars (for example, Spec 077's bar
of 502 of 557), the settling semantics glossa-settle-1,
the matrix definitions (matrix-defs v1), the confidence
thresholds of the assessment machinery — taken as given by
every verdict they govern.

*Disposition: the framework's own definitions, themselves
records.* Each such constant stands in the system as a
record: a frozen study record names its bar before
execution (§1.5); the settling semantics is a registered
document whose canonicals pin the exact bytes they govern;
the matrix definitions are named in the gate's registered
copies. Each is amendable only by a recorded act, and none
is a quantity of the domain: candidate states do not vary
over them, and they figure in verdicts about claims, not
in the projection or in any premise about the script.
They are the judging machinery's stated parameters —
stated, in the open, as records — not an absolute the
framework hides inside its reasoning about states.
Clause (ii) fails.

### 3.8 Candidate: transcription fidelity

*The candidate.* That the coded corpora faithfully render
the glyphs of the inscription records — silently assumed
whenever a coded record is used as evidence about an
object.

*Disposition: a provenance property of Class II, not a
quantity.* The G1 document asks no reader to assume
fidelity. Each coded corpus stands with its derivation
named (§1.2: for the M77 file, OCR and a sign-rank-
correlation glyph mapping from the 1977 concordance, per
its loader of record), and fidelity is exactly what that
provenance asserts and what a re-derivation against the
Class I sources would check. Where the derivation's own
documentation and the pinned file differ, this document
has already counted the file as it stands (§1.2). A
fidelity failure, if found, is a record error — corrigible
by a new derived record with its own provenance — not the
collapse of a premise the system never stated.

### 3.9 The disposition assembled

The candidates the practice uses are disposed of as
follows: the corpus frame is record-relative, its variation
exhibited (§3.2); the corpus's extent is the record
system's own ostensive definition, with its consequences
carried in the open (§3.3); the anchor readings' external
identifications, the object-level attributions, and
cross-frame identity are content of records with
provenance — assertions inside the system, under test,
never premises behind it (§3.4–§3.6); the framework's
constants are the framework's own stated definitions,
themselves records (§3.7); transcription fidelity is a
provenance property, asserted by each derived record's
named derivation and checkable against its sources (§3.8).
No candidate satisfies the test of §3.1. The record system
therefore takes **no primitive absolute**: this is D3's
none-needed branch, reached by exhibiting each candidate
the practice uses as record-relative, as record content, or
as a stated definition of the system itself. The at-most-one
bound is satisfied with none named.
