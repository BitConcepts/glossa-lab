"""Phase-116 (spec 015) — corpus-harmonization analysis.

Diagnostic only: why do Holdat and ICIT positional profiles
disagree (Phase-115, spec 014: T1 judged 51 strict signs, 43
FAIL, 40 on modal-class disagreement, median TV 0.789474)?

This module implements, as pure deterministic functions:

  - the spec-014 section 4 T1 v2 judgment (replicated; the
    run asserts it reproduces the published Phase-115 baseline
    before any arm executes),
  - the spec section 4 matched-text matcher (tiers A/B/C),
  - the section 5 arms: permutation context (5.0),
    H-COMPOSITION (5.1), H-SEGMENTATION (5.2), H-MAPPING (5.3),
    H-DIRECTION (5.4), H-DEFINITION (5.5),
  - the frozen verdict rules and the section 6 recommendation
    assembly.

Profile/modal/TV conventions are phase113_battery's, imported
(not reimplemented, so they cannot drift). No SA artifact, no
anchor basis text, and no prior phase's per-sign verdict is an
input to any statistic here (H26).
"""
from __future__ import annotations

import bisect
import collections
import csv
import json
import random
import re
from pathlib import Path

from glossa_lab.phase113_battery import (
    FAIL, NOT_ATTESTED, PASS, T1_TV_MAX, CorpusContext, modal_class,
    positional_counts, profile_from_counts, tv_distance,
)

SENTINEL = "UNK"
CLASSES = ("INITIAL", "MEDIAL", "TERMINAL")

# ── Frozen constants (spec 014 section 4; spec 015 sections 4-5) ──
OPPORTUNITY_BAND_LOW = 3.0
OPPORTUNITY_BAND_HIGH = 9.0
STABILITY_MIN_TOKENS = 3
PERMUTATIONS = 1999
PERM_SEED = 116116
BH_Q = 0.05


# ── Loaders ────────────────────────────────────────────────────

def find_downloads(repo: Path, main_repo: Path) -> Path:
    for cand in (repo / "corpora" / "downloads",
                 main_repo / "corpora" / "downloads"):
        if (cand / "icit_fieldcady" / "icit_converted_v2_keyed.json").exists():
            return cand
    raise FileNotFoundError("keyed layer not found in worktree or "
                            "main checkout (run the phase116 builder)")


def load_holdat_keyed(csv_path: Path):
    """Phase113 loader logic with keys retained: returns
    (inscriptions_by_id, site_by_id)."""
    seals: dict[str, list] = {}
    sites: dict[str, str] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals:
                seals[c] = []
                sites[c] = (row.get("site") or "").strip()
            while len(seals[c]) <= p:
                seals[c].append("")
            seals[c][p] = s
    ins = {c: [s for s in v if s] for c, v in seals.items() if any(v)}
    return ins, {c: sites[c] for c in ins}


def load_keyed_layer(path: Path) -> list[dict]:
    data = json.loads(path.read_text("utf-8"))
    return data["inscriptions"]


def kept_records(records) -> list[dict]:
    return [r for r in records if r["status"] == "kept"]


def population_records(records) -> list[dict]:
    """The section 4 matcher population: kept + Holdat-dedupe
    dropped (the v2 dedupe removed the best Holdat matches by
    construction)."""
    return [r for r in records
            if r["status"] in ("kept", "dropped_holdat_dup")]


# ── Conversion replication (audit + H-MAPPING provenance) ─────

def p_to_m_map(crosswalk_path: Path) -> dict[str, str]:
    conf = {"HIGH": 3, "MEDIUM": 2, "CANDIDATE": 1}
    data = json.loads(crosswalk_path.read_text())
    best: dict[str, tuple[str, int]] = {}
    for e in list(data["crosswalk"].values()):
        p = e.get("parpola_id") or e.get("p_id")
        m = e.get("mahadevan_id") or e.get("m_id")
        c = conf.get(e.get("confidence", "CANDIDATE"), 1)
        if p and m and (p not in best or c > best[p][1]):
            best[p] = (m, c)
    return {p: m for p, (m, _) in best.items()}


def registry_audit(registry_path: Path):
    """Per normalized Wells code: the M ids its registry rows
    point to (union, split on '|'), whether any listing row is
    multi-valued in mahadevan_ids, its Parpola ids, and the
    single-valued Wells->M / Wells->Parpola maps (the builder's
    semantics, replicated). Returns (audit, w2m, w2p) where
    audit[code] = {"m_ids": set, "multi_row": bool,
    "parpola_ids": set}."""
    audit: dict[str, dict] = {}
    w2m: dict[str, str] = {}
    w2p: dict[str, str] = {}

    def single(v):
        v = (v or "").strip()
        return v if v and "|" not in v else None

    with open(registry_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m_raw = (r.get("mahadevan_ids") or "").strip()
            m_ids = [x.strip() for x in m_raw.split("|") if x.strip()]
            p_single = single(r.get("parpola_id"))
            m_single = single(r.get("mahadevan_ids"))
            for w in (r.get("wells_ids") or "").split("|"):
                w = w.strip().lstrip("Ww")
                if not w:
                    continue
                k = str(int(w)) if w.isdigit() else w
                e = audit.setdefault(k, {"m_ids": set(),
                                         "multi_row": False,
                                         "parpola_ids": set()})
                e["m_ids"].update(m_ids)
                if len(m_ids) > 1:
                    e["multi_row"] = True
                if p_single:
                    e["parpola_ids"].add(p_single)
                if m_single:
                    w2m.setdefault(k, m_single)
                if p_single:
                    w2p.setdefault(k, p_single)
    return audit, w2m, w2p


def code_is_ambiguous(audit: dict, code: str) -> bool:
    e = audit.get(code)
    if e is None:
        return False
    return len(e["m_ids"]) > 1 or e["multi_row"]


def normalize_code(raw: str) -> str:
    return str(int(raw)) if raw.isdigit() else raw


def audit_conversion(records, w2m, w2p, p2m) -> int:
    """Recompute every kept/population token from its stored
    source code + kind and assert equality with the stored
    token. Returns the number of tokens audited. This pins the
    keyed layer's provenance to the conversion policy."""
    n = 0
    for r in records:
        for tok, kind, raw in zip(r["tokens"], r["kinds"], r["codes"]):
            if kind == "direct":
                exp = w2m[normalize_code(raw)]
            elif kind == "chain":
                exp = p2m[w2p[normalize_code(raw)]]
            else:  # placeholder / unmapped
                exp = SENTINEL
            assert tok == exp, (r["row"], raw, kind, tok, exp)
            n += 1
    return n


# ── T1 v2 (spec 014 section 4, replicated) ─────────────────────

def attestation_floor(opp: float) -> int:
    if opp < OPPORTUNITY_BAND_LOW:
        return 1
    if opp < OPPORTUNITY_BAND_HIGH:
        return 2
    return 3


def test_t1_v2(sign, holdat: CorpusContext, icit: CorpusContext,
               ratio: float, profile_source: CorpusContext = None) -> dict:
    """Counts and floors from `icit`; profiles from
    `profile_source` if given (spec 015 arm S1: sentinel-stripped
    profiles with counts/floors held fixed)."""
    prof_src = profile_source if profile_source is not None else icit
    n_h = holdat.token_count(sign)
    n_i = icit.token_count(sign)
    opp = ratio * n_h
    floor = attestation_floor(opp)
    out = {"n_icit_tokens": n_i, "n_holdat_tokens": n_h,
           "opportunity": round(opp, 6), "floor": floor}
    prof_h = holdat.profile(sign)
    if prof_h is None:
        out.update({"state": NOT_ATTESTED, "reason": "sign_absent_holdat"})
        return out
    if n_i < floor:
        out.update({"state": NOT_ATTESTED,
                    "reason": "below_opportunity_floor"})
        return out
    prof_i = prof_src.profile(sign)
    out["modal_holdat"] = modal_class(prof_h)
    out["modal_icit"] = modal_class(prof_i)
    out["tv"] = round(tv_distance(prof_h, prof_i), 6)
    agree = (out["modal_icit"] == out["modal_holdat"]
             and out["tv"] <= T1_TV_MAX)
    if agree:
        out["state"] = PASS
    elif n_i >= STABILITY_MIN_TOKENS:
        out["state"] = FAIL
    else:
        out.update({"state": NOT_ATTESTED,
                    "reason": "below_stability_floor"})
    return out


def stripped_context(records) -> CorpusContext:
    """CorpusContext over sentinel-stripped kept sequences
    (arm S1 geometry)."""
    seqs = [[t for t in r["tokens"] if t != SENTINEL]
            for r in kept_records(records)]
    return CorpusContext([s for s in seqs if s])


# ── The matched-text matcher (spec section 4) ──────────────────

def _compatible(h, i) -> bool:
    """Wildcard compatibility at equal length: i's mapped tokens
    all equal h's; >= 2 mapped positions in i."""
    if len(h) != len(i):
        return False
    mapped = 0
    for ht, it in zip(h, i):
        if it == SENTINEL:
            continue
        if it != ht:
            return False
        mapped += 1
    return mapped >= 2


def _compatible_reversed(h, i) -> bool:
    return _compatible(h, list(reversed(i)))


def _contains(h, i, h_counter, i_mapped_counter, i_unk) -> bool:
    """Strict containment either way under wildcard compatibility
    (the ICIT side carries the sentinels). Shorter length >= 3
    and >= 2 mapped positions on the shorter side. Counters are
    precomputed by the caller (h full Counter; i mapped-only
    Counter; i sentinel count)."""
    if len(h) == len(i):
        return False
    if len(i) < len(h):
        short, long_, short_is_icit = i, h, True
    else:
        short, long_, short_is_icit = h, i, False
    if len(short) < 3:
        return False
    if short_is_icit:
        if sum(1 for t in short if t != SENTINEL) < 2:
            return False
        need = collections.Counter(t for t in short if t != SENTINEL)
        if any(need[t] > h_counter[t] for t in need):
            return False
    else:
        if sum(i_mapped_counter.values()) < 2:
            return False
        need = h_counter
        if sum((need - i_mapped_counter).values()) > i_unk:
            return False
    for off in range(len(long_) - len(short) + 1):
        ok = True
        for k, st in enumerate(short):
            lt = long_[off + k]
            it = st if short_is_icit else lt
            ht = lt if short_is_icit else st
            if it != SENTINEL and it != ht:
                ok = False
                break
        if ok:
            return True
    return False


def run_matcher(holdat_items, icit_records):
    """holdat_items: list[(hid, seq)]; icit_records: population
    records. Returns dict with tier pair lists of (h_idx, i_idx),
    ambiguous pair count, and candidate degree stats."""
    H = [seq for _, seq in holdat_items]
    I = [list(r["tokens"]) for r in icit_records]
    I_rev = [list(reversed(s)) for s in I]
    h_counters = [collections.Counter(s) for s in H]
    i_mapped_counters = [collections.Counter(
        t for t in s if t != SENTINEL) for s in I]
    i_unk = [sum(1 for t in s if t == SENTINEL) for s in I]
    by_len_h: dict[int, list[int]] = collections.defaultdict(list)
    for hi, s in enumerate(H):
        by_len_h[len(s)].append(hi)
    compat_d: dict[int, set] = collections.defaultdict(set)
    compat_r: dict[int, set] = collections.defaultdict(set)
    for ii, s in enumerate(I):
        for hi in by_len_h.get(len(s), ()):
            if _compatible(H[hi], s):
                compat_d[hi].add(ii)
            if _compatible(H[hi], I_rev[ii]):
                compat_r[hi].add(ii)
    deg_d_h = {h: len(v) for h, v in compat_d.items()}
    deg_d_i = collections.Counter()
    for v in compat_d.values():
        deg_d_i.update(v)
    deg_r_h = {h: len(v) for h, v in compat_r.items()}
    deg_r_i = collections.Counter()
    for v in compat_r.values():
        deg_r_i.update(v)
    ambiguous = sum(1 for h, v in compat_d.items()
                    for i in v if i in compat_r.get(h, ()))
    tier_a, tier_b = [], []
    for h, v in compat_d.items():
        for i in v:
            if deg_d_h[h] == 1 and deg_d_i[i] == 1 \
                    and i not in compat_r.get(h, ()):
                tier_a.append((h, i))
    for h, v in compat_r.items():
        for i in v:
            if deg_r_h[h] == 1 and deg_r_i[i] == 1 \
                    and i not in compat_d.get(h, ()):
                tier_b.append((h, i))
    used_pairs = set(tier_a) | set(tier_b)
    cand_c: dict[int, set] = collections.defaultdict(set)
    for hi, hs in enumerate(H):
        for ii, iseq in enumerate(I):
            if (hi, ii) in used_pairs:
                continue
            if _contains(hs, iseq, h_counters[hi],
                         i_mapped_counters[ii], i_unk[ii]):
                cand_c[hi].add(ii)
    deg_c_i = collections.Counter()
    for v in cand_c.values():
        deg_c_i.update(v)
    tier_c = [(h, i) for h, v in cand_c.items() for i in v
              if len(v) == 1 and deg_c_i[i] == 1]
    return {"tier_a": sorted(tier_a), "tier_b": sorted(tier_b),
            "tier_c": sorted(tier_c), "ambiguous_pairs": ambiguous,
            "compat_direct_pairs": sum(len(v) for v in compat_d.values()),
            "compat_reversed_pairs": sum(len(v) for v in compat_r.values()),
            "containment_candidates": sum(len(v) for v in cand_c.values())}


# ── Section 5.0 permutation context + BH ───────────────────────

def bh_qvalues(pvals) -> list[float]:
    m = len(pvals)
    order = sorted(range(m), key=lambda k: pvals[k])
    q = [0.0] * m
    running = 1.0
    for rank in range(m, 0, -1):
        idx = order[rank - 1]
        running = min(running, pvals[idx] * m / rank)
        q[idx] = min(running, 1.0)
    return q


def permutation_tv_test(counts_h, counts_i, rng: random.Random,
                        nperm: int = PERMUTATIONS) -> float:
    """Token-label permutation test, statistic = profile TV.
    counts are (I, M, T) positional counts per corpus."""
    nh, ni = sum(counts_h), sum(counts_i)
    if nh == 0 or ni == 0:
        return 1.0
    obs = tv_distance(profile_from_counts(counts_h),
                      profile_from_counts(counts_i))
    classes = ([0] * counts_h[0] + [1] * counts_h[1] + [2] * counts_h[2]
               + [0] * counts_i[0] + [1] * counts_i[1] + [2] * counts_i[2])
    labels = [0] * nh + [1] * ni
    ge = 0
    for _ in range(nperm):
        rng.shuffle(labels)
        ch = [0, 0, 0]
        ci = [0, 0, 0]
        for lab, cl in zip(labels, classes):
            if lab == 0:
                ch[cl] += 1
            else:
                ci[cl] += 1
        tv = tv_distance(profile_from_counts(tuple(ch)),
                         profile_from_counts(tuple(ci)))
        if tv >= obs - 1e-12:
            ge += 1
    return (1 + ge) / (1 + nperm)


def permutation_family(signs, holdat: CorpusContext, icit: CorpusContext):
    """The section 5.0 family over `signs` (one shared seeded
    RNG stream, signs in the given order)."""
    rng = random.Random(PERM_SEED)
    pvals, detail = [], {}
    for s in signs:
        ch = positional_counts(holdat.inscriptions, s)
        ci = positional_counts(icit.inscriptions, s)
        p = permutation_tv_test(ch, ci, rng)
        pvals.append(p)
        detail[s] = {"counts_holdat": list(ch), "counts_icit": list(ci),
                     "p": round(p, 6)}
    qs = bh_qvalues(pvals)
    for s, q in zip(signs, qs):
        detail[s]["q"] = round(q, 6)
    n_sig = sum(1 for q in qs if q <= BH_Q)
    return {"n_tests": len(signs), "n_significant_bh": n_sig,
            "per_sign": detail}


# ── Positional helpers for H-DEFINITION ────────────────────────

def relative_positions(inscriptions, sign) -> list[float]:
    out = []
    for ins in inscriptions:
        n = len(ins)
        for pos, tok in enumerate(ins):
            if tok == sign:
                out.append(pos / (n - 1) if n > 1 else 0.5)
    return out


def wasserstein1(xs, ys) -> float:
    """Exact 1-D Wasserstein-1 distance between two empirical
    samples (CDF integral over the union of values)."""
    if not xs or not ys:
        return 0.0
    xs = sorted(xs)
    ys = sorted(ys)
    vals = sorted(set(xs) | set(ys))
    total = 0.0
    for a, b in zip(vals, vals[1:]):
        fx = bisect.bisect_right(xs, a) / len(xs)
        fy = bisect.bisect_right(ys, a) / len(ys)
        total += abs(fx - fy) * (b - a)
    return total


def _midranks(vals) -> list[float]:
    order = sorted(range(len(vals)), key=lambda k: vals[k])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys) -> float:
    rx, ry = _midranks(xs), _midranks(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx)
           * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def five_bin_profiles(inscriptions, sign):
    counts = [0] * 5
    for ins in inscriptions:
        n = len(ins)
        for pos, tok in enumerate(ins):
            if tok == sign:
                counts[min(4, int(5 * (pos + 0.5) / n))] += 1
    return counts


def five_bin_profile(counts):
    total = sum(counts)
    if total == 0:
        return None
    return tuple(c / total for c in counts)


def modal_bin(profile) -> int:
    """Largest share; ties break to the lowest bin index."""
    return max(range(5), key=lambda k: (profile[k], -k))


# ── Verdict rules (spec section 5, frozen thresholds) ──────────

def verdict_composition(powered: bool, a_restr, tv_restr,
                        a_full_sub, tv_full_sub) -> str:
    if not powered:
        return "UNRESOLVED"
    if a_restr >= 0.75 and tv_restr <= 0.50 * tv_full_sub:
        return "SUPPORTED"
    if a_restr <= a_full_sub + 0.05 and tv_restr >= 0.90 * tv_full_sub:
        return "REFUTED"
    return "UNRESOLVED"


def verdict_segmentation(s1: str, s2: str) -> str:
    if "SUPPORTED" in (s1, s2):
        return "SUPPORTED"
    if s1 == "REFUTED" and s2 == "REFUTED":
        return "REFUTED"
    return "UNRESOLVED"


def verdict_s1(f1: int, f0: int = 43) -> str:
    if f1 <= 21:
        return "SUPPORTED"
    if f1 >= 39:
        return "REFUTED"
    return "UNRESOLVED"


def verdict_s2(powered: bool, tv_art, tv_row) -> str:
    if not powered:
        return "UNRESOLVED"
    if tv_art <= 0.60 * tv_row:
        return "SUPPORTED"
    if tv_art >= 0.95 * tv_row:
        return "REFUTED"
    return "UNRESOLVED"


def verdict_mapping(top10_share, delta, group_sizes_ok: bool) -> str:
    if not group_sizes_ok:
        if top10_share is not None and top10_share <= 0.40:
            return "REFUTED"
        return "UNRESOLVED"
    if top10_share >= 0.60 and delta >= 0.20:
        return "SUPPORTED"
    if top10_share <= 0.40 and delta <= 0.05:
        return "REFUTED"
    return "UNRESOLVED"


def verdict_direction(d1: str, d2: str) -> str:
    if "SUPPORTED" in (d1, d2):
        return "SUPPORTED"
    if d1 == "REFUTED" and d2 == "REFUTED":
        return "REFUTED"
    return "UNRESOLVED"


def verdict_d1(powered: bool, reversed_share) -> str:
    if not powered:
        return "UNRESOLVED"
    if reversed_share >= 0.60:
        return "SUPPORTED"
    if reversed_share <= 0.10:
        return "REFUTED"
    return "UNRESOLVED"


def verdict_d2(a_flip, a_full) -> str:
    if a_flip - a_full >= 0.30:
        return "SUPPORTED"
    if a_flip - a_full <= 0.05:
        return "REFUTED"
    return "UNRESOLVED"


def verdict_definition(median_w1, material_share, a5) -> str:
    if median_w1 <= 0.12 and material_share <= 0.25 and a5 >= 0.70:
        return "SUPPORTED"
    if median_w1 >= 0.20 or material_share >= 0.50:
        return "REFUTED"
    return "UNRESOLVED"


# ── Section 6 recommendation assembly (mechanical) ─────────────

def assemble_recommendation(verdicts: dict, seg_via: dict) -> dict:
    """verdicts: {composition, segmentation, mapping, direction,
    definition} -> verdict strings. seg_via: {"s1": v, "s2": v}.
    Returns {"lines": [...], "may_assume": [...],
    "may_not_assume": [...], "unresolved": [...]} assembled
    strictly from the frozen section 6 templates."""
    lines, may, may_not, unres = [], [], [], []

    def note(hyp, verdict, supported_line, may_line, maynot_line):
        if verdict == "SUPPORTED":
            lines.append(supported_line)
            may.append(may_line)
        elif verdict == "REFUTED":
            may_not.append(maynot_line)
        else:
            unres.append(hyp)

    if verdicts["segmentation"] == "SUPPORTED":
        if seg_via.get("s1") == "SUPPORTED":
            lines.append(
                "R-SEG1: Before any cross-corpus positional comparison, "
                "strip sentinel (UNK) positions from converted-layer "
                "sequences and compute profiles on the compressed "
                "sequences; the spec-014 sentinel geometry is not "
                "harmonized with Holdat's convention.")
            may.append(
                "MAY assume (after R-SEG1 sentinel stripping) that "
                "cross-corpus profiles are computed under a shared "
                "boundary geometry.")
        if seg_via.get("s2") == "SUPPORTED":
            lines.append(
                "R-SEG2: Convert ICIT inscription units to artifact "
                "units (concatenate same-cisi rows in source file "
                "order) before computing positional profiles.")
            may.append(
                "MAY assume (after R-SEG2 artifact-unit conversion) "
                "that both layers profile the same text units.")
    elif verdicts["segmentation"] == "REFUTED":
        may_not.append(
            "MAY NOT assume the disagreement is a text-unit/boundary "
            "artifact: it survives sentinel stripping and artifact-unit "
            "re-unitization.")
    else:
        unres.append("segmentation")

    note("composition", verdicts["composition"],
         "R-COMP: Restrict cross-corpus positional comparisons to "
         "the matched-text intersection (Tier A pairs, spec 015 "
         "section 4); full-population cross-corpus profiles are not "
         "comparable across these two compilations.",
         "MAY assume (after R-COMP restriction to matched texts) "
         "that remaining cross-corpus disagreement measures "
         "transcription behavior rather than population mix.",
         "MAY NOT assume the disagreement is a population-mix "
         "artifact: it persists at full strength on identical texts.")
    note("mapping", verdicts["mapping"],
         "R-MAP: Exclude the audit-table signs (spec 015 section "
         "5.3) from any cross-corpus gate, or repair the listed "
         "crosswalk entries first; do not gate on chain-heavy or "
         "registry-ambiguous signs.",
         "MAY assume (after R-MAP exclusion/repair) that the "
         "remaining signs' crosswalk conversions are not the "
         "disagreement's driver.",
         "MAY NOT assume the disagreement is crosswalk error: it "
         "is not concentrated in crosswalk-risky signs.")
    note("direction", verdicts["direction"],
         "R-DIR: Reverse converted-layer sequences to Holdat's "
         "orientation convention before profiling (the orientation "
         "divergence is measured, spec 015 section 5.4).",
         "MAY assume (after R-DIR orientation alignment) that both "
         "layers store matched texts in a shared orientation.",
         "MAY NOT assume the disagreement is an orientation "
         "artifact: matched texts share orientation and a global "
         "flip does not repair profiles.")
    note("definition", verdicts["definition"],
         "R-DEF: Replace the 3-class modal/TV gate with a "
         "continuous relative-position statistic (per-sign W1 / "
         "mean relative position); the 3-class modal gate "
         "manufactures disagreement on this corpus pair.",
         "MAY assume (after R-DEF) that positional agreement is "
         "measured on a definition that does not itself manufacture "
         "the disagreement.",
         "MAY NOT assume the disagreement is a binning artifact: "
         "genuine positional displacement survives continuous "
         "relative-position measurement.")

    if not any(v == "SUPPORTED" for v in verdicts.values()):
        lines = [
            "R-NONE: No harmonization transformation is justified by "
            "this study. Cross-corpus positional validation between "
            "Holdat and the ICIT converted layer is not viable on "
            "this pair of compilations under any convention alignment "
            "tested. A future validation battery must not use a "
            "conjunctive cross-corpus positional gate on this pair; "
            "validation must proceed within a single compilation or "
            "await a genuinely independent corpus."
        ] + lines
    may.append(
        "MAY NOT assume the anchors' validation status changed: "
        "this study is diagnostic only and all 44 anchors remain "
        "pending_non_sa_validation.")
    return {"lines": lines, "may_assume": may,
            "may_not_assume": may_not, "unresolved": unres}


def norm_site(name: str) -> str:
    return re.sub(r"[\s\-]+", "", (name or "").strip().lower())


def norm_cisi_key(cisi: str, row: int) -> str:
    k = re.sub(r"[\s\-]+", "", (cisi or "").strip().upper())
    return k if k else f"ROW:{row}"
