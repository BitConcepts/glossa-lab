# Eligibility-defs v1 — WP4's classification rules over the locator and coding records

**Spec:** 091-anchor-comparison-integrity, Stage 1, task T101.
**Claim:** C091-3 (defs side). **Version:** v1 (2026-11-17).
**Status:** filed for the stage reviewer's human-as-oracle ruling
that this document applies WP4's classes without redefining them.

## What this document is

WP4's classifier (`backend/glossa_lab/crosswalk_provenance.py`,
repair brief PR #421) classifies every Mahadevan–Parpola crosswalk
comparison by where the crosswalk value actually came from, reading
three inputs off the staged crosswalk entry: the comparator value,
its value origin, and its exact primary-source locator. On the
staged file those inputs are what they are: no entry carries an
entry-level locator for its reading fields, so no comparison can
reach `independently_sourced` and the eligible set is empty
(184 = 0 independently sourced / 6 used during candidate
construction / 116 project-derived / 7 unverified / 55 ineligible).

W1 produces two new versioned records that speak to exactly those
inputs: the **locator record** (Stage 2, T201/T202: per entry, per
reading field, an entry-level primary-source locator or a
documented locator-not-found outcome) and the **coding record**
(Stage 4, T401: per located entry, the reading coded from the
primary source by a coder outside the derivation lineage, under
the blinding protocol). This document defines, mechanically, how
WP4's unchanged rules take their inputs from those two records,
and how the eligible set is recomputed from the three records
together. It is the rule Stage 5's recomputation (T501) executes.

**The anti-redefinition guarantee.** WP4's five classes, their
meanings, their precedence order, the three-part exactness test
for a locator, the value-origin vocabulary, and the eligibility
rule (eligible ⟺ `independently_sourced`) are used exactly as
`crosswalk_provenance.py` states them; §6 maps every definition
below to the WP4 text it applies. The one mechanical property
that guards the guarantee: **over the staged records alone (no
locator record, no coding record), the recomputation of §5
reproduces WP4's classification of every entry exactly** — the
extension changes outcomes only where a new record supplies an
input the staged file lacks, and only in the direction WP4's own
rules dictate for that input.

## 1. The records and their fields (as consumed here)

- **Staged record** — the WP4 provenance record per entry
  (`backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_provenance.json`,
  frozen): the entry's four provenance blocks, its
  `comparison_classification`, and the caller-established
  construction fact behind rule 3. Consumed unchanged.
- **Locator record** — per entry (keyed by sign id), per reading
  field (`phonetic_reading`, `semantic_reading`): either a
  **locator** (§2) or a **not-found** outcome carrying the
  documented search (sources consulted, in order, with dates —
  C091-1). An entry/field pair absent from the locator record is
  treated as not examined, never as not-found.
- **Coding record** — per entry, per reading field: the coded
  value and its `source_revision`, the coder's identity and
  lineage-exclusion statement, the blinding-protocol version the
  coding was produced under, and any deviation recorded against
  it (T102's deviation rule). A coding whose deviation voids it
  (C091-2) is **void** and supplies no input (§4).

## 2. The entry-level locator definition, per reading field

WP4's definition, applied: a reading counts as located only when
the entry itself carries a locator with all three parts — the
work, a page / table / figure inside that work, and the sign
scheme the locator addresses (`crosswalk_provenance.py` module
docstring, "Exact primary-source locator"; `primary_source_locator()`).
Eligibility-defs v1 defines the locator **in the locator record**
to be exactly that triple, addressed per reading field:

- **Phonetic field locator.** A locator whose pinpoint addresses
  the entry's sign in the named work and whose cited passage
  carries the phonetic value attributed to that sign (the
  entry's `reading`/`phoneme` field in WP4's terms —
  `comparator_value()`). A locator that addresses only the
  sign-number correspondence (the sign mapping) is a locator for
  the mapping provenance, not for the phonetic reading: Appendix-B-style
  correspondence tables supply the mapping, not readings, and
  WP4's rule is applied to them exactly as WP4 applies it to the
  staged entry.
- **Semantic field locator.** The same triple, whose cited
  passage carries the meaning attributed to the sign. WP4 records
  the semantic reading as not recorded separately in every
  crosswalk entry; the locator record therefore carries a
  semantic-field outcome for every entry (locator or not-found),
  and a not-found outcome on the semantic field states that the
  primary source, as searched, does not separately attest a
  meaning for the sign — it borrows nothing from the phonetic
  string, per WP4's own reporting rule.
- A **file-level citation** (a work named for the file as a
  whole, with no entry-level pinpoint) is not a locator for
  either field (C091-1; WP4: "A bare author-year label, a file
  name, or a pointer to another in-repo table is not a
  locator").
- The locator record's locator satisfies this definition only
  if all three parts are present and non-empty **for that
  field**; a locator carried on one field supplies nothing to
  the other.

## 3. "Independently sourced" over a coding record

WP4's rule 4 class is a property of the comparator value: it is
attributed to an external source, carries an exact
primary-source locator, and was neither copied from the project
nor used during candidate construction. Over the coding record,
the comparator value for a reading field is the **coded value**,
and it is independently sourced if and only if all four hold:

1. **Located.** The locator record carries a §2 locator for
   that entry and field, and the coding record states that the
   value was coded from the primary source at that locator
   (the coding record cites the locator it coded from).
2. **Outside the lineage.** The coding record names the coder
   and carries the lineage exclusion: the coder did not derive
   the project readings and is not a member of the derivation
   lineage (C091-2; D-091-1). A coded value whose coder is in
   the lineage is not an independent input; the entry is
   recomputed as if that coding were absent (§5, step 0).
3. **Under the filed protocol, unvoided.** The coding was
   produced under the blinding protocol filed at Stage 1
   (T102) — the coding record cites the protocol version —
   and no deviation recorded against it voids it. A voided
   coding supplies no input (§4); the affected entries fall
   back to their WP4 classes (C091-2's own fallback rule).
4. **Carried byte-for-byte.** The coded value and its
   `source_revision` are carried as supplied (WP4 acceptance
   property (iii)); no normalization is applied to the value
   for classification — normalization is for reporting identity
   only, exactly as in WP4.

The construction condition (WP4 rule 3) is **not** a property
of the coding record and is not re-decided here: whether the
anchor's value was imported through the crosswalk / literature
line is the caller-established provenance fact WP4 already
consumes from the anchor's own records (its source field or
the Phase-108 provenance register), and the recomputation
consumes the same fact from the same sources. Independent
coding of a construction input's source does not launder it:
rule 3 fires before rule 4, as in WP4.

## 4. Void and absent inputs

- A **void** coding (deviation-voided, or lineage-failed under
  §3.2) is treated as absent for every purpose of §5. The
  recomputation never partially credits a void coding.
- An entry with **no locator-record outcome** for a field is
  unexamined for that field; an entry with a **not-found**
  outcome has been examined and has no locator. Both supply no
  locator input, but the distinction is preserved in the
  recomputation's output record (Stage 5 reports the census of
  examined entries separately from the eligible set, per
  C091-1's totality).
- A located field with **no coding record** supplies a locator
  but no coded value: §5 step 2 cannot fire, and the entry
  keeps the class WP4's rules give the staged value (§5).

## 5. The mechanical recomputation of the eligible set

A pure function of the three records (same records → same
eligible set, on any machine). Per entry, for the phonetic
comparison (the comparison WP4 classifies; the semantic field
is carried in the records per §2 and, exactly as in WP4, no
crosswalk entry records a semantic reading separately, so no
separate semantic classification arises):

- **Step 0 — Effective inputs.** Construct the effective entry
  WP4's rules read:
  - *Effective value:* the coding record's coded value for the
    phonetic field, if a coding exists that satisfies §3.1,
    §3.2 and §3.4's preconditions as an input (located,
    lineage-excluded, unvoided); otherwise the staged entry's
    comparator value (`comparator_value()`).
  - *Effective locator:* the locator record's §2 phonetic
    locator, if present and three-part exact; otherwise the
    staged entry's locator (none on the current staged file).
  - *Effective value origin:* `independent_primary_source`
    when the effective value is a coded value under the first
    bullet; otherwise the staged entry's origin, computed by
    WP4's `reading_value_origin()` from the staged entry's
    provenance fields (declared origin, else the Phase-96
    builder fingerprint, else locator, else in-repo secondary,
    else external-unlocated).
  - *Construction fact:* unchanged from WP4's inputs (§3).
- **Step 1 — WP4's rules, in WP4's order**, over the effective
  inputs (`classify_comparison()`'s precedence, restated
  without change):
  1. `ineligible` — the effective value is absent, or there
     is no anchor entry, or the anchor carries no reading.
  2. `project_derived` — the effective value's origin is
     `project_anchor_table_copy`. (A valid coded value's
     origin is never the project copy; a staged copied value
     keeps this class until a valid coding re-bases the
     comparison on the primary source's own attestation —
     which is the test W1 exists to run. The copy in the file
     is a fact about the file; the class is a fact about the
     value compared.)
  3. `used_during_candidate_construction` — the construction
     fact holds.
  4. `independently_sourced` — the effective value is
     externally attributed (a coded value under §3, or a
     staged value WP4 itself would so class) **and** an
     effective exact locator is present **and** neither
     rule 2 nor rule 3 fired.
  5. `unverified` — everything else: an externally attributed
     value with no effective exact locator, including a
     located-but-uncoded field (§4) and values resting on
     secondary in-repo tables.
- **Step 2 — The eligible set.** The entries classified
  `independently_sourced`, reported as produced — including
  zero, in which case C091-3's carried register falsifier
  governs (the gap re-registers as structural at Stage 6, not
  as an unfinished task).

**Worked consequences (consequences of the rules, not new
rules).** (a) A project-derived entry whose reading the locator
pass locates and the blind coder codes from the primary
source, where the anchor was not itself a construction import:
`independently_sourced` — the comparison now testifies
independently, whatever the staged file's copy did. (b) The
same entry where the anchor was imported via the Phase-51
crosswalk line: `used_during_candidate_construction` — rule 3
precedes rule 4. (c) A located entry never coded (the coder's
pass did not reach it, or its coding was voided):
`unverified` at best, and `project_derived` where the staged
value was a copy — the fallback is the WP4 class, per §4.
(d) An entry whose locator search is not-found: its class is
exactly its WP4 class over the staged record.

## 6. Mapping to WP4 (the reviewer's table)

| # | Definition here | WP4 source it applies (no text redefined) |
|---|---|---|
| D1 | The five classes and their precedence (§5 step 1) | `backend/glossa_lab/crosswalk_provenance.py` docstring lines 47–73 ("Comparison classifications"); `classify_comparison()` line 249 |
| D2 | Locator = work + page/table/figure + sign scheme, all non-empty (§2) | docstring lines 39–45 ("Exact primary-source locator"); `primary_source_locator()` line 173 |
| D3 | File-level citation is not a locator (§2) | docstring lines 43–45; C091-1 (claims.md) |
| D4 | Phonetic field = `reading`, else `phoneme` (§2) | `comparator_value()` line 161; docstring lines 28–31 |
| D5 | Semantic field never borrowed from the phonetic string (§2) | docstring lines 32–35 (provenance 4: reported not recorded) |
| D6 | Value-origin vocabulary and its derivation (§5 step 0) | `reading_value_origin()` line 200; ORIGIN_* constants lines 129–133 (module lines as read 2026-11-17) |
| D7 | Project-copy detection: declared origin or Phase-96 fingerprint (§5 rule 2) | `classify_comparison()` rule 2; `_builder_copy_fingerprint()` |
| D8 | Construction fact is caller-established from the anchor's records (§3) | docstring rule 3 (lines 60–66); `classify_entry()` parameter |
| D9 | Eligibility ⟺ `independently_sourced` (§5 step 2) | docstring lines 79–84 ("Eligibility"); `earns_independent_support()` |
| D10 | Coded value + source revision carried byte-for-byte (§3.4) | docstring acceptance property (iii) |
| D11 | Classification never depends on agreement (§5 passim) | docstring: "Classification is derived from provenance fields only — never from whether the two readings agree" |
| D12 | Void coding → fallback to WP4 classes (§4) | C091-2's fallback rule (claims.md), applied through §5 step 0's input construction |

## 7. What this document does not do

It defines the recomputation before it is run (T101's own
boundary): it does not establish that the eligible set is
non-empty, or that WP4's classes are the right classes. It
changes no class definition; any future need to change one
returns to the owner (grounding record gap 3; T003's
ratification terms). It runs nothing: the locator record is
Stage 2's, the coding record is Stage 4's, and the
recomputation over them is Stage 5's.
