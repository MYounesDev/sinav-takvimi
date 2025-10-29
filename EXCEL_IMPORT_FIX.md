# Excel Import Fix - display_id Issue

## Problem

After adding the `display_id` column to the database schema, Excel imports were failing because:

1. The `display_id` column is marked as `NOT NULL` in the schema
2. Import functions were using `INSERT ... ON CONFLICT` without providing a `display_id`
3. SQLite requires a value for all NOT NULL columns

## Root Cause

The import functions in `courses_view.py` and `students_view.py` were using:

```python
INSERT INTO courses (department_id, code, name, ...)
VALUES (?, ?, ?, ...)
ON CONFLICT(department_id, code) DO UPDATE SET ...
```

This worked before, but after adding `display_id` as a required field, SQLite throws an error:
```
NOT NULL constraint failed: courses.display_id
```

## Solution

Fixed three files to use the `get_next_display_id()` method before inserting records:

### 1. **courses_view.py** - Course Import
- Changed from `INSERT ... ON CONFLICT` to explicit check-then-insert/update
- Calls `db_manager.get_next_display_id('courses', department_id)` for new courses
- Updates existing courses without changing their `display_id`

### 2. **students_view.py** - Student Import  
- Changed from `INSERT ... ON CONFLICT` to explicit check-then-insert/update
- Calls `db_manager.get_next_display_id('students', department_id)` for new students
- Updates existing students without changing their `display_id`
- Removed redundant student_id lookup code

### 3. **classrooms_view.py** - Classroom Dialog
- Added `get_next_display_id('classrooms', department_id)` call when creating new classrooms
- This was also missing and would have caused issues when manually adding classrooms

## Changes Made

### Before (courses_view.py):
```python
query = """
    INSERT INTO courses (department_id, code, name, instructor, class_level, type)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(department_id, code) DO UPDATE SET ...
"""
db_manager.execute_update(query, (selected_dept_id, code, name, ...))
```

### After (courses_view.py):
```python
# Check if course already exists
check_query = "SELECT id FROM courses WHERE department_id = ? AND code = ?"
existing = db_manager.execute_query(check_query, (selected_dept_id, code))

if existing:
    # Update existing course
    query = "UPDATE courses SET name = ?, ... WHERE department_id = ? AND code = ?"
    db_manager.execute_update(query, (name, ..., selected_dept_id, code))
else:
    # Insert new course with display_id
    display_id = db_manager.get_next_display_id('courses', selected_dept_id)
    query = "INSERT INTO courses (display_id, department_id, code, ...) VALUES (?, ?, ?, ...)"
    db_manager.execute_update(query, (display_id, selected_dept_id, code, ...))
```

## Why This Approach?

1. **Explicit is better than implicit**: We now clearly separate insert vs update logic
2. **Proper display_id management**: New records get proper sequential display_ids per department
3. **Maintains existing records**: Updates don't create new display_ids
4. **Recycling support**: The `get_next_display_id()` method reuses deleted IDs when available

## Testing

To verify the fix works:

1. **Test Course Import**:
   ```
   - Create a test Excel file with courses
   - Import via "📥 Import from Excel" button
   - Verify courses are imported with proper display_ids
   ```

2. **Test Student Import**:
   ```
   - Create a test Excel file with students
   - Import via "📥 Import from Excel" button
   - Verify students are imported with proper display_ids
   ```

3. **Test Update Scenario**:
   ```
   - Import the same Excel file again
   - Verify existing records are updated (not duplicated)
   - Verify display_ids remain unchanged for existing records
   ```

4. **Test Classroom Creation**:
   ```
   - Manually add a new classroom via the UI
   - Verify it gets a proper display_id
   ```

## Additional Notes

- The `get_next_display_id()` method handles:
  - Recycling deleted IDs from the `deleted_ids` table
  - Finding the next sequential ID per department (for scoped tables)
  - Thread-safe operations with proper transaction handling

- Other dialogs (departments, users) were already using `get_next_display_id()` correctly

## Files Modified

1. `src/ui/courses_view.py` - Fixed `import_from_excel()` method
2. `src/ui/students_view.py` - Fixed `import_from_excel()` method  
3. `src/ui/classrooms_view.py` - Fixed `save()` method in ClassroomDialog

## Date

Fixed: October 29, 2025
