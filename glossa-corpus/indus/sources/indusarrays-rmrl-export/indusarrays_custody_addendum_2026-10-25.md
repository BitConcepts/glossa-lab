# RMRL Indusarrays Layer: Custody Addendum — Second Copy Located by Search, Then Created

**Date:** 2026-10-25 (search and creation executed the same day as the
intake pin, PR #393).
**Owner directive:** "Do your recommended actions. And find the custody
copy, we must have it somewhere perhaps even git history."
**File of record:** `firestore_indusarrays_full.jsonl` — 1,938,791
bytes, 3,916 records, SHA-256
`073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578`
(the pin in `provenance.yaml` in this directory).

## Outcome

No second copy of the file — nor of any sibling in the probe bundle —
was found in any store or history searched (the full list is below).
The owner's hypothesis that a copy might survive in git history was
tested directly and is **ruled out**: in every glossa-lab object store
searched, on both machines and in the current GitHub history, there is
no blob of the file's size (nor of any sibling's size) and no tree
entry under any of the bundle's filenames. The only committed relative
is the derived staging file
`glossa-corpus/indus/staging/objects_2026-05-14_indusarrays.jsonl`
(blob `2931bc3c…`), a processed build made from the layer — evidence
the layer was used, not a copy of it.

Because no custody copy existed, one was **created** under the
directive, on 2026-10-25. Custody for the file of record is now
**RESOLVED: two copies, two machines**, both hash-verified against
the pin:

| Copy | Location | SHA-256 |
|------|----------|---------|
| 1 — original | TRISTEN-DESKTOP: `C:\Users\trist\Development\BitConcepts\glossa-lab\glossa-corpus\indus\sources\rmrl\raw\indusscript-probe\firestore_indusarrays_full.jsonl` (Windows clone, branch `phase-next`; gitignored) | `073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578` |
| 2 — custody copy (created 2026-10-25) | VM (this machine's local checkout sources store): `~/workspace/glossa-lab/glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl` — the same relative path as the original, inside the gitignored sources store (`glossa-corpus/.gitignore` line 12, `sources/`), so the file itself is not in git | `073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578` |

## How copy 2 was made and verified

- The original was re-hashed on TRISTEN-DESKTOP immediately before
  transfer: SHA-256 equal to the pin, size 1,938,791 bytes.
- Transfer ran over the desktop relay: the file was gzip-compressed on
  the desktop (187,609 bytes; SHA-256
  `9e483aeecda236723128c4da50a709f94141749377c6a8f28307b3e2cdedc8d2`),
  base64-encoded, and carried in three parts, each under the relay's
  100 KiB stdout cap and each received untruncated (90,000 / 90,000 /
  70,148 characters).
- On the VM the payload was reassembled and the gzip hash re-verified
  before decompression. The decompressed file measures 1,938,791
  bytes, 3,916 lines, SHA-256 equal to the pin. The copy at its
  destination path was then hashed a final time in place: equal to
  the pin.
- The local checkout's tracked state was proven untouched: `git
  status --porcelain` before and after the write is identical (13
  pre-existing modified entries, none near the sources store); the
  new tree appears only as an ignored path (`!!`).

## Stores and histories searched (all negative for the target and its siblings)

Target sizes searched for, by name and by exact byte size, were the
file of record (1,938,791) and its siblings
`firestore_indusarrays_full.json` (3,282,806),
`firestore_indusarray_extra.json` (3,294,021),
`firestore_missing_texts.json` (3,293,902) and `indusscript.har`
(22,636,105). Exact-size searching was functionally validated on the
desktop against the bundle's own files before its results were
trusted.

1. **Git history, VM:** all 52 distinct glossa-lab object stores on
   the VM (the local checkout, every worktree clone under
   `~/workspace`, the bare mirror `glossa-run/verify-remote.git`) —
   every blob in every store listed by size via `cat-file
   --batch-all-objects` (no blob of any target size), and every
   reachable tree entry listed via `rev-list --objects --all`
   (matches only for the probe *scripts*, the acquisition report, and
   the derived staging file named above). The desktop-relay
   repository's local object store was scanned the same way.
2. **Git history, TRISTEN-DESKTOP:** all seven glossa-lab clones (the
   Windows clone and WSL clones glossa-lab-423, glossa-lab-424,
   g4-pristine, gl047-merge, gl057-merge, glossa-048-fc) — same
   size-and-name object scan, no hits.
3. **Git history, GitHub (current remote):** the reachable history of
   `BitConcepts/glossa-lab` as mirrored by the local full clones and
   the bare mirror in (1), plus a trees-only clone of the current
   remote — no tree entry for any bundle filename under any path.
   (This covers the post-purge history; pre-purge history is what the
   local clones in (1) preserve, and they are negative too.)
4. **VM filesystem:** filename search across all of `~/workspace`
   and `/tmp` (no match); an exact-size walk of `~/workspace` plus
   `~/Downloads` and `~/Documents` (no file of any target size); a
   content-signature search for the records' own marker
   (`projects/theindusscript/databases/(default)/documents/indusarrays/`)
   across the glossa stores — the only matches are the Route 2 read
   tooling's small synthetic test fixtures, not corpus data; the two
   archive files in the corpus stores (mayig and Field-Cady zips) list
   no bundle entries.
5. **Desktop filesystem:** a name search and five exact-size searches
   across the WSL home (no match; the original is not in the WSL
   home). On the Windows side, the same day's holdings reconciliation
   had already inventoried all seven clones file-by-file and listed
   Downloads, the Kindle content and OneDrive in full: the file
   appears only at the original path in all of it. As a final
   redundant pass, a single-traversal size-and-name dump of the whole
   Windows user profile `C:\Users\trist` (AppData pruned, as in every
   sweep of this programme) was run and filtered for all five sizes
   and all bundle name patterns, excluding the original probe folder.
   [CUSTODY3-RESULT]
6. **Cloud-adjacent listings:** OSF project `nrb9u` storage is empty
   (0 files), so no registration snapshot holds a copy. All 25 Zenodo
   depositions on the programme's account were listed by filename and
   size — no bundle filename and no target size appears.

## What this addendum does not change

- The permission basis for the layer's use stands exactly as recorded
  in the intake; this addendum is about custody, not rights.
- Spec 054's executed verdict stands exactly as executed.
- The bundle's **siblings remain single-copy** on TRISTEN-DESKTOP
  (the three sibling exports and the `.har` capture). The directive's
  target was the file of record; copying the siblings is the same
  operation whenever the owner wants it, and the method above is
  proven at this size.
