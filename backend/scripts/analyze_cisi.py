"""Deep analysis of CISI corpus: positional profiles, bigrams, top signs."""
import sys, json
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent))
from glossa_lab.experiment_graph import ATOMIC_NODES

corpus_r = ATOMIC_NODES["BuiltinCorpus"].fn({}, {"corpus": "indus_cisi"})
seqs = corpus_r["sequences"]
n_tokens = corpus_r["total_tokens"]
n_signs = corpus_r["distinct_symbols"]
print(f"CISI: {len(seqs)} inscriptions, {n_tokens} tokens, {n_signs} distinct signs")

prof_r = ATOMIC_NODES["PositionalProfiler"].fn({"sequences": seqs}, {"min_count": 3})
profiles_list = prof_r.get("profiles", [])  # list of {symbol, count, t_rate, i_rate, m_rate, pos_class}
print(f"Profile summary: {prof_r.get('class_summary', {})}")

# Index by symbol for fast lookup
profiles = {p["symbol"]: {"terminal_rate": p["t_rate"], "initial_rate": p["i_rate"],
                           "medial_rate": p["m_rate"], "count": p["count"],
                           "pos_class": p["pos_class"]} for p in profiles_list}

# Sign breakdown by positional class
terminal = [(p["symbol"], p) for p in profiles_list if p["pos_class"] == "TERMINAL"]
initial  = [(p["symbol"], p) for p in profiles_list if p["pos_class"] == "INITIAL"]
medial   = [(p["symbol"], p) for p in profiles_list if p["pos_class"] == "MEDIAL"]
terminal.sort(key=lambda x: -x[1]["t_rate"])
initial.sort(key=lambda x: -x[1]["i_rate"])

print(f"\nTERMINAL signs (t_rate>=0.60): {len(terminal)}")
for s, d in terminal:
    print(f"  {s}: T={d['t_rate']:.2f} I={d['i_rate']:.2f} M={d['m_rate']:.2f} n={d['count']}")

print(f"\nINITIAL signs (i_rate>=0.50): {len(initial)}")
for s, d in initial[:12]:
    print(f"  {s}: T={d['t_rate']:.2f} I={d['i_rate']:.2f} M={d['m_rate']:.2f} n={d['count']}")
bigrams = Counter()
for seq in seqs:
    for i in range(len(seq)-1):
        bigrams[(seq[i], seq[i+1])] += 1

trigrams = Counter()
for seq in seqs:
    for i in range(len(seq)-2):
        trigrams[(seq[i], seq[i+1], seq[i+2])] += 1

def role(s):
    p = profiles.get(s, {})
    if p.get("initial_rate",0) > 0.45 or p.get("pos_class")=="INITIAL": return "I"
    if p.get("terminal_rate",0) > 0.45 or p.get("pos_class")=="TERMINAL": return "T"
    return "M"

print(f"\nTop 25 bigrams (role annotation: I=initial, M=medial, T=terminal):")
for (a,b), n in bigrams.most_common(25):
    print(f"  {a}({role(a)})->{b}({role(b)})  n={n}")

print(f"\nTop 15 trigrams:")
for (a,b,c), n in trigrams.most_common(15):
    print(f"  {a}({role(a)})->{b}({role(b)})->{c}({role(c)})  n={n}")

# Context for each terminal sign: what precedes it?
print(f"\nContext of top TERMINAL signs (what immediately precedes them?):")
for s, d in terminal[:7]:
    pre = Counter()
    for seq in seqs:
        for i in range(1, len(seq)):
            if seq[i] == s:
                pre[seq[i-1]] += 1
    top_pre = pre.most_common(5)
    t_rate = d.get('t_rate', d.get('terminal_rate', 0))
    print(f"  {s} (T={t_rate:.2f}, n={d['count']}): preceded by {top_pre}")

# Overall sign frequencies
freq = Counter(sign for seq in seqs for sign in seq)
print(f"\nTop 20 most frequent signs:")
for s, n in freq.most_common(20):
    p = profiles.get(s, {})
    print(f"  {s}: n={n} T={p.get('terminal_rate',0):.2f} I={p.get('initial_rate',0):.2f} M={p.get('medial_rate',0):.2f} cls={p.get('pos_class','')}")

# Save full analysis
out = {
    "n_inscriptions": len(seqs),
    "n_tokens": n_tokens,
    "n_distinct": n_signs,
    "terminal_signs": [(s, {k: round(v,3) if isinstance(v,float) else v
                            for k,v in d.items()}) for s,d in terminal],
    "initial_signs":  [(s, {k: round(v,3) if isinstance(v,float) else v
                            for k,v in d.items()}) for s,d in initial],
    "top_bigrams":    [{"a": a, "b": b, "role_a": role(a), "role_b": role(b), "count": n}
                       for (a,b),n in bigrams.most_common(40)],
    "top_trigrams":   [{"a": a, "b": b, "c": c, "count": n}
                       for (a,b,c),n in trigrams.most_common(20)],
    "top_signs":      [{"sign": s, "count": n, **profiles.get(s,{})}
                       for s,n in freq.most_common(30)],
}
Path("C:/Users/trist/Development/BitConcepts/glossa-lab/reports/cisi_deep_analysis.json").write_text(
    json.dumps(out, indent=2, default=str))
print("\nSaved: reports/cisi_deep_analysis.json")
