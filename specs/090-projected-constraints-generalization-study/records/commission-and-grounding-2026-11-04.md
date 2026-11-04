# Commission and grounding record — Spec 090 (2026-11-04)

## The commission

On 2026-11-04 the owner ordered "do both in order." Item 1 of that
order commissions the generalization study: Glossa-Lab, as the test
bed, attempts G1 and G2 of the Projected Constraints generalization
bar as a registered study in its own program, under its own spec-kit
+ AEE flow and ledger. The commission was delivered to this chat by
the VEXA chat (the chat that maintains the stack's umbrella repo),
which supplies the skeleton and the judging criteria and receives
the outcome for the improvement registry. G3, G4, and G5 are
commissioned in principle by the same order and sequenced after
G1/G2 land, so the study can stop honestly at NOT YET if G1 or G2
fails. The commission states, and this package repeats as a boundary:
nothing about Glossa's stack, specs in flight, or convergence state
changes; the program remains at convergence Stage 0, and this study
is not a convergence step.

## Sources of record (byte-identical copies in this package's records/)

- `GENERALIZATION-SKELETON-2026-11-04.md` — the skeleton document:
  definitions D1 (record system), D2 (projection), D3 (primitive
  absolute: at most one, named, or a proof that none is needed), D4
  (necessary condition: derived from D1–D3 and the stated projection,
  carrying its falsifier — a record the framework declares
  impossible, observed), D5 (separator), D6 (executable matrix); the
  skeleton S1–S5; the judging protocol (an independent reader
  receives only the skeleton, the domain's G1 document, and the
  domain's records — never the domain team's conclusions); the
  verdicts INSTANTIATES / ANALOGY / NOT YET, the last two publishable
  and recorded either way; and Appendix B, the G1 checklist.
  Source: AXIOVEX/vexa, commit 88839493. SHA-256
  a66ffe4fcb6826465e34e97c81a13aff85228939204c9629889d45f7ce8d9876.
- `GENERALIZATION-SCOPING-NOTE-2026-11-04.md` — the scoping note:
  the G1–G5 bar (all five required, else the verdict is analogy) and
  the honest boundaries, including the assessment that Glossa "has
  NOT done is state a projection rule, a primitive absolute, or a
  necessary condition in the skeleton's terms (its Spec 076/078
  projected-constraint corpus work is adjacent, on its own terms)."
  Source: AXIOVEX/vexa, commit 88839493. SHA-256
  281f35430bea3cbfbee1b9d932caf74f22f38e6c2ba8922e22d795bb1637c173.

Both hashes were verified against the delivered copies at drafting
time (2026-11-04); the copies in `records/` hash to the same values.

## What G1 and G2 demand (Appendix B items 1–4; the scoping note's G1/G2)

- **G1 (checklist items 1–3).** A single G1 document, written before
  results, stating: (1) the record system's definition, with
  provenance rules; (2) the projection rule, including the
  cannot-distinguish account (what the records provably cannot
  identify); (3) the named primitive absolute, or the none-needed
  proof. The document must be readable by the independent reader of
  the judging protocol: definitions only, no conclusions.
- **G2 (checklist item 4).** At least one necessary condition derived
  in the decipherment domain by the skeleton's machinery —
  proceeding from D1–D3 and the domain's stated projection rule, not
  imported from physics — stated with its falsifier in D4's form.

Checklist items 5–7 (a computed separator validated on held-out
records; a gate refusal instance; reproduction materials for the G5
reader) belong to G3/G4/G5 and are outside this study's scope.

## Grounding census (counted/read first-hand, 2026-11-04)

**Tree state read.** All repo facts below were read at **origin/main
= c643500b** (Merge PR #511, the Spec 088 closeout) via `git show`
from the program's audit clone, whose working tree was busy on the
Spec 089 adoption branch and was not touched. Where the Spec 089
adoption branch state differs, it is named separately.

### The claims ledger (`glossa-indus/ledger/claims.jsonl`)

- At origin/main: **907 lines**, SHA-256
  9f8144c3fa73d7cfa4ffd02d3b6c23c3ea9e0c1e164e9497232dd2842e0a022c;
  **876 claim entries** (853 bundle + 23 extracted, by the entries'
  own `population` field) and 31 annotation entries. A falsifier is
  present on **867 of 876** claim entries (the 9 nulls are in the
  extracted population, counted in Spec 088's census, never filled).
  Governing statuses: draft 852, untested 12, partially_supported 3,
  strongly_supported 2, contradicted 4, partially_falsified 1,
  unsupported 1, superseded 1.
- On the Spec 089 adoption branch (`feat/089-spec-package` at
  be866b0, PR #512, unmerged at the time of reading): 927 lines,
  SHA-256 b442ce7e5825e938fbd4bc0033bcb0582b37c71fe724a55f4584b5a4d5213712
  — the same ledger plus the C089 intake append. This study's own
  intake (plan.md Stage 0) appends after that, by the same path.

### The anchor register (`backend/reports/INDUS_FINAL_ANCHORS.json`)

- **287 records**, keyed by Mahadevan sign number; the settling
  canonicals pin the file at raw SHA-256 df0cf620… (570,344 bytes;
  `glossa-indus/ledger/settling-canonical.json`). Each record carries
  a reading, a confidence, a basis text, a stage with a stage history
  (actor, timestamp, evidence_refs — the provenance chain), a
  validation_status, and a strict_set flag.
- The **strict set is 94** (records with `strict_set` true; the same
  94 carry validation_status `strict_sa_independent` and stage
  `checked`). **44 records carry validation_status
  `pending_non_sa_validation`** — the 44 pending readings: proposed
  readings whose validation chain is not complete, named as such in
  the register itself (and carried in `glossa-indus/LEDGER.md` as
  "the 44 pending anchors"). Remaining validation statuses:
  sa_in_provenance_chain 33, no_validation_record 3,
  premise_superseded 113. Confidence tiers: HIGH 166, MEDIUM 5,
  LOW 3, CANDIDATE 113.

### The corpus records

- The M77 canonical flat file (`reports/mahadevan_corpus_flat.txt`):
  SHA-256
  878fd2231929f2105cb5c7fb37507ee7eceb7d83f355f1fa4d8e793926785c18,
  21,443 bytes. Counted from the file at origin/main: **1,669
  inscriptions, 5,361 sign tokens, 64 distinct signs**. Loader of
  record: `backend/glossa_lab/data/indus_m77.py` (Mahadevan 1977
  concordance; one inscription per line, 3-digit M77 codes).
- The ICIT-frame flat file (`reports/icit_corpus_flat.txt`), counted
  the same way: 4,410 inscriptions, 14,213 tokens, **713 distinct
  sign codes** — a different segmentation of the same script yields
  a different record set, which is itself grounding for G1's
  projection question.

### The signary's frame-dependence (underdetermination, on the record)

- Spec 077 (signary triangulation, FROZEN 2026-10-26) froze a
  population of **557 signs** (the Wells/ICIT-keyed population of
  Registry v2) and executed: **399 of 557 witnessed (71.63%)**
  against a frozen bar of 502 (90%) — the bar failed, on the record
  (`specs/077-signary-triangulation/outcome.md`).
- Against that 557-sign population: only **64 distinct signs are
  attested** in the M77 corpus file, and the ICIT frame counts 713
  distinct codes. How many signs the script has, and which signs a
  given inscription contains, are not fixed by the records
  independently of the frame a reader brings to them. This is the
  program's own measured underdetermination, and it is the raw
  material G1's cannot-distinguish account must be built from —
  cited as records, not as rhetoric.

### The executable matrix (D6 — the element plainly exhibited)

- The chain stands as Specs 086–089 built and verified it: the
  append-only ledger (above) → the **generated matrix**
  (`glossa-indus/matrix/matrix.json` at origin/main: 876 rows × 644
  columns, 1,399 cells, generated from the ledger by script) → the
  generated maps (Spec 086's claim map; Spec 088's program map —
  coverage at origin/main: 876 claims, open 867 / negative 6 /
  positive 2 / closed_other 1 — and its ratified gap register).
- The **verification gate** (`backend/glossa_lab/ledger_gate.py`,
  classes **V1–V10**) recomputes every downstream layer by an
  independent route under its own registered copies of the
  definitions; its header states the discipline: "**The gate never
  writes**." Publication (`gated_publish.py`) replaces published
  artifacts only on ALL PASS.
- **Settling**: claim statuses settle mechanically under the
  registered semantics glossa-settle-1
  (`glossa-indus/ledger/SETTLING-SEMANTICS.md`), with the canonical
  scenarios registered in `settling-canonical.json` (6/6 reproducing
  at the last recorded refresh, the Spec 088 adoption's) and the
  ledger/anchors/corpus pins carried in that file.
- Spec 089 (run-scoped results; package ratified 2026-11-04,
  adoption in flight at drafting time) adds run identity and the
  junction rule over this substrate. It changes nothing in this
  census except the ledger's line count, as recorded above.

### Specs 076/078 — the adjacent work, on its own terms

- **Spec 076** (the projected-constraint corpus model, method M12:
  "Demanding What Must Be True of the Missing Signs"), FROZEN
  2026-10-26. Its pilot closed the same day: **ASSUMPTION SET DOES
  NOT HOLD** (`specs/076-projected-constraint-corpus-model/pilot-record.md`).
- **Spec 078** (the bridge redesign, method M13, successor to 076),
  FROZEN 2026-10-26. Its pilot closed: **CANNOT BE ADMINISTERED —
  THE CORE MAKES TOO FEW CHECKABLE CLAIMS**
  (`specs/078-projected-constraint-bridge-redesign/pilot-record.md`).
- Both are the program's own projected-constraint work, designed and
  judged in the program's own terms. Neither states a D2 projection
  rule, a D3 absolute, or a D4 necessary condition in the skeleton's
  terms, and neither is an instantiation attempt. Their negative
  closures are part of this study's honest starting position: the
  domain has already failed twice at adjacent formulations, which is
  evidence about difficulty, not about the skeleton.

## The honest starting position

As of this package, in the skeleton's terms:

- **S5 / D6 (executable matrix): EXHIBITED** — the machinery above
  stands and is verified; the study claims no part of building it.
- **S1 / D1 (record system): PRESENT BUT UNSTATED** — the records
  exist with provenance (ledger entries carry sources; anchor
  records carry stage histories with evidence_refs; corpus files are
  hash-pinned), but no document defines the record system as a
  system in the skeleton's terms.
- **S2 / D2 (projection rule): UNSTATED.** No document states a rule
  mapping a candidate decipherment state to the records it would
  produce, and no cannot-distinguish account exists in those terms.
  The underdetermination facts exist in the records (above); the
  projection statement does not.
- **S3 / D3 (primitive absolute): UNSTATED.** The program has never
  named an absolute, nor proved none is needed. Candidate absolutes
  exist in practice (the frame a corpus is read under; the anchor
  readings' external identifications) and have never been audited as
  absolutes.
- **S4 / D4 (necessary condition): UNSTATED.** No necessary condition
  for the decipherment domain has been derived from a stated
  projection. Specs 076/078 demanded necessary-style truths of
  completions under assumption sets, on their own terms, and closed
  negatively; that is not a D4 derivation and this study does not
  present it as one.

G1 and G2 are therefore genuinely open, exactly as the scoping note
assessed. This package frames the attempt; it does not draft the G1
document or the G2 derivation, and it prejudges neither the absolute
question nor the derivation's success.
