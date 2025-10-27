# 📋 Changelog

## Version 1.1.0 - Auto-Refresh Update (October 22, 2025)

### 🎉 New Features

#### Auto-Refresh System
- ✅ **Automatic data refresh when switching tabs**
  - Every time you click a different tab, data is fetched fresh from database
  - No more stale data!

- ✅ **Window activation refresh**
  - When you switch back to the app from another program, data auto-refreshes
  - Perfect for multi-tasking!

- ✅ **F5 keyboard shortcut**
  - Press F5 anytime to manually refresh current tab
  - Quick and convenient!

- ✅ **Status bar with visual feedback**
  - See refresh status at the bottom of the window
  - Messages: "Refreshing...", "Updated", "Error", etc.
  - Auto-disappears after 2 seconds

#### Multi-Department Support
- ✅ **5 Engineering departments added**
  - Bilgisayar Mühendisliği (Computer Engineering)
  - Yazılım Mühendisliği (Software Engineering)
  - Elektrik Mühendisliği (Electrical Engineering)
  - Elektronik Mühendisliği (Electronics Engineering)
  - İnşaat Mühendisliği (Civil Engineering)

- ✅ **Department coordinators**
  - Each department has its own coordinator account
  - Login: `[department]@kocaeli.edu.tr` / `admin123`

#### Improved Classroom Management
- ✅ **Visual classroom preview**
  - See classroom layout while adding/editing
  - Real-time preview updates as you change rows/columns
  - Color-coded groups based on seats per desk
  - Shows desk positions (row, column)

- ✅ **Turkish interface improvements**
  - All buttons and labels in Turkish
  - Turkish error/success messages
  - Better user experience for Turkish users

### 🔧 Technical Improvements

- **Performance**: Only refreshes current tab (not all tabs)
- **Error Handling**: Graceful error messages in status bar
- **User Experience**: Visual feedback for all refresh operations
- **Multi-User Safe**: See changes from other coordinators immediately

### 🐛 Bug Fixes

- Fixed data not updating when switching between tabs
- Fixed stale data showing when other users make changes
- Improved database query performance

### 📚 Documentation

- Added `AUTO_REFRESH_GUIDE.md` - Complete guide to auto-refresh feature
- Added `CHANGELOG.md` - This file!

---

## Version 1.0.0 - Initial Release (October 22, 2025)

### Core Features

#### Authentication
- ✅ Secure login with bcrypt password hashing
- ✅ Role-based access (Admin, Coordinator)
- ✅ Default admin account auto-creation

#### Classroom Management
- ✅ Add, edit, delete classrooms
- ✅ Configure capacity, rows, columns
- ✅ Seats per desk configuration

#### Course Management
- ✅ Excel import for courses
- ✅ Bulk import with error handling
- ✅ Course types (mandatory/elective)

#### Student Management
- ✅ Excel import for students
- ✅ Automatic course enrollment
- ✅ Search and filter functionality

#### Exam Scheduling
- ✅ Intelligent scheduling algorithm
- ✅ Conflict prevention
- ✅ Classroom capacity optimization
- ✅ Configurable date ranges
- ✅ Export to Excel and PDF

#### Seating Plan
- ✅ Random seat assignment
- ✅ Multi-classroom support
- ✅ Visual layout view
- ✅ PDF export

#### UI/UX
- ✅ Modern, responsive design
- ✅ Smooth animations
- ✅ Intuitive navigation
- ✅ Custom styled components

---

## Upcoming Features (Roadmap)

### Planned for Next Release

- [ ] **Dark Theme** - Toggle between light and dark mode
- [ ] **User Settings** - Change password, preferences
- [ ] **Advanced Filters** - More filtering options in all views
- [ ] **Export Templates** - Customizable PDF templates
- [ ] **Email Notifications** - Send schedules to students
- [ ] **Audit Log** - Track all changes made by users
- [ ] **Backup/Restore** - Easy database backup and restore
- [ ] **Multi-Language** - Full English/Turkish support

### Under Consideration

- [ ] **Mobile App** - Companion mobile application
- [ ] **Web Interface** - Access via web browser
- [ ] **API** - REST API for integration
- [ ] **Analytics** - Usage statistics and reports
- [ ] **Cloud Sync** - Sync data across multiple installations

---

## Migration Guide

### From Version 1.0.0 to 1.1.0

**No migration needed!** Just update the files and run:

```bash
# Delete old database to get new departments
del database\exam_scheduler.db  # Windows
rm database/exam_scheduler.db   # Linux/Mac

# Run the app
python main.py
```

The database will be recreated with all new features!

---

## Known Issues

None currently! 🎉

If you find any bugs, please report them.

---

## Credits

**Developed for:** Kocaeli University  
**Project:** Yazlab-1 (Software Lab 1)  
**Technology Stack:**
- Python 3.12+
- PyQt6
- SQLite
- pandas
- ReportLab
- bcrypt

---

**Happy Scheduling! 🎓**

