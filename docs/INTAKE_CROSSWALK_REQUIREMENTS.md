# Crosswalk Adapter Requirements — what an incoming sign list must supply

Phase-130 (spec 021), deliverable 4. **Requirements only —
this document builds no crosswalk and asserts no mapping.**
It states what an incoming dataset's declared sign list
(intake schema v1, per-inscription `sign_list`) must provide
before a Phase-122-style crosswalk between that list and the
program's canonical Parpola space can be built, following
the Phase-122 crosswalk v1 model
(`reports/phase122_crosswalk_mayig.md`).

Terminology: the *incoming list* is the dataset's declared
numbering/segmentation (Parpola 1982, Mahadevan 1977, Wells,
Marshall, or an `other` list with a detail declaration); the
*map of record* is `data/crosswalks/canonical_sign_registry.csv`
(spec 018 §A2 names it the program's primary cross-system
map; the sparse `mahadevan_parpola_crosswalk_v2.json` is a
labelled source, never the map of record).

## 1. Sign-list declaration requirements

An incoming sign list is crosswalk-ready only if it supplies:

1. **Identity and version** — numbering system name, its
   publication/version, and the segmentation rules it uses
   (what counts as one sign: allograph grouping, ligature
   and variant handling, stroke-numeral treatment). The
   intake `sign_list_detail` field carries this at intake.
2. **Complete inventory** — every sign the list defines
   (not only the signs attested in the dataset), each with a
   stable ID in the list's own format, so that attested,
   unattested and unmapped signs can be counted honestly
   (Phase-122 recorded 4 unmapped P rows rather than forcing
   matches).
3. **Attestation data** — per-sign occurrence counts in the
   incoming dataset, and corpus frequency in the list's home
   corpus where available. Frequencies are rubric inputs
   (§3) and feed the spec 018 §3 conflict tie-breaks.
4. **Reading rules** — token order convention (spec 018 A1:
   sequences are taken in the source's own transcription
   order and never reversed by an adapter), the treatment of
   damaged/lost material (cf. P000, the damage marker, which
   correctly has no Mahadevan counterpart), and any
   placeholder/sentinel conventions equivalent to `UNK`.
5. **Glyph evidence where available** — sign drawings or
   image references per sign. Glyph comparison was one of
   the Phase-123 witness's recorded methods (`GLYPH`,
   `GLYPH-SEARCH-NEGATIVE`) and is the only evidence type
   that can arbitrate a split/merge question independently
   of numbering traditions.

## 2. Mapping evidence types

Every asserted pair (incoming sign ↔ Parpola sign) must
carry its evidence. Recognised types, after Phase-122 v1's
sources table:

| Evidence type | Phase-122 exemplar | Standing |
|---|---|---|
| Canonical registry assertion | `canonical_sign_registry.csv` `mahadevan_ids` per Parpola row (372 pairs) | Core source |
| Independent structured map | mayig `features/*.json` `mahadevan_graphemes` — an author's cross-match vs Parpola 1982 allographs / Wells 2015 (372 pairs) | Core source; independence from the registry is what makes agreement meaningful |
| Sourced per-entry assertion | `crosswalk_v2` entries citing e.g. Parpola 1994 App. B (171 pairs) | Labelled source only — v1 found 168 of its 171 pairs contradicting the registry+mayig consensus (it behaves near a number-identity map) |
| Number-identity inference | `candidates_unadmitted` (220 pairs, no explicit source) | Held candidates; admitted only as low-confidence rows, never silently |
| Glyph/image comparison | Phase-123 witness `correspondence_method` | Corroborating; required to arbitrate splits/merges |

A pair with no evidence type and no source is not a mapping;
it is a conjecture and must not be emitted as a row.

## 3. Confidence rubric inputs

Phase-122 v1's frozen rubric, and what an incoming list must
supply for each tier to be computable:

- **high** = attested by BOTH core sources (two independent
  structured maps). Inputs needed: the pair asserted in the
  registry (or its successor) AND in a second map whose
  compilation is demonstrably independent of the first —
  the supplier must state each map's provenance, because
  agreement between non-independent maps is not evidence.
  (In v1 the two core pair sets turned out identical,
  372/372, so every core pair is high and medium is empty —
  a finding, not an assumption.)
- **medium** = exactly one core source, uncontradicted.
  Inputs needed: the pair in one core source, plus a
  conflict check (§4) showing no other source contradicts it.
- **low** = secondary-source-only (sourced per-entry
  assertions) or candidate-only (number-identity inference).
  Inputs needed: the citing source per pair.

Usable-map rule (Phase-122 §3): coverage statistics are
computed through high+medium pairs only; low pairs are
published but excluded from the usable map, and clean /
ambiguous / unmapped token resolution is reported per token
and per inscription — ambiguity concentrated in
high-frequency signs is a property of the two lists, not a
data defect, and is reported as such.

## 4. Conflict handling

Non-negotiable, after Phase-122 v1 and spec 018 §3:

1. **Never silently resolved.** A pair contradicted by any
   source is kept on both sides and flagged `conflict`
   independently of its confidence tier (v1: 383 conflicted
   pairs across 209 P signs, published with both sides and
   their sources).
2. **No forced 1:1.** Relation types are recorded as found
   — 1:1, one-to-many, many-to-one, many-to-many (v1: 352 /
   78 / 66 / 266). Splits and merges between lists are real
   structure (the finer M-side granularity vs Parpola
   allograph grouping), not errors to be normalised away.
3. **Deterministic tie-breaks where a single map is
   required** (the harness's §3 adapter rule): highest
   `corpus_freq` wins; tie → lowest Parpola number; a
   residual tie is AMBIGUOUS — the token is emitted as the
   `UNK` sentinel and counted as ambiguous, never guessed
   (exemplar: M002, claimed by P015/P016 at equal standing).
4. **Honest unmapped.** A sign with no asserted counterpart
   is recorded as unmapped, with the reason where known
   (damage markers, list-specific signs). Unmapped +
   ambiguous share is a quality figure of the crosswalk;
   above 25% of tokens a dataset is NOT EVALUABLE under
   spec 018 §6.1.3 — a crosswalk that cannot beat that bound
   forces a spec amendment, not a silent wrong answer.
5. **Pre-recorded conflicts travel verbatim.** Unresolved
   conflicts recorded by a source (v1 carried the candidates
   file's four: M045; M006/M039/M062; M087; M047) are carried
   into the crosswalk's stats unchanged, not re-decided.

## 5. What building one would take (not authorized here)

A future phase building a crosswalk from an intake dataset
needs, beyond §§1–4: the crosswalk as versioned CSV+JSON
artifacts with a per-row `source` column; a loader module;
deterministic builder (re-runs byte-identical); coverage
recomputation tests in the Phase-122 pattern; and its own
spec. Until then, an incoming non-Parpola dataset stops at
intake Stage 5's recorded skip (see
`docs/INTAKE_RUNBOOK.md`).
