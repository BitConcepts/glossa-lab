"""Auto-fix anchor quality issues found by _audit_anchors.py.

Fixes applied:
1. Remove phantom anchors (signs not in Holdat corpus)
2. Remove anchors with empty readings
3. Downgrade bulk-duplicate readings (48x "mīn" etc.) to CANDIDATE
4. Recalculate total and coverage after cleanup

Creates a backup before modifying.
"""
import csv
import json
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"
BACKUP_PATH = ANCHORS_PATH.with_suffix(".json.bak")

# Load corpus signs
corpus_signs: set[str] = set()
corpus_freq: Counter[str] = Counter()
if HOLDAT_PATH.exists():
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sign = row.get("letters", "").strip()
            if sign:
                corpus_signs.add(sign)
                corpus_freq[sign] += 1
    print(f"Corpus: {len(corpus_signs)} unique signs, {sum(corpus_freq.values())} tokens")
else:
    print("ERROR: Holdat corpus not found!")
    exit(1)

# Load anchors
fa = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))
anchors = fa.get("anchors", {})
original_count = len(anchors)
print(f"Original anchors: {original_count}")

# Backup
shutil.copy2(ANCHORS_PATH, BACKUP_PATH)
print(f"Backup saved to: {BACKUP_PATH}")

# Track changes
removed_phantom = 0
removed_empty = 0
downgraded_dup = 0
now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# 1. Remove phantom anchors (not in corpus)
to_remove = []
for sid in list(anchors.keys()):
    if sid not in corpus_signs:
        to_remove.append(sid)

for sid in to_remove:
    del anchors[sid]
    removed_phantom += 1
print(f"Removed {removed_phantom} phantom anchors (not in corpus)")

# 2. Remove empty readings
to_remove = []
for sid, info in list(anchors.items()):
    reading = (info.get("reading") or "").strip()
    if not reading:
        to_remove.append(sid)

for sid in to_remove:
    del anchors[sid]
    removed_empty += 1
print(f"Removed {removed_empty} anchors with empty readings")

# 3. Downgrade bulk-duplicate readings
# Find readings assigned to > 5 signs
reading_to_signs: dict[str, list[str]] = defaultdict(list)
for sid, info in anchors.items():
    reading = info.get("reading", "").strip().lower()
    if reading:
        reading_to_signs[reading].append(sid)

DUPLICATE_THRESHOLD = 5  # more than 5 signs with same reading = suspicious
for reading, signs in reading_to_signs.items():
    if len(signs) > DUPLICATE_THRESHOLD:
        for sid in signs:
            old_conf = anchors[sid].get("confidence", "?")
            if old_conf in ("HIGH", "MEDIUM"):
                anchors[sid]["confidence"] = "CANDIDATE"
                anchors[sid]["_audit_note"] = (
                    f"Downgraded {old_conf}→CANDIDATE on {now}: "
                    f"reading '{reading}' shared by {len(signs)} signs (bulk assignment)"
                )
                downgraded_dup += 1

print(f"Downgraded {downgraded_dup} bulk-duplicate readings to CANDIDATE")

# 4. Recalculate totals
by_conf = Counter(v.get("confidence", "?") for v in anchors.values())
hm_count = by_conf.get("HIGH", 0) + by_conf.get("MEDIUM", 0)

# Recalculate coverage
hm_signs = {sid for sid, info in anchors.items()
            if info.get("confidence", "").upper() in ("HIGH", "MEDIUM")}
total_tokens = sum(corpus_freq.values())
covered_tokens = sum(corpus_freq[s] for s in hm_signs if s in corpus_freq)
coverage = round(covered_tokens / total_tokens, 4) if total_tokens > 0 else 0.0

fa["anchors"] = anchors
fa["total"] = hm_count
fa["corpus_token_coverage"] = coverage
fa["_cleanup_note"] = (
    f"Quality audit cleanup {now}: "
    f"removed {removed_phantom} phantom signs, "
    f"{removed_empty} empty readings, "
    f"downgraded {downgraded_dup} bulk-duplicate readings"
)

# Update metadata counts
fa["n_high"] = by_conf.get("HIGH", 0)
fa["n_medium"] = by_conf.get("MEDIUM", 0)
fa["n_low"] = by_conf.get("LOW", 0)
if "metadata" in fa:
    fa["metadata"]["total_count"] = hm_count
    fa["metadata"]["high_count"] = by_conf.get("HIGH", 0)
    fa["metadata"]["medium_count"] = by_conf.get("MEDIUM", 0)
    fa["metadata"]["low_count"] = by_conf.get("LOW", 0)

ANCHORS_PATH.write_text(json.dumps(fa, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"\n{'='*60}")
print(f"CLEANUP COMPLETE")
print(f"{'='*60}")
print(f"Before: {original_count} anchors")
print(f"After:  {len(anchors)} anchors")
print(f"  Removed: {removed_phantom + removed_empty} ({removed_phantom} phantom + {removed_empty} empty)")
print(f"  Downgraded: {downgraded_dup} bulk-duplicates → CANDIDATE")
print(f"  By confidence: {dict(by_conf)}")
print(f"  H+M total: {hm_count}")
print(f"  Coverage: {coverage*100:.1f}%")
print(f"\nBackup at: {BACKUP_PATH}")
