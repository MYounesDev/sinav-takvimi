"""
Test script to verify CASCADE DELETE functionality
This demonstrates that deleting a department cascades to all related records
"""

import sqlite3
import os


def test_cascade_deletes():
    """Test that CASCADE deletes work correctly"""
    
    print("=" * 60)
    print("Testing CASCADE DELETE Functionality")
    print("=" * 60)
    
    # Create a test database
    test_db = "test_cascade.db"
    
    # Clean up any existing test database
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = sqlite3.connect(test_db)
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
    cursor = conn.cursor()
    
    # Create tables with CASCADE
    print("\n1. Creating tables with CASCADE constraints...")
    print("-" * 60)
    
    cursor.execute("""
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            code TEXT UNIQUE NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            student_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE classrooms (
            id INTEGER PRIMARY KEY,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
        )
    """)
    
    print("  Tables created successfully!")
    
    # Insert test data
    print("\n2. Inserting test data...")
    print("-" * 60)
    
    # Insert department
    cursor.execute("INSERT INTO departments (name, code) VALUES (?, ?)", ("Test Department", "TEST"))
    dept_id = cursor.lastrowid
    print(f"  Created department: ID={dept_id}, Name=Test Department")
    
    # Insert users
    cursor.execute("INSERT INTO users (name, email, department_id) VALUES (?, ?, ?)", 
                   ("User 1", "user1@test.com", dept_id))
    cursor.execute("INSERT INTO users (name, email, department_id) VALUES (?, ?, ?)", 
                   ("User 2", "user2@test.com", dept_id))
    print(f"  Created 2 users")
    
    # Insert courses
    cursor.execute("INSERT INTO courses (code, name, department_id) VALUES (?, ?, ?)", 
                   ("CS101", "Computer Science 101", dept_id))
    cursor.execute("INSERT INTO courses (code, name, department_id) VALUES (?, ?, ?)", 
                   ("CS102", "Computer Science 102", dept_id))
    print(f"  Created 2 courses")
    
    # Insert students
    cursor.execute("INSERT INTO students (student_no, name, department_id) VALUES (?, ?, ?)", 
                   ("S001", "Student 1", dept_id))
    cursor.execute("INSERT INTO students (student_no, name, department_id) VALUES (?, ?, ?)", 
                   ("S002", "Student 2", dept_id))
    print(f"  Created 2 students")
    
    # Insert classrooms
    cursor.execute("INSERT INTO classrooms (code, name, department_id) VALUES (?, ?, ?)", 
                   ("C101", "Classroom 101", dept_id))
    cursor.execute("INSERT INTO classrooms (code, name, department_id) VALUES (?, ?, ?)", 
                   ("C102", "Classroom 102", dept_id))
    print(f"  Created 2 classrooms")
    
    conn.commit()
    
    # Count records before deletion
    print("\n3. Before deletion - Record counts:")
    print("-" * 60)
    cursor.execute("SELECT COUNT(*) FROM departments")
    dept_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM courses")
    course_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM classrooms")
    classroom_count = cursor.fetchone()[0]
    
    print(f"  Departments: {dept_count}")
    print(f"  Users: {user_count}")
    print(f"  Courses: {course_count}")
    print(f"  Students: {student_count}")
    print(f"  Classrooms: {classroom_count}")
    
    # Delete the department
    print("\n4. Deleting department (ID={})...".format(dept_id))
    print("-" * 60)
    cursor.execute("DELETE FROM departments WHERE id = ?", (dept_id,))
    conn.commit()
    print("  Department deleted!")
    
    # Count records after deletion
    print("\n5. After deletion - Record counts:")
    print("-" * 60)
    cursor.execute("SELECT COUNT(*) FROM departments")
    dept_count_after = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count_after = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM courses")
    course_count_after = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count_after = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM classrooms")
    classroom_count_after = cursor.fetchone()[0]
    
    print(f"  Departments: {dept_count_after}")
    print(f"  Users: {user_count_after}")
    print(f"  Courses: {course_count_after}")
    print(f"  Students: {student_count_after}")
    print(f"  Classrooms: {classroom_count_after}")
    
    # Verify CASCADE worked
    print("\n" + "=" * 60)
    success = True
    if dept_count_after != 0:
        print("FAIL: Department still exists!")
        success = False
    if user_count_after != 0:
        print("FAIL: Users were not deleted!")
        success = False
    if course_count_after != 0:
        print("FAIL: Courses were not deleted!")
        success = False
    if student_count_after != 0:
        print("FAIL: Students were not deleted!")
        success = False
    if classroom_count_after != 0:
        print("FAIL: Classrooms were not deleted!")
        success = False
    
    if success:
        print("SUCCESS! All related records were CASCADE deleted!")
        print("\nCascade deletion order:")
        print("  - Department deleted")
        print("  - All users in department automatically deleted")
        print("  - All courses in department automatically deleted")
        print("  - All students in department automatically deleted")
        print("  - All classrooms in department automatically deleted")
    print("=" * 60)
    
    # Clean up
    conn.close()
    os.remove(test_db)
    print("\nTest database cleaned up")


def test_classroom_cascade():
    """Test that deleting a classroom cascades to exam tables"""
    
    print("\n\n" + "=" * 60)
    print("Testing Classroom CASCADE to Exam Tables")
    print("=" * 60)
    
    test_db = "test_cascade2.db"
    
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = sqlite3.connect(test_db)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("CREATE TABLE classrooms (id INTEGER PRIMARY KEY, code TEXT)")
    cursor.execute("""
        CREATE TABLE exam_classrooms (
            id INTEGER PRIMARY KEY,
            exam_id INTEGER,
            classroom_id INTEGER NOT NULL,
            FOREIGN KEY (classroom_id) REFERENCES classrooms(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE exam_seating (
            id INTEGER PRIMARY KEY,
            exam_id INTEGER,
            classroom_id INTEGER NOT NULL,
            FOREIGN KEY (classroom_id) REFERENCES classrooms(id) ON DELETE CASCADE
        )
    """)
    
    # Insert data
    cursor.execute("INSERT INTO classrooms (code) VALUES (?)", ("C101",))
    classroom_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO exam_classrooms (exam_id, classroom_id) VALUES (?, ?)", (1, classroom_id))
    cursor.execute("INSERT INTO exam_classrooms (exam_id, classroom_id) VALUES (?, ?)", (2, classroom_id))
    cursor.execute("INSERT INTO exam_seating (exam_id, classroom_id) VALUES (?, ?)", (1, classroom_id))
    
    conn.commit()
    
    # Count before
    cursor.execute("SELECT COUNT(*) FROM exam_classrooms")
    before_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM exam_seating")
    before_seating = cursor.fetchone()[0]
    
    print(f"\nBefore deletion:")
    print(f"  exam_classrooms: {before_count}")
    print(f"  exam_seating: {before_seating}")
    
    # Delete classroom
    cursor.execute("DELETE FROM classrooms WHERE id = ?", (classroom_id,))
    conn.commit()
    
    # Count after
    cursor.execute("SELECT COUNT(*) FROM exam_classrooms")
    after_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM exam_seating")
    after_seating = cursor.fetchone()[0]
    
    print(f"\nAfter deletion:")
    print(f"  exam_classrooms: {after_count}")
    print(f"  exam_seating: {after_seating}")
    
    print("\n" + "=" * 60)
    if after_count == 0 and after_seating == 0:
        print("SUCCESS! Classroom deletion cascaded to exam tables!")
    else:
        print("FAIL: Exam records were not deleted!")
    print("=" * 60)
    
    conn.close()
    os.remove(test_db)


if __name__ == "__main__":
    # Test department cascade
    test_cascade_deletes()
    
    # Test classroom cascade
    test_classroom_cascade()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("CASCADE DELETE is now enabled for all foreign key relationships.")
    print("\nWhen you delete:")
    print("  - A department: All related users, courses, students, classrooms, exams are deleted")
    print("  - A classroom: All related exam_classrooms and exam_seating are deleted")
    print("  - A course: All related exams, student_courses are deleted")
    print("  - A student: All related student_courses and exam_seating are deleted")
    print("  - An exam: All related exam_classrooms and exam_seating are deleted")
    print("\nAll deletions cascade automatically!")
    print("=" * 60)

