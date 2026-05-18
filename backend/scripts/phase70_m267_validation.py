"""Phase-70: M267=in Genitive Validation.

Tests the Phase-64 conclusion that M267 = iN (genitive 'of') by:
  1. Baseline: Phase-63 phonotactic-filtered SA (54 anchors, z=14.18)
  2. Run A:   Same SA but M267 also pinned to 'in' (55 anchors)
  3. Run B:   Same SA but M267 pinned to 'col' (55 anchors, alternative)

Decision rule:
  - If z_in  > z_baseline: iN is linguistically coherent -> promote M267 to HIGH
  - If z_col > z_baseline: col is alternative winner
  - If both degrade: M267 remains UNCERTAIN (multi-syllabic, SA cannot pin)

GPU: BigramScorer CUDA. ~15 min total (3 runs x 5 seeds).
Output: reports/phase70_m267_validation.json
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

HOLDAT    = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
SYL_LM    = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"
CHAR_LM   = REPO / "backend/glossa_lab/data/dravidian_tamil_lm.json"
ANCHORS   = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS   = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT       = REPORTS / "phase70_m267_validation.json"

N_RESTARTS = 10
MAX_ITER   = 30_000
SA_TEMP    = 1.0
SA_COOL    = 0.9997
N_SEEDS    = 5

PD_INVALID_INITIAL = set("bdfgqwx")

def is_phonotactically_valid(s: str) -> bool:
    t = s.lower().strip()
    if not t: return False
    return t[0] in "aaiiiuuueeoooaaiiuu" or t[0] not in PD_INVALID_INITIAL


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


def load_lm():
    if SYL_LM.exists():
        raw = json.loads(SYL_LM.read_text("utf-8"))
        syl_freq = raw.get("syllable_freq", {})
        valid_syls = {s for s, c in syl_freq.items() if c >= 3}
        total = sum(v for k, v in raw.get("bigrams", {}).items()
                    if k.split(",", 1)[0] in valid_syls and k.split(",", 1)[1] in valid_syls) or 1
        prob = {tuple(k.split(",", 1)): v / total
                for k, v in raw.get("bigrams", {}).items()
                if "," in k and k.split(",", 1)[0] in valid_syls and k.split(",", 1)[1] in valid_syls}
        vocab = sorted(valid_syls)
        return prob, vocab
    raw = json.loads(CHAR_LM.read_text("utf-8"))
    bigrams = raw.get("bigrams", {}); total = sum(bigrams.values()) or 1
    prob = {tuple(k.split(",", 1)): v / total for k, v in bigrams.items() if "," in k}
    return prob, sorted(set(t for pair in prob for t in pair))


# Same SYLLABIC dict as Phase-57/63
SYLLABIC_BASE = {
    "M006":"pu","M016":"ka","M045":"ya","M062":"e","M099":"ko",
    "M176":"an","M342":"ay","M328":"aa","M059":"ee","M162":"il",
    "M391":"ka","M367":"am","M089":"tu","M051":"pu","M336":"i",
    "M048":"mu","M012":"o","M305":"ir","M073":"ko","M013":"na",
    "M233":"uu","M087":"ve","M077":"na","M030":"ko","M017":"ka",
    "M020":"ku","M004":"ke","M014":"ti","M026":"ma","M034":"to",
    "M027":"ma","M041":"pe","M018":"ne","M063":"mu","M080":"ve",
    "M057":"ma","M039":"aa","M060":"er","M211":"ko","M175":"ka",
    "M100":"ma","M117":"ar","M124":"ku","M125":"vi","M128":"mu",
    "M249":"ti","M261":"mu","M264":"pe","M281":"pi","M311":"va",
    "M001":"aa","M008":"er","M028":"ma","M029":"ka","M031":"to",
    "M047":"mi","M050":"mi","M065":"ku","M086":"or","M088":"mu",
    "M091":"aa","M092":"ee",
}


def build_pins(flat, vocab_set, extra_pin: dict | None = None) -> dict:
    """Build pin dict from SYLLABIC_BASE + optional M267 pin."""
    pins = {}
    syllabic = dict(SYLLABIC_BASE)
    if extra_pin:
        syllabic.update(extra_pin)
    for sign, syl in syllabic.items():
        if sign in set(flat):
            if syl in vocab_set:
                pins[sign] = syl
            else:
                match = next((s for s in sorted(vocab_set) if s.startswith(syl[:2])), None)
                if match:
                    pins[sign] = match
    return pins


def build_scorer(bigram_prob, flat):
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    return BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)


def run_sa(flat, scorer, bigram_prob, seed, pinned, filtered_vocab):
    rng = random.Random(seed)
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(filtered_vocab)
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")
    free_cipher = [c for c in cipher_alpha if c not in pinned]

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


def run_experiment(flat, scorer, bigram_prob, vocab_set, filtered_vocab,
                   extra_pin: dict | None, label: str) -> dict:
    """Run a full SA experiment with a given extra pin and return stats."""
    pins = build_pins(flat, vocab_set, extra_pin)
    print(f"\n  {label}: {len(pins)} anchors pinned")

    # Null estimate
    rng_null = random.Random(42)
    cipher_alpha = sorted(set(flat))
    target_list = sorted(filtered_vocab)
    while len(target_list) < len(cipher_alpha):
        target_list.append(f"?{len(target_list)}")
    null_scores = []
    for _ in range(30):
        tgt = list(target_list[:len(cipher_alpha)]); rng_null.shuffle(tgt)
        null_scores.append(scorer.score_full(dict(zip(cipher_alpha, tgt))))
    null_mu  = sum(null_scores) / len(null_scores)
    null_std = math.sqrt(sum((s - null_mu)**2 for s in null_scores) / len(null_scores)) or 1.0
    print(f"  Null mean={null_mu:.1f}")

    all_scores = []; t0 = time.perf_counter()
    for seed in range(N_SEEDS):
        score, _ = run_sa(flat, scorer, bigram_prob, seed, pins, filtered_vocab)
        z = (score - null_mu) / null_std
        all_scores.append(score)
        print(f"  Seed {seed}: score={score:.1f} z={z:.2f}")
    elapsed = time.perf_counter() - t0
    mean_s = sum(all_scores) / len(all_scores)
    z = (mean_s - null_mu) / null_std
    print(f"  {label}: z={z:.2f} ({elapsed:.1f}s)")
    return {"z_score": round(z, 3), "mean_score": round(mean_s, 2),
            "null_mu": round(null_mu, 2), "n_pins": len(pins),
            "elapsed": round(elapsed, 1)}


def main():
    print("Phase-70: M267=in Genitive Validation\n")
    flat, inscriptions = load_corpus()
    print(f"Corpus: {len(set(flat))} unique signs, {len(flat)} tokens")
    bigram_prob, vocab = load_lm()
    print(f"  LM: {len(bigram_prob)} bigrams, {len(vocab)} syllables")

    vocab_set = set(vocab)
    filtered_vocab = {s for s in vocab_set if is_phonotactically_valid(s)}
    n_filtered = len(vocab_set) - len(filtered_vocab)
    print(f"  Phonotactic filter: removed {n_filtered} invalid-initial syllables")

    scorer = build_scorer(bigram_prob, flat)
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]

    # Check if 'in' and 'col' are in the filtered vocabulary
    in_token  = next((s for s in sorted(filtered_vocab) if s.startswith("in") or s == "in"), None)
    col_token = next((s for s in sorted(filtered_vocab) if s.startswith("ko") or s == "ko"), None)
    print(f"\n  'in' token in vocab: {in_token!r}")
    print(f"  'col' proxy token (ko): {col_token!r}")

    # Run 1: Baseline (no M267 pin) = Phase-63 equivalent
    print(f"\n{'='*60}")
    print(f"Run 1: BASELINE (no M267 pin)")
    r_base = run_experiment(flat, scorer, bigram_prob, vocab_set, filtered_vocab,
                             None, "Baseline")

    # Run 2: M267 = 'in' (genitive)
    print(f"\n{'='*60}")
    print(f"Run 2: M267='in' (genitive 'of')")
    in_pin = in_token if in_token else "i"
    r_in = run_experiment(flat, scorer, bigram_prob, vocab_set, filtered_vocab,
                          {"M267": in_pin}, "M267=in")

    # Run 3: M267 = 'ko' / 'col' proxy (quotative/connective)
    print(f"\n{'='*60}")
    print(f"Run 3: M267='ko' (col-proxy, quotative/connective)")
    col_pin = col_token if col_token else "ko"
    r_col = run_experiment(flat, scorer, bigram_prob, vocab_set, filtered_vocab,
                           {"M267": col_pin}, "M267=col-proxy")

    # Decision
    z_base = r_base["z_score"]
    z_in   = r_in["z_score"]
    z_col  = r_col["z_score"]

    if z_in > z_col and z_in > z_base:
        winner = "in"
        m267_promoted = z_in > z_base + 0.2  # only promote if meaningful improvement
        verdict = f"WINNER=in (z={z_in:.2f} > baseline={z_base:.2f})"
    elif z_col > z_in and z_col > z_base:
        winner = "col"
        m267_promoted = False
        verdict = f"WINNER=col-proxy (z={z_col:.2f} > baseline={z_base:.2f})"
    else:
        winner = "baseline"
        m267_promoted = False
        verdict = f"M267 UNCERTAIN — both pins degrade SA (in={z_in:.2f}, col={z_col:.2f} vs base={z_base:.2f})"

    print(f"\n{'='*60}")
    print(f"=== Phase-70 Results ===")
    print(f"  Baseline z:  {z_base:.2f}")
    print(f"  z (in):      {z_in:.2f}  ({'+' if z_in >= z_base else ''}{z_in - z_base:.2f} vs baseline)")
    print(f"  z (col):     {z_col:.2f}  ({'+' if z_col >= z_base else ''}{z_col - z_base:.2f} vs baseline)")
    print(f"  Winner:      {winner}")
    print(f"  Verdict:     {verdict}")
    print(f"  M267 promoted to HIGH: {m267_promoted}")

    # If 'in' wins and improves, update ANCHORS
    if m267_promoted:
        data = json.loads(ANCHORS.read_text("utf-8"))
        data["anchors"]["M267"]["confidence"] = "MEDIUM"
        data["anchors"]["M267"]["reading"] = "iN/in (genitive)"
        data["anchors"]["M267"]["source"] = "Phase-70 SA validation + Phase-64 grammar analysis"
        ANCHORS.write_text(json.dumps(data, indent=2, ensure_ascii=False), "utf-8")
        print(f"  ANCHORS updated: M267 promoted to MEDIUM (was UNCERTAIN)")
    elif winner == "in" and z_in > z_base:
        print(f"  M267='in' shows improvement but below promotion threshold (need +0.2 z). Keeping UNCERTAIN.")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "z_baseline":    z_base,
        "z_in":          z_in,
        "z_col":         z_col,
        "winner":        winner,
        "verdict":       verdict,
        "m267_promoted": m267_promoted,
        "in_token_used": in_pin,
        "col_token_used":col_pin,
        "baseline_run":  r_base,
        "in_run":        r_in,
        "col_run":       r_col,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
