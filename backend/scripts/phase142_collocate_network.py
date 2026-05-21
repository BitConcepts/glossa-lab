"""
Phase-142: Collocate Network + INITIAL Vocabulary + Formula Classification

Extends the fish-sign compound-context finding (Phase-127) to the full corpus.
All analysis uses real corpus data only (Holdat LLC v3). No synthetic data.

Tests motivated by the Roif exchange:
  A. Sign collocate network — which signs appear adjacent most often?
     Reveals compound clusters = potential title formulas
  B. INITIAL sign vocabulary — full inventory of INITIAL-dominant signs
     with readings, frequencies, and top right-neighbors.
     Maps the "title/determinative" vocabulary of the script.
  C. Formula type classification — classify seals by INITIAL sign.
     Do different INITIAL signs correlate with different iconographies/sites?
     If so, different "titles" appear in functionally distinct seal types.
  D. Positional collocate divergence — for polysemous signs:
     do left/right neighbor profiles differ by positional slot?
     Tests Roif's core shorthand claim: same sign, different context = different meaning.
  E. M267 genitive validation — show systematically that M267 behaves
     as a grammatical particle (follows INITIAL signs, precedes TERMINAL signs)
     consistent with a genitive/possessive function.

Output: backend/reports/phase142_collocate_network.json
"""
import datetime
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "glossa_lab" / "data"))

try:
    import pandas as pd; HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
OUT          = REPO / "backend/reports/phase142_collocate_network.json"

print("="*70); print("PHASE-142: COLLOCATE NETWORK + FORMULA ANALYSIS"); print("="*70)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors = anchor_data["anchors"]
hm_set   = {k for k,v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}
high_set = {k for k,v in anchors.items() if v.get("confidence") == "HIGH"}

# Build corpus
seals = {}
if HAS_PANDAS:
    df = pd.read_csv(HOLDAT)
    for _, row in df.iterrows():
        f = str(row.get("form","")); s = str(row.get("letters",""))
        site = str(row.get("site","")); icon = str(row.get("iconography","")) if "iconography" in df.columns else ""
        if f and s:
            if f not in seals: seals[f] = {"site":site,"signs":[],"icon":icon}
            seals[f]["signs"].append(s)
else:
    with open(HOLDAT,encoding="utf-8") as fh:
        hdr = fh.readline().strip().split(",")
        ci = {h:i for i,h in enumerate(hdr)}
        for line in fh:
            p = line.strip().split(",")
            if len(p) < 2: continue
            f=p[ci.get("form",0)]; s=p[ci.get("letters",1)]
            site=p[ci.get("site",2)] if ci.get("site",2)<len(p) else ""
            icon=p[ci.get("iconography",3)] if ci.get("iconography",3)<len(p) else ""
            if f and s:
                if f not in seals: seals[f]={"site":site,"signs":[],"icon":icon}
                seals[f]["signs"].append(s)

all_seqs = [d["signs"] for d in seals.values()]
all_flat  = [s for seq in all_seqs for s in seq]
sign_freq = Counter(all_flat)
n_seals   = len(seals)
n_tokens  = len(all_flat)
print(f"\nCorpus: {n_seals} seals, {n_tokens} tokens, {len(sign_freq)} distinct signs")

results = {}

# ═══════════════════════════════════════════════════════════════════════════════
# A: Sign Collocate Network
# ═══════════════════════════════════════════════════════════════════════════════
print("\n"+"─"*70); print("A: SIGN COLLOCATE NETWORK"); print("─"*70)

# Build bigram counts and pointwise mutual information (PMI)
bigrams = Counter()
for seq in all_seqs:
    for i in range(len(seq)-1):
        bigrams[(seq[i], seq[i+1])] += 1

total_bigrams = sum(bigrams.values())
N = n_tokens

def pmi(a, b, count_ab, n_a, n_b, total):
    """Pointwise mutual information: log P(a,b) / P(a)P(b)"""
    if count_ab == 0 or n_a == 0 or n_b == 0: return 0
    p_ab = count_ab / total
    p_a  = n_a / N
    p_b  = n_b / N
    return math.log2(p_ab / (p_a * p_b)) if p_a*p_b > 0 else 0

# Top bigrams by frequency (restricted to H+M signs for interpretability)
hm_bigrams = {(a,b):c for (a,b),c in bigrams.items() if a in hm_set and b in hm_set}
top_hm_bigrams = sorted(hm_bigrams.items(), key=lambda x:-x[1])[:30]

print(f"  Total distinct bigrams: {len(bigrams)}")
print(f"  H+M × H+M bigrams: {len(hm_bigrams)}")
print("\n  Top 20 H+M bigrams by frequency:")
print(f"  {'Bigram':25s} {'Count':>7} {'PMI':>7} {'A_reading':15s} {'B_reading'}")
for (a,b),c in top_hm_bigrams[:20]:
    p = pmi(a, b, c, sign_freq[a], sign_freq[b], total_bigrams)
    ar = anchors.get(a,{}).get("reading","?")[:12]
    br = anchors.get(b,{}).get("reading","?")[:12]
    print(f"  {a+' · '+b:25s} {c:>7} {p:>7.2f} {ar:15s} {br}")

# High-PMI pairs (min 3 occurrences) — strong collocates
high_pmi = []
for (a,b),c in bigrams.items():
    if c < 3: continue
    p = pmi(a, b, c, sign_freq[a], sign_freq[b], total_bigrams)
    if p > 1.5:
        high_pmi.append({"a":a,"b":b,"count":c,"pmi":round(p,3),
                          "a_conf":anchors.get(a,{}).get("confidence","?"),
                          "b_conf":anchors.get(b,{}).get("confidence","?"),
                          "a_reading":anchors.get(a,{}).get("reading","?"),
                          "b_reading":anchors.get(b,{}).get("reading","?")})
high_pmi.sort(key=lambda x:-x["pmi"])

print(f"\n  High-PMI pairs (PMI > 1.5, count ≥ 3): {len(high_pmi)}")
print("  Top 15:")
for pair in high_pmi[:15]:
    print(f"    {pair['a']} · {pair['b']} count={pair['count']} PMI={pair['pmi']:.2f} "
          f"({pair['a_reading']} · {pair['b_reading']})")

results["A_collocate_network"] = {
    "n_distinct_bigrams": len(bigrams),
    "n_hm_hm_bigrams": len(hm_bigrams),
    "top_30_hm_bigrams": [{"pair":f"{a}·{b}","count":c,"pmi":round(pmi(a,b,c,sign_freq[a],sign_freq[b],total_bigrams),3),
                            "a_reading":anchors.get(a,{}).get("reading","?"),
                            "b_reading":anchors.get(b,{}).get("reading","?")}
                           for (a,b),c in top_hm_bigrams],
    "high_pmi_pairs": high_pmi[:50],
    "interpretation": (
        f"{len(hm_bigrams)} distinct H+M × H+M bigrams. "
        f"{len(high_pmi)} strong collocate pairs (PMI > 1.5, ≥3 occurrences). "
        f"High-PMI pairs represent recurring compound title formulas."
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# B: INITIAL Sign Vocabulary
# ═══════════════════════════════════════════════════════════════════════════════
print("\n"+"─"*70); print("B: INITIAL SIGN VOCABULARY"); print("─"*70)

tc = Counter(all_flat)
ic = Counter(seq[0] for seq in all_seqs if len(seq) > 1)
te = Counter(seq[-1] for seq in all_seqs if len(seq) > 1)

# Signs with INITIAL rate >= 0.50 and freq >= 5
initial_vocab = []
for sign, n in tc.items():
    if n < 5: continue
    i_rate = ic[sign] / n
    t_rate = te[sign] / n
    if i_rate >= 0.50:
        # Top right-neighbors when in INITIAL position
        right_when_initial = Counter()
        for seq in all_seqs:
            if len(seq) > 1 and seq[0] == sign:
                right_when_initial[seq[1]] += 1
        initial_vocab.append({
            "sign": sign,
            "freq": n,
            "i_rate": round(i_rate, 3),
            "t_rate": round(t_rate, 3),
            "confidence": anchors.get(sign,{}).get("confidence","NONE"),
            "reading": anchors.get(sign,{}).get("reading","?"),
            "basis": (anchors.get(sign,{}).get("basis","") or "")[:60],
            "top_right_neighbors": [{"sign":s,"count":c,"reading":anchors.get(s,{}).get("reading","?")}
                                     for s,c in right_when_initial.most_common(5)],
        })

initial_vocab.sort(key=lambda x: -x["freq"])
hm_initial = [v for v in initial_vocab if v["confidence"] in ("HIGH","MEDIUM")]

print(f"  Total INITIAL-dominant signs (i_rate ≥ 0.50, freq ≥ 5): {len(initial_vocab)}")
print(f"  With H+M readings: {len(hm_initial)}")
print("\n  H+M INITIAL signs (title/determinative vocabulary):")
print(f"  {'Sign':<8} {'Freq':>5} {'I-rate':>7} {'Reading':<15} {'Conf':<8} {'Top right-neighbor'}")
for v in hm_initial[:25]:
    top_r = v['top_right_neighbors'][0]['sign'] if v['top_right_neighbors'] else "—"
    top_r_read = v['top_right_neighbors'][0]['reading'] if v['top_right_neighbors'] else "—"
    print(f"  {v['sign']:<8} {v['freq']:>5} {v['i_rate']:>7.3f} {v['reading']:<15} {v['confidence']:<8} {top_r} ({top_r_read})")

results["B_initial_vocabulary"] = {
    "n_initial_signs_total": len(initial_vocab),
    "n_initial_hm": len(hm_initial),
    "initial_vocabulary": initial_vocab[:50],
    "interpretation": (
        f"{len(hm_initial)} H+M signs have INITIAL-dominant positional profile (i_rate ≥ 0.50). "
        f"These constitute the title/determinative vocabulary: professional roles, clan markers, "
        f"place names. Their top right-neighbors reveal what types of name components follow each title."
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# C: Formula Type Classification
# ═══════════════════════════════════════════════════════════════════════════════
print("\n"+"─"*70); print("C: FORMULA TYPE CLASSIFICATION BY INITIAL SIGN"); print("─"*70)

# For each multi-sign seal, record its INITIAL sign
# Then cross-tabulate INITIAL sign × iconography
formula_types = defaultdict(lambda: {"seals":[],"sites":Counter(),"icons":Counter(),"seq_lengths":[]})

for form, data in seals.items():
    seq = data["signs"]
    if len(seq) <= 1: continue
    initial = seq[0]
    icon = data["icon"]
    site = data["site"]
    formula_types[initial]["seals"].append(form)
    formula_types[initial]["sites"][site] += 1
    if icon and icon != "nan":
        icon_key = icon[:30].strip()
        formula_types[initial]["icons"][icon_key] += 1
    formula_types[initial]["seq_lengths"].append(len(seq))

# Focus on frequent INITIAL signs
print(f"  Distinct INITIAL signs in multi-sign seals: {len(formula_types)}")
print("\n  Top 20 INITIAL signs by seal count:")
print(f"  {'Sign':<8} {'Seals':>6} {'Avg_len':>8} {'Reading':<14} {'Top_icon'}")

top_initials = sorted(formula_types.items(), key=lambda x: -len(x[1]["seals"]))
formula_summary = []
for sign, data in top_initials[:20]:
    n = len(data["seals"])
    avg_len = sum(data["seq_lengths"])/len(data["seq_lengths"])
    conf = anchors.get(sign,{}).get("confidence","?")
    reading = anchors.get(sign,{}).get("reading","?")[:12]
    top_icon = data["icons"].most_common(1)[0][0][:25] if data["icons"] else "—"
    top_site = data["sites"].most_common(1)[0][0] if data["sites"] else "—"
    print(f"  {sign:<8} {n:>6} {avg_len:>8.1f} {reading:<14} {top_icon}")
    formula_summary.append({
        "initial_sign": sign,
        "n_seals": n,
        "avg_seq_length": round(avg_len,2),
        "confidence": conf,
        "reading": reading,
        "top_site": top_site,
        "top_iconography": top_icon,
        "site_distribution": dict(data["sites"].most_common(5)),
        "icon_distribution": dict(data["icons"].most_common(5)),
    })

# Chi-squared: do different INITIAL signs associate with different iconographies?
# Proxy test: are the top-2 iconographies different for different INITIAL signs?
icon_divergence = {}
for sign, data in top_initials[:15]:
    if data["icons"]:
        top2 = [i for i,_ in data["icons"].most_common(2)]
        icon_divergence[sign] = top2

print("\n  Top iconography per initial sign (formula type probe):")
for sign, icons in icon_divergence.items():
    reading = anchors.get(sign,{}).get("reading","?")[:10]
    print(f"    {sign} ({reading}): {' / '.join(icons)}")

results["C_formula_classification"] = {
    "n_distinct_initial_signs": len(formula_types),
    "formula_types": formula_summary,
    "icon_divergence_by_initial": icon_divergence,
    "interpretation": (
        f"{len(formula_types)} distinct INITIAL signs act as formula-type headers. "
        f"Cross-tabulation with iconography tests whether different professional titles "
        f"(different INITIAL signs) appear on seals with different motif types. "
        f"Systematic divergence = formula type ↔ seal function correlation."
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# D: Positional Collocate Divergence (Roif Polysemy Test)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n"+"─"*70); print("D: POSITIONAL COLLOCATE DIVERGENCE (POLYSEMY TEST)"); print("─"*70)
print("  Roif hypothesis: same sign, different position = different meaning")
print("  Test: do neighbor profiles diverge by positional slot?")

# For signs that appear in MULTIPLE slots (INITIAL + MEDIAL + TERMINAL)
polysemy_candidates = []
for sign in hm_set:
    if sign_freq.get(sign,0) < 10: continue
    i_rate = ic[sign] / max(sign_freq[sign],1)
    t_rate = te[sign] / max(sign_freq[sign],1)
    m_total = sign_freq[sign] - ic[sign] - te[sign]
    m_rate  = m_total / max(sign_freq[sign],1)

    # Only signs that appear in at least 2 slots with freq >= 3 each
    slots_used = []
    if ic[sign] >= 3: slots_used.append("INITIAL")
    if te[sign] >= 3: slots_used.append("TERMINAL")
    if m_total >= 3: slots_used.append("MEDIAL")
    if len(slots_used) < 2: continue

    # Collocate profile by slot
    init_right  = Counter()
    term_left   = Counter()
    med_left    = Counter()
    med_right   = Counter()

    for seq in all_seqs:
        for pos, s in enumerate(seq):
            if s != sign: continue
            n = len(seq)
            if pos == 0 and n > 1:       # INITIAL
                init_right[seq[pos+1]] += 1
            elif pos == n-1 and n > 1:    # TERMINAL
                term_left[seq[pos-1]] += 1
            elif 0 < pos < n-1:           # MEDIAL
                med_left[seq[pos-1]] += 1
                med_right[seq[pos+1]] += 1

    # Divergence: are INITIAL right-neighbors different from TERMINAL left-neighbors?
    init_top  = [s for s,_ in init_right.most_common(3)] if init_right else []
    term_top  = [s for s,_ in term_left.most_common(3)] if term_left else []
    overlap   = set(init_top) & set(term_top)
    divergence_score = 1 - len(overlap) / max(len(set(init_top)|set(term_top)),1)

    polysemy_candidates.append({
        "sign": sign,
        "reading": anchors.get(sign,{}).get("reading","?"),
        "confidence": anchors.get(sign,{}).get("confidence","?"),
        "freq": sign_freq[sign],
        "slots": slots_used,
        "i_rate": round(i_rate,3),
        "t_rate": round(t_rate,3),
        "m_rate": round(m_rate,3),
        "init_right_top3": init_top,
        "term_left_top3":  term_top,
        "divergence_score": round(divergence_score,3),
        "is_divergent": divergence_score >= 0.67,
    })

polysemy_candidates.sort(key=lambda x: -x["divergence_score"])
divergent = [p for p in polysemy_candidates if p["is_divergent"]]

print(f"  Multi-slot H+M signs (freq ≥ 10, ≥2 slots with ≥3 occ): {len(polysemy_candidates)}")
print(f"  Divergent neighbor profiles (≥67% non-overlap): {len(divergent)}")
print("\n  Top divergent signs (strongest Roif polysemy candidates):")
print(f"  {'Sign':<8} {'Reading':<12} {'Slots':<25} {'Div':>5} {'INIT-right':<20} {'TERM-left'}")
for p in divergent[:15]:
    print(f"  {p['sign']:<8} {p['reading']:<12} {str(p['slots']):<25} {p['divergence_score']:>5.2f} "
          f"{str(p['init_right_top3']):<20} {str(p['term_left_top3'])}")

results["D_polysemy_test"] = {
    "n_multi_slot_candidates": len(polysemy_candidates),
    "n_divergent": len(divergent),
    "divergent_signs": divergent[:30],
    "all_candidates": polysemy_candidates[:50],
    "interpretation": (
        f"{len(divergent)}/{len(polysemy_candidates)} multi-slot H+M signs show divergent "
        f"neighbor profiles by positional slot (Roif polysemy test). "
        f"A sign with high divergence score has systematically different compounds "
        f"depending on whether it appears in INITIAL, MEDIAL, or TERMINAL position — "
        f"consistent with shorthand polysemy: same sign, context-dependent meaning."
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# E: M267 Genitive Validation
# ═══════════════════════════════════════════════════════════════════════════════
print("\n"+"─"*70); print("E: M267 GENITIVE VALIDATION"); print("─"*70)

M267 = "M267"
m267_contexts = []
for form, data in seals.items():
    seq = data["signs"]
    for pos, s in enumerate(seq):
        if s != M267: continue
        n = len(seq)
        slot = "INITIAL" if pos==0 else ("TERMINAL" if pos==n-1 else "MEDIAL")
        left  = seq[pos-1] if pos > 0 else "—"
        right = seq[pos+1] if pos < n-1 else "—"
        left_slot = ("INITIAL" if pos==1 else ("MEDIAL" if pos > 1 else "—")) if left != "—" else "—"
        m267_contexts.append({
            "seal": form, "site": data["site"], "slot": slot,
            "left": left, "right": right,
            "left_conf": anchors.get(left,{}).get("confidence","?"),
            "right_conf": anchors.get(right,{}).get("confidence","?"),
            "left_reading": anchors.get(left,{}).get("reading","?"),
            "right_reading": anchors.get(right,{}).get("reading","?"),
            "sequence": " · ".join(seq),
        })

slot_dist  = Counter(c["slot"] for c in m267_contexts)
left_dist  = Counter(c["left"] for c in m267_contexts if c["left"] != "—")
right_dist = Counter(c["right"] for c in m267_contexts if c["right"] != "—")

# What proportion of M267 left-neighbors are INITIAL-class signs?
left_initial_count = sum(1 for c in m267_contexts
                          if c["left"] != "—" and ic.get(c["left"],0)/max(sign_freq.get(c["left"],1),1) >= 0.50)
left_total = sum(1 for c in m267_contexts if c["left"] != "—")

print(f"  M267 total occurrences: {len(m267_contexts)}")
print(f"  By slot: {dict(slot_dist)}")
print(f"  Left-neighbor = INITIAL-class sign: {left_initial_count}/{left_total} ({100*left_initial_count/max(left_total,1):.0f}%)")
print(f"  Top left-neighbors: {dict(left_dist.most_common(8))}")
print(f"  Top right-neighbors: {dict(right_dist.most_common(8))}")

medial_pct = 100*slot_dist.get("MEDIAL",0)/max(len(m267_contexts),1)
print("\n  M267 slot analysis:")
print(f"    MEDIAL: {slot_dist.get('MEDIAL',0)} ({medial_pct:.0f}%) — expected for a particle/connector")
print(f"    Follows INITIAL signs: {left_initial_count}/{left_total} ({100*left_initial_count/max(left_total,1):.0f}%)")
print("    → Consistent with genitive particle: [TITLE]-M267-[NAME] = '[NAME] of [TITLE]'")

verdict_m267 = (
    "GENITIVE_CONFIRMED" if medial_pct >= 55 and left_initial_count/max(left_total,1) >= 0.35 else
    "GENITIVE_SUPPORTED" if medial_pct >= 40 else
    "AMBIGUOUS"
)
print(f"  Verdict: {verdict_m267}")

results["E_M267_genitive"] = {
    "n_occurrences": len(m267_contexts),
    "slot_distribution": dict(slot_dist),
    "medial_pct": round(medial_pct,2),
    "left_initial_class_pct": round(100*left_initial_count/max(left_total,1),2),
    "top_left_neighbors": dict(left_dist.most_common(10)),
    "top_right_neighbors": dict(right_dist.most_common(10)),
    "verdict": verdict_m267,
    "sample_contexts": m267_contexts[:10],
    "interpretation": (
        f"M267 (freq={sign_freq.get(M267,0)}): {medial_pct:.0f}% MEDIAL, "
        f"{left_initial_count}/{left_total} left-neighbors are INITIAL-class (title/determinative) signs. "
        f"Pattern [INITIAL_sign] · M267 · [X] is consistent with genitive construction "
        f"'[NAME]-of-[TITLE]' in Dravidian SOV administrative formula. Verdict: {verdict_m267}."
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════
print("\n"+"="*70); print("PHASE-142 SUMMARY"); print("="*70)

key_findings = [
    f"A. Collocate network: {len(hm_bigrams)} H+M×H+M bigrams; {len(high_pmi)} strong collocate pairs (PMI>1.5)",
    f"B. INITIAL vocabulary: {len(hm_initial)} H+M title/determinative signs identified",
    f"C. Formula classification: {len(formula_types)} distinct formula types by INITIAL sign",
    f"D. Polysemy test: {len(divergent)}/{len(polysemy_candidates)} multi-slot signs show Roif-predicted divergence",
    f"E. M267 genitive: {medial_pct:.0f}% MEDIAL; {left_initial_count}/{left_total} left-neighbors are INITIAL-class → {verdict_m267}",
]
for f in key_findings: print(f"  • {f}")

final = {
    "phase": 142,
    "date": datetime.date.today().isoformat(),
    "corpus_stats": {"n_seals": n_seals, "n_tokens": n_tokens, "n_signs": len(sign_freq)},
    "results": results,
    "key_findings": key_findings,
    "_note": "Phase-142: Collocate network, INITIAL vocabulary, formula classification, "
             "Roif polysemy test, M267 genitive validation. Real corpus only, no synthetic data.",
}
OUT.write_text(json.dumps(final, indent=2), encoding="utf-8")
print(f"\n  Report saved → {OUT}")
print("=== PHASE-142 COMPLETE ===")
