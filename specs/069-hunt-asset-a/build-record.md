# Spec 069 / Phase 432 — Build Record (Asset A)

> ## EXECUTED — 2026-10-22 — ASSET BUILT AND FROZEN
>
> The build ran under the frozen Spec 069
> contract (freeze digest
> `657b930c9200299c7d540baa8ed51b7a90176bdea9822577e9cb1f4d292f99aa`;
> OSF registration r3xqb, filed at the freeze,
> pending the owner's approval act at the time
> of the run) as Phase 432, in the chain order
> of the owner act that commissioned the Hunt
> chain. Gates A1–A6 ran in order and all
> passed, before any join — this spec performs
> no join and computed no corpus or positional
> quantity of any kind.

## 1. Gate A1 — sources in hand, named by edition

- **The CISI volumes** — *Corpus of Indus Seals
  and Inscriptions*, Vol. 1 and Vol. 2 (Shah &
  Parpola eds., 1991), held digitally (IA
  scans, verified present at the gate).
- **The CISI sign list, as entered** — the
  volumes' sign identifications were entered
  through the held CISI digitization
  (mayig/indus-valley-script-corpus, April
  2026, MIT licence), one feature file per
  sign carrying the digitization's verbatim
  description of what the sign depicts.
  **Recorded incident:** the programme's
  downloads copy of the digitization was found
  missing at execution, during a concurrent
  workspace sweep; the source was restored
  from the same public upstream at commit
  `ad2f1e2` into
  `~/workspace/research_notes/hunt-chain-sources/`,
  and the descriptions read after the restore
  agree with the values read first-hand before
  the loss (P000, P001, P002, P123, P124
  spot-checked). The build record names the
  restored copy as the held copy used.
- **Parpola's published sign identifications**
  — consulted in held form: Parpola 2010,
  *The Dravidian solution* (Helsinki lecture,
  held PDF). Its sign numbers are Parpola's
  1994 list's and do not key to the pinned
  crosswalk's sign keys (its no. 123, the fig
  tree, is not the crosswalk's P123, three
  strokes), so no row could be corroborated or
  contested from it in a keyable way.
  **Consequence, stated openly:** every
  identified row's `agreement` is
  `single_source` (the CISI list governing),
  no row is `contested`, and that is a fact
  about the held sources' keyability, recorded
  here — not a claim that no second
  identification exists anywhere.

## 2. Gate A2 — the D-18 input state

Re-asserted at execution against the record:
`specs/046-horned-tiger-concordance/concordance-297.json`,
SHA-256
`772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf`,
`signs` an empty array, `closure` block of its
IDENTIFICATION FAILED outcome — the terminal
empty feed of the quoted §2.6. The build
proceeded without the feed, records its
absence (every row's `d18_input` is `none`),
and did not reconstruct it from the asset's
own labels. **Gate A2 PASSES.**

## 3. Blind entry — the order and the two passes

The §2.4 order was kept: sources consulted
(gate A1) → rows entered → dispute coding
completed → the D-18 absence recorded → the
asset freeze digest computed → (no join
follows in this spec). The enterer worked
from the held sources and the sign inventory
only; no positional result, part-membership
class, inscription assignment, or model
output was consulted at any point, and none
was in the enterer's working materials.

Entry ran in **two independent passes** over
the verbatim labels, reconciled sign by sign
(the machine-form entry log is
`asset-a/entry-decisions.json`):

- **Pass 1** — the enterer's own coding of
  each sign's depicted kind from its verbatim
  CISI-digitization description, read sign by
  sign for all 187 signs.
- **Pass 2** — an independent deterministic
  rule pass over the same verbatim labels
  (subject-term rules), written separately
  from Pass 1.
- **Reconciliation** — the passes disagreed on
  6 of 187 signs; each disagreement was
  adjudicated by re-reading the verbatim
  label, and every adjudication is recorded
  in the entry log with its reason (two
  source misspellings of "pitchfork" the rule
  pass missed; the person-arms figure P114;
  two substring false matches — "bowtie",
  "narrow"; and P384, where the subject rule
  applied consistently puts the diamond form
  over its wagon-wheel component).

Kind-coding rules as applied (from the
verbatim label's depicted subject): a person
or human figure → `human`; an animal →
`animal`; a named sun, star, moon or celestial
body → `sky_cycle`; a named made object or
tool (jar, pitchfork, bow, lyre, table, wheel)
as the depicted subject → `object_goods`;
plants, geometric and abstract forms, strokes,
and everything else → `other`; no governing
identification in any held §2.3 source →
`unidentified` with the searched sources
recorded. Two judgement calls are recorded
plainly: "prismed light rays" (P205, P206) is
coded `other` — the label names rays, not a
celestial body, and promoting it to
`sky_cycle` would be the enterer's inference,
which the contract forbids as a source; and
P360's "sun rays" are a component of a leaf
sign, whose depicted subject is the leaf
(`other`, the subject rule of P384/P096/P082
applied consistently).

## 4. Dispute coding (quoted §2.5)

No governing sources disagreed in a keyable
way, so **no row is `contested`** (see §1 for
why). Four rows are `borderline` — the
published identification is hedged in its own
source: P073 and P074 ("Unknown asymmetric
animal? Perhaps a fish…?"), P217 ("(arrow?
spear?)" — both candidates objects, kind
unaffected), and P320 ("A cat's paw perhaps").
Hedges in a label that concern the drawing's
form or orientation rather than what is
depicted (e.g. P355 "possibly rotated") were
noted in the entry process and not coded
borderline; the line taken is stated here so
it can be challenged as a line.

## 5. Gates A3–A6

- **A3 — coverage: PASSES.** 187 rows over the
  full pinned-crosswalk universe (205
  crosswalk rows, 187 distinct
  `registry_sign_id` values, the crosswalk
  re-hashed at the run to its pin
  `4ace1a61…`). One sign, **M059**, is
  `unidentified`: the held CISI digitization
  has no entry for it, Parpola's held
  identifications name none, and the pinned
  crosswalk records only a Fuls 2014 mapping
  for it, which is not a §2.3 source. Its row
  records the sources searched, as the
  contract directs.
- **A4 — citations: PASSES.** Every
  non-`unidentified` row carries its CISI
  citation with the verbatim label; every row
  carries an `agreement` value.
- **A5 — blind entry and order: PASSES**, on
  the attestation of §3, with the entry log
  preserved at `asset-a/entry-decisions.json`.
- **A6 — freeze recorded: PASSES.**
  `asset-a/asset-a-freeze.json` carries the
  §2.7 contents and its digest recomputes
  from the canonical CSV.

## 6. The product

- Canonical file:
  `asset-a/depicted-kind-classification.csv`,
  generated with a CSV writer and round-trip
  validated (every row parses to exactly the
  11 fields of the quoted §2.2). Its canonical
  form is UTF-8 with LF line endings, fixed in
  the build script, so the digest below is the
  digest of the file as committed and as any
  checkout reproduces it.
- **SHA-256:
  `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b`**
- 187 rows — per-kind counts: **animal 20,
  sky_cycle 0, object_goods 14, human 25,
  other 127, contested 0, unidentified 1**.
- Numbering fields: for P-prefixed sign keys,
  `cisi_no` and `parpola_no` both record the
  sign's number as held — the CISI sign list
  as digitized is kept in Parpola numbering,
  so the two numbers are the same value; for
  M059 both are empty, its row recording why.
- The script is deterministic: a second run
  reproduced every output byte-identically.
  Anchors asserted byte-identical before and
  after (`df0cf620…`).

**What this does not establish.** Asset A
records what the published lists say a sign
depicts, with citations; it does not establish
what any sign means, and the zero in the
`sky_cycle` row is a fact about the held
published identifications of these 187 signs,
not a finding about any corpus — Spec 071's
design is written to meet exactly this
possibility, and meets it in its own record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
