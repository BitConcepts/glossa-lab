# Spec 066 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has one adjudication input, recorded
> here so the draft's basis is inspectable:
>
> 1. **The owner's approval of 2026-10-21**: the
>    amendment package Item 7 — the Phase-130
>    catalogue-extension intake — approved as the
>    intake act itself, §4's lawful line included.
>    The authoritative draft is
>    `~/workspace/research_notes/amendment-queue-2026-10-21/item-7-phase130-catalogue.md`
>    (research notes; investigation + draft of
>    2026-10-21), whose §4 (the lawful line) and
>    §5 (construction, verification ladder,
>    stratum, halt rule, pinned artifacts) govern
>    exactly. That approval authorises this
>    freeze and the execution of the intake in
>    the same run (Phase-428, after the freeze
>    merges). It authorises no OSF filing for the
>    intake (DD-066-8), no spending or
>    acquisition, no external send, and no use of
>    the restricted extraction beyond §4's line.

## 1. The adopted basis (operative substance)

- **The material.** CISI Vol. 3.1 "Basic data"
  portion (printed pp. 413–443), received by ILL
  2026-10-14, intaken 2026-10-20 under the
  Phase-130 gate. Extracted local table: 2,123
  records / 2,101 distinct well-formed catalogue
  numbers (Mohenjo-daro 519; Harappa old
  excavations 510; Harappa HARP 1,094); number-cell
  confidence high 1,933 / medium 183 / low 7; the
  tables carry no sign transcriptions.
- **The gate.** Phase-130, recorded before any
  processing (restricted store PROVENANCE entry
  22): restricted research material; local use,
  extraction, and publishable derived statistics
  permitted; redistribution of scans or row data,
  upload anywhere, and sharing copies prohibited.
  The §4 line of this spec is the owner's
  approved reading of that gate for this act
  (Item 7 §4, confirmed in the approval above).
  In-repo gate pack: `specs/021-phase130-intake-pack/`.
- **The demand side.** Spec 059 closed at step
  0, JOIN GATE NOT MET: the object-ID join
  resolved 2,899 of 5,679 lineage rows against
  the ≥ 3,465 bar; 2,119 rows carry identifiers
  resolving to zero objects in the pinned
  vols. 1–2 catalogue layer (7,705 rows, 3,493
  distinct objects). The unblocking act named in
  its frozen outcome wording is a more complete
  published object catalogue entering through
  Phase-130 intake. This spec is that act.
- **The act.** Grade all 2,101 portion numbers
  (1,341 referenced + 760 unreferenced, reported
  separately) under the frozen §5.3 ladder —
  site, confidence gate, ambiguity bar, type
  carriage (not a gate), corroboration where
  available — into VERIFIED / CONFLICT /
  UNRESOLVED; hand-check the frozen seeded
  stratum; apply the halt rule (conflict share
  > 20% of all graded candidates, or any sampled
  true non-identity, halts: census reported in
  full, no index committed, no layer pinned); on
  pass, build the merged catalogue layer v2
  locally, validate its dataset form under the
  quoted entry-22 license basis, and commit only
  the §4 products (the extension index,
  aggregates, pins).
- **The fences.** A string match is a candidate,
  never a catalogue object; a VERIFIED catalogue
  object is not a verified join; no F1 quantity
  exists under this act and `STUDY-SPEC-024/F1`
  and Spec 059's record stand exactly as
  recorded; row-level products beyond the §4
  item-1 fact list stay in the restricted local
  store.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21:

- **Item 7 draft** — read in full: its §3 join
  arithmetic, §4 lawful line, §5 intake act
  (sources, construction, ladder, stratum, halt
  rule, pinned artifacts), §6 owner acts, §7
  does-not-establish. This spec carries §4 and
  §5 into frozen form; where the draft left a
  value as a proposal for the freeze (the halt
  threshold's successor form; the stratum's
  size), the freeze decisions are §4 below.
- **Gate record** — PROVENANCE entry 22 read in
  full: classification, permitted and
  not-permitted lists, receipt verification
  (8,206,446 bytes; sha256
  514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a;
  supplied through Oakland University ILL). The
  gate's own words are quoted in spec §2.
- **Portion PDF** — SHA-256 recomputed locally:
  equals `514338b1…` exactly (8,206,446 bytes).
  A byte operation; no content was processed.
- **Extraction table** — SHA-256 recomputed
  locally: `7179858d…`, matching the Spec 037
  execution record's pin; header read (26
  columns, the intake's field names); census
  recomputed from the table's own columns:
  2,123 records; sections 519 / 510 / 1,094;
  number-cell confidence high 1,933 / medium
  183 / low 7; the 7 low cells are the 5 garbled
  tokens (not well-formed, not candidates) plus
  2 well-formed HARP numbers whose text-layer
  raw reads were garbled — the 2 low-gated
  candidates of §5.3 rung 2. No row was graded,
  joined, or entered at draft.
- **Candidate sets re-derived (counts only).**
  From the committed Phase-421 census (each
  row's carried identifier and resolution class)
  and the table's distinct well-formed numbers:
  referenced 1,341 = 1,293 zero-resolution + 48
  already-joined (disjoint); unreferenced 760;
  zero-resolution rows over the 1,293: 1,790 —
  Item 7 §3's figures, reproduced exactly. No
  identifier list left the local computation;
  only the counts are recorded here.
- **Merge base** — vols. 1–2 catalogue CSVs
  located in the local store (the Spec 059
  execution records' paths:
  `corpora/downloads/cisi_image_layer/catalogue/`
  of the programme's local store): SHA-256
  recomputed, `e0d698f9…` (804,665 bytes, 3,320
  rows) and `e751244e…` (1,431,631 bytes, 4,385
  rows); headers read — the layers carry site
  and object_type and **no FC, excavation, or
  museum columns** (the DD-066-7 base fact).
- **Lineage layer** — horus84 `inscriptions.csv`
  in the sweep store: SHA-256 `c368f290…`,
  1,190,884 bytes, as pinned.
- **Committed pins, two routes** (the GitHub
  contents API and a fresh checkout of `main` at
  `7e483e74508ab0f6183a58b951e1be13e0625267`):
  Phase-421 census `95282931…`, Phase-421 results
  `3948cd01…`, Phase-130 schema `b94d03ad…`
  (6,197 bytes), validator
  `backend/glossa_lab/intake.py` `02b24e33…`
  (18,867 bytes) — all equal on both routes.
- **Mayig layer** — field inventory read: the
  mayig objects carry id, description, and
  graphemes; the `corpus_master` form carries
  `source_object_id`, `site`, `artifact_type`,
  `source_name`. No FC, excavation, or museum
  values on either form (the DD-066-7 base
  fact).
- **Phase allocation** — `main` read at the
  head above: Phase-424 (Spec 062), Phase-425
  (Spec 063), Phase-426 (Spec 064) allocated;
  Phase-427 and Phase-428 unreferenced anywhere
  on `main`. Execution is allocated Phase-428
  (DD-066-9).
- **Spec 037 / Spec 059 records** — read on
  `main`: Spec 037's ladder, class set,
  comparison tuple, stratum form, halt precedent
  (49.21% conflict against corpus_master,
  attributed in its stratum to compilation
  divergence, 0 true non-identity), and step-0
  form, all carried as this spec states them;
  Spec 059's closure and the F1 standing as §1
  states them.
- **Not done at draft, by design** — no
  candidate graded; no render inspected; no
  layer built; no join computed; the §3 counts
  stand as counts, and every quantity beyond
  them is a quantity the execution will produce,
  not one this draft has seen.

## 3. What the freeze decision is asked to decide

The owner's approval of 2026-10-21 (§0, item 1)
already decided the act and its §4 line. The
freeze itself decides the draft's open
proposals, openly, before any candidate is
graded:

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`) — the ladder,
   the halt rule and its denominator, the
   stratum design and seed, the confidence-gate
   operation, the storage and git fences all
   fixed before any grading — or decline,
   leaving the intake undesigned beyond Item
   7's draft.
2. **DD-066-4 (proposal): the halt threshold.**
   Draft: 20% of all graded candidates (Item 7
   §5.5's successor form), with the
   true-non-identity tripwire independent.
3. **DD-066-5 (proposal): the stratum.** Draft:
   60 (30 / 15 / 15, whole class where smaller),
   seed 20261021 fixed at freeze, with the
   medium-coverage supplement.
4. **DD-066-8 (proposal): no OSF registration**
   for the intake itself, for the reasons in
   spec §8; the registration attaches to the
   successor F1 study spec.
5. The draft-fixed readings stand unless the
   freeze overturns them openly: the fixed
   step-0 order, fail-closed (DD-066-1); the
   census, not a sample (DD-066-2); the ladder's
   order, precedence, and type carriage
   (DD-066-3); the confidence gate's operation
   (DD-066-6); the corroboration base fact
   (DD-066-7); the phase allocation
   (DD-066-9); the AEE gate reading (DD-066-10).

## 4. Freeze decisions (2026-10-21)

The freeze was executed under the owner's
approval of 2026-10-21 (the amendment package
Item 7: the intake act itself, §4's lawful line
included; freeze first, then execution in the
same run). The decisions:

- **DD-066-4 — CONFIRMED: the halt threshold
  and denominator.** The CONFLICT share that
  halts the extension is 20% of all graded
  candidates (the full 2,101 census), as
  drafted; the true-non-identity tripwire is
  independent of the share. Not changed.
- **DD-066-5 — DECIDED: the stratum is the
  frozen design of spec §5.4.** 60 candidates
  (30 VERIFIED / 15 CONFLICT / 15 UNRESOLVED,
  whole class where smaller), seed **20261021**
  fixed here and recorded in the build script
  before sampling, with the medium-coverage
  supplement as drafted.
- **DD-066-8 — DECIDED: no OSF registration
  for the intake itself.** This act is a data
  act under the Spec 021 machinery, not a
  study; Item 7 §6 attaches the registration to
  the successor F1 study spec, which files its
  own at its own freeze. Recorded openly so the
  absence is a decision, not an oversight.
- **DD-066-9 — Phase allocation: Phase-428.**
  Verified at freeze against `main` head
  `7e483e74…`: Phases 424–426 are allocated to
  Specs 062–064; Phase-427 is unreferenced on
  `main`; the next clean number for this
  execution is Phase-428. Execution of this
  contract is Phase-428.
- **DD-066-10 — the freeze gate reading
  (adopting DD-038-10).** The AEE lifecycle
  gate at this freeze is read as Spec 038's
  freeze read it: the substantive pass is zero
  correctness failure modes (no irreducibility,
  no negation conflict, no counterexample or
  precision challenge) and no claim below the
  0.70 threshold at each of after_specify,
  after_plan, after_tasks; the FR-2.3
  draft-cap records a draft register carries
  (15 here, one per claim) are structural, are
  disclosed in `aee/freeze-aee-note.md`, and are
  not correctness failures — the engine's
  outcome word therefore reads "iterate" at
  each hook while the gate passes. The hooks
  ran under the adopted aee 1.5.3; the
  register's rounds and any recovery are
  recorded in `aee/freeze-aee-note.md` and the
  register's own note. No expectation was
  updated in any recovery: claim texts are
  restated to single propositions with carried
  clauses moved into boundaries
  verbatim-in-substance, and propositions,
  falsifiers, and verdict rules stand as
  drafted.
- **Citation refresh.** Every pin the design
  rests on was re-verified at the freeze by
  the §2 routes (local recomputation for the
  local-store pins; two routes for the
  committed pins); no cited record moved
  between draft and freeze, the two acts being
  the same day's work under one approval.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
