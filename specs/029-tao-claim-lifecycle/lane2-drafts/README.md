# Lane-2 explanations for the live claims — Spec 029

**Status of everything in this directory: ADOPTED — authored by
Tristen Pierson, 2026-10-13.** The texts were AI-drafted on 2026-10-13,
shown to the owner in full (the readable copy in this directory), and
adopted by him as authored by him the same day, in his words: "Adopt
all 35 lane-2 drafts as authored by me." The drafting AI is not the
author (OD-2); the adoption is recorded in every record's
`ai_assistance_disclosure`. Ingestion of these records into the live
claim records is the companion act of the same owner order, recorded
in `../lane2-adoption-record.md`.

## Why these files exist

Spec 029 put every claim on a five-stage scale — **created, checked, explained,
accepted, digested** — and kept the two lanes separate: machine-speed checking
(lane 1) never displays as human-paced acceptance (lane 2). At the Spec 029
closeout the live claim set stood at 220 created / 116 checked / 0 explained /
0 accepted / 0 digested across the full register, and 105 records carried the
**verified but unexplained** flag: a check exists, but no human has ever
explained, in a durable record, what the evidence is and what it means.

This directory is the drafting step toward closing that gap for the claims on
the program's public evidence surface. It contains, for each in-scope claim:

1. the claim restated in plain words;
2. an **explanation draft** — what the evidence actually is, how it was
   checked, and why it supports the claim, only partly supports it, or
   contradicts it — grounded only in the merged record, with the source phase,
   spec or report cited for every figure;
3. a **`not_understood` draft** — what remains unknown, what evidence would
   change the picture, and what the claim does not establish.

## The rule that governs these drafts (OD-2)

An explanation counts only when a **named, accountable human** authors it in a
durable record. An AI may draft; an AI may never be the named human. Therefore:

- Every text here was written by an AI agent (Muse Spark, via Muse) on
  2026-10-13, at the direction of Tristen Pierson, and is marked as such in
  every record (`drafter` set; `ai_assistance_disclosure` filled in).
- The explanation-record fields that only a human can complete — `author`,
  `artifact_uri`, `content_hash`, `challenge_venue` — were **deliberately
  empty** in the drafts. Filling them in was the authorship act, and it
  happened at adoption: `author` is Tristen Pierson (`author_kind` human);
  `artifact_uri` is this directory's `drafts.json` on `main`, with a
  per-claim fragment; `content_hash` is the SHA-256 of the record's
  explanation text; `challenge_venue` is the repository's issue tracker,
  where challenges to these accounts are filed and answered.
- **Adoption itself changed no live record.** The stage moves and the
  writing of these texts into the claims, anchor-adjacent and prediction
  records are the ingestion act, recorded separately in
  `../lane2-adoption-record.md`. The script is not deciphered, and nothing
  here says otherwise.

## How authorship worked

1. The drafts were prepared (above) and the full readable copy was shown
   to the owner.
2. On 2026-10-13 the owner adopted all 35 as authored by him, verbatim:
   "Adopt all 35 lane-2 drafts as authored by me." The authoring fields
   were completed on every record in `drafts.json` at that point, and
   each completed record validates under the Phase B machinery
   (`backend/glossa_lab/claim_bundle.py`, `validate_explanation_record`).
3. The completed explanation records and the adopted `not_understood`
   texts were then written into the live claim records — stage changes
   only through the transition service, the single writer for stage
   changes, and only where its rules allow (a claim at `checked` with an
   authored explanation advances to `explained`; a claim still at
   `created` keeps its stage, because explanation cannot precede
   checking). Automation alone can never take a claim past `checked`;
   that is by design, not by backlog.

## Scope — what was drafted, and what was not

**Drafted: 35 claims** — every live claim record that carries a Spec 029
stage, lacks authored explanation / `not_understood` text, and has a record
substantive enough to draft against:

- the **23 canonical extracted claims** (the post-Phase-I store in
  `glossa-indus/claims/extracted_claims/`; 8 at `checked`, 15 at `created`);
- the **10 study headline claims** staged `checked` in the Spec 029 audit;
- **PRED-2026-006 and PRED-2026-007**, the two registered predictions with
  recorded partial checks (both staged `checked`).

**Not drafted, with reasons:**

- **PRED-2026-001, PRED-2026-002, PRED-2026-003** — registered predictions,
  still `PENDING` and never scored: no check has run, so there is nothing to
  explain. Drafting lane-2 text for an untested prediction would manufacture
  the appearance of substance the program's rules exist to prevent. They
  become drafting targets if and when a qualifying test runs.
- **The 8 merged evidence instances** in the extracted-claims store — since
  Phase I they are evidence instances of canonical claims, not claims of
  their own. Each is named on its canonical claim's draft; the proposition is
  drafted once, on the canonical record.
- **The 3 hypothesis models** (`HYP-roif_guild_ledger`,
  `HYP-hunt_civic_ritual`, `HYP-parpola_proto_dravidian`) — staged `created`,
  with no check or verdict records behind them (one record is empty). There
  is nothing on the record to explain.
- **The 287 sign-reading anchors** — readings, not claim records on the
  evidence surface. They carry `validation_status` from Phase H and are a
  different workstream; no per-anchor `not_understood` surface exists for a
  draft to target.

## Honesty notes carried into the drafts themselves

- Several checked claims rest partly or wholly on the program's own test
  batteries and on corpora of a single lineage (Mahadevan/ICIT). Where that
  is true, the draft says so in the body, not in a footnote.
- Two Parpola claims carry partial support computed with the program's
  semantic-anchoring method, which the program itself falsified on held-out
  data in Phase-107. Their drafts say this plainly; no rerun of those
  comparisons under a surviving method exists in the record.
- Nine records are **fragments**, not full claims — single table cells or
  section headings lifted by automatic extraction (five sign-value cells,
  two critique headings, one language-hypothesis label, one statistical
  heading). Their drafts are short on purpose: each states what the fragment
  is, why it cannot be checked as written (no named sign list, no stated
  proposition, or no falsification condition — per the Phase-104 evaluation),
  and what would make it checkable. A stated gap beats a padded draft.
- Three of the fragments (the two critique headings and the language label)
  restate the Farmer–Sproat–Witzel thesis. A Phase-104 evaluation argued
  their parent claim's `contradicted` verdict should carry over to them; the
  carry-over was never written into the live records, which still stand
  untested. The drafts record both facts and name the reconciliation as an
  append-only correction still owed.

## Files

- `drafts.json` — the structured records (the drafts, as adopted on
  2026-10-13). Field names mirror the Phase B explanation record
  (`author`, `author_kind`, `drafter`, `artifact_uri`, `content_hash`,
  `challenge_venue`, `ai_assistance_disclosure`) and the live
  `not_understood` field, so the adopted records ingest without renaming
  anything.
- `drafts-review.md` — the same content rendered for reading, generated from
  `drafts.json` by `build_review.py`. Edit the JSON, then re-run the script.
- `build_review.py` — the generator; it also refreshes the index table below.

## Index of drafts

<!-- BEGIN GENERATED INDEX -->

| Claim | Stage at drafting (2026-10-13) | One-line gist |
|---|---|---|
| `farmer_sproat_witzel_2004_manual_001` | checked | The claim that the Indus signs are not writing at all - contradicted by the recorded checks. |
| `indus_valley_script_deciphered_from_myth_65ff0a26_manual_002` | checked | The fish sign as a badge for coastal traders - its own stated test came back against it. |
| `parpola_2010_dravidian_solution_manual_001` | checked | Parpola's claim that the script writes Proto-Dravidian by the rebus method - partly supported, on a method the program later falsified. |
| `parpola_2010_dravidian_solution_manual_002` | checked | The fish sign read as 'meen' (fish/star) - one sign of the family passed its positional test; the family's commonest sign failed it. |
| `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001` | checked | Inscriptions follow a three-part pattern (opening, middle, ending) - the pattern is real; what the parts mean is untested. |
| `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003` | checked | Animal signs as opening markers - the opening-position half is supported; the animal half was never tested. |
| `yadav_2009_arxiv_manual_001` | checked | Sign frequencies follow the Zipf-Mandelbrot curve - the curve fits; the fit says little about what the signs mean. |
| `yadav_2009_arxiv_manual_002` | checked | Some signs prefer the start of texts and others the end - supported by the counts, but the claim carries no falsifier. |
| `indus_valley_script_deciphered_from_myth_65ff0a26_manual_001` | created | Roif's master claim - the script is an economic ledger of guilds and tribute. Never tested. |
| `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003` | created | The arrow sign as a border-enforcement marker. Never tested - and the counts that exist sit in the big cities. |
| `indus_valley_script_deciphered_from_myth_65ff0a26_manual_004` | created | The horned-deity sign as a fire-altar intermediary - tied to Kalibangan. Never tested. |
| `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_002` | created | Hunt's civic-ritual system: inscriptions encode a shared civic order, not royal power. Never tested. |
| `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004` | created | Sky signs (sun, star, moon) as closing markers for cycles. Never tested - the program has no sky-sign class to test with. |
| `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_005` | created | Hunt's 24-cluster 'Translation Atlas' - the atlas itself is not in the repository, so its test cannot run. |
| `ancient_writing_and_modern_technologies_51831ac9_sign_val_0001` | created | Fragment only: 'Sign 900 means the number six.' The sign list is never named, so nothing can be checked. |
| `ancient_writing_and_modern_technologies_51831ac9_sign_val_0002` | created | Fragment only: 'Sign 700 belongs to a measure system with a unit of 40.' Unverifiable as written - and a sibling record disagrees with it. |
| `ancient_writing_and_modern_technologies_51831ac9_sign_val_0003` | created | Fragment only: 'Sign 700 means a unit of 4.' The rival of the unit-of-40 fragment; neither can be checked as written. |
| `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001` | created | Fragment only: 'Sign 821 is used in a variety of contexts.' Too thin to test. |
| `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002` | created | Fragment only: 'Sign 297 is the horned tiger.' An identification with no named sign list and no test. |
| `ancient_writing_and_modern_technologies_51831ac9_statisti_0004` | created | Fragment only: the heading 'Statistical finding: positional analysis' with no finding attached. |
| `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001` | created | Fragment only: the heading 'Critique: myth of a literate Harappan' - points at the Farmer thesis; an evaluation says its verdict should carry over, but the record was never updated. |
| `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002` | created | Fragment only: the heading 'Critique: collapse of the Indus script thesis' - same position as its sibling fragment, same unapplied carry-over. |
| `without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001` | created | Fragment only: the label 'Language hypothesis: non-linguistic symbol' - a restatement of the Farmer thesis in label form. |
| `STUDY-SPEC-019/PHASE-125` | checked | The two great sign compilations were expected to agree on sign positions. They do not - and 93.9 percent of the disagreement is unexplained. |
| `STUDY-SPEC-023/PHASE-132+383` | checked | The claim that AI coders at this protocol could produce a publishable transcription layer - contradicted by its own agreement test. |
| `STUDY-SPEC-024/F1` | checked | Seals and tablets end their texts differently: the final sign's class depends on the object type, within each site. |
| `STUDY-SPEC-024/F2-HOLDAT` | checked | Sites were expected to have distinct sign repertoires in the Holdat compilation. Any effect there is smaller than the margin the program set in advance. |
| `STUDY-SPEC-024/F3-ICIT` | checked | In the ICIT-lineage corpus, sites do use different sign repertoires - supported, with named confounders that could be wearing the site label. |
| `STUDY-SPEC-025/G1` | checked | The site association survives controlling for preservation and text composition - but not for time. That rider is part of the result. |
| `STUDY-SPEC-027/STAGE1-PHASE-392` | checked | Do cities with similar sign repertoires sit closer together? A real but tiny signal that collapses without Harappa - inconclusive. |
| `STUDY-SPEC-028/ARM-A` | checked | The Stage-1 question with Harappa removed entirely: the effect shrinks below the margin - inconclusive. |
| `STUDY-SPEC-028/ARM-B` | checked | The Stage-1 question with every site counting equally: the headline number clears the margin, but dropping Harappa still breaks it - inconclusive. |
| `STUDY-SPECS-001-023+PHASES-TO-141` | checked | The audit headline: when the tightened framework re-read the program's first 141 phases, 75 of 116 items changed evidentiary status. |
| `PRED-2026-006` | checked | Predicted: INITIAL signs stay initial at Harappa. The number on record is global, not Harappa-specific - the registered test has not actually been run. |
| `PRED-2026-007` | checked | Predicted: at least 70 percent of ITM-coded signs land in TERMINAL clusters. The count stands at 2 of 3 - below the bar, on a sample of three. |

<!-- END GENERATED INDEX -->

*Drafts prepared 2026-10-13 against main `dede49f7` (Spec 029 closed);
adopted 2026-10-13 by Tristen Pierson. As adopted, `drafts.json` is the
durable artifact of record for the 35 explanation records; the program's
claim records are the stores and spec files the texts cite.*
