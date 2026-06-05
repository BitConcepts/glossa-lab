import sqlite3, json

conn = sqlite3.connect(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\data\glossa.db", timeout=3)
conn.row_factory = sqlite3.Row
row = conn.execute("SELECT params FROM jobs WHERE id LIKE '1f653368%'").fetchone()
if row:
    p = json.loads(row["params"])
    print(json.dumps(p, indent=2))
else:
    print("Job not found")

# Also check research_loop_state table
try:
    state = conn.execute("SELECT * FROM research_loop_state ORDER BY rowid DESC LIMIT 1").fetchone()
    if state:
        print("\n--- research_loop_state ---")
        for k in state.keys():
            val = str(state[k])[:200]
            print(f"  {k}: {val}")
except Exception as e:
    print(f"No research_loop_state: {e}")

conn.close()
