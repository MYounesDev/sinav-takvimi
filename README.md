# 📚 Exam Scheduler System

A modern, feature-rich desktop application for managing exam schedules, classroom assignments, and seating plans.

Built for **Kocaeli University** - Yazlab-1 Project

## ✨ Features

### 🔐 User Management
- Role-based access control (Admin & Department Coordinator)
- Secure password hashing with bcrypt
- Beautiful animated login screen

### 🏫 Classroom Management
- Add, edit, and delete classrooms
- Configure capacity, rows, columns, and seats per desk
- Visual classroom layout preview

### 📖 Course Management
- Import courses from Excel files
- Bulk import with error handling
- Support for course types (mandatory/elective)

### 👨‍🎓 Student Management
- Import students from Excel with course enrollments
- Search and filter functionality
- Automatic course enrollment

### 📅 Intelligent Exam Scheduling
- Automated exam scheduling with conflict prevention
- Configurable date ranges and time slots
- Exclude specific days (weekends, holidays)
- Optimal classroom assignment based on capacity
- Export to Excel and PDF

### 💺 Seating Plan Generation
- Automatic random seating arrangement
- Visual classroom layout view
- Export seating plans to PDF
- Per-classroom seating visualization

### 🎨 Modern UI/UX
- Beautiful, responsive design with animations
- Smooth transitions and fade effects
- Custom styled components
- Intuitive navigation with sidebar
- **Auto-refresh** - Data automatically updates when switching tabs
- **F5 shortcut** - Manual refresh with keyboard
- **Status bar** - Visual feedback for all operations

## 🔧 Technical Stack

- **Language**: Python 3.12+
- **GUI Framework**: PyQt6
- **Database**: SQLite (pure SQL, no ORM)
- **Excel Handling**: pandas, openpyxl
- **PDF Generation**: ReportLab
- **Security**: bcrypt for password hashing

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Setup

1. **Clone or download the project**
   ```bash
   cd exam-scheduler
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 🚀 Quick Start

### First Login

On first run, the application automatically creates a default admin account:

- **Email**: `admin@gmail.com`
- **Password**: `admin123`

⚠️ **Important**: Change the default password after first login!

### Basic Workflow

1. **Login** with admin credentials
2. **Add Classrooms** - Define your available exam rooms
3. **Import Courses** - Upload Excel file with course data
4. **Import Students** - Upload Excel file with student enrollments
5. **Generate Schedule** - Configure and auto-generate exam timetable
6. **Create Seating** - Generate seating arrangements for each exam
7. **Export** - Download PDF/Excel reports

## 📊 Excel Import Formats

### Courses Import

Create an Excel file with these columns:

| code | name | instructor | class_level | type |
|------|------|------------|-------------|------|
| CS101 | Programming I | Dr. Smith | 1 | mandatory |
| CS102 | Data Structures | Dr. Johnson | 2 | elective |

**Required columns**: `code`, `name`  
**Optional columns**: `instructor`, `class_level`, `type`

### Students Import

Create an Excel file with these columns:

| student_no | name | class_level | course_codes |
|------------|------|-------------|--------------|
| 20210001 | John Doe | 2 | CS101,CS102,CS201 |
| 20210002 | Jane Smith | 1 | CS101,CS103 |

**Required columns**: `student_no`, `name`  
**Optional columns**: `class_level`, `course_codes` (comma-separated)

Sample Excel templates are provided in the `examples/` folder.

## 🗂️ Project Structure

```
exam-scheduler/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── database/             # SQLite database storage
├── src/
│   ├── database/
│   │   └── db_manager.py  # Database operations
│   ├── ui/
│   │   ├── main_window.py        # Main application window
│   │   ├── login_view.py         # Login screen
│   │   ├── dashboard_view.py     # Dashboard
│   │   ├── classrooms_view.py    # Classroom management
│   │   ├── courses_view.py       # Course management
│   │   ├── students_view.py      # Student management
│   │   ├── exam_schedule_view.py # Exam scheduling
│   │   └── seating_plan_view.py  # Seating arrangements
│   ├── utils/
│   │   ├── auth.py          # Authentication
│   │   ├── scheduler.py     # Scheduling algorithm
│   │   ├── seating.py       # Seating generation
│   │   ├── pdf_export.py    # PDF export utilities
│   │   ├── styles.py        # UI styling
│   │   └── animations.py    # UI animations
│   └── models/             # Data models
└── examples/              # Sample Excel files
```

## 🎯 Key Features in Detail

### Exam Scheduling Algorithm

The intelligent scheduling algorithm:
- ✅ Prevents student exam conflicts (optional)
- ✅ Respects classroom capacities
- ✅ Optimizes classroom utilization
- ✅ Distributes exams across available time slots
- ✅ Excludes weekends and holidays

### Seating Plan Generation

Features:
- 🎲 Random seat assignment to prevent cheating
- 🏫 Multi-classroom support
- 📊 Visual layout preview
- 📄 Professional PDF export

## 🔒 Security

- Passwords are hashed using bcrypt
- SQL injection prevention with parameterized queries
- Role-based access control
- Department-level data isolation

## 📝 Database Schema

The application uses SQLite with the following main tables:

- `users` - User accounts and roles
- `departments` - Academic departments
- `classrooms` - Exam rooms and capacities
- `courses` - Course information
- `students` - Student records
- `student_courses` - Course enrollments
- `exams` - Scheduled exams
- `exam_classrooms` - Classroom assignments
- `exam_seating` - Seating arrangements

## 🎨 UI Customization

Colors and styling can be customized in `config.py`:

```python
COLORS = {
    "primary": "#4A90E2",
    "secondary": "#7B68EE",
    "success": "#52C41A",
    # ... more colors
}
```

## 🐛 Troubleshooting

### Database Issues
- Delete `database/exam_scheduler.db` to reset the database
- The database will be recreated on next run

### Import Errors
- Ensure Excel files have required columns
- Check for Turkish character encoding (UTF-8)
- Verify date formats

### Display Issues
- Update graphics drivers
- Try running with `--disable-gpu` flag
- Check screen resolution and DPI settings

## 📄 License

This project is developed for educational purposes as part of Kocaeli University's Yazlab-1 course.

## 👥 Support

For issues and questions:
- Check the documentation
- Review sample Excel files in `examples/`
- Contact your course instructor

## 🚀 Future Enhancements

Potential improvements:
- [ ] Multi-language support (Turkish/English)
- [ ] Dark theme toggle
- [ ] Email notifications
- [ ] Conflict detection reports
- [ ] Historical data analytics
- [ ] Mobile companion app

---

**Made with ❤️ for Kocaeli University**

*Version 1.0.0 - 2025*

