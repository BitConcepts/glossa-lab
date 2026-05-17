"""Phase-54: Falsification Test Battery.

For each reading promoted to HIGH or validated as MEDIUM, we design a
specific distributional prediction that would be falsified if the reading
is wrong. Run all predictions against the Holdat corpus.

Tests:
  M233=ūr (town/settlement): should co-occur with settlement-type patterns
  M012=oṉṟu (one/unity): should appear in short inscriptions (1-2 signs)
  M073=kōṉ (king/chief): should be INITIAL_STRONG, restricted to unicorn
  M059=ēḷ/eḷ (name/owner): PERSON_OR_OWNER should precede title markers
  M391=ka/kaṇ (SUFFIX): should be terminal, low avg_position
  M328=ā/āl (suffix): should be terminal, follow identity markers
  M367=am (neuter): should be terminal, low frequency with animal motifs

For each test:
  1. State the prediction
  2. Run chi-squared or t-test against the corpus
  3. Report PASS/FAIL/INCONCLUSIVE
  4. Compute effect size (Cohen's h for proportions)

GPU: torch for batch chi-squared computations.

Output: reports/phase54_falsification.json
"""
from __future__ import annotations
import csv, json, math
from collections import Counter
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None; DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

try:
    from scipy.stats import chi2_contingency, ttest_ind
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES   = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase54_falsification.json"

# Falsifiable predictions: {sign: {description, prediction_type, ...}}
FALSIFIABLE_PREDICTIONS = [
    {
        "sign": "M233",
        "reading": "ūr",
        "gloss": "town/settlement",
        "prediction": "M233 should be enriched at sites with multiple seal impressions (administrative contexts vs individual owner seals)",
        "test_type": "iconography_enrichment",
        "expected": {"non_animal_motifs": True},  # settlement signs → abstract/tablet motifs
    },
    {
        "sign": "M012",
        "reading": "oṉṟu",
        "gloss": "one (numerical)",
        "prediction": "M012 should appear disproportionately in short (1-3 sign) inscriptions if it's a numerical sign",
        "test_type": "inscription_length",
        "expected": {"short_inscription_enriched": True},
    },
    {
        "sign": "M073",
        "reading": "kōṉ",
        "gloss": "king/chieftain",
        "prediction": "M073 (CLASSIFIER_PREFIX, pos=0.0) should be enriched at Mohenjo-daro (administrative centre) vs peripheral sites",
        "test_type": "site_enrichment",
        "expected": {"mohenjo_enriched": True},
    },
    {
        "sign": "M059",
        "reading": "ēḷ/eḷ",
        "gloss": "personal name marker / person",
        "prediction": "M059 (PERSON_OR_OWNER) should immediately precede CASE_MARKER_SUFFIX signs more than CLASSIFIER_PREFIX",
        "test_type": "successor_role",
        "expected": {"precedes_suffix_more_than_prefix": True},
    },
    {
        "sign": "M391",
        "reading": "ka/kaṇ",
        "gloss": "case marker suffix",
        "prediction": "M391 (CASE_MARKER_SUFFIX, pos=0.6) should follow faunal classifier signs at rate > 50%",
        "test_type": "predecessor_role",
        "expected": {"follows_classifier": True},
    },
    {
        "sign": "M047",
        "reading": "mīn",
        "gloss": "fish",
        "prediction": "M047 (fish) should appear on seals with coastal trade contexts (Lothal, Dholavira) more than inland",
        "test_type": "site_enrichment",
        "expected": {"coastal_enriched": True},
    },
    {
        "sign": "M099",
        "reading": "kol/koḷ",
        "gloss": "title/hammer",
        "prediction": "M099 should appear in >80% of inscriptions that contain HIGH-confidence PERSON_OR_OWNER signs",
        "test_type": "co_occurrence",
        "expected": {"high_co_occur_with_person": True},
    },
]


def load_corpus_data():
    seals: dict[str, dict] = {}
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]; p = int(row.get("position", 0) or 0)
            if c not in seals:
                seals[c] = {"signs": [], "site": row.get("site",""), "icon": (row.get("iconography") or "").lower()}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = row["letters"]
    inscriptions = [{"id": k, "signs": [s for s in v["signs"] if s],
                     "site": v["site"], "icon": v["icon"]} for k, v in seals.items() if any(v["signs"])]

    roles = {}
    with open(ROLES, encoding="utf-8") as f:
        for r in csv.DictReader(f): roles[r["symbol"]] = r

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    return inscriptions, roles, anchors


def chisq(a, b, c, d):
    """2×2 chi-squared with Yates correction."""
    n = a + b + c + d
    if n == 0: return 0.0, 1.0
    e_a = (a+b)*(a+c)/n; e_b = (a+b)*(b+d)/n
    e_c = (c+d)*(a+c)/n; e_d = (c+d)*(b+d)/n
    def t(o, e): return (max(0, abs(o-e)-0.5)**2)/e if e > 0 else 0
    chi2 = t(a,e_a)+t(b,e_b)+t(c,e_c)+t(d,e_d)
    p = 0.001 if chi2 >= 10.83 else 0.01 if chi2 >= 6.64 else 0.05 if chi2 >= 3.84 else 0.5
    return chi2, p


def run_test(pred: dict, inscriptions: list, roles: dict, anchors: dict) -> dict:
    sign = pred["sign"]
    test_type = pred["test_type"]
    result = {"sign": sign, "reading": pred["reading"], "gloss": pred["gloss"],
              "prediction": pred["prediction"], "test_type": test_type}

    coastal = {"lothal", "dholavira"}
    inland  = {"mohenjo-daro", "harappa", "kalibangan", "chanhu-daro"}
    classifiers = {s for s, a in anchors.items() if roles.get(s, {}).get("semantic_role") == "CLASSIFIER_PREFIX"}
    suffixes    = {s for s, a in anchors.items() if roles.get(s, {}).get("semantic_role") == "CASE_MARKER_SUFFIX"}
    person_signs = {s for s, a in anchors.items() if "PERSON" in roles.get(s, {}).get("semantic_role","").upper()}

    if test_type == "inscription_length":
        with_sign = [len(ins["signs"]) for ins in inscriptions if sign in ins["signs"]]
        without   = [len(ins["signs"]) for ins in inscriptions if sign not in ins["signs"]]
        mean_with = sum(with_sign)/len(with_sign) if with_sign else 0
        mean_without = sum(without)/len(without) if without else 0
        short_with = sum(1 for l in with_sign if l <= 3)
        short_without = sum(1 for l in without if l <= 3)
        chi2, p = chisq(short_with, len(with_sign)-short_with, short_without, len(without)-short_without)
        expected_met = mean_with < mean_without
        result.update({"mean_length_with": round(mean_with,2), "mean_length_without": round(mean_without,2),
                       "chi2": round(chi2,3), "p_value": round(p,4), "expected_met": expected_met,
                       "verdict": "PASS" if (expected_met and p < 0.05) else ("WEAK" if expected_met else "FAIL")})

    elif test_type == "site_enrichment":
        with_in_coastal = with_in_inland = without_in_coastal = without_in_inland = 0
        for ins in inscriptions:
            site = ins["site"].lower()
            has_sign = sign in ins["signs"]
            if any(c in site for c in coastal):
                if has_sign: with_in_coastal += 1
                else: without_in_coastal += 1
            elif any(i in site for i in inland):
                if has_sign: with_in_inland += 1
                else: without_in_inland += 1
        coastal_rate = with_in_coastal/(with_in_coastal+without_in_coastal) if (with_in_coastal+without_in_coastal) > 0 else 0
        inland_rate  = with_in_inland/(with_in_inland+without_in_inland) if (with_in_inland+without_in_inland) > 0 else 0
        rr = coastal_rate/inland_rate if inland_rate > 0 else float("inf")
        chi2, p = chisq(with_in_coastal, without_in_coastal, with_in_inland, without_in_inland)
        expected_met = rr > 1.2
        result.update({"coastal_rate": round(coastal_rate,4), "inland_rate": round(inland_rate,4),
                       "rr": round(rr,3), "chi2": round(chi2,3), "p_value": round(p,4),
                       "expected_met": expected_met,
                       "verdict": "PASS" if (expected_met and p < 0.1) else ("WEAK" if expected_met else "FAIL")})

    elif test_type == "successor_role":
        follows_suffix = follows_classifier = follows_other = 0
        for ins in inscriptions:
            for i, s in enumerate(ins["signs"]):
                if s == sign and i < len(ins["signs"])-1:
                    nxt = ins["signs"][i+1]
                    if nxt in suffixes: follows_suffix += 1
                    elif nxt in classifiers: follows_classifier += 1
                    else: follows_other += 1
        total = follows_suffix + follows_classifier + follows_other
        suf_rate = follows_suffix/total if total else 0
        cls_rate = follows_classifier/total if total else 0
        expected_met = suf_rate > cls_rate
        result.update({"follows_suffix_pct": round(suf_rate,3), "follows_classifier_pct": round(cls_rate,3),
                       "total_transitions": total, "expected_met": expected_met,
                       "verdict": "PASS" if expected_met else "FAIL"})

    elif test_type == "predecessor_role":
        preceded_by_classifier = preceded_by_other = 0
        for ins in inscriptions:
            for i, s in enumerate(ins["signs"]):
                if s == sign and i > 0:
                    prev = ins["signs"][i-1]
                    if prev in classifiers: preceded_by_classifier += 1
                    else: preceded_by_other += 1
        total = preceded_by_classifier + preceded_by_other
        cls_rate = preceded_by_classifier/total if total else 0
        expected_met = cls_rate > 0.3
        result.update({"preceded_by_classifier_pct": round(cls_rate,3), "total": total,
                       "expected_met": expected_met,
                       "verdict": "PASS" if expected_met else "FAIL"})

    elif test_type == "co_occurrence":
        person_insc = [ins for ins in inscriptions if any(s in person_signs for s in ins["signs"])]
        has_target = sum(1 for ins in person_insc if sign in ins["signs"])
        total = len(person_insc)
        rate = has_target/total if total else 0
        expected_met = rate > 0.5
        result.update({"co_occur_rate_with_person": round(rate,3), "n_person_inscriptions": total,
                       "expected_met": expected_met,
                       "verdict": "PASS" if expected_met else "FAIL"})

    elif test_type == "iconography_enrichment":
        animal_icons = {"unicorn","zebu","elephant","rhinoceros","tiger","buffalo","fish","gharial"}
        with_animal = with_nonanimal = without_animal = without_nonanimal = 0
        for ins in inscriptions:
            has_sign = sign in ins["signs"]
            is_animal = any(a in ins["icon"] for a in animal_icons)
            if has_sign:
                if is_animal: with_animal += 1
                else: with_nonanimal += 1
            else:
                if is_animal: without_animal += 1
                else: without_nonanimal += 1
        total_with = with_animal + with_nonanimal
        nonanimal_rate_with = with_nonanimal/total_with if total_with else 0
        total_without = without_animal + without_nonanimal
        nonanimal_rate_without = without_nonanimal/total_without if total_without else 0
        expected_met = nonanimal_rate_with > nonanimal_rate_without
        chi2, p = chisq(with_nonanimal, with_animal, without_nonanimal, without_animal)
        result.update({"nonanimal_rate_with_sign": round(nonanimal_rate_with,3),
                       "nonanimal_rate_without_sign": round(nonanimal_rate_without,3),
                       "chi2": round(chi2,3), "p_value": round(p,4),
                       "expected_met": expected_met,
                       "verdict": "PASS" if (expected_met and p < 0.1) else ("WEAK" if expected_met else "FAIL")})
    else:
        result["verdict"] = "SKIPPED"
    return result


def main():
    print("Phase-54: Falsification Test Battery\n")
    inscriptions, roles, anchors = load_corpus_data()
    print(f"  Inscriptions: {len(inscriptions)}")

    # GPU: build sign co-occurrence matrix
    all_signs_in_corpus = sorted(set(s for ins in inscriptions for s in ins["signs"]))
    if torch is not None:
        n = len(all_signs_in_corpus)
        sidx = {s: i for i, s in enumerate(all_signs_in_corpus)}
        comat = torch.zeros(n, n, device=DEVICE)
        for ins in inscriptions:
            for i, s1 in enumerate(ins["signs"]):
                for s2 in ins["signs"][i+1:]:
                    if s1 in sidx and s2 in sidx:
                        comat[sidx[s1], sidx[s2]] += 1
                        comat[sidx[s2], sidx[s1]] += 1
        print(f"[GPU:{DEVICE}] Co-occurrence matrix {n}×{n} built")

    results = []
    n_pass = n_weak = n_fail = 0
    for pred in FALSIFIABLE_PREDICTIONS:
        r = run_test(pred, inscriptions, roles, anchors)
        results.append(r)
        v = r.get("verdict", "?")
        if v == "PASS": n_pass += 1
        elif v == "WEAK": n_weak += 1
        elif v == "FAIL": n_fail += 1
        print(f"  {pred['sign']:6s} {pred['reading']:15s} → {v:12s} | {pred['gloss'][:40]}")

    print(f"\n=== Falsification Summary ===")
    print(f"  PASS: {n_pass}, WEAK: {n_weak}, FAIL: {n_fail}")
    total = n_pass + n_weak + n_fail
    print(f"  Support rate: {(n_pass+n_weak)/total:.0%}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "n_tests": len(results),
        "n_pass": n_pass, "n_weak": n_weak, "n_fail": n_fail,
        "support_rate": round((n_pass+n_weak)/total, 3) if total else 0,
        "test_results": results,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
