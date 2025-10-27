# ✨ Features Documentation

Comprehensive guide to all features in the Exam Scheduler System.

## 🔐 Authentication & Security

### Login System
- **Email + Password** authentication
- **Bcrypt** password hashing (industry standard)
- **Session management** with global state
- **Auto-logout** on window close
- **Default admin account** created on first run

### Security Features
- ✅ Passwords stored as hashed values
- ✅ SQL injection prevention (parameterized queries)
- ✅ Role-based access control (RBAC)
- ✅ Department-level data isolation

### User Roles

#### 👨‍💼 Admin
- Full system access
- Manage all departments
- View all data across departments
- Create coordinator accounts
- System-wide settings

#### 👨‍🏫 Coordinator
- Department-specific access
- Manage classrooms, courses, students
- Generate exam schedules
- Create seating plans
- Export reports for their department

---

## 🏫 Classroom Management

### Features
- ✅ Add, edit, delete classrooms
- ✅ Configure room layout (rows × columns)
- ✅ Set seats per desk (1-3 students)
- ✅ Define total capacity
- ✅ Unique classroom codes
- ✅ Visual layout preview

### Classroom Properties
- **Code**: Unique identifier (e.g., "A101", "LAB-B")
- **Name**: Descriptive name
- **Capacity**: Maximum students
- **Rows**: Number of seat rows
- **Columns**: Seats per row
- **Seats/Desk**: Students sharing each desk

### Use Cases
1. **Regular Classroom**: 10 rows × 10 cols × 1 seat = 100 capacity
2. **Lab**: 5 rows × 8 cols × 2 seats = 80 capacity
3. **Amphitheater**: 15 rows × 12 cols × 1 seat = 180 capacity

---

## 📖 Course Management

### Excel Import
- ✅ Bulk import from Excel files
- ✅ Update existing courses
- ✅ Error reporting per row
- ✅ Progress indicator
- ✅ Turkish character support

### Required Fields
- **code**: Unique course code
- **name**: Course name

### Optional Fields
- **instructor**: Professor/teacher name
- **class_level**: Year (1-4)
- **type**: "mandatory" or "elective"

### Import Process
1. Prepare Excel with required columns
2. Click "Import from Excel"
3. Select file
4. Review import summary
5. Fix any errors and re-import if needed

### Validation
- Duplicate codes are updated (not duplicated)
- Invalid types are set to NULL
- Missing optional fields are allowed
- Progress shown for large files

---

## 👨‍🎓 Student Management

### Excel Import
- ✅ Bulk import students
- ✅ Automatic course enrollment
- ✅ Update existing records
- ✅ Search by student number or name

### Required Fields
- **student_no**: Unique student number
- **name**: Student full name

### Optional Fields
- **class_level**: Year (1-4)
- **course_codes**: Comma-separated course codes

### Course Enrollment
- Students auto-enrolled when course_codes provided
- Course codes must match existing courses
- Many-to-many relationship (students ↔ courses)

### Search & Filter
- Real-time search box
- Filter by student number or name
- Case-insensitive search

### Example Import
```csv
student_no,name,class_level,course_codes
20210001,Ahmet Yılmaz,2,"CS101,CS102,CS201"
```

---

## 📅 Exam Scheduling

### Intelligent Algorithm

#### Features
- ✅ **Conflict prevention**: No student has overlapping exams
- ✅ **Capacity optimization**: Assigns classrooms based on enrollment
- ✅ **Flexible scheduling**: Configure date range, time slots
- ✅ **Exclude days**: Skip weekends, holidays
- ✅ **Multi-classroom support**: Large courses span multiple rooms

#### Configuration Options

**Date Range**
- Start date (first exam day)
- End date (last exam day)

**Timing**
- Exam duration (default: 75 minutes)
- Break time between exams (default: 15 minutes)

**Constraints**
- Exclude specific weekdays (e.g., Saturday, Sunday)
- Conflict prevention toggle
- Available time slots (4 per day: 09:00, 11:00, 14:00, 16:00)

#### Scheduling Algorithm

1. **Load Data**: Get all courses, students, enrollments
2. **Sort Courses**: By student count (largest first)
3. **Generate Time Slots**: Based on date range and excluded days
4. **Assign Slots**: 
   - Check student conflicts
   - Find earliest conflict-free slot
   - Assign classroom(s) based on capacity
5. **Save Schedule**: Store in database

#### Example Scenario
- **Input**: 10 courses, 100 students, 5 classrooms
- **Constraints**: No weekends, prevent conflicts
- **Output**: Optimized schedule over 2 weeks

### Schedule Display
- Sortable table view
- Shows: Date, Time, Course, Duration, Students, Rooms
- Export to Excel or PDF

---

## 💺 Seating Plan Generation

### Features
- ✅ Random seat assignment (anti-cheating)
- ✅ Multi-classroom distribution
- ✅ Visual layout view
- ✅ PDF export with professional formatting
- ✅ Per-exam seating plans

### Generation Process
1. Select an exam
2. Click "Generate Seating"
3. Students randomly shuffled
4. Distributed across assigned classrooms
5. Seats filled row-by-row, column-by-column

### Classroom Layout View
- Grid visualization
- Each desk shows student info
- Empty seats shown in grey
- Color-coded for clarity

### Seating Assignment Logic
```python
for classroom in assigned_classrooms:
    for row in range(classroom.rows):
        for col in range(classroom.cols):
            for seat_pos in range(1, seats_per_desk + 1):
                assign_student(next_student)
```

### PDF Export
- Professional formatting
- University branding
- Exam details header
- Sortable by classroom/seat
- Auto-generated filename

---

## 📊 Export & Reports

### Excel Export
- **Exam Schedule**: Full timetable
- **Seating List**: All students with seat assignments
- **Student Lists**: Enrolled students per course

### PDF Export
- **Exam Schedule**: Professional calendar view
- **Seating Plan**: Per-exam seating with layout
- Custom formatting with ReportLab
- University header and footer

### File Naming
- Auto-generated names with timestamps
- Format: `{type}_{department}_{date}.{ext}`
- Examples:
  - `exam_schedule_CS_20251022.pdf`
  - `seating_plan_CS101_20251022.pdf`

---

## 🎨 User Interface

### Design Principles
- **Modern**: Rounded corners, soft shadows
- **Responsive**: Adapts to window size
- **Intuitive**: Clear navigation, consistent layout
- **Animated**: Smooth transitions, loading indicators

### Animations
- **Fade in/out**: View transitions
- **Slide**: Sidebar navigation
- **Bounce**: Error feedback
- **Scale**: Button hover effects
- **Progress**: Loading bars for long operations

### Color Scheme
- **Primary**: Blue (#4A90E2) - Actions, headers
- **Secondary**: Purple (#7B68EE) - Accents
- **Success**: Green (#52C41A) - Confirmations
- **Danger**: Red (#FF4D4F) - Deletions, errors
- **Warning**: Orange (#FAAD14) - Warnings
- **Dark**: Navy (#2C3E50) - Sidebar, headers
- **Light**: Off-white (#F5F7FA) - Backgrounds

### Components
- **Buttons**: 3 styles (primary, secondary, danger)
- **Tables**: Striped rows, hover effects
- **Forms**: Labeled inputs, validation
- **Cards**: Statistics, information panels
- **Dialogs**: Modal windows for forms

---

## 📱 Dashboard

### Statistics Cards
- **Classrooms**: Total count
- **Courses**: Total count
- **Students**: Total enrolled
- **Exams**: Total scheduled

### Real-time Updates
- Refreshes on data changes
- Department-filtered for coordinators
- System-wide for admins

---

## 🔔 Error Handling

### User Feedback
- **Success messages**: Green confirmation dialogs
- **Warnings**: Yellow alert dialogs
- **Errors**: Red error dialogs with details

### Import Error Handling
- Row-by-row error tracking
- Shows first 10 errors
- Error count summary
- Allows partial imports

### Validation
- Empty field checks
- Format validation
- Duplicate prevention
- Capacity warnings

---

## ⚙️ Configuration

### Customizable Settings (config.py)
- **Colors**: Full color scheme
- **Timing**: Default exam duration, break time
- **Limits**: Max file size for imports
- **Paths**: Database location
- **UI**: Window size, animation duration

### Example Customization
```python
# Change primary color
COLORS["primary"] = "#FF5733"

# Change default exam duration
DEFAULT_EXAM_DURATION = 90  # 90 minutes

# Change animation speed
ANIMATION_DURATION = 500  # milliseconds
```

---

## 🚀 Performance

### Optimization
- **Database indexes**: Fast queries on common fields
- **Bulk imports**: Batch inserts for Excel data
- **Lazy loading**: Load data only when needed
- **Connection pooling**: Efficient database connections

### Scalability
- Handles 1000+ students
- Supports 100+ courses
- Multiple classrooms per exam
- Large Excel files (progress indicators)

---

## 🛠️ Advanced Features

### Conflict Detection
- Checks if student has multiple exams at same time
- Prevents scheduling conflicts automatically
- Can be toggled on/off

### Classroom Optimization
- Assigns smallest sufficient classroom first
- Distributes large courses across multiple rooms
- Maximizes room utilization

### Multi-classroom Exams
- Automatically splits large courses
- Maintains seating plan across rooms
- Exports combined seating PDF

---

## 🎯 Future Enhancements

### Planned Features
- [ ] Email notifications to students
- [ ] QR code seat assignments
- [ ] Mobile app for viewing schedules
- [ ] Analytics dashboard
- [ ] Historical data tracking
- [ ] Theme toggle (dark/light mode)
- [ ] Multi-language support

---

*All features designed with user experience and efficiency in mind.*



