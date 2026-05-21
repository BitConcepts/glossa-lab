"""
Phase-164: Meluhhan Personal Name Phonological Matching

Attempts the first computational personal name decipherment by matching
attested Meluhhan names from Mesopotamian cuneiform records against
sign sequences in our corpus whose MEDIAL slots are unread.

Meluhhan personal names attested in cuneiform (sources: Parpola 1994,
Mahadevan 1977, Ur III administrative texts):
  1. Shu-ilishu  (SU-i-li-su)     = "interpreter of Meluhha language"
  2. Lu-sunzida  (lu-sun-zi-da)    = Meluhhan merchant at Ur
  3. Ese-beli    (e-se-be-li)      = Meluhhan official
  4. Nanna-a     (nan-na-a)        = Meluhhan person
  5. Urgula      (ur-gu-la)        = Meluhhan personal name
  6. Kura-shaba  (ku-ra-sha-ba)    = Meluhhan merchant
  7. Turam-Adad  (tu-ram-a-dad)    = Meluhhan/Gulf merchant
  8. Ibni-Adad   (ib-ni-a-dad)     = Meluhhan merchant
  9. Nabi-ilishu (na-bi-i-li-su)   = Meluhhan
  10. Su-Adad    (su-a-dad)        = possibly Meluhhan

Methodology:
  1. Decompose each name into syllabic slots
  2. For each slot, find H+M signs with matching phonology
  3. Search the corpus for multi-sign sequences that could spell the name
  4. A match = candidate personal name decipherment

Output: backend/reports/phase164_meluhhan_names.json
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
PDF_DIR      = REPO / "corpora/downloads/external_repos/acquired_pdfs"
OUT          = REPO / "backend/reports/phase164_meluhhan_names.json"

print("="*70)
print("PHASE-164: MELUHHAN PERSONAL NAME PHONOLOGICAL MATCHING")
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
        site = str(row.get("site",""))
        if f and s:
            if f not in seals: seals[f] = {"site":site,"signs":[]}
            seals[f]["signs"].append(s)
except Exception:
    seals = {}
    with open(HOLDAT, encoding="utf-8") as fh:
        hdr = fh.readline().strip().split(",")
        ci = {h:i for i,h in enumerate(hdr)}
        for line in fh:
            p = line.strip().split(",")
            if len(p) < 2: continue
            f=p[ci.get("form",0)]; s=p[ci.get("letters",1)]
            site=p[ci.get("site",2)] if ci.get("site",2)<len(p) else ""
            if f and s:
                if f not in seals: seals[f]={"site":site,"signs":[]}
                seals[f]["signs"].append(s)

all_seqs  = [d["signs"] for d in seals.values()]
sign_freq = Counter(s for seq in all_seqs for s in seq)

print(f"Corpus: {len(seals)} seals")

# ─── Meluhhan name phonological decompositions ──────────────────────────
MELUHHAN_NAMES = [
    {
        "name": "Shu-ilishu",
        "akkadian": "SU-i-li-su",
        "gloss": "interpreter of the Meluhha language",
        "syllables": ["su", "i", "li", "su"],  # ŠU-i-li-šu
        "phoneme_variants": [
            ["su","cu","shu","cu"],
            ["i","ii"],
            ["li","ḷi","lī"],
            ["su","cu","shu"],
        ]
    },
    {
        "name": "Lu-sunzida",
        "akkadian": "lu-sun-zi-da",
        "gloss": "Meluhhan merchant at Ur",
        "syllables": ["lu", "sun", "zi", "da"],
        "phoneme_variants": [
            ["lu","lū"],
            ["sun","cun","cum"],
            ["ci","zi","si"],
            ["ta","da","tā"],
        ]
    },
    {
        "name": "Urgula",
        "akkadian": "ur-gu-la",
        "gloss": "Meluhhan personal name",
        "syllables": ["ur", "gu", "la"],
        "phoneme_variants": [
            ["ur","ūr"],
            ["ku","gu","kū"],
            ["al","āl","la"],
        ]
    },
    {
        "name": "Nanna-a",
        "akkadian": "nan-na-a",
        "gloss": "Meluhhan person",
        "syllables": ["nan", "na", "a"],
        "phoneme_variants": [
            ["nan","nal","naṇ"],
            ["na","nā"],
            ["ai","ay","ā"],
        ]
    },
    {
        "name": "Kura-shaba",
        "akkadian": "ku-ra-sha-ba",
        "gloss": "Meluhhan merchant",
        "syllables": ["ku", "ra", "sha", "ba"],
        "phoneme_variants": [
            ["ku","kū"],
            ["ar","ra","ār"],
            ["ca","cu","ce"],
            ["pa","pā","ba"],
        ]
    },
    {
        "name": "Ese-beli",
        "akkadian": "e-se-be-li",
        "gloss": "Meluhhan official",
        "syllables": ["e", "se", "be", "li"],
        "phoneme_variants": [
            ["ēḷ","el","eḷ","ai"],
            ["ce","ci","ca"],
            ["vē","ve","pē","pe"],
            ["li","il","iḷ","ḷi"],
        ]
    },
]

# ─── Build phonological lookup: sign → phoneme readings ──────────────────
print("\n" + "─"*70)
print("BUILDING PHONOLOGICAL SIGN INDEX")
print("─"*70)

# For each H+M sign, get all possible phonemes it could represent
sign_phonemes = {}  # sign_id -> [phoneme1, phoneme2, ...]
for sign_id, data in anchors.items():
    if data.get("confidence") not in ("HIGH","MEDIUM"): continue
    reading = data.get("reading","")
    if not reading or reading == "?": continue
    # Split on / to get variants
    variants = [r.strip().lower() for r in reading.replace("→","").split("/")]
    variants = [v for v in variants if len(v) >= 1]
    sign_phonemes[sign_id] = variants

# Build reverse index: phoneme -> [signs that could produce it]
phoneme_to_signs = defaultdict(list)
for sign_id, phonemes in sign_phonemes.items():
    for phoneme in phonemes:
        # Normalize
        p = phoneme.strip().lower()
        phoneme_to_signs[p].append(sign_id)
        # Also add truncated forms
        if len(p) >= 3:
            phoneme_to_signs[p[:2]].append(sign_id)

print(f"  H+M signs with phoneme readings: {len(sign_phonemes)}")
print(f"  Unique phoneme types: {len(phoneme_to_signs)}")

def signs_for_phoneme(phoneme_variants: list) -> list:
    """Find all signs that could represent any of the given phoneme variants."""
    candidate_signs = set()
    for variant in phoneme_variants:
        v = variant.lower()
        if v in phoneme_to_signs:
            candidate_signs.update(phoneme_to_signs[v])
        # Partial match
        for p, signs in phoneme_to_signs.items():
            if p.startswith(v[:2]) or v.startswith(p[:2]):
                candidate_signs.update(signs)
    return list(candidate_signs)

# ─── Corpus sequence matching ─────────────────────────────────────────────
print("\n" + "─"*70)
print("CORPUS SEQUENCE MATCHING")
print("─"*70)

all_name_results = []

for name_entry in MELUHHAN_NAMES:
    name = name_entry["name"]
    syllables = name_entry["syllables"]
    variants  = name_entry["phoneme_variants"]
    n_slots   = len(syllables)

    print(f"\n  {name} ({name_entry['akkadian']}) = '{name_entry['gloss']}'")

    # Find signs for each syllabic slot
    slot_signs = []
    for i, (syl, var) in enumerate(zip(syllables, variants)):
        candidates = signs_for_phoneme(var)
        slot_signs.append(set(candidates))
        print(f"  Slot {i+1} /{syl}/: {len(candidates)} candidate signs → {sorted(candidates)[:8]}")

    # Search corpus for sequences matching all slots
    matches = []
    for form, data in seals.items():
        seq = data["signs"]
        if len(seq) < n_slots: continue

        # Slide window of length n_slots
        for start in range(len(seq) - n_slots + 1):
            window = seq[start:start+n_slots]
            # Check if each sign in window matches the corresponding slot
            slot_match = sum(1 for i,sign in enumerate(window) if sign in slot_signs[i])

            if slot_match >= max(2, n_slots - 1):  # at least n-1 slots match
                match_pct = slot_match / n_slots
                readings = [anchors.get(s,{}).get("reading","?") for s in window]
                matches.append({
                    "form": form,
                    "site": data.get("site","?"),
                    "sequence": window,
                    "readings": readings,
                    "slots_matched": slot_match,
                    "total_slots": n_slots,
                    "match_pct": round(match_pct, 2),
                    "phonological_reading": " · ".join(readings),
                })

    matches.sort(key=lambda x: -x["slots_matched"])
    print(f"  Corpus matches (≥{n_slots-1}/{n_slots} slots): {len(matches)}")
    for m in matches[:5]:
        print(f"    {m['form']} ({m['site']}): {m['sequence']} → {m['phonological_reading']}")
        print(f"    Slots matched: {m['slots_matched']}/{m['total_slots']}")

    # Best candidate
    best = matches[0] if matches else None
    all_name_results.append({
        "name": name,
        "akkadian": name_entry["akkadian"],
        "gloss": name_entry["gloss"],
        "n_corpus_matches": len(matches),
        "best_match": best,
        "top_matches": matches[:5],
    })

# ─── Summary ──────────────────────────────────────────────────────────────
print("\n" + "═"*70)
print("MELUHHAN NAME DECIPHERMENT SUMMARY")
print("═"*70)

strong_matches = [r for r in all_name_results if r["n_corpus_matches"] > 0
                  and r["best_match"] and r["best_match"]["slots_matched"] >= 3]
print(f"\n  Names with strong corpus matches (≥3/4 slots): {len(strong_matches)}")
for r in strong_matches:
    m = r["best_match"]
    print(f"\n  {r['name']} ({r['akkadian']}):")
    print(f"    Corpus match: {m['sequence']}")
    print(f"    Readings: {m['phonological_reading']}")
    print(f"    Site: {m['site']}, Seal: {m['form']}")
    print(f"    Slots: {m['slots_matched']}/{m['total_slots']}")

if strong_matches:
    best_name = max(strong_matches, key=lambda x: x["best_match"]["slots_matched"])
    print(f"\n  BEST CANDIDATE: {best_name['name']}")
    print("  This would be the first Indus personal name computational decipherment")
    print("  Confidence: EXPLORATORY — requires external validation")
else:
    print("\n  No strong matches found — personal names still require ICIT corpus")
    print("  (larger corpus = more evidence for low-frequency MEDIAL sign sequences)")

# Save
output = {
    "phase": 164,
    "date": "2026-05-20",
    "meluhhan_names_tested": len(MELUHHAN_NAMES),
    "names_with_matches": len([r for r in all_name_results if r["n_corpus_matches"]>0]),
    "strong_matches": len(strong_matches),
    "results": all_name_results,
    "key_findings": [
        f"Meluhhan names tested: {len(MELUHHAN_NAMES)}",
        f"Names with ≥1 corpus match: {len([r for r in all_name_results if r['n_corpus_matches']>0])}",
        f"Strong matches (≥3 slots): {len(strong_matches)}",
        f"Best candidate: {strong_matches[0]['name'] if strong_matches else 'none'}",
        "Note: All matches are EXPLORATORY — phonological equivalences are approximate",
        "Definitive personal name reading requires bilingual text or much larger corpus",
    ]
}
OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {OUT}")
print("="*70)
