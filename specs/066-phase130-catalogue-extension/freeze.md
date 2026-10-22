# Spec 066 — Freeze Record (Phase-130 catalogue extension)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the owner's approval of 2026-10-21 (amendment
> package Item 7: the intake act itself, §4's
> lawful line included; `adjudication.md` §4).
> The AEE lifecycle hooks ran over the register
> first (register recovered to 0.6-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). **No OSF registration is filed for
> this act** (DD-066-8; the reasoning is
> recorded in spec §8 and `adjudication.md`
> §4). Execution runs as **Phase-428** under
> this frozen contract, in the same run, after
> this freeze merges.

## 1. Basis

The contract implemented is the intake act the
owner approved as amendment-queue Item 7
(2026-10-21), over material held under the
Phase-130 gate (restricted store PROVENANCE
entry 22, recorded before any processing): the
portion PDF (8,206,446 bytes, SHA-256
`514338b1…`), its extracted local table (2,123
records / 2,101 distinct well-formed numbers,
SHA-256 `7179858d…`), the pinned vols. 1–2
catalogue layer (7,705 rows, 3,493 distinct
objects; `e0d698f9…` / `e751244e…`), and the
committed Phase-421 census (`95282931…`) as the
demand side.

The position at freeze is stated plainly: the
candidate sets exist as counts, re-derived
first-hand at draft (1,341 referenced = 1,293
zero-resolution + 48 already-joined; 760
unreferenced), and **no candidate has been
graded** — the verification rates, the conflict
share the halt rule reads, and the stratum's
attributions are all unknown at freeze, in
either direction. The freeze buys the census
under a ladder fixed before any candidate is
examined, plus — unless the halt rule fires —
the pinned merged catalogue layer v2. The
fences are part of the basis, not
qualifications added later: a string match is
not a catalogue object; a VERIFIED catalogue
object is not a verified join; no F1 quantity
exists under this act; row-level products
beyond the §4 item-1 fact list never leave the
restricted local store.

The freeze decided the draft's open proposals
(`adjudication.md` §4): **DD-066-4** (the halt
threshold confirmed at 20% of all graded
candidates, the full 2,101 census, with the
true-non-identity tripwire independent),
**DD-066-5** (the stratum is 60: 30 VERIFIED /
15 CONFLICT / 15 UNRESOLVED, whole class where
smaller, seed **20261021** fixed at freeze,
with the medium-coverage supplement),
**DD-066-8** (no OSF registration for the
intake itself), and **DD-066-9** (phase
allocation Phase-428). The confidence gate's
operation (DD-066-6) and the corroboration
rung's UNGRADED base on the held records
(DD-066-7) are confirmed as drafted.

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/066-phase130-catalogue-extension/freeze.md` (this
  document)
- `specs/066-phase130-catalogue-extension/spec.md`
- `specs/066-phase130-catalogue-extension/claims.json`
- `specs/066-phase130-catalogue-extension/adjudication.md`
- `specs/066-phase130-catalogue-extension/aee/freeze-aee-note.md`
- `specs/066-phase130-catalogue-extension/build_freeze.py`
- `backend/tests/test_spec066_freeze.py`

`plan.md` and `tasks.md` are lifecycle
bookkeeping and are not digest-covered (the
house rule since Spec 026: plans change as
work proceeds).

## 3. What the freeze fixes

- **The ladder** (spec §5.3 / F066-C03): site
  agreement where referencing rows exist; the
  confidence gate (low ungraded until
  hand-verified against the page render; medium
  provisional until the stratum covers its
  class); the number-ambiguity bar; type
  carriage under the closed class set, never a
  gate; corroboration where in-hand records
  carry values (UNGRADED on the held records,
  DD-066-7); exactly three outcome classes;
  conflicts recorded with reason codes, never
  repaired.
- **The census and the reporting set** (spec
  §§3, 6 / F066-C09, C11): all 2,101 candidates
  graded; referenced and unreferenced sets
  reported separately throughout; UNRESOLVED
  always its own class.
- **The halt rule** (spec §5.5 / F066-C05,
  C06): a conflict share above 20% of all
  graded candidates halts the extension (no
  index committed, no layer pinned; the census
  reports in full), and any stratum attribution
  to true non-identity halts it regardless of
  the share.
- **The lawful line** (spec §4 / F066-C07): the
  extension index (number + site section +
  published type class + grade class),
  aggregates, and pins enter the repo; the
  merged layer and every other row-level
  product stay in the restricted local store.
- **Step 0** (spec §7 / F066-C08): gate quoted
  on the record, pins recomputed by two routes
  where committed, candidate sets re-derived,
  repo cleanliness — fail-closed, in the frozen
  order, before any grading; cleanliness
  re-checked before the outcome commit.
- **The construction** (spec §5.2 / F066-C13):
  one object per distinct number; collisions
  recorded locally, the existing object stands;
  the garbled tokens never repaired into
  invented numbers.
- **The validator discipline** (spec §5.6 /
  F066-C14): the pinned Phase-130 validator
  over the extension dataset form, its
  license_basis the entry-22 gate quoted, before
  any pinning.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
