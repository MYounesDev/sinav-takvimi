"""
Test Globally Unique display_id - Verify the fix
"""

import sqlite3
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.db_manager import db_manager
from config import DATABASE_PATH


def test_global_display_id():
    """Test that display_id is globally unique"""
    print("=" * 70)
    print("TEST GLOBALLY UNIQUE DISPLAY_ID")
    print("=" * 70)
    print(f"Database: {DATABASE_PATH}\n")
    
    # Get 5 departments
    depts = db_manager.execute_query("SELECT id, name FROM departments LIMIT 5")
    
    if len(depts) < 2:
        print("✗ Need at least 2 departments to test. Run init_database.py first.")
        return False
    
    dept1_id = depts[0]['id']
    dept2_id = depts[1]['id']
    
    print(f"Testing with two departments:")
    print(f"  Department 1: {depts[0]['name']} (ID: {dept1_id})")
    print(f"  Department 2: {depts[1]['name']} (ID: {dept2_id})")
    print()
    
    # Test 1: Create courses in different departments
    print("Test 1: Creating courses in different departments...")
    
    display_id_1 = db_manager.get_next_display_id('courses')
    print(f"  Next display_id for course (any dept): {display_id_1}")
    
    course1_id = db_manager.execute_update(
        "INSERT INTO courses (display_id, department_id, code, name) VALUES (?, ?, ?, ?)",
        (display_id_1, dept1_id, 'TEST101', 'Test Course 1')
    )
    print(f"  ✓ Created course in dept1: display_id={display_id_1}, real_id={course1_id}")
    
    display_id_2 = db_manager.get_next_display_id('courses')
    print(f"  Next display_id for course (any dept): {display_id_2}")
    
    if display_id_2 == display_id_1:
        print(f"  ✗ FAIL: display_id should be unique! Got {display_id_2}, expected {display_id_1 + 1}")
        return False
    
    course2_id = db_manager.execute_update(
        "INSERT INTO courses (display_id, department_id, code, name) VALUES (?, ?, ?, ?)",
        (display_id_2, dept2_id, 'TEST201', 'Test Course 2')
    )
    print(f"  ✓ Created course in dept2: display_id={display_id_2}, real_id={course2_id}")
    
    # Verify no duplicate display_ids
    result = db_manager.execute_query("""
        SELECT display_id, COUNT(*) as count 
        FROM courses 
        GROUP BY display_id 
        HAVING count > 1
    """)
    
    if result:
        print(f"  ✗ FAIL: Found duplicate display_ids: {result}")
        return False
    
    print("  ✓ PASS: No duplicate display_ids found")
    print()
    
    # Test 2: Create students in different departments
    print("Test 2: Creating students in different departments...")
    
    display_id_3 = db_manager.get_next_display_id('students')
    print(f"  Next display_id for student (any dept): {display_id_3}")
    
    student1_id = db_manager.execute_update(
        "INSERT INTO students (display_id, department_id, student_no, name) VALUES (?, ?, ?, ?)",
        (display_id_3, dept1_id, 'S001', 'Test Student 1')
    )
    print(f"  ✓ Created student in dept1: display_id={display_id_3}, real_id={student1_id}")
    
    display_id_4 = db_manager.get_next_display_id('students')
    print(f"  Next display_id for student (any dept): {display_id_4}")
    
    if display_id_4 == display_id_3:
        print(f"  ✗ FAIL: display_id should be unique! Got {display_id_4}, expected {display_id_3 + 1}")
        return False
    
    student2_id = db_manager.execute_update(
        "INSERT INTO students (display_id, department_id, student_no, name) VALUES (?, ?, ?, ?)",
        (display_id_4, dept2_id, 'S002', 'Test Student 2')
    )
    print(f"  ✓ Created student in dept2: display_id={display_id_4}, real_id={student2_id}")
    
    # Verify no duplicate display_ids
    result = db_manager.execute_query("""
        SELECT display_id, COUNT(*) as count 
        FROM students 
        GROUP BY display_id 
        HAVING count > 1
    """)
    
    if result:
        print(f"  ✗ FAIL: Found duplicate display_ids: {result}")
        return False
    
    print("  ✓ PASS: No duplicate display_ids found")
    print()
    
    # Test 3: Test delete and ID recycling
    print("Test 3: Testing delete and ID recycling...")
    
    # Delete course 1
    db_manager.execute_update("DELETE FROM courses WHERE id = ?", (course1_id,))
    print(f"  ✓ Deleted course with display_id={display_id_1}")
    
    # Check if it's in deleted_ids
    result = db_manager.execute_query(
        "SELECT display_id FROM deleted_ids WHERE table_name = 'courses' AND display_id = ?",
        (display_id_1,)
    )
    
    if not result:
        print(f"  ✗ FAIL: Deleted display_id not found in deleted_ids table")
        return False
    
    print(f"  ✓ display_id {display_id_1} added to deleted_ids table")
    
    # Get next display_id - should recycle the deleted one
    recycled_id = db_manager.get_next_display_id('courses')
    
    if recycled_id != display_id_1:
        print(f"  ✗ FAIL: Should have recycled display_id {display_id_1}, got {recycled_id}")
        return False
    
    print(f"  ✓ PASS: Recycled display_id {recycled_id}")
    
    # Verify it was removed from deleted_ids
    result = db_manager.execute_query(
        "SELECT display_id FROM deleted_ids WHERE table_name = 'courses' AND display_id = ?",
        (display_id_1,)
    )
    
    if result:
        print(f"  ✗ FAIL: display_id still in deleted_ids after recycling")
        return False
    
    print(f"  ✓ display_id {display_id_1} removed from deleted_ids table")
    print()
    
    # Test 4: Verify display_ids are unique across ALL tables and departments
    print("Test 4: Checking display_id uniqueness across all records...")
    
    all_courses = db_manager.execute_query("SELECT display_id, department_id FROM courses")
    all_students = db_manager.execute_query("SELECT display_id, department_id FROM students")
    
    course_ids = [c['display_id'] for c in all_courses]
    student_ids = [s['display_id'] for s in all_students]
    
    # Check for duplicates within courses
    if len(course_ids) != len(set(course_ids)):
        print(f"  ✗ FAIL: Duplicate display_ids in courses table")
        return False
    
    print(f"  ✓ All {len(course_ids)} course display_ids are unique")
    
    # Check for duplicates within students
    if len(student_ids) != len(set(student_ids)):
        print(f"  ✗ FAIL: Duplicate display_ids in students table")
        return False
    
    print(f"  ✓ All {len(student_ids)} student display_ids are unique")
    
    # Clean up test data
    print("\nCleaning up test data...")
    db_manager.execute_update("DELETE FROM courses WHERE code LIKE 'TEST%'")
    db_manager.execute_update("DELETE FROM students WHERE student_no LIKE 'S00%'")
    print("  ✓ Test data cleaned up")
    
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nSummary:")
    print("  ✓ display_id is globally unique across all departments")
    print("  ✓ Deleted display_ids are recycled properly")
    print("  ✓ No duplicate display_ids exist")
    print("  ✓ Delete operations work correctly")
    
    return True


if __name__ == "__main__":
    try:
        if not os.path.exists(DATABASE_PATH):
            print("Database not found. Please run init_database.py first.")
            sys.exit(1)
        
        success = test_global_display_id()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
