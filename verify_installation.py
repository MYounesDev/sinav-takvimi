"""
Verification Script - Check if everything is set up correctly
"""

import sys
import os

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}/")
        return True
    else:
        print(f"❌ Missing {description}: {dirpath}/")
        return False

def check_module(module_name):
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ Module "{module_name}" is installed")
        return True
    except ImportError:
        print(f"❌ Module "{module_name}" is NOT installed")
        return False

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("  EXAM SCHEDULER - Installation Verification")
    print("="*60 + "\n")
    
    all_good = True
    
    print("📍 Python Version:")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print("   ⚠️ Python 3.12+ recommended")
        all_good = False
    else:
        print("   ✅ Version is compatible")
    print()
    
    print("📍 Core Files:")
    all_good &= check_file_exists("main.py", "Main entry point")
    all_good &= check_file_exists("config.py", "Configuration")
    all_good &= check_file_exists("requirements.txt", "Requirements")
    print()
    
    print("📍 Source Directories:")
    all_good &= check_directory_exists("src", "Source code")
    all_good &= check_directory_exists("src/database", "Database layer")
    all_good &= check_directory_exists("src/ui", "UI layer")
    all_good &= check_directory_exists("src/utils", "Utilities")
    print()
    
    print("📍 Key Source Files:")
    all_good &= check_file_exists("src/database/db_manager.py", "Database manager")
    all_good &= check_file_exists("src/ui/main_window.py", "Main window")
    all_good &= check_file_exists("src/ui/login_view.py", "Login view")
    all_good &= check_file_exists("src/utils/auth.py", "Authentication")
    all_good &= check_file_exists("src/utils/scheduler.py", "Scheduler algorithm")
    print()
    
    print("📍 Documentation:")
    all_good &= check_file_exists("README.md", "Main README")
    all_good &= check_file_exists("QUICK_START.md", "Quick Start Guide")
    all_good &= check_file_exists("PROJECT_STRUCTURE.md", "Project Structure")
    all_good &= check_file_exists("FEATURES.md", "Features Documentation")
    print()
    
    print("📍 Python Dependencies:")
    modules = [
        "PyQt6",
        "pandas",
        "openpyxl",
        "reportlab",
        "bcrypt"
    ]
    
    for module in modules:
        module_ok = check_module(module)
        all_good &= module_ok
    
    print()
    
    print("📍 Optional Directories:")
    check_directory_exists("examples", "Examples folder")
    check_directory_exists("database", "Database folder")
    print()
    
    print("="*60)
    if all_good:
        print("\n✅ ALL CHECKS PASSED!")
        print("\n🚀 Your installation is complete and ready to use!")
        print("\nNext steps:")
        print("  1. Run: python main.py")
        print("  2. Login with: admin@gmail.com / admin123")
        print("  3. Check QUICK_START.md for usage guide")
    else:
        print("\n⚠️ SOME CHECKS FAILED!")
        print("\nTo fix:")
        print("  1. Run: pip install -r requirements.txt")
        print("  2. Make sure all files are extracted properly")
        print("  3. Run this script again to verify")
    
    print("\n" + "="*60 + "\n")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

