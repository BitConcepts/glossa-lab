# Eteocypriot Program — Outcome Record

**Date:** 2026-11-20. **Program:** Spec 096 — Eteocypriot
Program, Stages 2–3 (registered analysis; outcome and
adjudication package). **Basis:** the freeze record
(`records/freeze-record-2026-11-20.md`, Stage 1, PR #605 merged
at `15d8b493c002301fdace64be7dac324fcbb44cd0`) and the E1 run
record (`records/eteocypriot-e1-run-2026-11-20.json`, produced
by `records/eteocypriot-e1-driver.py`). Every number below is
read from those records. All computation ran on the
mini-server, under the owner's standing execution-home rule.

## 1. What ran

E1's ICS 196 leg, under the frozen procedure (freeze §5), on
the frozen corpus (file SHA-256 verified by the driver against
the freeze pin before loading, fail-closed:
`5077285e8eac4b21785ca29cb151d47407f780998d85fa1eea27ef9d7e04f2dd`;
development pins verified; held-out records loaded: 0 — the
seal was never broken). The driver is deterministic: the filed
run record is byte-identical to an independent rehearsal run
over the same bytes.

E2 did not run: it closed TOO THIN at freeze (floor F-E2,
freeze §6), and its precondition (E1 success) also failed. No
candidate was developed or registered, and no held-out text
was scored. E3 did not engage: it engages only for E2
survivors, of which there are none.

## 2. E1 results (run record)

Development material scored: ICS 196, 11 segments, Greek side
7 words. Ground truth (freeze §5): Ἀρίστωνα (word 5) ↔ segment
6 (a-ri-si-to-no-se); Ἀριστώνακτος (word 6) ↔ segment 7
(a-ra-to-wa-na-ka-so-ko-o-se).

Derived spellings (rules R1–R3 only): Ἀρίστωνα →
a-ri-si-to-na; Ἀριστώνακτος → a-ri-si-to-na-ka-to-so.

**A1 (strict segment-parallel): 0 of 2 recovered.**
Ἀρίστωνα pairs positionally with segment 5 (la-sa-na), not its
correspondent; Ἀριστώνακτος pairs with segment 6
(a-ri-si-to-no-se), not its correspondent. The bilingual's
Eteocypriot version is roughly twice the Greek's length and is
not a literal translation (freeze §1), and the positional
assumption fails on both names.

**A2 (name-anchored free): 1 of 2 recovered.** Ἀρίστωνα: best
segment is 6, LCCS 4 (a-ri-si-to) — its correspondent,
recovered. Ἀριστώνακτος: best segment is 6, LCCS 4
(a-ri-si-to), not its correspondent segment 7 (LCCS 2) — not
recovered: the derived spelling's longest match sits inside
the patronymic's neighbour, because D(Ἀριστώνακτος) shares its
first four signs with D(Ἀρίστωνα) extended in segment 6
(a-ri-si-to-no-se) while the true correspondent spells the
name with a-ra-… (a-ra-to-wa-na-ka-so-ko-o-se). Full LCCS
tables for both names over all 11 segments are in the run
record.

**Androkles leg: TOO THIN at freeze** (floor F-E1b, freeze
§6): 0 Eteocypriot signs held for either dedication; the leg
was never administrable.

**P1 as registered: FAILS under both assumptions.** P1 is the
conjunction of both ICS 196 correspondences and at least one
Androkles correspondence. The ICS 196 conjunct fails under A1
(0/2) and under A2 (1/2); the Androkles conjunct is TOO THIN.
Precision basis: exact segment-level recovery counts and LCCS
scores over the complete development bilingual — a census of
the administrable material, not a sample.

## 3. Sensitivities (freeze §6)

- **S1 (ICS 194/195 under Perna 2019 vs Masson): not
  administered.** The Perna 2019 re-edition was NOT OBTAINED
  and the Masson leg holds form attestations only (7 forms,
  45 signs); there is no held-out scoring for either leg to
  vary.
- **S2 (Golgoi as its own stratum): not run** — E2/E3 are
  closed, and no Golgoi material was intaken.
- **S3 (results per alignment assumption): satisfied** — §2
  reports E1 under A1 and A2 separately.

## 4. Per-claim verdicts

**C096-1 (alignment procedure validated by known answers) —
NOT SUPPORTED.** The claim's falsifier is met: P1 fails under
both A1 and A2 (run record: A1_recovered_count 0,
A2_recovered_count 1, P1_passes_as_registered false). The
procedure is not validated; per the falsifier's own terms, E2
does not run. Precision basis: §2's exact counts over the
complete administrable leg; the Androkles leg is independently
TOO THIN (freeze F-E1b).

**C096-2 (at least one candidate predicts held-out material)
— TOO THIN.** E2 closed at freeze under its registered census
floor: held-out continuous text held is 0 legible signs
against a floor of 100 (freeze F-E2, §6). No candidate was
registered, no prediction was made, and the held-out seal was
never broken. The claim is neither supported nor falsified on
evidence; the leg is below its floor and is recorded TOO THIN,
the registered outcome class for that state. Precision basis:
the frozen census (freeze §3).

**C096-3 (survivors identifiable or reported as not) — NOT
ENGAGED.** The identifiability protocol (P3) engages only for
E2 survivors; there are none. No survivor was scored SUPPORTED,
so the claim's falsifier (a SUPPORTED scoring with no
rival-construction record, or with an equally consistent rival
unrecorded) is not triggered; the claim's positive content is
untested, not discharged. The claim stands at its intake state
and this record is its complete account. Precision basis:
vacuous — the survivor set is empty by the records above.

**C096-4 (the study reports its own thinness honestly) —
SUPPORTED.** Every outcome of the pilot is stated in this
record and the freeze with its precision basis (§§1–3: exact
recovery counts, LCCS tables in the run record, census counts
for every floor), and every below-floor leg is recorded TOO
THIN rather than scored as a result (Androkles leg, freeze
F-E1b; E2, freeze F-E2), including the closures made at freeze
under floors that could not be instantiated. The claim's
falsifier — a result reported without its precision basis, or
a below-floor leg scored as a result — does not occur in the
study's records.

## 5. Adjudication package (T302)

Prepared for the named human approver (proposal §6, item 3).
This execution changes no ledger standing: C096-1..C096-4 stand
in the ledger at their intake state (draft / created; ledger
canonical SHA-256
`09ca2407e2a7769e5fe73ded8402d22998ef8388ede777617fbfa678eb6f9a53`).
The package for adjudication is this record together with the
freeze record and the E1 run record: the verdicts of §4, each
with its evidence pointers (freeze §§3, 5, 6; run record legs
and P1 blocks), are what a recorded adjudication would enter.
An automated actor never approves, verifies, or promotes; the
standing changes, if any, are the approver's act on this
package.

## 6. Program state at outcome

The pilot is complete as registered. Its terminal outcomes:
E1 falsified the validation claim on the administrable leg;
the corpus, as lawfully obtainable at execution, is too thin
for the held-out experiment; the identifiability stage never
engaged. What would change the position is named in the freeze
record's survey: a text-accessible edition of the Androkles
syllabic sides (Hermary & Masson 1982, pp. 236–238) and of
Perna 2019's re-edition of ICS 194/195 (BCH Suppl. 60,
pp. 213–220) — acquisition routes are an owner act; none was
taken here, and no expert was contacted.

**AI disclosure:** executed by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution sec. VI.
