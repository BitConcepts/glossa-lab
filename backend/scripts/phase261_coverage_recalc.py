"""Phase-261: Token Coverage + Fully Decoded Seals Recalculation

With 413/413 H+M anchors (138 HIGH, 275 MEDIUM, 0 CANDIDATE), recalculate:
1. Token coverage: what % of the 7,002 corpus tokens have H+M readings?
2. Fully decoded seals: how many of the 1,670 seals have ALL signs decoded?
3. Site-stratified coverage: per-site decoded percentages

Output: outputs/phase261_coverage_recalc.json
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase261_coverage_recalc.json"
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_CSV = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "data"))


def norm_icon(s):
    s = s.strip().lower() if s and s != "nan" else ""
    if not s: return "none"
    for kw in ["unicorn","rhinoceros","elephant","buffalo","tiger","zebu","bull","gharial","bison"]:
        if kw in s: return "zebu" if kw in ("bull","buffalo","bison") else kw
    return "other"


def load_holdat():
    seals = []
    with open(HOLDAT_CSV, encoding="utf-8") as fh:
        hdr = fh.readline().strip().split(",")
        ci = {h.strip(): i for i, h in enumerate(hdr)}
        cur_form, cur_signs, cur_site, cur_icon = None, [], "", ""
        for line in fh:
            parts = line.strip().split(",")
            if len(parts) < 2: continue
            form = parts[ci.get("form",0)].strip()
            sign = parts[ci.get("letters",1)].strip()
            site = parts[ci.get("site",2)].strip() if "site" in ci else ""
            icon = parts[ci.get("iconography",3)].strip() if "iconography" in ci and ci.get("iconography",3)<len(parts) else ""
            if form != cur_form:
                if cur_form and cur_signs:
                    seals.append({"form": cur_form, "signs": list(cur_signs), "site": cur_site, "motif": norm_icon(cur_icon)})
                cur_form, cur_signs, cur_site, cur_icon = form, [], site, icon
            cur_signs.append(sign)
        if cur_form and cur_signs:
            seals.append({"form": cur_form, "signs": list(cur_signs), "site": cur_site, "motif": norm_icon(cur_icon)})
    return seals


def main():
    print("=" * 70)
    print("PHASE-261: TOKEN COVERAGE + FULLY DECODED SEALS RECALCULATION")
    print("=" * 70)

    anchors_raw = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_raw.get("anchors", {})
    hm_set = set()
    high_set = set()
    for k, v in anchors.items():
        conf = v.get("confidence", "")
        m77 = k.lstrip("M").lstrip("P")
        if conf in ("HIGH", "MEDIUM"):
            hm_set.add(m77)
            hm_set.add(k)  # Also add with prefix
        if conf == "HIGH":
            high_set.add(m77)
            high_set.add(k)

    by_conf = Counter(v.get("confidence","?") for v in anchors.values())
    print(f"\n  Anchors: H:{by_conf.get('HIGH',0)} M:{by_conf.get('MEDIUM',0)} "
          f"CAND:{by_conf.get('CANDIDATE',0)} Total:{len(anchors)}")

    seals = load_holdat()
    print(f"  Seals: {len(seals)}")

    # ── Token coverage ──────────────────────────────────────────────────────
    total_tokens = 0
    hm_tokens = 0
    high_tokens = 0
    for seal in seals:
        for sign in seal["signs"]:
            total_tokens += 1
            if sign in hm_set:
                hm_tokens += 1
            if sign in high_set:
                high_tokens += 1

    hm_cov = hm_tokens / total_tokens if total_tokens else 0
    high_cov = high_tokens / total_tokens if total_tokens else 0
    print(f"\n  Token coverage (H+M): {hm_tokens}/{total_tokens} = {hm_cov:.1%}")
    print(f"  Token coverage (HIGH only): {high_tokens}/{total_tokens} = {high_cov:.1%}")

    # ── Fully decoded seals ─────────────────────────────────────────────────
    n_fully_hm = 0
    n_fully_high = 0
    n_partial = 0
    n_none = 0
    for seal in seals:
        signs = seal["signs"]
        hm_count = sum(1 for s in signs if s in hm_set)
        high_count = sum(1 for s in signs if s in high_set)
        if hm_count == len(signs):
            n_fully_hm += 1
        elif hm_count > 0:
            n_partial += 1
        else:
            n_none += 1
        if high_count == len(signs):
            n_fully_high += 1

    pct_fully_hm = n_fully_hm / len(seals) if seals else 0
    pct_fully_high = n_fully_high / len(seals) if seals else 0
    print(f"\n  Fully decoded (H+M): {n_fully_hm}/{len(seals)} = {pct_fully_hm:.1%}")
    print(f"  Fully decoded (HIGH only): {n_fully_high}/{len(seals)} = {pct_fully_high:.1%}")
    print(f"  Partially decoded: {n_partial}")
    print(f"  Zero decoded: {n_none}")

    # ── Site-stratified ─────────────────────────────────────────────────────
    sites = {}
    for seal in seals:
        site = seal["site"] or "unknown"
        if site not in sites:
            sites[site] = {"total": 0, "fully_hm": 0, "tokens": 0, "hm_tokens": 0}
        sites[site]["total"] += 1
        signs = seal["signs"]
        sites[site]["tokens"] += len(signs)
        hm_count = sum(1 for s in signs if s in hm_set)
        sites[site]["hm_tokens"] += hm_count
        if hm_count == len(signs):
            sites[site]["fully_hm"] += 1

    print(f"\n  Site-stratified coverage:")
    print(f"  {'Site':<20} {'Seals':>6} {'Decoded':>8} {'Pct':>6} {'TokCov':>7}")
    for site, d in sorted(sites.items(), key=lambda x: -x[1]["total"]):
        pct = d["fully_hm"] / d["total"] if d["total"] else 0
        tcov = d["hm_tokens"] / d["tokens"] if d["tokens"] else 0
        print(f"  {site[:19]:<20} {d['total']:>6} {d['fully_hm']:>8} {pct:>5.0%} {tcov:>6.0%}")

    # ── Save ────────────────────────────────────────────────────────────────
    result = {
        "phase": 261,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_tokens": total_tokens,
        "hm_tokens": hm_tokens,
        "high_tokens": high_tokens,
        "hm_token_coverage": round(hm_cov, 4),
        "high_token_coverage": round(high_cov, 4),
        "total_seals": len(seals),
        "fully_decoded_hm": n_fully_hm,
        "fully_decoded_high": n_fully_high,
        "pct_fully_decoded_hm": round(pct_fully_hm, 4),
        "pct_fully_decoded_high": round(pct_fully_high, 4),
        "partially_decoded": n_partial,
        "zero_decoded": n_none,
        "site_coverage": {s: {**d, "pct_decoded": round(d["fully_hm"]/d["total"],4) if d["total"] else 0,
                               "token_coverage": round(d["hm_tokens"]/d["tokens"],4) if d["tokens"] else 0}
                          for s, d in sites.items()},
    }
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\n  Output: {OUT}")
    print(f"\n{'='*70}")
    print(f"PHASE-261 COMPLETE: Token coverage {hm_cov:.1%} | Seals decoded {pct_fully_hm:.1%}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
