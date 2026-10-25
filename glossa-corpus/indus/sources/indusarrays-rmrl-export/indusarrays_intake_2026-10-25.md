# RMRL Indusarrays Layer (indusscript.in Firestore Export): Intake Record — Pinned in Place

**Source work:** the Indus corpus served by the Roja Muthiah Research
Library's Indus Script portal (https://indusscript.in) — a concordance
based on Mahadevan 1977 — as exported from the portal's Firestore
backend during the programme's 2026-05-14 probe of the portal.

**This holding:** the export file `firestore_indusarrays_full.jsonl`
and the probe bundle around it, held by T. Pierson on TRISTEN-DESKTOP
inside the Windows glossa-lab clone (branch `phase-next`), at
`C:\Users\trist\Development\BitConcepts\glossa-lab\glossa-corpus\indus\sources\rmrl\raw\indusscript-probe\`
(WSL path `/mnt/c/Users/trist/Development/BitConcepts/glossa-lab/…`).
The bundle was captured 2026-05-14 (file mtimes 2026-05-14, EDT). The
content is **not** committed to this repository and was **not** copied,
moved, or ingested by this intake — this record pins it in place,
metadata only.

## File of record

- `firestore_indusarrays_full.jsonl`
- Bytes: 1,938,791
- Records: 3,916 (one JSON object per line; re-counted 2026-10-25)
- SHA-256: `073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578`

## The bundle around it (same folder; all values measured 2026-10-25)

| File | Bytes | SHA-256 |
|------|------:|---------|
| firestore_indusarrays_full.json | 3,282,806 | `0a3961ace8eb81dcfa1a29c5866724439c7721407827c4253a6f064a77c534d9` |
| firestore_indusarray_extra.json | 3,294,021 | `da1a3e4d7f97d743971cfcafd50456039e94cfbfcc5d99be8b5aed2cab3bb048` |
| firestore_missing_texts.json | 3,293,902 | `460f703fa8f9728a77a1f28e0d56a33d7db6c2afa558e691c57d0e7192fa72f1` |
| indusscript.har (network capture) | 22,636,105 | — (not hashed at intake) |
| im77intro.pdf | 2,705,072 | `d146f66168b321e52ea2745a97e875cf251d8147ae0e7f2819e7d23eba77f443` |

Plus `firestore_calls.json`, `firestore_collection_analysis.json`,
`firestore_network.tsv`, `bundle_strings_analysis.json`, the portal
web-app bundle files, and rendered-page captures. Folder totals,
measured 2026-10-25: the `indusscript-probe/` folder is 41,807,016
bytes; the enclosing `rmrl/raw/` tree is 53,576,874 bytes. The
`im77intro.pdf` in the bundle is the same Mahadevan 1977 Introduction
scan recorded at `CITATIONS.md` §A.1 and pinned under
`sources/mahadevan-1977/`.

## Verification performed (2026-10-25, on the desktop, via relay)

- *Presence and path:* directory listing of the probe folder read back
  in full; the file sits at the exact path above, alongside the bundle
  contents listed in the table.
- *Hash:* SHA-256 computed on the desktop over the file itself —
  `073a83aa…a578` (full value above). This matches the value the
  2026-10-25 holdings reconciliation had already recovered and
  re-verified; the intake computation is an independent third reading.
- *Size:* 1,938,791 bytes by `stat`, agreeing with the reconciliation.
- *Record count:* re-counted two ways on the desktop (`wc -l` and a
  full line scan), both 3,916 — equal to the reconciliation's count and
  to the first of the Route 2 read script's frozen census figures
  (3,916 / 2,665 / 3,137 / 12,494). The remaining three figures are
  properties of the file's content and were **not** recomputed by this
  intake (metadata only — no content was read).
- *Git status:* `git check-ignore` on the desktop clone confirms the
  file is ignored by `glossa-corpus/.gitignore` line 12 (`sources/`);
  it has never been committed, is absent from this repository (the
  reconciliation confirmed an API 404 on main), and exists in no other
  clone.

## Status correction (the point of this record)

The programme's standing record described this layer as **lost**: the
Spec 054 execution closed on the finding that the layer was not
pinnable because the file could not be located, and the Route 2
recovery procedure was written to re-read it from indusscript.in in an
owner session. That record is **factually superseded**: the file never
left the desktop clone it was acquired into on 2026-05-14; it was
invisible to every later search because its folder is gitignored and
the searches ran against git-tracked stores.

What this correction does and does not do:

- It corrects the custody fact: the layer is **located**, pinned above.
- Spec 054's executed verdict **stands exactly as executed** — its G2
  gate failed on the facts as known at execution time. Nothing in this
  record revises the verdict, the spec's records, or the claim it bore
  on.
- The permission basis for using the layer stands exactly as recorded
  elsewhere; locating the file changes custody, not rights.
- The strict-corpus question Spec 054 bore on is re-openable on this
  held file **whenever the owner orders it** — no re-execution is
  authorised or performed by this intake.

## Custody warning

**Single-copy.** The file exists only on TRISTEN-DESKTOP's disk, in a
gitignored folder, with no second copy in any store swept by the
reconciliation. One desktop disk failure would make the "lost" record
true in fact. Whether a content copy is made, and to where, is an
**owner decision**; this intake deliberately does not make it.

## Designated use

1. The substrate for a Spec 054 re-execution, if and when the owner
   orders one (a fresh execution order against this pin).
2. The data leg of Route 2: the read script's frozen census figures
   can be checked against this held file before any owner-session
   re-read from indusscript.in is contemplated; for the data itself,
   such a re-read is very likely unnecessary.

## What this pin does not do

- It does not copy, move, mirror, or ingest the file's content,
  anywhere.
- It does not execute or re-execute Spec 054, and does not change any
  executed verdict or spec record.
- It does not settle any permission question; the basis recorded
  elsewhere stands.
