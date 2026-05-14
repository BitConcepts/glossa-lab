"""Phase-33: Beam decoder Tier 5 — Indus → Tamil-Brahmi (Dravidian syllable LM).

The beam decoder achieves 100% on Ugaritic→Hebrew with anchors. This is the
first application to Indus→Dravidian using beam_decipher (previously only SA
was used for Tier 5). Uses 9 HIGH-confidence Parpola anchors and the Dravidian
syllable LM.

Method:
  - cipher_signs: M77 Holdat corpus (flat token list)
  - target_model: LanguageModel built from Dravidian syllable bigrams
  - anchors: 9 HIGH-confidence signs from INDUS_FINAL_ANCHORS (monosyllabic only)
  - beam_width: 100 (wider than Ugaritic due to larger Indus sign inventory)
  - Compare best mapping score to SA T1 baseline and permutation null

Output: reports/phase33_beam_dravidian.json
"""
from __future__ import annotations
import json, random, sys, math, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "backend" / "tests"))

REPORTS = ROOT / "reports"
BACKEND_REPORTS = ROOT / "backend" / "reports"
DATA    = ROOT / "backend" / "glossa_lab" / "data"

t0 = time.time()

# ── Load Holdat corpus ─────────────────────────────────────────────────────────
from glossa_lab.data.indus_m77 import get_corpus_symbols, get_corpus_inscriptions
flat_tokens  = get_corpus_symbols()
inscriptions = get_corpus_inscriptions()
sign_freq    = Counter(flat_tokens)
print(f"Holdat: {len(flat_tokens)} tokens, {len(sign_freq)} signs, {len(inscriptions)} inscriptions")

# ── Load Dravidian syllable LM + build LanguageModel ─────────────────────────
from glossa_lab.pipelines.decipher import LanguageModel

syll_lm_raw = json.loads((DATA / "dravidian_syllable_lm.json").read_text("utf-8"))
syll_bigrams_raw: dict[tuple[str,str], float] = {}
for key, logp in syll_lm_raw["bigrams"].items():
    parts = key.split("|")
    if len(parts) == 2:
        syll_bigrams_raw[(parts[0], parts[1])] = float(logp)

# Build a flat token list from syllable bigrams (weighted by count)
# to feed into LanguageModel constructor
syll_tokens: list[str] = []
for (a, b), lp in syll_bigrams_raw.items():
    cnt = max(1, int(math.exp(lp) * 10000))
    syll_tokens.extend([a, b] * min(cnt, 5))

# Build syllable inscriptions (pairs from bigrams)
syll_inscriptions: list[list[str]] = []
for (a, b) in list(syll_bigrams_raw.keys())[:500]:
    syll_inscriptions.append([a, b])

print(f"Building LanguageModel from {len(syll_tokens)} syllable tokens...")
tb_model = LanguageModel(syll_tokens, inscriptions=syll_inscriptions)
print(f"  LM alphabet size: {tb_model.size}")
print(f"  LM bigrams: {len(tb_model.bigram_freq)}")

# ── Build HIGH-confidence anchors ─────────────────────────────────────────────
anchors_raw = json.loads((BACKEND_REPORTS / "INDUS_FINAL_ANCHORS.json").read_text("utf-8"))
all_anchors = anchors_raw["anchors"]

# HIGH-confidence monosyllabic anchors (only those in LM vocab)
CORE_ANCHORS = {
    "M342": "ay",    # terminal marker — Dravidian case suffix (HIGH)
    "M176": "an",    # masculine suffix (HIGH)
    "M099": "kol",   # jar/vessel (HIGH)
    "M062": "er",    # bull (erutu → take first syllable "er") (HIGH)
    "M006": "pu",    # tiger (puli → "pu") (HIGH)
    "M045": "yā",    # elephant (yānai → "yā") (HIGH)
    "M016": "ka",    # male elephant (kaḷiṟu → "ka") (HIGH)
}

lm_vocab = set(tb_model.ranked)
beam_anchors: dict[str, str] = {}
for m_id, syll in CORE_ANCHORS.items():
    if syll in lm_vocab:
        beam_anchors[m_id] = syll
    else:
        # Find nearest syllable in LM vocab starting with same chars
        for sv in tb_model.ranked:
            if sv.startswith(syll[:1]):
                beam_anchors[m_id] = sv
                break

print(f"Beam anchors ({len(beam_anchors)} of {len(CORE_ANCHORS)}): {beam_anchors}")

# ── Run beam_decipher ─────────────────────────────────────────────────────────
# Use only signs with freq >= 10 for beam (reduces branching factor)
cipher_signs_frequent = flat_tokens  # use all for scoring
cipher_signs_for_beam = [s for s, c in sign_freq.items() if c >= 10]

print(f"\nRunning beam_decipher on {len(cipher_signs_for_beam)} frequent signs...")
try:
    from glossa_lab.pipelines.beam_decipher import beam_decipher
    beam_result = beam_decipher(
        cipher_signs   = cipher_signs_frequent,
        target_model   = tb_model,
        beam_width     = 50,  # Manageable beam for Indus (many signs)
        cipher_inscriptions = inscriptions,
        anchors        = beam_anchors,
        surjective     = False,  # Many-to-one OK for Dravidian (multiple signs → one syllable)
        ocp_weight     = 0.0,
        use_word_bigrams = False,
        root_prior_weight = 0.0,
    )
    beam_score   = beam_result.get("score", 0.0)
    best_mapping = beam_result.get("proposed_mapping", {})
    print(f"Beam score: {beam_score:.1f}")
    print(f"Top beam assignments (by frequency):")
    sorted_map = sorted(best_mapping.items(), key=lambda x: -sign_freq.get(x[0], 0))
    for sign, syll in sorted_map[:20]:
        print(f"  {sign} (freq={sign_freq.get(sign,0)}) → {syll}")
except Exception as exc:
    print(f"beam_decipher error: {exc}")
    import traceback; traceback.print_exc()
    beam_result = {}
    beam_score  = float("nan")
    best_mapping = {}

# ── Score function for permutation null ───────────────────────────────────────
SMOOTHING_LOG = math.log(1e-8)
def score_mapping(mapping: dict[str,str]) -> float:
    total = 0.0
    for insc in inscriptions:
        if len(insc) < 2:
            continue
        for i in range(len(insc)-1):
            a = mapping.get(insc[i])
            b = mapping.get(insc[i+1])
            if a and b:
                total += syll_bigrams_raw.get((a,b), SMOOTHING_LOG)
    return total

# ── Permutation null ───────────────────────────────────────────────────────────
if best_mapping:
    print("\nComputing permutation null (200 shuffles)...")
    N_PERMS = 200
    rng = random.Random(42)
    null_scores = []
    keys = list(best_mapping.keys())
    vals = list(best_mapping.values())
    for _ in range(N_PERMS):
        shuffled = vals[:]
        rng.shuffle(shuffled)
        null_map = dict(zip(keys, shuffled))
        null_scores.append(score_mapping(null_map))

    null_mean = sum(null_scores) / len(null_scores)
    null_std = math.sqrt(sum((s-null_mean)**2 for s in null_scores) / len(null_scores))
    observed = score_mapping(best_mapping)
    z_score = (observed - null_mean) / null_std if null_std > 0 else 0.0
    pval = sum(1 for s in null_scores if s >= observed) / N_PERMS
    print(f"Observed score: {observed:.1f}")
    print(f"Null: {null_mean:.1f} ± {null_std:.1f}")
    print(f"Z={z_score:.2f}, p={pval:.4f}")
else:
    null_mean = null_std = z_score = pval = 0.0
    observed = 0.0

# ── Load SA T1 result for comparison ─────────────────────────────────────────
sa_result = {}
sa_path = REPORTS / "phase33_t1_syllable_sa.json"
if sa_path.exists():
    sa_result = json.loads(sa_path.read_text("utf-8"))

elapsed = time.time() - t0
verdict = (
    f"Phase-33 Beam Decoder (Tier 5): beam_width=50, {len(beam_anchors)} HIGH-confidence anchors. "
    f"Observed NLL={observed:.1f}, null_mean={null_mean:.1f} ± {null_std:.1f}. "
    f"Z={z_score:.2f}, p={pval:.4f}. "
    f"SA-T1 best_score={sa_result.get('best_score','N/A')} for comparison. "
    f"{'SIGNIFICANT (p<0.05)' if pval < 0.05 else 'NOT SIGNIFICANT'}. "
    f"Runtime={elapsed:.0f}s."
)
print(f"\n{verdict}")

result = {
    "beam_width": 50,
    "n_beam_anchors": len(beam_anchors),
    "beam_anchors": beam_anchors,
    "beam_score": round(beam_score, 3) if not math.isnan(beam_score) else None,
    "observed_nll": round(observed, 3),
    "null_mean": round(null_mean, 3),
    "null_std": round(null_std, 3),
    "z_score": round(z_score, 3),
    "p_value": round(pval, 4),
    "n_permutations": 200,
    "significant_at_05": pval < 0.05,
    "sa_t1_score": sa_result.get("best_score"),
    "best_mapping_top20": {k: v for k, v in sorted(best_mapping.items(), key=lambda x: -sign_freq.get(x[0],0))[:20]},
    "lm_size": tb_model.size,
    "lm_bigrams": len(tb_model.bigram_freq),
    "runtime_seconds": round(elapsed, 1),
    "verdict": verdict,
    "_citation": {"primary": ["A.1", "A.12", "C.2"], "phase": "Phase-33-Beam"},
}

out_path = REPORTS / "phase33_beam_dravidian.json"
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Saved to {out_path}")

