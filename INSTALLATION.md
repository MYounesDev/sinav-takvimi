# 🔧 Installation Guide

Complete installation guide for the Exam Scheduler System.

## 📋 Prerequisites

### Required Software
- **Python 3.12 or higher**
  - Download from: https://www.python.org/downloads/
  - Make sure to check "Add Python to PATH" during installation
  
- **pip** (Python package manager)
  - Usually included with Python
  - Verify with: `pip --version`

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB for application and dependencies
- **Display**: 1280×720 minimum resolution

---

## 🚀 Quick Installation (Recommended)

### Method 1: Automated Installer

**Windows:**
```batch
python install.py
```

**Linux/Mac:**
```bash
python3 install.py
```

This will automatically:
1. Check Python version
2. Create necessary directories
3. Install all dependencies
4. Generate sample Excel files

### Method 2: Manual Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create sample files:**
   ```bash
   python create_sample_excel.py
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

---

## 📦 Detailed Installation Steps

### Step 1: Download/Clone Project

**Option A: Download ZIP**
1. Download the project ZIP file
2. Extract to a folder (e.g., `C:\ExamScheduler` or `~/ExamScheduler`)
3. Open terminal/command prompt in that folder

**Option B: Git Clone**
```bash
git clone <repository-url>
cd exam-scheduler
```

### Step 2: Install Python (if not installed)

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python@3.12

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
# Install Python 3.12
sudo apt update
sudo apt install python3.12 python3-pip

# Verify
python3 --version
```

### Step 3: Create Virtual Environment (Optional but Recommended)

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Or install individually:
pip install PyQt6==6.6.1
pip install pandas==2.1.4
pip install openpyxl==3.1.2
pip install reportlab==4.0.7
pip install bcrypt==4.1.2
```

### Step 5: Verify Installation

```bash
python verify_installation.py
```

This will check:
- ✅ Python version
- ✅ All required files
- ✅ All dependencies
- ✅ Directory structure

### Step 6: Generate Sample Files

```bash
python create_sample_excel.py
```

This creates sample Excel files in `examples/` folder for testing.

### Step 7: Run the Application

**Windows:**
```batch
# Using batch file
run.bat

# Or directly
python main.py
```

**Linux/Mac:**
```bash
# Using shell script
chmod +x run.sh
./run.sh

# Or directly
python3 main.py
```

---

## 🐛 Troubleshooting

### Problem: "python is not recognized"

**Solution:** Python not in PATH
- **Windows**: Reinstall Python with "Add to PATH" checked
- **Linux/Mac**: Use `python3` instead of `python`

### Problem: "No module named 'PyQt6'"

**Solution:** Dependencies not installed
```bash
pip install -r requirements.txt
```

### Problem: "Permission denied" (Linux/Mac)

**Solution:** Use sudo or virtual environment
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or use sudo (not recommended)
sudo pip3 install -r requirements.txt
```

### Problem: Application won't start

**Solution 1:** Check Python version
```bash
python --version
# Should be 3.12 or higher
```

**Solution 2:** Delete database and restart
```bash
# Delete the database file
rm database/exam_scheduler.db  # Linux/Mac
del database\exam_scheduler.db  # Windows

# Restart application
python main.py
```

**Solution 3:** Check for errors
```bash
# Run with verbose output
python main.py

# Check any error messages in terminal
```

### Problem: Import fails with "Invalid Excel format"

**Solution:** Check Excel file
- Column names must match exactly (case-sensitive)
- No empty rows at top
- Save as `.xlsx` or `.xls` format
- Use UTF-8 encoding for Turkish characters

### Problem: Database errors

**Solution:** Reset database
1. Close application
2. Delete `database/exam_scheduler.db`
3. Restart application (database will be recreated)

### Problem: Slow performance

**Solution:** Check system resources
- Close other applications
- Check available RAM
- Reduce number of records
- Use SSD if possible

---

## 🔒 Security Setup

### Change Default Admin Password

1. Login with: `admin@gmail.com` / `admin123`
2. Go to Settings (if implemented)
3. Change password to a strong password
4. Logout and login with new password

**Note:** Password changing feature can be added in `src/ui/settings_view.py`

### Database Backup

**Manual Backup:**
```bash
# Copy database file
cp database/exam_scheduler.db database/backup_2025.db
```

**Automated Backup Script** (create `backup.py`):
```python
import shutil
from datetime import datetime

source = 'database/exam_scheduler.db'
backup = f'database/backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
shutil.copy2(source, backup)
print(f"Backup created: {backup}")
```

---

## 📂 Directory Setup

The application automatically creates:
```
exam-scheduler/
├── database/          # Created on first run
│   └── exam_scheduler.db
└── examples/          # Created by sample script
    ├── sample_courses.xlsx
    └── sample_students.xlsx
```

---

## 🔄 Updating the Application

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Update Database Schema
If database schema changes:
1. Backup existing database
2. Run migration script (if provided)
3. Or delete database and reimport data

---

## 🌐 Network/Firewall Setup

### For Local Use Only
- No network configuration needed
- SQLite database is file-based
- All data stored locally

### For Network Access (Future)
- Would require server setup
- Database migration to PostgreSQL/MySQL
- Network security configuration

---

## 💻 Development Setup

For developers who want to modify the code:

### Additional Tools
```bash
# Install development dependencies
pip install pylint black autopep8

# Code formatting
black src/

# Linting
pylint src/
```

### IDE Setup
- **VSCode**: Install Python extension
- **PyCharm**: Open project, set Python interpreter
- **Sublime Text**: Install Python packages

---

## ✅ Post-Installation Checklist

- [ ] Python 3.12+ installed
- [ ] All dependencies installed
- [ ] `verify_installation.py` passes all checks
- [ ] Application starts without errors
- [ ] Can login with default credentials
- [ ] Sample Excel files generated
- [ ] Can import sample data
- [ ] Can generate exam schedule
- [ ] Can export to PDF
- [ ] Documentation reviewed

---

## 📞 Getting Help

### Check Documentation
1. **README.md** - Overview and features
2. **QUICK_START.md** - Quick start guide
3. **FEATURES.md** - Detailed feature list
4. **PROJECT_STRUCTURE.md** - Code organization

### Common Issues
- Check GitHub Issues (if applicable)
- Review error messages carefully
- Run verification script
- Check Python version

### Support
- Course instructor
- Project documentation
- Python community forums

---

## 🎓 Learning Resources

### Python/PyQt6
- PyQt6 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- Python SQLite: https://docs.python.org/3/library/sqlite3.html
- pandas Documentation: https://pandas.pydata.org/docs/

### Application Concepts
- Database design
- UI/UX principles
- Algorithm optimization
- Software architecture

---

*Installation should take 5-10 minutes on a modern system with good internet connection.*

**Need more help? Check QUICK_START.md for usage guide!**



