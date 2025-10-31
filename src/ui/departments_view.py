"""
Departments View - Manage departments (Admin only)
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QDialog, QFormLayout, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from src.utils.styles import Styles, configure_table_widget

class DepartmentsView(QWidget):
    """Departments management view (Admin only)"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        top_bar = QHBoxLayout()
        
        title = QLabel("Department Management")
        title.setStyleSheet(Styles.SUBTITLE_LABEL)
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        add_btn = QPushButton("➕ Add Department")
        add_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.add_department)
        top_bar.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_departments)
        top_bar.addWidget(refresh_btn)
        
        layout.addLayout(top_bar)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Code", "Created"
        ])
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        
        # Configure table for proper visibility and scrolling
        configure_table_widget(self.table, min_row_height=38, min_total_height=450)
        
        layout.addWidget(self.table)
        
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_department)
        action_bar.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet(Styles.DANGER_BUTTON)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_department)
        action_bar.addWidget(delete_btn)
        
        layout.addLayout(action_bar)
        
        self.load_departments()
    
    def load_departments(self):
        """Load departments from database"""
        query = """
            SELECT id, display_id, name, code, created_at
            FROM departments
            ORDER BY name
        """
        
        departments = db_manager.execute_query(query)
        
        self.table.setRowCount(len(departments))
        
        for row, dept in enumerate(departments):
            self.table.setItem(row, 0, QTableWidgetItem(str(dept['display_id'])))
            self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, dept['id'])
            self.table.setItem(row, 1, QTableWidgetItem(dept['name']))
            self.table.setItem(row, 2, QTableWidgetItem(dept['code']))
            created = dept['created_at'] or "N/A"
            self.table.setItem(row, 3, QTableWidgetItem(str(created)))
    
    def add_department(self):
        """Open dialog to add new department"""
        dialog = DepartmentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_departments()
    
    def edit_department(self):
        """Edit selected department"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a department to edit")
            return
        
        dept_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        query = "SELECT * FROM departments WHERE id = ?"
        result = db_manager.execute_query(query, (dept_id,))
        
        if result:
            dialog = DepartmentDialog(self, dict(result[0]))
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_departments()
    
    def delete_department(self):
        """Delete selected department - CASCADE DELETE will handle related records"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a department to delete")
            return
        
        dept_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        dept_name = self.table.item(row, 1).text()
        
        reply = QMessageBox.warning(
            self, "Confirm Delete",
            f"Are you sure you want to delete department '{dept_name}'?\n\n"
            f"⚠️ WARNING: This will also delete ALL related records:\n"
            f"  - All students in this department\n"
            f"  - All courses in this department\n"
            f"  - All classrooms in this department\n"
            f"  - All coordinators for this department\n"
            f"  - All exams for this department\n\n"
            f"This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                query = "DELETE FROM departments WHERE id = ?"
                db_manager.execute_update(query, (dept_id,))
                QMessageBox.information(self, "Success", 
                    "Department and all related records deleted successfully!\n"
                    "The ID will be reused for future entries.")
                self.load_departments()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete department: {str(e)}")

class DepartmentDialog(QDialog):
    """Dialog for adding/editing departments"""
    
    def __init__(self, parent=None, dept_data=None):
        super().__init__(parent)
        self.dept_data = dept_data
        self.is_edit = dept_data is not None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Edit Department" if self.is_edit else "Add Department")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(Styles.LINE_EDIT)
        form_layout.addRow("Name:", self.name_input)
        
        self.code_input = QLineEdit()
        self.code_input.setStyleSheet(Styles.LINE_EDIT)
        form_layout.addRow("Code:", self.code_input)
        
        layout.addLayout(form_layout)
        
        if self.is_edit:
            self.name_input.setText(self.dept_data['name'])
            self.code_input.setText(self.dept_data['code'])
            self.code_input.setReadOnly(True)  
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        save_btn.clicked.connect(self.save)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def save(self):
        """Save department data"""
        name = self.name_input.text().strip()
        code = self.code_input.text().strip()
        
        if not name or not code:
            QMessageBox.warning(self, "Validation Error", "Name and code are required")
            return
        
        try:
            if self.is_edit:
                query = "UPDATE departments SET name = ? WHERE id = ?"
                db_manager.execute_update(query, (name, self.dept_data['id']))
                QMessageBox.information(self, "Success", "Department updated successfully!")
            else:
                display_id = db_manager.get_next_display_id('departments')
                query = "INSERT INTO departments (display_id, name, code) VALUES (?, ?, ?)"
                db_manager.execute_update(query, (display_id, name, code))
                QMessageBox.information(self, "Success", 
                    f"Department created successfully with ID: {display_id}")
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save department: {str(e)}")

