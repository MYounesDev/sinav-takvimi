"""
Courses View - Manage courses and import from Excel
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QFileDialog, QMessageBox, QProgressDialog, QComboBox, QLineEdit, QDialog)
from PyQt6.QtCore import Qt
import pandas as pd
import re
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from src.utils.styles import Styles
from config import ALLOWED_EXCEL_EXTENSIONS

class CoursesView(QWidget):
    """Courses management view with Excel import"""
    
    def __init__(self):
        super().__init__()
        self.all_courses = []  
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        top_bar = QHBoxLayout()
        
        title = QLabel("Course Management")
        title.setStyleSheet(Styles.SUBTITLE_LABEL)
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        user = get_current_user()
        if user and user['role'] == 'admin':
            dept_label = QLabel("Department:")
            dept_label.setStyleSheet(Styles.NORMAL_LABEL)
            top_bar.addWidget(dept_label)
            
            self.dept_filter = QComboBox()
            self.dept_filter.addItem("All Departments", None)
            self.dept_filter.setStyleSheet(Styles.COMBO_BOX)
            
            departments = db_manager.execute_query("SELECT id, name, code FROM departments ORDER BY name")
            for dept in departments:
                self.dept_filter.addItem(f"{dept['name']} ({dept['code']})", dept['id'])
            
            self.dept_filter.currentIndexChanged.connect(self.load_courses)
            top_bar.addWidget(self.dept_filter)
        
        import_btn = QPushButton("📥 Import from Excel")
        import_btn.setStyleSheet(Styles.SUCCESS_BUTTON)
        import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        import_btn.clicked.connect(self.import_from_excel)
        top_bar.addWidget(import_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_courses)
        top_bar.addWidget(refresh_btn)
        
        layout.addLayout(top_bar)
        
        search_bar = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        search_label.setStyleSheet(Styles.NORMAL_LABEL)
        search_bar.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID, Code, Name, or Instructor...")
        self.search_input.setStyleSheet(Styles.LINE_EDIT)
        self.search_input.textChanged.connect(self.filter_courses)
        search_bar.addWidget(self.search_input)
        
        layout.addLayout(search_bar)
        
        self.table = QTableWidget()
        user = get_current_user()
        headers = ["ID", "Code", "Name", "Instructor", "Class Level", "Type", "Status"]
        if user and user['role'] == 'admin':
            headers.insert(3, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)  
        layout.addWidget(self.table)
        
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        view_btn = QPushButton("👁️ View Details")
        view_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.clicked.connect(self.view_course_details)
        action_bar.addWidget(view_btn)
        
        toggle_btn = QPushButton("🔄 Toggle Active/Inactive")
        toggle_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        toggle_btn.clicked.connect(self.toggle_course_status)
        action_bar.addWidget(toggle_btn)
        
        delete_btn = QPushButton("🗑️ Delete Selected")
        delete_btn.setStyleSheet(Styles.DANGER_BUTTON)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_course)
        action_bar.addWidget(delete_btn)
        
        clear_all_btn = QPushButton("🗑️ Clear All")
        clear_all_btn.setStyleSheet(Styles.DANGER_BUTTON)
        clear_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_all_btn.clicked.connect(self.clear_all_courses)
        action_bar.addWidget(clear_all_btn)
        
        layout.addLayout(action_bar)
        
        self.load_courses()
    
    def load_courses(self):
        """Load courses from database"""
        user = get_current_user()
        if not user:
            return
        
        headers = ["ID", "Code", "Name", "Instructor", "Class Level", "Type", "Status"]
        if user and user['role'] == 'admin':
            headers.insert(3, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        if user['role'] == 'admin':
            selected_dept_id = None
            if hasattr(self, 'dept_filter'):
                selected_dept_id = self.dept_filter.currentData()
            if selected_dept_id:
                dept_filter = f"WHERE c.department_id = {selected_dept_id}"
            else:
                dept_filter = ""
        else:
            dept_filter = f"WHERE c.department_id = {user['department_id']}"
        
        query = f"""
            SELECT c.id, c.display_id, c.code, c.name, c.instructor, c.class_level, c.type, c.isActive,
                   c.department_id, d.name as department_name, d.code as department_code
            FROM courses c
            LEFT JOIN departments d ON c.department_id = d.id
            {dept_filter}
            ORDER BY c.display_id
        """
        
        courses = db_manager.execute_query(query)
        self.all_courses = courses  
        self.populate_table(courses)
    
    def populate_table(self, courses):
        """Populate table with course data"""
        user = get_current_user()
        
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(courses))
        
        for row, course in enumerate(courses):
            col_idx = 0
            
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.DisplayRole, int(course['display_id']))
            id_item.setData(Qt.ItemDataRole.UserRole, course['id'])  
            self.table.setItem(row, col_idx, id_item)
            col_idx += 1
            
            self.table.setItem(row, col_idx, QTableWidgetItem(course['code']))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(course['name']))
            col_idx += 1
            
            if user and user['role'] == 'admin':
                dept_name = course['department_name'] or 'N/A'
                dept_code = course['department_code'] or ''
                self.table.setItem(row, col_idx, QTableWidgetItem(f"{dept_name} ({dept_code})"))
                col_idx += 1
            
            self.table.setItem(row, col_idx, QTableWidgetItem(course['instructor'] or ""))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(str(course['class_level']) if course['class_level'] else ""))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(course['type'] or ""))
            col_idx += 1
            
            status_text = "✅ Active" if course['isActive'] else "❌ Inactive"
            status_item = QTableWidgetItem(status_text)
            if not course['isActive']:
                status_item.setForeground(Qt.GlobalColor.red)
            self.table.setItem(row, col_idx, status_item)
        
        self.table.setSortingEnabled(True)
    
    def filter_courses(self):
        """Filter courses based on search text"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self.populate_table(self.all_courses)
            return
        
        filtered = []
        for course in self.all_courses:
            if (str(course['display_id']).lower().find(search_text) != -1 or
                course['code'].lower().find(search_text) != -1 or
                course['name'].lower().find(search_text) != -1 or
                (course['instructor'] and course['instructor'].lower().find(search_text) != -1)):
                filtered.append(course)
        
        self.populate_table(filtered)
    
    def _normalize_turkish_courses(self, df):
        """Normalize Turkish course format to standard format
        Handles hierarchical structure where class level and course type are indicated
        by section header rows (e.g., "2. Sınıf", "SEÇMELİ DERS")
        """
        column_map = {
            'DERS KODU': 'code',
            'Ders Kodu': 'code',
            'ders kodu': 'code',
            'DERS ADI': 'name',
            'Ders Adı': 'name',
            'ders adı': 'name',
            'DERSİN ADI': 'name',
            'Dersin Adı': 'name',
            'dersin adı': 'name',
            'DERSİ VEREN ÖĞR. ELEMANI': 'instructor',
            'Dersi Veren Öğr. Elemanı': 'instructor',
            'dersi veren öğr. elemanı': 'instructor',
            'Öğretim Elemanı': 'instructor',
            'öğretim elemanı': 'instructor',
        }
        
        new_columns = {}
        for col in df.columns:
            col_str = str(col).strip()
            if col_str in column_map:
                new_columns[col] = column_map[col_str]
        
        df = df.rename(columns=new_columns)
        
        if 'code' in df.columns and 'name' not in df.columns:
            unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col) or str(col).startswith('Unnamed')]
            if unnamed_cols:
                df = df.rename(columns={unnamed_cols[0]: 'name'})
        
        if 'code' not in df.columns:
            return df
        
        current_class_level = 1  
        current_course_type = None  
        
        processed_rows = []
        
        for idx, row in df.iterrows():
            code_value = str(row['code']).strip() if pd.notna(row['code']) else ''
            name_value = str(row['name']).strip() if 'name' in row and pd.notna(row.get('name')) else ''
            
            if 'Sınıf' in code_value or 'SINIF' in code_value or 'sınıf' in code_value:
                match = re.search(r'(\d+)', code_value)
                if match:
                    current_class_level = int(match.group(1))
                    current_course_type = None  
                continue  
            
            if 'SEÇMELİ' in code_value or 'SEÇİMLİK' in code_value or 'SEÇ' in code_value:
                current_course_type = 'elective'
                continue  
            
            if 'DERS KODU' in code_value or 'Ders Kodu' in code_value:
                continue  
            
            if 'ZORUNLU' in code_value:
                current_course_type = 'mandatory'
                continue  
            
            if code_value and code_value not in ['', 'nan', 'NaN']:
                new_row = row.copy()
                new_row['class_level'] = current_class_level
                
                if current_course_type is None:
                    new_row['type'] = 'mandatory'
                else:
                    new_row['type'] = current_course_type
                
                if name_value and name_value not in ['', 'nan', 'NaN']:
                    processed_rows.append(new_row)
        
        if processed_rows:
            result_df = pd.DataFrame(processed_rows)
            result_df = result_df.reset_index(drop=True)
            return result_df
        else:
            return pd.DataFrame(columns=['code', 'name', 'instructor', 'class_level', 'type'])
    
    def import_from_excel(self):
        """Import courses from Excel file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if not file_path:
            return
        
        try:
            df = pd.read_excel(file_path)
            
            if any('Sınıf' in str(col) for col in df.columns):
                df = pd.read_excel(file_path, header=1)
                df = self._normalize_turkish_courses(df)
            
            elif 'DERS KODU' in df.columns or 'Ders Kodu' in df.columns:
                df = self._normalize_turkish_courses(df)
            
            required_columns = ['code', 'name']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                QMessageBox.warning(
                    self, "Invalid Format",
                    f"Missing required columns: {', '.join(missing_columns)}\n\n"
                    "Expected columns: code, name, instructor (optional), class_level (optional), type (optional)\n\n"
                    "Or Turkish format with columns: DERS KODU, DERS ADI, DERSİ VEREN ÖĞR. ELEMANI"
                )
                return
            
            user = get_current_user()
            
            selected_dept_id = user['department_id']
            if user['role'] == 'admin':
                from PyQt6.QtWidgets import QInputDialog
                departments = db_manager.execute_query("SELECT id, name, code FROM departments ORDER BY name")
                dept_items = [f"{dept['name']} ({dept['code']})" for dept in departments]
                dept_map = {f"{dept['name']} ({dept['code']})": dept['id'] for dept in departments}
                
                item, ok = QInputDialog.getItem(
                    self, "Select Department", 
                    "Select the department for these courses:",
                    dept_items, 0, False
                )
                if not ok:
                    return
                selected_dept_id = dept_map[item]
            
            progress = QProgressDialog("Importing courses...", "Cancel", 0, len(df), self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            
            imported_count = 0
            errors = []
            
            for index, row in df.iterrows():
                if progress.wasCanceled():
                    break
                
                try:
                    code = str(row['code']).strip()
                    name = str(row['name']).strip()
                    instructor = str(row.get('instructor', '')).strip() if pd.notna(row.get('instructor')) else None
                    class_level = int(row.get('class_level', 0)) if pd.notna(row.get('class_level')) else None
                    course_type = str(row.get('type', '')).strip().lower() if pd.notna(row.get('type')) else None
                    
                    if course_type and course_type not in ['mandatory', 'elective']:
                        course_type = None
                    
                    check_query = "SELECT id FROM courses WHERE department_id = ? AND code = ?"
                    existing = db_manager.execute_query(check_query, (selected_dept_id, code))
                    
                    if existing:
                        query = """
                            UPDATE courses
                            SET name = ?, instructor = ?, class_level = ?, type = ?
                            WHERE department_id = ? AND code = ?
                        """
                        db_manager.execute_update(query, (
                            name, instructor, class_level, course_type, selected_dept_id, code
                        ))
                    else:
                        display_id = db_manager.get_next_display_id('courses')
                        query = """
                            INSERT INTO courses (display_id, department_id, code, name, instructor, class_level, type)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """
                        db_manager.execute_update(query, (
                            display_id, selected_dept_id, code, name, instructor, class_level, course_type
                        ))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
                
                progress.setValue(index + 1)
            
            progress.close()
            
            message = f"Successfully imported {imported_count} courses."
            if errors:
                message += f"\n\nErrors encountered:\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    message += f"\n... and {len(errors) - 10} more errors"
            
            QMessageBox.information(self, "Import Complete", message)
            self.load_courses()
            
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import Excel file:\n{str(e)}")
    
    def toggle_course_status(self):
        """Toggle course active/inactive status"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a course to toggle")
            return
        
        course_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        course_name = self.table.item(row, 2).text()
        
        course = db_manager.execute_query("SELECT isActive FROM courses WHERE id = ?", (course_id,))
        if not course:
            return
        
        current_status = course[0]['isActive']
        new_status = 0 if current_status else 1
        status_text = "active" if new_status else "inactive"
        
        reply = QMessageBox.question(
            self, "Confirm Status Change",
            f"Set course '{course_name}' to {status_text}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            query = "UPDATE courses SET isActive = ? WHERE id = ?"
            db_manager.execute_update(query, (new_status, course_id))
            QMessageBox.information(self, "Success", f"Course is now {status_text}")
            self.load_courses()
    
    def view_course_details(self):
        """View course details and enrolled students"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a course to view details")
            return
        
        course_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        course_query = """
            SELECT c.*, d.name as department_name, d.code as department_code
            FROM courses c
            LEFT JOIN departments d ON c.department_id = d.id
            WHERE c.id = ?
        """
        course = db_manager.execute_query(course_query, (course_id,))
        
        if not course:
            return
        
        course = dict(course[0])
        
        students_query = """
            SELECT s.display_id, s.student_no, s.name, s.class_level
            FROM students s
            JOIN student_courses sc ON s.id = sc.student_id
            WHERE sc.course_id = ?
            ORDER BY s.student_no
        """
        students = db_manager.execute_query(students_query, (course_id,))
        
        dialog = CourseDetailsDialog(self, course, students)
        dialog.exec()
    
    def delete_course(self):
        """Delete selected course"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a course to delete")
            return
        
        course_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        course_name = self.table.item(row, 2).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete course '{course_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM courses WHERE id = ?"
            db_manager.execute_update(query, (course_id,))
            self.load_courses()
    
    def clear_all_courses(self):
        """Clear all courses"""
        reply = QMessageBox.question(
            self, "Confirm Clear All",
            "Are you sure you want to delete ALL courses? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            user = get_current_user()
            if user['role'] == 'admin':
                query = "DELETE FROM courses"
                db_manager.execute_update(query)
            else:
                query = "DELETE FROM courses WHERE department_id = ?"
                db_manager.execute_update(query, (user['department_id'],))
            
            self.table.setRowCount(0)
            self.load_courses()

class CourseDetailsDialog(QDialog):
    """Dialog to show course details and enrolled students"""
    
    def __init__(self, parent, course, students):
        super().__init__(parent)
        self.course = course
        self.students = students
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle(f"Course Details - {self.course['code']}")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        info_label = QLabel("Course Information")
        info_label.setStyleSheet(Styles.SUBTITLE_LABEL)
        layout.addWidget(info_label)
        
        info_text = f"""
        <b>Code:</b> {self.course['code']}<br>
        <b>Name:</b> {self.course['name']}<br>
        <b>Instructor:</b> {self.course['instructor'] or 'N/A'}<br>
        <b>Department:</b> {self.course['department_name']} ({self.course['department_code']})<br>
        <b>Class Level:</b> {self.course['class_level'] or 'N/A'}<br>
        <b>Type:</b> {self.course['type'] or 'N/A'}<br>
        <b>Status:</b> {'✅ Active' if self.course['isActive'] else '❌ Inactive'}<br>
        <b>Total Students:</b> {len(self.students)}
        """
        
        info_display = QLabel(info_text)
        info_display.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px; color: #000000;")
        layout.addWidget(info_display)
        
        students_label = QLabel("Enrolled Students")
        students_label.setStyleSheet(Styles.SUBTITLE_LABEL)
        layout.addWidget(students_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Student No", "Name", "Class Level"])
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.students))
        for row, student in enumerate(self.students):
            self.table.setItem(row, 0, QTableWidgetItem(str(student['display_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(student['student_no']))
            self.table.setItem(row, 2, QTableWidgetItem(student['name']))
            self.table.setItem(row, 3, QTableWidgetItem(str(student['class_level']) if student['class_level'] else ""))
        self.table.setSortingEnabled(True)
        
        layout.addWidget(self.table)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

