"""
Exam Schedule View - Generate and view exam schedules
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QDialog, QFormLayout, QDateEdit, QSpinBox, QCheckBox,
                             QMessageBox, QFrame, QGridLayout, QComboBox, QFileDialog)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from src.utils.scheduler import ExamScheduler
from src.utils.styles import Styles
from config import COLORS, DEFAULT_EXAM_DURATION, DEFAULT_BREAK_TIME
import pandas as pd


class ExamScheduleView(QWidget):
    """Exam scheduling view"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Top bar with actions
        top_bar = QHBoxLayout()
        
        title = QLabel("Exam Schedule")
        title.setStyleSheet(Styles.SUBTITLE_LABEL)
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        # Department filter (for admin only)
        user = get_current_user()
        if user and user['role'] == 'admin':
            dept_label = QLabel("Department:")
            dept_label.setStyleSheet(Styles.NORMAL_LABEL)
            top_bar.addWidget(dept_label)
            
            self.dept_filter = QComboBox()
            self.dept_filter.addItem("All Departments", None)
            self.dept_filter.setStyleSheet(Styles.COMBO_BOX)
            
            # Load departments
            departments = db_manager.execute_query("SELECT id, name, code FROM departments ORDER BY name")
            for dept in departments:
                self.dept_filter.addItem(f"{dept['name']} ({dept['code']})", dept['id'])
            
            self.dept_filter.currentIndexChanged.connect(self.load_schedule)
            top_bar.addWidget(self.dept_filter)
        
        # Generate schedule button
        generate_btn = QPushButton("⚙️ Generate Schedule")
        generate_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_btn.clicked.connect(self.show_schedule_dialog)
        top_bar.addWidget(generate_btn)
        
        # Export to Excel button
        export_excel_btn = QPushButton("📊 Export to Excel")
        export_excel_btn.setStyleSheet(Styles.SUCCESS_BUTTON)
        export_excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_excel_btn.clicked.connect(self.export_to_excel)
        top_bar.addWidget(export_excel_btn)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_schedule)
        top_bar.addWidget(refresh_btn)
        
        layout.addLayout(top_bar)
        
        # Table
        self.table = QTableWidget()
        user = get_current_user()
        # Add department column for admin
        headers = ["Date", "Time", "Course Code", "Course Name", "Exam Type", "Duration", "Students", "Classrooms"]
        if user and user['role'] == 'admin':
            headers.insert(4, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)  # Allow double-click editing
        self.table.itemChanged.connect(self.on_item_changed)  # Connect to handle changes
        layout.addWidget(self.table)
        
        # Clear button
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        clear_btn = QPushButton("🗑️ Clear Schedule")
        clear_btn.setStyleSheet(Styles.DANGER_BUTTON)
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_schedule)
        action_bar.addWidget(clear_btn)
        
        layout.addLayout(action_bar)
        
        # Load data
        self.load_schedule()
    
    def load_schedule(self):
        """Load exam schedule from database"""
        user = get_current_user()
        if not user:
            return
        
        # Re-initialize table structure based on actual logged-in user
        headers = ["Date", "Time", "Course Code", "Course Name", "Exam Type", "Duration", "Students", "Classrooms"]
        if user and user['role'] == 'admin':
            headers.insert(4, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Build department filter
        if user['role'] == 'admin':
            selected_dept_id = None
            if hasattr(self, 'dept_filter'):
                selected_dept_id = self.dept_filter.currentData()
            if selected_dept_id:
                dept_filter = "WHERE e.department_id = ?"
                params = (selected_dept_id,)
            else:
                dept_filter = ""
                params = ()
        else:
            dept_filter = "WHERE e.department_id = ?"
            params = (user['department_id'],)
        
        query = f"""
            SELECT e.*, c.code as course_code, c.name as course_name,
                   GROUP_CONCAT(cl.name, ', ') as classroom_names,
                   (SELECT COUNT(*) FROM student_courses sc WHERE sc.course_id = e.course_id) as student_count,
                   d.name as department_name, d.code as department_code
            FROM exams e
            JOIN courses c ON e.course_id = c.id
            LEFT JOIN exam_classrooms ec ON e.id = ec.exam_id
            LEFT JOIN classrooms cl ON ec.classroom_id = cl.id
            LEFT JOIN departments d ON e.department_id = d.id
            {dept_filter}
            GROUP BY e.id
            ORDER BY e.date, e.start_time
        """
        
        exams = db_manager.execute_query(query, params)
        user = get_current_user()  # Refresh user for column calculation
        
        # Temporarily disconnect signal to avoid triggering during population
        try:
            self.table.itemChanged.disconnect(self.on_item_changed)
        except:
            pass  # Signal might not be connected yet
        
        self.table.setRowCount(len(exams))
        
        for row, exam in enumerate(exams):
            col_idx = 0
            
            # Store exam ID in first column's UserRole
            date_item = QTableWidgetItem(exam['date'])
            date_item.setData(Qt.ItemDataRole.UserRole, exam['id'])  # Store exam ID
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Not editable
            self.table.setItem(row, col_idx, date_item)
            col_idx += 1
            
            time_item = QTableWidgetItem(exam['start_time'])
            time_item.setFlags(time_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col_idx, time_item)
            col_idx += 1
            
            code_item = QTableWidgetItem(exam['course_code'])
            code_item.setFlags(code_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col_idx, code_item)
            col_idx += 1
            
            name_item = QTableWidgetItem(exam['course_name'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col_idx, name_item)
            col_idx += 1
            
            # Add department column for admin
            if user and user['role'] == 'admin':
                dept_name = exam['department_name'] or 'N/A'
                dept_code = exam['department_code'] or ''
                dept_item = QTableWidgetItem(f"{dept_name} ({dept_code})")
                dept_item.setFlags(dept_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col_idx, dept_item)
                col_idx += 1
            
            # Exam type with proper display name
            exam_type = exam['exam_type'] if 'exam_type' in exam.keys() else 'final'
            exam_type_display = {
                'final': 'Final Exam',
                'midterm': 'Midterm Exam',
                'resit': 'Resit Exam'
            }.get(exam_type, 'Final Exam')
            type_item = QTableWidgetItem(exam_type_display)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col_idx, type_item)
            col_idx += 1
            
            # Duration - EDITABLE (store as integer for easy editing)
            duration_item = QTableWidgetItem(str(exam['duration']))
            duration_item.setToolTip("Double-click to edit duration (minutes)")
            self.table.setItem(row, col_idx, duration_item)
            col_idx += 1
            
            student_item = QTableWidgetItem(str(exam['student_count']))
            student_item.setFlags(student_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col_idx, student_item)
            col_idx += 1
            
            classroom_item = QTableWidgetItem(exam['classroom_names'] or "N/A")
            classroom_item.setFlags(classroom_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col_idx, classroom_item)
        
        # Reconnect signal
        self.table.itemChanged.connect(self.on_item_changed)
    
    def on_item_changed(self, item):
        """Handle when a table item is changed (for duration editing)"""
        user = get_current_user()
        
        # Determine which column is Duration based on user role
        if user and user['role'] == 'admin':
            duration_col = 6  # Date, Time, Code, Name, Department, Type, Duration
        else:
            duration_col = 5  # Date, Time, Code, Name, Type, Duration
        
        # Only process Duration column changes
        if item.column() != duration_col:
            return
        
        row = item.row()
        new_duration_text = item.text().strip()
        
        # Validate input is a positive integer
        try:
            new_duration = int(new_duration_text)
            if new_duration < 30 or new_duration > 180:
                raise ValueError("Duration must be between 30 and 180 minutes")
        except ValueError as e:
            # Disconnect signal before showing message to prevent triggering during reload
            try:
                self.table.itemChanged.disconnect(self.on_item_changed)
            except:
                pass
            
            QMessageBox.warning(
                self,
                "Invalid Duration",
                f"Please enter a valid duration (30-180 minutes):\n{str(e)}"
            )
            
            # Reload to reset the value
            self.load_schedule()
            return
        
        # Get exam ID from the first column
        exam_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        try:
            # Disconnect signal during update to prevent recursive calls
            try:
                self.table.itemChanged.disconnect(self.on_item_changed)
            except:
                pass
            
            # Update duration in database
            query = "UPDATE exams SET duration = ? WHERE id = ?"
            db_manager.execute_update(query, (new_duration, exam_id))
            
            # Reconnect signal
            self.table.itemChanged.connect(self.on_item_changed)
            
            # Show success message briefly
            QMessageBox.information(
                self,
                "Duration Updated",
                f"Exam duration updated to {new_duration} minutes"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Update Failed",
                f"Failed to update duration:\n{str(e)}"
            )
            # Reload to reset the value
            self.load_schedule()
    
    def show_schedule_dialog(self):
        """Show dialog to configure and generate schedule"""
        dialog = ScheduleConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_schedule()
    
    def export_to_excel(self):
        """Export schedule to Excel"""
        user = get_current_user()
        if not user:
            return
        
        # Build department filter based on user role
        if user['role'] == 'admin':
            dept_filter = ""
            params = ()
        else:
            dept_filter = "WHERE e.department_id = ?"
            params = (user['department_id'],)
        
        # Get schedule data
        query = f"""
            SELECT e.date, e.start_time, c.code as course_code, c.name as course_name,
                   e.duration, e.exam_type,
                   (SELECT COUNT(*) FROM student_courses sc WHERE sc.course_id = e.course_id) as students,
                   GROUP_CONCAT(cl.name, ', ') as classrooms
            FROM exams e
            JOIN courses c ON e.course_id = c.id
            LEFT JOIN exam_classrooms ec ON e.id = ec.exam_id
            LEFT JOIN classrooms cl ON ec.classroom_id = cl.id
            {dept_filter}
            GROUP BY e.id
            ORDER BY e.date, e.start_time
        """
        
        exams = db_manager.execute_query(query, params)
        
        if not exams:
            QMessageBox.warning(self, "No Data", "No exam schedule to export")
            return
        
        # Convert to DataFrame
        data = []
        for exam in exams:
            exam_type = exam['exam_type'] if 'exam_type' in exam.keys() else 'final'
            exam_type_display = {
                'final': 'Final Exam',
                'midterm': 'Midterm Exam',
                'resit': 'Resit Exam'
            }.get(exam_type, 'Final Exam')
            
            data.append({
                'Date': exam['date'],
                'Time': exam['start_time'],
                'Course Code': exam['course_code'],
                'Course Name': exam['course_name'],
                'Exam Type': exam_type_display,
                'Duration (min)': exam['duration'],
                'Students': exam['students'],
                'Classrooms': exam['classrooms'] or 'N/A'
            })
        
        df = pd.DataFrame(data)
        
        # Generate default filename
        if user['role'] == 'admin':
            dept_code = 'all'
        else:
            dept_code = user.get('department_code', 'dept')
        
        default_filename = f"exam_schedule_{dept_code}_{datetime.now().strftime('%Y%m%d')}.xlsx"
        
        # Open file dialog to choose save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Exam Schedule",
            default_filename,
            "Excel Files (*.xlsx);;All Files (*)"
        )
        
        if not file_path:  # User cancelled
            return
        
        # Ensure .xlsx extension
        if not file_path.lower().endswith('.xlsx'):
            file_path += '.xlsx'
        
        try:
            # Save to file
            df.to_excel(file_path, index=False)
            QMessageBox.information(self, "Export Successful", f"Schedule exported to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Failed to export schedule:\n{str(e)}")
    
    def clear_schedule(self):
        """Clear all scheduled exams"""
        reply = QMessageBox.question(
            self, "Confirm Clear",
            "Are you sure you want to clear the entire exam schedule?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            user = get_current_user()
            # For admin, delete filtered or all; for coordinator, only their department
            if user['role'] == 'admin':
                if hasattr(self, 'dept_filter'):
                    selected_dept_id = self.dept_filter.currentData()
                    if selected_dept_id:
                        db_manager.execute_update("DELETE FROM exams WHERE department_id = ?", (selected_dept_id,))
                    else:
                        db_manager.execute_update("DELETE FROM exams")
                else:
                    db_manager.execute_update("DELETE FROM exams")
            else:
                db_manager.execute_update("DELETE FROM exams WHERE department_id = ?", (user['department_id'],))
            self.load_schedule()


class ScheduleConfigDialog(QDialog):
    """Dialog for configuring exam schedule generation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Generate Exam Schedule")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Exam type
        self.exam_type_combo = QComboBox()
        self.exam_type_combo.addItem("Final Exam", "final")
        self.exam_type_combo.addItem("Midterm Exam", "midterm")
        self.exam_type_combo.addItem("Resit Exam", "resit")
        self.exam_type_combo.setStyleSheet(Styles.COMBO_BOX)
        form_layout.addRow("Exam Type:", self.exam_type_combo)
        
        # Start date
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate().addDays(7))
        form_layout.addRow("Start Date:", self.start_date_input)
        
        # End date
        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate().addDays(21))
        form_layout.addRow("End Date:", self.end_date_input)
        
        # Exam duration
        self.duration_input = QSpinBox()
        self.duration_input.setMinimum(30)
        self.duration_input.setMaximum(180)
        self.duration_input.setValue(DEFAULT_EXAM_DURATION)
        self.duration_input.setSuffix(" minutes")
        self.duration_input.setStyleSheet(Styles.SPIN_BOX)
        form_layout.addRow("Exam Duration:", self.duration_input)
        
        # Break time
        self.break_input = QSpinBox()
        self.break_input.setMinimum(0)
        self.break_input.setMaximum(60)
        self.break_input.setValue(DEFAULT_BREAK_TIME)
        self.break_input.setSuffix(" minutes")
        self.break_input.setStyleSheet(Styles.SPIN_BOX)
        form_layout.addRow("Break Time:", self.break_input)
        
        layout.addLayout(form_layout)
        
        # Disabled days
        days_label = QLabel("Exclude Days:")
        days_label.setStyleSheet(Styles.NORMAL_LABEL)
        layout.addWidget(days_label)
        
        days_frame = QFrame()
        days_layout = QGridLayout(days_frame)
        
        self.day_checkboxes = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for i, day in enumerate(days):
            cb = QCheckBox(day)
            if i >= 5:  # Default: exclude Saturday and Sunday
                cb.setChecked(True)
            self.day_checkboxes.append(cb)
            days_layout.addWidget(cb, i // 4, i % 4)
        
        layout.addWidget(days_frame)
        
        # Conflict prevention
        self.conflict_checkbox = QCheckBox("Prevent student exam conflicts")
        self.conflict_checkbox.setChecked(True)
        layout.addWidget(self.conflict_checkbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate")
        generate_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        generate_btn.clicked.connect(self.generate_schedule)
        button_layout.addWidget(generate_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def generate_schedule(self):
        """Generate the exam schedule"""
        start_date = self.start_date_input.date().toPyDate()
        end_date = self.end_date_input.date().toPyDate()
        duration = self.duration_input.value()
        break_time = self.break_input.value()
        prevent_conflicts = self.conflict_checkbox.isChecked()
        exam_type = self.exam_type_combo.currentData()  # Get selected exam type
        
        # Get disabled days
        disabled_days = [i for i, cb in enumerate(self.day_checkboxes) if cb.isChecked()]
        
        if start_date >= end_date:
            QMessageBox.warning(self, "Invalid Dates", "End date must be after start date")
            return
        
        user = get_current_user()
        
        # For admin, select department
        dept_id = user['department_id']
        if user['role'] == 'admin':
            from PyQt6.QtWidgets import QInputDialog
            departments = db_manager.execute_query("SELECT id, name, code FROM departments ORDER BY name")
            dept_items = [f"{dept['name']} ({dept['code']})" for dept in departments]
            dept_map = {f"{dept['name']} ({dept['code']})": dept['id'] for dept in departments}
            
            item, ok = QInputDialog.getItem(
                self, "Select Department", 
                "Select the department to generate schedule for:",
                dept_items, 0, False
            )
            if not ok:
                return
            dept_id = dept_map[item]
        
        try:
            # Create scheduler
            scheduler = ExamScheduler(dept_id)
            
            # Generate schedule
            scheduled_exams = scheduler.schedule_exams(
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.min.time()),
                disabled_days,
                duration,
                break_time,
                prevent_conflicts
            )
            
            if not scheduled_exams:
                QMessageBox.warning(self, "No Exams", "No courses found to schedule")
                return
            
            # Save schedule
            saved_count = scheduler.save_schedule(scheduled_exams, exam_type)
            
            QMessageBox.information(
                self, "Success",
                f"Successfully scheduled {saved_count} exams!"
            )
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate schedule:\n{str(e)}")


