"""Quick fix: Build Sangam+TB combined syllable LM from actual corpus text.

Phase-39 T2 found the Sangam LM underperformed DEDR because:
  1. Only 1297 words → 381 unique syllables (below Sanskrit's 424)
  2. Bigrams from literary Tamil diverge from Proto-Dravidian patterns

Fix:
  - Use get_corpus_text() for syllable tokens (full corpus, not character-level)
  - Blend with DEDR bigrams (etymological) + clean TB inscriptions
  - Keep full natural vocabulary (no artificial 424-syllable cap on the source LM)
  - Result: dravidian_sangam_combined_lm.json with 2000+ raw bigrams

_citation: E.1 (DEDR), A.12 (Mahadevan 2003 TB)
"""
import json, math, re, sys, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
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

print("Building Sangam+TB combined Dravidian LM...")

# ── Source 1: Sangam corpus text (running syllabification) ────────────────────
from glossa_lab.data.dravidian import get_corpus_text
corpus_text = get_corpus_text()
words = re.findall(r"[a-z\u0b00-\u0bff\u0900-\u097f]+", corpus_text.lower())
sangam_tokens = []
for word in words:
    clean = _sd(word); clean = re.sub(r"[^a-z]", "", clean)
    if 2 <= len(clean) <= 20:
        sylls = _sylls(clean)
        sangam_tokens.extend(sylls if sylls else [clean[:3]])
print(f"  Sangam: {len(words)} words → {len(sangam_tokens)} syllable tokens")

# ── Source 2: Clean TB inscriptions (Phase-33 T3 cleaned) ────────────────────
tb_bigs_raw = {}
try:
    tb_lm = json.loads((DATA / "mahadevan_2003_tb_lm_clean.json").read_text("utf-8"))
    for key, lp in tb_lm.get("bigrams", {}).items():
        ps = key.split("|") if "|" in key else key.split(",")
        if len(ps) == 2:
            try: tb_bigs_raw[(ps[0].strip(), ps[1].strip())] = float(lp)
            except: pass
    print(f"  TB clean LM: {len(tb_bigs_raw)} bigrams")
except Exception as e:
    print(f"  TB LM unavailable: {e}")

# ── Source 3: Existing DEDR syllable LM (etymological) ───────────────────────
dedr_bigs_raw = {}
try:
    dedr_lm = json.loads((DATA / "dravidian_syllable_lm.json").read_text("utf-8"))
    for key, lp in dedr_lm.get("bigrams", {}).items():
        ps = key.split("|") if "|" in key else key.split(",")
        if len(ps) == 2:
            try: dedr_bigs_raw[(ps[0].strip(), ps[1].strip())] = float(lp)
            except: pass
    print(f"  DEDR syllable LM: {len(dedr_bigs_raw)} bigrams")
except Exception as e:
    print(f"  DEDR LM unavailable: {e}")

# ── Build Sangam bigrams from running text ─────────────────────────────────────
sangam_bg_count: Counter = Counter()
sangam_uni: Counter = Counter(sangam_tokens)
for i in range(len(sangam_tokens) - 1):
    sangam_bg_count[(sangam_tokens[i], sangam_tokens[i+1])] += 1
total_bg = sum(sangam_bg_count.values())
sangam_bigs = {(a, b): math.log(c / total_bg) for (a, b), c in sangam_bg_count.items() if c > 0}
print(f"  Sangam bigrams: {len(sangam_bigs)}")

# ── Blend: DEDR (50%) + Sangam (30%) + TB (20%) ───────────────────────────────
# DEDR is highest weight — most representative of Proto-Dravidian phonology
all_keys = set(dedr_bigs_raw) | set(sangam_bigs) | set(tb_bigs_raw)
blended = {}
for key in all_keys:
    d = dedr_bigs_raw.get(key, SMOOTHING)
    s = sangam_bigs.get(key, SMOOTHING)
    t = tb_bigs_raw.get(key, SMOOTHING)
    blended[key] = 0.50 * d + 0.30 * s + 0.20 * t

# Vocab: union of all sources, sorted by frequency
combined_uni = Counter(sangam_tokens)
# Add vocab from DEDR
for k in dedr_lm.get("vocab", []):
    combined_uni[k] = combined_uni.get(k, 0) + 1
vocab = [s for s, _ in combined_uni.most_common()]
print(f"  Combined vocab: {len(vocab)} syllables")
print(f"  Combined bigrams: {len(blended)}")

# ── Save ──────────────────────────────────────────────────────────────────────
out = {
    "_citation": {
        "primary_sources": ["E.1", "A.12"],
        "derivation": (
            "Sangam+TB+DEDR combined syllable LM. "
            "Sources: Dravidian corpus text (dravidian.py, Sangam poetry + Old Tamil), "
            "clean TB inscriptions (Phase-33 T3), DEDR etymological LM. "
            "Blend weights: DEDR 50% + Sangam 30% + TB 20%. "
            "No artificial vocab cap — full natural syllable inventory."
        ),
        "authors": "Burrow & Emeneau (1984) DEDR; Mahadevan (2003) TB; Sangam poets",
    },
    "language": "dravidian_sangam_combined",
    "n_bigrams": len(blended),
    "n_syllables": len(vocab),
    "vocab": vocab,
    "bigrams": {f"{a}|{b}": round(lp, 6) for (a, b), lp in blended.items()},
    "sources": {
        "sangam_tokens": len(sangam_tokens),
        "sangam_bigrams_raw": len(sangam_bigs),
        "tb_bigrams": len(tb_bigs_raw),
        "dedr_bigrams": len(dedr_bigs_raw),
    },
}
out_path = DATA / "dravidian_sangam_combined_lm.json"
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), "utf-8")
print(f"\nSaved: {out_path} ({out_path.stat().st_size // 1024}KB)")
print(f"  {len(vocab)} syllables | {len(blended)} bigrams")
print(f"  Top syllables: {vocab[:12]}")
print(f"  Blend: 50% DEDR + 30% Sangam + 20% TB")
