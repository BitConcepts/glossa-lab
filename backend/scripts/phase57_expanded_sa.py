"""Phase-57: Expanded Constrained SA with 70+ Anchors.
Re-runs Phase-52 SA after Phase-56 anchor expansion.
Expected: z > 20, SA agreement with confirmed > 70%.
GPU: BigramScorer CUDA. Output: reports/phase57_expanded_sa.json
"""
from __future__ import annotations
import csv, json, math, random, sys, time
from collections import Counter
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
OUT       = REPORTS / "phase57_expanded_sa.json"
OUT_TABLE = REPORTS / "phase57_decipherment_table.json"

N_RESTARTS = 10; MAX_ITER = 30_000; SA_TEMP = 1.0; SA_COOL = 0.9997; N_SEEDS = 5


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
        valid = {s for s,c in syl_freq.items() if c >= 3}
        total = sum(v for k,v in raw.get("bigrams",{}).items()
                    if k.split(",",1)[0] in valid and k.split(",",1)[1] in valid) or 1
        prob = {tuple(k.split(",",1)): v/total for k,v in raw.get("bigrams",{}).items()
                if "," in k and k.split(",",1)[0] in valid and k.split(",",1)[1] in valid}
        vocab = sorted(valid)
        print(f"  Syllabic LM: {len(prob)} bigrams, {len(vocab)} syllables")
        return prob, vocab
    raw = json.loads(CHAR_LM.read_text("utf-8"))
    bigrams = raw.get("bigrams", {}); total = sum(bigrams.values()) or 1
    prob = {tuple(k.split(",",1)): v/total for k,v in bigrams.items() if "," in k}
    return prob, sorted(set(t for pair in prob for t in pair))


def build_pins(flat, vocab_set, anchors):
    SYLLABIC = {
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
    pins = {}
    for sign, syl in SYLLABIC.items():
        if sign in set(flat):
            if syl in vocab_set: pins[sign] = syl
            else:
                match = next((s for s in sorted(vocab_set) if s.startswith(syl[:2])), None)
                if match: pins[sign] = match
    print(f"  Pinned {len(pins)} signs")
    return pins


def build_scorer(bigram_prob, flat):
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a,b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t,_ in tc.most_common()]
    return BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)


def run_sa(flat, scorer, bigram_prob, seed, pinned):
    rng = random.Random(seed)
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha): target_tokens.append(f"?{len(target_tokens)}")
    free_cipher = [c for c in cipher_alpha if c not in pinned]
    def _init(sh):
        m = dict(pinned); used = set(m.values())
        pool = [t for t in target_tokens[:len(cipher_alpha)] if t not in used]
        if sh: rng.shuffle(pool)
        for c,t in zip(free_cipher, pool): m[c] = t
        return m
    best_score = float("-inf"); best_map = {}
    for restart in range(N_RESTARTS):
        mapping = _init(sh=(restart > 0)); score = scorer.score_full(mapping); temp = SA_TEMP
        for _ in range(MAX_ITER):
            if len(free_cipher) < 2: break
            i,j = rng.sample(range(len(free_cipher)), 2)
            ca,cb = free_cipher[i], free_cipher[j]
            mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            ns = scorer.score_full(mapping)
            if ns > score or (temp > 0 and rng.random() < math.exp(min((ns-score)/temp, 0))): score = ns
            else: mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            temp *= SA_COOL
        if score > best_score: best_score = score; best_map = dict(mapping)
    return best_score, best_map


def main():
    print("Phase-57: Expanded Constrained SA\n")
    flat, inscriptions = load_corpus()
    print(f"Corpus: {len(inscriptions)} inscriptions, {len(set(flat))} unique signs")
    bigram_prob, vocab = load_lm()
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    pinned = build_pins(flat, set(vocab), anchors)
    scorer = build_scorer(bigram_prob, flat)
    # Null estimate
    rng_null = random.Random(42)
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha): target_tokens.append(f"?{len(target_tokens)}")
    null_scores = []
    for _ in range(30):
        tgt = list(target_tokens[:len(cipher_alpha)]); rng_null.shuffle(tgt)
        null_scores.append(scorer.score_full(dict(zip(cipher_alpha, tgt))))
    null_mu = sum(null_scores)/len(null_scores)
    null_std = math.sqrt(sum((s-null_mu)**2 for s in null_scores)/len(null_scores)) or 1.0
    print(f"Null: mean={null_mu:.1f}")
    all_scores = []; all_maps = []; t0 = time.perf_counter()
    for seed in range(N_SEEDS):
        score, mapping = run_sa(flat, scorer, bigram_prob, seed, pinned)
        z = (score - null_mu) / null_std; lift = score / null_mu if null_mu else 0
        all_scores.append(score); all_maps.append(mapping)
        print(f"  Seed {seed}: score={score:.1f} z={z:.2f} lift={lift:.4f}")
    elapsed = time.perf_counter() - t0
    mean_score = sum(all_scores)/len(all_scores)
    z = (mean_score - null_mu) / null_std
    # Build consensus table
    from collections import defaultdict
    votes: dict[str, Counter] = defaultdict(Counter)
    for m in all_maps:
        for sign, reading in m.items(): votes[sign][reading] += 1
    freq = Counter(flat)
    table = []
    for sign in sorted(votes, key=lambda s: -freq.get(s, 0)):
        best = votes[sign].most_common(1)[0]
        existing = anchors.get(sign, {})
        consensus_pct = best[1] / N_SEEDS
        agree = best[0][:2] == existing.get("reading","?")[:2] if existing.get("reading") else None
        table.append({"sign": sign, "n_corpus": freq.get(sign,0),
                      "sa_reading": best[0], "sa_consensus_pct": round(consensus_pct,2),
                      "confirmed_reading": existing.get("reading",""),
                      "confirmed_confidence": existing.get("confidence","UNREAD"),
                      "sa_agrees": agree,
                      "vote_dist": dict(votes[sign].most_common(3))})
    n_confirmed = sum(1 for t in table if t["confirmed_confidence"] in ("HIGH","MEDIUM"))
    n_agree = sum(1 for t in table if t.get("sa_agrees"))
    agree_rate = n_agree / max(n_confirmed, 1)
    print(f"\n=== Phase-57 Results ===")
    print(f"  z={z:.2f}, {len(pinned)} anchors pinned")
    print(f"  SA agrees with confirmed: {n_agree}/{n_confirmed} = {agree_rate:.0%}")
    print(f"  Time: {elapsed:.1f}s")
    OUT_TABLE.write_text(json.dumps(table, indent=2, ensure_ascii=False), "utf-8")
    result = {
        "_citation": {"primary": ["A.1"]}, "gpu_device": DEVICE,
        "n_pinned": len(pinned), "null_mu": round(null_mu,2),
        "mean_score": round(mean_score,2), "z_score": round(z,3),
        "sa_confirmed_agreement_pct": round(agree_rate*100,1),
        "n_confirmed": n_confirmed, "n_agree": n_agree,
        "elapsed_secs": round(elapsed,1), "top_30": table[:30],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
