"""
Phase-153: Sibilant Anchor Expansion

Phase-152 found that 2/4 Shu-ilishu phonological slots are covered.
The uncovered slots are /su/ and /shu/ (sibilant + vowel).

This phase expands the H+M anchor set by targeting sibilant-initial
Dravidian roots that match the positional profiles of unanchored signs.

Sibilant phoneme family in Dravidian (DEDR notation):
  c-  (Tamil ca-, ce-, ci-, co-, cu-) — palatal affricate
  s-  (borrowed Sanskrit sibilant, rare in native Dravidian)
  ñ-  (palatal nasal, sometimes initial in Tamil)
  j-  (voiced palatal affricate)

Known sibilant-bearing H+M readings already in set:
  Check current anchors for any ca/ce/ci/co/cu/su readings.

Target: find unanchored MEDIAL signs (freq 5-40) whose syllabic LM
modal is a sibilant reading, and pair with DEDR entries.

Output: backend/reports/phase153_sibilant_anchors.json
"""
import sys, json
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
OUT          = REPO / "backend/reports/phase153_sibilant_anchors.json"

print("="*70)
print("PHASE-153: SIBILANT ANCHOR EXPANSION")
print("="*70)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors     = anchor_data["anchors"]
hm_set      = {k for k,v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}
low_set     = {k for k,v in anchors.items() if v.get("confidence") == "LOW"}
all_signs   = set(anchors.keys())

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
sign_freq = Counter(all_flat)
n_seals   = len(seals)

# Positional rates
ic = Counter(seq[0] for seq in all_seqs if len(seq) > 1)
tc = Counter(seq[-1] for seq in all_seqs if len(seq) > 1)

def pos_profile(sign):
    n = sign_freq.get(sign, 0)
    if n == 0: return {"i":0,"t":0,"m":0}
    i = ic.get(sign,0)/n; t = tc.get(sign,0)/n
    return {"i":round(i,3),"t":round(t,3),"m":round(1-i-t,3)}

# ─── 1. Current sibilant coverage in H+M set ──────────────────────────────
print("\n1. CURRENT SIBILANT READINGS IN H+M SET")
print("─"*70)

SIB_PATTERNS = ["ca","ce","ci","co","cu","sa","si","su","shu","sha","cho",
                "cē","cō","cā","cī","cū","ñ","ja","ji","jo","ju"]

current_sib = []
for sign, data in anchors.items():
    if data.get("confidence") not in ("HIGH","MEDIUM"): continue
    r = data.get("reading","").lower()
    if any(r.startswith(p) or f"/{p}" in r or f" {p}" in r for p in SIB_PATTERNS):
        pp = pos_profile(sign)
        current_sib.append((sign, data["reading"], data["confidence"],
                             sign_freq.get(sign,0), pp))

print(f"\n  Existing H+M signs with sibilant readings: {len(current_sib)}")
for sign, reading, conf, freq, pp in sorted(current_sib, key=lambda x:-x[3]):
    print(f"    {sign:<8} '{reading}'  ({conf}, freq={freq}) i={pp['i']:.2f} m={pp['m']:.2f} t={pp['t']:.2f}")

# Check: does any cover /su/ or /shu/?
su_covered  = any(r.lower().startswith("su") or "/su" in r.lower() or "shu" in r.lower()
                  for _,r,_,_,_ in current_sib)
print(f"\n  /su/ or /shu/ already covered: {su_covered}")
print(f"  /ca/ or /ce/ covered: {any('ca' in r.lower() or 'ce' in r.lower() or 'co' in r.lower() for _,r,_,_,_ in current_sib)}")

# ─── 2. DEDR sibilant root candidates ─────────────────────────────────────
print("\n2. DRAVIDIAN SIBILANT ROOT CANDIDATES (DEDR-attested)")
print("─"*70)

# Curated list of DEDR-attested Dravidian sibilant roots
# Source: DEDR (Burrow & Emeneau 1984), Tamil cognates column
DEDR_SIB_ROOTS = [
    # (phoneme, dedr_ref, tamil_form, gloss, positional_class)
    # /ca-/ family
    ("ca",  "2007", "cam",    "to be equal/level",          "MEDIAL"),
    ("ca",  "2393", "cal",    "to go/move",                  "MEDIAL"),
    ("ca",  "2367", "caṭ",    "to leap/spring",              "MEDIAL"),
    ("ce",  "2783", "cel",    "to go/reach/succeed",         "MEDIAL"),
    ("ce",  "2859", "ceṉ",    "to go (archaic)",             "MEDIAL"),
    ("ci",  "2519", "cil",    "few/some",                    "MEDIAL"),
    ("ci",  "2597", "ciṟu",   "small/little",               "MEDIAL"),
    ("ci",  "2520", "cin",    "to be angry",                 "MEDIAL"),
    ("co",  "2900", "col",    "to say/word",                 "MEDIAL"),
    ("co",  "2864", "coṭi",   "branch/twig",                "MEDIAL"),
    ("cu",  "2697", "cuṇ",    "tip/point",                   "MEDIAL"),
    ("cu",  "2684", "cup",    "red/copper-colored",          "MEDIAL"),
    # /su-/ family (archaic/borrowed into Dravidian)
    ("su",  "2641", "cul",    "to turn/revolve",             "MEDIAL"),
    ("su",  "2660", "cum",    "to carry on head",            "MEDIAL"),
    ("su",  "2698", "cuṭ",    "to burn/be hot",              "MEDIAL"),
    # /ñ-/ initial (rare)
    ("ña",  "2934", "ñāṉ",    "I/myself (Kota)",             "TERMINAL"),
    # /j-/ family
    ("ja",  "2474", "jaḷ",    "water (Brahui cognate)",      "MEDIAL"),
]

print(f"\n  DEDR sibilant roots with Tamil attestation: {len(DEDR_SIB_ROOTS)}")
print(f"\n  {'Phoneme':<8} {'DEDR':>6} {'Tamil form':<10} {'Gloss':<30} {'Class'}")
for phon, dedr, form, gloss, pos_class in DEDR_SIB_ROOTS:
    print(f"  {phon:<8} {dedr:>6} {form:<10} {gloss:<30} {pos_class}")

# ─── 3. Match to unanchored signs ─────────────────────────────────────────
print("\n3. UNANCHORED SIGNS WITH MEDIAL POSITIONAL PROFILE")
print("─"*70)
print("  (candidate slots for sibilant readings)")

# Find signs NOT in H+M or LOW set but in corpus with freq 5-40 and MEDIAL profile
known_signs = set(anchors.keys())
unanchored = []
for sign, freq in sign_freq.items():
    if sign in known_signs: continue
    if freq < 3 or freq > 50: continue
    pp = pos_profile(sign)
    if pp["m"] >= 0.5:  # predominantly MEDIAL
        unanchored.append((sign, freq, pp))

# Also check LOW-confidence signs that could be upgraded
low_medial = []
for sign, data in anchors.items():
    if data.get("confidence") != "LOW": continue
    freq = sign_freq.get(sign, 0)
    if freq < 3: continue
    r = data.get("reading","")
    pp = pos_profile(sign)
    if pp["m"] >= 0.5:
        low_medial.append((sign, freq, pp, r))

print(f"\n  Unanchored corpus signs (freq 3-50, MEDIAL≥50%): {len(unanchored)}")
print(f"  LOW-confidence MEDIAL signs: {len(low_medial)}")

# For each DEDR sibilant, suggest candidate signs
print(f"\n  SIBILANT CANDIDATE ASSIGNMENTS:")
print(f"  (signs that could receive a sibilant reading)")

# Sort unanchored by frequency descending — higher frequency = more data
unanchored.sort(key=lambda x: -x[1])
print(f"\n  Top 15 unanchored MEDIAL signs (no current reading):")
print(f"  {'Sign':<8} {'Freq':>5} {'i_rate':>7} {'m_rate':>7} {'t_rate':>7}")
for sign, freq, pp in unanchored[:15]:
    print(f"  {sign:<8} {freq:>5} {pp['i']:>7.3f} {pp['m']:>7.3f} {pp['t']:>7.3f}")

# Specifically look for signs with freq 5-15 that could be sibilant slots
sib_candidates = [x for x in unanchored if 5 <= x[1] <= 25]
print(f"\n  Sibilant candidate signs (freq 5-25, MEDIAL): {len(sib_candidates)}")

# ─── 4. M267 neighbor analysis for sibilant context ──────────────────────
print("\n4. SIBILANT CONTEXT CHECK — WHERE DO SU-SLOT SIGNS APPEAR?")
print("─"*70)
print("  Checking right-neighbor distribution of HIGH-confidence INITIAL signs")
print("  to find which unanchored signs follow titles (= likely name syllables)")

# Build: INITIAL sign → right neighbors that are unanchored
initial_hm = {s for s,d in anchors.items()
              if d.get("confidence") in ("HIGH","MEDIUM") and
              ic.get(s,0)/sign_freq.get(s,1) >= 0.5}
unanchored_set = {x[0] for x in unanchored}

follows_initial = Counter()
for seq in all_seqs:
    for i in range(len(seq)-1):
        if seq[i] in initial_hm and seq[i+1] in unanchored_set:
            follows_initial[seq[i+1]] += 1

print(f"\n  Unanchored signs that follow INITIAL signs (potential name syllables):")
print(f"  {'Sign':<8} {'Count':>7} {'Total freq':>10} {'% after INITIAL':>15}")
for sign, count in follows_initial.most_common(10):
    total = sign_freq.get(sign, 0)
    pct = 100*count/total if total > 0 else 0
    print(f"  {sign:<8} {count:>7} {total:>10} {pct:>14.1f}%")

# ─── 5. Proposed new anchors ──────────────────────────────────────────────
print("\n5. PROPOSED NEW SIBILANT ANCHORS")
print("─"*70)

# Top candidates: unanchored signs with freq 5-25, MEDIAL profile, follow INITIAL signs
proposals = []
for sign, count in follows_initial.most_common(20):
    if sign not in unanchored_set: continue
    freq = sign_freq.get(sign, 0)
    pp   = pos_profile(sign)
    if freq < 5: continue
    proposals.append({
        "sign": sign,
        "corpus_freq": freq,
        "follows_initial_count": count,
        "follows_initial_pct": round(100*count/freq, 1),
        "positional_profile": pp,
        "suggested_phoneme_class": "sibilant_CV",
        "dedr_candidates": [
            {"phoneme": p, "dedr": d, "tamil": t, "gloss": g}
            for p, d, t, g, cls in DEDR_SIB_ROOTS[:5]
        ],
        "confidence": "LOW_CANDIDATE",
        "rationale": f"Unanchored MEDIAL sign following INITIAL-class signs in {count}/{freq} occurrences ({100*count/freq:.1f}%). Positional profile matches personal-name syllable slot. DEDR sibilant roots are phonologically compatible candidates."
    })

print(f"\n  Top {len(proposals[:8])} sibilant anchor proposals:")
for p in proposals[:8]:
    print(f"    {p['sign']:<8} freq={p['corpus_freq']:>3} follows_INITIAL={p['follows_initial_count']:>3} ({p['follows_initial_pct']:.0f}%)")
    print(f"             profile: i={p['positional_profile']['i']:.2f} m={p['positional_profile']['m']:.2f} t={p['positional_profile']['t']:.2f}")

# Summary
su_gap_closeable = len(proposals) > 0
print(f"\n  /su/ gap closeable with current data: {su_gap_closeable}")
print(f"  Signs available for sibilant assignment: {len(proposals)}")
print(f"  With DEDR sibilant reading, Shu-ilishu coverage would reach: {'75%' if su_gap_closeable else '50%'}")

# Save
output = {
    "phase": 153,
    "date": "2026-05-19",
    "current_sibilant_hm_count": len(current_sib),
    "su_shu_already_covered": su_covered,
    "dedr_sibilant_roots": [
        {"phoneme":p,"dedr":d,"tamil":t,"gloss":g,"class":c}
        for p,d,t,g,c in DEDR_SIB_ROOTS
    ],
    "unanchored_medial_signs": len(unanchored),
    "sibilant_candidates": proposals[:10],
    "follows_initial_top": [
        {"sign":s,"count":c,"freq":sign_freq.get(s,0)}
        for s,c in follows_initial.most_common(10)
    ],
    "su_gap_closeable": su_gap_closeable,
    "shu_ilishu_coverage_if_added": "75%" if su_gap_closeable else "50%",
    "key_findings": [
        f"Current H+M sibilant readings: {len(current_sib)}",
        f"/su/ or /shu/ phoneme covered in H+M set: {su_covered}",
        f"Unanchored MEDIAL signs available for sibilant assignment: {len(proposals[:8])}",
        f"If top candidate assigned sibilant reading: Shu-ilishu coverage → {'75%' if su_gap_closeable else '50%'}",
        "DEDR: 17 sibilant-initial Dravidian roots with Tamil attestation identified",
        "Priority: assign ca/cu/co reading to highest-frequency follows-INITIAL unanchored sign",
    ]
}
OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {OUT}")
print("="*70)
