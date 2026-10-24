# Spec 071 / Phase 434 — Outcome record (EXECUTED 2026-10-22 — INVALID, gate 0.3)

> ## EXECUTED — 2026-10-22 — STOPPED AT STEP 0 (gate 0.3): INVALID
>
> Executed under the frozen Spec 071 contract
> (freeze digest
> `c06a7a86804d8da2c9896638446f5712be9eccb8716a7b02303a5944f4bc0478`;
> freeze PR #343 merged at `161bbe0d`; OSF
> registration b62p4 filed at the freeze,
> pending the owner's approval act at the time
> of the run), as **Phase 434**, in the chain
> order of the owner act that commissioned the
> Hunt chain. The step-0 gates ran in order:
> 0.1 Asset A asserted and PASS; 0.2 the Shakti
> intake reproduced under P-F1 S1/S2 and PASS;
> **0.3 input integrity PASS, coverage FAIL —
> the run stops here as INVALID.** No
> final-position quantity was computed, gates
> 0.4 and 0.5 were not reached, and no verdict
> is recorded. The machine record is
> `reports/phase434_results.json`.

## Headline (spec §4.6 INVALID wording, filled from the run)

> "Spec 071 stopped at step 0, gate 0.3:
> coverage — of the 557 signs occurring in the
> primary population, 272 carry no Asset A row
> under the keying route the freeze fixed (134
> with no resolution in the pinned registry's
> Wells map; 138 resolving to registry signs
> outside Asset A's 187-row universe). An
> absent row is never treated as non-celestial
> by default, because that default would
> silently define the comparison class. No
> final-position quantity was computed and no
> verdict is recorded; the claim stands
> UNTESTED as recorded."

Lineage (P-F1 S3), carried in the headline
block as the design requires: the positional
classes were measured on the Shakti corpus
deposit (Zenodo) as graded by the programme's
intake record — documented-lineage rows are
CISI-verifiable; corroborated rows are supported
by an independent sign list; uncorroborated rows
enter no count. The Phase-43 counts (805/2,267;
the 40/61/20 classes) are never a basis for any
quantity here. G5 attestation: the battery is
threshold-only, with no chance-baseline step,
and none is claimed.

What this means, in plain words: this test
cannot be run honestly on the asset that
exists, and the design said so in advance.
Asset A classifies 187 signs — the universe of
the programme's pinned crosswalk. The Shakti
corpus's documented inscriptions use 557
distinct signs. For 285 of them the frozen
keying route finds an Asset A row; for 272 it
finds none — 134 Wells numbers the pinned
registry does not map at all, and 138 that map
to signs the crosswalk universe (and so the
asset) does not contain. Gate 0.3 exists for
exactly this situation: the comparison class is
built from signs that are *not* celestial, so
treating "no classification" as "not celestial"
would have let missing data define the test's
denominator. The gate forbids it, and the run
stops. The claim stands UNTESTED, exactly as
Spec 050 left it.

One adjacent fact belongs in this record
because it is part of the frozen record, not
because it changes the closure: the celestial
class is **empty** in Asset A — zero of its 187
rows carry `sky_cycle` — so even a coverage
repair would meet, at gate 0.4, a celestial
census of zero members and zero occurrences,
below the TOO THIN floor of 30. The execution's
closure is gate 0.3's INVALID, reached first in
the gate order; the empty class is stated here
so no reader mistakes this outcome for a near
miss, and so a successor's design work starts
from both facts.

## 1. The gates, as they ran

- **0.1 Asset A — PASS**, against the pin
  source the freeze fixed (Spec 069's
  `asset-a-freeze.json` in its merged executed
  record): the canonical CSV recomputes to
  `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b`;
  the presented file's per-kind counts match
  the pin source's (animal 20, sky_cycle 0,
  object_goods 14, human 25, other 127,
  contested 0, unidentified 1).
- **0.2 Shakti intake (P-F1 S1/S2) — PASS.**
  Both restricted-local files hash to their
  pins; the census reproduces from the files
  themselves: 5,704 rows; 5,536 analyzable;
  grades 3,212 documented / 2,087 corroborated /
  405 uncorroborated; 4,904 of 5,536 analyzable
  rows carrying a CISI identifier.
- **0.3 Input integrity and coverage —
  integrity PASS, coverage FAIL.** The
  registry, crosswalk and anchors hash to
  their freeze values. The coverage census
  (totals only — no positional quantity was
  taken at this gate) counts 557 distinct signs
  occurring in the primary population (550 of
  them in the battery's sequences of length
  ≥ 2); 285 carry exactly one Asset A row
  under the keying route of DD-071-10; 272
  carry none: 134 Wells ids with no resolution
  in the registry's `parpola_1982` Wells map,
  and 138 resolving to registry sign ids that
  carry no Asset A row (Asset A's universe is
  the pinned crosswalk's 187 signs; the
  registry names more). Every one of the 272
  is listed in the machine record with its
  Wells code, its primary-population total,
  and its reason. The gate's second coverage
  limb — every `sky_cycle` row's `sign_key`
  resolves in the pinned crosswalk — is
  vacuous on this asset: there are no
  `sky_cycle` rows. Under the gate's own
  terms the run stops as INVALID.
- **0.4 / 0.5 — not reached.** The
  terminal-strong frame was not enumerated
  under this spec, no class census was taken,
  and no freeze-order proof was needed: the
  record's gate order is itself the proof of
  where the run stopped.

## 2. Foundation check (H21), as measured

Run on the execution tree after the phase, with
the two Holdat CSVs copied from the existing
local downloads into the worktree's local store:
**40 checks passed, 0 failed, 8 warnings** — the
standing figure. Anchors were asserted
byte-identical before and after the run
(`df0cf620…`). The run is deterministic: a
second execution of the phase script reproduced
`reports/phase434_results.json` byte-identically.

## 3. What the outcome does not establish

This closure establishes nothing about whether
sky signs gather at text endings — in either
direction. It establishes two facts about the
join surface between the frozen classification
and this corpus: the classification's universe
covers barely half the signs the corpus's
documented rows use, and its celestial class is
empty. The claim
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
stands UNTESTED exactly as recorded, and no
dated append is made to its record, because the
§4.6 closure wordings carry the claim forward
unchanged — the appends belong to the verdict
classes, and this execution reached none. A
successor that wants this question answered
needs two repairs, both freeze decisions for a
new spec, not repairs this execution was
permitted to make: a depicted-kind
classification whose universe covers the signs
the corpus actually uses (or a design that
scopes its population to the covered signs and
says so), and — on the evidence of the frozen
asset — a celestial class that exists. Spec
050's frozen closure stands untouched.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
