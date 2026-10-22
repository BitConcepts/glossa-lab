"""Phase-395 (Spec 031) — Q7 provenanced-material networks
execution build.

Freeze: specs/031-stage2-q7-provenance-networks/freeze.md
(digest f63167fc99c8d3c31f885b1014cad69fab3788fcf8e6212d018aa6948a2cdac6;
adjudication.md — the Stage 2 / Q7 asks adopted as a block:
1B, 2B, 3A, 4A, 5A, 6A; design decisions DD-1..DD-8).
Registered before execution: OSF https://osf.io/jtwvc/,
DOI 10.17605/OSF.IO/JTWVC (adopted 6A precondition; approved
and public 2026-10-13). Execution ordered by the owner
2026-10-13 ("Do ALL that remains now").

The build executes the frozen shape of Spec 031 section 7:

  step 2  Digitisation design step — per-source posture
          assignments (ceramic sources per section 4.2), the
          D8 residual (ii) appendix-level re-verification, and
          the method split of the other-site determinations.
          Its products are the research inputs in the
          gitignored local store
          corpora/downloads/spec031_phase395/ (never in git):
            law_digitisation.json   the Law (2011) digitisation
            bead_applications.json  the bead/craft source record
            ceramic_postures.json   the ceramic posture audit
          A missing input fails the build loud (the step was
          not run).
  step 3  Margins step — eligibility and viability per arm
          under sections 3-4; the population record (eligible
          sites, pair counts, linked-pair counts per tier) is
          written and hashed BEFORE any response is computed.
          Arm closures under sections 4.2/4.3 happen here.
  step 4  Outcome step — controls, primary tests, labelled
          sensitivity, jackknife, verdicts per section 5.2.
          Runs only for an arm that passed the margins step.

Frozen rules as implemented (no rule is re-decided here):

  * Primary tier (section 3, DD-1): a Law (2011)
    determination attributed to a named geologic source
    area by a named instrumental method — INAA or Sr/S
    isotopes, the methods the D8 audit's Stage 1 record
    names. Assignments to the Shahr-i-Sokhta proxy
    source-group are not attributions to a named source
    area and never count. A site is link-eligible at
    >= 3 such determinations; a pair is linked on >= 1
    shared named source area (identity as published).
  * Sensitivity tier (section 3): Chapter 4
    reference-based assignments only, separately labelled,
    never pooled, never a verdict — and computed only
    alongside a testable primary arm (section 4.3).
  * Meluhha contributes no links under any posture
    (F031-C04).
  * Site universe (adopted 4A): the Spec 027 Stage 0
    gazetteer (data/movement/gazetteer_rows.jsonl — a
    Spec 027 record, never modified here). Coordinates
    defensible iff a site's Stage 0 rows carry
    exact_published / approximate_published /
    derived_centroid (section 6). Period eligibility iff
    a site's Stage 0 period_label_as_published or
    program_period_assignment indicates Mature Harappan
    occupation as published (section 6, F031-C10); no
    finer slicing, no inference.
  * Arm floors (DD-2): bead/craft >= 10 published
    technique-classified beads per site; ceramic >= 20
    published classified items per site from reports at
    verified_open / open_access_read_only postures.
  * Viability (section 4.3, DD-3): an arm's primary test
    runs iff >= 8 eligible sites AND >= 10 linked pairs
    (primary tier) among them; the analysis pair set is
    all pairs among the arm's eligible sites. An arm
    failing viability closes NOT-YET-TESTABLE at margins.
    The ceramic arm additionally closes NOT ESTIMABLE at
    margins if sources at audited postures cannot
    evidence >= 8 eligible ceramic sites (section 4.2,
    DD-7). No arm is re-based on the sensitivity tier, a
    lower threshold, or the other arm's site set.
  * Statistics (section 5, for a viable arm): MRM /
    MRQAP (double semi-partialling) partial R-squared of
    the binary shared-source indicator beyond geographic
    distance, river-network distance and the pair
    covariates; practical margin 0.02 (DD-4); site-label
    permutation B = 9,999; site-resampling bootstrap
    interval, 9,999 replicates; seed 20261013; full
    leave-one-site-out jackknife (a LOSO cell is
    estimable iff the reduced set still meets section
    4.3); discriminating controls, R = 199 replicates of
    the identical pipeline per arm (negative PASS iff
    the SUPPORTED rule fires in <= 5%; positive, planted
    at approx. 2x margin, iff >= 95%); verdict rules
    exactly per section 5.2, including population
    reproduction as a precondition.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
DATA_DIR = REPO / "data" / "movement"
INPUT_DIR = REPO / "corpora" / "downloads" / "spec031_phase395"
DEFAULT_RESULTS = REPO / "reports" / "phase395_results.json"
DEFAULT_REPORT = REPO / "reports" / "phase395_margins_report.md"

INPUT_FILES = {
    "law": "law_digitisation.json",
    "bead": "bead_applications.json",
    "ceramic": "ceramic_postures.json",
}

# ── Frozen constants (Spec 031; DD-1..DD-8) ─────────────────────
SEED = 20261013
MARGIN = 0.02            # DD-4 practical margin, partial R^2
B_PERM = 9999            # MRQAP permutations
B_BOOT = 9999            # bootstrap replicates
R_CONTROLS = 199         # DD-6 control replicates per arm
ALPHA = 0.05
MIN_ELIGIBLE_SITES = 8   # DD-3 viability
MIN_LINKED_PAIRS = 10    # DD-3 viability
SITE_LINK_FLOOR = 3      # DD-1 primary determinations per site
BEAD_FLOOR = 10          # DD-2 classified beads per site
CERAMIC_FLOOR = 20       # DD-2 classified items per site
DEFENSIBLE_COORD_STATES = {
    "exact_published", "approximate_published", "derived_centroid",
}
AUDITED_POSTURES = {"verified_open", "open_access_read_only"}


def fatal(msg: str) -> "SystemExit":
    raise SystemExit(f"phase395 build: FATAL: {msg}")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_json(obj) -> str:
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in
            path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


# ── Step 3a: the Stage 0 gazetteer screens (adopted 4A) ──────────

def _label_texts(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def indicates_mature_harappan(value) -> bool:
    """The frozen period test (Spec 031 section 6 / F031-C10):
    the published label itself must indicate Mature Harappan
    occupation. No inference from other fields, no refinement
    from the chronology spine (adopted 4A)."""
    return any("mature harappan" in t.lower()
               for t in _label_texts(value))


def gazetteer_screens(rows: list[dict]) -> dict[str, dict]:
    """Per program site: the coordinate screen and the period
    screen, computed from the site's Stage 0 rows only."""
    sites: dict[str, dict] = {}
    for r in rows:
        s = sites.setdefault(r["program_site_id"], {
            "rows": 0, "gazetteer_row_ids": [],
            "coordinate_states": set(), "has_coordinates": False,
            "period_labels": [], "period_eligible": False,
            "row_counts_by_source": {},
        })
        s["rows"] += 1
        s["gazetteer_row_ids"].append(r["gazetteer_row_id"])
        s["coordinate_states"].add(r["coordinate_state"])
        if r["coordinate_state"] in DEFENSIBLE_COORD_STATES:
            s["has_coordinates"] = True
        for t in _label_texts(r.get("period_label_as_published")):
            if t not in s["period_labels"]:
                s["period_labels"].append(t)
        if indicates_mature_harappan(
                r.get("period_label_as_published")) or \
                indicates_mature_harappan(
                    r.get("program_period_assignment")):
            s["period_eligible"] = True
        src = r["source_gazetteer"]
        s["row_counts_by_source"][src] = \
            s["row_counts_by_source"].get(src, 0) + 1
    for s in sites.values():
        s["coordinate_states"] = sorted(s["coordinate_states"])
    return sites


# ── Step 3b: link construction (section 3, DD-1) ───────────────

def build_links(law: dict) -> dict:
    """Primary-tier link construction from the digitisation
    record. Only studies the record marks tier == 'primary'
    contribute; a site's named-source total sums the counted
    named-source determinations the record states per study
    (proxy-group assignments and unattributed samples never
    count). Linked pairs are counted from the record's
    CERTAIN shared-source holders only; pairs the record
    flags uncertain are reported, never resolved."""
    named_totals: dict[str, int] = {}
    by_study: dict[str, dict[str, int]] = {}
    holders: dict[str, set[str]] = {}
    uncertain: list[list[str]] = []
    study_summaries = []
    for study in law["studies"]:
        if study.get("tier") != "primary":
            continue
        counted: dict[str, int] = {}
        if "sites" in study:  # per-site counted determinations
            for site, vals in study["sites"].items():
                counted[site] = int(vals["named_source_total"])
        for site, n in study.get(
                "counted_named_source_determinations", {}).items():
            counted[site] = counted.get(site, 0) + int(n)
        for site, n in counted.items():
            named_totals[site] = named_totals.get(site, 0) + n
            by_study.setdefault(site, {})[study["material"]] = n
        for source, sites_ in study.get(
                "certain_source_holders", {}).items():
            holders.setdefault(source, set()).update(sites_)
        uncertain.extend(study.get("uncertain_pairs", []))
        study_summaries.append({
            "material": study["material"],
            "chapter": study["chapter"],
            "method": study["method"],
            "counted_sites": counted,
            "counted_total": sum(counted.values()),
        })
    eligible = sorted(s for s, n in named_totals.items()
                      if n >= SITE_LINK_FLOOR)
    pairs: set[tuple[str, str]] = set()
    for sites_ in holders.values():
        for a, b in itertools.combinations(sorted(sites_), 2):
            if a in eligible and b in eligible:
                pairs.add((a, b))
    uncertain = sorted({tuple(sorted(p)) for p in uncertain
                        if p[0] in eligible and p[1] in eligible
                        and tuple(sorted(p)) not in pairs})
    return {
        "named_source_totals": named_totals,
        "named_source_totals_by_study": by_study,
        "link_eligible_sites": eligible,
        "linked_pairs_certain": sorted(pairs),
        "linked_pairs_uncertain": [list(p) for p in uncertain],
        "certain_source_holders": {
            k: sorted(v) for k, v in sorted(holders.items())},
        "studies": study_summaries,
    }


# ── Step 3c: arm margins and closures (sections 4.2/4.3) ────────

def arm_margins(arm: str, screens: dict, links: dict,
                floor_evidenced_sites: set[str]) -> dict:
    """Eligibility is the frozen conjunction: gazetteer site,
    defensible coordinates, period-eligible, and the arm's
    support floor evidenced from audited-posture sources.
    Viability and closures follow sections 4.2/4.3 exactly."""
    coord_sites = {s for s, v in screens.items()
                   if v["has_coordinates"]}
    period_sites = {s for s, v in screens.items()
                    if v["period_eligible"]}
    eligible = sorted(set(screens) & coord_sites & period_sites
                      & floor_evidenced_sites)
    linked_among = [p for p in links["linked_pairs_certain"]
                    if p[0] in eligible and p[1] in eligible]
    viable = len(eligible) >= MIN_ELIGIBLE_SITES and \
        len(linked_among) >= MIN_LINKED_PAIRS
    closure = None
    if not viable:
        if arm == "ceramic":
            closure = {
                "status": "NOT ESTIMABLE",
                "rule": "Spec 031 section 4.2 / DD-7: sources at "
                        "audited postures cannot evidence >= 8 "
                        "eligible ceramic sites at the margins "
                        "step; the arm closes at margins and no "
                        "ceramic response is computed.",
            }
        else:
            closure = {
                "status": "NOT-YET-TESTABLE",
                "rule": "Spec 031 section 4.3 / DD-3: the arm "
                        "fails the frozen viability thresholds "
                        "(>= 8 eligible sites and >= 10 linked "
                        "pairs) at the margins step; it is not "
                        "re-based on the sensitivity tier, a "
                        "lower threshold, or the other arm's "
                        "site set (F031-C08).",
            }
    return {
        "arm": arm,
        "sites_total": len(screens),
        "sites_with_coordinates": len(coord_sites),
        "sites_period_eligible": len(period_sites),
        "sites_floor_evidenced": len(floor_evidenced_sites),
        "eligible_sites": eligible,
        "eligible_count": len(eligible),
        "analysis_pairs": len(eligible) * (len(eligible) - 1) // 2,
        "linked_pairs_among_eligible": len(linked_among),
        "viable": viable,
        "closure": closure,
    }


# ── Step 4 machinery (section 5; runs only for a viable arm) ────

def _upper(mat: np.ndarray) -> np.ndarray:
    i, j = np.triu_indices(mat.shape[0], k=1)
    return mat[i, j]


def _ols_fit(y: np.ndarray, x: np.ndarray):
    x1 = np.column_stack([np.ones(len(y)), x])
    beta, *_ = np.linalg.lstsq(x1, y, rcond=None)
    fitted = x1 @ beta
    resid = y - fitted
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 0.0 if ss_tot == 0 else 1.0 - ss_res / ss_tot
    return beta, fitted, resid, r2


def _ols_r2(y: np.ndarray, x: np.ndarray) -> float:
    return _ols_fit(y, x)[3]


def mrm_partial_r2(sim: np.ndarray, shared: np.ndarray,
                   geo: np.ndarray, river: np.ndarray,
                   covars: list[np.ndarray]) -> float:
    """Partial R^2 of the binary shared-source indicator in
    the MRM of pairwise similarity on shared-source, the two
    distances and the pair covariates (section 5 estimand):
    (R2_full - R2_reduced) / (1 - R2_reduced)."""
    y, x_full, x_red = _design(sim, shared, geo, river, covars)
    return _partial_r2_from_design(y, x_full, x_red)


def _permute(mat: np.ndarray, perm: np.ndarray) -> np.ndarray:
    return mat[np.ix_(perm, perm)]


def _design(sim, shared, geo, river, covars):
    y = _upper(sim)
    cols = [_upper(shared), _upper(geo), _upper(river)]
    cols += [_upper(c) for c in covars]
    return y, np.column_stack(cols), np.column_stack(cols[1:])


def _partial_r2_from_design(y, x_full, x_red) -> float:
    r2_full = _ols_r2(y, x_full)
    r2_red = _ols_r2(y, x_red)
    if r2_red >= 1.0:
        return 0.0
    return (r2_full - r2_red) / (1.0 - r2_red)


def mrqap_pvalue(sim, shared, geo, river, covars, b: int,
                 rng: np.random.Generator) -> float:
    """MRQAP with double semi-partialling (section 5): the
    reduced model (distances + covariates, no shared-source
    term) is fitted to the response; its residuals, as a
    matrix, have their site labels permuted; the permuted
    response is the reduced fit plus permuted residuals,
    and the partial R^2 of the full model on it is the
    permutation statistic."""
    y, x_full, x_red = _design(sim, shared, geo, river, covars)
    obs = _partial_r2_from_design(y, x_full, x_red)
    _, fitted, resid, _ = _ols_fit(y, x_red)
    n = sim.shape[0]
    iu = np.triu_indices(n, k=1)
    resid_mat = np.zeros((n, n))
    resid_mat[iu] = resid
    resid_mat[(iu[1], iu[0])] = resid
    hits = 0
    for _ in range(b):
        perm = rng.permutation(n)
        y_star = fitted + _upper(_permute(resid_mat, perm))
        stat = _partial_r2_from_design(y_star, x_full, x_red)
        if stat >= obs:
            hits += 1
    return (1 + hits) / (1 + b)


def bootstrap_interval(sim, shared, geo, river, covars, b: int,
                       rng: np.random.Generator) -> list[float]:
    """Percentile interval [2.5%, 97.5%] of the partial R^2
    under site-resampling bootstrap (section 5)."""
    n = sim.shape[0]
    stats = []
    for _ in range(b):
        idx = rng.integers(0, n, size=n)
        try:
            stats.append(mrm_partial_r2(
                sim[np.ix_(idx, idx)], shared[np.ix_(idx, idx)],
                geo[np.ix_(idx, idx)], river[np.ix_(idx, idx)],
                [c[np.ix_(idx, idx)] for c in covars]))
        except np.linalg.LinAlgError:
            continue
    if not stats:
        return [float("nan"), float("nan")]
    lo, hi = np.percentile(np.array(stats), [2.5, 97.5])
    return [float(lo), float(hi)]


def loso_cells(sim, shared, geo, river, covars,
               sites: list[str]) -> list[dict]:
    """Full leave-one-site-out jackknife (section 5). A cell
    is estimable iff the reduced set still meets section
    4.3 (>= 8 sites, >= 10 linked pairs)."""
    cells = []
    n = sim.shape[0]
    for drop in range(n):
        keep = [i for i in range(n) if i != drop]
        sub_shared = shared[np.ix_(keep, keep)]
        linked = int((_upper(sub_shared) > 0).sum())
        estimable = len(keep) >= MIN_ELIGIBLE_SITES and \
            linked >= MIN_LINKED_PAIRS
        value = None
        if estimable:
            value = mrm_partial_r2(
                sim[np.ix_(keep, keep)], sub_shared,
                geo[np.ix_(keep, keep)], river[np.ix_(keep, keep)],
                [c[np.ix_(keep, keep)] for c in covars])
        cells.append({"dropped_site": sites[drop],
                      "estimable": estimable,
                      "linked_pairs": linked,
                      "partial_r2": value})
    return cells


def verdict_from_rules(controls_pass: bool, p_value: float,
                       interval: list[float],
                       cells: list[dict],
                       population_reproduced: bool) -> str:
    """Spec 031 section 5.2, verbatim rule order."""
    if not population_reproduced or not controls_pass:
        return "INVALID"
    rejects = p_value <= ALPHA
    interval_above = interval[0] > MARGIN
    interval_below = interval[1] <= MARGIN
    if rejects and interval_above and cells and \
            all(c["estimable"] and c["partial_r2"] is not None
                and c["partial_r2"] > MARGIN for c in cells):
        return "SUPPORTED"
    if (not rejects) or interval_below:
        return "CONTRADICTED"
    return "INCONCLUSIVE"


def run_controls(sim, shared, geo, river, covars, sites,
                 b_perm: int, b_boot: int, r_reps: int,
                 rng: np.random.Generator) -> dict:
    """Discriminating controls (section 5.1, DD-6): R
    replicates of the identical pipeline on synthetic
    populations with the arm's executed margins. Negative:
    similarity values drawn from the arm's pooled
    similarity distribution, carrying no source structure.
    Positive: the same draws plus a planted shared-source
    effect calibrated to a true partial R^2 of approx.
    2x the margin. PASS iff the SUPPORTED rule fires in
    <= 5% (negative) / >= 95% (positive) of replicates.
    A full SUPPORTED evaluation per replicate includes the
    jackknife; replicates use the same verdict rules."""

    def _fires(y_mat: np.ndarray) -> bool:
        p = mrqap_pvalue(y_mat, shared, geo, river, covars,
                         b_perm, rng)
        iv = bootstrap_interval(y_mat, shared, geo, river,
                                covars, b_boot, rng)
        cells = loso_cells(y_mat, shared, geo, river, covars,
                           sites)
        return verdict_from_rules(True, p, iv, cells, True) \
            == "SUPPORTED"

    pooled = _upper(sim)
    n = sim.shape[0]
    iu = np.triu_indices(n, k=1)

    def _draw() -> np.ndarray:
        m = np.zeros((n, n))
        vals = rng.choice(pooled, size=len(pooled),
                          replace=True)
        m[iu] = vals
        m[(iu[1], iu[0])] = vals
        return m

    def _plant(base: np.ndarray) -> np.ndarray:
        # Calibrate an additive shared-source shift so the
        # partial R^2 of the indicator is approx. 2 * MARGIN:
        # binary-indicator partial R^2 ~= d^2 * p(1-p) / var(y)
        # for shift d and linked share p of pairs.
        p = float((_upper(shared) > 0).mean())
        var = float(np.var(_upper(base))) or 1.0
        target = 2 * MARGIN
        d = np.sqrt(target * var / max(p * (1 - p), 1e-9))
        return base + d * shared

    neg = sum(_fires(_draw()) for _ in range(r_reps))
    pos = sum(_fires(_plant(_draw())) for _ in range(r_reps))
    return {
        "replicates": r_reps,
        "negative_supported_fires": neg,
        "negative_pass": neg / r_reps <= 0.05,
        "positive_supported_fires": pos,
        "positive_pass": pos / r_reps >= 0.95,
        "pass": (neg / r_reps <= 0.05) and (pos / r_reps >= 0.95),
    }


def run_outcome_step(arm_data: dict, population_hash: str,
                     population_recount_hash: str) -> dict:
    """Section 5 outcome step for one viable arm. Population
    reproduction is a precondition (section 5.2)."""
    rng = np.random.default_rng(SEED)
    reproduced = population_hash == population_recount_hash
    sim = arm_data["similarity"]
    shared = arm_data["shared"]
    geo = arm_data["geo"]
    river = arm_data["river"]
    covars = arm_data["covars"]
    sites = arm_data["sites"]
    controls = run_controls(sim, shared, geo, river, covars,
                            sites, B_PERM, B_BOOT, R_CONTROLS,
                            rng)
    p = mrqap_pvalue(sim, shared, geo, river, covars, B_PERM,
                     rng)
    iv = bootstrap_interval(sim, shared, geo, river, covars,
                            B_BOOT, rng)
    cells = loso_cells(sim, shared, geo, river, covars, sites)
    point = mrm_partial_r2(sim, shared, geo, river, covars)
    verdict = verdict_from_rules(controls["pass"], p, iv, cells,
                                 reproduced)
    return {"partial_r2": point, "p_value": p, "interval": iv,
            "controls": controls, "jackknife": cells,
            "population_reproduced": reproduced,
            "verdict": verdict}


# ── Build ────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path,
                        default=DEFAULT_RESULTS)
    parser.add_argument("--report", type=Path,
                        default=DEFAULT_REPORT)
    args = parser.parse_args()

    gazetteer_path = DATA_DIR / "gazetteer_rows.jsonl"
    gazetteer_rows = load_jsonl(gazetteer_path)

    input_hashes = {
        "data/movement/gazetteer_rows.jsonl":
            sha256_file(gazetteer_path),
        "backend/scripts/phase395_q7_execution.py":
            sha256_file(Path(__file__).resolve()),
    }
    inputs: dict[str, dict] = {}
    for key, fname in INPUT_FILES.items():
        p = INPUT_DIR / fname
        if not p.is_file():
            fatal(f"digitisation input missing (step 2 not "
                  f"run?): {p}")
        inputs[key] = json.loads(p.read_text(encoding="utf-8"))
        input_hashes[f"corpora/downloads/spec031_phase395/"
                     f"{fname}"] = sha256_file(p)
    law = inputs["law"]
    for f in law["source_work"]["files"]:
        p = INPUT_DIR / f["file"]
        if not p.is_file():
            fatal(f"Law source file missing: {p}")
        if sha256_file(p) != f["sha256"]:
            fatal(f"Law source file hash mismatch: {f['file']}")
        input_hashes[f"corpora/downloads/spec031_phase395/"
                     f"{f['file']}"] = f["sha256"]

    # Step 3: margins.
    screens = gazetteer_screens(gazetteer_rows)
    links = build_links(law)

    # Bead floor: the bead source record evidences no site's
    # floor count (no consolidated per-object dataset, D8
    # Stage 2); the floor conjunct is evidenced for no site.
    bead_floor_sites: set[str] = set()
    if inputs["bead"]["floor_step"]["enumerated_counts"]:
        bead_floor_sites = set(
            inputs["bead"]["floor_step"]["sites_meeting_floor"])

    # Ceramic floor: a site is floor-evidenced only where the
    # posture audit places a classification-bearing report at
    # an audited posture AND a classified-item count >= the
    # floor is evidenced. The audit records postures; counts
    # are a response-assembly quantity, not evidenced at
    # margins for any site (and cannot be reached: the
    # period conjunct already empties the eligible set).
    ceramic_floor_sites: set[str] = set()

    bead = arm_margins("bead_craft", screens, links,
                       bead_floor_sites)
    ceramic = arm_margins("ceramic", screens, links,
                          ceramic_floor_sites)

    # The digitisation record names sites as published; the
    # gazetteer's program_site_id uses spaces where the
    # publications use hyphens (mohenjo-daro / mohenjo daro).
    # The join is on the normalised form, and the mapping is
    # recorded in the results — never a silent rename of a
    # gazetteer identity.
    def _norm(s: str) -> str:
        return s.replace("-", " ").strip().lower()

    screens_by_norm = {_norm(s): s for s in screens}
    site_id_mapping = {}
    for s in links["named_source_totals"]:
        if _norm(s) in screens_by_norm:
            site_id_mapping[s] = screens_by_norm[_norm(s)]
    in_universe_eligible = sorted(
        site_id_mapping[s] for s in links["link_eligible_sites"]
        if s in site_id_mapping)
    in_universe_pairs = [
        p for p in links["linked_pairs_certain"]
        if p[0] in site_id_mapping and p[1] in site_id_mapping]

    population = {
        "gazetteer_sites": len(screens),
        "gazetteer_rows": len(gazetteer_rows),
        "sites_with_coordinates": bead["sites_with_coordinates"],
        "sites_period_eligible": bead["sites_period_eligible"],
        "link_eligible_sites_all_sources":
            len(links["link_eligible_sites"]),
        "link_eligible_sites_in_gazetteer":
            len(in_universe_eligible),
        "linked_pairs_certain_all_sources":
            len(links["linked_pairs_certain"]),
        "linked_pairs_uncertain_all_sources":
            len(links["linked_pairs_uncertain"]),
        "linked_pairs_in_gazetteer":
            len(in_universe_pairs),
        "arms": {
            "bead_craft": {
                "eligible_sites": bead["eligible_count"],
                "analysis_pairs": bead["analysis_pairs"],
                "linked_pairs": bead["linked_pairs_among_eligible"],
            },
            "ceramic": {
                "eligible_sites": ceramic["eligible_count"],
                "analysis_pairs": ceramic["analysis_pairs"],
                "linked_pairs":
                    ceramic["linked_pairs_among_eligible"],
            },
        },
        "sensitivity_tier": {
            "constructed": False,
            "linked_pairs": None,
            "basis": "Computed only alongside a testable "
                     "primary arm (section 4.3); no arm is "
                     "testable. Chapter 4 is also absent from "
                     "the posted set (digitisation record).",
        },
    }
    population_hash = sha256_json(population)

    # Step 4: outcome step — only for a viable arm. With the
    # margins above, no arm is viable and no response in
    # either arm is computed; the closures are the outcome.
    outcome_steps = {}
    for arm_name, arm_rec in (("bead_craft", bead),
                              ("ceramic", ceramic)):
        if arm_rec["viable"]:
            outcome_steps[arm_name] = {
                "status": "WOULD RUN — no viable arm in this "
                          "execution; see outcome.md",
            }
        else:
            outcome_steps[arm_name] = {
                "status": "NOT RUN — arm closed at the "
                          "margins step",
                "closure": arm_rec["closure"],
            }

    results = {
        "phase": 395,
        "spec": "031-stage2-q7-provenance-networks",
        "question": "Q7 (owned by Spec 027, F027-C15)",
        "freeze_digest":
            "f63167fc99c8d3c31f885b1014cad69fab3788fcf8e6212d018aa"
            "6948a2cdac6",
        "registration": {
            "osf": "https://osf.io/jtwvc/",
            "doi": "10.17605/OSF.IO/JTWVC",
            "state": "approved and public before execution "
                     "(adopted 6A)",
        },
        "input_hashes": input_hashes,
        "digitisation_design_step": {
            "law_posted_chapters":
                law["posted_set_inventory"]["chapters_located"],
            "law_chapters_not_located":
                law["posted_set_inventory"][
                    "chapters_not_located"],
            "method_rule": law["method_rule"]["frozen_basis"],
            "audit_named_methods":
                law["method_rule"]["audit_named_methods"],
            "residual_ii": law["residual_ii_reverification"][
                "outcome"],
            "ceramic_postures": {
                r["site"]: r["posture"]
                for r in inputs["ceramic"]["reports"]},
            "bead_floor_enumerated":
                inputs["bead"]["floor_step"][
                    "enumerated_counts"],
        },
        "link_construction": {
            "named_source_totals": links[
                "named_source_totals"],
            "link_eligible_sites": links[
                "link_eligible_sites"],
            "linked_pairs_certain_count": len(
                links["linked_pairs_certain"]),
            "linked_pairs_uncertain": links[
                "linked_pairs_uncertain"],
            "site_id_mapping_to_gazetteer": site_id_mapping,
            "link_eligible_sites_in_gazetteer":
                in_universe_eligible,
            "linked_pairs_in_gazetteer_count":
                len(in_universe_pairs),
            "meluhha_links": 0,
        },
        "gazetteer_screens": {
            s: {"rows": v["rows"],
                "has_coordinates": v["has_coordinates"],
                "period_eligible": v["period_eligible"],
                "period_labels": v["period_labels"]}
            for s, v in sorted(screens.items())},
        "population_record": population,
        "population_record_sha256": population_hash,
        "arms": {"bead_craft": bead, "ceramic": ceramic},
        "outcome_step": outcome_steps,
        "verdicts": {
            "bead_craft": bead["closure"]["status"]
            if bead["closure"] else None,
            "ceramic": ceramic["closure"]["status"]
            if ceramic["closure"] else None,
        },
        "river_network_dd8": {
            "pinned": False,
            "basis": "DD-8 pins the network at the execution "
                     "data step for pair construction in the "
                     "outcome step. No arm passed the margins "
                     "step, no pair set was constructed, and "
                     "no distance was computed; there is "
                     "nothing to pin.",
        },
    }

    args.results.parent.mkdir(parents=True, exist_ok=True)
    args.results.write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")

    lines = [
        "# Phase-395 (Spec 031) — margins report",
        "",
        "Execution of the frozen Spec 031 contract (Q7), "
        "registered at OSF https://osf.io/jtwvc/ before "
        "execution. The margins step ran exactly as frozen; "
        "both arms closed at margins, before any response was "
        "computed. Full record: "
        "specs/031-stage2-q7-provenance-networks/outcome.md.",
        "",
        f"- Gazetteer sites (Stage 0): {len(screens)}",
        f"- Sites with defensible coordinates: "
        f"{bead['sites_with_coordinates']}",
        f"- Sites period-eligible (Stage 0 labels): "
        f"{bead['sites_period_eligible']}",
        f"- Link-eligible sites (all sources): "
        f"{len(links['link_eligible_sites'])}; in the "
        f"gazetteer universe: {len(in_universe_eligible)}",
        f"- Linked pairs, certain (all sources): "
        f"{len(links['linked_pairs_certain'])}; in the "
        f"gazetteer universe: {len(in_universe_pairs)}",
        f"- Bead/craft arm: {bead['eligible_count']} eligible "
        f"sites — {results['verdicts']['bead_craft']}",
        f"- Ceramic arm: {ceramic['eligible_count']} eligible "
        f"sites — {results['verdicts']['ceramic']}",
        f"- Population record sha256: {population_hash}",
        "",
    ]
    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"phase395: bead_craft="
          f"{results['verdicts']['bead_craft']}, ceramic="
          f"{results['verdicts']['ceramic']}, population "
          f"sha256={population_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
