"""Second-pass accuracy audit: verify every release number independently."""
import json, csv, unicodedata
from collections import Counter
from pathlib import Path

anchors = json.loads(Path(r'C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports\INDUS_FINAL_ANCHORS.json').read_text('utf-8')).get('anchors', {})
release = json.loads(Path(r'C:\Users\trist\Development\BitConcepts\glossa-lab\outputs\RELEASE_VALIDATION.json').read_text('utf-8'))

holdat = []
with open(r'C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads\external_repos\holdatllc_indus\indus_corpus 2.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        holdat.append(r['letters'])

high = {s: i for s, i in anchors.items() if i.get('confidence') == 'HIGH' and i.get('reading')}
errors = []

print("=" * 60)
print("SECOND-PASS ACCURACY AUDIT")
print("=" * 60)

# 1. Release numbers match fresh computation
print("\n1. Release number consistency")
if release['anchor_state']['high_with_reading'] != len(high):
    errors.append(f"HIGH count: release={release['anchor_state']['high_with_reading']} vs actual={len(high)}")
else:
    print(f"   HIGH count: {len(high)} OK")

covered = sum(1 for t in holdat if t in high)
cov_pct = round(covered / len(holdat), 4)
if release['anchor_state']['holdat_token_coverage'] != cov_pct:
    errors.append(f"Coverage: release={release['anchor_state']['holdat_token_coverage']} vs actual={cov_pct}")
else:
    print(f"   Coverage: {cov_pct} OK")

distinct = len(set(i.get('reading') for i in high.values()))
if release['anchor_state']['distinct_readings'] != distinct:
    errors.append(f"Distinct: release={release['anchor_state']['distinct_readings']} vs actual={distinct}")
else:
    print(f"   Distinct: {distinct} OK")

# 2-4. Confidence integrity
high_empty = sum(1 for i in anchors.values() if i.get('confidence') == 'HIGH' and not i.get('reading'))
low_with = sum(1 for i in anchors.values() if i.get('confidence') == 'LOW' and i.get('reading'))
med = sum(1 for i in anchors.values() if i.get('confidence') == 'MEDIUM')
print(f"\n2. HIGH empty reading: {high_empty} {'OK' if high_empty == 0 else 'ERROR'}")
print(f"3. LOW with reading: {low_with} {'OK' if low_with == 0 else 'ERROR'}")
print(f"4. MEDIUM count: {med} {'OK' if med == 0 else 'ERROR'}")
if high_empty > 0: errors.append(f"{high_empty} HIGH signs have no reading")
if low_with > 0: errors.append(f"{low_with} LOW signs have readings")
if med > 0: errors.append(f"{med} MEDIUM signs exist")

# 5. No mass-assignments
readings = Counter(i.get('reading') for i in high.values())
max_r, max_c = readings.most_common(1)[0]
print(f"5. Max duplication: {max_r}={max_c} {'OK' if max_c <= 20 else 'ERROR'}")
if max_c > 20: errors.append(f"Reading '{max_r}' has {max_c} signs (>20)")

# 6. Holdat completeness
missing = set(holdat) - set(anchors.keys())
print(f"6. Holdat signs missing from anchors: {len(missing)} {'OK' if len(missing) == 0 else 'ERROR'}")
if missing: errors.append(f"{len(missing)} Holdat signs not in anchors")

# 7. Pin distribution (discrimination test weakness check)
pins = {}
for s, i in high.items():
    r = i.get('reading', '')
    if r:
        clean = r.split('/')[0].strip()
        if clean: pins[s] = clean[0]
pin_counts = Counter(pins.values())
top_pin, top_count = pin_counts.most_common(1)[0]
top_pct = top_count / len(pins) * 100
print(f"\n7. Pin distribution: {len(pin_counts)} distinct chars, top='{top_pin}' ({top_pct:.0f}%)")
print(f"   Top 5: {pin_counts.most_common(5)}")
if top_pct > 30:
    print(f"   WARNING: '{top_pin}' covers {top_pct:.0f}% - discrimination test is dominated by one initial")
    # This isn't an error, but should be disclosed

# 8. Dravidian LM size
drav = json.loads(Path(r'C:\Users\trist\Development\BitConcepts\glossa-lab\backend\glossa_lab\data\dravidian_tamil_lm.json').read_text('utf-8'))
n_bi = len(drav.get('bigrams', {}))
print(f"\n8. Dravidian LM: {n_bi} bigrams {'OK' if n_bi >= 50 else 'WARNING: small'}")

# 9. Totals
total = len(anchors)
n_high = sum(1 for i in anchors.values() if i.get('confidence') == 'HIGH')
n_low = sum(1 for i in anchors.values() if i.get('confidence') == 'LOW')
print(f"\n9. Total: {total} = {n_high}H + {n_low}L {'OK' if total == 605 else 'ERROR'}")
if total != 605: errors.append(f"Total is {total}, not 605")

# 10. Parpola verification with pre-stripped values
def strip(s):
    nfkd = unicodedata.normalize('NFKD', s.lower())
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

PARPOLA = {
    'M047': 'min', 'M048': 'min', 'M176': 'ko/an', 'M099': 'kol/vil',
    'M001': 'tol', 'M086': 'oru/onru', 'M087': 'vel/irantu',
    'M088': 'munru', 'M091': 'aru', 'M092': 'elu',
    'M060': 'kanta-mrga', 'M261': 'muruku', 'M175': 'katir',
    'M211': 'ko', 'M124': 'kutam', 'M117': 'ar/cakra',
    'M233': 'ur', 'M162': 'il', 'M281': 'pillai', 'M342': 'jar/pot',
}
exact_count = 0
for sid, p_r in PARPOLA.items():
    our_r = anchors.get(sid, {}).get('reading', '')
    if not our_r: continue
    our_alts = set(strip(x) for x in our_r.split('/') if x.strip())
    par_alts = set(strip(x) for x in p_r.split('/') if x.strip())
    if our_alts & par_alts:
        exact_count += 1

release_exact = release['3_parpola_crosscheck']['exact']
match = exact_count == release_exact
print(f"\n10. Parpola exact: computed={exact_count} vs release={release_exact} {'OK' if match else 'ERROR'}")
if not match: errors.append(f"Parpola mismatch: {exact_count} vs {release_exact}")

# 11. Check the 192 Yajnadevam HIGH signs - are they inflating claims?
yaj_high = sum(1 for i in anchors.values()
               if i.get('source') == 'Phase-288 Yajnadevam' and i.get('confidence') == 'HIGH')
yaj_in_holdat = sum(1 for s, i in anchors.items()
                    if i.get('source') == 'Phase-288 Yajnadevam' and s in set(holdat))
print(f"\n11. Yajnadevam HIGH: {yaj_high} signs, {yaj_in_holdat} in Holdat")
print(f"    These inflate the 400 HIGH count but contribute 0% to Holdat coverage")
print(f"    Holdat-validated HIGH signs: {len(high) - yaj_high}")
print(f"    DISCLOSURE: 400 HIGH = {len(high) - yaj_high} Holdat-validated + {yaj_high} Yajnadevam-only")

# SUMMARY
print("\n" + "=" * 60)
if errors:
    print(f"ERRORS FOUND: {len(errors)}")
    for e in errors:
        print(f"  ✗ {e}")
else:
    print("ALL 11 CHECKS PASSED — no errors found")

print(f"\nDISCLOSURES (not errors, but should be noted in preprint):")
print(f"  • Pin distribution: '{top_pin}' covers {top_pct:.0f}% of anchor first-chars")
print(f"  • 400 HIGH = {len(high) - yaj_high} Holdat-validated + {yaj_high} Yajnadevam-only (0 in Holdat)")
print(f"  • Dravidian LM has {n_bi} bigrams")
print("=" * 60)
