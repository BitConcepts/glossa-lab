# Errata — `findings_W5.md` (Spec 025 material audit, 2026-10-22)

**Append-only errata, filed 2026-10-30.** This note records the forensic
identity of `findings_W5.md` in this folder. The raw file itself is
**untouched** — it is not edited, completed, or replaced by this errata,
here or anywhere else. Facts below were established by a records-integrity
investigation on 2026-10-30 (GitHub API blob reads, hash-verified; baseline
re-verified against `main` at the time of filing).

## 1. Verified identity of the damaged file

- Path: `specs/025-paper-search-research-check/audit-2026-10-22/raw/findings_W5.md`
- Size: **5,606 bytes**
- Git blob: `b31f43bccef4293f7142e16d87ff4bb5242f191e`
- SHA-256 of content: `6405d664862eeed14e60c8b8a32923029b4b44ec52d5c569b1f1eb4f24a39e8d`
- The file's literal final bytes are `…Trade and Craft` followed by the
  in-file marker `...[truncated 10309 chars]` (no trailing newline).

## 2. Born truncated — proof

The path has exactly **one** commit in its history:
`5d436362c10a8f2822b7e4c7ed7c3936bea50890` (2026-10-22T15:41:34Z, "spec 025:
material audit 2026-10-22 — stage sidecars for all 31 claims, raw evidence,
preprint v5 citation corrections"). The blob at that commit is the same
`b31f43bc…` (5,606 bytes) — byte-identical to the file on `main` today,
re-verified 2026-10-30. The truncation was therefore in the file **as
committed**; nothing was lost later. (Same failure class as the Spec 081
`wireframes.css`, likewise born truncated and repaired under its own errata.)

## 3. The cut point and the missing length

The text survives through the title/scope header (8 claims, two dossiers),
the "Source status of the two documents (Task 4)" section (§1 Roif, §2 Fuls),
and the start of "Prior-art question (a)" — and stops **mid-sentence** inside
"Nearest neighbor 1" of that section, in the title of Bahata A.
Mukhopadhyay's "Guild-Based Trading, Taxation, Tax Farming, Trade and
Craft …". Everything from mid-(a) onward is absent from this file.

The in-file marker's **10,309-char figure is the only statement of the
missing length and is not independently verifiable**; taken at face value,
the original file was ~15.9 KB. For scale, the sibling findings files are:
W1 23,214 · W2 28,379 · W3 27,902 · W4 24,990 · W6 25,609 bytes, and
`findings_W5_part2.md` 26,791 bytes.

## 4. What already stands in the record (same 2026-10-22 commit)

The audit handled this loss at the time, append-only, and disclosed it:

- **`findings_W5_part2.md`** (26,791 bytes, blob
  `74b6084a0ebf30f2f2eaaaeb7a96be44f610bd2f`) — "Findings — Worker W5,
  part 2 (reconstruction by repair worker W7, 2026-10-22)". Built **only**
  from W5's filed evidence — the 27 manual query outputs
  `raw/W5_q01…q27_*.json` plus the 8 RESEARCH-CHECK stage sidecars; no new
  searches; subsections the evidence cannot support are written as open
  gaps, not invented. It covers (a) completed — guild/economic-function
  neighbours; (b) fish sign; (c) numerals and metrology; (d) per-claim
  summaries for all 8 W5 claims (4 Roif + 4 Fuls); (e) gaps.
- **`../AUDIT_REPORT.md`** discloses the loss in its method notes: "W5's
  findings file was truncated on disk mid-sentence (its tail never
  landed). Its evidence was fully filed, so the missing part was
  reconstructed from W5's own raw outputs as `findings_W5_part2.md`,
  marked as a reconstruction; anything the filed evidence could not
  support is written there as an open gap." Its W5 sections are headed
  "W5 + W7 reconstruction" throughout, so downstream consumers were never
  misled.

## 5. The unrecoverable residue — stated plainly

**W5's original prose from the cut point onward is unrecoverable.** A
complete-source hunt on 2026-10-30 (goal workspace, all local trees, full
git history, every clone/scratch copy) found no fuller copy anywhere: every
copy is the same committed, truncated state, and the path's history holds
no earlier blob. No complete version of `findings_W5.md` exists, and none
will be fabricated — a "complete" file would invent provenance. The
part-2 reconstruction preserves the substance W5's filed evidence
supports; it is not, and does not claim to be, W5's original text.

## What this errata does not do

- `findings_W5.md` is not modified: after this note lands, its blob must
  still read `b31f43bc…`. Any future change to that blob is a new event
  requiring its own record.
- No other existing file is modified by this repair.
