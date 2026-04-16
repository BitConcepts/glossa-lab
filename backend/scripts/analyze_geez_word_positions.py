"""
Analyse word-position preferences of signs in the Geez clean corpus.

Dr. Fuls specifically requested: "Check the preferred word position in the
Geez corpus of the anchor signs!"

Outputs:
  - For every sign: initial rate (I), medial rate (M), terminal rate (T)
  - Top 20 word-FINAL signs (best anchor candidates per Dr. Fuls)
  - Top 20 word-INITIAL signs
  - For the high-frequency (frequency-ranked) anchors: their position profiles
  - Saved to reports/geez_word_position_analysis.json
"""
import sys, os, json, re
from collections import Counter
from pathlib import Path

_BACKEND = Path(__file__).resolve().parent.parent
_CLEAN   = _BACKEND / "glossa_lab" / "data" / "geez" / "Geez_Genesis_syllabic_nopunctuation.txt"
_REPORTS = _BACKEND.parent / "reports"

def is_syllabic(c):
    cp = ord(c)
    return 0x1200 <= cp <= 0x137F and not (0x1361 <= cp <= 0x1368)

def load_words():
    content = _CLEAN.read_text(encoding="utf-8")
    words_raw = re.findall(r'[\u1200-\u1360]+', content)
    words = [[c for c in w if is_syllabic(c)] for w in words_raw]
    return [w for w in words if len(w) >= 2]

def analyse(words):
    total  = Counter(c for w in words for c in w)
    inits  = Counter(w[0] for w in words)
    terms  = Counter(w[-1] for w in words)
    meds   = Counter(c for w in words for c in w[1:-1] if len(w) > 2)

    results = {}
    for sign, n in total.items():
        i_rate = inits[sign] / n
        t_rate = terms[sign] / n
        m_rate = meds[sign]  / n
        dominant = "TERMINAL" if t_rate >= 0.60 else (
                   "INITIAL"  if i_rate >= 0.50 else (
                   "MEDIAL"   if m_rate >= 0.65 else "MIXED"))
        results[sign] = {
            "freq": n,
            "i_rate": round(i_rate, 4),
            "m_rate": round(m_rate, 4),
            "t_rate": round(t_rate, 4),
            "dominant": dominant,
            "codepoint": f"U+{ord(sign):04X}",
        }
    return results

def main():
    words = load_words()
    flat  = [c for w in words for c in w]
    print(f"Words: {len(words):,}  |  Tokens: {len(flat):,}  |  Signs: {len(set(flat))}")

    profiles = analyse(words)

    # Sort by terminal rate
    by_terminal  = sorted(profiles.items(), key=lambda x: -x[1]["t_rate"])
    by_initial   = sorted(profiles.items(), key=lambda x: -x[1]["i_rate"])
    by_frequency = sorted(profiles.items(), key=lambda x: -x[1]["freq"])

    # Top-20 word-FINAL anchors (Dr. Fuls' recommendation)
    print("\n=== TOP 20 WORD-FINAL SIGNS (best anchor candidates) ===")
    print(f"{'Sign':6} {'T-rate':8} {'I-rate':8} {'M-rate':8} {'Freq':7} {'Dominant':10} {'Codepoint'}")
    print("-" * 65)
    top_final = []
    for sign, p in by_terminal[:20]:
        print(f"  {sign}    {p['t_rate']:6.1%}   {p['i_rate']:6.1%}   {p['m_rate']:6.1%}   "
              f"{p['freq']:5,}  {p['dominant']:10}  {p['codepoint']}")
        top_final.append({"sign": sign, **p})

    # Top-10 word-INITIAL signs (for contrast)
    print("\n=== TOP 10 WORD-INITIAL SIGNS (contrast) ===")
    print(f"{'Sign':6} {'I-rate':8} {'T-rate':8} {'Freq':7} {'Dominant':10} {'Codepoint'}")
    print("-" * 55)
    for sign, p in by_initial[:10]:
        print(f"  {sign}    {p['i_rate']:6.1%}   {p['t_rate']:6.1%}   "
              f"{p['freq']:5,}  {p['dominant']:10}  {p['codepoint']}")

    # Top-20 frequency-ranked signs and their position profiles
    print("\n=== TOP 20 FREQUENCY-RANKED SIGNS (current structured anchors) ===")
    print(f"{'Sign':6} {'Freq':7} {'T-rate':8} {'I-rate':8} {'M-rate':8} {'Dominant':10}")
    print("-" * 60)
    freq_anchors = []
    for sign, p in by_frequency[:20]:
        marker = " <-- TERMINAL" if p["dominant"] == "TERMINAL" else ""
        print(f"  {sign}    {p['freq']:5,}   {p['t_rate']:6.1%}   {p['i_rate']:6.1%}   "
              f"{p['m_rate']:6.1%}  {p['dominant']:10}{marker}")
        freq_anchors.append({"sign": sign, **p})

    # How many of the top-20 freq anchors are TERMINAL?
    n_terminal = sum(1 for p in freq_anchors if p["dominant"] == "TERMINAL")
    mean_t_rate_freq  = sum(p["t_rate"] for p in freq_anchors) / len(freq_anchors)
    mean_t_rate_final = sum(p["t_rate"] for p in top_final)    / len(top_final)

    print(f"\nSummary:")
    print(f"  Frequency-ranked top-20: {n_terminal}/20 are TERMINAL dominant")
    print(f"  Mean T-rate (freq top-20):   {mean_t_rate_freq:.1%}")
    print(f"  Mean T-rate (word-final top-20): {mean_t_rate_final:.1%}")
    print(f"  Overlap (freq top-20 in word-final top-20): "
          f"{len(set(p['sign'] for p in freq_anchors) & set(p['sign'] for p in top_final))}")

    # Save
    out = {
        "corpus": "geez_clean_nopunct",
        "total_words":  len(words),
        "total_tokens": len(flat),
        "total_signs":  len(profiles),
        "top20_word_final":   top_final,
        "top20_frequency":    freq_anchors,
        "mean_t_rate_freq_top20":  round(mean_t_rate_freq, 4),
        "mean_t_rate_final_top20": round(mean_t_rate_final, 4),
        "all_profiles": {s: p for s, p in sorted(profiles.items(),
                                                   key=lambda x: -x[1]["freq"])},
    }
    outpath = _REPORTS / "geez_word_position_analysis.json"
    outpath.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved → {outpath}")
    return out

if __name__ == "__main__":
    main()
