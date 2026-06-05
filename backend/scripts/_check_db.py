import sqlite3
from pathlib import Path

db_path = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\data\glossa.db")
print(f"DB exists: {db_path.exists()}")
conn = sqlite3.connect(str(db_path), timeout=3)
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f"Tables: {[t[0] for t in tables]}")
cols = conn.execute("PRAGMA table_info(jobs)").fetchall()
print(f"Jobs columns: {[c[1] for c in cols]}")
# Sample a job row
row = conn.execute("SELECT id, status, params FROM jobs LIMIT 1").fetchone()
if row:
    print(f"Sample job: id={row[0]}, status={row[1]}, params_type={type(row[2])}")
    print(f"  params preview: {str(row[2])[:200]}")
conn.close()
