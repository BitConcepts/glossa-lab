# Spec 050 — Freeze Record (Hunt: Sky Signs at the Ends of Texts — Design D-13; Consumer of Asset A)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner AS WRITTEN on
> 2026-10-21 (campaign Wave 2; `adjudication.md`
> §7). The AEE lifecycle hooks ran over the
> register first (register recovered to
> 0.8-draft; `aee/freeze-aee-note.md`), and the
> digest in `freeze.json` was then computed
> **exactly once** over the recovered register
> and the finalised freeze texts (the Spec 039
> ordering). The freeze also files this spec's
> own OSF contract registration under campaign
> decision E-1 (DD-050-14;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-416** under this frozen contract, as
> a separate later act: it awaits the
> registration's approval, the campaign's
> execution pass (Wave 3), and Spec 045's
> execution building and freezing Asset A —
> and no sign was classified, no census taken,
> and no final-position quantity computed at
> the freeze.

## 1. Basis

The contract implements design D-13 (PR #195
packet, §D-13) over the claim
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
— Hunt's sky-signs-at-the-endings claim —
standing **UNTESTED**: Phase-104, RULE-CLASS —
the claim's falsifier requires a defined class
of celestial signs, and no such classification
existed in the repository's data. The class
comes from Asset A, the depicted-kind
classification built once inside Spec 045
(campaign decision E-6), consumed here as
exactly its `sky_cycle` kind. Its factual
basis is the §6 input set as pinned at draft
and **re-asserted at this freeze against
`main` at `e3399961` by two routes**
(contents API and git-data blob API; every pin
recomputed in the foreground and matched,
the two routes agreeing byte-for-byte): the
corpus layer (`c02e3d7b…`, 5,679 rows), the
positional record (`0e546962…`: 805/2,267,
rate 0.355 against null 0.006; 40/61/20
strong-sign classes), the Phase-43 battery
record (`78a6c219…`), the crosswalk master
(`4ace1a61…`: 205 rows, 187 distinct
`registry_sign_id` values), and the anchors
file (`df0cf620…`, 287 anchors). The
Phase-104 record for the claim was read at
the freeze: the claim stands `stays_untested`
under RULE-CLASS, for the reason the draft
states.

The freeze decided every open point
(`adjudication.md` §7): **DD-050-9** (the
DD-038-10 AEE gate reading adopted),
**DD-050-10** (Phase-416 allocated),
**DD-050-11** (the coordinator pin-timing
ruling: Spec 045's freeze digest
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`
quoted as the **contract anchor**, Spec 045's
`asset-a/asset-a-freeze.json` fixed as the pin
**source**, and gate 0.1 ruling the SHA-256
assertion at execution step 0 — mismatch
CLOSED AT STEP 0 — ASSET PIN MISMATCH,
unfrozen CLOSED AT STEP 0 — ASSET NOT FROZEN,
exactly as drafted; the same ruling as Specs
048/049/051), **DD-050-12** (coverage stands
as drafted on Spec 045's frozen full-universe
scope: the **DD-045-18 consequence** — Asset A
covers the FULL pinned-crosswalk sign universe
of 187 distinct sign keys, gate A3 restated to
that scope, so this spec's gate 0.3 does not
close INVALID for want of corpus-wide coverage
on that ground; no narrowing of the comparison
population is recorded), **DD-050-13**
(DD-050-1 to DD-050-6 confirmed as drafted;
**DD-050-1 FROZEN** — the celestial class is
Asset A's `sky_cycle` kind exactly, the
broader jurisdiction-inclusive closing notion
stated as an untested boundary in §2.2, never
silently widened), **DD-050-14** (the OSF
registration filed at the freeze; execution
awaits its approval), and **DD-050-15** (no
calibration beyond gate 0.5's reproduction is
required).

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/050-hunt-sky-signs-endings/freeze.md` (this
  document)
- `specs/050-hunt-sky-signs-endings/spec.md`
- `specs/050-hunt-sky-signs-endings/claims.json`
- `specs/050-hunt-sky-signs-endings/adjudication.md`
- `specs/050-hunt-sky-signs-endings/aee/freeze-aee-note.md`
- `specs/050-hunt-sky-signs-endings/build_freeze.py`
- `backend/tests/test_spec050_freeze.py`

`tasks.md` and `osf-spec-registration.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds). This spec has no separate
`plan.md`; `tasks.md` carries the plan.

## 3. What the freeze fixes

- **The celestial class** (spec §2 / F050-C05,
  C07): exactly the set of signs whose Asset A
  row carries `depicted_kind = sky_cycle`, one
  row per sign keyed by the pinned crosswalk
  identity, contested signs excluded from the
  primary, the broader closing notion an
  expressly untested boundary (DD-050-1,
  DD-050-13).
- **The Asset A consumption form** (spec §2.3 /
  F050-C06; DD-050-11): Spec 045's freeze digest
  quoted as contract anchor; Spec 045's
  `asset-a/asset-a-freeze.json` fixed as the pin
  source; gate 0.1 asserting the recorded
  SHA-256 against the recomputed digest of the
  canonical CSV at execution step 0, before any
  join or counting, with the two step-0 closure
  classes exactly as drafted.
- **The gates** (spec §3 / F050-C12): step-0
  gates 0.1–0.6, fail-closed, before any
  final-position quantity — the digest
  assertion (0.1), input integrity (0.2),
  coverage and join completeness at the
  corpus-wide scope DD-045-18 supplies (0.3),
  the totals-only class census with the
  symmetric 30-occurrence TOO THIN floor (0.4),
  positional reproduction (0.5), and the
  freeze-order proof (0.6).
- **The test** (spec §4 / F050-C03, C09–C11,
  C13): text-final position as the pinned
  framework counts it; the frequency-matched
  comparison class (the class's own count
  range, DD-050-2); the enrichment ratio
  against it with Fisher's exact test,
  two-sided, at the 5% level (DD-050-4); the
  criteria of §4.3 (SUPPORTED at ratio ≥ 1.5
  with the test passed and the
  half-of-occurrences condition; NOT SUPPORTED
  at ratio ≤ 1.0; INCONCLUSIVE otherwise; TOO
  THIN as INCONCLUSIVE's recorded form,
  DD-050-3); the full per-sign table; and the
  two pre-registered sensitivities (S1
  borderline removed; S2 contested included
  under CISI-governed `sky_cycle` labels).
- **The outcome classes** (spec §5 / F050-C14):
  SUPPORTED / NOT SUPPORTED / INCONCLUSIVE /
  TOO THIN, the two CLOSED AT STEP 0 classes,
  INVALID, and NOT ADJUDICATED (the
  reconciliation-failure class, DD-050-5), each
  with its pre-written §5.2 wording.
- **The fences** (spec §7 / F050-C01, C15):
  position is not meaning; the class is the
  sky only; depiction is the
  published-identification layer, not ground
  truth; Spec 037's 49% census caution travels
  with the asset and every verdict.

## 4. What this freeze does not do

It does not build Asset A (the asset is BUILT
at Spec 045's execution step 1, Wave 3),
classify any sign, quote any Asset A digest
(none exists; the freeze fixes the contract
anchor and the pin source instead, DD-050-11),
take any class census, compute any
final-position rate or any other quantity, or
file any outcome on the claim's record. It
does not test Hunt's closing part in any form
broader than the sky (§2.2), and it does not
amend design D-13, Spec 045's frozen record,
or any other spec. Execution (Phase-416) is a
separate act, gated as stated in the header
above.

## 5. Tooling pins

- AEE package **1.5.0** (pin `>=1.5.0,<1.6`),
  run from the venv `glossa-aee150`.
- specify CLI **1.0.10**; Python **3.12.3**.
- Freeze test: `backend/tests/test_spec050_freeze.py`
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
  was a scratch probe only and is not part of
  the frozen tree.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
