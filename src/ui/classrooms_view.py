"""
Classrooms View - Manage classrooms
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QDialog, QFormLayout, QLineEdit, QSpinBox, QMessageBox,
                             QFrame, QGridLayout, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from src.utils.styles import Styles, apply_shadow, configure_table_widget
from config import COLORS

class ClassroomsView(QWidget):
    """Classrooms management view"""
    
    def __init__(self):
        super().__init__()
        self.all_classrooms = []  
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        top_bar = QHBoxLayout()
        
        title = QLabel("Classroom Management")
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
            
            self.dept_filter.currentIndexChanged.connect(self.load_classrooms)
            top_bar.addWidget(self.dept_filter)
        
        add_btn = QPushButton("➕ Add Classroom")
        add_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.add_classroom)
        top_bar.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_classrooms)
        top_bar.addWidget(refresh_btn)
        
        layout.addLayout(top_bar)
        
        search_bar = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        search_label.setStyleSheet(Styles.NORMAL_LABEL)
        search_bar.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID, Code, or Name...")
        self.search_input.setStyleSheet(Styles.LINE_EDIT)
        self.search_input.textChanged.connect(self.filter_classrooms)
        search_bar.addWidget(self.search_input)
        
        layout.addLayout(search_bar)
        
        self.table = QTableWidget()
        user = get_current_user()
        headers = ["ID", "Code", "Name", "Capacity", "Rows", "Columns", "Seats/Desk"]
        if user and user['role'] == 'admin':
            headers.insert(3, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        
        # Configure table for proper visibility and scrolling
        configure_table_widget(self.table, min_row_height=38, min_total_height=450)
        
        layout.addWidget(self.table)
        
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_classroom)
        action_bar.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet(Styles.DANGER_BUTTON)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_classroom)
        action_bar.addWidget(delete_btn)
        
        clear_all_btn = QPushButton("🗑️ Clear All")
        clear_all_btn.setStyleSheet(Styles.DANGER_BUTTON)
        clear_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_all_btn.clicked.connect(self.clear_all_classrooms)
        action_bar.addWidget(clear_all_btn)
        
        layout.addLayout(action_bar)
        
        self.load_classrooms()
    
    def load_classrooms(self):
        """Load classrooms from database"""
        user = get_current_user()
        if not user:
            return
        
        headers = ["ID", "Code", "Name", "Capacity", "Rows", "Columns", "Seats/Desk"]
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
            SELECT c.id, c.display_id, c.code, c.name, c.capacity, c.rows, c.cols, c.seats_per_desk,
                   c.department_id, d.name as department_name, d.code as department_code
            FROM classrooms c
            LEFT JOIN departments d ON c.department_id = d.id
            {dept_filter}
            ORDER BY c.display_id
        """
        
        classrooms = db_manager.execute_query(query)
        self.all_classrooms = classrooms  
        self.populate_table(classrooms)
    
    def populate_table(self, classrooms):
        """Populate table with classroom data"""
        user = get_current_user()
        
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(classrooms))
        
        for row, classroom in enumerate(classrooms):
            col_idx = 0
            
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.DisplayRole, int(classroom['display_id']))
            id_item.setData(Qt.ItemDataRole.UserRole, classroom['id'])  
            self.table.setItem(row, col_idx, id_item)
            col_idx += 1
            
            self.table.setItem(row, col_idx, QTableWidgetItem(classroom['code']))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(classroom['name']))
            col_idx += 1
            
            if user and user['role'] == 'admin':
                dept_name = classroom['department_name'] or 'N/A'
                dept_code = classroom['department_code'] or ''
                self.table.setItem(row, col_idx, QTableWidgetItem(f"{dept_name} ({dept_code})"))
                col_idx += 1
            
            self.table.setItem(row, col_idx, QTableWidgetItem(str(classroom['capacity'])))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(str(classroom['rows'])))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(str(classroom['cols'])))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(str(classroom['seats_per_desk'])))
        
        # Ensure all rows are visible with proper height
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.setSortingEnabled(True)
    
    def filter_classrooms(self):
        """Filter classrooms based on search text"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self.populate_table(self.all_classrooms)
            return
        
        filtered = []
        for classroom in self.all_classrooms:
            if (str(classroom['display_id']).lower().find(search_text) != -1 or
                classroom['code'].lower().find(search_text) != -1 or
                classroom['name'].lower().find(search_text) != -1):
                filtered.append(classroom)
        
        self.populate_table(filtered)
    
    def add_classroom(self):
        """Open dialog to add new classroom"""
        dialog = ClassroomDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_classrooms()
    
    def edit_classroom(self):
        """Edit selected classroom"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a classroom to edit")
            return
        
        classroom_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        query = "SELECT * FROM classrooms WHERE id = ?"
        result = db_manager.execute_query(query, (classroom_id,))
        
        if result:
            dialog = ClassroomDialog(self, dict(result[0]))
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_classrooms()
    
    def delete_classroom(self):
        """Delete selected classroom"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a classroom to delete")
            return
        
        classroom_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        classroom_name = self.table.item(row, 2).text()
        
        reply = QMessageBox.question(
            self, "Confirm",
            f"Are you sure you want to delete classroom '{classroom_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM classrooms WHERE id = ?"
            db_manager.execute_update(query, (classroom_id,))
            QMessageBox.information(self, "Success", "Classroom deleted successfully!")
            self.load_classrooms()
    
    def clear_all_classrooms(self):
        """Clear all classrooms"""
        reply = QMessageBox.question(
            self, "Confirm",
            "Are you sure you want to delete ALL classrooms? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            user = get_current_user()
            if user['role'] == 'admin':
                if hasattr(self, 'dept_filter'):
                    selected_dept_id = self.dept_filter.currentData()
                    if selected_dept_id:
                        dept_filter = f"WHERE department_id = {selected_dept_id}"
                    else:
                        dept_filter = ""
                else:
                    dept_filter = ""
            else:
                dept_filter = f"WHERE department_id = {user['department_id']}"
            query = f"""DELETE FROM classrooms
            {dept_filter}"""
            db_manager.execute_update(query)
            QMessageBox.information(self, "Success", "All classrooms deleted successfully!")
            self.load_classrooms()

class ClassroomDialog(QDialog):
    """Dialog for adding/editing classrooms"""
    
    def __init__(self, parent=None, classroom_data=None):
        super().__init__(parent)
        self.classroom_data = classroom_data
        self.is_edit = classroom_data is not None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Edit Classroom" if self.is_edit else "Add Classroom")
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        
        main_layout = QHBoxLayout(self)
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        
        user = get_current_user()
        self.dept_combo = None
        if user and user['role'] == 'admin':
            self.dept_combo = QComboBox()
            self.dept_combo.setStyleSheet(Styles.COMBO_BOX)
            departments = db_manager.execute_query("SELECT id, name, code FROM departments ORDER BY name")
            for dept in departments:
                self.dept_combo.addItem(f"{dept['name']} ({dept['code']})", dept['id'])
            form_layout.addRow("Department:", self.dept_combo)
        
        self.code_input = QLineEdit()
        self.code_input.setStyleSheet(Styles.LINE_EDIT)
        form_layout.addRow("Kod:", self.code_input)
        
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(Styles.LINE_EDIT)
        form_layout.addRow("Ad:", self.name_input)
        
        self.rows_input = QSpinBox()
        self.rows_input.setMinimum(1)
        self.rows_input.setMaximum(50)
        self.rows_input.setValue(5)
        self.rows_input.setStyleSheet(Styles.SPIN_BOX)
        self.rows_input.valueChanged.connect(self.update_preview)
        form_layout.addRow("Satır Sayısı:", self.rows_input)
        
        self.cols_input = QSpinBox()
        self.cols_input.setMinimum(1)
        self.cols_input.setMaximum(50)
        self.cols_input.setValue(8)
        self.cols_input.setStyleSheet(Styles.SPIN_BOX)
        self.cols_input.valueChanged.connect(self.update_preview)
        form_layout.addRow("Sütun Sayısı:", self.cols_input)
        
        self.seats_input = QSpinBox()
        self.seats_input.setMinimum(1)
        self.seats_input.setMaximum(3)
        self.seats_input.setValue(2)
        self.seats_input.setStyleSheet(Styles.SPIN_BOX)
        self.seats_input.valueChanged.connect(self.update_preview)
        form_layout.addRow("Masa Başına Kişi:", self.seats_input)
        
        self.capacity_input = QLineEdit()
        self.capacity_input.setReadOnly(True)
        self.capacity_input.setStyleSheet(Styles.LINE_EDIT)
        form_layout.addRow("Kapasite:", self.capacity_input)
        
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        save_btn.clicked.connect(self.save)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        form_layout.addRow(button_layout)
        
        main_layout.addWidget(form_widget)
        
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        
        preview_title = QLabel("Classroom Preview")
        preview_title.setStyleSheet(Styles.SUBTITLE_LABEL)
        preview_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(preview_title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(Styles.SCROLL_AREA)
        
        self.preview_grid_container = QWidget()
        self.preview_grid = QGridLayout(self.preview_grid_container)
        self.preview_grid.setSpacing(5)
        
        scroll.setWidget(self.preview_grid_container)
        preview_layout.addWidget(scroll)
        
        main_layout.addWidget(preview_widget)
        
        if self.is_edit:
            self.code_input.setText(self.classroom_data['code'] or '')
            self.name_input.setText(self.classroom_data['name'])
            self.rows_input.setValue(self.classroom_data['rows'])
            self.cols_input.setValue(self.classroom_data['cols'])
            self.seats_input.setValue(self.classroom_data['seats_per_desk'])
            if self.dept_combo and 'department_id' in self.classroom_data:
                index = self.dept_combo.findData(self.classroom_data['department_id'])
                if index >= 0:
                    self.dept_combo.setCurrentIndex(index)
        
        self.update_preview()
    
    def update_preview(self):
        """Update the classroom layout preview"""
        while self.preview_grid.count():
            child = self.preview_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        rows = self.rows_input.value()
        cols = self.cols_input.value()
        seats_per_desk = self.seats_input.value()
        
        capacity = rows * cols * seats_per_desk
        self.capacity_input.setText(str(capacity))
        
        max_preview_rows = min(rows, 15)
        max_preview_cols = min(cols, 15)
        
        for r in range(max_preview_rows):
            for c in range(max_preview_cols):
                group_index = (c // seats_per_desk) % 3
                
                colors = [
                    QColor(227, 242, 253),  
                    QColor(232, 245, 233),  
                    QColor(255, 243, 224),  
                ]
                bg_color = colors[group_index]
                
                desk = QFrame()
                desk.setFixedSize(35, 35)
                desk.setStyleSheet(f"""
                    QFrame {{
                        background-color: rgb({bg_color.red()}, {bg_color.green()}, {bg_color.blue()});
                        border: 1px solid #BDBDBD;
                        border-radius: 4px;
                    }}
                """)
                
                desk_layout = QVBoxLayout(desk)
                desk_layout.setContentsMargins(2, 2, 2, 2)
                
                label = QLabel(f"{r+1},{c+1}")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("font-size: 9px; color: #34495E;")
                desk_layout.addWidget(label)
                
                self.preview_grid.addWidget(desk, r, c)
        
        if rows > 15 or cols > 15:
            note = QLabel(f"(Önizleme: {max_preview_rows}×{max_preview_cols}, Gerçek: {rows}×{cols})")
            note.setStyleSheet("color: #7F8C8D; font-size: 10px;")
            note.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.preview_grid.addWidget(note, max_preview_rows, 0, 1, max_preview_cols)
    
    def save(self):
        """Save classroom data"""
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        rows = self.rows_input.value()
        cols = self.cols_input.value()
        seats = self.seats_input.value()
        capacity = rows * cols * seats
        
        if not name:
            QMessageBox.warning(self, "Validation Error", "Classroom name cannot be empty")
            return
        
        user = get_current_user()
        
        if user['role'] == 'admin' and self.dept_combo:
            dept_id = self.dept_combo.currentData()
            if not dept_id:
                QMessageBox.warning(self, "Validation Error", "Please select a department")
                return
        else:
            dept_id = user['department_id']
        
        try:
            if self.is_edit:
                query = """
                    UPDATE classrooms
                    SET department_id = ?, code = ?, name = ?, capacity = ?, rows = ?, cols = ?, seats_per_desk = ?
                    WHERE id = ?
                """
                db_manager.execute_update(query, (dept_id, code, name, capacity, rows, cols, seats, self.classroom_data['id']))
                QMessageBox.information(self, "Success", "Classroom updated successfully!")
            else:
                display_id = db_manager.get_next_display_id('classrooms')
                query = """
                    INSERT INTO classrooms (display_id, department_id, code, name, capacity, rows, cols, seats_per_desk)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                db_manager.execute_update(query, (display_id, dept_id, code, name, capacity, rows, cols, seats))
                QMessageBox.information(self, "Success", "Classroom added successfully!")
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save classroom: {str(e)}")

