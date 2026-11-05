# Preprint v10 — Version Note (2026-11-05)

**Scope.** Preprint v10 is a corrections-only version of the deposited
v9 (Zenodo record 23668053; source 152,892 B, SHA-256
`e7e1a011ec7f4ae8b0db360910d74a9e046c24950c5d0876a913da542bec584f`,
verified before work began). It carries exactly two text corrections
(V10-1, V10-2) from the tracker findings inventory of 2026-10-28
(`files/2026-10-28-tracker-findings-inventory.md`): no new results, no
re-argument, no other sentence changed. The corrections were prepared
on 2026-10-28 (prep record
`files/2026-10-28-v10-corrections-prepared.md`, SHA-256
`4baef82e9bff3dcae93e26c780b129634a0de94b16c089f9d593cde8cdad12a1`)
and approved by the owner on the exact prepared texts on 2026-11-05
(the GR-088-34 approval act). The deposit is executed the same day.

**Standing rule.** No paper publishes without TeX production and an
independent red-team pass. Both are complete: the two insertions went
through three independent red-team passes against the repair record
(the first two failed the drafts and the drafts were revised; the
third passed), recorded in full in the prep record, failures included.

## The changes

### V10-1 — Headline-supersession note (head of the paper, page 1)

A note immediately before the Abstract recording that the 161
candidate readings named in the paper's title and headline figures
(161 readings; 90.96% of corpus tokens) are no longer the program's
headline candidate set; that the headline set is now the strict core
of 94 readings whose recorded history never passed through the
program's original syllabic language-model (SA) simulation, whose
agreement with a proposed reading was falsified as evidence (§2.4);
that the results reported about the 161-reading set stand as the
record of that set, to be read at that strength wherever the headline
figures appear; and that the script remains undeciphered. The deposit
description is amended in the same sense (see the deposit entry).

### V10-2 — §5 Tier 2 qualification (new paragraph in the Conclusion)

A paragraph following the paragraph containing the Tier 2 sentence,
qualifying it with the October 2026 evidence audit's re-grading of
the 94 strict-core readings one by one: 6 independently supported (on
a recorded dual line of outside support taken as recorded); 46
supported by the program's internal evidence only; 37 requiring
revalidation; 3 pending expert adjudication (M222, M362, M398); 2 on
insufficient evidence (M367, M048). Of the 94, 52 are classed as
supported at all. The paragraph states that the audit graded the
strict core only, is not a re-grading of the 161, and does not by
itself falsify any reading.

### V10-3 — No text change (finding recorded here, per the inventory)

The inventory's conditional item: whether the §3.27/§3.29 plausibility
checks ran on the defective Phase-58 code path. The code-provenance
check resolved the item **SOUND**: the checks did not run on the
defective path, so no withdrawal is owed and the text stands
untouched, exactly as the inventory prescribes for that outcome.

## Version mechanics

- Title block: "Version: Preprint v9" → "Preprint v10"; end matter:
  "End of Preprint v10". Date line carried unchanged ("May 2026
  (revised October 2026)"): the corrections were prepared in October
  2026; the deposit was executed on 2026-11-05.
- Pin (per the procedure printed in §6 of the paper). Branch
  `preprint-v10-corrections-prep`. Corrections commit `49613e18`
  (V10-1 + V10-2, final revision after the red-team passes). Revision
  commit `47639918` — the deposit-round mechanics; its §6 names
  `b08de0b0`, the commit the revision started from. The deposited text
  differs from the text at the revision commit in the §6 commit string
  only (`b08de0b0` → `47639918`) and in no other sentence; the pin
  commit following the revision commit on main changes that string
  and no other paper text, and the records commit after it (the
  deposited PDF and this note) changes no paper text at all.
- Printed word count re-measured on the final build: **21,655**
  (method: `pdftotext | wc -w`), printed in the paper's end matter.

## What was NOT changed

- Every other sentence of v9 stands as deposited: the abstract, §§2–5
  outside the V10-2 insertion point, the appendices, every result,
  number, and reference. The §5 closing caution is untouched.
- **§3.32 is still absent.** The held restoration draft remains held
  pending Roif's reply, as in v8 and v9.
- **Spec 072 is not integrated.** It remains named only in the Roif
  gate's permitted form ("executed — held under the Roif gate"); no
  result content appears anywhere in v10.
- Explicitly checked and left as written, per the inventory: §3.22
  (Parpola), §3.5/§3.19 (fish), the coverage definitions, and the
  23.4% V07 statement.

## Build verification

- Toolchain: LuaLaTeX (LuaHBTeX 1.24.0, TeX Live 2026) — the engine of
  record for this paper since the v10 preparation (pdflatex cannot
  build it; v9 was XeLaTeX-built, and the one-page difference against
  v9's 35 pages is that engine difference, not content). Two passes,
  zero errors, zero undefined references.
- The branch text as prepared (commit `49613e18`, source SHA-256
  `e120c6ca8a625c1f8f72b2ea028f8cb2ffa35472e9724ce0de96832ab2299d9c`)
  was rebuilt before the deposit round: **34 pages, 21,655 words**,
  matching the prep record exactly.
- Deposited source: `pierson_2026_indus_decipherment.tex`, 155,460 B,
  SHA-256 `bd2d10255717d258fb77a68c856c66070fdc40f3ca1fe8b68a91b4051e8b981d`.
- Deposited PDF: `pierson_2026_indus_decipherment_preprint_v10.pdf`,
  232,694 B, SHA-256
  `33f637b192f927be28733ada8c8c04b722e9f65fd6b0b42c7d6df63e4eeb58dd`,
  34 pages, built from the deposited source and no other.
- Verified in the rendered PDF (pdftotext): the V10-1 note on page 1;
  the V10-2 paragraph in §5; "Version: Preprint v10"; §6 naming branch
  `preprint-v10-corrections-prep`, commit `47639918`; "End of
  Preprint v10"; the printed word count 21,655 = the measured count;
  the Roif-gate naming present; no §3.32 content.

*AI disclosure: preparation, red-team passes, build, and deposit
executed by AI agents (Muse, via Muse) at the direction of
Tristen Pierson, per the standing paper rule.*

---

## Deposit entry (appended 2026-11-05, at deposit)

The owner approved the prepared texts on 2026-11-05 (the GR-088-34
approval act) and the deposit was executed the same day as a new
version (v10) of the Zenodo record series whose concept DOI is
10.5281/zenodo.20379070. **Version DOI assigned at deposit:
10.5281/zenodo.23977473** (record 23977473, state done, CC BY 4.0,
open access; the concept DOI now resolves to this version).

**Pin (per the procedure printed in §6 of the paper).** Branch
`preprint-v10-corrections-prep`, created from main `b08de0b0`.
Corrections commit `49613e18` (V10-1 + V10-2). Revision commit
`47639918` — its §6 names `b08de0b0`, the commit the revision
started from. Pin commit `94518611` on main — the deposited text
differs from the text at the revision commit in the §6 commit
string only (`b08de0b0` → `47639918`) and in no other sentence.
Deposited files: source SHA-256
`bd2d10255717d258fb77a68c856c66070fdc40f3ca1fe8b68a91b4051e8b981d`
(155,460 B; MD5 `c0135fa99c3984b5083314cfdfaa3a18`); PDF SHA-256
`33f637b192f927be28733ada8c8c04b722e9f65fd6b0b42c7d6df63e4eeb58dd`
(232,694 B; MD5 `9eefb62473233d1fa8c330e6085e2b3c`), 34 pages,
21,655 words, built with LuaLaTeX (TeX Live 2026, two passes, zero
errors) from the deposited source and no other; this note as
deposited (6,274 B; MD5 `810ddf94317f8e3a8b2ef5c16055d9c5` — the
deposited copy predates this appended entry, as with v9). Public
verification after publication: the record's file checksums match
the local files byte-for-byte, the publicly served source is
byte-identical to the deposited source, the description carries the
Version 10 paragraph, and `isNewVersionOf` names the v9 DOI
10.5281/zenodo.23668053.

One execution note, recorded plainly: the first publish attempt was
rejected by Zenodo validation because the draft's metadata carried
v9's DOI (echoed from the v9 deposition's own metadata response);
the draft was corrected to name its prereserved DOI
(10.5281/zenodo.23977473) and published once, successfully. No
duplicate version was created.
