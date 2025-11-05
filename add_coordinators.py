"""
Add coordinator accounts for all departments
Run this script to add/update coordinator accounts in the database
"""

import sqlite3
import bcrypt
import sys
from config import DATABASE_PATH

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def add_coordinators():
    """Add coordinator accounts for all departments"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, code FROM departments")
        departments = cursor.fetchall()
        
        dept_map = {dept["code"]: dept["id"] for dept in departments}
        
        print(f"Found {len(departments)} departments:")
        for dept in departments:
            print(f"  - {dept["name"]} ({dept["code"]})")
        
        coordinators = [
            ("Computer Coordinator", "bilgisayar@gmail.com", "COMPUTER"),
            ("Software Coordinator", "yazilim@gmail.com", "SOFTWARE"),
            ("Electrical Coordinator", "elektrik@gmail.com", "ELECTRICAL"),

        ]
        
        default_password = "admin123"
        hashed_password = bcrypt.hashpw(
            default_password.encode("utf-8"),
            bcrypt.gensalt()
        )
        
        print("\nAdding/Updating coordinators...")
        
        for coord_name, coord_email, dept_code in coordinators:
            if dept_code not in dept_map:
                print(f"  ⚠️  Department {dept_code} not found. Creating it...")
                
                dept_map = {
                    "COMPUTER": "Computer Engineering",
                    "SOFTWARE": "Software Engineering",
                    "ELECTRICAL": "Electrical Engineering",
                    "ELECTRONICS": "Electronics Engineering",
                    "CIVIL": "Civil Engineering"
                }
                
                cursor.execute("""
                    INSERT INTO departments (name, code)
                    VALUES (?, ?)
                """, (dept_names.get(dept_code, dept_code), dept_code))
                dept_map[dept_code] = cursor.lastrowid
                print(f"  ✓ Created department {dept_code}")
            
            dept_id = dept_map[dept_code]
            
            cursor.execute("""
                SELECT id FROM users 
                WHERE email = ?
            """, (coord_email,))
            
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute("""
                    UPDATE users 
                    SET name = ?, department_id = ?, role = "coordinator"
                    WHERE email = ?
                """, (coord_name, dept_id, coord_email))
                print(f"  ✓ Updated: {coord_name} ({coord_email})")
            else:
                cursor.execute("""
                    INSERT INTO users (name, email, password, role, department_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    coord_name,
                    coord_email,
                    hashed_password.decode("utf-8"),
                    "coordinator",
                    dept_id
                ))
                print(f"  ✓ Created: {coord_name} ({coord_email})")
        
        conn.commit()
        
        print("\n" + "="*60)
        print("COORDINATOR ACCOUNTS:")
        print("="*60)
        
        cursor.execute("""
            SELECT u.name, u.email, d.name as dept_name
            FROM users u
            JOIN departments d ON u.department_id = d.id
            WHERE u.role = "coordinator"
            ORDER BY d.name
        """)
        
        coordinators = cursor.fetchall()
        
        for coord in coordinators:
            print(f"\nDepartment: {coord["dept_name"]}")
            print(f"  Name:     {coord["name"]}")
            print(f"  Email:    {coord["email"]}")
            print(f"  Password: admin123")
        
        print("\n" + "="*60)
        print(f"✓ Successfully processed {len(coordinators)} coordinator accounts!")
        print("="*60)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("="*60)
    print("ADDING COORDINATOR ACCOUNTS")
    print("="*60)
    print()
    
    add_coordinators()
    
    print("\nDone! You can now login with any of the coordinator accounts.")
    print("Default password for all coordinators: admin123")

