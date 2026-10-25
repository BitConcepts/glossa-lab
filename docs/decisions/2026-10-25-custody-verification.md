# Custody verification — 2026-10-25 (realignment item 3.3)

Executed 2026-10-25 under the owner-approved realignment package
(finding RT-11: the gitignored-layer pattern has killed four datasets;
pins prove a file's identity but do not preserve the file). Each layer
below was verified first-hand on this date: the checksum recomputed on
the holding machine and compared to the pin of record.

| Layer | Pin of record (SHA-256) | Location verified 2026-10-25 | Result | Second location |
|---|---|---|---|---|
| Shakti corpus (`sanitized_corpus.json`, 1,570,041 bytes) | `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68` (intake record, 2026-10-22) | Owner's VM, restricted downloads tree | **VERIFIED** — recomputed hash equals the pin | **UNVERIFIED — no second copy found.** Searched the owner's desktop (WSL home, the Spec 062 grid tree, targeted user-tree search; a full user-tree search timed out). Creating one over the desktop-relay route would put the file in a git repository, which its holding terms forbid ("never in git"). An owner-side local copy (desktop, outside any repo) is the conforming remedy and is recommended. |
| Shakti row-grades (`shakti_row_grades_2026-10-22.csv`) | `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739` (intake record) | Owner's VM, beside the corpus | **VERIFIED** — recomputed hash equals the pin | **UNVERIFIED — no second copy found** (same search and same remedy as the corpus). |
| Fuls Vol. I — *Corpus of Indus Inscriptions* (PDF, 285,116,101 bytes) | `185fd0575d881568583a7002d705b2ded1313a525fafe093108f72e0fe897727` (provenance record, 2026-10-22) | TRISTEN-DESKTOP, owner's Kindle library folder | **VERIFIED** — hash recomputed on the desktop 2026-10-25 (detached job, log read back through the relay) equals the pin | Single copy by design: the PDFs stay on the desktop (too large for the relay route); the pin + this re-verification are the custody record. |
| Fuls Vol. II — *A Catalog of Indus Signs* (PDF, 274,176,439 bytes) | `31729a4f7b33bd1ec08633bb677f963b5de8f50d96afdfc25cff5ddc96f9a32a` (provenance record, 2026-10-22) | TRISTEN-DESKTOP, owner's Kindle library folder | **VERIFIED** — same act as Vol. I; hash equals the pin | Single copy by design, as Vol. I. |
| CISI Vol. 3.1 "Basic data" portion copy (PDF, 8,206,446 bytes; restricted ILL-supplied portion) | `514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a` (intake receipt verification, 2026-10-20) | Owner's VM, restricted downloads tree | **VERIFIED** — recomputed hash equals the pin | **UNVERIFIED — no second copy found** (same desktop search). Its intake terms prohibit uploading or sharing copies, so no relay transfer was attempted; an owner-side local copy on the desktop is the only conforming remedy. |
| indusarrays layer (indusscript.in Firestore export) | Census pin: 3,916 records / 2,665 dockeys / 3,137 sequences / 12,494 instances (Spec 054 freeze) | — | **LOST before this run** (RT-11) — re-acquisition is Route 2, prepared 2026-10-24, awaiting the owner's session act and permission basis; out of scope here | — |
| Fuls Catalog derived JSONs (behind Spec 057's pins) | Hash pins in the Spec 057 record | — | **LOST** (recorded 2026-10-22 salvage; derived CSVs and pins survive) | — |
| Holdat LLC v3 raw download | — | — | **LOST** (workspace copy gone; Specs 043/044 re-pointed to substitutes in their own records). The corpus CSV the foundation check reads survives in the programme's local checkout tree and was read successfully on this date | — |
| ICIT website CSVs (behind Spec 064's identification) | — | — | **LOST** (recorded as the cause of Spec 064's identification failure) | — |
| Asset A v2 (552-row depicted-kind table, Spec 073) | SHA-256 + per-row citation log in the repo | — | **UNVERIFIED in this run** — the file's holding location was not established from the records available to this act; the repo carries its hash and citation log only (RT-10) | Not established |

## What this does and does not establish

Verified here: five held files are byte-identical to their pins on
the machines that hold them, checked on 2026-10-25. Not established:
protection against loss. Three of the five remain single-copy, and
for two of them the programme's own holding terms rule out the only
transfer route available to this act — that residual is named, with
the owner-side remedy, rather than rounded up to "backed up".

Standing rule adopted with this record (from RT-11's mitigation): a
freeze may not proceed on an input with a single copy unless the
freeze record states that fact as an accepted risk.

## Note on the in-repo provenance stubs (item 3.3(ii))

The May-2026 acquisition stubs under `glossa-corpus/indus/sources/`
are not edited by this act: at least one of them (the CISI source
record) is cited by a frozen spec record and hash-pinned by its
freeze test (`test_spec052_freeze.py::test_cited_records_carry_the_design_facts`,
which failed on an appended custody block during this act's first
pass and passes with the file untouched). The verified state of the
held layers therefore lives in this custody record, which supersedes
the stubs as the statement of what is held; the stubs stand as
acquisition history.
