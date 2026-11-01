# Custody addendum — owner-side second copies (red team E-8), 2026-10-25

Programme red team 2026-10-25, finding E-8: several holdings existed as a
single copy on a single machine. Under the owner's order of 2026-10-25
17:23 EDT, verified second copies were created on the owner's other
machine for every holding listed below. This addendum is the custody
record: metadata only. No holding content is in git.

Method, in plain terms: each holding was packed (for folders, a
deterministic tar with a per-file manifest of SHA-256 hashes), moved
between the owner's two machines over the owner's desktop relay only,
and the receiving side re-checked the SHA-256 of the whole package and
of every file inside it before the copy was accepted. A copy is listed
here only where both checks passed. Originals were not modified or
deleted; copies are additive. CISI material (image layer, 3.1 portion,
IA scans, ICIT-derived stores) stayed on the owner's two machines in
restricted folders throughout: never uploaded to any third-party
service, never in git, never redistributed.

Excluded by the owner's brief and not touched by this work: the
indusarrays / indusscript-probe bundle (firestore_indusarrays_full.jsonl
— covered separately, PR #404). The four sibling files of that probe
folder were added to this addendum's scope by the parent agent's note
of 2026-10-25 18:29 EDT and are recorded in section B2.

Machines: "VM" = the owner's Muse VM (paths under /home/hatch/workspace).
"Desktop" = TRISTEN-DESKTOP (WSL2 user tpierson, Windows user trist).

## A. Copies made VM → Desktop

Desktop root for all section-A copies:
~/glossa-custody/copies-from-vm/2026-10-25/ (TRISTEN-DESKTOP, restricted folder)

### A1. Shakti deposit + row grades (brief item 1)
- Source (VM): research_notes/indus-data-deep-sweep-20261008/downloads/shaktiosindia-indus-sign-regimes-deposit/
  plus shakti_row_grades_2026-10-22.csv (located in the same downloads folder)
- Copy (Desktop): item1-shakti/ under the root above
- Files: 58; source bytes: 3,254,536; package: 688,859 B
- Package SHA-256: 330abac5b75c0bbd262a7ce1447d51184d9123bec2a6613eabb2fd62dc763852
- Verified: package hash + all 58 manifest hashes, 2026-10-25

### A2. CISI 3.1 portion (brief item 2) — RESTRICTED
- Source (VM): research_notes/indus-data-deep-sweep-20261008/downloads/oakland-ill-cisi31-portion/
- Copy (Desktop): item2-cisi31-portion/
- Files: 120; source bytes: 102,681,865; package: 100,250,977 B
- Package SHA-256: c400de0558495a0dd7d9f177d52cff84dd614e066982bca8339d5cec3b958621
- Verified: package hash + all 120 manifest hashes, 2026-10-25

### A3. CISI image layer (brief item 3) — RESTRICTED
- Source (VM): glossa-lab/corpora/downloads/cisi_image_layer/
- Copy (Desktop): item3-cisi-image-layer/
- Files: 18,056; source bytes: 870,884,730; package: 859,481,441 B
- Package SHA-256: bcfd1ecb683cd92a9b0382b86f1cdcddcc275c5378a8cf7dde7d493650b0c1f9
- Verified: package hash + all 18,056 manifest hashes, 2026-10-25

### A4. CISI IA scans + MASI 86 (brief item 4)
- Source (VM): research_notes/indus-data-deep-sweep-20261008/downloads/cisi-1-ia-scan/,
  cisi-2-ia-scan/, and masi-86-ia-scan/ (a second digitisation of Vol. 1,
  the register's DUPLICATED-1 — copied as briefed)
- Copy (Desktop): item4-ia-scans/
- Files: 6; source bytes: 96,072,975; package: 90,809,673 B
- Package SHA-256: acfa322052071313f8fb838da4e3dbe7eb74f3f256adc7408bbf524df7e43e17
- Verified: package hash + all 6 manifest hashes, 2026-10-25

### A5. Field-Cady / mayig stores (brief item 5)
- A5a field_cady_icit — Source (VM): glossa-lab/corpora/downloads/field_cady_icit/;
  Copy (Desktop): item5a-field-cady-icit/; Files: 628; bytes: 2,574,432;
  Package SHA-256: cc630469d7a5c89e3c747314f7893b1a368f6727f67bfb313d7930985e7e458d
- A5b icit_fieldcady — Source (VM): glossa-lab/corpora/downloads/icit_fieldcady/;
  Copy (Desktop): item5b-icit-fieldcady/; Files: 3; bytes: 1,740,274;
  Package SHA-256: 3c0b1d35b35aec3be499004f45a80a77f33f63b6cde16e017f87ea272c52651d
- A5c mayig_indus_valley — Source (VM): glossa-lab/corpora/downloads/mayig_indus_valley/;
  Copy (Desktop): item5c-mayig-indus-valley/; Files: 608; bytes: 867,897;
  Package SHA-256: ae16034f32ad83b3c6c0470cdef06e67088ffdca0ab20589bd6d2aa05bc20597
- A5d mayig_cisi layer file — Source (VM): glossa-lab/data/corpus_layers/mayig_cisi_layer_v1.json;
  Copy (Desktop): item5d-mayig-cisi-layer/; Files: 1; bytes: 102,003;
  Package SHA-256: 6646581894f58b9828e090691431cba048b2c5d7d04e3278e00880954c41a307
- A5e restricted-local store — RESTRICTED (ICIT-derived)
  Source (VM): glossa-lab/glossa-corpus/indus/sources/restricted-local/;
  Copy (Desktop): item5e-restricted-local-icit/; Files: 6; bytes: 4,754,040;
  Package SHA-256: 3846f607cc3c4d98f6915068fea36238fc0ea85d9c774f57d261dfab7833473e
- All A5 items verified: package hash + full manifest hashes, 2026-10-25

## B. Copies made Desktop → VM

VM root for section-B copies:
~/workspace/glossa-custody-e8/copies-from-desktop/ (Muse VM)

### B1. Fuls print corpus + MASI 77 (brief items 6–7)
- Fuls Vol. I — Source (Desktop): C:\Users\trist\OneDrive\Documents\My Kindle Content\Corpus of Indus Inscriptions.pdf
  Copy (VM): copies-from-desktop/fuls-print-corpus/Corpus of Indus Inscriptions.pdf
  Bytes: 285,116,101; SHA-256: 185fd0575d881568583a7002d705b2ded1313a525fafe093108f72e0fe897727
  (matches the holdings register pin; verified on receipt, 2026-10-25)
- Fuls Vol. II — Source (Desktop): C:\Users\trist\OneDrive\Documents\My Kindle Content\A Catalog of Indus Signs.pdf
  Copy (VM): copies-from-desktop/fuls-print-corpus/A Catalog of Indus Signs.pdf
  Bytes: 274,176,439; SHA-256: 31729a4f7b33bd1ec08633bb677f963b5de8f50d96afdfc25cff5ddc96f9a32a
  (matches the holdings register pin; verified on receipt, 2026-10-25)
- MASI 77 full volume — Source (Desktop): C:\Users\trist\Downloads\MASI 77 Indus Script Texts Concordances & Tables Iravatham Mahadevan.pdf
  Copy (VM): copies-from-desktop/mahadevan-1977-full-volume/MASI 77 Indus Script Texts Concordances & Tables Iravatham Mahadevan.pdf
  Bytes: 16,445,165; SHA-256: ef68fe8dc25e94fe9cb75b418c5189a084383e72498560ef393372e90a27e110
  (matches the intake pin of PR #390; verified on receipt, 2026-10-25)

### B2. Indusscript-probe sibling files (added 2026-10-25 18:29 EDT)
- Source (Desktop, all four): C:\Users\trist\Development\BitConcepts\glossa-lab\glossa-corpus\indus\sources\rmrl\raw\indusscript-probe\
- Copy (VM, all four): copies-from-desktop/indusscript-probe-siblings/
- firestore_indusarrays_full.json — Bytes: 3,282,806; SHA-256: 0a3961ace8eb81dcfa1a29c5866724439c7721407827c4253a6f064a77c534d9
- firestore_indusarray_extra.json — Bytes: 3,294,021; SHA-256: da1a3e4d7f97d743971cfcafd50456039e94cfbfcc5d99be8b5aed2cab3bb048
- firestore_missing_texts.json — Bytes: 3,293,902; SHA-256: 460f703fa8f9728a77a1f28e0d56a33d7db6c2afa558e691c57d0e7192fa72f1
- indusscript.har — Bytes: 22,636,105; SHA-256: 8d1061c4f0a0fabf70da8be1709ac5c2f6ece3df2b2515cbe8ec61e0a26133b8
- Each file's SHA-256 was computed on the Desktop before transfer and
  matched byte-for-byte on the VM copy, 2026-10-25. (The fifth sibling,
  im77intro.pdf, was not named in the addition and was not copied.)

## What this does not establish
- This addendum establishes second-copy custody and hash identity only.
  It says nothing about the correctness, completeness, or provenance of
  the holdings' contents, which remain as recorded in each source's own
  intake/provenance records.
- Transfer packages transited the owner's private desktop-relay repo in
  encoded chunks during the move; the relay repo is a transfer channel,
  not a custody location, and no holding is considered "copied" to it.
