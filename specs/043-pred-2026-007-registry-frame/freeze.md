# Spec 043 — Freeze Record (PRED-2026-012 at Full Population, Corrected Registry Frame; Successor to Spec 038)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner AS WRITTEN on 2026-10-21
> (Wave 2 freeze wave, delegated;
> `adjudication.md` §7). That campaign approval
> is also this member's Wave 3 execution
> authorization: the register's PRED-2026-012
> scoring gate ("registration alone is not a
> scoring order; scoring requires Spec 043's
> freeze and a separate owner execution order")
> is answered by the campaign approval itself,
> which orders this member's execution in Wave 3
> (campaign plan Part 4) — the citation is
> recorded in `adjudication.md` §7.6. The AEE
> lifecycle hooks ran over the register first
> (register recovered to 0.7-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). The freeze also files this spec's
> own OSF registration (campaign E-1, DD-043-11;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-410** under this frozen contract and
> **awaits the verified approval of that OSF
> registration**: the freeze merge does not wait
> for the approval click, but execution does.

## 1. Basis

The contract implements design D-31's successor:
PRED-2026-012, registered 2026-10-21 under
campaign ruling E-4 (`adjudication.md` §6),
carrying PRED-2026-007's frozen prediction and
success criterion verbatim, scored over the full
enumerated ITM population on the corrected frame
Spec 038's closure made necessary — the
canonical sign registry as primary source (its
coded values verified in full at draft, its
population listed in the draft), a re-derivation
gate on the column that defines the population,
and a documentary provenance gate on what the
ITM assignments rest on (spec §3, §4 check 0.3).
PRED-2026-007's own entry stands untouched and
remains PARTIALLY CONFIRMED as its pre-execution
record.

The design's factual basis was re-asserted at
this freeze by two independent routes
(`adjudication.md` §7.7): the pinned registry
(SHA-256 `8a0b2a82…`; 803 rows, 791 uncoded, 12
coded; ITM population P056, P324, P378, P385),
the builder rule reproducing all 803 recorded
`icit_function` values exactly, the cross-check's
pin (`8c2bd605…`), the builder's (`4af822f1…`),
the parser's (`9b57f0ec…`), the recorded Phase 5
output's pins (`623a787d…`, `54ebf660…`), and the
register as reconciled (`254ccf03…`,
re-derived, not inherited).

The freeze decided the open points
(`adjudication.md` §7): **DD-043-10** (the
provenance gate's borderline standard adopted
as drafted — a basis counts only if stated in
words with a locator), **DD-043-11** (this spec
files its own OSF contract registration under
campaign E-1), **DD-043-12** (the LOG class is
enumerated-only, ruled as the draft frames it;
no LOG quantity is scored), **DD-043-13**
(execution phase allocated as **Phase-410**),
and **DD-043-14** (the DD-038-10 AEE gate
reading adopted).

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`,
computed by `build_freeze.py` in this
directory). Covered sources (nothing else
decides the question):

- `specs/043-pred-2026-007-registry-frame/freeze.md` (this
  document)
- `specs/043-pred-2026-007-registry-frame/spec.md`
- `specs/043-pred-2026-007-registry-frame/claims.json`
- `specs/043-pred-2026-007-registry-frame/adjudication.md`
- `specs/043-pred-2026-007-registry-frame/aee/freeze-aee-note.md`
- `specs/043-pred-2026-007-registry-frame/build_freeze.py`
- `backend/tests/test_spec043_freeze.py`

`tasks.md` and `osf-spec-registration.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds; the OSF record is completed by
append after filing).

## 3. What the freeze fixes

- **The criterion** (spec §7 / F043-C02): at
  least 70% of ITM-coded signs are TERMINAL or
  cluster in TERMINAL clusters, carried
  verbatim; CONFIRMED / NOT CONFIRMED are the
  only verdicts; the verdict rule is mechanical
  and no band is added; the population size is
  stated wherever the share is stated.
- **The population frame** (spec §2 /
  F043-C03–C05): every distinct sign the pinned
  registry codes exactly ITM — listed at draft
  as P056, P324, P378, P385 — with the
  re-derivation gate (check 0.2) and the census
  reconciliation; P098 excluded by rule
  (F043-C06); the LOG set enumerated-only
  (DD-043-12; F043-C07).
- **Step 0, fail-closed, in a fixed order**
  (spec §4): sources and pins; enumeration with
  re-derivation and census reconciliation; the
  provenance gate; recorded-output verification.
  No Phase 5 assignment is looked up for any
  sign, the sanity anchor included, until the
  provenance gate has passed (F043-C08).
- **The provenance gate** (spec §4 check 0.3 /
  F043-C09): evidence set D1–D4 fixed; three
  limbs (class definition, per-sign basis,
  source agreement); the DD-043-10 borderline
  standard; failure on any limb or any single
  sign closes the study as **PROVENANCE —
  CANNOT BE RUN AS WRITTEN**, unscored, with no
  subset verdict.
- **The scoring inputs** (spec §§5–6 /
  F043-C11): the recorded Phase 5 output only,
  cluster classes per DD-043-7; no
  re-clustering; the sanity anchor must
  reproduce.
- **The coverage rule** (spec §7 / F043-C12):
  the design's rule, carried from DD-038-4,
  fixed in advance; the census branch is
  foreclosed under this frame.
- **The fences** (spec §§8, 10 / F043-C10,
  C14–C16): every outcome statement carries
  the lineage boundary and the
  clustering-stability caveat; register
  consequences land by dated append only; the
  two closure names are never interchanged and
  never reported as verdicts.

## 4. Able-to-fail proof (freeze test)

`backend/tests/test_spec043_freeze.py` was
proved able to fail at the freeze, in a scratch
copy of the tree, before the final digest was
computed: a scratch mutation of the frozen
register (register_version altered) turned
`test_register_integrity` red, and a scratch
mutation of a covered source (this freeze
record) turned `test_freeze_record_replays`
red; both mutations were then restored
byte-identically and the suite re-ran green.
The freeze test follows the Spec 038 form for
the PRED register — its freeze-time hash is
asserted as a definition constant and its
entry's facts are asserted on the live file —
because the register is this contract's own
append target and the backend suite rewrites
register-adjacent stores mid-run; no live-file
hash is asserted on any suite-regenerated file.
(The full suite result at the freeze is
recorded with the freeze PR.)

## 5. What the freeze does not do

The freeze does not run the provenance
adjudication: check 0.3 is execution step 0,
its D3/D4 documents are produced and judged at
execution, and no basis statement has been
adjudicated by this freeze. The freeze computes
no share, looks up no Phase 5 assignment beyond
the register's three named signs (whose anchor
the freeze test verifies as a form fact), and
changes no register text: PRED-2026-012 stands
PENDING and PRED-2026-007 stands PARTIALLY
CONFIRMED, exactly as the draft left them.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
