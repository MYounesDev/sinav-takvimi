# Quick Migration Instructions

## 🎯 What's New?

1. ✅ **Clear All button** added to Classrooms page
2. ✅ **ID Reuse** enabled - deleted IDs can now be reused

## 🚀 How to Apply Changes

### Step 1: Backup (Optional but Recommended)
The migration script automatically creates a backup, but you can manually backup too:
```bash
# Navigate to database folder and copy the database
copy database\exam_scheduler.db database\exam_scheduler_manual_backup.db
```

### Step 2: Run Migration
```bash
python migrate_database.py
```

You should see output like:
```
============================================================
DATABASE MIGRATION: Enabling ID Reuse
============================================================
✓ Database backup created: database/exam_scheduler_backup.db

Migrating table: users
  ✓ Created temporary table: users_new
  ✓ Copied X rows
  ✓ Dropped old table
  ✓ Renamed table

... (continues for all tables)

Recreating indexes...
  ✓ Indexes recreated

============================================================
✓ MIGRATION COMPLETED SUCCESSFULLY!
============================================================
```

### Step 3: Test (Optional)
Run the test script to see ID reuse in action:
```bash
python test_id_reuse.py
```

### Step 4: Run Your Application
```bash
python main.py
# or
run.bat
```

## 🔍 Verify Changes

1. **Clear All Button**: 
   - Login to the application
   - Navigate to Classrooms page
   - You should see "🗑️ Clear All" button next to the Delete button

2. **ID Reuse**:
   - Add 3 classrooms (they get IDs 1, 2, 3)
   - Click "Clear All"
   - Add a new classroom
   - It should get ID=1 (not ID=4!)

## ⚠️ Important Notes

- **One-time operation**: You only need to run the migration once
- **Automatic backup**: The script creates `exam_scheduler_backup.db`
- **Safe to re-run**: If migration fails, it rolls back automatically
- **New installations**: Don't need migration, just start using the app

## 🔄 Rollback (if needed)

If something goes wrong:
```bash
# Stop the application first
# Then restore from backup:
del database\exam_scheduler.db
rename database\exam_scheduler_backup.db exam_scheduler.db
# Restart the application
```

## 📖 More Information

- **Complete guide**: See `DATABASE_MIGRATION_GUIDE.md`
- **Changes summary**: See `CHANGES_SUMMARY.md`
- **Test demonstration**: Run `python test_id_reuse.py`

## ❓ FAQ

**Q: Do I have to migrate?**
A: Not immediately, but you won't get the new features without it.

**Q: Will I lose data?**
A: No, all data is preserved. A backup is created automatically.

**Q: What if migration fails?**
A: The script will rollback changes. Your backup file is safe.

**Q: Can I skip migration on a fresh install?**
A: Yes! Fresh installations automatically use the new schema.

**Q: What's the difference in behavior?**
A: Main difference is when you delete all records and add new ones, IDs start from 1 again instead of continuing to increment forever.

---

**Ready to migrate?** Just run: `python migrate_database.py`

