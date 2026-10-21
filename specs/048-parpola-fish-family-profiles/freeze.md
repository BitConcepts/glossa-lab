# Spec 048 — Freeze Record (Parpola's Fish-Sign Family, Sign by Sign; Design D-04, Consumes Asset F)

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
> after filing). Execution runs as **Phase-408**
> under this frozen contract, on a separate
> owner execution order, and **awaits the
> verified approval of that OSF registration**:
> the freeze merge does not wait for the
> approval click, but execution does.

## 1. Basis

The contract implements design D-04: the fish
family tested sign by sign under the Phase-43
T2.4 ending-follower measure on the strict
corpus, repeated on the Holdat layer as a second
arm. The claim is
`parpola_2010_dravidian_solution_manual_002`
(IN QUESTION, partially supported — sign 72
passed T2.4, sign 267 failed it). The campaign
plan's decisions stand recorded in
`adjudication.md` §§1, 7 (E-6: Asset F is built
by Spec 044 and consumed here; E-2 / R-7: the
Roif gate; E-1: this freeze's OSF registration);
the freeze does not re-ask them.

The design's factual basis, verified first-hand
at draft and re-asserted at this freeze against
`main` head `0cf9cd2f…` by two independent
routes (contents-API raw and git-blob, agreeing
byte-for-byte on every file; full record in
`adjudication.md` §8): the claim file (SHA-256
`3202aeca1ddaf7e588ebf19b2eaf8c93d06a34ecebba20d06c1b22810dfb000c`;
manual_002 partially_supported, stage explained,
Mahadevan sign_ids [72, 64, 70]), the Phase-43
record (SHA-256
`78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4`;
T2.4 candidates [267, 72, 65, 59, 60, 70]; sign
72 — 181 occurrences, terminal fraction 0.259,
supported; sign 267 — 356, 0.038, not supported),
the anchors file (SHA-256 `df0cf620a0d66b7…`;
287 anchors, 94 `strict_sa_independent`), the
Mahadevan–Parpola crosswalk (SHA-256
`9ebd7723472d888d…`), and Spec 033's §4 corpus
statement (Spec 033 spec SHA-256 `eaea0e2e…`).

The freeze decided the open points
(`adjudication.md` §7): **DD-048-9** — the
coordinator's Asset F pin-timing ruling,
recorded as a decided item (below, §3);
**OPEN-048-2** confirmed — "strict corpus" is
the Spec 033 §4 V3 / Mahadevan-lineage corpus
with the gate-0.3 T2.4 reproduction as the
operative check (DD-048-10); **OPEN-048-3** —
the member PASS bar confirmed at **20%**
(DD-048-11); **OPEN-048-4** — DD-048-4 confirmed,
a second-arm failure closes the execution
(DD-048-12); **OPEN-048-5** — the control-set
matching rule fixed mechanically and DD-048-7's
"at or above" comparison confirmed (DD-048-13);
**OPEN-048-6** — the spec files its own OSF
contract registration under E-1 (DD-048-14);
**OPEN-048-7** — DD-048-5 confirmed, the join
via `mahadevan_number` with the UNMAPPED
disposition (DD-048-15); **OPEN-048-8** —
execution phase allocated as **Phase-408**
(DD-048-16). **DD-048-17** adopts the DD-038-10
AEE gate reading, and **DD-048-18** records a
factual correction: sign 72's anchors entry
(M072) exists, with validation status
`pending_non_sa_validation` — it is the strict
status, not the entry, that it lacks.

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`,
computed by `build_freeze.py` in this
directory). Covered sources (nothing else
decides the question):

- `specs/048-parpola-fish-family-profiles/freeze.md` (this
  document)
- `specs/048-parpola-fish-family-profiles/spec.md`
- `specs/048-parpola-fish-family-profiles/claims.json`
- `specs/048-parpola-fish-family-profiles/adjudication.md`
- `specs/048-parpola-fish-family-profiles/aee/freeze-aee-note.md`
- `specs/048-parpola-fish-family-profiles/build_freeze.py`
- `backend/tests/test_spec048_freeze.py`

`tasks.md` and `osf-spec-registration.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds; the OSF record is completed by
append after filing).

## 3. What the freeze fixes

- **The Asset F contract anchor and pin source**
  (spec §§2, 4 / F048-C05, C06; DD-048-9). Asset
  F is built at Spec 044's execution step 0
  (Wave 3), so no byte-digest exists at this
  freeze. This freeze quotes Spec 044's freeze
  digest —
  `6851f943d196fa389e48b67cb5161b90daa1180d8a3e1cf3f020fcf25691d9c8`,
  read from PR #243's branch (its corrected
  digest; Spec 044's freeze had not yet merged
  when read) — as the **contract anchor**, and
  fixes the **pin source** as Spec 044's step-0
  outcome record for the canonical file
  `specs/044-fish-sign-coastal-residue/asset-f-fish-family.json`.
  Gate 0.1 asserts the byte-digest at execution
  step 0 against that record, under Spec 044
  §4.2's digest-field exclusion rule: absence
  closes **ASSET F NOT AVAILABLE**, a mismatch
  closes **ASSET F DIGEST MISMATCH**, exactly as
  drafted. The asset is never rebuilt,
  re-derived, or substituted under this spec.
- **Membership and the join** (spec §§3–4 /
  F048-C05): family membership is exactly Asset
  F as frozen by Spec 044; the join runs via
  each member's `mahadevan_number` locator
  through the pinned crosswalk, with UNMAPPED
  as its own disposition (DD-048-15), and the
  gate-0.2 cross-check against the claim
  record's trio (72, 64, 70) and the Phase-43
  six reported with every divergence named.
- **The strict corpus** (spec §§2–3 / F048-C07):
  the V3 / Mahadevan-lineage corpus of Spec 033
  §4 (DD-048-10), identified, exported, and
  pinned at gate 0.3 before any counting, with
  the T2.4 reference points reproduced from the
  pinned layer; failure closes STRICT CORPUS
  NOT PINNABLE.
- **The measure and the bar** (spec §5 /
  F048-C08): Phase-43 T2.4, unchanged; a member
  PASSES at an ending-follower rate of **20% or
  more** (DD-048-11). The Holdat second arm is
  integral (DD-048-12); the 72/64/70 sensitivity
  is pre-registered and reported alongside.
- **The family rule and outcomes** (spec §6 /
  F048-C03, C04, C10, C11): token-weighted
  passing share over tested members (mapped, at
  or above the 30-occurrence floor) — FAMILY
  SUPPORTED at 70% or more, FAMILY NOT
  SUPPORTED at 30% or less, INCONCLUSIVE
  between or on a cross-arm disagreement about
  the most frequent tested member — and exactly
  one headline outcome from §6's pre-written
  wordings, including the step-0 closures
  (TOO THIN, ASSET F NOT AVAILABLE, ASSET F
  DIGEST MISMATCH, STRICT CORPUS NOT PINNABLE,
  SECOND ARM NOT RUNNABLE) and INVALID.
- **The controls** (spec §§3, 5 / F048-C13): the
  gate-0.6 frozen set of non-fish animal signs
  under the matching rule fixed at DD-048-13,
  run through the identical measure; controls
  passing at or above the family's share report
  the fish result as a positional fact, not as
  support for the reading (DD-048-7).
- **The fences** (spec §7 / F048-C01, C02,
  C14, C15): no pronunciation or meaning
  conclusion; no mechanism for sign 267;
  compilation-relativity stated; the **Roif
  hold (R-7)** binds every output — records
  internal, nothing published or surfaced,
  campaign reporting names this member only as
  "executed — held under the Roif gate."

## 4. Able-to-fail proof (freeze test)

`backend/tests/test_spec048_freeze.py` was
proved able to fail at the freeze, in the
scratch tree: a scratch mutation of the frozen
register (register_version altered) turned
`test_register_integrity` red before the digest
was computed, and a scratch mutation of a
covered source (this document) turned
`test_freeze_record_replays` red; both mutations
were then restored byte-identically and the
suite re-ran green. (The full suite result at
the freeze is recorded with the freeze PR.)
The test asserts the claim file's facts on the
live file and its freeze-time hash as a
definition constant only — the Spec 038 form —
because the backend suite regenerates the
extracted-claims store mid-run (the Spec 044
freeze-repair lesson).

## 5. What this freeze does not do

- It does **not** build Asset F, state its
  byte-digest, or name any member beyond the
  record's own reference signs: the asset is
  Spec 044's execution step 0, and this
  freeze's gate 0.1 asserts its digest then
  (DD-048-9).
- It does **not** identify or pin the strict
  corpus or the Holdat layer: gates 0.3 and
  0.4 do that as fail-closed acts at step 0.
- It counts **nothing**: no census, no
  ending-follower rate, no control figure was
  computed at the freeze.
- It does **not** authorise execution or
  publication. Execution is Phase-408 on a
  separate owner execution order, after this
  freeze has merged and the OSF registration's
  approval act has completed. Publication of
  any result remains under the **Roif hold
  (R-7)**: the OSF registration filed at this
  freeze carries the frozen contract (a design
  text) only and clears nothing under the gate.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
