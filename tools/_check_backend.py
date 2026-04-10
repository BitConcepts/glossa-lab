import urllib.request, json

with urllib.request.urlopen('http://localhost:8001/api/v1/catalog', timeout=3) as r:
    data = json.loads(r.read())
    print("Experiments in catalog:", data['counts']['experiments'])
    print("Reports in catalog:", data['counts']['reports'])

with urllib.request.urlopen('http://localhost:8001/api/v1/experiments', timeout=3) as r:
    exps = json.loads(r.read())
    ids = [e['id'] for e in exps]
    print("Total experiment IDs served:", len(ids))
    new = ['tier3_oracle_analysis','tier3_sumerian_classified',
           'tier5_phonogram_only','ventris_threshold_sweep',
           'beam_decipher_benchmark','tier5_indus_decipherment',
           'tier3_sumerian_validation','tier5_indus_readings']
    print("\nNew experiments visibility:")
    for eid in new:
        status = "VISIBLE" if eid in ids else "MISSING - needs restart"
        print(f"  {eid}: {status}")

# Check study seeds
with urllib.request.urlopen('http://localhost:8001/api/v1/studies', timeout=3) as r:
    studies = json.loads(r.read())
    names = [s.get('name','?') for s in studies]
    print("\nStudies in DB:", len(studies))
    for n in names:
        print(f"  {n}")
    beam_suite = "Beam Decipherment Suite" in names
    fuls_updated = any("Fuls" in n for n in names)
    print("\nBeam Decipherment Suite study:", "PRESENT" if beam_suite else "MISSING - needs restart")
    print("Dr. Fuls study:", "PRESENT" if fuls_updated else "MISSING")
