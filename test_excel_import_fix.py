

import sqlite3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.db_manager import db_manager
from config import DATABASE_PATH

def test_display_id_generation():
    print("Testing display_id generation...")
    
    dept_id = 1 
    
    next_id = db_manager.get_next_display_id('courses', dept_id)
    print(f"✓ Next display_id for courses (dept {dept_id}): {next_id}")
    
    next_id = db_manager.get_next_display_id('students', dept_id)
    print(f"✓ Next display_id for students (dept {dept_id}): {next_id}")
    
    next_id = db_manager.get_next_display_id('departments')
    print(f"✓ Next display_id for departments: {next_id}")
    
    return True

def test_course_insert():
    """Test inserting a course with display_id"""
    print("\nTesting course insert with display_id...")
    
    try:
        dept_id = 1
        display_id = db_manager.get_next_display_id('courses', dept_id)
        
        query = """
            INSERT INTO courses (display_id, department_id, code, name, instructor)
            VALUES (?, ?, ?, ?, ?)
        """
        
        course_id = db_manager.execute_update(query, (
            display_id, dept_id, 'TEST101', 'Test Course Import', 'Test Instructor'
        ))
        
        print(f"✓ Course inserted with ID: {course_id}, display_id: {display_id}")
        
        verify = db_manager.execute_query(
            "SELECT id, display_id, code, name FROM courses WHERE id = ?",
            (course_id,)
        )
        
        if verify:
            row = verify[0]
            print(f"✓ Verified: ID={row['id']}, Display ID={row['display_id']}, Code={row['code']}")
        
        db_manager.execute_update("DELETE FROM courses WHERE id = ?", (course_id,))
        print("✓ Test course deleted")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_student_insert():
    """Test inserting a student with display_id"""
    print("\nTesting student insert with display_id...")
    
    try:
        dept_id = 1
        display_id = db_manager.get_next_display_id('students', dept_id)
        
        query = """
            INSERT INTO students (display_id, department_id, student_no, name)
            VALUES (?, ?, ?, ?)
        """
        
        student_id = db_manager.execute_update(query, (
            display_id, dept_id, 'TEST123456', 'Test Student Import'
        ))
        
        print(f"✓ Student inserted with ID: {student_id}, display_id: {display_id}")
        
        verify = db_manager.execute_query(
            "SELECT id, display_id, student_no, name FROM students WHERE id = ?",
            (student_id,)
        )
        
        if verify:
            row = verify[0]
            print(f"✓ Verified: ID={row['id']}, Display ID={row['display_id']}, No={row['student_no']}")
        
        db_manager.execute_update("DELETE FROM students WHERE id = ?", (student_id,))
        print("✓ Test student deleted")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_classroom_insert():
    """Test inserting a classroom with display_id"""
    print("\nTesting classroom insert with display_id...")
    
    try:
        dept_id = 1
        display_id = db_manager.get_next_display_id('classrooms', dept_id)
        
        query = """
            INSERT INTO classrooms (display_id, department_id, code, name, capacity, rows, cols)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        classroom_id = db_manager.execute_update(query, (
            display_id, dept_id, 'TEST-01', 'Test Classroom', 30, 5, 6
        ))
        
        print(f"✓ Classroom inserted with ID: {classroom_id}, display_id: {display_id}")
        
        verify = db_manager.execute_query(
            "SELECT id, display_id, code, name FROM classrooms WHERE id = ?",
            (classroom_id,)
        )
        
        if verify:
            row = verify[0]
            print(f"✓ Verified: ID={row['id']}, Display ID={row['display_id']}, Code={row['code']}")
        
        db_manager.execute_update("DELETE FROM classrooms WHERE id = ?", (classroom_id,))
        print("✓ Test classroom deleted")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 70)
    print("EXCEL IMPORT FIX - VERIFICATION TEST")
    print("=" * 70)
    print(f"Database: {DATABASE_PATH}")
    print()
    
    if not os.path.exists(DATABASE_PATH):
        print("✗ Database not found. Please run init_database.py first.")
        return False
    
    results = []
    
    results.append(("display_id generation", test_display_id_generation()))
    results.append(("Course insert", test_course_insert()))
    results.append(("Student insert", test_student_insert()))
    results.append(("Classroom insert", test_classroom_insert()))
    
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Excel import should now work correctly.")
        return True
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
