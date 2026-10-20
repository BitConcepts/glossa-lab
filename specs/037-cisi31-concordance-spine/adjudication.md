# Spec 037 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-20
>
> This spec has one adjudication input, recorded
> here so the draft's basis is inspectable:
>
> 1. **The owner's order of 2026-10-20**: move
>    everything the programme controls forward,
>    the CISI follow-on uses named among them.
>    That order commissions this **draft** — the
>    study design for the two candidate uses the
>    CISI 3.1 intake assessed (the concordance
>    spine and the HARP provenance structure;
>    intake report §7.5–7.6). It commissions the
>    design only: the freeze of this contract and
>    any execution are separate owner decisions,
>    not commissioned by it, and the intake's own
>    gate discipline (arrival plan §6 — no study
>    use without a fresh owner decision) is
>    satisfied by this draft and would be
>    satisfied for execution only by a further
>    order. This draft performs no join, no
>    extraction, and no data work.

## 1. The adopted basis (operative substance)

- **The material.** CISI Vol. 3.1 "Basic data"
  portion (printed pp. 413–443), received by ILL
  2026-10-14, intaken 2026-10-20 under the
  Phase-130 gate. Extracted local table: 2,123
  records / 2,101 distinct catalogue numbers
  (Mohenjo-daro 519; Harappa old excavations 510;
  Harappa HARP 1,094). The tables carry no sign
  transcriptions — zero sign tokens.
- **The gate.** Phase-130, recorded before any
  processing (restricted store PROVENANCE entry
  22): restricted research material; local use,
  extraction, and publishable derived statistics
  permitted; redistribution of scans or row data,
  upload anywhere, and sharing copies prohibited;
  nothing derived enters git. In-repo gate pack:
  `specs/021-phase130-intake-pack/`.
- **Workstream A.** The intake counted **693
  exact-string matches** between the portion's
  numbers and `corpus_master` object ids (M 289 /
  EH 102 / HARP 302) and recorded them as string
  matches against a mixed-provenance compilation,
  NOT verified same-object joins. The pilot test
  (spec §4) grades all 693 under a fixed ladder —
  site mandatory; object type mandatory where
  graded (a seal and a seal impression are
  different classes); FC / excavation / museum
  corroboration where records exist on both
  sides, contradiction = conflict; number-level
  ambiguity bars VERIFIED — into VERIFIED /
  CONFLICT / UNRESOLVED, reporting the registered
  aggregates, with a seeded hand-check stratum
  attributing conflicts to causes. The spine is
  built locally from VERIFIED joins only, and a
  conflict share above 20% halts the build
  (pilot still reported in full).
- **Workstream B.** A descriptive annex of the
  HARP rows' provenance structure (dig year, lot,
  period codes as printed), with the period-fill
  floor caveat attached. It does not change the
  Spec 031 (Q7) record and feeds no verdict.
- **The fences.** String match ≠ same object;
  the concordance is a finding aid, not evidence
  about readings; no PRED-2026 entry can be
  scored from this material; row-level products
  stay in the restricted local store; only
  aggregate statistics are publishable.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-20:

- **Intake record** — read in full (research
  notes, restricted store): receipt and gate
  (§§1–3), execution results (§7): the five
  printed columns and the HARP section's own
  conventions; extraction (2,029 text-layer rows
  + 94 visual; `row_source` separates them;
  26 columns); census (2,123 / 2,101; 519 / 510 /
  1,094; H-1019 absent as found; 14 numbers with
  multiple records; H-2243 and H-2245 carrying
  differing data under one number); field fill
  (FC 1,028 of 1,029 family-A; excavation 1,527;
  museum 1,029; HARP lot 754 of 1,094; HARP
  period 656 of 1,094, a floor); overlap (693
  exact-string matches vs `corpus_master`, M 289
  / EH 102 / HARP 302; 1,394 of 2,101 numbers new
  to the programme); the can/cannot assessment
  (§7.5) this design implements.
- **Gate record** — PROVENANCE entry 22 read in
  full: classification, permitted and
  not-permitted lists, receipt verification
  (8,206,446 bytes; sha256
  514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a;
  lender named on the delivery slip as
  University of Missouri–Kansas City, supplied
  through Oakland University).
- **Portion PDF** — SHA-256 recomputed locally at
  this draft: equals `514338b1…` exactly. A byte
  operation; no content was processed.
- **Local table** — line count verified locally
  (2,124 lines = header + 2,123 records) and
  header read (26 columns, the intake's field
  names). No row content was read, joined, or
  graded at draft; the pilot's census exists
  only as the intake's published count (693).
- **corpus_master** — read on `main` (head
  `5e7f3cdb`): 2,722 rows; two sources (mayig
  CISI digitisation 179; Yajnadevam 2,543);
  `source_object_id`, `site`, `artifact_type`,
  `source_name` present as the design's key
  inventory states; SHA-256 `b19cfe95…` as pinned
  in the Spec 035/036 records for the same file.
- **Spec 031 record** — read on `main`: Q7
  closed at the margins step (bead/craft
  NOT-YET-TESTABLE, ceramic NOT ESTIMABLE);
  in-universe link construction 2 sites /
  1 linked pair. The annex fence (F037-C13)
  cites it as found.
- **Spec 034 precedent** — the matched-object
  attribution study joined on
  `provenance.object_id` only, with Holdat
  `cisi_number` prohibited as a join key; this
  design carries the prohibition (§4.1).
- **Not done at draft, by design** — no join
  computed; no candidate graded; no HARP
  quantity recomputed; the 693 stands as the
  intake's count, and every quantity in the
  spec beyond the intake's aggregates is a
  quantity the execution will produce, not one
  this draft has seen.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`) — the ladder,
   the halt rule, the aggregate set, the storage
   and git fences, and the annex limits all
   fixed before any join is computed — or
   decline, leaving both workstreams undesigned
   beyond the intake's candidate list.
2. **DD-037-5 (proposal): the hand-check
   stratum size.** Draft proposal: 60 candidates
   (30 VERIFIED / 15 CONFLICT / 15 UNRESOLVED,
   whole class where a class is smaller), seed
   recorded before sampling. The stratification
   across outcome classes is fixed; the size is
   the freeze's to set.
3. **DD-037-6 (proposal): Workstream B's
   placement** — inside Phase-401 behind
   Workstream A, gated on step 0 only
   (**recommended**; B touches no joins and
   reads the same pinned table), or as a
   separate later phase.
4. **DD-037-7 (proposal): whether the frozen
   spec files its own OSF registration**
   (proposal: yes, following the Spec 027/030
   study-design pattern, so the ladder and halt
   rule are timestamped outside the repo before
   execution). Nothing is filed at draft.
5. The draft-fixed readings stand unless the
   freeze overturns them openly: the fixed
   step-0 order, fail-closed (DD-037-1); the
   census, not a sample (DD-037-2); the
   ladder's mandatory fields and UNGRADED
   handling (DD-037-3); the halt threshold at
   20% of all candidates (DD-037-4 — the freeze
   may change the value, but only before any
   join is computed, and the change is recorded
   here).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
