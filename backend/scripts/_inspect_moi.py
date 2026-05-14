import json, re
from pathlib import Path
from collections import Counter

base = Path('glossa-corpus/indus/sources/museums-of-india/raw/2026-05-14/api_scrape')
manifest = json.loads((base / 'manifest.json').read_text())

print("=== FACETS PER TERM ===\n")
for term in manifest['terms']:
    t = term['term']
    n = term['api_result_size']
    print(f"--- {t} ({n} results) ---")
    for facet_name, values in term.get('facets', {}).items():
        vals = ', '.join(f"{v['name']}({v['count']})" for v in values[:6])
        print(f"  {facet_name}: {vals}")
    print()

print("\n=== MUSEUM NAMES IN RECORDS ===")
museums = Counter()
descriptions = []
with open(base / 'records.ndjson', encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        museums[r['museum_name']] += 1
        descriptions.append(r['description_text'])

for name, count in museums.most_common():
    print(f"  {count:4d}  {name}")

print("\n=== COMMON WORDS IN DESCRIPTIONS (excluding stopwords) ===")
stopwords = {'the','a','an','and','or','of','in','is','it','to','with','on',
             'at','by','from','for','as','are','was','were','has','have',
             'this','that','these','those','which','its','also','been',
             'made','one','two','three','four','five','cm','mm','no','not'}
word_counts = Counter()
for desc in descriptions:
    words = re.findall(r'[a-z]{4,}', desc.lower())
    word_counts.update(w for w in words if w not in stopwords)

print("Top 60 content words:")
for word, count in word_counts.most_common(60):
    print(f"  {count:5d}  {word}")
