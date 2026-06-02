"""
Run this to verify the Oracle 23ai connection.
Usage: python vector_db/test_connection.py   (from db-agent/)
"""
import oracledb
import os

# --- connection details ---
USER     = os.getenv("VECTOR_DB_USER", "")
PASSWORD = os.getenv("VECTOR_DB_PASSWORD", "")
DSN      = os.getenv("VECTOR_DB_DSN", "")

# thick mode required for this Oracle 23ai server
oracledb.init_oracle_client()

print("Connecting to Oracle 23ai...")
conn = oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)
print(f"Connected. Oracle version: {conn.version}")

cur = conn.cursor()

# show tables owned by mldsdev
cur.execute("SELECT table_name FROM user_tables ORDER BY table_name")
tables = cur.fetchall()
if tables:
    print("\nTables in mldsdev schema:")
    for (t,) in tables:
        print(f"  - {t}")
else:
    print("\nNo tables found in mldsdev schema yet.")

cur.close()
conn.close()
print("\nDone.")
