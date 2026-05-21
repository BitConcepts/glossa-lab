import sqlite3
conn = sqlite3.connect("data/glossa.db")
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
print("Tables:", tables)
version = conn.execute("SELECT version FROM _schema_version").fetchone()
print("Schema version:", version)
conn.close()
