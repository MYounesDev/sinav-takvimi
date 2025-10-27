# 📁 Project Structure

Complete overview of the Exam Scheduler project structure and file organization.

## 🌳 Directory Tree

```
exam-scheduler/
│
├── 📄 main.py                      # Application entry point
├── 📄 config.py                    # Configuration settings
├── 📄 requirements.txt             # Python dependencies
├── 📄 install.py                   # Installation script
├── 📄 create_sample_excel.py       # Sample file generator
├── 📄 run.bat                      # Windows launcher
├── 📄 run.sh                       # Linux/Mac launcher
│
├── 📚 README.md                    # Main documentation
├── 📚 QUICK_START.md               # Quick start guide
├── 📚 PROJECT_STRUCTURE.md         # This file
├── 📄 .gitignore                   # Git ignore rules
│
├── 📁 database/                    # Database storage
│   └── exam_scheduler.db           # SQLite database (auto-created)
│
├── 📁 examples/                    # Sample Excel files
│   ├── sample_courses.xlsx         # Course import template
│   ├── sample_courses.csv          # Course CSV template
│   ├── sample_students.xlsx        # Student import template
│   └── sample_students.csv         # Student CSV template
│
└── 📁 src/                         # Source code
    ├── __init__.py
    │
    ├── 📁 database/                # Database layer
    │   ├── __init__.py
    │   └── db_manager.py           # Database operations & schema
    │
    ├── 📁 ui/                      # User interface
    │   ├── __init__.py
    │   ├── splash_screen.py        # Animated splash screen
    │   ├── main_window.py          # Main application window
    │   ├── login_view.py           # Login screen
    │   ├── dashboard_view.py       # Dashboard with statistics
    │   ├── classrooms_view.py      # Classroom management
    │   ├── courses_view.py         # Course management & import
    │   ├── students_view.py        # Student management & import
    │   ├── exam_schedule_view.py   # Exam scheduling
    │   └── seating_plan_view.py    # Seating plan generation
    │
    ├── 📁 utils/                   # Utilities
    │   ├── __init__.py
    │   ├── auth.py                 # Authentication & session
    │   ├── scheduler.py            # Exam scheduling algorithm
    │   ├── seating.py              # Seating plan generator
    │   ├── pdf_export.py           # PDF export utilities
    │   ├── styles.py               # UI styling definitions
    │   └── animations.py           # Animation helpers
    │
    └── 📁 models/                  # Data models (future use)
        └── __init__.py
```

## 📦 Core Modules

### Main Application
- **main.py**: Entry point, initializes app and shows splash screen
- **config.py**: Central configuration (colors, defaults, paths)

### Database Layer
- **db_manager.py**: 
  - SQLite connection management
  - Database schema creation
  - Query execution helpers
  - Initial data seeding

### User Interface

#### Core Windows
- **splash_screen.py**: Animated startup screen
- **main_window.py**: Main window with sidebar navigation
- **login_view.py**: User authentication screen

#### Feature Views
- **dashboard_view.py**: Statistics overview
- **classrooms_view.py**: CRUD operations for classrooms
- **courses_view.py**: Course management & Excel import
- **students_view.py**: Student management & Excel import
- **exam_schedule_view.py**: Exam scheduling configuration
- **seating_plan_view.py**: Seating arrangement visualization

### Business Logic

#### Authentication
- **auth.py**:
  - Password hashing (bcrypt)
  - Login validation
  - Session management
  - User creation

#### Scheduling
- **scheduler.py**:
  - Exam scheduling algorithm
  - Conflict detection
  - Classroom assignment
  - Time slot generation

#### Seating
- **seating.py**:
  - Random seat assignment
  - Multi-classroom distribution
  - Seating data retrieval

#### Export
- **pdf_export.py**:
  - Exam schedule PDF generation
  - Seating plan PDF generation
  - Professional formatting with ReportLab

### UI Utilities
- **styles.py**: Centralized styling (buttons, inputs, tables)
- **animations.py**: Fade, slide, scale, bounce animations

## 🗄️ Database Schema

### Core Tables

**users**
- User accounts (admin, coordinator)
- Password hashing
- Department association

**departments**
- Department information
- Department codes

**classrooms**
- Exam room details
- Capacity and layout (rows, cols, seats)

**courses**
- Course information
- Instructor, level, type

**students**
- Student records
- Class levels

**student_courses**
- Course enrollments (many-to-many)

### Exam Tables

**exams**
- Scheduled exams
- Date, time, duration

**exam_classrooms**
- Classroom assignments per exam

**exam_seating**
- Student seat assignments
- Row, column, position

## 🔄 Data Flow

### Import Flow
```
Excel File → pandas → Validation → SQLite → UI Refresh
```

### Scheduling Flow
```
Configure Parameters → Load Data → Algorithm → 
Save Schedule → Generate Seating → Export PDF
```

### Authentication Flow
```
Login Form → Hash Password → Check Database → 
Set Session → Show Dashboard
```

## 🎨 UI Architecture

### Layout Structure
```
MainWindow
├── Sidebar (Navigation)
│   ├── Logo
│   ├── Nav Buttons (Checkable)
│   └── Logout Button
│
└── Content Area
    ├── Top Bar
    │   ├── Page Title
    │   └── User Info
    │
    └── Stacked Widget (Pages)
        ├── Dashboard
        ├── Classrooms
        ├── Courses
        ├── Students
        ├── Exam Schedule
        └── Seating Plan
```

### State Management
- **Global**: Current user session (src/utils/auth.py)
- **Local**: View-specific state in each view class
- **Database**: Persistent state in SQLite

## 🚀 Execution Flow

1. **Startup** (main.py)
   - Initialize Qt Application
   - Show splash screen
   - Initialize database
   - Load main window

2. **Database Init** (db_manager.py)
   - Create tables if not exist
   - Create default admin if needed
   - Set up indexes

3. **Login** (login_view.py)
   - Show login form
   - Validate credentials
   - Set current user
   - Navigate to dashboard

4. **Main App** (main_window.py)
   - Setup navigation
   - Load initial view
   - Handle page switching

5. **Feature Operations**
   - Load data from database
   - Display in tables/forms
   - Handle user actions
   - Update database
   - Refresh views

## 📝 File Naming Conventions

- **Python files**: lowercase_with_underscores.py
- **Classes**: PascalCase
- **Functions**: snake_case
- **Constants**: UPPER_CASE
- **Private methods**: _leading_underscore

## 🔧 Configuration Files

**requirements.txt**
- Python package dependencies
- Version specifications

**.gitignore**
- Excludes database, generated files
- Keeps example files

**run.bat / run.sh**
- Quick launchers for different platforms

## 📊 Data Files

**Excel Templates**
- `.xlsx` format for actual imports
- `.csv` format for reference
- Column specifications documented

**Generated Files**
- PDF exports (exam schedules, seating plans)
- Excel exports
- Auto-named with timestamps

## 🎯 Best Practices Used

✅ **Separation of Concerns**: UI, Logic, Data layers  
✅ **DRY Principle**: Reusable utilities and components  
✅ **Type Hints**: Function signatures documented  
✅ **Docstrings**: All functions documented  
✅ **Error Handling**: Try-catch blocks for I/O operations  
✅ **Security**: Password hashing, SQL injection prevention  
✅ **User Experience**: Animations, feedback, validation  

## 🔮 Extension Points

Want to add features? Here's where:

- **New UI View**: Add to `src/ui/`, register in `main_window.py`
- **New Algorithm**: Add to `src/utils/`
- **New Export Format**: Extend `pdf_export.py`
- **Database Changes**: Update schema in `db_manager.py`
- **New Role**: Add to auth system in `auth.py`

---

*This structure is designed for maintainability, scalability, and ease of understanding.*



