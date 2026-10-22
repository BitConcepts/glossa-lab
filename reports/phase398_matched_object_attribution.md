# Phase-398 — Matched-Object Attribution (spec 034)

**This study attributes the residue of a settled result; it does not re-judge it.** The Phase-125 verdict — FAIL — DISAGREEMENT (16 judgeable pairs of 286; median TV 0.636931) — stands untouched (F034-C14). Phase-131 attributed 6.1% of the disagreement and left 93.9% unexplained because the two digital layers shared zero object keys. This phase builds the missing object bridge and asks the question object by object, under the frozen Spec 034 contract (freeze digest `696fd1855c8cbc1fe767fdc26a1697deb1f0dc85253376efdd7064f102594c2a`; OSF registration https://osf.io/zd7uq/, DOI 10.17605/OSF.IO/ZD7UQ).

## Step 0 — the bridge census

- CISI side: the mayig layer holds 179 objects (1003 tokens). The CISI catalogue layer (route (a)) attests 179 of them, out of 3493 catalogued objects (7705 rows).
- Mahadevan side: the ICIT published corpus carries a CISI object reference for 5018 of its 5679 inscriptions (4074 distinct objects), admitted through the Phase-130 intake schema (route (b); validation verdict: pass).
- **Matched objects: 179** (mayig objects with no ICIT reference: 0). Holdat `cisi_number` was never used as a key (F034-C06).
- Matched objects with texts of three or more signs in both compilations: **169** — the frozen gate is 150; gate PASSED.
- Sensitivity: counting only ICIT records the Phase-116 build kept, the same figure is 159 — the gate passes under both counts.
- Route (c): 61 of the gate objects carry a sign covered by one of the 44 Phase-128 dossiers.
- Composition residue (census level): 3895 CISI objects are referenced by the ICIT corpus but not transcribed in the mayig layer.

## Step 1 — profiles on the matched subset

Phase-125's own measurement (total variation, count floor 8, the 286 PRIMARY crosswalk pairs), computed on the 169 matched objects only: **25 judgeable pairs**, matched-object median TV **0.025694**.

## Outcome — ATTRIBUTED TO COMPOSITION

The frozen lines are 0.20 (composition) and 0.32 (transcription). The matched-object median TV of 0.025694 gives: **ATTRIBUTED TO COMPOSITION**. Subset: 169 matched objects, all Mohenjo-daro seals (the CISI vols 1–2 object population transcribed in the mayig layer), Mahadevan-side readings from the ICIT published corpus. As a persistence measure in Phase-131's estimator, the matched-object residual is 0.04034 of the corpus-level distance.

## Decomposition (Phase-131 categories)

Over 29 decomposition-eligible objects (140 not mappable all-or-nothing under the PRIMARY map), difference-block token shares: segmentation 0.0, substitution 0.909091, insertion/deletion 0.090909. Pair classes: {'substitution': 6, 'identical': 22, 'order-only': 1}. Substitutions checked against the crosswalk (a record of disagreement, never ground truth): {'no_crosswalk_row': 10}. Per-object distances: median 0.0 (n = 29).

## What this does not establish

Which compilation is right where they differ (F034-C01). Attribution explains disagreement; it does not crown a winner, and the settled Phase-125 verdict stands exactly as issued.

*Anchors file unchanged: sha256 eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed before and after (asserted in code).*

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.
