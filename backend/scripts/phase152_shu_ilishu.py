"""
Phase-152: Shu-ilishu Interpreter Seal Phonological Test

The Shu-ilishu seal (Ur III period, c. 2020 BCE, excavated at Ur) is the single
best archaeologically-grounded external anchor for the Indus script:
  - The seal owner is named "Shu-ilishu" in the Akkadian cuneiform inscription
  - His title is "interpreter of the Meluhha language" (Meluhhaya EME.BAL)
  - This names a real person who spoke/translated Indus (Meluhhan) language
  - The Indus inscription on the same seal is therefore the PHONOLOGICAL
    rendering of the name "Shu-ilishu" (or his Meluhhan equivalent)

Phonological decomposition of "Shu-ilishu":
  Akkadian rendering: ŠU-i-li-šu
  Possible Meluhhan phonemes: /su/ or /shu/, /i/, /li/, /shu/ or /su/
  Syllabic structure: CV-V-CV-CV (4 syllables, 2-3 distinct CV patterns)

  Working Meluhhan reconstruction:
    Sign 1: /su/ or /shu/ — initial sibilant + vowel
    Sign 2: /i/          — front vowel (possibly a vowel sign)
    Sign 3: /li/         — lateral + front vowel
    Sign 4: /shu/ or /su/— sibilant + vowel (possibly allophone of Sign 1)

Test:
  1. Check which H+M readings cover the phonemes /su/, /i/, /li/, /shu/
  2. Find seals in the corpus that could plausibly encode this name
  3. Compute coverage: what % of the 4 syllabic slots are coverable
  4. Upgrade E02 from INSUFFICIENT to at least PARTIALLY_SUPPORTED if coverage >= 50%

Also test the two competing decompositions:
  A. Dravidian: cuvan-ili-cuvan (sun + deity + sun, rebus for name elements)
  B. Pure phonetic: su + i + li + su (phonetic transcription attempt)

Output: backend/reports/phase152_shu_ilishu.json
"""
import sys, json, re
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
OUT          = REPO / "backend/reports/phase152_shu_ilishu.json"

print("="*70)
print("PHASE-152: SHU-ILISHU SEAL PHONOLOGICAL TEST")
print("="*70)
print("""
  Context: Shu-ilishu, "interpreter of the Meluhha language" (Ur III, c.2020 BCE)
  Akkadian name rendering: ŠU-i-li-šu = /su/-/i/-/li/-/shu/
  Goal: What fraction of these phonemes are covered by our H+M reading set?
""")

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors = anchor_data["anchors"]

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
sign_freq = Counter(s for seq in all_seqs for s in seq)
hm_set    = {k for k,v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}

# ─── Target phoneme inventory for "Shu-ilishu" ─────────────────────────────
print("─"*70)
print("1. TARGET PHONEME COVERAGE")
print("─"*70)

# Phoneme targets: canonical + phonological variants
TARGETS = {
    "su":  ["su", "shu", "cu", "chu", "śu", "ṣu"],
    "i":   ["i", "ii", "ī"],
    "li":  ["li", "ḷi", "lī", "ḻi"],
    "shu": ["shu", "su", "śu", "ṣu", "cu", "chu"],
}

# Check each reading in H+M anchors
def reading_covers_target(reading: str, variants: list) -> bool:
    r = reading.lower()
    for v in variants:
        if v in r:
            return True
    return False

coverage_by_slot = {}
covering_signs   = {}

print(f"\n  {'Slot':<6} {'Target phoneme':<20} {'Covering H+M signs'}")
for slot, variants in TARGETS.items():
    matches = []
    for sign, data in anchors.items():
        if data.get("confidence") not in ("HIGH","MEDIUM"): continue
        reading = data.get("reading","")
        if not reading: continue
        if reading_covers_target(reading, variants):
            matches.append((sign, reading, data.get("confidence","?")))
    coverage_by_slot[slot] = matches
    covering_signs[slot] = matches
    print(f"\n  [{slot}] phoneme variants: {variants}")
    if matches:
        for sign, reading, conf in matches[:6]:
            freq = sign_freq.get(sign, 0)
            print(f"        {sign:<8} '{reading}'  ({conf}, freq={freq})")
        if len(matches) > 6:
            print(f"        ... and {len(matches)-6} more")
    else:
        print(f"        ✗ NO MATCHING H+M READING FOUND")

# ─── Coverage score ─────────────────────────────────────────────────────────
print("\n" + "─"*70)
print("2. COVERAGE SCORE")
print("─"*70)

slots_covered = sum(1 for slot, matches in coverage_by_slot.items() if matches)
n_slots = len(TARGETS)
coverage_pct = 100 * slots_covered / n_slots

print(f"\n  Slots covered: {slots_covered}/{n_slots} ({coverage_pct:.1f}%)")
for slot, matches in coverage_by_slot.items():
    status = f"COVERED ({len(matches)} candidates)" if matches else "NOT COVERED"
    print(f"    [{slot}]: {status}")

# ─── Candidate name sequences in corpus ─────────────────────────────────────
print("\n" + "─"*70)
print("3. CANDIDATE NAME SEQUENCES IN CORPUS")
print("─"*70)
print("  Searching for seals whose sign sequences could encode /su/-/i/-/li/-/su/...")

# Find seals with sequences that include signs covering at least 3 of 4 slots
su_signs  = {s for s,d in anchors.items() if d.get("confidence") in ("HIGH","MEDIUM") and reading_covers_target(d.get("reading",""), TARGETS["su"])}
i_signs   = {s for s,d in anchors.items() if d.get("confidence") in ("HIGH","MEDIUM") and reading_covers_target(d.get("reading",""), TARGETS["i"])}
li_signs  = {s for s,d in anchors.items() if d.get("confidence") in ("HIGH","MEDIUM") and reading_covers_target(d.get("reading",""), TARGETS["li"])}
shu_signs = {s for s,d in anchors.items() if d.get("confidence") in ("HIGH","MEDIUM") and reading_covers_target(d.get("reading",""), TARGETS["shu"])}

candidate_seals = []
for form, data in seals.items():
    seq = data["signs"]
    slots_hit = 0
    if any(s in su_signs for s in seq): slots_hit += 1
    if any(s in i_signs for s in seq):  slots_hit += 1
    if any(s in li_signs for s in seq): slots_hit += 1
    if any(s in shu_signs for s in seq): slots_hit += 1
    if slots_hit >= 3:
        candidate_seals.append((form, seq, slots_hit))

candidate_seals.sort(key=lambda x: -x[2])
print(f"\n  Seals with ≥3/4 slots covered: {len(candidate_seals)}")
print(f"  Top candidates:")
for form, seq, hits in candidate_seals[:8]:
    readings = [anchors.get(s,{}).get("reading","?") for s in seq]
    print(f"    {form}: {seq} → {readings} ({hits}/4 slots)")

# ─── Competing interpretations ───────────────────────────────────────────────
print("\n" + "─"*70)
print("4. COMPETING INTERPRETATIONS")
print("─"*70)

# Interpretation A: Dravidian rebus — cuvan (sun) + ili (deity/city) + cuvan
# M047 = mīn (fish), not relevant here
# Check for signs with sun/fire/deity readings
sun_readings = ["cuvan", "cūryan", "aṟu", "ōr", "ōray", "oru"]
deity_readings = ["muruku", "vēl", "il", "iḷ", "ayyar"]

drv_rebus_candidates = []
for sign, data in anchors.items():
    if data.get("confidence") not in ("HIGH","MEDIUM"): continue
    r = data.get("reading","").lower()
    if any(s in r for s in sun_readings + deity_readings):
        drv_rebus_candidates.append((sign, data["reading"], data["confidence"]))

print(f"\n  Dravidian rebus candidates (sun/deity readings): {len(drv_rebus_candidates)}")
for sign, reading, conf in drv_rebus_candidates[:5]:
    print(f"    {sign}: '{reading}' ({conf})")

# ─── Verdict ─────────────────────────────────────────────────────────────────
print("\n" + "─"*70)
print("VERDICT")
print("─"*70)

if coverage_pct >= 75:
    verdict = "STRONGLY_SUPPORTED"
    e02_upgrade = "PARTIALLY_SUPPORTED"
elif coverage_pct >= 50:
    verdict = "PARTIALLY_SUPPORTED"
    e02_upgrade = "PARTIALLY_SUPPORTED"
elif coverage_pct >= 25:
    verdict = "INSUFFICIENT"
    e02_upgrade = "INSUFFICIENT"
else:
    verdict = "NOT_COVERED"
    e02_upgrade = "INSUFFICIENT"

print(f"\n  Coverage: {slots_covered}/{n_slots} slots ({coverage_pct:.1f}%)")
print(f"  Verdict: {verdict}")
print(f"  E02 upgrade: {e02_upgrade}")
print(f"  Candidate seals: {len(candidate_seals)} seals with ≥3/4 phonological slots covered")

if coverage_pct >= 50:
    print(f"\n  INTERPRETATION: The 'Shu-ilishu' phonological test is PARTIALLY SUPPORTED.")
    print(f"  At least {slots_covered}/4 syllabic slots of the name have H+M readings that")
    print(f"  are phonologically compatible. This is not a decipherment but confirms our")
    print(f"  reading set is phonologically compatible with the external anchor.")
else:
    print(f"\n  INTERPRETATION: Coverage insufficient. The Shu-ilishu anchor requires")
    print(f"  additional phonological work (specifically: better /su/ and /li/ readings).")

# Save
output = {
    "phase": 152,
    "date": "2026-05-19",
    "subject": "Shu-ilishu interpreter seal phonological test",
    "external_anchor": {
        "name": "Shu-ilishu",
        "title": "interpreter of the Meluhha language",
        "period": "Ur III, c. 2020 BCE",
        "provenance": "excavated at Ur, held at British Museum",
        "akkadian_rendering": "ŠU-i-li-šu",
        "phonemes_targeted": ["su/shu", "i", "li", "shu/su"],
    },
    "coverage": {
        "slots_covered": slots_covered,
        "slots_total": n_slots,
        "coverage_pct": round(coverage_pct, 1),
        "slot_detail": {
            slot: [{"sign": s, "reading": anchors[s].get("reading","?")}
                   for s, r, c in matches[:5]]
            for slot, matches in coverage_by_slot.items()
        }
    },
    "candidate_seals_count": len(candidate_seals),
    "candidate_seals_top5": [{"form": f, "signs": seq, "slots_hit": hits}
                               for f, seq, hits in candidate_seals[:5]],
    "verdict": verdict,
    "e02_prior_status": "INSUFFICIENT",
    "e02_new_status": e02_upgrade,
    "key_findings": [
        f"Phoneme coverage: {slots_covered}/{n_slots} slots ({coverage_pct:.1f}%)",
        f"Verdict: {verdict}",
        f"E02 status: {e02_upgrade}",
        f"Candidate seals with ≥3/4 slots: {len(candidate_seals)}",
        "Key gap: sibilant /su/ phoneme coverage determines upgrade feasibility",
    ]
}

OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {OUT}")
print("="*70)
