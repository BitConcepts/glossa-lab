# FIXROUND.md — Fix round on the Indus paper v11 draft of record

Date: 2026-11-18. Basis: `REDTEAM.md` (independent red-team pass;
verdict NOT READY — blocker B1, should-fix S1–S5, notes N1–N7) and
the parent's adjudication of those findings.

**Input (untouched):** `pierson_2026_indus_decipherment_v11_formatted_deref.tex`,
SHA-256 `09ef1236adcc46aa820dc45c6f2ac7131401993813ec2df55a775f69af0acfd4`
(re-verified after the round: unchanged).

**Output:** `pierson_2026_indus_decipherment_v11_final.tex`, built to
`pierson_2026_indus_decipherment_preprint_v11_FINAL.pdf`, with the
rewritten version note `v11_version_note_FINAL.md`.

---

## Changes applied, in the brief's order

### 1. Axiovex identity (REDTEAM N1, owner-ordered)

- Before: `Glossa-Lab / BitConcepts LLC`
  After: `Glossa-Lab / Axiovex Systems, LLC`
- Before: `Correspondence: \texttt{tpierson@bitconcepts.tech}`
  After: `Correspondence: \texttt{research@axiovexsystems.com}`

### 2. §6 repository URLs (repository transfer executed 2026-11-18)

- Before: `https://github.com/BitConcepts/glossa-lab`
  After: `https://github.com/AXIOVEX/glossa-lab`
- Before: `https://github.com/BitConcepts/glossa-lab/tree/main/research/indus/supplemental`
  After: `https://github.com/AXIOVEX/glossa-lab/tree/main/research/indus/supplemental`

Both occurrences; a case-insensitive scan for "bitconcepts" over the
final source returns zero hits.

### 3. Head-note removal (owner-ordered; REDTEAM N1/N2)

- Removed: the entire front-matter block "**Note on the headline set
  (added in v10; updated in v11).** …" (the 161-vs-94 note, ~180
  words).
- Inserted in its place, immediately after the Version line, one
  sentence (the parent's exact text, which also carries the
  strict-core definition whose only home was the removed note —
  REDTEAM N2 item 1): "The 161 readings named in the title are the
  set this paper reports on; the program's current candidate set is
  a strict core of 94 of those readings whose recorded history never
  passed through the program's original syllabic language-model
  simulation, and it is summarized in section 5, where the
  conclusion's statements are qualified accordingly."
- §5 back-pointer: before — "…one by one (see the note at the head
  of this paper), and in light of…"; after — "…one by one, and in
  light of…". The sentence stands without the parenthetical; no
  dangling pointer remains.

### 4. S1 — printed word count

- Before: `\emph{Word count: 22,263}` (the unformatted build's
  count, carried through both transforms).
- After: `\emph{Word count: 22,159}` — measured on this round's
  final build by the note's stated method (`pdftotext | wc -w`).
  The figure was set after all other edits and the build re-run;
  the re-measured count on the final PDF is again 22,159 (the count
  line is one token either way, so the figure is stable).

### 5. S2 — dangling "§8" pointer (§2.1.1)

- Before: "this paper gives no §8 entry and no fuller bibliographic
  identification for the Dering Roll source…"
- After: "this paper gives no bibliography entry and no fuller
  bibliographic identification for the Dering Roll source…"

### 6. S3 — chronology-note exemplar (§2.1.1)

- Before: "(the frequency-curve test of §2.1.1 and the
  depicted-kinds test of §3.31.1 were both executed later in it)"
- After: "(the frequency-curve test of §2.1.1, for example, was
  executed later in it)"
- (REDTEAM's exact fix: the depicted-kinds exemplar was a different
  study silently substituted during de-referencing; it is dropped,
  not replaced.)

### 7. S4 — two bare file names to full `\texttt` locators

- §2.1 — before: "(mahadevan\_parpola\_crosswalk.json)"; after:
  "(\texttt{research/indus/mahadevan\_parpola\_crosswalk.json})"
  (matching §3.5's form).
- Appendix C — before: "Internal consistency suite
  (foundation\_check.py)"; after: "Internal consistency suite
  (\texttt{backend/scripts/foundation\_check.py})".

### 8. S5 + B1 — one pointer, one hash

- Title page — before: "…identified by the SHA-256 of its source,
  recorded in the build record (\texttt{build/build\_record.md} in
  the deposit package; see §6), not by the DOI."
  After: "…identified by the SHA-256 of its source, recorded in its
  version note (\texttt{v11\_version\_note\_FINAL.md}, filed with
  this draft; see §6), not by the DOI."
  (No `build_record.md` exists; the pointer dangled.)
- §6 already read "recorded in its version note"; it now resolves
  to `v11_version_note_FINAL.md`, which states the final source's
  SHA-256 (below). One pointer (the version note), one hash (the
  final .tex SHA-256), identifying this file.

### 9. §3.30 scorecard gloss (REDTEAM N4)

- Before: "The updated evidence scorecard, incorporating every
  study since the first scorecard."
- After: "The updated evidence scorecard, incorporating the studies
  that followed the first scorecard."

### 10. B1 — version note rewritten

`v11_version_note_FINAL.md` replaces `v11_version_note_DRAFT.md` as
the version's note. It describes the formatted + de-referenced
final draft (not the superseded unformatted draft): Status, Scope
(the two §5 corrections; the RCPH-format re-typeset; the
de-referencing with its 250 replacements and DEREF-MAP.md; the
Axiovex identity migration and repository transfer; the head-note
removal and its one-sentence replacement), the fix-round
corrections S1–S5 and N4, version mechanics, what was not changed,
and build verification with the final source identity, page count,
PDF hash, and re-measured word count. The predecessor's false
sentences (the de-referencing denial and open-question framing, the
unformatted draft's source hash, its 35-page build facts, its word
count) do not appear; a scan of the final note for the superseded
hashes returns zero.

**Not touched, per the brief:** the §3.5 withheld-study paragraph
(REDTEAM N5 — an owner decision, reserved); every other sentence of
the text.

---

## Final artifacts and hashes

| Artifact | SHA-256 |
|---|---|
| `pierson_2026_indus_decipherment_v11_final.tex` | `c05167d9091a6b14ed640189ecb19ac02a48417e2b8ceb69fc757e7dad51c62a` |
| `pierson_2026_indus_decipherment_preprint_v11_FINAL.pdf` | `5e5dfcc4dc6ce5d5c3057ec4a84be4dddbe219c9d4eb0d8881662c8498809d2a` |
| `v11_version_note_FINAL.md` | `00683e74959c745621cd8eef002699d4be96a9a2071b81cef6c067a4a4c70968` |

- Pages: **39** (the draft of record built to 40; the head-note
  removal accounts for the page).
- Word count: **22,159**, method `pdftotext | wc -w` on the final
  PDF; printed figure in the end matter equals the measured figure.
- Build: LuaLaTeX (TeX Live 2026, VM durable install), two passes on
  the final source, exit 0 both passes, **0 errors, 0 undefined
  references or citations** (build directory `build-final/`).

## Residue scan (final .tex and built PDF text)

- "BitConcepts" (any case): **0** in source, **0** in PDF text.
- Former correspondence address `tpierson@bitconcepts.tech`: **0 / 0**.
- Removed head-note block ("Note on the headline set"): **0 / 0**.
- Spec/Phase id forms in prose (excluding `\texttt` public locators
  and `\label` slugs): **0** in source; **0** in PDF text.
- GR-/WP-/claim-id forms in PDF text: **0**.
- Ordinary prose uses of the word "headline" (the paper's own
  vocabulary — "headline positional statistic", "a true SA-free
  headline cannot be computed", etc.) remain, as in v10; they are
  not note remnants.
- Verified present in the built PDF text: the Axiovex identity
  block (page 1); the one-sentence strict-core statement after the
  version line; both §6 repository URLs at the AXIOVEX address; the
  S2, S3, S4, and §3.30 replacement texts; the version-note pointer
  on the title page; "Word count: 22,159".

## Flagged for a parent decision (NOT fixed in this round)

REDTEAM S2 fixed the §2.1.1 instance and asserted all other §
pointers resolve. Two further instances of the same dangling form
survive in the final text, outside this round's brief:

- §3 comparison with CISI: "neither it nor the mayig digitization
  has a §8 entry, and this paper can give no fuller bibliographic
  identification for either from its records."
- Shu-ilishu section: "…which is the source this section relies on;
  no §8 entry covers them."

No §8 exists in the reformatted draft, so both dangle exactly as
the §2.1.1 instance did. The same one-phrase fix applies to each
("has a bibliography entry" / "no bibliography entry covers them").
Left untouched here because the brief scoped S2 to §2.1.1 and
barred other text changes; flagged so the parent can rule.

## Deposit checklist (carried forward from REDTEAM N3 — NOT this round)

1. **Title-page DOI/SHA block (the DOI lines above the Version
   line):** remove at deposit; the §6 pin supersedes it. (Its
   pointer was fixed per S5 for as long as the draft circulates.)
2. **§6 deposit-pin procedure:** at deposit, strip the procedural
   detail (named commit / pin commit mechanics) from §6, keeping
   only the one sentence naming the frozen revision commit once it
   exists; the procedure itself stays in the version note.
3. **Chronology note (end of §2.1.1):** remove at deposit (its
   remaining content is process history); S3's shrink is the
   interim form while the draft circulates.
4. Kept as they stand (REDTEAM N3): the §6 draft-provenance
   paragraph while the text circulates as a draft (replaced by the
   pin sentence at deposit, by construction); the §2.1.1
   identification-notes paragraph (with S2's fix); Appendix C's
   provenance framing; the Version line and the AI disclosure.
5. The §6 pin itself: at the deposit round, name the revision
   commit in §6's first provenance sentence per the procedure the
   paper prints, and rebuild/re-verify the deposited artifacts at
   that round.

## Addendum (parent, 2026-11-18): S2 completed for its two sibling instances

The fix round flagged two further instances of REDTEAM S2's dangling "§8 entry" form outside its briefed scope and left them untouched. The parent applied the identical one-phrase fix to both in the final source: the CISI comparison ("neither it nor the mayig digitization has a bibliography entry") and the Shu-ilishu section ("no bibliography entry covers them"). Rebuilt (LuaLaTeX x2, 0 errors, 0 undefined references, 39 pages); the word count re-measured unchanged at 22,159, so the printed count stands. Residue scan on the rebuilt PDF text: BitConcepts 0, old correspondence address 0, "§8 entry" 0. Final hashes after this addendum: final .tex SHA-256 `8c98ae3bf82065829eca3cb7f6d78344a91aa6ddf3fec8e15f112da479a1ebb8`; FINAL PDF SHA-256 `b0a4758a5f21b291cfdc56b4aac02db1da0942abb9905376ea15c0d7a942b8c8`. The version note's stated hashes were updated to these values in the same motion.
