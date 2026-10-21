# Spec 057 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has two adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign
>    plan**, approved by the owner as written
>    on 2026-10-21
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`):
>    Spec 057 is member 14 of the twenty —
>    design D-19, the heading carried by five
>    sources; falsifier, in the plan's one
>    line: "A source's passage is empty or
>    unlocatable — each of the five is
>    accounted for, not assumed." Inputs in
>    hand: the five held source documents.
>    The campaign's Part 4 wave-1 order puts
>    the fragment recoveries (D-15, D-17,
>    D-19) in the independent parallel set,
>    sharing a drafting pattern.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-19 found **RIPE** — "Re-extraction
>    of the full passage under the same
>    heading in each of the five held source
>    documents; the deliverable is up to five
>    genuine claims entering at the *created*
>    stage, each accounted for as CLAIM
>    RECOVERED, PASSAGE EMPTY, or SOURCE
>    UNLOCATED."
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 057: both remain
> separate later acts. Under the campaign's
> E-1 decision, the freeze (when ordered)
> files this spec's own OSF contract
> registration; nothing is filed at draft.

## 1. The adopted basis (operative substance)

- **The design.** D-19 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/03-fragments.md`,
  §D-19): re-extract, from each of the five
  source documents, the full passage under
  the heading; each recovered passage becomes
  its own claim record through normal intake
  (proposition in plain words, numbers
  attached, falsifier written from the
  passage's own logic or its absence
  recorded); the checks those claims need are
  designed per claim at intake, not
  pre-invented in the spec; the heading
  record is dispositioned by appended note.
- **The criteria, fixed in the design in
  advance.** Every one of the five passages
  accounted for with one of three recorded
  outcomes: CLAIM RECOVERED (proposition +
  numbers + falsifier status on record),
  PASSAGE EMPTY (the section states no
  checkable finding — quoted evidence
  attached), or SOURCE UNLOCATED (the
  document cannot be found in the program's
  library after a stated search — the
  unblocking act is then named per source).
  Anything less is a failure of the design.
- **The claim.** `ancient_writing_and_modern_technologies_51831ac9_statisti_0004`:
  UNTESTED fragment, heading only, Phase-104
  RULE-NOCOND. The adopted lane-2
  not-understood text prescribes exactly this
  act (re-extraction, or an appended note
  retiring the fragment).
- **The five sources.** The canonical
  record's own source and its four evidence
  instances, enumerated in §2.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
from `main` at 83b6a563, via the gh git-data
API only (the local checkout was not
touched):

- **The canonical record** — read in
  `glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json`:
  the heading in full, `claim_status`
  untested, fingerprint
  `a4874349e0cc0ba23b711f10c78f60372639c2dc6f352165b48d4a9e44272469`,
  and the four evidence instances with their
  claim ids and `merged_into` pointers
  (Fuls 2023 …_statisti_0001; positional
  analysis paper …_statisti_0001; Wells
  …_statisti_0003; Hunt …_statisti_0002).
  Each instance's own claims file was also
  read and carries the same fingerprint and
  merge pointer.
- **Phase I merge** — `specs/029-tao-claim-lifecycle/phase-i-record.md`,
  merge group 3, agrees with the record
  exactly (canonical + the same four).
- **Phase-104** —
  `glossa-indus/reports/phase104_claims_evaluation.json`:
  this claim's entry is `stays_untested`,
  rule RULE-NOCOND, reason as spec §1 quotes.
- **Lane-2 draft** — the adopted entry for
  this claim (gist, claim_plain, explanation,
  not_understood) read in full; its evidence
  instance list agrees with the record.
- **The five source documents** — each
  source's literature registry file read in
  full: document_id, original filename, file
  size, `checksum_sha256`, recorded stored
  paths, license_status "unclear" (all
  five). Pin table (spec §2.1): every
  cleaned text, claims file, and registry
  file SHA-256 recomputed at this draft.
- **Cross-validation of the pinning method**
  — the S-4 cleaned text recomputes to
  `62acf855…` and the S-4 claims file to
  `bd0f7abd…`, identical to the pins Spec 046
  computed independently for the same files;
  the Phase-104 file recomputes to
  `2d0b83e8…` and the lane-2 drafts file to
  `3f645c9a…`, also identical to Spec 046's
  pins. Two independent drafts pinning four
  shared files to the same values is the
  method checking itself.
- **Heading occurrence posture (string
  search only — no passage was read for
  content, and none was extracted).**
  Case-insensitive occurrences of "positional
  analysis" in each held cleaned text, with
  the form of the occurrences:
  - S-1: 2 occurrences — one inside a running
    sentence (line 102), one in a
    bibliography entry citing Fuls 2013's
    paper (line 663). **No heading-form
    occurrence.**
  - S-2: 3 occurrences — a table-of-contents
    entry "3 Positional Analysis of Indus
    Signs 70" (line 65) and chapter running
    heads "CHAPTER 3. POSITIONAL ANALYSIS OF
    INDUS SIGNS" (lines 536, 612). A chapter
    heading exists.
  - S-3: 18 occurrences — the running head
    "Positional Analysis of Indus Signs"
    (the paper's own title) repeated from
    line 54 onward.
  - S-4: 10 occurrences — a table-of-contents
    entry for "Appendix II: Positional
    Analysis of Indus Signs" (line 86), the
    appendix heading itself (line 3456),
    figure captions, and running-text
    mentions. An appendix heading exists.
  - S-5: 1 occurrence — sentence-initial
    inside a running paragraph (line 267).
    **No heading-form occurrence.**
  These postures ground spec §10's first
  risk, claim F057-C07's heading-form rule,
  claim F057-C14's evidence, and defect D-1
  below. They are drafting verification of
  the inputs, not results: what any passage
  *states* has not been examined, by design.
- **Not done at draft, by design** — no
  passage was extracted, delimited, or read
  for its finding; no recovered claim was
  stated; no code was written or run; the
  AEE hooks have not run; nothing was filed
  with OSF.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   §2 pin re-asserted against the merged
   record — or decline, leaving the heading
   record with its lane-2 stated gap as the
   program's word on it.
2. **OPEN-1 (from DD-057-3): the HEADING NOT
   PRESENT sub-state.** Design D-19's three
   outcome words do not cover a located
   document with no heading in it — a real
   case for at least S-1 and S-5 on the
   draft's occurrence postures. The draft
   records it as a sub-state of SOURCE
   UNLOCATED (DD-057-3 / defect D-1). The
   freeze confirms that reading, or replaces
   it with a fourth outcome word and adjusts
   the §7 partition accordingly — openly,
   in the freeze record.
3. **OPEN-2: the S-3 delimitation.** The
   draft fixes: where the heading is the
   document's own title, the passage is the
   findings-bearing body, cited by line
   range (§5.2). The freeze confirms, or
   fixes a narrower delimitation for S-3
   (for example its stated-results sections
   only) before any passage is read.
4. **OPEN-3: whether the recovered claims'
   intake is an execution deliverable of
   this spec.** Proposal (DD-057-6): yes —
   the intake records are produced inside
   this execution through the normal intake
   form, at the created stage; their checks
   are designed later, per claim, outside
   this spec. The freeze confirms or assigns
   the intake to a follow-on act.
5. **OPEN-4 (campaign E-1): OSF
   registration.** The campaign settles that
   every specification in the pass files its
   own OSF contract registration at its
   freeze. The freeze act files it; nothing
   is filed at draft.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-057-1 — The five are the merge
  record's five.** The source set is the
  canonical record plus its four recorded
  evidence instances, identified by claim id
  and document id (claim F057-C03). The
  design's prose descriptions ("the Fuls
  2023 catalogue work", "Hunt's book") are
  resolved to records, not left as
  descriptions an executor could re-match.
- **DD-057-2 — Two-layer pins, document of
  last resort.** The held cleaned text is
  the working copy for location and
  extraction; the source document, verified
  by its registry checksum, is the copy of
  last resort within the stated search, so a
  heading lost by the text layer is found
  before a source is called unlocatable —
  and the discrepancy is recorded when it
  happens (spec §4 step 4).
- **DD-057-3 — HEADING NOT PRESENT is a
  sub-state of SOURCE UNLOCATED.** A located
  document in which no heading-form
  occurrence exists has no passage to
  extract; the source's passage is
  unlocatable in the held text even though
  the document is not. Folding it into
  PASSAGE EMPTY was rejected (an absent
  section is not an empty one, and the
  distinction decides whether re-acquisition
  can unblock it). Flagged OPEN-1.
- **DD-057-4 — Heading form, not string
  match.** Only a structural heading anchors
  a passage (claim F057-C07). The naive
  string rule was rejected on evidence found
  at this draft: it would anchor S-1's
  "passage" in its bibliography entry for
  S-3's paper — importing one source's
  passage into another's row and accounting
  for five sources with at most four
  passages.
- **DD-057-5 — A checkable proposition
  without numbers is RECOVERED.** Design
  D-19's CLAIM RECOVERED shorthand reads
  "proposition + numbers"; its PASSAGE EMPTY
  definition reads "states no checkable
  finding". Where the two pull apart — a
  passage stating a checkable proposition
  with no numbers — the EMPTY definition
  governs: the claim is recovered with
  "numbers: none stated" on its record
  (claim F057-C10).
- **DD-057-6 — Intake inside the execution;
  checks outside it.** Recovered claims are
  entered through normal intake as part of
  this execution's deliverables, at the
  created stage; designing their checks is
  later work, per the design. Flagged
  OPEN-3.
- **DD-057-7 — No retirement while a source
  is unlocated.** The design retires the
  heading record "if a passage recovers
  nothing statable". Read against the
  design's own SOURCE UNLOCATED outcome, the
  draft holds retirement unavailable when
  r = 0 and u ≥ 1: an unlocated passage
  might state a finding, and retiring the
  record would close a question the
  accounting has not answered (claim
  F057-C13).
- **DD-057-8 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-057-9 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today; the
  completion Spec 038's freeze had to
  retrofit is done here at the act that
  actually observed the records.

## 5. Double derivation of the acceptance tests (doctrine record)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived twice,
independently, from the requirement alone,
before the register was written:

- **Derivation A** worked from the
  requirement text forward: for each claim,
  what observable record, produced by the run
  itself, would show the requirement held?
- **Derivation B** worked from the falsifier
  and the pre-written outcome wordings
  backward: for each claim, what would a
  hostile reader check in the outcome record
  to show the requirement had *not* held?

The two derivations agreed on the gate,
count, and inspection tests for F057-C01,
C02, C03, C04, C05, C09, C11, C12, C13, and
C15 without amendment: in each case A's
"record produced in order" and B's "absence
or disorder of that record falsifies" are
the same check read from the two directions,
and the register states it once.

Disagreements, and their resolutions:

- **X-1 — Is the outcome mapping total over
  what the sources can actually do?** A
  mapped the five sources onto the design's
  three words directly. B enumerated the
  cases from the draft's own occurrence
  postures and found a fourth case the three
  words do not name: the document is located
  and pinned, searched in full, and contains
  no heading — so there is no passage to be
  empty and no document to be unlocated.
  S-1 and S-5 sit in that case on the
  postures of §2. **Resolution:** the gap is
  a defect in the design's outcome set (§6,
  D-1); the draft adds the HEADING NOT
  PRESENT sub-state under SOURCE UNLOCATED
  (DD-057-3) and flags it OPEN-1 for the
  freeze. The alternative — scoring it
  PASSAGE EMPTY — was rejected because it
  would state that a section exists and says
  nothing, when the record would show no
  section exists in the held text at all.
- **X-2 — What makes a passage "found"?**
  A, reading the recorded `quote_fragment`s,
  anchored the passage at any occurrence of
  the string "positional analysis". B quoted
  the record against A: S-1's instance is
  lowercase running text, and S-1's text
  carries a bibliography entry naming S-3's
  paper, so A's rule manufactures S-1's
  passage out of S-3's document and leaves
  the accounting at four real passages for
  five rows. **Resolution:** B governs; the
  heading-form rule is DD-057-4 /
  F057-C07, with the heading's verbatim form
  and locator recorded per row so the
  judgement is re-judgeable.
- **X-3 — Must a recovered claim carry
  numbers?** A read the design's CLAIM
  RECOVERED shorthand ("proposition +
  numbers + falsifier status") literally: no
  numbers, no recovery — such a passage is
  EMPTY. B read the design's PASSAGE EMPTY
  definition ("the section states no
  checkable finding") and held A's reading
  would record a passage that plainly states
  a checkable finding as stating none — a
  false row, quotable against the passage
  attached to it. **Resolution:** B governs
  (DD-057-5 / F057-C10): numbers are
  recorded as stated, or as "none stated";
  checkability, not numeracy, is the
  boundary.
- **X-4 — When is a source unlocatable?**
  A scored SOURCE UNLOCATED from the
  repository alone: cleaned text missing,
  source unlocated. B held the program's
  library is bigger than one path — the
  registry records stored paths and a
  checksum for the document itself, and a
  source acquirable from them has not
  survived "a stated search" until they are
  checked and any candidate hash-verified.
  **Resolution:** B governs; the four-step
  stated search is spec §4 / F057-C06, and
  an UNLOCATED row without its full log is
  void.
- **X-5 — Where does the verbatim passage
  live?** A proposed the outcome record
  reproduce all five passages inline. B
  noted S-3's passage may be a whole paper
  and S-4's an appendix, and that all five
  sources carry license_status "unclear":
  an inline reprint is unwieldy as a record
  and careless as a rights posture.
  **Resolution:** passage artifacts in the
  spec directory, SHA-256 on the row, cited
  by locator (F057-C08); the outcome record
  quotes what the accounting judgements need
  (§6's EMPTY evidence standard) and no
  more. F057-C15 carries the license limit.
- **X-6 — Does the headline need the
  unlocated count, or only the recovered
  count?** A wrote the headline from r
  alone. B enumerated the (r, e, u) triples
  and showed r alone conflates cases with
  different dispositions: (r=2, u=0) closes
  the heading record by supersession with a
  complete accounting behind it; (r=2, u=2)
  leaves two unblocking acts open. **Resolution:**
  the §7 partition is over (r, u) jointly —
  exhaustive over all 21 triples — and
  F057-C13's disposition rule keys on the
  same pair.

## 6. Defects found at drafting

- **D-1 — Design D-19's outcome set is not
  total.** CLAIM RECOVERED / PASSAGE EMPTY /
  SOURCE UNLOCATED name no outcome for a
  located document containing no heading —
  the case §2's postures show for S-1 and
  S-5 (and the case S-1's lowercase
  `quote_fragment` already hints at in the
  original record). Repaired at draft by
  DD-057-3's sub-state, flagged OPEN-1; the
  design itself is not edited.
- **D-2 — The registry metadata for the
  five sources is unreliable, and two
  extracted-claims files carry empty
  titles.** Recorded instances: S-2's
  registry `detected_year` is 2008 for a
  document the program cites as Fuls 2023;
  S-5's `detected_doi` is truncated
  mid-string ("10.1002/(SICI)1099-"); S-1
  and S-4 carry no detected year. Nothing in
  this draft identifies a source by that
  metadata — identity is document_id plus
  hash (F057-C04) — but a freeze that wants
  fuller citations for S-1 or S-5 must build
  them from the documents, not from the
  registry fields.
- **D-3 — "The five held source documents"
  is a two-layer holding, and the design
  does not say so.** The source PDFs are not
  in the repository; what the repository
  holds is the cleaned text of each, and the
  PDFs are held at the registry's recorded
  local paths under their checksums. A draft
  that pinned only the repository layer
  would make SOURCE UNLOCATED turn on which
  machine executes. Repaired at draft by
  DD-057-2's two-layer pin and the §4 stated
  search, which is venue-explicit.
- **D-4 — The campaign plan's one-line
  falsifier for D-19 is narrower than the
  design's criteria.** The plan's line ("a
  source's passage is empty or unlocatable")
  names two of the design's three outcomes
  and none of its accounting rule. The draft
  follows the design (which the plan's Part 2
  itself defers to: "the frozen
  specification's own wording governs"), and
  records the difference here so the freeze
  is not surprised by the third outcome or
  by the completeness rule.

## 7. Freeze decisions (2026-10-21)

> ## FREEZE ACT — DECIDED — 2026-10-21
>
> The freeze act of 2026-10-21, under the
> campaign plan approved by the owner as
> written the same date (Wave 2 freeze wave),
> decided the items §3 left open. Each
> resolution is recorded here on the record;
> the register rulings were carried into
> `claims.json` before the AEE hooks ran, and
> the hooks passed over the recovered register
> (0.8-draft; `aee/freeze-aee-note.md`).

- **DD-057-10 — OPEN-1 resolved: the HEADING
  NOT PRESENT sub-state confirmed.**
  DD-057-3 stands as drafted: a located
  document in which no heading-form occurrence
  exists is recorded SOURCE UNLOCATED with
  the sub-state HEADING NOT PRESENT IN HELD
  TEXT. It is not a fourth outcome word (the
  §7 partition over (r, e, u) stands exactly
  as drafted, exhaustive over all 21 count
  combinations), and it is not PASSAGE EMPTY
  (an absent section is not an empty one, and
  the distinction decides whether
  re-acquisition can unblock it). The freeze
  re-verified the ground first-hand at
  `main` 770155de: S-1's held text carries the
  string twice (line 102 running text; line
  663 a bibliography entry for S-3's paper)
  and in heading form not at all; S-5's held
  text carries it once (line 267, inside a
  running paragraph) and in heading form not
  at all.
- **DD-057-11 — OPEN-2 resolved: the S-3
  delimitation confirmed.** Spec §5.2 stands
  as drafted: where the heading is the
  document's own title (S-3, the paper
  "Positional Analysis of Indus Signs", its
  title standing as a running head from line
  54 onward, 18 occurrences in the held
  text), the passage is the document's
  findings-bearing body, cited by line range
  in the passage artifact of §5.3, not
  reprinted in the outcome record. No
  narrower delimitation is substituted: a
  stated-results-sections-only rule would
  have the freeze pre-judge which parts of
  the paper bear findings before any passage
  is read, which is the executor's recorded
  judgement under §6, visible on the row.
- **DD-057-12 — OPEN-3 resolved: intake
  inside the execution confirmed.**
  DD-057-6 stands as drafted: the recovered
  claims' intake records are produced inside
  this execution through the programme's
  intake, at the created stage; designing
  their checks is later work, per claim,
  outside this spec. No follow-on act is
  substituted for the intake itself.
- **DD-057-13 — OPEN-4 (campaign E-1): OSF
  registration at the freeze.** This spec
  files its own OSF contract registration at
  the freeze, under campaign decision E-1.
  The filing record is
  `osf-spec-registration.md`. Execution
  awaits the registration's approval act and
  a separate execution order; no mail is
  handled by the freeze.
- **DD-057-14 — DD-057-5 confirmed.** A
  checkable proposition stated without
  numbers is CLAIM RECOVERED, with
  "numbers: none stated" on its record; the
  design's PASSAGE EMPTY definition, not its
  CLAIM RECOVERED shorthand, governs the
  boundary.
- **DD-057-15 — DD-057-7 confirmed.**
  Retirement of the heading record is not
  available while r = 0 and u ≥ 1: the record
  stands as a stated gap, the note records
  the accounting so far and the named
  unblocking acts.
- **DD-057-16 — Phase-419 allocated.** The
  execution phase number (DD-057-8) is
  allocated at this freeze as **Phase-419**,
  from the merged record as it stands: the
  freeze records on `main` allocate
  Phase-404 to Phase-411, Phase-413,
  Phase-414, Phase-416, and Phase-418 (with
  Phase-412, Phase-415, and Phase-417
  standing unallocated as tombstones of the
  Spec 052, 049, and 054 freeze failures),
  and no record allocates Phase-419 to any
  other act.
- **DD-057-17 — The DD-038-10 AEE gate
  reading adopted.** The gate is: at every
  lifecycle hook, zero correctness failure
  modes and no claim below the 0.70
  threshold; FR-2.3 draft-cap records alone
  do not block a freeze, because they are
  lifted only by human ratification (a
  status change), not by any recovery
  available at a freeze. The hooks passed on
  that reading (`aee/freeze-aee-note.md`).

DD-057-1 to DD-057-9 are **confirmed** as
drafted, including DD-057-2's two-layer pin
(the held cleaned text as working copy; the
source document, verified by its registry
checksum, as the copy of last resort within
the stated search), DD-057-4's heading-form
rule, and DD-057-9's `observed_at` carriage.
Every §2 pin was re-asserted at the freeze
against `main` at 770155de by two independent
routes (contents-API raw and git-blob),
agreeing byte-for-byte, with a third local
route (a fresh clone's checked-out blobs)
agreeing on every file; every recomputed
hash equals its draft pin, including the
anchors file at `df0cf620…` (570,344 bytes),
recomputed fresh at the freeze.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
