"""Phase-108 Step 2: provenance classification (spec 006).

Pass 1 (default): programmatic classification under the pre-registered
rules -> reports/phase108_provenance_register_draft.json (explicit
decisions + needs_review queue with full trails for hand-review).

Finalize (--finalize): merges reports/phase108_review_decisions.json
(hand-review decisions authored after reading the trails) into the
final register -> reports/phase108_provenance_register.json +
reports/phase108_provenance_summary.md with the registered headline
counts (per category, by tier, three-way SA-independent number).
"""
from __future__ import annotations

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

from glossa_lab.pipelines.provenance_audit import (  # noqa: E402
    CATEGORIES, classify_pass1)

REPO = Path(__file__).parents[2]
TRAILS = REPO / "reports" / "phase108_anchor_trails.json"
DRAFT = REPO / "reports" / "phase108_provenance_register_draft.json"
DECISIONS = REPO / "reports" / "phase108_review_decisions.json"
REGISTER = REPO / "reports" / "phase108_provenance_register.json"
SUMMARY = REPO / "reports" / "phase108_provenance_summary.md"


def pass1() -> int:
    trails = json.loads(TRAILS.read_text(encoding="utf-8"))["trails"]
    records, queue = {}, []
    for sign, trail in trails.items():
        r = classify_pass1(trail)
        rec = {"sign": sign, "reading": trail["reading"],
               "confidence": trail["confidence"], "pass1": r}
        records[sign] = rec
        if r["decision"] == "needs_review":
            queue.append(sign)
    payload = {"phase": 108, "step": 2, "pass": 1, "gpu_device": _GPU,
               "n_anchors": len(records),
               "n_explicit": len(records) - len(queue),
               "n_needs_review": len(queue), "needs_review": queue,
               "records": records}
    DRAFT.write_text(json.dumps(payload, indent=1, ensure_ascii=False),
                     encoding="utf-8")
    print(f"pass1: {payload['n_explicit']} explicit, {len(queue)} needs review")
    return 0


def headline_counts(records: dict) -> dict:
    by_cat = Counter(r["category"] for r in records.values())
    by_tier: dict[str, Counter] = {}
    for r in records.values():
        by_tier.setdefault(r["confidence"], Counter())[r["category"]] += 1
    strict = sum(1 for r in records.values()
                 if r["category"] not in ("SA_DERIVED", "SA_CONFIRMED_ONLY",
                                          "UNTRACEABLE")
                 and not r["sa_in_chain"])
    untraceable = by_cat.get("UNTRACEABLE", 0)
    total = len(records)
    sa_dep = sum(1 for r in records.values()
                 if r["category"] in ("SA_DERIVED", "SA_CONFIRMED_ONLY")
                 or r["sa_in_chain"])
    return {
        "total": total,
        "by_category": {c: by_cat.get(c, 0) for c in CATEGORIES},
        "by_tier": {t: dict(c) for t, c in sorted(by_tier.items())},
        "sa_dependent_total": sa_dep,
        "sa_independent_strict": {"n": strict, "of": total,
                                  "rate": round(strict / total, 4)},
        "sa_independent_incl_untraceable": {
            "n": strict + untraceable, "of": total,
            "rate": round((strict + untraceable) / total, 4)},
        "sa_independent_excl_untraceable": {
            "n": strict, "of": total - untraceable,
            "rate": round(strict / (total - untraceable), 4)
            if total > untraceable else None},
    }


def finalize() -> int:
    trails = json.loads(TRAILS.read_text(encoding="utf-8"))["trails"]
    draft = json.loads(DRAFT.read_text(encoding="utf-8"))["records"]
    decisions = {}
    if DECISIONS.exists():
        decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]
    records, edge_cases = {}, []
    for sign, rec in draft.items():
        p1 = rec["pass1"]
        trail = trails[sign]
        d = decisions.get(sign)
        if d is not None:
            # Hand-review decisions override pass 1 for ANY record —
            # including pass-1 "explicit" ones (the Step-2 spot audit
            # found a systematic pass-1 error: the research-loop
            # staging cohort was classified DEDR-explicit off the
            # `dedr_support` gloss text; see register edge cases).
            records[sign] = {
                "sign": sign, "reading": rec["reading"],
                "confidence": rec["confidence"],
                "category": d["category"],
                "components": d.get("components", p1["components"]),
                "sa_in_chain": bool(d.get("sa_in_chain", False)),
                "sa_role": d.get("sa_role", "none"),
                "first_proposal": d.get("first_proposal"),
                "decision_source": "hand_review",
                "reasons": [d.get("rationale", "")],
                "trail_citations": _citations(trail)}
            if d.get("edge_case"):
                edge_cases.append({"sign": sign, "issue": d["edge_case"]})
            continue
        if p1["decision"] == "explicit":
            cat = p1["category"]
            # Presence in the Phase-52 SA table (role "phase52_table")
            # records that SA *measured* the sign; it is not SA
            # evidence in the anchor's chain and does not set
            # sa_in_chain. Only an SA-origin category does.
            final = {"sign": sign, "reading": rec["reading"],
                     "confidence": rec["confidence"], "category": cat,
                     "components": p1["components"],
                     "sa_in_chain": any(
                         c["type"] == "SA" and c.get("role") != "phase52_table"
                         for c in p1["components"]),
                     "sa_role": "none",
                     "first_proposal": None,
                     "decision_source": "pass1",
                     "reasons": p1["reasons"],
                     "trail_citations": _citations(trail)}
            if cat == "SA_DERIVED":
                final["sa_role"] = "origin"
                final["sa_in_chain"] = True
            records[sign] = final
        else:
            edge_cases.append({"sign": sign,
                               "issue": "needs_review without decision"})
            records[sign] = {
                "sign": sign, "reading": rec["reading"],
                "confidence": rec["confidence"],
                "category": "UNTRACEABLE", "components": p1["components"],
                "sa_in_chain": False, "sa_role": "none",
                "first_proposal": None, "decision_source": "default_untraceable",
                "reasons": ["no hand-review decision recorded; "
                            "pre-registered default is UNTRACEABLE"],
                "trail_citations": _citations(trail)}
    counts = headline_counts(records)
    payload = {"phase": 108, "step": 2, "gpu_device": _GPU,
               "taxonomy": "specs/006-anchor-provenance-audit/spec.md",
               "headline_counts": counts, "edge_cases": edge_cases,
               "records": records}
    REGISTER.write_text(json.dumps(payload, indent=1, ensure_ascii=False),
                        encoding="utf-8")
    SUMMARY.write_text(_summary_md(counts, edge_cases, records),
                       encoding="utf-8")
    print(f"final register: {counts['by_category']}")
    print(f"strict SA-independent: {counts['sa_independent_strict']}")
    return 0


def _citations(trail: dict) -> list[str]:
    cites = []
    for k, v in trail["structured"].items():
        if isinstance(v, dict) and v.get("citation"):
            cites.append(v["citation"])
    for m in trail["ledger_mentions"][:4]:
        cites.append(f"{m['source']}:{m['line']} ({m['header'][:60]})")
    return cites


def _summary_md(counts: dict, edge_cases: list, records: dict) -> str:
    lines = ["# Phase-108 Anchor Provenance Audit — Summary",
             "",
             "Spec: `specs/006-anchor-provenance-audit/` · Register: "
             "`reports/phase108_provenance_register.json` · Trails: "
             "`reports/phase108_anchor_trails.json`",
             "",
             "## Headline counts",
             "",
             f"Total anchors audited: **{counts['total']}**",
             "",
             "| Category | n |", "|---|---|"]
    for c in CATEGORIES:
        lines.append(f"| {c} | {counts['by_category'][c]} |")
    lines += ["", f"SA-dependent (SA_DERIVED + SA_CONFIRMED_ONLY + any "
              f"SA in chain): **{counts['sa_dependent_total']}**", "",
              "SA-independent, three ways (pre-registered):",
              f"- strict: **{counts['sa_independent_strict']['n']}** / "
              f"{counts['sa_independent_strict']['of']} "
              f"({counts['sa_independent_strict']['rate']:.1%})",
              f"- incl. untraceable as independent: "
              f"**{counts['sa_independent_incl_untraceable']['n']}** / "
              f"{counts['sa_independent_incl_untraceable']['of']} "
              f"({counts['sa_independent_incl_untraceable']['rate']:.1%})",
              f"- excl. untraceable from denominator: "
              f"**{counts['sa_independent_excl_untraceable']['n']}** / "
              f"{counts['sa_independent_excl_untraceable']['of']} "
              f"({counts['sa_independent_excl_untraceable']['rate']:.1%})",
              "", "## By confidence tier", ""]
    for tier, cats in counts["by_tier"].items():
        lines.append(f"- {tier}: " + ", ".join(f"{k}={v}" for k, v in
                                               sorted(cats.items())))
    staging = [s for s, r in records.items()
               if "staging archive" in str(r.get("first_proposal") or "")]
    gate_lb = [s for s, r in records.items()
               if r["category"] == "SA_CONFIRMED_ONLY"]
    lines += ["", "## Cohort notes (Step-2 hand review)", "",
              f"- Research-loop staging cohort: **{len(staging)}** anchors "
              "carry GRAMMAR because their current readings were proposed "
              "by the automated research loop's fixed heuristic tables "
              "(June 2026) and promoted via /staging/verify-sa, which "
              "performs no SA validation. These are inside the strict "
              "SA-independent count by the pre-registered rules (no SA "
              "evidence in their chains) but are the weakest-evidence "
              "cohort in the set; see the register rationales.",
              f"- SA_CONFIRMED_ONLY total: **{len(gate_lb)}** (Phase-116/216 "
              "recalibration-gate SA_ONLY paths, Phase-293 cross-corpus "
              "promotions where 'SA confirmation pending' was the only "
              "missing piece, and M293).",
              "- Pass 1 misclassified the staging cohort as DEDR-explicit; "
              "the Step-2 spot audit (12 sampled) caught it and all 116 "
              "were re-decided by hand. Pass-1 explicit labels are not "
              "used anywhere without the spot-audit caveat.",
              ""]
    lines += ["## Edge cases", ""]
    if edge_cases:
        for e in edge_cases:
            lines.append(f"- {e['sign']}: {e['issue']}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(finalize() if "--finalize" in sys.argv else pass1())
