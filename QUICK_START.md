# 🚀 Quick Start Guide

Get up and running with the Exam Scheduler in 5 minutes!

## Step 1: Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Step 2: First Login

Use the default admin credentials:
- **Email**: `admin@gmail.com`
- **Password**: `admin123`

## Step 3: Setup Your Department

### Add Classrooms

1. Click **"Classrooms"** in the sidebar
2. Click **"➕ Add Classroom"**
3. Fill in the details:
   - **Code**: e.g., "A101"
   - **Name**: e.g., "Amphitheater 101"
   - **Capacity**: Total number of students (e.g., 100)
   - **Rows**: Number of seat rows (e.g., 10)
   - **Columns**: Number of seat columns (e.g., 10)
   - **Seats per Desk**: Usually 1 or 2
4. Click **"Save"**

Repeat for all your exam rooms.

## Step 4: Import Courses

1. Click **"Courses"** in the sidebar
2. Prepare an Excel file with these columns:
   - `code` (required): Course code, e.g., "CS101"
   - `name` (required): Course name, e.g., "Programming"
   - `instructor` (optional): Instructor name
   - `class_level` (optional): Year level (1-4)
   - `type` (optional): "mandatory" or "elective"

3. Click **"📥 Import from Excel"**
4. Select your Excel file
5. Review import results

**Sample file**: See `examples/sample_courses.csv`

## Step 5: Import Students

1. Click **"Students"** in the sidebar
2. Prepare an Excel file with these columns:
   - `student_no` (required): Student number, e.g., "20210001"
   - `name` (required): Student name
   - `class_level` (optional): Year level
   - `course_codes` (optional): Comma-separated course codes, e.g., "CS101,CS102"

3. Click **"📥 Import from Excel"**
4. Select your Excel file
5. Students will be enrolled in specified courses automatically

**Sample file**: See `examples/sample_students.csv`

## Step 6: Generate Exam Schedule

1. Click **"Exam Schedule"** in the sidebar
2. Click **"⚙️ Generate Schedule"**
3. Configure settings:
   - **Start Date**: First exam day
   - **End Date**: Last exam day
   - **Exam Duration**: Usually 75 minutes
   - **Break Time**: Between exams (15 minutes)
   - **Exclude Days**: Check weekends or holidays
   - **Prevent Conflicts**: ✅ Recommended!

4. Click **"Generate"**
5. Review the generated schedule
6. Export to Excel or PDF if needed

## Step 7: Create Seating Plans

1. Click **"Seating Plan"** in the sidebar
2. Select an exam from the dropdown
3. Click **"⚙️ Generate Seating"**
4. Click **"👁️ View Layout"** to see visual classroom arrangement
5. Click **"📄 Export to PDF"** to save seating plan

## 📊 Tips & Tricks

### Best Practices

✅ **Add classrooms first** - You need them for scheduling
✅ **Import courses before students** - For course enrollment
✅ **Use CSV instead of XLSX** - Better compatibility
✅ **Check for conflicts** - Enable conflict prevention in scheduling
✅ **Backup your database** - Copy `database/exam_scheduler.db`

### Excel File Tips

- Save as `.xlsx` or `.xls` format
- First row must be column headers (exact names)
- No empty rows at the top
- Use UTF-8 encoding for Turkish characters
- Course codes in student import must match exactly

### Common Workflows

**Scenario 1: Re-schedule all exams**
1. Go to Exam Schedule
2. Click "Clear Schedule"
3. Click "Generate Schedule" with new settings

**Scenario 2: Add more students mid-semester**
1. Prepare Excel with new students
2. Import (existing students will be updated)
3. Re-generate seating plans

**Scenario 3: Change classroom**
1. Edit classroom details in Classrooms view
2. Re-generate exam schedule
3. Re-generate seating plans

## 🔧 Troubleshooting

### "No classrooms available"
→ Add at least one classroom before scheduling

### "Invalid Excel format"
→ Check column names match exactly (case-sensitive)

### Import shows errors
→ Review the error list, fix those rows, re-import

### Students not enrolled in courses
→ Make sure course codes match exactly
→ Import courses first, then students

### Seating plan is empty
→ Generate schedule first
→ Make sure students are enrolled in courses
→ Generate seating for each exam

## 📞 Need Help?

1. Check the full [README.md](README.md)
2. Review [sample Excel files](examples/)
3. Reset database if needed: delete `database/exam_scheduler.db`

---

**Happy Scheduling! 🎓**



