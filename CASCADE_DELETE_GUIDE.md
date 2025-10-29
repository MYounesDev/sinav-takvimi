# CASCADE DELETE Guide

## Overview

All foreign key relationships in the database now use `ON DELETE CASCADE`. This means when you delete a record, all related records are automatically deleted as well.

## What Changed?

### Before
- Deleting a department would fail if it had related users, courses, students, or classrooms
- Foreign key constraints would prevent deletion
- You had to manually delete all related records first

### After
- Deleting a department automatically deletes all related records
- No foreign key constraint violations
- Cascading deletes handle everything automatically

## CASCADE Delete Relationships

### Department Deletions
When you delete a department, the following are automatically deleted:

1. **All Users** in that department
2. **All Courses** in that department
3. **All Students** in that department
4. **All Classrooms** in that department
5. **All Exams** for that department
6. **All Related Records**:
   - `student_courses` (when course is deleted)
   - `exam_classrooms` (when exam is deleted)
   - `exam_seating` (when exam or student is deleted)

### Classroom Deletions
When you delete a classroom, the following are automatically deleted:

1. **All `exam_classrooms`** records referencing that classroom
2. **All `exam_seating`** records referencing that classroom

### Course Deletions
When you delete a course, the following are automatically deleted:

1. **All `exams`** for that course
2. **All `student_courses`** records for that course
3. **All `exam_classrooms`** (when exam is deleted)
4. **All `exam_seating`** (when exam is deleted)

### Student Deletions
When you delete a student, the following are automatically deleted:

1. **All `student_courses`** records for that student
2. **All `exam_seating`** records for that student

### Exam Deletions
When you delete an exam, the following are automatically deleted:

1. **All `exam_classrooms`** records for that exam
2. **All `exam_seating`** records for that exam

## Example Scenarios

### Scenario 1: Delete Department
```
Before:
  - Department: CS (ID=1)
  - Users: 5 users with department_id=1
  - Courses: 10 courses with department_id=1
  - Students: 100 students with department_id=1
  - Classrooms: 8 classrooms with department_id=1
  - Exams: 20 exams with department_id=1

Action: DELETE FROM departments WHERE id = 1

After:
  - Department: 0 records
  - Users: 0 records (all 5 deleted)
  - Courses: 0 records (all 10 deleted)
  - Students: 0 records (all 100 deleted)
  - Classrooms: 0 records (all 8 deleted)
  - Exams: 0 records (all 20 deleted)
  - All related records in exam_classrooms, exam_seating, student_courses deleted
```

### Scenario 2: Delete Classroom with Exams
```
Before:
  - Classroom: C101 (ID=10)
  - exam_classrooms: 5 records with classroom_id=10
  - exam_seating: 150 records with classroom_id=10

Action: DELETE FROM classrooms WHERE id = 10

After:
  - Classroom: 0 records
  - exam_classrooms: 0 records (all 5 deleted)
  - exam_seating: 0 records (all 150 deleted)
```

## Important Notes

### ⚠️ Warning: Irreversible Operations
CASCADE deletes are **permanent and cannot be undone**. When you delete a department:

- All data in that department is permanently removed
- There is no automatic backup (make your own backups!)
- The deletion propagates through all related tables

### Best Practices

1. **Backup First**: Always backup your database before deleting departments or large records
2. **Confirmation Dialogs**: The UI should show confirmation dialogs for destructive operations
3. **Verify Relationships**: Check what will be deleted before confirming
4. **Use Transaction Logs**: Consider logging deletions for audit purposes

### Testing

Run the test script to verify CASCADE deletes work correctly:

```bash
python test_cascade_deletes.py
```

This will:
- Create test data
- Delete a department
- Verify all related records were automatically deleted

## Migration

If you have an existing database, run the migration script:

```bash
python migrate_database.py
```

This will:
- Add CASCADE to all foreign key constraints
- Preserve all existing data
- Enable cascading deletes

## Technical Details

### Foreign Key Constraints Updated

All foreign keys now include `ON DELETE CASCADE`:

```sql
-- Before
FOREIGN KEY (department_id) REFERENCES departments(id)

-- After
FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
```

### SQLite Foreign Keys

SQLite foreign key constraints must be enabled for CASCADE to work. This is automatically enabled in `db_manager.py`:

```python
conn.execute("PRAGMA foreign_keys = ON")
```

### Deletion Order

SQLite automatically handles the deletion order based on foreign key dependencies:

1. Child records are deleted first (exam_seating, exam_classrooms, student_courses)
2. Parent records are deleted last (departments, courses, students, classrooms)

You don't need to worry about deletion order - SQLite handles it.

## Rollback

If you need to rollback CASCADE deletes:

1. Stop the application
2. Restore from your backup
3. Or run the migration script again (but this won't restore deleted data)

**Remember**: CASCADE deletes are permanent. Always backup before major deletions!

## Benefits

1. **Simplified Deletion**: No need to manually delete related records
2. **Data Integrity**: Foreign keys ensure consistency
3. **Automatic Cleanup**: Related records are automatically removed
4. **No Orphaned Data**: Prevents orphaned records from remaining in the database

## Questions?

If you have questions about CASCADE deletes:
- Check the test script: `test_cascade_deletes.py`
- Review the database schema in `src/database/db_manager.py`
- Test in a development environment first

