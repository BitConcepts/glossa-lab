# Preprint v11 — Version Note (DEPOSIT text, 2026-11-18)

**Status.** This is the version note for the deposited v11 text.
It supersedes `v11_version_note_CORRECTED.md`, which described the
corrected draft before deposit preparation and is retained as a
working record. The v11 text was frozen for deposit on
2026-11-18, after the owner approved the corrected text for
deposit the same day. The version DOI assigned to v11 is recorded
here as %%VERSION_DOI%% until the deposit is made; the title page
of the paper carries the concept DOI
(10.5281/zenodo.20379070), which resolves to the latest version.

**Where the text lives.** The deposited text is frozen in the
public repository (https://github.com/AXIOVEX/glossa-lab) on
branch `preprint-v11-deposit`, in `glossa-corpus/indus/`:

- Revision (freeze) commit **R′**:
  `c22ade1b000d62b8eb86a16b935233ad1a3a5c0b` — the deposit text
  and its build, with this version's working records (AUDIT.md,
  REDTEAM.md, DEREF-MAP.md, FORMAT.md, FIXROUND.md,
  ADJUDICATION.md, CORRECTIONS.md, S314-CHECK.md). The branch
  started from main at
  `bd921ec99828ce06e635865b710ce3ee2c152b85`, and §6 of the text
  at R′ names that starting commit, as the pin procedure
  prescribes. (An earlier freeze chain of the same round was
  superseded before anything was deposited — see the
  end-matter note under Deposit preparation below.)
- Pin commit: `3979767b64be274ce7661752a481a66685fc7b40` —
  changes exactly one string in one file (§6 now names R′ itself)
  and no other paper text; verified from the repository record.
- The deposited PDF was added by the records commit
  `971140b0d585c87d72288c7f674348fb9e7c1725` as
  `glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v11.pdf`.
  This note is added by a further records commit on the same
  branch.

**Identity of the deposited text.**

- Source: `pierson_2026_indus_decipherment_v11_deposited.tex`,
  SHA-256
  `3174d692a4b225ebd785c961e5638de73efdc4b8e2212df6cc1dac5c953fc0ce`.
  (In the repository the same bytes are the file
  `glossa-corpus/indus/pierson_2026_indus_decipherment_v11_deposit.tex`
  at the pin commit.)
- PDF: `pierson_2026_indus_decipherment_preprint_v11_DEPOSITED.pdf`,
  SHA-256
  `08490d342a024f434f23d178d2f3de5ffecbbd3b33ed35897c0a524778e523a9`.
- Build: **39 pages**; LuaLaTeX (TeX Live 2026), two passes, zero
  errors, zero undefined references or citations.
- Word count: **21,748** (method: `pdftotext | wc -w`); the
  printed figure in the paper's end matter equals the measured
  figure on the deposited build (rebuilt to the fixed point; the
  §6 commit-string swap between the freeze build and the
  deposited build does not change the count).
- The freeze build at R′ (which names the branch's starting
  commit in §6): source SHA-256
  `9094d83952cd57493f974bfd99d4d1576f86d19d3f58b8f817b1c4afdfe3bc34`,
  PDF SHA-256
  `f9dc2e00cdf5f784214a8173f77071a5b86e16b1fe2d3dcb7e5fc2b9115020a8`,
  39 pages, word count 21,748. The deposited text differs from
  the freeze text in the one §6 commit string and in no other
  sentence.

## How this text was reached

Preprint v11 is a corrections-and-presentation version of the
deposited v10 (Zenodo record 23977473). The full records are
committed beside the text at R′; in summary:

- A statement-by-statement audit of v10 against the program's
  records (41 statement blocks: 39 still accurate, 2 superseded,
  0 contradicted) — `AUDIT.md`.
- Exactly two text corrections to §5, bringing the conclusion's
  account of the strict-core revalidation up to the completed
  record (6 independently supported; 65 internal-only; 4 still
  requiring revalidation; 3 expert-pending; 16 insufficient —
  71 of 94 supported at all), plus a new §5 paragraph reporting
  that none of the six independently supported readings is
  identifiable under the program's standard.
- A complete re-typeset in the format of the program's RCPH
  paper — `FORMAT.md`.
- A de-referencing pass over the whole text: 250 replacements of
  internal study names by public identifiers or plain-language
  descriptions — `DEREF-MAP.md`.
- The program's migration to Axiovex Systems: affiliation
  "Glossa-Lab / Axiovex Systems, LLC", correspondence
  `research@axiovexsystems.com`, repository transferred to
  `github.com/AXIOVEX/glossa-lab` on 2026-11-18.
- Removal of the front-matter headline-set note, replaced by one
  plain sentence after the version line.
- An independent red-team pass (verdict NOT READY on the draft's
  version note, since rewritten) and its fix round —
  `REDTEAM.md`, `FIXROUND.md`.
- An external review received through the owner (an independent
  AI reviewer, Co-scientist), adjudicated finding by finding
  against the program's own records before any text changed —
  `ADJUDICATION.md`. Three findings were real, one was not, and
  one was a claim-strength question the owner ruled on (soften).
  The correction round that followed — the §3.3 terminal rates
  (M342 ends 70 of 584 tokens, 12.0%; M176 ends 68 of 356,
  19.1%; both predominantly medial) and every dependent
  statement, the §3.7 occurrence counts, the §3.8 significance
  estimate removed, the §3.18 terminal-rate definition, the
  §3.31.1 token-999 accounting sentence, the §2.4 record-bases
  clarification, and the softened §5 claim-strength wording —
  is itemized in `CORRECTIONS.md`.
- The §3.14 terminal-profile sentence, flagged unsettled by the
  correction round, was checked against its own study record
  and found wrong there too; it was replaced with the record's
  own result (no pair of signs dominates the domains' terminal
  profiles; the leading terminal sign differs by domain) —
  `S314-CHECK.md`, and the addendum in `CORRECTIONS.md`.

## Deposit preparation (2026-11-18)

Applied to the approved corrected text to produce the deposit
text; every edit is listed with before/after wording in
`DEPOSIT-PREP.md`, filed with the working records. The corrected
source itself is untouched (SHA-256
`8de26083419a1f801cb9f0e4d6d28e289763abc0f6205fb90f91a7e514473c81`).

- **Title page.** The DOI/SHA identification block is removed:
  the explanatory sentences after the DOI line are gone, a single
  DOI line naming the concept DOI remains, and the version line
  now reads "Preprint v11 — Not peer-reviewed" (it read
  "Preprint v11 (draft, not yet deposited) — Not peer-reviewed").
- **§6.** The pin-procedure passage is shrunk to its
  one-sentence named-commit form: the mechanics paragraphs are
  out, and §6 names the revision commit at which the version's
  text was frozen. The draft-provenance paragraph is rewritten
  to its deposited form: this version is the deposited v11 text
  (version DOI: %%VERSION_DOI%%), prepared from the deposited
  v10 text, identified by the freeze commit named in §6 and by
  this version note, deposited with it.
- **Chronology note.** The plain-language chronology note at the
  end of §2.1.1 (the study-numbering process history) is
  removed; the lead-in to the remaining identification note is
  adjusted to match ("One identification note belongs on the
  record").
- **Word count.** Re-measured on the deposit build and printed
  at the measured figure (21,748, above).
- **End matter.** The end-matter line read "End of Preprint v11
  (draft)" in the text as first frozen. Before anything was
  deposited, the word was struck on the owner's direction (the
  line now reads "End of Preprint v11"), the text was rebuilt
  to the fixed point (21,748 words), and the freeze chain on
  this branch was redone from the same starting commit: the
  first chain (freeze `b7e1b644…`, pin `e942137f…`) is
  superseded in full by R′ and the pin named above, and was
  never deposited or pulled anywhere.

## What was NOT changed

- Outside the rounds itemized above, every sentence of the paper
  stands as in the deposited v10 lineage: the title, the
  abstract, §§1–5 outside the disclosed corrections, the
  appendices, and every other result, number, and reference.
- **§3.32 is still absent**, and the held fish-family study is
  still named only in the permitted form, as in v8, v9, and v10.
  The §3.5 withheld-study paragraph is unchanged in every round,
  as the owner approved the text with it standing.

## Remaining deposit steps (for the deposit itself)

- Replace %%VERSION_DOI%% in §6 and in this note with the v11
  version DOI once the Zenodo draft exists, before upload; the
  swap is one token for one token, and the printed word count is
  re-verified on the rebuilt PDF at that step.
- Upload the deposited PDF (identity above) as the new version
  on the Zenodo record; bring ResearchGate current.

*AI disclosure: audit, draft preparation, red-team pass, fix
round, adjudication, correction round, deposit preparation, and
build executed by AI agents (Muse, via Muse) at the
direction of Tristen Pierson, per the standing paper rule; the
external review whose findings the correction round answers was
likewise the work of an AI reviewer (Co-scientist), received
through the owner.*
