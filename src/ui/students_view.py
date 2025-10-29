"""
Students View - Manage students and import from Excel
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QFileDialog, QMessageBox, QProgressDialog, QLineEdit, QComboBox)
from PyQt6.QtCore import Qt
import pandas as pd
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from src.utils.styles import Styles


class StudentsView(QWidget):
    """Students management view with Excel import"""
    
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
        
        title = QLabel("Student Management")
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
            
            self.dept_filter.currentIndexChanged.connect(self.load_students)
            top_bar.addWidget(self.dept_filter)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by student number or name...")
        self.search_input.setStyleSheet(Styles.LINE_EDIT)
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.filter_students)
        top_bar.addWidget(self.search_input)
        
        # Import from Excel button
        import_btn = QPushButton("📥 Import from Excel")
        import_btn.setStyleSheet(Styles.SUCCESS_BUTTON)
        import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        import_btn.clicked.connect(self.import_from_excel)
        top_bar.addWidget(import_btn)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_students)
        top_bar.addWidget(refresh_btn)
        
        layout.addLayout(top_bar)
        
        # Table
        self.table = QTableWidget()
        user = get_current_user()
        # Add department column for admin
        headers = ["ID", "Student No", "Name", "Class Level", "Enrolled Courses"]
        if user and user['role'] == 'admin':
            headers.insert(3, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Action buttons
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        delete_btn = QPushButton("🗑️ Delete Selected")
        delete_btn.setStyleSheet(Styles.DANGER_BUTTON)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_student)
        action_bar.addWidget(delete_btn)
        
        clear_all_btn = QPushButton("🗑️ Clear All")
        clear_all_btn.setStyleSheet(Styles.DANGER_BUTTON)
        clear_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_all_btn.clicked.connect(self.clear_all_students)
        action_bar.addWidget(clear_all_btn)
        
        layout.addLayout(action_bar)
        
        # Store all students for filtering
        self.all_students = []
        
        # Load data
        self.load_students()
    
    def load_students(self):
        """Load students from database"""
        user = get_current_user()
        if not user:
            return
        
        # Re-initialize table structure based on actual logged-in user
        headers = ["ID", "Student No", "Name", "Class Level", "Enrolled Courses"]
        if user and user['role'] == 'admin':
            headers.insert(3, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Build department filter
        if user['role'] == 'admin':
            selected_dept_id = None
            if hasattr(self, 'dept_filter'):
                selected_dept_id = self.dept_filter.currentData()
            if selected_dept_id:
                dept_filter = f"WHERE s.department_id = {selected_dept_id}"
            else:
                dept_filter = ""
        else:
            dept_filter = f"WHERE s.department_id = {user['department_id']}"
        
        query = f"""
            SELECT s.id, s.student_no, s.name, s.class_level,
                   COUNT(sc.course_id) as course_count,
                   s.department_id, d.name as department_name, d.code as department_code
            FROM students s
            LEFT JOIN student_courses sc ON s.id = sc.student_id
            LEFT JOIN departments d ON s.department_id = d.id
            {dept_filter}
            GROUP BY s.id, s.student_no, s.name, s.class_level, s.department_id, d.name, d.code
            ORDER BY s.student_no
        """
        
        self.all_students = list(db_manager.execute_query(query))
        self.display_students(self.all_students)
    
    def display_students(self, students):
        """Display students in table"""
        self.table.setRowCount(len(students))
        user = get_current_user()
        
        for row, student in enumerate(students):
            col_idx = 0
            self.table.setItem(row, col_idx, QTableWidgetItem(str(student['id'])))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(student['student_no']))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(student['name']))
            col_idx += 1
            
            # Add department column for admin
            if user and user['role'] == 'admin':
                dept_name = student['department_name'] or 'N/A'
                dept_code = student['department_code'] or ''
                self.table.setItem(row, col_idx, QTableWidgetItem(f"{dept_name} ({dept_code})"))
                col_idx += 1
            
            self.table.setItem(row, col_idx, QTableWidgetItem(str(student['class_level']) if student['class_level'] else ""))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(str(student['course_count'])))
    
    def filter_students(self):
        """Filter students based on search input"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self.display_students(self.all_students)
            return
        
        filtered = [s for s in self.all_students 
                   if search_text in s['student_no'].lower() or search_text in s['name'].lower()]
        
        self.display_students(filtered)
    
    def _normalize_turkish_students(self, df):
        """Normalize Turkish student format to standard format
        Turkish format is in long format: one row per student-course pair
        Need to convert to wide format: one row per student with all courses
        """
        # Turkish column name mappings
        column_map = {
            'Öğrenci No': 'student_no',
            'öğrenci no': 'student_no',
            'ÖĞRENCI NO': 'student_no',
            'Ad Soyad': 'name',
            'ad soyad': 'name',
            'AD SOYAD': 'name',
            'İsim': 'name',
            'isim': 'name',
            'Sınıf': 'class_level_str',
            'sınıf': 'class_level_str',
            'SINIF': 'class_level_str',
            'Ders': 'course_code',
            'ders': 'course_code',
            'DERS': 'course_code',
            'Ders Kodu': 'course_code',
            'ders kodu': 'course_code',
        }
        
        # Rename columns based on mapping
        new_columns = {}
        for col in df.columns:
            col_str = str(col).strip()
            if col_str in column_map:
                new_columns[col] = column_map[col_str]
        
        df = df.rename(columns=new_columns)
        
        # Clean up the dataframe
        df = df.dropna(how='all')
        
        # If we have the long format (student_no, name, course_code per row)
        if 'student_no' in df.columns and 'course_code' in df.columns:
            # Extract class level from class_level_str (e.g., "1. Sınıf" -> 1)
            if 'class_level_str' in df.columns:
                df['class_level'] = df['class_level_str'].astype(str).str.extract(r'(\d+)')[0]
                df['class_level'] = pd.to_numeric(df['class_level'], errors='coerce')
            
            # Group by student and aggregate courses
            grouped = df.groupby(['student_no', 'name']).agg({
                'class_level': 'first',  # Take the first class level
                'course_code': lambda x: ','.join(x.dropna().astype(str))  # Combine all courses
            }).reset_index()
            
            # Rename course_code column to course_codes
            grouped = grouped.rename(columns={'course_code': 'course_codes'})
            
            return grouped
        
        return df
    
    def import_from_excel(self):
        """Import students from Excel file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if not file_path:
            return
        
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Check if it's Turkish format (Ogrenci listesi.xlsx)
            turkish_columns = ['Öğrenci No', 'Ad Soyad', 'Sınıf', 'Ders']
            if any(col in df.columns for col in turkish_columns):
                df = self._normalize_turkish_students(df)
            
            # Expected columns: student_no, name, class_level, course_codes (comma-separated)
            required_columns = ['student_no', 'name']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                QMessageBox.warning(
                    self, "Invalid Format",
                    f"Missing required columns: {', '.join(missing_columns)}\n\n"
                    "Expected columns: student_no, name, class_level (optional), course_codes (optional, comma-separated)\n\n"
                    "Or Turkish format with columns: Öğrenci No, Ad Soyad, Sınıf, Ders"
                )
                return
            
            user = get_current_user()
            
            # For admin, show department selection dialog
            selected_dept_id = user['department_id']
            if user['role'] == 'admin':
                from PyQt6.QtWidgets import QInputDialog
                departments = db_manager.execute_query("SELECT id, name, code FROM departments ORDER BY name")
                dept_items = [f"{dept['name']} ({dept['code']})" for dept in departments]
                dept_map = {f"{dept['name']} ({dept['code']})": dept['id'] for dept in departments}
                
                item, ok = QInputDialog.getItem(
                    self, "Select Department", 
                    "Select the department for these students:",
                    dept_items, 0, False
                )
                if not ok:
                    return
                selected_dept_id = dept_map[item]
            
            # Show progress dialog
            progress = QProgressDialog("Importing students...", "Cancel", 0, len(df), self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            
            imported_count = 0
            errors = []
            
            for index, row in df.iterrows():
                if progress.wasCanceled():
                    break
                
                try:
                    student_no = str(row['student_no']).strip()
                    name = str(row['name']).strip()
                    class_level = int(row.get('class_level', 0)) if pd.notna(row.get('class_level')) else None
                    course_codes_str = str(row.get('course_codes', '')).strip() if pd.notna(row.get('course_codes')) else ""
                    
                    # Insert or update student
                    query = """
                        INSERT INTO students (department_id, student_no, name, class_level)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(student_no) DO UPDATE SET
                        name = excluded.name,
                        class_level = excluded.class_level
                    """
                    
                    student_id = db_manager.execute_update(query, (
                        selected_dept_id, student_no, name, class_level
                    ))
                    
                    # If course codes are provided, enroll student
                    if course_codes_str and student_id:
                        # Get the student id if it was an update
                        if not student_id:
                            result = db_manager.execute_query("SELECT id FROM students WHERE student_no = ?", (student_no,))
                            if result:
                                student_id = result[0]['id']
                        
                        course_codes = [c.strip() for c in course_codes_str.split(',') if c.strip()]
                        
                        for course_code in course_codes:
                            # Find course by code - for admin, search across all departments; for coordinator, only their department
                            if user['role'] == 'admin':
                                course_query = "SELECT id FROM courses WHERE code = ?"
                                course_result = db_manager.execute_query(course_query, (course_code,))
                            else:
                                course_query = "SELECT id FROM courses WHERE code = ? AND department_id = ?"
                                course_result = db_manager.execute_query(course_query, (course_code, user['department_id']))
                            
                            if course_result:
                                # Enroll student in course
                                enroll_query = """
                                    INSERT OR IGNORE INTO student_courses (student_id, course_id)
                                    VALUES (?, ?)
                                """
                                db_manager.execute_update(enroll_query, (student_id, course_result[0]['id']))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
                
                progress.setValue(index + 1)
            
            progress.close()
            
            # Show results
            message = f"Successfully imported {imported_count} students."
            if errors:
                message += f"\n\nErrors encountered:\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    message += f"\n... and {len(errors) - 10} more errors"
            
            QMessageBox.information(self, "Import Complete", message)
            self.load_students()
            
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import Excel file:\n{str(e)}")
    
    def delete_student(self):
        """Delete selected student"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a student to delete")
            return
        
        student_id = int(self.table.item(row, 0).text())
        student_name = self.table.item(row, 2).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete student '{student_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM students WHERE id = ?"
            db_manager.execute_update(query, (student_id,))
            self.load_students()
    
    def clear_all_students(self):
        """Clear all students"""
        reply = QMessageBox.question(
            self, "Confirm Clear All",
            "Are you sure you want to delete ALL students? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            user = get_current_user()
            # For admin, delete filtered or all; for coordinator, only their department
            if user['role'] == 'admin' :
                if hasattr(self, 'dept_filter'):
                    selected_dept_id = self.dept_filter.currentData()
                    if selected_dept_id is not None:
                        query = "DELETE FROM students WHERE department_id = ?"
                        db_manager.execute_update(query, (selected_dept_id,))
                    else:
                        query = "DELETE FROM students"
                        db_manager.execute_update(query)
                else:
                    query = "DELETE FROM students"
                    db_manager.execute_update(query)
            else:
                query = "DELETE FROM students WHERE department_id = ?"
                db_manager.execute_update(query, (user['department_id'],))
            
            # Clear the table before reloading to avoid dataChanged warnings
            self.table.setRowCount(0)
            self.all_students = []
            self.load_students()


