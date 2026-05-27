import json, csv
from collections import Counter
from pathlib import Path

anchors = json.loads(Path(r'C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports\INDUS_FINAL_ANCHORS.json').read_text('utf-8')).get('anchors', {})
high = {s: i for s, i in anchors.items() if i.get('confidence') == 'HIGH' and i.get('reading')}

inscriptions = []
with open(r'C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads\external_repos\holdatllc_indus\indus_corpus 2.csv', encoding='utf-8') as f:
    cur_seal = None; cur_signs = []; cur_motif = ''
    for r in csv.DictReader(f):
        if r['cisi_number'] != cur_seal:
            if cur_signs:
                inscriptions.append({'signs': cur_signs, 'motif': cur_motif, 'seal': cur_seal})
            cur_seal = r['cisi_number']; cur_signs = []; cur_motif = r.get('motif', '')
        cur_signs.append(r['letters'])
    if cur_signs:
        inscriptions.append({'signs': cur_signs, 'motif': cur_motif, 'seal': cur_seal})

# Translate
n_full = n_partial = n_zero = 0
translations = []
for ins in inscriptions:
    readings = [high.get(s, {}).get('reading', '?') for s in ins['signs']]
    pct = sum(1 for r in readings if r != '?') / len(readings)
    if pct == 1.0: n_full += 1
    elif pct > 0: n_partial += 1
    else: n_zero += 1
    if pct == 1.0 and len(ins['signs']) >= 3:
        translations.append({
            'seal': ins['seal'], 'motif': ins['motif'],
            'signs': ins['signs'], 'reading': ' '.join(readings),
            'length': len(ins['signs'])
        })

print(f"Inscriptions: {len(inscriptions)}")
print(f"Fully decoded (HIGH only): {n_full} ({n_full/len(inscriptions)*100:.0f}%)")
print(f"Partial: {n_partial}, Zero: {n_zero}")
print(f"\nFully decoded 3+ signs: {len(translations)}")
print("Longest fully-decoded inscriptions:")
for t in sorted(translations, key=lambda x: -x['length'])[:12]:
    signs_str = ' '.join(t['signs'])
    print(f"  {t['seal']:12s} [{t['motif']:12s}] {signs_str:30s} -> {t['reading']}")

# Motif correlation
motif_initial = {}
for ins in inscriptions:
    motif = ins['motif'].strip() or 'unknown'
    first_sign = ins['signs'][0] if ins['signs'] else ''
    r = high.get(first_sign, {}).get('reading', '')
    if r:
        motif_initial.setdefault(motif, Counter())[r] += 1

print("\nMotif vs initial-sign reading (top 5 motifs):")
for motif in sorted(motif_initial, key=lambda m: -sum(motif_initial[m].values()))[:6]:
    top = motif_initial[motif].most_common(5)
    total = sum(motif_initial[motif].values())
    print(f"  {motif:15s} (n={total}): {[(r,c) for r,c in top]}")

# Bigram reading pairs
bigram_readings = Counter()
for ins in inscriptions:
    for i in range(len(ins['signs']) - 1):
        r1 = high.get(ins['signs'][i], {}).get('reading', '')
        r2 = high.get(ins['signs'][i+1], {}).get('reading', '')
        if r1 and r2:
            bigram_readings[(r1, r2)] += 1

print("\nTop 15 reading bigrams:")
for (r1, r2), c in bigram_readings.most_common(15):
    print(f"  {r1:10s} + {r2:10s} = {c}")
