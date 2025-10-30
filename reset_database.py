"""
Database Reset Script - Reset database with new design
This script completely resets the database while keeping the new design
(display_id system and CASCADE DELETE)
"""

import os
import shutil
from datetime import datetime
from config import DATABASE_PATH

def clear_all_data():
    """Clear all data from existing database by recreating tables"""
    import sqlite3
    
    print("\n" + "=" * 70)
    print("CLEARING ALL DATA (Alternative Method)")
    print("=" * 70)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        conn.execute("PRAGMA foreign_keys = OFF")
        
        tables = ['exam_seating', 'exam_classrooms', 'exams', 'student_courses', 
                  'students', 'courses', 'classrooms', 'users', 'departments', 'deleted_ids']
        
        print("\nDropping all tables...")
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"  ✓ Dropped {table}")
        
        conn.commit()
        conn.close()
        
        print("\n✓ All tables dropped!")
        print("=" * 70)
        print("\nNow initializing fresh database with new design...")
        
        from src.database.db_manager import db_manager
        db_manager.initialize_database()
        
        print("\n" + "=" * 70)
        print("✓ DATABASE RESET COMPLETED!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        conn.rollback()
        conn.close()
        raise

def reset_database():
    """Completely reset the database"""
    
    print("=" * 70)
    print("DATABASE RESET")
    print("=" * 70)
    
    if not os.path.exists(DATABASE_PATH):
        print("\n✓ No existing database found. Will create fresh database.")
        return
    
    backup_path = DATABASE_PATH.replace('.db', f'_before_reset_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
    try:
        shutil.copy2(DATABASE_PATH, backup_path)
        print(f"\n✓ Database backed up to: {backup_path}")
    except Exception as e:
        print(f"\n⚠ Could not create backup: {e}")
    
    try:
        os.remove(DATABASE_PATH)
        print(f"✓ Database deleted: {DATABASE_PATH}")
        
        print("\n" + "=" * 70)
        print("✓ DATABASE RESET COMPLETED!")
        print("=" * 70)
        print("\nThe database has been completely reset.")
        print("When you run the application, a new database will be created")
        print("with the new design (display_id + CASCADE DELETE).")
        print("\nDefault users will be created:")
        print("  - Admin: admin@gmail.com / admin123")
        print("  - Coordinators for each department / admin123")
    except PermissionError:
        print(f"\n⚠ Could not delete database (file is in use)")
        print(f"\nPlease follow these steps:")
        print("1. Close any programs using the database (VS Code, Python processes, etc.)")
        print("2. Manually delete the file: {DATABASE_PATH}")
        print("3. Or rename it to something else")
        print("\nAlternatively, use the 'Clear All Data' option below:")
        clear_all_data()

if __name__ == "__main__":
    try:
        response = input("\n⚠️  WARNING: This will DELETE the entire database!\n"
                        "All data will be lost (a backup will be created).\n"
                        "Are you sure? (yes/no): ")
        
        if response.lower() in ['yes', 'y', 'evet', 'e']:
            reset_database()
            print("\n✓ Next step: Run 'python main.py' to create fresh database")
        else:
            print("\n✗ Operation cancelled.")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
