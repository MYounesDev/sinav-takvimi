"""
Courses View - Manage courses and import from Excel
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QFileDialog, QMessageBox, QProgressDialog)
from PyQt6.QtCore import Qt
import pandas as pd
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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Code", "Name", "Instructor", "Class Level", "Type"
        ])
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
        
        dept_filter = "" if user['role'] == 'admin' else f"WHERE department_id = {user['department_id']}"
        
        query = f"""
            SELECT id, code, name, instructor, class_level, type
            FROM courses
            {dept_filter}
            ORDER BY code
        """
        
        courses = db_manager.execute_query(query)
        
        self.table.setRowCount(len(courses))
        
        for row, course in enumerate(courses):
            self.table.setItem(row, 0, QTableWidgetItem(str(course['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(course['code']))
            self.table.setItem(row, 2, QTableWidgetItem(course['name']))
            self.table.setItem(row, 3, QTableWidgetItem(course['instructor'] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(str(course['class_level']) if course['class_level'] else ""))
            self.table.setItem(row, 5, QTableWidgetItem(course['type'] or ""))
    
    def _normalize_turkish_courses(self, df):
        """Normalize Turkish course format to standard format"""
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
            'SINIF': 'class_level',
            'Sınıf': 'class_level',
            'sınıf': 'class_level',
        }
        
        # Rename columns based on mapping
        new_columns = {}
        for col in df.columns:
            col_str = str(col).strip()
            if col_str in column_map:
                new_columns[col] = column_map[col_str]
        
        df = df.rename(columns=new_columns)
        
        # Clean up the dataframe - remove empty rows
        df = df.dropna(how='all')
        
        # If we have 'code' column, filter out section headers and duplicate headers
        if 'code' in df.columns:
            # Remove rows where code looks like a section header (contains "Sınıf" or is NaN)
            df = df[df['code'].notna()]
            df = df[~df['code'].astype(str).str.contains('Sınıf', case=False, na=False)]
            df = df[~df['code'].astype(str).str.contains('SINIF', case=False, na=False)]
            # Remove duplicate header rows (where code is "DERS KODU")
            df = df[~df['code'].astype(str).str.contains('DERS KODU', case=False, na=False)]
            df = df[~df['code'].astype(str).str.contains('Ders Kodu', case=False, na=False)]
        
        # If there's no 'name' column but we have 'code', try to find name in other columns
        if 'code' in df.columns and 'name' not in df.columns:
            # Look for unnamed columns that might contain course names
            unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col) or str(col).startswith('Unnamed')]
            if unnamed_cols:
                # Use the first unnamed column as the course name
                df = df.rename(columns={unnamed_cols[0]: 'name'})
        
        return df
    
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
                        user['department_id'], code, name, instructor, class_level, course_type
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
            dept_filter = "" if user['role'] == 'admin' else f"WHERE department_id = {user['department_id']}"
            query = f"""DELETE FROM courses
            {dept_filter}"""
            db_manager.execute_update(query)
            self.load_courses()


