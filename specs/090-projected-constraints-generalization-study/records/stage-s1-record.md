# Stage S1 record (draft act) — Spec 090 (2026-11-04)

**Scope:** tasks.md T101 — the G1 draft. Executed on branch
`feat/090-s1-g1-document` from origin/main
`a7db3cfb60bf84eeb87bd9f690050543c2ebb01c` (the Spec 090
adoption merge, PR #513). This PR carries the draft of the
G1 document and this record. It does **not** carry the
adversarial pass (T102) or the revision-and-freeze act
(T103): the plan's own separation rule puts the attack in a
separate worker's hands, and the freeze follows the attack.
Both tasks remain open in tasks.md and are the stage's
follow-on acts; the G1 outcome (STATED / NOT YET) is a T103
act, not this record's. T101 is ticked on the draft's
evidence below.

## The document

`records/g1-document.md`, **version v1**, 31,376 bytes,
**SHA-256
974d5043ab463d0e6a33912b6e1136bcac288cd679827edade3c81d7af858d5b**
(as committed in this PR; the hash is recorded here per
D-090-1 — the document carries the pointer, this record
carries the hash). Structure, exactly Appendix B items 1–3:
§1 the record system (five classes: inscription records,
coded corpus records, anchor records, ledger claim lines,
snapshots and frozen records — each with its provenance
rule, its counted population, and its exception classes
accounted); §2 the projection rule (candidate state
(Σ, γ, ρ, λ); π as the sequence table over the object set;
projection-equivalence up to label bijection, with the
decidability rule and a two-case illustration; the
cannot-distinguish account α–ε); §3 the primitive-absolute
audit and its disposition. No other content: no separator,
no necessary condition, no outcome language (see the
separation check under Verification).

## What was read

Governing documents, in the spec's records and directory:
spec.md, claims.md (C090-1..16; C090-1..8 govern this
stage), plan.md (Stage 1 section), tasks.md (T101);
`records/GENERALIZATION-SKELETON-2026-11-04.md` (D1–D6,
Appendix B items 1–3 as the checklist);
`records/GENERALIZATION-SCOPING-NOTE-2026-11-04.md`;
`records/commission-and-grounding-2026-11-04.md`;
`records/ratification-2026-11-04.md`.

Record material, read or counted first-hand at a7db3cfb:
the claims ledger (`glossa-indus/ledger/claims.jsonl`); the
anchor register (`backend/reports/INDUS_FINAL_ANCHORS.json`,
including individual records of each validation status —
M342 strict, M071 pending, M001 in-chain, M252
no-validation-record, M255 premise-superseded); the two
coded corpora (`reports/mahadevan_corpus_flat.txt`,
`reports/icit_corpus_flat.txt`) and the M77 loader of record
(`backend/glossa_lab/data/indus_m77.py`); the corpus
snapshot (`glossa-corpus/indus/exports/indus_research.jsonl`);
the settling canonicals
(`glossa-indus/ledger/settling-canonical.json`, including
its pin block and strict-rule text); the generated matrix
(`glossa-indus/matrix/matrix.json`) and program-map coverage
(`glossa-indus/map/program-map.json`); the gate's header
(`backend/glossa_lab/ledger_gate.py`: "The gate never
writes"); the anchor-support audit
(`docs/repair-2026-10-26/anchor-support-audit.json`); Spec
077's frozen outcome (`specs/077-signary-triangulation/outcome.md`);
the Fuls–Mahadevan crosswalk
(`reports/fuls_mahadevan_crosswalk.txt`); Specs 076/078's
pilot records (heads; cited only through the grounding
record's account of them as frozen adjacent work).

## Census re-counted at a7db3cfb (the document's figures)

- Ledger: 943 lines, canonical SHA-256 15a5fbad…; 912
  claims (bundle 889, extracted 23), 31 annotations;
  falsifier 903/912 (the 9 nulls all extracted); statuses
  draft 888, untested 12, partially_supported 3,
  strongly_supported 2, contradicted 4,
  partially_falsified 1, unsupported 1, superseded 1.
  (The grounding record's census at c643500b read 907
  lines / 876 claims; the difference is the Spec 089 and
  Spec 090 intake appends, exactly as the adoption records
  state. This stage re-counted, per the plan's design rule.)
- Anchor register: 287 records (286 Mahadevan keys M001–
  M416, one H003), SHA-256 df0cf620…, 570,344 bytes;
  validation statuses 94 / 33 / 44 / 3 / 113 as the document
  states; confidence tiers HIGH 166, MEDIUM 5, LOW 3,
  CANDIDATE 113; stages checked 94, created 193; strict by
  confidence HIGH 90 + MEDIUM 4 (canonical pin block).
- M77 coded corpus: 1,669 inscriptions, 5,361 tokens, 64
  distinct codes (numeric range 3–920), mean length 3.21,
  564 single-token inscriptions, one code occurring once,
  three codes occurring ≤3 times, most frequent code 541
  tokens, 25 lines longer than 14 tokens. SHA-256
  878fd223… (the pinned canonical bytes).
- ICIT coded corpus: 4,410 inscriptions, 14,213 tokens,
  713 distinct codes; SHA-256 c8839fd3….
- Corpus snapshot: 15,508 rows; source systems PennMuseum
  7,515, MetOpenAccess 4,904, indusscript-m77 2,906,
  mayig-cisi 179, ClevelandArtOpenAccess 4; schemes
  Mahadevan1977 2,906, Parpola1982 179, none stated 12,423;
  535 distinct diplomatic codes; crosswalk coverage >0 on
  3,021 rows, 0 on 12,487.
- Matrix: 912 rows × 644 columns, 1,435 cells (the
  document's §1.4 figure; the program-map coverage block
  agrees: 912 claims, open 903 / negative 6 / positive 2 /
  closed_other 1).
- Settling: `tools/ledger/run_settling.py verify-canonicals`
  run on this tree: **6/6 registered canonicals reproduce**.

## The absolute audit — disposition summary (the document's §3)

The audit's test (§3.1): a quantity is a primitive absolute
exactly when the system's reasoning about candidate states
uses it as given, it is not a record or record content with
provenance in R, and it is not derived from R by a stated
rule. Candidates enumerated from the program's practice —
claim C090-6's three named candidates plus four the reading
surfaced — and disposed of as follows:

| Candidate | Disposition | Where |
|---|---|---|
| Corpus frame (inventory a corpus answers to) | Record-relative — variation exhibited across five frames inside the system | §3.2 |
| Surviving corpus's extent (corpus boundary, object inclusion) | The record system's own ostensive definition; all projection statements relativized to O; consequences carried at §2.4δ | §3.3 |
| Anchor readings' external identifications | Assertion content with provenance — distributional parts derived from R; imported parts stand at claim standing, under test (strict rule; WP5 census 6/46/37/2/3; the 44 pending unused as settled) | §3.4 |
| Object-level imported identifications (site, material, typology, chronology) | Record content with provenance (Class I/V fields; period assignments as Class IV claim content or frozen study parameters); π does not use them | §3.5 |
| Cross-frame sign identity | Records — the crosswalks themselves, partial on their face (158/557 without counterpart) | §3.6 |
| Framework registered constants (frozen bars, glossa-settle-1, matrix-defs v1, thresholds) | The framework's own stated definitions, themselves records; not quantities of the domain | §3.7 |
| Transcription fidelity of coded corpora | A provenance property of Class II (derivation named per file), not a quantity; fidelity failures are record errors | §3.8 |

**Draft disposition: no candidate satisfies the test; the
document states D3's none-needed branch** (§3.9), assembled
from the dispositions above. This is the draft's
disposition, reached by the audit D-090-2 mandates. It is
not a closed outcome: T102's attack on the audit (in
particular its named question (i): a second absolute
functioning as given while disposed of as relative or
derived, or a practice absolute the audit omits) and T103's
freeze are the acts that close it, and a sustained split
goes to the owner as oracle under D-090-2.

## Verification

- The document was read back in full after writing; every
  count in it traces to the census above or to the frozen
  record named beside the figure (Spec 077's witnessed
  count and bar; the WP5 support census).
- Protocol separation (C090-7): the document was grepped
  for outcome vocabulary (instantiat-, verdict, succeed,
  conclude/conclusion, proven/proves, demonstrat-). The
  word "verdict" occurs only in the header's boundary
  statement ("no verdict on any skeleton element") and in
  descriptions of the program's own machinery (frozen
  verdict bars; frames entering verdicts) — never as a
  claim of this study. No necessary-condition or separator
  content appears.
- Gate on the final tree (this PR's changes present),
  verbatim summaries:
  full: `summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS`
  --regen: `summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS`
  — identical to the adoption's gate of record; the stage
  touches no gate input.
- The ledger is untouched by this PR (its diff is the two
  records files and the tasks.md tick).

## Departures and drafting notes, stated plainly

1. **PR shape.** plan.md's Stage 1 names one PR carrying
   the draft + the adversarial-pass record + the drafting
   record. This PR carries the draft + this drafting record
   only, because the pass must be executed by a worker other
   than the drafter (the plan's own separation rule, and
   T102's text) and the freeze (T103) follows the pass. If
   the parent prefers the plan's single-PR shape, T102/T103
   work can land as further commits on this branch; the
   draft itself is complete either way.
2. **A join that does not exist, avoided.** The obvious
   computation for "corpus-attested signs with no anchor
   coverage" — subtracting the register's keys from the M77
   file's attested codes — is invalid on these records: the
   two number spaces are demonstrably different (the file
   attests codes to 920; the Mahadevan list space the
   register keys occupy ends at 416 — and numerical
   coincidence is not identity: the 25 file codes whose
   numerals match a register key are matches of numerals,
   not established identities of signs). The document therefore grounds its
   coverage-and-identity items in records where the join is
   itself a record: the register's own validation statuses
   (§2.4γ) and the crosswalk records with their counted
   partiality (§2.4α/ε, Spec 077's 158). T102 should attack
   the document as written here, not the naive version.
3. **Loader documentation vs the pinned file.** The M77
   loader's header states an inscription-length range of
   1–14 (April 2026); the pinned file contains 25 lines
   longer than 14 tokens (counted). The document counts the
   file as it stands and names the discrepancy in place
   (§1.2), rather than repeating the header's range.
4. **The candidate-state tuple.** spec.md's brief for the
   state ("sign inventory + segmentation + reading
   assignments + language identification") is executed as
   (Σ, γ, ρ, λ) with segmentation and sign identity carried
   by the single component γ (a classification rule fixes
   both); the document states the equivalence of the two
   presentations where γ is defined (§2.1).

## Claims assessed at this stage (draft scope)

- **C090-1 — draft leg holds.** A single standalone
  document exists in the spec's records, written before any
  G2 work, versioned v1 with its hash recorded here. The
  freeze leg is T103's, not yet executed.
- **C090-2 — holds on the draft's evidence.** The five
  classes are the classes the program's verdicts rest on;
  each carries its provenance rule and counted population;
  exception classes are named with counts (extracted
  null-falsifier 9; no_validation_record 3; stage-`created`
  193; premise_superseded 113).
- **C090-3 — holds on the draft's evidence.** π is stated
  as a mapping from a defined candidate state to the
  records it would produce; equivalence is decidable for
  named states by the finite check of §2.3, illustrated on
  two cases. T102's question (ii) is its trial.
- **C090-4 — holds on the draft's evidence.** Items α–ε
  each cite the record or count that grounds them (§2.4).
  T102's question (iii) is its trial.
- **C090-5 / C090-6 — the audit is executed and reaches
  the none-needed disposition** (summary table above);
  under D-090-2 the disposition closes only at T103's
  freeze, after T102's attack. Recorded here as the draft's
  disposition, not as a settled outcome.
- **C090-7 — holds on the draft's evidence** (separation
  check above).
- **C090-12 — accounted as it stands.** §1.4 states the
  ledger's generated layers, the settling semantics, and
  the gate exactly as they operate, and credits this study
  with none of it.
- All other C090 claims are **not yet assessed** — their
  falsifiers execute against S2/S3, which have not started.

## T101's "does not establish" line (from tasks.md)

*This does not establish:* that the definitions are right —
only that they are stated, completely, in the skeleton's
terms, before results; their trial is T102's attack and
S2's use of them.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
