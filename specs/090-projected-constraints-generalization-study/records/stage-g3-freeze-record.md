# Stage G3 freeze record (T402) — Spec 090 (2026-11-12)

**Scope:** tasks.md T402 — the freeze of Spec 090's Stage G3
(the computed separator), executed on branch
`spec090-g3-freeze` at base main `a33642fe` (merge of PR
#558). Inputs: the ratified stage package
(`records/g3-package-draft.md`, ratified as a block
2026-11-06, decisions D-090-5..10; ratification act at
`records/ratification-2026-11-06.md`), in particular its
§3.4, which enumerates what this record must carry.

**Freeze statement.** The items below are fixed as of
this record's commit, before any identity-structure
profile is computed over H1 by anyone, for any purpose
including exploration (claim C090-19). No profile,
spectrum, multiplicity, length, position, or adjacency
quantity over H1 was computed for this freeze; the only
quantities taken are the counts §3.4 permits (H1's
extracted record count and token total), stated in §3.
Any change to a frozen item after this commit is an
amendment act; an amendment that touches the case list,
the profile definitions, or the bar voids the
administration, which must then re-freeze and re-run
from zero under Spec 089's run discipline (package
§3.4). Two items could not be frozen in the form the
package specifies — the object-overlap measurement (§4)
and one limb of the held-out verification (§5) — and
both are stated there in full, unresolved by this
record, for the parent seat's ruling. T403 must not
start on the strength of this record alone while §5's
tension stands unresolved.

## 1. The pinned source files

Both files were read in the freeze worker's clone at the
base above; the hashes below are the files as they stand
there, and both agree with the G1 document's canonical
pins (§1.2, §1.5), so the frozen bytes are the bytes the
study has always cited.

- **The corpus snapshot** (the H1 source):
  `glossa-corpus/indus/exports/indus_research.jsonl`,
  10,146,212 bytes, 15,508 records, **SHA-256
  `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`**
  (G1 §1.5's canonical pin, recomputed and agreeing).
- **The M77 flat file** (the comparison population of
  §4): `reports/mahadevan_corpus_flat.txt`, 21,443
  bytes, 1,669 lines, **SHA-256
  `878fd2231929f2105cb5c7fb37507ee7eceb7d83f355f1fa4d8e793926785c18`**
  (G1 §1.2's pin, recomputed and agreeing).

## 2. The extraction rules (package §3.1, stated exactly)

H1 is extracted from the pinned snapshot as follows.

- **Source-system filter.** A record belongs to H1
  exactly when its `source_system` field is
  `indusscript-m77`. Every other source system is
  excluded, including the snapshot's `mayig-cisi`
  subset (179 records; package §3.3: the same objects
  as the Class II CISI coded subset, its profile
  counted in G1 §1.2 / G2 step 4 — not held out in any
  sense).
- **The sequence.** The record's sequence is its
  `canonical_grapheme_ids` list, **as recorded** — the
  list's elements, in the list's order, with no element
  dropped, rewritten, or re-ordered. A token is one
  element of the list. The list includes the eroded
  code `000` and any `*`-prefixed marked ids where they
  stand; this freeze adopts no dropping rule (Spec
  076's construction, §5 below, adopted one; §3.1's
  does not).
- **What does not govern.** The diplomatic text strings
  (`text_code_diplomatic`,
  `text_code_diplomatic_normalized`) are not the
  sequence. The `sign_instance_count` field is not the
  sequence and not its length: it disagrees with the
  list's length on sampled records (package §3.1, §10
  gap 3), and the disagreement is explained, not
  merely observed — the snapshot census of record
  (Spec 093, `specs/093-material-context-channel/records/t101-census-completion-2026-11-06.md`,
  §1, "Sequence bookkeeping") establishes that exactly
  the 635 sequence records carrying the eroded token
  `000` are those whose `sign_instance_count` differs
  from the list length, because the count field
  deterministically counts tokens **excluding** `000`.
  The list therefore governs, per §3.1's ruling,
  verified against the snapshot's own census record as
  §10 gap 3 required. (That census also records exactly
  one sequence record with count 0, `GLI-IND-M77-03080`;
  its list is non-empty, so it qualifies below.)

## 3. The permitted counts, and the floors

Taken over the pinned snapshot by the rules of §2 (a
counting pass only; no per-type or per-record quantity
beyond membership and list length was produced):

- Snapshot records by source system: PennMuseum 7,515;
  MetOpenAccess 4,904; `indusscript-m77` **2,906**;
  `mayig-cisi` 179; ClevelandArtOpenAccess 4 — total
  15,508, agreeing with G1 §1.5's census.
- **H1 extracted record count: 2,906.** Every
  `indusscript-m77` record carries a non-empty
  `canonical_grapheme_ids` list; the empty-list
  exclusion of §2 removes none.
- **H1 token total: 12,639** (the sum of the qualifying
  lists' lengths).
- Cross-check, from published figures only: Spec 076's
  recorded construction over the same 2,906 records
  dropped 680 `000` tokens and 452 `*`-marked tokens to
  reach 11,507; 12,639 − 680 − 452 = 11,507. The
  freeze's raw total reconciles exactly with the
  record system's own earlier census under its stated
  dropping rule.
- **The floors (package §6) do not fire.** §6's
  CANNOT BE ADMINISTERED floor fires at "fewer than
  300 sequence-bearing records, or fewer than 1,000
  tokens". H1 stands at 2,906 sequence-bearing records
  and 12,639 tokens. (The floors as ratified are quoted
  in §9.)

## 4. The object-overlap item — not measurable as specified

Package §3.1 requires this freeze to "measure and
publish the object overlap between H1 and the flat
file's object set, **by the records' own identifiers**".
That measurement cannot be taken, and this record
states why instead of substituting a method:

- H1's records carry identifiers: `glossa_id`
  (`GLI-IND-M77-…`), whose numeric part is the IM77
  text number named in each record's
  `_citation.derivation` ("IM77 text 1001 from
  indusscript.in Firestore (RMRL, 2021)").
- The flat file carries **no identifiers at all**.
  Every one of its 1,669 lines is a bare sequence of
  space-separated 3-digit codes (verified line by line
  for this freeze: no line contains anything but digits
  and spaces; codes run 003–920; the code `000` never
  occurs). Its loader of record
  (`backend/glossa_lab/data/indus_m77.py`) states the
  format in the same terms: "one inscription per line,
  signs space-separated as 3-digit M77 codes". No
  in-repo record enumerates the flat file's lines by
  IM77 text number or by any other identifier.

An overlap number produced by matching sequence content
would rest on a rule no adopted text states (the two
derivations — OCR of the printed concordance for the
flat file, the indusscript.in Firestore for the
snapshot — transcribe the same objects independently,
and identical sequences on distinct objects are common
in both files), and fixing such a rule here would be an
amendment of §3.1's specified method, not an execution
of it. This freeze therefore records the overlap item
as **not measurable by the specified route**, with the
two populations standing side by side — 2,906 H1
records; 1,669 flat-file inscriptions — and no overlap
number. The untouched criterion (§5) does not turn on
the overlap (§3.1: it "holds either way"); the number
was owed to the reader's judgment of its weight, and
the reader is owed this explanation in its place.

## 5. The held-out verification (§3.4) — and an adjacent-record finding

The untouched criterion (package §3): no step of the
G1 document's drafting, the adversarial pass, the G2
derivation, or the G2 audit computed a table, a profile,
or a per-record quantity over H1.

**The enumerated verification passes.** §3.4 names two
adjacent frozen records; both were checked against
their own texts for this freeze:

- **Spec 077's frozen record**
  (`specs/077-signary-triangulation/freeze.md`,
  `outcome.md`, `step0-record.md`): its inputs are
  Registry v2, Spec 075's machine record, the M77 sign
  list, the Wells 1998 sign list, the C-7 canonical M77
  raw text, and Table I. The snapshot is not among its
  inputs and is nowhere mentioned in those records;
  its executed quantity is the registry witnessed count
  (399 of 557) that G1 §2.4α cites. It computed no
  table and no profile over H1.
- **The anchor-support audit**
  (`docs/repair-2026-10-26/anchor-support-audit.json`,
  repair program WP5): its inputs are the anchor
  register and its provenance trails (INDUS_FINAL_ANCHORS,
  the Phase-48 validation output, the Phase-108
  register); its method classifies the 94 strict-core
  anchors and 30 promotions by evidential support. It
  computes nothing over corpus records at all, and no
  profile over H1.

**Adjacent-record finding, stated in full.** The same
sweep of the frozen records found an adjacent study the
package does not name: **Spec 076**
(`specs/076-projected-constraint-corpus-model/`,
ASSUMPTION SET DOES NOT HOLD at its own close), whose
spec §7 ("Worked miniature example — real counts,
recomputed for the design") takes as its frame exactly
the snapshot's `indusscript-m77` records — the same
pinned file, the same 2,906 records — and publishes,
over that frame, a **sequence-length profile**
(1×225, 2×531, 3×563, 4×521, 5×444, 6×249, 7×189,
8×82, 9×32, 10×28, 11×11, 12×2, 13×1, 14×2) and
**positional slot aggregates** (Σ initial 2,655;
Σ final 2,655; Σ solo 225; Σ medial 5,972), under its
own token construction (dropping the 680 `000` tokens
and 452 `*`-marked tokens: 2,880 non-empty sequences,
11,507 tokens). Behind it, Spec 033's pipeline census
recorded the same frame's token totals (11,507; 5,883
strict) earlier still. A sequence-length histogram is,
in form, the L component of §6's profile, computed
over H1's record set — under a different token
construction than §2's extraction (Spec 076's
sequences drop tokens that H1, as frozen, keeps), and
in a study that is no part of Spec 090.

The texts this freeze answers to read two ways, and
this record does not choose between them:

- Under §3's criterion and claim C090-18 as written,
  the contamination test is scoped to the study's own
  steps — the G1 drafting, the adversarial pass, the
  G2 derivation, the G2 audit, and records they cite
  as computed grounding. Spec 076 is cited **nowhere**
  in the G1 document, the G2 derivation, or the G3
  package (verified by search for this freeze), and it
  designed no part of the separator. On this reading
  the verification stands.
- Under §6's gloss of this same verification — CANNOT
  BE ADMINISTERED fires if "the held-out verification
  of §3.4 fails (**an adjacent record is found to have
  computed over H1**)" — and under C090-19's phrasing
  ("the first profile over H1 is computed **by
  anyone**, for any purpose including exploration"), a
  length profile over H1's record set, frozen in the
  record system before this stage was drafted, is the
  shape of event those sentences name. On this reading
  the verification fails and §6's outcome is the
  stage's honest close.

The freeze states the finding, the quantities, and the
tension verbatim, and resolves none of it: that ruling
belongs to the parent seat (and, if it goes against the
stage, the outcome is recorded under §6, not repaired
inside this stage — D-090-8). Nothing in §§1–4 or
§§6–9 of this record depends on the ruling; if the
ruling voids the administration, this freeze is void
with it and any successor attempt re-freezes under a
new package.

## 6. The separator, frozen as defined (package §2)

For a table T over an object set O, the
identity-structure profile is

> P(T) = ( |Σ_O(T)| , M(T) , L(T) , X(T) , B(T) )

with all counts taken over O:

- **|Σ_O(T)|** — the exercised inventory size: the
  number of types γ assigns to at least one token on O
  (G1 §2.3's Σ_O, counted).
- **M(T)** — the sorted token-multiplicity vector: the
  multiset of per-type token counts over exercised
  types, sorted descending.
- **L(T)** — the sequence-length histogram: the
  multiset of per-object sequence lengths, as a count
  per length.
- **X(T)** — the positional spectrum: the multiset,
  over exercised types t, of the triple (initial(t),
  final(t), medial(t)) counting t's tokens in first,
  last, and interior positions of their sequences; a
  token in a one-token sequence is both initial and
  final and counts in both (and, having no interior
  position, not in medial).
- **B(T)** — the adjacent-pair spectrum: the multiset
  of counts of adjacent ordered type pairs (t, u) over
  all sequences, zero counts excluded — one count per
  ordered pair that occurs adjacently at least once,
  the count being its total adjacent occurrences.

Two named states s, s′ over the same record set C are
**separated over C** exactly when P(T_C(s)) ≠
P(T_C(s′)), componentwise; components compare as the
multisets and counts defined above. The named limit
stands as the package states it: P is a coarsening of
the identity structure, not the structure itself; two
non-equivalent tables can share a profile, and S does
not separate every pair of distinct classes. The
components may not be extended mid-run (C090-21).

## 7. The case list, frozen (package §4), in executable form

All cases are named states over H1 in the package §2
naming mode. All
share H1's object set and, except where a rule changes
them, its token total.

- **A0 — the recorded coding.** The identity rule:
  H1's table as recorded. A0's profile is H1's
  separator value.
- **A1 — the positional split.** The most frequent
  code of H1's recorded table is split into two types
  by the token's position: occurrences in initial
  position of their sequence form one type, all other
  occurrences the second.
- **A2 — the tail merger.** The two least frequent
  codes of H1's recorded table whose multiplicity is
  at least 10 are merged into one type. (The floor is
  a design parameter of the package, fixed there,
  applied mechanically here; it exists so the merged
  types are exercised enough for the merger to be a
  classification claim, not a hapax bookkeeping act.)
- **A3 — the head merger.** The two most frequent
  codes of H1's recorded table are merged into one
  type.
- **C1 — the relabeling control.** A0's codes permuted
  by the seeded random bijection of §8. By §6's
  invariance argument, P must be identical to A0's in
  every component; if it is not, the administration
  stops (package §6).
- **C2 — the identity control.** A0 against A0. Must
  not separate.

**Executable-form completions, fixed by this freeze**
(the package's rules, made mechanical; none of them
requires or produces a multiplicity over H1, which is
why they can be fixed here):

- *Tie-breaking.* Where a rule selects by multiplicity
  extreme (most frequent; least frequent at or above
  the floor; the two most frequent) and two or more
  codes tie, the tied codes are ordered ascending by
  their recorded code strings (the codes are zero-padded
  3-digit strings, so lexicographic order is numeric
  order) and selected in that order. For A2 the
  candidate order is (multiplicity ascending, code
  ascending); for A3, (multiplicity descending, code
  ascending); A1 takes the first code under
  (multiplicity descending, code ascending).
- *A2's floor, if it cannot be met.* If fewer than two
  codes of A0's table have multiplicity at least 10,
  case A2 cannot be formed as frozen; that is an
  administration fact for the outcome record under
  §6's vocabulary, not a defect this freeze repairs
  and not a license to lower the floor.
- *Split and merger labels.* Which of A1's two split
  types carries which new label, and what label a
  merged type carries, are immaterial: P is invariant
  under relabeling (§6), so no label rule is frozen.

**A records discrepancy, named.** spec.md's
stage-amendment section summarizes the case list as
"A0 the exercised core, A1 the unseen half, A2 the
designed-degenerate table, A3 the designed-separating
table". Those labels do not match §4's definitions
(positional split; tail merger; head merger), and the
amendment's bar summary ("separation of the
designed-degenerate case, separation of the unseen
half") likewise does not match §5's conditions. The
amendment itself states "The bar is the package's §5",
and the ratification adopted the package's definitions
(D-090-6: P as defined in §2; D-090-8: §5's three
conditions). This freeze therefore freezes the
package's §4/§5 texts, quotes them, and flags the
amendment's summary labels here as a discrepancy in
the record for the parent seat; the labels play no
part in the administration.

## 8. Control C1 — the relabeling seed, fixed by rule

The package delegates the seed to this freeze (§3.4:
"the relabeling seed for control C1"; §4: "the seed is
in the freeze") and states none. It is fixed here by a
stated mechanical rule, before any computation:

- **Rule.** The seed is the unsigned big-endian
  integer formed by the first 8 bytes of the SHA-256
  digest of the UTF-8 string
  `glossa-lab/spec090/g3/c1-relabeling-seed`.
- **Digest:**
  `0b9797c580fd2ca2786c98bcd2fd484b706d178da7968c05de423bf696e501b4`.
- **Seed: 835303130428943522.**
- **The bijection, in executable form.** Let `codes`
  be the distinct codes of A0's table, sorted ascending
  (lexicographic on the recorded strings). Let
  `shuffled` be a copy of `codes` permuted by
  `random.Random(SEED).shuffle` under CPython 3 (the
  repository's runtime). The relabeling maps
  `codes[i]` to `shuffled[i]` for every i, applied to
  every token of every sequence. An independent
  implementer with the seed, the sorted code list, and
  this construction reproduces the bijection exactly.

## 9. The bar, frozen verbatim (package §5), and the floors

> **The stage outcome is SEPARATED if and only if all
> three hold, on the audited profiles:**
>
> 1. **Distinctness.** For each pair (A0, A1), (A0,
>    A2), (A0, A3): the profiles differ in at least one
>    named component.
> 2. **Invariance.** For each pair (A0, C1), (A0, C2):
>    the profiles are identical in every component.
> 3. **No count separation.** No component counted
>    toward (1) differs through a difference in object
>    count or token total between the compared tables.

The administration runs once, under this freeze, by a
computer who did not draft the package, and is audited
by a second worker recomputing every profile
independently from the frozen inputs; runs are
run-scoped under Spec 089 (package §5). The outcome
vocabulary is §6's: SEPARATED; NOT YET, with the
obstruction named; CANNOT BE ADMINISTERED, with the
forcing counts shown — including its floor clause,
quoted here verbatim:

> "the freeze finds H1's sequence-bearing records too
> few or too short to carry the cases (a floor the
> freeze record must state numerically when it fires:
> fewer than 300 sequence-bearing records, or fewer
> than 1,000 tokens — draft floors, ratified with this
> package)"

§3 states the counts against those floors: they do
not fire. The study-level outcome after G3 stays
INSTANTIATES-path at most; the bare INSTANTIATES
verdict remains reserved to the independent reader
over G1–G5 (package §6).

## 10. The skeleton version this stage answers to

The skeleton copy of record in this spec's records:
`records/GENERALIZATION-SKELETON-2026-11-04.md`,
**SHA-256
`a66ffe4fcb6826465e34e97c81a13aff85228939204c9629889d45f7ce8d9876`**
(recomputed for this freeze), being the copy of
AXIOVEX/vexa commit `88839493` the G1 document and the
G2 derivation answered to (package basis note).
Ratification gave no direction to answer to the
A2-amended skeleton instead, so this stage answers to
the records' version, as the package's cross-program
note proposed.

## 11. Claims — the freeze's bearing

No claim's status, stage, or score is changed by this
record; the stage's ledger diff remains the adoption
append only (C090-23). The claims this act bears on:

- **C090-19 — the freeze precedes every computation.**
  This record is the freeze the claim requires,
  committed before any G3 profile over H1. Its
  falsifier's wider phrasing is the subject of §5's
  finding, which this record states rather than
  settles.
- **C090-18 — the held-out set is untouched by G1 and
  G2.** The extraction rules, the permitted counts,
  and the verification are stated at §§2, 3, 5; the
  overlap item the claim's text also names is
  discharged in the only honest form available, at
  §4.
- **C090-21 — the bar is the bar.** The bar and the
  case list are frozen at §§7, 9 exactly as adopted;
  nothing was added, dropped, or re-weighted.

## T402's "does not establish" line (from tasks.md)

*This does not establish:* that the held-out sets are
large enough to be interesting — the floors are the
minimum the administration needs to be a test at all.
Nor does it establish that the stage may proceed: §5's
finding stands for the parent seat's ruling before
T403.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI. No profile over H1 was computed
for this record; the only quantities taken are the
counts §3 states.
