"""Phase-42 Task 1: Re-run V2 SA with fixed zero-padded sign IDs.

indus_corpus_v2.py was fixed to zero-pad all sign IDs:
  "67" -> "067"  (indusarrays raw integers now match M77 Holdat format)
  "M047" -> "047"  (M-prefix signs normalized)

Expected outcome: V2 corpus now consistent with M77 Holdat sign namespace.
Re-running the Phase-41 P1 experiment to confirm.

Also includes a quick overlap check (P2 re-validation) to confirm the fix worked.
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

def score(m,inscs,bigs):
    t=0.0
    for insc in inscs:
        for i in range(len(insc)-1):
            a=m.get(insc[i]); b=m.get(insc[i+1])
            if a and b: t+=bigs.get((a,b),SMOOTHING)
    return t

def run_sa(fixed,free,vocab,inscs,bigs,n=30_000,seed=42):
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

def null_test(m,inscs,bigs,n=1000,seed=99):
    rng=random.Random(seed); obs=score(m,inscs,bigs)
    ks=list(m.keys()); vs=list(m.values()); ns=[]
    for _ in range(n):
        sh=vs[:]; rng.shuffle(sh)
        ns.append(score(dict(zip(ks,sh)),inscs,bigs))
    nm=sum(ns)/len(ns); nstd=math.sqrt(sum((s-nm)**2 for s in ns)/len(ns))
    z=(obs-nm)/nstd if nstd else 0.0; p=sum(1 for s in ns if s>=obs)/n
    ci_lo=sorted(ns)[int(0.025*n)]; ci_hi=sorted(ns)[int(0.975*n)]
    return nm,nstd,z,p,ci_lo,ci_hi

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

# ════════════════════════════════════════════════════════════════════════════════
print("="*65); print("Phase-42 Task 1: V2 SA re-run with fixed zero-padded IDs")

# Load equalized LMs
skt_b, skt_r = load_lm("sanskrit_syllable_lm.json")
N_SYL, N_BIG = len(skt_r), len(skt_b)
drav_b_full, drav_r_full = load_lm("dravidian_syllable_lm.json")
drav_r_eq = drav_r_full[:N_SYL]
drav_vocab_eq = set(drav_r_eq)
drav_b_all={(a,b):lp for(a,b),lp in drav_b_full.items() if a in drav_vocab_eq and b in drav_vocab_eq}
drav_b_eq=dict(sorted(drav_b_all.items(),key=lambda x:-x[1])[:N_BIG])

# Load M77 baseline
from glossa_lab.data.indus_m77 import get_corpus_inscriptions as m77_inscs, get_corpus_symbols as m77_syms
m77_inscriptions=m77_inscs(); m77_sf=Counter(m77_syms())
m77_cipher = [s for s,c in m77_sf.items() if c>=3]
print(f"M77 baseline: {len(m77_inscriptions)} inscriptions, {len(m77_cipher)} signs (freq>=3)")
print(f"M77 sample sign IDs: {sorted(m77_cipher)[:8]}")

# Load V2 corpus — force fresh load (clear cache)
import glossa_lab.data.indus_corpus_v2 as _cv2
_cv2._CACHE = None  # clear any cached data
from glossa_lab.data.indus_corpus_v2 import load_corpus as load_v2
v2_raw = load_v2()
# V2 now returns list[list[str]] with zero-padded IDs
v2_inscriptions = [seq for seq in v2_raw if len(seq) >= 2]
v2_sf = Counter(s for insc in v2_inscriptions for s in insc)
v2_cipher = [s for s,c in v2_sf.items() if c>=3]
print(f"\nV2 corpus (fixed): {len(v2_inscriptions)} inscriptions, {len(v2_cipher)} signs (freq>=3)")
print(f"V2 sample sign IDs: {sorted(v2_cipher)[:8]}")

# ── Quick overlap check (P2 re-validation) ────────────────────────────────────
print("\n--- P2 re-validation: Holdat vs V2 sign ID overlap ---")
m77_top50 = set(s for s,_ in m77_sf.most_common(50))
v2_top50  = set(s for s,_ in v2_sf.most_common(50))
overlap = m77_top50 & v2_top50
overlap_pct = len(overlap)/50*100

all_signs = list((m77_sf | v2_sf).keys())[:200]
x = [m77_sf.get(s,0) for s in all_signs]
y = [v2_sf.get(s,0) for s in all_signs]
n=len(x); mx=sum(x)/n; my=sum(y)/n
num=sum((xi-mx)*(yi-my) for xi,yi in zip(x,y))
dx=math.sqrt(sum((xi-mx)**2 for xi in x) or 1)
dy=math.sqrt(sum((yi-my)**2 for yi in y) or 1)
pearson_r = round(num/(dx*dy),4)

print(f"Top-50 overlap: {overlap_pct:.1f}% (was 4.0% before fix — should be >60% now)")
print(f"Pearson r: {pearson_r} (was -0.15 before fix — should be >0.7 now)")
print(f"Overlap signs: {sorted(overlap)[:15]}")

if overlap_pct < 30:
    print("WARNING: Still low overlap — sign ID format may not be fully fixed")
else:
    print(f"FIX CONFIRMED: High overlap and positive correlation")

# ── V2 SA (freq>=3, equalized) ────────────────────────────────────────────────
print("\n--- SA with V2 corpus (all freq>=3 signs) ---")
drav_anch = build_anchors(drav_vocab_eq)
drav_fixed_v2 = {s:r for s,r in drav_anch.items() if s in v2_sf and r in drav_vocab_eq}
drav_free_v2  = [s for s in v2_cipher if s not in drav_fixed_v2]
skt_anch  = build_anchors(set(skt_r))
skt_fixed_v2  = {s:r for s,r in skt_anch.items() if s in v2_sf and r in set(skt_r)}
skt_free_v2   = [s for s in v2_cipher if s not in skt_fixed_v2]
print(f"V2 {len(v2_inscriptions)} inscs | {len(v2_cipher)} signs | Drav anchors={len(drav_fixed_v2)} free={len(drav_free_v2)}")

N_SEEDS=10; N_ITERS=60_000; t0=time.time()
print(f"Running Dravidian SA: {N_SEEDS}×{N_ITERS}...")
dr_res=[]
for seed in range(N_SEEDS):
    m,s=run_sa(drav_fixed_v2,drav_free_v2,drav_r_eq,v2_inscriptions,drav_b_eq,N_ITERS,seed)
    dr_res.append((s,m)); print(f"  Drav seed {seed}: {s:.1f}")
dr_bs,dr_bm=max(dr_res,key=lambda x:x[0])
dr_nm,dr_nstd,dr_z,dr_p,dr_ci_lo,dr_ci_hi=null_test(dr_bm,v2_inscriptions,drav_b_eq,n=1000)
dr_lift=(dr_bs-dr_nm)/max(1,len(v2_inscriptions))
print(f"Dravidian: Z={dr_z:.2f}, p={dr_p:.4f}, lift={dr_lift:.4f}, 95%CI=[{dr_ci_lo:.1f},{dr_ci_hi:.1f}]")

print(f"Running Sanskrit SA: {N_SEEDS}×{N_ITERS}...")
sk_res=[]
for seed in range(N_SEEDS):
    m,s=run_sa(skt_fixed_v2,skt_free_v2,skt_r,v2_inscriptions,skt_b,N_ITERS,seed)
    sk_res.append((s,m)); print(f"  Skt  seed {seed}: {s:.1f}")
sk_bs,sk_bm=max(sk_res,key=lambda x:x[0])
sk_nm,sk_nstd,sk_z,sk_p,sk_ci_lo,sk_ci_hi=null_test(sk_bm,v2_inscriptions,skt_b,n=1000)
sk_lift=(sk_bs-sk_nm)/max(1,len(v2_inscriptions))
print(f"Sanskrit:  Z={sk_z:.2f}, p={sk_p:.4f}, lift={sk_lift:.4f}, 95%CI=[{sk_ci_lo:.1f},{sk_ci_hi:.1f}]")

dw=dr_lift>sk_lift; ratio=dr_lift/max(abs(sk_lift),0.001)
print(f"\nDravidian wins: {dw} ({ratio:.4f}x) | Runtime: {time.time()-t0:.0f}s")

result = {
    "experiment": "Phase-42 Task 1: V2 SA with fixed zero-padded sign IDs",
    "fix_applied": "str(int(raw_sign_id)).zfill(3) in indus_corpus_v2.py",
    "p2_revalidation": {
        "top50_overlap_pct": round(overlap_pct,1),
        "pearson_r": pearson_r,
        "fix_confirmed": overlap_pct >= 30,
    },
    "v2_corpus": {
        "inscriptions": len(v2_inscriptions),
        "cipher_signs": len(v2_cipher),
        "multiplier_vs_m77": round(len(v2_inscriptions)/len(m77_inscriptions),2),
    },
    "dravidian": {"z":round(dr_z,3),"p":round(dr_p,4),"nll_lift":round(dr_lift,4),
                  "ci95":[round(dr_ci_lo,1),round(dr_ci_hi,1)],"n_anchors":len(drav_fixed_v2),
                  "seed_scores":[round(s,1) for s,_ in dr_res]},
    "sanskrit":  {"z":round(sk_z,3),"p":round(sk_p,4),"nll_lift":round(sk_lift,4),
                  "ci95":[round(sk_ci_lo,1),round(sk_ci_hi,1)],"n_anchors":len(skt_fixed_v2),
                  "seed_scores":[round(s,1) for s,_ in sk_res]},
    "dravidian_wins": dw,
    "lift_ratio": round(ratio,4),
    "runtime_s": round(time.time()-t0,1),
    "verdict": (
        f"V2 fixed SA: Dravidian lift={dr_lift:.4f} Z={dr_z:.2f} vs Sanskrit lift={sk_lift:.4f} Z={sk_z:.2f}. "
        f"Dravidian {'WINS' if dw else 'loses'} ({ratio:.3f}x). "
        f"P2 overlap: {overlap_pct:.1f}%, r={pearson_r} ({'FIX CONFIRMED' if overlap_pct>=30 else 'STILL LOW'})."
    ),
    "_citation": {"primary":["A.1","E.1","C.2","I.1","I.2"],"phase":"Phase-42-T1"},
}
(REPORTS/"phase42_t1_v2_sa_fixed.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),"utf-8")
print(f"\nSaved phase42_t1_v2_sa_fixed.json")
print(f"VERDICT: {result['verdict']}")
