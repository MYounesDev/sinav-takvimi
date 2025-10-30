"""
Check database schema and foreign key constraints
"""

import sqlite3
from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 70)
print("DATABASE SCHEMA ANALYSIS")
print("=" * 70)

cursor.execute("PRAGMA foreign_keys")
result = cursor.fetchone()
print(f"\nForeign Keys: {'ENABLED' if result[0] else 'DISABLED'}")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print(f"\nTables found: {len(tables)}")
print("-" * 70)

for table in tables:
    table_name = table['name']
    
    if table_name.startswith('sqlite_'):
        continue
    
    print(f"\n{table_name}")
    print("  Foreign Keys:")
    
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    fks = cursor.fetchall()
    
    if fks:
        for fk in fks:
            print(f"    - {fk['from']} → {fk['table']}.{fk['to']} "
                  f"(ON DELETE: {fk['on_delete']}, ON UPDATE: {fk['on_update']})")
    else:
        print("    - None")

conn.close()
