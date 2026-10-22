# Spec 046 — Freeze Record ("Sign 297 Is the Horned Tiger": an Identification Concordance)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner AS WRITTEN on
> 2026-10-21 (campaign Wave 2; `adjudication.md`
> §7). The AEE lifecycle hooks ran over the
> register first (register recovered to
> 0.7-draft; `aee/freeze-aee-note.md`), and the
> digest in `freeze.json` was then computed
> **exactly once** over the recovered register
> and the finalised freeze texts (the Spec 039
> ordering). The freeze also files this spec's
> own OSF contract registration under campaign
> decision E-1 (DD-046-18;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-405** under this frozen contract,
> as a separate later act: it awaits the
> registration's approval and the campaign's
> execution pass (Wave 3, group 1, before
> Asset A freezes), and no list was opened
> for scoring at the freeze.

## 1. Basis

The contract implements design D-18 (PR #195
packet, §D-18) over the fragment
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`
— "Sign value: 297 / the horned tiger, or
perhaps just 'tiger' generically" — stopped
at Phase-104 under RULE-NUM. Its factual
basis is the §2 input set as pinned at draft
and **re-asserted at this freeze against
`main` at `83b6a563`** (every pin recomputed
and matched): the claim record
(SHA-256 `bd0f7abd…`), the held cleaned text
of Wells 2015 (`62acf855…`, the passage at
printed p. 97), the Phase-104 evaluation
(`2d0b83e8…`), the crosswalk registry
(`8a0b2a82…`, 803 rows), and the lane-2
adopted drafts file (`3f645c9a…`).

The freeze decided every open point
(`adjudication.md` §7): **DD-046-9** (PARTIAL
CONCURRENCE confirmed, in its space form —
the total outcome set stands as the design
repair of record), **DD-046-10** (the Wells
list of record: the 2015 book's own sign
apparatus, Chapter 2 / Figure 2.6),
**DD-046-11** (the CISI list of record: the
catalogue apparatus of CISI Vol. 1 (1987;
MASI 86) and Vol. 2 (1991) as held, with the
Parpola list — *Deciphering the Indus
Script*, 1994 — named in the same decision),
**DD-046-12** (the Mahadevan edition of
record: *The Indus Script: Texts, Concordance
and Tables*, MASI No. 77, 1977 — M77),
**DD-046-13** (the lineage note added to the
CONSENSUS wording, before any row is scored),
**DD-046-14** (the Spec 045 cross-check: see
§3), **DD-046-15** (no separate dry-run sign
required), **DD-046-16** (the DD-038-10 AEE
gate reading adopted), **DD-046-17**
(Phase-405 allocated), and **DD-046-18**
(the OSF registration filed at the freeze;
execution awaits its approval). DD-046-1,
DD-046-2, DD-046-3, and DD-046-6 stand
confirmed as drafted.

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/046-horned-tiger-concordance/freeze.md` (this
  document)
- `specs/046-horned-tiger-concordance/spec.md`
- `specs/046-horned-tiger-concordance/claims.json`
- `specs/046-horned-tiger-concordance/adjudication.md`
- `specs/046-horned-tiger-concordance/aee/freeze-aee-note.md`
- `specs/046-horned-tiger-concordance/build_freeze.py`
- `backend/tests/test_spec046_freeze.py`

`tasks.md` and `osf-spec-registration.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds). This spec has no separate
`plan.md`; `tasks.md` carries the plan.

## 3. What the freeze fixes

- **The gates** (spec §3 / F046-C05): step 0
  closes the run on an input pin mismatch, an
  unproducible source, or a list that is
  neither held nor citable with a locator —
  no three-list concordance exists.
- **Identification before scoring** (spec §4 /
  F046-C06, C07): the source's sign list is
  named from the book's own apparatus; the
  drawn sign is matched by drawn form, never
  by number, with the registry's two traps
  (P297 the ladder motif; W297 inside the
  P205 multi-value cell) named in advance.
- **The scoring and the total outcome set**
  (spec §5 / F046-C08–C10): AGREE / DISAGREE /
  SILENT per list, with `entry_present` on
  silence; Wells scored as SOURCE and never
  counted toward CONSENSUS; the mapping
  CONSENSUS / CONTESTED / PARTIAL CONCURRENCE /
  SINGLE-SOURCE is total over every score
  pattern.
- **The delivery form** (spec §6 / F046-C11):
  `concordance-297.json` in the frozen form,
  produced on every terminal outcome — on a
  closure, an empty `signs` array plus a
  `closure` block; on CONTESTED, the feed
  records the dispute instead of picking a
  side.
- **The Spec 045 cross-check verdict**
  (DD-046-14): aligned in form; **not aligned
  in outcome vocabulary**. Spec 045's draft
  §2.6 enumerates no PARTIAL CONCURRENCE
  consumption rule, does not name the CLOSED
  AT STEP 0 class, and rejects a row whose
  crosswalk key does not resolve, while this
  spec lawfully produces a Wells-list-entry
  match with a null registry id. That is a
  FREEZE-stage finding for Spec 045's freeze
  to repair on its side; this spec's outcome
  vocabulary was not changed to fit.
- **The fences** (spec §9 / F046-C01, C14):
  identification layer only; concordance is
  not correctness; one sign only; closures
  and non-consensus outcomes publish with the
  same prominence as consensus.

## 4. What this freeze does not do

It does not execute the concordance, open any
list for scoring, identify the drawn sign,
file any outcome on the claim's record, or
build any part of Asset A. It does not amend
design D-18, Spec 045's draft, or any frozen
record. Execution (Phase-405) is a separate
act, gated as stated in the header above.

## 5. Tooling pins

- AEE package **1.5.0** (pin `>=1.5.0,<1.6`),
  run from the venv `glossa-aee150` — the
  task-named `glossa-aee153` venv stands as
  an empty shell on the freeze machine, so
  the named fallback was used and the version
  is recorded in `freeze.json` and in
  `aee/freeze-aee-note.md`.
- specify CLI **1.0.10**; Python **3.12.3**.
- Freeze test: `backend/tests/test_spec046_freeze.py`
  (6 tests), proven able to fail at this
  freeze, before the final digest was
  computed: with a provisional digest in
  place, all 6 tests passed; a scratch
  mutation (one appended line,
  `MUTATION-PROBE`, in the covered source
  `spec.md`) turned `test_freeze_record_replays`
  red (1 failure, the other 5 still passing);
  restoring `spec.md` byte-identically
  returned all 6 tests to green. The mutation
  was a scratch probe only and is not part
  of the frozen tree.

## 6. Amendment — 2026-10-21 (pre-merge, on first CI)

The freeze PR's first CI run (run
39581775853) ran 6 of 7 jobs green; the
backend job failed on exactly one test —
this spec's `test_cited_records_carry_the_design_facts`
— and on no other (1 failed, 1,419 passed).
Cause, verified from the job log: the test
asserted live byte equality of the §2 pins
against the working tree, but the suite's
own Spec 029 regeneration tests run earlier
in the same suite and rewrite the
claim-lifecycle records (the claim record,
the Phase-104 evaluation, the lane-2
drafts) in the working tree with fresh
`extracted_at` timestamps, so the claim
record's live hash (`3eb89c04…`) differed
from its committed bytes (`bd0f7abd…`) for
that reason alone. The committed bytes, the
§2 pins, and every other freeze fact are
unchanged; the step-0 pin check remains an
execution-time act over a pristine checkout
(spec §5.1), exactly as frozen.

The correction is confined to the freeze
test: the pins stand asserted as freeze-time
facts against `freeze.json`'s definition
(`test_freeze_definition_constants`), and
the cited-records test now asserts that each
cited record is present and carries its
design facts (the claim entry untested with
the horned-tiger claim; the passage verbatim
in the source text; the Phase-104 RULE-NUM
stop for this claim; the registry census and
traps, unchanged). No claim, decision,
outcome, or contract wording changed.

A second, smaller correction followed on
the amended run (run 39583029748): the
backend job went green — the correction
above held — but the three shell-wrapper
jobs failed ruff on the amended test file
(F401: the `hashlib` import the first
correction had left unused). The unused
import was removed; nothing else changed.
Both corrections are confined to the freeze
test file and this section.

Because the test is a digest-covered source,
`freeze.json` was recomputed **exactly once**
over the amended state (both corrections in)
with this directory's `build_freeze.py`.
Following the Spec 030 precedent: the
freeze-act digest computed at the freeze
(`80c3be31…`, full value in
`osf-spec-registration.md`) stands as the
digest of the freeze act in every record
that cites it, including the filed OSF
registration `dnts8`; the successor digest
is the value in `freeze.json` as merged, and
is recorded in full in
`osf-spec-registration.md`. The amended test
suite was re-proven able to fail on the
amended tree: the same `spec.md` mutation
turned the replay test red, and the restore
returned all 6 tests to green.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
