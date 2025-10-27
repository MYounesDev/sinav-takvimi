"""
Database Manager - Handles all SQLite database operations
"""

import sqlite3
from typing import Optional, List, Tuple, Any
import bcrypt
from config import DATABASE_PATH, DEFAULT_ADMIN


class DatabaseManager:
    """Manages SQLite database connections and operations"""
    
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
        """Create all database tables"""
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'coordinator')),
                department_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        """)
        
        # Departments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Classrooms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classrooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                rows INTEGER NOT NULL,
                cols INTEGER NOT NULL,
                seats_per_desk INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id),
                UNIQUE(department_id, code)
            )
        """)
        
        # Courses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                instructor TEXT,
                class_level INTEGER,
                type TEXT CHECK(type IN ('mandatory', 'elective')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id),
                UNIQUE(department_id, code)
            )
        """)
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_id INTEGER NOT NULL,
                student_no TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                class_level INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id)
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
                course_id INTEGER NOT NULL,
                department_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                duration INTEGER NOT NULL,
                exam_type TEXT DEFAULT 'final',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (department_id) REFERENCES departments(id)
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
                FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
                UNIQUE(exam_id, classroom_id)
            )
        """)
        
        # Exam Seating table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_seating (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                classroom_id INTEGER NOT NULL,
                row INTEGER NOT NULL,
                col INTEGER NOT NULL,
                seat_position INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
                UNIQUE(exam_id, student_id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_no ON students(student_no)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_courses_code ON courses(code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exams_date ON exams(date)")
    
    def _create_default_admin(self, cursor: sqlite3.Cursor):
        """Create default admin user and departments with coordinators"""
        
        # Create departments
        departments = [
            ('Yönetim', 'ADMIN'),
            ('Bilgisayar Mühendisliği', 'BİLGİSAYAR'),
            ('Yazılım Mühendisliği', 'YAZILIM'),
            ('Elektrik Mühendisliği', 'ELEKTRİK'),
            ('Elektronik Mühendisliği', 'ELEKTRONİK'),
            ('İnşaat Mühendisliği', 'İNŞAAT')
        ]
        
        dept_ids = {}
        for dept_name, dept_code in departments:
            cursor.execute("""
                INSERT INTO departments (name, code)
                VALUES (?, ?)
            """, (dept_name, dept_code))
            dept_ids[dept_code] = cursor.lastrowid
        
        # Hash the default password
        hashed_password = bcrypt.hashpw(
            DEFAULT_ADMIN["password"].encode('utf-8'),
            bcrypt.gensalt()
        )
        
        # Create admin user
        cursor.execute("""
            INSERT INTO users (name, email, password, role, department_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            DEFAULT_ADMIN["name"],
            DEFAULT_ADMIN["email"],
            hashed_password.decode('utf-8'),
            DEFAULT_ADMIN["role"],
            dept_ids['ADMIN']
        ))
        
        # Create coordinators for each department
        coordinators = [
            ('Bilgisayar Koordinatörü', 'bilgisayar@kocaeli.edu.tr', 'BİLGİSAYAR'),
            ('Yazılım Koordinatörü', 'yazilim@kocaeli.edu.tr', 'YAZILIM'),
            ('Elektrik Koordinatörü', 'elektrik@kocaeli.edu.tr', 'ELEKTRİK'),
            ('Elektronik Koordinatörü', 'elektronik@kocaeli.edu.tr', 'ELEKTRONİK'),
            ('İnşaat Koordinatörü', 'insaat@kocaeli.edu.tr', 'İNŞAAT')
        ]
        
        for coord_name, coord_email, dept_code in coordinators:
            cursor.execute("""
                INSERT INTO users (name, email, password, role, department_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
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

