# Phase-438 — Spec 054 (amended): Yadav's opening/closing signs under battery NB-1

Claim under test: `yadav_2009_arxiv_manual_002` — "There are specific text-beginning and text-ending signs in the Indus corpus" (strongly supported as recorded; this run moves no claim status). Freeze digest `d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57`; OSF registration 8spvf (approved, public). Executed 2026-10-24 under the owner's execution order of 2026-10-24.

## The falsifier (appended to the claim's record at the freeze, 2026-10-23)

> This claim, as evaluated under battery NB-1 (the Spec 054 amendment, as frozen), is falsified if any of the following holds when the frozen battery is run on the frozen arm-1 and arm-2 corpora: (1) either arm-1 positional-strong set (opening or closing) is empty; (2) for either class, fewer than half of arm 1's positional-strong signs are also positional-strong in arm 2 in the same class, through the pinned crosswalk; or (3) the pooled cross-arm overlap of positional-strong signs does not exceed the 95th percentile of the 999-shuffle label-permutation null — the three conditions applied under the precedence rule of the Spec 054 amendment (§5.5).

## Step-0 gates (amendment section 6, in order)

- **Gate G1 — Pin checks (draft 0.1): PASS**
- **Gate G2 — Strict corpus identification and pin (draft 0.3): FAIL**
- **Gate G3 — Thinness: NOT REACHED**
- **Gate G4 — Second arm runnability: NOT REACHED**
- **Gate G5 — Determinism: NOT REACHED**

## Step-0 record — strict corpus identification (gate G2)

Reference census (C3, from the pinned Phase-43 record, T1_1): source "indusscript.in Firestore 'indusarrays' (2026-05-14)"; 3916 records; 2665 unique dockeys; 3137 sequences; 12494 sign instances.

C1 — the V3 loader's data file (the Firestore 'indusarrays' dump): absent at its path in this tree, in the main checkout, and in every sibling tree scanned (9 candidate paths); the loader therefore loads zero records and zero sequences.

C2 — database copies: no database copy exists in the execution tree; the programme database (backend/data/glossa.db, main checkout) holds 9 texts, of which the only Indus entry is the synthetic prototype ("Indus Script (synthetic, Yadav 2010 / Fuls 2014)", 923 inscriptions by its metadata) — not the V3 layer.

C4 — other layers held, censused; none is the corpus the Phase-43 record names, and none was substituted:

- **yajnadevam_inscriptions.csv (the programme's site-attributed layer; Specs 042/045's layer of record)** — records 5679. a different layer: not the Firestore 'indusarrays' reconstruction the Phase-43 record names (its record count also differs from C3's 3,916).
- **mayig CISI layer v1 (data/corpus_layers/mayig_cisi_layer_v1.json)** — inscriptions 179, tokens 1003, distinct_signs 182. the CISI compilation in Parpola numbering (Spec 019's arm) — a different compilation from the Mahadevan-lineage V3 layer.
- **indus_research.jsonl (the V1 research export)** — records 15508. a mixed-source-system export, not the Firestore 'indusarrays' reconstruction the Phase-43 record names.
- **the Holdat downloads layer (indus_corpus 2.csv; arm 2's layer)** — inscriptions 1670, tokens 7002, distinct_signs 390. the other compilation: the Phase-43 record itself treats it as a different corpus (its T4_3 cross-validation against V3); it is arm 2's layer, never a substitute for arm 1.
- **the Shakti corpus layer (restricted-local; Specs 068/052's layer)** — records 5704. a CISI-lineage compilation — a different lineage from the Mahadevan-lineage Firestore V3 layer the Phase-43 record names.

## Outcome

**STRICT CORPUS NOT PINNABLE**

Spec 054 closed at step 0, gate 0.3: the strict corpus layer of record could not be uniquely identified and pinned from the database as the V3 / Mahadevan-lineage corpus the Phase-43 battery used (the V3 loader's data file — the Firestore 'indusarrays' dump the Phase-43 record names as its corpus's source — is absent at its path in this tree, in the main checkout, and in every sibling tree scanned, so the loader loads zero records and zero sequences and the layer cannot be exported or pinned; no database copy of the layer exists (the programme database's only Indus text is the synthetic prototype); and no other layer held is the corpus the Phase-43 record names (the site-attributed layer at 5,679 records, the V1 research export, the mayig CISI layer, the Holdat downloads layer, and the Shakti layer are each a different corpus or lineage)). No positional quantity was computed. This closure is a statement about runnability, not about the claim; the claim stands exactly as recorded, with the falsifier appended at this spec's freeze.

## Limits

- No language conclusion: opening and closing markers occur in non-linguistic systems too; no outcome of this run establishes that the script encodes language (spec section 7.1).
- No meaning conclusion: no outcome establishes what any opening or closing sign means, or what any sign was read as.
- Compilation-relativity: the arms are two compilations' stories, computed inside each compilation and joined only through the pinned crosswalk; no output pools the corpora or presents a crosswalk pair as a finding that two drawn signs are the same sign.
- The Phase-43 record stands: this run edits no Phase-43 file and no prior claim status; the parent claim's record, including its strongly-supported status, is untouched by any verdict (amendment section 9).
- This spec's closing measure is "closing-strong under NB-1" (a per-sign terminal-rate band on an inscription-position basis), a different quantity from Spec 045's "Holdat final-position concentration" (amendment section 10).
- Negative, inconclusive, thin, and step-0 outcomes are recorded with the same prominence as a supported finding.
