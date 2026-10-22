# Spec 044 — Freeze Record (Fish-Sign Coastal Residue, Sign by Sign; Design D-02, Builds Asset F)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner AS WRITTEN on 2026-10-21
> (Wave 2 freeze wave, delegated;
> `adjudication.md` §7). The AEE lifecycle hooks
> ran over the register first (register recovered
> to 0.7-draft; `aee/freeze-aee-note.md`), and
> the digest in `freeze.json` was then computed
> **exactly once** over the recovered register
> and the finalised freeze texts (the Spec 035
> ordering). The freeze also files this spec's
> own OSF registration (campaign E-1;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-404**
> under this frozen contract, on a separate
> owner execution order, and **awaits the
> verified approval of that OSF registration**:
> the freeze merge does not wait for the
> approval click, but execution does.

## 1. Basis

The contract implements design D-02: the
sign-by-sign residue of the fish/coastal-traders
claim
`indus_valley_script_deciphered_from_myth_65ff0a26_manual_002`
(SETTLED, partially falsified on its
family-level coastal test), plus the one-time
build of Asset F, the frozen fish-family list.
The campaign plan's decisions stand recorded in
`adjudication.md` §§1, 7 (E-6: Asset F is built
here; E-2 / R-7: the Roif gate; E-1: this
freeze's OSF registration); the freeze does not
re-ask them.

The design's factual basis, verified first-hand
at draft and re-asserted at this freeze against
`main` head `83b6a563…`: the claim file
(SHA-256 `bc22d6f010f800d6…`; manual_002
partially falsified, stage explained), the
Spec 027 Stage 0 gazetteer (SHA-256
`5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6`;
36 rows, 30 sites), the Mahadevan–Parpola
crosswalk (SHA-256 `9ebd7723472d888d…`), the
anchors file (SHA-256 `df0cf620a0d66b7…`,
asserted at the freeze), and the Phase-45 T6
record (NO_ENRICHMENT for M047 at coastal sites,
n = 13, p = 0.685).

The freeze decided the open points
(`adjudication.md` §7): the consumer-name
correction (Asset F's consumer is **Spec 048**,
design D-04 — not Spec 045; §7.1), **OPEN-044-1**
(the CISI-based layer of record is identified
and pinned: the Holdat corpus file read by the
Phase-45/46/54 scripts, SHA-256
`62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`;
1,670 CISI-keyed inscriptions, 7,002 tokens,
reproducing the original population exactly —
M047 at 13 tokens, Fisher p = 0.685; gate 0.1
re-asserts this pin at step 0), **OPEN-044-2**
(Parpola 1994, fig. 5.1, pp. 70–78 confirmed as
Asset F's source; DD-044-5 confirmed),
**OPEN-044-3** (DD-044-7 confirmed: rule-built
coastal list, Lothal and Dholavira by name),
**OPEN-044-4** (DD-044-2 token primary and
DD-044-4 Bonferroni / Fisher one-sided
confirmed), **OPEN-044-5** (the spec files its
own OSF contract registration at the freeze),
and **OPEN-044-6** (execution phase allocated
as **Phase-404**). **DD-044-9** adopts the
DD-038-10 / DD-037-9 AEE gate reading.

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`,
computed by `build_freeze.py` in this
directory). Covered sources (nothing else
decides the question):

- `specs/044-fish-sign-coastal-residue/freeze.md` (this
  document)
- `specs/044-fish-sign-coastal-residue/spec.md`
- `specs/044-fish-sign-coastal-residue/claims.json`
- `specs/044-fish-sign-coastal-residue/adjudication.md`
- `specs/044-fish-sign-coastal-residue/aee/freeze-aee-note.md`
- `specs/044-fish-sign-coastal-residue/build_freeze.py`
- `backend/tests/test_spec044_freeze.py`

`tasks.md` and `osf-spec-registration.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds; the OSF record is completed by
append after filing).

## 3. What the freeze fixes

- **The layer** (spec §2 / F044-C07): the Holdat
  corpus file pinned in §1, keyed by
  `cisi_number` with per-inscription site
  attribution; gate 0.1 re-asserts the pin
  (export in full, hash, population
  reproduction) before any counting, and a
  failed re-assertion closes LAYER NOT PINNABLE.
- **Asset F** (spec §4 / F044-C05, C06): the
  fish-family list built at step 0 solely from
  Parpola's published list, every member
  carrying its per-sign locator; the canonical
  file's digest (digest field excluded) is the
  asset's identity; no in-place edits after
  freezing; Spec 048 consumes the asset by that
  digest under its own freeze.
- **The coastal list** (spec §3 gate 0.3 /
  F044-C08): frozen at step 0 under the design's
  rule from the pinned gazetteer and published
  geography, Lothal and Dholavira members by
  name, contested sites listed as contested, no
  site classed by its fish counts.
- **The test** (spec §5 / F044-C10): per member
  clearing the 30-occurrence floor, coastal
  share against the corpus-wide coastal share,
  sign tokens on both sides; Fisher's exact
  test, one-sided enrichment, Bonferroni
  family-wise correction at the 5% family
  level; ENRICHED requires the corrected result
  below 0.05 and a share ratio of at least 1.5;
  every member reported in full, with the three
  pre-registered sensitivities alongside.
- **The outcome set** (spec §6 / F044-C11):
  exactly one of ENRICHED MEMBER FOUND, NO
  MEMBER ENRICHED, TOO THIN, ASSET F FREEZE
  FAILED, LAYER NOT PINNABLE, COASTAL LIST
  FAILED, or INVALID, in §6's pre-written
  wording.
- **The fences** (spec §7 / F044-C01, C02, C13–
  C15): the family-level verdict stands and is
  not re-opened; no meaning conclusion; the
  Roif hold binds every output (records
  internal; campaign reporting names this
  member only as "executed — held under the
  Roif gate"); compilation-relativity stated
  wherever an outcome is stated.

## 4. Able-to-fail proof (freeze test)

`backend/tests/test_spec044_freeze.py` was
proved able to fail at the freeze, in the
scratch tree, before the digest was computed:
a scratch mutation of the frozen register
(register_version altered) turned
`test_register_integrity` red, and a scratch
mutation of a covered source turned
`test_freeze_record_replays` red; both mutations
were then restored byte-identically and the
suite re-ran green. (The full suite result at
the freeze is recorded with the freeze PR.)

## 5. Freeze repair (2026-10-21, pre-merge)

Recorded openly before the freeze merge (full
record: `adjudication.md` §7.11). The first
freeze commit (`1768785c`, PR #243) failed one
CI check: run `39581746155`, backend pytest,
failed only on
`test_cited_records_carry_the_design_facts` —
it asserted the live claim file's hash equals
the committed-bytes pin `bc22d6f010f8…`, but
the backend suite itself regenerates the
extracted-claims store mid-run
(`indus_claims.py` rewrites `extraction_date`
via `datetime.utcnow()`), so the working-tree
file hashed differently (`fbddaed1431f…`). The
pin is correct against committed bytes; no
frozen fact was wrong. Under the coordinator
ruling that the freeze is not locked until
merged (Spec 042 freeze §6 precedent), only
that assertion was repaired, to the Spec 038
form: the claim-file hash stands as a
`freeze.json` definition constant only, and
manual_002's entry facts are asserted on the
live file, with the regeneration reason
commented in the test. The freeze digest was
then recomputed once over the final files:
old digest
`9a0e6518f187bc91b342d7e8a97b56632340a8aeda9a801bb4c572816e4440dd`
is superseded by the new digest in
`freeze.json` (stated in full, with both
registration ids, in the supersession note in
`osf-spec-registration.md`, which is not
digest-covered). The OSF registration filed
at the first freeze commit (`3urwf`, old
digest, pending and unapproved) is superseded
by a corrected registration carrying the new
digest. Execution (Phase-404) still awaits
the corrected registration's verified
approval.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
