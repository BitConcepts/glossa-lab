# Positional-bigram mimicry bounds blind affiliation classification of the Indus script: two pre-registered null results

**Tristen Pierson** (BitConcepts LLC) — ORCID 0009-0003-7269-956X

Methods note, 2026-10-07. Prepared as a candidate addendum to the
program's preprint record (Zenodo DOI 10.5281/zenodo.23187630,
v4.0.0). Program provenance registry: OSF
[osf.io/ybd65](https://osf.io/ybd65/). Code, frozen specs, and
machine-readable results: BitConcepts/glossa-lab (specs 009 and
010; `reports/phase111_blind_affiliation_results.json`;
`reports/phase112_blind_affiliation_results.json`). This note
reports two null results exactly as recorded. Nothing in it is
evidence that the Indus script is, or is not, linguistic, and no
affiliation claim is made in either direction.

## Abstract

Can statistical feature classification, run blind, produce
admissible evidence about the language affiliation of an
undeciphered script? We pre-registered a two-stage protocol —
a validation gate on known corpora truncated to Indus
dimensions, followed by a conjunctive control-validity rule
that must hold before any verdict rule may fire — and ran it
twice on the Indus corpus. Both runs passed the validation gate
perfectly (balanced accuracy 1.000 on linguistic-vs-non-linguistic
and on seven-way family classification). Both runs then failed
control validity, for instructive and different reasons. In
Phase-111, a classifier using a general 28-feature vector placed
two structureless synthetic nulls built from the Indus unigram
profile in family space in 100% of draws: its power was carried
by unigram statistics. In Phase-112, with the feature set
restricted by a pre-registered audit to order-carrying
(permutation-sensitive) features only, those nulls were rejected
in every draw — but a new trap, a grammar-free generator
matching the Indus corpus's text lengths, unigram profile
(total variation 0.0419), and relative-position bigram
statistics by construction, was placed in family space in 100%
of draws. The pair of results bounds the evidentiary reach of
blind feature classification at current Indus corpus
dimensions: each mimicry level the protocol has been hardened
against defines the next. We record the design, both runs'
numbers, and the requirements a credible successor must meet.

## 1. Design

Both studies share one architecture (spec 009, inherited
unchanged by spec 010 except where §3 states the single change).

**Blinding.** A custodian module assembled an anonymized panel
(IDs C01–C16 in Phase-111) with seeded token remapping. An
analyst module — importing nothing from the custodian — saw only
feature matrices and the known-corpus label map. The Indus
material entered blind as three replicates: R1 (Holdat /
Mahadevan numbering; 1,670 texts / 7,002 tokens / 390 signs),
R2 (ICIT / Wells numbering; 4,410 / 14,213 / 713), R3 (pooled;
6,080 / 21,215 / 1,103).

**Panel (known corpora).** K1 Linear B (43,646 tokens), K2 Vedic
Sanskrit (374,893), K3 Classical Sanskrit / DCS (22,298), K4 Old
Tamil (17,414), K5 Sumerian Ur III (1,920,042), K7 Ge'ez
(80,221), K8 Turkish UD-IMST (125,818), K9 Indonesian UD-GSD
(251,339), N1 khipu (110,151; vocabulary of 10 knot-type codes).
Registered gaps, never scraped around: Akkadian (the `semitic`
class carried by Ge'ez alone), proto-cuneiform (no openly
licensed sequence source), Elamite (no verified open corpus;
the suffixing confound carried by Sumerian alone), attested SCA
heraldry (license unverified; a generator substituted).
Resampling: 100 draws per member at exactly N = 11,000 tokens;
sensitivity sizes 5,000 / 19,600 computed but never
verdict-bearing. Classifier: LDA with shrinkage λ = 0.1, equal
priors, frozen.

**Validation gate (spec §7).** Before any Indus classification,
the pipeline had to classify held-out draws of the *known*
corpora: G1 linguistic balanced accuracy ≥ 0.85 with bootstrap
95% CI lower bound > 0.70; G2 family balanced accuracy ≥ 0.70
with permutation p < 0.001 (1,000 permutations). Gate failure
stops the study as inconclusive.

**Control validity (spec §8).** Under the final model, every
synthetic control must be classified non-linguistic (posterior
mass on `non_linguistic` + `gen_heraldic` + `gen_administrative`
≥ mass on all family classes) in ≥ 95% of its draws. The rule is
conjunctive: one failing control invalidates the run, and no
verdict rule (§9: posterior ≥ 0.90, Bayes factor ≥ 10 against
the runner-up and against both generators, same winner under
both sign lists in ≥ 90% of draws) may fire. Multiplicity:
Benjamini–Hochberg at q = 0.05. No re-runs, no post-unblinding
changes (§6/§11 of both specs).

**Controls.** S1: R1 texts with within-text token order permuted
(unigram counts, lengths, hapax, inventory preserved; all
sequential and positional structure destroyed). S2: fresh texts
drawn i.i.d. from R1's unigram distribution. S3: a heraldic
generator (R1 position-class model, no sequential dependency).
S4: an administrative generator (R1 unigram restricted to 60
signs, template-closure motif). Phase-112 added S5 (§3).

## 2. Phase-111 (spec 009): the unigram bound

Spec frozen 2026-10-06 (commit ae472242; pre-run Addendum A,
9ca1c94b). Pipeline executed unmodified from git HEAD
92cad2ab1d14f035d04a8f440e5f21cac7fb25a4. Unblinded
2026-10-07T03:52:39.601141+00:00. The feature vector had 28
features (positional, block-entropy curve, local repetition,
vocabulary growth, Markov predictability, Zipf–Mandelbrot,
length).

**Gate: passed.**

| Test | Requirement | Observed |
|---|---|---|
| G1 linguistic balanced accuracy | ≥ 0.85, CI low > 0.70 | 1.000, CI lower bound 1.000, bootstrap p = 0.0004997501249375312 |
| G2 family balanced accuracy | ≥ 0.70, permutation p < 0.001 | 1.000, p = 0.000999000999000999 (1,000 permutations) |

Per-family recall on held-out test draws: 1.000 for every family
(dravidian, indo_aryan, semitic, indo_european_other,
isolate_sumerian, turkic, austronesian). Benjamini–Hochberg
(q = 0.05): T1 and T2 significant after adjustment (adjusted
p = 0.0020 each).

**Control validity: failed.**

| Control | Share of draws classified non-linguistic | Required |
|---|---:|---:|
| S1 permutation | 0.00 | ≥ 0.95 |
| S2 i.i.d. Zipf | 0.00 | ≥ 0.95 |
| S3 heraldic generator | 1.00 | ≥ 0.95 |
| S4 administrative generator | 1.00 | ≥ 0.95 |

**Verdict (verbatim): `INVALID RUN — CONTROL VALIDITY FAILED`.**

The two Indus-derived nulls sat in family space in 100% of
draws. The recorded mechanism is structural, not a tuning
failure: the gate's attested non-linguistic class rested on the
single panel member that survived the registered gaps — khipu,
a corpus with a 10-code vocabulary, trivially separable from
every linguistic member — so the validated boundary never had to
separate a linguistic-looking unigram profile from language.
The exceedance tests T3/T4 (raw p = 0.009900990099009901 each,
BH-significant) were computed but carry no verdict weight in an
invalid run; they are in the results file for audit only.

## 3. Phase-112 (spec 010): the positional-bigram bound

Spec frozen in commit 9410a23d, before any Phase-112 pipeline
output existed; pipeline executed unmodified from commit
7e2626cf527fb6b8621f072256f570a8bb0d6ae0. Unblinded
2026-10-07T16:02:08.334428+00:00. Exactly one design change
from Phase-111: **the classification feature set admits only
permutation-sensitive (order-carrying) features**, admitted by a
pre-registered audit on known corpora only (median |Cohen's d|
≥ 0.8 under within-text permutation, same sign in ≥ 8/9 corpora,
non-degenerate in ≥ 5/9, after a mechanical toy test). Of 23
candidates, **16 were admitted and 7 dropped**. Admitted
(median |d|): `cond_ent_gap` (60.007), `cond_ent` (40.242),
`bigram_type_ratio` (35.415), `blockH2` (34.157), `blockH3`
(25.119), `pp_ratio` (17.493), `blockH4` (12.387), `cond_ent2`
(12.276), `adj_clustering` (9.033), `ent_incr_43` (7.780),
`pp_ratio_tri` (7.641), `init_productivity` (6.257),
`term_productivity` (5.578), `restore_acc` (5.089), `rep_adj_1`
(4.566), `rep_adj_3` (2.348). Dropped: `init80_frac` (0.291),
`term80_frac` (0.339), `term_init_ratio` (0.116), `hend_first`
(0.421), `hend_last` (0.695), `rep_adj_2` (1.910), `fl_mi`
(1.280). One further trap was added: **S5, a positional-bigram
template generator** — a non-linguistic process with no grammar,
matching R1's text lengths exactly, its unigram profile to
total variation 0.0419, and its relative-position bigram
statistics by construction (as built: 13,057 texts / 55,002
tokens).

**Gate: passed**, with the same recorded values as Phase-111 —
G1 balanced accuracy 1.000 (CI lower bound 1.000, bootstrap
p = 0.0004997501249375312); G2 balanced accuracy 1.000
(permutation p = 0.000999000999000999); per-family recall 1.000
for all seven families. Order-carrying features alone separate
the known corpora perfectly at Indus size on held-out draws.

**Control validity: failed at S5.**

| Control | Share of draws classified non-linguistic | Phase-111 share |
|---|---:|---:|
| S1 permutation | 1.00 | 0.00 |
| S2 i.i.d. Zipf | 1.00 | 0.00 |
| S3 heraldic generator | 1.00 | 1.00 |
| S4 administrative generator | 1.00 | 1.00 |
| S5 positional-bigram template | 0.00 | — (new) |

**Verdict (verbatim): `INVALID RUN — CONTROL VALIDITY FAILED`.**

The design change did its work against the traps that killed
Phase-111: with unigram evidence excluded, destroyed-order
nulls (S1) and unigram resamples (S2) are rejected in every
draw. S5 caught what they could not. The admitted feature family
(block/conditional entropies to order 3, Markov perplexity
ratios to order 2, repetition structure, bigram type ratio,
adjacency clustering, boundary productivity) measures exactly
the statistics S5 reproduces by construction — local sequential
order up to relative-position bigrams. A positional template
process is therefore indistinguishable from genuine linguistic
order for this vector. Audit-only values (no verdict weight):
exceedance T3 vs gen_heraldic p = 0.0099, T4 vs
gen_administrative p = 0.0099, BH-adjusted T1–T4 all
significant at q = 0.05; at the sensitivity sizes the Indus
replicates' median linguistic posteriors are ~10⁻⁷ or smaller —
recorded solely as part of the frozen pipeline's complete
output, since an invalid run's classification values are not
evidence in either direction.

## 4. The mimicry ladder

The two runs are one result at two levels:

1. **Unigram mimicry (Phase-111).** A bag of signs carrying the
   Indus frequency profile is indistinguishable from language to
   a general feature classifier. Frequency profile, hapax ratio,
   inventory, and Zipf shape are not linguistic evidence.
2. **Positional-bigram mimicry (Phase-112).** A grammar-free
   template process carrying the Indus relative-position bigram
   statistics is indistinguishable from language to an
   order-carrying feature classifier. Local sequential order —
   the strongest internal structure the Indus corpus is known to
   have (cf. Yadav et al. 2010's beginner/ender asymmetry) — is
   not, at these dimensions, linguistic evidence either.

Both times, the pre-registered control-validity rule caught the
masquerade before any verdict issued. That is the protocol
working as designed, twice — and it is also the bound: a feature
family earns evidentiary standing only against nulls that
reproduce the statistics that family measures, and each such
null, once built, has so far been able to reproduce them.

## 5. What a credible successor requires

Recorded from the two runs' own limitation sections; each item
requires a new pre-registered spec, never a patch to these runs.

1. **Harder attested non-linguistic panel members, inside the
   gate.** Phase-111's gate validated its boundary against a
   single attested non-linguistic corpus of vocabulary 10. A
   credible design needs attested non-linguistic members whose
   difficulty is comparable to the synthetic nulls, or
   generator/null classes represented in gate training itself.
2. **Traps matched to the feature family, built adversarially.**
   Any new feature family creates a new mimicry surface
   (Phase-112's S5 was designed against Phase-111's lesson and
   caught Phase-112's). Successor traps must reproduce, by
   construction, the exact statistics the new features measure.
3. **Features beyond adjacent relative-position pairs** —
   longer-range dependencies, hierarchical constituency proxies
   — each with its own pre-registered permutation audit, since
   at ~7,000–21,000 tokens such statistics may simply be too
   sparse; a run that returns "indeterminate at this corpus
   size" is a measurement, not a failure.
4. **Independent data.** Classification evidence is bounded by
   the corpus it classifies. The program's frozen out-of-sample
   predictions (PRED-2026 series) against independent corpora
   remain the evidence class no internal mimicry result can
   substitute for.

## 6. Data, licensing, and reproducibility

Panel sources are openly licensed or in-repo (DCS CC BY 4.0;
CDLI via the MTAAC repository CC0 / CDLI data CC BY-NC 4.0,
local use only; UD treebanks CC BY-NC-SA / CC BY-SA, local use
only; Open Khipu Repository MIT). R2 (ICIT-derived) is a
restricted local file, used in local computation only and never
committed. Committed artifacts are code, specs, acquisition
logs, and results — never source texts. Full records:
`reports/phase111_acquisition_log.json`,
`reports/phase112_acquisition_log.json`. Both runs are merged
to the repository's main branch (PRs #66 and #67) with the
frozen specs, the results JSONs, and human summaries
(`reports/phase111_blind_affiliation_summary.md`,
`reports/phase112_blind_affiliation_summary.md`). Operational
disclosure for Phase-112 (two aborted panel-build attempts —
host contention and a VM reboot — producing no statistic of any
kind, and BLAS thread pinning as an environment-only mitigation)
is recorded in its summary and PR body.

## 7. AI disclosure

These studies were designed for execution by, and were executed
by, an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per the repository constitution §VI. The
blinding protocol existed for exactly this situation: the
executing agent was also the analyst, so the spec freeze (git
order as pre-registration proof), the custodian/analyst code
separation, and the no-re-run rules were the controls
substituting for a human firewall. This note was likewise
drafted by an AI agent under the same direction; every number in
it is taken from the merged results files cited above.

## References

- Pierson, T. (2026). *A Computational Decipherment Hypothesis
  for the Indus Script* (v4.0.0). Zenodo.
  DOI 10.5281/zenodo.23187630.
- Glossa-Lab program provenance registry. OSF.
  https://osf.io/ybd65/ (literature: zbh86; corpora: dfrhz;
  outputs: vwa7s).
- Spec 009 — Phase-111 blind language-affiliation study
  (pre-registration, frozen 2026-10-06) and Spec 010 —
  Phase-112 order-carrying successor (frozen 2026-10-07).
  BitConcepts/glossa-lab, `specs/`.
- Phase-111 results: `reports/phase111_blind_affiliation_results.json`;
  summary: `reports/phase111_blind_affiliation_summary.md`.
- Phase-112 results: `reports/phase112_blind_affiliation_results.json`;
  summary: `reports/phase112_blind_affiliation_summary.md`;
  feature audit: `reports/phase112_feature_audit.json`.
- Rao, R. P. N., et al. (2009). Entropies of the Indus script.
  *Science* 324: 1165.
- Yadav, N., et al. (2010). Statistical analysis of the Indus
  script using n-grams. *PLoS ONE* 5(3): e9506.
- Sproat, R. (2014). A statistical comparison of written
  language and nonlanguage. *Language* 90(2): 457–501.
- Rajan, K. & Sivanantham, R. (2025). *Indus Signs and Graffiti
  Marks of Tamil Nadu: A Morphological Study.* Tamil Nadu State
  Department of Archaeology. (Program context for the successor
  data path; not evidence used in either run.)
