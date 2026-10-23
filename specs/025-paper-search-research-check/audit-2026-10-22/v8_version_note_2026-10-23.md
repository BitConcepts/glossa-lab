# Preprint v8 — Version Note (2026-10-23)

**Scope.** Preprint v8 carries exactly four content edits (E1–E4) plus
version mechanics, made on branch `preprint-v8-f2-spec068` off
`origin/main` d20bc1bc. Nothing else in the paper changes. This note
records what changed, why, what was deliberately not changed, and how
the build was verified.

**Standing rule.** No paper publishes without TeX production and an
independent red-team pass. v8 is built with the TeX toolchain (below).
The independent red-team pass on v8 is **IN PROGRESS** under that rule;
its record will be filed in this same audit directory when complete.
This note does not claim it done.

## The changes

### E1 — §2.1: the Zipf sentence qualified in place (F2)

The v7 sentence ("Frequency distribution follows Zipf's law (exponent
~1.7), consistent with a natural language writing system") is replaced.
The sign-catalogue paragraph now says sign frequencies fall off
steeply, records that an earlier version reported a Zipf exponent of
about 1.7 and described it as consistent with a natural language
writing system, and states plainly: that exponent is this program's
own statistic on this corpus; no derivation of it has been published
that a reader can check; and it is no longer presented as evidence
that the script is a language. It cites Yadav et al. (2010) for the
published Zipf–Mandelbrot fit (on a pruned subset of Mahadevan's
corpus) and Yadav's own stated limit — the presence of such a
distribution "is not sufficient to declare a sequence as linguistic" —
and points to the new §2.1.1.

**Why, and the forced branch.** This is audit finding **F2**
(`adversarial_pass_2026-10-22.md`: "exact number without derivation";
verdict SUSTAINED in narrow form). The F2 recommendation offered two
honest options at submission time: add the derivation/fit details for
the exponent, or qualify the sentence in place as the program's own
corpus statistic. The first branch was **not honestly available**: the
only derivation on record, −1.7046 from the Sproat-benchmark script,
belongs to a **different corpus** (7,138 texts / 24,502 tokens / 649
types) than §2.1's Holdat corpus (7,002 sign tokens in the paper's own
description), so attaching that derivation to §2.1's exponent would
have mis-stated what was measured on which corpus. The second branch —
**qualify in place** — was therefore taken. (The §2.1 cross-reference
is written literally as "§2.1.1", matching the paper's existing style
of hard-coded section references such as "§3.6" and "§4.5.2".)

### E2 — New §2.1.1: what a frequency-curve fit can and cannot show (Spec 068)

A new numbered unit, §2.1.1 "What a Frequency-Curve Fit Can and Cannot
Show (Spec 068)", is inserted at the end of §2.1, immediately before
§2.2. (Heading form: the paper typesets every numbered unit under a
`subsection` with `\subsubsection`; §2.1.1 uses `\subsubsection` like
§2.1 and §2.2 — the closest consistent form the file's conventions
offer.)

It reports the Spec 068 test (executed as Phase-430; OSF registration
3pbwe), run under rules fixed and registered before the run. The
Zipf–Mandelbrot fitting rule frozen by Spec 053 was applied to Indus
sign counts from the **Shakti corpus** — a restricted ICIT-lineage
corpus, expressly **not** the Holdat corpus of this paper — 3,045
analysable rows of documented lineage; 11,805 tokens; 557 distinct
signs. Results: exponent α = 2.004, fit error 0.1584 on the
documented-lineage rows; α = 1.96, error 0.1544 on the wider
documented-plus-corroborated row set. The four comparison systems:
Mesopotamian numerical signs (error 0.5335), heraldic charges from the
Dering Roll (0.1839), a synthetic emblem process (median 0.2405), and
Linear B (0.9229). Linear B, the one system in the set that is
certainly writing, fitted the curve **worst** of the five.

**Registered outcome wording: COMPARISON UNINFORMATIVE.** Under the
rule fixed before the run, these measures do not separate the one
certain writing system from systems that are not writing, so a close
Indus fit on them is evidence neither for nor against the script being
language. The section closes by bounding the numbers: the Shakti
numbers measure the Shakti corpus only; they are not a measurement of
the Holdat corpus used in this paper, and they do not confirm or
correct any earlier exponent, including the Phase-43 exponent of about
1.35 recorded in this program's files.

### E3 — §3.10: Nair's Zipf slope qualified the same way

The Nair paragraph's ending gains two sentences: one of Nair's four
measures, his Zipf slope, is a frequency-curve fit of the kind tested
in §2.1.1; on the frozen comparison reported there, that kind of fit
did not separate writing from non-writing, so the paper does not use
his slope — any more than its own earlier figure — as evidence about
linguistic status. The rest of the paragraph (non-random sequential
structure; does not test the positional grammar, the anchor readings,
or the Dravidian hypothesis) is unchanged.

### E4 — §8: Yadav et al. (2010) entry added

One new reference-list entry, placed immediately after the Wells &
Fuls (2015) entry (the placement the commission specified; the list's
local ordering around that point is followed):

Yadav, N., Joglekar, H., Rao, R.P.N., Vahia, M.N., Adhikari, R. &
Mahadevan, I. (2010). Statistical Analysis of the Indus Script Using
n-Grams. *PLoS ONE*, 5(3), e9506. DOI: 10.1371/journal.pone.0009506.

No other §8 entry changed: the two Rao entries and both Roif entries
(2025a, 2025b) are byte-identical to v7, verified in the source diff
and in the rendered PDF.

### Version mechanics

Title block: "Version: Preprint v7" → "Version: Preprint v8". Footer:
"End of Preprint v7" → "End of Preprint v8". The date line already read
"(revised October 2026)" and is unchanged.
`docs/research/PREPRINT_VERSIONING.md` gains the v8 history row and an
updated "Current version" section; the root `AGENTS.md` preprint
fields (Source / PDF / Current version) are updated to v8; a dated
entry is added to `LEDGER.md`.

## What was NOT changed

- Everything else in the paper is carried from v7 intact — every other
  section, number, and reference. In particular the Roif credit in
  §3.5, §3.19, §7, and §8 stands exactly as v7 printed it.
- **§3.32 is still absent.** No betweenness-centrality content was
  inserted or restored; §3 still ends at §3.31. The held restoration
  draft remains held pending Roif's reply, as in v7.
- **Spec 072 is NOT integrated.** The Spec 072 (Phase-431) fish-family
  result does not appear in v8. Its insert paragraph is filed, held
  and internal, at
  `glossa-corpus/indus/pierson_2026_indus_decipherment_spec072_insert_HELD.md`
  (publication requires citation of Roif 2025a and Roif 2025b AND the
  owner's clearance of the specific publication act — claim F072-C14;
  specs/072-fish-family-profiles-redesign/spec.md §7 limit 1).
- **Heras note.** No Heras wording exists in v7 — nothing was preserved
  because nothing was there. Adding any Heras mention is an owner
  decision outside this commission's scope; none was added.
- **§1.2 Rao wording risk (owner-flagged, left unchanged).** The recon
  for this commission flagged a wording risk in the §1.2 treatment of
  the Rao material. It is left exactly as v7 printed it, flagged here
  for the owner's decision; this commission made no change to it.

## Build verification

- Toolchain: TinyTeX XeLaTeX under `~/workspace/tex-tools/` (the same
  toolchain that built v6/v7). No other engine was used. Font lookup
  required environment configuration only: `OSFONTDIR` covering the
  system Noto fonts and the TinyTeX texmf-dist fonts, plus a
  fontconfig file including the system fonts and the TinyTeX
  texmf-dist font directories (the TinyTeX-bundled fontconfig template
  still points at its build machine's home directory). No source or
  engine substitution was involved.
- Two clean XeLaTeX passes on
  `glossa-corpus/indus/pierson_2026_indus_decipherment.tex`: both
  passes exit 0 with **zero errors** and no warnings in the log.
- Rendered output: **19 pages** (v7 was 18; the new §2.1.1 accounts
  for the additional page).
- PDF: `glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf`
  (the v7 PDF is removed, following the v6→v7 pattern).
  **SHA-256: 0f70dece76d3cdd31fa2ccb5c9fdbc9c2953587a9895700b8cf4632cd81f6670**
- Verified in the rendered PDF (pdftotext): E1's new wording present
  ("we no longer present it as evidence"); the old §2.1 claim no
  longer asserted — the phrase "consistent with a natural language
  writing system" survives only inside E1's own retrospective sentence
  about the earlier version, as the replacement text itself reads;
  §5's different phrase "consistent with a decipherable linguistic
  system" remains, as expected and untouched; §2.1.1 present with
  2.004, 0.1584, 1.96, 0.1544, 0.5335, 0.1839, 0.2405, 0.9229, and
  "UNINFORMATIVE"; Yadav entry present in §8; Roif 2025a/2025b entries
  present; "End of Preprint v8" present; **no "betweenness" anywhere;
  no §3.32 heading**.

**Nothing submitted, deposited, or published.**

## Red-team round 1 revision (2026-10-23)

The independent red-team pass on v8 (standing rule above) ran as
round 1: an independent engine (GPT-5.5 via OpenAI API, full text ×3
passes, 241 raw findings aggregated to 125 items) attacked the draft;
every finding was then adjudicated against the program's primary
records by an adjudicator who did not draft the paper. Dispositions:
**44 sustained / 76 sustained in part / 3 not sustained / 2 moot of
125**. The raw attack and the adjudication are filed beside this note
(`v8_redteam_round1_raw_2026-10-23.md`,
`v8_redteam_round1_adjudication_2026-10-23.md`).

**Revision applied.** All adjudicated replacement blocks R-01…R-45
were applied verbatim to the .tex (formatting conversion only:
markdown emphasis to LaTeX, the R-09 exponent table as a LaTeX
tabular, the §3.3 HIGH table's Basis column converted to a wrapped
column so R-14's longer entries render on the page, line-break
allowances inside §6's long file paths). Load-bearing outcomes: the
§3.1 anchor arithmetic is corrected (6,369 of 7,002 tokens; HIGH
70.34%); the Phase-150 and Phase-146 tests are reported at their
recorded INCONCLUSIVE verdicts (§§3.13, 3.11); the Phase-107 SA
held-out failure (agreement 0.000) is disclosed in §2.4; the 79.8%
aggregate confidence score and the 6,869 / 47 text-mining counts are
withdrawn as evidence (§§3.30, 3.22); §2.1.1 gains the explicit
guard that the four exponents "must not be compared with each
other"; the Phase-109 re-based anchor numbers (94 / 73.68%) were
**not** substituted — adjudication §D item 2 reserves that choice to
the owner, and R-11's disclosure is the applied cure. Protected text
(§8 Roif 2025a/b and both Rao entries; §3.5/§3.19 Roif credit; §7
Roif acknowledgment) is byte-intact in the source diff. §3.32 stays
out; "betweenness" remains at 0 hits.

**§6 commit pin.** §6's data-availability paragraph names the
revision commit, per the adjudication's coordinator note. Procedure
used: the revision was committed with §6 naming `b77cd420`
(commit `8a9e80cf`); a second, pin-only commit (`dba6d486`) changed
only the §6 commit string to `8a9e80cf`. §6 therefore names the
revision commit, not the pin commit or any later records commit.

**DEDR check (§E item 7) — still open.** The anchor records conflict
and do not settle the numbers: `ANCHOR_STATUS_AUDIT.csv` and
`research/indus/anchor_table.csv` both leave the DEDR column blank
for M176 and M261, while `backend/scripts/phase132_comprehensive_validation.py`
(V08 spot-check) lists 135 ("aN/an (masculine suffix)") and 4988
("muruku (young/god Murugan)") in its table of canonical DEDR entries
attributed to Burrow & Emeneau (1984). That is an internal program
assertion, not a verification against DEDR itself. The numbers were
left exactly as the replacement blocks carry them (135 in R-14; 4988
in the §3.3 table) and the item is recorded as **still open**.

**Still-open items.** (1) Holdat corpus release — every corpus
number rests on an unreleased corpus; R-01/R-41 disclose this, only
release (or a public-corpus rerun) cures it. (2) SA re-base — the
owner's decision (see above). (3) DEDR 135 / 4988 verification
(above). (4) Red-team **round 2** on the revised draft is pending;
v8 is not cleared for publication until the loop closes.

**Rebuild.** TinyTeX XeLaTeX (same toolchain and font environment
fix as the original v8 build), two passes on the final .tex state,
both exit 0, **zero errors and zero warnings** in the final log.
PDF: `glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf`
— still named v8 (this is a pre-publication revision of the v8
draft, not a new version). **23 pages** (was 19).
**SHA-256: 1ef5eb721f4b9cdd7fc4f1afbe790793cd2c0ba74d48898c0331a0ae0309d2b0**

**Render verification (pdftotext of the new PDF).** Present:
"6,369 of 7,002"; "70.34"; INCONCLUSIVE in both §3.11 and §3.13;
"must not be compared with each other"; SA held-out "0.000"; "End of
Preprint v8"; §6 commit `8a9e80cf`; Roif 2025a/2025b entries in §8.
Absent as claims: "6,363", "76.3%", "79.8%" and "highest-PMI" each
survive only inside the corrective sentences the adjudication
itself prescribed (R-34's withdrawal of the 79.8% score; R-19's "It
is not the highest-PMI pair"); "6,869" appears once, only in R-30's
withdrawn-as-evidence framing. No "betweenness"; no §3.32.

**Nothing submitted, deposited, or published.** The PR
(#353) is not merged.

## Red-team round 2 revision (2026-10-23)

Round 2 of the independent red-team pass on v8 (attack: independent
engine, GPT-5.5 via OpenAI API, full PDF text ×4 passes, 207 raw
findings aggregated to 58 items plus positives P1–P5) was adjudicated
against the program's primary records by an adjudicator who did not
draft the paper. Dispositions: **28 sustained / 29 sustained in part /
0 not sustained / 1 moot (R2-06) of 58; positives P1–P5 all
confirmed**. The raw attack and the adjudication are filed beside
this note (`v8_redteam_round2_raw_2026-10-23.md`,
`v8_redteam_round2_adjudication_2026-10-23.md`). The round-2 pattern
was echoes: most round-1 cures had landed in their home section but
not in the abstract, the §1.3 summary list, or §§3.30/4.5/5. Two
round-1 replacement texts themselves contained errors the attacker
correctly caught (the permutation parenthetical, R2-10; the §3.27
sibilant clause, R2-12); both are corrected by this revision. No
round-2 finding overturned a round-1 settlement of fact.

**Revision applied.** All adjudicated replacement blocks
R2R-01…R2R-58 were applied verbatim to the .tex (57 blocks with
replacement text; R2R-06 is MOOT and has no replacement), with
formatting conversion only (markdown emphasis and dashes to LaTeX,
the R2R-22 KL formulas in math mode, the R2R-25 §3.5 table expanded
to all nine site rows as a LaTeX longtable). The adjudicator's notes
were honoured: §1.3 items were identified by their quoted text, not
item number; R2R-13's heading renames were extended to §§3.18 and
3.27 in the same pass ("Cross-Validation" now appears in no heading
and no §1.3 label); R2R-22 prints the KL definitions recovered from
the Phase-151/144/145 scripts; R2R-35 only *adds* §8 entries (Sproat
2014; Rao et al. 2010, *Computational Linguistics*) — no existing
entry was altered except the Nair access date required by R2R-54.
Load-bearing outcomes: the permutation parenthetical is corrected at
all three locations (0.0005, add-one estimate); the Phase-134
z-score inputs are printed unrounded (0.9916, 0.4385, 0.05347,
z = 10.344) with the F7 held-out sentence added; all four sibilants
are worded PROVISIONAL_MEDIUM everywhere (§§1.3, 2.2, 3.25, 3.27);
the SA-affected count is printed (43 SA+DEDR MEDIUM signs, 398
tokens; removal bound 118 signs / 5,971 tokens / 85.28%); "pre-registered"
for Phase-107 is replaced by the Spec 005 wording (protocol fixed in
advance in this repository; no external registration filed); the Gulf
echoes are brought down to the §3.19 cure everywhere (abstract,
§1.3, §3.30, §4.5, Appendix C); the Phase-133 figures are corrected
(43.5% full+partial; 44.3% is sign-position accuracy); the 19 blocker
signs are named in §3.29 with the 92.35% arithmetic; the §3.30 tally
is split by kind with no top-label aggregate; the CISI 87% figure is
marked uncountable. Protected text (§8 Roif 2025a/b and both Rao
entries; §3.5/§3.19 Roif credit; §7 Roif acknowledgment) is
byte-intact in the source diff against `de4f340f`, verified per entry
and per paragraph. §3.32 stays out; "betweenness" remains at 0 hits;
the Spec 072 insert stays HELD and unintegrated.

**§6 commit pin.** Two-commit procedure, as round 1. The revision
was committed with §6 naming `de4f340f` (the pre-revision HEAD) and
R2R-01's reader-facing pin-explanation sentence included with that
value (revision commit `2d26b929`); a second, pin-only commit
(`d39f75f0`) changed only the §6 commit string to `2d26b929`. §6
therefore names the revision commit, not the pin commit and not
`de4f340f`, and the shipped PDF prints `2d26b929`.

**Word count (R2R-52).** The adjudication settled **10,837** for the
PRE-revision PDF by the command `pdftotext <pdf> - | wc -w` (verified
again on the pre-revision build in this session: 10,837). That figure
moved when the text changed, as expected: the round-2 replacement
texts add substantial disclosure paragraphs, definitions, and the
expanded §3.5 table. Procedure followed: after the final build the
exact command was run on the new PDF (**14,370**), the .tex
word-count line was set to the measured value, the PDF was rebuilt,
and the command was re-run — the printed figure equals the shipped
PDF's count (14,370; the number token is one word either way, so the
count is stable across the pin rebuild, whose only text change is
the §6 commit string).

**Rebuild.** TinyTeX XeLaTeX (same toolchain and font environment
fix as the original v8 build), two passes on the final .tex state
and two on the pin state, all exit 0, **zero errors and zero LaTeX
warnings** in the final log (one 1.8pt overfull hbox in §3.28, from
the prescribed Phase-167 file path; no text runs off the page). PDF:
`glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf`
— still named v8 (a pre-publication revision of the v8 draft).
**27 pages** (was 23). **SHA-256:
8d0d676eee187de71ad268c6ff374b9d6d6e8a788582552f366e9dc59365ddd0**

**Render verification (pdftotext of the shipped PDF).** Present:
"0.0005" at all three permutation-parenthetical locations; the
unrounded Phase-134 inputs (0.9916, 0.4385, 0.05347, 10.344); the
Spec 005 wording in §2.4 with "no external or public registration";
all-four-PROVISIONAL_MEDIUM sibilant wording; 85.28% SA bound;
43.5% Phase-133 wording; the 19-sign blocker list in §3.29;
NO_SEAL_MATCH in §3.15; the nine site rows in the §3.5 table; the
new §8 Sproat (2014) and Rao et al. (2010) entries; the Nair access
date; renamed headings (§3.18 "Terminal Comparison", §3.22 "Reading
Overlap Count", §3.27 "Sibilant DEDR Check"); §6 commit `2d26b929`;
printed word count 14,370; "End of Preprint v8". Absent: "0.001 is
the smallest"; "Cross-Validation" in any heading or §1.3 label;
"44.3%" as a whole-inscription match (it now appears only as
Phase-133's sign-position accuracy, per R2R-48); "multiple
converging tests"; "0/140" as a combined result in the abstract,
§1.3, and Appendix C; "betweenness"; §3.32. ("Tamil Murugan" survives
only inside R2R-16's own withdrawal sentence in §3.3, as the
replacement text itself reads.)

**Still-open items.** (1) **Phase-132 V03 motif counts — reserved
for round 3.** V03's nine-motif counts (unicorn 147, zebu 78,
elephant 43, …) do not match §3.4's printed motif counts (unicorn
127, zebu 72, elephant 37, rhinoceros 25, …). The adjudication
deliberately scoped R2R-26 to degrees of freedom + expected-basis
wording + the record pointer only; R2R-26 was applied exactly as
written and the printed counts were left as they stand. The
discrepancy is reserved for the round-3 attack/adjudication.
(2) §3.19's body still carries its home-section sentence reporting
"the combined figure of 0/140 used in the abstract" (with its
different-units disclosure); the adjudication prescribed no
replacement for that sentence, so it stands as written — after this
revision the abstract no longer uses the combined figure, and the
stale cross-reference is flagged here for round 3. (3) Owner
decisions carried by the adjudication (§D): Holdat corpus release;
SA re-base; DEDR 135 (M176) / 4988 (M261) verification against
Burrow & Emeneau directly; whether to print the sign list. (4)
Record gaps the cures disclose but cannot fill (adjudication §E):
the DEDR search space, the SA training corpus, the CISI 87%
numerator/denominator, the Phase-156 search terms, the unverified
§8 identifications (Jha & Rajaram, Heras, CISI, mayig, ICIT, Shakti,
DAMOS, the Tamil-Brahmi inventory source), Phase-170 tie handling,
the Phase-150 exceedance count, and a true SA-free headline. (5)
Red-team **round 3** on this revised draft is pending; v8 is not
cleared for publication until the loop closes.

**Nothing submitted, deposited, or published.** The PR
(#353) is not merged.
