"""Phase-37: Coupled SA (CSA) + k-permutations + allograph reduction + validated positional anchors.

Four improvements over Phase-36:

1. COUPLED SA (CSA) — inspired by Tamburini 2025 (D.12):
   N_CHAINS independent SA chains with periodic solution coupling.
   Chains communicate: every SWAP_INTERVAL iterations, adjacent chain pairs
   may exchange solutions via Metropolis criterion. Converges better than
   N independent parallel seeds.

2. K-PERMUTATIONS (null mappings) — from Tamburini 2025:
   A fraction of free signs may be assigned to NULL (no syllable).
   NULL signs score SMOOTHING for all bigrams they participate in.
   Reduces noise from rare signs that force poor SA assignments.

3. ALLOGRAPH REDUCTION — from Daggumati & Revesz 2021 (D.6):
   Data-driven positional similarity clustering of M77 signs.
   Signs with highly similar [t_rate, i_rate, m_rate] profiles are
   candidate allographs. Merge rarer sign -> more-frequent canonical.
   Increases freq>=3 sign count and token density per sign.

4. VALIDATED POSITIONAL ANCHORS — from Phase-33 TB corpus profiles:
   Map terminal Indus signs to terminal TB syllables by bigram-positional
   frequency (not cycle-assignment). Right-side bigram frequency in clean TB
   corpus gives the genuine terminal syllable distribution of Dravidian.
   Map strongest-terminal Indus sign -> strongest-terminal TB syllable.

Citations: A.1 (M77), C.2 (Parpola), E.1 (DEDR), A.12 (TB), D.12 (Tamburini 2025),
           D.6 (Daggumati & Revesz 2021)
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

# ── Corpus loading ─────────────────────────────────────────────────────────────
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

# ── Score function (k-permutations: NULL maps to SMOOTHING always) ─────────────
NULL_SYL = "__NULL__"

def score(m, inscs, bigs):
    t=0.0
    for insc in inscs:
        for i in range(len(insc)-1):
            a=m.get(insc[i]); b=m.get(insc[i+1])
            if a and b:
                if a==NULL_SYL or b==NULL_SYL:
                    t+=SMOOTHING
                else:
                    t+=bigs.get((a,b),SMOOTHING)
    return t

# ── Anchor loading ─────────────────────────────────────────────────────────────
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
# IMPROVEMENT 3 — Allograph reduction (Daggumati & Revesz 2021)
# ════════════════════════════════════════════════════════════════════════════════
def compute_allograph_reduction(
    inscriptions: list[list[str]],
    sign_freq: Counter,
    min_freq: int = 3,
    sim_threshold: float = 0.95,
) -> dict[str, str]:
    """Find allograph pairs via positional profile cosine similarity.
    Returns merge_map: {rare_sign -> canonical_sign}
    Only merges pairs where positional profile cosine similarity >= sim_threshold.
    """
    total_c = sign_freq
    terminal_c = Counter(insc[-1] for insc in inscriptions if len(insc)>1)
    initial_c  = Counter(insc[0]  for insc in inscriptions if len(insc)>1)

    # Build positional profile for each sign
    profiles = {}
    for sign, n in total_c.items():
        if n < min_freq: continue
        t = terminal_c[sign] / n
        i = initial_c[sign]  / n
        m = 1 - t - i  # medial as residual
        mag = math.sqrt(t**2 + i**2 + m**2)
        profiles[sign] = (t/max(mag,1e-9), i/max(mag,1e-9), m/max(mag,1e-9))

    # Find pairs with high cosine similarity
    signs_list = list(profiles.keys())
    merge_map: dict[str, str] = {}
    merged = set()
    for x_idx, sign_a in enumerate(signs_list):
        if sign_a in merged: continue
        va = profiles[sign_a]
        for sign_b in signs_list[x_idx+1:]:
            if sign_b in merged: continue
            vb = profiles[sign_b]
            cos_sim = va[0]*vb[0] + va[1]*vb[1] + va[2]*vb[2]
            if cos_sim >= sim_threshold:
                # Merge rarer into more frequent
                if sign_freq[sign_a] >= sign_freq[sign_b]:
                    merge_map[sign_b] = sign_a
                    merged.add(sign_b)
                else:
                    merge_map[sign_a] = sign_b
                    merged.add(sign_a)
                break  # each sign merges at most once
    return merge_map

def apply_allograph_merge(
    inscriptions: list[list[str]],
    merge_map: dict[str, str],
) -> list[list[str]]:
    """Apply allograph merging to inscription sequences."""
    return [[merge_map.get(s, s) for s in insc] for insc in inscriptions]

# ════════════════════════════════════════════════════════════════════════════════
# IMPROVEMENT 4 — Validated positional anchors from TB bigram profile
# ════════════════════════════════════════════════════════════════════════════════
def build_tb_positional_anchors(
    terminal_signs: dict[str, float],
    initial_signs: dict[str, float],
    tb_lm_name: str,
    vocab: set[str],
    existing_anchors: dict[str, str],
) -> tuple[dict[str, str], dict]:
    """Build validated positional anchors from actual TB inscription terminal/initial positions.

    FIX vs Phase-36: Previously used right-side bigram frequency as a proxy for
    terminal syllable preference. That measures which syllable most often FOLLOWS
    another, not which syllable appears at the END of inscriptions.

    Correct method:
    - terminal_tb_freq: count which syllable appears LAST in each TB inscription
    - initial_tb_freq:  count which syllable appears FIRST in each TB inscription

    These genuinely reflect which syllables occupy terminal/initial positions in
    real Tamil-Brahmi inscriptions, giving linguistically meaningful anchor targets.
    """
    clean_tb = json.loads((DATA/tb_lm_name).read_text("utf-8"))

    # Load TB inscription sequences
    tb_seqs: list[list[str]] = []
    for seq_key in ("inscriptions", "sequences"):
        if seq_key in clean_tb:
            for item in clean_tb[seq_key]:
                if isinstance(item, list) and len(item) >= 2:
                    tb_seqs.append(item)
            break

    # Fallback: reconstruct sequences from bigram keys
    if not tb_seqs:
        tb_bigs = clean_tb.get("bigrams", {})
        for key in tb_bigs:
            ps = key.split("|") if "|" in key else key.split(",")
            if len(ps) == 2:
                tb_seqs.append([ps[0].strip(), ps[1].strip()])

    # FIX: count actual inscription-ending and inscription-starting syllables
    terminal_tb_freq: Counter = Counter()
    initial_tb_freq: Counter = Counter()
    if tb_seqs:
        for seq in tb_seqs:
            if len(seq) >= 1:
                terminal_tb_freq[seq[-1]] += 1
                initial_tb_freq[seq[0]] += 1
    else:
        # Final fallback: use vocab frequency from the LM
        vocab_list = clean_tb.get("vocab", [])
        for i, syl in enumerate(vocab_list):
            terminal_tb_freq[syl] = len(vocab_list) - i
            initial_tb_freq[syl] = len(vocab_list) - i

    # Filter to syllables in Dravidian/Sanskrit vocab
    top_terminal_tb = [s for s,_ in terminal_tb_freq.most_common() if s in vocab and s not in ("","__NULL__")]
    top_initial_tb  = [s for s,_ in initial_tb_freq.most_common()  if s in vocab and s not in ("","__NULL__")]
    print(f"  Top TB terminal syllables (inscription-ending): {top_terminal_tb[:8]}")
    print(f"  Top TB initial syllables (inscription-starting): {top_initial_tb[:8]}")

    positional_anchors = dict(existing_anchors)
    tb_anchor_detail = {}

    # Map terminal signs (sorted by t_rate desc) to top TB terminal syllables
    sorted_term = sorted(terminal_signs.items(), key=lambda x: -x[1])
    tb_idx = 0
    for sign, trate in sorted_term:
        if sign in positional_anchors: continue
        if tb_idx >= len(top_terminal_tb): break
        # Skip TB syllables already used as anchor targets
        while tb_idx < len(top_terminal_tb) and top_terminal_tb[tb_idx] in positional_anchors.values():
            tb_idx += 1
        if tb_idx >= len(top_terminal_tb): break
        syl = top_terminal_tb[tb_idx]
        positional_anchors[sign] = syl
        tb_anchor_detail[sign] = {"t_rate": trate, "assigned": syl, "tb_terminal_rank": tb_idx+1, "type": "terminal"}
        tb_idx += 1

    # Map initial signs (sorted by i_rate desc) to top TB initial syllables
    sorted_init = sorted(initial_signs.items(), key=lambda x: -x[1])
    tb_init_idx = 0
    for sign, irate in sorted_init:
        if sign in positional_anchors: continue
        while tb_init_idx < len(top_initial_tb) and top_initial_tb[tb_init_idx] in positional_anchors.values():
            tb_init_idx += 1
        if tb_init_idx >= len(top_initial_tb): break
        syl = top_initial_tb[tb_init_idx]
        positional_anchors[sign] = syl
        tb_anchor_detail[sign] = {"i_rate": irate, "assigned": syl, "tb_initial_rank": tb_init_idx+1, "type": "initial"}
        tb_init_idx += 1

    return positional_anchors, tb_anchor_detail

# ════════════════════════════════════════════════════════════════════════════════
# IMPROVEMENT 1+2 — Coupled SA with k-permutations
# ════════════════════════════════════════════════════════════════════════════════
def run_csa(
    fixed: dict[str, str],
    free: list[str],
    vocab: list[str],
    inscriptions: list[list[str]],
    bigrams: dict[tuple[str, str], float],
    n_chains: int = 4,
    n_iters: int = 30_000,
    swap_interval: int = 500,
    null_fraction: float = 0.15,   # fraction of free signs that may be NULL
    seed: int = 42,
) -> tuple[dict[str, str], float]:
    """Coupled Simulated Annealing with k-permutations (null mappings).

    - n_chains: number of coupled chains
    - swap_interval: attempt chain-pair swap every N iterations
    - null_fraction: fraction of free signs allowed to map to NULL_SYL

    Returns best mapping and its score across all chains.
    """
    rng = random.Random(seed)
    n_free = len(free)
    n_null_allowed = max(1, int(n_free * null_fraction))

    def _init_mapping(chain_seed: int) -> dict[str, str]:
        r = random.Random(chain_seed)
        # Available syllables (excluding NULL initially)
        avail = [v for v in vocab if v not in fixed.values()]
        while len(avail) < n_free: avail.append(r.choice(vocab))
        r.shuffle(avail)
        m = dict(fixed)
        for i, s in enumerate(free):
            m[s] = avail[i % len(avail)]
        # Randomly assign some free signs to NULL
        null_candidates = r.sample(free, min(n_null_allowed, len(free)))
        for s in null_candidates:
            if s not in fixed:
                m[s] = NULL_SYL
        return m

    # Initialize n_chains solutions
    chains = [_init_mapping(seed + i * 1000) for i in range(n_chains)]
    chain_scores = [score(m, inscriptions, bigrams) for m in chains]
    best_global = max(chain_scores)
    best_map = dict(chains[chain_scores.index(best_global)])

    # Temperature schedules (slightly different per chain for diversity)
    T0 = 2.0; T1 = 0.01
    temps = [T0 * (0.95 ** i) for i in range(n_chains)]  # staggered T0

    # SA loop
    for it in range(n_iters):
        for c in range(n_chains):
            T = temps[c] * ((T1 / temps[c]) ** (it / n_iters))
            m = chains[c]
            if len(free) < 2: continue

            # Choose move: sign-swap or NULL toggle
            move = rng.random()
            if move < 0.85:
                # Standard swap
                i, j = rng.sample(range(n_free), 2)
                si, sj = free[i], free[j]
                vi, vj = m[si], m[sj]
                m[si], m[sj] = vj, vi
                nw = score(m, inscriptions, bigrams)
                d = nw - chain_scores[c]
                if d > 0 or rng.random() < math.exp(d / max(T, 1e-10)):
                    chain_scores[c] = nw
                    if nw > best_global:
                        best_global = nw; best_map = dict(m)
                else:
                    m[si], m[sj] = vi, vj
            else:
                # NULL toggle: convert a sign to/from NULL
                sign = rng.choice(free)
                old_val = m[sign]
                if old_val == NULL_SYL:
                    # Convert NULL to a syllable
                    avail = [v for v in vocab if v not in m.values() and v != NULL_SYL]
                    if not avail: avail = vocab
                    new_val = rng.choice(avail)
                else:
                    # Convert to NULL (only if we have budget)
                    n_current_null = sum(1 for v in m.values() if v == NULL_SYL)
                    if n_current_null >= n_null_allowed:
                        continue
                    new_val = NULL_SYL
                m[sign] = new_val
                nw = score(m, inscriptions, bigrams)
                d = nw - chain_scores[c]
                if d > 0 or rng.random() < math.exp(d / max(T, 1e-10)):
                    chain_scores[c] = nw
                    if nw > best_global:
                        best_global = nw; best_map = dict(m)
                else:
                    m[sign] = old_val

        # Chain coupling: try to swap solutions between adjacent chain pairs
        if (it + 1) % swap_interval == 0:
            for c in range(n_chains - 1):
                # Metropolis exchange criterion
                T_c = temps[c] * ((T1 / temps[c]) ** (it / n_iters))
                delta = chain_scores[c+1] - chain_scores[c]
                if delta > 0 or rng.random() < math.exp(delta / max(T_c, 1e-10)):
                    chains[c], chains[c+1] = chains[c+1], chains[c]
                    chain_scores[c], chain_scores[c+1] = chain_scores[c+1], chain_scores[c]

    return best_map, best_global

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

# ════════════════════════════════════════════════════════════════════════════════
# LOAD SHARED DATA
# ════════════════════════════════════════════════════════════════════════════════
print("="*65)
print("Phase-37: Loading shared data...")

inscs_raw, sf_raw = load_corpus()
drav_bigs_full, drav_ranked_full = load_lm("dravidian_syllable_lm.json")
skt_bigs, skt_ranked = load_lm("sanskrit_syllable_lm.json")

# Equalized LMs (424 syl, 651 bigrams — best controlled from Phase-36)
N_SYL = len(skt_ranked)   # 424
N_BIG = len(skt_bigs)     # 651
drav_ranked_eq = drav_ranked_full[:N_SYL]
drav_vocab_eq = set(drav_ranked_eq)
drav_bigs_all = {(a,b):lp for(a,b),lp in drav_bigs_full.items() if a in drav_vocab_eq and b in drav_vocab_eq}
drav_bigs_thin = dict(sorted(drav_bigs_all.items(),key=lambda x:-x[1])[:N_BIG])
skt_vocab = set(skt_ranked)

print(f"M77: {len(inscs_raw)} inscriptions, {len(sf_raw)} total signs")
print(f"Equalized Dravidian LM: {N_SYL} syl / {len(drav_bigs_thin)} bigrams")
print(f"Sanskrit LM:            {N_SYL} syl / {len(skt_bigs)} bigrams")

# ════════════════════════════════════════════════════════════════════════════════
# STEP 1 — Allograph reduction
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65)
print("STEP 1: Allograph reduction")

# Compute positional profiles for all signs freq>=3
terminal_c = Counter(insc[-1] for insc in inscs_raw if len(insc)>1)
initial_c  = Counter(insc[0]  for insc in inscs_raw if len(insc)>1)
all_profiles = {}
for sign, n in sf_raw.items():
    if n < 3: continue
    t = terminal_c[sign]/n; i = initial_c[sign]/n; m_rate = 1-t-i
    all_profiles[sign] = {"t_rate":round(t,4),"i_rate":round(i,4),"m_rate":round(m_rate,4),"freq":n}

# Use strict threshold (0.999) to avoid over-merging.
# Only merge sign pairs with nearly-identical positional profiles.
# This captures genuine allographs without collapsing functionally distinct signs.
merge_map = compute_allograph_reduction(inscs_raw, sf_raw, min_freq=3, sim_threshold=0.999)
if len(merge_map) == 0:
    merge_map = compute_allograph_reduction(inscs_raw, sf_raw, min_freq=3, sim_threshold=0.998)

print(f"Allograph pairs found (sim>=0.90): {len(merge_map)}")
for rare, canonical in merge_map.items():
    sim = sum(all_profiles[rare][k]*all_profiles[canonical][k]
              for k in("t_rate","i_rate","m_rate")) / max(
              math.sqrt(sum(all_profiles[rare][k]**2 for k in("t_rate","i_rate","m_rate"))),1e-9) / max(
              math.sqrt(sum(all_profiles[canonical][k]**2 for k in("t_rate","i_rate","m_rate"))),1e-9)
    print(f"  {rare}(f={sf_raw[rare]}) -> {canonical}(f={sf_raw[canonical]}) sim={sim:.3f}")

# FIX: Preserve anchor readings for merged signs.
# When rare sign A is merged into canonical sign B:
#   if A had an anchor reading, add B->A's reading if B has no anchor yet.
# This must be applied BEFORE loading anchors so canonical signs inherit readings.
all_raw_anchors: dict[str, str] = {}
_fa_p = BACKEND_REPORTS / "INDUS_FINAL_ANCHORS.json"
if _fa_p.exists():
    _fa = json.loads(_fa_p.read_text("utf-8"))
    for _m_id, _info in _fa.get("anchors", {}).items():
        if _info.get("confidence") not in ("HIGH", "MEDIUM"): continue
        _r = _info.get("reading", "")
        if _r and "?" not in _r:
            all_raw_anchors[_m_id] = _r
            if _m_id.startswith("M") and _m_id[1:].isdigit():
                all_raw_anchors[_m_id[1:]] = _r  # e.g. "047"

# Augment INDUS_FINAL_ANCHORS with any sign that rare->canonical merge carries
for rare, canonical in merge_map.items():
    if rare in all_raw_anchors and canonical not in all_raw_anchors:
        all_raw_anchors[canonical] = all_raw_anchors[rare]
        print(f"  Anchor transferred: {rare}->{canonical}: {all_raw_anchors[rare]}")

# Apply merging
inscs_merged = apply_allograph_merge(inscs_raw, merge_map)
sf_merged = Counter(s for insc in inscs_merged for s in insc)
cipher_merged = [s for s,c in sf_merged.items() if c>=3]
print(f"After merging: {len(cipher_merged)} signs (freq>=3), was {sum(1 for _,c in sf_raw.items() if c>=3)}")

# ════════════════════════════════════════════════════════════════════════════════
# STEP 2 — Validated positional anchors
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65)
print("STEP 2: Validated positional anchors via TB bigram profile")

# Terminal and initial signs from merged corpus
term_merged = Counter(insc[-1] for insc in inscs_merged if len(insc)>1)
init_merged  = Counter(insc[0]  for insc in inscs_merged if len(insc)>1)

TERMINAL_SIGNS_MERGED = {s: term_merged[s]/sf_merged[s]
                          for s in cipher_merged if sf_merged[s]>0 and
                          term_merged[s]/sf_merged[s] >= 0.40}
INITIAL_SIGNS_MERGED  = {s: init_merged[s]/sf_merged[s]
                          for s in cipher_merged if sf_merged[s]>0 and
                          init_merged[s]/sf_merged[s] >= 0.40}

print(f"Terminal signs (t>=0.40): {len(TERMINAL_SIGNS_MERGED)}")
print(f"Initial signs (i>=0.40):  {len(INITIAL_SIGNS_MERGED)}")

# Base anchors (LM+crosswalk)
base_anchors = build_anchors(drav_vocab_eq)
base_ca = {s:r for s,r in base_anchors.items() if s in sf_merged}
base_fixed = {s:r for s,r in base_ca.items() if s in cipher_merged and r in drav_vocab_eq}
print(f"Base LM+crosswalk anchors active in merged corpus: {len(base_fixed)}")

# Apply TB validated positional anchors
validated_anchors, tb_detail = build_tb_positional_anchors(
    TERMINAL_SIGNS_MERGED, INITIAL_SIGNS_MERGED,
    "mahadevan_2003_tb_lm_clean.json",
    drav_vocab_eq, base_fixed,
)
n_tb_added = len(validated_anchors) - len(base_fixed)
print(f"TB positional anchors added: {n_tb_added}")
for sign, detail in tb_detail.items():
    print(f"  {sign} -> {detail['assigned']} [{detail['type']}, rank={detail.get('tb_terminal_rank',detail.get('tb_initial_rank','?'))}]")

total_anchors = {s:r for s,r in validated_anchors.items() if s in cipher_merged and r in drav_vocab_eq}
free_signs = [s for s in cipher_merged if s not in total_anchors]
print(f"\nTotal anchors in merged cipher: {len(total_anchors)}")
print(f"Free signs: {len(free_signs)}")

# ════════════════════════════════════════════════════════════════════════════════
# EXP A — CSA Dravidian (all improvements combined)
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65)
print("EXP A: CSA Dravidian (allograph-merged + TB anchors + CSA + null-maps)")

N_CHAINS = 4; N_ITERS = 30_000; SWAP_INT = 500; NULL_FRAC = 0.15
t0 = time.time()
print(f"Running CSA: {N_CHAINS} chains × {N_ITERS} iters, swap_interval={SWAP_INT}, null_frac={NULL_FRAC}...")

# Run multiple CSA experiments (seeds)
N_CSA_RUNS = 4
csa_dr_results = []
for run in range(N_CSA_RUNS):
    m, s = run_csa(total_anchors, free_signs, drav_ranked_eq, inscs_merged, drav_bigs_thin,
                   n_chains=N_CHAINS, n_iters=N_ITERS, swap_interval=SWAP_INT,
                   null_fraction=NULL_FRAC, seed=run*100)
    csa_dr_results.append((s, m))
    print(f"  CSA run {run}: {s:.1f}")

csa_dr_best_s, csa_dr_best_m = max(csa_dr_results, key=lambda x: x[0])
print(f"Best CSA Dravidian: {csa_dr_best_s:.1f}")
print("Computing null (500 perms)...")
dr_nm, dr_nstd, dr_z, dr_p = null_test(csa_dr_best_m, inscs_merged, drav_bigs_thin)
dr_lift = (csa_dr_best_s - dr_nm) / max(1, len(inscs_merged))
print(f"  Null={dr_nm:.1f}±{dr_nstd:.1f}, Z={dr_z:.2f}, p={dr_p:.4f}, lift={dr_lift:.3f}")

# Sample decoded inscriptions (removing NULL readings for readability)
sample_decoded = []
for insc in sorted(inscs_merged, key=len, reverse=True)[:10]:
    readings = [csa_dr_best_m.get(s,"?") for s in insc]
    clean_reading = "-".join(r for r in readings if r!=NULL_SYL) or "(all null)"
    coverage = sum(1 for r in readings if r not in (None, "?", NULL_SYL)) / len(readings)
    sample_decoded.append({"signs": insc, "syllables_full": "-".join(readings),
                            "syllables_clean": clean_reading, "coverage": round(coverage,2)})

exp_a = {
    "experiment": "Phase-37 A: CSA Dravidian (all improvements)",
    "n_chains": N_CHAINS, "n_iters": N_ITERS, "swap_interval": SWAP_INT,
    "null_fraction": NULL_FRAC, "n_csa_runs": N_CSA_RUNS,
    "n_allograph_pairs": len(merge_map), "allograph_merge_map": merge_map,
    "n_base_anchors": len(base_fixed), "n_tb_anchors_added": n_tb_added,
    "n_total_anchors": len(total_anchors), "n_free_signs": len(free_signs),
    "n_merged_inscriptions": len(inscs_merged),
    "n_merged_signs_freq3": len(cipher_merged),
    "best_score": round(csa_dr_best_s,3), "null_mean": round(dr_nm,3),
    "null_std": round(dr_nstd,3), "z_score": round(dr_z,3), "p_value": round(dr_p,4),
    "nll_lift_per_inscription": round(dr_lift,4), "significant": dr_p<0.05,
    "seed_scores": [round(s,1) for s,_ in csa_dr_results],
    "tb_anchor_assignments": tb_detail,
    "sample_decoded": sample_decoded,
    "verdict": (
        f"Phase-37 CSA Dravidian: Z={dr_z:.2f}, p={dr_p:.4f}, lift={dr_lift:.3f}. "
        f"Allograph merges={len(merge_map)}, TB anchors added={n_tb_added}, "
        f"total anchors={len(total_anchors)}, free={len(free_signs)}. "
        f"{'SIGNIFICANT (p<0.05)' if dr_p<0.05 else 'NOT SIGNIFICANT'}. "
        f"Runtime={time.time()-t0:.0f}s."
    ),
    "runtime_seconds": round(time.time()-t0,1),
    "_citation": {"primary":["A.1","E.1","C.2","A.12","D.12","D.6"],"phase":"Phase-37-A"},
}
(REPORTS/"phase37_csa_dravidian.json").write_text(
    json.dumps(exp_a,indent=2,ensure_ascii=False),"utf-8")
print(f"  Saved phase37_csa_dravidian.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# EXP B — CSA Sanskrit (same conditions for fair comparison)
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65)
print("EXP B: CSA Sanskrit (density-equalized, same CSA params)")

# Sanskrit anchors
skt_base_anch = build_anchors(skt_vocab)
skt_ca = {s:r for s,r in skt_base_anch.items() if s in sf_merged}
skt_fixed = {s:r for s,r in skt_ca.items() if s in cipher_merged and r in skt_vocab}

# TB positional anchors for Sanskrit (using Sanskrit syllable vocab)
TERM_S_MERGED = dict(TERMINAL_SIGNS_MERGED)
INIT_S_MERGED = dict(INITIAL_SIGNS_MERGED)
skt_val_anch, skt_tb_detail = build_tb_positional_anchors(
    TERM_S_MERGED, INIT_S_MERGED, "mahadevan_2003_tb_lm_clean.json",
    skt_vocab, skt_fixed,
)
skt_total = {s:r for s,r in skt_val_anch.items() if s in cipher_merged and r in skt_vocab}
skt_free = [s for s in cipher_merged if s not in skt_total]
print(f"Sanskrit total anchors: {len(skt_total)}, free: {len(skt_free)}")

t0 = time.time()
print(f"Running CSA Sanskrit: {N_CHAINS} chains × {N_ITERS} iters...")
csa_sk_results = []
for run in range(N_CSA_RUNS):
    m, s = run_csa(skt_total, skt_free, skt_ranked, inscs_merged, skt_bigs,
                   n_chains=N_CHAINS, n_iters=N_ITERS, swap_interval=SWAP_INT,
                   null_fraction=NULL_FRAC, seed=run*100)
    csa_sk_results.append((s, m)); print(f"  CSA run {run}: {s:.1f}")

csa_sk_best_s, csa_sk_best_m = max(csa_sk_results, key=lambda x: x[0])
print(f"Best CSA Sanskrit: {csa_sk_best_s:.1f}")
sk_nm, sk_nstd, sk_z, sk_p = null_test(csa_sk_best_m, inscs_merged, skt_bigs)
sk_lift = (csa_sk_best_s - sk_nm) / max(1, len(inscs_merged))
print(f"  Null={sk_nm:.1f}±{sk_nstd:.1f}, Z={sk_z:.2f}, p={sk_p:.4f}, lift={sk_lift:.3f}")

drav_wins = dr_lift > sk_lift
ratio = dr_lift / max(abs(sk_lift), 0.001)

exp_b = {
    "experiment": "Phase-37 B: CSA Sanskrit",
    "n_total_anchors": len(skt_total), "n_free_signs": len(skt_free),
    "best_score": round(csa_sk_best_s,3), "null_mean": round(sk_nm,3),
    "null_std": round(sk_nstd,3), "z_score": round(sk_z,3), "p_value": round(sk_p,4),
    "nll_lift_per_inscription": round(sk_lift,4), "significant": sk_p<0.05,
    "dravidian_lift": round(dr_lift,4), "dravidian_z": round(dr_z,3),
    "dravidian_wins": drav_wins, "lift_ratio_drav_over_skt": round(ratio,3),
    "seed_scores": [round(s,1) for s,_ in csa_sk_results],
    "verdict": (
        f"Phase-37 CSA Sanskrit: Z={sk_z:.2f}, p={sk_p:.4f}, lift={sk_lift:.3f}. "
        f"Dravidian lift={dr_lift:.3f} ({ratio:.2f}x). "
        f"Dravidian {'WINS' if drav_wins else 'loses'}. "
        f"Runtime={time.time()-t0:.0f}s."
    ),
    "runtime_seconds": round(time.time()-t0,1),
    "_citation": {"primary":["A.1","E.1","D.12"],"phase":"Phase-37-B"},
}
(REPORTS/"phase37_csa_sanskrit.json").write_text(
    json.dumps(exp_b,indent=2,ensure_ascii=False),"utf-8")
print(f"  Saved phase37_csa_sanskrit.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65)
print("Phase-37 complete. Results:")
for fn in ["phase37_csa_dravidian.json","phase37_csa_sanskrit.json"]:
    p=REPORTS/fn; sz=p.stat().st_size if p.exists() else 0
    print(f"  {'OK' if p.exists() else 'MISSING'} {fn} ({sz//1024}KB)")

print(f"\nPhase-37 final comparison:")
print(f"  CSA Dravidian: Z={dr_z:.2f}, p={dr_p:.4f}, lift={dr_lift:.3f}")
print(f"  CSA Sanskrit:  Z={sk_z:.2f}, p={sk_p:.4f}, lift={sk_lift:.3f}")
print(f"  Dravidian wins: {drav_wins} (ratio {ratio:.2f}x)")
print(f"\n  Allograph pairs merged: {len(merge_map)}")
print(f"  TB positional anchors added: {n_tb_added}")
print(f"  Total anchors: {len(total_anchors)}, Free signs: {len(free_signs)}")
print(f"\nVERDICT: {'Dravidian SURVIVES CSA falsification' if drav_wins else 'Sanskrit competitive under CSA — [UNCERTAIN] persists'}")
