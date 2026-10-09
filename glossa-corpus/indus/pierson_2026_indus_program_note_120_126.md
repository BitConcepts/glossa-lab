# Program note, Phases 120–126 and specs 019–020: new witnesses, a cross-compilation disagreement, and a non-qualifying evaluation source

**Tristen Pierson** (BitConcepts LLC) — ORCID 0009-0003-7269-956X

Program note, 2026-10-08. Prepared as an addendum to the program's
preprint record (Zenodo concept record DOI
10.5281/zenodo.20379070; previous published version v4.2.0, DOI
10.5281/zenodo.23223655). Program provenance registry: OSF
[osf.io/ybd65](https://osf.io/ybd65/). Code, frozen specs, and
machine-readable results: BitConcepts/glossa-lab (Phases 120–126;
specs 019 and 020; repository main at commit 9ef78ca6).

This note reports the outcomes of Phases 120–126 and specs 019–020
exactly as they stand in the merged reports, negatives included.
None of these phases changed any decipherment anchor: the anchors
file `backend/reports/INDUS_FINAL_ANCHORS.json` is byte-identical
across Phases 125, 126, and spec 020 (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed,
asserted in code in each phase). No phase in this note is evidence
that any particular reading of any Indus sign is right or wrong.

## Abstract

Seven phases and two adjudicative specs extended the program's
witness base and then tested it. Phase-120 triaged the 44 pending
anchors against Bhaskar (2024): 1 CONTESTED (M402), 43
NOT-COVERED, 0 ALL-AGREE — a descriptive triage that validates
nothing. Phase-121 extracted the Soviet positional dataset
(Kondratov 1965 Tables 1–4 and Proto-Indica 1973): 7 tables, 109
records, 36/36 hand-verified cells; the 1968 Formal Analysis
contains no frequency tables. Phase-122 built Parpola↔Mahadevan
crosswalk v1 (762 pairs; 372 high-confidence; the canonical
registry and the mayig features agree on 372/372 of those) and
integrated the mayig CISI corpus layer (179 inscriptions, 1,003
tokens, 768 of them clean). Phase-123 recorded the Wells
segmentation witness over 157 signs: SAME 87, SPLIT 40, MERGE 5,
NOT-COVERED 2, INDETERMINATE 23 (determinable for 134).
Phase-124 built the CISI image layer: 7,705 catalogue rows over
3,494 CISI object IDs, with 98.9% field accuracy on the checked
sample; the derived crops remain local-only under the volumes'
copyright. Phase-125 (spec 019) then ran the pre-registered
cross-compilation positional comparison between the mayig/CISI
and Holdat compilations, and it **failed**: verdict FAIL /
DISAGREEMENT — of 286 primary pairs only 16 were judgeable,
median total-variation distance 0.637 against a PASS bound of
≤ 0.35, Spearman ρ = −0.425 (initial) and 0.316 (terminal),
pairing-shuffle null p = 0.824. Anchor positional profiles do
not cross-validate between the mayig/CISI and Holdat
compilations at the frozen thresholds. Spec 020 adjudicated the
Phase-121 Soviet dataset as a candidate evaluation source for
the registered predictions PRED-2026-001/002 and returned
**NO**: five of six criteria fail and only independence passes,
so no scoring ran and PRED-2026-001/002 remain PENDING.
Phase-126 closed the sequence with a descriptive Wells-split
analysis of the 113 CANDIDATE anchors: split 27, merge 4,
unit-same 62, not-covered 1 (M312), indeterminate 19.

## 1. Phase-120 — Bhaskar (2024) triage of the 44 pending anchors

A descriptive triage of the 44 `pending_non_sa_validation`
anchors against Bhaskar (2024) and its supplementary materials.
The supplementary materials do not encode the per-sign
three-way disagreement table the commission assumed; the phase
therefore extracted every cross-source disagreement Bhaskar
actually documents (20 cases) and built a mention index instead
of fabricating a grid. Outcome, of the 44:

| Class | Count |
|---|---|
| ALL-AGREE | 0 |
| CONTESTED | 1 (M402) |
| NOT-COVERED | 43 (16 mentioned behaviourally, 27 not mentioned) |

The triage changes no anchor status, validates nothing, and
contains no prediction content. Report:
`reports/phase120_bhaskar_triage_44.md`.

## 2. Phase-121 — Soviet positional dataset

Extraction of the Soviet positional-statistical material:
Kondratov's 1965 preliminary report, Tables 1–4 (as translated
in Zide & Zvelebil 1976), and Proto-Indica 1973. The dataset
comprises 7 tables and 109 records, every record carrying its
source, printed page, and table coordinates; 36/36 cells in the
hand-verification sample match the printed page. The 1968 Brief
Report (Knorozov, "The Formal Analysis of the Proto-Indian
Texts") was searched in full: **it contains no frequency or
positional tables** — the tasking premise that it did is not
borne out by the volume. The dataset is descriptive only; no
prediction was scored against it and no anchor was validated by
it. Report: `reports/phase121_soviet_positional_dataset.md`.

## 3. Phase-122 — Parpola↔Mahadevan crosswalk v1 and the mayig CISI layer

Crosswalk v1 joins Parpola (P) and Mahadevan (M) sign numbers
from labelled sources, with the canonical sign registry as the
map of record: **762 mapping pairs** (plus 4 unmapped-P rows),
of which **372 are high-confidence** — attested by both the
canonical registry and the mayig features, which agree on
**372/372** of those pairs. The phase also integrated the mayig
corpus layer keyed to CISI objects: **179 inscriptions, 1,003
sign tokens, 182 distinct P signs**; of the 1,003 tokens, **768
are clean** (76.6%), 202 ambiguous, the remainder partial at
inscription level (42 inscriptions fully clean, 137 partial,
none empty). All 179 mayig objects are present in both the
Bhaskar ESM13 catalogue and the Phase-116 keyed ICIT layer.
Report: `reports/phase122_crosswalk_mayig.md`.

## 4. Phase-123 — Wells segmentation witness

A witness statement — not an adjudication — recording how
Wells's grapheme segmentation (1998 MA thesis; 2006 PhD thesis)
treats each of the program's 157 anchor signs (113 CANDIDATE
plus the 44 pending). Treatment was determinable for 134 of
157:

| Treatment | Count (of 157) |
|---|---|
| SAME | 87 |
| SPLIT | 40 |
| MERGE | 5 |
| NOT-COVERED | 2 |
| INDETERMINATE | 23 |

Twenty table rows were hand-checked against the thesis plates:
17 glyph-consistent, 2 partial, 1 discrepancy (M293), preserved
in the table rather than smoothed over. The memo makes no
recommendation to adopt Wells's segmentation and asserts no
implication for any anchor's status. Report:
`reports/phase123_wells_segmentation_witness.md`.

## 5. Phase-124 — CISI image layer

An enabling asset only: a structured catalogue of the CISI
photographic corpus (Vols. 1–2) and a documented sign-crop
pipeline. The catalogue holds **7,705 rows** (one per
photographed side) over **3,494 distinct CISI object IDs**.
Field accuracy on the hand-checked sample (36 rows, four pages)
was 87/88 field values, **98.9%**, reported as a sample figure.
The scans are in-copyright research copies: the catalogue
table, page renders, OCR checkpoints, and every crop image
live only in a gitignored local store; only pipeline code,
tests, this memo's counterpart in the repository, and a
counts-and-schema manifest are committed. The phase asserts
nothing about what any sign means. Report:
`reports/phase124_cisi_image_layer.md`.

## 6. Phase-125 (spec 019) — Cross-compilation positional comparison: FAIL / DISAGREEMENT

Spec 019 froze the design before any results: per-sign
positional profiles (initial/medial/terminal rates) computed
within the mayig/CISI compilation and within the Holdat
compilation separately — inscriptions never pooled — joined
only through the Phase-122 crosswalk v1. The primary arm is
the high-confidence unambiguous pair set (372 high pairs, 286
after the uniqueness rule), floor 8 tokens per sign per
compilation.

**Verdict: FAIL — DISAGREEMENT** (the spec §6.3 falsifier
pattern was met). Primary arm: **16 judgeable pairs of 286**;
median TV **0.637** (PASS bound ≤ 0.35; FAIL bound ≥ 0.50);
Spearman ρ initial **−0.425**, terminal **0.316** (PASS bound
≥ 0.50); pairing-shuffle null (B = 999) **p = 0.824** (PASS
requires ≤ 0.05). Both sensitivity arms return the same
pattern (arm B, all 762 pairs: 28 judgeable, median TV 0.637,
p = 0.737). The conclusion the frozen spec licenses is exactly
this: **anchor positional profiles do not cross-validate
between the mayig/CISI and Holdat compilations** — the pairing
carries no positional agreement beyond shuffled pairings at
these thresholds. The verdict does not identify which side
produces the disagreement, says nothing about any individual
sign's identity or reading, and is a statement about the
well-attested minority of pairs (16 judgeable of 286), never
about the script as a whole. The Phase-116 R-NONE result stands
untouched. No prediction verdict was issued and no anchor
status changed. Report:
`reports/phase125_cross_compilation_summary.md`; spec:
`specs/019-phase125-cross-compilation-positional/`.

## 7. Spec 020 — Soviet dataset adjudication for PRED-2026-001/002: NO

Spec 020 asked a narrower question: does the Phase-121 Soviet
positional dataset qualify as an evaluation source for the
registered predictions PRED-2026-001 and PRED-2026-002? The
six criteria were derived mechanically from the prediction
register and spec 018 and stated in the spec before any
application. Outcome: **NO — the dataset does not qualify.**
Five of the six criteria fail:

- C1, source-class membership / matrix qualification: FAIL
  (fits none of the six frozen source classes);
- C2, identity with the withheld data or a qualifying
  substitute: FAIL;
- C3, computability of the registered per-sign end/start
  rates: FAIL (0/14 TERMINAL end rates and 0/12 start rates
  computable from the aggregate tables);
- C4, applicability of the frozen deduplication protocol:
  FAIL (the dataset contains no inscription token sequences);
- C5, canonical sign-space mapping / harness ingestibility:
  FAIL (Marshall numbering; no frozen map; no adapter ingests
  aggregate tables);
- C6, independence from the derivation inputs: **PASS** — the
  only criterion that passes.

Scoring did not run. **PRED-2026-001 and PRED-2026-002 remain
PENDING**; an append-only adjudication note recording the
verdict and its reasons was added to the prediction register.
Spec: `specs/020-soviet-pred-adjudication/`.

## 8. Phase-126 — Wells-split analysis of the 113 CANDIDATE anchors

A descriptive design-input memo: how the Phase-123 Wells
witness treats each of the 113 CANDIDATE anchors, and how that
treatment distributes across the evidence features the anchors
file itself records. Of the 113:

| Wells treatment | Count |
|---|---|
| split | 27 |
| merge | 4 |
| unit-same | 62 |
| not-covered | 1 (M312) |
| indeterminate | 19 |

Wells treatment is determinable for 93 of the 113; the 27 split
signs are compound-suspects under Wells (20 split into 2
graphemes, 6 into 3, 1 into 5). The memo phrases no
adjudication of any sign's status, proposes no promotion or
demotion, and changes no anchor. Report:
`reports/phase126_wells_split_candidates.md`.

## 9. Non-claims

Nothing in Phases 120–126 or specs 019–020 changes the status
of any decipherment anchor, validates or refutes any individual
sign reading, or scores any registered prediction. The two
verdicts in this note are both negative and are reported at
exactly their frozen scope: positional profiles do not
cross-validate between the mayig/CISI and Holdat compilations
on the judgeable primary pairs (Phase-125), and the Soviet
positional dataset does not qualify as an evaluation source
for PRED-2026-001/002, which remain PENDING (spec 020). The
remaining phases are descriptive or enabling work whose counts
are reported as recorded.

## References

- Pierson, T. (2026). *A Computational Decipherment Hypothesis
  for the Indus Script* (v4.2.0). Zenodo.
  DOI 10.5281/zenodo.23223655. Concept record:
  DOI 10.5281/zenodo.20379070.
- Glossa-Lab program provenance registry. OSF.
  https://osf.io/ybd65/
- Phase reports and frozen specs, BitConcepts/glossa-lab,
  main at commit 9ef78ca6: `reports/phase120_bhaskar_triage_44.md`,
  `reports/phase121_soviet_positional_dataset.md`,
  `reports/phase122_crosswalk_mayig.md`,
  `reports/phase123_wells_segmentation_witness.md`,
  `reports/phase124_cisi_image_layer.md`,
  `reports/phase125_cross_compilation_summary.md`,
  `reports/phase126_wells_split_candidates.md`,
  `specs/019-phase125-cross-compilation-positional/`,
  `specs/020-soviet-pred-adjudication/`.

## AI disclosure

These studies were designed for execution by, and were
executed by, an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per the repository constitution
§VI. The spec freezes (git commit order as pre-registration
proof), the frozen verdict rules, and the anchors-file hash
assertions were the controls substituting for a human
firewall: the executing agents had no discretion to soften a
verdict, and the negative outcomes above — the Phase-125 FAIL /
DISAGREEMENT and the spec-020 NO — are reported as recorded
rather than narrated toward a conclusion. This note was
likewise drafted by an AI agent under the same direction;
every number in it is taken from the merged reports and specs
cited above.
