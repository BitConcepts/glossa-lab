# DEREF-MAP.md — de-referenced variant of the Indus paper v11 draft

Date: 2026-11-18. Status: PREPARED OPTION, not the default. Nothing published.

Source: `pierson_2026_indus_decipherment_v11_formatted.tex` (the RCPH-format variant).
Output: `pierson_2026_indus_decipherment_v11_formatted_deref.tex`, built to
`pierson_2026_indus_decipherment_preprint_v11_formatted_deref_DRAFT.pdf`
(LuaLaTeX, two passes, exit 0, 0 errors, 0 missing characters, 40 pages, letter).
Transform: `transform_deref.py` (asserted replacements; re-runnable).

## What was done

Every internal study name in the inherited text — Spec numbers, Phase numbers,
suite test ids (F1/F3/F7/F9/F12), validation ids (V03/V07/V12), tally item ids
(S09–S12, E06–E08, L07, L08), the "Asset A v2" layer label, and generic
"phase reports / phase records" phrasing — was replaced by:

- the public identifier where one exists (route "public pointer"): the four
  OSF-registered studies are cited by their OSF registration ids (3pbwe, 7cu23,
  cfe7z, jv74f) — 12 replacements; or
- a plain-language description of the study, taken from the paper's own section
  headings and first-mention descriptions (route "description") — 140 replacements; or
- removal of a redundant label or parenthetical where the sentence or heading
  already names the study in words (route "removed") — 98 replacements.

Total: 250 replacements. A residual scan of the result (outside `\texttt`
locators) for Phase-NNN, Spec NNN, F/V/S/E/L ids, "Asset A", and "phase
reports/records" returns 0 hits; the built PDF's extracted text likewise
contains no "Phase-", no "Spec NNN", and no "Asset A".

The inventory this pass worked from listed 259 occurrences. All prose
occurrences were replaced. The pass also caught 11 label instances the
inventory had not listed separately (the §3.30 tally ids and two further V07
forms). Occurrences inside `\texttt` file paths were kept (class decision
below). The v11 draft's own new §5 text was already reference-free and is
untouched; the §5 updates verify present in the built PDF ("71 of the 94…";
"none of the six is identifiable at that standard…").

## Numbers and claims

No number or claim changed. A numeric-token comparison of the two built PDFs'
extracted text shows differences only from: the removed internal study numbers
and label digits themselves; pagination (39 → 40 pages); pdftotext reflow of
table cells; and two section pointers added in the chronology note (§2.1.1,
§3.31.1 — verified against the formatted PDF's own heading numbers).

## Class decisions (owner can override any of these)

1. **File paths in `\texttt` are kept as public locators.** They resolve in the
   public GitHub repository the paper itself names in §6
   (github.com/BitConcepts/glossa-lab). 20 distinct paths contain a phase/spec
   string: the report and script paths for the falsification suite, the
   collocate-network, polysemy-permutation, site-divergence, Shu-ilishu,
   sibilant-inventory, Meluhhan-name, master-synthesis, validation-recount and
   substrate-screen studies, the early simulation record, and the
   `specs/005-…`, `specs/052-…`, `specs/068-…`, `specs/074-…`, `specs/075-…`
   directories. If the owner wants these out too, the descriptions in the
   table below already name each study, so the paths can be dropped without
   losing the reference.
2. **The withheld study (Spec 072 / Phase-431)** is de-referenced to
   "(the study is held from publication)" in §3.5. The held status stays
   visible; nothing about the study's content is added.
3. **"Tell F6 on Failaka Island"** in the bibliography is a published book
   title (a place name), not a test id — kept.
4. LaTeX `\label{...}` anchors still carry slugs derived from the original
   headings (e.g. `...-spec-052`). Labels are never rendered; they were left
   unchanged so cross-references stay intact.

## Judgment items (flagged for the owner)

- The chronology note (§2.1.2) originally explained the internal numbering
  itself ("`Phases 1--170' in this paper is the phase sequence… later work
  continued the same sequence under spec numbers (Spec 068 was executed as
  Phase-430, and Spec 071 as Phase-434)"). The variant rewrites it as: "the
  numbered study sequence behind the May 2026 anchor model ran to 170 studies.
  The numbering did not stop at 170 — later work in this program continued the
  same sequence (the frequency-curve test of §2.1.1 and the depicted-kinds test
  of §3.31.1 were both executed later in it)." The facts (a numbered sequence;
  170 studies behind the May 2026 model; the sequence continued) are preserved;
  the internal names are gone.
- The recorded verdict label `V12_ACTIVE_CONCERN` is paraphrased as "the
  recorded verdict flags an active concern" — the one place where a quoted
  record label was not carried verbatim, because the label itself is an
  internal name.
- Heading parentheticals were removed where the heading already names the
  study in words (e.g. "Sibilant DEDR Check (Phase-166)" → "Sibilant DEDR
  Check"); the §3.10 heading keeps its public attribution: "(Phase-145 +
  Nair 2026)" → "(with Nair 2026)".

## Replacement table

Route key: **osf** = public pointer (OSF registration) · **desc** = plain-language
description · **drop** = internal name removed (the surrounding text already
carries the reference, or a short substitution as shown). "×n" is the number of
occurrences the rule replaced.

| # | Original | Replacement | Route |
|---|---|---|---|
| 1 | (Spec 052) (×1) | (OSF registration 7cu23) | osf |
| 2 | (Spec 052, executed as Phase-437; OSF registration 7cu23) (×1) | (OSF registration 7cu23) | osf |
| 3 | (Spec 068, executed as Phase-430; OSF registration 3pbwe) (×1) | (OSF registration 3pbwe) | osf |
| 4 | in the Spec 068 record (×1) | in the registered study's record | osf |
| 5 | the same corpus layer as the Spec 068 test (×1) | the same corpus layer as the frequency-curve test | osf |
| 6 | the Spec 068 test (×1) | the frequency-curve test | osf |
| 7 | Spec 068 fit under the frozen Spec 053 rule (×1) | the registered fit under the frozen rule | osf |
| 8 | (Spec 068) (×1) | (OSF registration 3pbwe) | osf |
| 9 | (Spec 074) (×1) | (OSF registration cfe7z) | osf |
| 10 | (Spec 074, executed as Phase-440; OSF registration cfe7z) (×1) | (OSF registration cfe7z) | osf |
| 11 | (Spec 075) (×1) | (OSF registration jv74f) | osf |
| 12 | (Spec 075, executed as Phase-441; OSF registration jv74f) (×1) | (OSF registration jv74f) | osf |
| 13 | in this program's Spec 005 (\texttt{specs/005-phase52-v2/spec.md}), recorded in this repository before the runs (×1) | in a protocol recorded in this repository before the runs (\texttt{specs/005-phase52-v2/spec.md}) | desc |
| 14 | (Spec 072, executed as Phase-431) (×1) | (the study is held from publication) | desc |
| 15 | an earlier census in this program (Spec 037) found (×1) | an earlier census in this program found | drop |
| 16 | the Spec 037 census caution (×1) | the earlier census's caution | desc |
| 17 | the Zipf--Mandelbrot rule frozen by Spec 053 (×1) | the Zipf--Mandelbrot rule frozen in advance by this program | desc |
| 18 | (Glossa-Lab, Phases 1--170) (×1) | (Glossa-Lab) | drop |
| 19 | `Phases 1--170' in this paper is the phase sequence behind the May 2026 anchor model. (×1) | the numbered study sequence behind the May 2026 anchor model ran to 170 studies. | desc |
| 20 | The numbering did not stop at 170 --- later work in this program continued the same sequence under spec numbers (Spec 068 was executed as Phase-430, and Spec 071 as Phase-434). (×1) | The numbering did not stop at 170 --- later work in this program continued the same sequence (the frequency-curve test of §2.1.1 and the depicted-kinds test of §3.31.1 were both executed later in it). | desc |
| 21 | the Phase-52 lineage (×2) | the original sequence-analyser lineage | desc |
| 22 | (Phase-108 provenance register; Phase-109 re-review) (×1) | (the anchor provenance register and its re-review) | desc |
| 23 | the Phase-107 result on the SA machinery (×1) | the held-out test result on the SA machinery | desc |
| 24 | the Phase-107 held-out test (§2.4) (×1) | the held-out test (§2.4) | drop |
| 25 | (Phase-107, October 2026) (×1) | (October 2026) | drop |
| 26 | re-audit of its anchors (Phases 107--109) was itself (×1) | re-audit of its anchors was itself | drop |
| 27 | Phase-110 SA evidence (×1) | sequence-analyser evidence | desc |
| 28 | Phase-111 allograph (×1) | the allograph analysis | desc |
| 29 | this program's earlier Phase-43 framework (×1) | this program's earlier framework | drop |
| 30 | the Phase-43 exponent of about 1.35 (×1) | the earlier exponent of about 1.35 | desc |
| 31 | Phase-43 record in this program's files (×1) | an earlier record in this program's files | desc |
| 32 | (Phase-44) (×1) | (the early simulation study) | desc |
| 33 | In that suite's T3 run of the syllabic language-model simulation (×1) | In that study's syllabic language-model simulation run | drop |
| 34 | supported within internal checks (Phase-46) (×1) | supported within internal checks | drop |
| 35 | via this program's Phase-51 (×1) | via this program's extraction from that source | desc |
| 36 | Parpola 1994, via Phase-51 (×1) | Parpola 1994, via the same extraction | desc |
| 37 | (25 signs, Phase-123 --- the 25 are listed in the Phase-123 record, (×1) | (25 signs --- the 25 are listed in the substrate-screen record, | desc |
| 38 | The Phase-127 record, which made this count site by site, gives (×1) | An earlier site-by-site count record gives | desc |
| 39 | (Phases 124/127) (×1) | (the isolation counts) | desc |
| 40 | the Phase-128 re-review (×1) | the Munda-substrate re-review | desc |
| 41 | proposed by this program (Phase-128) (×2) | proposed by this program (in the Munda-substrate re-review) | desc |
| 42 | Summary of New Phase-128/129 (×1) | Summary of New Munda-Substrate Re-Review | desc |
| 43 | independently recounted in Phase-132 (×1) | independently recounted | drop |
| 44 | The counts are the Phase-132 record's (test V03 --- the distribution (×1) | The counts are the validation recount's (the distribution | drop |
| 45 | , test V03) (×1) | ) | drop |
| 46 | (Phase-132: 476 of 632 (×1) | (the validation recount: 476 of 632 | desc |
| 47 | Phase-133 corrected prior inflated count; (×1) | the grammar-match study corrected the prior inflated count; | desc |
| 48 | removed by Phase-133 (×2) | removed by the grammar-match study | desc |
| 49 | in the Phase-133 check, (×2) | in the grammar-match check, | desc |
| 50 | Retest of the Phase-133 grammar explained variance metric (×1) | Retest of the grammar-match study's explained-variance metric | desc |
| 51 | Phase-133's figures, (×1) | the grammar-match study's figures, | desc |
| 52 | Phase-133's 44.3\% (×1) | The grammar-match study's 44.3\% | desc |
| 53 | different definitions from the Phase-133 measure (×1) | different definitions from the grammar-match measure | desc |
| 54 | on a stricter cross-reading version (Phase-133e), or (×1) | on a stricter cross-reading version of the test, or | drop |
| 55 | comes from the Phase-134 F1 test (×1) | comes from the falsification suite's first test | drop |
| 56 | also ran a held-out check (F7): (×1) | also ran a held-out check: | drop |
| 57 | The F7 check behind the 97.7\% figure (Phase-134) is: (×1) | The held-out check behind the 97.7\% figure is: | drop |
| 58 | The F7 split was by site (×1) | The held-out split was by site | drop |
| 59 | our Phase-134 F1 positional test (×1) | the falsification suite's positional test | drop |
| 60 | (Phase-134, test F9) (×2) | (the falsification suite) | drop |
| 61 | (Phase-134, test F9: 0 single-sign seals in 1,670) (×1) | (the falsification suite: 0 single-sign seals in 1,670) | drop |
| 62 | (Phase-134, test F9: 0 single-sign seals) (×1) | (the falsification suite: 0 single-sign seals) | drop |
| 63 | it is the F9 fact restated (×1) | it is that fact restated | drop |
| 64 | on the 157-sign set (Phase-134 F12) (×1) | on the 157-sign set (the falsification suite's language-model comparison) | drop |
| 65 | rated the question AMBIGUOUS (Phase-134 F3) (×1) | rated the question AMBIGUOUS (the falsification suite's phonological-profile comparison) | drop |
| 66 | rests on the Phase-134 tests (§2.3) (×1) | rests on the falsification-suite tests (§2.3) | desc |
| 67 | rests on the Phase-134 permutation and held-out tests (×1) | rests on the falsification suite's permutation and held-out tests | desc |
| 68 | F3 redesign using phonemes (×1) | A redesigned form of the test, using phonemes | drop |
| 69 | Updated Phase-141 evidence scorecard incorporating Phases 142--168 (×1) | The updated evidence scorecard, incorporating every study since the first scorecard | desc |
| 70 | up from 23 at Phase-141 (×1) | up from 23 in the first scorecard | desc |
| 71 | the text-mining and positional methods of Phases 142--168 (×1) | the text-mining and positional methods of the later studies | desc |
| 72 | (Phase-142 formula classification; the clusters built on them are Phase-148's) (×1) | (the collocate study's formula classification; the clusters built on them are the formula-clustering study's) | desc |
| 73 | Positional constraint test (Phase-142D) (×1) | Positional constraint test (the collocate study's positional-constraint arm) | drop |
| 74 | was run against the Phase-142D polysemy finding (×1) | was run against the collocate study's polysemy finding | drop |
| 75 | so the Phase-142D descriptive result (81\% (×1) | so that descriptive result (81\% | drop |
| 76 | the Phase-146 and Phase-150 null results (×1) | the phonological-exclusivity and polysemy-permutation null results | desc |
| 77 | (`Uniform' in the Phase-149 summary of this test (×1) | (`Uniform' in the adversarial recheck's summary of this test | desc |
| 78 | An adversarial recheck (Phase-149) estimates (×1) | An adversarial recheck estimates | drop |
| 79 | `Robust' in the Phase-149 recheck (×1) | `Robust' in the adversarial recheck | desc |
| 80 | (Phase-149, challenge C2) (×1) | (the recheck's second challenge) | drop |
| 81 | none failed outright (Phase-149). (×1) | none failed outright. | drop |
| 82 | collocate context (Phase-144), and (×1) | collocate context, and | drop |
| 83 | in the Phase-144 blocker analysis (×1) | in the blocking-sign analysis | desc |
| 84 | (Phase-144/145 script) (×1) | (the cross-corpus comparison script) | desc |
| 85 | (Phase-152: candidate seals = 0) (×1) | (candidate seals = 0) | drop |
| 86 | (Phase-154: 417 of the 1,154 (×1) | (the vowel-harmony resolution study: 417 of the 1,154 | desc |
| 87 | have not been shown to account for the Phase-154 result (×1) | have not been shown to account for that result | desc |
| 88 | (270 of 1,154 decoded seals, Phase-155) (×1) | (270 of 1,154 decoded seals, in the Tamil-Brahmi comparison) | desc |
| 89 | (Phase-156: 0 hits) (×1) | (0 hits) | drop |
| 90 | (Phase-156, now complete) (×1) | (now complete) | drop |
| 91 | the Gulf text search (Phase-156) found (×1) | the Gulf text search found | drop |
| 92 | These Phase-158 counts (×1) | These counts | desc |
| 93 | Phase-158 counted every positional-class reference (×1) | The terminal-ideogram mining counted every positional-class reference | desc |
| 94 | the Phase-160 counts in §3.23 (×1) | the four-decade mining counts in §3.23 | desc |
| 95 | while Phase-160 counted, per paper, (×1) | while the four-decade mining counted, per paper, | desc |
| 96 | the Phase-160 counts give per-paper hits (×1) | the four-decade mining counts give per-paper hits | desc |
| 97 | (Phase-158: \texttt{vowel\_harmony\_refs} = 0) (×1) | (\texttt{vowel\_harmony\_refs} = 0) | drop |
| 98 | at time of Phase-161 analysis (×1) | at the time of that analysis | desc |
| 99 | Phase-163 adds 4 provisional sibilant upgrades (×1) | the text-proximity mining study adds 4 provisional sibilant upgrades | desc |
| 100 | in the mined literature (Phase-163), followed by a within-model check of the DEDR entry, the positional profile, and phonotactics (Phase-166), in which (×1) | in the mined literature (the text-proximity mining study), followed by a within-model check of the DEDR entry, the positional profile, and phonotactics (the sibilant DEDR check), in which | desc |
| 101 | The Phase-166 labels CONFIRMED (×1) | The sibilant DEDR check's labels CONFIRMED | desc |
| 102 | The Phase-163 mining record does not specify (×1) | The text-proximity mining record does not specify | desc |
| 103 | the four Phase-163 provisional MEDIUM sibilant upgrades (×1) | the four provisional MEDIUM sibilant upgrades | drop |
| 104 | the \textgreater{}=3 promotion threshold of Phase-163 (×1) | the \textgreater{}=3 promotion threshold used for those promotions | desc |
| 105 | the \textgreater{}=4 threshold Phase-166 uses (×1) | the \textgreater{}=4 threshold the sibilant DEDR check uses | desc |
| 106 | to PROVISIONAL\_MEDIUM in Phase-166 (×2) | to PROVISIONAL\_MEDIUM in the sibilant DEDR check | desc |
| 107 | by Phase-166.) (×1) | by the sibilant DEDR check.) | desc |
| 108 | (as in Phase-166) (×1) | (as in the sibilant DEDR check) | desc |
| 109 | Phase-166 partially addressed (×1) | The sibilant DEDR check partially addressed | desc |
| 110 | Sibilant DEDR check (Phase-166): (×1) | Sibilant DEDR check: | drop |
| 111 | Sibilant DEDR Check (Phase-166) (×1) | Sibilant DEDR Check | drop |
| 112 | (pre-Phase-163) (×1) | (before the sibilant promotions) | desc |
| 113 | against the pre-Phase-163 157 H+M readings (×1) | against the 157 H+M readings as they stood before the sibilant promotions | desc |
| 114 | before the Phase-163 sibilant additions (×1) | before the sibilant additions | desc |
| 115 | before the Phase-163 additions (×1) | before the sibilant additions | desc |
| 116 | the set as it stood at Phase-153, before the sibilant additions (×1) | the set as it stood at the time of the sibilant inventory, before the sibilant additions | desc |
| 117 | Expanding Phase-164 from 6 to 25 (×1) | Expanding the Meluhhan-name matching from 6 to 25 | desc |
| 118 | consistent with Phase-164. (×1) | consistent with the earlier name-matching result. | desc |
| 119 | name matching (Phase-167): (×1) | name matching: | drop |
| 120 | plausibility check (Phase-168): (×1) | plausibility check: | drop |
| 121 | Master evidence synthesis (Phase-169): (×1) | Master evidence synthesis: | drop |
| 122 | Grammar self-consistency retest (Phase-170): (×1) | Grammar self-consistency retest: | drop |
| 123 | 59 of 59 checks passing at Phase-170 (May 2026) (×1) | 59 of 59 checks passing (May 2026) | drop |
| 124 | all passing, at Phase-170 --- belongs (×1) | all passing --- belongs | drop |
| 125 | Phase-130 (signs whose presence (×1) | the decode-blocker list (signs whose presence | desc |
| 126 | (called Asset A v2 in this programme's records; the same layer used in §3.31.1) (×1) | (the same layer used in §3.31.1) | drop |
| 127 | identification layer (Asset A v2): (×1) | identification layer: | drop |
| 128 | Asset A v2 carries (×1) | that layer carries | drop |
| 129 | V07 phonotactic violation rate (×4) | phonotactic violation rate | drop |
| 130 | The V12 vowel-harmony warning is unresolved (×1) | The vowel-harmony warning is unresolved | drop |
| 131 | where the recorded verdict is V12\_ACTIVE\_CONCERN (×1) | where the recorded verdict flags an active concern | drop |
| 132 | the earlier description of V12 as a settled (×1) | the earlier description of the warning as a settled | drop |
| 133 | the program's authoritative V12 test (×1) | the program's authoritative vowel-harmony test | drop |
| 134 | The V12 warning therefore stands (×1) | The warning therefore stands | drop |
| 135 | cleared or condemned by V12 until (×1) | cleared or condemned by the vowel-harmony test until | drop |
| 136 | the status of V12, which remains unresolved (×1) | the status of the vowel-harmony question, which remains unresolved | drop |
| 137 | the unresolved V12 warning (×1) | the unresolved vowel-harmony warning | drop |
| 138 | as item S12, listed for completeness (×1) | as one of its items, listed for completeness | drop |
| 139 | Phase-134 JSON record (×1) | falsification suite's JSON record | desc |
| 140 | Phase-143 JSON record (×1) | iconographic cross-encoding JSON record | desc |
| 141 | (Phase-145 + Nair 2026) (×1) | (with Nair 2026) | desc |
| 142 | (§2.4, Phase-107) (×1) | (§2.4) | drop |
| 143 | driving the V07 rate (×1) | driving that rate | drop |
| 144 | the V07 phonotactic violations are concentrated (×1) | the phonotactic violations are concentrated | drop |
| 145 | (E06 ---  (×1) | ( | drop |
| 146 | (E07 ---  (×1) | ( | drop |
| 147 |  (E08), (×1) | , | drop |
| 148 | (S09 ---  (×1) | ( | drop |
| 149 |  (L07), (×1) | , | drop |
| 150 |  (L08), (×1) | , | drop |
| 151 | (S10 ---  (×1) | ( | drop |
| 152 | S10 is an internal consistency item (×1) | That item is an internal consistency item | drop |
| 153 |  (S11), (×1) | , | drop |
| 154 | (S12 ---  (×1) | ( | drop |
| 155 | Phase-132 record (×3) | validation-recount record | desc |
| 156 | Phase-133 record (×1) | grammar-match record | desc |
| 157 | Phase-134 record (×2) | falsification-suite record | desc |
| 158 | Phase-134 script (×2) | falsification-suite script | desc |
| 159 | Phase-134 suite (×1) | falsification suite | desc |
| 160 | Phase-142 record (×1) | collocate-network record | desc |
| 161 | Phase-142 script (×1) | collocate-network script | desc |
| 162 | Phase-143 record (×5) | iconographic cross-encoding record | desc |
| 163 | Phase-143 script (×3) | iconographic cross-encoding script | desc |
| 164 | Phase-144 record (×1) | blocking-sign record | desc |
| 165 | Phase-145 record (×2) | cross-corpus comparison record | desc |
| 166 | Phase-145 report (×1) | cross-corpus comparison report | desc |
| 167 | Phase-146 record (×1) | phonological-exclusivity record | desc |
| 168 | Phase-146 script (×1) | phonological-exclusivity script | desc |
| 169 | Phase-148 record (×1) | formula-clustering record | desc |
| 170 | Phase-149 record (×2) | adversarial-recheck record | desc |
| 171 | Phase-150 record (×1) | polysemy-permutation record | desc |
| 172 | Phase-150 script (×1) | polysemy-permutation script | desc |
| 173 | Phase-151 record (×2) | site-divergence record | desc |
| 174 | Phase-151 script (×2) | site-divergence script | desc |
| 175 | Phase-152 record (×3) | Shu-ilishu test record | desc |
| 176 | Phase-153 record (×2) | sibilant-inventory record | desc |
| 177 | Phase-155 record (×5) | Tamil-Brahmi comparison record | desc |
| 178 | Phase-156 record (×1) | Gulf-seal test record | desc |
| 179 | Phase-159 record (×1) | overlap-count record | desc |
| 180 | Phase-164 record (×1) | Meluhhan-name matching record | desc |
| 181 | Phase-166 record (×2) | sibilant DEDR check record | desc |
| 182 | Phase-167 record (×1) | expanded name-matching record | desc |
| 183 | Phase-168 record (×1) | decode-blocker record | desc |
| 184 | Phase-169 record (×2) | master synthesis record | desc |
| 185 | Phase-170 record (×1) | grammar-variance retest record | desc |
| 186 | (Phase-142) (×1) | *(removed)* | drop |
| 187 | (Phase-143) (×1) | *(removed)* | drop |
| 188 | (Phase-144) (×1) | *(removed)* | drop |
| 189 | (Phase-146) (×1) | *(removed)* | drop |
| 190 | (Phase-148) (×1) | *(removed)* | drop |
| 191 | (Phase-150) (×1) | *(removed)* | drop |
| 192 | (Phase-151) (×1) | *(removed)* | drop |
| 193 | (Phase-152) (×1) | *(removed)* | drop |
| 194 | (Phase-153) (×1) | *(removed)* | drop |
| 195 | (Phase-154) (×1) | *(removed)* | drop |
| 196 | (Phase-155) (×1) | *(removed)* | drop |
| 197 | (Phase-156) (×1) | *(removed)* | drop |
| 198 | (Phase-157) (×1) | *(removed)* | drop |
| 199 | (Phase-158) (×1) | *(removed)* | drop |
| 200 | (Phase-159) (×1) | *(removed)* | drop |
| 201 | (Phase-160) (×1) | *(removed)* | drop |
| 202 | (Phase-161/162/165) (×1) | *(removed)* | drop |
| 203 | (Phase-163) (×1) | *(removed)* | drop |
| 204 | (Phase-164) (×1) | *(removed)* | drop |
| 205 | (Phase-167) (×1) | *(removed)* | drop |
| 206 | (Phase-168) (×1) | *(removed)* | drop |
| 207 | (Phase-169) (×1) | *(removed)* | drop |
| 208 | (Phase-170) (×1) | *(removed)* | drop |
| 209 | phase reports (×5) | study reports | desc |
| 210 | phase records (×4) | study records | desc |
| 211 | per-phase results (×1) | per-study results | desc |
