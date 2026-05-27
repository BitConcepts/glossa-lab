import json, unicodedata
from pathlib import Path

anchors = json.loads(Path(r'C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports\INDUS_FINAL_ANCHORS.json').read_text('utf-8')).get('anchors', {})

def strip(s):
    nfkd = unicodedata.normalize('NFKD', s.lower())
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

PARPOLA = {
    'M047': 'mīn', 'M048': 'mīn', 'M176': 'kō/an', 'M099': 'kol/vil',
    'M001': 'tōḷ', 'M086': 'oru/oṉṟu', 'M087': 'veḷ/iraṇṭu',
    'M088': 'mūṉṟu', 'M091': 'āṟu', 'M092': 'ēḻu',
    'M060': 'kāṇṭā-mṛga', 'M261': 'muruku', 'M175': 'katir',
    'M211': 'kō', 'M124': 'kuṭam', 'M117': 'ar/cakra',
    'M233': 'ūr', 'M162': 'il', 'M281': 'piḷḷai', 'M342': 'jar/pot',
}

print("PARPOLA CROSS-CHECK - EVERY COMPARISON")
print(f"{'Sign':7s} | {'Our':20s} | {'Parpola':20s} | {'Our_s':15s} | {'Par_s':15s} | Match")
print("-" * 100)

exact = partial = disagree = 0
for sign_id in sorted(PARPOLA.keys()):
    p_reading = PARPOLA[sign_id]
    our_r = anchors.get(sign_id, {}).get('reading', '')
    if not our_r:
        print(f"{sign_id:7s} | {'(none)':20s} | {p_reading:20s} | {'':15s} | {'':15s} | NO_READING")
        continue

    our_s = strip(our_r.split('/')[0].strip())
    p_s = strip(p_reading.split('/')[0].strip())

    # Check: is p_s contained in the stripped full reading?
    full_stripped = strip(our_r)
    
    if our_s == p_s:
        match = "EXACT (first-word match)"
        exact += 1
    elif p_s in full_stripped:
        match = f"EXACT (p_s '{p_s}' in full '{full_stripped}')"
        exact += 1
    elif our_s[:3] == p_s[:3]:
        match = "PARTIAL (3-char)"
        partial += 1
    else:
        match = "DISAGREE"
        disagree += 1

    print(f"{sign_id:7s} | {our_r:20s} | {p_reading:20s} | {our_s:15s} | {p_s:15s} | {match}")

total = exact + partial + disagree
print(f"\nExact: {exact}, Partial: {partial}, Disagree: {disagree}")
print(f"Rate: {(exact+partial)/total*100:.0f}%")

# Flag the suspicious check: p_s in full_stripped
# This could be too loose - e.g. if p_s is "ar" and full reading contains "ar" somewhere
print("\n=== CHECKING FOR LOOSE MATCHES ===")
for sign_id in sorted(PARPOLA.keys()):
    p_reading = PARPOLA[sign_id]
    our_r = anchors.get(sign_id, {}).get('reading', '')
    if not our_r: continue
    our_s = strip(our_r.split('/')[0].strip())
    p_s = strip(p_reading.split('/')[0].strip())
    full_stripped = strip(our_r)
    
    if our_s != p_s and p_s in full_stripped:
        print(f"  LOOSE: {sign_id}: our='{our_r}' parpola='{p_reading}'")
        print(f"         our_s='{our_s}' != p_s='{p_s}' but p_s in full='{full_stripped}'")
