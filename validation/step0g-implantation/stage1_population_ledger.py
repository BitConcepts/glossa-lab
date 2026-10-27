#!/usr/bin/env python3
"""
G44-I validation, stage 1: pinned population + step 0, split, ledger
draws, budget scaling, position cells, feasibility record.
Implements DESIGN-AND-BARS-G44I.md sections 1, 3, 4 (steps 1-9).
Checkpoints: restricted/population.json, stage1.json, ledger_working.json.
If the section 4 step 9 ONLY-cap feasibility check fails, this stage
reports the breach and the run HALTS before any implantation.
"""
import csv
import hashlib
import json
import math
import random
from collections import Counter

FIRST, MIDDLE, LAST, ONLY = 0, 1, 2, 3
CLASS_NAMES = ["FIRST", "MIDDLE", "LAST", "ONLY"]
SCR = "/home/hatch/workspace/glossa-run/g44i-validation-2026-10-26"
BASE = "/home/hatch/workspace/research_notes/indus-data-deep-sweep-20261008/downloads"
SEED_MODEL = 20270321
SEED_SPLIT = 20270322
N_SIGNS = 44
BUDGET_FRAC = 0.20
QUOTA_FLOOR = 18
ONLY_SIGN_CAP = 3
ONLY_FAMILY_CAP_TOKENS = 30
ONLY_FAMILY_CAP_FRAC = 0.25


def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def pos_class(idx, length):
    if length == 1:
        return ONLY
    if idx == 0:
        return FIRST
    if idx == length - 1:
        return LAST
    return MIDDLE


def role_totals(population):
    tot = [0, 0, 0, 0]
    for seq in population:
        L = len(seq)
        for i in range(L):
            tot[pos_class(i, L)] += 1
    return tot


def round_half_up(x):
    return math.floor(x + 0.5)


# ---------------------------------------------------------------- pins
def check_pins():
    pins = [
        (BASE + "/shaktiosindia-indus-sign-regimes-deposit/sanitized_corpus.json",
         "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"),
        (BASE + "/shakti_row_grades_2026-10-22.csv",
         "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"),
        ("/home/hatch/workspace/glossa-run/spec074-exec/data/crosswalks/canonical_sign_registry_v2.csv",
         "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71"),
    ]
    out = {}
    for path, pin in pins:
        h = sha256_of(path)
        assert h == pin, (path, h)
        out[path.split("/")[-1]] = h
    m77 = "/home/hatch/workspace/glossa-lab/glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.csv"
    h = sha256_of(m77)
    assert h.startswith("9c619bfe"), h
    out["m77_sign_list.csv"] = h
    return out


def build_population():
    corpus = json.load(open(
        BASE + "/shaktiosindia-indus-sign-regimes-deposit/sanitized_corpus.json"))
    grades = {}
    with open(BASE + "/shakti_row_grades_2026-10-22.csv") as f:
        for row in csv.DictReader(f):
            grades[row["shakti_id"]] = row["grade"]
    pop = []
    for r in corpus:
        if grades.get(r["id"]) != "documented-lineage":
            continue
        syms = r["symbols"]
        if not syms or all(s == "000" for s in syms):
            continue
        pop.append({"id": r["id"], "seq": [s for s in syms if s != "000"]})
    return pop


# ---------------------------------------------------------------- ledger
def draw_ledger(model_seed):
    """Draws per DESIGN-AND-BARS section 4 steps 1-6 (pairs, ONLY-cap
    reassignment of position classes, concentrations, neighbor classes,
    masses, raw quotas). Budget scaling and cells are separate steps."""
    rng = random.Random(model_seed)
    labels = ["G44I-%02d" % i for i in range(1, N_SIGNS + 1)]
    signs = {lab: {} for lab in labels}
    # step 1: position classes
    for lab in labels:
        signs[lab]["pos_drawn"] = rng.choices(
            [FIRST, MIDDLE, LAST, ONLY], weights=[0.32, 0.32, 0.32, 0.04])[0]
    # step 2: ONLY cap = 3 signs; excess (4th+ in label order) reassigned
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
                    {"sign": lab, "from": "ONLY", "to": CLASS_NAMES[target],
                     "rule": "ONLY sign cap 3; fewest-assigned class, "
                             "ties FIRST/MIDDLE/LAST"})
                assigned[ONLY] -= 1
                assigned[target] += 1
                signs[lab]["pos_drawn"] = target
    for lab in labels:
        signs[lab]["pos_class"] = signs[lab]["pos_drawn"]
    # step 3: concentrations
    for lab in labels:
        if signs[lab]["pos_class"] == ONLY:
            signs[lab]["a"] = rng.uniform(0.55, 0.70)
        else:
            signs[lab]["a"] = rng.uniform(0.55, 0.85)
    # step 4: neighbor classes (pre-census; eligibility reassignment later)
    for lab in labels:
        signs[lab]["nbr_drawn"] = rng.randrange(4)
        signs[lab]["nbr_class"] = signs[lab]["nbr_drawn"]
    # step 5: target neighbor masses
    for lab in labels:
        signs[lab]["m"] = rng.uniform(0.55, 0.85)
    # step 6: raw quotas per compilation
    for comp in ("fitting", "scoring"):
        for lab in labels:
            if signs[lab]["pos_class"] == ONLY:
                signs[lab]["quota_raw_" + comp] = rng.randint(20, 28)
            else:
                signs[lab]["quota_raw_" + comp] = rng.randint(20, 40)
    return labels, signs, reassignments


def scale_quotas(raw, budget):
    """DESIGN-AND-BARS section 4 step 7: largest-remainder proportional
    scaling to exactly budget, floor 18. Returns (quotas, engaged)."""
    total = sum(raw.values())
    if total <= budget:
        return dict(raw), False
    labels = sorted(raw)
    scaled = {lab: raw[lab] * budget / total for lab in labels}
    q = {}
    for lab in labels:
        v = math.floor(scaled[lab])
        q[lab] = max(QUOTA_FLOOR, v)
    diff = budget - sum(q.values())
    while diff > 0:
        best = max(labels, key=lambda lab: (scaled[lab] - q[lab],
                                            -labels.index(lab)))
        q[best] += 1
        diff -= 1
    while diff < 0:
        cands = [lab for lab in labels if q[lab] > QUOTA_FLOOR]
        assert cands, "budget below 44*18 floor sum"
        best = min(cands, key=lambda lab: (scaled[lab] - q[lab],
                                           -labels.index(lab)))
        q[best] -= 1
        diff += 1
    assert sum(q.values()) == budget
    return q, True


def compute_cells(quota, a, pos_cls, base_shares):
    """DESIGN-AND-BARS section 4 step 8 (draft section 4.4)."""
    cells = [0, 0, 0, 0]
    planted = round_half_up(a * quota)
    cells[pos_cls] = planted
    remaining = quota - planted
    others = [c for c in range(4) if c != pos_cls]
    share_sum = sum(base_shares[c] for c in others)
    ideal = {c: remaining * base_shares[c] / share_sum for c in others}
    for c in others:
        cells[c] = math.floor(ideal[c])
    left = remaining - sum(cells[c] for c in others)
    while left > 0:
        best = max(others, key=lambda c: (ideal[c] - cells[c], -c))
        cells[best] += 1
        left -= 1
    assert sum(cells) == quota
    return cells


def main():
    out = {"stage": "1-population-ledger"}
    out["pins"] = check_pins()
    pop = build_population()
    seqs = [r["seq"] for r in pop]
    toks = sum(len(s) for s in seqs)
    types = {x for s in seqs for x in s}
    ge2 = len({x for s in seqs if len(s) >= 2 for x in s})
    out["step0"] = {"inscriptions": len(pop), "signs": len(types),
                    "tokens": toks, "signs_in_seq_ge2": ge2}
    out["step0_pass"] = (len(pop), len(types), toks, ge2) == (3045, 557, 11805, 550)
    print("STEP 0:", out["step0"], "PASS" if out["step0_pass"] else "MISMATCH")
    assert out["step0_pass"], "step 0 mismatch - cannot run as written"
    assert not any(x.startswith("G44I") for x in types), "label collision"
    out["frame_role_totals"] = {CLASS_NAMES[c]: role_totals(seqs)[c]
                                for c in range(4)}
    json.dump(pop, open(SCR + "/restricted/population.json", "w"))

    # split (record section 3)
    idx = list(range(len(pop)))
    random.Random(SEED_SPLIT).shuffle(idx)
    fit_idx, sco_idx = idx[0::2], idx[1::2]
    comps = {"fitting": [pop[i] for i in fit_idx],
             "scoring": [pop[i] for i in sco_idx]}
    out["split"] = {"fitting_inscriptions": len(comps["fitting"]),
                    "scoring_inscriptions": len(comps["scoring"])}
    comp_info = {}
    for name, comp in comps.items():
        cseqs = [r["seq"] for r in comp]
        rt = role_totals(cseqs)
        tt = sum(rt)
        comp_info[name] = {
            "inscriptions": len(comp),
            "tokens": tt,
            "role_totals": {CLASS_NAMES[c]: rt[c] for c in range(4)},
            "base_shares": [rt[c] / tt for c in range(4)],
            "solo_slots": sum(1 for s in cseqs if len(s) == 1),
            "budget_tokens": math.floor(BUDGET_FRAC * tt),
        }
        print(name, comp_info[name])
    out["compilations"] = comp_info
    json.dump({name: comps[name] for name in comps},
              open(SCR + "/restricted/split.json", "w"))

    # ledger draws
    labels, signs, reassign = draw_ledger(SEED_MODEL)
    out["position_reassignments"] = reassign
    out["drawn_position_counts"] = {
        CLASS_NAMES[c]: sum(1 for lab in labels
                            if signs[lab]["pos_class"] == c)
        for c in range(4)}
    out["drawn_neighbor_counts"] = {
        CLASS_NAMES[c]: sum(1 for lab in labels
                            if signs[lab]["nbr_class"] == c)
        for c in range(4)}
    print("position counts:", out["drawn_position_counts"])
    print("neighbor counts:", out["drawn_neighbor_counts"])

    feasibility = {}
    halt = False
    for name, comp in comps.items():
        info = comp_info[name]
        raw = {lab: signs[lab]["quota_raw_" + name] for lab in labels}
        quotas, engaged = scale_quotas(raw, info["budget_tokens"])
        for lab in labels:
            signs[lab]["quota_" + name] = quotas[lab]
            signs[lab]["cells_" + name] = compute_cells(
                quotas[lab], signs[lab]["a"], signs[lab]["pos_class"],
                info["base_shares"])
            shares = info["base_shares"]
            rest = 1.0 - signs[lab]["a"]
            denom = sum(shares[c] for c in range(4)
                        if c != signs[lab]["pos_class"])
            signs[lab]["q_" + name] = [
                signs[lab]["a"] if c == signs[lab]["pos_class"]
                else rest * shares[c] / denom for c in range(4)]
        only_cells = sum(signs[lab]["cells_" + name][ONLY] for lab in labels)
        only_cap = min(ONLY_FAMILY_CAP_TOKENS,
                       ONLY_FAMILY_CAP_FRAC * info["solo_slots"])
        demand = {CLASS_NAMES[c]: sum(
            signs[lab]["cells_" + name][c] for lab in labels)
            for c in range(4)}
        feasibility[name] = {
            "quota_sum_raw": sum(raw.values()),
            "budget_tokens": info["budget_tokens"],
            "scaling_engaged": engaged,
            "quota_sum_final": sum(quotas.values()),
            "family_ONLY_cells": only_cells,
            "family_ONLY_cap": only_cap,
            "ONLY_cap_satisfied": only_cells <= only_cap,
            "family_demand_by_class": demand,
            "slot_pools": info["role_totals"],
        }
        print(name, "feasibility:", json.dumps(feasibility[name]))
        if not feasibility[name]["ONLY_cap_satisfied"]:
            halt = True
    out["feasibility"] = feasibility
    out["feasibility_halt"] = halt
    json.dump(signs, open(SCR + "/ledger_working.json", "w"), indent=2)
    json.dump(out, open(SCR + "/stage1.json", "w"), indent=2)
    if halt:
        print("HALT: drawn ledger breaches the section 4.7 family ONLY "
              "cap and the draft names no reduction operation for it. "
              "No implantation performed.")
    else:
        print("STAGE 1 COMPLETE: step 0 exact, split built, ledger drawn, "
              "all feasibility caps satisfied as drawn.")
    return out


if __name__ == "__main__":
    main()
