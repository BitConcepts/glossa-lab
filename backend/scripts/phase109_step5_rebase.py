"""Phase-109 Step 5: headline re-base recomputation + bookkeeping
(spec 007).

Recomputes the programme's headline internal-consistency
quantities FRESH on the post-Step-1–3 anchor set, using the
Phase-108 registered methods (pipelines/provenance_audit.py) and
the Phase-108 strict SA-independent definition (register category
not SA_DERIVED / SA_CONFIRMED_ONLY and sa_in_chain false), and —
in `apply` mode — regenerates the anchors file's summary
bookkeeping from the changed entries (spec 004 WS3 method).

Modes: `decide` (default; writes reports/phase109_rebase.json)
and `apply` (bookkeeping regeneration + change register).

GPU: no compute; gpu_device recorded per H20 (torch guarded).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase109-step5] gpu_device={_GPU}", file=sys.stderr)

from glossa_lab.pipelines import phase109_followthrough as p109  # noqa: E402
from glossa_lab.pipelines import provenance_audit as pa  # noqa: E402

REPO = Path(__file__).parents[2]
OUT = REPO / "reports" / "phase109_rebase.json"


def _quantities(signs: set[str], anchors: dict) -> dict:
    subset = {s: anchors[s] for s in sorted(signs)}
    tokens = pa.load_holdat_tokens()
    return {
        "n_signs": len(signs),
        "coverage": pa.token_coverage(tokens, signs),
        "phonotactics": pa.phonotactic_check(subset),
        "parpola": pa.parpola_agreement(signs, anchors),
        "site_invariance": pa.site_invariance(signs),
    }


def build_rebase() -> tuple[dict, dict, set[str]]:
    anchors_data = p109.load_anchors_file()
    anchors = anchors_data["anchors"]
    records = p109.load_register()
    full_hm = {s for s, e in anchors.items()
               if (e.get("confidence") or "").upper() in ("HIGH", "MEDIUM")}
    strict = p109.strict_sa_independent_hm(anchors, records)
    tier_counts = Counter((e.get("confidence") or "").upper()
                          for e in anchors.values())
    strict_tiers = Counter(anchors[s]["confidence"].upper() for s in strict)
    payload = {
        "phase": 109, "step": 5, "spec": "specs/007-phase109-follow-through",
        "gpu_device": _GPU,
        "date": p109.DATE,
        "basis": "post-Step-1–3 anchors file (this branch)",
        "anchor_counts_by_tier": dict(tier_counts),
        "total_anchors": len(anchors),
        "sets": {
            "full_hm": _quantities(full_hm, anchors),
            "sa_independent_strict": _quantities(strict, anchors),
        },
        "strict_subset_tiers": dict(strict_tiers),
        "parpola_caveat": (
            "Crosswalk-v2.1 comparison quantity (Phase-108 method: "
            "normalised first-segment equality). NOT a like-for-like "
            "replacement for the retired 59% (a Phase-170-era "
            "quantity on a 44-sign set that was 45.5% SA-lineage); "
            "67/184 crosswalk entries are identity-only, so the rate "
            "is partially tautological (Phase-108)."),
        "methods": {
            "coverage": "Holdat CSV token rows; covered iff sign in set",
            "phonotactics": "phase58 analyze_phoneme_inventory",
            "parpola": "crosswalk v2.1 Parpola readings; normalised "
                       "first-segment equality (spec 006)",
            "site_invariance": "phase69 chi2_test + I/M/T counting",
            "strict_definition": "register category not in "
                                 "(SA_DERIVED, SA_CONFIRMED_ONLY) and "
                                 "register sa_in_chain == false, "
                                 "restricted to H+M of the post-change "
                                 "anchors file",
        },
    }
    return payload, anchors_data, full_hm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="decide",
                    choices=("decide", "apply"))
    args = ap.parse_args()
    payload, anchors_data, full_hm = build_rebase()
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    cov = payload["sets"]["full_hm"]["coverage"]["coverage"]
    scov = payload["sets"]["sa_independent_strict"]["coverage"]["coverage"]
    print(f"[phase109-step5] full H+M={len(full_hm)} coverage={cov}; "
          f"strict={payload['sets']['sa_independent_strict']['n_signs']} "
          f"coverage={scov} -> {OUT.name}")
    if args.mode == "apply":
        result = p109.regenerate_bookkeeping(anchors_data, cov)
        anchors_data["_phase109_note"] = (
            f"Phase-109 ({p109.DATE}, spec 007): staging-cohort "
            "re-review (Step 1), SA-lineage provenance flags "
            "(Step 2), M293/M362/M398 re-reviews (Step 3) applied; "
            "summary fields regenerated from the entries; full "
            "change record in reports/phase109_change_register.json.")
        reg = p109.load_change_register()
        p109.append_changes(reg, "step5b", [{
            "sign": "*", "rule": "step5(b)", "action": "bookkeeping",
            "before": {k: v[0] for k, v in result["changed_fields"].items()},
            "after": {k: v[1] for k, v in result["changed_fields"].items()},
            "citations": ["reports/phase109_rebase.json",
                          "spec 004 WS3 method"]}])
        p109.save_change_register(reg)
        p109.write_anchors_file(anchors_data)
        print(f"[phase109-step5] bookkeeping regenerated: "
              f"{result['changed_fields']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
