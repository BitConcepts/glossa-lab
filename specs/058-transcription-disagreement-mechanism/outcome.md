# Spec 058 / Phase-420 — Outcome record (EXECUTED 2026-10-21 — LOCALISED TO SIGNS)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 058 contract
> (freeze digest
> `8bdd4764380bf9e6cb442b1cc75a3b57f4507284676bcb65603e481a49435713`,
> PR #259 merged at `e4a99c24`), as **Phase-420**,
> in Wave 3 group 2 of the runnable-experiments
> campaign (plan approved AS WRITTEN on
> 2026-10-21). The execution gate was satisfied
> before the run: OSF registration **86dgh** is
> APPROVED + PUBLIC (DOI 10.17605/OSF.IO/86DGH).
> Outcome: **LOCALISED TO SIGNS** — every step-0
> gate passed, the produced record set reproduced
> the committed Phase-132 metrics in full, and of
> the three frozen locus rules only the sign rule
> fired. Arm B was not touched: it stays blocked,
> and no AI substitution for human coders exists
> anywhere in this execution (claim F058-C06).

## Headline (spec §5.2 wording, LOCALISED TO SIGNS form, with the mandatory UNK sentence)

"Re-analysed under Spec 058, the disagreement
between the two recorded Phase-132 pilot passes is
localised to signs: the 10 most-involved signs
account for 54.5% of all mismatch involvement, led
by UNK, P310, P144, UNMAPPED:M817, P145, P245,
P119, P184, P268, P324. The pilot's failure stands
exactly as recorded; this account names where its
disagreement sits, in this pilot's passes, and
says nothing about human coders. UNK — the passes'
'no identification' value — is itself among the
most-involved values (27.7% of involvement); the
localisation is in part a localisation to
illegibility, stated as such."

Claim: `STUDY-SPEC-023/PHASE-132+383` — SETTLED —
CONTRADICTED, unchanged. The pilot still failed,
and stays failed; this record appends the dated
mechanism account its lane-2 record asked for and
re-opens nothing. In plain words: the two passes
did not disagree evenly. Of 103 mismatch events
over the 40 objects where the passes differ, the
ten most-involved sign values carry over half of
all involvement — and the single largest of them
is UNK, the value a pass records when it cannot
identify a sign. The disagreement is concentrated
first in illegibility itself, then in a short list
of named signs (P310 above all). It is not
concentrated in one kind of object: seals carry
most events, but only in line with how much of the
frame they are — the frozen enrichment margin is
exactly what keeps that from counting as a
localisation. And it is not a segmentation story
under the registered proxy: only 14.6% of events
are insertions or deletions.

Fence sentence: "This account is about why two
recorded AI pilot passes disagreed. It is not
evidence about human transcription, and it
changes no verdict."

## 1. What was executed

The frozen contract's execution shape (spec §11),
in order, under the graph-first build (H15/H23):
experiment script
`backend/scripts/phase420_transcription_disagreement.py`;
graph module
`backend/glossa_lab/experiment_graph_phase420.py`
(node `IndusPhase420TranscriptionDisagreement`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The script imports the
pinned Phase-132 metrics module
(`backend/scripts/phase132_metrics.py`, SHA-256
`238dfafa…`) unchanged for the store loader, the
P-space derivation, the alignment, and the gate
0.4 reproduction; it reimplements none of them.
The run's base was `main` at
`3200b7b5b6841a7b9567a81368bf84004fd17255`. The
run's own records:
`reports/phase420_results.json` (SHA-256
`3d140333b3b751697721c1528d48b936ca0010fd2d78d4a667d2fca6b5388922`)
and `reports/phase420_report.md` (SHA-256
`b8634d761212d43de1341008f7fc8920387a9432c1cefc0242794a810719f0d8`)
— both digests derived twice by independent
routes (`sha256sum` and a Python `hashlib`
recomputation, identical), and the script is
deterministic: a second run reproduced both
output files byte-identically. An independent
spot re-derivation with the module's own
`alignment_differing` over the produced store
recomputes the same event total (103) and the
same matched-pair total (95) as the committed
metrics' per-token numerator.

Every §2.1 pin was also re-asserted in the
foreground before the run, by two independent
routes — the git-blob route and the GitHub
contents-API route, both at the run's base
commit — with identical results on all thirteen
pinned files (the twelve §2.1 inputs and the
lane-2 drafts file).

## 2. Step 0, gate by gate (all passed)

- **0.1 Committed-record integrity — PASS.**
  Every §2.1 input recomputes to its freeze pin
  in the run tree: Spec 023 spec `c2e5d166…`,
  pilot metrics `e864fca5…`, pilot report
  `e1df32da…`, pilot frame `a967144b…`, pilot
  dataset `adb596a1…`, dataset meta `b2c607fa…`,
  Phase-383 results `4e52942d…`, Phase-383 report
  `9f35f722…`, metrics module `238dfafa…`,
  rescoring module `b64b60de…`, crosswalk
  `4e7559df…`, anchors `df0cf620…`.
- **0.2 Pilot-pass record production — PASS.**
  The record set was produced at the execution
  venue — the machine holding the program's main
  checkout, whose gitignored store DD-058-15
  verified — read-only: the main checkout was
  inspected and read, never modified, cleaned,
  reset, staged, or committed in. Inventory
  against the pilot report's §9 counts, keyed by
  the committed frame's 50 canonical keys:
  `frame.json` present; 50 Pass A records; 50
  Pass B records; 10 gold-pass records (the 10
  gold keys); 50 adjudication records;
  `effort_log.csv` with 320 events. No record
  missing, none edited, completed, or
  re-created. A per-file SHA-256 manifest of the
  full 162-file produced set was computed and is
  recorded in `reports/phase420_results.json`
  and in the phase report. (The produced
  `frame.json` also hashes to `a967144b…`, the
  committed frame file's own hash — the two
  files are byte-identical; gate 0.3 requires
  only list equality, which also holds.)
- **0.3 Frame identity — PASS.** The produced
  store's frame list equals the committed pilot
  frame's frame list in full — the same 50
  canonical keys with the same site, recorded
  object type, and gold flag per key.
- **0.4 Reproduction of the committed metrics —
  PASS.** The pinned metrics module, imported
  unchanged, computed the metrics from the
  produced store, and the computed record equals
  the committed metrics file **in full**
  (whole-record equality, not only the headline
  values): exact-sequence agreement 0.20 (all-50,
  P and M), per-token agreement 0.4798 (all-50)
  and 0.4286 (gold), gold estimator 0.05, pass
  token totals 191 / 190 / 40 / 189, and every
  per-object exact flag and match count.
- **0.5 Adjudication-taxonomy cross-check —
  PASS.** The taxonomy recomputed from the
  produced adjudication records equals the pilot
  report's §4(c) counts exactly: identity 93,
  legibility 45, count 11, key 10, orientation 2,
  order 1; total 162.
- **0.6 Analysis census — PASS.** The mismatched
  population enumerated from the reproduced
  per-object flags is the 40 objects whose Pass A
  and Pass B P-sequences differ — Mohenjo-Daro
  20, Harappa 14, Lothal 5, Kalibangan 1; by
  recorded type Seals 30, Tablets 7, Unrecorded
  3; 9 of the 10 gold objects are in the census.
  The full census (key, site, recorded type,
  gold flag, both sequence lengths) is §3 below
  and is the population every §4 share is taken
  over. The gold pass and the adjudicated
  sequences were not inputs to the analysis
  (DD-058-2).

## 3. The census (gate 0.6)

| key | site | recorded type | gold | len A | len B |
|---|---|---|---|---|---|
| cisi:v1:M-21 | Mohenjo-Daro | Seals | no | 8 | 6 |
| cisi:v1:M-41 | Mohenjo-Daro | Seals | no | 8 | 8 |
| cisi:v1:M-58 | Mohenjo-Daro | Seals | no | 5 | 5 |
| cisi:v1:M-75 | Mohenjo-Daro | Seals | no | 5 | 5 |
| cisi:v1:M-93 | Mohenjo-Daro | Seals | yes | 5 | 5 |
| cisi:v1:M-110 | Mohenjo-Daro | Seals | no | 4 | 5 |
| cisi:v1:M-127 | Mohenjo-Daro | Seals | no | 5 | 5 |
| cisi:v1:M-144 | Mohenjo-Daro | Seals | yes | 6 | 6 |
| cisi:v1:M-162 | Mohenjo-Daro | Seals | no | 6 | 6 |
| cisi:v2:M-658 | Mohenjo-Daro | Seals | no | 7 | 5 |
| cisi:v1:M-195 | Mohenjo-Daro | Seals | no | 5 | 5 |
| cisi:v1:M-250 | Mohenjo-Daro | Seals | yes | 3 | 3 |
| cisi:v2:M-819 | Mohenjo-Daro | Seals | no | 6 | 6 |
| cisi:v1:M-321 | Mohenjo-Daro | Seals | no | 3 | 3 |
| cisi:v2:M-926 | Mohenjo-Daro | Seals | no | 7 | 7 |
| cisi:v2:M-983 | Mohenjo-Daro | Seals | no | 4 | 1 |
| cisi:v1:M-480 | Mohenjo-Daro | Tablets | no | 8 | 8 |
| cisi:v2:M-1247 | Mohenjo-Daro | Seals | yes | 0 | 1 |
| cisi:v2:M-1352 | Mohenjo-Daro | Seals | no | 4 | 3 |
| cisi:v2:M-1448 | Mohenjo-Daro | Tablets | no | 3 | 3 |
| cisi:v1:H-66 | Harappa | Seals | no | 4 | 4 |
| cisi:v1:H-139 | Harappa | Seals | no | 3 | 3 |
| cisi:v1:H-212 | Harappa | Tablets | no | 6 | 6 |
| cisi:v1:H-305 | Harappa | Tablets | no | 6 | 6 |
| cisi:v2:H-271 | Harappa | Seals | yes | 4 | 4 |
| cisi:v2:H-451 | Harappa | Seals | no | 3 | 4 |
| cisi:v2:H-523 | Harappa | Seals | no | 4 | 5 |
| cisi:v2:H-596 | Harappa | Seals | no | 2 | 2 |
| cisi:v2:H-669 | Harappa | Seals | no | 3 | 3 |
| cisi:v2:H-743 | Harappa | Tablets | yes | 7 | 7 |
| cisi:v2:H-814 | Harappa | Tablets | no | 5 | 5 |
| cisi:v2:H-960 | Harappa | Tablets | no | 5 | 5 |
| cisi:v2:Pk-24 | Harappa | Seals | no | 0 | 1 |
| cisi:v2:Skh-7 | Harappa | Unrecorded | no | 1 | 1 |
| cisi:v1:L-33 | Lothal | Seals | no | 3 | 3 |
| cisi:v1:L-66 | Lothal | Seals | yes | 6 | 8 |
| cisi:v1:L-98 | Lothal | Seals | yes | 4 | 4 |
| cisi:v1:L-165 | Lothal | Unrecorded | no | 4 | 4 |
| cisi:v1:L-227 | Lothal | Unrecorded | no | 1 | 1 |
| cisi:v1:K-63 | Kalibangan | Seals | yes | 4 | 4 |

## 4. Tabulations (spec §4; P space, primary)

The event total is **E = 103** mismatch events
over the 40 mismatched objects (88 SUBSTITUTION,
15 INDEL). Summed involvement is **191** (each
substitution counts once for each of its two
values, DD-058-6). Both passes' full token
streams total **381** tokens (191 + 190), the
frequency basis.

### T1 — by sign

The 10 most-involved values (ranked by
involvement, ties by value string ascending;
the full ranked table is in
`reports/phase420_report.md` and the results
JSON):

| value | involvement | involvement share | frequency | frequency share |
|---|---|---|---|---|
| UNK | 53 | 27.7% | 149 | 39.1% |
| P310 | 13 | 6.8% | 29 | 7.6% |
| P144 | 6 | 3.1% | 12 | 3.1% |
| UNMAPPED:M817 | 6 | 3.1% | 6 | 1.6% |
| P145 | 5 | 2.6% | 13 | 3.4% |
| P245 | 5 | 2.6% | 5 | 1.3% |
| P119 | 4 | 2.1% | 12 | 3.1% |
| P184 | 4 | 2.1% | 4 | 1.0% |
| P268 | 4 | 2.1% | 4 | 1.0% |
| P324 | 4 | 2.1% | 4 | 1.0% |
| **top 10** | **104** | **54.5%** | **238** | **62.5%** |

Sign state: **CONCENTRATED** — the top-10 share
(54.5%) meets the design's 50% line. UNK alone
carries 53 of 191 involvements (27.7%); the
mandatory §5.2 sentence is carried in the
headline above. After UNK, the concentration is
thin and spread: P310 (13) is the only other
value in double figures.

### T2 — by object type

| recorded type | events | event share | objects | object share | mismatched objects |
|---|---|---|---|---|---|
| Seals | 80 | 77.7% | 34 | 68.0% | 30 |
| Tablets | 18 | 17.5% | 11 | 22.0% | 7 |
| Unrecorded | 5 | 4.9% | 5 | 10.0% | 3 |

The object-type locus does **not** fire. Seals
meet the 50%-of-events half of the rule (77.7%)
but their enrichment over their frame share is
77.7% − 68.0% = **9.7 points**, below the frozen
10-point margin (DD-058-8) — seals carry most of
the disagreement at almost exactly the rate
their share of the frame predicts. Tablets
(17.5% of events) meet neither half.

### T3 — by divergence type

SUBSTITUTION 88 of 103 events (85.4%); INDEL 15
of 103 (14.6%). The segmentation locus does
**not** fire: the INDEL share — this spec's
registered proxy for segmentation (spec §8(4):
an indel cannot be separated into "the passes
cut the same glyphs differently" and "one pass
recorded a sign the other omitted") — is far
below the frozen 50% line. The passes differ
overwhelmingly in which signs they name at
aligned positions, not in how many signs they
record.

### First divergence

Per mismatched object (full table in the results
JSON): first-divergence position 1 in 21 of 40
objects, position 2 in 11, position 3 in 5,
position 4 in 2, position 5 in 1 — the passes
usually diverge at the very start of the
sequence. By type: SUBSTITUTION 30, INDEL 10.
The value most involved at first divergence is
again UNK (26 involvements), then P310 (6).

### Descriptive secondary (UNK-excluded) and M-space sensitivity

The §4.4 secondary — T1–T3 recomputed excluding
every event involving an UNK value — is
descriptive only and carries no headline: E
falls to 50 events (53 of the 103 events involve
UNK on at least one side); the top-10 sign share
is 41.5% (state BETWEEN — below the 50% line);
the INDEL share is 12.0% (6 of 50). Stated
plainly: with illegibility set aside, the
remaining disagreement does **not** meet the
frozen concentration criterion — the headline's
localisation to signs is carried in large part
by UNK itself, exactly the weakness spec §9
named in advance, and it is reported as such,
not smoothed over. The secondary's leading
values are P310 (7), UNMAPPED:M817 (6), P144 (5),
P145 (5), P119 (4).

The M-space sensitivity (descriptive only,
DD-058-4) tells the same story as the primary:
E = 103, top-10 share 53.9% (CONCENTRATED),
INDEL share 14.6%, and no object-type locus.
Full M-space tables are in the results JSON;
they move no headline.

### Per-locus verdicts

- **SIGNS — FIRES.** Top-10 involvement share
  104/191 = 54.5% ≥ 50% (F058-C11).
- **OBJECT TYPES — does not fire.** Best case
  Seals: 80/103 = 77.7% of events, enrichment
  9.7 points < 10 (F058-C12).
- **SEGMENTATION — does not fire.** INDEL share
  15/103 = 14.6% < 50% (F058-C13).
- **Headline — LOCALISED TO SIGNS** (exactly
  one locus fires; F058-C14), in the §5.2
  pre-written wording with quantities filled,
  with the mandatory UNK sentence.

## 5. Claim consequences (governed register)

One line per governed claim, F058-C01…C16.

- **F058-C01** (an outcome states only where
  the disagreement localises): HELD — every
  product of this execution states the pilot-pass
  localisation and nothing beyond it.
- **F058-C02** (the claim stands CONTRADICTED
  on its recorded numbers): HELD — the recorded
  numbers were re-verified at gate 0.1 (pins)
  and gate 0.4 (full reproduction); the verdict
  is quoted only as recorded.
- **F058-C03** (the disagreement is
  concentrated, not uniform): SUPPORTED, within
  its frozen boundary — the SIGNS locus fired
  under F058-C11 (top-10 share 54.5%, state
  CONCENTRATED). Support is for the pilot's two
  recorded AI passes only, and §4's secondary
  states the limit of the finding: excluding
  UNK-involved events, the concentration does
  not meet the criterion.
- **F058-C04** (no locus fires → NOT
  LOCALISED): NOT TRIGGERED — the sign locus
  fired, so the falsifier's outcome does not
  arise; the claim's wording machinery was
  nevertheless applied mechanically to reach
  the headline.
- **F058-C05** (residue re-analysis, appended;
  frozen records unedited): HELD — no Spec 023,
  Phase-132, or Phase-383 file was modified
  (their §2.1 hashes are unchanged after the
  run); the mechanism account appends as this
  record and the root LEDGER entry. No append
  was made to the lane-2 drafts file: its bytes
  are a frozen pin of this spec's own freeze
  record (`3f645c9a…`, asserted by
  `test_spec058_freeze.py`), and the dated
  append for the claim's record is this outcome
  record and the LEDGER entry — the Spec 044
  (F044-C02) reading.
- **F058-C06** (arm B out of scope): HELD —
  arm B appears in this execution only as
  blocked-out-of-scope; nothing was specified,
  recruited, simulated, or scored for it, and
  no AI substitution was designed or run.
- **F058-C07** (inputs only as named in §2):
  CHECKED — gates 0.1/0.2 records: the §2.1
  committed pins plus the produced store record
  set with its 162-file manifest; no other
  data, no re-coding, no images.
- **F058-C08** (frozen machinery): CHECKED —
  the pinned metrics module was imported
  unchanged; gate 0.4's exact reproduction is
  the identity proof, per the Phase-383
  precedent.
- **F058-C09** (step-0 gates fail-closed, in
  order): CHECKED — all six gates ran in frozen
  order and passed before any event was
  tabulated; the gate record precedes every
  quantity in the results JSON.
- **F058-C10** (event definition): CHECKED —
  events are the frozen alignment's columns as
  defined; every event is published per object
  in the results JSON, recomputable column by
  column.
- **F058-C11** (sign locus rule): FIRED as
  written — 104/191 = 54.5% ≥ 50%; companion
  state CONCENTRATED.
- **F058-C12** (object-type locus rule): DID
  NOT FIRE as written — Seals 77.7% of events
  with a 9.7-point enrichment, below the
  10-point margin; Tablets 17.5%.
- **F058-C13** (segmentation locus rule): DID
  NOT FIRE as written — INDEL share 14.6% <
  50%, carrying the registered proxy limit
  wherever stated.
- **F058-C14** (headline mapping): HELD — one
  firing locus (SIGNS) gives LOCALISED TO
  SIGNS, in the pre-written §5.2 wording.
- **F058-C15** (UNK counted as recorded):
  CHECKED — the primary counts UNK and
  UNMAPPED values exactly as recorded; the
  UNK-excluded secondary is reported beside it
  and carries no headline; the mandatory UNK
  sentence stands in the headline paragraph.
- **F058-C16** (nothing about human
  performance, the floor, or the codebook):
  HELD — no output of this execution states a
  human-performance, floor-correctness, or
  codebook claim, and none presents the
  localisation as explaining *why* any sign is
  hard to read; illegibility, image quality,
  sign-list ambiguity, and coder behaviour all
  remain live, named causes this tabulation
  does not adjudicate among.

## 6. What this does not establish

Carried from the frozen contract, verbatim in
substance: this account is about these 50
objects, these two passes, this protocol — both
passes are one model family's AI codings
(Phase-383 origin-group audit: effective
independent coder origin groups = 1). It
establishes nothing about human transcription
(arm B's question, still blocked), nothing
about whether the 0.80 floor was the right bar,
and nothing about whether a clarified codebook
would improve agreement. A localisation is not
an explanation and not an exculpation: the
pilot failed, and stays failed.

## 7. Records

- Results JSON: `reports/phase420_results.json`
  (SHA-256 `3d140333…`); report:
  `reports/phase420_report.md` (SHA-256
  `b8634d76…`).
- Graph node:
  `IndusPhase420TranscriptionDisagreement`
  (registered and verified by import before the
  run).
- Root LEDGER entry: `LEDGER.md`, 2026-10-21,
  Spec 058 execution (Phase-420).
- `adjudication.md` carries no execution
  append: it is a digest-covered source of the
  freeze, and the executed-spec form records
  execution in this outcome record, not in the
  frozen adjudication. Frozen files of this
  spec (spec, claims, freeze record) stand
  byte-identical.
- Foundation check (H21): run at the run tree
  before this record landed — **40 passed /
  0 failed / 8 warnings**, the standing figure;
  `reports/foundation_check_report.json`
  regenerated at the run (Holdat corpus
  CSV SHA-256 `62d14d2b…` verified first).
- Anchors: asserted byte-identical before and
  after (`df0cf620…` at both readings).
- Tasks E1–E5 stand ticked in `tasks.md` with
  this record.
- Local-environment disclosure (as on Specs
  056/057/058's freeze records):
  `test_register_integrity` fails locally under
  this VM's AEE 1.5.3 strict loader on the
  frozen register's string `boundary` field —
  identically on the clean `main` tree at the
  run's base, before any change of this
  execution; CI is the figure of record.
- Landing record (PR, merge commit, CI,
  foundation check at merge): appended below
  at merge, dated, append-only.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
