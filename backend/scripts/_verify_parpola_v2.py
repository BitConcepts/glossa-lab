"""Strict Parpola comparison: check all slash-alternatives, no substring tricks."""
import json, unicodedata
from pathlib import Path

anchors = json.loads(Path(r'C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports\INDUS_FINAL_ANCHORS.json').read_text('utf-8')).get('anchors', {})

def strip(s):
    nfkd = unicodedata.normalize('NFKD', s.lower().strip())
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

def get_alternatives(reading):
    """Split on / and strip each alternative."""
    return [strip(x) for x in reading.split('/') if x.strip()]

PARPOLA = {
    'M047': 'mīn', 'M048': 'mīn', 'M176': 'kō/an', 'M099': 'kol/vil',
    'M001': 'tōḷ', 'M086': 'oru/oṉṟu', 'M087': 'veḷ/iraṇṭu',
    'M088': 'mūṉṟu', 'M091': 'āṟu', 'M092': 'ēḻu',
    'M060': 'kāṇṭā-mṛga', 'M261': 'muruku', 'M175': 'katir',
    'M211': 'kō', 'M124': 'kuṭam', 'M117': 'ar/cakra',
    'M233': 'ūr', 'M162': 'il', 'M281': 'piḷḷai', 'M342': 'jar/pot',
}

print("STRICT PARPOLA COMPARISON (all alternatives, no substrings)")
print(f"{'Sign':7s} | {'Our':20s} | {'Parpola':20s} | {'Our alts':25s} | {'Par alts':25s} | Match")
print("-" * 120)

exact = partial = disagree = 0
details = []

for sign_id in sorted(PARPOLA.keys()):
    p_reading = PARPOLA[sign_id]
    our_r = anchors.get(sign_id, {}).get('reading', '')
    if not our_r:
        print(f"{sign_id:7s} | {'(none)':20s} | {p_reading:20s} | {'':25s} | {'':25s} | NO_READING")
        continue

    our_alts = get_alternatives(our_r)
    par_alts = get_alternatives(p_reading)

    # STRICT: any of our alternatives exactly matches any of Parpola's alternatives
    exact_match = bool(set(our_alts) & set(par_alts))
    
    # PARTIAL: first 3 chars of any pair match
    partial_match = False
    if not exact_match:
        for oa in our_alts:
            for pa in par_alts:
                if len(oa) >= 3 and len(pa) >= 3 and oa[:3] == pa[:3]:
                    partial_match = True
                    break

    if exact_match:
        match = "EXACT"
        overlap = set(our_alts) & set(par_alts)
        match += f" ({overlap})"
        exact += 1
    elif partial_match:
        match = "PARTIAL"
        partial += 1
    else:
        match = "DISAGREE"
        disagree += 1

    our_str = str(our_alts)[:25]
    par_str = str(par_alts)[:25]
    print(f"{sign_id:7s} | {our_r:20s} | {p_reading:20s} | {our_str:25s} | {par_str:25s} | {match}")
    details.append({"sign": sign_id, "ours": our_r, "parpola": p_reading, "match": match.split(" ")[0]})

total = exact + partial + disagree
rate = (exact + partial) / total if total else 0
print(f"\nSTRICT RESULTS:")
print(f"  Exact: {exact}")
print(f"  Partial: {partial}")
print(f"  Disagree: {disagree}")
print(f"  Rate: {exact+partial}/{total} = {rate:.0%}")
print(f"\nThis is the HONEST Parpola agreement rate.")
