"""
Courses View - Manage courses and import from Excel
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QFileDialog, QMessageBox, QProgressDialog, QComboBox)
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
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Top bar with actions
        top_bar = QHBoxLayout()
        
        title = QLabel("Course Management")
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
            
            self.dept_filter.currentIndexChanged.connect(self.load_courses)
            top_bar.addWidget(self.dept_filter)
        
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
        refresh_btn.clicked.connect(self.load_courses)
        top_bar.addWidget(refresh_btn)
        
        layout.addLayout(top_bar)
        
        # Table
        self.table = QTableWidget()
        user = get_current_user()
        # Add department column for admin
        headers = ["ID", "Code", "Name", "Instructor", "Class Level", "Type"]
        if user and user['role'] == 'admin':
            headers.insert(3, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Delete button
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
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
        
        # Load data
        self.load_courses()
    
    def load_courses(self):
        """Load courses from database"""
        user = get_current_user()
        if not user:
            return
        
        # Re-initialize table structure based on actual logged-in user
        headers = ["ID", "Code", "Name", "Instructor", "Class Level", "Type"]
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
                dept_filter = f"WHERE c.department_id = {selected_dept_id}"
            else:
                dept_filter = ""
        else:
            dept_filter = f"WHERE c.department_id = {user['department_id']}"
        
        query = f"""
            SELECT c.id, c.code, c.name, c.instructor, c.class_level, c.type,
                   c.department_id, d.name as department_name, d.code as department_code
            FROM courses c
            LEFT JOIN departments d ON c.department_id = d.id
            {dept_filter}
            ORDER BY c.code
        """
        
        courses = db_manager.execute_query(query)
        user = get_current_user()  # Refresh user for column calculation
        
        self.table.setRowCount(len(courses))
        
        for row, course in enumerate(courses):
            col_idx = 0
            self.table.setItem(row, col_idx, QTableWidgetItem(str(course['id'])))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(course['code']))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(course['name']))
            col_idx += 1
            
            # Add department column for admin
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
    
    def _normalize_turkish_courses(self, df):
        """Normalize Turkish course format to standard format
        Handles hierarchical structure where class level and course type are indicated
        by section header rows (e.g., "2. Sınıf", "SEÇMELİ DERS")
        """
        # Turkish column name mappings (case-insensitive)
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
        
        # Rename columns based on mapping
        new_columns = {}
        for col in df.columns:
            col_str = str(col).strip()
            if col_str in column_map:
                new_columns[col] = column_map[col_str]
        
        df = df.rename(columns=new_columns)
        
        # If there's no 'name' column but we have 'code', try to find name in other columns
        if 'code' in df.columns and 'name' not in df.columns:
            # Look for unnamed columns that might contain course names
            unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col) or str(col).startswith('Unnamed')]
            if unnamed_cols:
                # Use the first unnamed column as the course name
                df = df.rename(columns={unnamed_cols[0]: 'name'})
        
        # Now process rows sequentially to handle hierarchical structure
        if 'code' not in df.columns:
            return df
        
        # Track current class level and course type as we process rows
        current_class_level = 1  # Default to 1st year
        current_course_type = None  # None means not yet determined (will default to 'mandatory')
        
        # Prepare list for processed rows
        processed_rows = []
        
        # Process each row sequentially
        for idx, row in df.iterrows():
            code_value = str(row['code']).strip() if pd.notna(row['code']) else ''
            name_value = str(row['name']).strip() if 'name' in row and pd.notna(row.get('name')) else ''
            
            # Check if this is a class level indicator (e.g., "1. Sınıf", "2. Sınıf")
            if 'Sınıf' in code_value or 'SINIF' in code_value or 'sınıf' in code_value:
                # Extract class level number (e.g., "2. Sınıf" -> 2)
                match = re.search(r'(\d+)', code_value)
                if match:
                    current_class_level = int(match.group(1))
                    current_course_type = None  # Reset type when class level changes
                continue  # Skip this row, don't add it
            
            # Check if this is a course type indicator (e.g., "SEÇMELİ DERS", "SEÇİMLİK DERS")
            if 'SEÇMELİ' in code_value or 'SEÇİMLİK' in code_value or 'SEÇ' in code_value:
                current_course_type = 'elective'
                continue  # Skip this row, don't add it
            
            # Check if this is a duplicate header row
            if 'DERS KODU' in code_value or 'Ders Kodu' in code_value:
                continue  # Skip duplicate headers
            
            # Check if this looks like a mandatory course indicator (optional - some files might have this)
            if 'ZORUNLU' in code_value:
                current_course_type = 'mandatory'
                continue  # Skip this row
            
            # If we have a valid code (not empty, not NaN), this is a course row
            if code_value and code_value not in ['', 'nan', 'NaN']:
                # Create a new row with the current class_level and course_type
                new_row = row.copy()
                new_row['class_level'] = current_class_level
                
                # Set course type: use current type, or default to 'mandatory' if None
                if current_course_type is None:
                    # If we haven't seen a type indicator, default to mandatory
                    new_row['type'] = 'mandatory'
                else:
                    new_row['type'] = current_course_type
                
                # Only add if we have a name (or at least it looks like a real course)
                if name_value and name_value not in ['', 'nan', 'NaN']:
                    processed_rows.append(new_row)
        
        # Create new DataFrame from processed rows
        if processed_rows:
            result_df = pd.DataFrame(processed_rows)
            # Reset index
            result_df = result_df.reset_index(drop=True)
            return result_df
        else:
            # Fallback: return empty dataframe with expected columns
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
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Check if it's Turkish format (Ders Listesi.xlsx)
            # Turkish format has columns like '1. Sınıf' and first row contains actual headers
            if any('Sınıf' in str(col) for col in df.columns):
                # Re-read with proper header row (row 1)
                df = pd.read_excel(file_path, header=1)
                # Standardize column names from Turkish to English
                df = self._normalize_turkish_courses(df)
            
            # Check if Turkish format in different structure (with Turkish column names)
            elif 'DERS KODU' in df.columns or 'Ders Kodu' in df.columns:
                df = self._normalize_turkish_courses(df)
            
            # Expected columns: code, name, instructor, class_level, type
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
            
            # For admin, show department selection dialog
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
            
            # Show progress dialog
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
                    
                    # Validate type
                    if course_type and course_type not in ['mandatory', 'elective']:
                        course_type = None
                    
                    # Insert or update course
                    query = """
                        INSERT INTO courses (department_id, code, name, instructor, class_level, type)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ON CONFLICT(department_id, code) DO UPDATE SET
                        name = excluded.name,
                        instructor = excluded.instructor,
                        class_level = excluded.class_level,
                        type = excluded.type
                    """
                    
                    db_manager.execute_update(query, (
                        selected_dept_id, code, name, instructor, class_level, course_type
                    ))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
                
                progress.setValue(index + 1)
            
            progress.close()
            
            # Show results
            message = f"Successfully imported {imported_count} courses."
            if errors:
                message += f"\n\nErrors encountered:\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    message += f"\n... and {len(errors) - 10} more errors"
            
            QMessageBox.information(self, "Import Complete", message)
            self.load_courses()
            
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import Excel file:\n{str(e)}")
    
    def delete_course(self):
        """Delete selected course"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a course to delete")
            return
        
        course_id = int(self.table.item(row, 0).text())
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
            # For admin, delete filtered or all; for coordinator, only their department
            if user['role'] == 'admin':
                query = "DELETE FROM courses"
                db_manager.execute_update(query)
            else:
                query = "DELETE FROM courses WHERE department_id = ?"
                db_manager.execute_update(query, (user['department_id'],))
            
            # Clear the table before reloading to avoid dataChanged warnings
            self.table.setRowCount(0)
            self.load_courses()


