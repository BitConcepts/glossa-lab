# Phase-418 — Spec 056 sign-821 recovery report

Executed 2026-10-21 by Muse Spark via Muse (AI agent), under the frozen Spec 056 contract (freeze digest
`64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e`; OSF registration 3eygs, approved + public before the run,
DOI 10.17605/OSF.IO/3EYGS).

## Outcome

**IDENTIFICATION FAILED**

Re-extraction found a specific argument in the passage of record (‘It is suggested here that sign 821, in the Dholavira signboard contexts, has a meaning of ‘city’, either as a determinative or as a word.’, printed p. 92), but the claim cannot be recovered in the program's form: the drawn sign could not be identified by either route §5 R-3 allows. The fragment is neither recovered nor retired; it stays a stated gap, with this closure as the record of why, and the unblocking act is the preservation, as a committed and hashed record, of an inspectable drawn-form reference for Wells's sign 821 — the Figure 2.6 sign-list pages (printed pp. 19–22) or the Figure 6.13 examples as images tied to the list entry — from which the drawn sign can be matched by drawn form through the crosswalk registry or quoted as the source list's own entry.

This act is record repair. It establishes, at most, what the source passage argues — never whether the argument is right, and nothing about sign 821 itself.

## The passage of record

Wells (2015), ‘The Dholavira signboard, revisited’,
printed pp. 90–94; held cleaned text
(`glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`),
lines 2783–2871; passage slice 5,354 bytes, SHA-256
`51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604`. Anchor sentence: “Whatever sign 821 reads it is used in a variety of contexts (Figure 6.13).”

The held text drops the book's sign glyphs and
Figure 6.13 is graphic-only in it, present only as its
caption; that limit stands as a stated boundary of
the recovery test (DD-056-13) and is stated wherever
this outcome is stated.

## Step 0 (all gates passed)

Gate 0.1 — input integrity, every pin recomputed:

- `glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt` — SHA-256 `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` (pin match: True)
- `glossa-indus/reports/phase104_claims_evaluation.json` — SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (pin match: True)
- `specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json` — SHA-256 `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` (pin match: True)
- `data/crosswalks/canonical_sign_registry.csv` — SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` (pin match: True)
- `backend/reports/INDUS_FINAL_ANCHORS.json` — SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (pin match: True)

Claim record, in the freeze's Spec 038 form: freeze-time
SHA-256 constant `bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a`
carried in freeze.json; the fragment's facts asserted
on the live file (entry found, status untested, stage
created, the source passage named in its
not-understood text) — match: True.

Gate 0.2 — the passage was produced from the held copy:
both anchor lines stand as standalone lines exactly
once, and the anchor sentence occurs exactly once.

Gate 0.3 — the passage slice recomputes to its
freeze-pinned digest
(`51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604`,
5354 bytes).

## Dry-run (DD-056-16)

The sheet and checklist machinery was exercised on
‘The Mohenjo-daro bangle pot’ (cleaned-text lines
2872–2931), a passage other than the passage of
record, before the protocol touched the fragment.
Its quote was verified verbatim and its checklist
completed in form; it produces no candidate and no
outcome for the fragment.

## Step 1 — extraction (two passes, reconciled)

- **K-1** — Sign 821, in the Dholavira signboard contexts, has a meaning of ‘city’, either as a determinative or as a word; of the passage's candidate glosses (DED 752 ūr; DED 808 eyil; DED 3568 nakar; DED 4112 pāri), eyil is the best choice, because Dholavira is a walled city made of cut stone.
- **K-2** — Considered and not credited as a candidate about sign 821: the passage's Fuls paragraph, framed as a verification of the 821 ‘city’ reading, whose asserted content concerns sign 861.
- **K-3** — The bare fragment restated: sign 821 is used in a variety of contexts.
- **K-4** — Considered as a standalone candidate: eyil-ay or eyil-i (sign 821 collocating with sign 740) is not attested.

Both passes found the same candidate set; the
reconciliation records full agreement, settled by
the quotations on the sheets. Every quote was
verified verbatim against the pinned passage by the
phase script. The full sheets, reconciliation, and
per-candidate checklists are the extraction record:
`specs/056-sign821-recovery/extraction-record.md`.

## Step 2 — the recovery test

The decisive candidate K-1 passes R-1, R-2, R-4 and
R-5 on both sheets. R-3: the sign list is named from
the document itself — Wells's own sign list (Wells
2011), as given in Wells 2015, Chapter 2 / Figure
2.6. The drawn sign is identified by neither
allowed route: the pinned registry carries no W821
value in any of its 803 rows (its Yunmapped_0821 row
is a Yajnadevam glyph identifier — the frozen
number-collision trap — and was not used), the
Phase-123 Wells witness carries no grapheme 821,
and the source list's own entry stands in Figure
2.6, whose drawn forms did not survive the held
copy's text extraction, so no entry can be quoted.
R-3 therefore fails, and §6's mapping gives
IDENTIFICATION FAILED: the fragment is neither
recovered nor retired.

Unblocking act: Preserve, as a committed and hashed record, an inspectable drawn-form reference for Wells's sign 821 — the Figure 2.6 sign-list pages (printed pp. 19–22) or the Figure 6.13 examples as images tied to the list entry — so the drawn sign can be matched by drawn form through the crosswalk registry or quoted as the source list's own published entry with its locator, satisfying §5 R-3.

Anchors asserted byte-identical before and after
(`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
