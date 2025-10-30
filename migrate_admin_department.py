"""
Migration script to set admin users' department_id to NULL
"""

import sys
from src.database.db_manager import db_manager

def migrate():
    """Update all admin users to have NULL department_id"""
    try:
        query = """
            UPDATE users 
            SET department_id = NULL 
            WHERE role = 'admin' AND department_id IS NOT NULL
        """
        
        rows_affected = db_manager.execute_update(query)
        
        print(f"✅ Migration completed successfully!")
        print(f"   Updated {rows_affected} admin user(s) to have NULL department_id")
        
        admins = db_manager.execute_query("SELECT id, name, email, department_id FROM users WHERE role = 'admin'")
        print(f"\n📋 Current admin users:")
        for admin in admins:
            dept_status = "NULL (correct)" if admin['department_id'] is None else f"ID: {admin['department_id']} (needs update)"
            print(f"   - {admin['name']} ({admin['email']}): {dept_status}")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()

