"""Phase-127 (spec 021) — orchestration: load the frozen
inputs -> assert totals + anchors hash -> read the
Phase-125 judgeable set from the results of record ->
compute diagnostic arms (a)-(f) -> reports.

Executes the frozen protocol of
specs/021-phase127-cross-compilation-diagnostic/spec.md.
This phase does NOT re-score Phase-125 and issues no
verdict: the Phase-125 verdict (FAIL — DISAGREEMENT) is
final and is reported unchanged. Profiles are computed
strictly within each compilation; inscriptions are never
pooled; no object-level join is performed (spec 019
section 2.1). The composition controls of spec section 7
read Holdat stratum membership (site / iconography
columns) per inscription from the same CSV the
Phase-125 loader reads; stratum-inconsistent
inscriptions are counted and excluded from the affected
control. Holdat data is read from the gitignored
downloads area and never committed; only statistics are
published. The anchors file is never opened for writing;
its sha256 is asserted identical before and after.
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_BACKEND = _REPO / "backend"
sys.path.insert(0, str(_BACKEND))

from glossa_lab.data import mayig_layer as ml  # noqa: E402
from glossa_lab.data import (  # noqa: E402
    parpola_mahadevan_crosswalk_v1 as xw,
)
from glossa_lab.phase113_battery import CorpusContext  # noqa: E402
from glossa_lab.phase113_run import _gpu_device  # noqa: E402
from glossa_lab.phase125_cross_compilation import (  # noqa: E402
    FLOOR, profiles_from_context,
)
from glossa_lab.phase125_run import (  # noqa: E402
    ANCHORS_PATH, ANCHORS_SHA256, HOLDAT_EXPECTED, MAYIG_EXPECTED,
    _find_holdat_csv, _sha256, load_holdat_inscriptions,
)
from glossa_lab.phase127_diagnostic import (  # noqa: E402
    OBSERVED_MEDIAN_TV, bootstrap_arm, class_labels,
    evaluate_pairs_on_contexts, inscription_count_vectors,
    matched_size_arm, neighbourhood_decomposition, power_grid,
    split_half_arm,
)

RESULTS_PATH = _REPO / "reports" / "phase127_cross_compilation_diagnostic_results.json"
REPORT_PATH = _REPO / "reports" / "phase127_cross_compilation_diagnostic.md"
PHASE125_RESULTS = _REPO / "reports" / "phase125_cross_compilation_results.json"
SPEC = "specs/021-phase127-cross-compilation-diagnostic"
DATE = "2026-10-08"


def load_holdat_stratified(csv_path: Path) -> list[dict]:
    """Holdat inscriptions with per-inscription stratum
    values, grouped exactly as the Phase-125 loader
    groups (cisi_number + position). Each record:
    {tokens, sites: set, iconographies: set}."""
    seals: dict[str, list] = {}
    strata: dict[str, dict[str, set]] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals:
                seals[c] = []
                strata[c] = {"site": set(), "iconography": set()}
            while len(seals[c]) <= p:
                seals[c].append("")
            seals[c][p] = s
            if (row.get("site") or "").strip():
                strata[c]["site"].add(row["site"].strip())
            if (row.get("iconography") or "").strip():
                strata[c]["iconography"].add(row["iconography"].strip())
    out = []
    for c, toks in seals.items():
        tokens = [t for t in toks if t]
        if tokens:
            out.append({"tokens": tokens,
                        "sites": strata[c]["site"],
                        "iconographies": strata[c]["iconography"]})
    return out


def _fmt(x, nd=6):
    return "null" if x is None else f"{x:.{nd}f}"


def run_all(write: bool = True) -> dict:
    anchors_before = _sha256(ANCHORS_PATH)
    assert anchors_before == ANCHORS_SHA256, anchors_before

    # ── Frozen inputs (spec 021 section 2) ──
    mayig_records = ml.load_inscriptions()
    mayig_inscriptions = [list(r["tokens"]) for r in mayig_records]
    mayig_ctx = CorpusContext(mayig_inscriptions)
    assert len(mayig_inscriptions) == MAYIG_EXPECTED["inscriptions"]
    assert mayig_ctx.n_tokens == MAYIG_EXPECTED["tokens"]
    assert len(mayig_ctx.token_counts) == MAYIG_EXPECTED["signs"]
    # Metadata support facts (spec section 7): all mayig
    # objects are Mohenjo-daro M-series unicorn seals.
    assert all(r["cisi_object_id"].startswith("M-") for r in mayig_records)
    descriptions = sorted({r["description"] for r in mayig_records})
    assert all(d.startswith("unicorn") and d.endswith("seal")
               for d in descriptions), descriptions

    holdat_csv = _find_holdat_csv()
    holdat_inscriptions = load_holdat_inscriptions(holdat_csv)
    holdat_ctx = CorpusContext(holdat_inscriptions)
    assert len(holdat_inscriptions) == HOLDAT_EXPECTED["inscriptions"]
    assert holdat_ctx.n_tokens == HOLDAT_EXPECTED["tokens"]
    assert len(holdat_ctx.token_counts) == HOLDAT_EXPECTED["signs"]

    stratified = load_holdat_stratified(holdat_csv)
    assert [r["tokens"] for r in stratified] == holdat_inscriptions
    n_site_inconsistent = sum(1 for r in stratified if len(r["sites"]) != 1)
    n_icon_inconsistent = sum(
        1 for r in stratified if len(r["iconographies"]) != 1)

    rows = xw.load_crosswalk()
    assert xw.crosswalk_stats()["n_pairs"] == 762
    all_pairs = [{"parpola_id": r["parpola_id"],
                  "mahadevan_id": r["mahadevan_id"],
                  "confidence": r["confidence"]}
                 for r in rows if r.get("mahadevan_id")]

    # ── The fixed judgeable set (from Phase-125 record) ──
    p125 = json.loads(PHASE125_RESULTS.read_text(encoding="utf-8"))
    primary_records = p125["arms"]["primary"]["records"]
    judged = [r for r in primary_records if r["judgeable"]]
    assert len(judged) == 16, len(judged)
    assert p125["arms"]["primary"]["stats"]["median_tv"] == OBSERVED_MEDIAN_TV
    assert p125["verdict"]["verdict"] == "FAIL"
    pairs = [{"parpola_id": r["parpola_id"],
              "mahadevan_id": r["mahadevan_id"]} for r in judged]
    pair_keys = [f"{p['parpola_id']}-{p['mahadevan_id']}" for p in pairs]

    # Holdat token pools + mayig sizes, keyed by pair.
    pools, sizes = {}, {}
    for pair, key, rec in zip(pairs, pair_keys, judged, strict=True):
        pools[key] = class_labels(holdat_inscriptions, pair["mahadevan_id"])
        assert len(pools[key]) == rec["holdat_n"]
        sizes[key] = rec["mayig_n"]

    # ── Arm (a): split-half ──
    arm_a = split_half_arm(pools)
    # ── Arm (b): matched-size ──
    arm_b = matched_size_arm(pools, sizes)
    # ── Arm (f): power grid (same pools) ──
    arm_f = power_grid(pools)

    # ── Arm (c): inscription bootstrap ──
    mayig_vectors = inscription_count_vectors(
        mayig_inscriptions, [p["parpola_id"] for p in pairs])
    holdat_vectors = inscription_count_vectors(
        holdat_inscriptions, [p["mahadevan_id"] for p in pairs])
    arm_c = bootstrap_arm(
        mayig_vectors, holdat_vectors,
        [(p["parpola_id"], p["mahadevan_id"]) for p in pairs])

    # ── Arm (d): neighbourhood decomposition ──
    tv_cache: dict = {}

    def tv_lookup(p_sign, m_sign):
        key = (p_sign, m_sign)
        if key not in tv_cache:
            pp, pn = profiles_from_context(mayig_ctx, p_sign)
            hp, hn = profiles_from_context(holdat_ctx, m_sign)
            if pp is None or hp is None or pn < FLOOR or hn < FLOOR:
                tv_cache[key] = None
            else:
                from glossa_lab.phase113_battery import tv_distance
                tv_cache[key] = tv_distance(pp, hp)
        return tv_cache[key]

    arm_d_records = [neighbourhood_decomposition(all_pairs, pair, tv_lookup)
                     for pair in pairs]
    amb_shares = [r["ambiguity_share"] for r in arm_d_records
                  if r["ambiguity_share"] is not None]
    attr = [r["attributable_tv"] for r in arm_d_records
            if r["attributable_tv"] is not None]
    attr_shares = [r["attributable_share"] for r in arm_d_records
                   if r["attributable_share"] is not None]
    from glossa_lab.phase125_cross_compilation import median as _median
    arm_d = {
        "records": arm_d_records,
        "median_ambiguity_share": (
            round(_median(amb_shares), 6) if amb_shares else None),
        "median_attributable_tv": (
            round(_median(attr), 6) if attr else None),
        "median_attributable_share": (
            round(_median(attr_shares), 6) if attr_shares else None),
        "n_pairs_no_judgeable_neighbourhood": sum(
            1 for r in arm_d_records if r["neighbourhood_median_tv"] is None),
        "construction_note": "PRIMARY pairs are unambiguous within the "
                             "high-confidence set by construction (spec 019 "
                             "section 3): ambiguous mappings contribute "
                             "exactly zero to the Phase-125 PRIMARY TVs. "
                             "This arm prices the counterfactual under the "
                             "spec 021 section 6 estimator.",
    }

    # ── Arm (e): composition controls ──
    def restricted_ctx(pred):
        return CorpusContext([r["tokens"] for r in stratified if pred(r)])

    controls = {}
    control_defs = {
        "site_mohenjo_daro": (
            "Holdat restricted to site = Mohenjo-daro",
            lambda r: r["sites"] == {"Mohenjo-daro"}),
        "iconography_unicorn": (
            "Holdat restricted to iconography = unicorn",
            lambda r: r["iconographies"] == {"unicorn"}),
        "site_and_iconography": (
            "Holdat restricted to site = Mohenjo-daro AND "
            "iconography = unicorn",
            lambda r: r["sites"] == {"Mohenjo-daro"}
            and r["iconographies"] == {"unicorn"}),
    }
    for name, (label, pred) in control_defs.items():
        ctx = restricted_ctx(pred)
        ev = evaluate_pairs_on_contexts(pairs, mayig_ctx, ctx, floor=FLOOR)
        controls[name] = {"definition": label,
                          "n_holdat_inscriptions": ctx.n_inscriptions,
                          "n_holdat_tokens": ctx.n_tokens, **ev}
    arm_e = {
        "controls": controls,
        "n_site_inconsistent_inscriptions": n_site_inconsistent,
        "n_iconography_inconsistent_inscriptions": n_icon_inconsistent,
        "mayig_side": "No restriction applied or possible: all 179 mayig "
                      "inscriptions are Mohenjo-daro (M-series) unicorn "
                      "seals, so the mayig side is already entirely "
                      "inside every controlled stratum.",
        "gaps": [
            "mayig unicorn variants (I-V) have no counterpart granularity "
            "in Holdat's iconography column (single 'unicorn' value): "
            "variant-level composition cannot be controlled.",
            "The mayig layer has no non-Mohenjo-daro site, no non-seal "
            "object type, and no non-unicorn iconography: no mayig-side "
            "stratum restriction is possible, and no stratum beyond site "
            "and iconography exists on both sides.",
            "Provenience finer than site, artefact material, and find "
            "context are absent from the mayig layer metadata and cannot "
            "be controlled.",
            "Inscription-length composition is token data, not layer "
            "metadata; it is outside arm (e)'s registered scope and is "
            "not controlled.",
        ],
    }

    results = {
        "phase": 127,
        "spec": SPEC,
        "date": DATE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gpu_device": _gpu_device(),
        "phase125_verdict_of_record": {
            "verdict": "FAIL", "substate": "DISAGREEMENT",
            "median_tv": OBSERVED_MEDIAN_TV,
            "spearman_initial": p125["arms"]["primary"]["stats"]["spearman_initial"],
            "spearman_terminal": p125["arms"]["primary"]["stats"]["spearman_terminal"],
            "p_null": p125["arms"]["primary"]["stats"]["null"]["p_null"],
            "n_judgeable": 16, "n_primary_pairs": 286,
            "status": "FINAL — unchanged by this diagnostic (spec 021 "
                      "section 0 non-goals)",
        },
        "inputs": {
            "mayig_layer": {"inscriptions": 179, "tokens": 1003,
                            "signs": 182, "descriptions": descriptions},
            "holdat": {"inscriptions": 1670, "tokens": 7002, "signs": 390},
            "crosswalk": {"n_pairs": 762,
                          "confidence_breakdown":
                          xw.crosswalk_stats()["confidence_breakdown"]},
            "judgeable_set": "the 16 Phase-125 PRIMARY judgeable pairs, "
                             "read from reports/"
                             "phase125_cross_compilation_results.json",
        },
        "arms": {
            "a_split_half": arm_a,
            "b_matched_size": arm_b,
            "c_bootstrap": arm_c,
            "d_crosswalk_decomposition": arm_d,
            "e_composition": arm_e,
            "f_power": arm_f,
        },
        "anchors_sha256_before": anchors_before,
    }
    anchors_after = _sha256(ANCHORS_PATH)
    assert anchors_after == anchors_before
    results["anchors_sha256_after"] = anchors_after
    results["anchors_unchanged"] = anchors_after == anchors_before

    if write:
        RESULTS_PATH.write_text(
            json.dumps(results, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8")
        REPORT_PATH.write_text(_report(results), encoding="utf-8")
    return results


def _report(r: dict) -> str:
    a = r["arms"]["a_split_half"]
    b = r["arms"]["b_matched_size"]
    c = r["arms"]["c_bootstrap"]
    d = r["arms"]["d_crosswalk_decomposition"]
    e = r["arms"]["e_composition"]
    f = r["arms"]["f_power"]
    bd = b["median_tv_distribution"]
    req_med = f["tokens_per_sign_required_median_gate"]
    req_per = f["tokens_per_sign_required_per_sign"]
    power_line = (
        f"tokens-per-sign required for the median-TV gate to clear the "
        f"noise criterion (95th percentile of the replicate median TV "
        f"≤ 0.35): **{req_med}** (grid maximum 256; "
        f"{'reached within the grid' if req_med else 'NOT reached within the grid — reported without extrapolation'}); "
        f"per-sign criterion (pooled per-sign 95th percentile ≤ 0.35): "
        f"**{req_per}**"
        + ("" if req_per else " (not reached within the grid)"))
    ctrl_rows = "\n".join(
        f"| {name} | {ctl['n_holdat_inscriptions']} | "
        f"{ctl['n_judgeable']} | {_fmt(ctl['median_tv'])} |"
        for name, ctl in e["controls"].items())
    d_rows = "\n".join(
        f"| {rec['parpola_id']}-{rec['mahadevan_id']} | "
        f"{rec['neighbourhood_size']} | {_fmt(rec['ambiguity_share'])} | "
        f"{_fmt(rec['tv_primary'])} | "
        f"{_fmt(rec['neighbourhood_median_tv'])} | "
        f"{_fmt(rec['attributable_tv'])} | {_fmt(rec['attributable_share'])} |"
        for rec in d["records"])
    return f"""# Phase-127 — Cross-Compilation Disagreement Diagnostic (spec 021)

**The Phase-125 verdict is FAIL — DISAGREEMENT, and it is FINAL.**
**This diagnostic does not re-score Phase-125, does not issue any
verdict, and no finding below softens, qualifies, or re-opens that
verdict.** Phase-125 (spec 019, PRIMARY arm): 16 judgeable pairs of
286; median TV 0.636931; Spearman ρ initial −0.424758 / terminal
0.316034; pairing-shuffle null p = 0.824. What follows decomposes
the *observed distances* of that finished result — how much of
them sampling noise, crosswalk ambiguity, and population
composition can account for, at the observed sizes — under the
estimators frozen in spec 021 before any diagnostic statistic
existed. **Spec:** {SPEC} · **Date:** {DATE} · **GPU device:** {r['gpu_device']}

## Headline decomposition

| Component | Figure | Reading |
|---|---|---|
| Observed median TV (Phase-125, of record) | 0.636931 | the quantity being decomposed |
| (a) Split-half noise floor, raw (median of per-sign medians) | {_fmt(a['noise_floor_median_tv'])} | TV between two halves of the *same* Holdat sign pool |
| (a) Split-half noise floor, full-size estimate (÷ √2) | {_fmt(a['noise_floor_fullsize_est'])} | within-Holdat sampling noise at full Holdat sizes |
| (b) Matched-size expected median TV (Holdat at mayig sizes) | {_fmt(bd['median'])} (95% interval {_fmt(bd['ci95_lo'])}–{_fmt(bd['ci95_hi'])}) | pure Holdat-internal sampling, at the token counts mayig actually has |
| (b) Share of matched-size replicates with median TV ≥ observed | {_fmt(bd['share_replicates_ge_observed'])} | how often sampling alone reaches the observed median |
| (c) Bootstrap CI for the median TV | {_fmt(c['median_tv']['ci95_lo'])}–{_fmt(c['median_tv']['ci95_hi'])} (bootstrap median {_fmt(c['median_tv']['median'])}) | inscription-level resampling of *both* compilations |
| (d) Median ambiguity share per judgeable pair | {_fmt(d['median_ambiguity_share'])} | share of each pair's crosswalk neighbourhood that is not the primary pair (primary TVs themselves contain zero ambiguity by construction — §(d)) |
| (d) Median attributable TV (spec §6 estimator) | {_fmt(d['median_attributable_tv'])} (share {_fmt(d['median_attributable_share'])}) | primary TV minus neighbourhood median TV |
| (f) Power | {power_line} | derived from arm (b)'s machinery, spec §8 method |

## (a) Holdat split-half noise floor (spec §3; B = 999 per sign, seed 127001)

Per-sign medians and intervals are in the results JSON. The
split-half statistic compares two halves (≈ n/2 tokens each) of a
single Holdat sign pool, so it prices a comparison at half size;
the full-size estimate divides by √2 (registered multinomial
scaling approximation). Token-level caveat (spec A3): tokens
within an inscription are not independent, so token-level nulls
understate clustered noise; arm (c) is the cluster-respecting
statement.

## (b) Matched-size subsampling null (spec §4; B = 999, seed 127002)

For each pair, Holdat tokens are subsampled without replacement
to exactly the mayig token count for that sign; the primary
statistic is TV(subsample, disjoint remainder). Expected median
TV under pure Holdat-internal sampling at mayig's sizes:
**{_fmt(bd['median'])}**, vs the observed cross-compilation
median 0.636931; sampling alone reached or exceeded the observed
median in a share {_fmt(bd['share_replicates_ge_observed'])} of
replicates. Registered limitation: this arm prices Holdat-side
noise only; mayig-side noise is priced by arm (c). The arms are
reported together and never averaged.

## (c) Inscription bootstrap CIs (spec §5; B = 999, seed 127003)

Inscriptions of each compilation were resampled with
replacement, independently (179 mayig / 1,670 Holdat per
replicate), profiles recomputed within each resampled
compilation, and the fixed 16-pair set re-evaluated. Per-pair
CIs are in the results JSON. The median-TV bootstrap CI is
**{_fmt(c['median_tv']['ci95_lo'])}–{_fmt(c['median_tv']['ci95_hi'])}**.
Pairs excluded from a replicate only when a resampled sign had
0 tokens; exclusion counts are recorded per pair in the JSON.

## (d) Crosswalk arm decomposition (spec §6)

The Phase-125 PRIMARY arm admits only pairs unambiguous within
the high-confidence set, so **ambiguous mappings contribute
exactly zero to the primary TVs by construction**; this arm
prices the counterfactual — the same signs under the ambiguous
mappings the primary arm excluded. Estimator (frozen in spec
§6): attributable TV = TV_primary − median TV of the pair's
judgeable neighbourhood comparisons; a positive value means the
primary mapping disagrees *more* than the ambiguous
alternatives typically do (ambiguity is not what produces that
pair's disagreement, under this estimator); a negative value
means the alternatives disagree more. Pairs with no judgeable
neighbourhood comparison: {d['n_pairs_no_judgeable_neighbourhood']}.

| Pair | Neighbourhood | Ambiguity share | TV primary | Neighbourhood median TV | Attributable TV | Attributable share |
|---|---|---|---|---|---|---|
{d_rows}

## (e) Composition controls (spec §7)

Holdat-side restrictions only — the mayig side (all 179
inscriptions Mohenjo-daro, all unicorn seals) is already
entirely inside every stratum. The frozen floor 8 is re-applied
to the restricted Holdat counts; medians are over each
control's own judgeable set. Phase-125 median of record:
0.636931 over 16 judgeable.

| Control | Holdat inscriptions | Judgeable | Median TV |
|---|---|---|---|
{ctrl_rows}

Stratum-inconsistent inscriptions (rows disagreeing on the
stratum value; counted and excluded from the affected control,
never silently assigned): site {e['n_site_inconsistent_inscriptions']},
iconography {e['n_iconography_inconsistent_inscriptions']}.

**Gaps (stated, not improvised):**

- mayig unicorn variants (I–V) have no counterpart granularity
  in Holdat's iconography column (single 'unicorn' value):
  variant-level composition cannot be controlled.
- The mayig layer has no non-Mohenjo-daro site, no non-seal
  object type, and no non-unicorn iconography: no mayig-side
  stratum restriction is possible, and no stratum beyond site
  and iconography exists on both sides.
- Provenience finer than site, artefact material, and find
  context are absent from the mayig layer metadata and cannot
  be controlled.
- Inscription-length composition is token data, not layer
  metadata; it is outside this arm's registered scope and is
  not controlled.

## (f) Power statement (spec §8; B = 499 per grid point, seed 127004)

{power_line}. Method: for each grid size, TV(subsample,
disjoint remainder) over the judgeable Holdat pools — pure
sampling noise at that size; the criterion is the size at
which that noise's 95th percentile falls to the frozen
Phase-125 PASS bound 0.35. The full grid is in the results
JSON. This statement is about the gates' informativeness at
the observed effect scale; it re-opens no gate and re-judges
no pair. Grid-shape note: the pooled per-sign 95th
percentile is not monotone at the largest grid points
(128–256), where few signs contribute (pools no larger than
the grid size are excluded) and the disjoint remainder —
the comparison reference — becomes small, so remainder-side
noise dominates; the registered criterion is the *smallest*
qualifying grid size, which is reached at the grid's first
point on both criteria, so the tail shape does not affect
the statement.

## Claim scope (spec §9)

Every figure above is a statement about the 16 judgeable
primary pairs and the frozen Phase-125 design — never about
the script as a whole, any individual pair's crosswalk
correctness, any below-floor or ambiguous pair's identity, or
Holdat vs the ICIT lineage (Phase-116 R-NONE stands
untouched). "Genuine" in this report's vocabulary means
exactly: not accounted for by the §§3–5 sampling nulls, the
§6 mapping-choice estimator, or the §7 controls, at the
observed sizes; it does not attribute the residual to any
side or mechanism. **The Phase-125 verdict — FAIL —
DISAGREEMENT — is unchanged by anything in this report.**

## Inputs and guards

- mayig layer: 179 inscriptions / 1,003 tokens / 182 P signs;
  Holdat: 1,670 inscriptions / 7,002 tokens / 390 M signs;
  crosswalk v1: 762 pairs (high 372 / medium 0 / low 390) —
  all asserted in code against the frozen totals.
- No object-level join was performed; no inscriptions were
  pooled across compilations; Phase-125 artifacts were read,
  never modified.
- Anchors file unchanged: sha256 {r['anchors_sha256_after']}
  before and after (asserted in code).

## Deviations

None in the frozen arms, estimators, seeds, replicate counts,
grids, or interval methods. One filename deviation, recorded
per spec §11: the graph module is
`backend/glossa_lab/experiment_graph_phase127_diagnostic.py`
(not `experiment_graph_phase127.py` as listed in spec §10.4),
because that filename is already taken by a legacy
experiment-graph node family (Gulf corpus / Roif mining /
fish site polysemy) that predates the ledger-sequence
numbering — the Phase-126 Wells precedent
(`experiment_graph_phase126_wells.py`). The registered node
id is exactly as specified:
`IndusPhase127CrossCompilationDiagnostic`. (Verification
counts are recorded in the ledger entries for this phase.)

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
section VI.
"""


if __name__ == "__main__":
    out = run_all()
    print(json.dumps({
        "a": out["arms"]["a_split_half"]["noise_floor_median_tv"],
        "b_median": out["arms"]["b_matched_size"]["median_tv_distribution"],
        "c_median_tv": out["arms"]["c_bootstrap"]["median_tv"],
        "f_required": out["arms"]["f_power"][
            "tokens_per_sign_required_median_gate"],
        "anchors_unchanged": out["anchors_unchanged"],
    }, indent=1))
