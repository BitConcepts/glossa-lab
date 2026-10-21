# Spec 030 — Owner Adjudication Record

> ## ADJUDICATED — 2026-10-12
>
> Owner decision (Tristen Pierson, 2026-10-12, verbatim):
> **"Freeze it"** — given in response to the science
> packets presented in the program chat on 2026-10-12
> (this spec's design draft and the Spec 027 Stage 2/Q7
> adjudication packet, together in draft PR #170).
>
> Reading of the instruction, recorded so the record is
> not ambiguous later: under the owner's established
> block-ratification pattern (Spec 027: "Approve Spec
> 027 with the recommended answers and freeze it";
> Spec 029: "ratify all of these as a block and do it";
> the same-day D-A…D-E block: "do all this"), "Freeze
> it" adjudicates this design by **adopting the
> design's stated proposals for §9 Asks 1, 3, 4, and 5
> as a block** and moving the spec to freeze. Ask 2
> states no proposal — see its entry below; it is
> expressly **not** covered by this ratification, and
> no answer is invented for it here.

## Ask 1 — Coordinate-less chronology rows (§5.7) → **ADOPTED AS PROPOSED**

Dated records whose origin carries no coordinates are
admitted to the chronology for a site whose cluster
the Stage 0 gazetteer already establishes, with the
chronology row's coordinate state recorded as
**inherited-from-cluster**. This is a rule of this
extension's build (integrity rule 7); it changes no
frozen criterion, threshold, grade rule, or material
mapping (F030-C01). Gazetteer changes are otherwise
out of scope, except assigning `program_site_id` to
genuinely new sites under the frozen name
normalisation.

## Ask 2 — CONTESTED sensitivity (§5.5) → **NOT DECIDED — EXPRESSLY NOT COVERED**

The design states no recommendation for this ask.
Claim F030-C04 is satisfied by the reporting
"whichever way the owner later rules on bindingness",
and §5 rule 5 puts the question to the owner without
a proposed answer. A block adoption of recommendations
cannot adopt a recommendation that does not exist.

Operative position until a future owner decision: the
re-test reports every criterion twice — as frozen
(all rows) and excluding CONTESTED-scenario rows —
under integrity rule 5 and F030-C04, and the
as-frozen computation is the assessment's verdict
basis. Whether the sensitivity must also **bind** a
future Q6 freeze is reserved to that freeze's own
adjudication under Spec 027 §8.2.

## Ask 3 — Tracing selectivity (§3.3) → **ADOPTED AS PROPOSED**

Origin records are traced in **short-lived-first
order** (the design's proposal), with the full pool
reported. The selectivity is in tracing order only:
grading stays rule-bound per row under the frozen
rule, and no traced row is ever excluded from the
pool to shape a criterion value (§5 rule 3). The
parametric consequence the design states stands as
the build's planning fact: with *g* long-lived
grade-ups, the C3 requirement is *s* ≥ 31 + *g* net
new short-lived window d/a rows.

## Ask 4 — Route scope and posture → **ADOPTED; R3 POSTURE CONFIRMED**

All five routes run in the §4 order — **R5 XRONOS
re-retrieval → R1 origin-record tracing → R2
c14bazAAR source-database audit → R4 TwoRains
published-supplement audit → R3 targeted
published-date extraction** — with a margins-only
interim assessment after each route (the §6
computation on the then-current pool, outcomes
uninspected beyond the four criterion values) and the
owner's stop points preserved. If the joint targets
are shown unreachable with routes remaining, that
showing is itself the negative closure (F030-C07) and
R3's labour is never spent.

Posture confirmed: R3 extraction enters the spine as
`open_access_read_only` — **internal-spine-only,
never in any CC BY release package** — mirroring the
Phase-124 CISI precedent (F030-C06). A source that
turns out `permission_required` stops at catalogue
and is reported; no route involves contacting anyone.

## Ask 5 — Phase and registration → **ADOPTED**

The build is **Phase-394** (the first free number
after Phase-393). Mirroring Spec 027 Stage 1, the
frozen contract — this spec as frozen by its freeze
record — is **registered on OSF before any
execution**. The registration is prescribed by this
adjudication as a precondition of execution; it is a
separate act and is not performed by this record or
by the freeze.

## Scope note

This record adjudicates §9 Asks 1, 3, 4, and 5 of
Spec 030. Ask 2 is expressly not decided (above). The
Q7 packet's six asks are adjudicated in their own
record (`specs/027-movement-culture-language/
stage2-q7-adjudication.md`), under the same owner
instruction. Nothing else is decided by this record.

## Freeze consequences

- Spec 030 freezes on this record: the design
  (`spec.md`, with §9 annotated DECIDED/NOT DECIDED
  under each ask, question text preserved) and the
  governed claim register (`claims.json`,
  F030-C01…C07) enter the freeze record
  (`freeze.md` / `freeze.json`, framework026 digest)
  built over them.
- **The Phase-394 build does not execute under this
  record.** Adopted Ask 5 makes OSF registration of
  the frozen contract a precondition of execution;
  execution follows registration under its own go,
  with the route scope adopted under Ask 4 as the
  build's scope and the §6 re-test — the Stage 0 §4
  assessment verbatim — as its only verdict-shaped
  output.
- Q6 remains owned by Spec 027 (F027-C16). This
  freeze changes no Spec 027 record; a Q6 freeze, if
  the re-test ever supports one, is a separate later
  act under Spec 027 §8.2 with its own freeze and
  owner gate.

AI disclosure: recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI. The decision text above is the
owner's, given in the program chat on 2026-10-12; the
decision substance is the design's stated proposals
as presented to and ratified by him.
## Ask 2 — owner ruling, 2026-10-21 → **DECIDED: BINDING**

> Owner decision (Tristen Pierson, 2026-10-21, given
> in the program chat via the options widget):
> **"Ask 2 is decided BINDING: a future Q6 freeze's
> timing-support assessment must meet every frozen
> criterion with CONTESTED-scenario rows excluded as
> well as with all rows included, and a support claim
> that holds only with contested rows included does
> not authorise a Q6 freeze."**

This entry records the ruling the Ask 2 entry above
expressly reserved to a future owner decision. The
2026-10-12 entries stand untouched: Asks 1, 3, 4,
and 5 were decided there; Ask 2 was not, and is
decided only here.

Basis of record: the decision memo of 2026-10-21
(`spec030-ask2-decision-memo-2026-10-21.md`, held
in the owner's research notes), which recommended
BINDING and verified against the Phase-394 record
that the ruling changes no standing outcome: the
re-test reported both computations and they
returned identical values (C1 1 FAIL, C2 6 FAIL,
C3 0.0 FAIL, C4 70 BP PASS under both), so Q6
remains NOT-YET-TESTABLE either way.

Consequence: the operative position recorded in
the Ask 2 entry above — both computations
reported, the as-frozen (all-rows) computation as
the assessment's verdict basis — is superseded
for future Q6 freezes: from this ruling, a future
Q6 freeze's timing-support assessment must meet
every frozen criterion under both computations,
and a support claim that holds only with
contested rows included does not authorise a Q6
freeze. The both-ways reporting duty (integrity
rule 5; F030-C04) is unchanged, and this ruling
alters no frozen criterion, threshold, or
Phase-394 record.

AI disclosure: recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI. The ruling text above is the
owner's, adopted verbatim from the decision memo's
ruling sentence as presented to and selected by
him on 2026-10-21.

## Freeze-test amendment — owner-ordered, 2026-10-21

The Ask 2 ruling entry above is a dated append to
this file, and this file is a digest-covered source
of the Spec 030 freeze: `freeze.json` pins its
whole-file SHA-256
(`f962f910d81cb63f44abb4db0e1be2ee0fb9fca45f5242f23656113ddd609738`;
5,867 bytes) among the freeze's sources, under the
freeze-act digest
`3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3db00e9`.
The freeze replay fence —
`backend/tests/test_spec030_freeze.py::test_freeze_record_replays`
(framework026 `verify_freeze` over every covered
source) — therefore failed on the ruling record
(PR #241, run 39573949471) by construction: the
backend suite's single failure, `frozen source
changed: specs/030-q6-chronology-spine-extension/adjudication.md`,
in an otherwise 1,366 passed / 20 skipped suite
with the run's other six jobs green. No frozen
byte was altered — the ruling is an append, and
the frozen bytes remain an exact prefix of this
file — but a whole-file fence cannot distinguish
an append from an edit. The conflict is between
the fence's form and this file's function: this
adjudication is the spec's ruling record, where
owner decisions are recorded by dated append, and
the frozen contract mandates no appends to it —
unlike Spec 038's register fence, no contract
term is in conflict; the fence's form alone
cannot carry the file's role.

**Ruling.** The owner ordered the amendment on
2026-10-21, verbatim: **"Amend the freeze test
(Spec 038 precedent)"**. The amendment is exactly
this, and nothing broader:

1. In `test_freeze_record_replays`, the replay of
   `adjudication.md` is narrowed to
   **prefix-integrity**: the bytes pinned at
   freeze time (5,867 bytes, SHA-256
   `f962f910d81cb63f44abb4db0e1be2ee0fb9fca45f5242f23656113ddd609738`)
   must remain an exact prefix of the live file;
   dated appends after them are permitted. The
   pin is carried in `freeze.json` (`prefix_pins`,
   hash and byte length) and asserted as a
   constant in the test. Every other covered
   source keeps its live whole-file hash
   assertion under the same `verify_freeze`
   replay; no other assertion changes, and no
   production code changes.
2. `freeze.json` is recomputed ONCE over the
   amended state with the repo's own builder
   (`build_freeze.py`, framework026
   `build_freeze`), in the freeze environment
   (python 3.12.3, aee 1.0.4), faithfulness-proven
   first: the pre-amendment builder over the
   original (pre-append, pre-amendment) bytes
   reproduces the freeze-act digest `3a61c63a…`
   exactly. The successor digest is the `digest`
   recorded in the amended `freeze.json` and is
   carried in the LEDGER entry of 2026-10-21
   recording this amendment.

**What does not change.** The freeze-act digest
`3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3db00e9`
stands as the digest of the freeze act in every
record that cites it — the OSF contract
registration (bge3k), `osf-registration.md`,
`outcome.md` — and is edited nowhere. The frozen
definition is untouched, including its
freeze-time statement that Ask 2's bindingness
was not decided at the freeze; the Ask 2 ruling
stands as recorded above, and Q6 remains
NOT-YET-TESTABLE. The guarantee the narrowed
assertion states is the one this file's role
requires: the frozen bytes are immutable — any
edit to them fails the fence — and appends after
them are dated and visible, never silent.

AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.
