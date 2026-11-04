# Stage S1 freeze record (T103) — Spec 090 (2026-11-04)

**Scope:** tasks.md T103 — revision and freeze of the G1
document, executed on branch `feat/090-s1-g1-document`
(PR #514) on top of the draft act (T101, head f43447bb) and
the adversarial pass (T102, head ac09c517). Inputs: the
pass record (`records/stage-s1-adversarial-record.md`),
whose findings F1–F9 carry the repairs this act executes;
the adopted spec's plan.md Stage 1 and tasks.md T103;
claims C090-1..8 and C090-12; decision D-090-1 (the
document is versioned; amendments are recorded acts — this
record is the amendment act that produces v1.1 and the
freeze act that closes the stage).

## The G1 outcome

**G1: STATED.** Every sustained attack was answerable by
revision, so the NOT YET exit is not taken: the projection
stands stated as a rule (§2, as repaired), and the absolute
audit closes on its disposition (below). The D-090-2
owner-oracle rule **does not fire**: the pass sustained no
attack on the audit's disposition and the disposition is
not split — attack (i) was not sustained, and the pass's
hunt for practice absolutes the audit omits found none.

**The disposition, standing as audited and as attacked:**
no candidate absolute satisfies the test of §3.1; the
record system takes **no primitive absolute** (D3's
none-needed branch, §3.9 as revised under F8).

## The frozen document

`records/g1-document.md`, **version v1.1**, 34,226 bytes,
**SHA-256
4f2018f40c9ccaf0811cd7661b0c9e1ebd840c7e014d954f778c42edef27efc2**
(recomputed from the committed file in the revision commit
f565ca5; the working-tree hash and the committed blob's
hash agree). It supersedes v1 (31,376 bytes, SHA-256
974d5043ab463d0e6a33912b6e1136bcac288cd679827edade3c81d7af858d5b,
recorded in `records/stage-s1-record.md`, which stands
unamended as the draft act's record).

**Freeze statement.** G1 v1.1, at the hash above, is the
document Stage 2 derives against and the document an
independent reader is handed. Further changes are new
versions by recorded amendment act under D-090-1; a
revision the derivation forces would itself be a finding
for the outcome record (plan.md, design rules).

## Findings disposition (T102 → T103)

| # | Severity | Repair made in v1.1 | Location |
|---|---|---|---|
| F1 | High — required | §2.3's equivalence is quantified over the exercised inventories: Σ_O / Σ′_O are defined (the signs γ / γ′ assign somewhere on O) and β runs between them; a closing passage states the consequence — a state differing only by an unexercised inventory member has the same exercised inventory and the same table, and is equivalent. §2.3 and §2.4α now answer the pass's Case Z the same way (equivalent). Both illustrations survive: B's split subtypes are both exercised (code 047: 375 initial / 166 non-initial occurrences, per the pass), C's relabeling is a β | §2.3 |
| F2 | High — required | §2.4α re-stated: its equivalence claims are confined to what repaired §2.3 decides (same identity structure over surviving tokens up to relabeling of exercised signs; the unexercised-member case); realized splits and mergers are removed from the equivalence examples and carried as the epistemic point they make — realized in a rival classification they are *distinguished* by §2.3 whenever both resulting types are exercised, and the records do not determine which named state is the script's own. α's counts are untouched | §2.4α |
| F3 | Medium — required | "Named" restricted to the mode the records support: an explicit assignment over O, or a rule stated over the coded records of §1.2 (relabeling, split or merger of codes, re-segmentation) whose input is in R and whose output is the assignment. The glyph-data mode is expressly not admitted — §1 defines no glyph-data record class — and §2.3's decidability claim is scoped to named states in this sense | §2.1 |
| F4 | Medium — required | Both units stated correctly: the diplomatic text codes appear in **2,465 distinct code strings**, drawing on **535 distinct sign codes**. Both figures re-counted by this act from the snapshot at the branch head (codes parsed as the `+`-wrapped, `-`-separated token strings they are: 535 distinct tokens; 2,465 distinct strings) — agreeing with the pass's re-derivation | §1.5 |
| F5 | Low | CISI subset stated as the loader of record's own detail states it: "179 inscription sides (178 of them multi-sign)" (loader header: 178/179 have ≥ 2 signs) | §1.2 |
| F6 | Low | Reading direction stated with its coverage: "the value is `rtl` on 171 of 287 records, and the field is absent on 116" — re-counted by this act from the register at its pinned hash (171 carried, all `rtl`; 116 absent) | §1.2 |
| F7 | Low — clarity | §2.2 now states the operative narrowing explicitly (an object attested only in a held Class I source, in no coded corpus and with no snapshot text code, stands outside π's domain; §2.4δ reads over the operative O), and §3.3's disposition now argues the point: under §3.1's test the extent candidate fails clauses (ii) and (iii) because §2.2 derives O operatively from the records by a stated rule. The disposition itself is unchanged | §2.2, §3.3 |
| F8 | Low — clarity | §3.9's closing sentence replaced: the disposition is stated in the audit's own test language ("no candidate satisfies the test of §3.1, and so none is named") in place of "the at-most-one bound is satisfied with none named" | §3.9 |
| F9 | Note | No repair was required; under the note's license ("the freeze may say so in a clause") one clarifying clause was added: item γ closes by stating it is an indistinguishability of the record system — of its validation records — not a π-class statement, item β already placing every reading difference inside one π-class. No grounding changed | §2.4γ |

**Repair-boundary check (the pass's own condition).** The
pass record states that if T103's revision on F1 or F2
changed the equivalence definition's substance *beyond the
repairs it prescribes*, the revision would be a new draft
act and attack (ii) would stand to be re-run. The F1
repair is the prescribed one (quantify β over the
exercised inventories); the F2 repair is the prescribed
re-statement (equivalence claims confined to §2.3's rule;
the epistemic point carried as epistemic). Nothing beyond
the prescribed repairs was changed in §2 or §2.4α, so no
new draft act arises and no re-run is owed.

## Separation re-check on v1.1 (C090-7)

After revision, the document was grepped with the pass's
own search set (instantiat-, ANALOGY, NOT YET, separator,
necessary condition, verdict, outcome, succeed, conclud-,
demonstrat-, G2, D4/D5/S4/S5 outside hashes). Result: no
occurrence of instantiat-, ANALOGY, NOT YET, separator,
succeed-, conclud-, demonstrat-, G2, D4, D5, S4, or S5;
"necessary condition," "verdict," and "outcome" occur only
in the header's boundary statement (the one permitted
place) and in descriptions of the program's own machinery
and frozen records (§1.5's and §2.4α's citations of Spec
077's frozen outcome record; §3.2/§3.7's frozen verdict
bars) — the same profile the pass verified on v1. The
revision introduced no outcome vocabulary, no necessary
condition, no separator, and no S2 content.

## Gate and settling, on the final tree

The stage touches no ledger line and no gate input; the
gate was run both modes on this PR's tree with the
revision present, and the settling canonicals verified:

- full: `summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS`
- --regen: `summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS`
- `run_settling.py verify-canonicals`: **6/6 registered
  canonicals reproduce** (exit 0)

— identical to the adoption's and the draft act's gate of
record; the standing profile is unchanged.

## Claims — the stage's closing summary

Stage assessments, at the strength the evidence supports.
No claim's status, stage, or score was moved by this
stage: claim movement is a ledger act, this PR's ledger
diff is empty, and the study's per-claim dispositions of
record are the outcome record's act (T301).

- **C090-1 — discharged.** One standalone document in the
  spec's records, written before any G2 work, now frozen
  as v1.1 with its hash recorded here; later change only
  by recorded amendment act (D-090-1).
- **C090-2 — discharged on the document's evidence, as
  corrected.** Five classes, each with its provenance rule
  and its population re-counted at a7db3cfb; exception
  classes accounted (extracted null-falsifier 9;
  `no_validation_record` 3; stage-`created` 193;
  `premise_superseded` 113). F4–F6 were defects against
  this claim's falsifier shape at the level of single
  figures; all three are repaired and were re-counted or
  re-read from the records by this act (above).
- **C090-3 — discharged.** π is stated as a rule and was
  executed as one by the pass (the document's two
  illustrations and two attacker-constructed cases all
  decide as the rule states). As first written, the rule
  answered the unexercised-inventory question two opposite
  ways — the claim's falsifier in its second form; F1–F3
  repair exactly that, and the repaired rule decides every
  case put to it one way.
- **C090-4 — discharged.** Items α–ε were each opened
  against their grounding records and re-counted by the
  pass; none failed. F2 repaired α's equivalence wording
  (its counts stand untouched); F9's clause marks γ's
  instrument for what it is.
- **C090-5 — discharged.** At most one primitive absolute
  is taken: none. No second absolute was sustained under
  attack, and no demotion in the audit lacks its exhibited
  variation, derivation, or record-content account.
- **C090-6 — discharged.** The audit enumerates the
  candidates the practice uses — C090-6's three named
  candidates (corpus frame, §3.2; anchor readings' external
  identifications, §3.4; the corpus's extent, §3.3) plus
  the four the drafting surfaced (object-level
  identifications, §3.5; cross-frame identity, §3.6;
  framework constants, §3.7; transcription fidelity, §3.8)
  — each disposed of on the record. The pass hunted for
  omitted practice absolutes and found none; F7 repaired
  §3.3's argument, not its disposition.
- **C090-7 — discharged for the frozen version.** The pass
  verified the draft's separation independently; this act
  re-verified v1.1 after revision (above). Definitions
  only: record system, projection rule, cannot-distinguish
  account, absolute disposition.
- **C090-8 — not discharged; not this stage's.** It binds
  the G2 derivation (S2: T201/T202) — every derivation
  step from D1–D3 and this document's stated projection
  only. Nothing in S1 discharges it or prejudges it; it
  stands for S2 to execute against the frozen v1.1.
- **C090-12 — accounted as it stands.** §1.4 states the
  ledger's generated layers, the settling semantics, and
  the gate (V1–V10) exactly as they operate, and credits
  this study with none of it; unchanged by this stage.
- C090-9, C090-10, C090-11 (G2 form and failure
  discipline) and C090-13..16 (boundaries and closeout)
  are **not yet assessed** — their falsifiers execute
  against S2/S3, which have not started. C090-13's bound
  held through this stage: the study's only ledger change
  remains the adoption intake append.

## Observation carried, not repaired

§1.3's field list names "a reading direction" among what
each register record carries; as F6 establishes for §1.2,
the field is carried on 171 of 287 records. The pass
located F6 at §1.2's sentence and sustained nothing
against §1.3's list, which describes the record's fields;
this act repaired the findings as located and records the
adjacency here rather than editing beyond the pass's
record. It affects no disposition; a future amendment act
may take it up.

## T103's "does not establish" line (from tasks.md)

*This does not establish:* that a frozen G1 document is
the final G1 answer — amendments remain possible as
recorded acts, and the reader's verdict is not this
study's to give.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI. The drafter of the G1 document and
the worker of the adversarial pass were different workers,
per the plan's separation rule; this act is the reviser's.
