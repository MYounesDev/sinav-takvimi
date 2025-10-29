"""
Database Manager - Enhanced with display_id support and CASCADE deletes
"""

import sqlite3
from typing import Optional, List, Tuple, Any
import bcrypt
from config import DATABASE_PATH, DEFAULT_ADMIN


class DatabaseManager:
    """Manages SQLite database connections and operations with display_id support"""
    
    def __init__(self):
        """Initialize database manager"""
        self.db_path = DATABASE_PATH
        
    def get_connection(self) -> sqlite3.Connection:
        """
        Get a new database connection
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """
        Execute a SELECT query and return results
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of rows
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        finally:
            conn.close()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows or last inserted row ID
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        finally:
            conn.close()
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute multiple queries with different parameters
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            Number of affected rows
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()
    
    def initialize_database(self):
        """Create database schema and seed initial data"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Create tables
            self._create_tables(cursor)
            
            # Create triggers for display_id management
            self._create_triggers(cursor)
            
            # Check if admin exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]
            
            if admin_count == 0:
                # Create default admin and department
                self._create_default_admin(cursor)
            
            conn.commit()
            print("Database initialized successfully!")
        finally:
            conn.close()
    
    def _create_tables(self, cursor: sqlite3.Cursor):
        """Create all database tables with display_id support"""
        
        # Deleted IDs tracking table for each entity type
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deleted_ids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER NOT NULL,
                table_name TEXT NOT NULL,
                deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(table_name, display_id)
            )
        """)
        
        # Departments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
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
        
        # Classrooms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classrooms (
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
        
        # Courses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_id INTEGER UNIQUE NOT NULL,
                department_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                instructor TEXT,
                class_level INTEGER,
                type TEXT CHECK(type IN ('mandatory', 'elective')),
                isActive INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
                UNIQUE(department_id, code)
            )
        """)
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
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
            CREATE TABLE IF NOT EXISTS student_courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE(student_id, course_id)
            )
        """)
        
        # Exams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
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
            CREATE TABLE IF NOT EXISTS exam_classrooms (
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
            CREATE TABLE IF NOT EXISTS exam_seating (
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
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_display_id ON users(display_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_no ON students(student_no)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_display_id ON students(display_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_courses_code ON courses(code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_courses_display_id ON courses(display_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_classrooms_display_id ON classrooms(display_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_departments_display_id ON departments(display_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exams_date ON exams(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exams_display_id ON exams(display_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_deleted_ids_table ON deleted_ids(table_name, display_id)")
    
    def _create_triggers(self, cursor: sqlite3.Cursor):
        """Create triggers for automatic display_id management"""
        
        # Trigger to recycle deleted display_ids for departments
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS before_delete_department
            BEFORE DELETE ON departments
            BEGIN
                INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
                VALUES ('departments', OLD.display_id);
            END
        """)
        
        # Trigger to recycle deleted display_ids for users
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS before_delete_user
            BEFORE DELETE ON users
            BEGIN
                INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
                VALUES ('users', OLD.display_id);
            END
        """)
        
        # Trigger to recycle deleted display_ids for classrooms
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS before_delete_classroom
            BEFORE DELETE ON classrooms
            BEGIN
                INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
                VALUES ('classrooms', OLD.display_id);
            END
        """)
        
        # Trigger to recycle deleted display_ids for courses
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS before_delete_course
            BEFORE DELETE ON courses
            BEGIN
                INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
                VALUES ('courses', OLD.display_id);
            END
        """)
        
        # Trigger to recycle deleted display_ids for students
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS before_delete_student
            BEFORE DELETE ON students
            BEGIN
                INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
                VALUES ('students', OLD.display_id);
            END
        """)
        
        # Trigger to recycle deleted display_ids for exams
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS before_delete_exam
            BEFORE DELETE ON exams
            BEGIN
                INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
                VALUES ('exams', OLD.display_id);
            END
        """)
    
    def get_next_display_id(self, table_name: str, department_id: Optional[int] = None) -> int:
        """
        Get the next available display_id for a table.
        Reuses deleted IDs if available, otherwise returns max + 1.
        display_id is now GLOBALLY UNIQUE across all tables and departments.
        
        Args:
            table_name: Name of the table
            department_id: Deprecated - kept for backward compatibility but not used
            
        Returns:
            Next available display_id (globally unique)
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Check for recycled IDs first
            cursor.execute("""
                SELECT display_id FROM deleted_ids
                WHERE table_name = ?
                ORDER BY display_id ASC
                LIMIT 1
            """, (table_name,))
            
            result = cursor.fetchone()
            if result:
                recycled_id = result[0]
                # Remove from deleted_ids
                cursor.execute("""
                    DELETE FROM deleted_ids
                    WHERE table_name = ? AND display_id = ?
                """, (table_name, recycled_id))
                conn.commit()
                return recycled_id
            
            # No recycled ID available, get max display_id + 1 (globally)
            cursor.execute(f"""
                SELECT COALESCE(MAX(display_id), 0) + 1
                FROM {table_name}
            """)
            
            result = cursor.fetchone()
            return result[0]
        finally:
            conn.close()
    
    def _create_default_admin(self, cursor: sqlite3.Cursor):
        """Create default admin user and departments with coordinators"""
        
        # Create departments
        departments = [
            ('Bilgisayar Mühendisliği', 'BİLGİSAYAR'),
            ('Yazılım Mühendisliği', 'YAZILIM'),
            ('Elektrik Mühendisliği', 'ELEKTRİK'),
            ('Elektronik Mühendisliği', 'ELEKTRONİK'),
            ('İnşaat Mühendisliği', 'İNŞAAT')
        ]
        
        dept_ids = {}
        for idx, (dept_name, dept_code) in enumerate(departments, 1):
            cursor.execute("""
                INSERT INTO departments (display_id, name, code)
                VALUES (?, ?, ?)
            """, (idx, dept_name, dept_code))
            dept_ids[dept_code] = cursor.lastrowid
        
        # Hash the default password
        hashed_password = bcrypt.hashpw(
            DEFAULT_ADMIN["password"].encode('utf-8'),
            bcrypt.gensalt()
        )
        
        # Create admin user (no department assignment)
        cursor.execute("""
            INSERT INTO users (display_id, name, email, password, role, department_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            1,  # Admin gets display_id = 1
            DEFAULT_ADMIN["name"],
            DEFAULT_ADMIN["email"],
            hashed_password.decode('utf-8'),
            DEFAULT_ADMIN["role"],
            None  # Admin is not tied to any department
        ))
        
        # Create coordinators for each department
        coordinators = [
            ('Bilgisayar Koordinatörü', 'bilgisayar@gmail.com', 'BİLGİSAYAR'),
            ('Yazılım Koordinatörü', 'yazilim@gmail.com', 'YAZILIM'),
            ('Elektrik Koordinatörü', 'elektrik@gmail.com', 'ELEKTRİK')
        ]
        
        for idx, (coord_name, coord_email, dept_code) in enumerate(coordinators, 2):
            cursor.execute("""
                INSERT INTO users (display_id, name, email, password, role, department_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                idx,  # Coordinators get display_id 2-6
                coord_name,
                coord_email,
                hashed_password.decode('utf-8'),  # Same password: admin123
                'coordinator',
                dept_ids[dept_code]
            ))
        
        print(f"Default admin created: {DEFAULT_ADMIN['email']} / {DEFAULT_ADMIN['password']}")
        print(f"Coordinators created for all departments (password: admin123)")


# Singleton instance
db_manager = DatabaseManager()
