# Scan plan — Spec 088 Stage 5 (three clusters)

The scans run over the **generated** map (S2's artifacts + find list),
never over prose. Each cluster produces one scan record
(`records/scan-<cluster>.md` in the spec directory). This plan fixes the
template, the inputs, and the legs that are already answered from records
— a scan cites a pre-answered leg from its record; it does not re-derive
it, and it does not spend its effort re-proving what the program already
knows.

## The four-kind template (verbatim, in Glossa terms)

Every find a scan records is exactly one of these four kinds (RCPH's
template, translated):

1. **Missing node** — work the picture needs that has no node: a study
   never run, a claim family never extracted, a corpus never keyed, a
   comparison never made. (Example shape: an extracted document whose
   claims no study has ever taken up.)
2. **Missing edge** — two nodes exist but the relation between them was
   never built or never recorded: a study whose result no successor
   consumed, a claim family with no edge to the anchors it bears on, an
   outside literature result never tied to the claims it would confirm or
   contradict.
3. **Thin evidence** — a node stands on few, weak, or circular supports:
   standings resting on a single arm, support classes dominated by
   internal-only derivations, falsifiers absent. Thinness is counted from
   the map's own fields and the cited censuses, not impressionistically.
4. **Stale bookkeeping** — the records disagree with each other or with
   the territory: standings that exist only in prose (C2 finds),
   directories with no claims (GAP-C13's shape), numbers with no
   directory, trackers describing retired systems, derivations two
   records compute differently.

Every **candidate** a scan proposes (a study that would close a find)
carries: a one-line **falsifier**, and its **honesty-rule type** —
*in-house re-derivation* or *independent confirmation* (C088-12). A
candidate that only re-derives in-house never closes an
outside-reproduction find.

## Inputs common to all clusters

- `program-map.json` (nodes, classes, coverage block) and
  `program-map-finds.json` (bundle-less studies, judgment calls,
  null-falsifier claims, restricted notices) — the S2 outputs.
- The standing source lists the register must consolidate (C088-11):
  the system-coupling audit's gap register (GAP-C07, GAP-C12 remnant,
  GAP-C13), the repair brief (WP2/WP3/WP5 residuals), Spec 086's
  residuals, the T201 derivation divergence, and the adoption record's
  §4 items.
- The pre-answered legs below.

## Pre-answered legs (cite, do not re-derive)

- **Falsifier census: 848 of 857 ledger claims carry a falsifier**
  (bundle population 834/834; extracted 14/23). The 9 nulls are all in
  the extracted population and are enumerated claim-by-claim in the
  builder's find list. Source: the ledger itself, counted 2026-11-04;
  the schema's population accounting (`glossa-indus/ledger/SCHEMA.md`).
  Scan consequence: the null-falsifier question is a *disposition* item
  (backfill vs accept-and-record), not a measurement item.
- **WP5 support census over the 94 strict anchors: 6 independently
  supported / 46 internal-only / 37 requires revalidation / 3
  expert-pending (M222, M362, M398) / 2 insufficient (M367, M048).**
  Source: the repair brief's WP5 record. Scan consequence: the
  thin-evidence mass in the anchors domain is already counted; the scan
  classifies and routes it (which of the 37 revalidations are edges,
  which are nodes), it does not recount it.
- **WP4: eligible independent Parpola comparisons = 0 of 184** (the
  comparisons on record are circular — they share the lineage they would
  independently confirm). Source: the repair brief's WP4 record. Scan
  consequence: the program's flagship outside-reproduction gap is already
  measured; the scan's work is the candidate design space (what *would*
  count as independent), typed under C088-12.
- **GAP-C13, restated by S2: 31 specs without claims bundles at the
  Spec 086 audit; 28 bundle-less directories against today's tree**
  (the 001–025 directories + `026-core-research-source`), each already a
  per-study unjudged find in the find list. Source: Spec 086's audit
  record; S2's census. Scan consequence: Cluster C classifies the 28
  (which deserve bundles, which are honestly pre-ledger history), it
  does not rediscover them.

## Cluster A — Corpus + anchors (Domains 1 + 2) → `scan-corpus-anchors.md`

Scope: Sign inventory & corpus (17 studies); Anchors & readings (13).
Expected find mass, from the inputs: the anchor-provenance and validation
era (004–018) is entirely bundle-less — 13 of Domain 2's studies are
unjudged nodes whose standings live in prose and phase records (C2
finds, stale bookkeeping, at scale); the WP5 census's 37
requires-revalidation anchors are the domain's thin-evidence core; the
44 pending anchor readings (287 recorded / 94 strict / 44 pending) are
the domain's missing-node/edge question (readings pending on what,
blocked by whom); cross-compilation disagreement (Domain 1) is a
missing-edge candidate space — the compilations disagree and the
attribution line (019/021/022/034/058) is the edge partly built.
Pre-answered legs: WP5 census; falsifier census (anchors-adjacent claims
are bundle claims, 834/834 falsifier-complete — thinness here is support
class, not falsifier absence).

## Cluster B — Claim families + contact zone (Domains 3 + 4) → `scan-families-contact.md`

Scope: Claim families by study line (40 studies); Contact zone &
external corpora (2). Expected find mass: WP4's 0-of-184 (the
outside-reproduction hole, missing edge at program scale); WP2's
linguist certification of the five template families (DATA-BLOCKED,
carried from the repair brief); the three extracted documents with no
testing line (12 claims: ancient-writing technologies ×4,
archaeology-and-epigraphy ×2, deciphered-from-myth ×6 — missing node);
the D-design lines' successor structure (which designs have an open
residue no successor took up — missing edge); Domain 4's thinness itself
(2 study nodes for the whole contact zone — classify: honestly small, or
a missing-node find for the Gulf/Laursen line's study-level presence).
Pre-answered legs: WP4 count; WP5 census where it touches claim
families; the extracted-claim falsifier split (14/23).

## Cluster C — Infrastructure + bookkeeping (Domain 5 + cross-cutting) → `scan-infra-bookkeeping.md`

Scope: Program infrastructure (16 studies) plus every cross-cutting
bookkeeping item on the source lists, wherever it lives. Expected find
mass: GAP-C07 (open; its current statement taken from the audit record);
the GAP-C12 remnant; Spec 086's residuals (matrix edges for the live
population; the two-graph-worlds join at population one); the T201
mahadevan:64 derivation divergence (the one settled value two registered
routes derive differently — stale bookkeeping with a named oracle
decision outstanding); spec numbers 049 and 085 with no directory
(counted 2026-11-04; 049 is named as a predecessor in Spec 070's title);
the tracker llms.txt describing pre-086 functions (byte-mismatched
against the served file); the desktop clone's unpushed local commit and
the Spec 083-sequence sync it waits on; the data-lineage owner question
(VM dataset vs snapshot 1). Pre-answered legs: the counts in the
taxonomy draft's coverage notes; the find list's bookkeeping items.

## Output discipline

A scan record contains only: finds (kind, the nodes/edges named by their
citations, the evidence pointer), candidates (with falsifier + type),
and a short "what this cluster did not scan" line. Anything outside the
four kinds is not a find — it goes to the register stage as a note, or
nowhere. The consolidation check (T504) enforces the shape mechanically;
classification quality is human-as-oracle.
