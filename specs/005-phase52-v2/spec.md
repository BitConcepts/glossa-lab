# Spec 005 — Phase-52 v2: held-out validation, blind controls, constraint ablation, delta search, corpus pooling, metrology check

**Status:** Proposed 2026-10-05 on `feat/phase52-v2` (from main ad6de412).
Owner-approved execution of the six-step Phase-52 strengthening plan from
the 2026-10-05 research briefing (research sweep:
`~/workspace/research_notes/indus-decipherment-research-sweep-20261005-2342/`,
program analysis in its `notes/program-analysis.md`), plus the owner's
corpus-acquisition addition to Step 4. The strengthened run is ledgered as
**Phase-107** in the glossa-indus ledger sequence (the sequence that
reached Phase-106 on 2026-10-05).

**Phase-numbering note (read before objecting):** legacy script files from
an earlier era already occupy some numbers in this range
(`phase107_tb_name_check.py`, the `IndusTBNameCheck` node). Those files
are append-only history and are NOT renamed or reused here. This
package's Phase-107 is the ledger-sequence phase, exactly as Phase-106
(the Phase-52 re-run) was ledgered over the legacy
`phase106_name_sa_sprint.py`. All new artifacts carry distinct names
(`phase107_sa_*`) and new graph node IDs.

## Context (audit findings, 2026-10-05)

- Phase-52's objective is a syllabic bigram LM score ONLY
  (`backend/scripts/phase52_syllabic_sa.py`). The project's own validated
  constraints — Phase-58/61 phonotactics, Phase-61 vowel harmony,
  Phase-133 sign-position grammar — are not in the objective.
- The headline Phase-52 numbers are circular: the re-run (Phase-106)
  reported z = 17.642 and per-sign agreement 113/275 = 41.09% measured
  against anchors that include the 116 pinned signs the SA was forced to
  reproduce. No held-out estimate exists.
- A June-2026 blind test of a rival claim showed an identical SA protocol
  "reading" the corpus in four languages AND a scrambled non-lexicon.
  Phase-52 has never faced blind controls under its own protocol.
- The program is corpus-bound: Holdat = 1,670 seals / 7,002 tokens /
  390 signs, about a third of the field's known sign occurrences.
- SA cost is bounded by full rescoring every iteration
  (measured 2026-10-05: score_full ≈ 0.211 ms; the Phase-52 full config
  is 1.5M iterations ≈ 420 s).

## Pre-registered protocol (binding for Steps 1–5)

**Gold values.** For every HIGH/MEDIUM anchor sign, the gold syllabic
value is extracted by the Phase-52 pin procedure generalised to all H+M
readings: the hardcoded `HIGH_SYLLABIC` value where one exists, else the
reading's first segment (before `/`), lowercased, diacritics stripped
(`[^a-z]` removed, max 4 chars), mapped into the LM vocabulary exactly as
`load_anchors_as_pins` does (exact match, else first vocab entry with the
same 2-char prefix, else no gold). Extraction code is shared with the
baseline, not re-invented.

**Primary CV (Step 1a).** k = 5 folds, stratified by confidence,
deterministic fold seed 107, over the 116 Phase-52-pinnable anchors.
Per fold: pins = the other folds' gold values; SA runs the CURRENT
objective (LM only); held-out agreement = fraction of the fold's held-out
signs whose SA consensus value (majority across seed-best mappings,
Phase-52 style) equals gold. Report per-fold values, mean ± SD.
**Secondary metric:** agreement over the 159 H+M anchors the Phase-52
procedure never pins (held out by construction), same gold extraction,
reported with its evaluable n.

**Harness SA config (fixed for Steps 1, 2, 4):** 3 seeds (0, 1, 2) ×
5 restarts × 10,000 iterations, temp 1.0, cooling 0.9997 (Phase-52's
schedule), full rescoring. ~150K iterations ≈ 32 s per (fold, config).
Null model per (LM, corpus): 30 random permutations, Phase-52 method,
seed 42; z from the run's mean seed score.

**What counts as improvement / discrimination (falsifiers):**

- *Claim A — the SA generalises beyond its pins.* FALSIFIED if primary
  held-out agreement is not above the scrambled control's (Step 1c) by
  more than the pooled fold SD.
- *Claim B — the Dravidian LM is the discriminating target.* FALSIFIED
  if Sanskrit or Ge'ez held-out agreement ≥ Dravidian under the
  identical protocol.
- *Step 1c discrimination verdict:* "discriminating" iff Dravidian mean
  held-out agreement exceeds every control's mean by > 1 pooled SD;
  otherwise reported as non-discriminating on this protocol. z alone
  never counts as discrimination.
- *Claim C — a constraint term helps.* Ablation (Step 2), terms added
  ONE AT A TIME in the fixed order (i) phonotactic, (ii) vowel harmony,
  (iii) positional grammar. A term is KEPT iff mean held-out agreement
  improves ≥ +2.0 percentage points over the Step-1a baseline AND mean z
  does not fall by > 10% relative; otherwise DROPPED and reported with
  its numbers. The combined config (all kept terms) is also measured.
- *Claim D — delta scoring is equivalent (Step 3).* Same seeds/config,
  full vs delta: PASS iff |mean best-score difference| < 1% of the mean
  AND ≥ 95% of signs share the same consensus value; per-seed numbers
  reported either way.
- *Stability selection (Step 3):* scaled run 10 seeds × 10 restarts ×
  100,000 iterations with the kept-terms objective via delta scoring.
  "SA-supported" = consensus ≥ 0.80 across the 10 seed-best mappings;
  the ≥ 0.60 tier is also reported. No threshold is tuned post-hoc.
- *Claim E — pooling helps (Step 4).* FALSIFIED if the pooled-corpus
  primary held-out agreement < Holdat-only headline by more than the
  pooled fold SD.
- *Claim F — metrology consistency (Step 5):* per-constraint pass/fail
  with counts, constraints fixed below from in-repo artifacts.

**Constraint terms (Step 2), all reused from the phases' own code:**
- (i) Phonotactic: penalty λ=3.0 per inscription whose INITIAL sign's
  assigned syllable is an invalid Proto-Dravidian initial under
  `phase61_phonotactic.py:check_phonotactics` rules (initial ∈
  {b,d,f,g,q,w,x}, or single-consonant syllable). Phase-58's retroflex
  rule (`phase58_phonological_gap.py:is_valid_dravidian_initial`) is
  vacuous on the diacritic-stripped LM representation and is recorded
  as such, not silently dropped.
- (ii) Vowel harmony: penalty λ=3.0 per inscription containing both a
  front-vowel syllable (vowel ∈ i ī e ē) and a back-vowel syllable
  (u ū o ō) — Phase-61's sequence definition applied to SA syllables.
- (iii) Positional grammar: +1.0 × Σ_tokens log P(value | position
  class), position classes per Phase-133b (first sign = initial slot,
  last = terminal, else medial); P estimated per fold from TRAINING
  anchors' gold values over their corpus occurrences (add-1 smoothing).
  Held-out anchors contribute to neither pins nor profiles in their
  fold. λ rationale: 3.0 ≈ log-odds of the observed 87–94% compliance
  rates in Phases 58/61/133e.

**Step 5 constraints (fixed now, from in-repo artifacts):** numeral
subsystem = the stroke-sign family identified in
`backend/glossa_lab/data/indus_sign_crosswalk.py` sign notes
("Single vertical stroke", "Two vertical strokes", …) cross-checked
against `outputs/phase21d_numerical_weights.json` and
`outputs/phase203_falsify_metrological.json`.
- C1 Distinctness: stroke-numeral signs receive pairwise-distinct values
  under the strengthened SA consensus. Pass = all distinct.
- C2 Order: IF the SA values for stroke signs are Dravidian numeral
  syllables, their numeric order must be monotone in stroke count.
  If they are not numeral syllables, C2 = NOT APPLICABLE (reported,
  never counted as pass or fail).
- C3 Positional: stroke-sign tokens' inscription positions match the
  metrological pattern recorded in the phase203/phase21d artifacts
  (the exact pattern statement is copied verbatim into the Step-5
  script header before it runs). Pass/fail by the artifact's own rule.

## Steps

### Step 0 — This spec (H2). No code before it lands.

### Step 1 — Validation harness on the current objective
(a) Primary + secondary held-out metrics per the pre-registered
protocol. (b) Pin-count sweep on fold 0: budgets {0 (all-free), 53, 90,
all-available} with pin priority = HIGH_SYLLABIC pins first, then
MEDIUM pins by descending sign corpus frequency. (c) Blind controls,
identical protocol, same folds: (i) Sanskrit syllabic LM
(`sanskrit_syllable_lm.json`); (ii) Ge'ez syllabic LM built from the
in-repo Fuls Ge'ez Genesis syllabic corpus (Semitic, syllabic —
the in-repo NW Semitic assets are consonantal benchmark corpora, not
syllabic LMs; this substitution is recorded here, not hidden);
(iii) scrambled Dravidian LM (syllable labels permuted in the bigram
structure, fixed seed). Pins for a control = the fold's pins whose
syllable exists in the control LM's vocabulary (counts reported).
Held-out agreement for Ge'ez is structurally bounded by inventory
overlap; its z and cross-seed stability are reported alongside, with the
caveat printed in the artifact.

### Step 2 — Constraint ablation
Per the pre-registered order and keep rule. Terms implemented once in
the harness library with per-fold profile construction; each ablation
run uses the Step-1a protocol (same folds, seeds, harness config).

### Step 3 — Delta scoring + scaled run
Incremental scorer for the LM term and all kept constraint terms
(affected bigrams / inscriptions / rows only). Equivalence test per
Claim D. Then the scaled run + stability selection per protocol.

### Step 4 — Corpus pooling + acquisition hunt
(a) In-repo pooling: convert `indus_cisi_corpus.json` (179 inscriptions,
1,003 tokens, Parpola P-numbers) to M-numbers via crosswalk v2.1;
report conversion coverage (signs and tokens), inscription overlap with
Holdat (dedupe rule stated before pooling), pooled token total.
(b) Acquisition hunt (owner addition, 2026-10-05): systematically
search for public Indus corpora not yet ingested, checking against
CITATIONS.md first (no re-fetch of ingested sources). Candidates:
RMRL Mahadevan concordance online release; ICIT (Fuls) public forms;
CISI/CISID public subsets; CDLI Indus/Meluhha material beyond in-repo;
Harappa.com datasets; Wells sign-list resources; public code-hosting
repos with Indus corpora/sign lists; Zenodo/Figshare/OSF datasets;
datasets released with the 2025 conferences or Dixit et al. 2025;
Dilmun/Gulf seal corpora. Public download links only — nothing behind
access controls or terms prohibiting download. Each obtained corpus:
ingested as a separately-flagged layer under `corpora/downloads/`
(gitignored per repo convention) + a CITATIONS.md entry; token/sign
counts reported. Each candidate NOT obtained: exact blocker recorded
(paywall / form-only / no download / license / not found).
(c) Where pooling is legitimate (same numbering or crosswalk-
convertible, deduped), re-run the Step-1a primary metric on the
enlarged pool with the best objective from Steps 2–3. The Tamil Nadu
graffiti database, if obtained, is a COMPARATIVE layer only — never
pooled into the Indus training corpus.

### Step 5 — Numerals/metrology validation
Run the strengthened SA's consensus mapping against C1–C3 on the
numeral/metrological subsystem. Pass/fail per constraint with counts.

### Step 6 — Registration + close-out (H15/H23/H21)
1. Scripts written (Steps 1–5) under `backend/scripts/phase107_sa_*.py`
   BEFORE first execution, per H23 ordering with the graph module.
2. Graph module `backend/glossa_lab/experiment_graph_phase107.py`
   (single-phase module, per the phase126/phase127 precedent) with
   AtomicNodeDef nodes per script; registered in `experiment_graph.py`
   via try/except import; registration verified in ATOMIC_NODES
   BEFORE the scripts' first run.
3. Full backend test suite (exact counts; baseline 564 passed /
   9 skipped), ruff on changed Python files, foundation check
   (baseline 40/0/8; must show 0 failures — H21).
4. Ledger: `glossa-indus/LEDGER.md` Phase-107 entries per step +
   root `LEDGER.md` summary, AI disclosure in each (H1, constitution
   §II/§VI).
5. Push branch; open PR to main via `gh pr create`. NOT merged —
   owner reviews scientific results.

## Assumptions (H13 epistemic boundaries)

- The anchor set itself is a hypothesis, not ground truth: held-out
  agreement measures the SA's consistency with the anchor programme,
  not with the (unknown) historical reality. Adversarial case: if the
  anchors are systematically wrong, high held-out agreement certifies
  only internal coherence. This is stated wherever the metric is
  reported.
- Gold extraction inherits Phase-52's normalisation losses
  (diacritic stripping, first-syllable truncation, 2-char prefix vocab
  fallback). A held-out "miss" can be an extraction artefact; the
  evaluable-n is reported per fold so the metric's denominator is
  never hidden.
- Control LMs differ in inventory size and corpus size from the
  Dravidian LM; z-scores are therefore compared only within-LM
  (each against its own null), and cross-LM claims rest on held-out
  agreement + stability, not raw z.
- GPU: this VM has no CUDA GPU and torch is not installed (foundation
  NEW-G warns). All scripts follow the established Phase-52/106
  pattern: torch import guarded, `gpu_device` recorded in every
  artifact, CPU warning printed — never a silent fallback (H20).
- Pooled CISI material may transcribe some of the same physical seals
  as Holdat. Pooling without dedupe would double-count evidence; the
  dedupe rule is fixed in Step 4 before any pooled run.
- New phase result files land in `reports/` (Phase-52/57 pattern);
  H21 foundation check must show 0 failures before the close-out
  commit is pushed.

## Out of scope

- ANY change to anchor readings, confidences, or
  `INDUS_FINAL_ANCHORS.json`. SA output is evidence, never applied.
- Merging the PR (owner review gate).
- Re-adjudication of claims; changes to the Phase-52 script itself
  (it stays as the historical baseline; v2 lives in the harness +
  phase107 scripts).
- Scraping anything behind access controls; email or outreach (H14).
