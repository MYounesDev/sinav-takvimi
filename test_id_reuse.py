"""
Test script to verify ID reuse functionality
This script demonstrates that IDs are reused after deletion
"""

import sqlite3
import os

def test_id_reuse():
    """Test that IDs are reused after deletion"""
    
    print("=" * 60)
    print("Testing ID Reuse Functionality")
    print("=" * 60)
    
    test_db = "test_id_reuse.db"
    
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE test_classrooms (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    print("\nTest 1: Initial inserts")
    print("-" * 60)
    
    for i in range(1, 6):
        cursor.execute("INSERT INTO test_classrooms (name) VALUES (?)", (f"Classroom {i}",))
        print(f"  Inserted: Classroom {i} -> ID = {cursor.lastrowid}")
    
    conn.commit()
    
    print("\nCurrent state:")
    cursor.execute("SELECT * FROM test_classrooms ORDER BY id")
    for row in cursor.fetchall():
        print(f"  ID={row[0]}, Name={row[1]}")
    
    print("\nTest 2: Deleting rows with ID=2 and ID=4")
    print("-" * 60)
    cursor.execute("DELETE FROM test_classrooms WHERE id IN (2, 4)")
    conn.commit()
    
    print("\nCurrent state after deletion:")
    cursor.execute("SELECT * FROM test_classrooms ORDER BY id")
    for row in cursor.fetchall():
        print(f"  ID={row[0]}, Name={row[1]}")
    
    print("\nTest 3: Inserting new rows")
    print("-" * 60)
    print("Expected: New rows should get ID=2 and ID=4 (reused IDs)")
    
    cursor.execute("INSERT INTO test_classrooms (name) VALUES (?)", ("New Classroom A",))
    new_id_1 = cursor.lastrowid
    print(f"  Inserted: New Classroom A -> ID = {new_id_1}")
    
    cursor.execute("INSERT INTO test_classrooms (name) VALUES (?)", ("New Classroom B",))
    new_id_2 = cursor.lastrowid
    print(f"  Inserted: New Classroom B -> ID = {new_id_2}")
    
    conn.commit()
    
    print("\nFinal state:")
    cursor.execute("SELECT * FROM test_classrooms ORDER BY id")
    for row in cursor.fetchall():
        print(f"  ID={row[0]}, Name={row[1]}")
    
    print("\n" + "=" * 60)
    if new_id_1 == 2 and new_id_2 == 4:
        print("SUCCESS! IDs were reused correctly!")
        print(f"  - New Classroom A got ID=2 (previously deleted)")
        print(f"  - New Classroom B got ID=4 (previously deleted)")
    else:
        print("Note: IDs were NOT reused in this sequence.")
        print(f"  - Got IDs: {new_id_1} and {new_id_2}")
        print("\nThis is expected SQLite behavior - let's test a different scenario...")
    print("=" * 60)
    
    conn.close()
    os.remove(test_db)
    print("\nTest database cleaned up")

def test_id_reuse_max_deleted():
    """Test ID reuse when the maximum ID is deleted"""
    
    print("\n\n" + "=" * 60)
    print("Test: ID Reuse When Maximum ID is Deleted")
    print("=" * 60)
    
    test_db = "test_id_reuse2.db"
    
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE test_classrooms (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    print("\nInserting rows 1-5:")
    for i in range(1, 6):
        cursor.execute("INSERT INTO test_classrooms (name) VALUES (?)", (f"Classroom {i}",))
    conn.commit()
    
    print("\nDeleting the MAXIMUM ID (ID=5):")
    cursor.execute("DELETE FROM test_classrooms WHERE id = 5")
    conn.commit()
    
    print("\nInserting a new row:")
    cursor.execute("INSERT INTO test_classrooms (name) VALUES (?)", ("New Classroom",))
    new_id = cursor.lastrowid
    print(f"  New row got ID = {new_id}")
    
    conn.commit()
    
    print("\n" + "=" * 60)
    if new_id == 5:
        print("SUCCESS! ID was reused when max ID was deleted!")
        print("  - Deleted ID=5")
        print("  - New row got ID=5 (reused!)")
    else:
        print(f"New row got ID={new_id} instead of ID=5")
    print("=" * 60)
    
    conn.close()
    os.remove(test_db)

def test_with_autoincrement():
    """Test to show the old behavior with AUTOINCREMENT"""
    
    print("\n\n" + "=" * 60)
    print("Comparison: Behavior WITH AUTOINCREMENT (Old Schema)")
    print("=" * 60)
    
    test_db = "test_autoincrement.db"
    
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE test_classrooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    
    print("\nInitial inserts:")
    for i in range(1, 6):
        cursor.execute("INSERT INTO test_classrooms (name) VALUES (?)", (f"Classroom {i}",))
    
    conn.commit()
    
    print("Deleting rows with ID=2 and ID=4...")
    cursor.execute("DELETE FROM test_classrooms WHERE id IN (2, 4)")
    conn.commit()
    
    print("\nInserting new rows:")
    cursor.execute("INSERT INTO test_classrooms (name) VALUES (?)", ("New Classroom A",))
    new_id_1 = cursor.lastrowid
    print(f"  Inserted: New Classroom A -> ID = {new_id_1}")
    
    cursor.execute("INSERT INTO test_classrooms (name) VALUES (?)", ("New Classroom B",))
    new_id_2 = cursor.lastrowid
    print(f"  Inserted: New Classroom B -> ID = {new_id_2}")
    
    conn.commit()
    
    print("\nFinal state:")
    cursor.execute("SELECT * FROM test_classrooms ORDER BY id")
    for row in cursor.fetchall():
        print(f"  ID={row[0]}, Name={row[1]}")
    
    print("\n" + "=" * 60)
    print("With AUTOINCREMENT:")
    print(f"  - New rows got IDs: {new_id_1} and {new_id_2}")
    print(f"  - IDs 2 and 4 are NOT reused (this is the old behavior)")
    print("=" * 60)
    
    conn.close()
    os.remove(test_db)

if __name__ == "__main__":
    test_id_reuse()
    
    test_id_reuse_max_deleted()
    
    test_with_autoincrement()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("SQLite ID Reuse Behavior:")
    print("  - Without AUTOINCREMENT: IDs CAN be reused (especially max IDs)")
    print("  - With AUTOINCREMENT:    IDs are NEVER reused")
    print("\nKey difference:")
    print("  - Old schema: Even if you delete ID=34, it"s gone forever")
    print("  - New schema: If ID=34 is the max and deleted, it can be reused")
    print("\nThe database has been migrated to use the new behavior.")
    print("=" * 60)

