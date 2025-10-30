"""
Fix classroom capacity calculation
Capacity should be: rows × cols × seats_per_desk
"""

import sqlite3
from pathlib import Path

db_path = Path("database/exam_scheduler.db")

if not db_path.exists():
    print(f"❌ Database not found at: {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, rows, cols, seats_per_desk, capacity FROM classrooms")
    classrooms = cursor.fetchall()
    
    if not classrooms:
        print("ℹ️  No classrooms found in database")
        conn.close()
        exit(0)
    
    print(f"\n🔧 Fixing capacity for {len(classrooms)} classrooms...\n")
    
    updated_count = 0
    for classroom_id, name, rows, cols, seats_per_desk, old_capacity in classrooms:
        correct_capacity = rows * cols * seats_per_desk
        
        if old_capacity != correct_capacity:
            print(f"📝 {name}:")
            print(f"   Rows: {rows}, Cols: {cols}, Seats/Desk: {seats_per_desk}")
            print(f"   Old capacity: {old_capacity}")
            print(f"   New capacity: {correct_capacity} ✅")
            print()
            
            cursor.execute(
                "UPDATE classrooms SET capacity = ? WHERE id = ?",
                (correct_capacity, classroom_id)
            )
            updated_count += 1
        else:
            print(f"✓ {name}: Capacity already correct ({correct_capacity})")
    
    conn.commit()
    
    print(f"\n{'='*50}")
    print(f"✅ Successfully updated {updated_count} classrooms")
    print(f"✓ {len(classrooms) - updated_count} classrooms were already correct")
    print(f"{'='*50}\n")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    if 'conn' in locals():
        conn.rollback()
finally:
    if 'conn' in locals():
        conn.close()
