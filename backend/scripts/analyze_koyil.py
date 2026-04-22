"""Test the M-5A 'koyil' (temple) hypothesis and analyze P096 positionally.

M-5A = [P324, P096, P062, P060, P120, P256]
With P324='ko': 'ko' + P096 + P062 + P060 + P120 + P256

Tamil 'koyil' (temple) = ko + y + i + l
Breakdown check:
  P324 = 'ko' (full syllable, VERIFIED: never precedes P122)
  P096 = 'y'? (to be tested: must be MEDIAL, not initial)
  P062 = 'i' (MEDIAL, mapped in 10-anchor; but 'koyil' needs 'i' after 'y')
  P060 = 'i' (confirmed anchor MEDIAL)
  P120 = ??? (pure MEDIAL M=1.00)
  P256 = 'l' (TERMINAL, 2nd most common terminal)

If P096='y' and P062='i' are collapsed (both = 'i'), the sequence becomes:
ko + y + i + i + ? + l -> 'koyiil' (emphatic temple?) or ko + yi + l = koyil
OR P096='y' and P062 is a vowel lengthener, so: ko + y(i) + i + ? + l

Run via: shell.cmd python backend/scripts/analyze_koyil.py
"""
import sys, json
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent.parent))

REPORTS = Path(__file__).parent.parent.parent / "reports"

def main():
    corpus_file = Path(__file__).parent.parent.parent / "data" / "indus_cisi_corpus.json"
    corpus = json.loads(corpus_file.read_text())
    seqs = [[g["id"] for g in insc.get("graphemes", [])] for insc in corpus]
    seqs = [s for s in seqs if len(s) >= 2]

    print("="*60)
    print("P096 POSITIONAL ANALYSIS")
    print("="*60)

    # Positional stats for P096
    total = initial = terminal = medial = 0
    before_p096 = Counter()
    after_p096 = Counter()

    for seq in seqs:
        for i, s in enumerate(seq):
            if s != "P096": continue
            total += 1
            if i == 0:               initial += 1
            elif i == len(seq) - 1:  terminal += 1
            else:                    medial += 1
            if i > 0:       before_p096[seq[i-1]] += 1
            if i < len(seq)-1: after_p096[seq[i+1]] += 1

    print(f"P096 total: {total}")
    if total > 0:
        print(f"  Initial:  {initial}/{total} = {100*initial/total:.0f}%")
        print(f"  Medial:   {medial}/{total} = {100*medial/total:.0f}%")
        print(f"  Terminal: {terminal}/{total} = {100*terminal/total:.0f}%")
        print(f"  Before P096: {dict(before_p096.most_common(5))}")
        print(f"  After P096:  {dict(after_p096.most_common(5))}")

    print()
    print("="*60)
    print("M-5A KOYIL HYPOTHESIS TEST")
    print("="*60)
    print("M-5A signs: P324+P096+P062+P060+P120+P256")
    print("With P324='ko' (full syllable):")
    print("  'ko' + P096 + P062 + P060 + P120 + P256")
    print()

    # Check if P096 is strictly MEDIAL (necessary for 'y' = medial consonant)
    if total > 0:
        medial_rate = medial / total
        print(f"P096 medial rate: {medial_rate:.2f}")
        if medial_rate >= 0.60:
            print("  -> P096 is predominantly MEDIAL: consistent with being medial consonant 'y'")
            print("  -> P096 = 'y' hypothesis is STRUCTURALLY SUPPORTED")
        else:
            print(f"  -> P096 is NOT predominantly medial (medial_rate={medial_rate:.2f})")
            print("  -> P096 = 'y' hypothesis is STRUCTURALLY WEAK")

    print()

    # Check: does P324+P096 ONLY appear at start of inscriptions?
    p324_p096 = 0
    p324_p096_initial = 0
    for seq in seqs:
        for i in range(len(seq)-1):
            if seq[i] == "P324" and seq[i+1] == "P096":
                p324_p096 += 1
                if i == 0: p324_p096_initial += 1
    print(f"P324->P096 bigram: n={p324_p096}, of which P324 is inscription-initial: {p324_p096_initial}")

    # What does P062 look like positionally?
    p062_total = p062_init = p062_term = p062_med = 0
    for seq in seqs:
        for i, s in enumerate(seq):
            if s != "P062": continue
            p062_total += 1
            if i == 0: p062_init += 1
            elif i == len(seq)-1: p062_term += 1
            else: p062_med += 1
    if p062_total > 0:
        print(f"\nP062 positional: total={p062_total}, I={p062_init/p062_total:.2f}, M={p062_med/p062_total:.2f}, T={p062_term/p062_total:.2f}")
        print(f"  P062 is {'predominantly MEDIAL' if p062_med/p062_total > 0.7 else 'mixed'}")

    print()
    print("="*60)
    print("REVISED READING ATTEMPT WITH P324='o'")
    print("="*60)

    # Updated anchor map with P324='o'
    anchor_o = {
        "P385": "n",  # genitive suffix [VERIFIED]
        "P324": "o",  # ko-syllable vowel [CRITICAL REVISION]
        "P122": "a",  # pure medial [VERIFIED]
        "P086": "m",  # initial consonant [VERIFIED]
        "P060": "i",  # medial vowel [VERIFIED]
    }

    # Tamil words to check - now including 'o' initial words
    WORDS_O = {
        "on": ["one, alone (Tamil: oru/on)"],
        "oru": ["one (Tamil: oru)"],
        "om": ["sacred sound, fullness"],
        "ol": ["sound, strong (Tamil: ol)"],
        "man": ["earth, sand (Tamil: man)"],
        "kan": ["eye (Tamil: kan)"],
        "kal": ["stone (Tamil: kal)"],
        "van": ["sky, strong (Tamil: van)"],
        "pan": ["work, pig (Tamil: pan)"],
        "maan": ["deer (Tamil: maan)"],
        "mann": ["earth (Tamil: mann)"],
        "nan": ["good, fine (Tamil: nan)"],
        "pon": ["gold (Tamil: pon)"],
        "ton": ["ancient, old (Tamil: tol/ton)"],
        "ona": ["one (Tamil: oru/ona)"],
        "oma": ["Tamil sacred sound"],
        "min": ["fish, star (Tamil: min)"],
        "ain": ["five (Tamil: ain/aintu)"],
        "mai": ["black, ink (Tamil: mai)"],
        "mai": ["black (Tamil: mai)"],
        "mai": ["eye shadow (Tamil: mai)"],
    }

    print("\nSample inscriptions re-read with P324='o':")
    readable = []
    for insc in corpus:
        insc_id = insc.get("id", "?")
        signs = [g["id"] for g in insc.get("graphemes", []) if g.get("id")]
        if len(signs) < 2: continue
        phonemes = [anchor_o.get(s, "?") for s in signs]
        n_anchored = sum(1 for p in phonemes if p != "?")
        cov = n_anchored / len(signs)
        if cov < 0.4: continue  # skip very low coverage

        ps = "".join(p for p in phonemes if p != "?")
        full = "".join(phonemes)

        # Check for word matches
        matches = []
        for w, gs in WORDS_O.items():
            if w in ps: matches.append(f"{w}:{gs[0][:30]}")

        readable.append((insc_id, signs, full, ps, cov, matches))

    # Sort by coverage desc
    readable.sort(key=lambda x: -x[4])
    for insc_id, signs, full, ps, cov, matches in readable[:25]:
        match_str = f"  [{', '.join(matches[:2])}]" if matches else ""
        print(f"  {insc_id:8s}  {''.join(full):20s}  ({cov*100:.0f}% cov){match_str}")

    # M-5A specifically
    print()
    print("M-5A specifically:")
    m5a = next((insc for insc in corpus if insc.get("id") == "M-5A"), None)
    if m5a:
        signs = [g["id"] for g in m5a.get("graphemes", []) if g.get("id")]
        p_o = [anchor_o.get(s, "?") for s in signs]
        print(f"  Signs: {signs}")
        print(f"  P324='o' mapping: {''.join(p_o)}")
        print(f"  Full anchor: P324='ko' + P096='?' + P062='?' + P060='i' + P120='?' + P256='?'")
        print(f"  If P096='y': 'ko'+'y'+'?'+'i'+'?'+'?' = first chars = 'koy...'")
        if total > 0 and medial / total >= 0.6:
            print(f"  P096 IS medial ({medial}/{total}): 'koyil' reading STRUCTURALLY POSSIBLE [INFERRED]")
        else:
            print(f"  P096 positional evidence too weak to confirm")

    # Save results
    out = REPORTS / "koyil_analysis.json"
    out.write_text(json.dumps({
        "p096_stats": {
            "total": total, "initial": initial, "medial": medial, "terminal": terminal,
            "before_top5": dict(before_p096.most_common(5)),
            "after_top5": dict(after_p096.most_common(5)),
        },
        "p324_p096_bigram": {"count": p324_p096, "initial_count": p324_p096_initial},
        "m5a_reading": {
            "signs": ["P324","P096","P062","P060","P120","P256"],
            "with_p324_o": "o?ui?",
            "koyil_possible": total > 0 and medial / max(total,1) >= 0.6,
        },
        "top_readable_with_o": [(a,b) for a,_,b,_,_,_ in readable[:20]],
    }, indent=2))
    print(f"\nSaved -> reports/koyil_analysis.json")


if __name__ == "__main__":
    main()
