"""Phase-108 Step 4: circularity + downstream impact map (spec 006).

A MAP, not an edit — nothing mapped here is modified.
  * circular chains: anchor -> SA pin/proposal -> SA agreement cited
    in a later promotion or claim (structural detection + citations)
  * claims map: the 31 extracted claims vs SA-lineage anchors
  * headline numbers: 161 anchors / 90.96% coverage / 59% Parpola —
    source set for each + its SA-lineage share per the register
  * foundation-check map: every SA-citing claim text in
    foundation_check.py with its post-Phase-107 status (STATUS dict
    below, authored with rationale in the Step-4 summary)
Output: reports/phase108_impact_map.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase108-impact] gpu_device={_GPU}", file=sys.stderr)

from glossa_lab.pipelines.provenance_audit import (  # noqa: E402
    CLAIMS_DIR, SIGN_RE, load_anchors, load_holdat_tokens, load_json)

REPO = Path(__file__).parents[2]
REGISTER = REPO / "reports" / "phase108_provenance_register.json"
TRAILS = REPO / "reports" / "phase108_anchor_trails.json"
OUT = REPO / "reports" / "phase108_impact_map.json"
FOUNDATION = REPO / "backend" / "scripts" / "foundation_check.py"

# Post-Phase-107 status per foundation-check SA-citing item, keyed by a
# substring of the claim text. Authored in Step 4; rationale in the
# Step-4 section of reports/phase108_provenance_summary.md.
FOUNDATION_STATUS: dict[str, str] = {}


def circular_chains(records: dict, trails: dict) -> list[dict]:
    chains = []
    for sign, rec in records.items():
        trail = trails.get(sign, {})
        st = trail.get("structured", {})
        pinned52 = "phase52_sa_table" in st
        promoted_sa = rec.get("sa_role") == "promotion"
        origin_sa = rec.get("category") == "SA_DERIVED"
        inj = [m for m in trail.get("artifact_mentions", {})
               .get("upgrade_artifacts", []) if m["kind"] == "injection"]
        if origin_sa:
            chains.append({
                "sign": sign, "type": "sa_origin",
                "detail": "value first proposed by an SA run (register)",
                "citations": rec.get("trail_citations", [])})
        elif promoted_sa and pinned52:
            chains.append({
                "sign": sign, "type": "pin_then_sa_promotion",
                "detail": "sign appears in the Phase-52 SA table and its "
                          "promotion to current confidence cites SA agreement",
                "citations": ["reports/phase52_full_decipherment_table.json"]
                             + rec.get("trail_citations", [])})
        elif promoted_sa and inj:
            chains.append({
                "sign": sign, "type": "injection_then_sa_promotion",
                "detail": "sign entered via an anchor-injection artifact and "
                          "its promotion cites SA agreement",
                "citations": [m["file"] for m in inj]
                             + rec.get("trail_citations", [])})
    return chains


def claims_map(records: dict) -> dict:
    sa_signs = {s for s, r in records.items()
                if r["category"] in ("SA_DERIVED", "SA_CONFIRMED_ONLY")
                or r["sa_in_chain"]}
    per_claim, n_with_sa = [], 0
    for f in sorted(CLAIMS_DIR.glob("*.json")):
        d = load_json(f) or {}
        for c in d.get("claims", []):
            blob = json.dumps(c, ensure_ascii=False)
            signs = sorted(set(SIGN_RE.findall(blob)))
            sa_cited = [s for s in signs if s in sa_signs]
            if sa_cited:
                n_with_sa += 1
            per_claim.append({
                "claim_id": c.get("claim_id"),
                "status": c.get("claim_status"),
                "signs_cited": signs, "sa_lineage_signs": sa_cited,
                "file": f"glossa-indus/claims/extracted_claims/{f.name}"})
    return {"n_claims": len(per_claim), "n_claims_citing_sa_lineage":
            n_with_sa, "claims": per_claim}


def headline_map(records: dict, anchors: dict) -> dict:
    sa_signs = {s for s, r in records.items()
                if r["category"] in ("SA_DERIVED", "SA_CONFIRMED_ONLY")
                or r["sa_in_chain"]}
    tokens = load_holdat_tokens()
    out: dict = {}
    # 59% Parpola: Phase-159 confirmed_signs (44) — exact source set.
    p159 = load_json(REPO / "backend" / "reports"
                     / "phase157_160_reference_mining.json") or {}
    confirmed = (p159.get("results", {}).get("phase_159", {})
                 .get("confirmed_signs", []))
    if confirmed:
        sa44 = [s for s in confirmed if s in sa_signs]
        out["parpola_59pct"] = {
            "source": "backend/reports/phase157_160_reference_mining.json "
                      "(phase_159.confirmed_signs, 44 signs; 44/75 HIGH then)",
            "n_signs": len(confirmed), "n_sa_lineage": len(sa44),
            "sa_lineage_signs": sa44,
            "sa_share": round(len(sa44) / len(confirmed), 4)}
    # 161 anchors / 90.96%: Phase-170-era H+M set. Recoverable only if a
    # Phase-170 artifact enumerates its signs; check the known places.
    cand = None
    for p in (REPO / "outputs" / "phase170_grammar_variance.json",
              REPO / "backend" / "reports" / "phase170_grammar_variance.json",
              REPO / "reports" / "phase170_grammar_variance.json"):
        if p.exists():
            cand = (p, load_json(p))
            break
    if cand:
        p, d = cand
        signs = sorted(set(SIGN_RE.findall(json.dumps(d))))
        hm161 = [s for s in signs if s in anchors
                 and anchors[s]["confidence"] in ("HIGH", "MEDIUM")]
        sa161 = [s for s in hm161 if s in sa_signs]
        covered_sa = sum(1 for t in tokens if t in set(sa161))
        out["anchors_161"] = {
            "source": str(p.relative_to(REPO)),
            "n_signs_mentioned": len(hm161), "n_sa_lineage": len(sa161),
            "sa_lineage_signs": sa161,
            "tokens_attributable_to_sa_lineage": covered_sa,
            "note": "sign set recovered from the Phase-170 artifact's "
                    "mentions; the historical 161-set is not stored as a "
                    "standalone file in-repo"}
    else:
        out["anchors_161"] = {
            "source": None,
            "note": "no Phase-170 artifact enumerating its sign set was "
                    "found in-repo; SA-lineage share of the historical "
                    "161-set cannot be computed without reconstructing "
                    "it, which this audit does not do"}
    return out


def foundation_map() -> list[dict]:
    text = FOUNDATION.read_text(encoding="utf-8")
    hits = []
    pat = re.compile(r"Phase-(52|55|56|57|61|62|63|66|67|70|73|77|93|97|"
                     r"106|107|110|116|122|168|193|207|213|216|229)\b|\bSA\b")
    for i, ln in enumerate(text.splitlines(), 1):
        if pat.search(ln) and ('"' in ln or "'" in ln):
            key = next((k for k in FOUNDATION_STATUS if k in ln), None)
            hits.append({"line": i, "text": ln.strip()[:200],
                         "post107_status": FOUNDATION_STATUS.get(key or "", "TO_ASSESS")})
    return hits


def main() -> int:
    records = json.loads(REGISTER.read_text(encoding="utf-8"))["records"]
    trails = json.loads(TRAILS.read_text(encoding="utf-8"))["trails"]
    anchors = load_anchors()["anchors"]
    out = {"phase": 108, "step": 4, "gpu_device": _GPU,
           "circular_chains": circular_chains(records, trails),
           "claims_map": claims_map(records),
           "headline_map": headline_map(records, anchors),
           "foundation_map": foundation_map()}
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    print(f"chains={len(out['circular_chains'])} "
          f"claims={out['claims_map']['n_claims']} "
          f"({out['claims_map']['n_claims_citing_sa_lineage']} cite SA-lineage) "
          f"foundation_hits={len(out['foundation_map'])}")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
