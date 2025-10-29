"""
Database Migration Script - Migrate to display_id support
This script migrates the existing database to use display_id fields
while maintaining CASCADE DELETE functionality.

IMPORTANT: Run this script ONLY ONCE to migrate existing database!
"""

import sqlite3
import os
import shutil
from datetime import datetime
from config import DATABASE_PATH


def backup_database():
    """Create a backup of the current database"""
    if not os.path.exists(DATABASE_PATH):
        print("No existing database found. Starting fresh.")
        return False
    
    backup_path = DATABASE_PATH.replace('.db', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
    shutil.copy2(DATABASE_PATH, backup_path)
    print(f"✓ Database backed up to: {backup_path}")
    return True


def migrate_database():
    """Migrate existing database to new schema with display_id"""
    
    print("=" * 70)
    print("DATABASE MIGRATION - Adding display_id Support")
    print("=" * 70)
    
    # Backup first
    has_existing = backup_database()
    
    if not has_existing:
        print("\nNo migration needed. Database will be created with new schema.")
        return
    
    print("\nStarting migration process...")
    print("-" * 70)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = OFF")  # Disable temporarily for migration
    cursor = conn.cursor()
    
    try:
        # Step 1: Create deleted_ids table
        print("\n[1/9] Creating deleted_ids tracking table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deleted_ids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                display_id INTEGER NOT NULL,
                deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(table_name, display_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_deleted_ids_table ON deleted_ids(table_name, display_id)")
        print("  ✓ deleted_ids table created")
        
        # Step 2: Migrate departments table
        print("\n[2/9] Migrating departments table...")
        cursor.execute("PRAGMA table_info(departments)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'display_id' not in columns:
            cursor.execute("ALTER TABLE departments ADD COLUMN display_id INTEGER")
            # Set display_id = id for existing records
            cursor.execute("UPDATE departments SET display_id = id WHERE display_id IS NULL")
            print("  ✓ Added display_id to departments")
        else:
            print("  ✓ display_id already exists in departments")
        
        # Step 3: Migrate users table
        print("\n[3/9] Migrating users table...")
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'display_id' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN display_id INTEGER")
            cursor.execute("UPDATE users SET display_id = id WHERE display_id IS NULL")
            print("  ✓ Added display_id to users")
        else:
            print("  ✓ display_id already exists in users")
        
        # Step 4: Migrate classrooms table
        print("\n[4/9] Migrating classrooms table...")
        cursor.execute("PRAGMA table_info(classrooms)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'display_id' not in columns:
            cursor.execute("ALTER TABLE classrooms ADD COLUMN display_id INTEGER")
            # For department-scoped tables, reset numbering per department
            cursor.execute("""
                WITH numbered AS (
                    SELECT id, department_id,
                           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY id) as row_num
                    FROM classrooms
                )
                UPDATE classrooms
                SET display_id = (
                    SELECT row_num FROM numbered WHERE numbered.id = classrooms.id
                )
                WHERE display_id IS NULL
            """)
            print("  ✓ Added display_id to classrooms (per department)")
        else:
            print("  ✓ display_id already exists in classrooms")
        
        # Step 5: Migrate courses table
        print("\n[5/9] Migrating courses table...")
        cursor.execute("PRAGMA table_info(courses)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'display_id' not in columns:
            cursor.execute("ALTER TABLE courses ADD COLUMN display_id INTEGER")
            cursor.execute("""
                WITH numbered AS (
                    SELECT id, department_id,
                           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY id) as row_num
                    FROM courses
                )
                UPDATE courses
                SET display_id = (
                    SELECT row_num FROM numbered WHERE numbered.id = courses.id
                )
                WHERE display_id IS NULL
            """)
            print("  ✓ Added display_id to courses (per department)")
        else:
            print("  ✓ display_id already exists in courses")
        
        # Step 6: Migrate students table
        print("\n[6/9] Migrating students table...")
        cursor.execute("PRAGMA table_info(students)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'display_id' not in columns:
            cursor.execute("ALTER TABLE students ADD COLUMN display_id INTEGER")
            cursor.execute("""
                WITH numbered AS (
                    SELECT id, department_id,
                           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY id) as row_num
                    FROM students
                )
                UPDATE students
                SET display_id = (
                    SELECT row_num FROM numbered WHERE numbered.id = students.id
                )
                WHERE display_id IS NULL
            """)
            print("  ✓ Added display_id to students (per department)")
        else:
            print("  ✓ display_id already exists in students")
        
        # Step 7: Migrate exams table
        print("\n[7/9] Migrating exams table...")
        cursor.execute("PRAGMA table_info(exams)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'display_id' not in columns:
            cursor.execute("ALTER TABLE exams ADD COLUMN display_id INTEGER")
            cursor.execute("""
                WITH numbered AS (
                    SELECT id, department_id,
                           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY id) as row_num
                    FROM exams
                )
                UPDATE exams
                SET display_id = (
                    SELECT row_num FROM numbered WHERE numbered.id = exams.id
                )
                WHERE display_id IS NULL
            """)
            print("  ✓ Added display_id to exams (per department)")
        else:
            print("  ✓ display_id already exists in exams")
        
        # Step 8: Create triggers
        print("\n[8/9] Creating triggers for display_id recycling...")
        
        triggers = [
            ("before_delete_department", "departments"),
            ("before_delete_user", "users"),
            ("before_delete_classroom", "classrooms"),
            ("before_delete_course", "courses"),
            ("before_delete_student", "students"),
            ("before_delete_exam", "exams"),
        ]
        
        for trigger_name, table_name in triggers:
            cursor.execute(f"""
                CREATE TRIGGER IF NOT EXISTS {trigger_name}
                BEFORE DELETE ON {table_name}
                BEGIN
                    INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
                    VALUES ('{table_name}', OLD.display_id);
                END
            """)
        print("  ✓ All triggers created")
        
        # Step 9: Create indexes
        print("\n[9/9] Creating indexes for display_id columns...")
        indexes = [
            ("idx_users_display_id", "users", "display_id"),
            ("idx_students_display_id", "students", "display_id"),
            ("idx_courses_display_id", "courses", "display_id"),
            ("idx_classrooms_display_id", "classrooms", "display_id"),
            ("idx_departments_display_id", "departments", "display_id"),
            ("idx_exams_display_id", "exams", "display_id"),
        ]
        
        for idx_name, table_name, column in indexes:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table_name}({column})")
        print("  ✓ All indexes created")
        
        # Commit all changes
        conn.commit()
        
        # Re-enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        
        print("\n" + "=" * 70)
        print("✓ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nSummary:")
        print("  - display_id added to all main tables")
        print("  - Triggers created for automatic ID recycling")
        print("  - Indexes created for performance")
        print("  - CASCADE DELETE already configured")
        print("\nNext steps:")
        print("  1. Replace src/database/db_manager.py with db_manager_new.py")
        print("  2. Update UI views to use display_id instead of id")
        print("  3. Run tests to verify functionality")
        
    except Exception as e:
        print(f"\n✗ ERROR during migration: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()


def verify_migration():
    """Verify that migration was successful"""
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        tables_to_check = ['departments', 'users', 'classrooms', 'courses', 'students', 'exams']
        
        print("\nChecking display_id columns:")
        for table in tables_to_check:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            has_display_id = 'display_id' in columns
            status = "✓" if has_display_id else "✗"
            print(f"  {status} {table}: {'display_id found' if has_display_id else 'MISSING display_id'}")
        
        print("\nChecking triggers:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'before_delete_%'")
        triggers = cursor.fetchall()
        print(f"  ✓ Found {len(triggers)} triggers:")
        for trigger in triggers:
            print(f"    - {trigger[0]}")
        
        print("\nChecking deleted_ids table:")
        cursor.execute("SELECT COUNT(*) FROM deleted_ids")
        count = cursor.fetchone()[0]
        print(f"  ✓ deleted_ids table exists with {count} entries")
        
        print("\nSample data with display_id:")
        cursor.execute("SELECT id, display_id, name FROM departments LIMIT 3")
        depts = cursor.fetchall()
        if depts:
            print("  Departments:")
            for dept in depts:
                print(f"    - id={dept['id']}, display_id={dept['display_id']}, name={dept['name']}")
        
    except Exception as e:
        print(f"\n✗ Verification error: {str(e)}")
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        migrate_database()
        verify_migration()
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
