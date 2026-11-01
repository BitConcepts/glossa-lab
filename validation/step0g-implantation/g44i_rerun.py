#!/usr/bin/env python3
"""
G44-I VALIDATION RERUN (Amendment 1) - self-contained package.

Implements the amended G44-I implantation validation end to end:
draft 2026-10-26-spec-draft-step0g-implantation-instrument.md
(SHA-256 53b4ae9e...) as amended by Amendment 1
(2026-10-27-spec-draft-step0g-implantation-amendment1.md,
SHA-256 b1bdb053...), under DESIGN-AND-BARS-G44I-RERUN.md.

Reads population.json from its own directory (SHA-256 pinned in
CONFIG), writes stage checkpoints, markers.txt and results.json
under output/ beside itself. Resume-safe: re-running verifies and
skips completed stages. Python 3 standard library only.
Non-interactive; creates no windows.

The machinery sections below are embedded verbatim from the tested
Amendment 1 design-stage modules: implant_lib (profiles, evidence,
scorer, baseline, null, certification, selection/implantation,
SIGIL generator), amended_ledger (the amended ledger draw, cell
construction, feasibility), auditor (the independent gate recount).
"""
import hashlib
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict


# ============ implant_lib (verbatim body) ========
FIRST, MIDDLE, LAST, ONLY = 0, 1, 2, 3
CLASS_NAMES = ["FIRST", "MIDDLE", "LAST", "ONLY"]
FLOOR = 10
ACC_BAR = 0.60
RECOVERY_BAR_SIGN = 0.60
RECOVERY_BAR_SIGNS = 33
POS_FLOOR = 0.55
NBR_FLOOR = 0.45
MARGIN_BAR = 0.05
N_PERMS = 9999


def pos_class(idx, length):
    if length == 1:
        return ONLY
    if idx == 0:
        return FIRST
    if idx == length - 1:
        return LAST
    return MIDDLE


def role_totals(seqs):
    tot = [0, 0, 0, 0]
    for seq in seqs:
        L = len(seq)
        for i in range(L):
            tot[pos_class(i, L)] += 1
    return tot


def round_half_up(x):
    return math.floor(x + 0.5)


def argmax4(vals):
    """Argmax with ties broken FIRST, MIDDLE, LAST, ONLY."""
    best = 0
    for c in range(1, 4):
        if vals[c] > vals[best]:
            best = c
    return best


# ------------------------------------------------------------- profiles
def build_profiles(seqs):
    """p(s): four-class share distribution of s's attestations."""
    per_sign = defaultdict(Counter)
    for seq in seqs:
        L = len(seq)
        for i, s in enumerate(seq):
            per_sign[s][pos_class(i, L)] += 1
    profiles, totals = {}, {}
    for s, cnt in per_sign.items():
        n = sum(cnt.values())
        totals[s] = n
        profiles[s] = [cnt[c] / n for c in range(4)]
    return profiles, totals


def corpus_profile(profiles, totals):
    tot = sum(totals.values())
    cp = [0.0, 0.0, 0.0, 0.0]
    for s, p in profiles.items():
        for c in range(4):
            cp[c] += p[c] * totals[s]
    return [x / tot for x in cp]


def attestation_evidence(seq, i, profiles):
    """Neighbor evidence of one attestation: mean over adjacent signs
    that have a profile of p(adjacent). None if no adjacent sign has a
    profile (the attestation is not neighbor-bearing)."""
    L = len(seq)
    ev = [0.0, 0.0, 0.0, 0.0]
    n = 0
    if i > 0 and seq[i - 1] in profiles:
        p = profiles[seq[i - 1]]
        for c in range(4):
            ev[c] += p[c]
        n += 1
    if i < L - 1 and seq[i + 1] in profiles:
        p = profiles[seq[i + 1]]
        for c in range(4):
            ev[c] += p[c]
        n += 1
    if n == 0:
        return None
    return [x / n for x in ev]


def population_stats(seqs, profiles):
    """Per-sign scoring statistics against a profile table (carried
    from G44-S population_stats)."""
    n_att = defaultdict(int)
    pos_counts = defaultdict(Counter)
    nbr_ev_sum = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    nbr_bearing = defaultdict(int)
    for seq in seqs:
        L = len(seq)
        for i, s in enumerate(seq):
            n_att[s] += 1
            pos_counts[s][pos_class(i, L)] += 1
            ev = attestation_evidence(seq, i, profiles)
            if ev is not None:
                for c in range(4):
                    nbr_ev_sum[s][c] += ev[c]
                nbr_bearing[s] += 1
    return {"n_att": dict(n_att), "pos_counts": pos_counts,
            "nbr_ev_sum": nbr_ev_sum, "nbr_bearing": dict(nbr_bearing)}


def sign_components(s, pred, stats):
    n = stats["n_att"].get(s, 0)
    if n < FLOOR:
        return None, None, None
    pos_comp = stats["pos_counts"][s][pred[0]] / n
    nb = stats["nbr_bearing"].get(s, 0)
    if nb > 0:
        nbr_comp = stats["nbr_ev_sum"][s][pred[1]] / nb
        return pos_comp, nbr_comp, (pos_comp + nbr_comp) / 2.0
    return pos_comp, None, pos_comp


def batch_score(assignment, stats):
    """assignment: dict label -> (pos_class, nbr_class), iterated in
    insertion order. Carried from G44-S batch_score."""
    per_sign, vals = {}, []
    pos_vals, nbr_vals = [], []
    for s, pred in assignment.items():
        pc, nc, a = sign_components(s, pred, stats)
        per_sign[s] = {"pred": [pred[0], pred[1]], "pos_comp": pc,
                       "nbr_comp": nc, "accuracy": a,
                       "neighbor_unscored": nc is None and a is not None,
                       "unscored": a is None}
        if a is not None:
            vals.append(a)
            pos_vals.append(pc)
            if nc is not None:
                nbr_vals.append(nc)
    B = sum(vals) / len(vals) if vals else None
    return {"B": B, "n_scored": len(vals),
            "mean_pos": (sum(pos_vals) / len(pos_vals)) if pos_vals else None,
            "mean_nbr": (sum(nbr_vals) / len(nbr_vals)) if nbr_vals else None,
            "n_nbr_scored": len(nbr_vals),
            "recovered": sum(1 for a in vals if a >= RECOVERY_BAR_SIGN),
            "per_sign": per_sign}


def baseline_assignment(signs, profiles, fit_stats, corp_profile):
    """The section 2 baseline, defined exactly, with the pinned
    fallbacks (carried from G44-S)."""
    assignment = {}
    for s in signs:
        if s in profiles:
            pos_pred = argmax4(profiles[s])
        else:
            pos_pred = argmax4(corp_profile)
        nb = fit_stats["nbr_bearing"].get(s, 0)
        if nb > 0:
            means = [fit_stats["nbr_ev_sum"][s][c] / nb for c in range(4)]
            nbr_pred = argmax4(means)
        elif s in profiles:
            nbr_pred = argmax4(profiles[s])
        else:
            nbr_pred = argmax4(corp_profile)
        assignment[s] = (pos_pred, nbr_pred)
    return assignment


def permutation_null(assignment, stats, seed):
    rng = random.Random(seed)
    signs = list(assignment.keys())
    pairs = [assignment[s] for s in signs]
    scores = []
    for _ in range(N_PERMS):
        perm = pairs[:]
        rng.shuffle(perm)
        scores.append(batch_score(dict(zip(signs, perm)), stats)["B"])
    return scores


def null_summary(null_scores, value):
    srt = sorted(null_scores)
    p95 = srt[math.ceil(0.95 * len(srt)) - 1]
    share_ge = sum(1 for x in null_scores if x >= value) / len(null_scores)
    return {"p95": p95, "share_ge": share_ge,
            "percentile": 100.0 * sum(1 for x in null_scores
                                      if x < value) / len(null_scores),
            "null_mean": sum(null_scores) / len(null_scores),
            "null_max": max(null_scores)}


def certification_conditions(batch, margin, b_base, null_summ):
    """The batch-level conditions of draft section 7.5 as evaluated for
    one batch on one population pair (carried from G44-S)."""
    conds = {
        "B_ge_0.60": batch["B"] is not None and batch["B"] >= ACC_BAR,
        "signs_recovered_ge_33": batch["recovered"] >= RECOVERY_BAR_SIGNS,
        "mean_pos_ge_0.55": batch["mean_pos"] is not None
            and batch["mean_pos"] >= POS_FLOOR,
        "mean_nbr_ge_0.45": batch["mean_nbr"] is not None
            and batch["mean_nbr"] >= NBR_FLOOR,
        "margin_ge_0.05_and_B_gt_baseline": margin is not None
            and margin >= MARGIN_BAR and batch["B"] > b_base,
        "null_p95_and_share": batch["B"] is not None
            and batch["B"] > null_summ["p95"]
            and null_summ["share_ge"] <= 0.05,
    }
    conds["certified"] = all(conds.values())
    return conds


# ---------------------------------------------------------- implantation
class ImplantFailure(Exception):
    def __init__(self, sign, cls, needed, available):
        super().__init__(sign, cls, needed, available)
        self.sign = sign
        self.cls = cls
        self.needed = needed
        self.available = available


def implant(records, signs, comp, profiles_table):
    """Implant one compilation per draft section 4.5 and the
    design-and-bars section 5 pins.

    records: list of {"id": str, "seq": [labels]} (unimplanted).
    signs: ledger dict label -> per-sign parameters incl.
           "cells_<comp>", "quota_<comp>", "nbr_class", "m".
    comp: "fitting" or "scoring".
    profiles_table: the stage's profile table for ranking evidence.
    Returns (implanted records, relabel log list). Deterministic.
    Raises ImplantFailure if a cell cannot be filled."""
    work = [{"id": r["id"], "seq": list(r["seq"])} for r in records]
    orig = [list(r["seq"]) for r in records]
    source_total = Counter()
    for seq in orig:
        for t in seq:
            source_total[t] += 1

    def source_cap(src):
        return min(30, math.floor(0.20 * source_total[src]))

    relabeled = set()
    away = Counter()
    log = []
    order = sorted(signs, key=lambda lab: (-signs[lab]["quota_" + comp],
                                           lab))
    for lab in order:
        s = signs[lab]
        cells = s["cells_" + comp]
        dstar = s["nbr_class"]
        m = s["m"]
        for cls in (FIRST, MIDDLE, LAST, ONLY):
            need = cells[cls]
            if need == 0:
                continue
            pool = []
            for i, rec in enumerate(work):
                seq = work[i]["seq"]
                L = len(seq)
                for j, tok in enumerate(seq):
                    if (i, j) in relabeled:
                        continue
                    if pos_class(j, L) != cls:
                        continue
                    src = orig[i][j]
                    if away[src] >= source_cap(src):
                        continue
                    pool.append((i, j, src))
            if cls == ONLY:
                pool.sort(key=lambda t: (away[t[2]],
                                         work[t[0]]["id"], t[1]))
            else:
                def rank_key(t):
                    i, j, src = t
                    ev = attestation_evidence(work[i]["seq"], j,
                                              profiles_table)
                    base = (away[src], work[i]["id"], j)
                    if ev is None:
                        return (1, 0.0) + base
                    return (0, abs(ev[dstar] - m)) + base
                pool.sort(key=rank_key)
            # Take in ranked order, skipping any candidate whose
            # source sign reaches its cap during this cell's take
            # (draft 4.5: "A candidate whose source sign is at cap
            # is skipped") — the pool-build check alone would let
            # one cell take several tokens from a source with only
            # one cap slot left.
            taken = 0
            for (i, j, src) in pool:
                if taken >= need:
                    break
                if away[src] >= source_cap(src):
                    continue
                work[i]["seq"][j] = lab
                relabeled.add((i, j))
                away[src] += 1
                taken += 1
                log.append({"sign": lab, "class": CLASS_NAMES[cls],
                            "inscription": work[i]["id"],
                            "token_index": j, "source": src})
            if taken < need:
                raise ImplantFailure(lab, CLASS_NAMES[cls], need,
                                     taken)
    return work, log

# ============ amended_ledger (verbatim body) =====
FIRST, MIDDLE, LAST, ONLY = 0, 1, 2, 3
CLASS_NAMES = ["FIRST", "MIDDLE", "LAST", "ONLY"]
N_SIGNS = 44
BUDGET_FRAC = 0.20
QUOTA_LO, QUOTA_HI = 12, 18
QUOTA_FLOOR = 12
ONLY_SIGN_CAP = 1
ONLY_FAMILY_CAP_TOKENS = 30
ONLY_FAMILY_CAP_FRAC = 0.25
C_MAX_MIN = 10  # feasibility precondition when an ONLY sign is planted


def round_half_up(x):
    return math.floor(x + 0.5)


def pos_class(idx, length):
    if length == 1:
        return ONLY
    if idx == 0:
        return FIRST
    if idx == length - 1:
        return LAST
    return MIDDLE


NBR_CLASS_CAP = 12
MASS_BY_CLASS = {FIRST: (0.50, 0.68), MIDDLE: (0.55, 0.80),
                 LAST: (0.50, 0.68)}


def draw_ledger(model_seed, nbr_classes=(FIRST, MIDDLE, LAST)):
    """Steps 1-6 of the first run's record section 4, amended as
    marked in the module docstring. Returns (labels, signs,
    reassignments). Neighbor classes are drawn uniform over
    nbr_classes (the amended default is the eligible set; the
    Amendment 1 census computation passed all four explicitly,
    as its file records). The neighbor-class cap reassignment
    runs between the neighbor draw and the mass draw, and masses
    are drawn from the FINAL class's range."""
    rng = random.Random(model_seed)
    labels = ["G44I-%02d" % i for i in range(1, N_SIGNS + 1)]
    signs = {lab: {} for lab in labels}
    for lab in labels:
        signs[lab]["pos_drawn"] = rng.choices(
            [FIRST, MIDDLE, LAST, ONLY],
            weights=[0.32, 0.32, 0.32, 0.04])[0]
    reassignments = []
    assigned = Counter(signs[lab]["pos_drawn"] for lab in labels)
    only_seen = 0
    for lab in labels:
        if signs[lab]["pos_drawn"] == ONLY:
            only_seen += 1
            if only_seen > ONLY_SIGN_CAP:
                counts = {c: assigned[c] for c in (FIRST, MIDDLE, LAST)}
                target = min((FIRST, MIDDLE, LAST),
                             key=lambda c: (counts[c], c))
                reassignments.append(
                    {"sign": lab, "from": "ONLY",
                     "to": CLASS_NAMES[target],
                     "rule": "Amendment 1 ONLY sign cap 1; "
                             "fewest-assigned class, ties "
                             "FIRST/MIDDLE/LAST"})
                assigned[ONLY] -= 1
                assigned[target] += 1
                signs[lab]["pos_drawn"] = target
    for lab in labels:
        signs[lab]["pos_class"] = signs[lab]["pos_drawn"]
    for lab in labels:
        if signs[lab]["pos_class"] == ONLY:
            signs[lab]["a"] = rng.uniform(0.55, 0.70)
        else:
            signs[lab]["a"] = rng.uniform(0.55, 0.85)
    for lab in labels:
        signs[lab]["nbr_drawn"] = rng.choice(list(nbr_classes))
        signs[lab]["nbr_class"] = signs[lab]["nbr_drawn"]
    # Amendment 1 neighbor-class cap: at most 12 per class; excess
    # in label order reassigned to MIDDLE (largest census pool).
    if tuple(nbr_classes) == (FIRST, MIDDLE, LAST):
        ncount = Counter(signs[lab]["nbr_class"] for lab in labels)
        seen = Counter()
        for lab in labels:
            c = signs[lab]["nbr_class"]
            seen[c] += 1
            if seen[c] > NBR_CLASS_CAP and c != MIDDLE:
                reassignments.append(
                    {"sign": lab, "from": CLASS_NAMES[c],
                     "to": "MIDDLE",
                     "rule": "Amendment 1 neighbor-class cap 12; "
                             "excess to MIDDLE (largest census pool)"})
                ncount[c] -= 1
                ncount[MIDDLE] += 1
                signs[lab]["nbr_class"] = MIDDLE
    for lab in labels:
        lo, hi = MASS_BY_CLASS[signs[lab]["nbr_class"]] \
            if tuple(nbr_classes) == (FIRST, MIDDLE, LAST) \
            else (0.55, 0.85)
        signs[lab]["m"] = rng.uniform(lo, hi)
    for comp in ("fitting", "scoring"):
        for lab in labels:
            signs[lab]["quota_raw_" + comp] = rng.randint(QUOTA_LO,
                                                          QUOTA_HI)
    return labels, signs, reassignments


def scale_quotas(raw, budget):
    """The draft section 4.3 largest-remainder scaling, unchanged
    except the floor (12, amended). Returns (quotas, engaged)."""
    total = sum(raw.values())
    if total <= budget:
        return dict(raw), False
    labels = sorted(raw)
    scaled = {lab: raw[lab] * budget / total for lab in labels}
    q = {}
    for lab in labels:
        q[lab] = max(QUOTA_FLOOR, math.floor(scaled[lab]))
    diff = budget - sum(q.values())
    while diff > 0:
        best = max(labels, key=lambda lab: (scaled[lab] - q[lab],
                                            -labels.index(lab)))
        q[best] += 1
        diff -= 1
    while diff < 0:
        cands = [lab for lab in labels if q[lab] > QUOTA_FLOOR]
        assert cands, "budget below 44*12 floor sum"
        best = min(cands, key=lambda lab: (scaled[lab] - q[lab],
                                           -labels.index(lab)))
        q[best] -= 1
        diff += 1
    assert sum(q.values()) == budget
    return q, True


def c_max_for(solo_slots):
    return math.floor(min(ONLY_FAMILY_CAP_TOKENS,
                          ONLY_FAMILY_CAP_FRAC * solo_slots))


def compute_cells(quota, a, pos_cls, base_shares, c_max):
    """Amended cell construction. Returns (cells, info)."""
    cells = [0, 0, 0, 0]
    uncapped = round_half_up(a * quota)
    info = {"uncapped_planted_cell": uncapped}
    if pos_cls == ONLY:
        planted = min(uncapped, c_max)
        recipients = [FIRST, MIDDLE, LAST]
        info["capped"] = planted < uncapped
        info["a_eff"] = planted / quota
    else:
        planted = uncapped
        recipients = [c for c in (FIRST, MIDDLE, LAST) if c != pos_cls]
        info["capped"] = False
        info["a_eff"] = a
    cells[pos_cls] = planted
    remaining = quota - planted
    share_sum = sum(base_shares[c] for c in recipients)
    ideal = {c: remaining * base_shares[c] / share_sum
             for c in recipients}
    for c in recipients:
        cells[c] = math.floor(ideal[c])
    left = remaining - sum(cells[c] for c in recipients)
    while left > 0:
        best = max(recipients,
                   key=lambda c: (ideal[c] - cells[c], -c))
        cells[best] += 1
        left -= 1
    assert sum(cells) == quota
    return cells, info


def compilation_capacity(records):
    """The per-source-sign cap's funding capacity of a compilation:
    aggregate, and per class the sum over sources of
    min(cap_s, tokens of s sitting in that class). Necessary
    conditions for implantation under draft section 4.5's cap."""
    tot = Counter()
    slot_src = [Counter() for _ in range(4)]
    for r in records:
        seq = r["seq"]
        L = len(seq)
        for j, t in enumerate(seq):
            tot[t] += 1
            slot_src[pos_class(j, L)][t] += 1
    cap = {s: min(30, math.floor(0.20 * n)) for s, n in tot.items()}
    per_class = []
    for c in range(4):
        per_class.append(sum(min(cap[s], slot_src[c][s]) for s in tot))
    return {"aggregate": sum(cap.values()),
            "per_class": per_class,
            "slot_pools": [sum(slot_src[c].values()) for c in range(4)]}

# ============ auditor (verbatim body) ============
F, M, L, O = 0, 1, 2, 3
NAMES = ["FIRST", "MIDDLE", "LAST", "ONLY"]


def _cls(i, n):
    if n == 1:
        return O
    if i == 0:
        return F
    if i == n - 1:
        return L
    return M


def _profiles(seqs):
    per = defaultdict(Counter)
    for seq in seqs:
        n = len(seq)
        for i, s in enumerate(seq):
            per[s][_cls(i, n)] += 1
    out = {}
    for s, cnt in per.items():
        t = sum(cnt.values())
        out[s] = [cnt[c] / t for c in range(4)]
    return out


def _evidence(seq, i, prof):
    n = len(seq)
    acc = [0.0, 0.0, 0.0, 0.0]
    k = 0
    if i > 0 and seq[i - 1] in prof:
        p = prof[seq[i - 1]]
        for c in range(4):
            acc[c] += p[c]
        k += 1
    if i < n - 1 and seq[i + 1] in prof:
        p = prof[seq[i + 1]]
        for c in range(4):
            acc[c] += p[c]
        k += 1
    if k == 0:
        return None
    return [x / k for x in acc]


def _nbr_means(seqs, prof, targets):
    """Mean neighbor evidence per class for each target sign, and
    neighbor-bearing counts."""
    sums = {s: [0.0, 0.0, 0.0, 0.0] for s in targets}
    bear = {s: 0 for s in targets}
    want = set(targets)
    for seq in seqs:
        n = len(seq)
        for i, s in enumerate(seq):
            if s not in want:
                continue
            ev = _evidence(seq, i, prof)
            if ev is None:
                continue
            for c in range(4):
                sums[s][c] += ev[c]
            bear[s] += 1
    means = {}
    for s in targets:
        if bear[s] > 0:
            means[s] = [x / bear[s] for x in sums[s]]
        else:
            means[s] = None
    return means, bear


def _argmax(vals):
    b = 0
    for c in range(1, 4):
        if vals[c] > vals[b]:
            b = c
    return b


def audit(ledger, orig, impl):
    """ledger: label -> params with cells_<comp>, quota_<comp>,
    nbr_class, m. orig/impl: {"fitting": records, "scoring":
    records} of {"id","seq"}. Returns the gate report dict."""
    labels = sorted(ledger)
    rep = {"R1": {}, "R2": {}, "R3": {}, "R4": {}}
    seqs_impl = {name: [r["seq"] for r in impl[name]] for name in impl}
    seqs_orig = {name: [r["seq"] for r in orig[name]] for name in orig}

    # ---- R1: position realization, exact
    r1_fail = []
    argmax_ok = {}
    for name in ("fitting", "scoring"):
        counts = {lab: [0, 0, 0, 0] for lab in labels}
        for seq in seqs_impl[name]:
            n = len(seq)
            for i, s in enumerate(seq):
                if s in counts:
                    counts[s][_cls(i, n)] += 1
        ok = 0
        for lab in labels:
            if counts[lab] != ledger[lab]["cells_" + name]:
                r1_fail.append({"compilation": name, "sign": lab,
                                "realized": counts[lab],
                                "ledger": ledger[lab]["cells_" + name]})
            realized = counts[lab]
            if _argmax(realized) == ledger[lab]["pos_class"] and \
                    realized.count(max(realized)) == 1:
                ok += 1
        argmax_ok[name] = ok
    rep["R1"] = {"pass": not r1_fail, "failures": r1_fail[:10],
                 "planted_class_unique_argmax": argmax_ok}

    # ---- R2: neighbor realization
    prof = _profiles(seqs_impl["fitting"])
    r2 = {}
    for name, tol in (("scoring", 0.08), ("fitting", 0.12)):
        means, bear = _nbr_means(seqs_impl[name], prof, labels)
        per_sign = {}
        diffs = []
        misses = []
        unscored = []
        for lab in labels:
            if means[lab] is None:
                unscored.append(lab)
                continue
            d = ledger[lab]["nbr_class"]
            realized = means[lab][d]
            diff = realized - ledger[lab]["m"]
            diffs.append(diff)
            am = _argmax(means[lab])
            if am != d:
                misses.append({"sign": lab,
                               "planted": NAMES[d],
                               "realized_argmax": NAMES[am],
                               "realized_means": means[lab]})
            per_sign[lab] = {"realized": realized, "diff": diff,
                             "within_tol": abs(diff) <= tol,
                             "bearing": bear[lab]}
        entry = {"per_sign_within_tol":
                 all(v["within_tol"] for v in per_sign.values()),
                 "n_unscored": len(unscored), "unscored": unscored,
                 "argmax_misses": misses}
        if name == "scoring":
            fam = (sum(diffs) / len(diffs)) if diffs else None
            entry["family_mean_signed_diff"] = fam
            entry["family_mean_within_0.03"] = (
                fam is not None and abs(fam) <= 0.03)
            entry["pass"] = (entry["per_sign_within_tol"]
                             and entry["family_mean_within_0.03"]
                             and len(misses) <= 4)
        else:
            entry["pass"] = entry["per_sign_within_tol"]
        entry["max_abs_diff"] = (max((abs(d) for d in diffs),
                                     default=None))
        r2[name] = entry
    rep["R2"] = r2

    # ---- R3: background integrity, exact
    r3 = {}
    for name in ("fitting", "scoring"):
        o, im = seqs_orig[name], seqs_impl[name]
        lo = Counter(len(s) for s in o)
        li = Counter(len(s) for s in im)
        def roles(ss):
            t = [0, 0, 0, 0]
            for seq in ss:
                n = len(seq)
                for i in range(n):
                    t[_cls(i, n)] += 1
            return t
        away = Counter()
        relabeled = 0
        for so, si in zip(o, im):
            for a, b in zip(so, si):
                if a != b:
                    away[a] += 1
                    relabeled += 1
        src_tot = Counter()
        for seq in o:
            for t in seq:
                src_tot[t] += 1
        cap_breaks = [{"source": s, "away": away[s],
                       "cap": min(30, math.floor(0.20 * src_tot[s]))}
                      for s in away
                      if away[s] > min(30, math.floor(0.20 * src_tot[s]))]
        toks = sum(src_tot.values())
        solos = sum(1 for s in o if len(s) == 1)
        fam_only = sum(ledger[lab]["cells_" + name][O] for lab in labels)
        entry = {
            "inscriptions_equal": len(o) == len(im),
            "length_multiset_equal": lo == li,
            "tokens_equal": sum(lo.elements()) == sum(li.elements()),
            "role_totals_equal": roles(o) == roles(im),
            "relabeled_total": relabeled,
            "budget": math.floor(0.20 * toks),
            "relabeled_within_budget": relabeled <= math.floor(0.20 * toks),
            "per_source_cap_breaks": cap_breaks[:10],
            "family_ONLY_cells": fam_only,
            "family_ONLY_cap": min(30, 0.25 * solos),
            "family_ONLY_within_cap": fam_only <= min(30, 0.25 * solos),
        }
        entry["pass"] = all([entry["inscriptions_equal"],
                             entry["length_multiset_equal"],
                             entry["tokens_equal"],
                             entry["role_totals_equal"],
                             entry["relabeled_within_budget"],
                             not cap_breaks,
                             entry["family_ONLY_within_cap"]])
        r3[name] = entry
    rep["R3"] = r3

    # ---- R4: support and testability
    sco_counts = Counter()
    for seq in seqs_impl["scoring"]:
        for t in seq:
            if t in ledger:
                sco_counts[t] += 1
    r4_fail = [{"sign": lab, "realized": sco_counts[lab],
                "ledger_quota": ledger[lab]["quota_scoring"]}
               for lab in labels
               if sco_counts[lab] != ledger[lab]["quota_scoring"]]
    rep["R4"] = {"pass": not r4_fail, "failures": r4_fail[:10],
                 "neighbor_unscored_signs": r2["scoring"]["unscored"]}
    rep["pass"] = (rep["R1"]["pass"] and rep["R2"]["scoring"]["pass"]
                   and rep["R2"]["fitting"]["pass"]
                   and all(rep["R3"][n]["pass"]
                           for n in ("fitting", "scoring"))
                   and rep["R4"]["pass"])
    return rep

# ============ SIGIL generator (verbatim, g44s.py) ==
N_TYPES = 557
N_INSC = 3045
TIER_QUOTAS = {}
for _e in range(0, 4):
    TIER_QUOTAS[_e] = 500          # tier A
for _e in range(4, 24):
    TIER_QUOTAS[_e] = 150          # tier B
for _e in range(24, 104):
    TIER_QUOTAS[_e] = 40           # tier C
for _e in range(104, 429):
    TIER_QUOTAS[_e] = 8            # tier D, 325 emblems
for _e in range(429, 557):
    TIER_QUOTAS[_e] = 7            # tier D, 128 emblems
DEAL_STRIDE = 4531                 # coprime to 11,696
LENGTH_COUNTS = {1: 244, 2: 521, 3: 759, 4: 600, 5: 380,
                 6: 230, 7: 145, 8: 85, 9: 52, 10: 29}
LENGTH_STRIDE = 1124               # coprime to 3,045
SOLO_BAND = (0.06, 0.10)           # calibration check 5 band (compliance file)
# --------------------------------------------------------- SIGIL-class gen
def build_sigil():
    """Deterministic structured non-language corpus (compliance file
    section 1): quota-dealt emblem stream, fixed length cycle. No RNG
    anywhere in the construction."""
    token_list = []
    for e in range(N_TYPES):
        token_list.extend([e] * TIER_QUOTAS[e])
    n_tok = len(token_list)
    stream = [token_list[(p * DEAL_STRIDE) % n_tok] for p in range(n_tok)]
    lengths_multiset = []
    for L in sorted(LENGTH_COUNTS):
        lengths_multiset.extend([L] * LENGTH_COUNTS[L])
    n_insc = len(lengths_multiset)
    lengths = [lengths_multiset[(j * LENGTH_STRIDE) % n_insc]
               for j in range(n_insc)]
    inscriptions = []
    pos = 0
    for L in lengths:
        inscriptions.append(tuple(stream[pos:pos + L]))
        pos += L
    counts = Counter(tok for seq in inscriptions for tok in seq)
    total = sum(counts.values())
    solo_share = sum(1 for seq in inscriptions if len(seq) == 1) / len(inscriptions)
    calib = {
        "inscriptions": len(inscriptions),
        "total_tokens": total,
        "distinct_types": len(counts),
        "top_type_share": max(counts.values()) / total,
        "length1_share": solo_share,
    }
    calib["checks"] = {
        "1_inscriptions_eq_3045": calib["inscriptions"] == N_INSC,
        "2_types_eq_557": calib["distinct_types"] == N_TYPES,
        "3_tokens_in_band": 11215 <= calib["total_tokens"] <= 12395,
        "4_top_share_ge_0.04": calib["top_type_share"] >= 0.04,
        "5_length1_share_in_band": SOLO_BAND[0] <= solo_share <= SOLO_BAND[1],
    }
    calib["pass"] = all(calib["checks"].values())
    return inscriptions, calib


# ================= RUNNER (G44-I rerun) =================
# Everything above this section is the tested machinery, embedded
# verbatim from the Amendment 1 design-stage modules (implant_lib,
# amended_ledger, auditor). The runner below only orchestrates:
# pins, split, stages, checkpoints, markers, verdict.

CONFIG = {
    "model_seed": 20280865,
    "split_seed": 20281686,
    "leg2_seed": 20281727,
    "leg3_seed": 20284065,
    "population_sha256":
        "f1d984c546c77bbd5459895e9ab31b877dd7a2af69a88ff4248049bf11e8811c",
    "amendment_sha256":
        "b1bdb05319e844eac02ca9a01d60230f35e9e8c32703148fd1dc36075008e670",
    "draft_sha256":
        "53b4ae9e3b00c13643057119b073a8fa14af8216101928608f66a6e2125389da",
}
PKG_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(PKG_DIR, "output")
CONFIG_SHA = hashlib.sha256(
    json.dumps(CONFIG, sort_keys=True).encode()).hexdigest()
LABELS = ["G44I-%02d" % i for i in range(1, 45)]
STEP0 = [3045, 557, 11805, 550]

_mfh = None


def marker(line):
    print(line, flush=True)
    if _mfh is not None:
        _mfh.write(line + "\n")
        _mfh.flush()


def _enc_label(x):
    return ("i:" + str(x)) if isinstance(x, int) else ("s:" + str(x))


def _dec_label(s):
    return int(s[2:]) if s.startswith("i:") else s[2:]


def _enc_stream(recs):
    return [{"id": r["id"],
             "seq": [_enc_label(t) for t in r["seq"]]} for r in recs]


def _dec_stream(recs):
    return [{"id": r["id"],
             "seq": [_dec_label(t) for t in r["seq"]]} for r in recs]


def _enc_profiles(prof):
    return [[_enc_label(k), v] for k, v in prof.items()]


def _dec_profiles(pairs):
    return {_dec_label(k): v for k, v in pairs}


def finalize_ledger(signs, comps):
    """Ledger finalization, replicating the Amendment 1 design-stage
    rehearsal exactly: per compilation, budget scaling of the drawn
    quotas, amended cell construction, and the feasibility battery
    (family ONLY cap, aggregate cap capacity, per-class cap
    capacity). Returns (signs, feasibility-by-compilation)."""
    labels = list(signs.keys())
    feas = {}
    for name, comp in comps.items():
        rt = role_totals([r["seq"] for r in comp])
        tt = sum(rt)
        shares = [rt[c] / tt for c in range(4)]
        solos = sum(1 for r in comp if len(r["seq"]) == 1)
        budget = math.floor(0.20 * tt)
        raw = {lab: signs[lab]["quota_raw_" + name] for lab in labels}
        quotas, engaged = scale_quotas(raw, budget)
        cmax = c_max_for(solos)
        for lab in labels:
            signs[lab]["quota_" + name] = quotas[lab]
            cells, info = compute_cells(
                quotas[lab], signs[lab]["a"], signs[lab]["pos_class"],
                shares, cmax)
            signs[lab]["cells_" + name] = cells
            signs[lab]["cell_info_" + name] = info
            signs[lab]["q_" + name] = [cells[c] / quotas[lab]
                                       for c in range(4)]
        demand = [sum(signs[lab]["cells_" + name][c] for lab in labels)
                  for c in range(4)]
        capacity = compilation_capacity(comp)
        feas[name] = {
            "quota_sum": sum(quotas.values()),
            "budget": budget,
            "scaling_engaged": engaged,
            "demand_by_class": {CLASS_NAMES[c]: demand[c]
                                for c in range(4)},
            "capacity_per_class": {
                CLASS_NAMES[c]: capacity["per_class"][c]
                for c in range(4)},
            "capacity_aggregate": capacity["aggregate"],
            "feasible": (
                demand[ONLY] <= min(30, 0.25 * solos)
                and sum(quotas.values()) <= capacity["aggregate"]
                and all(demand[c] <= capacity["per_class"][c]
                        for c in range(4))),
        }
    return signs, feas


def _ckpt(stage):
    return os.path.join(OUT_DIR, "checkpoint_%s.json" % stage)


def save_ckpt(stage, payload):
    doc = {"stage": stage, "config_sha": CONFIG_SHA, "payload": payload}
    h = hashlib.sha256(
        json.dumps(doc, sort_keys=True).encode()).hexdigest()
    doc["payload_sha256"] = h
    with open(_ckpt(stage), "w", encoding="utf-8") as f:
        json.dump(doc, f)
    marker("G44I_STAGE %s DONE sha256=%s" % (stage, h))
    return payload


def load_ckpt(stage):
    if not os.path.exists(_ckpt(stage)):
        return None
    doc = json.load(open(_ckpt(stage), encoding="utf-8"))
    if doc.get("config_sha") != CONFIG_SHA:
        print("checkpoint configuration mismatch at", stage)
        sys.exit(4)
    marker("G44I_STAGE %s SKIPPED sha256=%s"
           % (stage, doc.get("payload_sha256")))
    return doc["payload"]


def seeded_split(records, split_seed):
    rng = random.Random(split_seed)
    bands = {}
    for idx, rec in enumerate(records):
        bands.setdefault(len(rec["seq"]), []).append(idx)
    order = []
    for length in sorted(bands):
        band = sorted(bands[length])
        rng.shuffle(band)
        order.extend(band)
    fit = [records[i] for i in order[0::2]]
    sco = [records[i] for i in order[1::2]]
    return fit, sco, order


def finish(results, code=0):
    with open(os.path.join(OUT_DIR, "results.json"), "w",
              encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    marker("G44I_DONE")
    return code


def main():
    global _mfh
    os.makedirs(OUT_DIR, exist_ok=True)
    _mfh = open(os.path.join(OUT_DIR, "markers.txt"), "a",
                encoding="utf-8")
    results = {"config": CONFIG, "config_sha": CONFIG_SHA}

    # ---- S0: input pins + step 0
    p = load_ckpt("S0")
    if p is None:
        raw = open(os.path.join(PKG_DIR, "population.json"),
                   "rb").read()
        if hashlib.sha256(raw).hexdigest() != \
                CONFIG["population_sha256"]:
            print("population.json SHA-256 pin mismatch")
            return 2
        pop = json.loads(raw)
        seqs = [r["seq"] for r in pop]
        counts = [len(pop),
                  len({t for s in seqs for t in s}),
                  sum(len(s) for s in seqs),
                  len({t for s in seqs if len(s) >= 2 for t in s})]
        if counts != STEP0:
            print("step 0 mismatch:", counts)
            return 2
        p = save_ckpt("S0", {"step0": counts})
    results["step0"] = p["step0"]
    pop = json.loads(open(os.path.join(PKG_DIR, "population.json"),
                          encoding="utf-8").read())
    records = [{"id": i, "seq": r["seq"]}
               for i, r in enumerate(pop)]

    # ---- S1: split + ledger + feasibility battery
    p = load_ckpt("S1")
    if p is None:
        fit, sco, order = seeded_split(records, CONFIG["split_seed"])
        _labels, signs, reas = draw_ledger(CONFIG["model_seed"])
        signs, feas = finalize_ledger(
            signs, {"fitting": fit, "scoring": sco})
        halt = None
        if not all(feas[c]["feasible"]
                   for c in ("fitting", "scoring")):
            halt = "ledger feasibility battery failed"
        if halt is None and any(signs[l]["pos_class"] == ONLY
                                for l in _labels):
            for cname, comp in (("fitting", fit), ("scoring", sco)):
                solos = sum(1 for r in comp if len(r["seq"]) == 1)
                if c_max_for(solos) < C_MAX_MIN:
                    halt = ("C_max precondition failed in " + cname)
        if halt is not None:
            marker("G44I_HALT " + halt)
            results["halt"] = {"stage": "S1", "reason": halt,
                               "feasibility": feas}
            return finish(results, 3)
        p = save_ckpt("S1", {
            "order": order, "signs": signs, "reassignments": reas,
            "feasibility": feas,
            "split_counts": {
                "fitting": len(fit), "scoring": len(sco),
                "fitting_tokens": sum(len(r["seq"]) for r in fit),
                "scoring_tokens": sum(len(r["seq"]) for r in sco)}})
    signs = p["signs"]
    fit = [records[i] for i in p["order"][0::2]]
    sco = [records[i] for i in p["order"][1::2]]
    results["split_counts"] = p["split_counts"]
    results["feasibility"] = p["feasibility"]

    # ---- S2: fitting implantation + final profiles + census
    p = load_ckpt("S2")
    if p is None:
        provisional, _ = build_profiles([r["seq"] for r in fit])
        impl_fit, log1 = implant(fit, signs, "fitting", provisional)
        final_profiles, final_totals = build_profiles(
            [r["seq"] for r in impl_fit])
        P = [0, 0, 0, 0]
        bearing = 0
        total_att = 0
        for seq in [r["seq"] for r in sco]:
            for i in range(len(seq)):
                total_att += 1
                ev = attestation_evidence(seq, i, final_profiles)
                if ev is None:
                    continue
                bearing += 1
                for c in range(4):
                    if ev[c] >= 0.55:
                        P[c] += 1
        if any(P[c] < 300 for c in (FIRST, MIDDLE, LAST)):
            marker("G44I_HALT in-run census eligibility "
                   "disagreement: P=" + json.dumps(P))
            results["halt"] = {"stage": "S2",
                               "reason": "census eligibility "
                                         "disagreement",
                               "census_P": P}
            return finish(results, 3)
        p = save_ckpt("S2", {
            "impl_fit": _enc_stream(impl_fit),
            "final_profiles": _enc_profiles(final_profiles),
            "final_totals": _enc_profiles(final_totals),
            "census": {"P": P, "bearing": bearing, "total": total_att},
            "relabels_fitting": len(log1)})
    impl_fit = _dec_stream(p["impl_fit"])
    final_profiles = _dec_profiles(p["final_profiles"])
    final_totals = _dec_profiles(p["final_totals"])
    results["census"] = p["census"]
    results["relabels_fitting"] = p["relabels_fitting"]

    # ---- S3: scoring implantation
    p = load_ckpt("S3")
    if p is None:
        impl_sco, log2 = implant(sco, signs, "scoring",
                                 final_profiles)
        p = save_ckpt("S3", {"impl_sco": _enc_stream(impl_sco),
                             "relabels_scoring": len(log2)})
    impl_sco = _dec_stream(p["impl_sco"])
    results["relabels_scoring"] = p["relabels_scoring"]

    # ---- S4: adequacy gate (independent recount)
    p = load_ckpt("S4")
    if p is None:
        rep = audit(signs, {"fitting": fit, "scoring": sco},
                    {"fitting": impl_fit, "scoring": impl_sco})
        p = save_ckpt("S4", {"report": rep})
    rep = p["report"]
    r2s = rep["R2"]["scoring"]
    r2f = rep["R2"]["fitting"]
    r3_pass = (rep["R3"]["fitting"]["pass"]
               and rep["R3"]["scoring"]["pass"])
    marker("G44I_GATE %s R1=%s R2s_max=%.4f R2s_fam=%+.4f "
           "R2f_max=%.4f misses=%d R3=%s R4=%s"
           % ("PASS" if rep["pass"] else "FAIL", rep["R1"]["pass"],
              r2s["max_abs_diff"], r2s["family_mean_signed_diff"],
              r2f["max_abs_diff"], len(r2s["argmax_misses"]),
              r3_pass, rep["R4"]["pass"]))
    results["gate"] = rep
    if not rep["pass"]:
        results["verdict_code"] = "INCOMPLETE_IMPLANTATION_DEFECT"
        results["verdict"] = "INCOMPLETE — IMPLANTATION DEFECT"
        marker("G44I_VERDICT INCOMPLETE — IMPLANTATION DEFECT")
        return finish(results)

    # ---- S5: legs 1, 1B, 2 + OD-1 quantities
    p = load_ckpt("S5")
    if p is None:
        fit_stats = population_stats([r["seq"] for r in impl_fit],
                                     final_profiles)
        sco_stats = population_stats([r["seq"] for r in impl_sco],
                                     final_profiles)
        corp = corpus_profile(final_profiles, final_totals)
        batch = {lab: (signs[lab]["pos_class"],
                       signs[lab]["nbr_class"]) for lab in LABELS}
        bres = batch_score(batch, sco_stats)
        baseline = baseline_assignment(LABELS, final_profiles,
                                       fit_stats, corp)
        bbase = batch_score(baseline, sco_stats)
        margin = bres["B"] - bbase["B"]
        null = permutation_null(batch, sco_stats,
                                CONFIG["leg2_seed"])
        ns = null_summary(null, bres["B"])

        def half(labs):
            pv = [bres["per_sign"][l]["pos_comp"] for l in labs
                  if bres["per_sign"][l]["pos_comp"] is not None]
            nv = [bres["per_sign"][l]["nbr_comp"] for l in labs
                  if bres["per_sign"][l]["nbr_comp"] is not None]
            return {"mean_pos": (sum(pv) / len(pv)) if pv else None,
                    "mean_nbr": (sum(nv) / len(nv)) if nv else None}

        h1 = half(LABELS[:22])
        h2 = half(LABELS[22:])
        leg1 = (bres["B"] >= 0.60 and bres["recovered"] >= 33
                and h1["mean_pos"] is not None
                and h1["mean_pos"] >= 0.55
                and h2["mean_pos"] is not None
                and h2["mean_pos"] >= 0.55
                and h1["mean_nbr"] is not None
                and h1["mean_nbr"] >= 0.45
                and h2["mean_nbr"] is not None
                and h2["mean_nbr"] >= 0.45)
        full = sum(1 for l in LABELS
                   if baseline[l] == batch[l])
        pos_only = sum(1 for l in LABELS
                       if baseline[l][0] == batch[l][0]
                       and baseline[l][1] != batch[l][1])
        nbr_only = sum(1 for l in LABELS
                       if baseline[l][1] == batch[l][1]
                       and baseline[l][0] != batch[l][0])
        p = save_ckpt("S5", {
            "batch": bres, "baseline_B": bbase["B"],
            "baseline": {l: [baseline[l][0], baseline[l][1]]
                         for l in LABELS},
            "margin": margin, "null": ns,
            "halves": {"first": h1, "second": h2},
            "leg1_pass": leg1,
            "leg1b_pass": margin >= MARGIN_BAR,
            "leg2_pass": bres["B"] > ns["p95"],
            "od1": {"full": full, "pos_only": pos_only,
                    "nbr_only": nbr_only,
                    "pos_total": full + pos_only,
                    "nbr_total": full + nbr_only}})
    bres = p["batch"]
    marker("G44I_LEG1 B=%.4f recovered=%d/44 mean_pos=%.4f "
           "mean_nbr=%.4f %s"
           % (bres["B"], bres["recovered"], bres["mean_pos"],
              bres["mean_nbr"],
              "PASS" if p["leg1_pass"] else "FAIL"))
    marker("G44I_LEG1B B_baseline=%.4f margin=%+.4f %s"
           % (p["baseline_B"], p["margin"],
              "PASS" if p["leg1b_pass"] else "FAIL"))
    marker("G44I_LEG2 p95=%.4f share_ge=%.4f %s"
           % (p["null"]["p95"], p["null"]["share_ge"],
              "PASS" if p["leg2_pass"] else "FAIL"))
    results["leg1"] = {"B": bres["B"], "recovered": bres["recovered"],
                       "mean_pos": bres["mean_pos"],
                       "mean_nbr": bres["mean_nbr"],
                       "halves": p["halves"], "pass": p["leg1_pass"],
                       "per_sign": bres["per_sign"]}
    results["leg1b"] = {"B_baseline": p["baseline_B"],
                        "margin": p["margin"],
                        "pass": p["leg1b_pass"]}
    results["leg2"] = {"null": p["null"], "pass": p["leg2_pass"]}
    results["od1"] = p["od1"]
    results["od1"]["margin"] = p["margin"]
    marker("G44I_OD1 full=%d pos_only=%d nbr_only=%d margin=%+.4f"
           % (p["od1"]["full"], p["od1"]["pos_only"],
              p["od1"]["nbr_only"], p["margin"]))

    # ---- S6: leg 3 (calibration checks first, then arms 3A/3B)
    p = load_ckpt("S6")
    if p is None:
        calib_seen = None
        try:
            fake, calib = build_sigil()
            calib_seen = calib
            marker("G44I_LEG3_CALIB insc=%d types=%d tokens=%d "
                   "top=%.4f len1=%.4f %s"
                   % (calib["inscriptions"], calib["distinct_types"],
                      calib["total_tokens"], calib["top_type_share"],
                      calib["length1_share"],
                      "PASS" if calib["pass"] else "FAIL"))
            if not calib["pass"]:
                p = save_ckpt("S6", {"calib": calib,
                                     "notrun": "calibration"})
            else:
                frec = [{"id": i, "seq": list(t)}
                        for i, t in enumerate(fake)]
                ffit = frec[0::2]
                fsco = frec[1::2]
                fprof, ftot = build_profiles([r["seq"] for r in ffit])
                ffit_stats = population_stats(
                    [r["seq"] for r in ffit], fprof)
                fcorp = corpus_profile(fprof, ftot)
                cnt = Counter(t for r in ffit for t in r["seq"])
                batch_types = sorted(cnt,
                                     key=lambda t: (-cnt[t], t))[:44]
                base_fake = baseline_assignment(batch_types, fprof,
                                                ffit_stats, fcorp)
                # arm 3A: the batch is the baseline assignment
                stats_a = population_stats(
                    [r["seq"] for r in fsco], fprof)
                bres_a = batch_score(base_fake, stats_a)
                null_a = permutation_null(base_fake, stats_a,
                                          CONFIG["leg3_seed"])
                cert_a = certification_conditions(
                    bres_a, 0.0, bres_a["B"],
                    null_summary(null_a, bres_a["B"]))
                # arm 3B: working ledger under the amended draw;
                # k-th label-order entry pairs with the k-th batch
                # type in frequency order
                wlabels, wsigns, _w = draw_ledger(
                    CONFIG["model_seed"])
                fsigns = {}
                for k, t in enumerate(batch_types):
                    fsigns[t] = dict(wsigns[wlabels[k]])
                fsigns, _ff = finalize_ledger(
                    fsigns, {"fitting": ffit, "scoring": fsco})
                impl_ffit, _l = implant(ffit, fsigns, "fitting",
                                        fprof)
                prof3b, tot3b = build_profiles(
                    [r["seq"] for r in impl_ffit])
                fit_stats3b = population_stats(
                    [r["seq"] for r in impl_ffit], prof3b)
                corp3b = corpus_profile(prof3b, tot3b)
                pairs3b = baseline_assignment(batch_types, prof3b,
                                              fit_stats3b, corp3b)
                rt_s = role_totals([r["seq"] for r in fsco])
                tt = sum(rt_s)
                shares_s = [rt_s[c] / tt for c in range(4)]
                solos_s = sum(1 for r in fsco
                              if len(r["seq"]) == 1)
                cmax_s = c_max_for(solos_s)
                for t in batch_types:
                    fsigns[t]["pos_class"] = pairs3b[t][0]
                    fsigns[t]["nbr_class"] = pairs3b[t][1]
                    cells, info = compute_cells(
                        fsigns[t]["quota_scoring"], fsigns[t]["a"],
                        pairs3b[t][0], shares_s, cmax_s)
                    fsigns[t]["cells_scoring"] = cells
                    fsigns[t]["cell_info_scoring"] = info
                    fsigns[t]["q_scoring"] = [
                        cells[c] / fsigns[t]["quota_scoring"]
                        for c in range(4)]
                impl_fsco, _l2 = implant(fsco, fsigns, "scoring",
                                         prof3b)
                stats_b = population_stats(
                    [r["seq"] for r in impl_fsco], prof3b)
                bres_b = batch_score(pairs3b, stats_b)
                # the arm's planted pairs ARE the baseline pairs on
                # the implanted fake fitting compilation, so the
                # margin against that baseline is zero by
                # construction (draft 7.4's stated expectation)
                null_b = permutation_null(pairs3b, stats_b,
                                          CONFIG["leg3_seed"])
                cert_b = certification_conditions(
                    bres_b, 0.0, bres_b["B"],
                    null_summary(null_b, bres_b["B"]))
                p = save_ckpt("S6", {
                    "calib": calib,
                    "arm3A": {"B": bres_a["B"],
                              "certified": cert_a["certified"],
                              "conditions": cert_a},
                    "arm3B": {"B": bres_b["B"],
                              "certified": cert_b["certified"],
                              "conditions": cert_b},
                    "leg3_pass": (not cert_a["certified"]
                                  and not cert_b["certified"])})
        except ImplantFailure as e:
            p = save_ckpt("S6", {"calib": calib_seen,
                                 "notrun": "implant failure in leg "
                                           "3: %s" % (e.args,)})
    results["leg3"] = {k: v for k, v in p.items()}
    if p.get("notrun"):
        marker("G44I_LEG3 NOTRUN reason=%s" % p["notrun"])
        results["verdict_code"] = "INCOMPLETE_LEG3_NOT_ADMINISTERED"
        results["verdict"] = ("INCOMPLETE — leg 3 could not be "
                              "administered (%s)" % p["notrun"])
        marker("G44I_VERDICT " + results["verdict"])
        return finish(results)
    marker("G44I_LEG3 arm3A_certified=%d arm3B_certified=%d %s"
           % (p["arm3A"]["certified"], p["arm3B"]["certified"],
              "PASS" if p["leg3_pass"] else "FAIL"))

    # ---- S7: K3 + verdict
    legs_pass = (p is not None and results["leg1"]["pass"]
                 and results["leg2"]["pass"] and p["leg3_pass"])
    k3 = bool(legs_pass and results["od1"]["full"] >= 40
              and results["leg1b"]["margin"] <= 0.10)
    marker("G44I_K3 " + ("TRIGGERED" if k3 else "CLEAR"))
    results["k3_triggered"] = k3
    if not (results["leg1"]["pass"] and results["leg2"]["pass"]
            and p["leg3_pass"]):
        results["verdict_code"] = "FAILED"
        results["verdict"] = "FAILED"
    elif results["leg1b"]["pass"]:
        results["verdict_code"] = ("VALIDATED_FLAGGED_K3" if k3
                                   else "VALIDATED_OD1_HELD")
        results["verdict"] = (
            "ALL LEG CONDITIONS MET — VALIDATED"
            + (" — FLAGGED NEAR-TAUTOLOGY (KI-3)" if k3 else "")
            + ", subject to the owner's OD-1 confirmation of leg "
              "1B's certification role (leg 1B passes as printed)")
    else:
        results["verdict_code"] = "OD1_DECIDES_FAILED_OR_VALIDATED"
        results["verdict"] = (
            "ALL LEG CONDITIONS EXCEPT LEG 1B MET — FAILED under "
            "the reading where leg 1B certifies"
            + ("; VALIDATED — FLAGGED NEAR-TAUTOLOGY (KI-3) under "
               "the descriptive reading" if k3 else
               "; VALIDATED under the descriptive reading")
            + " — the owner's OD-1 decision is required")
    marker("G44I_VERDICT " + results["verdict"])
    return finish(results)


if __name__ == "__main__":
    sys.exit(main())
