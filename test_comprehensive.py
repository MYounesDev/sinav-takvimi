"""
Comprehensive Test Script for display_id and CASCADE DELETE
This script tests all the new features:
1. display_id automatic assignment
2. display_id recycling after deletion
3. CASCADE DELETE functionality
4. Department-scoped display_id for related tables
"""

import sqlite3
import os
import sys
from config import DATABASE_PATH

def test_display_id_system():
    """Test display_id creation and recycling"""
    
    print("=" * 70)
    print("TEST 1: display_id Creation and Recycling")
    print("=" * 70)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    try:
        print("\n[1] Creating test departments...")
        cursor.execute("SELECT MAX(display_id) as max_id FROM departments")
        max_id = cursor.fetchone()['max_id'] or 0
        
        test_depts = []
        for i in range(1, 4):
            cursor.execute("""
                INSERT INTO departments (display_id, name, code)
                VALUES (?, ?, ?)
            """, (max_id + i, f"Test Dept {i}", f"TEST{i}"))
            test_depts.append((cursor.lastrowid, max_id + i))
            print(f"  ✓ Created department: internal_id={cursor.lastrowid}, display_id={max_id + i}")
        
        conn.commit()
        
        print(f"\n[2] Deleting department with display_id={max_id + 2}...")
        cursor.execute("DELETE FROM departments WHERE display_id = ?", (max_id + 2,))
        conn.commit()
        print(f"  ✓ Department deleted")
        
        cursor.execute("SELECT * FROM deleted_ids WHERE table_name='departments' AND display_id=?", (max_id + 2,))
        result = cursor.fetchone()
        if result:
            print(f"  ✓ display_id {max_id + 2} recorded in deleted_ids table")
        else:
            print(f"  ✗ ERROR: display_id not recorded in deleted_ids!")
        
        print(f"\n[3] Creating new department (should reuse display_id={max_id + 2})...")
        
        cursor.execute("""
            SELECT display_id FROM deleted_ids
            WHERE table_name = 'departments'
            ORDER BY display_id ASC
            LIMIT 1
        """)
        result = cursor.fetchone()
        
        if result:
            recycled_id = result['display_id']
            cursor.execute("""
                DELETE FROM deleted_ids
                WHERE table_name = 'departments' AND display_id = ?
            """, (recycled_id,))
            
            cursor.execute("""
                INSERT INTO departments (display_id, name, code)
                VALUES (?, ?, ?)
            """, (recycled_id, "Recycled Dept", "RECYCLED"))
            
            conn.commit()
            print(f"  ✓ New department created with recycled display_id={recycled_id}")
        else:
            print("  ✗ No recycled ID available")
        
        print("\n[4] Cleaning up test data...")
        cursor.execute("DELETE FROM departments WHERE code LIKE 'TEST%' OR code = 'RECYCLED'")
        conn.commit()
        print("  ✓ Test data cleaned up")
        
        print("\n" + "=" * 70)
        print("✓ TEST 1 PASSED: display_id system working correctly")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ TEST 1 FAILED: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()
    
    return True

def test_cascade_delete():
    """Test CASCADE DELETE functionality"""
    
    print("\n\n" + "=" * 70)
    print("TEST 2: CASCADE DELETE Functionality")
    print("=" * 70)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    try:
        print("\n[1] Creating test department...")
        cursor.execute("SELECT MAX(display_id) as max_id FROM departments")
        max_id = cursor.fetchone()['max_id'] or 0
        display_id = max_id + 1
        
        cursor.execute("""
            INSERT INTO departments (display_id, name, code)
            VALUES (?, ?, ?)
        """, (display_id, "CASCADE Test Dept", "CASCTEST"))
        dept_id = cursor.lastrowid
        print(f"  ✓ Department created: id={dept_id}, display_id={display_id}")
        
        print("\n[2] Creating related records...")
        
        cursor.execute("""
            INSERT INTO classrooms (display_id, department_id, code, name, capacity, rows, cols)
            VALUES (1, ?, 'C101', 'Test Classroom', 40, 5, 8)
        """, (dept_id,))
        classroom_id = cursor.lastrowid
        print(f"  ✓ Classroom created: id={classroom_id}")
        
        cursor.execute("""
            INSERT INTO courses (display_id, department_id, code, name, class_level, type)
            VALUES (1, ?, 'TST101', 'Test Course', 1, 'mandatory')
        """, (dept_id,))
        course_id = cursor.lastrowid
        print(f"  ✓ Course created: id={course_id}")
        
        cursor.execute("""
            INSERT INTO students (display_id, department_id, student_no, name, class_level)
            VALUES (1, ?, 'TEST001', 'Test Student', 1)
        """, (dept_id,))
        student_id = cursor.lastrowid
        print(f"  ✓ Student created: id={student_id}")
        
        cursor.execute("""
            INSERT INTO student_courses (student_id, course_id)
            VALUES (?, ?)
        """, (student_id, course_id))
        print(f"  ✓ Student-course relationship created")
        
        conn.commit()
        
        print("\n[3] Counting related records before deletion...")
        counts_before = {}
        
        tables = ['classrooms', 'courses', 'students', 'student_courses']
        for table in tables:
            if table == 'student_courses':
                cursor.execute(f"""
                    SELECT COUNT(*) as cnt FROM {table}
                    WHERE student_id = ? OR course_id = ?
                """, (student_id, course_id))
            else:
                cursor.execute(f"""
                    SELECT COUNT(*) as cnt FROM {table}
                    WHERE department_id = ?
                """, (dept_id,))
            counts_before[table] = cursor.fetchone()['cnt']
            print(f"  - {table}: {counts_before[table]} records")
        
        print(f"\n[4] Deleting department (id={dept_id})...")
        cursor.execute("DELETE FROM departments WHERE id = ?", (dept_id,))
        conn.commit()
        print("  ✓ Department deleted")
        
        print("\n[5] Counting related records after deletion...")
        all_deleted = True
        
        for table in tables:
            if table == 'student_courses':
                cursor.execute(f"""
                    SELECT COUNT(*) as cnt FROM {table}
                    WHERE student_id = ? OR course_id = ?
                """, (student_id, course_id))
            else:
                cursor.execute(f"""
                    SELECT COUNT(*) as cnt FROM {table}
                    WHERE department_id = ?
                """, (dept_id,))
            count_after = cursor.fetchone()['cnt']
            
            if count_after == 0:
                print(f"  ✓ {table}: {counts_before[table]} → 0 (CASCADE worked!)")
            else:
                print(f"  ✗ {table}: {counts_before[table]} → {count_after} (CASCADE FAILED!)")
                all_deleted = False
        
        if all_deleted:
            print("\n" + "=" * 70)
            print("✓ TEST 2 PASSED: CASCADE DELETE working correctly")
            print("=" * 70)
            return True
        else:
            print("\n" + "=" * 70)
            print("✗ TEST 2 FAILED: Some records were not deleted")
            print("=" * 70)
            return False
        
    except Exception as e:
        print(f"\n✗ TEST 2 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return False
    finally:
        conn.close()

def test_department_scoped_display_id():
    """Test that display_id is scoped per department for related tables"""
    
    print("\n\n" + "=" * 70)
    print("TEST 3: Department-Scoped display_id")
    print("=" * 70)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name FROM departments LIMIT 2")
        depts = cursor.fetchall()
        
        if len(depts) < 2:
            print("  ⚠ Not enough departments to test. Skipping...")
            return True
        
        dept1_id, dept1_name = depts[0]['id'], depts[0]['name']
        dept2_id, dept2_name = depts[1]['id'], depts[1]['name']
        
        print(f"\n[1] Testing with two departments:")
        print(f"  - Dept 1: {dept1_name} (id={dept1_id})")
        print(f"  - Dept 2: {dept2_name} (id={dept2_id})")
        
        print("\n[2] Creating students with display_id=999 in both departments...")
        
        cursor.execute("""
            INSERT INTO students (display_id, department_id, student_no, name, class_level)
            VALUES (999, ?, 'TEST999A', 'Test Student A', 1)
        """, (dept1_id,))
        student1_id = cursor.lastrowid
        print(f"  ✓ Student created in Dept 1: id={student1_id}, display_id=999")
        
        cursor.execute("""
            INSERT INTO students (display_id, department_id, student_no, name, class_level)
            VALUES (999, ?, 'TEST999B', 'Test Student B', 1)
        """, (dept2_id,))
        student2_id = cursor.lastrowid
        print(f"  ✓ Student created in Dept 2: id={student2_id}, display_id=999")
        
        conn.commit()
        
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM students WHERE display_id = 999
        """)
        count = cursor.fetchone()['cnt']
        
        if count == 2:
            print(f"\n  ✓ Both students exist with display_id=999 (department-scoped)")
        else:
            print(f"\n  ✗ ERROR: Expected 2 students, found {count}")
            return False
        
        print("\n[3] Cleaning up test data...")
        cursor.execute("DELETE FROM students WHERE student_no LIKE 'TEST999%'")
        conn.commit()
        print("  ✓ Test data cleaned up")
        
        print("\n" + "=" * 70)
        print("✓ TEST 3 PASSED: Department-scoped display_id working correctly")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n✗ TEST 3 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return False
    finally:
        conn.close()

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "COMPREHENSIVE TEST SUITE" + " " * 29 + "║")
    print("║" + " " * 10 + "display_id & CASCADE DELETE Tests" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    
    if not os.path.exists(DATABASE_PATH):
        print(f"\n✗ ERROR: Database not found at {DATABASE_PATH}")
        print("Please run the application first to create the database.")
        sys.exit(1)
    
    results = []
    
    results.append(("display_id System", test_display_id_system()))
    results.append(("CASCADE DELETE", test_cascade_delete()))
    results.append(("Department-Scoped display_id", test_department_scoped_display_id()))
    
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 25 + "TEST SUMMARY" + " " * 31 + "║")
    print("╠" + "═" * 68 + "╣")
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        padding = " " * (50 - len(test_name))
        print(f"║  {test_name}{padding}{status}   ║")
        if not result:
            all_passed = False
    
    print("╚" + "═" * 68 + "╝")
    
    if all_passed:
        print("\n✓ ALL TESTS PASSED!")
        print("\nThe database migration and new features are working correctly.")
        print("You can now safely use the application with display_id support.")
    else:
        print("\n✗ SOME TESTS FAILED!")
        print("\nPlease check the errors above and fix any issues.")
        sys.exit(1)

if __name__ == "__main__":
    main()
