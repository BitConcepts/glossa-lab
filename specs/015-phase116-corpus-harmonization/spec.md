# Spec 015 — Phase-116: Corpus-Harmonization Study — Why Holdat and ICIT Positional Profiles Disagree (pre-registration)

**Status:** FROZEN 2026-10-07 on `phase/harmonization-study`
(from main `5d8f5d58`). Owner authorization: Tristen Pierson,
2026-10-07 ("Launch the corpus-harmonization study"). This spec
is committed alone, before any harmonization statistic exists
under it. Git order is the pre-registration proof.

**This study is DIAGNOSTIC ONLY.** It produces no anchor
changes, no validation verdicts on anchors, and no battery. The
anchors file is never opened for writing under this spec.

**Phase-numbering note:** ledger-sequence **Phase-116**.
Phase-113 (spec 011) and Phase-115 (spec 014, PR #70, unmerged
at this freeze) are the two rejected batteries this study
follows; Phase-114 (spec 012, adversarial blind affiliation) is
in flight in a separate worktree and is untouched by this
phase. Artifact names carry the phase number
(`phase116_build_keyed_layer`, `phase116_harmonization`,
`phase116_run`, graph node `IndusPhase116Harmonization`).

**AI disclosure:** this study is designed for execution by an AI
agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.

## Context — the question, and what is already established

Phase-113 (spec 011) and Phase-115 (spec 014) froze two non-SA
validation batteries for the 44 SA-lineage anchors and rejected
both at calibration. Phase-115 rebuilt the ICIT converted layer
(4,531 inscriptions / 13,492 mapped tokens / 91.554% token-map
coverage, builder reproducible, sha256 `f837a15a…`), scaled
T1's attestation floors to measured opportunity, and still
rejected: STRICT94 validated 1/94 (gate ≥ 57) while KUR113
passed (0/113 ≤ 5). The failure inverted between versions —
v1 could not attest the strict core; v2 attests it and finds
**cross-corpus positional disagreement**:

- T1 v2 judged **51** of the 94 strict signs (8 PASS, **43
  FAIL**); 40 failures are modal-position-class disagreement,
  median TV **0.789474** over the failures, mean TV 0.657011
  over the judged 51. Modal-pair decomposition of the 43
  (Holdat → ICIT): INITIAL→MEDIAL 18, INITIAL→TERMINAL 7,
  TERMINAL→MEDIAL 7, TERMINAL→INITIAL 1, MEDIAL→INITIAL 3,
  MEDIAL→TERMINAL 4, same-modal TV-only 3. A pure
  INITIAL↔TERMINAL reading-direction swap therefore accounts
  for at most 8 of 43 failures; the dominant pattern is
  Holdat-initial signs appearing medial-modal in the ICIT
  population.
- 25/94 strict signs have zero tokens in the v2 layer.
- T2/T3 were never the problem (tallies identical across both
  phases).

Phase-115's recorded conclusion: before any successor battery,
a pre-registered study must establish *why* Holdat and ICIT
positional profiles disagree. This is that study. Its question
is singular: **what mechanism(s) produce the disagreement —
the populations compiled, the text-unit/boundary conventions,
the sign crosswalk, the orientation conventions, or the
3-class positional definition itself?**

## 1. Pre-freeze diagnostics (schema/count level only; measured before this freeze)

The following are corpus-schema and identity facts, measured
read-only before this freeze to make the design below
operable. No per-sign positional statistic was computed before
this freeze beyond the published Phase-115 aggregates taken as
baseline assertions in §3.

- **There is no shared artifact key between the layers.**
  Holdat's `cisi_number` is Holdat-internal sequential
  numbering (site prefix + zero-padded serial: `M-0001`…
  `M-0606` for Mohenjo-daro; `seal_id`/`form` are likewise
  internal). The ICIT source's `cisi` column carries CISI
  artifact numbers (`M-1`…`M-2129`, `H-…`, site codes `Agr`,
  `Ad`, `Ns`, `Kd`, `Blk`, `Sktd`, …). Raw intersection of the
  two key sets is **0**; normalized (case/space/hyphen
  stripped) intersection is **0**. Identity between the layers
  can therefore only be established by inscription *content*
  in the shared M-sign space (the route frozen in §4).
- **ICIT source metadata** (per row, field-cady MIT mirror of
  the Lipi/ICIT export): `id`, `cisi`, `site` (77 distinct),
  `material` (Steatite 2,633 rows; Clay 960; Faience 619;
  Copper 264; `-` 973; …), `type`/`class`, `sides` (1: 3,822;
  2: 1,654; 3: 168; 4: 18; 5: 17), `dir.` (R/L 4,266; `-` 776;
  NR 386; L/R 215; T/B 16; BUS 10; SYM 8; R/l 2), `text`.
  5,679 rows; 4,075 distinct `cisi`; 661 rows with `cisi`
  missing/`-`; 865 `cisi` values carry > 1 row (multi-face /
  multi-text artifacts).
- **Holdat**: 1,670 artifacts / 7,002 sign rows (`letters` =
  M-sign ids, `position` = 0-based slot, grouped by
  `cisi_number` per the phase113 loader); `site` in full names
  (Mohenjo-daro 2,534 sign rows; Harappa 2,079; Lothal 507;
  Kalibangan 485; Dholavira 439; Chanhu-daro 310; …); the
  population is seals (form `seal_NNNN`) plus other inscribed
  objects under Holdat's own numbering.

## 2. Data (frozen)

- **Holdat keyed layer**: the `phase113_run.load_holdat_inscriptions`
  loader logic replicated with keys retained — dict from
  Holdat `cisi_number` to its token sequence (M-signs). 1,670
  inscriptions / 7,002 tokens (asserted).
- **ICIT keyed layer**: a rebuild of the spec 014 §2 conversion
  policy, replicated exactly (parse `\d{3}` codes in file
  order; normalize key `str(int(code))`; map via the canonical
  registry Wells→M direct, else Wells→Parpola→crosswalk-v2
  chain; placeholders `000`/`999` and unmapped codes emit the
  `UNK` sentinel; zero-mapped inscriptions dropped; Holdat
  wildcard dedupe; intra-layer exact dedupe), retaining per
  inscription: source row index, source `id`, `cisi`, `site`,
  `material`, `type`, `sides`, `dir.`, the emitted token
  sequence, the per-token conversion kind
  (direct/chain/placeholder/unmapped), and an `in_v2_layer`
  flag (kept vs dropped-by-Holdat-dedupe). Output:
  `corpora/downloads/icit_fieldcady/icit_converted_v2_keyed.json`
  (gitignored; statistics only are published).
  **Assertions (run time):** the kept subset reproduces the
  Phase-115 layer exactly — 4,531 inscriptions, 13,492 mapped
  tokens, 2,388 sentinel tokens, and the emitted sequences
  identical in order and content to the stored
  `icit_converted_v2.json`. The pre-Holdat-dedupe population
  (kept + Holdat-dedupe-dropped) is 4,614 inscriptions; the
  matcher of §4 runs on this population, because the v2 dedupe
  removed precisely the inscriptions that match Holdat best.
- **Profiles / modal class / TV**: `phase113_battery`
  conventions verbatim (position 0 of a multi-sign inscription
  is INITIAL, last position TERMINAL, everything else —
  including sole tokens — MEDIAL; modal ties break
  INITIAL > TERMINAL > MEDIAL; TV = ½Σ|Δshare|). STRICT94 set
  per `phase113_run.compute_sets` (asserted 94, disjoint from
  FLAGGED44).
- Sets and corpora are those of specs 011/014; no SA artifact,
  no anchor `basis` text, and no prior phase's per-sign verdict
  is an input to any statistic below (H26). The Phase-115 T1
  records are used only as the §3 baseline assertions.

## 3. Baseline (frozen recomputation + assertions)

T1 v2 (spec 014 §4 verbatim: layer sampling ratio `r`,
opportunity floors, stability guard) is recomputed over
STRICT94 from the §2 layers. The run **asserts** equality with
the published Phase-115 record: judged (PASS+FAIL) = **51**,
PASS = **8**, FAIL = **43**, modal-disagreement failures =
**40**, same-modal TV-only failures = **3**, median TV over
failures = **0.789474** (± 0.0005), mean TV over judged =
**0.657011** (± 0.0005). If any assertion fails, the run stops
and reports the discrepancy; no hypothesis test proceeds on an
unreproduced baseline.

Frozen notation for §5: **J51** = the 51 judged strict signs;
**A_full** = modal-class agreement share over J51 on the full
layers = 11/51 (8 PASS + 3 same-modal); **TV_full(s)** = the
baseline per-sign TV; downstream comparisons always use the
paired sign subset named in each arm.

## 4. The matched-text matcher (frozen)

Units: Holdat inscriptions (1,670) × ICIT pre-dedupe keyed
inscriptions (4,614). For a Holdat sequence `h` and an ICIT
sequence `i` (with sentinels):

- **Compatibility(h, i)**: `len(h) == len(i)`, the number of
  mapped (non-`UNK`) positions in `i` is ≥ 2, and at every
  position `i`'s token equals `h`'s token or is `UNK`.
- **Tier A (direct)**: Compatibility(h, i) holds, (h, i) is
  mutually unique (h is compatible with exactly one i and i
  with exactly one h, over the whole population), and the pair
  is not also compatible in reversed orientation.
- **Tier B (reversed)**: Compatibility(h, reverse(i)) holds
  under the same mutual-uniqueness rule, and the pair is not
  Tier A. A pair compatible in both orientations is
  **ambiguous-orientation**: excluded from A and B, counted.
- **Tier C (containment)**: not Tier A/B; `len ≥ 3` and ≥ 2
  mapped positions on the shorter side; one sequence is a
  contiguous subsequence of the other under position-wise
  wildcard compatibility (sentinels in the ICIT side wildcard;
  if the ICIT side is the container, its window must satisfy
  the same rule); the pairing is mutually unique (each side
  participates in exactly one Tier C pair).
- **MATCHED set M** = Tier A pairs. Restricted layers:
  Holdat|M and ICIT|M (each layer's own inscription units).
- **Matcher yield is a result, not an assumption.** The
  Phase-115 build guarantees ≥ 83 candidate direct matches
  exist before uniqueness filtering (the Holdat-dedupe drops).

**Identity is textual, not artifactual** (§8): a Tier A pair
establishes that the same sign text (up to sentinel wildcards)
occurs in both compilations. That is exactly what the
composition test needs — disagreement computed over identical
texts cannot be explained by which texts each compilation
includes.

## 5. Hypotheses (frozen statistics, thresholds, verdict rules)

Verdicts are per hypothesis: **SUPPORTED** / **REFUTED** /
**UNRESOLVED**, by the frozen rules only. BH discipline: the
only per-sign significance family in this study is the
permutation family of §5.0, Benjamini–Hochberg at q = 0.05;
all other statistics are aggregate (means, shares, counts)
with no per-sign significance claims.

### 5.0 Shared arm — permutation context (descriptive, no verdict)

For each sign in J51: pool its Holdat and ICIT tokens (full
layers), permute the corpus labels preserving counts
(`n_H`, `n_I`), statistic = TV of the two positional profiles,
1,999 permutations, PRNG `random.Random(116116)` (fixed seed;
deterministic). BH q = 0.05 over the 51 tests → count of
signs whose cross-corpus disagreement exceeds token-level
sampling noise, full layers; repeated on the restricted
layers over J51R (§5.1). Reported as context for H-COMPOSITION;
not a verdict input.

### 5.1 H-COMPOSITION — the layers compile different populations

**Core test (paired).** On the restricted layers, let
**J51R** = signs of J51 with ≥ 3 tokens in Holdat|M and ≥ 3
mapped tokens in ICIT|M. Compute modal agreement **A_restr**
and mean TV **TV_restr** over J51R, and the paired full-layer
values A_full(J51R), TV_full(J51R) on the same signs.

- **Power gate (frozen):** if |M| < 100 pairs or |J51R| < 15,
  the core test is UNDERPOWERED: H-COMPOSITION =
  **UNRESOLVED (power)**, the secondary arm is reported, and
  no composition conclusion is drawn either way.
- **SUPPORTED** iff A_restr ≥ 0.75 **and** TV_restr ≤ 0.50 ×
  TV_full(J51R) — disagreement collapses on identical texts.
- **REFUTED** iff A_restr ≤ A_full(J51R) + 0.05 **and**
  TV_restr ≥ 0.90 × TV_full(J51R) — disagreement persists at
  full strength on identical texts, so it lives in
  transcription/segmentation of the same objects, not in
  population mix.
- Otherwise **UNRESOLVED**.

**Secondary arm (descriptive).** Token-share site mix for both
layers over sites covering ≥ 1% of either layer's tokens
(site strings normalized: lowercase, hyphens/spaces stripped;
ICIT `site` field vs Holdat `site` field); ICIT material and
type/class mix; Holdat's seals-only construction recorded as
a composition fact. Reported regardless of verdict.

### 5.2 H-SEGMENTATION — text-unit and boundary conventions differ

**Arm S1 (sentinel geometry).** Recompute ICIT profiles over
**sentinel-stripped** sequences (remove `UNK` positions from
each kept-layer inscription; drop sequences that become
empty; classes taken on the stripped sequence). Recompute the
T1 judgment over STRICT94 with spec 014 §4 floors and counts
unchanged (n_I = mapped-token count, identical by
construction; only profiles change). F0 = 43 (baseline FAIL
count), F1 = FAIL count under stripped geometry.

- **SUPPORTED** iff F1 ≤ 21 (≥ 50% of failures repaired).
- **REFUTED** iff F1 ≥ 39 (< 10% repaired). Else UNRESOLVED.

**Arm S2 (unit convention, paired).** Take the Holdat
inscriptions participating in Tier A ∪ Tier C pairs. For each
such artifact's ICIT side, build the **artifact-unit**
sequence by concatenating, in source file order, all
pre-dedupe keyed inscriptions sharing its normalized `cisi`
key (rows with missing `cisi` are their own units). Compute
per-sign profiles from artifact-units vs from row-units over
this matched population, each against Holdat restricted to
the same artifacts; **J51U** = J51 signs with ≥ 3 tokens on
both sides under both unit conventions; TV_art and TV_row =
mean TV over J51U under artifact-units and row-units.

- **Power gate:** |J51U| < 15 → arm UNRESOLVED (power).
- **SUPPORTED** iff TV_art ≤ 0.60 × TV_row.
- **REFUTED** iff TV_art ≥ 0.95 × TV_row. Else UNRESOLVED.

**Arm S3 (descriptives).** Inscription-length distributions
(both layers, full and matched); leading-sentinel rate in the
v2 layer (share of kept inscriptions whose first token is
`UNK`); per-sign **demoted-initial share** for J51: of a
sign's ICIT tokens sitting at stripped-position 0 (initial
once sentinels are ignored), the share whose in-sequence
position is > 0 — median over J51 reported. Text-boundary
behavior of boundary signs under both geometries is
tabulated in the results JSON.

**H-SEGMENTATION verdict:** SUPPORTED iff S1 or S2 is
SUPPORTED; REFUTED iff both are REFUTED; else UNRESOLVED.

### 5.3 H-MAPPING — residual M77↔Wells crosswalk error, concentrated

Population J51; per-sign quantities from the keyed layer
(full kept layer):

- `chain_share(s)` = chain tokens / (direct + chain tokens).
- `codes(s)` = number of distinct normalized Wells codes
  emitting s (either path).
- `amb_share(s)` = share of s's tokens whose source Wells code
  is **registry-ambiguous**: the code appears in canonical
  registry rows pointing to more than one distinct M sign, or
  in a row whose `mahadevan_ids` is multi-valued.
- Concentration: shares of Σ_{J51} TV_full carried by the
  top-5 and top-10 signs (TV descending, ties by sign id).
- Group contrast: chain-heavy = {chain_share > 0.5, n_I ≥ 3};
  clean = {chain_share = 0, n_I ≥ 3}; Δ = mean TV(chain-heavy)
  − mean TV(clean).

- **SUPPORTED** iff top-10 share ≥ 0.60 **and** Δ ≥ 0.20 —
  disagreement is concentrated in few signs and those signs
  are the crosswalk-risky ones.
- **REFUTED** iff top-10 share ≤ 0.40 **and** Δ ≤ 0.05.
- If either group has < 5 signs, the Δ component is void and
  the verdict is **UNRESOLVED (group size)** unless the
  concentration component alone is ≤ 0.40 (then REFUTED on
  diffuseness) — recorded explicitly either way.
- Otherwise **UNRESOLVED**.

**Audit table (published in the results JSON):** for the
top-10 TV signs of J51: every Wells code emitting the sign,
with per-code token count, conversion kind, Parpola id where
the chain was used, and registry flags (multi-valued row,
ambiguous code). Sign-level crosswalk metadata only; no
corpus text.

### 5.4 H-DIRECTION — orientation conventions differ

Phase-115 bounds pure I↔T-swap failures at 8/43; these arms
refine per-object.

**Arm D1 (matcher orientation).** Among Tier A ∪ Tier B
pairs, reversed share = |B| / (|A| + |B|).

- **SUPPORTED** iff reversed share ≥ 0.60 (the layers store
  matched texts in opposite orientations as the norm).
- **REFUTED** iff reversed share ≤ 0.10. Else UNRESOLVED.
- If |A| + |B| < 50 pairs → arm UNRESOLVED (power).

**Arm D2 (global flip).** Recompute ICIT profiles over fully
reversed kept-layer sequences; modal agreement A_flip over
J51 (full layers, baseline sign set) vs A_full = 11/51.

- **SUPPORTED** iff A_flip − A_full ≥ 0.30 (a global flip
  repairs a third or more of the judged set).
- **REFUTED** iff A_flip − A_full ≤ 0.05. Else UNRESOLVED.

**H-DIRECTION verdict:** SUPPORTED iff D1 or D2 is SUPPORTED;
REFUTED iff both are REFUTED; else UNRESOLVED. (Registered
interpretation: D1 measures the storage orientation of
matched texts; D2 measures whether one global flip repairs
profiles. The `dir.` column's label semantics are *not*
assumed anywhere — orientation is tested empirically.)

### 5.5 H-DEFINITION — the 3-class binning manufactures disagreement

Geometry exactly as the baseline profiles (kept layer with
sentinels for ICIT; Holdat as loaded). For each token at
position `pos` in a sequence of length `len`: relative
position `r = pos / (len − 1)` if `len > 1`, else `r = 0.5`.

- Per sign in J51: empirical r-distributions per corpus;
  **W1** = exact 1-D Wasserstein-1 distance between them;
  mean r per corpus.
- Aggregates over J51: median W1; **material-displacement
  share** = share of J51 with W1 > 0.20; Spearman ρ (midranks)
  between the corpora over per-sign mean r.
- **5-bin arm:** bin `b = min(4, floor(5 × (pos + 0.5) /
  len))`; 5-bin profiles per corpus; TV5 per sign; modal-bin
  agreement share **A5** over J51.

- **SUPPORTED** iff median W1 ≤ 0.12 **and** material share
  ≤ 0.25 **and** A5 ≥ 0.70 — positional behavior agrees under
  continuous and finer-grained measurement; the disagreement
  is an artifact of the coarse 3-class modal gate.
- **REFUTED** iff median W1 ≥ 0.20 **or** material share
  ≥ 0.50 — genuine positional displacement survives
  redefinition.
- Otherwise **UNRESOLVED**.

## 6. Harmonization recommendation (frozen decision table)

The summary's recommendation is assembled **mechanically**
from the §5 verdicts, using these templates (measured numbers
inserted). No other recommendation text is permitted.

- **R-SEG1** (H-SEGMENTATION SUPPORTED via S1): "Before any
  cross-corpus positional comparison, strip sentinel (UNK)
  positions from converted-layer sequences and compute
  profiles on the compressed sequences; the spec-014 sentinel
  geometry is not harmonized with Holdat's convention."
- **R-SEG2** (via S2): "Convert ICIT inscription units to
  artifact units (concatenate same-`cisi` rows in source file
  order) before computing positional profiles."
- **R-COMP** (H-COMPOSITION SUPPORTED): "Restrict cross-corpus
  positional comparisons to the matched-text intersection
  (Tier A pairs, §4); full-population cross-corpus profiles
  are not comparable across these two compilations."
- **R-MAP** (H-MAPPING SUPPORTED): "Exclude the audit-table
  signs (§5.3) from any cross-corpus gate, or repair the
  listed crosswalk entries first; do not gate on chain-heavy
  or registry-ambiguous signs."
- **R-DIR** (H-DIRECTION SUPPORTED): "Reverse converted-layer
  sequences to Holdat's orientation convention before
  profiling (the orientation divergence is measured, §5.4)."
- **R-DEF** (H-DEFINITION SUPPORTED): "Replace the 3-class
  modal/TV gate with a continuous relative-position statistic
  (per-sign W1 / mean relative position); the 3-class modal
  gate manufactures disagreement on this corpus pair."
- **R-NONE** (no hypothesis SUPPORTED): "No harmonization
  transformation is justified by this study. Cross-corpus
  positional validation between Holdat and the ICIT converted
  layer is not viable on this pair of compilations under any
  convention alignment tested. A future validation battery
  must not use a conjunctive cross-corpus positional gate on
  this pair; validation must proceed within a single
  compilation or await a genuinely independent corpus."

The summary additionally prints, verbatim-assembled, the
**future-battery assumptions list**: one "MAY assume (after
the named transformation)" line per SUPPORTED hypothesis and
one "MAY NOT assume" line per REFUTED hypothesis (the
assumption named is the hypothesis's own premise), plus the
standing line: "MAY NOT assume the anchors' validation status
changed: this study is diagnostic only and all 44 anchors
remain `pending_non_sa_validation`."

## 7. Execution order (frozen)

1. This spec (+ plan/tasks) committed alone (pre-registration).
2. Keyed-layer builder `backend/scripts/phase116_build_keyed_layer.py`;
   build executed; §2 assertions verified (the stored v2
   layer reproduced exactly by the kept subset).
3. Implementation: `backend/glossa_lab/phase116_harmonization.py`
   (matcher, profiles, all §5 arms),
   `backend/glossa_lab/phase116_run.py` (baseline assertions,
   orchestration, reports), runner
   `backend/scripts/phase116_harmonization_study.py`; unit
   tests `backend/tests/test_phase116_harmonization.py`.
4. H23 gate, in order: script written → graph module
   `backend/glossa_lab/experiment_graph_phase116.py` (node
   `IndusPhase116Harmonization`) → registration in
   `experiment_graph.py` → registration asserted in
   `ATOMIC_NODES` by the unit tests → only then any run.
5. Run: baseline assertions (§3) → matcher (§4) → arms (§5) →
   verdicts → recommendation assembly (§6).
6. Reports: `reports/phase116_harmonization_results.json`,
   `reports/phase116_harmonization_summary.md`.
7. Full backend suite + foundation check (H21). Ruff clean
   before push.
8. Ledger entries (root `LEDGER.md` and
   `glossa-indus/LEDGER.md`, AI disclosure) and one PR. No
   merge without the owner's explicit say-so.

Determinism: builder, matcher, and all statistics are pure
counting, set membership, and sorting in file order; the only
PRNG use is the §5.0 permutation family under the frozen seed.
Re-running on the same inputs reproduces the reports
byte-identically except timestamps.

## 8. Limitations and epistemic boundaries (H13, registered at freeze)

- **Identity is textual, not artifactual.** Formulaic texts
  recur on distinct artifacts; a Tier A pair shows the same
  text in both compilations, not provably the same physical
  object. The composition test needs exactly this: profile
  disagreement over identical texts cannot be composition.
  Conversely, a SUPPORTED composition verdict means
  disagreement is carried by the *non-shared* texts; it does
  not identify which compilation's extra population is
  "wrong."
- **Wildcard asymmetry.** ICIT sentinels (2,388 of 15,880 kept
  positions, 15.0%) wildcard-match any Holdat token, so the
  matcher cannot detect ICIT-side sign misidentification at
  sentinel positions, and short formulaic sequences can match
  spuriously; mutual uniqueness is the frozen mitigation, and
  matcher yield is reported with its tier decomposition so the
  reader can judge.
- **Dedupe residue.** Intra-layer duplicates (795) stay
  dropped (they duplicate kept ICIT texts; matching coverage
  is unaffected up to ICIT-internal duplication). Inscriptions
  of length < 3 participate in matching only via Tier A/B's
  ≥ 2-mapped rule as written; length-1/2 texts are weakly
  identified and their pairs are reported separately in the
  tier decomposition.
- **Permutation arm (§5.0)** permutes tokens, ignoring
  inscription-level clustering; its BH counts are descriptive
  context, not verdict inputs.
- **Site-mix arm** matches site names by string normalization
  only; ICIT site codes (`Agr`, `Ns`, …) that do not
  string-match a Holdat site name appear as unmatched shares
  and are reported, not silently mapped.
- **`dir.` semantics not assumed.** The source's direction
  labels are never interpreted; orientation is measured
  (D1/D2). A SUPPORTED H-DIRECTION licenses the R-DIR
  transformation as a *measured* alignment, not as a claim
  about either corpus's editorial intent.
- **Sentinel-stripped profiles (S1)** change the measured
  population geometry (a stripped sequence is shorter);
  F1 is comparable to F0 because the judgment floors and
  counts are held fixed, but S1 does not claim the stripped
  geometry is "correct" — only whether the disagreement
  survives it.
- **Diagnostic only.** No outcome of this study validates,
  demotes, or promotes any anchor; the 44 remain
  `pending_non_sa_validation`, STRICT94 remains the strict
  core, and tier counts and Holdat coverage are unchanged by
  construction (the anchors file is never written).
- **Corpus caveats (carried from specs 011/014):** Holdat and
  the ICIT layer are independent compilations of the same
  published catalogues, not independent archaeology.

## 9. Licensing / data handling

The field-cady corpus is MIT-licensed; the canonical registry
and crosswalk v2 are in-repo artifacts. Holdat and the ICIT
layers are used locally under their recorded terms
(Phase-107 acquisition log); no corpus file is committed or
redistributed by this phase. Published artifacts contain only
counts, shares, distances, verdicts, and sign-level crosswalk
metadata.

## 10. Deliverables (frozen)

- `specs/015-phase116-corpus-harmonization/{spec,plan,tasks}.md`
- `backend/scripts/phase116_build_keyed_layer.py` (+ gitignored
  keyed layer under `corpora/downloads/icit_fieldcady/`)
- `backend/glossa_lab/phase116_harmonization.py`,
  `backend/glossa_lab/phase116_run.py`,
  `backend/glossa_lab/experiment_graph_phase116.py`
  (+ registration in `experiment_graph.py`)
- `backend/scripts/phase116_harmonization_study.py`
- `backend/tests/test_phase116_harmonization.py`
- `reports/phase116_harmonization_results.json`
- `reports/phase116_harmonization_summary.md`
- Ledger entries in `LEDGER.md` and `glossa-indus/LEDGER.md`
- One PR; suite + foundation results recorded in the summary
