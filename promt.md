# Project Prompt: Dynamic Exam Scheduler System (PyQt6 + SQLite)

You are an AI software developer.  
Your task is to **create a complete desktop project** named **ExamScheduler** using **Python** and **PyQt6** for GUI, and **SQLite** for database management (no ORM — use only raw SQL queries).

This project is based on the “Dynamic Exam Scheduler System” specification from Kocaeli University’s Yazlab-1 project.  
You can refer to an existing folder called `ExamScheduler` to understand the initial structure and continue building upon it.

---

## 🔧 Technical Requirements

### General
- Programming Language: **Python 3.12+**
- GUI Framework: **PyQt6** (must look modern, animated, and well-styled)
- Database: **SQLite** (use only SQL statements, no ORM)
- File Handling: Excel parsing using `pandas` or `openpyxl`
- Output Formats: PDF and Excel exports using `reportlab` and `pandas`

## 🎨 UI & Experience

The interface must be **aesthetic and dynamic**, including:
- Rounded corners, soft colors, and responsive layouts.
- **Smooth animations and transitions** between screens (fade, slide, or scale effects).
- Animated loading indicators and hover effects.
- Custom message boxes and alert dialogs.
- A sidebar or top navigation for switching between modules.

Each screen should be implemented as a **QWidget class**, connected via stacked pages or stacked layouts.

---

## 👤 User Roles and Access

### Admin
- Can manage all departments, coordinators, classrooms, and global settings.
- Has full visibility of all data.

### Department Coordinator
- Can only view and manage data of their department.
- Handles classrooms, course imports, student imports, exam scheduling, and seating plan generation.

Login must be via **email + password**.  
Default admin user must be auto-created on first database initialization.

---

## 🧩 Core Functionalities

### 1. Login System
- Basic login screen with animations.
- Store hashed passwords in SQLite.
- After login:
- If Admin → open Admin Dashboard.
- If Coordinator → open Coordinator Dashboard.

### 2. Classroom Management
- Coordinator can add, edit, delete, and view classrooms.
- Fields: Department, Code, Name, Capacity, Rows, Columns, Seats per Desk.
- Visualize classroom layout with a **grid view animation**.
- Show search and filter by classroom code.

### 3. Course Import (Excel)
- Upload Excel with course code, name, instructor, class level, type (mandatory/elective).
- Parse and bulk-insert into database.
- Handle parsing errors and show animated warnings with detailed row info.

### 4. Student Import (Excel)
- Upload Excel with student number, name, class, and enrolled course codes.
- Parse and insert all records.
- Display list and allow searching by student number.

### 5. Exam Scheduling
- Allow user to set constraints:
- Date range
- Disabled days
- Exam duration (default 75 min)
- Break time (default 15 min)
- Conflict prevention toggle
- Generate optimized exam timetable using Python logic:
- No overlapping exams per student.
- Respect classroom capacity.
- Optimize classroom usage.
- Show the resulting exam schedule visually in a table or calendar.
- Allow exporting as Excel or PDF.

### 6. Seating Plan
- After scheduling, generate per-exam seating arrangements.
- Display each room’s layout visually with seat markers (student ID & name).
- Allow exporting seating plan to PDF.

### 7. Error & Warning Handling
- Use popup animations and clear messages such as:
- “Classroom capacity insufficient”
- “Exam overlap detected”
- “Invalid Excel format”

---

## 🗃️ Database Design (SQLite)

Tables (examples):
- `users(id, name, email, password, role, department)`
- `departments(id, name)`
- `classrooms(id, department_id, code, name, capacity, rows, cols, seats_per_desk)`
- `courses(id, department_id, code, name, instructor, class_level, type)`
- `students(id, student_no, name, class_level, department_id)`
- `student_courses(student_id, course_id)`
- `exams(id, course_id, date, start_time, duration, room_id, exam_type)`
- `exam_seating(id, exam_id, student_id, room_id, row, col)`

---

## 📤 Export Features
- Generate reports (PDF or Excel) for:
- Exam schedules
- Seating plans
- Course and student summaries

PDFs should include:
- University logo
- Styled tables
- Automatic file naming (e.g. `ExamSchedule_ComputerEng_2025.pdf`)

---

## 💡 Extra Features (Optional)
- Animated splash screen on startup.
- Dark/Light theme toggle.
- Auto-detect Excel headers and support Turkish characters.
- Tooltips and hover animations.
- Minimal loading spinner during data imports or scheduling.

---

## ✅ Output Expectation
The final generated project should:
- Be fully functional and runnable with `python main.py`.
- Include all modules with working navigation.
- Have beautiful UI with smooth transitions.
- Use SQLite with pure SQL queries.
- Contain clear comments and docstrings in every file.
- Store database file locally in the `database/` folder.
- Handle all specified requirements in the original Yazlab document. 