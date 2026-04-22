"""Analyze P332 (most common P324-follower) and disambiguate M-148A.

P332: appears n=10 in CISI, always follows P324. Positional class determines
whether it's a vowel sign (completing 'ko' + vowel) or a consonant.

M-148A = [P324, P385, P231]:
  With 5-anchor SA: k+n+? = 'kn?' — phonologically odd (CCC cluster)
  Interpretation A: P324(ko) + P385(n-suffix) + P231 = "ko" (king) + genitive '-n' + something
  Interpretation B: P324(k) + vowel(implicit) + P385(n) = 'Xan/Xon' word
  Interpretation C: M-148A is a short formula "ko-n" = "of the king" (royal seal?)

Also tests 6-anchor SA: add P332 as anchor if phoneme is strongly indicated.

Run: shell.cmd python backend/scripts/analyze_p332_m148.py
"""
import sys, json
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent.parent))

REPORTS = Path(__file__).parent.parent.parent / "reports"

def positional_stats(sign, seqs):
    total = initial = terminal = medial = 0
    before = Counter()
    after = Counter()
    contexts = []
    for seq in seqs:
        for i, s in enumerate(seq):
            if s != sign: continue
            total += 1
            if i == 0:               initial += 1
            elif i == len(seq) - 1:  terminal += 1
            else:                    medial += 1
            if i > 0:        before[seq[i-1]] += 1
            if i < len(seq)-1: after[seq[i+1]] += 1
            pre  = seq[i-1] if i > 0 else "--"
            post = seq[i+1] if i < len(seq)-1 else "--"
            contexts.append((pre, sign, post, seq))
    return total, initial, terminal, medial, before, after, contexts


def main():
    corpus_file = Path(__file__).parent.parent.parent / "data" / "indus_cisi_corpus.json"
    corpus = json.loads(corpus_file.read_text())
    seqs = [[g["id"] for g in insc.get("graphemes",[]) if g.get("id")] for insc in corpus]
    seqs = [s for s in seqs if len(s) >= 2]

    anchor5 = {"P385":"n","P324":"k","P122":"a","P086":"m","P060":"i"}

    print("="*60)
    print("P332 POSITIONAL ANALYSIS")
    print("="*60)
    t, i, term, med, bef, aft, ctxs = positional_stats("P332", seqs)
    print(f"P332 total: {t}")
    if t > 0:
        print(f"  Initial:  {i}/{t} = {100*i/t:.0f}%")
        print(f"  Medial:   {med}/{t} = {100*med/t:.0f}%")
        print(f"  Terminal: {term}/{t} = {100*term/t:.0f}%")
        print(f"  Before P332: {dict(bef.most_common(6))}")
        print(f"  After P332:  {dict(aft.most_common(6))}")

    # Does P332 always follow P324?
    p324_before_p332 = bef.get("P324", 0)
    print(f"\nP324 before P332: {p324_before_p332}/{t} = {100*p324_before_p332/max(t,1):.0f}%")

    # What follows P332 (trigrams)?
    print(f"\nTrigrams P324 -> P332 -> ? :")
    p332_after_p324 = Counter()
    for seq in seqs:
        for idx in range(len(seq)-2):
            if seq[idx]=="P324" and seq[idx+1]=="P332":
                p332_after_p324[seq[idx+2]] += 1
    for sign, n in p332_after_p324.most_common(10):
        role = anchor5.get(sign, "?")
        print(f"  -> {sign} (n={n}) maps_to={role}")

    # Phoneme candidate for P332
    print(f"\nP332 PHONEME ASSESSMENT:")
    if t > 0:
        med_rate = med / t
        init_rate = i / t
        term_rate = term / t
        p324_pct = p324_before_p332 / t
        print(f"  Medial rate: {med_rate:.2f}")
        print(f"  Always after P324: {p324_pct:.2f}")
        if med_rate >= 0.70 and p324_pct >= 0.80:
            print("  -> P332 is predominantly MEDIAL and almost always follows P324")
            print("  -> P332 likely = vowel completing P324's syllable: 'ko'+'vowel'")
            print("  -> Candidates: P332='o' (ko+o=koo?), P332='u' (ku), P332='e' (ke)")
            print("  -> Most likely: P332 = VOWEL LENGTHENER or null sign, NOT a phoneme by itself")
            print("  -> OR: P332 = second sign of 'ko' syllable (if P324=k then P332=o)")
        elif med_rate >= 0.70:
            print(f"  -> P332 = predominantly medial CV phoneme")
        else:
            print(f"  -> P332 = mixed positional class")

    # Full inscriptions with P332
    print(f"\nAll inscriptions containing P332:")
    for insc in corpus:
        signs = [g["id"] for g in insc.get("graphemes",[]) if g.get("id")]
        if "P332" not in signs: continue
        phonemes = [anchor5.get(s, "?") for s in signs]
        print(f"  {insc['id']:8s}  {signs}  -> {''.join(phonemes)}")

    print()
    print("="*60)
    print("M-148A DISAMBIGUATION: 'kon/kn' vs 'on' vs TITLE FORMULA")
    print("="*60)
    m148 = next((insc for insc in corpus if insc.get("id")=="M-148A"), None)
    if m148:
        signs = [g["id"] for g in m148.get("graphemes",[]) if g.get("id")]
        print(f"Signs: {signs}")
        print(f"5-anchor mapping: {''.join(anchor5.get(s,'?') for s in signs)}")
        print()
        # P231 analysis
        t231, i231, term231, med231, bef231, aft231, _ = positional_stats("P231", seqs)
        print(f"P231 stats: total={t231}, I={i231/max(t231,1):.2f}, M={med231/max(t231,1):.2f}, T={term231/max(t231,1):.2f}")
        print(f"  Before P231: {dict(bef231.most_common(5))}")
        print(f"  After P231: {dict(aft231.most_common(5))}")

        # Interpretation analysis
        print()
        print("INTERPRETATIONS:")
        print("A) P324(ko) + P385(n=genitive) + P231(?) = 'ko-n-?' = 'king's X' [title formula]")
        print("   This reading treats M-148A as a royal seal formula: ko(king) + genitive")
        print("   If P231 is a terminal name/marker: 'of-the-king [name]'")
        print()
        print("B) P324(k) + implicit-vowel + P385(n) = 'k?n' consonant frame")
        print("   Tamil frames: k_n = kan(eye), kon(kill), kun(mound), kin(below)")
        print("   Most likely: 'kon' = to kill/take (Tamil: koNal) or 'kin' = eastern")
        print()
        print("C) M-148A = SHORT TITLE SEAL = '[royal-title] + [genitive] + [personal-marker]'")
        print("   Consistent with Harappan seals as administrative/identity markers")
        print("   P324 = 'ko' (title), P385 = genitive '-n', P231 = terminal marker")

    print()
    print("="*60)
    print("6-ANCHOR CANDIDATE: P332")
    print("="*60)
    # Check if adding P332 as an anchor is justified
    if t > 0 and med / t >= 0.70:
        # What is the most common sign that follows P332 after P324?
        most_common_after = p332_after_p324.most_common(1)
        print(f"Most common after P324->P332: {most_common_after}")
        print()
        print("If P332 = 'o' (vowel sign completing 'ko' from P324='k'):")
        print("  P324(k)+P332(o)+... = 'ko...' compound representation")
        print("  This would support: P324+P332 = bi-gram sign for 'ko'")
        print()
        print("If P332 = 'u' (another vowel, giving P324+P332 = 'ku'):")
        print("  Tamil 'ku' = to dig, to sow; prefix in many words")
        print()
        print("Frequency: P332 appears only", t, "times in 178 inscriptions")
        if t < 8:
            print(f"  -> INSUFFICIENT frequency (n={t}) for reliable anchor assignment")
            print("  -> DO NOT add P332 as anchor yet; need full corpus (3K+ inscriptions)")
        else:
            print(f"  -> Frequency sufficient (n={t}) — candidate for 6th anchor if phoneme confirmed")
    else:
        print(f"P332 frequency n={t} or medial rate too low — NOT a reliable anchor candidate yet")

    # Save
    out = REPORTS / "p332_m148_analysis.json"
    out.write_text(json.dumps({
        "p332": {
            "total": t, "initial": i, "medial": med, "terminal": term,
            "before_top5": dict(bef.most_common(5)) if t > 0 else {},
            "after_top5": dict(aft.most_common(5)) if t > 0 else {},
            "p324_before_pct": round(p324_before_p332/max(t,1)*100, 1),
            "trigrams_after_p324": dict(p332_after_p324.most_common(8)),
        },
        "m148a": {
            "signs": signs if m148 else [],
            "interpretations": ["title_formula", "consonant_frame", "short_title_seal"],
            "p231_stats": {"total": t231, "medial_rate": round(med231/max(t231,1),2)},
        },
        "p332_anchor_viable": t >= 8 and med/max(t,1) >= 0.70,
    }, indent=2))
    print(f"\nSaved -> reports/p332_m148_analysis.json")


if __name__ == "__main__":
    main()
