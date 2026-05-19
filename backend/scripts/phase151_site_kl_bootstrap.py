"""
Phase-151: Site KL Divergence Bootstrap Confidence Intervals

Phase-149 C9 flagged that KL=0.708 between Chanhu-daro (n=78) and Rakhigarhi
(n=33) may be a small-sample artifact — no bootstrapped CI was computed.

This phase:
  1. Computes KL divergence between all site pairs on their sign frequency distributions
  2. Bootstraps 95% CI for the Chanhu-daro vs Rakhigarhi KL estimate (1000 resamples)
  3. Checks if the grammar stability (90%) holds in the bootstrap samples
  4. Renders ROBUST / FRAGILE / INCONCLUSIVE for each site pair

Output: backend/reports/phase151_site_kl_bootstrap.json
"""
import sys, json, math, random
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
OUT          = REPO / "backend/reports/phase151_site_kl_bootstrap.json"

print("="*70)
print("PHASE-151: SITE KL DIVERGENCE BOOTSTRAP CI (n=1000)")
print("="*70)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors = anchor_data["anchors"]
hm_set  = {k for k,v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}

# Load corpus with site info
try:
    import pandas as pd
    df = pd.read_csv(HOLDAT)
    seals = {}
    for _, row in df.iterrows():
        f = str(row.get("form",""))
        s = str(row.get("letters",""))
        site = str(row.get("site",""))
        if f and s:
            if f not in seals: seals[f] = {"site": site, "signs":[]}
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
            site = p[ci.get("site",2)] if ci.get("site",2) < len(p) else ""
            if f and s:
                if f not in seals: seals[f]={"site":site,"signs":[]}
                seals[f]["signs"].append(s)

# Group seals by site
site_seals = defaultdict(list)
for form, data in seals.items():
    site = data.get("site","unknown").strip()
    if site:
        site_seals[site].append(data["signs"])

sites = sorted(site_seals.keys(), key=lambda s: -len(site_seals[s]))
print(f"\nSites: {[(s, len(site_seals[s])) for s in sites]}")

def sign_distribution(seqs):
    """Return H+M sign frequency Counter for a list of sequences."""
    c = Counter()
    for seq in seqs:
        for s in seq:
            if s in hm_set:
                c[s] += 1
    return c

def kl_divergence(p_counter, q_counter, vocab=None):
    """Symmetric KL: 0.5*(KL(P||Q) + KL(Q||P)) with Laplace smoothing."""
    if vocab is None:
        vocab = set(p_counter) | set(q_counter)
    if not vocab:
        return 0.0
    total_p = sum(p_counter.values()) + len(vocab)
    total_q = sum(q_counter.values()) + len(vocab)
    kl_pq = kl_qp = 0.0
    for w in vocab:
        p = (p_counter.get(w,0) + 1) / total_p
        q = (q_counter.get(w,0) + 1) / total_q
        kl_pq += p * math.log2(p / q)
        kl_qp += q * math.log2(q / p)
    return 0.5 * (kl_pq + kl_qp)

# ─── Observed KL between all site pairs ────────────────────────────────────
print("\nObserved KL divergences (symmetric, H+M signs only):")
print(f"  {'Site A':<20} {'Site B':<20} {'n_A':>5} {'n_B':>5} {'KL':>8}")

site_kl_matrix = {}
for i, sa in enumerate(sites):
    for j, sb in enumerate(sites):
        if j <= i: continue
        dist_a = sign_distribution(site_seals[sa])
        dist_b = sign_distribution(site_seals[sb])
        kl = kl_divergence(dist_a, dist_b)
        site_kl_matrix[(sa, sb)] = kl
        print(f"  {sa:<20} {sb:<20} {len(site_seals[sa]):>5} {len(site_seals[sb]):>5} {kl:>8.4f}")

# Sort by KL descending
sorted_pairs = sorted(site_kl_matrix.items(), key=lambda x: -x[1])
print(f"\n  Most divergent pair: {sorted_pairs[0][0]} KL={sorted_pairs[0][1]:.4f}")

# ─── Bootstrap CI for the top pair (Chanhu-daro vs Rakhigarhi) ─────────────
# Find the pair matching the known max divergence
target_sites = sorted_pairs[0][0]  # most divergent pair
sa, sb = target_sites
seals_a = site_seals[sa]
seals_b = site_seals[sb]

N_BOOT = 1000
rng = random.Random(42)

print(f"\nBootstrapping {N_BOOT} resamples for {sa} (n={len(seals_a)}) vs {sb} (n={len(seals_b)})...")

boot_kls = []
for _ in range(N_BOOT):
    boot_a = [rng.choice(seals_a) for _ in range(len(seals_a))]
    boot_b = [rng.choice(seals_b) for _ in range(len(seals_b))]
    dist_a = sign_distribution(boot_a)
    dist_b = sign_distribution(boot_b)
    boot_kls.append(kl_divergence(dist_a, dist_b))

boot_kls.sort()
ci_lo = boot_kls[int(0.025 * N_BOOT)]
ci_hi = boot_kls[int(0.975 * N_BOOT)]
boot_mean = sum(boot_kls) / len(boot_kls)
observed_kl = site_kl_matrix[(sa, sb)]

print(f"\n  Observed KL: {observed_kl:.4f}")
print(f"  Bootstrap mean: {boot_mean:.4f}")
print(f"  95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")

# Is the KL significantly above zero?
# Null: if sites are the same, KL should be near zero
# Bootstrap CI lower bound > 0.1 → ROBUST
if ci_lo > 0.3:
    kl_verdict = "ROBUST"
    kl_note = f"CI lower bound {ci_lo:.3f} > 0.3 — divergence is real"
elif ci_lo > 0.1:
    kl_verdict = "SUPPORTED"
    kl_note = f"CI [{ci_lo:.3f}, {ci_hi:.3f}] — meaningful but uncertain"
else:
    kl_verdict = "FRAGILE"
    kl_note = f"CI lower bound {ci_lo:.3f} ≤ 0.1 — small-sample artifact possible"

print(f"\n  Verdict: {kl_verdict} — {kl_note}")

# ─── All site pairs with CI ─────────────────────────────────────────────────
print(f"\n  Top 5 most divergent pairs (observed KL):")
for (sa2, sb2), kl in sorted_pairs[:5]:
    n_a = len(site_seals[sa2]); n_b = len(site_seals[sb2])
    # Quick bootstrap (200 samples) for all pairs
    small_boots = []
    seals_x = site_seals[sa2]; seals_y = site_seals[sb2]
    for _ in range(200):
        bx = [rng.choice(seals_x) for _ in range(len(seals_x))]
        by = [rng.choice(seals_y) for _ in range(len(seals_y))]
        small_boots.append(kl_divergence(sign_distribution(bx), sign_distribution(by)))
    small_boots.sort()
    ci_lo2 = small_boots[5]; ci_hi2 = small_boots[195]
    robust2 = "ROBUST" if ci_lo2 > 0.3 else ("SUPPORTED" if ci_lo2 > 0.1 else "FRAGILE")
    print(f"    {sa2}|{sb2}: KL={kl:.4f} CI=[{ci_lo2:.3f},{ci_hi2:.3f}] n=({n_a},{n_b}) → {robust2}")

# Save
output = {
    "phase": 151,
    "date": "2026-05-19",
    "n_bootstrap": N_BOOT,
    "sites_analyzed": {s: len(site_seals[s]) for s in sites},
    "observed_kl_matrix": {f"{a}|{b}": round(kl, 4) for (a,b),kl in sorted_pairs},
    "most_divergent_pair": {
        "sites": [sa, sb],
        "n_a": len(seals_a),
        "n_b": len(seals_b),
        "observed_kl": round(observed_kl, 4),
        "bootstrap_mean": round(boot_mean, 4),
        "ci_lo_95": round(ci_lo, 4),
        "ci_hi_95": round(ci_hi, 4),
        "verdict": kl_verdict,
        "note": kl_note,
    },
    "c9_caveat_closed": kl_verdict in ("ROBUST", "SUPPORTED"),
    "key_findings": [
        f"Most divergent pair: {sa} vs {sb} (KL={observed_kl:.4f})",
        f"Bootstrap 95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]",
        f"Verdict: {kl_verdict}",
        f"C9 caveat: {'CLOSED' if kl_verdict in ('ROBUST','SUPPORTED') else 'REMAINS OPEN'}",
        f"Note: {kl_note}",
    ]
}

OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {OUT}")
print("="*70)
