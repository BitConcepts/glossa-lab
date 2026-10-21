# Spec 053 / Phase-413 — Outcome record (EXECUTED 2026-10-21 — STRICT CORPUS NOT PINNABLE, gate 0.3)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 053 contract
> (freeze digest
> `fd2d5cb86b6aed51882a945719bb747ac34f149b08a21e6485b1407c6dc6b309`,
> PR #257 merged at `8e7c58cc`), as **Phase-413**,
> in Wave 3 Group 2 of the runnable-experiments
> campaign (plan approved AS WRITTEN on
> 2026-10-21). The execution gate was satisfied
> before the run: OSF registration **s9yfe** is
> APPROVED + PUBLIC (parent-verified at
> dispatch). Arm A only ran; arm B is
> trigger-armed and did not join (campaign
> decision E-3). Outcome: **STRICT CORPUS NOT
> PINNABLE** — gate 0.3 (strict corpus
> identification and pin) failed on observed
> values. Gates 0.1 and 0.2 passed. No system
> was fitted, no control count was entered, no
> strength label is added, and the claim stands
> exactly as recorded.

## Headline (spec §6 wording, STRICT CORPUS NOT PINNABLE form)

"Spec 053 closed at step 0, gate 0.3: the
V3 / Mahadevan-lineage corpus layer of record
could not be uniquely identified and pinned as
the Phase-43 framework's corpus (the V3 layer's
data file — the Firestore 'indusarrays' dump
the V3 loader reads — is absent from the tree,
so the loader loads zero sequences and the
layer cannot be exported or pinned; no database
copy exists in the execution tree; and no other
layer in the tree is the corpus the Phase-43
record names (its source at 3,916 records,
against 5,679 records for the site-attributed
layer, 15,508 mixed-source objects for the V1
export, and 3,085 ICIT-encoded sequences)). No
fit was computed. This closure is a statement
about runnability, not about the claim; the
claim stands exactly as recorded."

Claim: `yadav_2009_arxiv_manual_001` —
strongly supported, stage explained, recorded
Zipf exponent about 1.35, unchanged. Its record
was not edited and no dated append was made to
it: a step-0 closure adds no strength label
(spec §6). The §9 headline quantities that a
completed run would carry — the pinned corpus
digest and census, the frozen control tables,
the per-system fit errors and gaps, the
positive-control condition's outcome, and the
sensitivities S1–S3 — do not exist under this
spec, and this record says so rather than
supplying substitutes. The fence sentence is
carried as §9 requires: "This result is a
strength label for a recorded curve fit. It is
not evidence that the script encodes language,
and it changes no verdict." This closure adds
no label; the sentence is restated so no reader
can mistake the closure for one.

## 1. What was executed

Step 0 only (spec §3, gates in frozen order),
under the graph-first build (H15/H23):
experiment script
`backend/scripts/phase413_yadav_zipf_controls.py`;
graph module
`backend/glossa_lab/experiment_graph_phase413.py`
(node `IndusPhase413YadavZipfControls`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`, 487 nodes total).
The script contains the one estimator of record
(spec §4.2, specified completely at the freeze
under DD-053-11) and the step-0 gate machinery;
it contains no control table — no count is
typed into a script (H16) — and the primary-fit
and sensitivity stages do not exist in it,
because a gate 0.3 failure closes the execution
before any of those can run, by the frozen
design. The run's own records:
`reports/phase413_results.json` (SHA-256
`98ccd10a96088a01657786320a7376264587eacf7d799b3e0145d8ec5ed970c7`)
and `reports/phase413_step0_report.md` (SHA-256
`e0edac40c410943b37dbf9fe67584b5c000bbfb4136102c539fc63d100b8c69f`)
— both digests derived twice by independent
routes (`sha256sum` and a Python `hashlib`
recomputation, identical), and the script is
deterministic: a second run reproduced both
output files byte-identically. The run's base
was `main` at
`3200b7b5b6841a7b9567a81368bf84004fd17255`.
Foundation check (H21) at the run, on this
checkout with the two gitignored Holdat CSVs
copied from the existing local downloads
(corpus CSV SHA-256 `62d14d2b…` verified
first): **40 passed / 0 failed / 8 warnings**
— the standing figure.

## 2. Step 0, gate by gate

- **0.1 Input integrity — PASS.** Every §2
  input that carries a pin recomputes to its
  freeze value: the claim file `90476623…`
  (13,230 bytes), the anchors file `df0cf620…`
  (570,344 bytes; census re-read: 287 anchors,
  94 `strict_sa_independent`), the crosswalk
  `4ace1a61…`, the Mahadevan–Parpola crosswalk
  `9ebd7723…`, and the Phase-43 results file
  `78a6c219…`. Each pin was verified in the
  foreground by two independent routes — the
  working-tree files and the git blobs at the
  run's base commit — with identical results,
  and again by the phase machinery in the
  worktree. The Phase-43 file was re-read in
  the same pass: it contains no occurrence of
  the word "Zipf" and no Mandelbrot parameter,
  exactly as the freeze recorded (DD-053-11).
  No Phase-43 estimator was sought or
  substituted at any point in this execution.
- **0.2 Estimator self-test — PASS.** The
  §4.2 estimator, implemented once in the
  phase script, was run on the frozen planted
  distribution (α = 1.20, q = 2.0, V = 200,
  N = 50,000, seed 20261021; counts drawn by
  the multinomial procedure stated in the
  script: probabilities proportional to
  1/(r+q)^α, one multinomial sample with
  numpy's default generator at the frozen
  seed). Drawn counts: sum 50,000, minimum 24,
  maximum 5,549, no zero-count types. The fit
  recovered **α = 1.256** (error 0.056 against
  the ±0.10 tolerance) and **q = 2.72** (error
  0.72 against the ±1.0 tolerance), with
  SSE 0.5635, NRMSE_log 0.05308, and log-space
  R² 0.9975. The machinery the comparison
  would have used first recovered the
  parameters it planted; the closure below is
  not an estimator failure.
- **0.3 Strict corpus identification and pin —
  FAIL (the execution closes here).** The gate
  requires the V3 / Mahadevan-lineage layer to
  be identified from the database as the layer
  the Phase-43 framework ran on, exported in
  full, and pinned by digest. The attempt was
  mechanical, in four parts, and every part is
  in the run's record:
  - **C1 — the V3 layer itself is absent.**
    The V3 corpus has exactly one loader of
    record (`backend/glossa_lab/data/indus_corpus_v3.py`),
    and it reads one data file:
    `glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl`
    — the Firestore 'indusarrays' dump. That
    file does not exist in the tree (the whole
    `sources/` subtree is untracked, per
    `glossa-corpus/.gitignore`), and it does
    not exist in the programme's main checkout
    on this machine either (its `sources/rmrl/`
    directory holds only its bulletin and
    provenance files). Run against this tree,
    the loader loads **zero** sequences: by its
    own code a missing file yields an empty
    record list. A layer that cannot be loaded
    cannot be exported whole or pinned.
  - **C2 — no database copy exists to identify
    it from.** The execution tree holds no
    database at all (`backend/data/` is not
    tracked). The programme's main-checkout
    database, inspected read-only at this
    execution, holds nine text corpora and no
    V3 Indus corpus among them — its only
    Indus text is the synthetic "Indus Script
    (synthetic, Yadav 2010 / Fuls 2014)"
    corpus, which is not the V3 layer and was
    not substituted for it.
  - **C3 — what the layer would have to be.**
    The pinned Phase-43 record (§T1_1) names
    its corpus exactly: source "indusscript.in
    Firestore 'indusarrays' (2026-05-14)",
    3,916 records, 3,137 sequences, 2,665
    dockeys, 12,494 sign instances. That is
    the identification standard gate 0.3
    sets, and no candidate below meets it.
  - **C4 — no other layer in the tree is that
    corpus.** The site-attributed layer
    (`yajnadevam_inscriptions.csv`, SHA-256
    `c02e3d7b…`) carries 5,679 records and is
    a different layer of record (the Phase-393
    layer; the layer Specs 027/028/042/045 pin
    for their own contracts — Spec 045's
    record established from its own side that
    this layer is not the corpus the Phase-43
    quantities belong to). The V1 research
    export (`indus_research.jsonl`) carries
    15,508 objects across five source systems
    in mixed sign schemes (PennMuseum 7,515;
    MetOpenAccess 4,904; indusscript-m77
    2,906; mayig-cisi 179; ClevelandArt 4) and
    is labelled V1 in the corpus versioning
    record — a multi-source export, not the
    V3 reconstruction. The ICIT-format export
    carries 3,085 ICIT-encoded sequences, a
    different lineage and encoding. The Holdat
    downloads path is absent from the tree,
    and the Holdat compilation is in any case
    the distinct second compilation of the
    sibling specs, not the Mahadevan-lineage
    V3 layer. No subset rule, reconstruction,
    or substitute layer was invented to stand
    in for the missing one.
  Gate 0.3 therefore fails as written: the
  layer cannot be uniquely identified in any
  store this run can reach, cannot be exported
  whole, and cannot be pinned. This is the
  same absence the freeze-stage records of
  Specs 049 and 052 and the execution record
  of Spec 045 established for the Phase-43
  corpus from their own sides; this record
  re-derived it first-hand against Spec 053's
  own frozen gate and borrows none of their
  verdicts.
- **0.4 Control set freeze — NOT REACHED.** No
  control count was entered for any system
  (N1, N2, N3, P1), and no judgement about the
  control set's enterability is recorded or
  implied by this closure: the gate was never
  run, because the frozen order puts the
  corpus pin first.
- **0.5 Census and floors — NOT REACHED.** No
  strict census exists (there is no pinned
  corpus to census), so the frozen floors
  (50 types, 2,000 tokens) were never applied
  and no TOO THIN judgement is recorded or
  implied.

## 3. What does not exist, stated plainly

No strict-corpus pin or digest; no frozen
control tables; no fit of any system (the
gate 0.2 self-test fit on synthetic data is a
gate quantity, prescribed by the frozen gate
order itself — it is not a fit of the Indus
corpus or of any control, and no separability
quantity derives from it); no positive-control
evaluation (§4.4 was never reached); no
sensitivities S1, S2, or S3 (in particular, no
full-inventory exponent exists to set beside
the recorded about 1.35); and no strength
label. The claim
`yadav_2009_arxiv_manual_001` stands exactly
as recorded — strongly supported, stage
explained — and its record was not edited.
Arm B did not join and nothing in this record
designs, registers, or pre-registers it
(campaign E-3; spec §12). Anchors asserted
byte-identical before and after (`df0cf620…`
at both readings).

## 4. What this closure does and does not establish

What was proven: the frozen pins hold (gate
0.1); the estimator the freeze specified is
implementable as written and recovers planted
parameters within its frozen tolerances (gate
0.2); and the strict corpus this spec's
primary stands on is not pinnable from the
records and stores the programme holds in
this tree (gate 0.3). What was not
established: anything about whether the Indus
fit is separable from non-linguistic systems,
anything about Yadav's recorded exponent,
and anything about whether the script encodes
language. The unblocking act is a records
act, not a re-scope: the Firestore
'indusarrays' dump (or another uniquely
identified, exportable copy of the V3 layer,
pinned as a record of record) entering the
programme's tracked stores, after which this
spec's frozen gates could be run as written
under a new execution order; any change to
the gate itself would be an amendment for the
owner, queued outside this pass.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
