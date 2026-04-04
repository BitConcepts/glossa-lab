"""TMK sign cross-validation against Mahadevan bigram table.

Tests the agglutinative-suffix hypothesis:
  If Indus TMK (Terminal Marker) signs are grammatical suffixes,
  they should appear disproportionately as the SECOND element in bigrams.

Requires:
  reports/mahadevan_bigrams.json  (from: python ocr_mahadevan.py --target tables)
  reports/real_indus_catalog_analysis.json  (already present)

Usage:
  python backend/experiments/tmk_bigram_crossvalidation.py
"""

from __future__ import annotations

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_BIGRAMS_PATH = _REPO_ROOT / "reports" / "mahadevan_bigrams.json"
_CATALOG_PATH = _REPO_ROOT / "reports" / "real_indus_catalog_analysis.json"
_OUTPUT_PATH = _REPO_ROOT / "reports" / "tmk_bigram_crossvalidation.json"


def run() -> dict:
    if not _BIGRAMS_PATH.exists():
        print("[ERROR] Bigram table not found. Run: python ocr_mahadevan.py --target tables")
        return {}

    bigrams: list[dict] = json.loads(_BIGRAMS_PATH.read_text(encoding="utf-8"))
    catalog: dict = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))

    tmk_signs = {s["sign"] for s in catalog.get("tmk_signs", [])}
    all_signs = set()
    sign_as_first: dict[str, int] = {}
    sign_as_second: dict[str, int] = {}
    sign_total_bigram: dict[str, int] = {}

    for b in bigrams:
        a, s, freq = b["sign_a_fuls"], b["sign_b_fuls"], b["freq"]
        all_signs.update([a, s])
        sign_as_first[a] = sign_as_first.get(a, 0) + freq
        sign_as_second[s] = sign_as_second.get(s, 0) + freq
        sign_total_bigram[a] = sign_total_bigram.get(a, 0) + freq
        sign_total_bigram[s] = sign_total_bigram.get(s, 0) + freq

    total_bigram_tokens = sum(b["freq"] for b in bigrams)

    # For each sign: compute second_rate = as_second / (as_first + as_second)
    results = []
    for sign in sorted(all_signs):
        first = sign_as_first.get(sign, 0)
        second = sign_as_second.get(sign, 0)
        total = first + second
        if total == 0:
            continue
        second_rate = second / total
        is_tmk = sign in tmk_signs
        results.append({
            "sign": sign,
            "is_tmk": is_tmk,
            "as_first": first,
            "as_second": second,
            "total_bigram_appearances": total,
            "second_rate": round(second_rate, 4),
        })

    results.sort(key=lambda r: -r["second_rate"])

    # Summary statistics
    tmk_results = [r for r in results if r["is_tmk"]]
    non_tmk_results = [r for r in results if not r["is_tmk"]]

    def avg_second_rate(items: list[dict]) -> float:
        if not items:
            return 0.0
        return sum(r["second_rate"] for r in items) / len(items)

    tmk_avg = avg_second_rate(tmk_results)
    non_tmk_avg = avg_second_rate(non_tmk_results)

    # Top-10 second-position signs: how many are TMK?
    top10 = results[:10]
    top10_tmk = sum(1 for r in top10 if r["is_tmk"])

    summary = {
        "total_bigram_tokens": total_bigram_tokens,
        "total_signs_in_bigrams": len(results),
        "tmk_signs_in_bigrams": len(tmk_results),
        "tmk_avg_second_rate": round(tmk_avg, 4),
        "non_tmk_avg_second_rate": round(non_tmk_avg, 4),
        "tmk_advantage": round(tmk_avg - non_tmk_avg, 4),
        "top10_second_position_signs_that_are_tmk": top10_tmk,
        "interpretation": (
            "SUPPORTS agglutinative-suffix hypothesis: TMK signs prefer second position in bigrams"
            if tmk_avg > non_tmk_avg + 0.05
            else "WEAK or no second-position advantage for TMK signs"
        ),
    }

    output = {
        "summary": summary,
        "top_second_position_signs": results[:30],
        "tmk_sign_profiles": sorted(tmk_results, key=lambda r: -r["second_rate"]),
        "all_signs": results,
    }

    _OUTPUT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print("\n── TMK Bigram Cross-Validation ─────────────────────────────")
    print(f"  Total bigram tokens:       {total_bigram_tokens:,}")
    print(f"  Signs in bigrams:          {len(results)}")
    print(f"  TMK signs in bigrams:      {len(tmk_results)}")
    print(f"  TMK avg second-rate:       {tmk_avg:.4f}")
    print(f"  Non-TMK avg second-rate:   {non_tmk_avg:.4f}")
    print(f"  TMK advantage:             {tmk_avg - non_tmk_avg:+.4f}")
    print(f"  Top-10 second-pos TMK:     {top10_tmk}/10")
    print(f"\n  → {summary['interpretation']}")
    print(f"\n  Saved: {_OUTPUT_PATH}")
    print("────────────────────────────────────────────────────────────\n")

    print("Top 15 signs by second-position rate:")
    print(f"  {'Sign':>6}  {'TMK':>4}  {'As-2nd':>8}  {'As-1st':>8}  {'Rate':>6}")
    for r in results[:15]:
        print(f"  {r['sign']:>6}  {'✓' if r['is_tmk'] else '':>4}  {r['as_second']:>8,}  {r['as_first']:>8,}  {r['second_rate']:>6.3f}")

    return output


if __name__ == "__main__":
    run()
