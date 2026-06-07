"""Check all corpus reading directions for contradictions and errors."""
import sqlite3
import json
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "data" / "glossa.db"
conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row

rows = conn.execute(
    "SELECT id, name, corpus_type, reading_direction, alphabet_size, content "
    "FROM texts ORDER BY name"
).fetchall()

# Known correct directions from linguistics
KNOWN_DIRECTIONS = {
    "ge'ez": "ltr",      # Ge'ez/Ethiopic is LEFT-TO-RIGHT
    "geez": "ltr",       # Ge'ez/Ethiopic is LEFT-TO-RIGHT
    "ethiopic": "ltr",   # Ge'ez/Ethiopic is LEFT-TO-RIGHT
    "ugaritic": "ltr",   # Ugaritic cuneiform is LEFT-TO-RIGHT
    "sumerian": "ltr",   # Cuneiform is LEFT-TO-RIGHT
    "coptic": "ltr",     # Coptic is LEFT-TO-RIGHT (Greek-derived)
    "linear b": "ltr",   # Linear B is LEFT-TO-RIGHT
    "hebrew": "rtl",     # Hebrew is RIGHT-TO-LEFT
    "proto-sinaitic": "rtl",  # Proto-Sinaitic is RIGHT-TO-LEFT
    "nw semitic": "rtl", # NW Semitic abjads are RIGHT-TO-LEFT
    "old hebrew": "rtl", # Old Hebrew is RIGHT-TO-LEFT
}

print(f"{'ID':12} {'Dir':8} {'Correct?':9} {'Alpha':5} Name")
print("=" * 90)

issues = []
for r in rows:
    rid = r["id"]
    name = r["name"] or ""
    direction = r["reading_direction"] or "unknown"
    alpha = r["alphabet_size"] or 0
    
    # Determine expected direction
    expected = None
    matched_key = None
    for key, exp_dir in KNOWN_DIRECTIONS.items():
        if key in name.lower():
            expected = exp_dir
            matched_key = key
            break
    
    # Check
    if expected and direction != "unknown":
        if direction == expected:
            status = "✓"
        else:
            status = f"✗ WRONG (should be {expected})"
            issues.append((rid, name, direction, expected, matched_key))
    elif direction == "unknown":
        status = "— (unset)"
    else:
        status = f"~ ({direction})"
    
    print(f"{rid:12} {direction:8} {status:20} {alpha:5} {name[:50]}")

# Check for duplicate corpus names with different directions
name_dirs = {}
for r in rows:
    name = (r["name"] or "").strip()
    direction = r["reading_direction"] or "unknown"
    if name in name_dirs:
        if name_dirs[name] != direction:
            issues.append((r["id"], name, direction, name_dirs[name], "DUPLICATE_CONFLICT"))
            print(f"\n⚠ CONFLICT: '{name}' has both {name_dirs[name]} and {direction}")
    else:
        name_dirs[name] = direction

print(f"\n{'='*90}")
print(f"Total corpora: {len(rows)}")
print(f"Issues found: {len(issues)}")

if issues:
    print("\n🔴 ISSUES TO FIX:")
    for rid, name, current, expected, key in issues:
        print(f"  {rid}: '{name[:40]}' is {current}, should be {expected} (matched: {key})")

conn.close()
