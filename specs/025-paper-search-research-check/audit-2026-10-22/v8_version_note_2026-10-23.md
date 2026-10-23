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
