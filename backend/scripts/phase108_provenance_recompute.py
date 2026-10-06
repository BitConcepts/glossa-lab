"""Phase-108 Step 3: subset recomputation (spec 006).

Recomputes the programme's headline internal-consistency quantities
on the SA-INDEPENDENT subset (from the final provenance register),
with UNTRACEABLE reported both ways as a sensitivity pair:
  (a) Holdat token coverage          (b) Phase-58 phonotactic rate
  (c) Parpola agreement (crosswalk)  (d) Phase-69 site invariance
Output: reports/phase108_subset_recomputation.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase108-recompute] gpu_device={_GPU}", file=sys.stderr)

from glossa_lab.pipelines.provenance_audit import (  # noqa: E402
    load_anchors, load_holdat_tokens, parpola_agreement,
    phonotactic_check, site_invariance, token_coverage)

REPO = Path(__file__).parents[2]
REGISTER = REPO / "reports" / "phase108_provenance_register.json"
OUT = REPO / "reports" / "phase108_subset_recomputation.json"
P159 = REPO / "backend" / "reports" / "phase157_160_reference_mining.json"

HM = ("HIGH", "MEDIUM")


def sets_from_register(records: dict, anchors: dict) -> dict[str, set[str]]:
    hm = {s for s, r in records.items() if r["confidence"] in HM}
    strict = {s for s in hm
              if records[s]["category"] not in ("SA_DERIVED",
                                                "SA_CONFIRMED_ONLY",
                                                "UNTRACEABLE")
              and not records[s]["sa_in_chain"]}
    untr = {s for s in hm if records[s]["category"] == "UNTRACEABLE"}
    return {"full_hm": hm, "sa_independent_strict": strict,
            "sa_independent_incl_untraceable": strict | untr}


def main() -> int:
    anchors = load_anchors()["anchors"]
    records = json.loads(REGISTER.read_text(encoding="utf-8"))["records"]
    sets = sets_from_register(records, anchors)
    tokens = load_holdat_tokens()
    p159_confirmed = set()
    if P159.exists():
        d = json.loads(P159.read_text(encoding="utf-8"))
        p159_confirmed = set(d.get("results", {}).get("phase_159", {})
                             .get("confirmed_signs", []))
    out: dict = {"phase": 108, "step": 3, "gpu_device": _GPU,
                 "methods": {
                     "coverage": "Holdat CSV token rows; covered iff sign in set",
                     "phonotactics": "phase58 analyze_phoneme_inventory "
                                     "(initial-validity of readings; LOW skipped by that code)",
                     "parpola": "crosswalk v2.1 Parpola readings; normalised "
                                "first-segment equality (spec 006)",
                     "parpola_p159_crosscheck": "share of the set's HIGH signs "
                                                "on Phase-159 confirmed_signs (source of README 59%)",
                     "site_invariance": "phase69 chi2_test + I/M/T counting; "
                                        "sites with per-sign total >= 3; <2 sites = insufficient data"},
                 "sets": {}}
    for name, signs in sets.items():
        sub = {s: anchors[s] for s in signs}
        high = {s for s in signs if anchors[s]["confidence"] == "HIGH"}
        entry = {
            "n_signs": len(signs),
            "coverage": token_coverage(tokens, signs),
            "phonotactics": phonotactic_check(sub),
            "parpola": parpola_agreement(signs, anchors),
            "parpola_p159_crosscheck": {
                "n_high": len(high),
                "n_on_p159_list": len(high & p159_confirmed),
                "rate": round(len(high & p159_confirmed) / len(high), 6)
                if high else None},
            "site_invariance": site_invariance(signs),
        }
        out["sets"][name] = entry
        print(f"{name}: n={len(signs)} cov={entry['coverage']['coverage']} "
              f"phono_viol={entry['phonotactics']['n_violations']} "
              f"parpola={entry['parpola']['rate']} "
              f"siteinv={entry['site_invariance']['invariant_rate_of_tested']}")
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
