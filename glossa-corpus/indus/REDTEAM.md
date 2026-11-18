# REDTEAM.md — Independent red-team pass on the Indus paper v11 draft of record

Date: 2026-11-18. Reviewer: independent red-team pass (this report only;
no draft file was edited, nothing published).

**Draft under review:**
`pierson_2026_indus_decipherment_v11_formatted_deref.tex`,
SHA-256 `09ef1236adcc46aa820dc45c6f2ac7131401993813ec2df55a775f69af0acfd4`
(hash re-verified at the start of this pass), and its build
`pierson_2026_indus_decipherment_preprint_v11_formatted_deref_DRAFT.pdf`,
SHA-256 `27f108b6c1b2cd972a26b1f1de7e24f05038aa63c342656ac6e5ab05cfcf00ec`
(re-verified).

**Method.** Every number in the changed §5 text was re-derived from the
filed records, not from AUDIT.md's summary: the T302 and T303
reclassification acts and the WP5 support audit were read from the repo
BitConcepts/glossa-lab on main (the working copies in `records/` are
byte-identical to the repo files — git blob SHAs `999706bf…` and
`292a5235…` match); the Spec 095 identifiability application and the
Stage 2 locator supplement record were read in full. All four OSF
registrations and the Zenodo concept DOI were live-checked. All 20 kept
`\texttt` paths were checked against the public repo. A full-text diff
of the v10 deposit PDF against the draft PDF was run and every numeric
or verdict-bearing change hunk inspected. 59+ de-referencing
replacements were individually checked against the v10 source in
context (9 public-pointer, 25+ description, 25+ removal), on top of the
full-text diff over all 250. An independent residue scan was run over
the draft's prose.

**Counts: BLOCKER 1 · SHOULD-FIX 5 · NOTE 7.** The single blocker is
in the accompanying version note, not in the paper text; the paper
text itself carries no blocker.

---

## BLOCKER

### B1 — The version note misdescribes the draft of record

`v11_version_note_DRAFT.md` was written for the earlier unformatted
v11 draft and never updated for the reformat and de-referencing. As it
stands it would be deposited alongside v11 (every version in the
Zenodo chain carries its note) and it misstates the version in four
ways:

1. **It affirmatively denies the naming change.** The note says: "The
   deposited text's own internal study names are untouched; every
   sentence v11 adds or rewrites is free of them. Whether a
   de-referencing pass should be run over the paper itself is flagged
   in the audit as an open question for the owner." For the draft of
   record this is false: on the owner's order the pass was run — 250
   replacements (DEREF-MAP.md) — and the reformat is nowhere mentioned
   in the note. A deposit note that states the opposite of the
   version's most visible change falsifies the deposit's provenance
   record.
2. **Wrong source identity.** The note identifies the draft source as
   `pierson_2026_indus_decipherment_v11.tex`, SHA-256 `42ed3cbd…` —
   the unformatted draft. The draft of record is
   `pierson_2026_indus_decipherment_v11_formatted_deref.tex`,
   SHA-256 `09ef1236…`.
3. **Wrong build facts.** The note's build section reports 35 pages
   and PDF SHA-256 `e7e118b7…` (the unformatted build). The draft of
   record builds to 40 pages, PDF SHA-256 `27f108b6…`.
4. **Wrong word count.** The note reports 22,263, measured on the
   unformatted build; the draft of record measures 22,357 (see S1).

**Fix (exact):** rewrite the note's Status, Scope, and Build
verification sections for the formatted + de-referenced draft of
record before any deposit: state that v11 (a) carries the two §5
corrections, (b) is re-typeset in the program's RCPH paper format
(FORMAT.md), and (c) has had every internal study name replaced by a
public identifier or a plain-language description, with the full
mapping filed as DEREF-MAP.md (250 replacements; the kept `\texttt`
repo paths are public locators); give the draft source as
`pierson_2026_indus_decipherment_v11_formatted_deref.tex`,
SHA-256 `09ef1236adcc46aa820dc45c6f2ac7131401993813ec2df55a775f69af0acfd4`;
the build as 40 pages, PDF SHA-256
`27f108b6c1b2cd972a26b1f1de7e24f05038aa63c342656ac6e5ab05cfcf00ec`;
and the word count as re-measured on that build (S1). Delete the
sentence "The deposited text's own internal study names are
untouched…" and the open-question framing of the de-referencing pass.

---

## SHOULD-FIX

### S1 — The printed word count is wrong for this build (§end matter, line 1197)

The draft prints "Word count: 22,263". Measured on the draft's own
PDF by the version note's stated method (`pdftotext | wc -w`), the
draft of record has **22,357** words. 22,263 is the measured count of
the earlier unformatted v11 build (verified: that PDF measures
exactly 22,263; the formatted build measures 22,304). The figure was
carried through both transforms without re-measurement, and it breaks
the paper's own standard that the printed figure equals the measured
figure on the final build.
**Fix:** replace `\emph{Word count: 22,263}` with
`\emph{Word count: 22,357}`. (The count line is one token either way,
so the figure is stable once corrected.)

### S2 — Dangling "§8" pointer (§2.1.1, line 174)

The text reads: "this paper gives no §8 entry and no fuller
bibliographic identification for the Dering Roll source, the
Mesopotamian numerical-sign table, or DAMOS…". In v10 the References
were §8, so the pointer worked. In the reformatted draft the
bibliography is an unnumbered `thebibliography` after §7 and the
appendices; **no §8 exists**. A reader sent to §8 finds nothing. This
is a reformat side-effect both transforms missed.
**Fix:** replace "this paper gives no §8 entry and no fuller
bibliographic identification" with "this paper gives no bibliography
entry and no fuller bibliographic identification". (All other §
pointers in the paper were checked against the built numbering —
§§2.1.1, 2.2, 2.4, 3.2, 3.3, 3.5, 3.10, 3.14, 3.17–3.19, 3.21–3.24,
3.27, 3.29–3.31.1, 4.4, 5, 6 — and all resolve.)

### S3 — The chronology-note rewrite substitutes a different study (§2.1.1, line 174; DEREF-MAP row 20)

v10's note exemplified the continued sequence with two executions:
"Spec 068 was executed as Phase-430, and Spec 071 as Phase-434". The
rewrite names "the frequency-curve test of §2.1.1 and the
depicted-kinds test of §3.31.1". The first is a faithful
de-reference of Spec 068 (Phase-430; §2.1.1 verified). The second is
not a de-reference of Spec 071 at all: the depicted-kinds test is
Spec 075, executed as Phase-441 — a different study, silently
substituted for the original's second exemplar. The printed sentence
is true (both named tests were executed later in the sequence, and
both section pointers are correct against the built numbering), so
this is not a false statement in the paper; but the transform
changed content beyond de-referencing, and DEREF-MAP's judgment note
("The facts … are preserved") is inaccurate for this item — the
Spec 071 / Phase-434 fact is not preserved, a different fact stands
in its place. The paper nowhere describes Spec 071's study in words,
so no faithful description-route replacement exists for it.
**Fix:** replace "(the frequency-curve test of §2.1.1 and the
depicted-kinds test of §3.31.1 were both executed later in it)" with
"(the frequency-curve test of §2.1.1, for example, was executed
later in it)". This keeps the one exemplar that faithfully
de-references the original and drops the other without substitution.

### S4 — Two bare internal file names survive in prose (§2.1, line 153; Appendix C, line 1188)

The de-referencing pass's residual scan covered id patterns but not
bare file names. Two remain in reader-facing prose, both inherited
from v10:

- §2.1: "(mahadevan\_parpola\_crosswalk.json)" — no path, not set as
  a locator. §3.5 cites the same file properly, with its full path in
  `\texttt`. **Fix:** replace "(mahadevan\_parpola\_crosswalk.json)"
  with "(\texttt{research/indus/mahadevan\_parpola\_crosswalk.json})",
  matching §3.5's form.
- Appendix C: "Internal consistency suite (foundation\_check.py)" —
  an internal script name as the suite's identity. The file exists in
  the public repo at `backend/scripts/foundation_check.py`
  (verified). **Fix:** replace "(foundation\_check.py)" with
  "(\texttt{backend/scripts/foundation\_check.py})".

### S5 — The draft's own identity pointers dangle (title page, line 37; §6, line 986)

The title page states the draft's exact text "is identified by the
SHA-256 of its source, recorded in the build record
(\texttt{build/build\_record.md} in the deposit package; see §6)".
No file named `build_record.md` exists anywhere in the working
directory or the draft's build folders. §6 instead says the SHA is
"recorded in its version note" — and the version note's printed SHA
identifies the earlier unformatted draft, not this one (B1). A reader
who tries to identify this exact text from either pointer fails.
**Fix (in the fix round, with B1):** either create
`build/build_record.md` in the deposit package carrying this draft's
SHA-256 (`09ef1236…`), or change the title-page sentence to point at
the version note and correct the note's SHA per B1. One pointer, one
hash, identifying this file.

---

## NOTES

### N1 — Owner-ordered items, not graded as findings (recorded so the fix round and this report agree)

- **Identity block (lines 28–29).** The draft still reads
  "Glossa-Lab / BitConcepts LLC" with correspondence
  tpierson@bitconcepts.tech. Per the owner's migration order this
  changes in the fix round to "Glossa-Lab / Axiovex Systems, LLC"
  and research@axiovexsystems.com, matching the RCPH paper. Not
  graded.
- **§6 GitHub URLs.** At the time of this pass's verification the
  repository lived at github.com/BitConcepts/glossa-lab and all
  URLs and `\texttt` paths were verified resolving there. The owner
  has since executed the repository transfer (2026-11-18):
  BitConcepts/glossa-lab is now AXIOVEX/glossa-lab (old address
  redirects; verified via the API). Accordingly the fix round DOES
  update the §6 repository URLs to
  https://github.com/AXIOVEX/glossa-lab. Not graded; the path
  verifications in this report hold under the new address via the
  redirect.
- **The head-note block (line 40)** is being removed in the fix
  round on the owner's instruction; its wording is not graded. §5's
  pointer "(see the note at the head of this paper)" must be
  adjusted in the same motion or it dangles — the owner order states
  it will be. See N2 for the self-sufficiency check.

### N2 — §5 is self-sufficient without the head note, with two reader losses to close in the replacement sentence

Checked line by line: §5's qualification paragraph and
identifiability paragraph carry the full audit picture on their own
— the October 2026 audit and its re-grading, all five counts, both
revalidation legs with their outcomes, the unrun etymological leg,
the four remaining readings named, the located passages for M087 and
M311, the "not a re-grading of the 161 / falsifies nothing" caveat,
and the identifiability outcome at record strength. Everything else
in the note is covered elsewhere: the SA falsification in §2.4, the
undeciphered position in the abstract and §5's closing, the
161-as-record-of-that-set point in §5's "not a re-grading" sentence.
Two items in the note are **not** carried anywhere else and a reader
loses them when the note goes:

1. **The strict-core definition.** The note is the only place the
   paper says what the 94 are: readings "whose recorded history never
   passed through the program's original syllabic language-model (SA)
   simulation". §5 uses "the program's strict core" without defining
   it, and no other section defines the set. Recommend the owner's
   replacement front-matter sentence (or §5's first mention) carry
   the clause: "the 94 readings of the strict core — the readings
   whose recorded history never passed through the program's original
   syllabic language-model simulation".
2. **The qualification's reach over the title and abstract.** §5
   qualifies the conclusion's own Tier 2 sentence ("as used above of
   the 161"); the note additionally instructed that the headline
   figures be read at that strength "wherever they appear — in the
   title, in the abstract, and in the conclusion". The planned
   replacement sentence (the title's 161 are the set the paper
   reports on; the program's current candidate set is the 94 strict
   core, summarized in §5) carries the essential fact at the front of
   the paper and adequately covers this; no further change needed if
   that sentence lands as described.

### N3 — Other process notes of the head-note genre (keep/remove)

- **Title-page DOI/SHA block (lines 36–38).** Author bookkeeping
  about identifying the draft. At deposit the §6 pin supersedes it.
  **Remove at deposit** (and fix its pointer per S5 while the draft
  circulates).
- **§6 deposit-pin procedure (line 986, the long paragraph on named
  commits and pin commits).** Assessed on whether a reader needs it
  to verify the text: a reader needs the *named commit* — one
  sentence, the form v10 used — not the mechanics of how the pin
  commit is constructed. The procedure is instructions to the
  deposit process. **Remove the procedural detail from the paper at
  deposit; keep the procedure in the version note, and keep in §6
  only the sentence naming the frozen revision commit once it
  exists.**
- **§6 draft-provenance paragraph ("This version of the paper is a
  draft: it was prepared from the deposited v10 text…").** Draft
  status bookkeeping. **Keep while the text circulates as a draft**
  (it is the honest status of this artifact); it disappears by
  construction at deposit, replaced by the pin sentence.
- **§2.1.1 "Two identification notes belong on the record" paragraph.**
  Provenance-flavoured, but its content is stated limits a reader
  needs (where the test's inputs are identified; what the paper does
  not identify). **Keep** (with S2's fix).
- **The chronology note (end of §2.1.1).** After de-referencing, its
  remaining content — a numbered study sequence ran to 170 and
  continued — is process history no reader needs. **Remove at
  deposit**, or keep only as shrunk by S3's fix; either is defensible,
  removal is cleaner under the owner's stated preference.
- **Appendix C provenance framing** ("recorded here as provenance,
  not as the current result"). Stated-strength substance, not
  process. **Keep.**
- **"Version: Preprint v11 (draft, not yet deposited) — Not
  peer-reviewed" line and the AI Disclosure.** Reader-facing status.
  **Keep.**

### N4 — One loose gloss in §3.30 (DEREF-MAP row 69)

v10: "Updated Phase-141 evidence scorecard incorporating Phases
142–168." Draft: "The updated evidence scorecard, incorporating
every study since the first scorecard." "Every study since" is
unbounded — read literally it claims incorporation of studies after
the scorecard's own span as well. The governing content (the 32-item
tally that follows) is unchanged, so this is imprecision at the
margin, not a changed claim. **Proposed replacement:** "The updated
evidence scorecard, incorporating the studies that followed the
first scorecard."

### N5 — The withheld-study paragraph (§3.5): the de-reference is compliant; the surrounding text is v10's permitted form

The replacement "(the study is held from publication)" was verified
as the *only* change the de-referencing made to that paragraph: it
neither names the study (no Spec 072, no Phase-431) nor describes it
beyond its held status. Flagged for the owner's awareness, not as a
draft defect: the surrounding paragraph is v10's deposited text,
which describes the study's design in some detail (a registered test
of the fish family on a separate corpus, contract/family list/pass
line frozen in advance, two list members unidentifiable and one below
the counting floor — the last expressly framed as dispositions of the
frozen record, "not of its results", with no result stated in either
direction). AUDIT.md (row 27) records this paragraph as the program's
permitted form, and the audit cleared it as still accurate. A strict
"named only as executed — held" reading sits in tension with the
design detail; whether to trim the deposited wording is an owner
decision outside the v11 corrections, and this pass takes no position
beyond flagging it.

### N6 — `\label` slugs retain spec/phase strings

Labels such as `…-spec-052`, `master-evidence-synthesis-phase-169`
still carry the internal names (DEREF-MAP class decision 4). They
are never rendered, and the paper's cross-references are manual §
numbers, so there is zero reader impact. Leave them, or strip them
at deposit production; not a deposit consideration either way.

### N7 — The paraphrased verdict label (§3.17; DEREF-MAP row 131)

"where the recorded verdict is V12\_ACTIVE\_CONCERN" → "where the
recorded verdict flags an active concern". Verified: the label's
entire content is carried in words; nothing is dropped or softened
(the same passage keeps the pass-rate disagreement and the
"unresolved" statements). The one non-verbatim label in the pass,
and it is faithful. No action.

---

## Verified clean (the affirmative checks behind the verdict)

- **§5 numbers, re-derived from the acts.** T302 acts (run
  study-20261117T103816Z-a25969): 28 acts, 19 →
  supported_internal_only, 9 → insufficient_evidence; the 9 are
  M012, M039, M059, M077, M162, M233, M305, M328, M336 — the draft's
  list exactly, including all three default-only promotions; the
  evidence-retirement act covers all 28. T303 acts (run
  study-20261118T151605Z-4c5c8b): M042, M046, M108 →
  insufficient_evidence on insufficient_data (no statistic computed);
  M176 χ² = 22.8589, df 14, p = 0.06261 → printed 0.063 ✓; M342
  χ² = 25.2468, df 16, p = 0.06559 → printed 0.066 ✓; both
  difference_not_detected → insufficient_evidence, matching
  GR-088-03 candidate 2's falsifier. WP5 baseline 6 / 46 / 37 / 3 / 2
  with expert-pending M222, M362, M398 (the draft's three ✓).
  Arithmetic: 46 + 19 = 65 internal-only; 2 + 9 + 5 = 16
  insufficient; 37 − 33 = 4 still requiring revalidation (M087,
  M165, M264, M311 — GR-088-03's R5d four, "comparison-table or
  literature import" ✓); 6 + 65 = **71 of 94 supported at all**;
  94 − 71 = 23 remaining. Every §5 count and sign list matches.
- **§5's "dual line" clause.** "on a recorded dual line of support
  from outside this program that the audit took as recorded without
  re-verifying it against the primary publications" — the WP5 record
  for each of the six (rule R3_dual_external_corroboration) states
  verbatim that the status "credits the corroboration line as
  recorded; it does not re-verify the comparanda against their
  primary publications." Faithful.
- **Identifiability paragraph.** Checked sentence by sentence against
  the Spec 095 Stage 3 application record: all six NOT IDENTIFIABLE;
  the standard as stated (an observation the reading fits and the
  rivals do not) matches the protocol; the rival gloss ("a rival
  value of the same shape, or the sign carrying no phonetic value at
  all") matches the record's rival constructions; M047 — meaning
  'fish' discriminated ("observations a rival meaning must also
  explain"), value follows "only by the rebus assumption" (the
  record's own words); M202 — the sibilant class discriminated by the
  Shu-ilishu slot, the value not; "does not disprove any of the six"
  and dispositions unchanged, both as the record states. Nothing
  stronger, nothing weaker.
- **Locator census.** Supplement record §3: phonetic 9 located /
  175 not-found; semantic 0 / 184. The nine: M047, M087, M088, M091,
  M092, M175, M261, M281, M311. The draft's §5 statement (passages
  located for M087 and M311, of the four still requiring
  revalidation) is exact — M165 and M264 are not among the nine.
- **Public pointers, live-checked 2026-11-18.** OSF 3pbwe = the
  frequency-curve (Zipf–Mandelbrot) frozen contract → §2.1.1 ✓;
  7cu23 = the Farmer-pattern battery → §3.2.1 ✓; cfe7z = the
  animal-openings hunt → §3.8.1 ✓; jv74f = the depicted-kind endings
  atlas → §3.31.1 ✓. Each registration's title matches the study the
  text assigns it to. The title-page concept DOI
  10.5281/zenodo.20379070 resolves to this paper's Zenodo chain.
- **Kept `\texttt` paths.** All 20 resolve in the public repo,
  including `specs/068-yadav-zipf-controls-successor/outcome.md`,
  the exact file §2.1.1 points to. (Four directory paths initially
  returned "not found" from the contents API; the specs/ listing and
  file-level checks prove all four exist — an API quirk, recorded
  here so the fix round does not chase it.)
- **No strengthening anywhere else.** Full-text diff, v10 deposit vs
  draft: the title is identical; the abstract's changes are only the
  catalogued de-references; every numeric or verdict-bearing change
  in the body is accounted for by the §5 rewrite, the version
  mechanics, the bibliography's bullet-to-number conversion, or a
  DEREF-MAP row. The F3/F12 glosses ("phonological-profile
  comparison", "language-model comparison") match the paper's own
  §4.4 vocabulary and the falsification-suite script's definitions
  (F3: HIGH-anchor exclusivity language fit; F12: Sanskrit A/B LM
  comparison at 157 anchors). §5's "M342, the most frequent terminal
  in the corpus" is supported by the paper's own §3.2 ("most frequent
  terminal at 584").
- **Integrity.** The standing position is intact and unhedged in the
  wrong direction (abstract: the script "remains undeciphered"; §5
  closing unchanged from v10). Build log: 0 errors, no undefined
  references or citations. Bibliography: 35 items, complete and
  numbered, consistent with the in-text author–date citations.
- **Residue scan (independent).** Over the draft's prose (excluding
  `\texttt` locators and `\label` slugs): Phase-NNN 0, Spec NNN 0,
  F/V/S/E/L ids 0 (the single "F6" hit is the published book title
  *Tell F6 on Failaka Island*), "Asset" labels 0, WP/GR/claim/task/
  run/PR ids 0. The only residue found is S4's two bare file names.

**Divergences between notices and records:** none encountered. Every
figure relied on above was read from its filed record or live-checked;
the two initial API "not found" results for repo directories were
resolved against the directory listing before any conclusion was
drawn (see "Kept \texttt paths").

---

## Verdict

**NOT READY** — one blocker: **B1** (the version note misdescribes
the draft of record, including affirmatively denying the naming
change the draft embodies). The paper text itself carries no
blocker; with B1 rewritten and the five SHOULD-FIX items (S1–S5)
applied in the already-planned fix round, the draft is deposit-ready
on this pass's evidence.
