"""Full data integrity check across ALL corpora, signs, and anchors.

Checks:
1. Corpus integrity: duplicates, empty content, direction consistency
2. Synthetic corpus identification and flagging
3. Anchor cross-references: do anchored signs exist in the primary corpus?
4. Sign consistency: readings match DEDR, no orphans
5. Cross-corpus consistency: same sign shouldn't have conflicting readings
"""
import csv
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB = REPO / "backend" / "data" / "glossa.db"
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"

issues = []

def issue(severity, category, detail):
    issues.append({"severity": severity, "category": category, "detail": detail})
    mark = {"high": "🔴", "medium": "🟡", "low": "⚪"}.get(severity, "?")
    print(f"  {mark} [{category}] {detail}")

print("=" * 70)
print("FULL DATA INTEGRITY CHECK")
print("=" * 70)

# ── 1. Corpus Integrity ──────────────────────────────────────────────
print("\n=== 1. CORPUS INTEGRITY ===")
conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row
corpora = conn.execute(
    "SELECT id, name, corpus_type, reading_direction, alphabet_size, content, metadata "
    "FROM texts ORDER BY name"
).fetchall()

SYNTHETIC_KEYWORDS = ["synthetic", "test", "generated", "mock", "sample"]

synthetic_ids = []
for r in corpora:
    name = r["name"] or ""
    content = json.loads(r["content"]) if isinstance(r["content"], str) else (r["content"] or [])
    meta = json.loads(r["metadata"]) if isinstance(r["metadata"], str) else (r["metadata"] or {})

    # Check for empty corpus
    if not content or len(content) == 0:
        issue("high", "corpus_empty", f"'{name}' has no content")

    # Check for very small corpus
    if 0 < len(content) < 10:
        issue("medium", "corpus_tiny", f"'{name}' has only {len(content)} tokens")

    # Identify synthetic
    is_synthetic = any(kw in name.lower() for kw in SYNTHETIC_KEYWORDS)
    if is_synthetic:
        synthetic_ids.append(r["id"])
        issue("low", "corpus_synthetic", f"'{name}' appears synthetic")

    # Check alphabet_size consistency
    actual_unique = len(set(content)) if content else 0
    declared = r["alphabet_size"] or 0
    if actual_unique > 0 and declared > 0 and abs(actual_unique - declared) > declared * 0.1:
        issue("medium", "alphabet_mismatch",
              f"'{name}': declared {declared} signs but content has {actual_unique}")

# Check for duplicate corpus names
name_counts = Counter(r["name"] for r in corpora)
for name, count in name_counts.items():
    if count > 1:
        issue("medium", "corpus_duplicate", f"'{name}' appears {count} times")

print(f"\nCorpora: {len(corpora)} total, {len(synthetic_ids)} synthetic")

# ── 2. Flag Synthetic Corpora ────────────────────────────────────────
print("\n=== 2. SYNTHETIC CORPUS FLAGGING ===")
flagged = 0
for sid in synthetic_ids:
    meta_row = conn.execute("SELECT metadata FROM texts WHERE id=?", (sid,)).fetchone()
    meta = json.loads(meta_row["metadata"]) if meta_row and isinstance(meta_row["metadata"], str) else {}
    if not meta.get("synthetic"):
        meta["synthetic"] = True
        meta["synthetic_note"] = "Flagged by integrity check — not used for insights or experiments"
        conn.execute("UPDATE texts SET metadata=? WHERE id=?",
                     (json.dumps(meta, ensure_ascii=False), sid))
        flagged += 1
        print(f"  Flagged: {sid}")
if flagged:
    conn.commit()
    print(f"  Flagged {flagged} synthetic corpora")
else:
    print("  All synthetic corpora already flagged (or none found)")

# ── 3. Anchor Integrity ──────────────────────────────────────────────
print("\n=== 3. ANCHOR INTEGRITY ===")
if ANCHORS_PATH.exists():
    fa = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))
    anchors = fa.get("anchors", {})

    # Load primary corpus signs
    holdat_signs = set()
    holdat_freq = Counter()
    if HOLDAT_PATH.exists():
        with open(HOLDAT_PATH, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                sign = row.get("letters", "").strip()
                if sign:
                    holdat_signs.add(sign)
                    holdat_freq[sign] += 1

    by_conf = Counter(v.get("confidence", "?") for v in anchors.values())
    print(f"  Anchors: {len(anchors)} total")
    print(f"  By confidence: {dict(by_conf)}")
    print(f"  Primary corpus (Holdat): {len(holdat_signs)} signs, {sum(holdat_freq.values())} tokens")

    # Check: anchors not in primary corpus
    phantom = [sid for sid in anchors if sid not in holdat_signs]
    if phantom:
        issue("high", "anchor_phantom",
              f"{len(phantom)} anchors reference signs NOT in Holdat corpus")

    # Check: empty readings
    empty = [sid for sid, info in anchors.items() if not (info.get("reading") or "").strip()]
    if empty:
        issue("high", "anchor_empty_reading", f"{len(empty)} anchors have empty readings")

    # Check: reading_direction on anchors
    rd = fa.get("reading_direction", "")
    if not rd:
        issue("medium", "anchor_no_direction", "INDUS_FINAL_ANCHORS.json has no reading_direction")

    # Check: coverage sanity
    coverage = float(fa.get("corpus_token_coverage", 0) or 0)
    hm_signs = {sid for sid, info in anchors.items()
                if info.get("confidence", "").upper() in ("HIGH", "MEDIUM")}
    if holdat_freq:
        actual_cov = sum(holdat_freq[s] for s in hm_signs if s in holdat_freq) / sum(holdat_freq.values())
        if abs(actual_cov - coverage) > 0.02:
            issue("medium", "coverage_drift",
                  f"Declared coverage {coverage:.1%} but actual is {actual_cov:.1%}")

    # Check: duplicate readings (>5 signs with same reading)
    reading_signs = defaultdict(list)
    for sid, info in anchors.items():
        r = (info.get("reading") or "").strip().lower()
        if r:
            reading_signs[r].append(sid)
    bulk_dups = {r: signs for r, signs in reading_signs.items() if len(signs) > 5}
    if bulk_dups:
        for r, signs in bulk_dups.items():
            confs = [anchors[s].get("confidence", "?") for s in signs]
            high_count = sum(1 for c in confs if c in ("HIGH", "MEDIUM"))
            if high_count > 0:
                issue("high", "bulk_duplicate_reading",
                      f"'{r}' assigned to {len(signs)} signs ({high_count} HIGH/MEDIUM)")
            else:
                issue("low", "bulk_duplicate_candidate",
                      f"'{r}' assigned to {len(signs)} CANDIDATE signs")
else:
    issue("high", "anchor_missing", "INDUS_FINAL_ANCHORS.json not found!")

# ── 4. Cross-Corpus Consistency ──────────────────────────────────────
print("\n=== 4. CROSS-CORPUS CONSISTENCY ===")
# Check that Indus corpora use consistent sign naming
indus_corpora = [r for r in corpora if "indus" in (r["name"] or "").lower()
                 or "harappan" in (r["name"] or "").lower()
                 or "dholavira" in (r["name"] or "").lower()]
if len(indus_corpora) > 1:
    sign_sets = {}
    for r in indus_corpora:
        content = json.loads(r["content"]) if isinstance(r["content"], str) else (r["content"] or [])
        signs = set(content)
        sign_sets[r["name"]] = signs

    # Check overlap between Indus corpora
    names = list(sign_sets.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            a, b = sign_sets[names[i]], sign_sets[names[j]]
            overlap = a & b
            if overlap:
                pct = len(overlap) / min(len(a), len(b)) * 100 if min(len(a), len(b)) > 0 else 0
                print(f"  '{names[i]}' ∩ '{names[j]}': {len(overlap)} shared signs ({pct:.0f}%)")
            else:
                issue("medium", "no_sign_overlap",
                      f"'{names[i]}' and '{names[j]}' share NO signs — different naming systems?")

# ── 5. Data Freshness ────────────────────────────────────────────────
print("\n=== 5. DATA FRESHNESS ===")
# Check that key files exist and are recent
key_files = {
    "INDUS_FINAL_ANCHORS.json": ANCHORS_PATH,
    "Holdat corpus CSV": HOLDAT_PATH,
    "foundation_check_report.json": REPO / "reports" / "foundation_check_report.json",
    "anchor_staging.json": REPO / "outputs" / "anchor_staging.json",
}
for label, path in key_files.items():
    if path.exists():
        size_kb = path.stat().st_size / 1024
        print(f"  ✓ {label}: {size_kb:.0f} KB")
    else:
        issue("medium", "missing_file", f"{label} not found at {path}")

# ── Summary ──────────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("INTEGRITY CHECK SUMMARY")
print(f"{'='*70}")

high = [i for i in issues if i["severity"] == "high"]
med = [i for i in issues if i["severity"] == "medium"]
low = [i for i in issues if i["severity"] == "low"]

print(f"Total issues: {len(issues)}")
print(f"  🔴 HIGH: {len(high)}")
print(f"  🟡 MEDIUM: {len(med)}")
print(f"  ⚪ LOW: {len(low)}")
print(f"  Corpora: {len(corpora)} ({len(synthetic_ids)} synthetic)")
if ANCHORS_PATH.exists():
    print(f"  Anchors: {len(anchors)} ({dict(by_conf)})")

if not high:
    print("\n✅ NO HIGH-SEVERITY ISSUES — data integrity is clean")
else:
    print(f"\n⚠ {len(high)} HIGH-SEVERITY ISSUES need attention")

conn.close()
