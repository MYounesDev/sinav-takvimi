# 🔄 Auto-Refresh Feature Guide

## Overview

The Exam Scheduler now automatically refreshes data from the database to ensure you always see the most up-to-date information!

## ✨ Features

### 1. **Automatic Tab Refresh**
Every time you switch between tabs (Dashboard, Classrooms, Courses, etc.), the data is automatically refreshed from the database.

**Example:**
1. You're on the "Courses" tab
2. Another coordinator adds a new course
3. You switch to "Students" tab
4. When you come back to "Courses", you'll see the new course!

### 2. **Window Activation Refresh**
When you switch back to the Exam Scheduler window from another application, the current tab's data is automatically refreshed.

**Example:**
1. You have Exam Scheduler open on "Classrooms" tab
2. You switch to Excel to prepare data
3. When you click back on Exam Scheduler window, data refreshes automatically!

### 3. **Manual Refresh (F5)**
Press **F5** at any time to manually refresh the current tab's data.

**Keyboard Shortcut:** `F5`

### 4. **Visual Status Indicator**
A status bar at the bottom of the window shows refresh status:

- 🔄 **"Refreshing data..."** - Data is being loaded
- ✅ **"Dashboard updated"** - Data successfully refreshed  
- ❌ **"Error refreshing data"** - Something went wrong
- **"Ready | Press F5 to refresh"** - Default status

## 📊 What Gets Refreshed?

| Tab | Data Refreshed |
|-----|----------------|
| **Dashboard** | Statistics (classrooms, courses, students, exams counts) |
| **Classrooms** | All classroom records |
| **Courses** | All course records |
| **Students** | All student records and enrollments |
| **Exam Schedule** | All scheduled exams |
| **Seating Plan** | Exam list and current seating arrangements |

## 🎯 Use Cases

### Multi-User Scenario
**Problem:** Coordinator A adds classrooms while Coordinator B is working on courses.

**Solution:** When Coordinator B switches tabs or presses F5, they'll see Coordinator A's new classrooms immediately!

### Data Import Scenario
**Problem:** You import students from Excel, but the dashboard still shows old count.

**Solution:** Switch to Dashboard tab or press F5, and you'll see updated student count!

### Window Switching Scenario
**Problem:** You're working with external tools (Excel, database viewer) and making changes.

**Solution:** Click back to Exam Scheduler window, and it auto-refreshes to show your changes!

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **F5** | Refresh current tab |

## 💡 Tips

1. **No Need to Click Refresh Button:** The old refresh buttons still work, but now they're optional!

2. **Multi-Monitor Setup:** If you have Exam Scheduler on one monitor and data sources on another, just click back to the Exam Scheduler window to refresh.

3. **Status Messages:** Watch the status bar (bottom of window) to confirm data has been refreshed.

4. **Performance:** Refreshing is fast! It only loads data for the current tab, not all tabs.

## 🔧 Technical Details

### When Does Auto-Refresh Trigger?

1. **Tab Switch:** Every time you click a different navigation button
2. **Window Activation:** When the window gains focus (you click on it)
3. **Manual:** When you press F5

### What Happens During Refresh?

```
1. Status bar shows "🔄 Refreshing data..."
2. Database query executes for current tab
3. Table/UI updates with fresh data
4. Status bar shows "✅ [Tab] updated" for 2 seconds
5. Status returns to "Ready | Press F5 to refresh"
```

### Error Handling

If refresh fails:
- ❌ Error message shown in status bar for 5 seconds
- Error details printed to console
- Old data remains visible (not cleared)

## 🎨 Visual Indicators

### Status Bar Messages

| Message | Meaning | Duration |
|---------|---------|----------|
| 🔄 Refreshing data... | Loading from database | Until complete |
| 🔄 Manual refresh (F5)... | You pressed F5 | Until complete |
| ✅ Dashboard updated | Dashboard refreshed successfully | 2 seconds |
| ✅ Classrooms updated | Classrooms refreshed | 2 seconds |
| ✅ Courses updated | Courses refreshed | 2 seconds |
| ✅ Students updated | Students refreshed | 2 seconds |
| ✅ Exam schedule updated | Schedule refreshed | 2 seconds |
| ✅ Seating plan updated | Seating refreshed | 2 seconds |
| ❌ Error refreshing data | Refresh failed | 5 seconds |
| Ready \| Press F5 to refresh | Idle state | Permanent |

## 🚀 Benefits

✅ **Always Current:** No stale data, ever!  
✅ **Multi-User Safe:** See changes from other coordinators  
✅ **No Manual Action Needed:** Happens automatically  
✅ **Performance Optimized:** Only refreshes current tab  
✅ **User Friendly:** Visual feedback via status bar  
✅ **Flexible:** Auto + manual refresh options  

## 📝 Examples

### Example 1: Importing Data
```
1. Import courses from Excel
2. Import shows "50 courses imported"
3. Switch to Dashboard tab
4. Dashboard automatically refreshes
5. Status bar: "✅ Dashboard updated"
6. Dashboard now shows correct course count!
```

### Example 2: Multi-User Collaboration
```
Coordinator A (Computer Engineering):
- Adds 3 new classrooms at 10:00 AM

Coordinator B (Software Engineering):
- Working on exam schedule at 10:00 AM
- Switches to Classrooms tab at 10:05 AM
- Automatically sees A's 3 new classrooms!
- Can now use them for scheduling
```

### Example 3: External Updates
```
1. You're viewing Students list
2. Database is updated externally (via another tool)
3. You press F5
4. Students list refreshes with new data
5. Status bar confirms: "✅ Students updated"
```

## 🔍 Troubleshooting

**Q: Data not refreshing?**
- A: Try pressing F5 manually
- Check status bar for error messages
- Verify database connection

**Q: Too many refreshes?**
- A: Auto-refresh only happens on tab switch and window focus
- It's designed to be non-intrusive

**Q: Want to disable auto-refresh?**
- A: Currently not configurable, but you can ignore it
- Manual refresh (F5) always available

## 🎓 Best Practices

1. **Trust the Auto-Refresh:** Don't manually click refresh buttons unless needed
2. **Watch Status Bar:** Confirm your actions via status messages
3. **Use F5 When Needed:** For immediate refresh without tab switching
4. **Multi-Monitor Friendly:** Works great with external data sources

---

**Made with ❤️ for Kocaeli University**

*Last Updated: October 2025*

