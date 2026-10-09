# Release-Integrity Audit — Zenodo v4.2.0 Anchors Divergence

**Date:** 2026-10-08 · **Workstream:** owner-ordered program, WS3
(release-integrity audit + hash gate) · **Scope:** one file —
`INDUS_FINAL_ANCHORS.json` — in two Zenodo deposits. No deposit was
edited, no new release was made, and the anchors file was not
modified (sha256 `eccea6d5…` before and after this audit, asserted
in the ledger entry).

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.

## 1. Verdict

**(i) STAGING ERROR — the v4.2.0 deposit was built from a stale,
out-of-tree copy of the anchors file.**

The deposited copy is not any committed repo version. Its *parsed
JSON content* is exactly the anchors state of 2026-05-27 (commit
`bbecc1cd`, §3), re-serialised with CRLF line endings — a Windows
working-tree copy, not a git blob (the repo's `.gitattributes`
mandates `*.json text eol=lf`). That content had not been the repo
state since 2026-06-05, and the repo file had reached its current
content (`eccea6d5…`) on **2026-10-06, more than a day before** the
v4.2.0 deposit was created (**2026-10-07**). Verdict (ii),
legitimate-at-the-time, is falsified: there is no post-deposit
changing commit — there is no post-2026-10-06 changing commit at
all on mainline before either deposit.

## 2. The deposits, from the Zenodo records themselves

Pulled 2026-10-08 via the Zenodo API (`zenodo_api.py request()`,
`GET /records/<id>`; authenticated `custom.zenodo` route). Zenodo
stores **MD5** checksums; the sha256 values below were computed by
downloading the deposited files (public) and hashing them locally —
each download's MD5 matches its record checksum, so the downloads
are the deposited bytes.

| | v4.2.0 | v4.3.0 |
|---|---|---|
| Record ID | 23223655 | 23250395 |
| DOI | 10.5281/zenodo.23223655 | 10.5281/zenodo.23250395 |
| Concept DOI | 10.5281/zenodo.20379070 | 10.5281/zenodo.20379070 |
| Record `created` (UTC) | **2026-10-07T22:12:48Z** | 2026-10-08T23:25:25Z |
| `publication_date` | 2026-10-07 | 2026-10-08 |
| Anchors filename | `INDUS_FINAL_ANCHORS.json` | `INDUS_FINAL_ANCHORS.json` |
| Anchors size (record) | 391,969 bytes | 350,026 bytes |
| Anchors checksum (record, MD5) | `b6eb0823c52142ff79f245422f893fcc` | `00fde4dbf2ee6cbf96d020cba12ce043` |
| Anchors sha256 (downloaded & hashed) | **`841e9067a68c933d3b9511ba95f5efae23b80a5fad0f083a8eedbde6cf078fdf`** | **`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`** |

Two corrections to the program record this audit was briefed with:

1. **The v4.2.0 deposit date is 2026-10-07, not 2026-10-08** (record
   `created` 2026-10-07T22:12:48Z = 18:12 EDT; `publication_date`
   2026-10-07). The 2026-10-08 date belongs to v4.3.0.
2. v4.3.0's deposited anchors file is byte-identical to the current
   repo file (`eccea6d5…`, MD5 `00fde4db…`, 350,026 bytes, LF) — the
   v4.3.0 refresh stated in the brief is confirmed from the record.

Full v4.2.0 file list (record): `INDUS_FINAL_ANCHORS.json`,
`RELEASE_VALIDATION.json` (MD5 `41bec5db…`, 1,726 B),
`AUDIT_CORRECTIONS.json` (MD5 `31de5453…`), 
`pierson_2026_indus_preprint_v3.pdf`,
`pierson_2026_indus_harmonization_note_116.md`,
`pierson_2026_indus_decipherment_addendum_v5.md`,
`pierson_2026_indus_methods_note_111_112.md`. v4.3.0 carries the
same set plus `pierson_2026_indus_program_note_120_126.md` and a
refreshed `RELEASE_VALIDATION.json` (MD5 `e43b9b00…`, 4,162 B);
the other shared files' checksums are identical across versions.

## 3. Git history: every version, both histories

Method: for `backend/reports/INDUS_FINAL_ANCHORS.json`, enumerate
every commit on the mainline of (a) the current (twice-rewritten)
history at `origin/main` (`d9e7c501`) and (b) the pre-purge backup
mirror `glossa-lab-backup-20261008-prepurge2.git` (bare, main
`9ef78ca6`); hash each distinct blob's raw bytes with sha256. Also
scan **every blob in each object store** (`cat-file
--batch-all-objects`) for the target hash and for the target size.

Results:

- **70 distinct content versions** on each mainline; the two sets
  are identical (70/70 intersection — the rewrites preserved this
  file's contents exactly).
- **`841e9067…` matches 0 of 70 versions in either history**, and
  **no blob of size 391,969 exists in either object store**
  (12,464 blobs current / 12,726 backup scanned) — the deposited
  bytes were never committed, under this path or any other.
- **`eccea6d5…` became the content on 2026-10-06** (see timeline)
  and has not changed since, in either history.
- The deposited file's parsed JSON is **exactly equal** to the
  version at commit `bbecc1cd` (current history; `f302fa68` in the
  backup history) — *"AUDIT: Revert Phase 312 kol mass-assignment"*,
  **2026-05-27 08:44 -0400**, sha256 `569e51a7…`, 385,915 bytes:
  same top-level keys, same 605 anchors, 0 differing shared anchors.
- The byte difference from that commit is **line endings only**:
  the deposit has 6,054 CRLF line breaks and 0 bare LF; replacing
  CRLF→LF yields 385,915 bytes whose sha256 is exactly `569e51a7…`.
  (6,055 lines − 1 = 6,054 breaks = the 6,054-byte size delta.)

Substantively, the deposited content is the pre-cleanup state:
605 anchors (400 HIGH / 205 LOW — the state
`backend/scripts/release_validation.py` describes as "the audited
anchor file (400 HIGH + 205 LOW)"), with stale summary fields
(`total` 605 vs `total_all_entries` 397; `by_confidence`
{HIGH 105, MEDIUM 59, LOW 243, CANDIDATE 6} counts none of the
actual entries) and none of the later annotations — no
`reading_direction`, no `_ws3_reconciliation_note` (2026-10-05),
no `_phase109_note`, no `_phase110_note`. The current file has 287
anchors (166 HIGH / 5 MEDIUM / 3 LOW / 113 CANDIDATE).

## 4. Hash timeline

Mainline content of `backend/reports/INDUS_FINAL_ANCHORS.json`
(only the versions relevant to the divergence are listed; the full
enumeration is 70 versions, 2026-05-11 → 2026-10-06, method in §3):

| Date (UTC unless noted) | Event / commit | sha256 | Size |
|---|---|---|---|
| 2026-05-27 12:44 | `bbecc1cd` — AUDIT: Revert Phase 312 kol mass-assignment (backup-history twin `f302fa68`) — **parsed content of the future v4.2.0 deposit** | `569e51a748d9841fa3d30d14ec1f081e5718fb3ddd71fefdd24538a03e08c24f` | 385,915 |
| 2026-06-05 14:36 | `265ba7b1` — chore: update project files — deposited content **ceases to be repo content** | `3fe131da00c38bd3ce36cf2b552f8f27e7880547fe99391642895ff8f456df35` | 338,158 |
| 2026-10-05 21:35 | `2a13d4ff` — anchors bookkeeping reconciliation (spec 004 WS3/WS4) | `f2bc1d6753eba67fef65b38a4c95adeecde6e0f1947635f01f54c65029467b21` | 128,494 |
| 2026-10-06 10:38 | `b15a5ce4` — Phase-109 Step 1 | `ba99218fbeb9a2a4bc3b2965ab951053985bd234223139392927e826671bb9ee` | 184,009 |
| 2026-10-06 10:38 | `40034c96` — Phase-109 Step 2 | `a2dce3db0b39cf78654290093dc22ce191f4d1ecef07840740ef344eb4911f00` | 201,889 |
| 2026-10-06 10:38 | `5343296e` — Phase-109 Step 3 | `d3e7df7863251c8e7250bc7cb699629b8567e23c52f6732b9cbfc65b3ab17b7f` | 202,817 |
| 2026-10-06 10:41 | `90fc05b0` — Phase-109 Step 5 | `4694aaf4977b29ff9641fe50d6720f7908e3136e51028c46c707b9f92a27751f` | 203,099 |
| 2026-10-06 11:46 | `0ce70794` — Phase-110 Part B (backup/pre-rewrite twin `87d421ad`) — **current content established** | `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed` | 350,026 |
| **2026-10-07 22:12** | **Zenodo v4.2.0 deposit created** (record 23223655) | **`841e9067a68c933d3b9511ba95f5efae23b80a5fad0f083a8eedbde6cf078fdf`** (deposited) | 391,969 |
| 2026-10-08 23:25 | Zenodo v4.3.0 deposit created (record 23250395) — anchors refreshed, byte-identical to repo | `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed` | 350,026 |

## 5. Why the other verdicts fail

- **(ii) Legitimate-at-the-time** would require a commit changing
  the repo file from the deposited content to `eccea6d5…` *after*
  2026-10-07 22:12 UTC. No such commit exists: the last mainline
  change is 2026-10-06 11:46 UTC, and the deposited content had
  already left the repo on 2026-06-05. Falsified on both ends.
- **(iii) Indeterminable** is not needed: the deposited bytes were
  recovered in full, their parsed content identified with a single
  historical commit, and their byte-level divergence from that
  commit fully accounted for (CRLF, §3). Nothing material is
  missing. What cannot be determined from the available evidence
  is *which* local Windows copy / checkout the CRLF file was taken
  from, and by whom — the audit makes no claim about that.

## 6. Consequence and remedy

Anyone reusing v4.2.0's `INDUS_FINAL_ANCHORS.json` gets the
pre-audit 605-anchor state (400 HIGH incl. mass-assigned readings
later reverted/demoted), not the reconciled 287-anchor state its
version line implies. v4.3.0 already supersedes it with the correct
file; no deposit edit is made or recommended by this audit (any
such step is the owner's). The preventive remedy is the release
hash gate shipped with this audit — `backend/scripts/release_gate.py`
plus the mandatory step in `docs/RELEASE_CHECKLIST.md`: hash every
staged deposit file against its named repo source, on raw bytes,
from a clean LF checkout at a named commit, and record the gate
output in the release record before depositing.
