"""
Add isActive column to courses table
"""

import sqlite3
from config import DATABASE_PATH
from datetime import datetime

def add_isactive_column():
    """Add isActive column to courses table"""
    
    print("=" * 70)
    print("ADD isActive COLUMN TO COURSES TABLE")
    print("=" * 70)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(courses)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'isActive' in columns:
            print("✓ isActive column already exists in courses table")
            return
        
        print("\nAdding isActive column...")
        
        cursor.execute("""
            ALTER TABLE courses 
            ADD COLUMN isActive INTEGER DEFAULT 1
        """)
        
        cursor.execute("UPDATE courses SET isActive = 1")
        
        conn.commit()
        
        print("✓ isActive column added successfully")
        print("✓ All existing courses set to active (isActive = 1)")
        
        cursor.execute("SELECT COUNT(*) FROM courses WHERE isActive = 1")
        count = cursor.fetchone()[0]
        print(f"✓ {count} active courses in database")
        
        print("\n" + "=" * 70)
        print("✓ MIGRATION COMPLETED!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        add_isactive_column()
        print("\nYou can now mark courses as inactive in the Courses view.")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
