# Database Migration Guide - ID Reuse Feature

## Overview

This guide explains the database migration that enables ID reuse when rows are deleted. After this migration, when you delete a row with ID=34 and then insert a new row, the new row will get ID=34 instead of continuing to the next available ID (35, 36, etc.).

## What Changed?

### Before Migration
- All tables used `INTEGER PRIMARY KEY AUTOINCREMENT`
- SQLite's AUTOINCREMENT prevents ID reuse
- Deleted IDs are never reused, IDs always increase

### After Migration
- All tables now use `INTEGER PRIMARY KEY` (without AUTOINCREMENT)
- SQLite will reuse the lowest available ID
- When you delete row with ID=34, that ID becomes available again

## Migration Instructions

### For Existing Databases

If you have an existing database with data:

1. **Backup your database** (automatically done by the migration script)
2. **Run the migration script:**
   ```bash
   python migrate_database.py
   ```

The migration script will:
- Create a backup of your database (`exam_scheduler_backup.db`)
- Recreate all tables without AUTOINCREMENT
- Copy all existing data to new tables
- Preserve all relationships and data integrity
- Recreate all indexes

### For New Installations

No migration needed! The updated database schema will be used automatically when you initialize the database.

## Safety Features

1. **Automatic Backup**: The migration creates a backup before making any changes
2. **Transaction Safety**: All changes are wrapped in a transaction and rolled back if any error occurs
3. **Data Preservation**: All existing data is copied to new tables
4. **Index Recreation**: All indexes are recreated for optimal performance

## Affected Tables

All tables in the database are migrated:
- `users`
- `departments`
- `classrooms`
- `courses`
- `students`
- `student_courses`
- `exams`
- `exam_classrooms`
- `exam_seating`

## Example: ID Reuse Behavior

### Before Migration (WITH AUTOINCREMENT)
```
Insert row -> ID=1
Insert row -> ID=2
Insert row -> ID=3
Delete ID=3 (max ID)
Insert row -> ID=4  (ID=3 is NEVER reused, even though it was the max)
Delete ALL rows
Insert row -> ID=5  (IDs continue counting, never reset)
```

### After Migration (WITHOUT AUTOINCREMENT)
```
Insert row -> ID=1
Insert row -> ID=2
Insert row -> ID=3
Delete ID=3 (max ID)
Insert row -> ID=3  (ID=3 is reused!)
Delete ALL rows
Insert row -> ID=1  (IDs reset and start from 1)
```

### Important Notes

- **Maximum ID Reuse**: When the highest ID is deleted, it will be reused for the next insert
- **Clear All Behavior**: When all rows are deleted, new rows will start from ID=1 again
- **Middle ID Reuse**: SQLite may not immediately reuse middle IDs (e.g., ID=2 when max is 5), but they become available for reuse
- **Key Benefit**: The "Clear All" button will properly reset IDs to start from 1

## Clear All Feature

A new "Clear All" button has been added to the Classrooms page that allows you to delete all classrooms at once. This feature respects department permissions:
- **Coordinators**: Can only clear classrooms in their department
- **Administrators**: Can clear all classrooms

## Rollback

If you need to rollback the migration:

1. Stop the application
2. Delete the current `exam_scheduler.db`
3. Rename `exam_scheduler_backup.db` to `exam_scheduler.db`
4. Restart the application

## Technical Details

### SQLite ID Allocation

When using `INTEGER PRIMARY KEY` without AUTOINCREMENT:
- SQLite uses the ROWID as the primary key
- Deleted ROWIDs become available for reuse
- The smallest unused ROWID is assigned to new rows
- This is the default SQLite behavior and is very efficient

### Performance

- No performance degradation expected
- ID reuse can actually improve performance for databases with many delete operations
- All indexes are preserved and recreated during migration

## Troubleshooting

### Migration Fails
- Check that the database file is not locked by another process
- Ensure you have write permissions to the database directory
- Review the error message and backup file location

### Data Inconsistency After Migration
- Restore from the backup file
- Report the issue with details about your data
- Wait for an updated migration script

## Questions?

If you encounter any issues during migration, please:
1. Check the backup file is created successfully
2. Review the migration output for specific error messages
3. Keep the backup file safe before attempting the migration again

