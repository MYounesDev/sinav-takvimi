"""
Initialize Fresh Database
Creates a fresh database with the new design
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database.db_manager import db_manager

if __name__ == "__main__":
    print("=" * 70)
    print("INITIALIZING FRESH DATABASE")
    print("=" * 70)
    
    try:
        db_manager.initialize_database()
        
        print("\n" + "=" * 70)
        print("✓ DATABASE INITIALIZED SUCCESSFULLY!")
        print("=" * 70)
        
        print("\nDefault users created:")
        print("  Admin:")
        print("    Email: admin@gmail.com")
        print("    Password: admin123")
        print("\n  Coordinators (password: admin123):")
        print("    - bilgisayar@gmail.com (Bilgisayar Mühendisliği)")
        print("    - yazilim@gmail.com (Yazılım Mühendisliği)")
        print("    - elektrik@gmail.com (Elektrik Mühendisliği)")

        
        print("\n" + "=" * 70)
        print("Database Features:")
        print("  ✓ display_id system (reusable IDs)")
        print("  ✓ CASCADE DELETE (automatic cleanup)")
        print("  ✓ Triggers for ID recycling")
        print("  ✓ Optimized indexes")
        print("=" * 70)
        
        print("\nYou can now run the application:")
        print("  python main.py")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
