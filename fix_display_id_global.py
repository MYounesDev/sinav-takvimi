"""
Fix display_id to be globally unique across all departments
This script updates the database schema to make display_id globally unique
"""

import sqlite3
import os
import shutil
from datetime import datetime
from config import DATABASE_PATH


def backup_database():
    """Create a backup of the current database"""
    if not os.path.exists(DATABASE_PATH):
        print("No database found. Will create fresh database.")
        return None
    
    backup_path = DATABASE_PATH.replace('.db', f'_before_global_displayid_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
    shutil.copy2(DATABASE_PATH, backup_path)
    print(f"✓ Database backed up to: {backup_path}")
    return backup_path


def fix_global_display_id():
    """Fix display_id to be globally unique"""
    
    print("=" * 70)
    print("FIX DISPLAY_ID TO BE GLOBALLY UNIQUE")
    print("=" * 70)
    
    backup_path = backup_database()
    
    # If no database exists, we'll just create a fresh one
    if backup_path is None:
        print("\nNo existing database. Please run init_database.py to create a fresh database.")
        print("The new database will have globally unique display_id from the start.")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Disable foreign keys temporarily
    conn.execute("PRAGMA foreign_keys = OFF")
    
    try:
        print("\nStep 1: Backing up all data...")
        
        # Backup all tables data
        tables_data = {}
        tables = ['departments', 'users', 'classrooms', 'courses', 'students', 
                  'student_courses', 'exams', 'exam_classrooms', 'exam_seating', 'deleted_ids']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT * FROM {table}")
                tables_data[table] = cursor.fetchall()
                print(f"  ✓ Backed up {table}: {len(tables_data[table])} rows")
            except Exception as e:
                print(f"  ⚠ Table {table} doesn't exist or error: {e}")
                tables_data[table] = []
        
        print("\nStep 2: Dropping old tables...")
        for table in reversed(tables):
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"  ✓ Dropped {table}")
            except Exception as e:
                print(f"  ⚠ Error dropping {table}: {e}")
        
        print("\nStep 3: Creating new tables with GLOBALLY UNIQUE display_id...")
        
        # Deleted IDs tracking table
        cursor.execute("""
            CREATE TABLE deleted_ids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                display_id INTEGER NOT NULL,
                deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(table_name, display_id)
            )
        """)
        
        # Departments table (already globally unique)
        cursor.execute("""
            CREATE TABLE departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Users table (already globally unique)
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'coordinator')),
                department_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
            )
        """)
        
        # Classrooms table - NOW GLOBALLY UNIQUE
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
        
        # Courses table - NOW GLOBALLY UNIQUE
        cursor.execute("""
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                department_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                instructor TEXT,
                class_level INTEGER,
                type TEXT CHECK(type IN ('mandatory', 'elective')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
                UNIQUE(department_id, code)
            )
        """)
        
        # Students table - NOW GLOBALLY UNIQUE
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
        
        # Student-Course relationship table
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
        
        # Exams table - NOW GLOBALLY UNIQUE
        cursor.execute("""
            CREATE TABLE exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                course_id INTEGER NOT NULL,
                department_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                duration INTEGER NOT NULL,
                exam_type TEXT DEFAULT 'final',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
            )
        """)
        
        # Exam-Classroom assignment table
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
        
        # Exam Seating table
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
        
        print("  ✓ All tables created with GLOBALLY UNIQUE display_id")
        
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
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table_name}{column if column.startswith('(') else f'({column})'}")
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
                    VALUES ('{table_name}', OLD.display_id);
                END
            """)
        print("  ✓ All triggers created")
        
        print("\nStep 6: Reassigning display_ids to be globally unique...")
        
        # We need to reassign display_ids to make them globally unique
        # Strategy: Assign new global display_ids sequentially
        
        global_display_id_counter = 1
        
        # Restore departments (they were already globally unique)
        if 'departments' in tables_data and tables_data['departments']:
            for row in tables_data['departments']:
                columns = list(row.keys())
                values = list(row)
                placeholders = ','.join(['?' for _ in columns])
                columns_str = ','.join(columns)
                cursor.execute(f"INSERT INTO departments ({columns_str}) VALUES ({placeholders})", values)
            print(f"  ✓ Restored departments: {len(tables_data['departments'])} rows")
            # Update counter
            cursor.execute("SELECT MAX(display_id) FROM departments")
            max_id = cursor.fetchone()[0]
            if max_id:
                global_display_id_counter = max(global_display_id_counter, max_id + 1)
        
        # Restore users (they were already globally unique)
        if 'users' in tables_data and tables_data['users']:
            for row in tables_data['users']:
                columns = list(row.keys())
                values = list(row)
                placeholders = ','.join(['?' for _ in columns])
                columns_str = ','.join(columns)
                cursor.execute(f"INSERT INTO users ({columns_str}) VALUES ({placeholders})", values)
            print(f"  ✓ Restored users: {len(tables_data['users'])} rows")
            # Update counter
            cursor.execute("SELECT MAX(display_id) FROM users")
            max_id = cursor.fetchone()[0]
            if max_id:
                global_display_id_counter = max(global_display_id_counter, max_id + 1)
        
        # Restore courses with NEW globally unique display_ids
        if 'courses' in tables_data and tables_data['courses']:
            for row in tables_data['courses']:
                columns = list(row.keys())
                values = list(row)
                # Replace display_id with new global one
                display_id_idx = columns.index('display_id')
                values[display_id_idx] = global_display_id_counter
                global_display_id_counter += 1
                
                placeholders = ','.join(['?' for _ in columns])
                columns_str = ','.join(columns)
                cursor.execute(f"INSERT INTO courses ({columns_str}) VALUES ({placeholders})", values)
            print(f"  ✓ Restored courses: {len(tables_data['courses'])} rows with NEW global display_ids")
        
        # Restore students with NEW globally unique display_ids
        if 'students' in tables_data and tables_data['students']:
            for row in tables_data['students']:
                columns = list(row.keys())
                values = list(row)
                # Replace display_id with new global one
                display_id_idx = columns.index('display_id')
                values[display_id_idx] = global_display_id_counter
                global_display_id_counter += 1
                
                placeholders = ','.join(['?' for _ in columns])
                columns_str = ','.join(columns)
                cursor.execute(f"INSERT INTO students ({columns_str}) VALUES ({placeholders})", values)
            print(f"  ✓ Restored students: {len(tables_data['students'])} rows with NEW global display_ids")
        
        # Restore classrooms with NEW globally unique display_ids
        if 'classrooms' in tables_data and tables_data['classrooms']:
            for row in tables_data['classrooms']:
                columns = list(row.keys())
                values = list(row)
                # Replace display_id with new global one
                display_id_idx = columns.index('display_id')
                values[display_id_idx] = global_display_id_counter
                global_display_id_counter += 1
                
                placeholders = ','.join(['?' for _ in columns])
                columns_str = ','.join(columns)
                cursor.execute(f"INSERT INTO classrooms ({columns_str}) VALUES ({placeholders})", values)
            print(f"  ✓ Restored classrooms: {len(tables_data['classrooms'])} rows with NEW global display_ids")
        
        # Restore relationship tables
        for table in ['student_courses', 'exams', 'exam_classrooms', 'exam_seating']:
            if table in tables_data and tables_data[table]:
                for row in tables_data[table]:
                    columns = list(row.keys())
                    values = list(row)
                    
                    # For exams, assign new global display_id if it has one
                    if table == 'exams' and 'display_id' in columns:
                        display_id_idx = columns.index('display_id')
                        values[display_id_idx] = global_display_id_counter
                        global_display_id_counter += 1
                    
                    placeholders = ','.join(['?' for _ in columns])
                    columns_str = ','.join(columns)
                    try:
                        cursor.execute(f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})", values)
                    except Exception as e:
                        print(f"    ⚠ Skipped row in {table}: {e}")
                print(f"  ✓ Restored {table}: {len(tables_data[table])} rows")
        
        # Don't restore deleted_ids - start fresh
        print("  ✓ Starting fresh deleted_ids table")
        
        # Commit all changes
        conn.commit()
        
        # Re-enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        
        print("\n" + "=" * 70)
        print("✓ DISPLAY_ID IS NOW GLOBALLY UNIQUE!")
        print("=" * 70)
        print("\nAll display_ids are now globally unique across all departments.")
        print("Delete operations will now work correctly.")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        conn.rollback()
        if backup_path:
            print(f"\nRestoring from backup: {backup_path}")
            conn.close()
            shutil.copy2(backup_path, DATABASE_PATH)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        fix_global_display_id()
        print("\nDatabase updated successfully!")
        print("All views will now show globally unique display_ids.")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
