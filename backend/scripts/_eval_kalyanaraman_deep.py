"""Deep evaluation of Kalyanaraman papers against INDUS_FINAL_ANCHORS.

Extracts full text from PDFs (not just 2KB preview), finds Dravidian
terms, and cross-checks against anchor readings.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
DOWNLOADS = Path.home() / "Downloads"

# Load anchors
fa = json.loads(ANCHORS.read_text(encoding="utf-8"))
anchors = fa.get("anchors", {})

# Build reading → sign mapping (all variants)
reading_to_sign: dict[str, list[str]] = defaultdict(list)
for sid, info in anchors.items():
    reading = info.get("reading", "")
    if reading:
        for variant in reading.split("/"):
            v = re.sub(r"[^a-z]", "", variant.strip().lower())
            if len(v) >= 2:
                reading_to_sign[v].append(sid)

# Known Dravidian terms from your anchor readings
anchor_terms = set(reading_to_sign.keys())
print(f"Anchors: {len(anchors)} signs, {len(anchor_terms)} unique reading roots")

# Extract full text from all 52 PDFs
import pdfplumber

papers = sorted(DOWNLOADS.glob("*.pdf"))
keywords = [
    'Meluhha', 'kamaha', 'Smelted', 'Proto_elamite', 'Trisiras', 'Koava',
    'Array_of', 'Merchant_metal', 'Chimerae', 'Bar_of_metal', 'badhia',
    'Sarasvati', 'Koiya', 'kol_raft', 'Wealth_goods', 'Vaisali', 'kuavari',
    'Semantograph', 'Black_drongo', 'Kot_Diji', 'Soma_tin', 'Konda',
    'Treasure', 'Eureka', 'Pon_pavana', 'Inscriptions_on', 'anthropomorph',
    'Steersman', 'metalwork_ledgers', 'Warehouse', 'Ledgers_of', 'Bronze_Age',
    'satavu', 'Kunda', 'Kaa_wealth', 'Metalcastings', 'Dul_metal',
    'khara_hare', 'Maritime', 'Thar_line', 'kolhe_jhal', 'Malhar',
    'Kuikuila', 'Metalwork_semantographs', 'Etymology', 'Fauna_economic',
    'Metalcasting_forge', 'Focus_on_Kodava',
]
target_papers = [p for p in papers if any(kw.lower() in p.name.lower() for kw in keywords)]

all_terms: Counter = Counter()
all_rebuses: dict[str, str] = {}
paper_count = 0

for pdf_path in target_papers:
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            text = ""
            for page in pdf.pages[:15]:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception as e:
        print(f"  Skip {pdf_path.name}: {e}")
        continue

    paper_count += 1

    # Extract 'term' patterns (single-quoted Dravidian words)
    for m in re.finditer(r"['\u2018\u2019]([a-zA-Z\u0100-\u1EFF]{2,15})['\u2018\u2019]", text):
        term = re.sub(r"[^a-z]", "", m.group(1).lower())
        if len(term) >= 2:
            all_terms[term] += 1

    # Extract "X rebus Y" patterns (broader)
    for m in re.finditer(
        r"['\u2018]([a-zA-Z\u0100-\u1EFF]{2,20})['\u2019]?\s*(?:rebus|=)\s*['\u2018]?([a-zA-Z\u0100-\u1EFF]{2,20})['\u2019]?",
        text, re.IGNORECASE
    ):
        pic = re.sub(r"[^a-z]", "", m.group(1).lower())
        meaning = re.sub(r"[^a-z]", "", m.group(2).lower())
        if len(pic) >= 2 and len(meaning) >= 2:
            all_rebuses[pic] = meaning

print(f"\nPapers fully analyzed: {paper_count}")
print(f"Unique quoted terms: {len(all_terms)}")
print(f"Rebus pairs: {len(all_rebuses)}")

# Cross-check terms against anchor readings
print("\n=== ANCHOR OVERLAP: Terms found in BOTH Kalyanaraman AND your anchors ===\n")

overlap = []
for term, count in all_terms.most_common(200):
    if term in anchor_terms:
        signs = reading_to_sign[term]
        for sid in signs[:2]:
            conf = anchors[sid].get("confidence", "?")
            reading = anchors[sid].get("reading", "")
            overlap.append((term, count, sid, conf, reading))

for term, count, sid, conf, reading in overlap[:25]:
    print(f"  '{term}' ×{count}  →  {sid} [{conf}] = '{reading}'")

print(f"\nTotal overlapping terms: {len(overlap)}")

# Rebus cross-check
print("\n=== REBUS CROSS-CHECK ===\n")
rebus_matches = 0
rebus_new = 0
for pic, meaning in sorted(all_rebuses.items()):
    pic_in = pic in anchor_terms
    meaning_in = meaning in anchor_terms
    if pic_in or meaning_in:
        rebus_matches += 1
        signs = reading_to_sign.get(pic, []) or reading_to_sign.get(meaning, [])
        sid = signs[0] if signs else "?"
        print(f"  ✓ '{pic}' → '{meaning}' (anchor: {sid})")
    else:
        rebus_new += 1

print(f"\nRebus matches: {rebus_matches}, New: {rebus_new}")

# Summary
print(f"\n{'='*60}")
print(f"EVALUATION SUMMARY")
print(f"{'='*60}")
print(f"Papers analyzed:           {paper_count}")
print(f"Unique Dravidian terms:    {len(all_terms)}")
print(f"Your anchor readings:      {len(anchor_terms)}")
print(f"Overlapping terms:         {len(overlap)}")
print(f"Rebus pairs extracted:     {len(all_rebuses)}")
print(f"Rebus/anchor matches:      {rebus_matches}")
print(f"New rebus candidates:      {rebus_new}")
if overlap:
    high_conf = sum(1 for _, _, _, c, _ in overlap if c == "HIGH")
    med_conf = sum(1 for _, _, _, c, _ in overlap if c == "MEDIUM")
    print(f"Corroborated HIGH anchors: {high_conf}")
    print(f"Corroborated MED anchors:  {med_conf}")
