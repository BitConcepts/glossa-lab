# Spec 041 — Freeze Record (Site × Local-Label Period Mapping: the Placement Artifact Spec 040's Gate Requires)

> ## FROZEN — 2026-10-22
>
> This contract was frozen on 2026-10-22 under
> the owner's instruction of 2026-10-22 to
> resolve the program's open pull requests,
> which lifted the freeze gate for this act
> (the draft was commissioned 2026-10-21; the
> freeze and the execution were recorded there
> as separate owner gates). The AEE lifecycle
> hooks ran over the register first (register
> recovered to 0.8-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). The freeze also files this spec's
> own OSF contract registration (DD-041-12;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-435** under this frozen contract,
> and only on a separate execution order.
> **Execution has not been ordered and has not
> started.** At the freeze itself no cell was
> constructed, no census was computed, no
> placement count was taken, and no artifact
> was produced.

## 1. Basis

The contract is the act Spec 040's closure
record (§3, "What would satisfy the gate")
named: a separately governed act producing a
frozen, machine-readable mapping keyed **site
× the layer's recorded local chronological
label(s) → one coarse period (or UNASSIGNED)**,
every mapping carrying its published citation
and locator and contested flag, covering the
seven G1 population sites, built to Spec 040
§4's interface under the published-
determinations-only standard (Spec 039's
DD-039-3 carried verbatim in substance, with
its verification bar). Spec 040 closed
NOT-YET-TESTABLE at its dependency gate
(conditions 2 and 4 failed against Spec 039's
executed product); this act does not amend
that closure, does not satisfy the gate by
existing, and states the §1 substitution
openly (spec §1; claim F041-C13 states form
only; the substitution decision is reserved
to a future Spec 040 freeze, DD-041-13).

The freeze decided the open points
(`adjudication.md` §6): **DD-041-10** (no
single sensitivity label is frozen for any
contested cell; the determination **set** is
the frozen sensitivity basis — candidates
(b)/(c) of the draft, as recommended),
**DD-041-11** (source-acquisition scope (a):
sources already held plus interlibrary access
under the program's existing caps and gates,
everything unreached landing at
DETERMINATION_UNVERIFIED and counted),
**DD-041-12** (this spec files its own OSF
contract registration at the freeze),
**DD-041-14** (the execution phase is
**Phase-435**), and **DD-041-15** (the
DD-038-10 AEE gate reading adopted).
**DD-041-13**'s reservations (the row-level
derivation of spec §8; the §1 substitution)
are recorded, expressly **not** decided by
this freeze. The DECIDED-BY-DRAFT readings
DD-041-1 … DD-041-9 are **confirmed** as
drafted.

## 2. Pin verification (two routes, at the freeze)

The §4 repository pins were re-derived **in
the foreground** by two independent routes —
the contents-API raw route and the local-file
route — both at the merged record (`main` at
`ba61d9cd`, the merge parent of this freeze):

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |
| `data/evidence_integration/phase139_harmonized_covariates.json` | `a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413` | 2,665,622 |

Both recomputed hashes equal their §4 pins.
The anchors pin is the refreshed value
(DD-041-7); Spec 040's carried value
(`eccea6d5…`) is superseded and is used
nowhere in this spec's texts.

The layer file (horus84 `inscriptions.csv`,
pin `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`;
5,679 rows × 38 fields; 1,190,884 bytes) is an
acquired input, not committed to this
repository, and is **not producible on the
freeze machine**: the Phase-137 loader's
default-path copy is absent. Its pin
therefore stands on the records of record —
Spec 025 §3, the Phase-139 and Phase-140
reproductions from it, and the held-copy
verifications at the Spec 060 and Spec 067
freezes, each at the same pin — stated openly
here and in `adjudication.md` §6, never
silently refreshed. Execution gate G0.1
re-asserts the pin fail-closed in the
executing environment before any cell is
constructed; an environment that cannot
produce the file at that hash cannot run the
act.

## 3. Machine record

`freeze.json` in this directory is the
canonical JSON record (framework026
`build_freeze`, computed by `build_freeze.py`
in this directory). Covered sources (nothing
else decides the question):

- `specs/041-site-local-label-period-mapping/freeze.md`
  (this document)
- `specs/041-site-local-label-period-mapping/spec.md`
- `specs/041-site-local-label-period-mapping/claims.json`
- `specs/041-site-local-label-period-mapping/adjudication.md`
- `specs/041-site-local-label-period-mapping/aee/freeze-aee-note.md`
- `specs/041-site-local-label-period-mapping/build_freeze.py`
- `backend/tests/test_spec041_freeze.py`

`tasks.md`, `plan.md` (none), and
`osf-spec-registration.md` are lifecycle
bookkeeping and are not digest-covered (the
house rule since Spec 026: plans change as
work proceeds).

## 4. What the freeze fixes

- **The key and the value vocabulary** (spec
  §5 / F041-C02, C04): the layer's verbatim
  (site, field, local label) triple; exactly
  one of EARLY / MATURE / LATE / UNASSIGNED
  per cell; every population-attested triple
  present exactly once (F041-C03).
- **The evidence standard** (spec §3 /
  F041-C05, C06): published determinations
  only, DD-039-3's venue-and-locator test with
  its conservative default, Spec 039's
  verification bar; no program-derived
  inference of any kind; locator aids point
  and never ground.
- **The contested discipline** (spec §7.2 /
  F041-C07): contests retained verbatim, both
  determinations kept, binding value
  UNASSIGNED, no preference rule; and the
  freeze's sensitivity ruling (DD-041-10): no
  single label frozen; the determination set
  is the basis a future Spec 040 freeze
  constructs from.
- **The unassigned discipline** (spec §5.4 /
  F041-C08): exactly one reason from the
  enumerated set of five; extending the set
  is a freeze amendment, recorded openly.
- **The step-0 gates** (spec §6 / F041-C09):
  layer identity, population reproduction
  (seven sites, 5,410 rows), the value-level
  label census reproducing the recorded
  tables exactly (period 2,266; phase 2,638;
  both 1,788; union 3,116), the covariates
  copy asserted against the layer, anchors at
  the refreshed pin, source admissibility
  classified before extraction, and the
  no-computation fence — any failure closes
  the act at step 0 with no artifact.
- **The construction rules** (spec §7 /
  F041-C11): one cell, one determination; no
  precedence and no skipped class; dual
  verification of every grounded cell before
  the artifact is pinned, reclassifications
  recorded and never edited into agreement.
- **The reporting contract** (spec §8 /
  F041-C12): placement counts published under
  derivations A1 / A2 / B / C with unplaced
  rows split by cause and the 57.6% ceiling
  stated; no derivation adopted or preferred
  by this act.
- **The fences** (spec §10 / F041-C01, C13,
  C14, C15): no G1 quantity at any stage; no
  frozen record amended; the artifact's
  fitness judged by a future Spec 040 freeze,
  not asserted here; the ICIT-lineage label
  on every output; anchors asserted
  byte-identical before and after.

## 5. Execution gate

Not satisfied, by design: execution requires
its own owner order after this freeze has
merged and the registration's approval act
has completed. Nothing in this freeze is an
execution order, and no step-0 gate has been
run under it.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
