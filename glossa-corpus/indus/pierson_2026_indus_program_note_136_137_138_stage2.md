# Indus Program Note — Spec 024 Stage 2: Context Association Tests (Phases 136–138)

**Tristen Kyle Pierson / BitConcepts LLC** · 2026-10-09
**Release:** Glossa-Lab v4.8.0 · **Repository:**
github.com/BitConcepts/glossa-lab · **Anchors:**
`INDUS_FINAL_ANCHORS.json` sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`
(287 anchors; unchanged by this program)

**AI disclosure:** the work recorded here was
executed by AI agents (Muse Spark, via Muse) at
the direction of the author, per the project
constitution §VI. All quantities are computed by
script from the data files and are reproducible
from the repository at the commits named below.

---

## 1. What this note reports

Spec 024 (evidence integration) ties the Indus
inscriptions to non-textual evidence —
archaeological context, object type, site — under
a strict fence: associations describe **use, not
meaning**; no result obtainable under this spec
can mint, promote, demote, or validate any sign
reading, change any anchor's status, or move the
registered predictions PRED-2026-001/002/003 in
either direction. Stage 0 (Phase-133, v4.6.0)
inventoried the context fields, audited the join
keys, and graded every field's provenance. Stage 1
(Phases 134–135, v4.7.0) found the motif-coding arm
unreliable on this pipeline and it was closed as
run. This note reports **Stage 2**: the three
remaining arms — (a) terminal-class × object type,
(c) site repertoire differentiation, and (d) a
descriptive graffiti protocol — each designed,
frozen, and executed under spec §5's
pre-registration discipline, with one declared
test family and one Benjamini–Hochberg correction.

Design freezes (each merged before its arm's code
ran): PR #117 (`stage2a-freeze.md`, incl. the
family declaration), PR #118 (`stage2c-freeze.md`),
PR #119 (`stage2d-freeze.md`). Executions:
Phase-136 (PR #121), Phase-137 (PR #122),
Phase-138 (PR #120, corrective PR #123). Combined
report:
`reports/phase136_137_138_stage2_report.md`.

## 2. The family and its verdicts

All confirmatory tests form one declared family;
Benjamini–Hochberg FDR control at q = 0.05 was
applied once, across all three raw p-values, in
the combined report. Each test is a permutation
test (B = 9,999, seed 20261009) against a
composition-controlled null; no asymptotic
p-values are reported.

| Member | Test | Raw p | BH q | Verdict |
|---|---|---:|---:|---|
| F1 | Terminal-class × object type, within-site stratified (ICIT-lineage layer) | 0.0001 | 0.00015 | SUPPORTED |
| F2 | Site repertoire differentiation (Holdat layer) | 0.7354 | 0.7354 | NOT SUPPORTED |
| F3 | Site repertoire differentiation (ICIT-lineage layer) | 0.0001 | 0.00015 | SUPPORTED |

Both p = 0.0001 values are the minimum the frozen
formula returns at B = 9,999 (0 permutations
reached the observed statistic).

## 3. F1 — Closing-sign class differs between seals and tablets (ICIT-lineage layer)

On the ICIT-lineage layer's catalogue-joined
subset (2,062 inscriptions in the three eligible
site strata, of 5,679 layer rows; 49.0% of the
layer is unjoinable under the audited key), the
terminal sign of a seal inscription falls in the
frozen TERMINAL class (spec 018) markedly more
often than a tablet's, within sites: observed
shares — Mohenjo-daro 30.0% vs 16.4%, Harappa
24.6% vs 10.5%, Kalibangan 12.5% vs 9.1%; pooled
28.1% vs 12.5%. CMH statistic 47.0047 (null median
0.455); Mantel–Haenszel common odds ratio **2.384**
(95% CI 1.847–3.077). The within-site control
attenuates the crude association (OR 2.748) but
does not remove it.

*Labels and limits:* this layer is an ICIT-lineage
derivative — not an independent witness — and the
result is reported with that label wherever it
appears. The strongest alternative explanation is
compilation-internal (transcription and object
typing within one scholarly tradition). The
finding is a fact about how the writing system was
deployed, as recorded in this layer: closing-sign
behaviour differs by object class. It is not a
PRED-2026 evaluation, and it says nothing about
what any sign means.

## 4. F2 / F3 — Site repertoires: a split outcome, reported by layer

**Holdat layer (F2): NOT SUPPORTED.** Across all
9 sites (1,670 inscriptions), the observed
repertoire divergence (χ² = 745.95) sits *below*
its composition-controlled permutation median
(770.32): raw p = 0.7354. Per the falsifier stated
in advance, per-site repertoire "dialects" in this
layer are recorded as an artifact of what each
site happens to preserve, not a finding.

**ICIT-lineage layer (F3): SUPPORTED.** Across 7
eligible sites (5,410 inscriptions), observed
χ² = 4,966.36 against a null median of 2,667.87:
raw p = 0.0001, Cramér's V 0.2190 — repertoires
differ beyond object-type and text-length
composition. Period, preservation, and excavation
history are not available in this layer and are
not controlled; that caveat travels with the
result.

The two outcomes are reported side by side and
their contrast is not itself a test: site
differentiation is **not** a layer-free fact. It
appears in one compilation's record beyond
composition controls and does not appear in
another's.

## 5. Arm (d) — The catalogue graffiti subset, described

417 catalogue photo rows over 395 distinct objects
(Vol. 1: 119/100; Vol. 2: 298/295). Objects by
site: Harappa 262, Lothal 44, Mohenjo-Daro 42,
Kalibangan 26 — a Harappa-centred distribution,
the reverse of the seal/tablet mass. 374 of 395
objects carry a single photographed side. The
editors' depiction-chapter field is filled on
**0 of 417** graffiti rows: the graffiti subset
carries no depiction coding in the catalogue at
all. No test was computed in this arm.

The Tamil Nadu graffiti corpus is not in hand
(0 records). Its material is separated from the
Indus material by ≥ 1,000 years on the published
rebuttal of the continuity claims; the Kodumanal
volume's graffiti discussion is qualitative in
this record (its printed tallies are internally
inconsistent and were used as no counts). No
overlap statistic against the seal-text repertoire
exists — no machine-readable sign-form repertoire
of the catalogue graffiti objects is in hand — and
no continuity, descent, or survival claim is made.

## 6. Process record

Phase-138's merging PR (#120) landed on a CI
readout that did not match its run's actual
conclusion: two pins in the phase's own test file
had failed (test code only; no descriptive
quantity was affected). The executing worker
caught the discrepancy against the run's API
record, corrected it in PR #123 with CI verified
green from the run's own conclusion and job log,
and the episode is recorded in the repository
ledgers and the combined report rather than left
in a PR thread. One Phase-137 CI run failed on the
same pin (a file that phase did not touch) and
proceeded only after the correction landed.

## 7. What this program does not claim

Nothing here decipheres anything. The strict core
of 94 readings at 73.68% coverage remains a
hypothesis; 44 anchors remain
`pending_non_sa_validation`; PRED-2026-001/002/003
remain PENDING for lack of a qualifying independent
corpus — unplayed, not lost and not won. Stage 2's
findings are Tier-(ii) knowledge in the spec's
terms: measured facts about how the writing system
was organized and used, labeled with the layers
they were measured on. Hypotheses they suggest are
hypothesis-grade and wait, like all others in this
program, for genuinely independent data and a
registered test.
