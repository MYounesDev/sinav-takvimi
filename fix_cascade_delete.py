"""
Fix CASCADE DELETE - Recreate tables with proper constraints
This script fixes the CASCADE DELETE issue by recreating tables with ON DELETE CASCADE
"""

import sqlite3
import os
import shutil
from datetime import datetime
from config import DATABASE_PATH

def backup_database():
    """Create a backup of the current database"""
    backup_path = DATABASE_PATH.replace(".db", f"_before_cascade_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db")
    shutil.copy2(DATABASE_PATH, backup_path)
    print(f"✓ Database backed up to: {backup_path}")
    return backup_path

def fix_cascade_delete():
    """Fix CASCADE DELETE by recreating tables"""
    
    print("=" * 70)
    print("FIX CASCADE DELETE CONSTRAINTS")
    print("=" * 70)
    
    backup_path = backup_database()
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    conn.execute("PRAGMA foreign_keys = OFF")
    
    try:
        print("\nStep 1: Backing up all data...")
        
        tables_data = {}
        
        tables = ["departments", "users", "classrooms", "courses", "students", 
                  "student_courses", "exams", "exam_classrooms", "exam_seating", "deleted_ids"]
        
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            tables_data[table] = cursor.fetchall()
            print(f"  ✓ Backed up {table}: {len(tables_data[table])} rows")
        
        print("\nStep 2: Dropping old tables...")
        for table in reversed(tables):  # Drop in reverse order to avoid FK issues
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"  ✓ Dropped {table}")
        
        print("\nStep 3: Creating new tables with CASCADE DELETE...")
        
        cursor.execute("""
            CREATE TABLE deleted_ids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                display_id INTEGER NOT NULL,
                deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(table_name, display_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ("admin", "coordinator")),
                department_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE classrooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                department_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                rows INTEGER NOT NULL,
                cols INTEGER NOT NULL,
                seats_per_desk INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
                UNIQUE(department_id, code)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                department_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                instructor TEXT,
                class_level INTEGER,
                type TEXT CHECK(type IN ("mandatory", "elective")),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
                UNIQUE(department_id, code)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                department_id INTEGER NOT NULL,
                student_no TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                class_level INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE student_courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE(student_id, course_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                course_id INTEGER NOT NULL,
                department_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                duration INTEGER NOT NULL,
                exam_type TEXT DEFAULT "final",
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE exam_classrooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id INTEGER NOT NULL,
                classroom_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
                FOREIGN KEY (classroom_id) REFERENCES classrooms(id) ON DELETE CASCADE,
                UNIQUE(exam_id, classroom_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE exam_seating (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                exam_id INTEGER NOT NULL,
                classroom_id INTEGER NOT NULL,
                row INTEGER NOT NULL,
                col INTEGER NOT NULL,
                seat_position INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (classroom_id) REFERENCES classrooms(id) ON DELETE CASCADE,
                UNIQUE(exam_id, student_id)
            )
        """)
        
        print("  ✓ All tables created with CASCADE DELETE")
        
        print("\nStep 4: Creating indexes...")
        indexes = [
            ("idx_users_email", "users", "email"),
            ("idx_users_display_id", "users", "display_id"),
            ("idx_students_no", "students", "student_no"),
            ("idx_students_display_id", "students", "display_id"),
            ("idx_courses_code", "courses", "code"),
            ("idx_courses_display_id", "courses", "display_id"),
            ("idx_classrooms_display_id", "classrooms", "display_id"),
            ("idx_departments_display_id", "departments", "display_id"),
            ("idx_exams_date", "exams", "date"),
            ("idx_exams_display_id", "exams", "display_id"),
            ("idx_deleted_ids_table", "deleted_ids", "(table_name, display_id)"),
        ]
        
        for idx_name, table_name, column in indexes:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table_name}{column if column.startswith("(") else f"({column})"}")
        print("  ✓ All indexes created")
        
        print("\nStep 5: Creating triggers...")
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
                CREATE TRIGGER {trigger_name}
                BEFORE DELETE ON {table_name}
                BEGIN
                    INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
                    VALUES ("{table_name}", OLD.display_id);
                END
            """)
        print("  ✓ All triggers created")
        
        print("\nStep 6: Restoring data...")
        
        restore_order = ["departments", "users", "classrooms", "courses", "students", 
                        "student_courses", "exams", "exam_classrooms", "exam_seating", "deleted_ids"]
        
        for table in restore_order:
            if table in tables_data and tables_data[table]:
                first_row = tables_data[table][0]
                columns = list(first_row.keys())
                placeholders = ",".join(["?" for _ in columns])
                columns_str = ",".join(columns)
                
                for row in tables_data[table]:
                    values = tuple(row[col] for col in columns)
                    cursor.execute(f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})", values)
                
                print(f"  ✓ Restored {table}: {len(tables_data[table])} rows")
        
        conn.commit()
        
        conn.execute("PRAGMA foreign_keys = ON")
        
        print("\n" + "=" * 70)
        print("✓ CASCADE DELETE FIX COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nAll tables have been recreated with ON DELETE CASCADE.")
        print("Foreign keys are now properly configured.")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        conn.rollback()
        print(f"\nRestoring from backup: {backup_path}")
        conn.close()
        shutil.copy2(backup_path, DATABASE_PATH)
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        fix_cascade_delete()
        print("\nRun test_comprehensive.py again to verify the fix.")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
