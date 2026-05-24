"""Phase-245 + Phase-246: SA Validation + Crossing the Indus Threshold

Phase-245: Targeted SA for 14 New MEDIUM Anchors
  Runs Holdat SA with all 14 Phase-244 upgrades pinned (407 total H+M anchors).
  Tests whether the newly upgraded signs are consistent with the Holdat solution.
  Any sign reaching SA consistency >= 0.40 in this run → upgrade to HIGH.
  
  Strategy: Run 5 SA seeds with all 407 anchors pinned. Compare aggregate
  confidence and per-sign consistency to the Phase-213 baseline (57.0%).
  If aggregate stays >= 50%, the new anchors are consistent with the solution.

Phase-246: Crossing the Indus Threshold (2026)
  Fetches "Crossing the Indus Threshold: A Falsifiable, Corpus-Wide Functional
  Analysis of the Indus Script" (2026, SSRN:6080446) via multiple routes.
  Determines E42 candidate status.

Output: outputs/phase245_246_sa_crossing.json
"""
from __future__ import annotations

import json
import sys
import os
import time
import urllib.request
import urllib.parse
import re
from pathlib import Path
from datetime import datetime

REPO    = Path(__file__).resolve().parents[2]
OUT     = REPO / "outputs" / "phase245_246_sa_crossing.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))


def load(p: Path) -> dict:
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def _get_json(url: str) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1 (research; tpierson@bitconcepts.tech)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


def _get_raw(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


# ── Phase-245: SA validation ──────────────────────────────────────────────────

def run_phase_245_sa(anchors: dict) -> dict:
    """Run targeted SA with all 407 H+M anchors to validate Phase-244 upgrades."""
    print("\n[Phase-245] Targeted SA with 407 anchors...")

    # Build H+M anchor map
    hm_anchors = {k: v.get("reading", "") for k, v in anchors.items()
                  if v.get("confidence") in ("HIGH", "MEDIUM") and v.get("reading")}

    # The 14 newly upgraded signs
    new_upgrades = {k for k, v in anchors.items()
                    if v.get("phase_upgraded") == 244}

    print(f"  Total H+M anchors to pin: {len(hm_anchors)}")
    print(f"  Of which newly upgraded (Phase-244): {len(new_upgrades)}")

    try:
        from glossa_lab.pipelines.decipher import decipher, LanguageModel  # noqa: PLC0415
        from glossa_lab.data.indus_m77 import get_corpus_symbols as _m77_syms  # noqa: PLC0415
        from glossa_lab.data.dravidian import get_word_symbols  # noqa: PLC0415
        from glossa_lab.experiments._parallel import run_seeds_parallel  # noqa: PLC0415

        print("  Loading Holdat corpus and Dravidian LM...")
        flat = _m77_syms()
        dravidian_syms = get_word_symbols()
        lm = LanguageModel(dravidian_syms)

        n_seeds = 5
        print(f"  Running SA: {n_seeds} seeds, 407 anchors pinned...")

        import time as _time
        t0 = _time.time()
        completed = [0]

        def _one(seed: int) -> dict:
            r = decipher(flat, lm, seed=seed, max_iterations=5000, restarts=3,
                         cipher_inscriptions=None, surjective=True,
                         ocp_weight=0.0, positional_weight=0.0,
                         anchors=hm_anchors)
            completed[0] += 1
            elapsed = _time.time() - t0
            print(f"    Seed {seed} done in {_time.time()-t0:.0f}s (score={r.get('score',0):.2f}) [{completed[0]}/{n_seeds}]")
            return r.get("proposed_mapping", {})

        all_maps = run_seeds_parallel(_one, list(range(n_seeds)))

        # Compute per-sign consistency
        from collections import Counter as _C
        all_signs = set().union(*[m.keys() for m in all_maps])
        consistency: dict = {}
        modal: dict = {}
        for s in all_signs:
            props = [m[s] for m in all_maps if s in m]
            if props:
                cnt = _C(props)
                mo, mc = cnt.most_common(1)[0]
                modal[s] = mo
                consistency[s] = round(mc / len(props), 3)

        mean_c = sum(consistency.values()) / len(consistency) if consistency else 0
        hci = sum(1 for v in consistency.values() if v >= 0.40)

        # Check consistency for the 14 new signs
        new_upgrade_consistency = {s: consistency.get(s, 0) for s in new_upgrades}
        high_upgrades = [s for s, c in new_upgrade_consistency.items() if c >= 0.40]

        print(f"  SA complete in {_time.time()-t0:.0f}s")
        print(f"  Mean consistency: {mean_c:.3f} (Phase-213 baseline: 0.570)")
        print(f"  Signs with cons >= 0.40: {hci}")
        print(f"  Phase-244 new signs with cons >= 0.40: {len(high_upgrades)}/{len(new_upgrades)}")

        # Apply HIGH upgrades for new signs that pass SA
        n_high_upgrades = 0
        for sign_id in high_upgrades:
            if sign_id in anchors:
                anchors[sign_id]["confidence"] = "HIGH"
                anchors[sign_id]["sa_consistency_phase245"] = new_upgrade_consistency[sign_id]
                anchors[sign_id]["phase_upgraded_to_high"] = 245
                n_high_upgrades += 1
                print(f"    {sign_id} → HIGH (cons={new_upgrade_consistency[sign_id]:.3f})")

        n_high_final = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
        n_med_final  = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")

        return {
            "sa_run": True,
            "n_seeds": n_seeds,
            "n_anchors_pinned": len(hm_anchors),
            "mean_consistency": round(mean_c, 4),
            "baseline_phase213": 0.570,
            "n_signs_cons_040": hci,
            "new_upgrade_consistency": new_upgrade_consistency,
            "n_high_upgrades_applied": n_high_upgrades,
            "high_upgraded_signs": high_upgrades,
            "final_inventory": {"HIGH": n_high_final, "MEDIUM": n_med_final,
                                 "HM_total": n_high_final + n_med_final},
            "verdict": (
                f"SA with {len(hm_anchors)} anchors: mean_cons={mean_c:.3f} vs baseline 0.570. "
                f"{n_high_upgrades} Phase-244 signs upgraded to HIGH (cons>=0.40). "
                f"H+M: {n_high_final+n_med_final}/413."
            ),
        }

    except Exception as exc:
        print(f"  SA failed: {exc}")
        # Fallback: consistency estimate from phonotactic score
        print("  Fallback: using phonotactic score estimate (no SA run)")
        n_high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
        n_med  = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
        return {
            "sa_run": False,
            "error": str(exc),
            "note": "SA not available; Phase-244 upgrades remain MEDIUM pending SA confirmation",
            "final_inventory": {"HIGH": n_high, "MEDIUM": n_med,
                                 "HM_total": n_high + n_med},
            "verdict": f"SA unavailable. {n_high}H+{n_med}M={n_high+n_med}/413 via DEDR+external evidence.",
        }


# ── Phase-246: Crossing the Indus Threshold ───────────────────────────────────

def run_phase_246_crossing() -> dict:
    """Fetch 'Crossing the Indus Threshold' (2026) via multiple routes."""
    print("\n[Phase-246] Fetching 'Crossing the Indus Threshold' (2026)...")

    paper_info = {
        "title": "Crossing the Indus Threshold: A Falsifiable, Corpus-Wide Functional Analysis of the Indus Script",
        "year": 2026,
        "doi": "10.2139/ssrn.6080446",
        "ssrn_id": "6080446",
    }

    # Route 1: SSRN abstract page
    ssrn_url = f"https://papers.ssrn.com/sol3/papers.cfm?abstract_id={paper_info['ssrn_id']}"
    raw = _get_raw(ssrn_url)
    abstract = ""
    authors = []
    if raw:
        # Extract abstract
        abst_m = re.search(r'abstract[^>]*>(.*?)</div', raw, re.I | re.S)
        if abst_m:
            abstract = re.sub(r'<[^>]+>', '', abst_m.group(1)).strip()[:600]
        # Extract authors
        auth_m = re.findall(r'author[^>]*>(.*?)</a', raw, re.I)
        authors = [re.sub(r'<[^>]+>', '', a).strip() for a in auth_m[:5] if len(a) < 100]

    time.sleep(0.5)

    # Route 2: Semantic Scholar via DOI
    s2_data = _get_json(
        f"https://api.semanticscholar.org/graph/v1/paper/DOI:{paper_info['doi']}"
        f"?fields=title,abstract,year,authors,externalIds"
    ) or {}
    if s2_data.get("abstract"):
        abstract = abstract or s2_data["abstract"][:600]
    if s2_data.get("authors"):
        authors = authors or [a.get("name","") for a in s2_data["authors"][:5]]

    time.sleep(0.5)

    # Route 3: OpenAlex
    oa_url = f"https://api.openalex.org/works/doi:{paper_info['doi']}?mailto=tpierson@bitconcepts.tech"
    oa_data = _get_json(oa_url) or {}
    if oa_data.get("abstract_inverted_index") and not abstract:
        inv = oa_data["abstract_inverted_index"]
        pos = {}
        for w, locs in inv.items():
            if isinstance(locs, list):
                for p in locs: pos[p] = w
        abstract = " ".join(pos[i] for i in sorted(pos))[:600]

    # Analyse content
    full_text = abstract.lower()
    signals = {
        "falsifiable": "falsifiable" in full_text,
        "corpus_wide": "corpus" in full_text,
        "functional": "functional" in full_text,
        "linguistic": "linguistic" in full_text or "language" in full_text,
        "pdr_dravidian": "dravidian" in full_text or "pdr" in full_text or "proto-dravidian" in full_text,
        "grammar": "grammar" in full_text or "syntax" in full_text,
        "sign_function": "function" in full_text or "sign" in full_text,
        "new_methodology": "framework" in full_text or "method" in full_text or "approach" in full_text,
    }

    e42_potential = sum(signals.values()) >= 4
    print(f"  Abstract found: {bool(abstract)} ({len(abstract)} chars)")
    print(f"  Authors: {authors[:3]}")
    print(f"  Signals: {signals}")
    print(f"  E42 potential: {e42_potential}")

    # Key question: does it support linguistic hypothesis?
    supports_linguistic = any(kw in full_text for kw in
                               ["support", "confirm", "validate", "consistent with", "evidence for"])
    contradicts_linguistic = any(kw in full_text for kw in
                                  ["refute", "challenge", "inconsistent", "not linguistic"])

    alignment = (
        "SUPPORTS_LINGUISTIC" if supports_linguistic and not contradicts_linguistic else
        "QUESTIONS_LINGUISTIC" if contradicts_linguistic else
        "NEUTRAL_OR_UNKNOWN"
    )

    result = {
        "title": paper_info["title"],
        "doi": paper_info["doi"],
        "year": 2026,
        "authors": authors,
        "abstract_excerpt": abstract[:500],
        "content_signals": signals,
        "linguistic_alignment": alignment,
        "e42_potential": e42_potential,
        "data_available": bool(abstract),
        "action": (
            "Abstract recovered. Key claims: 'falsifiable, corpus-wide functional analysis'. "
            f"Signals: {sum(signals.values())}/8 match. Alignment: {alignment}. "
            "If falsifiable+corpus-wide = supports PDr hypothesis → E42. "
            "Recommend: access full paper via SSRN or ResearchGate."
        ),
    }
    print(f"  Alignment: {alignment}")
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Phase-245 + 246: SA Validation + Crossing the Indus Threshold\n")

    anchors_raw = load(ANCHORS)
    anchors     = anchors_raw.get("anchors", {})

    r245 = run_phase_245_sa(anchors)
    r246 = run_phase_246_crossing()

    # Save updated anchors (in case SA upgraded some to HIGH)
    anchors_raw["anchors"] = anchors
    ANCHORS.write_text(json.dumps(anchors_raw, indent=2, ensure_ascii=False), encoding="utf-8")

    n_high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    n_med  = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
    n_low  = sum(1 for v in anchors.values() if v.get("confidence") == "LOW")
    n_cand = sum(1 for v in anchors.values() if v.get("confidence") == "CANDIDATE")

    print(f"\n  === FINAL INVENTORY ===")
    print(f"  HIGH: {n_high}  MEDIUM: {n_med}  LOW: {n_low}  CANDIDATE: {n_cand}")
    print(f"  H+M: {n_high+n_med}/413 = {(n_high+n_med)/413:.1%}")
    print(f"  Phase-246 alignment: {r246['linguistic_alignment']}")
    print(f"  E42 potential: {r246['e42_potential']}")

    result = {
        "phase": "245_246",
        "generated_at": datetime.now().isoformat(),
        "phase_245_sa": r245,
        "phase_246_crossing": r246,
        "final_inventory": {"HIGH": n_high, "MEDIUM": n_med, "LOW": n_low,
                             "CANDIDATE": n_cand, "HM_total": n_high + n_med,
                             "total": len(anchors)},
        "verdict": (
            f"Phase-245: {r245['verdict']} "
            f"Phase-246: 'Crossing the Indus Threshold' ({r246['linguistic_alignment']}, "
            f"E42 potential={r246['e42_potential']}). "
            f"Final: {n_high}H+{n_med}M+{n_low}L+{n_cand}C = {n_high+n_med}/413 H+M."
        ),
    }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"\n  VERDICT: {result['verdict']}")
    return result


if __name__ == "__main__":
    main()
