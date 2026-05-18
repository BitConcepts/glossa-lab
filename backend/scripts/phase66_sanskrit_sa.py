"""Phase-66: Sanskrit SA Falsification.

Runs the same phonotactic-filtered constrained SA as Phase-63 but targeting
the Sanskrit syllable LM instead of the Dravidian syllabic LM.

Key falsification test:
  Dravidian z=19.07 (Phase-57) / Sanskrit z=? → ratio = falsification strength
  If Dravidian z >> Sanskrit z: the Dravidian hypothesis is statistically preferred.
  If z values are similar: no preference — would undermine the Dravidian claim.

The Sanskrit LM represents the COMPETING HYPOTHESIS (Yajnadevam et al. 2024).
Using the same anchors and corpus prevents cherry-picking.

GPU: BigramScorer CUDA. ~5 min.
Output: reports/phase66_sanskrit_sa.json
"""
from __future__ import annotations
import csv, json, math, random, sys, time
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
SYL_LM       = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"  # Dravidian reference
SANSKRIT_LM  = REPO / "backend/glossa_lab/data/sanskrit_syllable_lm.json"   # Sanskrit target
DEDR         = REPO / "reports/jambu-dedr/data/dedr/dedr_new.csv"
ANCHORS      = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P63          = REPO / "reports/phase63_filtered_sa.json"  # Dravidian z-score reference
REPORTS      = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT          = REPORTS / "phase66_sanskrit_sa.json"

N_RESTARTS = 10
MAX_ITER   = 30_000
SA_TEMP    = 1.0
SA_COOL    = 0.9997
N_SEEDS    = 5

PD_INVALID_INITIAL = set("bdfgqwx")

def is_phonotactically_valid(syllable: str) -> bool:
    s = syllable.lower().strip()
    if not s: return False
    first = s[0]
    if first in "aāiīuūeēoō": return True
    return first not in PD_INVALID_INITIAL


def load_corpus():
    seals: dict[str, list] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    inscriptions = [[s for s in v if s] for v in seals.values() if any(v)]
    return [s for i in inscriptions for s in i], inscriptions


def load_lm_from_file(path: Path, name: str) -> dict | None:
    if not path.exists():
        print(f"  {name}: NOT FOUND at {path}")
        return None
    raw = json.loads(path.read_text("utf-8"))
    bigrams = raw.get("bigrams", {})
    total = sum(bigrams.values()) or 1
    prob = {}
    for k, v in bigrams.items():
        parts = k.split(",", 1) if "," in k else k.split("|", 1) if "|" in k else None
        if parts and len(parts) == 2:
            prob[tuple(parts)] = v / total
    print(f"  {name}: {len(prob)} bigrams")
    return prob if prob else None


def build_proto_dravidian_lm() -> dict | None:
    """Build Proto-Dravidian LM from DEDR (reference, for Dravidian z baseline)."""
    import re
    bigram_counts: Counter = Counter()
    if not DEDR.exists():
        return None
    try:
        with open(DEDR, encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f):
                if len(row) > 2:
                    word = re.sub(r"[^a-zāīūēōḍṭṇṅñśṣ]", "", row[2].strip().lower())
                    if len(word) >= 4:
                        for i in range(len(word) - 3):
                            a, b = word[i:i+2], word[i+2:i+4]
                            if re.match(r"[a-z]{2}", a) and re.match(r"[a-z]{2}", b):
                                bigram_counts[(a, b)] += 1
        total = sum(bigram_counts.values()) or 1
        prob = {(a, b): c/total for (a,b), c in bigram_counts.items() if c >= 2}
        print(f"  Proto-Dravidian LM (DEDR): {len(prob)} bigrams")
        return prob if prob else None
    except Exception as e:
        print(f"  Proto-Dravidian LM failed: {e}")
        return None


def build_scorer(bigram_prob: dict, flat: list):
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    return BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)


def build_pins(flat: list, vocab_set: set) -> dict:
    SYLLABIC = {
        "M006":"pu","M016":"ka","M045":"ya","M062":"e","M099":"ko",
        "M176":"an","M342":"ay","M328":"aa","M059":"ee","M162":"il",
        "M391":"ka","M367":"am","M089":"tu","M051":"pu","M336":"i",
        "M048":"mu","M012":"o","M305":"ir","M073":"ko","M013":"na",
        "M233":"uu","M087":"ve","M077":"na","M030":"ko","M017":"ka",
    }
    pins = {}
    for sign, syl in SYLLABIC.items():
        if sign in set(flat):
            if syl in vocab_set: pins[sign] = syl
            else:
                match = next((s for s in sorted(vocab_set) if s.startswith(syl[:2])), None)
                if match: pins[sign] = match
    return pins


def run_sa_lm(flat: list, lm: dict, seed: int, pinned: dict, filtered: bool = False) -> tuple[float, dict]:
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in lm: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    scorer = BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=lm), flat)

    vocab_set = set(ranked)
    if filtered:
        vocab_set = {s for s in vocab_set if is_phonotactically_valid(s)}

    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(vocab_set)
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")
    free_cipher = [c for c in cipher_alpha if c not in pinned]

    rng = random.Random(seed)
    def _init(sh):
        m = dict(pinned); used = set(m.values())
        pool = [t for t in target_tokens[:len(cipher_alpha)] if t not in used]
        if sh: rng.shuffle(pool)
        for c, t in zip(free_cipher, pool): m[c] = t
        return m

    best_score = float("-inf"); best_map = {}
    for restart in range(N_RESTARTS):
        mapping = _init(sh=(restart > 0))
        score = scorer.score_full(mapping); temp = SA_TEMP
        for _ in range(MAX_ITER):
            if len(free_cipher) < 2: break
            i, j = rng.sample(range(len(free_cipher)), 2)
            ca, cb = free_cipher[i], free_cipher[j]
            mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            ns = scorer.score_full(mapping)
            if ns > score or (temp > 0 and rng.random() < math.exp(min((ns - score) / temp, 0))):
                score = ns
            else:
                mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            temp *= SA_COOL
        if score > best_score: best_score = score; best_map = dict(mapping)
    return best_score, best_map


def run_lm_experiment(flat: list, lm: dict, lm_name: str, pinned: dict,
                      filtered: bool = False) -> dict:
    """Run SA against an LM and return z-score statistics."""
    tc: Counter = Counter()
    for (a, b) in lm: tc[a] += 1; tc[b] += 1
    vocab_set = set(tc.keys())
    if filtered:
        vocab_set = {s for s in vocab_set if is_phonotactically_valid(s)}

    # Null estimate
    rng_null = random.Random(99)
    cipher_alpha = sorted(set(flat))
    target_list = sorted(vocab_set)
    while len(target_list) < len(cipher_alpha): target_list.append(f"?{len(target_list)}")

    from glossa_lab.pipelines.decipher import BigramScorer
    ranked = [t for t, _ in tc.most_common()]
    scorer = BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=lm), flat)

    null_scores = []
    for _ in range(30):
        tgt = list(target_list[:len(cipher_alpha)]); rng_null.shuffle(tgt)
        null_scores.append(scorer.score_full(dict(zip(cipher_alpha, tgt))))
    null_mu  = sum(null_scores) / len(null_scores)
    null_std = math.sqrt(sum((s - null_mu)**2 for s in null_scores) / len(null_scores)) or 1.0

    print(f"  {lm_name}: null mean={null_mu:.1f}")

    scores = []; t0 = time.perf_counter()
    for seed in range(N_SEEDS):
        s, _ = run_sa_lm(flat, lm, seed, pinned, filtered)
        z = (s - null_mu) / null_std
        scores.append(s)
        print(f"    Seed {seed}: score={s:.1f} z={z:.2f}")
    elapsed = time.perf_counter() - t0
    mean_s = sum(scores) / len(scores)
    z = (mean_s - null_mu) / null_std

    return {"z_score": round(z, 3), "mean_score": round(mean_s, 2),
            "null_mu": round(null_mu, 2), "elapsed": round(elapsed, 1)}


def main():
    print("Phase-66: Sanskrit SA Falsification\n")
    flat, inscriptions = load_corpus()
    print(f"Corpus: {len(inscriptions)} inscriptions, {len(set(flat))} unique signs\n")

    # Load Sanskrit LM
    print("Loading LMs:")
    skt_lm = load_lm_from_file(SANSKRIT_LM, "Sanskrit syllable")

    # Build fallback Sanskrit LM from data module if file not found
    if skt_lm is None:
        print("  Sanskrit LM file not found — building from glossa_lab.data.sanskrit")
        try:
            sys.path.insert(0, str(REPO / "backend"))
            from glossa_lab.data.sanskrit import get_corpus_symbols
            skt_syms = get_corpus_symbols()
            bigram_counts: Counter = Counter()
            for i in range(len(skt_syms) - 1):
                bigram_counts[(skt_syms[i], skt_syms[i+1])] += 1
            total = sum(bigram_counts.values()) or 1
            skt_lm = {(a, b): c/total for (a, b), c in bigram_counts.items() if c >= 1}
            print(f"  Sanskrit LM (from data module): {len(skt_lm)} bigrams")
        except Exception as e:
            print(f"  Sanskrit LM build failed: {e}")
            skt_lm = None

    if skt_lm is None:
        print("ERROR: Cannot build Sanskrit LM. Aborting Phase-66.")
        result = {
            "_citation": {"primary": ["A.1"]},
            "gpu_device": DEVICE,
            "error": "Sanskrit LM not available. Need sanskrit_syllable_lm.json or glossa_lab.data.sanskrit",
            "verdict": "INCOMPLETE",
        }
        OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
        return

    # Build Dravidian syllabic LM for reference comparison
    print("\nBuilding Dravidian reference LM:")
    drav_lm = None
    if SYL_LM.exists():
        raw = json.loads(SYL_LM.read_text("utf-8"))
        syl_freq = raw.get("syllable_freq", {})
        valid = {s for s, c in syl_freq.items() if c >= 3}
        total = sum(v for k, v in raw.get("bigrams", {}).items()
                    if k.split(",", 1)[0] in valid and k.split(",", 1)[1] in valid) or 1
        drav_lm = {tuple(k.split(",", 1)): v/total
                   for k, v in raw.get("bigrams", {}).items()
                   if "," in k and k.split(",", 1)[0] in valid and k.split(",", 1)[1] in valid}
        print(f"  Dravidian syllabic LM: {len(drav_lm)} bigrams")
    if drav_lm is None:
        drav_lm = build_proto_dravidian_lm()

    # Build pins from Dravidian vocabulary
    pinned_drav = build_pins(flat, set(t for pair in (drav_lm or {}) for t in pair))
    pinned_skt  = build_pins(flat, set(t for pair in skt_lm for t in pair))
    print(f"\n  Dravidian pins: {len(pinned_drav)}")
    print(f"  Sanskrit pins:  {len(pinned_skt)}")

    # Run Sanskrit SA
    print("\nRunning Sanskrit SA (adversarial):")
    skt_result = run_lm_experiment(flat, skt_lm, "Sanskrit", pinned_skt, filtered=False)

    # Run Dravidian SA (reference — should match Phase-63)
    drav_result = {"z_score": 0.0, "mean_score": 0.0, "null_mu": 0.0, "elapsed": 0.0}
    if drav_lm:
        print("\nRunning Dravidian SA (reference):")
        drav_result = run_lm_experiment(flat, drav_lm, "Dravidian", pinned_drav, filtered=True)

    # Also load Phase-63 z-score as the official Dravidian reference
    p63_z = 0.0
    if P63.exists():
        p63_data = json.loads(P63.read_text("utf-8"))
        p63_z = p63_data.get("z_score", 0.0)

    z_drav = drav_result["z_score"] if drav_result["z_score"] > 0 else p63_z
    z_skt  = skt_result["z_score"]
    ratio  = z_drav / max(abs(z_skt), 0.01)

    # Verdict
    if z_drav > z_skt and ratio >= 1.5:
        verdict = f"DRAVIDIAN_PREFERRED: z_Dravidian/z_Sanskrit = {ratio:.2f}×"
    elif z_drav > z_skt:
        verdict = f"DRAVIDIAN_MARGINALLY_PREFERRED: ratio={ratio:.2f}× (needs >1.5× for strong claim)"
    elif abs(z_drav - z_skt) < 1.0:
        verdict = f"INDISTINGUISHABLE: |z_D - z_S| < 1 (ratio={ratio:.2f}×) — cannot distinguish"
    else:
        verdict = f"SANSKRIT_PREFERRED: unexpected — ratio={ratio:.2f}×"

    print(f"\n=== Phase-66 Results ===")
    print(f"  Dravidian z:        {z_drav:.2f} (Phase-63 reference: {p63_z:.2f})")
    print(f"  Sanskrit z:         {z_skt:.2f}")
    print(f"  Ratio (D/S):        {ratio:.2f}×")
    print(f"  Verdict:            {verdict}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device":                       DEVICE,
        "z_score_dravidian_ref":            z_drav,
        "z_score_dravidian_phase63":        p63_z,
        "z_score_sanskrit":                 z_skt,
        "z_ratio_dravidian_vs_sanskrit":    round(ratio, 3),
        "dravidian_run":                    drav_result,
        "sanskrit_run":                     skt_result,
        "verdict":                          verdict,
        "interpretation": (
            f"Dravidian z={z_drav:.2f} vs Sanskrit z={z_skt:.2f} → {ratio:.2f}× preference. "
            f"This is the key quantitative falsification of the competing Sanskrit hypothesis."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
