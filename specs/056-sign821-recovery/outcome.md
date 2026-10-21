# Spec 056 / Phase-418 — Outcome record (EXECUTED 2026-10-21 — IDENTIFICATION FAILED)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 056 contract
> (freeze digest
> `64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e`
> in `freeze.json` as merged, PR #254 merged at
> `2e15fad5`), as **Phase-418**, in Wave 3 group 2
> of the runnable-experiments campaign (plan
> approved AS WRITTEN on 2026-10-21). The
> execution gate was satisfied before the run:
> OSF registration **3eygs** is APPROVED +
> PUBLIC, DOI **10.17605/OSF.IO/3EYGS**. Base
> for the run: `main` at `3200b7b5`. Outcome:
> **IDENTIFICATION FAILED** — step 0 passed in
> full, two independent extraction passes
> recovered a specific argument from the pinned
> passage, the sign list was named from the
> document itself, and the drawn sign could not
> be identified by either route §5 R-3 allows.
> The fragment is neither recovered nor
> retired; it stays a stated gap. No statement
> about sign 821 is made.

## 1. What was executed

The frozen contract's execution shape (spec
§13), in order. Graph-first build (H15/H23):
experiment script
`backend/scripts/phase418_sign821_recovery.py`;
graph module
`backend/glossa_lab/experiment_graph_phase418.py`
(node `IndusPhase418Sign821Recovery`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The run's own
records: `reports/phase418_results.json`
(SHA-256
`f6b8c97b3b95ed3176f10994cbf109de1ff451fc1f11e2f7cf68ca5ca8b7c513`)
and `reports/phase418_recovery_report.md`
(SHA-256
`531c054cd1a0d9697e48b4e10adc377b03055898e1e95c5318e72714c460644e`);
the script is deterministic and a second run
reproduced both output files byte-identically.
The evidence of record:
`specs/056-sign821-recovery/extraction-record.md`
(SHA-256
`73792a47e137fdbee80bce3a2919aafc0c93fcad3fde4651548e0e2c1192312e`)
— the dry-run, both extraction sheets, the
reconciliation, and the R-3 record, in full.

**Headline (spec §6.1 wording, IDENTIFICATION
FAILED form).** "Re-extraction found a specific
argument in the passage of record (‘It is
suggested here that sign 821, in the Dholavira
signboard contexts, has a meaning of ‘city’,
either as a determinative or as a word.’,
printed p. 92), but the claim cannot be
recovered in the program's form: the drawn sign
could not be identified by either route §5 R-3
allows. The fragment is neither recovered nor
retired; it stays a stated gap, with this
closure as the record of why, and the
unblocking act is the preservation, as a
committed and hashed record, of an inspectable
drawn-form reference for Wells's sign 821 — the
Figure 2.6 sign-list pages (printed pp. 19–22)
or the Figure 6.13 examples as images tied to
the list entry — from which the drawn sign can
be matched by drawn form through the crosswalk
registry or quoted as the source list's own
entry."

**The passage of record (spec §8, element
1).** Wells (2015), "The Dholavira signboard,
revisited", printed pp. 90–94; held cleaned
text
(`glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`),
start anchor line "The Dholavira signboard,
revisited" (line 2783), end anchor line "The
Mohenjo-daro bangle pot" (line 2872); passage
lines 2783–2871, 5,354 bytes, SHA-256
`51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604`.
Anchor sentence, verbatim: "Whatever sign 821
reads it is used in a variety of contexts
(Figure 6.13)." (printed p. 93; occurrence
count 1 in the document.)

**The figure limit, stated with the outcome
(spec §8; DD-056-13).** The held cleaned text
drops the book's sign glyphs (blank slots stand
where glyphs were) and Figure 6.13 is
graphic-only in it, present only as its
caption. A contention carried only by the
figure's images or by a dropped glyph is
outside the passage of record; that limit
stands as a stated boundary of the recovery
test.

**Fence sentence (spec §8, element 6).** "This
act is record repair. It establishes, at most,
what the source passage argues — never whether
the argument is right, and nothing about sign
821 itself."

## 2. Step 0, gate by gate (all passed)

- **0.1 Input integrity — PASS.** Every §2
  input was recomputed at the run's base by
  two independent routes (the isolated
  worktree and the GitHub contents API, with
  identical results): held cleaned text
  `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e`;
  Phase-104 evaluation
  `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d`;
  lane-2 adopted drafts
  `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb`;
  crosswalk registry
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`;
  anchors
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`.
  The claim record was asserted in the
  freeze's own Spec 038 form (freeze.md §2):
  its freeze-time hash `bd0f7abd…` stands as
  the definition constant in `freeze.json`,
  and the fragment's facts were asserted on
  the live file — entry present, wording,
  UNTESTED status, and `created` stage exactly
  as the frozen record states, the source
  passage named in its not-understood text.
  The live file's whole hash differs from the
  constant for one recorded reason only: Spec
  046's execution appended its `first_check`
  entry to the _0002 claim in the same file
  (PR #263). The _0001 fragment entry was
  verified unchanged from the pinned bytes,
  field for field. The phase script
  re-verifies all of this fail-closed before
  any output is written.
- **0.2 Passage producible — PASS.** The
  source document was produced from the
  program's held copy; both anchor lines were
  located as standalone lines exactly once
  each, and the anchor sentence was located
  verbatim, occurrence count 1.
- **0.3 Passage pinnable — PASS.** The byte
  slice (lines 2783–2871) recomputed to
  5,354 bytes, SHA-256 `51d6fb3a…` — the
  freeze-pinned passage digest.

## 3. Dry-run (DD-056-16)

Before the protocol touched the fragment, the
§§4–5 sheet and checklist machinery was
exercised on a passage other than the passage
of record — "The Mohenjo-daro bangle pot"
(cleaned-text lines 2872–2931) — with a worked
candidate (sign 575 as a kiln logograph), its
verbatim quote verified by the phase script,
and its checklist completed in form. It
produced no candidate and no outcome for the
fragment. The worked dry-run is recorded in
the extraction record, §3.

## 4. Step 1 — re-extraction (two passes, reconciled)

Two independent passes over the pinned passage
only, each producing its extraction sheet, then
reconciliation (extraction record, §§4–6).
Pass A read the passage sequentially; Pass B
worked every "821" mention outward and swept
for unnumbered references. Both sheets found
the same candidate set, and the reconciliation
records full agreement on every checklist
line — no disagreement arose, settled or
unsettled, so the against-recovery rule
(DD-056-14) was not needed. Every quote on the
sheets was verified verbatim against the
pinned passage by the phase script.

- **K-1 (decisive).** "Sign 821, in the
  Dholavira signboard contexts, has a meaning
  of ‘city’, either as a determinative or as a
  word; of the passage's candidate glosses
  (DED 752 ūr; DED 808 eyil; DED 3568 nakar;
  DED 4112 pāri), eyil is the best choice,
  because Dholavira is a walled city made of
  cut stone." Quotes: the suggestion (lines
  2835–2836, printed p. 92); the gloss list
  (lines 2842–2845, p. 93); the eyil
  preference with its reason (lines 2846–2847,
  p. 93); premise quote, the signboard
  sequence's locative (lines 2794–2795,
  p. 91).
- **K-2.** The Fuls verification paragraph
  (lines 2848–2853, p. 93) — considered, and
  not credited as a candidate about sign 821:
  its asserted content concerns sign 861.
- **K-3.** The bare fragment restated (lines
  2854–2856, p. 93).
- **K-4.** The non-attestation of eyil-ay /
  eyil-i (lines 2854–2856, p. 93), considered
  as a standalone candidate.

Agreed non-candidates: the "copper/bronze
tool" sign-pair suggestion (the toponym pair),
the toponym-sequence observations (the
sequence), and the sign-798 discussion (a
different sign).

## 5. Step 2 — the recovery test (R-1…R-5)

- **K-1: R-1 PASS** (the passage's own
  suggestion, in its own words); **R-2 PASS**
  (a specific reading in a stated context —
  §5's own illustration of a specific
  contention); **R-4 PASS** (falsification
  condition stated from the passage's own
  logic: 821 shown to carry a different
  established value in signboard contexts, or
  the signboard sequence's locative element
  shown to be carried by other signs with 821
  outside it — with the passage's own ruling
  respected, that the non-attestation of
  eyil-ay / eyil-i is "not a nullification of
  the reading" and cannot serve as the
  condition); **R-5 PASS** (context bound,
  determinative-or-word alternative, all four
  glosses with DED numbers, the eyil
  preference with its reason, and the
  passage's hedge — no firm reading, correct
  gloss unknowable — all carried).
  **R-3 FAIL** (§6 below).
- **K-2: R-1 FAIL** — the paragraph's asserted
  content is about sign 861; a framing clause
  ("One verification of the sign 821 reading…")
  is not a proposition about 821 argued from
  evidence about 821.
- **K-3: R-1 FAIL, R-2 FAIL, R-4 FAIL** — the
  fragment restated; §5 rules it is not a
  recovery in its own right, it states no
  contention, and no falsifier can be written
  for it without inventing one.
- **K-4: R-1 PASS (narrow), R-2 FAIL** — an
  attestation absence from which the passage
  draws no contention; its content is carried
  into K-1's record under R-5 and R-4.

**R-3 (for K-1, the one candidate that reaches
it).** *The list is named from the document
itself:* "Chapter 2 gives the Indus sign list
used in this analysis" (held-text line 414);
"The sign list used here (Wells 2011)" (line
665); Chapter 2, "The Indus Sign List", with
Figure 2.6, "An Indus Sign List" (printed
pp. 19–22) — **Wells's own sign list (Wells
2011), as given in Wells 2015, Chapter 2 /
Figure 2.6**, the same apparatus finding Spec
046 recorded for its fragment from this book.
*The drawn sign is identified by neither
allowed route:* the pinned crosswalk registry
carries **no W821 value in any of its 803
rows** (sole or inside a multi-value cell), no
registry description names a city, and the
Phase-123 Wells segmentation witness (157
rows) carries no grapheme 821 — there is no
registry entry to match a drawn form against,
and the held text drops the glyph, so no drawn
form is available to match with; and the
source list's own entry for the sign stands in
Figure 2.6, which in the held text survives
only as its captions (lines 868–880), so no
entry can be quoted with its locator. The
registry's `Yunmapped_0821` row is a
Yajnadevam glyph identifier (`yajnadevam_glyphid`,
empty `wells_ids`, corpus frequency 10) — the
frozen number-collision trap; it was asserted
as a trap and not used, and no number-match
was used or attempted as an identification.
The appendix's "Doubled Signs" text (printed
pp. 128–129) describes 821's formation from
820 by number; it is not the list's entry,
carries no drawn form, and was not used.

**Mapping (spec §6).** No candidate passes
R-1…R-5, so RECOVERED does not fire. K-1
passes the argument conditions, so RETIREMENT
RECOMMENDED cannot fire — its wording would
call an arguing passage a catalogue
observation, which this record shows it is
not. The run closes as **IDENTIFICATION
FAILED** (DD-056-2, confirmed DD-056-11). No
test-design note arises (that note belongs to
a RECOVERED outcome, DD-056-17), and no test
was run on any sign, corpus, or reading.

**Unblocking act (named, per §6.1).** The
preservation, as a committed and hashed
record, of an inspectable drawn-form reference
for Wells's sign 821 — the Figure 2.6
sign-list pages (printed pp. 19–22) or the
Figure 6.13 examples as images tied to the
list entry — from which the drawn sign can be
matched by drawn form through the crosswalk
registry or quoted as the source list's own
entry. This record does not commission that
act.

## 6. What this outcome does and does not establish

It establishes that the pinned passage *does*
argue something specific about sign 821 — the
‘city’ reading in Dholavira signboard contexts,
in the form §4 above records — and that the
argument cannot be carried into the program's
claim form because the drawn sign cannot be
identified from the held record by the routes
the frozen test allows. The hypothesis of
spec §1.2 is therefore left **unjudged at the
identification condition**: it is not
supported (no claim was recovered) and not
refuted (the passage is not a catalogue
observation, so the falsifier — re-extraction
recovers no claim because no argument exists —
did not fire in its stated form; what fired is
the identification gate in front of recovery).
It does **not** establish anything about sign
821 itself: not its reading, classification,
distribution, or meaning (spec §10). Recovery
was not verification, and this closure is not
a verdict on the passage's suggestion, which
stands exactly as Wells stated it, hedges
included. Nothing about the book's other
sign-821 discussions (Chapter 3; the
appendices) is decided — they are outside the
passage of record, and the appendix text was
consulted only to record why it is not an R-3
route, never as argument evidence.

## 7. Claim consequences (governed register)

Executed under register 0.7-draft (frozen); one
line per claim, F056-C01…C15.

- **F056-C01** (an outcome states nothing about
  sign 821 itself): HELD — the outcome states
  what the passage argues and why the claim
  cannot be recovered in form; it states
  nothing about the sign.
- **F056-C02** (the fragment stands UNTESTED at
  the created stage): HELD — the record was
  read and asserted at gate 0.1 in the Spec
  038 form; its wording, status, and stage are
  as the frozen record states, and this
  closure leaves them unchanged.
- **F056-C03** (the passage argues something
  specific recoverable as a claim): UNJUDGED
  at the identification condition — the
  passage does argue something specific
  (K-1), but recoverability in the program's
  form failed at R-3, so the hypothesis is
  neither supported by a recovery nor refuted
  by a retirement; the outcome record says so
  (§6 above).
- **F056-C04** (no proposition passing the test
  → RETIREMENT RECOMMENDED): NOT FIRED — its
  antecedent is a passage with no passing
  argument; K-1 passed the argument
  conditions, so the case is the
  IDENTIFICATION FAILED closure the claim's
  own family mapping provides, not a
  retirement.
- **F056-C05** (the passage of record is the
  headed section, pinned): HELD — the passage
  was produced and recomputed to its pinned
  digest at gates 0.2–0.3 (5,354 bytes,
  `51d6fb3a…`), and no other text was
  extracted from.
- **F056-C06** (execution stops before any
  extraction pass if an input hash mismatches):
  HELD — the gates ran in order before any
  pass; all passed (the claim record in its
  frozen Spec 038 form), so no step-0 closure
  arose.
- **F056-C07** (re-extraction is two
  independent passes over the pinned passage
  only): HELD — Pass A and Pass B, the union
  set, reconciliation by quotation, in the
  extraction record; neither pass consulted
  the claim record's adopted explanation, the
  design packet, or any corpus result while
  extracting.
- **F056-C08** (a candidate is a recovered
  claim only under the §5 test): HELD — the
  conjunctive test was applied as written;
  K-1's failure at one condition (R-3) is
  dispositive, and no candidate was recovered
  on a partial pass.
- **F056-C09** (a candidate's subject is
  identified only if the list is named from
  the document itself and the drawn sign is
  identified by an allowed route): FIRED —
  the list was named from the document
  (Wells's own, Wells 2011, Ch. 2 / Fig. 2.6)
  and the drawn sign could not be identified
  by either route, closing the run as
  IDENTIFICATION FAILED with the reason
  named; the `Yunmapped_0821` trap was
  asserted as a trap and never used.
- **F056-C10** (the headline outcome is
  assigned by §6's mapping alone): HELD —
  the wording is §6.1's IDENTIFICATION FAILED
  form, filled from the run, and no outcome
  word outside §6 was used.
- **F056-C11** (a recovered claim enters at
  created, untested, with a designed-never-run
  test note): NOT REACHED — no claim was
  recovered, so no restatement, lifecycle
  entry, or test-design note arises.
- **F056-C12** (on RETIREMENT RECOMMENDED,
  execution writes exactly §7's entries): NOT
  REACHED — no retirement was recommended and
  no disposition entry was written; the
  fragment is not retired.
- **F056-C13** (every product carries the §8
  reporting set): HELD — passage identified
  in full (§1), both sheets and the
  reconciliation in full (extraction record),
  per-candidate checklists with failing
  conditions named (§5), the §6.1 headline
  wording (§1), and the fence sentence (§1).
- **F056-C14** (no outcome establishes
  anything about sign 821): HELD — see §6 of
  this record.
- **F056-C15** (Spec 056 appends records
  only): HELD — the §7 closure append was
  made to the fragment's own record as a new
  `spec056_closure` entry (Phase-418,
  2026-10-21, the §6.1 wording, the gap, and
  the unblocking act); verification at the
  act: removing the appended entry reproduces
  the pre-act file byte-identically, and the
  claim's status and stage are unchanged. The
  Phase-104 evaluation and the lane-2 adopted
  explanation were not edited, and nothing
  was deleted.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 8. Records

- Evidence: `specs/056-sign821-recovery/extraction-record.md`
  (dry-run, both sheets, reconciliation, R-3
  record); results record:
  `reports/phase418_results.json`; report:
  `reports/phase418_recovery_report.md`.
- Claim closure append: `spec056_closure`
  entry on the fragment's record (see
  F056-C15 above).
- Root LEDGER entry: "Spec 056 (Phase-418)"
  entry added with this record.
- No further program act is outstanding under
  this spec: the §7 form for IDENTIFICATION
  FAILED (outcome record, closure entry,
  LEDGER entry, graph node) is complete in
  this delivery. The unblocking act named in
  §5 is a future act outside this spec, not
  an outstanding step of it.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges, in the Spec 039 completion pattern —
  this section is completed by append, not
  edited.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
