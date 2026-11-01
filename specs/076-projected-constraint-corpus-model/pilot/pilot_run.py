#!/usr/bin/env python3
"""Spec 076 pilot — single frozen run (spec §8, FF-5).

Step 0: reproduction gate over the §7 census (any mismatch -> CANNOT
        BE RUN AS WRITTEN, halt).
Step 1: Tier-C derivation; assert pre-named headline numbers
        (677 exclusions / residual 178 / solo-only 13).
Step 2: marginals-preserving shuffle null, B=999, seed 20261026.
        Bars: real residual 178 below null 5th percentile;
        real solo-only 13 above null 95th percentile.
        (Label permutation is NOT used anywhere.)
Step 3: positive control — blind-coded strict claimed types
        (strict-coding-output.json, coded under CR-1..CR-7 without
        sight of any census row) vs the derivation's possibility
        sets. Bar: exclusions <= 5 among frame-attested strict
        signs; frame-absent strict signs reported separately (CR-7).

Usage: python3 pilot_run.py [coding_output.json]
Writes pilot-results.json beside this script.
"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
INP = HERE / "inputs"
CODING = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "strict-coding-output.json"
SEED = 20261026
B = 999

TYPES = ["ONLY-INIT", "ONLY-FIN", "ONLY-MED", "ONLY-SOLO",
         "NEVER-INIT", "NEVER-FIN", "NEVER-MED", "NEVER-SOLO", "FREE"]


def poss(r):
    i, m, f, s, t = r["init"], r["med"], r["fin"], r["solo"], r["t"]
    out = []
    if not (m + f + s > 0):
        out.append("ONLY-INIT")
    if not (i + m + s > 0):
        out.append("ONLY-FIN")
    if not (i + f + s > 0):
        out.append("ONLY-MED")
    if not (t > s):
        out.append("ONLY-SOLO")
    if not (i > 0):
        out.append("NEVER-INIT")
    if not (f > 0):
        out.append("NEVER-FIN")
    if not (m > 0):
        out.append("NEVER-MED")
    if not (s > 0):
        out.append("NEVER-SOLO")
    out.append("FREE")
    return out


def percentile(sorted_vals, p):
    """Linear-interpolation percentile (numpy 'linear')."""
    n = len(sorted_vals)
    if n == 1:
        return float(sorted_vals[0])
    rank = (p / 100.0) * (n - 1)
    lo = int(rank)
    hi = min(lo + 1, n - 1)
    frac = rank - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def main():
    results = {"seed": SEED, "B": B}
    recs = [json.loads(l) for l in open(INP / "indus_research.jsonl") if l.strip()]
    m77 = [r for r in recs if r["source_system"] == "indusscript-m77"]
    anchors = json.load(open(INP / "INDUS_FINAL_ANCHORS.json"))["anchors"]
    strict = {k[1:] for k, v in anchors.items()
              if v.get("validation_status") == "strict_sa_independent"}
    pending = {k[1:] for k, v in anchors.items()
               if v.get("validation_status") == "pending_non_sa_validation"}
    anchored = {k[1:] for k in anchors}

    n000 = nstar = 0
    seqs = []
    for r in m77:
        toks = []
        for g in r["canonical_grapheme_ids"]:
            if g == "000":
                n000 += 1
            elif g.startswith("*"):
                nstar += 1
            else:
                toks.append(g)
        seqs.append(toks)
    tokens = [t for s in seqs for t in s]
    nonempty = [s for s in seqs if s]
    strict_tokens = sum(1 for t in tokens if t in strict)

    # ---- Step 0: reproduction gate ----
    step0 = {
        "records": len(m77), "dropped_000": n000, "dropped_star": nstar,
        "tokens": len(tokens), "strict_tokens": strict_tokens,
        "nonempty_sequences": len(nonempty),
    }
    expected0 = {"records": 2906, "dropped_000": 680, "dropped_star": 452,
                 "tokens": 11507, "strict_tokens": 5883,
                 "nonempty_sequences": 2880}
    results["step0"] = {**step0, "expected": expected0,
                        "pass": step0 == expected0}
    if not results["step0"]["pass"]:
        results["verdict"] = "CANNOT BE RUN AS WRITTEN"
        (HERE / "pilot-results.json").write_text(json.dumps(results, indent=1) + "\n")
        print(json.dumps(results, indent=1))
        return 1

    # ---- Step 1: derivation ----
    rows = {}
    for s in nonempty:
        if len(s) == 1:
            slots = [(s[0], "solo")]
        else:
            slots = [(s[0], "init"), (s[-1], "fin")] + [(t, "med") for t in s[1:-1]]
        for sign, slot in slots:
            r = rows.setdefault(sign, Counter())
            r[slot] += 1
            r["t"] += 1
    slot_totals = {k: sum(r[k] for r in rows.values())
                   for k in ("init", "fin", "solo", "med")}
    part = Counter()
    for sign, r in rows.items():
        if r["fin"]:
            if sign in strict:
                part["strict"] += r["fin"]
            elif sign in pending:
                part["pending"] += r["fin"]
            elif sign in anchored:
                part["anchored_other"] += r["fin"]
            else:
                part["no_anchor"] += r["fin"]
    u2 = sorted(s for s in rows if s not in anchored)
    poss_map = {s: poss(rows[s]) for s in rows}
    excl_u2 = sum(9 - len(poss_map[s]) for s in u2)
    solo_only = sorted(s for s in rows if rows[s]["solo"] == rows[s]["t"] > 0)
    residual = sum(rows[s]["fin"] for s in u2)
    step1 = {
        "slot_totals": slot_totals,
        "finals_partition": dict(part),
        "u2_signs": len(u2), "u2_exclusions": excl_u2,
        "u2_finals_residual": residual,
        "solo_only_count": len(solo_only), "solo_only": solo_only,
        "pass": (slot_totals == {"init": 2655, "fin": 2655, "solo": 225, "med": 5972}
                 and dict(part) == {"strict": 1707, "pending": 250,
                                    "anchored_other": 520, "no_anchor": 178}
                 and excl_u2 == 677 and residual == 178 and len(solo_only) == 13),
    }
    results["step1"] = step1
    if not step1["pass"]:
        results["verdict"] = "CANNOT BE RUN AS WRITTEN"
        (HERE / "pilot-results.json").write_text(json.dumps(results, indent=1) + "\n")
        print(json.dumps(results, indent=1))
        return 1

    # ---- Step 2: shuffle null ----
    lengths = [len(s) for s in nonempty]
    u2_set = set(u2)
    pool = list(tokens)
    rng = random.Random(SEED)
    null_residual, null_solo = [], []
    for _ in range(B):
        dealt_pool = list(pool)
        rng.shuffle(dealt_pool)
        idx = 0
        res = 0
        solo_ct = Counter()
        other_ct = Counter()
        for L in lengths:
            chunk = dealt_pool[idx:idx + L]
            idx += L
            if L == 1:
                solo_ct[chunk[0]] += 1
            else:
                if chunk[-1] in u2_set:
                    res += 1
                for t in chunk:
                    other_ct[t] += 1
        null_residual.append(res)
        null_solo.append(sum(1 for s in solo_ct if other_ct[s] == 0))
    nr = sorted(null_residual)
    ns = sorted(null_solo)
    p5_res = percentile(nr, 5)
    p95_solo = percentile(ns, 95)
    step2 = {
        "residual_real": residual, "residual_null_p5": p5_res,
        "residual_null_min": nr[0], "residual_null_median": percentile(nr, 50),
        "residual_null_max": nr[-1],
        "residual_empirical_frac_le_real": sum(1 for v in nr if v <= residual) / B,
        "bar_i_pass": residual < p5_res,
        "solo_real": len(solo_only), "solo_null_p95": p95_solo,
        "solo_null_min": ns[0], "solo_null_median": percentile(ns, 50),
        "solo_null_max": ns[-1],
        "solo_empirical_frac_ge_real": sum(1 for v in ns if v >= len(solo_only)) / B,
        "bar_ii_pass": len(solo_only) > p95_solo,
    }
    results["step2"] = step2

    # ---- Step 3: positive control ----
    coding = json.loads(CODING.read_text())
    coded = {c["sign"][1:] if c["sign"].startswith("M") else c["sign"]: c
             for c in coding}
    attested, absent, exclusions = [], [], []
    for sign in sorted(strict):
        c = coded.get(sign)
        assert c is not None, f"missing coding for strict sign {sign}"
        if sign not in rows:
            absent.append({"sign": sign, "coded_type": c["coded_type"]})
            continue
        attested.append(sign)
        if c["coded_type"] not in poss_map[sign]:
            exclusions.append({"sign": sign, "coded_type": c["coded_type"],
                               "poss": poss_map[sign],
                               "row": dict(rows[sign])})
    step3 = {
        "strict_total": len(strict),
        "frame_attested": len(attested),
        "frame_absent": absent,
        "exclusions": exclusions,
        "exclusion_count": len(exclusions),
        "bar_pass": len(exclusions) <= 5,
    }
    results["step3"] = step3

    if not (step2["bar_i_pass"] and step2["bar_ii_pass"]):
        results["verdict"] = ("THE FRAME'S CONSTRAINT STRUCTURE IS NOT "
                              "DISTINGUISHABLE FROM A MARGINALS-PRESERVING "
                              "SCRAMBLE IN THE TESTED FAMILY")
    elif not step3["bar_pass"]:
        results["verdict"] = "ASSUMPTION SET DOES NOT HOLD"
    else:
        results["verdict"] = "PILOT PASSES"
    (HERE / "pilot-results.json").write_text(json.dumps(results, indent=1) + "\n")
    print(json.dumps({k: results[k] for k in ("step0", "step2", "step3", "verdict")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
