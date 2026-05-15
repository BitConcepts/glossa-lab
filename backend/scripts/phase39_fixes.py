"""Phase-39: Fix Phase-38 T2/T3 imports and re-run with correct data.

Fixes:
  T2 Sangam LM: use get_corpus_text() directly (no INSCRIPTIONS import needed).
                Syllabify Tamil words from running corpus text. True Sangam bigrams.
  T3 Meroitic:  use get_line_inscriptions(encoded=False) for full phonetic sequences.
  T3 Coptic:    build bigrams from get_coptic_symbols() flat list (sliding window).
  Both:         equalized to Sanskrit size (424 syl / 651 bigrams).
"""
from __future__ import annotations
import json, math, random, re, sys, time, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
REPORTS = ROOT / "reports"
BACKEND_REPORTS = ROOT / "backend" / "reports"
DATA = ROOT / "backend" / "glossa_lab" / "data"
SMOOTHING = math.log(1e-8)

# ── Helpers ───────────────────────────────────────────────────────────────────
_D = {"ā":"a","ī":"i","ū":"u","ṉ":"n","ṟ":"r","ḷ":"l","ḻ":"l","ṛ":"r",
      "ṭ":"t","ḍ":"d","ṅ":"n","ṇ":"n","ñ":"n","ś":"s","ṣ":"s","ḥ":"h"}
def _sd(s):
    o=[]
    for c in unicodedata.normalize("NFD",s):
        p=_D.get(c)
        if p: o.append(p)
        elif unicodedata.category(c)!="Mn": o.append(c)
    return "".join(o)
def _sylls(w):
    V=set("aeiou"); C=set("bcdfghjklmnpqrstvwxyz")
    r=[]; i=0; cur=""
    while i<len(w):
        c=w[i]; cur+=c
        if c in V:
            if i+1<len(w) and w[i+1] in C and (i+2>=len(w) or w[i+2] in V): i+=1; cur+=w[i]
            r.append(cur); cur=""
        elif len(cur)>=3: r.append(cur); cur=""
        i+=1
    if cur:
        if r: r[-1]+=cur
        else: r.append(cur)
    return [s for s in r if s]
def _to_syl(reading, vocab):
    reading=reading.split("/")[0].strip()
    reading=re.sub(r"\(.*?\)","",reading).strip().rstrip("?")
    if re.match(r"(term|med|init|ctx|role|boundary|suffix|uncertain)[-:]?",reading.lower()): return None
    if not reading or reading in("?","-") or "uncertain" in reading.lower(): return None
    clean=_sd(reading); clean=re.sub(r"[^a-z]","",clean.lower())
    if not clean: return None
    if clean in vocab: return clean
    for s in _sylls(clean):
        if s in vocab: return s
    for l in(2,3,1):
        if len(clean)>=l:
            c=clean[:l]
            if c in vocab: return c
    return clean[:3] if len(clean)>3 else clean

def load_corpus():
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    return get_corpus_inscriptions(), Counter(get_corpus_symbols())

def load_lm(name):
    raw=json.loads((DATA/name).read_text("utf-8"))
    braw=raw.get("bigrams",raw.get("bigram_freq",{}))
    bigs={}
    for k,lp in braw.items():
        ps=k.split("|") if "|" in k else k.split(",") if "," in k else [k]
        if len(ps)==2:
            try: bigs[(ps[0].strip(),ps[1].strip())]=float(lp)
            except: pass
    freq=Counter()
    for(a,b) in bigs: freq[a]+=1; freq[b]+=1
    ranked=raw.get("vocab",[]) or [s for s,_ in freq.most_common()]
    return bigs, ranked

def score(m, inscs, bigs):
    t=0.0
    for insc in inscs:
        for i in range(len(insc)-1):
            a=m.get(insc[i]); b=m.get(insc[i+1])
            if a and b: t+=bigs.get((a,b),SMOOTHING)
    return t

def run_sa(fixed, free, vocab, inscs, bigs, n=30_000, seed=42):
    rng=random.Random(seed)
    if not vocab: return dict(fixed),score(fixed,inscs,bigs)
    ft=[v for v in vocab if v not in fixed.values()]
    while len(ft)<len(free): ft.append(rng.choice(vocab))
    rng.shuffle(ft)
    m=dict(fixed)
    for i,s in enumerate(free): m[s]=ft[i%len(ft)]
    cur=score(m,inscs,bigs); best=dict(m); bs=cur
    T0,T1=2.0,0.01
    for it in range(n):
        T=T0*((T1/T0)**(it/n))
        if len(free)<2: break
        i,j=rng.sample(range(len(free)),2)
        si,sj=free[i],free[j]; vi,vj=m[si],m[sj]
        m[si],m[sj]=vj,vi; nw=score(m,inscs,bigs); d=nw-cur
        if d>0 or rng.random()<math.exp(d/max(T,1e-10)):
            cur=nw
            if nw>bs: bs=nw; best=dict(m)
        else: m[si],m[sj]=vi,vj
    return best,bs

def null_test(m, inscs, bigs, n=500, seed=99):
    rng=random.Random(seed); obs=score(m,inscs,bigs)
    ks=list(m.keys()); vs=list(m.values()); ns=[]
    for _ in range(n):
        sh=vs[:]; rng.shuffle(sh)
        ns.append(score(dict(zip(ks,sh)),inscs,bigs))
    nm=sum(ns)/len(ns); nstd=math.sqrt(sum((s-nm)**2 for s in ns)/len(ns))
    z=(obs-nm)/nstd if nstd else 0.0
    p=sum(1 for s in ns if s>=obs)/n
    return nm,nstd,z,p

def build_anchors(vocab):
    anchors={}
    pp=json.loads((DATA/"parpola_phonemes.json").read_text("utf-8"))
    for sid,info in pp.get("phoneme_map",{}).items():
        if not isinstance(info,dict): continue
        pv=info.get("phoneme",info.get("phoneme_value",""))
        if pv and info.get("confidence","low") in("high","medium") and "?" not in pv:
            s=_to_syl(pv,vocab)
            if s:
                anchors[sid]=s
                if sid.isdigit(): anchors[sid.zfill(3)]=s
    fa_p=BACKEND_REPORTS/"INDUS_FINAL_ANCHORS.json"
    if fa_p.exists():
        for m_id,info in json.loads(fa_p.read_text("utf-8")).get("anchors",{}).items():
            if info.get("confidence") not in("HIGH","MEDIUM"): continue
            r=info.get("reading","")
            if "?" in r: continue
            s=_to_syl(r,vocab)
            if not s: continue
            anchors[m_id]=s
            if m_id.startswith("M") and m_id[1:].isdigit(): anchors[m_id[1:]]=s
    xw_p=DATA/"mahadevan_parpola_crosswalk_v2.json"
    if xw_p.exists():
        for m_id,entry in json.loads(xw_p.read_text("utf-8")).get("crosswalk",{}).items():
            ph=entry.get("phoneme",""); conf=entry.get("confidence","LOW")
            if conf.upper() not in("HIGH","MEDIUM") or "?" in ph: continue
            s=_to_syl(ph,vocab)
            if not s: continue
            anchors[m_id]=s
            bare=m_id[1:] if m_id.startswith("M") and m_id[1:].isdigit() else m_id
            if bare not in anchors: anchors[bare]=s
    return anchors

def equalized_lm(name, n_syl=424, n_big=651):
    bigs_full,ranked_full=load_lm(name)
    ranked_eq=ranked_full[:n_syl]
    vocab_eq=set(ranked_eq)
    bigs_all={(a,b):lp for(a,b),lp in bigs_full.items() if a in vocab_eq and b in vocab_eq}
    bigs_eq=dict(sorted(bigs_all.items(),key=lambda x:-x[1])[:n_big])
    return bigs_eq,ranked_eq

def build_lm_from_tokens(tokens: list[str], n_syl: int, n_big: int):
    """Build equalized LM from a flat list of syllable tokens."""
    uni: Counter = Counter(tokens)
    bg: Counter = Counter()
    for i in range(len(tokens)-1):
        bg[(tokens[i],tokens[i+1])]+=1
    total=sum(bg.values())
    if total==0: return {},{}, []
    bigs={(a,b):math.log(c/total) for(a,b),c in bg.items()}
    ranked=[s for s,_ in uni.most_common()]
    # equalize
    ranked_eq=ranked[:n_syl]
    vocab_eq=set(ranked_eq)
    bigs_all={(a,b):lp for(a,b),lp in bigs.items() if a in vocab_eq and b in vocab_eq}
    bigs_eq=dict(sorted(bigs_all.items(),key=lambda x:-x[1])[:n_big])
    return bigs_eq,ranked_eq,ranked

def run_lang(label, bigs, vocab, inscs, sf, n_seeds=5, n_iters=30_000):
    cipher=[s for s,c in sf.items() if c>=3]
    anchors=build_anchors(set(vocab))
    fixed={s:r for s,r in anchors.items() if s in cipher and r in set(vocab)}
    free=[s for s in cipher if s not in fixed]
    print(f"  {label}: anchors={len(fixed)}, free={len(free)}, vocab={len(vocab)}, bigrams={len(bigs)}")
    if len(free)<2 or not bigs:
        print(f"  {label}: insufficient data — skipping")
        return None
    results=[]
    for seed in range(n_seeds):
        m,s=run_sa(fixed,free,vocab,inscs,bigs,n_iters,seed)
        results.append((s,m)); print(f"    Seed {seed}: {s:.1f}")
    bs,bm=max(results,key=lambda x:x[0])
    nm,nstd,z,p=null_test(bm,inscs,bigs,n=500)
    lift=(bs-nm)/max(1,len(inscs))
    print(f"  {label}: Z={z:.2f}, p={p:.4f}, lift={lift:.4f}")
    return {"z":round(z,3),"p":round(p,4),"nll_lift":round(lift,4),"significant":p<0.05,
            "n_anchors":len(fixed),"n_bigrams":len(bigs),"n_vocab":len(vocab),
            "seed_scores":[round(s,1) for s,_ in results]}

# ════════════════════════════════════════════════════════════════════════════════
print("="*65); print("Phase-39: Loading shared data...")
inscs_raw, sf_raw = load_corpus()
skt_b, skt_r = load_lm("sanskrit_syllable_lm.json")
N_SYL, N_BIG = len(skt_r), len(skt_b)  # 424, 651
drav_b_eq, drav_r_eq = equalized_lm("dravidian_syllable_lm.json", N_SYL, N_BIG)
print(f"M77: {len(inscs_raw)} inscriptions | Target: {N_SYL} syl / {N_BIG} bigrams")

# ════════════════════════════════════════════════════════════════════════════════
# T2 FIX: TRUE Sangam LM from get_corpus_text() syllabification
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65); print("T2 FIX: True Sangam syllable LM from corpus text")
t0=time.time()

from glossa_lab.data.dravidian import get_corpus_text  # correct: no INSCRIPTIONS
corpus_text = get_corpus_text()
sangam_tokens: list[str] = []
words = re.findall(r"[a-z\u0b00-\u0bff\u0900-\u097f]+", corpus_text.lower())
for word in words:
    clean=_sd(word); clean=re.sub(r"[^a-z]","",clean)
    if 2<=len(clean)<=20:
        sylls=_sylls(clean)
        sangam_tokens.extend(sylls if sylls else [clean[:3]])

print(f"  Corpus text: {len(words)} words -> {len(sangam_tokens)} syllable tokens")

# Add bigrams from the Tamil-Brahmi clean LM (real inscriptions)
try:
    tb_b, tb_r = load_lm("mahadevan_2003_tb_lm_clean.json")
    print(f"  Added TB clean LM: {len(tb_r)} syllables, {len(tb_b)} bigrams")
except Exception as e:
    tb_b, tb_r = {}, []
    print(f"  TB LM unavailable: {e}")

# Build Sangam LM from tokens
sangam_b_raw, sangam_r_raw, _ = build_lm_from_tokens(sangam_tokens, N_SYL*2, N_BIG*4)
# Blend with TB bigrams
for (a,b),lp in tb_b.items():
    if (a,b) not in sangam_b_raw:
        sangam_b_raw[(a,b)]=lp
    else:
        sangam_b_raw[(a,b)]=0.7*sangam_b_raw[(a,b)]+0.3*lp
# Equalize
sangam_uni=Counter(sangam_tokens)
sangam_r_all=[s for s,_ in sangam_uni.most_common()]
sangam_r_eq=sangam_r_all[:N_SYL]; sangam_vocab_eq=set(sangam_r_eq)
sangam_b_filt={(a,b):lp for(a,b),lp in sangam_b_raw.items() if a in sangam_vocab_eq and b in sangam_vocab_eq}
sangam_b_eq=dict(sorted(sangam_b_filt.items(),key=lambda x:-x[1])[:N_BIG])
print(f"  Sangam LM (equalized): {len(sangam_r_eq)} syl, {len(sangam_b_eq)} bigrams (raw {len(sangam_b_raw)})")

r_sang = run_lang("Sangam_Tamil", sangam_b_eq, sangam_r_eq, inscs_raw, sf_raw)
r_drav = run_lang("Dravidian_DEDR", drav_b_eq, drav_r_eq, inscs_raw, sf_raw)
r_skt  = run_lang("Sanskrit", skt_b, skt_r, inscs_raw, sf_raw)

t2_out={
    "experiment":"Phase-39 T2 FIX: True Sangam LM",
    "sangam_tokens": len(sangam_tokens), "sangam_words": len(words),
    "sangam_raw_bigrams": len(sangam_b_raw),
    "sangam_equalized_bigrams": len(sangam_b_eq),
    "sangam": r_sang, "dravidian_dedr": r_drav, "sanskrit": r_skt,
    "sangam_wins_vs_sanskrit": (r_sang or {}).get("nll_lift",0)>(r_skt or {}).get("nll_lift",0),
    "dravidian_wins_vs_sanskrit": (r_drav or {}).get("nll_lift",0)>(r_skt or {}).get("nll_lift",0),
    "verdict":(
        f"Sangam lift={(r_sang or {}).get('nll_lift','?')}, "
        f"DEDR lift={(r_drav or {}).get('nll_lift','?')}, "
        f"Sanskrit lift={(r_skt or {}).get('nll_lift','?')}. "
        f"Sangam wins: {(r_sang or {}).get('nll_lift',0)>(r_skt or {}).get('nll_lift',0)}. "
        f"Runtime={time.time()-t0:.0f}s."
    ),
    "_citation":{"primary":["A.1","E.1","A.12"],"phase":"Phase-39-T2"},
}
(REPORTS/"phase39_t2_true_sangam_lm.json").write_text(json.dumps(t2_out,indent=2,ensure_ascii=False),"utf-8")
print(f"Saved phase39_t2_true_sangam_lm.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# T3 FIX: Meroitic (line-level) + Coptic (running tokens) + full ranking
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65); print("T3 FIX: Multi-language falsification (correct imports)")
t0=time.time()

multi_results={}
multi_results["dravidian_sangam"] = r_sang or {}
multi_results["dravidian_dedr"]   = r_drav or {}
multi_results["sanskrit"]         = r_skt  or {}

# Meroitic — use get_line_inscriptions(encoded=False) for full phonetic sequences
print("\n  Meroitic (line-level, phonetic):")
from glossa_lab.data.meroitic import get_line_inscriptions as get_mer_lines
mer_lines = get_mer_lines(encoded=False)  # phonetic values (a,t,n,r,...)
print(f"  Meroitic lines: {len(mer_lines)}, avg len={sum(len(l) for l in mer_lines)/max(len(mer_lines),1):.1f}")
mer_flat=[tok for line in mer_lines for tok in line]
mer_b_eq, mer_r_eq, _ = build_lm_from_tokens(mer_flat, N_SYL, N_BIG)
print(f"  Meroitic LM: {len(mer_r_eq)} syl, {len(mer_b_eq)} bigrams")
r_mer = run_lang("Meroitic_NiloSaharan", mer_b_eq, mer_r_eq, inscs_raw, sf_raw)
multi_results["meroitic_nilosaharan"] = r_mer or {}

# Coptic — use get_coptic_symbols() as running text
print("\n  Coptic (running symbols):")
from glossa_lab.data.meroitic import get_coptic_symbols
cop_flat = get_coptic_symbols()
print(f"  Coptic symbols: {len(cop_flat)}, unique: {len(set(cop_flat))}")
cop_b_eq, cop_r_eq, _ = build_lm_from_tokens(cop_flat, N_SYL, N_BIG)
print(f"  Coptic LM: {len(cop_r_eq)} syl, {len(cop_b_eq)} bigrams")
r_cop = run_lang("Coptic_AfroAsiatic", cop_b_eq, cop_r_eq, inscs_raw, sf_raw)
multi_results["coptic_afroasiatic"] = r_cop or {}

# Sumerian (ePSD2 running bigrams if available)
print("\n  Sumerian (ePSD2/CDLI):")
try:
    from glossa_lab.data.sumerian_ur3 import get_corpus_symbols as get_sum_syms, get_corpus_inscriptions as get_sum_inscs
    sum_flat = get_sum_syms()
    print(f"  Sumerian tokens: {len(sum_flat)}, unique: {len(set(sum_flat))}")
    sum_b_eq,sum_r_eq,_=build_lm_from_tokens(sum_flat,N_SYL,N_BIG)
    print(f"  Sumerian LM: {len(sum_r_eq)} syl, {len(sum_b_eq)} bigrams")
    r_sum=run_lang("Sumerian_UR3",sum_b_eq,sum_r_eq,inscs_raw,sf_raw)
    multi_results["sumerian_ur3"]=r_sum or {}
except Exception as e:
    print(f"  Sumerian error: {e}")
    multi_results["sumerian_ur3"]={"error":str(e)}

# Rank all by lift
ranked=sorted([(lang,v.get("nll_lift",0)) for lang,v in multi_results.items() if "error" not in v and v],
              key=lambda x:-x[1])
print("\n  === Final language ranking by NLL lift/inscription ===")
for rank,(lang,lift) in enumerate(ranked,1):
    r=multi_results.get(lang,{}); z=r.get("z","?"); p=r.get("p","?")
    sig="*" if r.get("significant") else " "
    print(f"  {rank:2d}. {lang:35s} lift={lift:.4f}  Z={z}  {sig}")

# Check if both Dravidian variants beat all non-Dravidian
drav_lifts=[multi_results.get(k,{}).get("nll_lift",0) for k in("dravidian_sangam","dravidian_dedr")]
non_drav_lifts=[v.get("nll_lift",0) for k,v in multi_results.items()
                if "dravidian" not in k and "error" not in v and v]
drav_beats_all = drav_lifts and non_drav_lifts and all(max(drav_lifts)>l for l in non_drav_lifts)
print(f"\n  Max Dravidian lift: {max(drav_lifts):.4f} vs max non-Dravidian: {max(non_drav_lifts) if non_drav_lifts else 0:.4f}")
print(f"  Dravidian beats ALL non-Dravidian: {drav_beats_all}")

t3_out={
    "experiment":"Phase-39 T3 FIX: Multi-language falsification (corrected imports)",
    "languages":multi_results,"ranking":ranked,
    "dravidian_beats_all_non_dravidian":drav_beats_all,
    "max_dravidian_lift":round(max(drav_lifts),4) if drav_lifts else 0,
    "max_non_dravidian_lift":round(max(non_drav_lifts),4) if non_drav_lifts else 0,
    "verdict":(
        f"Language ranking: {', '.join(f'{l}={v:.3f}' for l,v in ranked[:6])}. "
        f"Dravidian beats ALL non-Dravidian: {drav_beats_all}. "
        f"Runtime={time.time()-t0:.0f}s."
    ),
    "_citation":{"primary":["A.1","E.1"],"phase":"Phase-39-T3"},
}
(REPORTS/"phase39_t3_multilang_fixed.json").write_text(json.dumps(t3_out,indent=2,ensure_ascii=False),"utf-8")
print(f"Saved phase39_t3_multilang_fixed.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65); print("Phase-39 experiments complete:")
for fn in ["phase39_t2_true_sangam_lm.json","phase39_t3_multilang_fixed.json"]:
    p=REPORTS/fn; sz=p.stat().st_size if p.exists() else 0
    print(f"  {'OK' if p.exists() else 'MISSING'} {fn} ({sz//1024}KB)")

print(f"\nT2: Sangam lift={(r_sang or {}).get('nll_lift','?')} | DEDR={(r_drav or {}).get('nll_lift','?')} | Sanskrit={(r_skt or {}).get('nll_lift','?')}")
print(f"T3: ranking top-4: {ranked[:4]}")
print(f"    Dravidian beats all non-Dravidian: {drav_beats_all}")
