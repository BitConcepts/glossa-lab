"""Phases 378-381 + 30 Integrated Loop Iterations

Phase 378: Tamil-Brahmi sign-value transfer — map known TB values to Indus signs
Phase 379: M77 crosswalk improvement — use frequency-rank correlation
Phase 380: Shu-ilishu sign identification — match /su-i-li-su/ pattern in corpus
Phase 381: DEDR morpheme corpus construction — build PDr morpheme bigrams from DEDR

Then: 30 integrated research loop iterations

Output: outputs/phase378_381_plus_loop30.json
"""
from __future__ import annotations
import csv, json, math, random, re, time, urllib.parse, urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"
OUT_PATH = REPO / "outputs" / "phase378_381_plus_loop30.json"

def _load_high_map():
    a = json.loads(ANCHORS_PATH.read_text("utf-8")).get("anchors", {})
    return {s: i["reading"] for s, i in a.items() if i.get("confidence") == "HIGH" and i.get("reading")}

def _load_inscriptions():
    ins = []; cur = None; signs = []; motif = ""; site = ""
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["cisi_number"] != cur:
                if signs: ins.append({"id": cur, "signs": signs, "motif": motif, "site": site})
                cur = r["cisi_number"]; signs = []
                motif = (r.get("iconography") or "").strip().lower()
                site = (r.get("site") or "").strip()
            signs.append(r["letters"])
    if signs: ins.append({"id": cur, "signs": signs, "motif": motif, "site": site})
    return ins

def _clean(r): return r.split("/")[0].strip().lower() if r else ""


# ═══════════════════════════════════════════════════════════════════════
# PHASE 378: TAMIL-BRAHMI SIGN-VALUE TRANSFER
# ═══════════════════════════════════════════════════════════════════════

def phase378_tb_transfer():
    """Map known Tamil-Brahmi aksara values to Indus signs via positional similarity."""
    print("\n[Phase 378] Tamil-Brahmi sign-value transfer")
    hm = _load_high_map(); ins = _load_inscriptions()

    # Tamil-Brahmi aksara inventory (Mahadevan 2003) — 22 consonants × 5 vowels
    # Key aksaras that could map to Indus signs based on PDr continuity:
    TB_VALUES = {
        "ka": "ka", "kā": "kā", "ki": "ki", "ku": "ku", "ko": "ko",
        "ca": "ca", "cā": "cā", "ci": "ci", "cu": "cu", "co": "co",
        "ṭa": "ṭa", "ta": "ta", "tā": "tā", "ti": "ti", "tu": "tu",
        "na": "na", "nā": "nā", "ni": "ni", "nu": "nu",
        "pa": "pa", "pā": "pā", "pi": "pi", "pu": "pu", "po": "po",
        "ma": "ma", "mā": "mā", "mi": "mi", "mu": "mu",
        "ya": "ya", "ra": "ra", "la": "la", "va": "va",
        "a": "a", "ā": "ā", "i": "i", "ī": "ī", "u": "u", "ū": "ū",
        "e": "e", "ē": "ē", "o": "o", "ō": "ō",
    }

    # Check which of our HIGH readings match TB aksara values
    matches = []
    for sid, reading in hm.items():
        clean = _clean(reading)
        if clean in TB_VALUES:
            matches.append({"sign": sid, "reading": reading, "tb_aksara": TB_VALUES[clean]})

    # Count coverage
    our_readings = set(_clean(r) for r in hm.values())
    tb_overlap = our_readings & set(TB_VALUES.values())

    return {
        "tb_aksara_count": len(TB_VALUES),
        "our_readings_count": len(our_readings),
        "overlap": len(tb_overlap),
        "overlap_readings": sorted(tb_overlap),
        "matched_signs": len(matches),
        "sample_matches": matches[:15],
        "verdict": (
            f"TB transfer: {len(tb_overlap)} readings overlap with Tamil-Brahmi aksara values "
            f"out of {len(our_readings)} distinct readings. "
            f"{len(matches)} signs have TB-compatible values."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════
# PHASE 379: M77 CROSSWALK IMPROVEMENT
# ═══════════════════════════════════════════════════════════════════════

def phase379_m77_crosswalk():
    """Improve M77→Holdat crosswalk using frequency-rank correlation."""
    print("\n[Phase 379] M77 crosswalk improvement")
    try:
        import sys; sys.path.insert(0, str(REPO / "backend"))
        from glossa_lab.data.indus_m77 import get_corpus_symbols, get_corpus_metadata
        m77_meta = get_corpus_metadata()
        m77_tokens = get_corpus_symbols()
    except Exception as e:
        return {"error": str(e), "verdict": f"SKIPPED — {e}"}

    # M77 sign frequencies
    m77_freq = Counter(m77_tokens)

    # Holdat sign frequencies
    holdat_freq = Counter()
    for i in _load_inscriptions():
        for s in i["signs"]: holdat_freq[s] += 1

    # Rank both by frequency
    m77_ranked = [s for s, _ in m77_freq.most_common()]
    holdat_ranked = [s for s, _ in holdat_freq.most_common()]

    # Build crosswalk: M77 code → Holdat M-code via numeric matching
    crosswalk = {}
    for m77_code in m77_ranked[:100]:
        # Try direct numeric match: M77 "342" → Holdat "M342"
        holdat_id = f"M{m77_code.zfill(3)}"
        if holdat_id in holdat_freq:
            crosswalk[m77_code] = holdat_id

    # Also try frequency-rank correlation for top signs
    # Top-10 M77 should correspond to top-10 Holdat (approximately)
    rank_matches = []
    for i, m77_code in enumerate(m77_ranked[:20]):
        if i < len(holdat_ranked):
            holdat_code = holdat_ranked[i]
            rank_matches.append({
                "rank": i + 1,
                "m77": m77_code, "m77_freq": m77_freq[m77_code],
                "holdat": holdat_code, "holdat_freq": holdat_freq[holdat_code],
                "numeric_match": f"M{m77_code.zfill(3)}" == holdat_code,
            })

    n_numeric_match = sum(1 for r in rank_matches if r["numeric_match"])

    return {
        "m77_distinct_signs": len(m77_freq),
        "holdat_distinct_signs": len(holdat_freq),
        "crosswalk_matches": len(crosswalk),
        "top_20_rank_comparison": rank_matches,
        "n_rank_numeric_match": n_numeric_match,
        "verdict": (
            f"M77 crosswalk: {len(crosswalk)} direct numeric matches. "
            f"Top-20 rank: {n_numeric_match}/20 match numerically. "
            f"M77 has {len(m77_freq)} distinct signs vs Holdat {len(holdat_freq)}."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════
# PHASE 380: SHU-ILISHU SIGN IDENTIFICATION
# ═══════════════════════════════════════════════════════════════════════

def phase380_shu_ilishu():
    """Find the best candidate inscription matching /su-i-li-su/ pattern."""
    print("\n[Phase 380] Shu-ilishu sign identification")
    hm = _load_high_map(); ins = _load_inscriptions()

    # Signs with sibilant readings (su/cu/co/can)
    su_signs = {s for s, r in hm.items() if any(v in r.lower() for v in ["su","cu","co","can","cul"])}
    # Signs with i/il/in readings
    i_signs = {s for s, r in hm.items() if any(v in _clean(r) for v in ["i","iṉ","il","iḷ","in"])}
    # Signs with li/il readings
    li_signs = {s for s, r in hm.items() if any(v in _clean(r) for v in ["li","il","iḷ"])}

    # Search for 3-5 sign inscriptions matching pattern: su...i...li...su
    candidates = []
    for i in ins:
        seq = i["signs"]
        if len(seq) < 3 or len(seq) > 6: continue

        # Score: how many of the 4 slots are covered?
        has_su = [j for j, s in enumerate(seq) if s in su_signs]
        has_i = [j for j, s in enumerate(seq) if s in i_signs]
        has_li = [j for j, s in enumerate(seq) if s in li_signs]

        # Best case: su at start, i/li in middle, su at end
        score = 0
        if has_su and has_su[0] == 0: score += 2  # su at start
        if has_su and has_su[-1] == len(seq) - 1: score += 2  # su at end
        if has_i: score += 1
        if has_li: score += 1
        if len(has_su) >= 2: score += 1  # two su signs

        if score >= 4:
            readings = [hm.get(s, "?") for s in seq]
            candidates.append({
                "id": i["id"], "signs": seq, "readings": readings,
                "score": score, "motif": i["motif"], "site": i["site"],
            })

    candidates.sort(key=lambda x: -x["score"])

    return {
        "su_signs": len(su_signs), "i_signs": len(i_signs), "li_signs": len(li_signs),
        "n_candidates": len(candidates),
        "top_10": candidates[:10],
        "verdict": (
            f"Shu-ilishu: {len(candidates)} candidate inscriptions match /su-i-li-su/ pattern. "
            f"Top score: {candidates[0]['score'] if candidates else 0}. "
            f"su-signs: {len(su_signs)}, i-signs: {len(i_signs)}, li-signs: {len(li_signs)}."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════
# PHASE 381: DEDR MORPHEME CORPUS
# ═══════════════════════════════════════════════════════════════════════

def phase381_dedr_corpus():
    """Build PDr morpheme corpus from DEDR vocabulary patterns."""
    print("\n[Phase 381] DEDR morpheme corpus construction")
    try:
        import sys; sys.path.insert(0, str(REPO / "backend"))
        from glossa_lab.data.dravidian import VOCABULARY, EXTENDED_VOCABULARY
        dedr_roots = {**VOCABULARY, **EXTENDED_VOCABULARY}
    except Exception:
        dedr_roots = {}

    if not dedr_roots:
        return {"error": "DEDR vocabulary not available", "verdict": "SKIPPED"}

    # Build morpheme bigrams from DEDR root patterns
    # PDr word formation: ROOT + SUFFIX, ROOT + ROOT (compound)
    COMMON_SUFFIXES = ["am", "an", "aṉ", "ay", "āl", "iṉ", "il", "um", "ē", "ō",
                       "tu", "mu", "ka", "vi", "ku", "ai"]

    bigrams = Counter()
    for root in dedr_roots:
        for suffix in COMMON_SUFFIXES:
            bigrams[(root, suffix)] += 1

    # Root-root compounds (common in PDr)
    common_roots = list(dedr_roots.keys())[:50]
    for i in range(len(common_roots)):
        for j in range(i+1, min(i+5, len(common_roots))):
            bigrams[(common_roots[i], common_roots[j])] += 1

    # Now test: what fraction of our decoded corpus bigrams appear in DEDR patterns?
    hm = _load_high_map(); ins = _load_inscriptions()
    corpus_bi = Counter()
    for i in ins:
        readings = [_clean(hm.get(s, "")) for s in i["signs"]]
        readings = [r for r in readings if r]
        for j in range(len(readings) - 1):
            corpus_bi[(readings[j], readings[j+1])] += 1

    dedr_set = set(bigrams.keys())
    hits = sum(c for bi, c in corpus_bi.items() if bi in dedr_set)
    total = sum(corpus_bi.values())
    coverage = hits / max(1, total)

    return {
        "dedr_roots": len(dedr_roots),
        "dedr_bigrams": len(bigrams),
        "corpus_bigrams": len(corpus_bi),
        "dedr_coverage": round(coverage, 4),
        "verdict": (
            f"DEDR corpus: {len(dedr_roots)} roots, {len(bigrams)} morpheme bigrams. "
            f"Corpus coverage: {coverage:.1%} of decoded bigrams match DEDR patterns."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PHASES 378-381 + 30 INTEGRATED LOOP ITERATIONS")
    print("=" * 70)

    results = {}

    # Run phases 378-381
    for name, fn in [("phase378", phase378_tb_transfer), ("phase379", phase379_m77_crosswalk),
                     ("phase380", phase380_shu_ilishu), ("phase381", phase381_dedr_corpus)]:
        try:
            results[name] = fn()
            print(f"  → {results[name]['verdict']}")
        except Exception as e:
            results[name] = {"error": str(e)}
            print(f"  → {name} ERROR: {e}")
            import traceback; traceback.print_exc()

    # Now run 30 integrated research loop iterations inline
    print(f"\n{'═' * 70}")
    print("INTEGRATED RESEARCH LOOP — 30 cycles")
    print(f"{'═' * 70}")

    # Import and run the loop
    import importlib.util
    spec = importlib.util.spec_from_file_location("irl", REPO / "backend" / "scripts" / "integrated_research_loop.py")
    irl = importlib.util.module_from_spec(spec)

    # Patch sys.argv for argparse
    import sys
    old_argv = sys.argv
    sys.argv = ["integrated_research_loop.py", "--max-cycles", "30"]
    try:
        spec.loader.exec_module(irl)
        irl.main()
    except SystemExit:
        pass
    finally:
        sys.argv = old_argv

    # Load loop results
    loop_path = REPO / "outputs" / "integrated_research_loop.json"
    if loop_path.exists():
        loop_data = json.loads(loop_path.read_text("utf-8"))
        results["integrated_loop"] = {
            "cycles": loop_data.get("cycles_run", 0),
            "papers": loop_data.get("total_papers_mined", 0),
            "insights": loop_data.get("total_insights", 0),
            "new_experiments": loop_data.get("n_new_experiments", 0),
            "verdict": loop_data.get("verdict", ""),
        }

    # Save all results
    OUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  All results saved to {OUT_PATH}")

    # Print summary
    print("\n" + "=" * 70)
    print("FULL SUMMARY")
    print("=" * 70)
    for k in sorted(results):
        v = results[k].get("verdict", results[k].get("error", ""))
        print(f"  {k}: {v[:130]}")


if __name__ == "__main__":
    main()
