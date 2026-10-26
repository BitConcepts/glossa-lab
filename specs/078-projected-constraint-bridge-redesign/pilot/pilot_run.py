#!/usr/bin/env python3
"""Spec 078 pilot — single frozen run (spec §7, FF-078-5).

Step 0: reproduction gate over the inherited census (any mismatch ->
        CANNOT BE RUN AS WRITTEN, halt; the inherited Spec 076 step-2
        standing falls with the census, spec §7.2).
Step 2: NOT re-run — inherited standing from Spec 076 (both bars
        passed wide; seed 20261026; B = 999), cited, per spec §7.2.
Step 3': positive control under NC-1..NC-8 — the blind coding
        (strict-coding-output-nc.json, produced by a coder blind to
        every census row, to the 076 pilot's results, and to the
        design's §6 codings; sealed 2026-10-26T14:37Z, SHA-256
        d63eb914ec62d9faa8e664828f1ef57973a2797400ccf46dc46811b6a851370b)
        checked mechanically against the step-0 census rows:
        - distributional line: a coded type-claim contradicted by the
          sign's row (spec §3.4 arithmetic) = one failure;
        - functional line: anchor share (anchor tokens / total) below
          the frame's base rate for that slot (base rates computed
          from the step-0 census, never quoted) = one failure;
        - summary line: counted and reported with named positions and
          sample sizes; transfer (named position holds the sign's
          plurality in this frame) recorded as a tendency; summaries
          generate no failures.
        Lines: frame-absent strict signs (t = 0) on their own line
        (NC-8); the three worked examples (M002, M342, M347) on their
        own line; the remaining frame-attested strict signs are the
        counted population (frozen definition, FF-078-2; expected 86).
Bars (spec §7.3, frozen, unmoved): administrability — at least 25 of
        the counted signs yield at least one checkable claim; total
        failures <= 3 with neither line above 2; pattern clause
        adjudicated in the pilot record (FF-078-4).

Usage: python3 pilot_run.py
Inputs are read from ./inputs (the three pinned files, fetched from
repo main at the merged freeze and digest-verified before the run).
Writes pilot-results.json beside this script.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INP = HERE / "inputs"
CODING = HERE / "strict-coding-output-nc.json"
WORKED = {"002", "342", "347"}
SLOTS = ["init", "med", "fin", "solo"]
FUNC_ANCHOR = {"TERM-FUNC": "fin", "INIT-FUNC": "init",
               "MED-FUNC": "med", "SOLO-FUNC": "solo"}
SUM_POS = {"INITIAL": "init", "TERMINAL": "fin", "FINAL": "fin",
           "MEDIAL": "med", "SOLO": "solo"}


def main():
    results = {"spec": "078", "parent_step2": {
        "source": "Spec 076 pilot record (step 2, seed 20261026, B=999)",
        "standing": "INHERITED — not re-run (spec §7.2)",
        "bars": "both passed wide (residual 178 vs null 5th pct 395.0; "
                "solo-only 13 vs null 95th pct 5.0; empirical 0.000 both)"}}
    recs = [json.loads(l) for l in open(INP / "indus_research.jsonl")
            if l.strip()]
    m77 = [r for r in recs if r["source_system"] == "indusscript-m77"]
    anchors = json.load(open(INP / "INDUS_FINAL_ANCHORS.json"))["anchors"]
    strict = {k[1:] for k, v in anchors.items()
              if v.get("validation_status") == "strict_sa_independent"}

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
    step0 = {"records": len(m77), "dropped_000": n000,
             "dropped_star": nstar, "tokens": len(tokens),
             "strict_tokens": strict_tokens,
             "nonempty_sequences": len(nonempty)}
    expected0 = {"records": 2906, "dropped_000": 680, "dropped_star": 452,
                 "tokens": 11507, "strict_tokens": 5883,
                 "nonempty_sequences": 2880}
    # slot totals + finals partition + headline derivation numbers
    rows = {}
    for s in nonempty:
        if len(s) == 1:
            slots = [(s[0], "solo")]
        else:
            slots = [(s[0], "init")] + [(g, "med") for g in s[1:-1]] + \
                    [(s[-1], "fin")]
        for g, slot in slots:
            row = rows.setdefault(g, {"init": 0, "med": 0, "fin": 0,
                                      "solo": 0, "t": 0})
            row[slot] += 1
            row["t"] += 1
    slot_totals = {sl: sum(r[sl] for r in rows.values()) for sl in SLOTS}
    finals = {"strict": 0, "pending": 0, "anchored_other": 0,
              "no_anchor": 0}
    pending = {k[1:] for k, v in anchors.items()
               if v.get("validation_status") ==
               "pending_non_sa_validation"}
    anchored = {k[1:] for k in anchors}
    for g, r in rows.items():
        if r["fin"] == 0:
            continue
        if g in strict:
            finals["strict"] += r["fin"]
        elif g in pending:
            finals["pending"] += r["fin"]
        elif g in anchored:
            finals["anchored_other"] += r["fin"]
        else:
            finals["no_anchor"] += r["fin"]
    step0_extra = {"slot_totals": slot_totals, "finals_partition": finals}
    expected_extra = {
        "slot_totals": {"init": 2655, "med": 5972, "fin": 2655,
                        "solo": 225},
        "finals_partition": {"strict": 1707, "pending": 250,
                             "anchored_other": 520, "no_anchor": 178}}
    results["step0"] = {**step0, **step0_extra,
                        "expected": {**expected0, **expected_extra},
                        "pass": step0 == expected0 and
                        step0_extra == expected_extra}
    if not results["step0"]["pass"]:
        results["verdict"] = "CANNOT BE RUN AS WRITTEN"
        results["step2_standing"] = "VOID — falls with the census (§7.2)"
        (HERE / "pilot-results.json").write_text(
            json.dumps(results, indent=1) + "\n")
        print(json.dumps(results, indent=1))
        return 1
    results["step2_standing"] = "STANDS (inherited, §7.2)"

    total_tokens = step0["tokens"]
    base_rates = {sl: slot_totals[sl] / total_tokens for sl in SLOTS}
    results["base_rates"] = {sl: round(base_rates[sl], 4) for sl in SLOTS}

    # ---- Step 3': checks over the blind coding ----
    coding = json.load(open(CODING))
    by_sign = {e["sign"][1:]: e for e in coding}  # strip leading 'M'
    assert set(by_sign) == strict, "coding population != strict core"

    def check(e, row):
        """Return (failures, checkable_claims, summary_notes)."""
        fails, checkable, sums = [], 0, []
        for c in e["codings"]:
            if c["kind"] == "distributional":
                checkable += 1
                typ = c["type"]
                i, m, f, s = (row["init"], row["med"], row["fin"],
                              row["solo"])
                contradicted = {
                    "ONLY-INIT": m + f + s > 0, "ONLY-FIN": i + m + s > 0,
                    "ONLY-MED": i + f + s > 0, "ONLY-SOLO": row["t"] > s,
                    "NEVER-INIT": i > 0, "NEVER-FIN": f > 0,
                    "NEVER-MED": m > 0, "NEVER-SOLO": s > 0,
                }[typ]
                if contradicted:
                    fails.append({"line": "distributional", "type": typ,
                                  "rule": c["rule"]})
            elif c["kind"] == "functional":
                checkable += 1
                anchor = FUNC_ANCHOR[c["type"]]
                share = row[anchor] / row["t"]
                if share < base_rates[anchor]:
                    fails.append({"line": "functional", "type": c["type"],
                                  "rule": c["rule"],
                                  "anchor_share": round(share, 4),
                                  "base_rate": round(base_rates[anchor], 4)})
            elif c["kind"] == "summary":
                pos = SUM_POS.get(c["type"].upper())
                note = {"named_position": c["type"],
                        "sample_size": c.get("sample_size")}
                if pos and row["t"]:
                    top = max(SLOTS, key=lambda sl: row[sl])
                    note["plurality_here"] = top
                    note["transfers"] = (top == pos)
                sums.append(note)
        return fails, checkable, sums

    lines = {"counted": [], "worked_example": [], "frame_absent": []}
    for g in sorted(strict):
        e = by_sign[g]
        row = rows.get(g, {"init": 0, "med": 0, "fin": 0, "solo": 0,
                            "t": 0})
        if row["t"] == 0:
            line = "frame_absent"
            fails, checkable, sums = [], 0, []
            n_check = sum(1 for c in e["codings"]
                          if c["kind"] in ("distributional", "functional"))
            entry = {"sign": "M" + g, "checkable_claims_coded": n_check,
                     "codings": e["codings"]}
        else:
            line = "worked_example" if g in WORKED else "counted"
            fails, checkable, sums = check(e, row)
            entry = {"sign": "M" + g, "row": row, "failures": fails,
                     "checkable_claims": checkable, "summaries": sums,
                     "codings": e["codings"]}
        lines[line].append(entry)

    counted = lines["counted"]
    dist_fails = [f for e in counted for f in e["failures"]
                  if f["line"] == "distributional"]
    func_fails = [f for e in counted for f in e["failures"]
                  if f["line"] == "functional"]
    signs_with_claims = [e["sign"] for e in counted
                         if e["checkable_claims"] > 0]
    results["step3prime"] = {
        "counted_population": len(counted),
        "worked_example_line": [e["sign"] for e in lines["worked_example"]],
        "frame_absent_line": [e["sign"] for e in lines["frame_absent"]],
        "signs_with_checkable_claims": len(signs_with_claims),
        "checkable_signs": signs_with_claims,
        "distributional_failures": len(dist_fails),
        "functional_failures": len(func_fails),
        "total_failures": len(dist_fails) + len(func_fails),
        "failure_detail": [{"sign": e["sign"], **f} for e in counted
                           for f in e["failures"]],
        "worked_example_detail": lines["worked_example"],
        "frame_absent_detail": lines["frame_absent"],
        "summary_census": {
            "counted_summaries": sum(len(e["summaries"]) for e in counted),
            "transfers": sum(1 for e in counted for s in e["summaries"]
                             if s.get("transfers")),
            "non_transfers": sum(1 for e in counted for s in e["summaries"]
                                 if s.get("transfers") is False)},
        "counted_detail": counted,
    }
    s3 = results["step3prime"]
    administrable = s3["signs_with_checkable_claims"] >= 25
    results["administrability"] = {
        "floor": 25, "observed": s3["signs_with_checkable_claims"],
        "pass": administrable}
    if not administrable:
        results["verdict"] = ("CANNOT BE ADMINISTERED — THE CORE MAKES "
                              "TOO FEW CHECKABLE CLAIMS")
    elif (s3["total_failures"] <= 3 and len(dist_fails) <= 2
          and len(func_fails) <= 2):
        results["verdict"] = ("PILOT PASSES on counts — pattern clause "
                              "adjudicated in the pilot record (§7.4)")
    else:
        results["verdict"] = "BRIDGE DOES NOT HOLD"
    (HERE / "pilot-results.json").write_text(
        json.dumps(results, indent=1) + "\n")
    print(json.dumps({k: results[k] for k in
                      ("step0", "base_rates", "administrability",
                       "verdict")}, indent=1))
    print("counted:", s3["counted_population"],
          "| checkable signs:", s3["signs_with_checkable_claims"],
          "| dist fails:", len(dist_fails),
          "| func fails:", len(func_fails))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
