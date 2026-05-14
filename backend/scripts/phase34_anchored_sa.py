"""Phase-34 T1: Anchored Syllable SA — with sign-ID namespace fix.

Root cause fixed:
  INDUS_FINAL_ANCHORS keys use M-number format ("M047", "M099")
  M77 corpus uses 3-digit zero-padded strings ("047", "099")
  → strip the leading "M" when building corpus-matched anchor dict

Experiments:
  1. Phase-34 T1: Anchored Dravidian Syllable SA (M77 → Dravidian syllable LM)
  2. Phase-34 T7: Anchored Sanskrit Syllable SA  (M77 → Sanskrit syllable LM)
  3. Phase-34 Sign-Reading: Top-50 sign candidate syllable readings from best SA mapping

Citations:
  A.1  — M77 corpus (Mahadevan 1977)
  C.2  — Parpola 2010 phoneme map
  E.1  — DEDR (Burrow & Emeneau 1984)
  A.12 — Mahadevan 2003 TB
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

# ── Corpus loading ─────────────────────────────────────────────────────────────
def load_corpus() -> tuple[list[list[str]], Counter]:
    """Load M77 Holdat corpus. Sign IDs are 3-digit zero-padded strings."""
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    inscriptions = get_corpus_inscriptions()
    flat = get_corpus_symbols()
    print(f"M77 corpus: {len(inscriptions)} inscriptions, {len(flat)} tokens")
    return inscriptions, Counter(flat)

# ── Syllable LM loading ────────────────────────────────────────────────────────
def load_syllable_lm(name: str) -> tuple[dict, list[str]]:
    """Load syllable LM bigrams and vocab. Returns (bigrams_dict, ranked_vocab)."""
    lm_raw = json.loads((DATA / name).read_text("utf-8"))
    bigrams_raw = lm_raw.get("bigrams", lm_raw.get("bigram_freq", {}))
    bigrams: dict[tuple[str, str], float] = {}
    for key, logp in bigrams_raw.items():
        parts = key.split("|") if "|" in key else key.split(",") if "," in key else [key]
        if len(parts) == 2:
            try:
                bigrams[(parts[0].strip(), parts[1].strip())] = float(logp)
            except (ValueError, TypeError):
                pass
    freq: Counter = Counter()
    for (a, b) in bigrams:
        freq[a] += 1; freq[b] += 1
    ranked = lm_raw.get("vocab", []) or [s for s, _ in freq.most_common()]
    return bigrams, ranked

# ── Anchor loading — FIXED ─────────────────────────────────────────────────────
_DIACRITIC_MAP = {
    "ā": "a", "ī": "i", "ū": "u", "ṉ": "n", "ṟ": "r", "ḷ": "l",
    "ḻ": "l", "ṛ": "r", "ṭ": "t", "ḍ": "d", "ṅ": "n", "ṇ": "n",
    "ñ": "n", "ś": "s", "ṣ": "s", "ḥ": "h",
}

def _strip_diacritics(s: str) -> str:
    out = []
    for ch in unicodedata.normalize("NFD", s):
        plain = _DIACRITIC_MAP.get(ch)
        if plain:
            out.append(plain)
        elif unicodedata.category(ch) != "Mn":
            out.append(ch)
    return "".join(out)

def _split_syllables(word: str) -> list[str]:
    VOWELS = set("aeiouāīū")
    CONSONANTS = set("bcdfghjklmnpqrstvwxyz")
    syllables: list[str] = []
    i = 0; current = ""
    while i < len(word):
        c = word[i]
        current += c
        if c in VOWELS:
            if (i + 1 < len(word) and word[i+1] in CONSONANTS and
                    (i + 2 >= len(word) or word[i+2] in VOWELS)):
                i += 1
                current += word[i]
            syllables.append(current)
            current = ""
        elif len(current) >= 3:
            syllables.append(current); current = ""
        i += 1
    if current:
        if syllables: syllables[-1] += current
        else: syllables.append(current)
    return [s for s in syllables if len(s) >= 1]

def _to_syllable(reading: str, syllable_vocab: set[str]) -> str | None:
    """Convert a Tamil word reading to a syllable token from the LM vocab."""
    reading = reading.split("/")[0].strip()
    reading = re.sub(r"\(.*?\)", "", reading).strip()
    reading = reading.rstrip("?")
    if re.match(r"(term|med|init|ctx|role)[-:]", reading.lower()):
        return None
    if not reading or "uncertain" in reading.lower() or reading in ("?", "-"):
        return None
    clean = _strip_diacritics(reading)
    clean = re.sub(r"[^a-z]", "", clean)
    if not clean:
        return None
    if clean in syllable_vocab:
        return clean
    for s in _split_syllables(clean):
        if s in syllable_vocab:
            return s
    for length in (2, 3, 1):
        if len(clean) >= length:
            candidate = clean[:length]
            if candidate in syllable_vocab:
                return candidate
    return clean[:3] if len(clean) > 3 else clean

def load_anchors(syllable_vocab: set[str]) -> dict[str, str]:
    """Load anchors from Parpola + INDUS_FINAL_ANCHORS.

    KEY FIX: INDUS_FINAL_ANCHORS uses M-number keys ("M047").
    M77 corpus uses zero-padded 3-digit strings ("047").
    Strip the leading "M" to bridge the namespace.
    """
    anchors: dict[str, str] = {}

    # --- Parpola phonemes (keys are plain integers "47", "1", etc.) ---
    pp_path = DATA / "parpola_phonemes.json"
    if pp_path.exists():
        raw = json.loads(pp_path.read_text("utf-8"))
        phmap = raw.get("phoneme_map", {})
        if isinstance(phmap, dict):
            for sid, info in phmap.items():
                if isinstance(info, dict):
                    pv = info.get("phoneme", info.get("phoneme_value", ""))
                    conf = info.get("confidence", "low")
                    if pv and conf in ("high", "medium") and "?" not in pv:
                        syll = _to_syllable(pv, syllable_vocab)
                        if syll:
                            anchors[sid] = syll
                            # Also add zero-padded version for M77 corpus format
                            if sid.isdigit():
                                anchors[sid.zfill(3)] = syll

    # --- INDUS_FINAL_ANCHORS (keys are "M047" format) ---
    fa_path = BACKEND_REPORTS / "INDUS_FINAL_ANCHORS.json"
    if fa_path.exists():
        fa = json.loads(fa_path.read_text("utf-8"))
        loaded = 0
        for m_id, info in fa.get("anchors", {}).items():
            if info.get("confidence") not in ("HIGH", "MEDIUM"):
                continue
            reading = info.get("reading", "")
            if "?" in reading:
                continue
            syll = _to_syllable(reading, syllable_vocab)
            if not syll:
                continue
            # Original M-number key (e.g., "M047")
            anchors[m_id] = syll
            # *** THE FIX: also add the M77-format key (e.g., "047") ***
            if m_id.startswith("M") and m_id[1:].isdigit():
                anchors[m_id[1:]] = syll  # "047"
            loaded += 1
        print(f"INDUS_FINAL_ANCHORS: {loaded} HIGH/MEDIUM anchors loaded (M-prefix stripped)")

    return anchors

# ── Scoring + SA ───────────────────────────────────────────────────────────────
def score_mapping(
    mapping: dict[str, str],
    inscriptions: list[list[str]],
    bigrams: dict[tuple[str, str], float],
) -> float:
    total = 0.0
    for insc in inscriptions:
        for i in range(len(insc) - 1):
            a = mapping.get(insc[i]); b = mapping.get(insc[i+1])
            if a and b:
                total += bigrams.get((a, b), SMOOTHING_LOG)
    return total

def run_sa(
    fixed: dict[str, str],
    free: list[str],
    vocab: list[str],
    inscriptions: list[list[str]],
    bigrams: dict[tuple[str, str], float],
    n_iters: int = 30_000,
    seed: int = 42,
) -> tuple[dict[str, str], float]:
    rng = random.Random(seed)
    if not vocab:
        return dict(fixed), score_mapping(fixed, inscriptions, bigrams)
    free_target = [sv for sv in vocab if sv not in fixed.values()]
    while len(free_target) < len(free):
        free_target.append(rng.choice(vocab))
    rng.shuffle(free_target)
    mapping = dict(fixed)
    for i, sign in enumerate(free):
        mapping[sign] = free_target[i % len(free_target)]
    current_score = score_mapping(mapping, inscriptions, bigrams)
    best_mapping = dict(mapping); best_score = current_score
    T_start, T_end = 2.0, 0.01
    for iteration in range(n_iters):
        T = T_start * ((T_end / T_start) ** (iteration / n_iters))
        if len(free) < 2: break
        i, j = rng.sample(range(len(free)), 2)
        si, sj = free[i], free[j]
        vi, vj = mapping[si], mapping[sj]
        mapping[si], mapping[sj] = vj, vi
        new_score = score_mapping(mapping, inscriptions, bigrams)
        delta = new_score - current_score
        if delta > 0 or rng.random() < math.exp(delta / max(T, 1e-10)):
            current_score = new_score
            if new_score > best_score:
                best_score = new_score; best_mapping = dict(mapping)
        else:
            mapping[si], mapping[sj] = vi, vj
    return best_mapping, best_score

def permutation_null(
    best_mapping: dict[str, str],
    inscriptions: list[list[str]],
    bigrams: dict[tuple[str, str], float],
    n_perms: int = 500,
    seed: int = 99,
) -> tuple[float, float, float, float]:
    rng = random.Random(seed)
    observed = score_mapping(best_mapping, inscriptions, bigrams)
    keys = list(best_mapping.keys()); vals = list(best_mapping.values())
    null_scores = []
    for _ in range(n_perms):
        shuffled = vals[:]; rng.shuffle(shuffled)
        null_scores.append(score_mapping(dict(zip(keys, shuffled)), inscriptions, bigrams))
    null_mean = sum(null_scores) / len(null_scores)
    null_std = math.sqrt(sum((s - null_mean)**2 for s in null_scores) / len(null_scores))
    z = (observed - null_mean) / null_std if null_std > 0 else 0.0
    pval = sum(1 for s in null_scores if s >= observed) / n_perms
    return null_mean, null_std, z, pval

# ── Load shared data ───────────────────────────────────────────────────────────
print("=" * 65)
print("Phase-34: Loading shared data...")

drav_bigrams, drav_ranked = load_syllable_lm("dravidian_syllable_lm.json")
drav_vocab = set(drav_ranked)
print(f"Dravidian syllable LM: {len(drav_ranked)} syllables, {len(drav_bigrams)} bigrams")

inscriptions, sign_freq = load_corpus()
cipher_signs = [s for s, c in sign_freq.items() if c >= 3]
print(f"Signs with freq>=3: {len(cipher_signs)}")

all_anchors = load_anchors(drav_vocab)
# Filter to signs actually present in corpus
corpus_anchors = {s: r for s, r in all_anchors.items() if s in sign_freq}
print(f"Total anchors loaded: {len(all_anchors)}")
print(f"Anchors active in corpus: {len(corpus_anchors)}")
if corpus_anchors:
    sample = list(corpus_anchors.items())[:8]
    print(f"  Sample: {sample}")

# ════════════════════════════════════════════════════════════════════════════════
# EXP 1 — Phase-34 T1: Anchored Dravidian Syllable SA
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("EXP 1: Phase-34 T1 — Anchored Dravidian Syllable SA")
t0 = time.time()

drav_fixed = {s: r for s, r in corpus_anchors.items() if r in drav_vocab}
drav_free = [s for s in cipher_signs if s not in drav_fixed]
print(f"Fixed (anchored) signs: {len(drav_fixed)}")
print(f"Free signs (to be assigned): {len(drav_free)}")

N_SEEDS, N_ITERS = 5, 30_000
print(f"Running anchored Dravidian SA: {N_SEEDS} seeds × {N_ITERS} iters...")
drav_seed_results = []
for seed in range(N_SEEDS):
    m, s = run_sa(drav_fixed, drav_free, drav_ranked, inscriptions, drav_bigrams,
                  n_iters=N_ITERS, seed=seed)
    drav_seed_results.append((s, m))
    print(f"  Seed {seed}: {s:.1f}")

drav_best_score, drav_best_map = max(drav_seed_results, key=lambda x: x[0])
print(f"Best anchored Dravidian SA score: {drav_best_score:.1f}")
print("Computing null (500 perms)...")
drav_null_mean, drav_null_std, drav_z, drav_pval = permutation_null(
    drav_best_map, inscriptions, drav_bigrams, n_perms=500)
drav_lift = (drav_best_score - drav_null_mean) / max(1, len(inscriptions))
print(f"  Null={drav_null_mean:.1f}±{drav_null_std:.1f}, Z={drav_z:.2f}, p={drav_pval:.4f}, "
      f"lift/insc={drav_lift:.3f}")

# Sample decoded inscriptions
sample_decoded = []
for insc in sorted(inscriptions, key=len, reverse=True)[:15]:
    decoded = "-".join(drav_best_map.get(s, f"?{s}") for s in insc)
    n_map = sum(1 for s in insc if s in drav_best_map)
    sample_decoded.append({"signs": insc, "syllables": decoded,
                            "coverage": round(n_map / len(insc), 2)})

t1_result = {
    "experiment": "Phase-34 T1: Anchored Dravidian Syllable SA",
    "best_score": round(drav_best_score, 3),
    "null_mean": round(drav_null_mean, 3),
    "null_std": round(drav_null_std, 3),
    "z_score": round(drav_z, 3),
    "p_value": round(drav_pval, 4),
    "n_permutations": 500,
    "n_fixed_anchors": len(drav_fixed),
    "n_free_signs": len(drav_free),
    "nll_lift_per_inscription": round(drav_lift, 4),
    "significant_at_05": drav_pval < 0.05,
    "fixed_anchors": drav_fixed,
    "seed_scores": [round(s, 1) for s, _ in drav_seed_results],
    "sample_decoded": sample_decoded,
    "verdict": (
        f"Phase-34 T1 Anchored Dravidian SA (namespace fixed): score={drav_best_score:.1f}, "
        f"null={drav_null_mean:.1f}±{drav_null_std:.1f}, Z={drav_z:.2f}, p={drav_pval:.4f}. "
        f"NLL lift/inscription={drav_lift:.3f}. "
        f"Anchors={len(drav_fixed)} (M77-format, syllabified). "
        f"{'SIGNIFICANT (p<0.05)' if drav_pval < 0.05 else 'NOT SIGNIFICANT'}. "
        f"Runtime={time.time()-t0:.0f}s."
    ),
    "runtime_seconds": round(time.time() - t0, 1),
    "_citation": {"primary": ["A.1", "E.1", "C.2"], "phase": "Phase-34-T1"},
}
(REPORTS / "phase34_t1_anchored_dravidian_sa.json").write_text(
    json.dumps(t1_result, indent=2, ensure_ascii=False), "utf-8")
print(f"  Saved phase34_t1_anchored_dravidian_sa.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# EXP 2 — Phase-34 T7: Anchored Sanskrit Syllable SA (falsification)
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("EXP 2: Phase-34 T7 — Anchored Sanskrit Syllable SA (falsification)")
t0 = time.time()

skt_path = DATA / "sanskrit_syllable_lm.json"
skt_bigrams: dict[tuple[str, str], float] = {}
skt_ranked: list[str] = []
if skt_path.exists():
    skt_bigrams, skt_ranked = load_syllable_lm("sanskrit_syllable_lm.json")
    print(f"Sanskrit LM: {len(skt_ranked)} syllables, {len(skt_bigrams)} bigrams")

t7_result: dict = {}
if skt_bigrams and skt_ranked:
    skt_vocab = set(skt_ranked)
    # Re-load anchors syllabified against Sanskrit vocab for fair comparison
    skt_corpus_anchors = load_anchors(skt_vocab)
    skt_corpus_anchors = {s: r for s, r in skt_corpus_anchors.items() if s in sign_freq}
    skt_fixed = {s: r for s, r in skt_corpus_anchors.items() if r in skt_vocab}
    skt_free = [s for s in cipher_signs if s not in skt_fixed]
    print(f"Sanskrit fixed anchors: {len(skt_fixed)}, free: {len(skt_free)}")

    print(f"Running anchored Sanskrit SA: {N_SEEDS} seeds × {N_ITERS} iters...")
    skt_seed_results = []
    for seed in range(N_SEEDS):
        m, s = run_sa(skt_fixed, skt_free, skt_ranked, inscriptions, skt_bigrams,
                      n_iters=N_ITERS, seed=seed)
        skt_seed_results.append((s, m))
        print(f"  Seed {seed}: {s:.1f}")

    skt_best_score, skt_best_map = max(skt_seed_results, key=lambda x: x[0])
    print(f"Best Sanskrit SA score: {skt_best_score:.1f}")
    print("Computing Sanskrit null (500 perms)...")
    skt_null_mean, skt_null_std, skt_z, skt_pval = permutation_null(
        skt_best_map, inscriptions, skt_bigrams, n_perms=500)
    skt_lift = (skt_best_score - skt_null_mean) / max(1, len(inscriptions))
    print(f"  Null={skt_null_mean:.1f}±{skt_null_std:.1f}, Z={skt_z:.2f}, p={skt_pval:.4f}, "
          f"lift/insc={skt_lift:.3f}")

    drav_wins = drav_lift > skt_lift
    t7_result = {
        "experiment": "Phase-34 T7: Anchored Sanskrit Syllable SA",
        "best_score": round(skt_best_score, 3),
        "null_mean": round(skt_null_mean, 3),
        "null_std": round(skt_null_std, 3),
        "z_score": round(skt_z, 3),
        "p_value": round(skt_pval, 4),
        "n_permutations": 500,
        "n_fixed_anchors": len(skt_fixed),
        "nll_lift_per_inscription": round(skt_lift, 4),
        "significant_at_05": skt_pval < 0.05,
        "dravidian_t1_score": round(drav_best_score, 3),
        "dravidian_t1_z": round(drav_z, 3),
        "dravidian_t1_lift": round(drav_lift, 4),
        "dravidian_wins": drav_wins,
        "lift_ratio_drav_over_skt": round(drav_lift / max(abs(skt_lift), 0.001), 3),
        "seed_scores": [round(s, 1) for s, _ in skt_seed_results],
        "verdict": (
            f"Phase-34 T7 Anchored Sanskrit SA: score={skt_best_score:.1f}, "
            f"null={skt_null_mean:.1f}±{skt_null_std:.1f}, Z={skt_z:.2f}, p={skt_pval:.4f}. "
            f"lift/insc={skt_lift:.3f} vs Dravidian={drav_lift:.3f}. "
            f"{'Dravidian WINS falsification' if drav_wins else 'Sanskrit >= Dravidian — weakens hypothesis'}. "
            f"Runtime={time.time()-t0:.0f}s."
        ),
        "runtime_seconds": round(time.time() - t0, 1),
        "_citation": {"primary": ["A.1", "E.1"], "phase": "Phase-34-T7"},
    }
else:
    t7_result = {
        "error": "Sanskrit LM not available",
        "verdict": "Phase-34 T7 INCOMPLETE: Sanskrit syllable LM not found.",
        "_citation": {"primary": ["A.1"], "phase": "Phase-34-T7"},
    }

(REPORTS / "phase34_t7_anchored_sanskrit_sa.json").write_text(
    json.dumps(t7_result, indent=2, ensure_ascii=False), "utf-8")
print(f"  Saved phase34_t7_anchored_sanskrit_sa.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# EXP 3 — Phase-34 Sign-Reading: Top-50 candidate syllable readings
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("EXP 3: Phase-34 Sign-Reading — Top-50 candidate syllable assignments")
t0 = time.time()

top50_signs = [s for s, _ in sign_freq.most_common(50)]
sign_readings: list[dict] = []
for rank, sign in enumerate(top50_signs, 1):
    freq_count = sign_freq[sign]
    is_anchored = sign in drav_fixed
    drav_reading = drav_best_map.get(sign, "—")
    skt_reading = t7_result.get("best_score") and skt_best_map.get(sign, "—") if t7_result and "best_score" in t7_result else "—"

    # Positional class from corpus
    t_rate = sum(1 for insc in inscriptions if insc and insc[-1] == sign and len(insc) > 1) / max(freq_count, 1)
    i_rate = sum(1 for insc in inscriptions if insc and insc[0] == sign and len(insc) > 1) / max(freq_count, 1)
    pos_class = "TERMINAL" if t_rate >= 0.4 else "INITIAL" if i_rate >= 0.4 else "MIXED"

    # Agreement across seeds
    all_readings = [m.get(sign, "") for _, m in drav_seed_results]
    most_common_reading, mc_count = Counter(all_readings).most_common(1)[0]
    agreement_pct = round(mc_count / N_SEEDS * 100)

    sign_readings.append({
        "rank": rank,
        "sign": sign,
        "freq": freq_count,
        "is_anchored": is_anchored,
        "anchor_reading": drav_fixed.get(sign, ""),
        "sa_reading_dravidian": drav_reading,
        "sa_reading_sanskrit": skt_reading if isinstance(skt_reading, str) else "—",
        "seed_agreement_pct": agreement_pct,
        "positional_class": pos_class,
        "t_rate": round(t_rate, 3),
        "i_rate": round(i_rate, 3),
    })

    status = "ANCHOR" if is_anchored else f"SA={drav_reading}({agreement_pct}%)"
    print(f"  #{rank:2d} Sign {sign:>4s}  freq={freq_count:4d}  {pos_class:8s}  {status}")

sign_reading_result = {
    "experiment": "Phase-34 Sign-Reading: Top-50 candidate syllable readings",
    "n_signs": len(sign_readings),
    "n_anchored": sum(1 for r in sign_readings if r["is_anchored"]),
    "n_sa_assigned": sum(1 for r in sign_readings if not r["is_anchored"]),
    "sign_readings": sign_readings,
    "verdict": (
        f"Phase-34 Sign-Reading: {len(sign_readings)} top-50 signs. "
        f"{sum(1 for r in sign_readings if r['is_anchored'])} are anchored (fixed readings). "
        f"{sum(1 for r in sign_readings if not r['is_anchored'])} are SA-assigned. "
        f"Average seed agreement: "
        f"{sum(r['seed_agreement_pct'] for r in sign_readings) / len(sign_readings):.0f}%."
    ),
    "runtime_seconds": round(time.time() - t0, 1),
    "_citation": {"primary": ["A.1", "C.2", "E.1"], "phase": "Phase-34-SignReading"},
}
(REPORTS / "phase34_sign_reading_top50.json").write_text(
    json.dumps(sign_reading_result, indent=2, ensure_ascii=False), "utf-8")
print(f"  Saved phase34_sign_reading_top50.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("Phase-34 session complete. Results:")
for fn in [
    "phase34_t1_anchored_dravidian_sa.json",
    "phase34_t7_anchored_sanskrit_sa.json",
    "phase34_sign_reading_top50.json",
]:
    p = REPORTS / fn
    size = p.stat().st_size if p.exists() else 0
    print(f"  {'OK' if p.exists() else 'MISSING'} {fn} ({size // 1024}KB)")

# Quick comparison summary
t1_z = t1_result.get("z_score", 0)
t1_p = t1_result.get("p_value", 1)
t7_z = t7_result.get("z_score", 0)
drav_wins_final = t1_result.get("nll_lift_per_inscription", 0) > t7_result.get("nll_lift_per_inscription", 0)
print(f"\nComparison (anchored):")
print(f"  Dravidian T1: Z={t1_z}, p={t1_p}, anchors={t1_result.get('n_fixed_anchors',0)}")
print(f"  Sanskrit T7:  Z={t7_z}, p={t7_result.get('p_value',1)}, anchors={t7_result.get('n_fixed_anchors',0)}")
print(f"  Dravidian wins: {drav_wins_final}")
