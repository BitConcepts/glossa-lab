# Spec 033 — Outcome (Phase-397, the SA-free language comparison)

Date: 2026-10-13 · Execution phase: **Phase-397** · Frozen contract:
`specs/033-sa-free-language-comparison/freeze.json`, digest
`412b4805063bbffb3915a834354cb428cc9b10958f614a1680b859005a43b66d` ·
Registered before execution: OSF https://osf.io/ephf7/,
DOI 10.17605/OSF.IO/EPHF7 · Machine-readable results:
`reports/phase397_results.json`

## What was run

The program's old language comparison — the one that produced the
"partial support" behind the claim that the Indus script encodes a
Dravidian language — was rerun with the semantic-anchoring (SA)
machinery removed entirely. That machinery was later falsified by
the program itself (Phase-107: its predictions scored 0.000 on
held-out inscriptions), so its numbers could no longer be trusted,
and this rerun was registered in advance to replace them.

Five signs carry published word values in three language families
(the lists were written down, with sources, before any score was
computed — `anchors-phase397.json`, SHA-256
`8b1d2db8265dd4b315c4d3a43a736b917c659b19a98701175e1abca0ce0d42ca`).
Each family turns the inscriptions into sound sequences using its
own values; a simple counted model of "which sound follows which"
is then built from the corpus itself, and each family is scored by
how probable it makes the inscriptions look, per sign. The same
arithmetic is applied to a no-language baseline (the five signs
carry no values at all) and to 999 random assignments of the same
published values. Everything runs on the strict sign set — the 94
signs whose readings rest on evidence independent of the falsified
method.

## Verdict

**NOT SUPPORTED** — the bounded claim ("Dravidian assignments fit
the Indus sign sequences better than the named rival assignments
under this method, within the Mahadevan lineage") does not pass
the bars fixed in advance.

The frozen rule that fired: a rival assignment scores at or above
Dravidian on the primary run (claim F033-C11). The best rival is
the **no-language baseline**: giving the five signs no values at
all fits the inscriptions better than giving them Dravidian
values. A second frozen trigger also holds and is reported for
completeness: the Dravidian score lies **inside** the random
assignments' range (F033-C11 again), so the 99th-percentile
condition (F033-C15) fails as well.

## The numbers behind the verdict

Primary run — mean log probability per sign (higher means a
better fit; 1,722 scored sequences):

| Assignment | Score | Rank among the 999 random assignments |
|---|---|---|
| No-language baseline | **−2.6233** | above all 999 |
| Dravidian | −2.8465 | 91.2nd percentile |
| Munda | −2.8616 | 87.6th percentile |
| Sanskrit | −3.1184 | 10.6th percentile |

Margin arithmetic, exactly as the frozen rules require it:
Dravidian − best rival = −2.8465 − (−2.6233) = **−0.2232**. The
bar was **+0.10**. The margin is not merely below the bar; it is
negative, because the leading rival is the baseline.

The 999 random assignments (seed 20261013): lowest −3.3415, mean
−2.9822, middle −2.9783, 99th percentile −2.7695, highest
−2.7215. **88 of the 999 random assignments scored above
Dravidian**, and the best random assignment (−2.7215) beats it
outright.

One fact is worth separating from the verdict, because the
historical claim was always stated as Dravidian against Sanskrit:
head-to-head, Dravidian (−2.8465) still finishes ahead of
Sanskrit (−3.1184), by 0.2719. That ordering survives the rerun.
What does not survive is the wider claim: against the full field
the frozen contract named — including Munda and, decisively, the
no-language baseline — Dravidian does not lead, and random
assignments of the same values do about as well.

Pre-registered sensitivity (Harappa's inscriptions removed; 1,649
scored sequences): baseline −2.6173, Dravidian −2.8415, Munda
−2.8518, Sanskrit −3.1109 — the same ordering. The sensitivity
carries no verdict consequence here, because the verdict was
already reached on the primary run; it is reported as run.
Limitation, recorded in advance: 1,940 of the 2,906 corpus records
carry no site label in the corpus as held, so the sensitivity
removes the 110 records labelled Harappa and keeps the rest as
held.

Robustness arm (each family's second list of five published
candidates, same arithmetic, reported beside the outcome and never
deciding it): Munda −2.6522, Sanskrit −2.6971, Dravidian −2.9876.
On their second lists the ordering differs and Dravidian finishes
last of the three. The Munda second list has four signs, not five:
no fifth Munda value could be cited from the published sources
reached, and the anchor freeze records that shortfall rather than
filling it.

A note on the arithmetic, because readers will ask how "no
values" can beat a real language family: in this model every
sound a value adds is one more estimated step, and the score is
divided by signs, not by sounds — so a value only helps if the
sound patterns it creates are markedly more predictable than the
sign patterns they replace. Under the frozen method, none of the
three families' values cleared even that baseline. This is a
property of the registered method, reported here so the result
can be understood; no part of the method was adjusted after the
numbers were seen, and none may be.

## How the run was made (the inspectable trail)

- Corpus: the program's Mahadevan-lineage corpus as held in the
  tracked primary corpus (`glossa-corpus/indus/exports/
  indus_research.jsonl`, SHA-256
  `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`;
  the records in the Mahadevan 1977 sign scheme, 2,906 records,
  11,507 sign tokens, 5,883 of them strict-set tokens — 51.13%).
  The frozen claim names "the V3 corpus as held in the database";
  the V3 loader's own external export file is not present on disk,
  and the corpus catalogue (`glossa-corpus/indus/CORPUS_VERSIONS.md`)
  records that the primary corpus already holds the same data in
  this form. That held form is what was scored; the choice and its
  reason are recorded here and in the anchor freeze.
- Strict set: 94 of 287 anchors, exactly as the Spec 029 Phase H
  record stamped them (`backend/reports/INDUS_FINAL_ANCHORS.json`,
  SHA-256
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
  at run time). Censuses were checked before scoring and matched
  the frozen counts exactly; any mismatch would have stopped the
  run.
- Anchors: the two lists in `anchors-phase397.json`, frozen in a
  merged pull request (PR #212) before the scoring script ran.
  Two caveats travel with them and are stated in the freeze: the
  Sanskrit values were taken from the program's extraction file
  of the published Sanskrit decipherment traditions (Yajnadevam
  2024; Rao 1982; the Sanskrit words anchored in Monier-Williams
  1899 and Apte 1957), a file that describes itself as a synthetic
  reconstruction built to give that tradition its best case; and
  the Munda values are the published Munda words for what each
  sign depicts (Santali *haku* "fish", *ak'* "bow", *bar* "two",
  Mundari *catu* "earthen waterpot"), because no sign-by-sign
  Munda decipherment proposal exists in the published record.
- No semantic anchoring, no anchor promotion, and no quantity
  derived from either appears anywhere in the run.

## What this verdict does NOT establish

Per the frozen design, a verdict in either direction was never
going to settle more than the bounded claim. This one does not
establish:

- that the Indus language was not Dravidian — only that these
  published Dravidian values, under this registered method, do not
  fit better than the named rivals and the no-language baseline;
- anything about the rebus method, for or against;
- anything about any single sign's reading;
- anything about decipherment, in either direction.

It is a within-lineage result: every corpus the program holds
descends from the Mahadevan compilation, so no independent-corpus
replication of this comparison exists.

## What remains not understood

This outcome is the checking stage, done at machine speed. The
result is negative and it is clean, but nobody yet understands,
in the human sense, *why* the no-language baseline wins by this
much: whether the counted model punishes exactly the structure a
real language would create, whether five anchor signs are simply
too few to carry a family's signal, or whether the strict corpus
itself is too damaged by uncertain sign identification for any
value assignment to show through. Those questions are now the
open residue of this claim, and they are stated here so the
verdict is never quoted as more than a check.

## Claim-status consequence (frozen section 6 / DD-03-3)

The verdict is NOT SUPPORTED, so the partial support the
Dravidian-solution claim (`parpola_2010_dravidian_solution_
manual_001`) inherited from the Phase-41/Phase-43 numbers is
replaced: a dated entry recording this outcome is appended to
that claim's record in this same change, and its status is
reclassified to **unsupported** (the claim store's standing token for a not-supported verdict) through that entry. The record also
carries the correction in the store's `status_correction` field
(the shape the Phase-104 correction established), so a future
regeneration of the claims store carries the corrected status
over instead of silently restoring the extraction status. The old
numbers (Phase-41 ratio 1.0566; Phase-43 +0.484 log units per
sign) stay in the claim's history, labelled as what they are:
results produced by a method the program later falsified. The
sibling fish-sign claim (`..._manual_002`) is a separate test
(design D-04), not touched by this outcome. The claim's stage is
not moved by this lane-1 result: it stands at `explained` on its
author's record, and the explanation text itself now describes a
support that this rerun has withdrawn — that tension is exactly
what the appended entry records.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution section VI.
