# Spec 031 — Spec 027 Stage 2 / Q7: Provenanced-Material Networks and Craft Style

> ## DESIGN — FOR FREEZE — 2026-10-13
>
> Owner order (Tristen Pierson, 2026-10-13): design and
> freeze Spec 027 Stage 2 / Q7 from the D8 margins.
> Execution is NOT ordered by that instruction and is
> not authorised by this spec: the deliverable is the
> frozen design and its OSF registration. The execution
> phase designated below (Phase-395) runs only on a
> separate owner order after this freeze merges and
> the registration verifies public.
>
> Governing record: Spec 027 §8.1 (the bounded Q7
> question), the Stage 2 / Q7 adjudication packet and
> its adjudication record (adopted **1B, 2B, 3A, 4A,
> 5A, 6A**, 2026-10-12), and the D8 source/licence
> audit (`specs/027-movement-culture-language/
> stage2-d8-audit.md`, 2026-10-12). Q7 the question
> stays owned by Spec 027 (claim F027-C15); this spec
> owns the Stage 2 design, its governed claim subset,
> its freeze, and its registration. Spec 028 (a
> Spec 027 follow-up under its own number) is the
> placement precedent.

## 1. Purpose

Spec 027 §8.1 sets the gate: Q7 may be frozen only
after Stage 0 (complete, Phase-391) **and** after the
D8 source/licence audit establishes which provenance
links are lawfully and traceably usable. The D8 audit
ran under adopted Ask 1B and closed on 2026-10-12
with **no rights failure in any stage**. This spec is
the freeze the adjudication's cascade prescribes as
its step 2: a Q7 design built from the audit's
margins, under adopted Asks 2B, 3A, 4A, 5A, and 6A,
with its minimum-support rules fixed **from those
margins, before any response is computed**.

**Bounded question (Spec 027 §8.1, unchanged):** Do
site pairs that share provenanced material sources
show greater ceramic or bead/craft-technique
similarity than expected from geographic and
river-network distance alone?

- **Unit:** site pair.
- **Predictor:** shared geological/provenance source,
  with the provenance method recorded per link.
- **Responses:** separately modelled ceramic
  similarity and bead/craft-technique similarity;
  never pooled into a single "culture" score
  (FR-027-8).
- **Controls:** geographic distance, river-network
  distance, period eligibility, site sample size, and
  publication/excavation intensity where measurable.
- **Null:** geography and river distance explain all
  shared variance; source-sharing adds no predictive
  power.
- **Falsifier (§8.1):** source-sharing adds no
  predictive power, or its effect is not robust to
  the frozen site jackknife.
- **Licensed conclusion:** a statement about objects,
  materials, and techniques only (F027-C15,
  F031-C01).

## 2. The D8 margins this design is built from

All quantities below are the audit's, stated as the
audit states them; nothing here is re-measured.

| Component | Posture | What it holds | Margin that binds this design |
|---|---|---|---|
| Law (2011), instrumental subsets (INAA for agate and vesuvianite-grossular; Sr/S isotopes for alabaster) | `open_access_read_only` | Provenience determinations tying artifacts to named geologic source areas, method recorded per material study | **>2,100 determinations at Harappa; almost 120 at all other sites combined; ≈95% single-site (Harappa) concentration** |
| Law (2011), Chapter 4 assemblage-wide assignments | `open_access_read_only` | Assemblage provenience outlines from field observation and contemporary geologic reference materials | Reference-based: the **sensitivity tier** under 2B, never the primary set |
| Kenoyer/Vidale craft studies (1992 and published applications) | `open_access_read_only` (openly posted texts); `catalogue_only` (publisher-only items) | The bead-drilling technique classification and its per-site published applications (Harappa, Chanhu-Daro, Mohenjo-Daro assemblages dominate) | **No consolidated per-object dataset exists**; the bead/craft arm's cell values are assembled at execution from the published applications, source recorded per cell |
| Possehl (1996) Meluhha compilation | `catalogue_only` | 76 cuneiform citations naming a source **region**, never an Indus site | **Contributes no site-pair links under any posture** (F031-C04) |

Site universe: the Spec 027 Stage 0 gazetteer —
**30 program sites** (36 source-asserted rows;
21 `verified_open` / 15 `open_access_read_only`).
Site identities, coordinates, and period labels come
from Stage 0 only (adopted 4A; §6 below).

Two consequences of the margins are stated here so
the freeze cannot be misread later:

1. **The primary link mass is small and
   Harappa-centred.** The other-site primary mass is
   bounded above by the ~120 other-site
   determinations, and only their instrumentally
   analysed subset is primary-tier; the audit does
   not split the ~120 by method, and that split is
   determined at digitisation design time under the
   audit's residual (ii), before any link is built.
   A design that pretended otherwise would be fitting
   its rules to hoped-for data.
2. **The drop-Harappa jackknife cell is the expected
   pressure point** (the Spec 028 lesson, named in
   advance): with ≈95% of determinations at one site,
   most linked pairs, if any, will involve Harappa.
   The verdict rules in §5 are written so that a
   Harappa-dependent effect cannot be reported as a
   general network pattern.

## 3. Link construction (adopted 2B, two tiers)

**Primary tier.** A determination is primary-tier
iff it is a Law (2011) determination attributed to a
named geologic source area by a named instrumental
method (INAA, Sr/S isotopes, or another instrumental
method the audit's Stage 1 record names), digitised
internally at `open_access_read_only` under the
Phase-124 read-only precedent. Nothing derived from
it is released (adopted 6A; F031-C11).

**Sensitivity tier.** Law's Chapter 4 reference-based
assignments form a separately labelled sensitivity
link set. It is never pooled into the primary set,
never carries a verdict, and is computed only
alongside a testable primary (§4.3).

**Links.** Source-area identity is exactly as
published by Law; the program merges no source areas
and renames none.

- A site is **link-eligible (primary)** iff it
  carries **≥ 3 primary-tier determinations** to
  named source areas (DD-1).
- A site pair is **linked (primary)** iff both sites
  carry ≥ 1 primary-tier determination attributed to
  the **same named source area** (DD-1).
- The same constructions on the sensitivity tier
  define sensitivity-eligible sites and
  sensitivity-linked pairs, labelled as such wherever
  reported.

**Meluhha** contributes contextual narrative only.
It enters no link set, no covariate, and no
sensitivity (F031-C04).

## 4. Response arms (adopted 3A)

Each arm is computed on **its own eligible site set**
and returns its own verdict. The arms are never
pooled (F031-C05).

### 4.1 Bead/craft arm

- **Response:** per-site composition over the
  published Kenoyer/Vidale drilling-technique classes
  (pecked perforation; tapered cylindrical;
  constricted cylindrical / "Ernestite"; copper —
  solid and tubular — as published), assembled from
  the classification's published applications, with
  the classification source recorded per cell
  (F031-C06).
- **Site eligibility (DD-2):** a gazetteer site with
  defensible coordinates (§6), period-eligible (§6),
  and **≥ 10 published technique-classified beads**
  from applications at audited postures
  (`open_access_read_only` texts; `catalogue_only`
  items contribute nothing until read under the same
  rule at digitisation design time).
- **Similarity:** Bray–Curtis on the per-site class
  proportions (the Stage 1 distance convention).

### 4.2 Ceramic arm

- **Response:** per-site composition over published
  fabric/typology classes from site reports, with
  the classification source recorded per cell.
- **Posture rule (D8 residual (i), decided here):**
  the ceramic response sources were outside D8's
  three audited components. Under Spec 027 §5.1,
  each site report used is assigned a posture at
  digitisation design time; only reports at
  `verified_open` or `open_access_read_only` may be
  digitised internally; `permission_required` and
  `catalogue_only` reports contribute catalogue
  records only, and a site whose classifications
  rest solely on such reports cannot enter the arm.
- **Site eligibility (DD-2):** a gazetteer site with
  defensible coordinates, period-eligible, and
  **≥ 20 published classified ceramic items**
  (fabric/typology determinations) from reports at
  the postures above.
- **Estimability — declared in advance (DD-7):** the
  ceramic arm is **conditionally estimable**. Its
  source basis has never been audited as a set, so
  no margin exists from which this freeze could
  honestly declare it estimable outright. The frozen
  rule is: at the execution margins step (§7),
  **before any ceramic response is computed**, if
  sources at audited postures cannot evidence
  **≥ 8 eligible ceramic sites** (§4.3), the ceramic
  arm is **NOT ESTIMABLE under this freeze** and
  closes at margins (F031-C07). This is the
  stage1-freeze §7 pattern (a margins determination
  recorded before outcomes), applied to the arm the
  margins cannot yet carry — declared now, not left
  vague.

### 4.3 Arm viability (adopted 5A; DD-3)

An arm's primary test runs iff, at the margins step:

- **≥ 8 eligible sites** in the arm, and
- **≥ 10 linked pairs** (primary tier) among them,
  and
- the analysis pair set is **all pairs** among the
  arm's eligible sites (linked and unlinked alike;
  the linked indicator is the predictor, not a
  filter).

An arm failing any viability threshold closes
**NOT-YET-TESTABLE** (a registration status, per
Spec 027 §3.3 usage) at the margins step, before any
response in that arm is computed. It is **not**
re-based on the sensitivity tier, on a lower
threshold, or on the other arm's site set
(F031-C08). The sensitivity tier is computed only
for an arm whose primary test runs, is labelled a
sensitivity wherever reported, and carries no
verdict.

### 4.4 Declared NOT ESTIMABLE / untestable in advance

Recorded at this freeze, before any outcome
(Spec 027 §9 discipline):

- **Sub-period-resolution Q7 variants** (e.g.
  period-sliced networks finer than published period
  labels): **untestable** under adopted 4A. Any such
  variant is a new question with its own design
  (F031-C10).
- **A visual-tier primary test:** not a variant of
  this design at all (2B). If the primary tier is
  too sparse, the affected arm is NOT-YET-TESTABLE,
  not re-based.
- **Dose-response as a verdict-bearing test**
  (shared-source *count* as the predictor): declared
  a **labelled sensitivity only** (DD-7); the
  verdict-bearing predictor is the binary
  shared-source indicator.
- **The ceramic arm**, conditionally, per §4.2.

## 5. Frozen statistics (adopted 5A)

The Spec 026/027 control and verdict discipline is
inherited wholesale; what follows operationalises it
for a site-pair estimand. All quantities are fixed
here, before execution.

- **Estimand (per arm):** the partial R² of the
  binary shared-source indicator in a multiple
  regression on distance matrices (MRM; MRQAP with
  double semi-partialling) of the arm's pairwise
  similarity on: shared-source indicator (primary
  tier), geographic distance, river-network
  distance, and the pair covariates of §6. The
  estimand is "similarity variance attributable to
  source-sharing beyond geography and river distance",
  on the pair set of §4.3. A p-value alone cannot
  produce SUPPORTED (Spec 027 §7.3 convention).
- **Practical margin (DD-4):** partial R² = **0.02**.
  Declared convention: a source-sharing share of
  similarity variance at or below 2% beyond the
  distance controls is not a provenance-network
  pattern for program purposes. (Stage 1's 0.01
  margin governed a 3,030-inscription estimand; the
  pair-level estimand here has at most C(30, 2)
  pairs and far fewer effective observations, and
  the margin is set accordingly — a design decision
  under 5A, recorded in `adjudication.md`.)
- **Permutation:** MRQAP site-label permutation,
  **B = 9,999**, p = (1 + #{stat_perm ≥ stat_obs}) /
  (1 + B), α = 0.05.
- **Interval:** percentile interval [2.5%, 97.5%] of
  the partial R² under site-resampling bootstrap,
  **9,999 replicates**.
- **Seed:** `20261013` for permutation, bootstrap,
  controls, and jackknife (one seed, named here so
  no later choice exists).
- **Jackknife (the §8.1 falsifier's second clause):**
  leave-one-site-out over every eligible site in the
  arm, the full MRM recomputed identically per
  dropped site. A LOSO cell is **estimable** iff the
  reduced set still meets §4.3's thresholds
  (≥ 8 sites, ≥ 10 linked pairs).

### 5.1 Discriminating controls (failure = INVALID)

Both controls run the **identical** pipeline (same
pair set construction, MRM, permutation, interval,
jackknife) on synthetic populations with the arm's
executed margins (site count, pair count, linked-pair
count, similarity distribution margins), in
**R = 199 replicates** each (DD-6):

- **Negative control:** similarity values generated
  with no source structure (drawn from the arm's
  pooled similarity distribution; linked labels
  carry no similarity information). **PASS** iff the
  SUPPORTED rule of §5.2 fires in **≤ 5%** of
  replicates.
- **Positive control:** similarity generated with a
  planted shared-source effect calibrated to a true
  partial R² of ≈ **2× the margin** (0.04). **PASS**
  iff the SUPPORTED rule fires in **≥ 95%** of
  replicates.

A control that cannot differentially fail makes the
run INVALID (FR-027-7; F031-C09). Controls are
computed per arm, on that arm's margins.

### 5.2 Verdict rules (per arm; Spec 027 §7.6 pattern)

Population reproduction is a precondition: if the
executed pair population differs from the margins
step's recorded population in any count, the run is
INVALID (population not reproduced) and stops.

- **SUPPORTED** iff controls pass AND the permutation
  rule rejects (p ≤ 0.05) AND the partial-R² interval
  lies entirely above 0.02 AND every LOSO cell is
  estimable and every LOSO partial-R² point estimate
  is above 0.02.
- **CONTRADICTED** iff controls pass AND (the
  permutation rule does not reject OR the interval
  lies entirely at or below 0.02). The bounded claim
  for that arm is defeated: source-sharing adds no
  predictive power beyond geography and river
  distance in this arm.
- **INCONCLUSIVE** iff controls pass and neither rule
  fires — including a jackknife range crossing the
  margin, or any LOSO cell non-estimable while the
  primary interval lies above the margin.
- **INVALID** iff a control fails, the population is
  not reproduced, or a frozen rule was changed after
  outcome inspection.
- **NOT-YET-TESTABLE** is a registration status, not
  a verdict: it is assigned at the margins step under
  §4.3, before outcomes exist.

No outcome of either arm identifies a people, a
workshop population, a migration, or a language
(F031-C01; Spec 027 §8.3: a Q7 result is not the
mobility arm of Q1 and does not upgrade Q1).

## 6. Pair construction and controls data

- **Geographic distance:** great-circle distance
  between Stage 0 site coordinates.
- **River-network distance (DD-8):** along-network
  distance on a drainage network connecting the
  sites' coordinates, sites snapped to the nearest
  network node with a **25 km** tolerance; the
  network source is pinned by name and file hash in
  the execution data step and recorded in the outcome
  record. A site that cannot be snapped within
  tolerance is excluded from all pair sets and
  reported.
- **Coordinates:** a site enters a pair set only if
  Stage 0 gives it defensible coordinates
  (`exact_published`, `approximate_published`, or
  `derived_centroid` under Spec 027 §5.2).
  `restricted` coordinates are used at their
  published precision only; `unknown` excludes the
  site. No coordinate is made more precise by
  inference (§5.2).
- **Period eligibility (adopted 4A; F031-C10):** a
  site is period-eligible iff its Stage 0 gazetteer
  `period_label_as_published` or Stage 0 program
  period assignment indicates Mature Harappan
  occupation as published. A pair is period-eligible
  iff both sites are. No finer temporal slicing is
  attempted anywhere in this design.
- **Sample-size covariate:** per pair, the minimum
  of the two sites' arm-specific classified-item
  counts (log-transformed), recorded per pair.
- **Publication/excavation-intensity covariate:**
  per pair, the minimum of the two sites'
  Stage 0 source-asserted gazetteer row counts as a
  declared proxy, recorded per pair; where the
  freeze's estimand is fit, it enters as a covariate
  — it is never a response or a filter.
- **Lineage:** every link and every response cell
  carries its source (Law material study; Kenoyer/
  Vidale application; site report) and its method
  where the source records one. One origin group per
  published source; aggregators create none
  (FR-027-11).

## 7. Execution shape (NOT authorised by this spec)

For the later owner order, the frozen shape is:

1. **Phase-395**, graph-first (FR-027-13 / H15/H23):
   script → graph module → registration →
   registration verification → run. No phase script
   runs before its graph node exists.
2. **Digitisation design step** (first execution
   act): per-source posture assignment under §5.1
   (ceramic sources per §4.2), the D8 residual (ii)
   appendix-level method-completeness re-verification
   for Law's printed tables, and the method split of
   the ~120 other-site determinations — all recorded
   before any link is built.
3. **Margins step:** eligibility and viability
   computed per arm under §§3–4; the population
   record (eligible sites, pair counts, linked-pair
   counts per tier) is written and hashed **before
   any response is computed**. Arm closures under
   §4.2/§4.3 happen here, in writing.
4. **Outcome step:** controls, primary tests,
   sensitivity tier (labelled), jackknife, verdicts
   per §5.2.
5. **Records:** outcome recorded in this spec's
   `outcome.md` and cross-recorded under Spec 027
   per adopted 6A; nothing is written into Stage 1's
   or Spec 028's records. No anchor or PRED-2026
   contact (FR-027-15).

## 8. What this design does not do

Spec 027 §10's hard limits bind this spec in full.
In particular:

- **No people or language conclusion** from any
  outcome (limits 1–4; F031-C01). A network pattern
  in materials is not movement of people, workshops,
  or speech.
- **No Q1 upgrade** (§8.3): Q7 is not Q1's mobility
  arm and no Q7 outcome changes Q1's blocked state.
- **No digitisation before rights clearance:** every
  source used sits at an audited posture
  (`stage2-d8-audit.md`; §4.2 for ceramic sources);
  `permission_required` material is not copied, and
  no rights holder is contacted under this spec — a
  permission request would be a separate owner
  decision.
- **No new primary data generation** (no laboratory
  provenance work, no fieldwork data).
- **No release of read-only-derived data** (adopted
  6A): link data derived from `open_access_read_only`
  sources are internal; only `verified_open`-derived
  rows may ever be published, CC BY 4.0 through the
  release gate.
- **No PRED-2026 or anchor contact**, and nothing
  here enters a sign-reading model.
- **No silent model-shopping** (limit 8): every
  variant run is reported, including the sensitivity
  tier and any non-estimable LOSO cell.

## 9. Governed claims (summary)

The governed register is `claims.json`
(F031-C01…C12), each claim with its falsifier,
boundary, and origin-grouped evidence:

- **C01** — Q7 verdicts under Spec 031 concern craft
  evidence only (objects, materials, and
  techniques).
- **C02** — The primary link set contains only
  Law (2011) determinations made by a named
  instrumental method.
- **C03** — Reference-based assignments enter only
  the separately labelled sensitivity tier.
- **C04** — The Meluhha compilations contribute no
  site-pair links under this design.
- **C05** — The two response arms are computed on
  separate eligible site sets, and the arms are never
  pooled.
- **C06** — The bead/craft response is built only
  from published Kenoyer/Vidale technique
  classifications (reaching assemblages through their
  published applications), with source recorded per
  cell.
- **C07** — The ceramic arm is NOT ESTIMABLE under
  this freeze if the margins step cannot evidence
  the frozen minimum eligible site count from
  sources at audited postures.
- **C08** — An arm failing the frozen viability
  thresholds at the margins step closes
  NOT-YET-TESTABLE and is not re-based on weaker
  links.
- **C09** — A verdict is issued only under the frozen
  verdict rules, and a non-discriminating control
  makes the run INVALID.
- **C10** — Period eligibility rests only on Stage 0
  gazetteer labels as published, and no
  sub-period-resolution variant is tested.
- **C11** — No released row is derived from an
  `open_access_read_only` source. (The registration
  half of adopted 6A — the frozen contract registered
  on OSF before any execution — is carried in §7 and
  the freeze record.)
- **C12** — Support thresholds take their values from
  the D8 audit margins, fixed in this freeze.

## 10. Design decisions taken under the packet's 5A mandate

Adopted Ask 5A fixes the support rules **in the
freeze, from margins only**; the margins force the
following specific choices, which the packet did not
itself enumerate. Each is a design decision taken
under that mandate — stated here and in
`adjudication.md`, with its recommendation and
reasoning, not buried:

- **DD-1** — Link support thresholds (site ≥ 3
  primary determinations; pair linked on ≥ 1 shared
  named source). *Reasoning:* a single stray
  determination cannot be allowed to create a link;
  with the other-site primary mass bounded by ~120
  determinations, a higher per-site floor would
  decide the viability question by construction
  rather than by the margins step.
- **DD-2** — Arm site-support floors (ceramic ≥ 20
  classified items per site; bead ≥ 10 classified
  beads per site). *Reasoning:* composition
  proportions over fewer items are dominated by
  sampling variation; 20 mirrors Stage 1's
  analysis-site floor, and 10 reflects the bead
  literature's smaller published counts while still
  supporting a proportion vector.
- **DD-3** — Arm viability (≥ 8 eligible sites and
  ≥ 10 linked pairs). *Reasoning:* below 8 sites the
  site jackknife has too few cells for the §8.1
  falsifier's robustness clause to operate, and
  below 10 linked pairs the shared-source term is
  not separately estimable from two distance
  covariates in a matrix regression.
- **DD-4** — Practical margin: partial R² = 0.02 for
  the shared-source term. *Reasoning:* §5 above.
- **DD-5** — Verdict-rule operationalisation exactly
  on the Stage 1 pattern, with NOT-YET-TESTABLE as a
  margins-step registration status (§5.2).
- **DD-6** — Controls as R = 199 synthetic replicates
  of the identical pipeline per arm, with the
  ≤ 5% / ≥ 95% SUPPORTED-rule firing rates as the
  discrimination test — the Stage 1 control logic
  translated to a pipeline without rarefaction
  draws.
- **DD-7** — The ceramic arm declared conditionally
  estimable with a pre-registered NOT ESTIMABLE
  closure at margins (§4.2), and dose-response
  declared sensitivity-only (§4.4). *Reasoning:* the
  ceramic source basis was never audited as a set
  (D8 residual (i)); inventing either an estimable
  or a not-estimable finding at this freeze would
  exceed the margins.
- **DD-8** — River-network distance construction
  (network pinned by name and hash at execution;
  25 km snap tolerance; unsnappable sites excluded
  and reported). *Reasoning:* §8.1 names the control
  but no network dataset exists in the program
  record; the construction rule is frozen here, the
  dataset identity is pinned before outcomes at
  execution — the same pattern as Stage 1's corpus
  pinning.

Any owner change to a DD item is a new adjudication
and, after this freeze merges, a new freeze — never
an amendment in place.

AI disclosure: drafted by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.
