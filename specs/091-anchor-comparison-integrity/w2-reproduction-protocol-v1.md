# W2 reproduction protocol v1 — outside reproduction over the 46 internal-only strict anchors

**Spec:** 091-anchor-comparison-integrity, Stage 1, task T103.
**Claim:** C091-5 (protocol side). **Version:** v1 (2026-11-17).
**Status:** filed before the pass starts, as C091-5 requires.
Engaging the readers is the owner's D-091-1 act; this filing
contacts nobody and establishes the standard the pass is
judged against (compliance is Stage 4's oracle act, T402).

## 1. Population

The pass covers all **46** strict anchors the WP5 audit
classes `supported_internal_only`
(`docs/repair-2026-10-26/anchor-support-audit.json`, audit_id
`repair-2026-10-26-wp5-anchor-support-audit`). The census is
46 accounted of 46: every one of the 46 carries a recorded
outcome under §4, including failures and non-attempts with
their reasons. The 6 independently supported anchors
(M044, M047, M124, M202, M329, M330) are not in the
population; no anchor outside the 46 is in it.

## 2. The two routes, per anchor

For each anchor, the outside attempt takes one of two routes,
chosen per anchor before the attempt starts and recorded
with the outcome:

- **Independent attestation.** A reader outside the anchor's
  derivation lineage attests the anchor's reading from
  sources outside the program's derivation: the reader
  examines the reading as proposed and records whether an
  external source line supports it, naming the source at
  entry level (work, pinpoint, sign scheme — the locator
  standard of eligibility-defs v1 §2). An attestation that
  rests on the program's own publications or on material the
  program derived is not an attestation under this route; it
  is a same-lineage re-examination and changes nothing
  (C091-6).
- **Blind re-derivation.** A reader outside the anchor's
  derivation lineage derives the reading afresh from the
  primary material (the corpus evidence and the published
  sources for the sign), **without** being shown the
  project's derivation or its conclusion, under the blinding
  discipline of §3. The reader's derived value is recorded
  byte-for-byte as produced. Agreement or disagreement with
  the project's reading is computed from the filed records
  afterwards, never during the derivation.

An anchor may receive both routes; each route's outcome is
recorded separately. A route not attempted for an anchor is
recorded as not attempted, with the reason (for example: no
reader engaged for that anchor — the D-091-1 act outstanding).

## 3. Blinding and lineage exclusion

- **Reader lineage exclusion.** A reader for an anchor must
  not have produced, and must not have worked from, that
  anchor's original derivation, and must not be an author of
  the derivation line the anchor rests on (the audit's
  `original_derivation` record names the lineage per anchor).
  The reader's identity and lineage-exclusion statement are
  recorded per anchor, as in the coding record of W1
  (eligibility-defs v1 §3.2 consumes the same fields).
- **Blind re-derivation blinding.** The re-deriving reader
  sees the primary material and the sign list; they do not
  see the project's reading for the anchor, its derivation,
  its audit class, or any other reader's outcome, until
  their derivation is filed. The filing act, and the
  deviation rule of the blinding protocol
  (`blinding-protocol-v1.md` §§5–6) applied per anchor,
  govern: a deviation voids the derivation it touches,
  which is then redone by a still-blind reader or recorded
  as attempted and not landed with the deviation as its
  reason.
- **Attestation** is not blind (the attester examines the
  proposed reading), but the attester must not be shown the
  project's derivation trail or audit class: the attestation
  judges the reading against external sources, not against
  the program's own account of itself.

## 4. Outcome vocabulary (the complete set)

Per anchor, per route, exactly one outcome is recorded:

| Outcome | Meaning |
|---|---|
| `external_line_landed` | The route produced a filed external support line: an attestation naming its external source at entry level, or a blind re-derivation whose filed value agrees with the anchor's reading (agreement under the program's recorded normalization, computed from the filed records). |
| `external_line_attempted_not_landed` | The route was executed under this protocol and produced no external line: the attester found no external source supporting the reading; the re-derivation's filed value disagrees; the derivation was voided by a recorded deviation and not redone; or the reader reports the material insufficient to derive from. The attempt's record (what was examined, what was produced) is filed either way. |
| `not_attempted_with_reason` | The route was not executed for this anchor. The reason is recorded (no reader engaged; reader engaged but unavailable; the anchor's material not yet assembled). "Pending" without a reason is not an outcome. |

No fourth outcome exists. In particular there is no outcome
in which an anchor's class moves on same-lineage material:
class changes are Stage 5's recomputation over landed lines
only (C091-6), and this protocol's records are its inputs.

## 5. The per-anchor record

For each of the 46, the pass files: the anchor's sign id; the
route or routes attempted; the reader's identity and
lineage-exclusion statement per route; the outcome per
route; for a landed attestation, the external source's
entry-level locator; for a re-derivation, the filed derived
value and its source revision, byte-for-byte; any deviation
and its handling. The record is the evidence; an outcome
with no record does not exist (C091-5's falsifier: "an
outcome recorded with no protocol on record" — this document
is that protocol, and each outcome names it by version).

## 6. Mapping to the ratified record (the reviewer's table)

| # | Protocol element | Source it restates |
|---|---|---|
| Q1 | Population = the WP5 audit's 46 `supported_internal_only` anchors; census 46 of 46 (§1) | C091-5; spec.md W2; grounding record (46 = GRAMMAR 20 / DEDR 17 / ICONOGRAPHIC 4 / MIXED 2 / CROSSWALK_CORPUS 2 / LITERATURE 1) |
| Q2 | Two routes: independent attestation or blind re-derivation (§2) | C091-5: "independent attestation or blind re-derivation by readers who did not produce the original derivations"; register GR-088-02 candidate |
| Q3 | Reader lineage exclusion (§3) | C091-5 falsifier: "an attempt by a reader inside the anchor's derivation lineage"; D-091-1 |
| Q4 | Outcome vocabulary: landed / attempted-not-landed / not-attempted-with-reason (§4) | C091-5: "external line landed, external line attempted and not landed, or not attempted with the reason"; plan.md Stage 1 |
| Q5 | Classes move only on landed lines, at recomputation (§4) | C091-6 |
| Q6 | Engagement is the owner's act; the protocol contacts nobody (§header) | D-091-1; spec.md non-goal "No contact without the owner's act" |
