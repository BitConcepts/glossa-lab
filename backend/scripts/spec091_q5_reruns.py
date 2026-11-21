"""Spec 091 Q5 item 3 — dependency-aware reruns (Round 2, 2026-11-21).

Venue: tower-compute only. Inputs: in-repo records only (the raw Holdat
CSV is gitignored and NOT held in this clone; where a from-raw recount
binds, the rerun records that fact instead of substituting silently).

Every section prints a PAYLOAD VERDICT line with its own outcome.
Exit code: 0 if every executable check ran; 3 if any executable check
failed to run. Non-executable-as-specified items are recorded, not
counted as failures of execution.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
from glossa_lab.site_stats_v2 import chi_square_independence

REC = ROOT / "specs/091-anchor-comparison-integrity/records"
out = {"venue": "tower-compute", "workstream": "Q5 item 3 dependency-aware reruns",
       "raw_holdat_csv_held_in_clone": (ROOT / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv").exists(),
       "sections": {}}
failures = []

def load(p):
    return json.loads(Path(p).read_text("utf-8"))

# ---------------- Tranche 1: M342, M176 (T303 site-statistics arm) ----
t303 = load(REC / "t303-reclassification-acts.json")
filed = {"M342": dict(n=584, term=70, chi2=25.246836667200593, df=16, p=0.06559048567133662),
         "M176": dict(n=356, term=68, chi2=22.858877313772798, df=14, p=0.0626051531789166)}
t1 = {}
for act in t303["acts"]:
    s = act["sign"]
    if s not in filed:
        continue
    tab = act["basis"]["table"]
    rows = tab["rows"]
    allc = tab["all_site_counts"]
    total_all = sum(sum(v) for v in allc.values())
    term_all = sum(v[2] for v in allc.values())
    chk = chi_square_independence([list(r) for r in rows]).to_dict()
    f = filed[s]
    repro = (total_all == f["n"] and term_all == f["term"]
             and abs(chk["statistic"] - f["chi2"]) < 1e-6
             and chk["df"] == f["df"] and abs(chk["p_value"] - f["p"]) < 1e-6)
    t1[s] = {"corpus_n_from_filed_all_site_counts": total_all,
             "table_grand_total": sum(sum(r) for r in rows),
             "terminal_count": term_all,
             "terminal_rate": term_all / total_all,
             "filed_terminal_rate": f["term"] / f["n"],
             "recomputed_chi2": chk["statistic"], "filed_chi2": f["chi2"],
             "recomputed_df": chk["df"], "filed_df": f["df"],
             "recomputed_p": chk["p_value"], "filed_p": f["p"],
             "checker_status": chk["status"],
             "filed_corrected_result_reproduces": repro}
    print(f"PAYLOAD VERDICT T1 {s}: exit=0 chi2={chk['statistic']:.4f} df={chk['df']} "
          f"p={chk['p_value']:.4f} n={total_all} terminal={term_all} "
          f"rate={term_all/total_all:.4f} reproduces={repro}")
    if not repro:
        failures.append(f"T1 {s} did not reproduce")
out["sections"]["tranche1"] = t1

# ---------------- Tranche 2: raw-count verification -------------------
p142 = load(ROOT / "backend/reports/phase142_collocate_network.json")
entries = {}
def walk(o):
    if isinstance(o, dict):
        if "sign" in o and "freq" in o and "top_right_neighbors" in o:
            entries[o["sign"]] = o
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(p142)

def right_count(sign, nbr):
    e = entries.get(sign)
    if not e:
        return None
    for n in e.get("top_right_neighbors", []):
        if n.get("sign") == nbr:
            return n.get("count")
    return 0

t2 = {}
colloc = {"M005": ("M342", 4), "M030": ("M342", 4), "M037": ("M267", 4)}
for sign, (nbr, filed_n) in colloc.items():
    got = right_count(sign, nbr)
    t2[sign] = {"filed_collocation": f"{sign}-{nbr} n={filed_n}",
                "phase142_right_neighbor_count": got,
                "raw_count_verified": got == filed_n,
                "anchor_deleted": nbr,
                "anchor_class": "U" if nbr == "M342" else "I"}
    print(f"PAYLOAD VERDICT T2 {sign}: exit=0 filed_n={filed_n} phase142_n={got} verified={got == filed_n}")
    if got != filed_n:
        failures.append(f"T2 {sign} collocation mismatch")

# M068 / M075: filed n=4 each; phase142 holds no initial-entry for them.
for sign, nbr in [("M068", "M342"), ("M075", "M267")]:
    t2[sign] = {"filed_collocation": f"{sign}-{nbr} n=4",
                "phase142_right_neighbor_count": right_count(sign, nbr),
                "raw_count_verified": None,
                "note": "no phase142 initial-sign entry for this sign; count stands on the anchor record only, not independently verified from a second in-repo corpus record",
                "anchor_deleted": nbr, "anchor_class": "U" if nbr == "M342" else "I"}
    print(f"PAYLOAD VERDICT T2 {sign}: exit=0 filed_n=4 phase142=absent verified=None (single-source)")

# M089: filed upgrade counts are internally duplicated/inconsistent.
anchors = load(ROOT / "backend/reports/INDUS_FINAL_ANCHORS.json")["anchors"]
b89 = anchors["M089"]["basis"]
t2["M089"] = {"filed_basis_excerpt": b89[:400],
              "note": "upgrade text lists M342 collocations twice with different counts (n=15 and n=13) and M176 twice (n=6 and n=12); the raw counts are not stated consistently on file, and all three invoked anchors are deleted in any case (M342 U, M176 U, M267 I)",
              "t302_battery_v2": "positional pass + bigram pass (neighbour_match=4/5=80.0%), dedr not_run; structural only"}
print("PAYLOAD VERDICT T2 M089: exit=0 filed upgrade counts internally inconsistent (duplicated, differing); anchors deleted regardless")

# M347: raw contexts from the anchor record basis.
import csv, io
rows = list(csv.DictReader(io.StringIO((ROOT / "research/indus/anchor_table.csv").read_text("utf-8"))))
by = {r["Sign"]: r for r in rows}
t2["M347"] = {"filed_basis": by["M347"]["Basis"],
              "raw_context_patterns_on_file": ["M342-[M347]-M293", "M028-[M347]-M367", "M211-[M347]-M099"],
              "n_contexts_filed": 7,
              "note": "7 contexts claimed, 3 distinct patterns exemplified on file; every interpreted neighbour is U (M342, M328-in-pattern-family, M367) or I (M099) except context signs M293/M028/M211, which are outside the 94 and carry no standing here"}
print("PAYLOAD VERDICT T2 M347: exit=0 n_contexts=7 patterns_on_file=3 slot interpretation removed")

# M375 / M398: phase103 raw pattern counts.
p103 = load(ROOT / "outputs/phase103_name_lexicon.json")
for sign in ("M375", "M398"):
    cand = [c for c in p103["name_candidates"] if c["sign"] == sign][0]
    t2[sign] = {"corpus_freq": cand["corpus_freq"], "name_slot_count": cand["name_slot_count"],
                "ay_an_pattern_count": cand["ay_an_pattern_count"],
                "genitive_pattern_count": cand["genitive_pattern_count"],
                "sample_patterns_raw": cand["sample_patterns"]}
    print(f"PAYLOAD VERDICT T2 {sign}: exit=0 freq={cand['corpus_freq']} ay_an={cand['ay_an_pattern_count']} genitive={cand['genitive_pattern_count']}")

# M267: arithmetic + slot-independence determination.
p74 = load(ROOT / "outputs/phase74_m267_grammar_test.json")
obs, null_mean, z = p74["observed_agent_m267_title"], p74["null_mean"], p74["z_score"]
t2["M267"] = {"observed": obs, "null_mean": null_mean, "enrichment_recomputed": obs / null_mean,
              "filed_enrichment": 4.3, "z_filed": z, "p_filed": p74["p_value"],
              "implied_null_sd_from_filed_z": (obs - null_mean) / z,
              "poisson_null_z_crosscheck": (obs - null_mean) / (null_mean ** 0.5),
              "pattern_counts": p74["pattern_counts"],
              "agent_markers": p74["agent_markers_used"], "title_markers": p74["title_markers_used"],
              "rerun_as_specified": "NOT EXECUTABLE AS SPECIFIED",
              "reason": "AGENT markers include M176 (U) and M328 (U); TITLE markers include M099 (I) and M073 (I); the slot labels are assigned from the same candidate reading/grammar system the test is meant to support, so no slot labelling independent of that system exists on file, and no selection correction over the candidate search is stated on file"}
print(f"PAYLOAD VERDICT T2 M267: exit=0 enrichment={obs/null_mean:.4f} (filed 4.3x) z_filed={z} rerun_as_specified=NOT_EXECUTABLE")

# M374: no numeric claim; record only.
t2["M374"] = {"filed_basis_excerpt": by["M374"]["Basis"][:400],
              "interpreted_context_removed": ["M328=man (U)", "M073=king (I)"]}
print("PAYLOAD VERDICT T2 M374: exit=0 no numeric claim on file; interpreted context removed")
out["sections"]["tranche2"] = t2

# ---------------- Tranche 3: M063 motif claim ------------------------
b63 = anchors["M063"]["basis"]
t302 = load(REC / "t302-reclassification-acts.json")
m063_tests = [a["basis"]["tests"] for a in t302["acts"] if a["sign"] == "M063"][0]
out["sections"]["tranche3"] = {"M063": {
    "filed_corrected": "lift 4.35; 3 of 18 gharial seals carry the sign; also 4 unicorn, 3 zebu bull seals (anchor fact-check correction 2026-05-11)",
    "gharial_carriage_rate": 3 / 18,
    "original_threshold": 5.0,
    "filed_lift_below_threshold": 4.35 < 5.0,
    "full_2x2_reconstructible_from_repo_records": False,
    "reason_not_fully_reconstructible": "the filed records state the gharial cell (3/18) and the lift (4.35) but do not jointly file the sign's total seal count and the deduplicated seal population the lift denominator uses; the raw Holdat CSV is gitignored and not held in this clone, so the missing cells cannot be recounted from held data",
    "t302_battery_v2_tests": m063_tests,
    "motif_claim_rerun_by_battery_v2": False,
    "verdict_on_claim_as_specified": "FAILS on the filed corrected figures: lift 4.35 < 5.0 threshold; exclusivity also fails on file (sign present on unicorn and zebu seals)"}}
print("PAYLOAD VERDICT T3 M063: exit=0 gharial=3/18 rate=0.1667 filed_lift=4.35 threshold=5.0 claim_fails_on_filed_figures=True full_2x2_reconstructible=False")

out["failures"] = failures
dest = REC / "q5-reruns-2026-11-21.json"
dest.write_text(json.dumps(out, indent=1) + "\n", "utf-8")
print(f"WROTE {dest}")
print("OVERALL PAYLOAD VERDICT:", "FAIL" if failures else "PASS (all executable checks ran)")
sys.exit(3 if failures else 0)
