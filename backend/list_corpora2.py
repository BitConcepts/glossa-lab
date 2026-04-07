"""List corpora non-blocking."""
import sqlite3, json
conn = sqlite3.connect("data/glossa.db")
rows = conn.execute("SELECT id, name, corpus_type, content FROM texts ORDER BY created_at DESC").fetchall()
print(f"\n{'ID':12} {'Tokens':>8} {'Type':12} Name")
print("-"*70)
for r in rows:
    tokens = json.loads(r[3]) if r[3].startswith('[') else r[3].split()
    print(f"{r[0]:12} {len(tokens):>8} {r[2]:12} {r[1][:40]}")
print(f"\nTotal: {len(rows)} corpora")
conn.close()
