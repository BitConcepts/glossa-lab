# Stage S2 record — Spec 090 (2026-11-04)

**Scope:** tasks.md T201 — candidate G2 derivations against
the frozen G1 document. Executed on branch
`feat/090-s2-g2-derivation` from origin/main
`8d8e470a3d14eaee59794d2bc6b2e1dcf88f7cc8` (the Spec 090
S1 merge, PR #514). This PR carries the derivation record
(`records/g2-derivation.md`), this record, and the tasks.md
updates (T201 ticked with its completion note; T202
annotated, still open). It does **not** carry the derivation
audit (T202): the plan's separation rule puts the audit in
a worker other than the deriver's hands, and the G2
outcome (DERIVED / NOT YET) is declared on the audit. The
ledger is untouched by this PR.

## The basis, verified before deriving

`records/g1-document.md` at this branch: 34,226 bytes,
SHA-256
**4f2018f40c9ccaf0811cd7661b0c9e1ebd840c7e014d954f778c42edef27efc2**
— recomputed from the committed file and matched against
`records/stage-s1-freeze-record.md`. The derivation runs
against frozen G1 v1.1 and no other basis (C090-8): the
skeleton's D1–D5 (of record in the spec's records), the
G1 document, and record facts counted at this stage from
the artifacts the G1 document names. The absolute
disposition the chains inherit is the audit's NONE-NEEDED
(§3.9); Candidate 2's per-corpus form is one place that
disposition does work inside a derivation.

## What was read

Governing documents: spec.md, claims.md (C090-8..11
govern this stage; C090-13..15 bound it), plan.md (Stage 2
section, including its named hunting grounds), tasks.md
(T201, T202); the frozen G1 document in full (§1 the record
system; §2 the projection as repaired — equivalence over
exercised inventories, §2.4α–ε; §3 the absolute audit with
its §3.1 test and §3.9 close); the S1 records
(`stage-s1-record.md`, `stage-s1-adversarial-record.md`,
`stage-s1-freeze-record.md` — the last for the repair
boundary on §2, which the chains rely on and do not exceed);
the skeleton document (D4 the target definition; D5 and
S3–S4 for the counted form); the scoping note (occasion
only, per D-090-3).

Record material, read or counted first-hand at 8d8e470a:
the three Class II derivations of record (the M77 loader
`backend/glossa_lab/data/indus_m77.py`; the CISI loader
`backend/glossa_lab/data/indus_cisi.py`; the ICIT OCR
script `backend/scripts/ocr_icit_corpus.py`, which writes
`reports/icit_corpus_flat.txt`); the two coded-corpus flat
files and the CISI corpus JSON, re-counted (below).

## The counted-form checks executed at this stage

Two records-side checks belong to the derivation itself
(the derivations' inputs), and both were run at this
stage. Neither is a G3 administration: no separator was
computed and no held-out record was used (C090-15).

**(a) Candidate 1's count — Class II derivations taking a
reading assignment as input: 0 of 3.** Method: read each
member's derivation of record and enumerate its inputs.
M77: OCR + a sign-rank-correlation glyph mapping from
Mahadevan (1977) — inputs: the concordance's glyph data,
the frame. CISI subset: digitization of the CISI volumes
(mayig corpus) in Parpola P-codes — inputs: the published
texts, the frame. ICIT: OCR extraction from Fuls (2023) —
inputs: the published books' glyph data, the frame. No
derivation takes (ρ, λ) as an input; no member's table is
other than a function of glyph streams under a frame.

**(b) Candidate 2's recorded profiles, recomputed** from
the files at this tree state (a line/token count over the
pinned files; the G1 §1.2 figures reproduce exactly, and
both file hashes match §1.2's pins):

- M77 (`reports/mahadevan_corpus_flat.txt`, SHA-256
  878fd223…): 1,669 inscriptions; 5,361 tokens; 64 distinct
  codes; sorted multiplicity vector (descending): 541,
  432, 355, 219, 211, 196, 179, 171, 147, 138, 124, 121,
  107, 105, 102, 92, 85, 80, 76, 73, 73, 68, 64, 63, 61,
  61, 60, 59, 56, 55, 52, 50, 48, 48, 48, 48, 47, 46, 46,
  45, 43, 43, 41, 41, 41, 40, 40, 40, 39, 39, 38, 36, 35,
  35, 34, 32, 32, 19, 16, 14, 5, 3, 2, 1 — maximum 541,
  exactly one code occurring once, three occurring three
  times or fewer; length histogram headed by 564
  single-token inscriptions, 25 lines longer than 14
  tokens (as §1.2 counts them).
- ICIT (`reports/icit_corpus_flat.txt`, SHA-256
  c8839fd3…): 4,410 inscriptions; 14,213 tokens; 713
  distinct codes; maximum multiplicity 527; 218 codes
  occurring once; 386 occurring three times or fewer; 946
  single-token inscriptions.
- CISI coded subset (`backend/glossa_lab/data/
  indus_cisi_corpus.json`, via the loader of record): 179
  inscription sides, 178 of them multi-sign; 1,003 tokens;
  182 distinct Parpola P-codes — agreeing with the loader
  header's own stated figures.

## The candidates (derivation record §2–§5)

| Candidate | Outcome on the deriver's side |
|---|---|
| 1 — Non-certification: every state is projection-equivalent to states differing in (ρ, λ), in unexercised inventory, and off O; no record singles a state out within its class | Chain complete, 7 steps, every step traced to D2 / §2.2 / §2.3 / §2.4β / §2.4δ; counted form executed (check (a): 0 of 3); falsifier stated (a Class II record whose derivation takes a reading assignment as input); bite stated (no decipherment is record-determined; corpus statistics bound to classification-level conclusions) |
| 2 — Recorded-profile: every consistent state induces each coded corpus's recorded identity structure (exercised count, multiplicity profile, length profile, up to relabeling) | Chain complete, 5 steps (the preservation step is arithmetic on §2.3's β, shown in the record); recorded side re-counted (check (b)); falsifier stated (a faithful re-derivation of a corpus from its Class I sources, non-equivalent to the pinned file); bite stated with its caveat in the open — the excluding power is consistency's, made countable; C090-9 pressure point labeled for the audit |
| 3 — Register-certification over the 44 pending / 3 unrecorded / 113 superseded readings | **NOT DERIVED.** Chain breaks at its step 2: the bridge premise (certification = a completed validation record) is supplied by neither D1–D3 nor the G1 document, which places validation in the assertion layer and marks §2.4γ's item a validation-record statement, not a π-class statement. The statement's truth-maker is the register's bookkeeping at a date, not the states quantified over. Its derivable core is Candidate 1's (ρ, λ) clause. What would have to change: a G1 amendment making validation outcomes part of the projection — contradicting §2.2's frozen separation, not this stage's to make |
| 4 — Standalone corpus regularities as necessary conditions | **NOT DERIVED as stated.** Their only derivation is enumeration of the observed corpus — C090-9's excluded shape. Each is a component of Candidate 2's recorded profile and inherits its derivation there as a corollary, not a derivation of its own |

The derivation record's §6 carries the provenance
self-audit: every premise of both completed chains traced
to the frozen G1 document, to D1–D3, or to a record fact
counted at this stage; the physics-premise check (none;
the candidates' occasions are the plan's own hunting
grounds, named as occasion); and four labeled boundaries
for the audit to press (Candidate 1's reliance on §2.2's
assertion disposition; its counted form's exclusion of the
assertion classes by rule rather than by count; its
falsifier's through-the-basis character; Candidate 2's
consistency assembly and bite caveat).

## Gate on the final tree

The stage touches no ledger line and no gate input; the
gate was run both modes on this PR's tree and the settling
canonicals verified, verbatim summaries:

- full: `summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS`
- --regen: `summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS`
- `run_settling.py verify-canonicals`: **6/6 registered
  canonicals reproduce**

— identical to the adoption's and S1's gate of record;
the standing profile is unchanged.

## Claims assessed at this stage (deriver's side)

No claim's status, stage, or score was moved by this
stage; per-claim dispositions of record are the outcome
record's act (T301). These assessments state what this
stage's evidence supports, at that strength, for T202's
audit and T301 to settle.

- **C090-8 — holds on the derivation record's evidence.**
  Every step of both completed chains cites D1–D3 or the
  frozen G1 document; the self-audit traces every premise;
  no physics result appears as a premise (the F0 pattern
  is named once, as occasion, in the self-audit — the
  chains stand with it removed, as the audit is written to
  verify).
- **C090-9 — holds for Candidates 1 and 2; executed as a
  refusal for Candidate 4.** Both derived statements
  quantify over states in projection-equivalence classes
  (Candidate 1 over every state; Candidate 2 over the
  classes consistent with the records), and Candidate 2's
  record states its own pressure point under this claim
  plainly. Candidate 4 was refused on exactly this claim's
  ground.
- **C090-10 — holds on the record's evidence.** Each
  derived candidate carries its falsifier as a named
  record kind with named properties, of a kind the record
  system admits (a Class II record in both cases), whose
  observation would refute the derivation's application.
  Candidate 1's falsifier-character is labeled in the
  record's §6 for the audit.
- **C090-11 — executed for Candidates 3 and 4.** Each is
  recorded NOT DERIVED with its obstruction named at the
  step where the chain breaks and what would have to
  change; no weaker statement is substituted for either,
  and neither is carried as essentially derived.
- **C090-13 — held.** This PR's diff is the derivation
  record, this record, and the tasks.md updates; the
  ledger is untouched.
- C090-12, C090-14, C090-15, C090-16 are S3's to close;
  nothing in this stage engages them beyond holding their
  bounds (no machinery built; no convergence implication;
  G3–G5 unattempted — the stage's two checks are the
  derivations' own input verifications, not separator
  administrations).

## Departures, stated plainly

1. **T202 is not in this PR.** The plan's Stage 2 contents
   name one PR for the stage (the derivation record), and
   its verification paragraph makes the audit record the
   stage's verification; the audit is a separate worker's
   act by the plan's separation rule (as S1 split T101's
   draft from T102's attack). This PR therefore lands
   T201 complete and T202 open, with the derivation
   record's self-audit written as the audit's input. The
   G2 outcome is not declared here.
2. **The counted forms were brought to the records only
   on their recorded side.** Candidate 1's count ran over
   the derivations of record (an input inspection);
   Candidate 2's count recomputed the recorded profiles.
   Running either count against arbitrary named candidate
   states — bringing proposed decipherments to the test —
   is administration, and its held-out form is G3's bar;
   this stage states both counting rules in full and runs
   neither administration (C090-15).
3. **No G1 amendment was needed or made.** Both completed
   chains derive against v1.1 exactly as frozen; nothing
   in the derivation's fortunes was carried back into the
   definitions (the plan's design rule). Candidate 3's
   obstruction names a G1 amendment as what *would* have
   to change — recorded as a finding for the outcome
   record, not executed.

## T201's "does not establish" line (from tasks.md)

*This does not establish:* that any chain is sound —
soundness is T202's audit, and a complete-looking chain is
exactly what an audit exists to test.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
