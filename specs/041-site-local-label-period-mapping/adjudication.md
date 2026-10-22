# Spec 041 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has one adjudication input, recorded here
> so the draft's basis is inspectable:
>
> **The owner's order of 2026-10-21**: "address all
> these remaining items now" — taking up, among the
> open items reported with the completed 2026-10-20
> pipeline, the item Spec 040's closure record (§3)
> left as an owner decision: commissioning the
> separately governed act that produces the site ×
> local-label period mapping built to Spec 040 §4's
> interface.
>
> The order commissions this **draft**. It is not a
> freeze order and not an execution order: the
> freeze (lifecycle hooks, the decisions of §4,
> a digest, a phase allocation) and the execution
> remain separate owner gates, as with Specs
> 036–040. Drafts are standing pre-approved.

## 1. The adopted basis (operative substance)

- **The gate that defines the product.** Spec 040
  §1 (dependency gate) and §4 (period assignment):
  the consumer joins, per inscription, its site and
  its recorded local chronological label(s) to
  exactly one coarse period (`EARLY` / `MATURE` /
  `LATE`), to `UNASSIGNED`, or to a flagged
  contested assignment — through an artifact keyed
  at site-period resolution, every non-UNASSIGNED
  assignment carrying its published citation,
  locator, mapping rule, and contested flag, under
  published determinations only.
- **The closure that commissions the shape.** Spec
  040's outcome record, dependency-gate record
  (appended 2026-10-20): conditions 2 and 4 FAILED
  against Spec 039's executed product; §3 states
  what would satisfy the gate (quoted in spec §1)
  and that a satisfied dependency still requires a
  Spec 040 freeze act and a separate execution
  order.
- **The population.** The Phase-137 F3 population
  on the ICIT-lineage layer (horus84, SHA-256
  `c368f290…`): 5,410 inscriptions at 7 eligible
  sites — Chanhu-daro (74), Dholavira (238),
  Harappa (2,717), Kalibangan (212), Lothal (208),
  Mohenjo-daro (1,923), Nausharo (38) — reproduced
  by rule in the Phase-140 freeze record and the
  Phase-139 report.
- **The label record.** Layer fields `period` and
  `phase` (Spec 025 §3): population coverage
  period 2,266 (41.9%), phase 2,638 (48.8%), both
  1,788 (33.0%), union 3,116 (57.6%); vocabularies
  site-local; missingness structural.
- **The evidence standard.** The owner's
  2026-10-20 decision (Spec 039, Option 1):
  published period determinations only, with
  DD-039-3's venue-and-locator test and Spec 039's
  verification bar carried into this act verbatim
  in substance (spec §3).

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
against `main` at `82b29490`:

- **Spec 040 closure** — read in full on main:
  the condition-by-condition verification
  (condition 1 satisfied; conditions 2 and 4
  failed), the artifact identity it checked
  (`gazetteer_rows_assigned.jsonl`, SHA-256
  `64f288d3…`, 36 rows / 30 sites), the §3
  consequences (DD-040-1/5/6/9 undecided,
  DD-040-10 open, no OSF filed, register at
  0.5-draft), and the secondary finding on the
  stale anchors pin (below).
- **Spec 040 spec §§1, 3, 4** — read in full:
  the four gate conditions; the §3 input pins
  (layer `c368f290…`; Phase-139 covariates
  `a0f0d05a…`); §4.1's join (layer row +
  covariates row + assignment artifact keyed
  site × local label); §4.2's assignment rules
  (UNASSIGNED for unrecorded, unmapped,
  multi-mapping, and contested-only labels);
  §4.3's exclusions (site labels, radiocarbon,
  Phase-139 `chron_band`, analyst judgement);
  §4.4's contested posture (a frozen sensitivity
  label per contested mapping, or NOT ESTIMABLE).
- **Spec 025 spec §3 + Phase-140 freeze §2** —
  read in full: the layer's identity (5,679 rows
  × 38 fields, 1,190,884 bytes, `c368f290…`), the
  §3.1 fill tables, the §3.2 per-site structural
  missingness (Harappa period ∩ phase = 0.6%),
  the §3.3 site-local vocabularies, the
  Phase-137 eligibility rule, and the seven
  sites named in the freeze.
- **Phase-139 report + citation register +
  covariates meta** — read in full: the census
  reproduced exactly (report §2); the
  harmonization's 35 mapped cells under 7
  scheme-level citations; its unmapped cells
  (Harappa `2/3`, `3/4`, `B?`; Dholavira `5/6`,
  `5?`; Nausharo `4`) and unmapped classes
  (Harappa `Stratum I–VII`, 837 rows; Lothal
  `Layer 2–15`, 105 rows; Mohenjo-daro phase
  class; Kalibangan phase class unexamined;
  Nausharo phase `B, C`; Dholavira phase `F`;
  Chanhu-daro none); its precedence rule; its
  Class C status. The covariates file carries
  `period_raw` / `phase_raw` per population
  inscription (meta field list), which spec
  §6 G0.3 asserts against the layer itself.
- **DD-039-3** — read in Spec 039's adjudication:
  the venue-and-locator test, the not-published
  list (internal datasets, non-determination
  deposits, unpublished records, theses as
  sole ground), the conservative default, and
  the rule that a freeze may widen venues but
  never narrow the locator requirement.
- **Anchors pin state** — carried from Spec
  040's closure record (§3, secondary finding),
  which verified first-hand that
  `backend/reports/INDUS_FINAL_ANCHORS.json`
  recomputes to
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
  on current main and at that draft's own base,
  unchanged since 2026-10-12 (Spec 029 Phase H).
  This draft carries `df0cf620…`; the freeze
  re-verifies it before any use (tasks L5).
- **Layer file locus** — `data/inscriptions.csv`
  is **not** committed to this repository (tree
  checked at `82b29490`); it is an acquired input
  consumed by pin. Step 0 (G0.1) therefore
  verifies the file produced at execution
  against the §4 pin, and an execution
  environment that cannot produce the file at
  that hash cannot run the act.
- **Phase-number state** — Phase-400 (Spec 036),
  401 (038), 402 (037), 403 (039) are allocated;
  Spec 040 allocated none. This draft allocates
  none (DD-041-14, §4).
- **Not done at draft, by design** — no label
  census was computed beyond the cited records
  (the value-level census is an execution
  step-0 product, spec §6 G0.3); no cell was
  constructed; no determination source was read
  for extraction; no placement count under any
  §8 derivation was computed. Every quantity in
  this draft is a quantity of the cited records.

## 3. Draft-fixed readings (DECIDED-BY-DRAFT — stand unless the freeze overturns them openly)

- **DD-041-1 — The key is the layer's own
  strings.** Site (verbatim layer string) ×
  field (`period` | `phase`) × local label
  (verbatim, query and span marks intact). The
  consumer joins on layer rows (Spec 040 §4.1);
  the gazetteer's key space is a different
  artifact's. (Spec §5.1; F041-C02.)
- **DD-041-2 — The value vocabulary is Spec
  040 §4.1's codes** (`EARLY` / `MATURE` /
  `LATE` / `UNASSIGNED`). Neither Spec 039's
  display strings nor Phase-139's site-relative
  band names are values here. (Spec §5.2;
  F041-C04.)
- **DD-041-3 — The evidence standard is
  carried, not re-derived.** DD-039-3's
  venue-and-locator test, its conservative
  default, and Spec 039's verification bar
  govern every cell; locator aids (the
  Phase-139 register, the Phase-394 spine,
  compilations) may point and never ground.
  (Spec §3; F041-C05, C06.)
- **DD-041-4 — The enumeration universe is the
  population.** Cells are the (site, field,
  label) triples attested on population rows;
  labels attested only off-population are a
  coverage-report census, not cells — the
  consumer's join covers the population
  (Spec 040 §1 condition 4, §4.1). (Spec §5.5;
  F041-C03.)
- **DD-041-5 — No precedence in construction.**
  Phase-139's period-wins rule is not carried;
  every attested cell is resolved on its own
  published evidence or is UNASSIGNED with its
  reason, including the classes Phase-139 left
  unexamined. (Spec §7.3.)
- **DD-041-6 — Contests are retained, never
  resolved.** Two admissible determinations
  assigning different coarse periods make a
  cell CONTESTED with binding value UNASSIGNED;
  no tier, recency, or majority preference
  applies (DD-039-2's hierarchy orders
  presentation only, there as here). (Spec
  §7.2; F041-C07.)
- **DD-041-7 — The anchors pin is the
  refreshed value** (`df0cf620…`, §2 above).
  Spec 040's carried value (`eccea6d5…`) is
  superseded and is not used anywhere in this
  spec's texts.
- **DD-041-8 — Artifact form and paths.**
  `data/evidence_integration/
  site_period_mapping.jsonl` (one object per
  cell) + `site_period_mapping_meta.json`
  (provenance and counts), per spec §5.6; the
  freeze pins both by SHA-256.
- **DD-041-9 — The act adopts no row-level
  derivation.** The coverage report publishes
  placement counts under derivations A1 / A2 /
  B / C (spec §8) and states no preference; the
  derivation choice is reserved (§4,
  DD-041-13).

## 4. Open for the freeze (OPEN — not decided by this draft)

- **DD-041-10 — Sensitivity labels for
  contested cells.** Spec 040 §4.4 consumes a
  frozen sensitivity label per contested
  mapping and defaults to NOT ESTIMABLE where
  none is frozen. Candidates: (a) freeze one
  sensitivity label per contested cell — but
  choosing one determination's label over the
  other's is itself a preference the standard
  disfavours (DD-041-6); (b) freeze no label,
  and record both determinations as the
  sensitivity basis a future Spec 040 freeze
  constructs from; (c) freeze the determination
  *set* as the label, leaving the sensitivity's
  construction wholly to that freeze.
  **Draft recommendation: (b)/(c)** — the set
  is the honest frozen object; a single label
  would smuggle a resolution into a record
  whose discipline is retention. The schema
  reserves the nullable field either way
  (spec §5.3).
- **DD-041-11 — Source-acquisition scope.**
  The stratigraphic authorities are 1931–1993
  excavation literature; some cells' verdicts
  turn on obtaining and reading them.
  Candidates: (a) sources already held by the
  program plus interlibrary access under the
  program's existing caps and gates, with
  everything unreached landing at
  DETERMINATION_UNVERIFIED and counted;
  (b) a wider, separately approved acquisition
  effort with its own budget and time-box.
  **Draft recommendation: (a)** — the act's
  discipline is to record what the evidence
  reached supports, not to mount an acquisition
  program inside a mapping act (spec §14).
- **DD-041-12 — The spec's own OSF contract
  registration.** **Draft recommendation:
  YES**, following the Spec 036–039 pattern —
  the schema, gates, and standard timestamped
  outside the repo before execution. Nothing
  is filed at draft.
- **DD-041-13 — Reserved, expressly not for
  this freeze.** Two decisions belong to a
  future Spec 040 freeze and are recorded here
  so neither is mistaken for an oversight:
  (i) the row-level derivation (spec §8) that
  turns an inscription's label(s) into a
  stratum; (ii) the substitution decision —
  Spec 040 §1 as written names Spec 039's
  product, and accepting this act's artifact
  in its place is that freeze's openly
  recorded act (spec §1). This spec's freeze
  decides neither.
- **DD-041-14 — Execution phase number.**
  Allocated at the freeze act from the merged
  record, per the standing rule (phase numbers
  are allocated by freeze acts). No number is
  claimed at draft.

## 5. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json` computed once
   over the recovered register and finalised
   texts), with the §4 pins re-verified — or
   decline, leaving Spec 040's closure as the
   program's final word on the dependency.
2. Decide DD-041-10, DD-041-11, and DD-041-12;
   record DD-041-13's reservations and
   DD-041-14's allocation.
3. Confirm or overturn, openly, any
   DECIDED-BY-DRAFT reading of §3.

## 6. Freeze decisions (FREEZE ACT — 2026-10-22)

This freeze act was performed under the owner's
instruction of 2026-10-22 to resolve the program's
open pull requests, which lifted the freeze gate
for this spec. Execution was **not** ordered and
has **not** started; it remains a separate owner
gate. The decisions of §5 are taken as follows:

1. **The contract is frozen as drafted**, with
   the §4 pins re-verified at the freeze (record
   in `freeze.md` §2): the anchors file recomputes
   to `df0cf620…` and the Phase-139 covariates to
   `a0f0d05a…`, each by two independent routes at
   the merged record. The layer file
   (`inscriptions.csv`, pin `c368f290…`) is not
   producible on the freeze machine — the
   loader's default-path copy is absent — so its
   pin stands on the records of record (Spec 025
   §3; the Phase-139/140 reproductions; the
   held-copy verifications at the Spec 060 and
   Spec 067 freezes, at the same pin), stated
   openly here rather than silently refreshed;
   execution gate G0.1 re-asserts it fail-closed
   before any construction.
2. **DD-041-10 — DECIDED: candidates (b)/(c), as
   the draft recommended.** No single sensitivity
   label is frozen for any contested cell — a
   single label would smuggle a resolution into a
   record whose discipline is retention
   (DD-041-6). What is frozen is the determination
   **set** itself: every CONTESTED cell retains
   all its admissible determinations verbatim,
   and a future Spec 040 freeze constructs the
   sensitivity treatment from that set under its
   own decision. The schema's `sensitivity_label`
   field stays nullable (spec §5.3), and Spec 040
   §4.4's default applies in the meantime: a
   contested mapping without a frozen sensitivity
   label is NOT ESTIMABLE for that mapping in any
   consumer that does not make its own freeze
   decision.
3. **DD-041-11 — DECIDED: candidate (a), as the
   draft recommended.** The construction seeks
   determinations in sources already held by the
   program plus interlibrary access under the
   program's existing caps and gates; everything
   unreached lands at DETERMINATION_UNVERIFIED
   and is counted in the coverage report. No
   wider acquisition effort is commissioned by
   this act (spec §14).
4. **DD-041-12 — DECIDED: YES.** This spec files
   its own OSF contract registration at the
   freeze, following the Spec 036–039 pattern
   (record in `osf-spec-registration.md`).
5. **DD-041-13 — RESERVATIONS RECORDED, NOT
   DECIDED.** The row-level derivation (spec §8)
   and the substitution decision (spec §1) both
   belong to a future Spec 040 freeze. This
   freeze decides neither, and nothing in the
   frozen contract asserts that Spec 040's gate
   is satisfied (claim F041-C13 states form
   only).
6. **DD-041-14 — Phase-435 ALLOCATED.** Phase
   numbers 404–432 stand allocated on the merged
   record (the campaign freezes and their
   successors, latest Phase-432 at this act);
   the execution phase for this contract is
   **Phase-435**, the number allocated to this
   freeze. Numbers 433–434 stand unallocated on
   the record at this act and are not claimed
   by it.
7. **DD-041-15 — The DD-038-10 AEE gate reading
   is ADOPTED** for this freeze, as at Specs
   037–067: the lifecycle hooks pass when every
   hook carries zero correctness failure modes
   and no claim below the 0.70 threshold, the
   engine's "iterate" outcome word resting
   solely on the FR-2.3 draft-cap records. The
   hooks so passed over the recovered register
   (0.8-draft; `aee/freeze-aee-note.md`).
8. **DECIDED-BY-DRAFT readings (§3) — CONFIRMED.**
   DD-041-1 … DD-041-9 stand as drafted; the
   freeze overturns none of them.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
