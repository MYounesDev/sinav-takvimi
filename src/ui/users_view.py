"""
Users View - Manage users and coordinators (Admin only)
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QDialog, QFormLayout, QLineEdit, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user, AuthService
from src.utils.styles import Styles


class UsersView(QWidget):
    """Users management view (Admin only)"""
    
    def __init__(self):
        super().__init__()
        self.all_users = []  # Store all users for filtering
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Top bar with actions
        top_bar = QHBoxLayout()
        
        title = QLabel("User Management")
        title.setStyleSheet(Styles.SUBTITLE_LABEL)
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        # Add user button
        add_btn = QPushButton("➕ Add User")
        add_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.add_user)
        top_bar.addWidget(add_btn)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_users)
        top_bar.addWidget(refresh_btn)
        
        layout.addLayout(top_bar)
        
        # Search bar
        search_bar = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        search_label.setStyleSheet(Styles.NORMAL_LABEL)
        search_bar.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID, Name, or Email...")
        self.search_input.setStyleSheet(Styles.LINE_EDIT)
        self.search_input.textChanged.connect(self.filter_users)
        search_bar.addWidget(self.search_input)
        
        layout.addLayout(search_bar)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Email", "Role", "Department", "Created"
        ])
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)  # Enable column sorting
        layout.addWidget(self.table)
        
        # Action buttons
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_user)
        action_bar.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet(Styles.DANGER_BUTTON)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_user)
        action_bar.addWidget(delete_btn)
        
        layout.addLayout(action_bar)
        
        # Load data
        self.load_users()
    
    def load_users(self):
        """Load users from database"""
        query = """
            SELECT u.id, u.display_id, u.name, u.email, u.role, u.created_at,
                   u.department_id, d.name as department_name, d.code as department_code
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
            ORDER BY u.role, u.name
        """
        
        users = db_manager.execute_query(query)
        self.all_users = users  # Store for filtering
        self.populate_table(users)
    
    def populate_table(self, users):
        """Populate table with user data"""
        # Disable sorting while populating
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # Show display_id to user, but keep internal id for operations
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.DisplayRole, int(user['display_id']))
            id_item.setData(Qt.ItemDataRole.UserRole, user['id'])  # Store real ID
            self.table.setItem(row, 0, id_item)
            
            self.table.setItem(row, 1, QTableWidgetItem(user['name']))
            self.table.setItem(row, 2, QTableWidgetItem(user['email']))
            
            role_text = "Administrator" if user['role'] == 'admin' else "Coordinator"
            self.table.setItem(row, 3, QTableWidgetItem(role_text))
            
            dept_text = f"{user['department_name']} ({user['department_code']})" if user['department_name'] else "N/A"
            self.table.setItem(row, 4, QTableWidgetItem(dept_text))
            
            created = user['created_at'] or "N/A"
            self.table.setItem(row, 5, QTableWidgetItem(str(created)))
        
        # Re-enable sorting
        self.table.setSortingEnabled(True)
    
    def filter_users(self):
        """Filter users based on search text"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            # Show all users
            self.populate_table(self.all_users)
            return
        
        # Filter users
        filtered = []
        for user in self.all_users:
            # Search in display_id, name, and email
            if (str(user['display_id']).lower().find(search_text) != -1 or
                user['name'].lower().find(search_text) != -1 or
                user['email'].lower().find(search_text) != -1):
                filtered.append(user)
        
        self.populate_table(filtered)
    
    def add_user(self):
        """Open dialog to add new user"""
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_users()
    
    def edit_user(self):
        """Edit selected user"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a user to edit")
            return
        
        # Get internal id from hidden data
        user_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # Get user data
        query = """
            SELECT u.*, d.name as department_name, d.code as department_code
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = ?
        """
        result = db_manager.execute_query(query, (user_id,))
        
        if result:
            dialog = UserDialog(self, dict(result[0]))
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_users()
    
    def delete_user(self):
        """Delete selected user"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a user to delete")
            return
        
        # Get internal id from hidden data
        user_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        user_name = self.table.item(row, 1).text()
        user_role = self.table.item(row, 3).text()
        
        # Prevent deleting own account
        current_user = get_current_user()
        if current_user and current_user['id'] == user_id:
            QMessageBox.warning(self, "Cannot Delete", "You cannot delete your own account!")
            return
        
        # Prevent deleting last admin
        if user_role == "Administrator":
            admin_count = db_manager.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'admin'")
            if admin_count[0]['count'] <= 1:
                QMessageBox.warning(self, "Cannot Delete", "Cannot delete the last administrator!")
                return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete user '{user_name}'?\n\n"
            f"The ID will be reused for future entries.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM users WHERE id = ?"
            db_manager.execute_update(query, (user_id,))
            QMessageBox.information(self, "Success", "User deleted successfully!")
            self.load_users()


class UserDialog(QDialog):
    """Dialog for adding/editing users"""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.is_edit = user_data is not None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Edit User" if self.is_edit else "Add User")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(Styles.LINE_EDIT)
        form_layout.addRow("Name:", self.name_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(Styles.LINE_EDIT)
        form_layout.addRow("Email:", self.email_input)
        
        # Password (only for new users)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(Styles.LINE_EDIT)
        if self.is_edit:
            self.password_input.setPlaceholderText("Leave blank to keep current password")
        else:
            form_layout.addRow("Password:", self.password_input)
        if self.is_edit:
            form_layout.addRow("New Password (optional):", self.password_input)
        
        # Role
        self.role_combo = QComboBox()
        self.role_combo.setStyleSheet(Styles.COMBO_BOX)
        self.role_combo.addItem("Coordinator", "coordinator")
        self.role_combo.addItem("Administrator", "admin")
        self.role_combo.currentIndexChanged.connect(self.on_role_changed)
        form_layout.addRow("Role:", self.role_combo)
        
        # Department (only for coordinators)
        self.dept_combo = QComboBox()
        self.dept_combo.setStyleSheet(Styles.COMBO_BOX)
        self.dept_combo.addItem("N/A", None)
        departments = db_manager.execute_query("SELECT id, name, code FROM departments ORDER BY name")
        for dept in departments:
            self.dept_combo.addItem(f"{dept['name']} ({dept['code']})", dept['id'])
        form_layout.addRow("Department:", self.dept_combo)
        
        layout.addLayout(form_layout)
        
        # Load existing data if editing
        if self.is_edit:
            self.name_input.setText(self.user_data['name'])
            self.email_input.setText(self.user_data['email'])
            self.email_input.setReadOnly(True)  # Email cannot be changed
            
            role_index = self.role_combo.findData(self.user_data['role'])
            if role_index >= 0:
                self.role_combo.setCurrentIndex(role_index)
            
            if self.user_data.get('department_id'):
                dept_index = self.dept_combo.findData(self.user_data['department_id'])
                if dept_index >= 0:
                    self.dept_combo.setCurrentIndex(dept_index)
        
        # Buttons
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
        
        # Set initial state
        self.on_role_changed()
    
    def on_role_changed(self):
        """Handle role change"""
        role = self.role_combo.currentData()
        # Admin should not have department
        if role == 'admin':
            self.dept_combo.setCurrentIndex(0)  # Set to N/A
            self.dept_combo.setEnabled(False)
        else:
            self.dept_combo.setEnabled(True)
    
    def save(self):
        """Save user data"""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_combo.currentData()
        dept_id = self.dept_combo.currentData() if role != 'admin' else None
        
        if not name or not email:
            QMessageBox.warning(self, "Validation Error", "Name and email are required")
            return
        
        try:
            if self.is_edit:
                # Update existing user
                user_id = self.user_data['id']
                
                # Check if password should be updated
                password = self.password_input.text().strip()
                if password:
                    hashed_password = AuthService.hash_password(password)
                    query = """
                        UPDATE users
                        SET name = ?, role = ?, department_id = ?, password = ?
                        WHERE id = ?
                    """
                    db_manager.execute_update(query, (name, role, dept_id, hashed_password, user_id))
                else:
                    query = """
                        UPDATE users
                        SET name = ?, role = ?, department_id = ?
                        WHERE id = ?
                    """
                    db_manager.execute_update(query, (name, role, dept_id, user_id))
                
                QMessageBox.information(self, "Success", "User updated successfully!")
            else:
                # Create new user
                password = self.password_input.text().strip()
                if not password:
                    QMessageBox.warning(self, "Validation Error", "Password is required for new users")
                    return
                
                # Get next available display_id
                display_id = db_manager.get_next_display_id('users')
                hashed_password = AuthService.hash_password(password)
                query = """
                    INSERT INTO users (display_id, name, email, password, role, department_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                db_manager.execute_update(query, (display_id, name, email, hashed_password, role, dept_id))
                QMessageBox.information(self, "Success", f"User created successfully with ID: {display_id}")
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save user: {str(e)}")

