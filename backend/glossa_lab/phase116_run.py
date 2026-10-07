"""Phase-116 (spec 015) — corpus-harmonization study run.

Orchestration: load the keyed layers, audit the conversion,
recompute the Phase-115 T1 baseline and ASSERT it reproduces
the published record (spec section 3), then execute the frozen
matcher (section 4) and hypothesis arms (section 5), assemble
verdicts and the section 6 recommendation mechanically, and
write reports/phase116_harmonization_results.json +
reports/phase116_harmonization_summary.md.

DIAGNOSTIC ONLY: the anchors file is read (for the STRICT94
set definition, via phase113's compute_sets) and never written.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_BACKEND = _REPO / "backend"
_MAIN_REPO = Path.home() / "workspace" / "glossa-lab"
sys.path.insert(0, str(_BACKEND))

from glossa_lab.phase113_battery import (  # noqa: E402
    FAIL, PASS, CorpusContext, modal_class, tv_distance,
)
from glossa_lab.phase113_run import compute_sets  # noqa: E402
from glossa_lab.phase116_harmonization import (  # noqa: E402
    assemble_recommendation, audit_conversion, code_is_ambiguous,
    find_downloads, five_bin_profile, five_bin_profiles,
    kept_records, load_holdat_keyed, load_keyed_layer, modal_bin,
    norm_cisi_key, norm_site, normalize_code, p_to_m_map,
    permutation_family, population_records, registry_audit,
    relative_positions, run_matcher, spearman, stripped_context,
    test_t1_v2, verdict_composition, verdict_d1, verdict_d2,
    verdict_definition, verdict_direction, verdict_mapping,
    verdict_s1, verdict_s2, verdict_segmentation, wasserstein1,
)

ANCHORS_PATH = _BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
REGISTER_PATH = _REPO / "reports" / "phase108_provenance_register.json"
RESULTS_PATH = _REPO / "reports" / "phase116_harmonization_results.json"
SUMMARY_PATH = _REPO / "reports" / "phase116_harmonization_summary.md"
SPEC = "specs/015-phase116-corpus-harmonization"
DATE = "2026-10-07"


def _gpu_device() -> str:
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:  # noqa: BLE001
        return "cpu (torch absent)"


def _modal_agreement(signs, ctx_a, ctx_b):
    """(modal agreement share, mean TV) over signs with profiles
    in both contexts."""
    agree, tvs = 0, []
    for s in signs:
        pa, pb = ctx_a.profile(s), ctx_b.profile(s)
        if pa is None or pb is None:
            continue
        if modal_class(pa) == modal_class(pb):
            agree += 1
        tvs.append(tv_distance(pa, pb))
    n = len(tvs)
    return (agree / n if n else 0.0), (sum(tvs) / n if n else 0.0), n


def _len_stats(seqs):
    lens = [len(s) for s in seqs]
    return {"n": len(lens),
            "mean_len": round(sum(lens) / len(lens), 4) if lens else 0.0,
            "median_len": statistics.median(lens) if lens else 0,
            "share_len_le2": round(
                sum(1 for x in lens if x <= 2) / len(lens), 4) if lens else 0.0,
            "max_len": max(lens) if lens else 0}


def run_all() -> dict:
    downloads = find_downloads(_REPO, _MAIN_REPO)
    holdat_ins, holdat_sites = load_holdat_keyed(
        downloads / "external_repos" / "holdatllc_indus"
        / "indus_corpus 2.csv")
    records = load_keyed_layer(
        downloads / "icit_fieldcady" / "icit_converted_v2_keyed.json")
    kept = kept_records(records)
    pop = population_records(records)
    assert len(holdat_ins) == 1670
    assert len(kept) == 4531 and len(pop) == 4614

    holdat = CorpusContext(list(holdat_ins.values()))
    icit = CorpusContext([r["tokens"] for r in kept])
    mapped = sum(1 for r in kept for t in r["tokens"] if t != "UNK")
    sentinels = sum(1 for r in kept for t in r["tokens"] if t == "UNK")
    assert mapped == 13492 and sentinels == 2388
    ratio = mapped / holdat.n_tokens

    # Conversion audit: every population token recomputed from
    # its stored source code must equal the stored token.
    audit, w2m, w2p = registry_audit(
        _REPO / "data/crosswalks/canonical_sign_registry.csv")
    p2m = p_to_m_map(
        _BACKEND / "glossa_lab/data/mahadevan_parpola_crosswalk_v2.json")
    n_audited = audit_conversion(pop, w2m, w2p, p2m)

    anchors = json.loads(ANCHORS_PATH.read_text("utf-8"))["anchors"]
    register = json.loads(REGISTER_PATH.read_text("utf-8"))
    sets = compute_sets(anchors, register)
    strict = sorted(sets["strict94"])

    # ── Section 3 baseline: recompute T1 v2 and assert the
    # published Phase-115 record before any arm executes.
    baseline = {s: test_t1_v2(s, holdat, icit, ratio) for s in strict}
    judged = {s: t for s, t in baseline.items()
              if t["state"] in (PASS, FAIL)}
    fails = {s: t for s, t in judged.items() if t["state"] == FAIL}
    n_modal_dis = sum(1 for t in fails.values()
                      if t["modal_holdat"] != t["modal_icit"])
    med_tv = statistics.median(t["tv"] for t in fails.values())
    mean_tv = statistics.mean(t["tv"] for t in judged.values())
    assert len(judged) == 51, len(judged)
    assert sum(1 for t in judged.values() if t["state"] == PASS) == 8
    assert len(fails) == 43, len(fails)
    assert n_modal_dis == 40, n_modal_dis
    assert len(fails) - n_modal_dis == 3
    assert abs(med_tv - 0.789474) <= 0.0005, med_tv
    assert abs(mean_tv - 0.657011) <= 0.0005, mean_tv
    j51 = sorted(judged)
    tv_full = {s: judged[s]["tv"] for s in j51}
    a_full, _, _ = _modal_agreement(j51, holdat, icit)
    assert abs(a_full - 11 / 51) < 1e-9

    # ── Section 4 matcher.
    holdat_items = list(holdat_ins.items())
    m = run_matcher(holdat_items, pop)
    tier_a, tier_b, tier_c = m["tier_a"], m["tier_b"], m["tier_c"]

    # ── Section 5.0 permutation context (full layers).
    perm_full = permutation_family(j51, holdat, icit)

    # ── Section 5.1 H-COMPOSITION.
    holdat_r = CorpusContext([holdat_items[h][1] for h, _ in tier_a])
    icit_r = CorpusContext([pop[i]["tokens"] for _, i in tier_a])
    j51r = [s for s in j51
            if holdat_r.token_count(s) >= 3 and icit_r.token_count(s) >= 3]
    powered = len(tier_a) >= 100 and len(j51r) >= 15
    a_restr, tv_restr, _ = _modal_agreement(j51r, holdat_r, icit_r)
    a_full_sub, tv_full_sub, _ = _modal_agreement(j51r, holdat, icit)
    v_comp = verdict_composition(powered, a_restr, tv_restr,
                                  a_full_sub, tv_full_sub)
    perm_restr = permutation_family(j51r, holdat_r, icit_r) if j51r else {
        "n_tests": 0, "n_significant_bh": 0, "per_sign": {}}
    # Secondary arm: site/material/type mix (descriptive).
    h_site_tokens = Counter()
    for hid, seq in holdat_ins.items():
        h_site_tokens[norm_site(holdat_sites[hid])] += len(seq)
    i_site_tokens = Counter()
    for r in kept:
        i_site_tokens[norm_site(r["site"])] += len(r["tokens"])
    h_total, i_total = sum(h_site_tokens.values()), sum(i_site_tokens.values())
    site_mix = []
    for site in sorted(set(h_site_tokens) | set(i_site_tokens)):
        hs = h_site_tokens.get(site, 0) / h_total
        is_ = i_site_tokens.get(site, 0) / i_total
        if hs >= 0.01 or is_ >= 0.01:
            site_mix.append({"site_normalized": site,
                             "holdat_share": round(hs, 4),
                             "icit_share": round(is_, 4)})
    site_mix.sort(key=lambda d: -max(d["holdat_share"], d["icit_share"]))
    icit_unmatched_site_share = round(
        sum(v for k, v in i_site_tokens.items()
            if k not in h_site_tokens) / i_total, 4)

    # ── Section 5.2 H-SEGMENTATION.
    stripped = stripped_context(records)
    s1 = {s: test_t1_v2(s, holdat, icit, ratio, profile_source=stripped)
          for s in strict}
    f1 = sum(1 for t in s1.values() if t["state"] == FAIL)
    v_s1 = verdict_s1(f1)
    # S2: artifact units over matched artifacts (Tier A union C).
    matched_h = sorted({h for h, _ in tier_a} | {h for h, _ in tier_c})
    group_keys = {}
    for h in matched_h:
        partner = next(pop[i] for hh, i in tier_a + tier_c if hh == h)
        group_keys[h] = norm_cisi_key(partner["cisi"], partner["row"])
    wanted = set(group_keys.values())
    groups: dict[str, list] = defaultdict(list)
    for r in pop:
        k = norm_cisi_key(r["cisi"], r["row"])
        if k in wanted:
            groups[k].append(r)
    row_seqs = [r["tokens"] for k in sorted(groups) for r in groups[k]]
    art_seqs = [[t for r in groups[k] for t in r["tokens"]]
                for k in sorted(groups)]
    holdat_m = CorpusContext([holdat_items[h][1] for h in matched_h])
    row_ctx = CorpusContext(row_seqs)
    art_ctx = CorpusContext(art_seqs)
    j51u = [s for s in j51
            if holdat_m.token_count(s) >= 3
            and row_ctx.token_count(s) >= 3
            and art_ctx.token_count(s) >= 3]
    _, tv_row, _ = _modal_agreement(j51u, holdat_m, row_ctx)
    _, tv_art, _ = _modal_agreement(j51u, holdat_m, art_ctx)
    v_s2 = verdict_s2(len(j51u) >= 15, tv_art, tv_row)
    v_seg = verdict_segmentation(v_s1, v_s2)
    # S3 descriptives.
    demoted: dict[str, list] = defaultdict(lambda: [0, 0])
    for r in kept:
        spos = 0
        for pos, tok in enumerate(r["tokens"]):
            if tok == "UNK":
                continue
            if spos == 0:
                demoted[tok][0] += 1
                if pos > 0:
                    demoted[tok][1] += 1
            spos += 1
    demoted_shares = [demoted[s][1] / demoted[s][0]
                      for s in j51 if demoted[s][0] > 0]
    s3 = {
        "length_holdat_full": _len_stats(holdat.inscriptions),
        "length_icit_full": _len_stats(icit.inscriptions),
        "length_holdat_matched": _len_stats(
            [holdat_items[h][1] for h, _ in tier_a]),
        "length_icit_matched": _len_stats(
            [pop[i]["tokens"] for _, i in tier_a]),
        "leading_sentinel_rate": round(
            sum(1 for r in kept if r["tokens"] and r["tokens"][0] == "UNK")
            / len(kept), 4),
        "median_demoted_initial_share_j51": round(
            statistics.median(demoted_shares), 4) if demoted_shares else 0.0,
    }

    # ── Section 5.3 H-MAPPING.
    per_sign_map: dict[str, dict] = {}
    for s in j51:
        per_sign_map[s] = {"n_direct": 0, "n_chain": 0,
                           "codes": {}, "amb_tokens": 0}
    for r in kept:
        for tok, kind, raw in zip(r["tokens"], r["kinds"], r["codes"]):
            if tok not in per_sign_map or kind not in ("direct", "chain"):
                continue
            d = per_sign_map[tok]
            d[f"n_{kind}"] += 1
            code = normalize_code(raw)
            cd = d["codes"].setdefault(code, {"count": 0, "kind": kind})
            assert cd["kind"] == kind
            cd["count"] += 1
            if code_is_ambiguous(audit, code):
                d["amb_tokens"] += 1
    for s, d in per_sign_map.items():
        tot = d["n_direct"] + d["n_chain"]
        d["chain_share"] = round(d["n_chain"] / tot, 4) if tot else 0.0
        d["amb_share"] = round(d["amb_tokens"] / tot, 4) if tot else 0.0
        d["n_codes"] = len(d["codes"])
        d["n_icit_tokens"] = tot
        d["tv_full"] = tv_full[s]
    total_tv = sum(tv_full.values())
    by_tv = sorted(j51, key=lambda s: (-tv_full[s], s))
    top5_share = round(sum(tv_full[s] for s in by_tv[:5]) / total_tv, 4)
    top10_share = round(sum(tv_full[s] for s in by_tv[:10]) / total_tv, 4)
    heavy = [s for s in j51
             if per_sign_map[s]["chain_share"] > 0.5
             and baseline[s]["n_icit_tokens"] >= 3]
    clean = [s for s in j51
             if per_sign_map[s]["chain_share"] == 0
             and baseline[s]["n_icit_tokens"] >= 3]
    delta = None
    if heavy and clean:
        delta = round(statistics.mean(tv_full[s] for s in heavy)
                      - statistics.mean(tv_full[s] for s in clean), 4)
    groups_ok = len(heavy) >= 5 and len(clean) >= 5
    v_map = verdict_mapping(top10_share, delta if groups_ok else None,
                             groups_ok)
    audit_table = []
    for s in by_tv[:10]:
        codes = []
        for code, cd in sorted(per_sign_map[s]["codes"].items(),
                               key=lambda kv: (-kv[1]["count"], kv[0])):
            e = audit.get(code, {"m_ids": set(), "multi_row": False})
            codes.append({
                "wells_code": code, "count": cd["count"],
                "kind": cd["kind"],
                "parpola_id": w2p.get(code) if cd["kind"] == "chain" else None,
                "registry_m_ids": sorted(e["m_ids"]),
                "registry_multi_row": bool(e["multi_row"]),
                "ambiguous": code_is_ambiguous(audit, code)})
        audit_table.append({"sign": s, "tv_full": tv_full[s],
                            "modal_holdat": judged[s]["modal_holdat"],
                            "modal_icit": judged[s]["modal_icit"],
                            "chain_share": per_sign_map[s]["chain_share"],
                            "amb_share": per_sign_map[s]["amb_share"],
                            "codes": codes})

    # ── Section 5.4 H-DIRECTION.
    n_a, n_b = len(tier_a), len(tier_b)
    rev_share = round(n_b / (n_a + n_b), 4) if (n_a + n_b) else 0.0
    v_d1 = verdict_d1(n_a + n_b >= 50, rev_share)
    flipped = CorpusContext([list(reversed(r["tokens"])) for r in kept])
    a_flip, _, _ = _modal_agreement(j51, holdat, flipped)
    v_d2 = verdict_d2(a_flip, a_full)
    v_dir = verdict_direction(v_d1, v_d2)

    # ── Section 5.5 H-DEFINITION.
    def_detail = {}
    w1s, mean_pairs = [], []
    a5_agree = 0
    for s in j51:
        xs = relative_positions(holdat.inscriptions, s)
        ys = relative_positions(icit.inscriptions, s)
        w1 = wasserstein1(xs, ys)
        ch = five_bin_profiles(holdat.inscriptions, s)
        ci = five_bin_profiles(icit.inscriptions, s)
        ph, pi = five_bin_profile(ch), five_bin_profile(ci)
        tv5 = tv_distance(ph, pi)
        mb_h, mb_i = modal_bin(ph), modal_bin(pi)
        if mb_h == mb_i:
            a5_agree += 1
        def_detail[s] = {"w1": round(w1, 6),
                         "mean_r_holdat": round(sum(xs) / len(xs), 4),
                         "mean_r_icit": round(sum(ys) / len(ys), 4),
                         "tv5": round(tv5, 6),
                         "modal_bin_holdat": mb_h, "modal_bin_icit": mb_i}
        w1s.append(w1)
        mean_pairs.append((sum(xs) / len(xs), sum(ys) / len(ys)))
    median_w1 = round(statistics.median(w1s), 6)
    material_share = round(sum(1 for w in w1s if w > 0.20) / len(w1s), 4)
    rho = round(spearman([p[0] for p in mean_pairs],
                         [p[1] for p in mean_pairs]), 4)
    a5 = round(a5_agree / len(j51), 4)
    v_def = verdict_definition(median_w1, material_share, a5)

    verdicts = {"composition": v_comp, "segmentation": v_seg,
                "mapping": v_map, "direction": v_dir,
                "definition": v_def}
    recommendation = assemble_recommendation(
        verdicts, {"s1": v_s1, "s2": v_s2})

    results = {
        "phase": 116, "spec": SPEC, "date": DATE,
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "gpu_device": _gpu_device(),
        "diagnostic_only": True,
        "layers": {
            "holdat": {"inscriptions": holdat.n_inscriptions,
                       "tokens": holdat.n_tokens},
            "icit_v2_kept": {"inscriptions": len(kept),
                             "mapped_tokens": mapped,
                             "sentinel_tokens": sentinels,
                             "token_map_coverage_excl_placeholders": 0.91554},
            "matcher_population": len(pop),
            "conversion_audit_tokens": n_audited,
            "sampling_ratio_r": round(ratio, 6)},
        "baseline": {
            "judged": len(judged),
            "pass": sum(1 for t in judged.values() if t["state"] == PASS),
            "fail": len(fails), "modal_disagreement_failures": n_modal_dis,
            "same_modal_failures": len(fails) - n_modal_dis,
            "median_tv_failures": round(med_tv, 6),
            "mean_tv_judged": round(mean_tv, 6),
            "a_full": round(a_full, 4), "j51": j51,
            "per_sign": {s: baseline[s] for s in j51}},
        "matcher": {
            "tier_a_pairs": n_a, "tier_b_pairs": n_b,
            "tier_c_pairs": len(tier_c),
            "ambiguous_orientation_pairs": m["ambiguous_pairs"],
            "compat_direct_pairs": m["compat_direct_pairs"],
            "compat_reversed_pairs": m["compat_reversed_pairs"],
            "containment_candidates": m["containment_candidates"],
            "tier_a_pairs_by_length": dict(sorted(Counter(
                len(holdat_items[h][1]) for h, _ in tier_a).items()))},
        "arms": {
            "permutation_context": {
                "full_layers": {"n_tests": perm_full["n_tests"],
                                "n_significant_bh": perm_full[
                                    "n_significant_bh"]},
                "restricted_layers": {
                    "n_tests": perm_restr["n_tests"],
                    "n_significant_bh": perm_restr["n_significant_bh"]}},
            "composition": {
                "powered": powered, "n_pairs": n_a, "j51r": j51r,
                "a_restr": round(a_restr, 4), "tv_restr": round(tv_restr, 4),
                "a_full_paired": round(a_full_sub, 4),
                "tv_full_paired": round(tv_full_sub, 4),
                "site_mix": site_mix,
                "icit_unmatched_site_token_share": icit_unmatched_site_share,
                "icit_material_mix": dict(Counter(
                    r["material"] for r in kept).most_common()),
                "icit_type_mix": dict(Counter(
                    r["type"] for r in kept).most_common(12))},
            "segmentation": {
                "s1": {"f0": 43, "f1": f1, "verdict": v_s1},
                "s2": {"powered": len(j51u) >= 15, "j51u": j51u,
                       "tv_artifact_units": round(tv_art, 4),
                       "tv_row_units": round(tv_row, 4),
                       "verdict": v_s2},
                "s3": s3},
            "mapping": {
                "per_sign": {s: {k: v for k, v in per_sign_map[s].items()
                                 if k != "codes"} for s in j51},
                "top5_tv_share": top5_share, "top10_tv_share": top10_share,
                "chain_heavy_signs": heavy, "clean_signs": clean,
                "delta_mean_tv": delta, "group_sizes_ok": groups_ok,
                "audit_table_top10": audit_table},
            "direction": {
                "d1": {"tier_a": n_a, "tier_b": n_b,
                       "reversed_share": rev_share,
                       "powered": n_a + n_b >= 50, "verdict": v_d1},
                "d2": {"a_flip": round(a_flip, 4),
                       "a_full": round(a_full, 4), "verdict": v_d2}},
            "definition": {
                "per_sign": def_detail, "median_w1": median_w1,
                "material_displacement_share": material_share,
                "spearman_mean_r": rho, "a5_modal_bin_agreement": a5}},
        "verdicts": verdicts,
        "arm_verdicts": {"s1": v_s1, "s2": v_s2, "d1": v_d1, "d2": v_d2},
        "recommendation": recommendation,
        "deviations": [],
    }
    RESULTS_PATH.write_text(json.dumps(results, indent=1) + "\n")
    SUMMARY_PATH.write_text(_summary_md(results))
    return results


def _summary_md(r: dict) -> str:
    b, m, a, v = r["baseline"], r["matcher"], r["arms"], r["verdicts"]
    comp, seg, mp = a["composition"], a["segmentation"], a["mapping"]
    dr, df = a["direction"], a["definition"]
    rec = r["recommendation"]
    lines = [
        "# Phase-116 — Corpus-Harmonization Study: Why Holdat and ICIT "
        "Positional Profiles Disagree",
        "",
        f"**Spec:** {r['spec']} (frozen before any results) · "
        f"**Date:** {r['date']} · **GPU device:** {r['gpu_device']}",
        "",
        "**Diagnostic only.** No anchor was changed, no validation "
        "verdict was issued; all 44 anchors remain "
        "`pending_non_sa_validation`.",
        "",
        "## Baseline (recomputed; asserted against the Phase-115 record)",
        "",
        f"T1 v2 over STRICT94: judged {b['judged']} "
        f"({b['pass']} PASS / {b['fail']} FAIL), "
        f"{b['modal_disagreement_failures']} modal-disagreement failures, "
        f"median TV over failures {b['median_tv_failures']}, mean TV over "
        f"judged {b['mean_tv_judged']}, full-layer modal agreement "
        f"A_full = {b['a_full']}.",
        "",
        "## Matcher yield (spec section 4)",
        "",
        f"Tier A (direct, mutually unique): **{m['tier_a_pairs']}** pairs. "
        f"Tier B (reversed): **{m['tier_b_pairs']}**. Tier C "
        f"(containment): **{m['tier_c_pairs']}**. Ambiguous-orientation "
        f"candidate pairs: {m['ambiguous_orientation_pairs']} (excluded "
        f"from A/B). Raw compatible pairs before uniqueness: "
        f"{m['compat_direct_pairs']} direct / "
        f"{m['compat_reversed_pairs']} reversed.",
        "",
        "## Verdicts (frozen rules, spec section 5)",
        "",
        "| Hypothesis | Verdict | Headline numbers |",
        "|---|---|---|",
        f"| H-COMPOSITION | **{v['composition']}** | "
        f"restricted: A {comp['a_restr']} / TV {comp['tv_restr']} on "
        f"{len(comp['j51r'])} paired signs vs full-layer "
        f"A {comp['a_full_paired']} / TV {comp['tv_full_paired']} "
        f"(powered: {comp['powered']}) |",
        f"| H-SEGMENTATION | **{v['segmentation']}** | "
        f"S1 sentinel-strip: FAIL {seg['s1']['f0']} → {seg['s1']['f1']} "
        f"({seg['s1']['verdict']}); S2 artifact-units: TV "
        f"{seg['s2']['tv_artifact_units']} vs row-units "
        f"{seg['s2']['tv_row_units']} ({seg['s2']['verdict']}) |",
        f"| H-MAPPING | **{v['mapping']}** | "
        f"top-10 TV share {mp['top10_tv_share']}; chain-heavy minus clean "
        f"mean TV Δ = {mp['delta_mean_tv']} "
        f"(groups ok: {mp['group_sizes_ok']}) |",
        f"| H-DIRECTION | **{v['direction']}** | "
        f"D1 reversed share {dr['d1']['reversed_share']} "
        f"({dr['d1']['verdict']}); D2 flip: A {dr['d2']['a_flip']} vs "
        f"{dr['d2']['a_full']} ({dr['d2']['verdict']}) |",
        f"| H-DEFINITION | **{v['definition']}** | "
        f"median W1 {df['median_w1']}; material-displacement share "
        f"{df['material_displacement_share']}; 5-bin agreement "
        f"{df['a5_modal_bin_agreement']}; Spearman ρ "
        f"{df['spearman_mean_r']} |",
        "",
        f"Permutation context (BH q = 0.05, token-level): "
        f"{a['permutation_context']['full_layers']['n_significant_bh']} of "
        f"{a['permutation_context']['full_layers']['n_tests']} judged "
        f"signs disagree beyond sampling noise on the full layers; "
        f"{a['permutation_context']['restricted_layers']['n_significant_bh']} "
        f"of {a['permutation_context']['restricted_layers']['n_tests']} on "
        f"the matched restriction.",
        "",
        "## Harmonization recommendation (assembled mechanically, spec section 6)",
        "",
    ]
    lines += [f"- {x}" for x in rec["lines"]]
    lines += ["", "## What a future validation battery may / may not assume", ""]
    lines += [f"- {x}" for x in rec["may_assume"]]
    lines += [f"- {x}" for x in rec["may_not_assume"]]
    if rec["unresolved"]:
        lines.append(
            f"- UNRESOLVED (no assumption licensed either way): "
            f"{', '.join(rec['unresolved'])}.")
    lines += [
        "",
        "## Limitations",
        "",
        "Registered in spec section 8: identity is textual, not "
        "artifactual; sentinel wildcard asymmetry (15.0% of kept "
        "positions); token-level permutation ignores inscription "
        "clustering; site-mix matching is string-normalized only; "
        "`dir.` label semantics never assumed. Full per-sign records, "
        "the matcher tier decomposition, and the section 5.3 crosswalk "
        "audit table are in `phase116_harmonization_results.json`.",
        "",
        "## Verification",
        "",
        "Recorded in the phase ledger entries and the PR body (full "
        "backend suite; foundation check per H21 — anchors untouched, "
        "reports added). Conversion audit: every population token "
        f"({r['layers']['conversion_audit_tokens']}) recomputed from "
        "its stored source code matches the keyed layer.",
        "",
        "**AI disclosure:** executed by an AI agent (Muse Spark, via "
        "Muse) at the direction of Tristen Pierson, per constitution "
        "section VI.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    results = run_all()
    print(json.dumps(results["verdicts"], indent=1))
    print(f"matcher: A={results['matcher']['tier_a_pairs']} "
          f"B={results['matcher']['tier_b_pairs']} "
          f"C={results['matcher']['tier_c_pairs']}")
    print(f"wrote {RESULTS_PATH}")
    print(f"wrote {SUMMARY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
