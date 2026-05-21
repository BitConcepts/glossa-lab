"""
Phase-150: Polysemy Permutation Null Test

The Phase-142D polysemy result (17/21 signs show context-dependent collocate
profiles) was challenged in Phase-149 C1 with only a binomial null (p=0.006).
This phase runs the proper corpus-shuffled permutation null:

  For each of 1000 iterations:
    1. Shuffle sign POSITIONS within each seal (preserving seal lengths)
    2. Recompute collocate divergence for the same 21 signs tested in Phase-142D
    3. Record how many of the 21 signs show "polysemous" divergence in the shuffled corpus

  Null distribution: distribution of polysemy rate under random sign assignment
  Observed: 17/21 = 0.810
  p-value: fraction of shuffles that produce polysemy rate >= 0.810

  If p < 0.01 → upgrade C1 to STRONGLY_CONFIRMED

Output: backend/reports/phase150_polysemy_permutation.json
"""
import sys, json, random, math
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
PHASE142_RPT = REPO / "backend/reports/phase142_collocate_network.json"
OUT          = REPO / "backend/reports/phase150_polysemy_permutation.json"

print("="*70)
print("PHASE-150: POLYSEMY PERMUTATION NULL TEST (n=1000)")
print("="*70)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors = anchor_data["anchors"]
hm_set  = {k for k,v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}

# Load corpus
try:
    import pandas as pd
    df = pd.read_csv(HOLDAT)
    seals = {}
    for _, row in df.iterrows():
        f = str(row.get("form",""))
        s = str(row.get("letters",""))
        if f and s:
            if f not in seals: seals[f] = {"signs":[]}
            seals[f]["signs"].append(s)
except Exception:
    seals = {}
    with open(HOLDAT, encoding="utf-8") as fh:
        hdr = fh.readline().strip().split(",")
        ci = {h:i for i,h in enumerate(hdr)}
        for line in fh:
            p = line.strip().split(",")
            if len(p) < 2: continue
            f = p[ci.get("form",0)]; s = p[ci.get("letters",1)]
            if f and s:
                if f not in seals: seals[f]={"signs":[]}
                seals[f]["signs"].append(s)

all_seqs = [d["signs"] for d in seals.values()]
all_flat  = [s for seq in all_seqs for s in seq]
n_seals = len(seals)
print(f"\nCorpus: {n_seals} seals, {len(all_flat)} tokens")

# The 21 signs tested in Phase-142D (H+M high-frequency signs with >=20 occurrences)
sign_freq = Counter(all_flat)
test_signs = sorted(
    [s for s in hm_set if sign_freq.get(s,0) >= 20],
    key=lambda s: -sign_freq[s]
)[:21]
print(f"Test signs (top-21 H+M by frequency): {test_signs}")

def compute_polysemy_rate(seqs, target_signs):
    """
    For each sign in target_signs, compute left and right collocate profiles
    in INITIAL vs non-INITIAL position. A sign is 'polysemous' if the two
    profiles have KL divergence > threshold (0.3 bits).
    """
    # Build collocate distributions split by position
    initial_right = defaultdict(Counter)   # sign -> {right_neighbor: count} when sign is INITIAL
    noninitial_right = defaultdict(Counter) # sign -> {right_neighbor: count} when sign is not INITIAL

    for seq in seqs:
        for i, s in enumerate(seq):
            if s not in target_signs: continue
            is_initial = (i == 0)
            right = seq[i+1] if i < len(seq)-1 else None
            if right:
                if is_initial:
                    initial_right[s][right] += 1
                else:
                    noninitial_right[s][right] += 1

    def kl_div(p_counter, q_counter):
        """KL(P||Q) in bits, with smoothing."""
        vocab = set(p_counter) | set(q_counter)
        if not vocab: return 0.0
        total_p = sum(p_counter.values()) + len(vocab)  # Laplace smoothing
        total_q = sum(q_counter.values()) + len(vocab)
        kl = 0.0
        for w in vocab:
            p = (p_counter.get(w,0) + 1) / total_p
            q = (q_counter.get(w,0) + 1) / total_q
            if p > 0:
                kl += p * math.log2(p / q)
        return kl

    THRESHOLD = 0.3  # bits — divergence above this = polysemous
    polysemous = 0
    for s in target_signs:
        if sum(initial_right[s].values()) < 3 or sum(noninitial_right[s].values()) < 3:
            # Not enough data in one slot — skip
            continue
        kl = kl_div(initial_right[s], noninitial_right[s])
        if kl > THRESHOLD:
            polysemous += 1

    return polysemous / len(target_signs) if target_signs else 0.0

# ─── Observed rate ─────────────────────────────────────────────────────────
print("\nComputing observed polysemy rate on real corpus...")
observed_rate = compute_polysemy_rate(all_seqs, test_signs)
print(f"  Observed polysemy rate: {observed_rate:.4f} ({observed_rate*100:.1f}%)")

# ─── Permutation null ──────────────────────────────────────────────────────
N_PERMS = 1000
print(f"\nRunning {N_PERMS} permutations (shuffling sign positions within each seal)...")

null_rates = []
rng = random.Random(42)  # fixed seed for reproducibility

for i in range(N_PERMS):
    shuffled = []
    for seq in all_seqs:
        s = seq[:]
        rng.shuffle(s)
        shuffled.append(s)
    rate = compute_polysemy_rate(shuffled, test_signs)
    null_rates.append(rate)
    if (i+1) % 200 == 0:
        print(f"  {i+1}/{N_PERMS} done... mean null so far: {sum(null_rates)/len(null_rates):.4f}")

null_rates.sort()
null_mean = sum(null_rates) / len(null_rates)
null_sd   = math.sqrt(sum((r - null_mean)**2 for r in null_rates) / len(null_rates))
p_value   = sum(1 for r in null_rates if r >= observed_rate) / N_PERMS
pct95     = null_rates[int(0.95 * N_PERMS)]
pct99     = null_rates[int(0.99 * N_PERMS)]
z_score   = (observed_rate - null_mean) / null_sd if null_sd > 0 else 0

print(f"\n  Null distribution (n={N_PERMS}):")
print(f"    Mean:  {null_mean:.4f}")
print(f"    SD:    {null_sd:.4f}")
print(f"    95th percentile: {pct95:.4f}")
print(f"    99th percentile: {pct99:.4f}")
print(f"\n  Observed: {observed_rate:.4f}")
print(f"  p-value (one-tailed): {p_value:.4f}")
print(f"  z-score: {z_score:.2f}")

if p_value < 0.001:
    verdict = "STRONGLY_CONFIRMED"
elif p_value < 0.01:
    verdict = "CONFIRMED"
elif p_value < 0.05:
    verdict = "SUPPORTED"
else:
    verdict = "INCONCLUSIVE"

print(f"\n  VERDICT: {verdict}")
print(f"  C1 caveat status: {'CLOSED — permutation null confirms polysemy' if p_value < 0.05 else 'REMAINS OPEN'}")

output = {
    "phase": 150,
    "date": "2026-05-19",
    "test": "polysemy_permutation_null",
    "n_permutations": N_PERMS,
    "n_test_signs": len(test_signs),
    "test_signs": test_signs,
    "threshold_kl_bits": 0.3,
    "observed_polysemy_rate": round(observed_rate, 4),
    "null_mean": round(null_mean, 4),
    "null_sd": round(null_sd, 4),
    "null_p95": round(pct95, 4),
    "null_p99": round(pct99, 4),
    "p_value": round(p_value, 4),
    "z_score": round(z_score, 2),
    "verdict": verdict,
    "c1_caveat_closed": p_value < 0.05,
    "key_findings": [
        f"Observed polysemy rate: {observed_rate:.4f} ({observed_rate*100:.1f}%)",
        f"Null distribution mean: {null_mean:.4f} (SD={null_sd:.4f})",
        f"p-value (one-tailed permutation): {p_value:.4f}",
        f"z-score: {z_score:.2f}",
        f"Verdict: {verdict}",
        f"C1 caveat: {'CLOSED' if p_value < 0.05 else 'OPEN'}",
    ]
}

OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {OUT}")
print("="*70)
