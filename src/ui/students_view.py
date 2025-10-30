
from src.utils.auth import get_current_user
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QFileDialog, QMessageBox, QProgressDialog, QLineEdit, QComboBox, QDialog)
import pandas as pd
from src.utils.styles import Styles
from src.database.db_manager import db_manager

class StudentsView(QWidget):
    def __init__(self):
        super().__init__()
        self.all_students = []  
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        top_bar = QHBoxLayout()
        
        title = QLabel("Student Management")
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
            
            self.dept_filter.currentIndexChanged.connect(self.load_students)
            top_bar.addWidget(self.dept_filter)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by ID, Student No, or Name...")
        self.search_input.setStyleSheet(Styles.LINE_EDIT)
        self.search_input.setFixedWidth(350)
        self.search_input.textChanged.connect(self.filter_students)
        top_bar.addWidget(self.search_input)
        
        import_btn = QPushButton("📥 Import from Excel")
        import_btn.setStyleSheet(Styles.SUCCESS_BUTTON)
        import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        import_btn.clicked.connect(self.import_from_excel)
        top_bar.addWidget(import_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_students)
        top_bar.addWidget(refresh_btn)
        
        layout.addLayout(top_bar)
        
        self.table = QTableWidget()
        user = get_current_user()
        headers = ["ID", "Student No", "Name", "Class Level", "Enrolled Courses"]
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
        
        view_details_btn = QPushButton("👁️ View Details")
        view_details_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        view_details_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_details_btn.clicked.connect(self.view_student_details)
        action_bar.addWidget(view_details_btn)
        
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
        
        self.all_students = []
        
        self.load_students()
    
    def load_students(self):
        """Load students from database"""
        user = get_current_user()
        if not user:
            return
        
        headers = ["ID", "Student No", "Name", "Class Level", "Enrolled Courses"]
        if user and user['role'] == 'admin':
            headers.insert(3, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
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
            SELECT s.id, s.display_id, s.student_no, s.name, s.class_level,
                   COUNT(sc.course_id) as course_count,
                   s.department_id, d.name as department_name, d.code as department_code
            FROM students s
            LEFT JOIN student_courses sc ON s.id = sc.student_id
            LEFT JOIN departments d ON s.department_id = d.id
            {dept_filter}
            GROUP BY s.id, s.display_id, s.student_no, s.name, s.class_level, s.department_id, d.name, d.code
            ORDER BY s.display_id
        """
        
        self.all_students = list(db_manager.execute_query(query))
        self.display_students(self.all_students)
    
    def display_students(self, students):
        """Display students in table"""
        user = get_current_user()
        
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            col_idx = 0
            
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.DisplayRole, int(student['display_id']))
            id_item.setData(Qt.ItemDataRole.UserRole, student['id'])  
            self.table.setItem(row, col_idx, id_item)
            col_idx += 1
            
            self.table.setItem(row, col_idx, QTableWidgetItem(student['student_no']))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(student['name']))
            col_idx += 1
            
            if user and user['role'] == 'admin':
                dept_name = student['department_name'] or 'N/A'
                dept_code = student['department_code'] or ''
                self.table.setItem(row, col_idx, QTableWidgetItem(f"{dept_name} ({dept_code})"))
                col_idx += 1
            
            self.table.setItem(row, col_idx, QTableWidgetItem(str(student['class_level']) if student['class_level'] else ""))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(str(student['course_count'])))
        
        self.table.setSortingEnabled(True)
    
    def filter_students(self):
        """Filter students based on search input"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self.display_students(self.all_students)
            return
        
        filtered = [s for s in self.all_students 
                   if (str(s['display_id']).lower().find(search_text) != -1 or
                       s['student_no'].lower().find(search_text) != -1 or
                       s['name'].lower().find(search_text) != -1)]
        
        self.display_students(filtered)
    
    def _normalize_turkish_students(self, df):
        """Normalize Turkish student format to standard format
        Turkish format is in long format: one row per student-course pair
        Need to convert to wide format: one row per student with all courses
        """
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
        
        new_columns = {}
        for col in df.columns:
            col_str = str(col).strip()
            if col_str in column_map:
                new_columns[col] = column_map[col_str]
        
        df = df.rename(columns=new_columns)
        
        df = df.dropna(how='all')
        
        if 'student_no' in df.columns and 'course_code' in df.columns:
            if 'class_level_str' in df.columns:
                df['class_level'] = df['class_level_str'].astype(str).str.extract(r'(\d+)')[0]
                df['class_level'] = pd.to_numeric(df['class_level'], errors='coerce')
            
            grouped = df.groupby(['student_no', 'name']).agg({
                'class_level': 'first',  
                'course_code': lambda x: ','.join(x.dropna().astype(str))  
            }).reset_index()
            
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
            df = pd.read_excel(file_path)
            
            turkish_columns = ['Öğrenci No', 'Ad Soyad', 'Sınıf', 'Ders']
            if any(col in df.columns for col in turkish_columns):
                df = self._normalize_turkish_students(df)
            
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
                    
                    check_query = "SELECT id FROM students WHERE student_no = ?"
                    existing = db_manager.execute_query(check_query, (student_no,))
                    
                    if existing:
                        query = """
                            UPDATE students
                            SET name = ?, class_level = ?
                            WHERE student_no = ?
                        """
                        db_manager.execute_update(query, (name, class_level, student_no))
                        student_id = existing[0]['id']
                    else:
                        display_id = db_manager.get_next_display_id('students')
                        query = """
                            INSERT INTO students (display_id, department_id, student_no, name, class_level)
                            VALUES (?, ?, ?, ?, ?)
                        """
                        student_id = db_manager.execute_update(query, (
                            display_id, selected_dept_id, student_no, name, class_level
                        ))
                    
                    if course_codes_str and student_id:
                        course_codes = [c.strip() for c in course_codes_str.split(',') if c.strip()]
                        
                        for course_code in course_codes:
                            if user['role'] == 'admin':
                                course_query = "SELECT id FROM courses WHERE code = ?"
                                course_result = db_manager.execute_query(course_query, (course_code,))
                            else:
                                course_query = "SELECT id FROM courses WHERE code = ? AND department_id = ?"
                                course_result = db_manager.execute_query(course_query, (course_code, user['department_id']))
                            
                            if course_result:
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
        
        student_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
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
            
            self.table.setRowCount(0)
            self.all_students = []
            self.load_students()
    
    def view_student_details(self):
        """Show detailed view of selected student with enrolled courses"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a student to view details")
            return
        
        student_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        student_query = """
            SELECT s.id, s.display_id, s.student_no, s.name, s.class_level,
                   d.name as department_name, d.code as department_code
            FROM students s
            LEFT JOIN departments d ON s.department_id = d.id
            WHERE s.id = ?
        """
        student = db_manager.execute_query(student_query, (student_id,))
        if not student:
            QMessageBox.warning(self, "Error", "Could not load student data")
            return
        student = student[0]
        
        courses_query = """
            SELECT c.display_id, c.code, c.name, c.instructor, c.class_level, c.type,
                   CASE WHEN c.isActive = 1 THEN '✅' ELSE '❌' END as status
            FROM courses c
            INNER JOIN student_courses sc ON c.id = sc.course_id
            WHERE sc.student_id = ?
            ORDER BY c.code
        """
        courses = list(db_manager.execute_query(courses_query, (student_id,)))
        
        dialog = StudentDetailsDialog(self, student, courses)
        dialog.exec()

class StudentDetailsDialog(QDialog):
    """Dialog to show student details and enrolled courses"""
    
    def __init__(self, parent, student, courses):
        super().__init__(parent)
        self.student = student
        self.courses = courses
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle(f"Student Details - {self.student['student_no']}")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        info_label = QLabel("Student Information")
        info_label.setStyleSheet(Styles.SUBTITLE_LABEL)
        layout.addWidget(info_label)
        
        info_text = f"""
        <b>ID:</b> {self.student['display_id']}<br>
        <b>Student No:</b> {self.student['student_no']}<br>
        <b>Name:</b> {self.student['name']}<br>
        <b>Department:</b> {self.student['department_name']} ({self.student['department_code']})<br>
        <b>Class Level:</b> {self.student['class_level'] or 'N/A'}<br>
        <b>Total Courses:</b> {len(self.courses)}
        """
        
        info_display = QLabel(info_text)
        info_display.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px; color: #000000;")
        layout.addWidget(info_display)
        
        courses_label = QLabel("Enrolled Courses")
        courses_label.setStyleSheet(Styles.SUBTITLE_LABEL)
        layout.addWidget(courses_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Code", "Name", "Instructor", "Class Level", "Type", "Status"])
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.courses))
        for row, course in enumerate(self.courses):
            self.table.setItem(row, 0, QTableWidgetItem(str(course['display_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(course['code']))
            self.table.setItem(row, 2, QTableWidgetItem(course['name']))
            self.table.setItem(row, 3, QTableWidgetItem(course['instructor'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(str(course['class_level']) if course['class_level'] else ""))
            self.table.setItem(row, 5, QTableWidgetItem(course['type'] or ''))
            self.table.setItem(row, 6, QTableWidgetItem(course['status']))
        self.table.setSortingEnabled(True)
        
        layout.addWidget(self.table)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

