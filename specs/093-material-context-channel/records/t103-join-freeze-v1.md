# Spec 093 Stage 1 — T103 join freeze v1

Frozen 2026-11-06, before the audit run. This freeze states the
join's design, its pair-correctness criterion, its audit sample
rule, and its precision floor in advance. The audit
(`tools/spec093/run_join_audit.py`) executes exactly this
design; its record
(`records/t103-join-audit-2026-11-06.md`) reports the measured
values against this freeze. Any change to this design after the
audit runs is a new freeze version, never an edit of this one.

## 1. What the join is for

The pinned corpus snapshot (SHA-256 `08fc96c8…`, T101 census)
holds two disjoint populations: 12,423 material-bearing
museum records with no sign sequence, and 3,085 text-bearing
records with no material or holding field. A material pass
(Stage 4) can only be conditioned on objects if some records
can be connected across the two populations by identity. This
join is that connection, and its coverage bound is part of its
output, not a defect to be repaired by weaker matching.

## 2. Inputs (pinned)

- Corpus snapshot `glossa-corpus/indus/exports/indus_research.jsonl`,
  SHA-256 `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`.
- Canonical store `glossa-corpus/indus/canonical/objects.jsonl`,
  SHA-256 `e24f42a95ee4cc1fdb16c789c3edfb937993ed7c82223d6daa96d66895174ae5`
  (the snapshot's records are a strict subset; the canonical
  store carries the key fields the export dropped).
- CISI data-list compilation
  `backend/glossa_lab/data/yajnadevam_inscriptions.csv`,
  SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`
  (5,679 rows; a third-party compilation of the CISI data
  lists — see §7 for its trust bound).

## 3. Key families

**K1 — cross-population exact keys.** Within the canonical
store, join a material-bearing record to a text-bearing record
when a key-shaped field is byte-equal on both sides. The
candidate fields, fixed by the T101 census: `accession_number`
(present only on the museum side — it can produce no pairs,
and is recorded as such) and `source_object_id`. No
normalization, no fuzzy matching: byte equality only.

**K2 — CISI catalogue concordance.** The canonical store's
mayig-cisi records carry `source_object_id` values of the form
`<catalogue number><side suffix>` (e.g. `M-1A`), where the
suffix is the inscribed side of the object. Normalization
(frozen): strip exactly one trailing `A` or `B` when it
immediately follows a digit; the result is the object
catalogue number. Join to the CSV's `cisi` column by byte
equality of the normalized number; the CSV value is read with
surrounding whitespace stripped (a catalogue number contains
no whitespace; measured before this freeze was executed: 2 of
5,018 non-empty `cisi` values carry a trailing space — `L-78 `
and `M-929 ` — and neither is in the snapshot's CISI slice, so
the clause decides no pair in this audit). The join delivers, per
text-bearing record, the CSV row's data-list fields:
`material`, `site`, `period`, `type`, `area-section`,
`excavation-idno`, and the three dimension fields.

## 4. Pair-correctness criterion (frozen)

A produced pair is CORRECT iff affirmative identification
evidence in the two records establishes that they denote the
same physical object:

- K2: (a) the normalized catalogue numbers are equal;
  (b) the key is 1:1 — exactly one CSV row and exactly one
  snapshot record carry the number (a catalogue number
  consumed by more than one pair, or a CSV row matched by
  more than one record, makes every pair on that number
  incorrect, because no principled choice among them exists);
  (c) site-prefix consistency — the CSV row's `site` is the
  site the catalogue prefix denotes (`M` = Mohenjo-daro);
  (d) type consistency — the CSV row's `type` is in the SEAL
  family and the snapshot record's `artifact_type` is `seal`.
- K1: the shared value is an identifier of the object in BOTH
  namespaces, AND at least one corroborating field agrees:
  equal non-empty `site_name`, or the museum record's
  provenience naming the text record's site, or a second
  shared identifier (accession or image URI). A bare value
  collision across namespaces with no corroboration is
  incorrect under this criterion — the two namespaces are
  known to be different numbering systems (Penn registration
  numbers; Mahadevan text indices), so equality alone is not
  identification evidence.

## 5. Diagnostics (frozen as diagnostics, never criteria)

Reported, never used to accept or reject a pair: sign-count
agreement between the two digitizations (the CSV's `text
length` and `text` token count against the mayig record's
`sign_instance_count` and diplomatic-code token count), and
the error census in three classes: (a) false pairs (identity
failures under §4), (b) content disagreements among true
pairs, (c) count-field artifacts (a count field disagreeing
with its own file's tokens). The audit does NOT compare sign
sequences across the two files: the CSV's `text` uses a third
sign numbering that is neither Parpola's nor Mahadevan's, and
comparing sequences across numberings without a crosswalk
would move evidence between channels (hard constraint H1).

## 6. Sample rule and floor (frozen)

- Any key family producing 200 pairs or fewer is audited by
  complete enumeration: every produced pair is adjudicated
  individually against §4, and every exception is listed in
  the audit record. (Both families are expected to fall under
  this rule; if a family produced more, the audit takes a
  seeded sample of 200, seed `093-t103-v1`, and says so.)
- **Floor: identity precision ≥ 0.90 per key family**,
  precision = correct pairs / produced pairs under §4.
- A family below the floor is REJECTED: its pairs are not
  join output. The join consists of the accepted families'
  pairs only. **If no family passes, the material arm stops
  here, and the recorded stop is the T103 outcome** (the
  spec's honest-stop rule); no weaker matching may be
  substituted inside this freeze.

## 7. Bounds stated on the freeze's face

- The CSV is a third-party compilation of the CISI data
  lists. Under the standing CISI restriction its statistics
  and data-list fields are publishable; no CISI scan or image
  is involved or redistributed. The compilation's `text`,
  `sanskrit`, and `translation` columns — its claimed-readings
  layer — are never consumed by the join or the audit.
- The join's coverage is whatever its keys cover. The census
  establishes in advance that the Mahadevan (indusscript-m77)
  population has no in-repo concordance: K2 can cover at most
  the 179-record CISI slice, one site. That bound is reported
  with the result, not repaired.
- The join delivers the CSV's material values RAW (23 distinct
  values). Normalizing them is outside the T102 register,
  which is bound to the pinned snapshot's values; a Stage 4
  pass over this join needs its own register version or
  amendment first.
- This freeze does not establish that the joined fields are
  accurate descriptions of the objects — only that the pairs
  are identified to the frozen criterion. Content
  disagreements among true pairs are censused (§5), not
  adjudicated away.
