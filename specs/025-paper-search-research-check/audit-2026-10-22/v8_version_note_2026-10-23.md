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

## Red-team round 3 revision (2026-10-23)

Round 3 of the independent red-team pass on v8 (attack: independent
engine, GPT-5.5 via OpenAI API, full PDF text ×4 passes, 116 raw
findings aggregated to 53 items, plus 4 adjudicator-only probes and
36 positives) was adjudicated against the program's primary records
by an adjudicator who did not draft the paper. Dispositions:
**12 sustained / 32 sustained in part / 9 moot of 53; probes
R3X-1, R3X-2, R3X-3 sustained, R3X-4 not sustained; positives
36/36 confirmed**. The raw attack and the adjudication are filed
beside this note (`v8_redteam_round3_raw_2026-10-23.md`,
`v8_redteam_round3_adjudication_2026-10-23.md`). No round-3 finding
overturned a round-1 or round-2 settlement of fact; the surviving
defects were echoes the round-2 revision did not reach, and two
tables printed from a secondary note instead of the test record.

**Revision applied.** All adjudicated replacement blocks
R3R-01…R3R-X3 (47 blocks) were applied verbatim to the .tex, with
formatting conversion only (markdown emphasis and dashes to LaTeX,
the R3R-X2 table as LaTeX longtable rows, percentages escaped).
Nine blocks carry no replacement text and were applied as their
dispositions direct: R3R-23, R3R-42 and R3R-46 are record gaps whose
existing in-paper disclosures stand as the complete cure, and the
MOOT items (R3-04, R3-08, R3-09, R3-10, R3-27, R3-43, R3-48,
R3-52, R3-53) and probe R3X-4 have no replacement. Class (b)
blocks were applied with their interim cure text exactly; the
owner decisions themselves were not taken. Class (c) blocks print
the honest disclosure and invent nothing (in particular R3R-49:
no §8 entry was added, removed or altered — Crawford (2001) stands
as printed, flagged incomplete-on-record; only the in-text
"Wells (2015)" citation form was aligned to "Wells & Fuls (2015)").
R3R-22's artefact direction was followed exactly: §3.8 now
describes the supplemental file `iconographic_formula_pairs.csv`
honestly as the 15 strongest enriched pairs, not the full table.
Load-bearing outcomes: §3.4 prints the Phase-132 V03 motif table
(unicorn 147, zebu bull 78, elephant 43, rhinoceros 26, buffalo 20,
script only 34, geometric 19, tiger 17, gharial 16 — 400 tokens)
beside the χ² = 12.98 statistic it was computed from, and withdraws
the basis-note counts (127/72/37/25); §3.8 prints the true top five
(M060, M045, M016, M067, M039; χ² 158.5, 155.3, 148.8, 118.9,
116.5 — record values 118.88 and 116.456 for the last two); §3.19
no longer prints the combined 0/140 figure anywhere; §3.27's
"Formal cross-validation" heading-strength wording and its
PROVISIONAL_SUPPORTED_WITHIN_MODEL verdict are replaced by the
within-model plausibility check and the unchanged-status outcome
(the record's label survives only inside R3R-29's own sentence
saying it is not used in this paper); §4.4 no longer asserts a
named SA training corpus and no longer calls the MEDIUM threshold
"deliberately strict" or high-frequency signs "well-constrained";
the recorded HIGH basis for M342, M176 and M261 (the audit's
iconographic + distributional evidence pair) is printed in §3.3,
with M176's 94% terminal figure stated not to meet the >95%
criterion on its own; the sibilant count is corrected to 6 in
§3.16 and the M305 mismatch is disclosed in §3.15; all seven
Tamil-Brahmi terminal signs are printed in §3.18. Protected text
(§8 Roif 2025a/b and both Rao entries; §3.5/§3.19 Roif credit;
§7 Roif acknowledgment) is byte-intact in the source diff against
`5050947d`, verified per entry and per paragraph before and after
the revision. §3.32 stays out; "betweenness" remains at 0 hits;
the Spec 072 insert stays HELD and unintegrated.

**§6 commit pin.** Two-commit procedure, as rounds 1–2. The
revision was committed with §6 naming `5050947d` (the pre-revision
HEAD, which carries the round-3 adjudication) and R3R-02's
replacement text included with that value, keeping the round-2
pin-explanation sentence (revision commit `196ea0a2`); a second,
pin-only commit (`20463bd9`) changed only the §6 commit string to
`196ea0a2`. §6 therefore names the revision commit, not the pin
commit and not `5050947d`, and the shipped PDF prints `196ea0a2`.

**Word count.** The round-2 printed figure was **14,370**. After
the final build the adjudicated command `pdftotext <pdf> - | wc -w`
was run on the new PDF (**17,016**), the .tex word-count line was
set to the measured value, the PDF was rebuilt, and the command
was re-run — the printed figure equals the shipped PDF's count
(17,016; the number token is one word either way, so the count is
stable across the pin rebuild, whose only text change is the §6
commit string). The increase is the round-3 replacement texts
themselves: the added disclosure paragraphs, the printed V03 and
top-five tables' accompanying text, the §2.3 operational
appendices, and the completed §7 AI-tooling disclosure.

**Rebuild.** TinyTeX XeLaTeX (same toolchain and font environment
fix as the earlier v8 builds — OSFONTDIR covering the system Noto
directory and the TinyTeX Latin Modern Math directory, plus a
fontconfig file including the system fonts and the TinyTeX
texmf-dist font directories), two passes on the final .tex state
and two on the pin state, all exit 0, **zero errors** in the final
log. PDF:
`glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf`
— still named v8 (a pre-publication revision of the v8 draft).
**30 pages** (was 27). **SHA-256:
ddf71f1db2f6655c651420a7c103e0492c9325e5a0fa36d8019173206dd1934d**

**Render verification (pdftotext of the shipped PDF).** Present:
the V03 motif counts 147/78/43 in §3.4 beside χ² = 12.98 and the
400-token total; the true §3.8 top five M060/M045/M016/M067/M039
with 118.9 and 116.5 and the "five largest associations" caption;
the §3.3 HIGH-basis note (ICONOGRAPHIC+DISTRIBUTIONAL) with
M176's 94% caveat; §2.4's SA bound and consistency-definition
gap; the §3.14 matrix pointer, the Harappa–Rakhigarhi 0.481 next
pair, and the seed-42 statement; all seven Tamil-Brahmi signs in
§3.18; §6 commit `196ea0a2`; the §6 DOI/commit/supplements
sentences; printed word count 17,016; "End of Preprint v8";
end-matter date "May 2026; revised October 2026". Absent:
"0/140" anywhere; "Formal cross-validation"; "deliberately
strict"; "distinctively divergent"; "well-constrained"; "the one
point of agreement"; "semantic registers" in the §3.12 claim;
"betweenness"; §3.32. (§4.4's SA item now reads "described in
this program's records as trained on modern Tamil material, but
no record names the specific corpus" — the cured form, not a
named-corpus assertion. PROVISIONAL_SUPPORTED_WITHIN_MODEL
appears exactly once, inside R3R-29's prescribed sentence in
§3.27 stating that the label is not used in this paper.)

**Still-open items.** (1) **Owner decisions (adjudication §D)** —
none taken by this revision; the interim cure texts stand in
their place: (i) release the Holdat corpus or an inscription-level
derived table; (ii) commission a calibration of the HIGH/MEDIUM
labels; (iii) re-base the headline without SA and with the V07
drivers addressed, or formally decline; (iv) run the
rival-template and rival-family comparisons §4.4 names;
(v) archive the exact v8 source and supplements under the Zenodo
DOI. Block-level owner decisions also standing: printing the
161-row anchor table and 397-row inventory; whether M176 remains
HIGH on the audit's distributional type; whether to keep printing
the CISI 87.08% figure; freezing one V12 protocol and re-running
it on the 161-set; the title's "Anchors" framing. (2) **Record
gaps (adjudication §E)** the cures disclose but cannot fill: the
DEDR search space; the SA specification (training corpus,
syllable inventory, consistency context definition); a true
SA-free headline; criterion-level scoring for HIGH; the CISI
87.08% numerator/denominator and CISI/mayig identification; the
Tamil-Brahmi and F3 inventory sources; the bibliographic details
listed in §E item 7 (Jha & Rajaram 2000, Parpola 1975, the
Arthaśāstra edition, CISI, mayig, DAMOS, the Dering Roll source,
the Mesopotamian numerical-sign table, the mined Mahadevan
document list, Crawford (2001) publisher/place, Failaka catalogue
numbers, a Shu-ilishu authority); the M261 DEDR number (4988);
the 161-set site-by-site coverage table; the Phase-151 bootstrap
interval type and the Phase-134 permutation seed; the F1 data
matrix in the JSON record; the Phase-163 proximity rule and the
Phase-167 per-segment match rule; Phase-170 tie/overlap handling;
the V12 rule changes; the Phase-153 sibilant list; the 394-pair
inclusion rule. (3) Red-team **round 4** on this revised draft is
pending; v8 is not cleared for publication until the loop closes.

**Nothing submitted, deposited, or published.** The PR
(#353) is not merged.

## Red-team round 4 revision (2026-10-23)

Round 4 of the independent red-team pass on v8 (attack: independent
engine, GPT-5.5 via OpenAI API, full PDF text ×4 passes, 85 raw
findings aggregated to 38 items, plus 68 positives) was adjudicated
against the program's primary records by an adjudicator who did not
draft the paper. Dispositions: **8 sustained / 9 sustained in part /
20 moot / 1 not sustained of 38; positives 68/68 confirmed**. The
raw attack and the adjudication are filed beside this note
(`v8_redteam_round4_raw_2026-10-23.md`,
`v8_redteam_round4_adjudication_2026-10-23.md`). Round 4 produced
one genuinely new settlement of fact (S1, the fish-isolation
tautology), one new contradiction between two printed passages
(S3), and two new arithmetic settlements (S2: R4-04, R4-05);
everything else that re-litigated rounds 1–3 was held to its
precedent (in particular S5: the §5 "favours" sentence stays MOOT
under R2-06/R3-09).

**Revision applied.** All adjudicated text-bearing replacement
blocks were applied verbatim to the .tex (formatting conversion
only), each target passage verified by exact match before
substitution, locations identified by quoted text: R4R-01, R4R-03,
R4R-04, R4R-05, R4R-06, R4R-07, R4R-08, R4R-09, R4R-11, R4R-12,
R4R-13, R4R-15, R4R-18, R4R-21 (class (a)); R4R-10 and R4R-20
(class (a)+(c) — the interim text applied; the underlying record
gaps stand in adjudication §E). R4R-16 is class (c), a record gap
with no text: the seven §8 identifications (Jha & Rajaram 2000;
Parpola 1975; the five mined Mahadevan titles) remain unrecorded
and no entry was invented or added. MOOT items (R4-02, R4-14,
R4-19, R4-22–R4-38) and the NOT SUSTAINED item (R4-17) have no
replacement. Class (b) owner decisions named in the blocks were
not taken; only the interim text was applied.
Load-bearing outcomes, as the S1–S5 settlements were applied:
**S1 (R4R-01)** — the fish-sign isolation result is re-described
at all eight locations (abstract, §1.3, §3.5 definition paragraph,
§3.5 bounds paragraph, §3.19, §4.5, §5, Appendix C): the corpus
contains no single-sign inscriptions at all (Phase-134 test F9)
and the Phase-127 record's own conclusion was UNTESTABLE, so the
count is stated as a fact about the corpus, not a fish-specific
pattern; the binomial bounds (2.6% / 39% / 63%) are withdrawn as
isolation-rate estimates and kept only as arithmetic for a corpus
in which single-sign inscriptions occur; §3.5 also corrects the
supplemental-file description (27 compound occurrences for M047
and M001, not an occurrence-by-occurrence listing of all 113
seals; the M001 mismatch is stated as on record and unresolved).
**S2 (R4R-04, R4R-05)** — §3.16's sibilant count is tied to its
set: 6 for the 157-sign set, **10 for the current 161-sign set**;
§3.11's marker figures are corrected to **35/161 (21.7%)**
Dravidian-side and **0/161** Sanskrit-side under the test's own
definition (the 39/161 (24.2%) counting is withdrawn).
**S3 (R4R-03)** — §1.3 no longer says the blocker plausibility
check "is not counted" in §3.30: it is counted as item S12 in
the 32-item tally, listed for completeness, and is not evidence
that the blocker readings are correct. **S4 (R4R-10)** — §2.2
gains the HIGH-rule limit sentence for all 75 HIGH signs (same
recorded evidence-type pair for all 75; §3.3 prints selected rows
for 12; no criterion-by-criterion pass/fail exists for any HIGH
sign), and §3.3's lead sentence no longer presents M261's
published source as itself a §2.2 criterion. **S5** — MOOT, no
text change (see above). Further cures: §3.30's E07 cross-reference
corrected to §3.20 and its label aligned to Wells & Fuls (2015)
(R4R-06, with §3.20's heading and pronouns, R4R-12); §3.18's
incoherent "sole sign in a 2-sign formula" phrase withdrawn
(R4R-07); §4.2's "candidate Munda substrate readings" renamed to
the DEDR-backed wording — after this block, no location calls
M374 or M351 a Munda substrate reading without the DEDR basis in
the same sentence (R4R-08); §3.8's "roughly 20" sentence given
its uncorrected-level qualifier (R4R-09); §4.5's first sentences
gain the word "open" (R4R-11); §3.29's heading renamed
"Decode-Blocker Plausibility Check" (R4R-13); §2.3 prints the F7
split rule (by site: 1,176 fitted / 494 held out; 70.4% / 29.6%;
no seed) (R4R-15); the abstract's three-slot sentence is tied to
sign level with the Phase-133 whole-inscription rates (5.1% full,
38.4% partial) (R4R-18); §3.4 discloses the M267 test's
token-level unit of analysis (R4R-20); Appendix B no longer
converts token counts into seal counts (R4R-21). Protected text
(§8 Roif 2025a/b and both Rao entries; §3.5/§3.19 Roif credit
paragraphs — kept strictly separate from R4R-01's §3.5/§3.19
fish-test passages; §7 Roif acknowledgment) is byte-intact in the
source diff against `a92c53aa`, verified per entry and per
paragraph before and after the revision (no diff line touches a
Roif or Rao passage). §3.32 stays out; "betweenness" remains at
0 hits; the Spec 072 insert stays HELD and unintegrated; no
earlier settlement was reopened.

**§6 commit pin.** Two-commit procedure, as rounds 1–3. The
revision was committed with §6 naming `a92c53aa` (the pre-revision
HEAD, which carries the round-4 adjudication) and the
pin-explanation sentence kept (revision commit `ba5b4bf9`); a
second, pin-only commit (`0bf385b4`) changed only the §6 commit
string to `ba5b4bf9`. §6 therefore names the round-4 revision
commit, not the pin commit and not `a92c53aa`, and the shipped
PDF prints `ba5b4bf9`.

**Word count.** The round-3 printed figure was **17,016**. After
the final build the adjudicated command `pdftotext <pdf> - | wc -w`
was run on the new PDF (**17,997**), the .tex word-count line was
set to the measured value, the PDF was rebuilt, and the command
was re-run — the printed figure equals the shipped PDF's count
(17,997; the number token is one word either way, so the count is
stable across the pin rebuild, whose only text change is the §6
commit string).

**Rebuild.** TinyTeX XeLaTeX (same toolchain and font environment
fix as the earlier v8 builds — OSFONTDIR covering the system Noto
directory and the TinyTeX Latin Modern Math directory, plus a
fontconfig file including the system fonts and the TinyTeX
texmf-dist font directories), two passes on the final .tex state
and two on the pin state, all exit 0, **zero errors** in the final
log (two overfull hboxes, one pre-existing at the §3.8 file-name
paragraph and one 1.8pt at §3.27; no text runs off the page). PDF:
`glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf`
— still named v8 (a pre-publication revision of the v8 draft).
**31 pages** (was 30). **SHA-256:
ea924ec13f3e8a33fa7045bca386a5baed68bd94357800ceb339e6eedf38e942**

**Render verification (pdftotext of the shipped PDF).** The fish
result is stated at UNTESTABLE / no-single-sign-inscriptions
strength in every R4R-01 location: the abstract ("That count is
not fish-specific evidence: the corpus contains no single-sign
inscriptions of any kind (Phase-134, test F9)"), §1.3, §3.5
("gives its own conclusion as 'UNTESTABLE'"), §3.19 ("no
counterexample to the Holdat count"), §4.5 ("No verdict on a
fish-specific compound-only rule is claimed"), §5, and Appendix C
("the corpus contains no single-sign inscriptions, so the count
is not a fish-specific result"). Absent as claims: "systematic
fish-sign isolation test"; "A fish-sign isolation test:" (§1.3);
"compound-only verdict rests"; "fish-sign compound-only pattern"
(§5); the pooled-rate bound phrasing ("pooled isolated rate is
bounded"); "occurrence-by-occurrence listing is in". Present:
35/161 and 21.7% in §3.11, with "35/161 (21.7%) readings with
Dravidian-side markers"; §3.16's count of 10 for the current
161-sign set; §1.3's S12 wording matching §3.30 ("counted in
§3.30's 32-item tally as item S12, listed for completeness");
the §2.2 HIGH limit sentence ("no record gives a
criterion-by-criterion pass/fail for any HIGH sign"); the §2.3 F7
split rule ("The F7 split was by site"); the §3.29 heading
"Decode-Blocker Plausibility Check"; the §3.20 heading "Wells &
Fuls (2015) Sign List"; "candidate Munda substrate" at 0 hits;
§6 commit `ba5b4bf9`; printed word count 17,997; "End of Preprint
v8". Absent: "betweenness"; §3.32. **Prescribed-string survivals,
flagged explicitly:** (1) "39/161" and "24.2%" each appear exactly
once, inside R4R-05's own corrective sentence in §3.11 ("The
39/161 (24.2%) figure printed in earlier drafts counted the four
c-initial readings as Dravidian-side markers; that counting
changed the test's definition and is withdrawn") — not as claims.
(2) "compound-only pattern" survives in three places the
adjudication's blocks leave standing: the §1.3 Gulf-search item
and §4.5 point 2's first sentence, both in the weakened
"no counterexample … no confirmation" form, and §3.5's sentence
"The compound-only pattern holds at coastal and inland sites
alike", which sits in the paragraph remainder R4R-01 expressly
leaves unchanged (its following sentences fence it as a corpus
fact, and the same paragraph now carries the UNTESTABLE
re-description). No other survival of the old fish phrasing was
found.

**Still-open items.** (1) **Owner decisions (adjudication §D)** —
the loop does **not** close at round 4 (see the adjudication's
loop-closure statement): the previously adjudicated owner
decisions whose interim cures are in place are not reopened —
corpus release (R3-01), a calibration study for the confidence
labels (R3-07), the SA/V07 re-base (R3-05, R3-51), the V12
protocol freeze (R3-45), and archiving the exact v8 source under
the Zenodo DOI (R3-02) — and block-level decisions named in
round 4 stand open: whether M176 stays HIGH (R3R-15, standing);
a seal-level retest of the M267 motif distribution (R4R-20); the
per-criterion re-audit of the 75 HIGH signs behind R4-10/S4.
(2) **Record gaps (adjudication §E)** the cures disclose but
cannot fill: the fish supplement/M001 mismatch and whether F9's
absence is a corpus inclusion rule (§E.1, new this round); the
DEDR search space; the SA specification; criterion-level scoring
for HIGH; the seven unrecorded §8 identifications at R4-16
(Jha & Rajaram 2000, Parpola 1975, the five mined Mahadevan
titles); the CISI 87.08% numerator/denominator; the Phase-151
bootstrap interval type and the Phase-134 permutation seed;
unrounded M067/M039 expected counts; per-sign seal counts (the
18 Appendix-B signs; the distinct seals behind M267's 400
tokens); the formula analysis behind §3.18's withdrawn phrase;
and the standing round-3 §E gaps carried without change.
(3) Red-team **round 5** on this revised draft is pending; v8 is
not cleared for publication until the loop closes.

**Nothing submitted, deposited, or published.** The PR
(#353) is not merged.

## Red-team round 5 revision (2026-10-23)

Round 5 of the independent red-team pass on v8 (attack: independent
engine, GPT-5.5 via OpenAI API, direct, four passes over the full
PDF-extracted text, 94 raw findings aggregated to 38 items, plus 87
positives) was adjudicated against the program's primary records by
an adjudicator who did not draft the paper. Dispositions:
**5 sustained / 6 sustained in part / 25 moot / 2 not sustained of
38; positives 87/87 confirmed**. The raw attack and the
adjudication are filed beside this note
(`v8_redteam_round5_raw_2026-10-23.md`,
`v8_redteam_round5_adjudication_2026-10-23.md`). Round 5 produced
three genuinely new settlements (S8, S9, and the §6 cross-check in
S10), narrowed one precedent on new verification (S10 against
R3-02/R4-14's substance, which stands), and held the two
fifth-airing items to their precedents (S6, S7). No earlier
settlement was reopened by this revision.

**Revision applied.** All adjudicated replacement blocks
R5R-01…R5R-11 were applied verbatim to the .tex (formatting
conversion only: markdown emphasis and dashes to LaTeX, χ² / × / ≳ /
≈ in math mode, percentages escaped, `CLAIM_AUDIT.md` set as a
typewriter file name with its underscore escaped), each target passage verified
by exact match before substitution, locations identified by quoted
text: R5R-01 (§6 pin explanation, S10), R5R-02 (§2.3 z-score
cross-reference), R5R-03 (§3.8, four sub-replacements, S9),
R5R-04 (§1.3 and §6 anchor-table DEDR coverage, S8), R5R-05 (§5
tier definitions, inserted immediately before the Tier-2 sentence),
R5R-06 (§5 lead, class (a)+(b): the text was applied; the
corpus-release decision it names is the owner's and was **not**
taken), R5R-07 (§4.5 Gulf scope), R5R-08 (§3.28 and §1.3 ICIT
necessity claim), R5R-09 (§2.3 semantic labels), R5R-10 (§2.2
ghost criteria), R5R-11 (abstract subject). MOOT items (R5-01,
R5-02, R5-09–R5-12, R5-14–R5-19, R5-22, R5-26–R5-37) and the NOT
SUSTAINED items (R5-20, R5-38) have no replacement; their §A rows
are the complete disposition. R5R-09's instruction was followed in
its alternative form: §2.2's MEDIUM parenthetical
"(INITIAL=title prefix, TERMINAL=case suffix)" was left unchanged
and stands as a gloss read with the §2.3 cure, rather than
disturbing the criterion text.
**Settlements as applied. S6 (HIGH checkability, R5-01, MOOT)** —
round 4's S4 upheld; the R4R-10 limit sentence in §2.2 stands; no
text change. **S7 (§5 "favours", R5-02, MOOT)** — R2-06, R3-09 and
R4-S5 upheld, nothing material changed; no text change.
**S8 (R5-06, sustained, R5R-04)** — the anchor table's DEDR
coverage is now stated at its counted strength at both locations:
§1.3 prints that a DEDR citation is recorded in
`research/indus/anchor_table.csv` for **15 of the 161** signs (the
other 146 rows carry no DEDR entry in the table) and that no claim
is made that every reading carries a DEDR citation; §6 prints "a
DEDR citation on the 15 rows that have one". The second counted
figure in S8 — **16 of 161** in
`glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv` (145 blank; the two
files' DEDR columns agree on only 4 signs) — is the adjudication's
record of the audit file; no R5R block prints it in the paper, and
it is recorded here and in the adjudication, not in the PDF.
**S9 (R5-05, SIP, R5R-03)** — §3.8 now prints: **63 pairs enriched**
at a single-cell contribution **above 1.0** (the Phase-143 record's
own sense, observed above expected); **exactly 14 pairs at or above
the Bonferroni threshold χ² ≈ 14.7 on that statistic** (the
fourteenth value is 15.0); the threshold named as the critical
value, at 0.05/394 ≈ 0.000127, of the one-degree-of-freedom
chi-square distribution of a full 2×2 test, with the direction of
validity stated per S9 (the contribution is one positive term of
the full statistic, so a pass on the contribution necessarily
passes on the full 2×2 χ² — the comparison is conservative and
the 14 passes are valid; the full 2×2 value per pair is recorded
nowhere, the class (c) part of the block); the Phase-149 "robust"
definition corrected to what C2 actually computed (about 43 by
subtracting the roughly 20 false positives expected among 394
tests at an uncorrected 5% level, 63 − 19.7 — not a threshold
count); and the **394 denominator's filters, from the Phase-143
script**, printed in full (attested pairs only; multi-sign
inscriptions; first sign HIGH or MEDIUM; sign heads at least 5
such inscriptions; icon type on at least 5 seals in that set;
expected count at least 1), with the family stated as selected
from the data. **S10 (R5-03, SIP (minor), R5R-01)** — the §6 pin
explanation sentence was replaced with the adjudication's
corrected sentence; see the pin procedure and the post-pin truth
check below. Further cures: §5's Tier 2 / Tier 3 labels are now
defined where first used, from `CLAIM_AUDIT.md` (Tier 2:
probable linguistic interpretation — supported, not proven;
Tier 3: speculative or provisional, requiring explicit caveats);
§5's lead "reproducible" now carries the abstract's settled split
(scripts, phase reports and anchor table can be re-run and
checked from the repository; corpus-level counts cannot be
re-run until the Holdat corpus is released); §2.2's HIGH
independence sentence no longer names "the DEDR and Parpola
criteria", which are not criteria in the HIGH list, and states
them as inputs to the iconographic criterion; §2.3's three
semantic-label sentences are restated as positional classification
plus the model's interpretation, pointing to §3.2; §2.3's z-score
sentence now points to the printed inputs in §2.3 itself (observed
R² = 0.9916, null mean 0.4385, standard deviation 0.05347), not
to §5; §4.5 point 2's Gulf scope is aligned with §3.19 (no mention
of an isolated fish sign in either text; no fish-sign mentions at
all in the Laursen text, with §3.19 giving the source-specific
statement); §3.28's and §1.3's "ICIT corpus required" necessity
claim is replaced with what the Phase-167 record shows (a larger
corpus with contextual metadata would be needed; ICIT is the
named candidate; neither its unique necessity nor its sufficiency
is shown); and the abstract's subjectless clause is repaired
("§3.2). We also propose 161 candidate readings…"). Protected
text (§8 Roif 2025a/b and the Rao entries, each byte-checked;
§3.5/§3.19 Roif credit; §7 Roif
acknowledgment) is byte-intact in the source diff against
`ff9b9146`, verified per passage by hash before and after the
revision (no diff line touches a Roif or Rao passage). §3.32
stays out; "betweenness" remains at 0 hits; the Spec 072 insert
stays HELD and unintegrated; no earlier settlement was reopened.

**§6 commit pin.** Two-commit procedure, as rounds 1–4. The
revision was committed with §6 naming `ff9b9146` (the pre-revision
HEAD, which carries the round-5 adjudication) and R5R-01's
replacement text included with that value (revision commit
`88a6bf46`); a second, pin-only commit (`e585c767`) changed only
the §6 commit string to `88a6bf46`. §6 therefore names the
round-5 revision commit, not the pin commit and not `ff9b9146`,
and the shipped PDF prints `88a6bf46`.
**Post-pin truth check of the §6 explanation sentence (checked
once more after the pin commit, as required; flagged, not
silently fixed).** The R5R-01 sentence, applied verbatim, reads
in part: "the first sentence of this section there names
a92c53aa, the commit the round-4 revision started from, where
this draft names ba5b4bf9." That sentence was true of the
round-4 state the adjudication examined. It is **not true of
the final round-5 state**: at the named commit `88a6bf46`, the
first sentence of §6 names `ff9b9146` (the round-5 adjudication
commit, the commit this revision started from), not `a92c53aa`;
and the draft in hand names `88a6bf46`, not `ba5b4bf9`. The rest
of the corrected sentence **is** true of the final state,
verified against the git record: exactly one sentence differs
between the named commit and the shipped draft, and only in
that commit string (`git diff 88a6bf46 e585c767` on the .tex is
one line, one string); the pin commit changes only that string;
and the records commit that follows changes no paper text. The
two stale commit names inside the explanation sentence are a
residual inaccuracy carried by applying R5R-01 verbatim across
a new pin cycle; it is flagged here — and for round 6 — rather
than corrected silently, because no adjudicated replacement
authorises different wording. (The preceding §6 sentence,
"Commits after it on this branch add only records … and do not
change the paper's text", stands as in rounds 1–4 and is to be
read with the R5R-01 sentence, exactly as the adjudication's
note to R5R-01 directs: the pin commit's one-string change is
the difference that sentence exists to state.)

**Word count.** The round-4 printed figure was **17,997**. After
the final build the adjudicated command `pdftotext <pdf> - | wc -w`
was run on the new PDF (**18,591**), the .tex word-count line was
set to the measured value, the PDF was rebuilt, and the command
was re-run — the printed figure equals the shipped PDF's count
(18,591; the number token is one word either way, so the count is
stable across the pin rebuild, whose only text change is the §6
commit string, verified again after the pin: 18,591).

**Rebuild.** TinyTeX XeLaTeX (same toolchain and font environment
fix as the earlier v8 builds — OSFONTDIR covering the system Noto
directory and the TinyTeX Latin Modern Math directory, plus a
fontconfig file including the system fonts and the TinyTeX
texmf-dist font directories), two passes on the final .tex state
and two on the pin state, all exit 0, **zero errors** in the final
log. PDF:
`glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf`
— still named v8 (a pre-publication revision of the v8 draft).
**32 pages** (was 31). **SHA-256:
969c45d8da58a110371fabdf48875641a466eb20daacec0a78b65efb3b2c7a1f**

**Render verification (pdftotext of the shipped PDF).** Present:
"15 of the 161 signs" with the 146-row statement in §1.3 and "a
DEDR citation on the 15 rows that have one" in §6; §3.8's "63
pairs (16%) are enriched in the Phase-143 record's own sense"
with "single-cell contribution (below) is above 1.0", "14 pairs
stand at or above the Bonferroni threshold on that same
statistic" with the fourteenth value 15.0, the corrected
"robust" wording ("is that recheck's word for the roughly 43
pairs it judged genuinely significant by the subtraction just
described"; "it does not mean that 43 pairs stand at the
Bonferroni threshold — 14 pairs do, on the printed statistic"),
and the denominator filters (multi-sign inscriptions; first sign
HIGH or MEDIUM; sign heads at least 5; icon type on at least 5
seals in that set; expected count at least 1) with the Phase-143
JSON/script distinction; the §5 Tier 2 / Tier 3 definitions; the
§5 lead split (scripts, reports and anchor table re-runnable;
corpus-level counts not until the Holdat corpus is released);
§2.3's "Positional analysis classifies signs by position only"
with the semantic labels stated as the model's interpretation;
§2.3's "printed inputs in this section (observed R² = 0.9916,
null mean 0.4385, standard deviation 0.05347)"; §4.5's "no
fish-sign mentions at all in the Laursen text (§3.19 gives the
source-specific statement)"; the §3.28/§1.3 ICIT candidate
wording; the abstract's "We also propose 161 candidate
readings"; §6 commit `88a6bf46`; the R5R-01 explanation sentence
as applied (see the truth check above); printed word count
18,591; "End of Preprint v8". Absent: the "161 … with DEDR
citations" claim in §1.3 ("candidate readings with DEDR
citations"; "DEDR-linked phonetic hypotheses") and its §6 echo
("each sign's reading, DEDR citation, and basis"); "63 pairs
(16%) pass the corrected threshold"; "all except the DEDR and
Parpola criteria"; "INITIAL-dominant signs are classified as
title prefixes"; "printed inputs (§5)"; "The search found no
fish-sign mentions at all, so the Gulf material" (§4.5's old
both-texts form); "ICIT corpus required for personal names"; "is
required to identify name-bearing seal sequences"; "We propose
a reproducible computational grammar"; "(§3.2), and propose 161"
(the abstract's subjectless clause); "betweenness"; §3.32. The
§2.2 MEDIUM parenthetical "(INITIAL=title prefix, TERMINAL=case
suffix)" stands, as a gloss read with the §2.3 cure (R5R-09's
instruction, alternative form — see above). The "16 of 161"
audit-file figure does not appear in the PDF: it is S8's count
for `ANCHOR_STATUS_AUDIT.csv`, recorded in the adjudication and
above, and no R5R block prints it (see S8 as applied).

**Still-open items.** (1) **Owner decisions (adjudication §D)** —
the loop does **not** close at round 5 (see the adjudication's
loop-closure statement): the previously adjudicated owner
decisions whose interim cures are in place are not reopened —
corpus release (R3-01; also the class (b) half of R5R-06), a
calibration study for the confidence labels (R3-07), the
SA/V07 re-base (R3-05, R3-51), the V12 protocol freeze (R3-45),
archiving the exact v8 source under the Zenodo DOI (R3-02),
whether M176 stays HIGH (R3R-15), the paper's title (R3-14),
retention of the CISI 87.08% figure with its disclosure
(R3R-19), a seal-level retest of the M267 motif distribution
(R4R-20), and the per-criterion re-audit of the 75 HIGH signs
behind R4-10/S4 (carried at S6). (2) **The R5R-01 residual**
flagged in the post-pin truth check above: the explanation
sentence's two commit names (a92c53aa / ba5b4bf9) describe the
round-4 pin cycle, not the final round-5 state (ff9b9146 /
88a6bf46) — for the round-6 attack/adjudication to settle.
(3) **Record gaps (adjudication §E)** the cures disclose but
cannot fill, including the three new this round: the full
Phase-143 pair list and per-pair full 2×2 statistics (§E.1);
why the two central files' DEDR columns disagree — 15 vs 16 of
161, overlap 4 (§E.2); the Mitchell half of the Phase-156 search
(59 hits on unrecorded terms, §E.3); and the standing gaps: the
DEDR search space, the SA specification, criterion-level scoring
for HIGH, the unrecorded §8 identifications (R5-19), the CISI
87.08% numerator/denominator, the Phase-151 bootstrap type /
Phase-134 seed and F1 matrix, unrounded M067/M039 expected
counts, per-sign seal counts, and the fish supplement / M001
mismatch. (4) Red-team **round 6** on this revised draft is
pending; v8 is not cleared for publication until the loop
closes.

**Nothing submitted, deposited, or published.** The PR
(#353) is not merged.

## Red-team round 6 revision (2026-10-23)

Round 6 of the independent red-team pass on v8 (attack: independent
engine, GPT-5.5 via OpenAI API, direct, four passes over the full
PDF-extracted text, 84 raw findings aggregated to 39 items, plus 74
positives, and a 14-sentence line-by-line audit of §6 in Pass 3) was
adjudicated against the program's primary records by an adjudicator
who did not draft the paper. Dispositions: **5 sustained / 4
sustained in part / 28 moot / 2 not sustained of 39; positives 74/74
confirmed**. The raw attack and the adjudication are filed beside
this note (`v8_redteam_round6_raw_2026-10-23.md`,
`v8_redteam_round6_adjudication_2026-10-23.md`). Round 6 produced
six genuinely new settlements (S11–S16) and re-engaged two
precedents with reasons (S17, S18). No earlier settlement was
reopened by this revision.

**Revision applied.** All adjudicated replacement blocks
R6R-01…R6R-10 were applied verbatim to the .tex (formatting
conversion only: markdown emphasis and dashes to LaTeX, markdown
code spans to `\texttt{}` with escaped underscores, `&` to `\&` in
the R6R-06 citation, the en dash in the 1972–2018 span as `--`),
each target passage verified by exact match before substitution,
locations identified by quoted text: R6R-01 (§6 pin, purely
procedural form, S11), R6R-02 (DEDR distinctions at three
locations — §1.3, §2.4, §3.27 — S12), R6R-03 (§6 anchor-table
scope, S13), R6R-04 (§6 selected-rows sentence, S14), R6R-05 (§8
addition only — Jha & Rajaram (2000), S15), R6R-06 (§3.28 in-text
citation aligned to the §8 entry already present, S15, class
(a)+(b)), R6R-07 (Appendix C Phase-44 lift, S16), R6R-08 (§3.23
"four decades" label, heading and both text occurrences),
R6R-09 (Phase-134 cross-reference; the sentence stands in §3.13
Polysemy Permutation Null in the current numbering — the
adjudication names it §3.9's polysemy section, at line 604), and
R6R-10 (§3.7 PMI denominator). MOOT items (R6-06, R6-08, R6-09,
R6-10, R6-12, R6-13, R6-17, R6-18…R6-38) and the NOT SUSTAINED
items (R6-15, R6-39) have no replacement; their §A rows are the
complete disposition. For R6R-06, the adjudicated text was
applied; the owner-confirmation fallback named in the block was
**not** invoked (it is not the revision worker's to invoke, and
the tasking directed applying the text). For R6R-10, the inserted
sentences were placed at the adjudicated point immediately after
"the Phase-142 record", and the record's file-name parenthetical
that stood at that point in the .tex is retained between the
inserted sentences and the original "which is also where the
distinct-bigram counts above … are recorded" clause, so no
original text was dropped. Class (b) owner decisions named in
the blocks were not taken; only the interim text was applied.

**Settlements as applied. S11 (R6-01, sustained, R6R-01)** — §6's
pin paragraph is replaced in full with the purely procedural
form naming no historical commit (see the pin procedure and the
clause-by-clause truth check below). **S12 (R6-02, SIP,
R6R-02)** — the paper's three DEDR counts are now distinguished
at the three locations that print them, as counts of three
different recorded things: entries in the anchor table's DEDR
column (15 of 161, §1.3, with the three-way distinction printed
there in full); the combined SA+DEDR evidence-type label in the
status audit (43 MEDIUM signs, §2.4 — the label records the
promotion route; in the audit file's own DEDR column only 15 of
the 43 carry an entry and 28 do not); and the DEDR entry numbers
printed for individual signs (§§3.3, 3.27 — taken from basis
statements and phase records, not all recorded in either file's
DEDR column; §3.27's four upgrades now state their Phase-166
`dedr_id` record and that neither file's DEDR column carries an
entry for them, their audit evidence type being DEDR_PROXIMITY).
No DEDR number changes. **S13 (R6-03, SIP, R6R-03)** — §6 now
describes the anchor table as the file it is: 397 rows (one for
every Mahadevan catalogue sign), of which 161 are the HIGH/MEDIUM
rows and 236 carry LOW readings, with the DEDR clause preserved
in its corrected scope (a citation recorded in the table's DEDR
column on 15 rows, all among the 161). §§2.1 and 3.1 were correct
and are unchanged. **S14 (R6-04, sustained, R6R-04)** — §6 no
longer claims the tables are "deliberately not summarised by
selected rows anywhere in this paper": selected rows are printed
in §3.3 and Appendix A as illustrations only, the complete tables
are printed nowhere in the paper and are in the repository.
**S15 (R6-05, SIP, R6R-05 + R6R-06)** — §8 gains exactly one
entry, Jha & Rajaram (2000), *The Deciphered Indus Script*, New
Delhi: Aditya Prakashan, in alphabetical position (after Hojlund
& Abu-Laban, before Lubotsky), at the Spec 025 audit's own
metadata level — no author initials (none in any record located),
no subtitle, no pagination; and §3.28's in-text source list now
cites "(Parpola, Parpola & Brunswig 1977; …)", aligning it to the
1977 Meluḥḥa Village entry already in §8. No existing §8 entry
was removed or altered. **S16 (R6-07, sustained, R6R-07)** —
Appendix C's Phase-44 item no longer reads "Dravidian Tier 1 lift
ratio: 3.13x above null": it states the stored ratio 3.1334,
printed as 3.13, as what it is — a ratio of two lifts (Dravidian
0.4965 over its null, Sanskrit 0.1584 over its null, from the
Phase-44 T3 record `outputs/phase44_t3_v3_sa_300k.json`) — with
the §2.4 / Phase-107 held-out limit beside it and the statement
that it is not evidence Dravidian fits better and does not
qualify §4.4. Further cures: §3.23 prints the span 1972–2018
instead of the "four-decade" label at the heading and both text
occurrences (the second as "1972–2018 (46 years)"); the
Phase-134 cross-reference now points to §2.3 only; §3.7's PMI
worked example now prints the denominator — 5,332 bigram tokens
(7,002 sign tokens minus one per each of the 1,670 inscriptions),
P(M342·M176) = 122/5,332, P(M342) = 584/7,002, P(M176) =
356/7,002 — and 2.43 recomputes from those fractions (2.432, the
Phase-142 record's stored value). Protected text (§8 Roif 2025a/b
and both Rao entries and the Rao et al. (2010) entry, each
byte-checked; §3.5/§3.19 Roif credit; §7 Roif acknowledgment) is
byte-intact in the source diff against `dff001c7`, verified per
passage before and after the revision: the §8 section is
identical to the pre-revision §8 apart from the single Jha &
Rajaram addition, and no diff line touches a Roif or Rao passage.
§3.32 stays out; "betweenness" remains at 0 hits; the Spec 072
insert stays HELD and unintegrated; no earlier settlement was
reopened.

**§6 commit pin.** Two-commit procedure, as rounds 1–5. The
revision was committed with §6 naming `dff001c7` (the
pre-revision HEAD, which carries the round-6 adjudication) and
R6R-01's replacement text included (revision commit `b28cf2f5`);
a second, pin-only commit (`81a37e06`) changed only the §6
commit string to `b28cf2f5`. §6 therefore names the round-6
revision commit, not the pin commit and not `dff001c7`, and the
shipped PDF prints `b28cf2f5`.

**Post-pin truth check of the shipped §6 paragraph (the critical
check required for R6R-01; carried out clause by clause after
the pin commit against the git record — every clause verified
true; no clause required editing, and none was edited).**
(1) *"The text of this draft is identified by the branch and
commit named here, together with the one-string difference
explained below, not by the DOI."* — TRUE: §6's first sentence
names branch `preprint-v8-f2-spec068` and commit `b28cf2f5`;
the one-string difference is the pin string itself, explained
in the sentences that follow; the DOI sentence stands
separately and identifies only the preprint and its Zenodo
version record. (2) *"The commit named here is the revision
commit: the commit at which this paper's text was frozen for
the current round."* — TRUE: `b28cf2f5` is the round-6 revision
commit ("preprint v8: red-team round 6 revision (R6R-01..R6R-10
applied)"); all round-6 paper text was frozen at that commit.
(3) *"A commit cannot contain its own hash, so the copy of this
section at the named commit names, in its first sentence, the
commit that the revision started from."* — TRUE: at
`b28cf2f5`, §6's first sentence names `dff001c7` (verified by
reading the .tex at that commit), and `dff001c7` is
`b28cf2f5`'s parent — the round-6 adjudication commit, the
commit the revision started from. (4) *"The draft in hand
differs from the text at the named commit in that one commit
string, and in no other sentence."* — TRUE: `git diff b28cf2f5
81a37e06` on the .tex is exactly one line, and in that line only
the commit string `dff001c7` → `b28cf2f5`, inside §6's first
sentence; the rendered-text diff of the two commits' PDFs is
likewise exactly one line, that same string. (5) *"The commit
that follows the named commit on this branch and changes that
string — the pin commit — changes no other paper text."* —
TRUE: the pin commit `81a37e06` is the immediate child of
`b28cf2f5` on this branch; its only .tex change is that one
string, plus the rebuilt PDF in which that string is the sole
text change. (6) *"The records commits that follow it (the
rebuilt PDF, the version note, and the records of later rounds)
change no paper text at all."* — TRUE for this round's records
commit, verified after it was made: it touches only this
version note, `LEDGER.md` and `AGENTS.md` — no .tex and no PDF —
so the shipped paper text at the records commit is identical to
the pinned text. As a statement about later rounds the clause is
procedural — it holds for as long as the established procedure
is followed, which is exactly the durability the adjudication
prescribed; it names no historical commit, and the shipped §6
contains no historical commit hash in its explanation sentences
(the only 8-hex string in §6 is `b28cf2f5`, in the first
sentence).

**Word count.** The round-5 printed figure was **18,591**. After
the final build the adjudicated command `pdftotext <pdf> - | wc
-w` was run on the new PDF (**19,011**), the .tex word-count
line was set to the measured value, the PDF was rebuilt, and the
command was re-run — the printed figure equals the shipped
PDF's count (19,011; the number token is one word either way, so
the count is stable across the pin rebuild, whose only text
change is the §6 commit string, verified again after the pin:
19,011).

**Rebuild.** TinyTeX XeLaTeX (same toolchain and font environment
fix as the earlier v8 builds — OSFONTDIR covering the system Noto
directory and the TinyTeX Latin Modern Math directory, plus a
fontconfig file including the system fonts and the TinyTeX
texmf-dist font directories), two passes on the final .tex state
and two on the pin state, all exit 0, **zero errors** in the
final log. PDF:
`glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf`
— still named v8 (a pre-publication revision of the v8 draft).
**32 pages** (was 32). **SHA-256:
48dfb48ed0d860af64c8d74786b79638dc8cd6185c491c2df2f76efe57a3a69b**

**Render verification (pdftotext of the shipped PDF).** Present:
§6 in the durable procedural form naming `b28cf2f5` ("The commit
named here is the revision commit"; "A commit cannot contain
its own hash"), with **no** historical commit hash anywhere in
§6 (no `a92c53aa`, `ba5b4bf9`, `ff9b9146`, `88a6bf46` or
`dff001c7`); the DEDR distinctions at all three R6R-02 locations
(§1.3 "Three DEDR counts in this paper count three different
recorded things"; §2.4 "also carries the combined SA+DEDR
evidence type" with "it is not a count of entries in that file's
DEDR column, where 15 of the 43 signs carry an entry and 28 do
not"; §3.27 the Phase-166 `dedr_id` statement with "(Neither
file's DEDR column carries an entry for these four signs; in the
status audit their evidence type is recorded as
DEDR_PROXIMITY.)"); §6's anchor-table scope "397 rows — one for
every sign in the Mahadevan catalogue — of which 161 are the
HIGH/MEDIUM rows … and the other 236 carry LOW readings" with
the DEDR-column clause (15 rows, all among the 161); the
corrected selected-rows sentence ("Selected rows from the anchor
evidence are printed in this paper — in §3.3 and in Appendix A —
as illustrations only; the complete tables are printed nowhere
in this paper and are in the repository", split across a page
break in the extraction but present in full); §8's Jha & Rajaram
(2000) entry with *The Deciphered Indus Script* and Aditya
Prakashan, and the Roif 2025a/b and Rao entries standing as
before; §3.28's "(Parpola, Parpola & Brunswig 1977; Steinkeller
1982; Potts 1994; Reade 2001; Kjaerum 1983)"; Appendix C's lift
sentence as cured (0.4965 / 0.1584 / 3.1334 / "It is a ratio of
two lifts, not a lift above a null" / the §2.4 Phase-107 limit);
§3.7's "5,332 bigram tokens" with "122/5,332" and "the printed
PMI of 2.43 recomputes from those three fractions"; §3.23's
heading "Mahadevan Grammar Consistency, 1972–2018" and the
"1972–2018 (46 years)" wording; the corrected Phase-134
cross-reference "(§2.3), not on this one"; printed word count
19,011; "End of Preprint v8". Absent: "deliberately not
summarised by selected rows"; "Dravidian Tier 1 lift ratio";
"3.13x above null"; "four decades" / "Four-Decade" (the §3.23
internal LaTeX label retains its old slug, as in prior heading
renames — it is not printed text); "Parpola 1975"; the old §6
anchor-table description; "betweenness"; §3.32.

**Still-open items.** (1) **Owner decisions (adjudication §D)** —
the loop does **not** close at round 6 (see the adjudication's
loop-closure statement): the previously adjudicated owner
decisions whose interim cures are in place are not reopened —
corpus release (R3-01), a calibration study for the confidence
labels (R3-07), the SA/V07 re-base (R3-05, R3-51), the V12
protocol freeze (R3-45), archiving the exact v8 source under
the Zenodo DOI (R3-02), whether M176 stays HIGH (R3R-15), the
paper's title (R3-14), retention of the CISI 87.08% figure with
its disclosure (R3R-19), a seal-level retest of the M267 motif
distribution (R4R-20), and the per-criterion re-audit of the 75
HIGH signs behind R4-10/S4. The R6R-06 owner confirmation also
stands: if the owner identifies a distinct 1975 Parpola source
behind the Phase-167 name list, R6R-06's fallback wording
applies and a sourced §8 entry would still be needed. (2)
**Record gaps (adjudication §E)** the cures disclose but cannot
fill, including the items new or extended this round: the full
Phase-143 pair list and per-pair full statistics (§E.1); why
the two central files' DEDR columns disagree (15 vs 16 of 161,
overlap 4) and where the 11 §3.3-printed DEDR numbers recorded
in neither column are each recorded (§E.2); the Phase-167
Parpola source's identity at title level (§E.3); the remaining
bibliographic details not in any record (the Arthaśāstra edition
among them; Jha & Rajaram's initials, subtitle and pagination
remain unrecorded) (§E.4); and the standing gaps: the DEDR
search space, the SA specification, criterion-level scoring for
HIGH, the CISI 87.08% numerator/denominator, the Phase-151
bootstrap type / Phase-134 seed and F1 matrix, unrounded
M067/M039 expected counts, per-sign seal counts, and the fish
supplement / M001 mismatch. (3) Red-team **round 7** on this
revised draft is pending; v8 is not cleared for publication
until the loop closes.

**Nothing submitted, deposited, or published.** The PR
(#353) is not merged.

## Red-team round 7 revision (2026-10-23)

Round 7 of the independent red-team pass on v8 (attack: independent
engine, GPT-5.5 via OpenAI API, direct, four passes over the full
PDF-extracted text, 93 raw findings aggregated to 40 items, plus 48
positives, including a 16-item line-by-line audit of §6 in Pass 3)
was adjudicated against the program's primary records by an
adjudicator who did not draft the paper. Dispositions: **3 sustained
/ 1 sustained in part / 34 moot / 2 not sustained of 40; positives
48/48 confirmed**. The raw attack and the adjudication are filed
beside this note (`v8_redteam_round7_raw_2026-10-23.md`,
`v8_redteam_round7_adjudication_2026-10-23.md`). Round 7 produced
two new settlements (S19, S20) and re-engaged two precedents with
reasons (S21, S22). No earlier settlement was reopened by this
revision; in particular §6's R6R-01 procedural paragraph was not
touched except its pin string itself.

**Revision applied.** All adjudicated replacement blocks
R7R-01…R7R-04 were applied verbatim to the .tex (formatting
conversion only: markdown code spans to `\texttt{}` with escaped
underscores where the block prints a file path), each target
passage verified by exact match before substitution, locations
identified by quoted text: R7R-01 (§3.7, §3.12 and §3.28 — the
cluster population stated as the population the Phase-148 record
groups: the 97 types are the 97 distinct INITIAL signs that begin
inscriptions in this corpus and carry a HIGH or MEDIUM reading; a
seal is grouped by its first sign alone, so the clusters partition
all 1,670 seals, not only the 1,165 seals that consist entirely of
HIGH-or-MEDIUM signs (§3.6); §3.28's matching set named the same
way; no number in §3.7, §3.12 or §3.28 changes, S19), R7R-02 (§3.28
— the Phase-167 record path made breakable at its slashes,
`backend/\allowbreak reports/\allowbreak
phase167\_meluhhan\_names\_expanded.json`, the device §6 already
uses), R7R-03 (§2.1 — "represents the primary published formal-seal
assemblage" replaced by the corpus's printed scope, formal stamp
seals from the nine sites, with the share of the full published
formal-seal assemblage stated as not measured and no claim about
that share made, R7-07 sustained in part), and R7R-04 (§3.13 — the
Phase-150 permutation's random seed printed: the Phase-150 script
fixes it at 42; the Phase-150 record itself does not state the
seed, R7-29). MOOT items (R7-04…R7-06, R7-08…R7-28, R7-30…R7-34,
R7-36…R7-40) and the NOT SUSTAINED items (R7-03, R7-35) have no
replacement; their §A rows are the complete disposition.

**Settlements as they stand.** **S19** (R7-01, SUSTAINED): the
Phase-148 record (`n_clusters` = 97, `n_seals_classified` = 1,670;
domain seal counts 845 + 446 + 145 + 135 + 99 = 1,670; the 97
per-cluster counts summed independently to 1,670) groups seals by
first sign alone; the printed counts were always correct for the
whole corpus and the population label was wrong in §3.7 and §3.12,
with a lesser instance in §3.28 — cured by R7R-01. **S20** (R7-03,
NOT SUSTAINED): the §6 line-by-line audit's 16 clauses were each
verified true against the git graph of the completed round-6 pin
cycle (revision `b28cf2f5`, pin `81a37e06`, records `045a24f2`, raw
`c1273175`) — the R6R-01 procedural form's first full test, passed.
**S21** (R7-22, MOOT): the §5 Tier-2 sentence, checked against the
tier definition R5R-05 printed and the body's adverse results
(Phase-107 agreement 0.000, Phase-134 F3 INCONCLUSIVE/AMBIGUOUS,
the V12 ACTIVE_CONCERN warning, Phase-150 INCONCLUSIVE), does not
exceed what its own definition permits; R3-07, R3-10, R5-07 and
R6-10 upheld. **S22** (R7-23, MOOT): the §5 "favours" sentence,
seventh airing; R2-06, R3-09, R4-S5, R5-S7 and R6-S17 upheld —
nothing material changed in the round-6-revised text.

**Pin procedure.** Two commits, as rounds 1–6: (1) revision commit
`649e0e75` ("preprint v8: red-team round 7 revision (R7R-01..R7R-04
applied)"), whose §6 commit string names `36e8c7ad`, the commit the
revision started from (the round-7 adjudication commit); (2)
pin-only commit `9133db8f`, changing only the §6 commit string
(`36e8c7ad` → `649e0e75`) plus the rebuilt PDF. §6 in the shipped
PDF names the round-7 revision commit `649e0e75`.

**§6 clause check (after the pin).** The shipped §6 paragraph was
re-verified clause by clause against the git graph, as the round-6
revision did. (1) *"All sign readings … are available in the
Glossa-Lab repository (…, branch preprint-v8-f2-spec068, commit
649e0e75)."* — TRUE: the named files exist in the tree at
`649e0e75` (`git ls-tree` verified: `research/indus/anchor_table.csv`,
`glossa-corpus/indus/ANCHOR_STATUS_AUDIT.csv`, the four supplemental
CSVs in `research/indus/supplemental/`, `backend/scripts/`,
`backend/reports/`). (2) *"The DOI named on the title page
identifies this preprint and its version record on Zenodo."* —
TRUE as printed (identification only; the next sentence expressly
denies that the DOI identifies this draft's text). (3) *"The text
of this draft is identified by the branch and commit named here,
together with the one-string difference explained below, not by
the DOI."* — TRUE: it claims a procedure, not a hash of the draft
in hand. (4) *"The supplemental files named in this paper … are in
the same repository at the same commit; no separate archive copy
of them exists yet."* — TRUE (item 1; the absence of an archive
copy is stated in the sentence itself). (5) *"The commit named
here is the revision commit: the commit at which this paper's text
was frozen for the current round."* — TRUE: `649e0e75` is the
commit that applied the round-7 replacements and froze the round-7
text; the one later change to paper text is the pin's single
string, which the following sentences describe. (6) *"A commit
cannot contain its own hash, so the copy of this section at the
named commit names, in its first sentence, the commit that the
revision started from."* — TRUE, verified: at `649e0e75` §6's first
sentence names `36e8c7ad`, and `36e8c7ad` is that commit's parent
(the round-7 adjudication commit the revision started from). (7)
*"The draft in hand differs from the text at the named commit in
that one commit string, and in no other sentence."* — TRUE,
verified: the .tex diff `649e0e75` → `9133db8f` is exactly one
line, and in that line only the commit string; the rendered-text
diff of the two commits' PDFs is likewise exactly one line, that
same string. (8) *"The commit that follows the named commit on
this branch and changes that string — the pin commit — changes no
other paper text."* — TRUE: the pin commit `9133db8f` is the
immediate child of `649e0e75` on this branch; its only .tex change
is that one string, plus the rebuilt PDF in which that string is
the sole text change. (9) *"The records commits that follow it
(the rebuilt PDF, the version note, and the records of later
rounds) change no paper text at all."* — TRUE for this round's
records commit, verified after it was made: it touches only this
version note, `LEDGER.md` and `AGENTS.md` — no .tex and no PDF —
so the shipped paper text at the records commit is identical to
the pinned text. As a statement about later rounds the clause is
procedural — it holds for as long as the established procedure is
followed; the shipped §6 contains no historical commit hash in its
explanation sentences (the only 8-hex string in §6 is `649e0e75`,
in the first sentence). The remaining §6 sentences (the
anchor-table sentence, the neither-table-printed sentence, the
selected-rows sentence, the reader-direction sentence, and the two
Holdat-corpus sentences) are unchanged by this revision and stand
as verified at S20. **All clauses verified true; no clause was
edited.**

**Word count.** The round-6 printed figure was **19,011**. After
the final build the adjudicated command `pdftotext <pdf> - | wc
-w` was run on the new PDF (**19,193**), the .tex word-count line
was set to the measured value, the PDF was rebuilt, and the
command was re-run — the printed figure equals the shipped PDF's
count (19,193; the number token is one word either way, so the
count is stable across the pin rebuild, whose only text change is
the §6 commit string, verified again after the pin: 19,193).

**Rebuild.** TinyTeX XeLaTeX (same toolchain and font environment
fix as the earlier v8 builds — OSFONTDIR covering the system Noto
directory and the TinyTeX Latin Modern Math directory, plus a
fontconfig file including the system fonts and the TinyTeX
texmf-dist font directories), two passes on the final .tex state
and two on the pin state, all exit 0, **zero errors** in the final
log. PDF:
`glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf`
— still named v8 (a pre-publication revision of the v8 draft).
**32 pages** (was 32). **SHA-256:
5335cdaba21c88c7ae6b56a75e5ec0f1a4db109ad480e57c652568709920b035**

**Render verification (pdftotext of the shipped PDF, plus a
rendered-page inspection).** Present: §3.7's cured definition
("the 97 distinct INITIAL signs that begin inscriptions in this
corpus and carry a HIGH or MEDIUM reading"; "the 97 types together
cover all 1,670 seals — not only the 1,165 seals that consist
entirely of HIGH-or-MEDIUM signs (§3.6)"); §3.12's cured lead
("the seal counts below sum to 1,670; they are not counts over the
1,165 seals that consist entirely of HIGH-or-MEDIUM signs (§3.6),
and no further size threshold is applied to the grouping"); §3.28's
cured population wording ("in the seal set decoded with the
161-anchor reading set (all 1,670 seals, as stated at the head of
this section)"); §2.1's cured scope ("It consists of formal stamp
seals from those sites; what share of the full published
formal-seal assemblage its 1,670 seals represent is not measured in
this paper, and no claim about that share is made"); §3.13's seed
("the Phase-150 script, backend/scripts/phase150_polysemy_permutation.py,
fixes the random seed at 42 — the Phase-150 record itself does not
state the seed"); §6 naming the revision commit `649e0e75`, with no
other 8-hex string anywhere in §6; printed word count 19,193;
"End of Preprint v8". Absent: "found among the H+M-covered seals";
"in the H+M-covered seal set"; "represents the primary published
formal-seal assemblage"; "betweenness"; §3.32. **§3.28
rendered-page check (the R7R-02 cure's own verification):** page 23
was rendered and inspected as a page image — the Phase-167 path now
breaks at its slash and prints in full inside the text block,
"(backend/reports/phase167_meluhhan_names_expanded.json)," with
its closing parenthesis on the page; nothing runs off the right
margin. No adjustment beyond the adjudicated `\allowbreak` points
was needed. **Protected text:** the .tex diff against `36e8c7ad`
touches only §2.1, §3.7, §3.12, §3.13, §3.28, §6's pin string and
the word-count line — all §8 entries (Roif 2025a/b, both Rao
entries, Jha & Rajaram 2000 as added at round 6, all others), the
§3.5/§3.19 Roif credit paragraphs and the §7 Roif acknowledgment
are byte-intact.

**Still-open items.** (1) **Owner decisions (adjudication §D)** —
the loop does **not** close at round 7 (see the adjudication's
loop-closure statement): the previously adjudicated owner decisions
whose interim cures are in place are not reopened — corpus release
(R3-01), a calibration study for the confidence labels (R3-07),
the SA/V07 re-base (R3-05, R3-51), the V12 protocol freeze (R3-45),
archiving the exact v8 source under the Zenodo DOI (R3-02),
whether M176 stays HIGH (R3R-15), the paper's title (R3-14),
retention of the CISI 87.08% figure with its disclosure (R3R-19),
a seal-level retest of the M267 motif distribution (R4R-20), and
the per-criterion re-audit of the 75 HIGH signs behind R4-10/S4.
The R6R-06 owner confirmation also stands: if the owner identifies
a distinct 1975 Parpola source behind the Phase-167 name list,
R6R-06's fallback wording applies and a sourced §8 entry would
still be needed. (2) **Record gaps (adjudication §E)** the cures
disclose but cannot fill, standing as filed in round 7's §E.1–§E.14
(items 1–14 of round 6's §E stand except where round 7's
settlements narrow them — the Phase-150 seed is removed from the
§E.9 family by R7-29/R7R-04; §E.11 is extended: no record reports,
for the Phase-148 clusters, how many of each cluster's seals are
among the 1,165 fully H+M-covered seals — S19 settles the clusters'
total population, not that breakdown; and §E.4 now also names a §8
source for the Holdat corpus's share of the published formal-seal
assemblage, the quantity R7R-03 states is not measured). (3)
Red-team **round 8** on this revised draft is pending; v8 is not
cleared for publication until the loop closes.

**Nothing submitted, deposited, or published.** The PR
(#353) is not merged.
