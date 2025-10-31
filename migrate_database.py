"""
Database Migration Script - Remove AUTOINCREMENT to allow ID reuse
This script migrates the database schema to allow reusing IDs from deleted rows.
"""

import sqlite3
import os
from config import DATABASE_PATH

def backup_database():
    """Create a backup of the current database"""
    if os.path.exists(DATABASE_PATH):
        backup_path = DATABASE_PATH.replace(".db", "_backup.db")
        import shutil
        shutil.copy2(DATABASE_PATH, backup_path)
        print(f"✓ Database backup created: {backup_path}")
        return True
    return False

def migrate_table(cursor, table_name, create_sql, columns):
    """
    Migrate a table by recreating it without AUTOINCREMENT
    
    Args:
        cursor: Database cursor
        table_name: Name of the table to migrate
        create_sql: SQL to create the new table
        columns: List of column names to copy
    """
    print(f"\nMigrating table: {table_name}")
    
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}"")
    if not cursor.fetchone():
        print(f"  Table {table_name} does not exist, skipping...")
        return
    
    temp_table = f"{table_name}_new"
    cursor.execute(create_sql.replace(f"CREATE TABLE IF NOT EXISTS {table_name}", 
                                     f"CREATE TABLE {temp_table}"))
    print(f"  ✓ Created temporary table: {temp_table}")
    
    columns_str = ", ".join(columns)
    cursor.execute(f"INSERT INTO {temp_table} ({columns_str}) SELECT {columns_str} FROM {table_name}")
    print(f"  ✓ Copied {cursor.rowcount} rows")
    
    cursor.execute(f"DROP TABLE {table_name}")
    print(f"  ✓ Dropped old table")
    
    cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
    print(f"  ✓ Renamed table")

def migrate_database():
    """Migrate the database schema"""
    print("=" * 60)
    print("DATABASE MIGRATION: Enabling ID Reuse & CASCADE Deletes")
    print("=" * 60)
    
    if not backup_database():
        print("No existing database found. Migration not needed.")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = OFF")  
    cursor = conn.cursor()
    
    try:
        tables = [
            {
                "name": "users",
                "sql": """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL CHECK(role IN ("admin", "coordinator")),
                        department_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
                    )
                """,
                "columns": ["id", "name", "email", "password", "role", "department_id", "created_at"]
            },
            {
                "name": "departments",
                "sql": """
                    CREATE TABLE IF NOT EXISTS departments (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        code TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """,
                "columns": ["id", "name", "code", "created_at"]
            },
            {
                "name": "classrooms",
                "sql": """
                    CREATE TABLE IF NOT EXISTS classrooms (
                        id INTEGER PRIMARY KEY,
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
                """,
                "columns": ["id", "department_id", "code", "name", "capacity", "rows", "cols", "seats_per_desk", "created_at"]
            },
            {
                "name": "courses",
                "sql": """
                    CREATE TABLE IF NOT EXISTS courses (
                        id INTEGER PRIMARY KEY,
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
                """,
                "columns": ["id", "department_id", "code", "name", "instructor", "class_level", "type", "created_at"]
            },
            {
                "name": "students",
                "sql": """
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY,
                        department_id INTEGER NOT NULL,
                        student_no TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        class_level INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
                    )
                """,
                "columns": ["id", "department_id", "student_no", "name", "class_level", "created_at"]
            },
            {
                "name": "student_courses",
                "sql": """
                    CREATE TABLE IF NOT EXISTS student_courses (
                        id INTEGER PRIMARY KEY,
                        student_id INTEGER NOT NULL,
                        course_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                        FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                        UNIQUE(student_id, course_id)
                    )
                """,
                "columns": ["id", "student_id", "course_id", "created_at"]
            },
            {
                "name": "exams",
                "sql": """
                    CREATE TABLE IF NOT EXISTS exams (
                        id INTEGER PRIMARY KEY,
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
                """,
                "columns": ["id", "course_id", "department_id", "date", "start_time", "duration", "exam_type", "created_at"]
            },
            {
                "name": "exam_classrooms",
                "sql": """
                    CREATE TABLE IF NOT EXISTS exam_classrooms (
                        id INTEGER PRIMARY KEY,
                        exam_id INTEGER NOT NULL,
                        classroom_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
                        FOREIGN KEY (classroom_id) REFERENCES classrooms(id) ON DELETE CASCADE,
                        UNIQUE(exam_id, classroom_id)
                    )
                """,
                "columns": ["id", "exam_id", "classroom_id", "created_at"]
            },
            {
                "name": "exam_seating",
                "sql": """
                    CREATE TABLE IF NOT EXISTS exam_seating (
                        id INTEGER PRIMARY KEY,
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
                """,
                "columns": ["id", "student_id", "exam_id", "classroom_id", "row", "col", "seat_position", "created_at"]
            }
        ]
        
        for table_info in tables:
            migrate_table(cursor, table_info["name"], table_info["sql"], table_info["columns"])
        
        print("\nRecreating indexes...")
        cursor.execute("DROP INDEX IF EXISTS idx_users_email")
        cursor.execute("CREATE INDEX idx_users_email ON users(email)")
        
        cursor.execute("DROP INDEX IF EXISTS idx_students_no")
        cursor.execute("CREATE INDEX idx_students_no ON students(student_no)")
        
        cursor.execute("DROP INDEX IF EXISTS idx_courses_code")
        cursor.execute("CREATE INDEX idx_courses_code ON courses(code)")
        
        cursor.execute("DROP INDEX IF EXISTS idx_exams_date")
        cursor.execute("CREATE INDEX idx_exams_date ON exams(date)")
        print("  ✓ Indexes recreated")
        
        conn.execute("PRAGMA foreign_keys = ON")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✓ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nChanges applied:")
        print("  1. IDs will now be reused when rows are deleted")
        print("  2. CASCADE deletes enabled - deleting a department will")
        print("     automatically delete all related data (users, courses,")
        print("     students, classrooms, exams, etc.)")
        print("\nExample: Deleting a department will cascade delete:")
        print("  - All users in that department")
        print("  - All courses in that department")
        print("  - All students in that department")
        print("  - All classrooms in that department")
        print("  - All exams for that department")
        print("  - And all related records (student_courses, exam_seating, etc.)")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Migration failed: {str(e)}")
        print("Database has been rolled back to previous state.")
        print("Your backup is still available for manual recovery.")
        raise
    finally:
        conn.execute("PRAGMA foreign_keys = ON")  
        conn.close()

if __name__ == "__main__":
    try:
        migrate_database()
    except Exception as e:
        print(f"\nError during migration: {str(e)}")
        import traceback
        traceback.print_exc()

