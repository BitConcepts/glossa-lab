# Spec 056 / Phase-418 — Extraction record (EXECUTED 2026-10-21)

> The evidence of the execution: the dry-run
> (DD-056-16), both extraction sheets and the
> reconciliation (spec §4), and the recovery-test
> record (spec §5) over the reconciled candidate
> set. The outcome record is `outcome.md` in this
> directory; the run's machine record is
> `reports/phase418_results.json` (SHA-256
> `f6b8c97b3b95ed3176f10994cbf109de1ff451fc1f11e2f7cf68ca5ca8b7c513`),
> produced by `backend/scripts/phase418_sign821_recovery.py`,
> which verified every quote on these sheets
> verbatim against the pinned passage before any
> outcome was written; a second run reproduced
> both machine outputs byte-identically.

## 1. The passage of record (spec §8, element 1)

- **Document:** Bryan K. Wells, *The Archaeology
  and Epigraphy of Indus Writing* (Archaeopress,
  2015), as held by the program in cleaned text:
  `glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`,
  SHA-256
  `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e`.
- **Start anchor:** the line consisting solely of
  `The Dholavira signboard, revisited`
  (cleaned-text line 2783; unique as a standalone
  line).
- **End anchor:** the next line consisting solely
  of `The Mohenjo-daro bangle pot` (cleaned-text
  line 2872; unique as a standalone line).
- **Passage:** cleaned-text lines 2783–2871
  inclusive, printed pp. 90–94; 5,354 bytes;
  SHA-256
  `51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604`.
- **Anchor sentence (verbatim):** "Whatever sign
  821 reads it is used in a variety of contexts
  (Figure 6.13)." — printed p. 93; occurrence
  count 1 in the document.
- **The limit of the held text, stated wherever
  this outcome is stated:** the cleaned text
  drops the book's sign glyphs (sentences contain
  blank slots where glyphs stood) and Figure
  6.13 itself is a graphic, present only as its
  caption ("Figure 6.13. Examples of the various
  contexts of sign 821.", cleaned-text line
  2860). Anything carried only by the figure's
  images is outside the passage of record
  (DD-056-13).

## 2. Step 0 — the gate record (spec §3; all passed)

- **0.1 Input integrity — PASS.** Held text
  `62acf855…`, Phase-104 evaluation `2d0b83e8…`,
  lane-2 drafts `3f645c9a…`, crosswalk registry
  `8a0b2a82…`, anchors `df0cf620…` — each
  recomputed at the run's base (`main` at
  `3200b7b5`) by two independent routes (the
  isolated worktree and the GitHub contents API,
  identical results) and each equal to its
  freeze pin. The claim record was asserted in
  the freeze's Spec 038 form (freeze.md §2): its
  freeze-time hash `bd0f7abd…` stands as the
  definition constant in `freeze.json`, and the
  fragment's facts were asserted on the live
  file — entry present, `normalized_claim`
  "Sign value: 821 / it is used in a variety of
  contexts (Figure 6", `claim_status` untested,
  `stage` created, the source passage named in
  its not-understood text. The live file's whole
  hash differs from the constant for one
  recorded reason only: Spec 046's execution
  appended its `first_check` entry to the
  _0002 claim in the same file (PR #263);
  the _0001 fragment entry is unchanged from
  the pinned bytes (verified field-for-field at
  this run).
- **0.2 Passage producible — PASS.** Both anchor
  lines located as standalone lines exactly
  once each; the anchor sentence located
  verbatim, occurrence count 1.
- **0.3 Passage pinnable — PASS.** The slice
  recomputed to 5,354 bytes, SHA-256
  `51d6fb3a…` — the freeze-pinned digest.

## 3. Dry-run of the machinery (DD-056-16)

Required before the protocol touches the
fragment: a worked dry-run of the §§4–5 sheet
and checklist machinery on a passage other than
the passage of record. Passage used: Wells
2015, "The Mohenjo-daro bangle pot"
(cleaned-text lines 2872–2931, the headed
section immediately following the passage of
record).

- **Candidate proposition (dry-run only):**
  sign 575 is likely a logograph representing a
  kiln (cullai), so sign 740 beside it is not
  needed as a phonetic complement.
- **Verbatim quote:** "As sign 575 is likely a
  logograph representing a kiln, the use of 740
  as a phonetic complement is redundant and
  wasteful of space in a medium in which space
  is precious." (cleaned-text lines 2925–2926;
  verified verbatim by the phase script.)
- **Checklist machinery, exercised in form:**
  R-1 — the proposition is asserted in the
  passage's own words. R-2 — a specific
  contention (a logograph value for 575 in this
  context). R-3 — route fields recorded; no
  identification attempted or needed for a
  machinery proof. R-4 — a condition is
  statable in form (575's contexts shown to
  carry a single non-kiln value); not
  adjudicated. R-5 — the passage's stated hedge
  ("likely") and its space rationale carried
  with the proposition.
- **Output:** none. The dry-run produces no
  candidate and no outcome for the fragment; it
  proves the sheet and checklist machinery
  before that machinery touches the passage of
  record.

## 4. Pass A — extraction sheet

*Method: a sequential reading of the pinned
passage in order, enumerating every candidate
proposition the passage asserts or argues about
sign 821, in passage order. The pass read only
the pinned passage and spec §5.*

**Candidate K-1 (decisive).**
Proposition, in the pass's own words: sign 821,
in the Dholavira signboard contexts, has a
meaning of ‘city’, either as a determinative or
as a word; of the passage's candidate glosses
(DED 752 ūr; DED 808 eyil; DED 3568 nakar;
DED 4112 pāri), eyil is the best choice,
because Dholavira is a walled city made of cut
stone.
Verbatim quotes:

> "It is suggested here that sign 821, in the
> Dholavira signboard contexts, has a meaning
> of ‘city’, either as a determinative or as a
> word." (cleaned-text lines 2835–2836;
> printed p. 92)

> "752 Ta. ūr village, town, city. 808 Ta. eyil
> fortress, wall, fortification, city, town
> 3568 Ta. nakar house, abode, mansion, temple,
> palace, town, city. 4112 Ta. pāri temple;
> town, city, town of an agricultural tract,
> hermitage;" (lines 2842–2845; printed p. 93)

> "Any of these is possible. Which of these, if
> any, are the correct gloss cannot be known,
> but eyil seems the best choice given the fact
> that Dholavira is a walled city made of cut
> stone." (lines 2846–2847; printed p. 93)

Supporting premise, quoted because the R-4
condition is derived from it:

> "I have posited (Wells 2011) that some part
> of this sign sequence would be the site’s
> locative (place name)." (lines 2794–2795;
> printed p. 91)

Checklist (spec §5): **R-1 PASS** — the
proposition is the passage's own suggestion,
stated in its own words; not a topic mention,
not the figure, not the bare fragment
restated. **R-2 PASS** — a specific
contention: a stated reading (‘city’,
determinative or word) in a stated context
(the Dholavira signboard contexts), of exactly
the kind §5 names ("a specific classification
or reading in a stated context"); a contrary
finding — 821 shown to carry another value in
those contexts — could oppose it. **R-3** —
run at step 2 (see §7 of this record).
**R-4 PASS** — falsification condition,
stated from the passage's own logic: "The
claim counts as falsified if sign 821 in
Dholavira signboard contexts is shown to carry
a different established value, or if the
signboard sequence's locative (place-name)
element is shown to be carried by other signs,
with sign 821 outside it — either result
removes the basis the passage itself states
for the ‘city’ suggestion. The passage rules
one observation out as a falsifier in its own
words: the non-attestation of eyil-ay or
eyil-i (collocation with sign 740) is
expressly ‘not a nullification of the
reading’, so that absence cannot serve as the
condition." **R-5 PASS** — the passage's
stated conditions are carried with the
contention: the context bound, the
determinative-or-word alternative, all four
candidate glosses with their DED numbers, the
eyil preference with its stated reason, and
the passage's own hedge that no firm reading
exists and the correct gloss cannot be known.

**Candidate K-2.** Considered and not credited
as a candidate about sign 821: the Fuls
paragraph, framed as a verification of the 821
‘city’ reading, whose asserted content
concerns sign 861.
Verbatim quote:

> "One verification of the sign 821 reading as
> ‘city’ has been pointed out by Andreas Fuls
> (pers. com. 2011; Figure 6.12). He notes
> that the sign combination of 861+740 matches
> the imagery of a cow (740=*ay=’cow’) and the
> person in front of a structure, which may be
> a pictographic toponym (861 = city), seem to
> fit the readings developed so far. This
> evidence does not bring us any closer to a
> reading for sign 861, but does reinforce the
> association of this sign with important
> places." (lines 2848–2853; printed p. 93)

Checklist: **R-1 FAIL** — the sentences assert
a proposition about sign 861 (the 861+740
combination as a pictographic toponym, ‘cow at
the city’, and 861's association with
important places). The head clause frames the
paragraph as a verification of the 821
reading, but a framing clause is not a
proposition about 821 argued from evidence
about 821; crediting it would assemble a
candidate about one sign from another sign's
evidence. The paragraph is supporting context
for K-1's narrative, not a candidate.
R-2…R-5 not reached.

**Candidate K-3.** The bare fragment restated:
sign 821 is used in a variety of contexts.
Verbatim quote (the anchor sentence, lines
2854–2856; printed p. 93): "Whatever sign 821
reads it is used in a variety of contexts
(Figure 6.13). While eyil-ay or eyil-i (i.e.
collocating with sign 740) is not attested,
this is not a nullification of the reading, as
we really do not have a firm reading for sign
821."
Checklist: **R-1 FAIL** — §5 rules this in
advance: the restated fragment is not a
recovery. **R-2 FAIL** — no contention a
contrary finding could oppose; the
observation is true of almost any common
sign, and the passage draws no contention
from it (Figure 6.13, which it cites, is
graphic-only in the held text). **R-4 FAIL**
— no falsification condition can be written
for it from the passage's own logic without
inventing one. R-3, R-5 not reached.

**Candidate K-4.** Considered as a standalone
candidate: eyil-ay or eyil-i (sign 821
collocating with sign 740) is not attested.
Verbatim quote: the anchor-sentence passage
above (lines 2854–2856; printed p. 93).
Checklist: **R-1 PASS in the narrow sense** —
the passage does assert the non-attestation.
**R-2 FAIL** — a catalogue observation (an
absence in the attestation record) from which
the passage draws no contention about sign
821; the only point the passage draws from it
is defensive — that it does not nullify K-1.
Its content is carried into K-1's record
under R-5 and into K-1's R-4 condition, where
it belongs. R-3…R-5 not reached.

**Not candidates (agreed scope notes):** the
sign-pair suggestion "One possible meaning of
this sign pair is ‘copper/bronze tool’" (lines
2824–2831) is about the toponym sign pair, not
sign 821; the toponym-sequence observations
(the sequence "repeated on 5 artifacts", lines
2794–2815) are about the sequence, not 821 —
the locative premise among them is carried as
K-1's premise quote; the discussion of the
final sign, 798 (lines 2857–2871), is about a
different sign.

## 5. Pass B — extraction sheet

*Method: an independent second reading,
mention-driven: every "821" mention inside
the passage was worked outward to the
proposition it carries, followed by a sweep
for propositions about 821 carried without
the number (by "this sign" and similar
references). The pass read only the pinned
passage and spec §5.*

Mentions worked: line 2835 (the ‘city’
suggestion), line 2848 (the Fuls verification
head clause), lines 2854 and 2856 (the anchor
sentence and the "no firm reading" clause),
line 2860 (the Figure 6.13 caption — a
caption, asserting nothing). The sweep found
no further proposition about 821: the "this
sign" references at lines 2868–2871 are to
sign 798, and the sign-pair discussion's
references are to the toponym pair.

Candidates found: **K-1, K-2, K-3, K-4 — the
same set as Pass A**, with the same quotes,
the same propositions, and the same checklist
results on every line, including K-1's R-4
condition in the same words (each pass
derived it from the same quoted premise and
the same quoted exclusion). Pass B's sheet
records one emphasis of its own: on K-2, the
pass notes the paragraph's final clause —
"does reinforce the association of this sign
with important places" — has "this sign"
referring to 861 (the subject of its own
sentence), so reading it as a claim about 821
would misattribute the reference as well as
the evidence; the R-1 failure stands on both
grounds.

## 6. Reconciliation (spec §4.3)

The candidate set of record is the union of
the two sheets: **{K-1, K-2, K-3, K-4}**. The
passes agree on the set and on every checklist
line; no disagreement arose on any candidate,
settled or unsettled — in particular not on
the decisive candidate K-1, whose R-1, R-2,
R-4 and R-5 results are identical on both
sheets and rest on the quotations recorded
with it. Had a disagreement on K-1 remained
unsettled after quotation, K-1 would have
been treated as not recovered (DD-056-14);
that rule was not needed. Both sheets are
deliverables of this execution and stand
above in full.

## 7. Step 2 — the R-3 identification record

R-3 runs for K-1, the one candidate that
reaches it. R-3 has two halves.

**The sign list, named from the document
itself — SATISFIED.** The book's apparatus
names the list its numbering belongs to:
"Chapter 2 gives the Indus sign list used in
this analysis" (held text, line 414); "The
sign list used here (Wells 2011) was
constructed using a uniform method" (line
665); Chapter 2 is headed "The Indus Sign
List" and its Figure 2.6 is captioned "An
Indus Sign List" (printed pp. 19–22). The
list is **Wells's own sign list (Wells 2011),
as given in Wells 2015, Chapter 2 / Figure
2.6** — the same apparatus finding Spec 046
recorded for its fragment from this book.

**The drawn sign, identified by an allowed
route — NOT SATISFIED, by either route.**

- *Crosswalk registry, by drawn form.* The
  pinned registry (803 rows) carries **no
  W821 value in any row's `wells_ids`** — not
  as a sole value and not inside any
  multi-value cell. No registry entry exists
  for the sign at all, by number or otherwise;
  a drawn-form match has nothing to match
  against, and the held text itself drops the
  glyph (the passage's sign slots stand
  blank), so no drawn form is available to
  match with. No registry description names a
  city (0 of 803). The registry's
  `Yunmapped_0821` row was asserted as the
  frozen trap and not used: its numbering
  system is `yajnadevam_glyphid`, its
  `wells_ids` is empty, its corpus frequency
  is 10 — it is a Yajnadevam glyph identifier,
  not Wells's 821 (§5 R-3). The Phase-123
  Wells segmentation witness (157 rows)
  carries **no Wells grapheme 821**.
- *The source list's own published entry,
  quoted with its locator.* The list's entry
  for sign 821 stands in Figure 2.6 (printed
  pp. 19–22). In the held cleaned text those
  pages carry captions only — "Figure 2.6 An
  Indus Sign List" and its "(Continued)"
  repetitions (held-text lines 868–880) — the
  drawn forms did not survive text extraction,
  so no entry text exists in the held record
  to quote. The appendix's "Doubled Signs"
  text (printed pp. 128–129) states that "sign
  820 doubles to form sign 821" and describes
  821's positional behaviour; it is not the
  sign list's entry for the sign, it carries
  no drawn form, and quoting it would
  identify the sign by number and formation —
  the number-matching §5 forbids as identity.

**R-3 result: FAIL** (identification half).
K-1 therefore passes the argument conditions
R-1, R-2, R-4 and R-5, and fails R-3.

## 8. Final checklists and the outcome mapping

| Candidate | R-1 | R-2 | R-3 | R-4 | R-5 |
|---|---|---|---|---|---|
| K-1 (‘city’ reading, signboard contexts) | PASS | PASS | **FAIL** (identification half) | PASS | PASS |
| K-2 (Fuls paragraph, about 861) | FAIL | — | — | — | — |
| K-3 (fragment restated) | FAIL | FAIL | — | FAIL | — |
| K-4 (non-attestation of eyil-ay/eyil-i) | PASS (narrow) | FAIL | — | — | — |

Spec §6's mapping, applied to exactly these
results: no candidate passes R-1…R-5, so
RECOVERED does not fire; K-1 passes the
argument conditions, so the retirement
wording — which would call an arguing passage
a catalogue observation — cannot fire either;
the run closes as **IDENTIFICATION FAILED**
(DD-056-2, confirmed DD-056-11). The
headline wording, the closure entry, and the
unblocking act are recorded in `outcome.md`.

**Fence sentence (spec §8):** "This act is
record repair. It establishes, at most, what
the source passage argues — never whether the
argument is right, and nothing about sign 821
itself."

**The figure limit, stated with the outcome:**
Figure 6.13 is graphic-only in the held text,
present only as its caption, and the cleaned
text drops the book's sign glyphs; a
contention carried only by the figure's
images or by a dropped glyph is outside the
passage of record and unrecoverable under
this spec (DD-056-13).

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
