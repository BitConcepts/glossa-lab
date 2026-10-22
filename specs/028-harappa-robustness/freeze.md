# Spec 028 — Freeze Record (Phase-393, Harappa Robustness)

> ## FROZEN at the Spec 028 freeze merge (2026-10-11)
>
> Basis: Spec 028 as adjudicated by delegation
> (`adjudication.md` — the owner's 2026-10-11 order
> authorising the follow-up and delegating the design), with
> Spec 027's adjudicated values inherited (M77 governs;
> Ask 3 corpus rules as frozen in Spec 027's Stage 1
> freeze). This record pins every Phase-393 quantity BEFORE
> any arm outcome is computed. Its margins come from the
> margins-only audit (`margins-audit.json`, produced by
> `build_margins_audit.py`); the audit computes no
> site-by-sign association, divergence, or permutation
> statistic, and a test pins the absence of outcome fields.
> Its machinery evidence comes from the synthetic-only
> calibration (`calibration.json`, produced by
> `build_calibration.py` through `pipeline393.py`). The
> machine freeze record is `freeze.json` (framework026
> digest).

## 1. Bounded claims and estimands (spec §5)

- **Arm A (CONFIRMATORY, primary).** Bounded claim:
  site-linked repertoire structure at/above the practical
  margin exists among the non-Harappa sites — in the named
  corpus, under M77, after rarefaction to a common cell
  size and stratification by object type, site explains
  more recorded sign-repertoire variation than expected
  under permuted site labels, at adjusted R² margin 0.01,
  in the population that excludes Harappa.
- **Arm B (CONFIRMATORY, secondary).** Bounded claim: the
  site effect is not an inscription-count artefact of the
  large corpora — the same form of claim on the full
  six-site population under a site-equal-weight estimand
  (every site contributes equally to every draw).
- **Arm C (EXPLORATORY).** A descriptive decomposition of
  Harappa's contribution (spec §5.3). No verdict, no
  p-value, no margin rule.

The claims are about *recorded repertoires in this corpus*;
no outcome identifies a dialect, a language, an ethnic
group, a political unit, or a workshop as a people.

- **Response:** per-inscription sign composition
  (proportions over the frozen 125 sign columns) under M77.
- **Grouping:** site (Arm A: 5 sites; Arm B: 6 sites).
- **Distance:** Bray–Curtis on proportions.
- **Estimand:** adjusted PERMANOVA R² for site,
  rarefaction-averaged (§4). The unadjusted R² is reported
  alongside for transparency; every rule uses the adjusted
  scale.
- **Practical margin:** adjusted R² = **0.01** (the Spec
  026/027 convention: a site share of repertoire dispersion
  below 1% beyond the null expectation is not a regional
  repertoire pattern for program purposes). A p-value alone
  cannot produce SUPPORTED.

## 2. Corpus (inherited from the Spec 027 Stage 1 freeze)

- **Substrate:** `icit_converted_v2_keyed.json` (sha256
  `bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8`),
  the program's M77-keyed layer and named deduplication
  artifact, built by the Phase-115/116 layer build from the
  ICIT-lineage export.
- **Metadata join:** horus84 `inscriptions.csv` (sha256
  `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`)
  joined on `id` for the completeness field. (Audit: 5,678
  of 5,679 records join, site agreement 5,678/5,678 — as
  frozen in Spec 027.)
- **Local store:** `corpora/downloads/spec028_harappa/`
  (gitignored); both hashes asserted by the audit, the
  calibration, and the execution run.
- **Token rules, eligibility, object classes:** exactly as
  Spec 027 `stage1-freeze.md` §2 — M77 on every record;
  composition tokens = `direct` + `chain` + `unmapped`
  pooled as UNMAPPED; `placeholder` positions are not signs;
  legible-token rule ≥ 2; provenanced only (site present,
  not `Unknown`); SEAL + TAB only; pottery graffiti
  (`POT:T:g`) excluded from every population. Multi-line
  status is not recorded in this layer (inherited stated
  boundary). Period is not a stratum or sensitivity (layer
  period field 59.2% uninformative; inherited limitation,
  restated in every verdict headline's record).
- **Parpola/CISI sensitivity:** none. It was recorded
  NOT ESTIMABLE at the frozen crosswalk rule in Spec 027's
  Stage 1 freeze (17.57% unambiguous coverage); this spec
  inherits that determination and does not revisit it.

## 3. Populations (frozen margins; execution must reproduce exactly)

Flow (audit): 5,679 layer records → dedup-kept 4,531 →
site-`Unknown` excluded 26 → provenanced 4,505 → SEAL/TAB
3,605 → legible ≥ 2 → **eligible 3,144** (52 sites).

**Analysis population** (eligible records at sites with
≥ 20 eligible inscriptions): 6 sites, **3,030 inscriptions**
— the Phase-392 population, reproduced exactly:

| Site | SEAL | TAB | Total |
|---|---|---|---|
| Harappa | 361 | 1,076 | 1,437 |
| Mohenjo-daro | 1,138 | 164 | 1,302 |
| Dholavira | 96 | 15 | 111 |
| Lothal | 72 | 2 | 74 |
| Chanhu-daro | 52 | 2 | 54 |
| Kalibangan | 49 | 3 | 52 |

**Arm A population:** the analysis population minus
Harappa — **1,593 records**, 5 sites (Mohenjo-daro 1,302;
Dholavira 111; Lothal 74; Chanhu-daro 54; Kalibangan 52).

**Arm B population:** the full analysis population.

**Arm C population:** Harappa's 1,437 analysis records
(47.43% of the analysis population; SEAL 361 / TAB 1,076).

**Sign columns:** the frozen 125 (123 M-signs with ≥ 10
mapped tokens in the eligible population + UNMAPPED +
OTHER), defined on the eligible population as in
Phase-392 — not re-derived per arm.

## 4. Frozen statistics

**Shared:** R = **199 draws**; B = **499 permutations** of
site labels within permutation strata per draw,
p = (1 + #{F_perm ≥ F_obs}) / (1 + B); α = 0.05; summaries =
median adjusted R², percentile interval [2.5%, 97.5%],
share of draws rejecting, median raw R² (transparency).
**Seed 20261012** for all arms, controls, jackknives, and
sensitivities (one seed, named here so no later choice
exists). Adjusted R² per draw =
1 − (1 − R²)(n − 1)/(n − g), n = inscriptions per draw,
g = sites in the draw.

**Permutation strata (Amendment 1):** type class ×
legible-length value (the exact legible-token count).
Labels are exchangeable only within a stratum. Support
(margins): 98.0% of Arm A and 99.6% of Arm B inscriptions
sit in multi-site strata.

**Arm A draw:** within each site × type-class cell of the
Arm A population, sample without replacement to
**n_cell = 49**; cells below 49 are excluded from the
rarefied population and reported. Included cells (6):
Mohenjo-daro SEAL/TAB, Dholavira SEAL, Lothal SEAL,
Chanhu-daro SEAL, Kalibangan SEAL → **294 inscriptions per
draw**. Excluded: Dholavira TAB 15, Lothal TAB 2,
Chanhu-daro TAB 2, Kalibangan TAB 3.

**Arm A jackknife:** LOSO over the 5 Arm A sites; per
dropped site the median adjusted R² recomputed identically
(no permutation); n_cell held at 49. LOSO cell support
(margins): every drop leaves ≥ 4 included cells.

**Arm A sensitivity (labelled, no verdict):** S-complete —
exclude records whose joined `complete` field is `N`
(1,303 records; included cells re-derived under the same
≥ 49 rule → 4 cells); recompute median adjusted R² and
rejection share.

**Arm B draw (site-equal quota):** each site contributes
exactly **Q = 52** inscriptions per draw (**312 per draw**);
Q is the smallest analysis-site total (Kalibangan 52).
Within a site, the quota is split across type classes by
the frozen allocation rule: largest-remainder proportional
allocation over the site's type-class counts, ties broken
by type-class name ascending, a stratum capped at its own
count with any capped remainder reassigned by continuing
the same order; sampling within each allocation without
replacement. The deterministic allocations are:

| Site | SEAL | TAB |
|---|---|---|
| Harappa | 13 | 39 |
| Mohenjo-daro | 45 | 7 |
| Dholavira | 45 | 7 |
| Lothal | 51 | 1 |
| Chanhu-daro | 50 | 2 |
| Kalibangan | 49 | 3 |

(Kalibangan's quota equals its full record count; its
contribution is its whole recorded repertoire in every
draw — the equal-weight estimand working as designed.)

**Arm B jackknife:** LOSO over the 6 sites with Q held at
52 (a design constant, not re-derived per drop);
recomputed identically (no permutation). Quota feasibility
for every drop is verified in the audit (min remaining
site total ≥ 52 in all six cases).

**Arm B sensitivity:** none (frozen design decision, spec
§5.2).

**Arm C (descriptive only):** computed on mean
compositions (no rarefaction): the 6 × 6 site-centroid
Bray–Curtis matrix; Harappa vs the pooled other-five mean
composition — total Bray–Curtis and its per-column
decomposition (|p_i − q_i| / 2, ranked, top 25 recorded
with shares); Harappa-vs-others Bray–Curtis within SEAL
only and within TAB only; Harappa SEAL vs Harappa TAB
centroid distance; Harappa token mass by type class. No
p-values, no margin comparisons, no verdict language;
labelled EXPLORATORY in every output.

## 5. Discriminating controls (per arm; failure = that arm INVALID)

Each arm runs the identical arm pipeline on synthetic
populations templated on the arm's analysis entries (same
slots, same per-inscription legible lengths), with the
synthetic population **regenerated per draw** (Amendment
1: each draw is an independent null or planted world).

- **Negative control:** each synthetic inscription's tokens
  drawn from the arm's pooled composition (Arm A: pooled
  over the Arm A eligible population; Arm B: pooled over
  the full eligible population; pooled compositions are
  margins). PASS iff median adjusted R² < 0.01 AND the
  share of draws rejecting is ≤ 0.10 (Amendment 1 part 3:
  under per-draw regeneration the share is a binomial
  proportion over 199 independent worlds, sd ≈ 0.0154 at
  α = 0.05; the Phase-392 ≤ 0.05 bound would fail a
  calibrated instrument ~41% of the time by chance, while
  0.10 sits ~3.2 sd above nominal and still fails the
  miscalibration this control exists to catch — the
  broken-construction shares observed pre-freeze were
  0.156–0.171. The observed share itself is always
  reported.)
- **Positive control:** each site's composition = the arm's
  pooled composition perturbed toward a site-specific set
  of 10 signs (probability × 3, renormalised). Sets are
  **deterministic**: disjoint blocks of 10 from the 60 most
  frequent mapped sign columns under the arm's pooled
  ranking, assigned in the arm's frozen site order (§3);
  the sets are recorded in `margins-audit.json`. PASS iff
  ≥ 95% of draws reject AND the adjusted R² interval lies
  entirely above 0.01.

If either of an arm's controls fails, that arm's run is
**INVALID**, its verdict is recorded as INVALID, and no
verdict is issued from its numbers. The other arm is
unaffected.

## 6. Verdict rules (per arm, applied mechanically)

Population reproduction is a precondition: if the executed
populations differ from §3's frozen margins in any count,
the run is INVALID (population not reproduced) and stops
before any outcome.

For each confirmatory arm, with its own quantities:

- **SUPPORTED** iff the arm's controls pass AND ≥ 95% of
  the arm's primary draws reject (p ≤ 0.05) AND the arm's
  adjusted R² percentile interval lies entirely above
  0.01 AND every LOSO median adjusted R² of that arm
  is > 0.01.
- **CONTRADICTED** iff the arm's controls pass AND
  (≥ 95% of the arm's primary draws fail to reject OR the
  arm's adjusted R² percentile interval lies entirely at
  or below 0.01).
- **INCONCLUSIVE** iff the arm's controls pass and neither
  rule fires (including a jackknife range crossing the
  margin while the primary interval does not).
- **INVALID** iff a control of that arm fails, the
  population is not reproduced, or a frozen rule was
  changed after outcome inspection.

Reporting is hierarchical (spec §5.4): Arm A primary,
Arm B secondary, no pooled cross-arm headline. No Spec 027
closure attaches to either arm: an Arm A or Arm B
CONTRADICTED defeats only its own bounded claim, and
SUPPORTED authorises no downstream work.

## 7. Calibration evidence (synthetic data only, pre-freeze)

Final configuration (this freeze, Amendment 1 applied),
seed 20261012, produced by `build_calibration.py` through
`pipeline393.py` — the pipeline the execution script
copies verbatim (identity asserted by test):

| Arm | Control | Median adj R² | Interval [2.5%, 97.5%] | Share rejecting | Result |
|---|---|---|---|---|---|
| A | negative | 0.00046 | [−0.0035, 0.0054] | 0.040 | **PASS** |
| A | positive | 0.02396 | [0.0156, 0.0336] | 1.000 | **PASS** |
| B | negative | 0.00204 | [−0.0018, 0.0071] | 0.055 | **PASS** |
| B | positive | 0.01670 | [0.0105, 0.0240] | 1.000 | **PASS** |

The instrument discriminates at the declared margin on
both arms' population shapes: the negative worlds sit at
~0, and the planted ~2×-margin worlds are detected
unanimously with intervals entirely above the margin. Arm
B's positive-control interval lower bound (0.0105) clears
the margin narrowly — recorded here so the execution's
control result is read against it; the PASS criterion is
the frozen one in §5, not this observation.

## 8. Execution shape

- Phase-393 script + graph module (H23 order: script →
  graph module → registration → verification → run), after
  this freeze merges and after the frozen contract is
  registered on OSF (registration URL recorded in
  `osf-registration.md` and both ledgers).
- Outputs: `reports/phase393_results.json`,
  `reports/phase393_report.md`; outcome + side-by-side +
  any historical assessment in this spec's directory;
  ledgers appended.
- No anchor or PRED contact. Nothing in this freeze
  authorises any change to Spec 027's records.

## Amendment 1 — control regeneration and permutation strata (2026-10-11, pre-merge, pre-outcome)

Two changes made after the design was drafted, **before
the freeze merged and before any repertoire outcome was
computed on real data**, each forced by machinery evidence
from synthetic data only:

1. **Controls regenerate their synthetic population per
   draw.** The drafted design inherited Phase-392's control
   construction: one synthetic population per control,
   rarefied over 199 draws. Calibration attempt 1 (frozen
   seed 20261012, Phase-392 type-only strata) showed Arm
   A's negative control falsely rejecting in **17.1%** of
   draws (median adjusted R² 0.00215 — the median was fine;
   the share was not). Attempt 2 (strata refined to length
   bands {2}, {3–4}, {5+}) and attempt 3 (strata refined to
   the exact length value) still failed (shares not
   recorded for attempt 2; attempt 3: **15.6%**). A
   synthetic diagnostic then isolated the mechanism: under
   a second generation seed the identical constructions
   gave shares of **0.015** (type-only) and **0.000**
   (exact length) — the share is a property of the single
   generated population, whose small-cell generation noise
   (e.g. Kalibangan SEAL's 49 synthetic inscriptions)
   recurs identically in all 199 rarefaction draws, not a
   property of the instrument. Regenerating the population
   per draw — each draw an independent null world —
   returned the shares to nominal in every diagnostic
   variant (**0.050** type-only strata, **0.035** and
   **0.070** exact-length strata, across two seeds). An
   earlier length-shuffle diagnostic (share 0.005) is
   consistent with the same mechanism: shuffling
   regenerated the population's noise alignment. The
   Phase-392 control itself is not impugned retroactively:
   its recorded share (0.005) is one draw of the same
   lottery that happened to land benign, and its verdict
   did not rest on the negative control's share alone —
   but a construction whose calibration demonstrably
   lotteries is not freezable for this spec.
2. **Permutation strata carry the exact legible-length
   value.** Legible length is site-correlated within type
   class (margins: mean 3.88–4.96 across the included
   cells) and multinomial sampling dispersion follows
   length, so within a type-only stratum, labels are not
   exchangeable under the null to the standard this
   program requires. The exact-length stratum (support:
   98.0% / 99.6% of Arm A / Arm B inscriptions in
   multi-site strata) removes the channel by construction.
   Under per-draw regeneration the diagnostic shares were
   nominal with either strata choice; the exact-length
   strata are frozen because the exchangeability property
   is stronger, at no cost to any effect-size quantity
   (strata govern only legal permutations).
3. **The negative control's PASS bound is restated for the
   regenerated construction.** Phase-392's bound (≥ 95% of
   draws non-rejecting, i.e. share ≤ 0.05) was written for
   a single-population share. Under per-draw regeneration
   the share is a binomial proportion over 199 independent
   worlds: at a truly calibrated α = 0.05 its sd is
   ≈ 0.0154, and the ≤ 0.05 bound rejects a calibrated
   instrument with probability ≈ 0.41 (P(X ≥ 11) for
   X ~ Binomial(199, 0.05)) — a gate that fails a sound
   instrument two times in five is itself defective.
   The final calibration made the point concrete: Arm B's
   negative control at the frozen seed gave share 0.055
   (11 of 199) with median 0.00204 — a value a calibrated
   instrument produces routinely. The frozen bound is
   therefore share ≤ **0.10** (≈ 3.2 sd above nominal;
   failure probability ≈ 0.0025 for a calibrated
   instrument), which still fails every broken-construction
   share observed pre-freeze (0.156–0.171). The primary
   arms' rejection-share clauses (§6) are untouched: for a
   real population the share is a rarefaction-distribution
   property, not a binomial rate, and the Phase-392
   convention stands. The positive control's criteria are
   untouched (a power criterion, not a calibration rate).

No quantity in this amendment derives from the real
corpus's site-by-sign structure; every number above comes
from synthetic populations or from margins (cell counts,
length distributions, pooled compositions), as the frozen
control definitions themselves require.
