"""Build the Kalyanaraman rebus lexicon from the 52 imported PDFs.

Extracts:
  - Rebus pairs (pictogram → meaning)
  - Dravidian craft/trade terms with frequency
  - Sign references (M-numbers or description → reading)
  - Metalwork vocabulary

Output: backend/glossa_lab/data/kalyanaraman_rebus.json
"""
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB = REPO / "backend" / "data" / "glossa.db"
DOWNLOADS = Path.home() / "Downloads"
OUT = REPO / "backend" / "glossa_lab" / "data" / "kalyanaraman_rebus.json"

# ── 1. Extract full text from PDFs ──────────────────────────────────────────

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber required. pip install pdfplumber")
    exit(1)

# Find the PDFs — look in Downloads and also check the DB for file paths
conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row
db_rows = conn.execute(
    "SELECT id, title, raw_json FROM discovery_items WHERE source='local_pdf'"
).fetchall()
conn.close()

# Collect PDF file paths from DB raw_json
pdf_paths: list[Path] = []
for r in db_rows:
    raw = r["raw_json"]
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = {}
    fn = raw.get("filename", "")
    if fn:
        # Try Downloads folder
        p = DOWNLOADS / fn
        if p.exists():
            pdf_paths.append(p)
            continue
    # Also try matching title to filename in Downloads
    title = r["title"] or ""
    for pdf in DOWNLOADS.glob("*.pdf"):
        if title[:30].lower().replace(" ", "_") in pdf.stem.lower():
            pdf_paths.append(pdf)
            break

pdf_paths = sorted(set(pdf_paths))
print(f"Found {len(pdf_paths)} PDF files to process")

# ── 2. Extract terms from each PDF ─────────────────────────────────────────

all_rebus: dict[str, dict] = {}  # pictogram → {meaning, sources[], count}
all_terms: Counter = Counter()
craft_terms: dict[str, dict] = {}  # term → {meaning_context, count, sources[]}
sign_refs: dict[str, list[str]] = defaultdict(list)  # M-number → [readings]

# Known craft/trade domain terms from Kalyanaraman's metalwork lexicon
CRAFT_DOMAIN = {
    "kaṇḍ", "khār", "kolhe", "kol", "kolimi", "kuṭhi", "dul", "dhāḷ",
    "phaḍ", "eraka", "kamaṭha", "kammaṭa", "sāṅgaḍa", "meḍ", "mēḍh",
    "baṭa", "badhia", "dula", "jhāl", "karṇī", "loa", "lohar",
    "arka", "arke", "bica", "bica", "kaḍa", "kuṭila", "kunda",
    "pōḷa", "sālika", "satavu", "ṭhākur", "tagar",
}

for pdf_path in pdf_paths:
    source_name = pdf_path.stem
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            text = ""
            for page in pdf.pages[:20]:  # up to 20 pages
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception as e:
        print(f"  Skip {pdf_path.name}: {e}")
        continue

    # a) Extract rebus pairs: 'X' rebus 'Y' or X rebus Y
    for m in re.finditer(
        r"['\u2018]([a-zA-Z\u0100-\u1EFF\u0900-\u097F]{2,25})['\u2019]?"
        r"\s*(?:rebus|Rebus|=)\s*"
        r"['\u2018]?([a-zA-Z\u0100-\u1EFF\u0900-\u097F]{2,25})['\u2019]?",
        text, re.IGNORECASE
    ):
        pic = m.group(1).strip()
        meaning = m.group(2).strip()
        # Skip English function words
        if pic.lower() in ("the", "and", "for", "with", "from", "that", "this",
                           "are", "was", "were", "has", "have", "had", "been",
                           "being", "which", "their", "there", "these", "those"):
            continue
        if meaning.lower() in ("the", "and", "for", "with", "from", "that",
                               "this", "reading", "decoding", "signifier"):
            continue
        key = pic.lower()
        if key not in all_rebus:
            all_rebus[key] = {
                "pictogram": pic,
                "meaning": meaning,
                "sources": [],
                "count": 0,
            }
        all_rebus[key]["count"] += 1
        if source_name not in all_rebus[key]["sources"]:
            all_rebus[key]["sources"].append(source_name)

    # b) Extract single-quoted Dravidian terms
    for m in re.finditer(
        r"['\u2018\u2019]([a-zA-Z\u0100-\u1EFF]{2,20})['\u2018\u2019]",
        text
    ):
        term = m.group(1).strip()
        if len(term) >= 2 and term.lower() not in (
            "the", "and", "for", "with", "from", "that", "this", "are",
            "was", "were", "has", "have", "had", "been", "being", "is",
            "it", "its", "or", "an", "as", "in", "on", "to", "of", "a",
        ):
            all_terms[term.lower()] += 1

    # c) Extract M-number references: M-123, M123, Sign 123
    for m in re.finditer(r"(?:M-?|Sign\s+)(\d{1,3})\b", text):
        num = int(m.group(1))
        if 1 <= num <= 420:
            sign_id = f"M{num:03d}"
            # Look for a reading near this reference
            start = max(0, m.start() - 100)
            end = min(len(text), m.end() + 200)
            ctx = text[start:end]
            # Find quoted terms near the sign reference
            for tm in re.finditer(
                r"['\u2018]([a-zA-Z\u0100-\u1EFF]{2,15})['\u2019]", ctx
            ):
                reading = tm.group(1).strip().lower()
                if reading not in sign_refs[sign_id] and len(reading) >= 2:
                    sign_refs[sign_id].append(reading)

    # d) Extract craft domain terms
    for craft in CRAFT_DOMAIN:
        pattern = re.escape(craft)
        hits = re.findall(pattern, text, re.IGNORECASE)
        if hits:
            key = craft.lower()
            if key not in craft_terms:
                craft_terms[key] = {"term": craft, "count": 0, "sources": []}
            craft_terms[key]["count"] += len(hits)
            if source_name not in craft_terms[key]["sources"]:
                craft_terms[key]["sources"].append(source_name)

# ── 3. Build the lexicon ────────────────────────────────────────────────────

# Sort rebus pairs by count
rebus_list = sorted(all_rebus.values(), key=lambda x: -x["count"])

# Top Dravidian terms (frequency >= 3)
top_terms = [
    {"term": t, "frequency": c}
    for t, c in all_terms.most_common(200)
    if c >= 3
]

# Sign references with readings
sign_readings = {
    sid: readings[:5]  # cap at 5 per sign
    for sid, readings in sorted(sign_refs.items())
    if readings
}

lexicon = {
    "_citation": "Kalyanaraman, S. (2017-2024). Indus Script Cipher: "
                 "Hieroglyphs of Indian linguistic area. "
                 "52 papers on rebus interpretation of Indus Script seal "
                 "inscriptions. Sarasvati Research Center.",
    "_method": "Extracted via pdfplumber from 52 PDF papers. "
               "Rebus pairs identified by 'X rebus Y' pattern. "
               "Dravidian terms by single-quote extraction. "
               "Sign references by M-number proximity.",
    "_built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "_stats": {
        "papers_processed": len(pdf_paths),
        "rebus_pairs": len(rebus_list),
        "dravidian_terms": len(top_terms),
        "sign_references": len(sign_readings),
        "craft_terms": len(craft_terms),
    },
    "system": "content_word_rebus",
    "domain": "metalwork_trade_craft",
    "rebus_pairs": rebus_list,
    "dravidian_terms": top_terms,
    "sign_readings": sign_readings,
    "craft_vocabulary": sorted(
        craft_terms.values(), key=lambda x: -x["count"]
    ),
}

OUT.write_text(json.dumps(lexicon, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"\n{'='*60}")
print("KALYANARAMAN REBUS LEXICON BUILT")
print(f"{'='*60}")
print(f"Papers processed:   {len(pdf_paths)}")
print(f"Rebus pairs:        {len(rebus_list)}")
print(f"Dravidian terms:    {len(top_terms)} (freq >= 3)")
print(f"Sign references:    {len(sign_readings)} signs with readings")
print(f"Craft vocabulary:   {len(craft_terms)} terms")
print(f"\nOutput: {OUT}")
