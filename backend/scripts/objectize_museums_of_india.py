"""Convert Museums of India NDJSON into canonical staging objects."""
import json, sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
TODAY = datetime.utcnow().strftime("%Y-%m-%d")
SRC = REPO / "glossa-corpus/indus/sources/museums-of-india/raw/2026-05-14/api_scrape_final/records.ndjson"
STAGING = REPO / "glossa-corpus/indus/staging"
STAGING.mkdir(exist_ok=True)

lines = SRC.read_text(encoding="utf-8").splitlines()
objects, quarantine = [], []

for i, line in enumerate(lines):
    if not line.strip():
        continue
    rec = json.loads(line)
    obj_id = rec.get("record_id", "")
    title = rec.get("title") or rec.get("name_to_view") or ""
    museum = rec.get("museum_name", "")
    desc = rec.get("description_text", "")[:500] if rec.get("description_text") else ""
    img = rec.get("display_image_url") or rec.get("thumbnail_url") or None
    terms = rec.get("search_terms_hit", [])

    reason = None if obj_id else "no record_id"

    obj = {
        "glossa_id": f"GLI-IND-MOI-{i:06d}",
        "source_system": "MuseumsOfIndia",
        "source_object_id": obj_id,
        "artifact_type": "unknown",
        "current_holding": museum,
        "site_name": None,
        "rights_status": "india-museum-restricted",
        "text_code_diplomatic": None,
        "sign_id_scheme": None,
        "image_master_uri": img,
        "review_state": "unreviewed",
        "pipeline_stage": "objectized",
        "quarantine_reason": reason,
        "_source_extra": {"title": title, "description": desc, "search_terms": terms},
        "_citation": rec.get("_citation", {"primary_sources": ["I.7"]}),
    }
    (quarantine if reason else objects).append(obj)

out = STAGING / f"objects_{TODAY}_moi.jsonl"
qur = STAGING / f"quarantine_{TODAY}_moi.jsonl"
out.write_text("\n".join(json.dumps(o) for o in objects), encoding="utf-8")
qur.write_text("\n".join(json.dumps(o) for o in quarantine), encoding="utf-8")

print(f"MoI objects: {len(objects)} written, {len(quarantine)} quarantined")
print(f"Output: {out}")
print(f"Note: rights=india-museum-restricted — discovery/metadata only, no ML/research export")
