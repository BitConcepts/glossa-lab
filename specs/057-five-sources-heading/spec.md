# Spec 057 — The Heading Carried by Five Sources: Re-extract the Five Passages (Design D-19)

> ## FROZEN — 2026-10-21
>
> Frozen at the freeze act of 2026-10-21
> under the runnable-experiments
> campaign plan approved by the owner as
> written on 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
> Part 2, member 14), and the portfolio
> triage of the same date
> (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`),
> which found design D-19 RIPE. The AEE
> lifecycle hooks ran at the freeze gate and
> passed over the recovered register
> (0.8-draft; `aee/freeze-aee-note.md`); the
> freeze record is `freeze.md` / `freeze.json`
> in this directory, and the spec's OSF
> contract registration is filed at the freeze
> under campaign decision E-1
> (`osf-spec-registration.md`). **Execution
> is a separate later act**: it runs as
> Phase-419 (DD-057-16), only after this
> freeze has merged, the registration's
> approval act has completed, and a separate
> execution order is given. Nothing has been
> extracted, recovered, or run by the freeze
> itself.
>
> The execution phase number was allocated
> at the freeze act: **Phase-419** (DD-057-16,
> completing DD-057-8).

**Design source:** D-19 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/03-fragments.md`,
§D-19, read in full at this draft).

**Claim under test:**
`ancient_writing_and_modern_technologies_51831ac9_statisti_0004`
— an UNTESTED fragment, in full a heading:
"Statistical finding: positional analysis."
Phase I merged five extractions of that
heading, from five source documents, into
this one record; the four others are kept on
it as evidence instances.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The record states no proposition. Phase-104's
evaluation says exactly why it cannot be
checked as it stands (`glossa-indus/reports/phase104_claims_evaluation.json`):
verdict `stays_untested`, rule **RULE-NOCOND** —
"Auto-extraction fragment with no falsification
condition and no stated proposition; not
evaluable as stated (constitution section IV)."

The merge is on record in Spec 029's Phase I
record (`specs/029-tao-claim-lifecycle/phase-i-record.md`,
merge group 3): proposition fingerprint
`a4874349e0cc0ba23b711f10c78f60372639c2dc6f352165b48d4a9e44272469`,
canonical record the claim above, evidence
instances the same heading extracted from the
Fuls 2023 catalogue work, from a
positional-analysis paper, from the
archaeology-and-epigraphy source (Wells 2015),
and from Hunt's book. The adopted lane-2 draft
for the record (`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`)
states the open point this spec answers: "What
would change the picture: re-extraction of the
five source passages in full, each becoming
its own claim with its numbers attached, or an
appended note retiring this fragment as an
extraction artefact."

### 1.1 The question, in plain words

Five published documents each carried a
section the extraction harvested as the bare
heading "Statistical finding: positional
analysis" — and kept the heading and lost
whatever each section found. What did each of
the five sections actually say? Go back to
each source document, find the passage under
that heading, and put what it says on the
record — or put on the record, for that
source, that the passage states nothing
checkable, or that the source cannot be
located. Every one of the five is accounted
for, not assumed.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** The five passages are not all
empty: at least one of them states a checkable
finding about sign positions — a proposition,
with its numbers, its corpus, and its stated
conditions — that can enter the claim set as a
real claim at the *created* stage.

**Falsifier / accounting rule.** The design's
success condition is accounting, not recovery:
this spec succeeds if every one of the five
sources ends with exactly one recorded outcome
— CLAIM RECOVERED, PASSAGE EMPTY, or SOURCE
UNLOCATED (§6). A source skipped without an
outcome, a passage assumed rather than
located, or a "recovered" proposition the
passage does not state, falsifies the
execution, whatever the headline says.

## 2. Inputs (pinned at this draft; re-asserted at the freeze — all pins verified, `freeze.md` §2)

### 2.1 The five sources — the fixed set

The set is exactly the canonical record plus
its four evidence instances, as recorded in
§1. No source may be added, dropped, or
substituted. Each source is pinned three
ways: its extracted-claims file and its
literature registry file in the repository,
its held cleaned text, and the source
document's own checksum as recorded in the
registry at intake.

| # | Source (as cited in the program's record) | Source claim_id | document_id |
|---|---|---|---|
| S-1 | "Ancient Writing and Modern Technologies" (the canonical record's own source; detected DOI 10.13109/hisp.2015.128.1.42) | `ancient_writing_and_modern_technologies_51831ac9_statisti_0004` | `ancient_writing_and_modern_technologies_51831ac9` |
| S-2 | Fuls 2023, *A Catalog of Indus Signs* (CITATIONS.md §A.10; the design's "Fuls 2023 catalogue work") | `fuls2023_catalog_of_indussigns_searchins_1dbdecdb_statisti_0001` | `fuls2023_catalog_of_indussigns_searchins_1dbdecdb` |
| S-3 | Fuls 2013, "Positional Analysis of Indus Signs", *Voprosi Epigrafiki* 7(1): 253–275 (CITATIONS.md §D.9; the design's "positional-analysis paper") | `positional_analysis_of_indus_signs_a2bedc93_statisti_0001` | `positional_analysis_of_indus_signs_a2bedc93` |
| S-4 | Wells 2015, *The Archaeology and Epigraphy of Indus Writing* (CITATIONS.md §A.7; the design's "archaeology-and-epigraphy source") | `the_archaeology_and_epigraphy_of_indus_w_27f45a68_statisti_0003` | `the_archaeology_and_epigraphy_of_indus_w_27f45a68` |
| S-5 | Hunt, *Without Kings or Conquests* (the design's "Hunt's book"; registry file name as recorded) | `without_kings_or_conquests_the_indus_scr_ce9d98cc_statisti_0002` | `without_kings_or_conquests_the_indus_scr_ce9d98cc` |

Pins per source (all recomputed at this draft
from `main` at 83b6a563; every pin re-asserted
at the freeze against `main` at 770155de by
two independent routes, agreeing byte-for-byte
— `freeze.md` §2):

| # | Held cleaned text (`glossa-indus/processed/cleaned_text/<document_id>.txt`) SHA-256 | Extracted-claims file (`glossa-indus/claims/extracted_claims/<document_id>.json`) SHA-256 | Registry file (`glossa-indus/literature/documents/<document_id>.json`) SHA-256 | Source document as recorded in the registry (original filename; size; checksum_sha256) |
|---|---|---|---|---|
| S-1 | `1275b795903260221f5226bada352de27471c010e2ad8ace556c548c20da1fc4` | `e98190894202a2a1c0e314229dcb585c62a0f5c12c059bcabd63b055c42959e8` | `92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c` | `Ancient_Writing_and_Modern_Technologies.pdf`; 3,565,316 bytes; `51831ac997f54782fc6483e04c06d6b60f08af81101b39bfe00daa5556b88b04` |
| S-2 | `dae154327592d19366c9feb56362477fa842114cec944416b9b05dc3f0efd4cb` | `857abacac4317fa0f7bdf7d4052661a4109b6f5ee507843b93cac8c5ad46c5a4` | `bb23e5e9f90c30ebebb2d45e2967fb668a54432a56692a8772753fd228316f47` | `Fuls2023_Catalog_of_IndusSigns_SearchInside.pdf`; 9,814,734 bytes; `1dbdecdb14854b57d7d6a7a4b978ef814312cc3f6bf246f8cf0313acdbbd6f2a` |
| S-3 | `9ed24098c006fcde5bb0ca7be6a6fa188011c3bc7bb8db46796abc77961a0708` | `713576363f9678281703866e6b749a9486d754906173bb48b7b44367531dc6f8` | `9b95174bad62c9a4879ae3db28a03ee52bc665df4e1d9897e65f84f353baa53c` | `Positional_Analysis_of_Indus_Signs.pdf`; 468,669 bytes; `a2bedc93d9c0fc7dfae53ea0b93859c2ac2110639d7ab53d5daab3cd034d6f6c` |
| S-4 | `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` | `bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a` | `b2638a705549348d2d857989e74f7a8ab09bd4e3ea60d6e3dfab4e49fd9eba68` | `The Archaeology and Epigraphy of Indus Writing.pdf`; 8,357,942 bytes; `27f45a680c021d75bc757fecb948e63ddc1bbcc5af5cd9130369a959d857fedc` |
| S-5 | `dd58497528db89fe75111d2431b9611aebd4a5a9715a4ecceb012d9d1538029e` | `c1a433d539a0ed899fe7ab11af2be0c608cb85d9f0fc99b2ccfefdb6e866262a` | `38122256305b8451e49e4ef4d56df7399363bdc3c57052b10f9165ab593261a7` | `Without_Kings_or_Conquests_The_Indus_Scr.pdf`; 321,649 bytes; `ce9d98cc32646b0d0023dd24a2f5c059f639019da8717b2ab3b7fb0f41012399` |

The recorded normalised heading differs only
in case across the five ("Statistical
finding: positional analysis" /
"…Positional Analysis"), and every instance's
recorded `quote_fragment` is "Positional
Analysis" — except S-1's, which is the
lowercase "positional analysis". That
difference is data, not noise: it is the
first sign (confirmed at this draft,
adjudication.md §2) that the five extractions
did not all harvest the same kind of object.

### 2.2 Record inputs

| Input | Pin / state |
|---|---|
| Phase-104 evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) | SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (recomputed at this draft) |
| Lane-2 adopted drafts (`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`) | SHA-256 `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` (recomputed at this draft) |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | Asserted byte-identical before and after any execution; this spec moves no anchor. Freeze-act pin, from a fresh recompute at the freeze (the Spec 040 stale-pin precedent): SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (570,344 bytes; `freeze.md` §2). |

No corpus, positional data, or classification
asset is an input to this spec. This is desk
work on held documents; nothing is counted.

## 3. Step 0 — gates before any passage is read for content (fail-closed)

Execution runs these checks in order, before
any heading search or passage reading. A
failure stops the execution in the class
named; nothing is repaired at run time.

- **0.1 Input integrity.** Every §2 pin
  hashes to its freeze-record value —
  including every held cleaned text that is
  present. (A cleaned text that is *absent*
  is not a pin mismatch; it starts the stated
  search, §4.) A mismatch closes the run as
  **CLOSED AT STEP 0 — INPUT PIN MISMATCH**,
  naming the input.
- **0.2 Source-set integrity.** The canonical
  record still carries exactly the four
  evidence instances of §2.1, with the claim
  ids and the proposition fingerprint
  `a4874349…` as recorded. A different set
  closes the run as **CLOSED AT STEP 0 —
  SOURCE SET CHANGED**: the five this spec
  was drafted and frozen against no longer
  exist as a set, and re-drafting — not
  repair — is the next act.
- **0.3 Order.** No passage text is read for
  content, and no heading search is run,
  before gates 0.1–0.2 pass. The execution
  record shows the gate verdicts before the
  first per-source row, or the run is
  non-compliant on its face.

## 4. The stated search (what "unlocatable" must survive)

A source is recorded SOURCE UNLOCATED only
after every step below has been run for that
source and has returned nothing, and the
search log (each step, its location, its
result) is attached to that source's row.
The steps, in order:

1. **The pinned held cleaned text** at its
   §2.1 path. Present at pin → the source is
   located; proceed to §5.
2. **Repository-wide search** for the
   source's `document_id` string (a moved or
   renamed copy), any candidate verified by
   SHA-256 against the §2.1 cleaned-text pin.
3. **The recorded stored paths** in the
   source's registry file (`stored_path_raw`,
   `stored_path_text`, and the original
   filename) on the execution host, any
   candidate document verified by SHA-256
   against the registry's recorded
   `checksum_sha256` for the source document.
4. **The source document itself**, if a copy
   is produced by any step: its text layer is
   searched under §5's heading rule; a
   heading found in the document but not in
   the cleaned text is extracted from the
   document, and the cleaned-text discrepancy
   is recorded on the source's row.

SOURCE UNLOCATED carries one of two recorded
sub-states, and the row states which:

- **DOCUMENT UNLOCATED** — no copy of the
  document was found by steps 1–3.
- **HEADING NOT PRESENT IN HELD TEXT** — the
  document was located and pinned (step 1, 2,
  or 3), the full text was searched under
  §5's heading rule including step 4, and no
  heading-form occurrence exists in it.

For either sub-state, the row names the
**unblocking act** for that source:
re-acquisition of the source through ordinary
published-source channels, identified by the
§2.1 citation (for HEADING NOT PRESENT: a
copy of the edition the original extraction
ran on, if a different edition is what the
program holds — the row says which possibility
the evidence supports, or that it cannot
distinguish them).

## 5. Step 1 — locate the heading, extract the passage

For each located source, in §2.1 order:

### 5.1 What counts as the heading

An occurrence of "positional analysis"
(case-insensitive) counts as **the heading**
only if it is in **heading form**: it stands
as the title of a section, chapter, appendix,
or titled part of the document — shown in the
held text by standing alone as a line or
running head, by chapter/appendix numbering,
or by a table-of-contents entry that points
to the passage it introduces. The heading
text as it stands (for example "Positional
Analysis of Indus Signs", "CHAPTER 3.
POSITIONAL ANALYSIS OF INDUS SIGNS") is
recorded verbatim on the source's row.

Occurrences that are **not** the heading, and
never anchor a passage: mentions inside
running sentences; bibliography and reference
entries (one source's bibliography citing
another source's paper does not make that
paper this source's passage — the five
passages are five, and they do not borrow
from each other); figure and table captions;
and cross-references to another document's
analysis.

### 5.2 Delimitation

The passage under a heading runs from the
heading occurrence to the next heading of
equal or higher rank in the same document, or
to the document's end. Running heads repeated
across pages are one heading, not many
passages. Where the heading is the document's
own title (a paper titled with the heading),
the passage is the document's findings-bearing
body — its stated results, in the document's
own sections — and the verbatim record is the
passage artifact of §5.3 cited by line range,
not a reprint of the whole document in the
outcome record.

### 5.3 The locator and the verbatim record

For each located passage, the row records:

- **citation** — the §2.1 citation of the
  source;
- **locator** — the held cleaned text's line
  range of the passage; the heading's line;
  and the source document's page or chapter/
  appendix designation where the held text
  carries one;
- **verbatim passage** — the passage text
  exactly as it stands in the pinned held
  text, written to a per-source passage
  artifact in this spec's directory at
  execution, whose SHA-256 is recorded on the
  row. The only permitted normalisation is
  rejoining lines broken by the text layer;
  every rejoined passage is produced from the
  pinned bytes, and any other alteration —
  modernised spelling, silently supplied
  punctuation, a dropped table — makes the
  row non-compliant. Tables and figures the
  passage relies on are named in the locator
  even where their content cannot be carried
  as text.

## 6. Step 2 — the per-source accounting

Each source receives exactly one outcome.
The three outcome words are design D-19's,
with their content standards fixed here:

- **CLAIM RECOVERED** — the passage states a
  checkable finding. The row carries the
  recovered claim record, stated from the
  passage and nothing else: (a) the
  proposition, in plain words; (b) its
  numbers, verbatim as the passage states
  them — or the recorded entry "numbers:
  none stated" where the passage states a
  checkable proposition without numbers
  (DD-057-5); (c) its corpus and stated
  conditions, as the passage states them, or
  "not stated"; (d) **falsifier status** —
  a falsifier written from the passage's own
  logic, or the recorded absence of one (as
  D-08 had to record for a claim that lacked
  one). The recovered claim enters the claim
  set through the program's normal intake at
  the *created* stage, unchecked; designing
  its check is intake's work, not this
  spec's.
- **PASSAGE EMPTY** — the passage was located
  and extracted verbatim (§5), and it states
  no checkable finding: no proposition about
  sign positions carrying a quantity, a named
  corpus, or a directional or comparative
  assertion that could in principle be
  checked. The row attaches the quoted
  evidence: the passage itself if short, or
  its opening and closing and the
  finding-bearing span the executor judged —
  with the judgement stated, so a reader can
  disagree with it from the record.
- **SOURCE UNLOCATED** — per §4, with its
  sub-state, its search log, and its named
  unblocking act.

### 6.1 The accounting table (the form of record)

The outcome record's central table has
exactly five rows, in §2.1 order:

| # | Source (citation) | Source claim_id | Location state | Locator (or search-log ref) | Outcome | Recovered claim id (intake) or evidence ref |
|---|---|---|---|---|---|---|
| S-1 | … | … | located / unlocated (§4 sub-state) | line range + heading line, or §4 log | CLAIM RECOVERED / PASSAGE EMPTY / SOURCE UNLOCATED | … |
| S-2 | … | … | … | … | … | … |
| S-3 | … | … | … | … | … | … |
| S-4 | … | … | … | … | … | … |
| S-5 | … | … | … | … | … | … |

A table with a missing row, a row without an
outcome, or a row whose outcome its own
evidence does not support is a failed
execution under §1.2, not a result.

## 7. Aggregate outcomes — the headline, fixed in advance

Let *r* = sources CLAIM RECOVERED, *e* =
sources PASSAGE EMPTY, *u* = sources SOURCE
UNLOCATED; *r + e + u* = 5 by §6. The headline
is exactly one of the following classes,
derived mechanically from (*r*, *e*, *u*) —
the partition is exhaustive over all 21
count combinations:

- **A — FULL RECOVERY** (*r* = 5).
- **B — COMPLETE ACCOUNTING, PARTIAL
  RECOVERY** (*r* = 1–4, *u* = 0).
- **C — PARTIAL RECOVERY WITH UNLOCATED
  SOURCES** (*r* = 1–4, *u* ≥ 1).
- **D — NO CLAIM RECOVERED: ALL PASSAGES
  EMPTY** (*r* = 0, *u* = 0, *e* = 5).
- **E — NO CLAIM RECOVERED: EMPTY AND
  UNLOCATED** (*r* = 0, *u* = 1–4).
- **F — NO SOURCE LOCATED** (*r* = 0, *u* = 5).

### 7.1 Pre-written headline wordings

The outcome record's headline paragraph uses
the class's form, with the bracketed material
filled from the accounting table:

- **A:** "All five passages under the heading
  'Statistical finding: positional analysis'
  were located in their source documents and
  each states a checkable finding. Five
  claims, one per source, enter the claim set
  at the created stage with their numbers and
  falsifier status on record: [claim ids].
  None of the five is checked by this act;
  recovery is not verification."
- **B:** "All five sources are accounted for.
  [r] of the five passages state a checkable
  finding and enter the claim set at the
  created stage: [claim ids]. The remaining
  [e] passage(s) state no checkable finding:
  [source ids], recorded PASSAGE EMPTY with
  the passages quoted. No finding is
  attributed to any source beyond what its
  own passage states."
- **C:** "Five sources were to be accounted
  for; [r] yielded a recovered claim [claim
  ids], [e] passage(s) were located and state
  no checkable finding [source ids], and [u]
  source(s) could not be located after the
  stated search [source ids, sub-states]. The
  unblocking act for each unlocated source is
  named on its row. The heading record is not
  retired while a source remains unlocated."
- **D:** "All five passages were located, and
  none of them states a checkable finding.
  The heading 'Statistical finding:
  positional analysis' carried no finding in
  any of the five sources. No claim is
  recovered; the five passages stand quoted
  on the record as the evidence for that
  judgement."
- **E:** "No claim was recovered. [e]
  passage(s) were located and state no
  checkable finding [source ids]; [u]
  source(s) could not be located after the
  stated search [source ids, sub-states],
  with the unblocking act named on each row.
  What the unlocated passages state is not
  known and is not guessed here."
- **F:** "None of the five source documents
  could be located after the stated search.
  No passage was extracted and no claim is
  recovered. The unblocking act — re-acquisition
  of the five sources through published-source
  channels — is named on each row. The
  heading record stands exactly as recorded:
  a stated gap."
- **Step-0 closure:** "Spec 057 closed at
  step 0: [gate and observed values]. No
  passage was read for content and no source
  was accounted. The heading record stands
  exactly as recorded."

### 7.2 Disposition of the heading record

By appended, dated note on the canonical
record — appended only; the frozen record is
never edited — in exactly one of these forms,
chosen by the same counts:

- If *r* ≥ 1: **superseded** by the recovered
  claims it pointed at, which are named in
  the note.
- If *r* = 0 and *u* = 0: **retired** as an
  extraction artefact, with the five quoted
  passages as the note's evidence.
- If *r* = 0 and *u* ≥ 1: **no disposition** —
  the record stands as a stated gap, the note
  records the accounting so far and the named
  unblocking acts, and retirement is not
  available while a passage that might state
  a finding remains unlocated.

## 8. Reporting obligations

Every product of an execution carries:

1. the step-0 gate verdicts (§3), before any
   per-source material;
2. the five-row accounting table (§6.1), in
   §2.1 order, with each row's locator or
   search log;
3. the verbatim passage artifacts (§5.3) and
   their SHA-256 values;
4. for each recovered claim, its intake
   record (proposition, numbers, corpus and
   conditions, falsifier status) and its
   created-stage claim id;
5. the headline class and wording (§7), with
   the counts (*r*, *e*, *u*) it was derived
   from shown beside it;
6. the disposition note (§7.2) as appended;
7. the fence sentence: "This act recovered
   what five passages state. It checked none
   of it."

Deliverables at execution: the outcome
record under these rules, the per-source
passage artifacts, the recovered claims'
intake records, the experiment-graph node
(H15/H23, registered and verified before the
run), the outcome append in this directory,
and the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not. Anchors
asserted byte-identical before and after.

## 9. Epistemic limits (binding on all outputs)

1. **Recovery is not verification.** No
   outcome under this spec establishes any
   positional finding at all. Recovered
   claims start unchecked, and no output may
   present a recovered proposition as
   supported by its recovery.
2. **No credit transfers.** The topic the
   heading points at — whether signs occupy
   preferred positions — is well tested in
   this program on other records. None of
   that credit belongs on this record or on a
   recovered claim until the claim earns its
   own check.
3. **No invented propositions.** A recovered
   claim states what its passage states, in
   plain words, with the passage quoted
   beside it. An executor's paraphrase that
   strengthens, narrows, or numbers a claim
   the passage did not make is a defect of
   the execution, recorded as such.
4. **The frozen records stand.** The
   canonical record, its evidence instances,
   and the Phase I merge are never edited;
   this spec's products append beside them.
5. **Verbatim is internal.** Every registry
   record for the five sources carries
   license_status "unclear". The verbatim
   passage artifacts are internal program
   records; any later publication use of
   passage text requires the license
   verification the registry itself demands,
   as its own act.

## 10. Risks and honest weaknesses

- **The heading is not the same kind of
  object in all five sources.** At this
  draft, a string search of the held cleaned
  texts (adjudication.md §2 — occurrence
  postures only; no passage was extracted)
  finds a chapter heading in S-2, an appendix
  heading in S-4, the paper's own title as a
  running head throughout S-3, and no
  heading-form occurrence at all in S-1 or
  S-5. The §5.1 rule and the §4 HEADING NOT
  PRESENT sub-state exist because of this;
  a freeze that expects five identical
  sections will misread the record.
- **S-3's passage may be a whole paper.**
  Delimitation (§5.2) handles it by line-range
  citation, but the recovered-claim standard
  (§6) still has to be applied to a paper's
  stated results as a whole, and the
  executor's judgement there is visible in
  the record or the row fails §6.1.
- **Cleaned text is a copy.** The original
  extractions ran on the source documents;
  the held cleaned texts are the program's
  working copies. §4 step 4 exists so a
  heading lost by the text layer is found in
  the document before a source is called
  unlocatable — and so the discrepancy is
  recorded when it happens.
- **Registry metadata is unreliable.**
  Detected years and DOIs in the registry
  files are wrong or truncated for some
  sources (adjudication.md §6, D-2). Nothing
  in this spec identifies a source by that
  metadata; identity is by document_id and
  hash.

## 11. Stop conditions and outcome classes

Execution ends in exactly one of:

- **CLOSED AT STEP 0 — INPUT PIN MISMATCH**
  (gate 0.1) or **CLOSED AT STEP 0 — SOURCE
  SET CHANGED** (gate 0.2). No passage read.
- **A headline class of §7** (A–F), after all
  gates pass and all five sources carry an
  outcome. Classes C, E, and F contain
  unlocated sources; they are results of the
  design as written, not interruptions of it.

There is no outcome class for a partial
accounting: four rows and a headline is a
failed execution (§1.2), recorded as such.

## 12. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — input integrity,
   source-set integrity, order.
3. **Location** (§§4–5) — the stated search
   where needed; heading location and verbatim
   extraction per source.
4. **Accounting** (§6) — one outcome per
   source; recovered claims through normal
   intake at the created stage.
5. **Outcome** (§§7–8) — headline, disposition
   append, LEDGER entry; anchors asserted
   byte-identical; foundation check reported
   as measured.

## 13. What this spec is not

Not a positional analysis, not a check of any
recovered claim, not an edition hunt beyond
the stated search, and not an authorisation
to execute. It is the re-extraction of five
held passages, designed so that its honest
outcomes — including passages that state
nothing and sources that cannot be found —
are written down before any passage is read.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
