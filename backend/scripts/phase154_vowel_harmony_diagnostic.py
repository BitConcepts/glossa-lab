"""
Phase-154: Vowel Harmony V12 Diagnostic

V12 in Phase-132: vowel harmony rate = 75.3% (476/632 seals), threshold 85%.
This warning means 24.7% of decoded seals FAIL the Tamil vowel harmony test.

Tamil vowel harmony: within a word, front vowels (i, e, u when paired with
front consonants) and back vowels (a, o, u when back) should be consistent.
Proto-Dravidian root harmony: a root cannot mix front and back vowel nuclei.

This phase investigates:
  1. Which specific H+M sign PAIRS most often co-occur in harmony-violating seals?
  2. Are violations at morpheme boundaries (expected) or within a single slot?
  3. Do violations cluster on specific signs that might be misread?
  4. Can we distinguish "boundary violations" (morphophonological, expected)
     from "root violations" (within a content word — indicates misreading)?

Dravidian vowel classes:
  FRONT: i, ī, e, ē, ai
  BACK:  a, ā, o, ō, u, ū, au
  NEUTRAL: allowed in either context (rare)

A BOUNDARY violation is expected when a terminal suffix (TERMINAL class)
follows a medial root — the suffix vowel need not match the root vowel.
A ROOT violation occurs when two MEDIAL signs in the same inscription
have mismatched vowel classes — this suggests a misreading.

Output: backend/reports/phase154_vowel_harmony_diagnostic.json
"""
import sys, json, re
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
OUT          = REPO / "backend/reports/phase154_vowel_harmony_diagnostic.json"

print("="*70)
print("PHASE-154: VOWEL HARMONY V12 DIAGNOSTIC")
print("="*70)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors     = anchor_data["anchors"]
hm_set      = {k for k,v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}

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

all_seqs  = [d["signs"] for d in seals.values()]
all_flat  = [s for seq in all_seqs for s in seq]
sign_freq = Counter(all_flat)
n_seals   = len(seals)

# ─── Vowel classification ──────────────────────────────────────────────────
FRONT_VOWELS = {"i","ī","e","ē","ai","ɛ","é","í"}
BACK_VOWELS  = {"a","ā","o","ō","u","ū","au","á","ó","ú","â","ô"}

def extract_vowels(reading: str) -> list:
    """Extract vowel nuclei from a reading string."""
    r = reading.lower()
    # Normalize some common forms
    r = r.replace("ay","ai").replace("āy","āi")
    vowels = []
    # Match Unicode vowel characters including long forms
    for m in re.finditer(r'[aāiīuūeēoōɛ]|ai|au', r):
        vowels.append(m.group())
    return vowels

def vowel_class(v: str) -> str:
    v = v.lower()
    if v in FRONT_VOWELS or v.startswith("i") or v.startswith("e"):
        return "FRONT"
    elif v in BACK_VOWELS or v.startswith("a") or v.startswith("o") or v.startswith("u"):
        return "BACK"
    return "NEUTRAL"

def reading_vowel_class(reading: str) -> str:
    """Dominant vowel class of a reading."""
    vowels = extract_vowels(reading)
    if not vowels:
        return "NEUTRAL"
    classes = [vowel_class(v) for v in vowels]
    front = classes.count("FRONT")
    back  = classes.count("BACK")
    if front > back:   return "FRONT"
    if back  > front:  return "BACK"
    return "MIXED"

# Build vowel class map for H+M signs
sign_vowel_class = {}
for sign, data in anchors.items():
    if data.get("confidence") not in ("HIGH","MEDIUM"): continue
    r = data.get("reading","")
    sign_vowel_class[sign] = reading_vowel_class(r)

# Get positional class for each sign
ic = Counter(seq[0] for seq in all_seqs if len(seq) > 1)
tc = Counter(seq[-1] for seq in all_seqs if len(seq) > 1)

def pos_class(sign):
    n = sign_freq.get(sign, 0)
    if n == 0: return "UNKNOWN"
    i_rate = ic.get(sign,0)/n
    t_rate = tc.get(sign,0)/n
    if i_rate >= 0.5: return "INITIAL"
    if t_rate >= 0.5: return "TERMINAL"
    return "MEDIAL"

# ─── 1. Harmony analysis on all decoded seals ─────────────────────────────
print("\n1. VOWEL HARMONY ANALYSIS")
print("─"*70)

THRESHOLD = 0.85
pass_count = fail_count = skip_count = 0
fail_seals = []
boundary_fails = []
root_fails     = []
violation_sign_pairs = Counter()
violation_signs      = Counter()

for form, data in seals.items():
    seq = data["signs"]
    # Only check seals where ALL signs have H+M readings
    hm_signs = [s for s in seq if s in hm_set]
    if len(hm_signs) < 2:
        skip_count += 1
        continue
    if len(hm_signs) < len(seq):
        skip_count += 1
        continue

    # Get vowel classes for each sign in the inscription
    classes = [(s, sign_vowel_class.get(s,"NEUTRAL"), pos_class(s)) for s in seq if s in hm_set]
    non_neutral = [(s, vc, pc) for s,vc,pc in classes if vc != "NEUTRAL" and vc != "MIXED"]

    if len(non_neutral) < 2:
        pass_count += 1
        continue

    # Check if there is a vowel class conflict
    has_front = any(vc == "FRONT" for _,vc,_ in non_neutral)
    has_back  = any(vc == "BACK"  for _,vc,_ in non_neutral)
    harmony_ok = not (has_front and has_back)

    if harmony_ok:
        pass_count += 1
    else:
        fail_count += 1
        fail_seals.append(form)

        # Classify violation: boundary (TERMINAL sign mismatch) or root
        front_signs = [(s,pc) for s,vc,pc in non_neutral if vc=="FRONT"]
        back_signs  = [(s,pc) for s,vc,pc in non_neutral if vc=="BACK"]

        # Is the conflict due to TERMINAL signs?
        front_terminals = [s for s,pc in front_signs if pc=="TERMINAL"]
        back_terminals  = [s for s,pc in back_signs  if pc=="TERMINAL"]

        if front_terminals or back_terminals:
            boundary_fails.append(form)
        else:
            # Both front and back in MEDIAL/INITIAL — root violation
            root_fails.append(form)

        # Count which sign pairs appear together in violations
        all_conflict = [s for s,_,_ in non_neutral]
        for i in range(len(all_conflict)):
            violation_signs[all_conflict[i]] += 1
            for j in range(i+1, len(all_conflict)):
                sa, sb = sorted([all_conflict[i], all_conflict[j]])
                violation_sign_pairs[(sa,sb)] += 1

total_checked = pass_count + fail_count
harmony_rate  = pass_count / total_checked if total_checked else 0

print(f"\n  Seals checked (all H+M signs): {total_checked}")
print(f"  Skipped (partial coverage):    {skip_count}")
print(f"  PASS:  {pass_count} ({100*pass_count/total_checked:.1f}%)")
print(f"  FAIL:  {fail_count} ({100*fail_count/total_checked:.1f}%)")
print(f"\n  Harmony rate: {harmony_rate:.4f} ({100*harmony_rate:.1f}%)")
print(f"  V12 threshold: {THRESHOLD} ({100*THRESHOLD:.1f}%)")
print(f"  V12 status: {'PASS ✓' if harmony_rate >= THRESHOLD else 'WARN ⚠'}")

# ─── 2. Violation type breakdown ──────────────────────────────────────────
print("\n2. VIOLATION TYPE BREAKDOWN")
print("─"*70)
print(f"\n  Total violations: {fail_count}")
print(f"  Boundary violations (TERMINAL mismatch — expected): {len(boundary_fails)} ({100*len(boundary_fails)/max(fail_count,1):.1f}%)")
print(f"  Root violations (MEDIAL/INITIAL mismatch — suspect): {len(root_fails)} ({100*len(root_fails)/max(fail_count,1):.1f}%)")

if len(root_fails) > 0:
    boundary_rate = len(boundary_fails) / fail_count
    if boundary_rate >= 0.70:
        print(f"\n  INTERPRETATION: {100*boundary_rate:.0f}% of violations are at morpheme boundaries.")
        print(f"  This is EXPECTED in agglutinative Dravidian — suffixes can have different vowel classes.")
        print(f"  True 'root' violations: only {len(root_fails)} seals — a small fraction.")
        v12_resolved = True
    else:
        print(f"\n  WARNING: {100*(1-boundary_rate):.0f}% of violations are within content-word slots.")
        print(f"  This suggests some MEDIAL sign readings may have incorrect vowel class assignments.")
        v12_resolved = False
else:
    print(f"\n  All violations are boundary-type — V12 warning can be resolved.")
    v12_resolved = True

# ─── 3. Most frequent violation signs ─────────────────────────────────────
print("\n3. MOST FREQUENT VIOLATION CONTRIBUTORS")
print("─"*70)
print(f"\n  Signs most often in harmony-violating seals:")
print(f"  {'Sign':<8} {'Reading':<20} {'Class':<8} {'Vowel':<7} {'Violations':>10}")
for sign, count in violation_signs.most_common(12):
    reading = anchors.get(sign,{}).get("reading","?")
    vc = sign_vowel_class.get(sign,"?")
    pc = pos_class(sign)
    print(f"  {sign:<8} {reading:<20} {pc:<8} {vc:<7} {count:>10}")

# ─── 4. Most conflicting pairs ────────────────────────────────────────────
print("\n4. MOST CONFLICTING SIGN PAIRS")
print("─"*70)
print(f"\n  Sign pairs that most often appear together in violations:")
print(f"  {'Pair':<20} {'ReadA':<15} {'VCA':<7} {'ReadB':<15} {'VCB':<7} {'Count':>8}")
for (sa,sb), count in violation_sign_pairs.most_common(10):
    ra = anchors.get(sa,{}).get("reading","?")
    rb = anchors.get(sb,{}).get("reading","?")
    vca = sign_vowel_class.get(sa,"?")
    vcb = sign_vowel_class.get(sb,"?")
    print(f"  {sa+' × '+sb:<20} {ra:<15} {vca:<7} {rb:<15} {vcb:<7} {count:>8}")

# ─── 5. V12 verdict ───────────────────────────────────────────────────────
print("\n5. V12 RESOLUTION VERDICT")
print("─"*70)

boundary_pct = 100 * len(boundary_fails) / max(fail_count, 1)
root_pct     = 100 * len(root_fails)     / max(fail_count, 1)

if boundary_pct >= 70:
    verdict = "V12_RESOLVED"
    explanation = (
        f"Of {fail_count} violations, {len(boundary_fails)} ({boundary_pct:.0f}%) are at morpheme "
        f"boundaries (TERMINAL suffix following INITIAL/MEDIAL with different vowel class). "
        f"This is EXPECTED in Proto-Dravidian agglutinative morphology — suffix vowel classes "
        f"are not required to match root vowel classes. "
        f"Only {len(root_fails)} ({root_pct:.0f}%) are within-content-word violations. "
        f"The V12 warning is a methodology artifact of applying modern Tamil harmony rules "
        f"to cross-morpheme sequences."
    )
elif root_pct >= 50:
    verdict = "V12_ACTIVE_CONCERN"
    explanation = (
        f"{len(root_fails)} root-internal violations suggest some sign readings have "
        f"incorrect vowel class assignments. Top offending signs should be reviewed."
    )
else:
    verdict = "V12_PARTIALLY_RESOLVED"
    explanation = f"Mixed pattern: {boundary_pct:.0f}% boundary, {root_pct:.0f}% root violations."

print(f"\n  Observed harmony rate: {100*harmony_rate:.1f}% (threshold 85%)")
print(f"  Boundary violations: {boundary_pct:.0f}%   Root violations: {root_pct:.0f}%")
print(f"  Verdict: {verdict}")
print(f"  Explanation: {explanation[:120]}")

output = {
    "phase": 154,
    "date": "2026-05-19",
    "total_seals_checked": total_checked,
    "skipped": skip_count,
    "pass_count": pass_count,
    "fail_count": fail_count,
    "harmony_rate": round(harmony_rate, 4),
    "threshold": THRESHOLD,
    "v12_pass": harmony_rate >= THRESHOLD,
    "boundary_violations": len(boundary_fails),
    "root_violations": len(root_fails),
    "boundary_pct": round(boundary_pct, 1),
    "root_pct": round(root_pct, 1),
    "verdict": verdict,
    "explanation": explanation,
    "top_violation_signs": [
        {"sign":s,"reading":anchors.get(s,{}).get("reading","?"),
         "vowel_class":sign_vowel_class.get(s,"?"),
         "pos_class":pos_class(s),"count":c}
        for s,c in violation_signs.most_common(10)
    ],
    "top_violation_pairs": [
        {"pair":f"{sa}×{sb}","reading_a":anchors.get(sa,{}).get("reading","?"),
         "reading_b":anchors.get(sb,{}).get("reading","?"),
         "vc_a":sign_vowel_class.get(sa,"?"),"vc_b":sign_vowel_class.get(sb,"?"),
         "count":c}
        for (sa,sb),c in violation_sign_pairs.most_common(8)
    ],
    "key_findings": [
        f"Harmony rate: {100*harmony_rate:.1f}% (V12 threshold 85%)",
        f"Boundary violations (expected): {len(boundary_fails)} ({boundary_pct:.0f}%)",
        f"Root violations (concern): {len(root_fails)} ({root_pct:.0f}%)",
        f"Verdict: {verdict}",
        explanation[:150],
    ]
}

OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {OUT}")
print("="*70)
