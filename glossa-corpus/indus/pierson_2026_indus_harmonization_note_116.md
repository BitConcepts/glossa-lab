# Two standard Indus compilations encode position incommensurably: a pre-registered harmonization null (Holdat vs ICIT)

**Tristen Pierson** (BitConcepts LLC) — ORCID 0009-0003-7269-956X

Methods note, 2026-10-07. Prepared as a candidate addendum to the
program's preprint record (Zenodo concept record DOI
10.5281/zenodo.20379070; current published version v4.1.0, DOI
10.5281/zenodo.23219644). Program provenance registry: OSF
[osf.io/ybd65](https://osf.io/ybd65/). Code, frozen spec, and
machine-readable results: BitConcepts/glossa-lab (spec 015;
`reports/phase116_harmonization_results.json`). This note reports
a null result exactly as recorded. The study behind it was
diagnostic only: it changed no decipherment anchor, issued no
validation verdict, and all 44 anchors it concerned remain
`pending_non_sa_validation`. Nothing in it is evidence that any
particular reading of any Indus sign is right or wrong; it is a
result about the two compilations, not about the script.

## Abstract

Two widely used machine-readable compilations of the Indus
corpus — Holdat (Mahadevan numbering) and the ICIT corpus
(Wells numbering), the latter in a converted layer built from
the openly licensed field-cady lineage — were found, in the
course of a pre-registered validation study (Phase-115), to
disagree about the positional behaviour of the strict core of a
decipherment hypothesis so strongly that no cross-corpus
validation gate built on the pair could function: of 51
strict-core signs the cross-corpus test could judge, 43 failed,
40 of them on modal-position disagreement, at a median total
variation distance of 0.789474. Phase-116 (spec 015,
pre-registered and frozen before any results) asked why, under
five frozen hypotheses. Two were refuted. The disagreement is
not concentrated in crosswalk-risky signs (top-5 TV share
0.1492; top-10 share 0.2956, below the frozen diffuseness bar),
so it is not a sign-mapping error (H-MAPPING refuted). And it
is not an artifact of the coarse three-class positional scheme:
under continuous relative-position measurement the two
compilations' per-sign mean positions are essentially
uncorrelated (Spearman ρ = −0.0826), with median
Wasserstein-1 displacement 0.451927 and 43 of 51 judged signs
disagreeing beyond token-level sampling noise
(Benjamini–Hochberg q = 0.05), so the displacement is genuine
(H-DEFINITION refuted). The remaining three hypotheses —
corpus composition, segmentation conventions, and reading
direction — could not be resolved at the frozen power, for a
reason that is itself a finding: the two compilations share no
artifact key, and content matching recovers only 13
mutually-unique identical-text pairs between them (against 135
direct-compatible and 240 reversed-compatible candidate pairs
before uniqueness). The study's mechanically assembled
recommendation is R-NONE: no harmonization transformation is
justified, and cross-corpus positional validation between these
two compilations is not viable under any convention alignment
tested. Anyone pooling or cross-validating positional
statistics across Holdat and ICIT should treat the pair as
incommensurable until the unresolved mechanisms are
characterized.

## 1. The motivating anomaly (Phase-115, spec 014)

Phases 113 and 115 built non-simulated-annealing validation
batteries for 44 decipherment anchors whose only support was
the SA lineage falsified in Phase-107. Each battery had to pass
frozen calibration gates — validate at least 57 of the 94-sign
strict SA-independent core (STRICT94), and validate at most 5
of a 113-sign known-bad cohort — before it was permitted to
judge the 44. Neither battery passed calibration, so neither
judged them.

Phase-115's battery v2 repaired the first battery's data
starvation (an expanded ICIT converted layer: 4,531 kept
inscriptions, 13,492 mapped tokens, token-map coverage
excluding placeholders 0.91554) and rebuilt the cross-corpus
leg, T1, with attestation floors scaled to each sign's measured
opportunity to be attested. STRICT94 then validated 1/94
against the frozen gate of ≥ 57, and the battery was rejected
at calibration. The T1 leg itself is the anomaly this note
concerns. T1 could judge 51 of the 94 strict-core signs. Of
those 51, 8 passed and 43 failed; 40 of the failures were
modal-position-class disagreements (the sign's most frequent
position class — initial, medial, or terminal — differs between
the compilations) and only 3 were same-modal failures. The
median total variation distance over the failures was
0.789474, the mean TV over all judged signs 0.657011, and the
full-layer modal agreement was 0.2157. Phase-115 also bounded
pure initial↔terminal swap failures at 8 of 43, so a simple
reading-direction flip could not be the whole story. Before any
successor battery could be designed, the disagreement itself
had to be explained: compilation conventions, conversion error,
measurement definition — or something in how the two traditions
transcribe the same objects.

## 2. Design (spec 015)

Spec 015 (`specs/015-phase116-corpus-harmonization`) was frozen
in its own commit (0b626308) before any result existed. The
study is diagnostic only, by construction: it computes no
anchor verdicts and changes no anchor.

**Layers.** Holdat working layer: 1,670 inscriptions, 7,002
tokens (Mahadevan numbering). ICIT v2 converted layer (Wells
numbering, converted through the in-repo crosswalks): 4,531
kept inscriptions, 13,492 mapped tokens, 2,388 sentinel
(wildcard) tokens, token-map coverage excluding placeholders
0.91554.

**The intersection problem.** The frozen design's core test
restricts both layers to the *same* inscriptions. That
presupposes a shared artifact key, and there is none: Holdat's
`cisi_number` is Holdat-internal, while ICIT's `cisi` field is
CISI numbering — a naive key intersection is empty. Identity
was therefore established by a content matcher over the
pre-dedupe ICIT matcher population (4,614 inscriptions) against
the 1,670 Holdat inscriptions, with frozen tiers: Tier A
(direct sequence identity, mutually unique), Tier B (reversed
sequence identity, mutually unique), Tier C (containment,
mutually unique). Ambiguous-orientation candidates were
excluded from A/B by rule.

**Hypotheses and arms.** Five hypotheses, each with a frozen
statistic, frozen thresholds, and a frozen verdict mapping
(spec §5): H-COMPOSITION (the layers compile different
populations; paired test on the restricted layers), H-SEGMENTATION
(text-boundary conventions differ; arms S1 sentinel-stripping,
S2 artifact-units vs row-units, S3 length profiles), H-MAPPING
(residual M77↔Wells crosswalk error concentrated in risky
signs; concentration shares and a chain-heavy vs clean group
contrast, with a full audit table of the top-10 TV signs),
H-DIRECTION (orientation conventions differ; arms D1 matcher
orientation shares, D2 a global flip applied to one layer), and
H-DEFINITION (the three-class binning manufactures the
disagreement; continuous relative-position statistics and a
five-bin scheme). A token-level permutation context with
Benjamini–Hochberg control at q = 0.05 accompanies the verdicts.

## 3. The matcher yield is a finding in itself

The matcher returned: **Tier A 13 pairs, Tier B 17 pairs,
Tier C 1 pair**, with 0 ambiguous-orientation pairs. Before the
mutual-uniqueness requirement, the candidate pool held 135
direct-compatible pairs against **240 reversed-compatible**
pairs, and 14,456 containment candidates collapsed to a single
mutually-unique pair. The 13 Tier A pairs are short (by length:
five of length 2, two of length 3, four of length 4, two of
length 5).

Two compilations of substantially the same excavated corpus
thus share almost no mutually-unique identical texts under
content matching, and among raw compatible pairs the reversed
orientation is the majority. Every intersection-based arm of
the study inherits this scarcity: the paired tests were
designed against a frozen power gate of 100 pairs (composition)
or 50 pairs (direction), and the material supplies 13 and 30.
That scarcity — not any statistic computed on the pairs — is
what leaves three of the five hypotheses unresolved, and it
constrains every future cross-compilation design on this pair:
there is no large set of agreed identical texts to calibrate
against.

## 4. Baseline integrity

Before any arm ran, the Phase-115 result was recomputed under
assertion and reproduced exactly: T1 v2 judged 51 (8 PASS / 43
FAIL), 40 modal-disagreement failures, median TV over failures
0.789474, mean TV over judged 0.657011, full-layer modal
agreement 0.2157. The keyed ICIT layer's kept subset reproduces
the Phase-115 v2 layer byte-for-byte in sequence content and
order (4,531 inscriptions; 13,492 mapped tokens; 2,388
sentinels), consistent with its recorded hash (sha256
f837a15a…). The conversion audit recomputed all 16,141
matcher-population tokens from their stored source codes with
zero mismatches. The disagreement reported below is therefore
not the pipeline disagreeing with itself, and not an artifact
introduced by the Phase-115 layer expansion: it is a property
of the two compilations as converted by crosswalks that audit
clean.

## 5. Verdicts

| Hypothesis | Verdict | Headline numbers |
|---|---|---|
| H-COMPOSITION | **UNRESOLVED** (power) | 13 Tier A pairs vs the frozen 100-pair gate; on the 3 qualifying signs the restriction agrees perfectly (A 1.0, TV 0.0) — at n = 3, licenses nothing |
| H-SEGMENTATION | **UNRESOLVED** | arm S1 REFUTED (sentinel stripping: failures 43 → 45); arm S2 underpowered (artifact-units TV 0.1042 vs row-units 0.0917) |
| H-MAPPING | **REFUTED** | top-5 TV share 0.1492; top-10 share 0.2956 (frozen diffuseness bar ≤ 0.40); chain-heavy group 3 signs vs 46 clean |
| H-DIRECTION | **UNRESOLVED** | D1 underpowered (30 pairs vs the frozen 50); reversed share 0.5667; D2 global flip: modal agreement 0.2157 → 0.3137 (+0.098), inside the frozen unresolved band |
| H-DEFINITION | **REFUTED** | median W1 0.451927; material-displacement share 0.6863; 5-bin modal agreement 0.1373; Spearman ρ = −0.0826; 43/51 signs beyond sampling noise at BH q = 0.05 |

**H-COMPOSITION — UNRESOLVED (power).** The frozen power gate
requires |M| ≥ 100 pairs and |J51R| ≥ 15 qualifying signs; the
material gives |M| = 13 pairs and |J51R| = 3 signs (M059, M089,
M328). On those three signs the restricted layers agree
perfectly (A_restr 1.0, TV_restr 0.0, against paired full-layer
A 0.6667 and TV 0.33), and the permutation context finds 0 of 3
significant on the restriction — the direction the hypothesis
predicts, at a sample size the frozen rules state licenses no
conclusion. Descriptively, the layers do sample different
populations (site mix, string-normalized: Mohenjo-daro Holdat
share 0.3619 vs ICIT 0.4378; Harappa 0.2969 vs 0.3695), but
descriptive difference is not a verdict.

**H-SEGMENTATION — UNRESOLVED, with its cleanest mechanism
refuted.** Arm S1 tested whether sentinel (wildcard) positions
manufacture the disagreement — the ICIT layer carries a
leading-sentinel rate of 0.1284, and the median demoted-initial
share over the judged signs is 0.1667. Stripping sentinel
positions made the T1 failures *worse*, 43 → 45: arm S1 is
REFUTED, and with it the sentinel-geometry explanation. Arm S2
compares artifact-level units against row-level units on the
matched material: 4 qualifying signs, artifact-units TV 0.1042
vs row-units TV 0.0917 — no repair, and under the frozen
15-sign power gate the arm is UNRESOLVED. The S3 length
profiles record how different the two layers' text populations
look (Holdat: mean length 4.1928, share of texts of length ≤ 2
is 0.1611; ICIT: mean 3.5047, share ≤ 2 is 0.4392), but the
hypothesis as frozen — segmentation conventions as the
mechanism — is neither established nor excluded.

**H-MAPPING — REFUTED.** If residual crosswalk error caused
the disagreement, the disagreement mass would concentrate in
the signs whose conversions are risky (chained or ambiguous
mappings). It does not: the top-5 signs carry 0.1492 of the
total TV mass and the top-10 carry 0.2956, below the frozen
diffuseness bar of 0.40. The chain-heavy group contains only 3
signs (M030, M076, M124) against 46 clean signs, so the frozen
group-size clause voided the group-contrast component
(descriptive Δ mean TV = 0.0598) and the verdict is REFUTED on
diffuseness, exactly as the spec's rule prescribes. The full
audit table of the top-10 TV signs is in the results file;
their conversions are direct, with chain share 0.0.

**H-DIRECTION — UNRESOLVED.** Arm D1 is underpowered on its
face: Tier A ∪ Tier B gives 30 pairs against the frozen
50-pair gate. Among them the reversed share is 0.5667 — below
the 0.60 bar the spec sets for SUPPORTED, and at this n only
suggestive. Arm D2 applies a global orientation flip to one
layer: full-layer modal agreement rises from 0.2157 to 0.3137
(+0.098), which the frozen band records as UNRESOLVED — a flip
helps at most marginally and is contributory at most, not the
primary mechanism (consistent with Phase-115's bound of 8
pure-swap failures out of 43).

**H-DEFINITION — REFUTED, decisively.** The surviving
benign explanation was that the coarse three-class scheme
(initial/medial/terminal) manufactures the disagreement. The
continuous statistics say otherwise. Median per-sign
Wasserstein-1 displacement of relative position is 0.451927
(frozen REFUTED bar: ≥ 0.20). The material-displacement share
— the share of judged signs with W1 > 0.20 — is 0.6863
(REFUTED bar: ≥ 0.50). Five-bin modal agreement is 0.1373,
*lower* than the three-class 0.2157. And the per-sign mean
relative positions in the two compilations are essentially
uncorrelated: Spearman ρ = −0.0826. The token-level permutation
context agrees: 43 of 51 judged signs disagree beyond sampling
noise on the full layers (Benjamini–Hochberg q = 0.05). The
positional displacement is genuine under every measurement
definition tested; it is not a binning artifact.

## 6. Recommendation (R-NONE, verbatim)

The spec (§6) assembles the recommendation mechanically from
the verdicts; the study's recorded recommendation is:

> R-NONE: No harmonization transformation is justified by this
> study. Cross-corpus positional validation between Holdat and
> the ICIT converted layer is not viable on this pair of
> compilations under any convention alignment tested. A future
> validation battery must not use a conjunctive cross-corpus
> positional gate on this pair; validation must proceed within
> a single compilation or await a genuinely independent corpus.

What a future validation battery may and may not assume,
recorded with the recommendation:

- MAY NOT assume the anchors' validation status changed: this
  study is diagnostic only and all 44 anchors remain
  `pending_non_sa_validation`.
- MAY NOT assume the disagreement is crosswalk error: it is not
  concentrated in crosswalk-risky signs.
- MAY NOT assume the disagreement is a binning artifact:
  genuine positional displacement survives continuous
  relative-position measurement.
- UNRESOLVED (no assumption licensed either way): segmentation,
  composition, direction.

## 7. Implications for cross-use of the two compilations

This null is not only about one decipherment program's
validation battery. Holdat and ICIT are the two standard
machine-readable forms of the Indus corpus, and positional
statistics — which signs begin texts, which end them, which
sit medially — are among the most-cited quantitative results
in Indus studies. The present result bears on any work that:

- **pools** the two compilations into one positional analysis
  (the pooled distribution is a mixture of two incommensurable
  encodings, in proportions set by corpus sizes, not by the
  archaeology);
- **validates** a result obtained in one compilation against
  the other (a failure to replicate across the pair is, on this
  evidence, uninformative in both directions — agreement would
  be equally hard to interpret);
- **compares** positional profiles across publications that
  used different compilations (an apparent substantive
  disagreement may be a compilation difference; the two most
  natural benign explanations — crosswalk error and class
  definition — are the two this study refuted).

What the unresolved verdicts mean in practice is restraint, not
license: composition, segmentation, and direction differences
may yet explain part or all of the displacement, but this
study could not power those tests because the pair shares too
few agreed identical texts, and no convention alignment among
those tested (sentinel handling, unit redefinition, global
flip, re-binning) repairs the disagreement. Positional claims
should be stated per compilation, with the compilation named,
until a harmonization that *is* justified exists — or until a
genuinely independent corpus (the program is pursuing two:
the Roja Muthiah Research Library's Indus Research Centre
materials, and the image-derived transcriptions of Dixit et
al. 2025) allows the question to be asked of data that does not
share either compilation's conventions.

## 8. Limitations

Registered in spec §8 and carried into the results: identity
between the layers is textual, not artifactual — the matcher
cannot certify that two matched rows describe the same physical
object, only the same sign sequence; sentinel wildcard asymmetry
(15.0% of kept ICIT positions are sentinels); the token-level
permutation context ignores inscription clustering, so its
significance counts are optimistic about independence; site-mix
matching is string-normalized only; and the semantics of ICIT's
`dir.` labels were never assumed. Above all: the intersection
material is 13 + 17 + 1 pairs, and every paired conclusion in
this note is bounded by that scarcity. The refuted hypotheses
were refuted on the full layers (n = 51 judged signs), not on
the intersection, and stand at full strength; the unresolved
hypotheses are unresolved because the decisive test is the one
the material cannot power.

## 9. Data, licensing, and reproducibility

The ICIT-derived converted layer is a restricted local file,
used in local computation only and never committed; no source
texts appear in any committed artifact. Committed artifacts
are the frozen spec (spec 015, freeze commit 0b626308), the
analysis code, the machine-readable results
(`reports/phase116_harmonization_results.json`), and the human
summary (`reports/phase116_harmonization_summary.md`), merged
to the repository's main branch in PR #72. The study registered
its H23 graph node (`IndusPhase116Harmonization`) before the
run; verification (full backend suite; foundation check) is
recorded in the phase ledger entries and the PR body. Deviations
from the frozen spec: none (`deviations: []` in the results
file); interpretive choices made in execution (Tier C
strict-length-inequality reading; Tier A partner preference in
multi-partner artifact groups; retention of per-token source
codes in the keyed layer beyond the spec's field list, required
by the conversion audit) are disclosed in the PR body.

## 10. AI disclosure

This study was designed for execution by, and was executed by,
an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per the repository constitution §VI. The spec
freeze (git commit order as pre-registration proof), the frozen
verdict rules, and the mechanically assembled recommendation
were the controls substituting for a human firewall: the
executing agent had no discretion to soften a verdict, and the
three UNRESOLVED outcomes are reported as unresolved rather
than narrated toward a conclusion. This note was likewise
drafted by an AI agent under the same direction; every number
in it is taken from the results file cited above, checked
against it verbatim.

## References

- Pierson, T. (2026). *A Computational Decipherment Hypothesis
  for the Indus Script* (v4.0.0). Zenodo.
  DOI 10.5281/zenodo.23187630. Concept record:
  DOI 10.5281/zenodo.20379070.
- Pierson, T. (2026). Methods note (Phases 111–112): positional-
  bigram mimicry bounds blind affiliation classification
  (v4.1.0). Zenodo. DOI 10.5281/zenodo.23219644.
- Glossa-Lab program provenance registry. OSF.
  https://osf.io/ybd65/ (literature: zbh86; corpora: dfrhz;
  outputs: vwa7s).
- Spec 015 — Phase-116 corpus-harmonization study
  (pre-registration, frozen 2026-10-07, commit 0b626308).
  BitConcepts/glossa-lab, `specs/015-phase116-corpus-harmonization/`.
- Phase-116 results:
  `reports/phase116_harmonization_results.json`; summary:
  `reports/phase116_harmonization_summary.md`. Merged in PR #72.
- Spec 014 — Phase-115 non-SA validation battery v2; results:
  `reports/phase115_nonsa44v2_summary.md` (the motivating
  anomaly: STRICT94 validated 1/94 at the frozen ≥ 57 gate;
  T1 leg 51 judged / 43 FAIL / median TV over failures
  0.789474).
- Spec 011 — Phase-113 non-SA validation battery (v1);
  summary: `reports/phase113_nonsa44_summary.md`.
- Methods note (Phases 111–112), in-repo:
  `glossa-corpus/indus/pierson_2026_indus_methods_note_111_112.md`.
- Dixit et al. (2025). Computational approaches to the Indus
  script. *Journal of Computer Applications in Archaeology*.
  DOI 10.5334/jcaa.175. (Independent-corpus prospect; no data
  deposit accompanies the article.)
