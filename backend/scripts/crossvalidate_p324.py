"""Cross-validate P324 phoneme: 'ko' (king/chief) vs 'k' + vowel (kal/kan/etc.)

P324 is the most frequent sign in CISI (n=99, I=0.78). Our 10-anchor mapping assigns it 'k'.
The question: is P324 the initial consonant /k/ (so the vowel comes from the next sign),
or is it a full syllable 'ko', 'ku', 'ka', etc.?

Evidence from CISI bigrams:
- P324 -> P332 (n=10): P332 is MEDIAL. If P324='k', P332 carries the vowel.
- P324 -> P086 (n=5): P086 is also INITIAL (mapped to 'm'). P324+P086 = 'k'+'m'?
  More likely P086 here is medial (its I=0.54 means ~46% medial).
- P324 -> P175 (n=4): P175 is MEDIAL.
- P324 -> P154 (n=4): P154 is MEDIAL.
- P324 -> P050 (n=3): P050 is pure MEDIAL (mapped to 'v'). P324+P050 = 'k'+'v' = kv-? 
  More likely P050 here carries /va/ so P324+P050 = 'kva' (unlikely) or P324='ko' and P050='v'...

If P324 = 'ko': P324+P050+... = 'ko'+'v'... = 'kov...' = possibly 'kovaL' or 'koval'
If P324 = 'k' only: P324+P050+... = 'k'+'v'... = missing vowel between them

Tamil linguistic check:
- 'ko' = king/chief → 'ko-v-al' = shepherd, 'ko' = bull/bovine (Dravidian DEDR 2147)
- 'kal' = stone (k+a+l, needs P122='a' and P256='l' after P324)
- 'kan' = eye (k+a+n, needs P122='a' and P385='n')

Key test: does P324 appear directly before P122 (='a')?
If yes: P324+P122 = 'k'+'a' = 'ka' (P324 is pure consonant /k/)
If P324 rarely precedes P122, it might carry its own vowel.

Run via: shell.cmd python backend/scripts/crossvalidate_p324.py
"""
import sys, json
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    corpus_file = Path(__file__).parent.parent.parent / "data" / "indus_cisi_corpus.json"
    if not corpus_file.exists():
        print("ERROR: data/indus_cisi_corpus.json not found.")
        sys.exit(1)

    corpus = json.loads(corpus_file.read_text())
    seqs = [[g["id"] for g in insc.get("graphemes", [])] for insc in corpus]
    seqs = [s for s in seqs if len(s) >= 2]

    # What follows P324?
    p324_followers = Counter()
    p324_precedes = Counter()
    p324_contexts = []  # (preceding, P324, following1, following2)

    for seq in seqs:
        for i, sign in enumerate(seq):
            if sign == "P324":
                if i > 0:
                    p324_precedes[seq[i-1]] += 1
                if i < len(seq) - 1:
                    p324_followers[seq[i+1]] += 1
                # Record full context
                pre = seq[i-1] if i > 0 else "--"
                post1 = seq[i+1] if i < len(seq)-1 else "--"
                post2 = seq[i+2] if i < len(seq)-2 else "--"
                p324_contexts.append((pre, "P324", post1, post2))

    print(f"P324 total occurrences: {sum(p324_followers.values()) + (1 if p324_followers else 0)}")
    print(f"\nSigns that FOLLOW P324 (top 15):")
    for sign, n in p324_followers.most_common(15):
        print(f"  {sign}: n={n}")

    print(f"\nSigns that PRECEDE P324 (top 10):")
    for sign, n in p324_precedes.most_common(10):
        print(f"  {sign}: n={n}")

    # Key test: does P324 directly precede P122?
    p324_before_p122 = p324_followers.get("P122", 0)
    p324_total = sum(p324_followers.values())
    print(f"\nKEY TEST: P324 directly before P122 ('a'): {p324_before_p122}/{p324_total} = {100*p324_before_p122/max(p324_total,1):.1f}%")

    if p324_before_p122 / max(p324_total, 1) > 0.15:
        print("  -> P324 frequently precedes 'a' (P122): SUPPORTS P324 = consonant /k/ (needs next sign for vowel)")
        print("  -> Reading: P324+P122+... = 'k'+'a'+... = 'ka...' Dravidian stem")
    else:
        print("  -> P324 rarely precedes 'a' (P122): SUGGESTS P324 = syllable 'ko' or 'ku' (has own vowel)")
        print("  -> Reading: P324+... = 'ko...' or 'ku...' Dravidian stem")

    # Check P324+P122+P385 = 'kan' (eye)
    kan_count = 0
    for seq in seqs:
        for i in range(len(seq)-2):
            if seq[i]=="P324" and seq[i+1]=="P122" and seq[i+2]=="P385":
                kan_count += 1
    print(f"\nTrigram P324+P122+P385 = 'k'+'a'+'n' = 'kan' (eye): n={kan_count}")

    # Check P324+P122+P256 = 'kal' (stone)
    kal_count = 0
    for seq in seqs:
        for i in range(len(seq)-2):
            if seq[i]=="P324" and seq[i+1]=="P122" and seq[i+2]=="P256":
                kal_count += 1
    print(f"Trigram P324+P122+P256 = 'k'+'a'+'l' = 'kal' (stone): n={kal_count}")

    # Check P217+P122+P385 = 'pan' (work)
    pan_count = 0
    for seq in seqs:
        for i in range(len(seq)-2):
            if seq[i]=="P217" and seq[i+1]=="P122" and seq[i+2]=="P385":
                pan_count += 1
    print(f"Trigram P217+P122+P385 = 'p'+'a'+'n' = 'pan' (work/pig): n={pan_count}")

    # Check P086+P122+P385 = 'man' (earth)
    man_count = 0
    for seq in seqs:
        for i in range(len(seq)-2):
            if seq[i]=="P086" and seq[i+1]=="P122" and seq[i+2]=="P385":
                man_count += 1
    print(f"Trigram P086+P122+P385 = 'm'+'a'+'n' = 'man' (earth/sand): n={man_count}")

    # Full sequence display for inscriptions containing P324
    print(f"\nAll inscriptions containing P324 (sample 20):")
    anchor = {"P385":"n","P324":"k","P122":"a","P086":"m","P060":"i",
              "P256":"l","P217":"p","P050":"v","P145":"r","P062":"u"}
    shown = 0
    for insc in corpus:
        signs = [g["id"] for g in insc.get("graphemes",[]) if g.get("id")]
        if "P324" not in signs: continue
        phonemes = [anchor.get(s, "?") for s in signs]
        print(f"  {insc['id']:8s}  {signs}  ->  {''.join(phonemes)}")
        shown += 1
        if shown >= 20: break

    # Save
    out = Path(__file__).parent.parent.parent / "reports" / "p324_crossvalidation.json"
    out.write_text(json.dumps({
        "p324_followers": dict(p324_followers.most_common(20)),
        "p324_precedes": dict(p324_precedes.most_common(10)),
        "p324_before_p122_count": p324_before_p122,
        "p324_before_p122_pct": round(p324_before_p122/max(p324_total,1)*100, 1),
        "kan_trigram_count": kan_count,
        "kal_trigram_count": kal_count,
        "pan_trigram_count": pan_count,
        "man_trigram_count": man_count,
    }, indent=2))
    print(f"\nSaved -> reports/p324_crossvalidation.json")


if __name__ == "__main__":
    main()
