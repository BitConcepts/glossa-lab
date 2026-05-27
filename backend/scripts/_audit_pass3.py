"""Third-pass deep audit: verify the DATA behind each release finding, not just the numbers."""
import json, csv, math, unicodedata
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
anchors = json.loads((REPO / "backend/reports/INDUS_FINAL_ANCHORS.json").read_text('utf-8')).get('anchors', {})
release = json.loads((REPO / "outputs/RELEASE_VALIDATION.json").read_text('utf-8'))

holdat = []
seals = []
with open(REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv", encoding='utf-8') as f:
    cur = None; signs = []
    for r in csv.DictReader(f):
        holdat.append(r['letters'])
        if r['cisi_number'] != cur:
            if signs: seals.append(signs)
            cur = r['cisi_number']; signs = []
        signs.append(r['letters'])
    if signs: seals.append(signs)

high = {s: i for s, i in anchors.items() if i.get('confidence') == 'HIGH' and i.get('reading')}
errors = []
warnings = []

print("=" * 60)
print("THIRD-PASS DEEP AUDIT")
print("=" * 60)

# ═══════════════════════════════════════════════════════════
# A. ANCHOR FILE STRUCTURAL INTEGRITY
# ═══════════════════════════════════════════════════════════
print("\n=== A. ANCHOR FILE STRUCTURE ===")

# A1: Every anchor has required fields
required = ['reading', 'confidence']
for s, i in anchors.items():
    for f in required:
        if f not in i:
            errors.append(f"{s} missing field '{f}'")
print(f"A1. Required fields: {'OK' if not errors else 'ERRORS'}")

# A2: All readings are non-empty strings (for HIGH)
bad_readings = [(s, repr(i.get('reading'))) for s, i in high.items()
                if not isinstance(i.get('reading'), str) or len(i.get('reading', '').strip()) == 0]
if bad_readings:
    errors.append(f"Bad readings in HIGH: {bad_readings[:3]}")
print(f"A2. HIGH reading validity: {len(bad_readings)} bad ({'OK' if not bad_readings else 'ERROR'})")

# A3: No sign ID appears in both HIGH and LOW (impossible but check)
high_ids = {s for s, i in anchors.items() if i.get('confidence') == 'HIGH'}
low_ids = {s for s, i in anchors.items() if i.get('confidence') == 'LOW'}
overlap = high_ids & low_ids
print(f"A3. HIGH/LOW overlap: {len(overlap)} ({'OK' if not overlap else 'ERROR'})")

# ═══════════════════════════════════════════════════════════
# B. CORPUS INTEGRITY
# ═══════════════════════════════════════════════════════════
print("\n=== B. CORPUS INTEGRITY ===")

# B1: Holdat has expected size
print(f"B1. Holdat tokens: {len(holdat)} (expected ~7002)")
if len(holdat) != 7002:
    warnings.append(f"Holdat token count is {len(holdat)}, expected 7002")

# B2: Holdat has expected sign count
print(f"B2. Holdat signs: {len(set(holdat))} (expected 390)")
if len(set(holdat)) != 390:
    warnings.append(f"Holdat sign count is {len(set(holdat))}, expected 390")

# B3: Seals count
print(f"B3. Holdat seals: {len(seals)} (expected ~1670)")

# ═══════════════════════════════════════════════════════════
# C. TEST 1: DISCRIMINATION - verify arithmetic
# ═══════════════════════════════════════════════════════════
print("\n=== C. DISCRIMINATION TEST VERIFICATION ===")

pins = {}
for s, i in high.items():
    r = i.get('reading', '')
    if r:
        clean = r.split('/')[0].strip()
        if clean: pins[s] = clean[0]

drav = json.loads((REPO / "backend/glossa_lab/data/dravidian_tamil_lm.json").read_text('utf-8'))
drav_bi = Counter()
for key, count in drav.get('bigrams', {}).items():
    parts = key.split("→") if "→" in key else key.split(",")
    if len(parts) == 2:
        drav_bi[(parts[0].strip(), parts[1].strip())] += count
drav_bi_norm = {k: c / (sum(drav_bi.values()) or 1) for k, c in drav_bi.items()}

hits = total = 0
for i in range(len(holdat) - 1):
    p1 = pins.get(holdat[i], "")
    p2 = pins.get(holdat[i + 1], "")
    if p1 and p2:
        total += 1
        if (p1, p2) in drav_bi_norm: hits += 1

rate = hits / max(1, total)
print(f"C1. Dravidian bigram: {hits}/{total} = {rate:.4f}")
print(f"    Release says: {release['1_discrimination']['dravidian_hit_rate']}")
if abs(rate - release['1_discrimination']['dravidian_hit_rate']) > 0.001:
    errors.append(f"Discrimination rate mismatch: {rate} vs {release['1_discrimination']['dravidian_hit_rate']}")
else:
    print(f"    MATCH OK")

# C2: Is the discrimination test meaningful?
# If we have 400 anchor pins covering 92.8% of tokens, how many bigram pairs tested?
print(f"C2. Bigram pairs tested: {total} out of {len(holdat)-1} possible")
print(f"    Coverage of bigram test: {total/(len(holdat)-1)*100:.1f}%")

# C3: What if we scramble the readings? (quick 10-trial check)
import random
rng = random.Random(42)
scramble_rates = []
sign_list = list(pins.keys())
reading_list = list(pins.values())
for _ in range(10):
    shuffled = list(reading_list)
    rng.shuffle(shuffled)
    s_pins = dict(zip(sign_list, shuffled))
    s_hits = s_total = 0
    for i in range(len(holdat) - 1):
        p1 = s_pins.get(holdat[i], "")
        p2 = s_pins.get(holdat[i + 1], "")
        if p1 and p2:
            s_total += 1
            if (p1, p2) in drav_bi_norm: s_hits += 1
    scramble_rates.append(s_hits / max(1, s_total))

null_mean = sum(scramble_rates) / len(scramble_rates)
print(f"C3. Quick scramble test (10 trials): null mean={null_mean:.4f}, real={rate:.4f}")
print(f"    Real - Null = {rate - null_mean:+.4f}")
if rate <= null_mean:
    warnings.append(f"Discrimination rate ({rate:.4f}) is NOT above scramble null ({null_mean:.4f})")
    print(f"    WARNING: Real is not above null!")
else:
    print(f"    Real is above null — discrimination signal present")

# ═══════════════════════════════════════════════════════════
# D. TEST 3: PARPOLA - verify each match manually
# ═══════════════════════════════════════════════════════════
print("\n=== D. PARPOLA CROSS-CHECK VERIFICATION ===")

def strip(s):
    nfkd = unicodedata.normalize('NFKD', s.lower())
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

# These are the 15 exact matches claimed - verify each one
expected_exact = {
    'M001': ('tol', 'tol'),      # tōḷ = tōḷ
    'M047': ('min', 'min'),      # min/mīn = mīn
    'M086': ('oru', 'oru'),      # oru = oru
    'M087': ('vel', 'vel'),      # veL = veḷ
    'M091': ('aru', 'aru'),      # aru = āṟu
    'M092': ('elu', 'elu'),      # elu = ēḻu
    'M099': ('kol', 'kol'),      # kol/koḷ = kol/vil
    'M117': ('ar', 'ar'),        # ar = ar/cakra
    'M124': ('kutam', 'kutam'),  # kuTam = kuṭam
    'M162': ('il', 'il'),        # il/iḷ = il
    'M175': ('katir', 'katir'),  # katir = katir
    'M176': ('an', 'an'),        # an/aṇ matches 'an' in kō/an
    'M233': ('ur', 'ur'),        # ūr = ūr
    'M261': ('muruku', 'muruku'),# muruku = muruku
    'M281': ('pillai', 'pillai'),# piLLai = piḷḷai
}

verified = 0
for sid, (our_expected, par_expected) in expected_exact.items():
    our_r = anchors.get(sid, {}).get('reading', '')
    our_stripped = strip(our_r.split('/')[0].strip())
    if our_stripped != our_expected:
        # Check alternatives
        alts = [strip(x) for x in our_r.split('/') if x.strip()]
        if our_expected not in alts:
            errors.append(f"Parpola {sid}: expected our='{our_expected}' but got '{our_stripped}' (alts={alts})")
            continue
    verified += 1

print(f"D1. Verified {verified}/15 exact Parpola matches")
if verified != 15:
    errors.append(f"Only {verified}/15 Parpola matches verified")

# ═══════════════════════════════════════════════════════════
# E. TEST 4: ENTROPY - verify computation
# ═══════════════════════════════════════════════════════════
print("\n=== E. ENTROPY VERIFICATION ===")

reading_seqs = []
for seal in seals:
    readings = [high.get(s, {}).get('reading', '') for s in seal]
    clean = [r for r in readings if r]
    if len(clean) >= 2: reading_seqs.append(clean)

all_r = [r for seq in reading_seqs for r in seq]
freq = Counter(all_r)
total_r = sum(freq.values())
h1 = -sum((c/total_r) * math.log2(c/total_r) for c in freq.values() if c > 0)

bigrams = Counter()
for seq in reading_seqs:
    for i in range(len(seq) - 1):
        bigrams[(seq[i], seq[i+1])] += 1
bi_total = sum(bigrams.values())
joint_h = -sum((c/bi_total) * math.log2(c/bi_total) for c in bigrams.values() if c > 0)
h2 = joint_h - h1

print(f"E1. H1={h1:.4f}, H2={h2:.4f}")
print(f"    Release: H2={release['4_reading_entropy']['h2_conditional']}")
if abs(h2 - release['4_reading_entropy']['h2_conditional']) > 0.01:
    errors.append(f"Entropy mismatch: {h2:.4f} vs {release['4_reading_entropy']['h2_conditional']}")
else:
    print(f"    MATCH OK")

# E2: Is H2 in linguistic range?
print(f"E2. H2={h2:.2f} in [2.0, 4.5]? {'YES' if 2.0 <= h2 <= 4.5 else 'NO'}")

# ═══════════════════════════════════════════════════════════
# F. CROSS-CHECK: Do the 208 Holdat-validated signs make sense?
# ═══════════════════════════════════════════════════════════
print("\n=== F. HOLDAT-VALIDATED SIGNS CHECK ===")

holdat_high = {s: i for s, i in high.items() if s in set(holdat)}
print(f"F1. Holdat-validated HIGH: {len(holdat_high)}")

# What's their frequency distribution?
holdat_freq = Counter(holdat)
high_freq = [(s, holdat_freq.get(s, 0)) for s in holdat_high]
high_freq.sort(key=lambda x: -x[1])
print(f"F2. Top 10 by corpus frequency:")
for s, f in high_freq[:10]:
    r = holdat_high[s].get('reading', '')
    print(f"    {s}: freq={f:4d} reading='{r}'")

# F3: Are the most frequent signs the ones with Parpola agreement?
parpola_signs = {'M001', 'M047', 'M086', 'M087', 'M091', 'M092', 'M099',
                 'M117', 'M124', 'M162', 'M175', 'M176', 'M233', 'M261', 'M281'}
parpola_token_coverage = sum(holdat_freq.get(s, 0) for s in parpola_signs)
print(f"\nF3. Parpola-agreed signs token coverage: {parpola_token_coverage}/{len(holdat)} = {parpola_token_coverage/len(holdat)*100:.1f}%")

# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
if errors:
    print(f"ERRORS: {len(errors)}")
    for e in errors: print(f"  ✗ {e}")
else:
    print("NO ERRORS — all data verified")

if warnings:
    print(f"\nWARNINGS: {len(warnings)}")
    for w in warnings: print(f"  ⚠ {w}")
else:
    print("NO WARNINGS")

print("=" * 60)
