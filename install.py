"""
Installation and Setup Script
Automates the installation process for the Exam Scheduler
"""

import subprocess
import sys
import os

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check if Python version is 3.12 or higher"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print("❌ Error: Python 3.12 or higher is required")
        print("Please install Python 3.12+ from https://www.python.org/downloads/")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_sample_files():
    """Create sample Excel files"""
    print_header("Creating Sample Files")
    
    try:
        subprocess.check_call([sys.executable, "create_sample_excel.py"])
        print("✅ Sample files created")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Could not create sample files (optional)")
        return True  # Don"t fail if this doesn"t work

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    dirs = ["database", "examples"]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created/verified: {directory}/")
    
    return True

def main():
    """Main installation process"""
    print("\n" + "🎓"*30)
    print("\n   EXAM SCHEDULER - Installation Script")
    print("   Kocaeli University - Yazlab-1 Project\n")
    print("🎓"*30)
    
    if not check_python_version():
        return False
    
    if not create_directories():
        return False
    
    if not install_dependencies():
        return False
    
    create_sample_files()
    
    print_header("Installation Complete! 🎉")
    print("\n✨ The Exam Scheduler has been installed successfully!\n")
    print("Next steps:")
    print("  1. Run the application:")
    print("     python main.py")
    print("\n  2. Login with default credentials:")
    print("     Email: admin@gmail.com")
    print("     Password: admin123")
    print("\n  3. Check QUICK_START.md for a step-by-step guide")
    print("\n  4. Sample Excel files are in the examples/ folder")
    print("\n📚 Documentation: README.md")
    print("🚀 Quick Start: QUICK_START.md")
    print("\nHappy scheduling! 🎓\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

