# Spec 096 — Eteocypriot Program

**Status: ADOPTED 2026-11-20** (owner's direction, this chat,
2026-11-20: Eteocypriot is to be set up as its own separate
program in Glossa-Lab, not as a deliverable inside Spec 095's
package; the same direction carries the execution commission
for the pilot's stages, the gate on which the owner lifted in
chat on 2026-11-20: "in parallel start the other ancient
language decoding work"). Stage 0 (program setup) is complete
at adoption. The pilot's execution stages run under this spec's
own records, in stage order.

**Provenance.** The program is founded on Spec 095's Stage 5
second-target scoping, which stays in place, unedited, as the
founding record and is cited here as provenance:
`specs/095-red-team-remediation/second-targets/eteocypriot-proposal-2026-11-17.md`
(SHA-256
`6034663dba1c7a0bfc88d5475031f7b894240a2e4f0e25eb748733c9f1af12d6`),
`specs/095-red-team-remediation/second-targets/eteocypriot-preregistration-draft-2026-11-17.md`
(SHA-256
`ab680522bffcf7a87bfebe784aaae54b5226f0df1deb8330120a0b962277f30f`),
and `specs/095-red-team-remediation/records/stage-5-scoping-record-2026-11-17.md`
§2 (SHA-256
`3b1fa6c5587c74b245b40f3a6dcf4682f89d9a78629582739254b8d87624fadf`).
The preregistration draft's claims EC-D1..EC-D4 are re-expressed
as this program's own claims C096-1..C096-4 at intake (D-096-2);
the draft itself is not edited and no Spec 095 claim, task, or
record is modified by this spec.

## 1. What this spec is

A decipherment program over a second target: Eteocypriot, a
known syllabary (the Cypriot syllabary, sign values settled
since the 19th century) writing an unknown language, with
bilingual evidence. The program applies the Glossa-Lab
machinery — corpus identity and fail-closed loading (C095-3),
claim form with pre-fixed falsifiers, held-out prediction,
rival-construction identifiability (Standards of Record
Part III), and named-human adjudication — to that target, and
accepts its registered outcome classes in full: SUPPORTED at a
stated strength, NOT SUPPORTED, NOT IDENTIFIABLE, TOO THIN,
and step-0 CLOSED. A TOO THIN outcome is a legitimate terminal
outcome of this program, landed as such, never worked around.

The research question is the preregistration draft's §1,
adopted verbatim as this program's question: can the machinery
produce, for Eteocypriot, at least one grammatical or lexical
result that survives its own falsifier on held-out
inscriptions; and where it cannot, does it correctly return
NOT IDENTIFIABLE or TOO THIN instead of a confident answer? No
outcome of this program is a translation claim.

## 2. Scope

- **Corpus:** the primary-stratum Eteocypriot corpus under the
  delimitation of record (Perna 2015, as scoped in the
  proposal §3.4): the Amathus material, with ICS 196 and the
  Androkles dedications as the development set together with
  the Greek syllabic control corpus, and every remaining
  primary-stratum inscription (ICS 194/195 under Perna 2019's
  re-edition) as the sealed held-out set. Golgoi is a separate
  stratum, never merged (sensitivity S2 only).
- **Editions of record:** Masson's ICS; Perna 2019 for
  ICS 194/195; IG XV 1,1; Perna 2015 for the delimitation. The
  ancient texts are uncopyrighted; the critical editions are
  copyrighted scholarship — the program transcribes the ancient
  text with citation and never redistributes edition material
  (no scans, no apparatus dumps). A text that cannot be
  obtained from lawfully available sources is recorded as not
  obtained, per inscription, and the study proceeds with what
  is held.
- **Experiments:** E1 (known-answer validation on the
  development set, under the rival alignment assumptions A1
  strict segment-parallel and A2 name-anchored free), E2
  (held-out prediction, candidates developed only on the
  development set and registered before the seal breaks), E3
  (identifiability, before any SUPPORTED scoring), exactly as
  the preregistration draft registers them, with the numeric
  floors instantiated against the frozen census at the freeze.
- **Adjudication:** the route of the proposal §6 — ledger
  intake in claim form through the sanctioned importer,
  hash-pinned evidence in Spec 094's registered classes,
  standing changes only by recorded adjudication with a named
  human approver. Automated actors never approve, verify, or
  promote.

## 3. Hard limits

- No external contact of any kind: no expert outreach, no
  external registration or filing (the preregistration draft's
  §10 OSF filing is not performed; the preregistration is
  repo-filed at this program's freeze), no purchases.
- No claim status changes outside this program's own claims,
  and those only as §2's adjudication route provides. The
  Indus program's claims and standings are untouched.
- The held-out set stays sealed until the preregistration's
  own procedure opens it; a floor that cannot be instantiated
  closes the affected experiment as TOO THIN at freeze rather
  than silently weakening the test.

## 4. Decisions

- **D-096-1 — separate program.** Eteocypriot is Spec 096, its
  own program, per the owner's direction of 2026-11-20. Spec
  095's scoping documents are provenance, not a home.
- **D-096-2 — claims.** C096-1..C096-4 (claims.md) re-express
  the preregistration draft's EC-D1..EC-D4 in this program's
  claim form, with the same falsifiers and does-not-establish
  bounds. They are intaken at adoption through
  `tools/ledger/import_bundle.py`, the only sanctioned path,
  inside the adoption PR. Intake sets no standing.
- **D-096-3 — execution commissioned.** The pilot's stages
  (corpus assembly and freeze; registered analysis; outcome
  record) are commissioned by the owner's 2026-11-20 direction
  and run under this spec's records in stage order, each landed
  as its own PR on genuine per-job CI green.
- **D-096-4 — program-map placement.** The program is entered
  in `glossa-indus/map/program-map-taxonomy.json` under Program
  infrastructure / Governance, lifecycle & generated layers —
  the subdomain of the study-program specs (086–092, 094, 095).
  The taxonomy's claim-family domains classify the Indus
  program's families; this program's claims are a separate
  target's and are not placed under an Indus family. A future
  taxonomy amendment may give the second-target programs their
  own domain; none is created unilaterally here.
- **D-096-5 — adjudication package.** Preparing the expert
  adjudication package (proposal §6 item 4) is program work;
  contacting any specialist is an external act requiring the
  owner's approval at the time, and is not authorized by this
  spec.

## 5. Stages

- **Stage 0 — program setup (complete at adoption).** This
  package, the program-map assignment, the claims intake, the
  generated-layer refresh, and the adoption record.
- **Stage 1 — corpus assembly and freeze.** The pilot's step 0:
  corpus-availability survey, intake under a C095-3 identity
  record (per-inscription SHA-256 pins, the development /
  held-out split by inscription, the Common signary frame with
  Paphian as a variant frame), the rival alignment assumptions
  and the frozen E1 procedure, and the registered thinness
  floors instantiated against the frozen census. The freeze is
  committed before any analysis runs.
- **Stage 2 — registered analysis.** E1 on the administrable
  legs; E2 and E3 exactly as the freeze's floors and the
  preregistration's preconditions provide. Every verdict is
  recorded from the run records themselves.
- **Stage 3 — outcome and adjudication package.** The outcome
  record (per-claim verdicts with their precision basis) and,
  if the outcome carries anything to adjudicate, the expert
  adjudication package prepared for the owner's approval act.

## 6. What adoption does and does not do

Adoption lands this package, enters C096-1..C096-4 into the
claims ledger through the importer inside this same PR
(D-096-2), assigns the program in the program map (D-096-4),
and records Stage 0 as complete. It moves no claim's status,
stage, or score, modifies no Spec 095 record, and sends
nothing anywhere. The execution stages run under D-096-3, each
on its own landing.
