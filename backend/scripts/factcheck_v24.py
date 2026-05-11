"""
Fact-check script for V8-V24 decipherment results.
Checks:
  1. TB correlation circularity - is 0.914 self-fulfilling?
  2. Iconographic HIGH-confidence assignments data-backed?
  3. Crosswalk completeness
  4. Corpus identity (is Holdat really Mahadevan 1977?)
  5. Sign count sanity check
"""
import csv
import json
import numpy as np
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab")
HOLDAT = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES  = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
FINAL  = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
XW     = REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk.json"

TAMIL_BRAHMI_FREQ = {
    "a":0.12,"i":0.08,"u":0.06,"e":0.04,"o":0.03,
    "k":0.09,"c":0.04,"t":0.08,"p":0.06,"n":0.10,
    "m":0.08,"y":0.03,"r":0.05,"l":0.04,"v":0.04,
}
ALL_READINGS = [
    "ko","nal","cem","vel","kai","per","tiru","cer","an","ma","ner","por",
    "kun","kal","kel","pat","tol","mar","par","col","erutu","yanai","puli",
    "kon","matu","min","kol","ur","il","al","kan","mul","nir","pon","vel",
    "ney","cel","kul","ten","mal","pan","tin","cul","nar","vil","tat","kur",
    "ver","ay","am","in","ar","otu","ul","el","pu","tu","mu","aku","utai",
    "ati","eru","or","un","van","tan","pin","mun","nan","pal",
]

# ── Load corpus ────────────────────────────────────────────────────────────────
seals = defaultdict(list)
with open(HOLDAT, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        seals[r["cisi_number"]].append(r)

sign_freq = Counter()
for v in seals.values():
    for s in v:
        sign_freq[s["letters"]] += 1

n_seals   = len(seals)
n_tokens  = sum(sign_freq.values())
n_signs   = len(sign_freq)
sites     = Counter(v[0]["site"] for v in seals.values())

print("=" * 60)
print("FACT-CHECK 1: Corpus identity")
print("=" * 60)
print(f"  Seals (inscriptions): {n_seals}  (Mahadevan 1977 claims ~2,000; Holdat = 1,670)")
print(f"  Tokens:               {n_tokens}")
print(f"  Distinct signs:       {n_signs}  (Mahadevan lists 417; subset expected in 1,670-seal sample)")
print(f"  Sites: {dict(sites)}")
print()

# Verify M-numbers look like Mahadevan sign IDs
sample = [s for s in sign_freq if not s.startswith("M")]
print(f"  Non-M-prefixed sign IDs: {sample[:10] if sample else 'NONE — all M-prefixed ✓'}")
print()

# ── Check circularity in TB correlation ───────────────────────────────────────
print("=" * 60)
print("FACT-CHECK 2: TB correlation circularity")
print("=" * 60)

def tb_corr(assigned: dict[str, str]) -> float:
    pf, tw = Counter(), 0
    for sign, reading in assigned.items():
        fr = sign_freq.get(sign, 1)
        if reading and reading[0].isalpha():
            pf[reading[0].lower()] += fr
            tw += fr
    if tw == 0:
        return 0.0
    dist = {k: v / tw for k, v in pf.items()}
    sh = set(dist) & set(TAMIL_BRAHMI_FREQ)
    if len(sh) < 3:
        return 0.0
    x = [dist.get(k, 0) for k in sorted(sh)]
    y = [TAMIL_BRAHMI_FREQ.get(k, 0) for k in sorted(sh)]
    return round(float(np.corrcoef(x, y)[0, 1]), 4)

# Actual V24 anchors
anchors = json.loads(FINAL.read_text(encoding="utf-8"))["anchors"]
actual_readings = {s: info["reading"] for s, info in anchors.items()
                   if not info["reading"].startswith(("TERM-","INIT-","MED-","?"))}
actual_corr = tb_corr(actual_readings)

# Null model 1: assign ALL HIGH-TB-biased readings (maximize TB freq score, no positional logic)
tb_max = {}
for sign in sign_freq.most_common(len(sign_freq)):
    best, best_sc = ALL_READINGS[0], -1
    for r in ALL_READINGS:
        sc = TAMIL_BRAHMI_FREQ.get(r[0], 0) * 10
        if sc > best_sc:
            best_sc, best = sc, r
    tb_max[sign[0]] = best  # sign[0] because most_common returns (sign, count)
max_possible_corr = tb_corr(tb_max)

# Null model 2: all readings = "n" (highest TB freq phoneme = 0.10)
all_n = {s: "nal" for s in sign_freq}
all_n_corr = tb_corr(all_n)

# Null model 3: random 50-trial average
rng = np.random.default_rng(2026)
rand_corrs = []
for _ in range(50):
    rand_a = {s: rng.choice(ALL_READINGS) for s in sign_freq}
    rand_corrs.append(tb_corr(rand_a))
rand_mean = round(float(np.mean(rand_corrs)), 4)
rand_std  = round(float(np.std(rand_corrs)), 4)

# Null model 4: uniform distribution (what a completely random non-Tamil script would give)
# Every reading starts with a different random letter
import string
rand_letters = {s: rng.choice(list(string.ascii_lowercase)) for s in sign_freq}
uniform_corr = tb_corr(rand_letters)

print(f"  Actual V24 correlation:              {actual_corr}")
print(f"  Max possible (all best-TB readings): {max_possible_corr}")
print(f"  All-'n' assignment:                  {all_n_corr}")
print(f"  Random assignment (50-trial avg):    {rand_mean} ± {rand_std}")
print(f"  Uniform random letters:              {uniform_corr}")
print()
print(f"  >> CIRCULARITY GAP: actual ({actual_corr}) vs random ({rand_mean})")
gap = round(actual_corr - rand_mean, 4)
print(f"     Delta above random: {gap}")
if gap < 0.1:
    print("     WARNING: Most of the correlation is noise / circularity!")
elif gap < 0.3:
    print("     CAUTION: Modest lift above random — partial circularity present")
else:
    print("     OK: Substantial lift above random — correlation not purely circular")
print()

# ── Iconographic HIGH-confidence verification ─────────────────────────────────
print("=" * 60)
print("FACT-CHECK 3: Iconographic HIGH-confidence data backing")
print("=" * 60)

roles_data = {}
with open(ROLES, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        roles_data[r["symbol"].strip()] = r

motif_col = "iconography"
icon_claims = {
    "M062": ("erutu",   "zebu bull",  "Zebu Bull"),
    "M045": ("yānai",   "elephant",   "Elephant"),
    "M006": ("puli",    "tiger",      "Tiger"),
    "M063": ("mutalai", "crocodile",  "Gharial"),
    "M016": ("kaḷiṟu",  "elephant",   "Elephant"),
}

# Check: does each sign appear predominantly on the claimed motif seals?
motif_counts = defaultdict(lambda: defaultdict(int))  # sign → motif → count
for v in seals.values():
    motif = v[0][motif_col].lower().strip()
    for s in v:
        motif_counts[s["letters"]][motif] += 1

for sign_id, (reading, expected_motif, expected_label) in icon_claims.items():
    mc = motif_counts.get(sign_id, {})
    total = sum(mc.values())
    top_motif, top_count = max(mc.items(), key=lambda x: x[1]) if mc else ("—", 0)
    pct = round(top_count / total * 100, 1) if total else 0
    on_expected = mc.get(expected_motif, mc.get(expected_motif.lower(), 0))
    pct_expected = round(on_expected / total * 100, 1) if total else 0
    # Lift = P(sign|motif) / P(sign overall)
    motif_seals = sum(1 for v in seals.values() if v[0][motif_col].lower().strip() == expected_motif.lower())
    p_sign = total / n_tokens
    p_sign_given_motif = (mc.get(expected_motif.lower(), 0) / motif_seals) if motif_seals else 0
    lift = round(p_sign_given_motif / p_sign, 2) if p_sign > 0 else 0
    claimed_high = anchors.get(sign_id, {}).get("confidence") == "HIGH"
    ok = "✓" if pct_expected > 40 or lift > 2 else "✗"
    print(f"  {sign_id} ({reading:10s}): top motif = '{top_motif}' ({pct}%), "
          f"on '{expected_motif}' = {pct_expected}%, lift={lift:.2f}, "
          f"HIGH={'✓' if claimed_high else '?'} {ok}")
print()

# ── Crosswalk completeness ─────────────────────────────────────────────────────
print("=" * 60)
print("FACT-CHECK 4: Mahadevan-Parpola crosswalk")
print("=" * 60)
xw_data = json.loads(XW.read_text(encoding="utf-8"))
print(f"  mahadevan_parpola_crosswalk.json entries: {len(xw_data)}")

# Check other crosswalk sources
crosswalk_dir = REPO / "crosswalks"
data_dir      = REPO / "backend/glossa_lab/data"
xw_files = list(crosswalk_dir.glob("*.csv")) + list(crosswalk_dir.glob("*.json")) + \
           list(data_dir.glob("*crosswalk*")) + list(data_dir.glob("*cross*"))
print(f"  Other crosswalk files found:")
for f in xw_files:
    try:
        with open(f, encoding="utf-8") as fh:
            content = fh.read()
        print(f"    {f.name}: {len(content.splitlines())} lines")
    except:
        print(f"    {f.name}: [unreadable]")

# Are Holdat M-numbers actual Mahadevan numbers?
# Mahadevan lists ~417 signs. Check range of M-numbers in corpus.
m_nums = []
for s in sign_freq:
    try:
        m_nums.append(int(s.replace("M", "")))
    except:
        pass
if m_nums:
    print(f"\n  Holdat sign number range: M{min(m_nums)} to M{max(m_nums)}")
    print(f"  Total distinct M-numbers: {len(m_nums)}")
    print(f"  (Mahadevan 1977 concordance has 417 signs; 390 in 1,670-seal sample is consistent)")
print()

# ── Phase-27c anchor score sanity check ───────────────────────────────────────
print("=" * 60)
print("FACT-CHECK 5: Phase-27c IconographicAnchorScore")
print("=" * 60)
phase27c = REPO / "reports/indus_phase27c_iconographic_anchors_20260430T120500.json"
if phase27c.exists():
    d = json.loads(phase27c.read_text(encoding="utf-8"))
    score = d.get("anchor_score") or d.get("result", {}).get("anchor_score") or "?"
    print(f"  Phase-27c anchor_score: {score}")
    # Show top-level keys
    print(f"  Keys: {list(d.keys())[:10]}")
    # Show result
    for k in ["anchor_score","total_anchors","matched","parpola_score","dravidian_score","verdict"]:
        if k in d:
            print(f"    {k}: {d[k]}")
        elif "result" in d and k in d.get("result",{}):
            print(f"    result.{k}: {d['result'][k]}")
else:
    print("  [file not found]")
print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Corpus: {n_seals} seals, {n_tokens} tokens, {n_signs} distinct signs")
print(f"  TB corr actual={actual_corr}, random={rand_mean}±{rand_std}, gap={gap}")
print(f"  Circularity verdict: {'PARTIALLY CIRCULAR' if gap < 0.3 else 'MOSTLY GENUINE'}")
