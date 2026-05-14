"""Phase-35: Vocabulary equalization + anchor augmentation + controlled SA comparison.

Three bugs fixed vs Phase-34:
  1. VOCAB SIZE CONFOUND: Dravidian LM truncated to top-N syllables to match Sanskrit
  2. SPARSE ANCHORS: Crosswalk (mahadevan_parpola_crosswalk_v2.json) used to add more anchors
  3. LM QUALITY: Merged LM from DEDR bigrams + clean TB bigrams (no OCR noise)

Experiments:
  A. Anchor audit — how many crosswalk entries match freq>=3 corpus signs?
  B. Phase-35 T1 — Equalized Dravidian SA (Dravidian LM truncated to Sanskrit's vocab size)
  C. Phase-35 T7 — Equalized Sanskrit SA (unchanged, 424 syllables)
  D. LM quality analysis — DEDR-only vs DEDR+cleanTB combined bigrams

Citations: A.1 (M77), C.2 (Parpola), E.1 (DEDR), A.12 (Mahadevan 2003 TB)
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
SMOOTHING_LOG = math.log(1e-8)

# ── Helpers (same as phase34) ─────────────────────────────────────────────────
_DIACRITIC_MAP = {
    "ā": "a", "ī": "i", "ū": "u", "ṉ": "n", "ṟ": "r", "ḷ": "l",
    "ḻ": "l", "ṛ": "r", "ṭ": "t", "ḍ": "d", "ṅ": "n", "ṇ": "n",
    "ñ": "n", "ś": "s", "ṣ": "s", "ḥ": "h", "ẓ": "z", "ḻ": "l",
}

def _strip_diacritics(s: str) -> str:
    out = []
    for ch in unicodedata.normalize("NFD", s):
        plain = _DIACRITIC_MAP.get(ch)
        if plain: out.append(plain)
        elif unicodedata.category(ch) != "Mn": out.append(ch)
    return "".join(out)

def _split_syllables(word: str) -> list[str]:
    VOWELS = set("aeiouaiu")
    CONSONANTS = set("bcdfghjklmnpqrstvwxyz")
    syllables: list[str] = []
    i = 0; current = ""
    while i < len(word):
        c = word[i]; current += c
        if c in VOWELS:
            if (i + 1 < len(word) and word[i+1] in CONSONANTS and
                    (i + 2 >= len(word) or word[i+2] in VOWELS)):
                i += 1; current += word[i]
            syllables.append(current); current = ""
        elif len(current) >= 3:
            syllables.append(current); current = ""
        i += 1
    if current:
        if syllables: syllables[-1] += current
        else: syllables.append(current)
    return [s for s in syllables if s]

def _to_syllable(reading: str, vocab: set[str]) -> str | None:
    reading = reading.split("/")[0].strip()
    reading = re.sub(r"\(.*?\)", "", reading).strip().rstrip("?")
    if re.match(r"(term|med|init|ctx|role|boundary|suffix|uncertain)[-:]?", reading.lower()):
        return None
    if not reading or reading in ("?", "-") or len(reading) < 1:
        return None
    if "uncertain" in reading.lower() or "boundary" in reading.lower():
        return None
    clean = _strip_diacritics(reading)
    clean = re.sub(r"[^a-z]", "", clean.lower())
    if not clean or len(clean) < 1:
        return None
    if clean in vocab: return clean
    for s in _split_syllables(clean):
        if s in vocab: return s
    for length in (2, 3, 1):
        if len(clean) >= length:
            c = clean[:length]
            if c in vocab: return c
    return clean[:3] if len(clean) > 3 else clean

def load_corpus():
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    inscriptions = get_corpus_inscriptions()
    flat = get_corpus_symbols()
    return inscriptions, Counter(flat)

def load_lm(name: str) -> tuple[dict, list[str]]:
    raw = json.loads((DATA / name).read_text("utf-8"))
    braw = raw.get("bigrams", raw.get("bigram_freq", {}))
    bigrams: dict[tuple[str,str], float] = {}
    for key, lp in braw.items():
        parts = key.split("|") if "|" in key else key.split(",") if "," in key else [key]
        if len(parts) == 2:
            try: bigrams[(parts[0].strip(), parts[1].strip())] = float(lp)
            except: pass
    freq: Counter = Counter()
    for (a,b) in bigrams: freq[a]+=1; freq[b]+=1
    ranked = raw.get("vocab", []) or [s for s,_ in freq.most_common()]
    return bigrams, ranked

def score_mapping(m, inscs, bigs):
    t = 0.0
    for insc in inscs:
        for i in range(len(insc)-1):
            a=m.get(insc[i]); b=m.get(insc[i+1])
            if a and b: t += bigs.get((a,b), SMOOTHING_LOG)
    return t

def run_sa(fixed, free, vocab, inscs, bigs, n_iters=30_000, seed=42):
    rng = random.Random(seed)
    if not vocab: return dict(fixed), score_mapping(fixed, inscs, bigs)
    free_target = [v for v in vocab if v not in fixed.values()]
    while len(free_target) < len(free): free_target.append(rng.choice(vocab))
    rng.shuffle(free_target)
    mapping = dict(fixed)
    for i, sign in enumerate(free): mapping[sign] = free_target[i % len(free_target)]
    cur = score_mapping(mapping, inscs, bigs)
    best = dict(mapping); best_s = cur
    T0, T1 = 2.0, 0.01
    for it in range(n_iters):
        T = T0 * ((T1/T0)**(it/n_iters))
        if len(free) < 2: break
        i,j = rng.sample(range(len(free)), 2)
        si,sj = free[i],free[j]; vi,vj = mapping[si],mapping[sj]
        mapping[si],mapping[sj] = vj,vi
        new = score_mapping(mapping, inscs, bigs)
        d = new - cur
        if d > 0 or rng.random() < math.exp(d/max(T,1e-10)):
            cur = new
            if new > best_s: best_s=new; best=dict(mapping)
        else: mapping[si],mapping[sj] = vi,vj
    return best, best_s

def perm_null(m, inscs, bigs, n=500, seed=99):
    rng = random.Random(seed)
    obs = score_mapping(m, inscs, bigs)
    ks=list(m.keys()); vs=list(m.values())
    nulls=[]
    for _ in range(n):
        sh=vs[:]; rng.shuffle(sh)
        nulls.append(score_mapping(dict(zip(ks,sh)), inscs, bigs))
    nm=sum(nulls)/len(nulls); nstd=math.sqrt(sum((s-nm)**2 for s in nulls)/len(nulls))
    z=(obs-nm)/nstd if nstd>0 else 0.0
    p=sum(1 for s in nulls if s>=obs)/n
    return nm,nstd,z,p

# ── Load shared data ──────────────────────────────────────────────────────────
print("="*65)
print("Phase-35: Loading shared data...")
inscriptions, sign_freq = load_corpus()
cipher_signs = [s for s,c in sign_freq.items() if c >= 3]
drav_bigrams, drav_ranked = load_lm("dravidian_syllable_lm.json")
drav_vocab_full = set(drav_ranked)
skt_bigrams, skt_ranked = load_lm("sanskrit_syllable_lm.json")
skt_vocab = set(skt_ranked)
print(f"M77: {len(inscriptions)} inscriptions, {len(cipher_signs)} signs (freq>=3)")
print(f"Dravidian LM full: {len(drav_ranked)} syllables, {len(drav_bigrams)} bigrams")
print(f"Sanskrit LM: {len(skt_ranked)} syllables, {len(skt_bigrams)} bigrams")

# ════════════════════════════════════════════════════════════════════════════════
# EXP A — Anchor Audit
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("EXP A: Anchor Audit — crosswalk + INDUS_FINAL_ANCHORS vs corpus")

# Build full anchor map using ALL sources
def build_augmented_anchors(vocab: set[str]) -> dict[str, str]:
    """Build anchor dict from all sources, returning corpus-ID-keyed dict."""
    anchors: dict[str, str] = {}

    # 1. Parpola phonemes
    pp = json.loads((DATA / "parpola_phonemes.json").read_text("utf-8"))
    for sid, info in pp.get("phoneme_map", {}).items():
        if not isinstance(info, dict): continue
        pv = info.get("phoneme", info.get("phoneme_value", ""))
        conf = info.get("confidence", "low")
        if pv and conf in ("high","medium") and "?" not in pv:
            s = _to_syllable(pv, vocab)
            if s:
                anchors[sid] = s
                if sid.isdigit(): anchors[sid.zfill(3)] = s

    # 2. INDUS_FINAL_ANCHORS (M-prefix stripped)
    fa_path = BACKEND_REPORTS / "INDUS_FINAL_ANCHORS.json"
    if fa_path.exists():
        fa = json.loads(fa_path.read_text("utf-8"))
        for m_id, info in fa.get("anchors", {}).items():
            if info.get("confidence") not in ("HIGH","MEDIUM"): continue
            reading = info.get("reading","")
            if "?" in reading: continue
            s = _to_syllable(reading, vocab)
            if not s: continue
            anchors[m_id] = s
            if m_id.startswith("M") and m_id[1:].isdigit():
                anchors[m_id[1:]] = s  # "047"

    # 3. M↔P Crosswalk (additional source)
    xw_path = DATA / "mahadevan_parpola_crosswalk_v2.json"
    if xw_path.exists():
        xw = json.loads(xw_path.read_text("utf-8"))
        added_from_cw = 0
        for m_id, entry in xw.get("crosswalk", {}).items():
            phoneme = entry.get("phoneme", "")
            conf = entry.get("confidence", "LOW")
            if conf.upper() not in ("HIGH","MEDIUM"): continue
            if "?" in phoneme: continue
            s = _to_syllable(phoneme, vocab)
            if not s: continue
            # Add M-number key and bare numeric key
            anchors[m_id] = s
            bare = m_id[1:] if m_id.startswith("M") and m_id[1:].isdigit() else m_id
            if bare not in anchors:
                anchors[bare] = s
                added_from_cw += 1
        print(f"  Crosswalk added {added_from_cw} new anchor mappings")

    return anchors

all_anchors = build_augmented_anchors(drav_vocab_full)
corpus_anchors = {s: r for s, r in all_anchors.items() if s in sign_freq}
drav_fixed_aug = {s: r for s, r in corpus_anchors.items() if r in drav_vocab_full}

print(f"Total anchor entries: {len(all_anchors)}")
print(f"Active in corpus (any freq): {len(corpus_anchors)}")
print(f"Active in freq>=3 signs: {len([s for s in drav_fixed_aug if s in cipher_signs])}")
if drav_fixed_aug:
    print("  Active anchors:")
    for sign, reading in sorted(drav_fixed_aug.items()):
        if sign in sign_freq:
            print(f"    {sign:>6s} (freq={sign_freq[sign]:4d}) → {reading}")

# Audit: which crosswalk entries are missing from corpus?
print("\n  Crosswalk entries NOT in freq>=3 corpus:")
xw_data = json.loads((DATA / "mahadevan_parpola_crosswalk_v2.json").read_text("utf-8"))
missing = []
for m_id, entry in xw_data.get("crosswalk", {}).items():
    bare = m_id[1:] if m_id.startswith("M") and m_id[1:].isdigit() else m_id
    freq = sign_freq.get(bare, 0)
    conf = entry.get("confidence","?")
    phoneme = entry.get("phoneme","")
    if freq < 3:
        missing.append(f"    {m_id:8s} corpus_freq={freq:3d} [{conf}] {phoneme}")
    else:
        syll = _to_syllable(phoneme, drav_vocab_full)
        is_active = bare in drav_fixed_aug
        status = "ACTIVE" if is_active else f"SYLL_FILTERED({phoneme}→{syll})"
        print(f"    {m_id:8s} freq={freq:4d} [{conf}] {phoneme} → {status}")
for line in missing[:10]: print(line)
if len(missing) > 10: print(f"    ...and {len(missing)-10} more low-freq entries")

anchor_audit = {
    "total_anchor_entries": len(all_anchors),
    "active_any_freq": len(corpus_anchors),
    "active_freq_gte3": len([s for s in drav_fixed_aug if s in cipher_signs]),
    "active_anchors": {s: r for s,r in drav_fixed_aug.items() if s in cipher_signs},
    "crosswalk_entries_in_corpus": sum(1 for m,e in xw_data["crosswalk"].items()
                                        if sign_freq.get(m[1:]if m.startswith("M") else m,0) >= 3),
    "_citation": {"primary": ["A.1","C.2"], "phase": "Phase-35-AnchorAudit"},
}

# ════════════════════════════════════════════════════════════════════════════════
# EXP B — Vocabulary-equalized Dravidian SA (Phase-35 T1)
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("EXP B: Phase-35 T1 — Equalized Dravidian SA")

# Truncate Dravidian LM to match Sanskrit's vocabulary size
N_EQUALIZED = len(skt_ranked)  # 424
drav_ranked_eq = drav_ranked[:N_EQUALIZED]   # top-424 by frequency
drav_vocab_eq = set(drav_ranked_eq)
# Rebuild bigrams restricted to equalized vocab
drav_bigrams_eq = {(a,b):lp for (a,b),lp in drav_bigrams.items()
                   if a in drav_vocab_eq and b in drav_vocab_eq}
print(f"Dravidian LM truncated: {len(drav_ranked_eq)} syllables, {len(drav_bigrams_eq)} bigrams "
      f"(from {len(drav_ranked)} / {len(drav_bigrams)})")

# Build equalized anchors (must be in truncated vocab)
drav_fixed_eq = {s: r for s,r in drav_fixed_aug.items()
                 if s in cipher_signs and r in drav_vocab_eq}
drav_free_eq = [s for s in cipher_signs if s not in drav_fixed_eq]
print(f"Fixed anchors (equalized vocab): {len(drav_fixed_eq)}, free: {len(drav_free_eq)}")

t0 = time.time()
N_SEEDS, N_ITERS = 5, 30_000
print(f"Running equalized Dravidian SA: {N_SEEDS} seeds × {N_ITERS} iters...")
drav_eq_results = []
for seed in range(N_SEEDS):
    m, s = run_sa(drav_fixed_eq, drav_free_eq, drav_ranked_eq, inscriptions, drav_bigrams_eq,
                  n_iters=N_ITERS, seed=seed)
    drav_eq_results.append((s, m))
    print(f"  Seed {seed}: {s:.1f}")

drav_eq_best_s, drav_eq_best_m = max(drav_eq_results, key=lambda x: x[0])
print(f"Best equalized Dravidian score: {drav_eq_best_s:.1f}")
print("Computing null (500 perms)...")
drav_eq_nm, drav_eq_nstd, drav_eq_z, drav_eq_p = perm_null(
    drav_eq_best_m, inscriptions, drav_bigrams_eq)
drav_eq_lift = (drav_eq_best_s - drav_eq_nm) / max(1, len(inscriptions))
print(f"  Null={drav_eq_nm:.1f}±{drav_eq_nstd:.1f}, Z={drav_eq_z:.2f}, p={drav_eq_p:.4f}, "
      f"lift/insc={drav_eq_lift:.3f}")

t1_result = {
    "experiment": "Phase-35 T1: Equalized Dravidian SA",
    "n_vocab_equalized": N_EQUALIZED,
    "n_bigrams_after_truncation": len(drav_bigrams_eq),
    "n_fixed_anchors": len(drav_fixed_eq),
    "n_free_signs": len(drav_free_eq),
    "best_score": round(drav_eq_best_s, 3),
    "null_mean": round(drav_eq_nm, 3),
    "null_std": round(drav_eq_nstd, 3),
    "z_score": round(drav_eq_z, 3),
    "p_value": round(drav_eq_p, 4),
    "nll_lift_per_inscription": round(drav_eq_lift, 4),
    "significant_at_05": drav_eq_p < 0.05,
    "fixed_anchors": drav_fixed_eq,
    "seed_scores": [round(s,1) for s,_ in drav_eq_results],
    "verdict": (
        f"Phase-35 T1 Equalized Dravidian SA (vocab={N_EQUALIZED} syllables): "
        f"score={drav_eq_best_s:.1f}, null={drav_eq_nm:.1f}±{drav_eq_nstd:.1f}, "
        f"Z={drav_eq_z:.2f}, p={drav_eq_p:.4f}, lift/insc={drav_eq_lift:.3f}. "
        f"Anchors={len(drav_fixed_eq)}, free={len(drav_free_eq)}. "
        f"{'SIGNIFICANT (p<0.05)' if drav_eq_p < 0.05 else 'NOT SIGNIFICANT'}. "
        f"Runtime={time.time()-t0:.0f}s."
    ),
    "runtime_seconds": round(time.time()-t0, 1),
    "_citation": {"primary": ["A.1","E.1","C.2"], "phase": "Phase-35-T1"},
}
(REPORTS / "phase35_t1_equalized_dravidian_sa.json").write_text(
    json.dumps(t1_result, indent=2, ensure_ascii=False), "utf-8")
print(f"  Saved phase35_t1_equalized_dravidian_sa.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# EXP C — Equalized Sanskrit SA (Phase-35 T7)
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("EXP C: Phase-35 T7 — Equalized Sanskrit SA (424 syllables, unchanged)")

skt_all_anchors = build_augmented_anchors(skt_vocab)
skt_corpus_anchors = {s: r for s,r in skt_all_anchors.items() if s in sign_freq}
skt_fixed_eq = {s: r for s,r in skt_corpus_anchors.items() if s in cipher_signs and r in skt_vocab}
skt_free_eq = [s for s in cipher_signs if s not in skt_fixed_eq]
print(f"Sanskrit fixed anchors: {len(skt_fixed_eq)}, free: {len(skt_free_eq)}")
print(f"Sanskrit LM: {len(skt_ranked)} syllables, {len(skt_bigrams)} bigrams (same size as equalized Dravidian)")

t0 = time.time()
print(f"Running equalized Sanskrit SA: {N_SEEDS} seeds × {N_ITERS} iters...")
skt_eq_results = []
for seed in range(N_SEEDS):
    m, s = run_sa(skt_fixed_eq, skt_free_eq, skt_ranked, inscriptions, skt_bigrams,
                  n_iters=N_ITERS, seed=seed)
    skt_eq_results.append((s, m))
    print(f"  Seed {seed}: {s:.1f}")

skt_eq_best_s, skt_eq_best_m = max(skt_eq_results, key=lambda x: x[0])
print(f"Best equalized Sanskrit score: {skt_eq_best_s:.1f}")
print("Computing Sanskrit null (500 perms)...")
skt_eq_nm, skt_eq_nstd, skt_eq_z, skt_eq_p = perm_null(
    skt_eq_best_m, inscriptions, skt_bigrams)
skt_eq_lift = (skt_eq_best_s - skt_eq_nm) / max(1, len(inscriptions))
print(f"  Null={skt_eq_nm:.1f}±{skt_eq_nstd:.1f}, Z={skt_eq_z:.2f}, p={skt_eq_p:.4f}, "
      f"lift/insc={skt_eq_lift:.3f}")

drav_wins_eq = drav_eq_lift > skt_eq_lift
lift_ratio = drav_eq_lift / max(abs(skt_eq_lift), 0.001)

t7_result = {
    "experiment": "Phase-35 T7: Equalized Sanskrit SA",
    "n_vocab_sanskrit": len(skt_ranked),
    "n_fixed_anchors": len(skt_fixed_eq),
    "n_free_signs": len(skt_free_eq),
    "best_score": round(skt_eq_best_s, 3),
    "null_mean": round(skt_eq_nm, 3),
    "null_std": round(skt_eq_nstd, 3),
    "z_score": round(skt_eq_z, 3),
    "p_value": round(skt_eq_p, 4),
    "nll_lift_per_inscription": round(skt_eq_lift, 4),
    "significant_at_05": skt_eq_p < 0.05,
    "dravidian_t1_equalized_lift": round(drav_eq_lift, 4),
    "dravidian_t1_equalized_z": round(drav_eq_z, 3),
    "dravidian_wins": drav_wins_eq,
    "lift_ratio_drav_over_skt": round(lift_ratio, 3),
    "seed_scores": [round(s,1) for s,_ in skt_eq_results],
    "verdict": (
        f"Phase-35 T7 Equalized Sanskrit SA (vocab={len(skt_ranked)} syllables): "
        f"score={skt_eq_best_s:.1f}, null={skt_eq_nm:.1f}±{skt_eq_nstd:.1f}, "
        f"Z={skt_eq_z:.2f}, p={skt_eq_p:.4f}, lift/insc={skt_eq_lift:.3f}. "
        f"Dravidian lift={drav_eq_lift:.3f} — "
        f"{'Dravidian WINS (lift ratio=' + str(round(lift_ratio,2)) + 'x)' if drav_wins_eq else 'Sanskrit >= Dravidian — weakens hypothesis'}. "
        f"Runtime={time.time()-t0:.0f}s."
    ),
    "runtime_seconds": round(time.time()-t0, 1),
    "_citation": {"primary": ["A.1","E.1"], "phase": "Phase-35-T7"},
}
(REPORTS / "phase35_t7_equalized_sanskrit_sa.json").write_text(
    json.dumps(t7_result, indent=2, ensure_ascii=False), "utf-8")
print(f"  Saved phase35_t7_equalized_sanskrit_sa.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# EXP D — LM Quality Analysis: DEDR vs DEDR+CleanTB combined
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("EXP D: LM quality analysis — DEDR-only vs DEDR+cleanTB merged")
t0 = time.time()

# Load clean TB LM
clean_tb_path = DATA / "mahadevan_2003_tb_lm_clean.json"
clean_tb_bigrams: dict[tuple[str,str], float] = {}
clean_tb_vocab: list[str] = []
if clean_tb_path.exists():
    clean_tb_bigrams, clean_tb_vocab = load_lm("mahadevan_2003_tb_lm_clean.json")
    print(f"Clean TB LM: {len(clean_tb_vocab)} syllables, {len(clean_tb_bigrams)} bigrams")

# Merge DEDR + clean TB bigrams (average log-probs, add new bigrams)
merged_bigrams: dict[tuple[str,str], float] = {}
# First, take all DEDR bigrams
for bg, lp in drav_bigrams.items():
    merged_bigrams[bg] = lp
# Add/blend clean TB bigrams
for bg, lp in clean_tb_bigrams.items():
    if bg in merged_bigrams:
        # Log-sum blend: weight DEDR 70%, cleanTB 30%
        merged_bigrams[bg] = 0.7 * merged_bigrams[bg] + 0.3 * lp
    else:
        merged_bigrams[bg] = lp
print(f"Merged LM: {len(merged_bigrams)} bigrams (DEDR {len(drav_bigrams)} + cleanTB {len(clean_tb_bigrams)} → {len(merged_bigrams)} merged)")

# Score the best Dravidian mapping with merged LM
merged_score = score_mapping(drav_eq_best_m, inscriptions, merged_bigrams)
dedr_score = score_mapping(drav_eq_best_m, inscriptions, drav_bigrams_eq)
print(f"Score with DEDR-only (truncated): {dedr_score:.1f}")
print(f"Score with merged DEDR+cleanTB: {merged_score:.1f}")

# Save merged LM as the new canonical Dravidian syllable LM
merged_vocab = drav_ranked[:]  # keep full vocab order from DEDR
# Add any clean TB syllables not in DEDR
for syl in clean_tb_vocab:
    if syl not in drav_vocab_full:
        merged_vocab.append(syl)
# Convert to bigram_freq string keys
merged_bigrams_str = {f"{a}|{b}": round(lp, 6) for (a,b),lp in merged_bigrams.items()}

merged_lm_out = {
    "_citation": {
        "primary_sources": ["E.1", "A.12"],
        "derivation": (
            "Merged DEDR-based Dravidian syllable LM (2293 bigrams) with "
            "clean Mahadevan 2003 Tamil-Brahmi LM (Phase-33 T3, 1128 bigrams). "
            "Blend: 70% DEDR weight + 30% clean TB weight for shared bigrams. "
            "Unique bigrams from each source added directly."
        ),
        "authors": (
            "Burrow, T. & Emeneau, M.B. (1984). A Dravidian Etymological Dictionary. "
            "Mahadevan, I. (2003). Early Tamil Epigraphy, Harvard Oriental Series 62."
        ),
    },
    "language": "dravidian_merged",
    "phase": "Phase-35",
    "n_bigrams": len(merged_bigrams),
    "n_syllables": len(merged_vocab),
    "vocab": merged_vocab,
    "bigrams": merged_bigrams_str,
}
merged_lm_path = DATA / "dravidian_syllable_lm_merged.json"
merged_lm_path.write_text(json.dumps(merged_lm_out, indent=2, ensure_ascii=False), "utf-8")
print(f"Saved merged LM: {merged_lm_path} ({merged_lm_path.stat().st_size // 1024}KB)")

lm_quality = {
    "dedr_only_bigrams": len(drav_bigrams),
    "clean_tb_bigrams": len(clean_tb_bigrams),
    "merged_bigrams": len(merged_bigrams),
    "merged_vocab": len(merged_vocab),
    "score_dedr_only": round(dedr_score, 1),
    "score_merged": round(merged_score, 1),
    "score_delta": round(merged_score - dedr_score, 1),
    "merged_lm_file": str(merged_lm_path),
    "verdict": (
        f"LM quality analysis: DEDR {len(drav_bigrams)} + cleanTB {len(clean_tb_bigrams)} → "
        f"{len(merged_bigrams)} merged bigrams. "
        f"Score delta with merged LM: {merged_score - dedr_score:.1f} "
        f"({'better' if merged_score > dedr_score else 'worse or same'} fit). "
        f"Merged LM saved as dravidian_syllable_lm_merged.json."
    ),
    "runtime_seconds": round(time.time()-t0, 1),
    "_citation": {"primary": ["E.1","A.12"], "phase": "Phase-35-LMQuality"},
}
(REPORTS / "phase35_lm_quality.json").write_text(
    json.dumps(lm_quality, indent=2, ensure_ascii=False), "utf-8")
print(f"  Saved phase35_lm_quality.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("Phase-35 complete. Results:")
for fn in [
    "phase35_t1_equalized_dravidian_sa.json",
    "phase35_t7_equalized_sanskrit_sa.json",
    "phase35_lm_quality.json",
]:
    p = REPORTS / fn
    size = p.stat().st_size if p.exists() else 0
    print(f"  {'OK' if p.exists() else 'MISSING'} {fn} ({size//1024}KB)")

anchor_audit["_phase35_summary"] = {
    "active_anchors_augmented": len(drav_fixed_eq),
    "equalized_vocab_size": N_EQUALIZED,
    "dravidian_eq_z": round(drav_eq_z, 3),
    "dravidian_eq_lift": round(drav_eq_lift, 4),
    "sanskrit_eq_z": round(skt_eq_z, 3),
    "sanskrit_eq_lift": round(skt_eq_lift, 4),
    "dravidian_wins": drav_wins_eq,
    "lift_ratio": round(lift_ratio, 3),
}
(REPORTS / "phase35_anchor_audit.json").write_text(
    json.dumps(anchor_audit, indent=2, ensure_ascii=False), "utf-8")

print(f"\nControlled comparison (equalized vocab={N_EQUALIZED} syllables):")
print(f"  Dravidian T1: Z={drav_eq_z:.2f}, p={drav_eq_p:.4f}, lift/insc={drav_eq_lift:.3f}, anchors={len(drav_fixed_eq)}")
print(f"  Sanskrit T7:  Z={skt_eq_z:.2f}, p={skt_eq_p:.4f}, lift/insc={skt_eq_lift:.3f}, anchors={len(skt_fixed_eq)}")
print(f"  Dravidian wins: {drav_wins_eq} (ratio {lift_ratio:.2f}x)")
print(f"  VERDICT: {'Dravidian hypothesis SURVIVES controlled falsification' if drav_wins_eq else 'Sanskrit competitive under equalized conditions — [UNCERTAIN]'}")
