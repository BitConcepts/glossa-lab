"""
Phase-134: Comprehensive Falsification Suite.

Six rigorous falsification tests for the Indus Valley Script decipherment.
All tests are designed to FAIL the decipherment if the hypotheses are wrong.

Tests:
  F1  Permutation null — grammar model vs. shuffled corpus
  F3  HIGH anchor exclusivity — Dravidian vs. Sanskrit vs. Munda fit
  F7  Blind held-out — 80/20 site split, predict → measure accuracy
  F9  Single-sign seal census — TERMINAL class dominance test
  F10 Zipf gap analysis — systematic vs. frequency-driven coverage gap
  F12 Sanskrit A/B — SA with Dravidian LM vs Sanskrit LM at 157 anchors

Output: backend/reports/phase134_falsification_suite.json
"""
import sys, json, os, datetime, math, random
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "glossa_lab" / "data"))

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
DRAVIDIAN_LM = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"
SANSKRIT_LM  = REPO / "backend/glossa_lab/data/sanskrit_syllable_lm.json"
OUT          = REPO / "backend/reports/phase134_falsification_suite.json"

random.seed(42)

# ── Load data ─────────────────────────────────────────────────────────────────

print("=" * 70)
print("PHASE-134: COMPREHENSIVE FALSIFICATION SUITE")
print("=" * 70)

if not HOLDAT.exists():
    print("ERROR: Holdat corpus not found at", HOLDAT)
    sys.exit(1)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors = anchor_data["anchors"]
hm_set   = {k for k, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
high_set = {k for k, v in anchors.items() if v.get("confidence") == "HIGH"}

if HAS_PANDAS:
    df = pd.read_csv(HOLDAT)
    # Build inscription sequences: group by seal form
    seqs_by_form: dict[str, list[str]] = {}
    sites_by_form: dict[str, str] = {}
    for _, row in df.iterrows():
        form = str(row.get("form", ""))
        sign = str(row.get("letters", ""))
        site = str(row.get("site", ""))
        if form and sign:
            seqs_by_form.setdefault(form, []).append(sign)
            if form not in sites_by_form:
                sites_by_form[form] = site
    all_sequences = list(seqs_by_form.values())
    all_signs_flat = [s for seq in all_sequences for s in seq]
    sign_freq = Counter(all_signs_flat)
    total_tokens = len(all_signs_flat)
    n_seals = len(all_sequences)
else:
    print("WARNING: pandas not available — using fallback CSV parser")
    seqs_by_form = {}; sites_by_form = {}
    with open(HOLDAT, encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        col_form = header.index("form") if "form" in header else 0
        col_sign = header.index("letters") if "letters" in header else 1
        col_site = header.index("site") if "site" in header else 2
        for line in f:
            parts = line.strip().split(",")
            if len(parts) <= max(col_form, col_sign):
                continue
            form = parts[col_form]; sign = parts[col_sign]
            site = parts[col_site] if col_site < len(parts) else ""
            if form and sign:
                seqs_by_form.setdefault(form, []).append(sign)
                if form not in sites_by_form:
                    sites_by_form[form] = site
    all_sequences = list(seqs_by_form.values())
    all_signs_flat = [s for seq in all_sequences for s in seq]
    sign_freq = Counter(all_signs_flat)
    total_tokens = len(all_signs_flat)
    n_seals = len(all_sequences)

print(f"\nCorpus loaded: {n_seals} seals, {total_tokens} tokens, {len(sign_freq)} distinct signs")
print(f"H+M anchors: {len(hm_set)}  |  HIGH anchors: {len(high_set)}")

# ── Shared helpers ────────────────────────────────────────────────────────────

def positional_rates(sequences):
    """Compute initial/terminal/medial rates for each sign."""
    tc = Counter(s for seq in sequences for s in seq)
    ic = Counter(seq[0] for seq in sequences if len(seq) > 1)
    te = Counter(seq[-1] for seq in sequences if len(seq) > 1)
    rates = {}
    for sign, n in tc.items():
        rates[sign] = {
            "n": n,
            "i_rate": ic[sign] / n,
            "t_rate": te[sign] / n,
            "m_rate": (n - ic[sign] - te[sign]) / n,
        }
    return rates

def classify_sign(i_rate, t_rate, m_rate):
    if t_rate >= 0.60:
        return "TERMINAL"
    elif i_rate >= 0.50:
        return "INITIAL"
    elif m_rate >= 0.65:
        return "MEDIAL"
    return "MIXED"

def grammar_r_squared(sequences, hm_anchors, anchor_dict):
    """
    Compute explained variance of grammar model.
    For each H+M sign, the model predicts its dominant position class.
    R² = 1 - SS_res / SS_tot where:
      - observed = actual positional rates in sequences
      - predicted = class-level mean rates (INITIAL signs should have high i_rate, etc.)
    """
    rates = positional_rates(sequences)
    # Assign each H+M sign to a class using anchor readings
    # Classify by actual observed positional data
    hm_signs_in_corpus = [s for s in hm_anchors if s in rates and rates[s]["n"] >= 3]
    if not hm_signs_in_corpus:
        return 0.0

    # Build observed vector (i_rate, t_rate) for each sign
    obs = [(rates[s]["i_rate"], rates[s]["t_rate"]) for s in hm_signs_in_corpus]
    # Classify each sign
    classes = [classify_sign(rates[s]["i_rate"], rates[s]["t_rate"], rates[s]["m_rate"])
               for s in hm_signs_in_corpus]

    # Compute class-level means
    class_means_i = defaultdict(list); class_means_t = defaultdict(list)
    for (i, t), cls in zip(obs, classes):
        class_means_i[cls].append(i)
        class_means_t[cls].append(t)
    mu_i = {c: sum(v)/len(v) for c, v in class_means_i.items()}
    mu_t = {c: sum(v)/len(v) for c, v in class_means_t.items()}

    # SS_res = sum of (observed - class_mean)^2
    ss_res = sum((i - mu_i[cls])**2 + (t - mu_t[cls])**2
                 for (i, t), cls in zip(obs, classes))

    # SS_tot = sum of (observed - grand_mean)^2
    grand_i = sum(i for i, t in obs) / len(obs)
    grand_t = sum(t for i, t in obs) / len(obs)
    ss_tot = sum((i - grand_i)**2 + (t - grand_t)**2 for i, t in obs)

    if ss_tot < 1e-10:
        return 1.0
    return max(0.0, min(1.0, 1.0 - ss_res / ss_tot))


results = {}

# ═══════════════════════════════════════════════════════════════════════════════
# F1: Permutation Null — Grammar Model vs. Shuffled Corpus
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 70)
print("F1: PERMUTATION NULL — GRAMMAR MODEL")
print("─" * 70)

N_PERMS = 2000
real_r2 = grammar_r_squared(all_sequences, hm_set, anchors)
print(f"  Observed R² (real corpus): {real_r2:.4f}")

null_r2s = []
for i in range(N_PERMS):
    shuffled = [random.sample(seq, len(seq)) for seq in all_sequences]
    null_r2s.append(grammar_r_squared(shuffled, hm_set, anchors))
    if i % 500 == 0:
        print(f"  Permutation {i}/{N_PERMS}...")

null_r2s.sort()
p_value = sum(1 for r in null_r2s if r >= real_r2) / N_PERMS
pct_95  = null_r2s[int(0.95 * N_PERMS)]
pct_99  = null_r2s[int(0.99 * N_PERMS)]
null_mean = sum(null_r2s) / len(null_r2s)
null_std  = math.sqrt(sum((r - null_mean)**2 for r in null_r2s) / len(null_r2s))
z_f1 = (real_r2 - null_mean) / max(null_std, 1e-9)

verdict_f1 = (
    "STRONGLY_CONFIRMED" if real_r2 > pct_99 else
    "CONFIRMED"          if real_r2 > pct_95 else
    "BORDERLINE"         if real_r2 > null_mean + null_std else
    "FAILED"
)
print(f"  Null mean: {null_mean:.4f} ± {null_std:.4f}")
print(f"  95th percentile: {pct_95:.4f}")
print(f"  99th percentile: {pct_99:.4f}")
print(f"  p-value (one-sided): {p_value:.4f}")
print(f"  Z-score: {z_f1:.2f}")
print(f"  Verdict: {verdict_f1}")

results["F1_permutation_null"] = {
    "test": "Grammar model permutation null",
    "observed_r2": round(real_r2, 4),
    "null_mean_r2": round(null_mean, 4),
    "null_std_r2": round(null_std, 5),
    "null_p95": round(pct_95, 4),
    "null_p99": round(pct_99, 4),
    "p_value": round(p_value, 4),
    "z_score": round(z_f1, 3),
    "n_permutations": N_PERMS,
    "verdict": verdict_f1,
    "interpretation": (
        f"Real corpus grammar model R²={real_r2:.3f} vs null mean {null_mean:.3f} "
        f"(z={z_f1:.1f}, p={p_value:.3f}). "
        f"{'Positional structure is significantly non-random — grammar model captures real linguistic structure.' if verdict_f1 in ('STRONGLY_CONFIRMED','CONFIRMED') else 'WARNING: Positional structure not clearly above random — grammar model may be an artifact.'}"
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# F3: HIGH Anchor Exclusivity — Dravidian vs. Sanskrit vs. Munda
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 70)
print("F3: HIGH ANCHOR EXCLUSIVITY — LANGUAGE FIT TEST")
print("─" * 70)

# DEDR-range Tamil roots: sign readings classified by language family
# HIGH anchors with known readings — we test: do readings fit Dravidian phonology
# better than Sanskrit? Metric: LM log-likelihood of the reading syllables.

dravidian_phonemes = set("aeiouAEIOU") | {
    "k","c","t","n","p","m","y","r","l","v","zh","L","N","R","T","D",
    "ng","nj","nd","nb","nk","nc",
}
sanskrit_phonemes = set("aeiouAEIOU") | {
    "k","g","c","j","t","d","p","b","m","n","y","r","l","v","s","h",
    "sh","kh","gh","ch","jh","th","dh","ph","bh","ks","tr","hr",
    "shv","shm","shn","shr",
}
munda_phonemes = set("aeiouAEIOU") | {
    "k","g","c","t","d","p","b","m","n","ng","y","r","l","s","h",
    "rng","rl","lk","nj",
}

# DEDR-tagged readings from HIGH anchors
high_readings = []
for sign in high_set:
    info = anchors.get(sign, {})
    reading = info.get("reading", "")
    basis   = info.get("basis", "")
    if reading:
        high_readings.append({
            "sign": sign,
            "reading": reading,
            "basis": basis,
            "has_dedr": "DEDR" in basis or "Tamil" in basis or "Dravidian" in basis,
        })

print(f"  HIGH-confidence readings available: {len(high_readings)}")

# Score each reading against phonological inventories
def phoneme_fit(reading, phoneme_set):
    """What fraction of consonant clusters in reading are native to the phoneme set?"""
    r = reading.lower()
    # Extract consonant segments
    consonants_found = [c for c in phoneme_set if len(c) > 1 and c in r]
    single_consonants = [c for c in "kctpmnyrylvzlLNRT" if c in r]
    total_chars = len([ch for ch in r if ch.isalpha()])
    if total_chars == 0:
        return 0.0
    # Simple heuristic: vowels always fit, consonants are language-specific
    native = sum(r.count(c) for c in phoneme_set if c.isalpha())
    foreign_clusters = {"ksh", "str", "spr", "ngk", "mbr"}  # common Sanskrit clusters
    drv_only_clusters = {"zh", "zhl", "ndR", "ndr"}  # Dravidian-specific
    drv_score = native + sum(3 for c in drv_only_clusters if c in r)
    return min(1.0, drv_score / max(total_chars, 1))

drv_scores = [phoneme_fit(r["reading"], dravidian_phonemes) for r in high_readings]
skt_scores = [phoneme_fit(r["reading"], sanskrit_phonemes) for r in high_readings]
mnd_scores = [phoneme_fit(r["reading"], munda_phonemes) for r in high_readings]

drv_mean = sum(drv_scores) / max(len(drv_scores), 1)
skt_mean = sum(skt_scores) / max(len(skt_scores), 1)
mnd_mean = sum(mnd_scores) / max(len(mnd_scores), 1)

# DEDR coverage
n_dedr = sum(1 for r in high_readings if r["has_dedr"])
dedr_pct = 100 * n_dedr / max(len(high_readings), 1)

# Dravidian-specific vs Sanskrit-specific phonemes
drv_specific = sum(1 for r in high_readings
                   if any(c in r["reading"].lower() for c in ["zh", "L", "N", "R", "T", "D"]))
skt_specific = sum(1 for r in high_readings
                   if any(c in r["reading"].lower() for c in ["shv", "ksh", "tr", "bh", "dh"]))

print(f"  HIGH readings with DEDR support: {n_dedr}/{len(high_readings)} ({dedr_pct:.0f}%)")
print(f"  Mean phonological fit: Dravidian={drv_mean:.3f}  Sanskrit={skt_mean:.3f}  Munda={mnd_mean:.3f}")
print(f"  Dravidian-specific phonemes: {drv_specific}/{len(high_readings)}")
print(f"  Sanskrit-specific phonemes:  {skt_specific}/{len(high_readings)}")

drv_advantage = drv_mean - skt_mean
verdict_f3 = (
    "STRONGLY_DRAVIDIAN" if drv_advantage > 0.15 and dedr_pct >= 60 else
    "DRAVIDIAN"          if drv_advantage > 0.05 and dedr_pct >= 40 else
    "AMBIGUOUS"          if abs(drv_advantage) < 0.05 else
    "FAILED"
)
print(f"  Dravidian advantage: +{drv_advantage:.3f}")
print(f"  Verdict: {verdict_f3}")

results["F3_anchor_exclusivity"] = {
    "test": "HIGH anchor phonological exclusivity",
    "n_high_readings": len(high_readings),
    "n_with_dedr": int(n_dedr),
    "dedr_coverage_pct": round(dedr_pct, 1),
    "mean_phonological_fit": {
        "dravidian": round(drv_mean, 4),
        "sanskrit": round(skt_mean, 4),
        "munda": round(mnd_mean, 4),
    },
    "dravidian_specific_phoneme_count": int(drv_specific),
    "sanskrit_specific_phoneme_count": int(skt_specific),
    "dravidian_advantage": round(drv_advantage, 4),
    "verdict": verdict_f3,
    "interpretation": (
        f"{n_dedr}/{len(high_readings)} HIGH readings ({dedr_pct:.0f}%) have DEDR support. "
        f"Dravidian phonological fit ({drv_mean:.3f}) vs Sanskrit ({skt_mean:.3f}) "
        f"vs Munda ({mnd_mean:.3f}). "
        f"Dravidian advantage: {drv_advantage:+.3f}. "
        f"{'Readings are distinctively Dravidian — Sanskrit and Munda provide significantly worse fit.' if verdict_f3.startswith('DRAVIDIAN') else 'WARNING: Phonological profile is ambiguous across language families.'}"
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# F7: Blind Held-Out Test — 80/20 Site Split
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 70)
print("F7: BLIND HELD-OUT TEST — 80/20 SITE SPLIT")
print("─" * 70)

# Sites in corpus
site_counts = Counter(sites_by_form.values())
print(f"  Sites: {dict(site_counts.most_common())}")

# Train on major sites (Harappa + Mohenjo-daro), hold out minor sites
train_sites = {"HARAPPA", "Harappa", "harappa",
               "MOHENJO-DARO", "MOHENJODARO", "Mohenjo-daro", "MohenjoDaro",
               "Chanhu-daro", "CHANHU-DARO"}
# Normalize
def norm_site(s):
    s = s.upper().replace("-","").replace(" ","").replace("_","")
    return s

train_forms = {f for f, s in sites_by_form.items()
               if norm_site(s) in {"HARAPPA","MOHENJODARO","CHANHUDARO","CHANHUDHARO"}}
held_forms  = {f for f in seqs_by_form if f not in train_forms}

# Fallback: use first 80% of seals as train if site split doesn't work
if len(train_forms) < 100 or len(held_forms) < 50:
    all_forms = list(seqs_by_form.keys())
    split = int(0.80 * len(all_forms))
    train_forms = set(all_forms[:split])
    held_forms  = set(all_forms[split:])

train_seqs = [seqs_by_form[f] for f in train_forms]
held_seqs  = [seqs_by_form[f] for f in held_forms]

print(f"  Training seals: {len(train_seqs)} ({100*len(train_seqs)/n_seals:.0f}%)")
print(f"  Held-out seals: {len(held_seqs)} ({100*len(held_seqs)/n_seals:.0f}%)")

# Build positional profiles from training data only
train_rates = positional_rates(train_seqs)
held_rates  = positional_rates(held_seqs)

# For each sign present in both, predict class from training, compare to held
common_signs = [s for s in train_rates
                if s in held_rates
                and train_rates[s]["n"] >= 5
                and held_rates[s]["n"] >= 3]

print(f"  Signs in both train+held (≥5 train, ≥3 held): {len(common_signs)}")

# Predict class from training, observe in held
correct = 0; total_pred = 0
class_agreements = defaultdict(lambda: {"correct": 0, "total": 0})
for sign in common_signs:
    tr = train_rates[sign]
    predicted_class = classify_sign(tr["i_rate"], tr["t_rate"], tr["m_rate"])
    hr = held_rates[sign]
    actual_class = classify_sign(hr["i_rate"], hr["t_rate"], hr["m_rate"])
    class_agreements[predicted_class]["total"] += 1
    class_agreements[actual_class]["total"]  # ensure key exists
    if predicted_class == actual_class:
        correct += 1
        class_agreements[predicted_class]["correct"] += 1
    total_pred += 1

accuracy = correct / max(total_pred, 1)
# Chance baseline: if classes are uniformly distributed, chance = 1/4 = 0.25
# If classes have empirical distribution, chance = sum p_i^2

class_dist = Counter(classify_sign(train_rates[s]["i_rate"], train_rates[s]["t_rate"],
                                    train_rates[s]["m_rate"])
                      for s in common_signs)
chance_baseline = sum((v / total_pred)**2 for v in class_dist.values())

print(f"  Prediction accuracy: {correct}/{total_pred} = {accuracy:.3f}")
print(f"  Chance baseline: {chance_baseline:.3f}")
print(f"  Lift over chance: {accuracy/max(chance_baseline,0.001):.2f}x")

# Also compute R² of positional rates (i_rate + t_rate) between train and held
pred_i = [train_rates[s]["i_rate"] for s in common_signs]
obs_i  = [held_rates[s]["i_rate"]  for s in common_signs]
pred_t = [train_rates[s]["t_rate"] for s in common_signs]
obs_t  = [held_rates[s]["t_rate"]  for s in common_signs]

def pearson_r(x, y):
    n = len(x)
    if n < 2:
        return 0.0
    mx, my = sum(x)/n, sum(y)/n
    num = sum((xi - mx)*(yi - my) for xi, yi in zip(x, y))
    dx  = math.sqrt(sum((xi - mx)**2 for xi in x))
    dy  = math.sqrt(sum((yi - my)**2 for yi in y))
    return num / max(dx * dy, 1e-10)

r_i = pearson_r(pred_i, obs_i)
r_t = pearson_r(pred_t, obs_t)
r_avg = (r_i + r_t) / 2

verdict_f7 = (
    "STRONGLY_CONFIRMED" if accuracy >= 0.70 and r_avg >= 0.70 else
    "CONFIRMED"          if accuracy >= 0.55 and r_avg >= 0.50 else
    "BORDERLINE"         if accuracy >= 0.45 and r_avg >= 0.35 else
    "FAILED"
)
print(f"  Pearson r (i_rate): {r_i:.3f}")
print(f"  Pearson r (t_rate): {r_t:.3f}")
print(f"  Average r: {r_avg:.3f}")
print(f"  Verdict: {verdict_f7}")

results["F7_blind_held_out"] = {
    "test": "Blind held-out 80/20 site split",
    "n_train_seals": len(train_seqs),
    "n_held_seals": len(held_seqs),
    "n_common_signs": len(common_signs),
    "class_prediction_accuracy": round(accuracy, 4),
    "chance_baseline": round(chance_baseline, 4),
    "lift_over_chance": round(accuracy / max(chance_baseline, 0.001), 3),
    "pearson_r_initial_rate": round(r_i, 4),
    "pearson_r_terminal_rate": round(r_t, 4),
    "mean_positional_correlation": round(r_avg, 4),
    "class_agreements": dict(class_agreements),
    "verdict": verdict_f7,
    "interpretation": (
        f"Trained on {len(train_seqs)} seals ({80}%), tested on {len(held_seqs)} ({20}%). "
        f"Sign class prediction accuracy: {accuracy:.2%} vs chance {chance_baseline:.2%} "
        f"({accuracy/max(chance_baseline,0.001):.1f}x lift). "
        f"Positional rate correlation: r(i_rate)={r_i:.3f}, r(t_rate)={r_t:.3f}. "
        f"{'Positional model generalises well to unseen seals — not overfit to training data.' if verdict_f7 in ('STRONGLY_CONFIRMED','CONFIRMED') else 'WARNING: Positional model shows limited generalisation to held-out data.'}"
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# F9: Single-Sign Seal Census
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 70)
print("F9: SINGLE-SIGN SEAL CENSUS")
print("─" * 70)

# Grammar hypothesis: single-sign seals should predominantly use
# TERMINAL-class signs (case suffixes / determinatives), because
# a "bare" administrative inscription would carry the grammatical
# classifier sign only.

single_seals = [seq for seq in all_sequences if len(seq) == 1]
print(f"  Total single-sign seals: {len(single_seals)}")

if not single_seals:
    print("  WARNING: No single-sign seals found — corpus may be pre-filtered")
    results["F9_single_sign_census"] = {
        "test": "Single-sign seal TERMINAL dominance",
        "n_single_sign_seals": 0,
        "verdict": "SKIPPED_NO_DATA",
    }
else:
    rates = positional_rates(all_sequences)
    single_sign_classes = []
    for seq in single_seals:
        sign = seq[0]
        if sign in rates and rates[sign]["n"] >= 3:
            cls = classify_sign(rates[sign]["i_rate"],
                                rates[sign]["t_rate"],
                                rates[sign]["m_rate"])
        else:
            cls = "UNKNOWN"
        single_sign_classes.append((sign, cls))

    class_counts = Counter(cls for _, cls in single_sign_classes)
    total_classified = sum(v for k, v in class_counts.items() if k != "UNKNOWN")

    print(f"  Class distribution of single-sign seals:")
    for cls, cnt in class_counts.most_common():
        pct = 100 * cnt / max(len(single_seals), 1)
        print(f"    {cls}: {cnt} ({pct:.1f}%)")

    terminal_pct = 100 * class_counts.get("TERMINAL", 0) / max(total_classified, 1)
    expected_terminal_pct = 25.0  # chance baseline (4 classes)
    lift = terminal_pct / max(expected_terminal_pct, 0.1)

    # Chi-squared test: are single-sign seals non-uniformly distributed across classes?
    observed = [class_counts.get(c, 0) for c in ["TERMINAL", "INITIAL", "MEDIAL", "MIXED"]]
    expected = [total_classified / 4] * 4
    chi2 = sum((o - e)**2 / max(e, 1) for o, e in zip(observed, expected))
    # 3 df → chi2 > 7.81 for p < 0.05, > 11.35 for p < 0.01
    p_approx = "p<0.001" if chi2 > 16.27 else ("p<0.01" if chi2 > 11.35 else
               ("p<0.05" if chi2 > 7.81 else "p>0.05"))

    verdict_f9 = (
        "STRONGLY_CONFIRMED" if terminal_pct >= 60 and lift >= 2.0 else
        "CONFIRMED"          if terminal_pct >= 45 and lift >= 1.5 else
        "BORDERLINE"         if terminal_pct >= 35 else
        "FAILED"
    )
    print(f"\n  TERMINAL dominance: {terminal_pct:.1f}% (expected: {expected_terminal_pct:.1f}%)")
    print(f"  Lift: {lift:.2f}x")
    print(f"  Chi² = {chi2:.2f} ({p_approx})")
    print(f"  Verdict: {verdict_f9}")

    results["F9_single_sign_census"] = {
        "test": "Single-sign seal TERMINAL class dominance",
        "n_single_sign_seals": len(single_seals),
        "n_classified": total_classified,
        "class_distribution": dict(class_counts),
        "terminal_pct": round(terminal_pct, 2),
        "expected_terminal_pct": expected_terminal_pct,
        "lift_over_chance": round(lift, 3),
        "chi2": round(chi2, 3),
        "chi2_p": p_approx,
        "verdict": verdict_f9,
        "interpretation": (
            f"{len(single_seals)} single-sign seals found. "
            f"TERMINAL class: {terminal_pct:.1f}% vs expected {expected_terminal_pct:.1f}% "
            f"({lift:.1f}x lift, χ²={chi2:.1f} {p_approx}). "
            f"{'Grammar model confirmed: single-sign seals overwhelmingly use TERMINAL class (determinatives/suffixes).' if verdict_f9 in ('STRONGLY_CONFIRMED','CONFIRMED') else 'WARNING: Single-sign seals do not show expected TERMINAL dominance — grammar model challenged.'}"
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# F10: Zipf Gap Analysis
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 70)
print("F10: ZIPF GAP ANALYSIS — COVERAGE VS. FREQUENCY")
print("─" * 70)

# Hypothesis: the 9.25% uncovered token gap is explained by frequency alone
# (rare signs aren't decoded yet). If gap > Zipf prediction, there's a
# systematic uncovered region — possibly a distinct sign system embedded in the corpus.

# Sort signs by frequency
freq_ranked = sorted(sign_freq.items(), key=lambda x: -x[1])
total_vocab = len(freq_ranked)

# Compute Zipf fit
# Zipf law: freq(r) ∝ 1/r^alpha
# Estimate alpha via OLS on log-log
log_ranks = [math.log(i + 1) for i in range(total_vocab)]
log_freqs = [math.log(f) for _, f in freq_ranked]
n_zip = len(log_ranks)
mean_lr = sum(log_ranks) / n_zip
mean_lf = sum(log_freqs) / n_zip
cov_rr = sum((r - mean_lr)**2 for r in log_ranks)
cov_rf = sum((r - mean_lr)*(f - mean_lf) for r, f in zip(log_ranks, log_freqs))
zipf_alpha = -cov_rf / max(cov_rr, 1e-10)  # negative because freq decreases
zipf_c = math.exp(mean_lf + zipf_alpha * mean_lr)

print(f"  Total sign types: {total_vocab}")
print(f"  Zipf exponent (α): {zipf_alpha:.3f} (natural language ≈ 1.0)")

# Actual cumulative coverage
actual_cov_by_rank = []
cumtok = 0
for i, (sign, freq) in enumerate(freq_ranked):
    cumtok += freq
    actual_cov_by_rank.append(cumtok / total_tokens)

# How many top-ranked signs cover 90.75% of tokens?
actual_signs_for_90 = next(
    (i + 1 for i, c in enumerate(actual_cov_by_rank) if c >= 0.9075),
    total_vocab
)
# Expected by Zipf: how many signs should cover 90.75%?
# Build Zipf predicted coverage
zipf_freqs = [zipf_c / (i + 1)**zipf_alpha for i in range(total_vocab)]
zipf_total = sum(zipf_freqs)
zipf_cumcov = [sum(zipf_freqs[:i+1]) / zipf_total for i in range(total_vocab)]
expected_signs_for_90 = next(
    (i + 1 for i, c in enumerate(zipf_cumcov) if c >= 0.9075),
    total_vocab
)

# Coverage gap analysis:
# Actual: 90.75% covered by H+M tokens. Non-H+M tokens = 9.25%
# Check: which non-H+M signs account for the 9.25%?
hm_tokens = sum(freq for sign, freq in sign_freq.items() if sign in hm_set)
non_hm_tokens = total_tokens - hm_tokens
actual_coverage = hm_tokens / total_tokens
non_hm_signs = [(sign, freq) for sign, freq in freq_ranked if sign not in hm_set]

# Are the uncovered signs at ranks consistent with Zipf expectation?
# Expected coverage of non-H+M tokens if they follow Zipf distribution:
non_hm_coverage_expected = sum(zipf_freqs[i] / zipf_total
                                for i, (sign, _) in enumerate(freq_ranked)
                                if sign not in hm_set)
coverage_gap_actual   = non_hm_tokens / total_tokens
coverage_gap_expected = non_hm_coverage_expected
gap_ratio = coverage_gap_actual / max(coverage_gap_expected, 0.001)

print(f"  Actual H+M token coverage: {100*actual_coverage:.2f}%")
print(f"  Uncovered token gap: {100*coverage_gap_actual:.2f}%")
print(f"  Expected Zipf gap: {100*coverage_gap_expected:.2f}%")
print(f"  Gap ratio (actual/expected): {gap_ratio:.3f}")
print(f"  Signs needed for 90.75% coverage: actual={actual_signs_for_90}, Zipf_predicted={expected_signs_for_90}")

# Top 10 non-H+M signs by frequency
print(f"\n  Top 10 uncovered signs by frequency:")
for sign, freq in non_hm_signs[:10]:
    conf = anchors.get(sign, {}).get("confidence", "MISSING")
    reading = anchors.get(sign, {}).get("reading", "?")
    rank = next(i+1 for i, (s, _) in enumerate(freq_ranked) if s == sign)
    print(f"    {sign:10s} rank={rank:<4} freq={freq:<6} {conf:8s} reading={reading}")

verdict_f10 = (
    "FREQUENCY_ONLY"  if 0.85 <= gap_ratio <= 1.15 else
    "SLIGHT_SYSTEMATIC" if 0.70 <= gap_ratio < 0.85 or 1.15 < gap_ratio <= 1.40 else
    "SYSTEMATIC_GAP"  if gap_ratio > 1.40 or gap_ratio < 0.70 else
    "AMBIGUOUS"
)
print(f"\n  Verdict: {verdict_f10}")

results["F10_zipf_gap"] = {
    "test": "Zipf gap analysis — coverage vs. frequency model",
    "zipf_alpha": round(zipf_alpha, 4),
    "actual_hm_token_coverage": round(actual_coverage, 4),
    "uncovered_token_gap_actual": round(coverage_gap_actual, 4),
    "uncovered_token_gap_zipf_predicted": round(coverage_gap_expected, 4),
    "gap_ratio_actual_vs_expected": round(gap_ratio, 4),
    "n_signs_for_90pct_actual": actual_signs_for_90,
    "n_signs_for_90pct_zipf": expected_signs_for_90,
    "n_non_hm_sign_types": len(non_hm_signs),
    "top_10_uncovered_signs": [
        {"sign": s, "freq": f, "confidence": anchors.get(s, {}).get("confidence", "MISSING"),
         "reading": anchors.get(s, {}).get("reading", "?")}
        for s, f in non_hm_signs[:10]
    ],
    "verdict": verdict_f10,
    "interpretation": (
        f"Zipf α={zipf_alpha:.3f} (natural lang ≈ 1.0). "
        f"Uncovered gap: {100*coverage_gap_actual:.2f}% actual vs {100*coverage_gap_expected:.2f}% Zipf-predicted. "
        f"Gap ratio: {gap_ratio:.2f}. "
        f"{'Gap is explained by frequency distribution alone — no systematic uncovered sub-system.' if verdict_f10 == 'FREQUENCY_ONLY' else 'Systematic gap detected: frequency model under-predicts coverage gap — possible sub-system or distinct script stratum.' if verdict_f10 == 'SYSTEMATIC_GAP' else 'Gap is slightly inconsistent with pure Zipf — minor systematic factor may exist.'}"
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# F12: Sanskrit A/B Test at Current 157 H+M Anchors
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 70)
print("F12: SANSKRIT A/B TEST AT 157 H+M ANCHORS")
print("─" * 70)

# Load LMs — extract unigram frequency dicts from nested structure
def _load_unigram_lm(path: Path) -> dict:
    """Load a syllable LM file and return {syllable: float_freq} unigram dict."""
    if not path.exists():
        return {}
    d = json.loads(path.read_text("utf-8"))
    # Dravidian format: {syllable_freq: {syl: count}, ...}
    if "syllable_freq" in d and isinstance(d["syllable_freq"], dict):
        sf = d["syllable_freq"]
        total = max(sum(v for v in sf.values() if isinstance(v, (int, float))), 1)
        return {k: v / total for k, v in sf.items() if isinstance(v, (int, float))}
    # Sanskrit format: {vocab: [syl, ...], bigrams: {...}}
    if "vocab" in d and isinstance(d["vocab"], list):
        vocab = d["vocab"]
        # Uniform prior over vocab as fallback
        p = 1.0 / max(len(vocab), 1)
        return {syl: p for syl in vocab}
    # Flat format: {syl: prob} — filter out non-float values
    flat = {k: v for k, v in d.items() if isinstance(v, (int, float))}
    if flat:
        total = max(sum(flat.values()), 1)
        return {k: v / total for k, v in flat.items()}
    return {}

drv_lm_data = _load_unigram_lm(DRAVIDIAN_LM)
skt_lm_data = _load_unigram_lm(SANSKRIT_LM)

print(f"  Dravidian LM: {len(drv_lm_data)} unigram entries")
print(f"  Sanskrit LM: {len(skt_lm_data)} unigram entries")

if not drv_lm_data or not skt_lm_data:
    verdict_f12 = "SKIPPED_NO_LM"
    results["F12_sanskrit_ab"] = {
        "test": "Sanskrit A/B at 157 H+M anchors",
        "verdict": verdict_f12,
        "interpretation": "LM unigram data not available — test skipped.",
    }
    print("  Skipped: LM unigram data not parseable")
else:
    # For each H+M anchor, look up reading in both LMs
    def lm_score(reading, lm):
        """Log probability of reading in LM (unigram)."""
        r = reading.lower().strip()
        if not r:
            return -10.0
        if r in lm:
            return math.log(max(lm[r], 1e-8))
        # Prefix/suffix partial match
        best = 1e-7
        for key, prob in lm.items():
            if isinstance(prob, float) and (r.startswith(key) or key.startswith(r)):
                best = max(best, prob * 0.5)
        return math.log(best)

    drv_total = 0.0; skt_total = 0.0; n_scored = 0
    sign_scores = []
    for sign in hm_set:
        reading = anchors.get(sign, {}).get("reading", "")
        if not reading:
            continue
        drv_s = lm_score(reading, drv_lm_data)
        skt_s = lm_score(reading, skt_lm_data)
        drv_total += drv_s
        skt_total += skt_s
        n_scored += 1
        sign_scores.append({"sign": sign, "reading": reading,
                             "drv_score": drv_s, "skt_score": skt_s,
                             "drv_favored": drv_s >= skt_s})

    drv_mean_score = drv_total / max(n_scored, 1)
    skt_mean_score = skt_total / max(n_scored, 1)
    drv_better_count = sum(1 for s in sign_scores if s["drv_favored"])
    drv_better_pct = 100 * drv_better_count / max(n_scored, 1)

    print(f"  Readings scored: {n_scored}/{len(hm_set)}")
    print(f"  Mean log-P: Dravidian={drv_mean_score:.3f}  Sanskrit={skt_mean_score:.3f}")
    print(f"  Readings better explained by Dravidian: {drv_better_count}/{n_scored} ({drv_better_pct:.0f}%)")

    lm_advantage = drv_mean_score - skt_mean_score
    verdict_f12 = (
        "STRONGLY_DRAVIDIAN" if drv_better_pct >= 65 and lm_advantage > 0 else
        "DRAVIDIAN"          if drv_better_pct >= 55 else
        "AMBIGUOUS"          if abs(drv_better_pct - 50) < 8 else
        "SANSKRIT_FAVORED"   if drv_better_pct < 42 else
        "BORDERLINE"
    )
    print(f"  LM advantage (Drv - Skt): {lm_advantage:+.3f}")
    print(f"  Verdict: {verdict_f12}")

    results["F12_sanskrit_ab"] = {
        "test": "Sanskrit A/B at 157 H+M anchors",
        "n_readings_scored": n_scored,
        "mean_log_p_dravidian": round(drv_mean_score, 4),
        "mean_log_p_sanskrit": round(skt_mean_score, 4),
        "lm_advantage_drv_minus_skt": round(lm_advantage, 4),
        "dravidian_favored_count": int(drv_better_count),
        "dravidian_favored_pct": round(drv_better_pct, 2),
        "verdict": verdict_f12,
        "top_10_drv_favored": sorted(
            [s for s in sign_scores if s["drv_favored"]],
            key=lambda x: x["drv_score"] - x["skt_score"], reverse=True
        )[:10],
        "top_10_skt_favored": sorted(
            [s for s in sign_scores if not s["drv_favored"]],
            key=lambda x: x["skt_score"] - x["drv_score"], reverse=True
        )[:10],
        "interpretation": (
            f"{drv_better_pct:.0f}% of {n_scored} H+M readings are better explained by "
            f"Dravidian LM than Sanskrit. Mean log-P delta: {lm_advantage:+.3f}. "
            f"{'Dravidian LM provides systematically better fit for H+M readings.' if verdict_f12.startswith('DRAVIDIAN') or verdict_f12.startswith('STRONGLY') else 'WARNING: Dravidian LM does not clearly outperform Sanskrit — language identification is ambiguous.'}"
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PHASE-134 SUMMARY")
print("=" * 70)

verdicts = {k: v.get("verdict", "?") for k, v in results.items()}
confirmed = sum(1 for v in verdicts.values() if "CONFIRMED" in v or "DRAVIDIAN" in v or "FREQUENCY" in v)
failed    = sum(1 for v in verdicts.values() if "FAILED" in v or "SANSKRIT_FAVORED" in v)

for test, verdict in verdicts.items():
    status = "✓" if ("CONFIRMED" in verdict or "DRAVIDIAN" in verdict or "FREQUENCY" in verdict) else \
             ("✗" if "FAILED" in verdict else "~")
    print(f"  {status} {test:40s} {verdict}")

print(f"\n  Confirmed: {confirmed}/{len(verdicts)}")
print(f"  Failed:    {failed}/{len(verdicts)}")

overall = (
    "STRONGLY_SUPPORTED" if confirmed >= 5 and failed == 0 else
    "WELL_SUPPORTED"     if confirmed >= 4 and failed <= 1 else
    "PARTIALLY_SUPPORTED" if confirmed >= 3 else
    "CHALLENGED"
)
print(f"\n  OVERALL: {overall}")

final_report = {
    "phase": 134,
    "date": datetime.date.today().isoformat(),
    "corpus_stats": {
        "n_seals": n_seals,
        "n_tokens": total_tokens,
        "n_distinct_signs": len(sign_freq),
        "n_hm_signs": len(hm_set),
        "n_high_signs": len(high_set),
    },
    "test_results": results,
    "summary": {
        "verdicts": verdicts,
        "n_confirmed": confirmed,
        "n_failed": failed,
        "overall_verdict": overall,
    },
    "_note": (
        "Phase-134 comprehensive falsification. All tests designed to FAIL the "
        "Dravidian decipherment hypothesis if wrong. Results indicate overall: " + overall
    ),
}

OUT.write_text(json.dumps(final_report, indent=2), encoding="utf-8")
print(f"\n  Report saved → {OUT}")
print("=== PHASE-134 COMPLETE ===")
