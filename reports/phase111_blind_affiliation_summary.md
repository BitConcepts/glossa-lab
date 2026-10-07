# Phase-111 — Blind Language-Affiliation Study: Results Summary

**Spec:** 009-phase111-blind-affiliation (frozen 2026-10-06, commit
ae472242, + pre-run Addendum A, commit 9ca1c94b) · **Results file:**
`reports/phase111_blind_affiliation_results.json` · **Acquisition
log:** `reports/phase111_acquisition_log.json`

**Verdict (spec §9 V6 vocabulary, verbatim):**

## `INVALID RUN — CONTROL VALIDITY FAILED`

The validation gate **passed perfectly**; the run then failed the
frozen control-validity rule (§8) at the classification stage. Under
§8 this invalidates the *run*, not the hypotheses: the study
produced **no admissible evidence about Indus language affiliation
in either direction**, and no family verdict of any kind is reported.

## Design recap

A blinded, pre-registered feature-classification study. A custodian
module built an anonymized panel (IDs C01–C16 only, seeded token
remapping); an analyst module — importing nothing from the
custodian — saw feature matrices (28 frozen features per draw:
positional, block-entropy curve, local repetition, vocabulary
growth, Markov predictability, Zipf–Mandelbrot, length) and the
known-corpus label map only. Draws: 100 per member at exactly
N = 11,000 tokens (sensitivity sizes 5,000 / 19,600, reported in
the results file, never verdict-bearing). Classifier: LDA with
shrinkage λ = 0.1, equal priors, frozen. Blinded items: the three
Indus replicates (R1 Holdat/Mahadevan, R2 ICIT/Wells, R3 pooled)
and the four synthetic controls (S1–S4). A frozen validation gate
had to pass on *known* corpora before any Indus classification;
frozen control validity (§8) had to hold under the final model
before any §9 verdict rule could fire.

## Gate outcome (frozen §7 thresholds)

| Test | Requirement | Observed | Pass |
|---|---|---|---|
| G1 linguistic balanced accuracy (test draws 50–99) | ≥ 0.85, bootstrap 95% CI lower bound > 0.70 | **1.000**, CI lower bound **1.000**, bootstrap p = 0.00050 | ✔ |
| G2 family balanced accuracy (7 family classes) | ≥ 0.70, permutation p < 0.001 (1,000 permutations) | **1.000**, p = 0.000999 | ✔ |

Per-family recall on held-out test draws: 1.000 for every family
(dravidian, indo_aryan, semitic, indo_european_other,
isolate_sumerian, turkic, austronesian). Benjamini–Hochberg
(q = 0.05): T1 and T2 significant after adjustment (adjusted
p = 0.0020 each).

## Control validity (§8) — where the run failed

Requirement: under the final model, each synthetic control S1–S4
must be classified non-linguistic (posterior mass on
`non_linguistic` + `gen_heraldic` + `gen_administrative` ≥ mass on
all family classes) in ≥ 95% of its draws.

| Control | What it is | Share of draws classified non-linguistic | Required |
|---|---|---|---|
| S1 permutation | R1 texts, within-text token order permuted (unigram counts, lengths, hapax, inventory preserved; sequential + positional structure destroyed) | **0.00** | ≥ 0.95 |
| S2 i.i.d. Zipf | fresh texts, tokens i.i.d. from R1's unigram distribution | **0.00** | ≥ 0.95 |
| S3 heraldic generator | R1 position-class (initial/final/medial) model, no sequential dependency | 1.00 | ≥ 0.95 |
| S4 administrative generator | R1 unigram restricted to 60 signs, template-closure motif | 1.00 | ≥ 0.95 |

Both Indus-derived nulls were placed in family space in **100%**
of draws. Recorded mechanism (analysis of the run, not a verdict):
the gate's attested non-linguistic class rested on the single
panel member that survived the registered gaps — khipu (N1,
vocabulary of 10 knot-type codes), a corpus trivially separable
from every linguistic member — so the validated decision boundary
never had to separate "linguistic-looking unigram profile" from
language; the two position-structured generators (S3/S4) were
caught by their own disclosed generator classes, but nothing in
the trained boundary rejected structureless draws carrying an
Indus unigram profile. §8 existed for exactly this case, and it
fired. The exceedance tests T3/T4 were computed (raw p = 0.0099
each, BH-significant) but under §8/§10 they carry **no verdict
weight** in an invalid run and are recorded in the results file
for audit only.

Per §6 (no re-runs) and §11, no feature, panel member, or
threshold was changed after unblinding, and the pipeline was not
re-run.

## Panel as assembled (counts as built; full record in the acquisition log)

Known (gate + training): K1 Linear B 43,646 tokens · K2 Vedic
Sanskrit 374,893 · K3 Classical Sanskrit (DCS) 22,298 · K4 Old
Tamil 17,414 · K5 Sumerian Ur III 1,920,042 (30,000-file cap
reached) · K7 Ge'ez 80,221 · K8 Turkish (UD-IMST, addendum-A
substitution) 125,818 · K9 Indonesian (UD-GSD, substitution)
251,339 · N1 khipu 110,151. Targets: R1 1,670 texts / 7,002
tokens / 390 signs · R2 4,410 / 14,213 / 713 · R3 6,080 /
21,215 / 1,103. Controls S1–S4 as frozen in §5; generator-training
instances disclosed per Addendum A item 5.

Registered gaps (frozen §1e + Addendum A, never scraped around):
K6 Akkadian (ORACC unreachable; `semitic` carried by Ge'ez
alone), N2 proto-cuneiform (no openly licensed sequence source;
attested non-linguistic panel = khipu alone), Elamite (no
verified open corpus; suffixing confound carried by Sumerian
alone), attested SCA heraldry (license unverified; S3
substitutes), Sproat anchor set (not acquired; outside the
verdict path). Power rule: every assembled corpus ≥ 5,000 clean
tokens (smallest K4, 17,414) — no corpus demoted.

## Unblinding record

Unblinded 2026-10-07T03:52:39.601141+00:00 (join of analyst
posteriors to the custodian key, performed by
`phase111_run.run_classify_stage`). Blind key: C02 = R1
Holdat/M77, C08 = R2 ICIT/Wells, C14 = R3 mixed, C04 = S2,
C05 = S1, C09 = S3, C15 = S4. Code state at run: git HEAD
`92cad2ab1d14f035d04a8f440e5f21cac7fb25a4` (the committed
pipeline — no code was modified to obtain these results);
module SHA-256 digests for custodian/features/analyst/run are
recorded in the results file (`code_hash`). Gate stage completed
2026-10-07T03:48:02Z per the results record.

## Limitations (registered §12, plus what this run exposed)

- All §12 limitations stand (representation-level heterogeneity,
  genre mismatch, chunked positional features, bootstrap-draw
  dependence, R2's source-reconstructed sign order, Elamite's
  absence, Holdat's A.13 verification caveat).
- This run's specific lesson, recorded for any successor spec:
  a gate whose non-linguistic class has exactly one attested
  member — and that member an extreme outlier (vocabulary 10) —
  cannot validate the boundary the verdict path actually needs.
  Control validity (§8) caught the failure, which is the protocol
  working as designed; but a future panel needs at least one
  attested non-linguistic corpus whose difficulty is comparable
  to the synthetic nulls, or generator/null classes represented
  inside the gate itself. Any such change is a new spec (§11),
  never a patch to this run.
- The §8 outcome invalidates this run's classification only. It
  is not evidence that the Indus system is or is not linguistic,
  and it touches no anchor, reading, or prior phase result.

## Licensing summary

Full record: `reports/phase111_acquisition_log.json`. Downloads
only under recorded licenses (DCS CC BY 4.0; CDLI-via-MTAAC CC0 /
CC BY-NC 4.0 local-only; UD treebanks CC BY-NC-SA / CC BY-SA
local-only; Open Khipu Repository MIT). Raw texts live only in
the gitignored store; committed artifacts are code, spec, logs,
and results — never source texts. R2 remains a restricted local
file, used locally only (PR #65 compliance). Never ingested:
ETCSL, Project Madurai, any Elamite edition.

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution §VI.
