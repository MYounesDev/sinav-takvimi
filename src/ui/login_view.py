"""
Login View - User authentication screen
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from src.utils.auth import AuthService, set_current_user
from src.utils.styles import Styles, apply_shadow
from src.utils.animations import AnimationHelper
from config import COLORS


class LoginView(QWidget):
    """Login screen widget"""
    
    # Signal emitted when login is successful
    login_successful = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Center the login form
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Login card
        login_card = self.create_login_card()
        center_layout.addWidget(login_card)
        
        main_layout.addWidget(center_widget)
        
        # Set background
        self.setStyleSheet(f"QWidget {{ background-color: {COLORS['light']}; }}")
        
        # Apply entrance animation (disabled due to QPainter conflicts)
        # AnimationHelper.fade_in(self, 500)
    
    def create_login_card(self) -> QFrame:
        """Create the login form card"""
        card = QFrame()
        card.setFixedWidth(450)
        card.setStyleSheet(Styles.CARD)
        # apply_shadow(card)  # Temporarily disabled due to QPainter conflicts
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Logo/Title
        title = QLabel("Exam Scheduler")
        title.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary']};
                font-size: 32px;
                font-weight: bold;
            }}
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Kocaeli University")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 16px;
            }}
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Email input
        email_label = QLabel("Email")
        email_label.setStyleSheet(Styles.NORMAL_LABEL)
        layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet(Styles.LINE_EDIT)
        self.email_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.email_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet(Styles.NORMAL_LABEL)
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(Styles.LINE_EDIT)
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(10)
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        # Default credentials hint
        hint_label = QLabel("Admin: admin@gmail.com / admin123")
        hint_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 12px;
                font-style: italic;
            }}
        """)
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint_label)
        
        # Coordinators hint
        coord_hint = QLabel("Koordinatörler: bilgisayar@kocaeli.edu.tr, yazilim@kocaeli.edu.tr")
        coord_hint.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 11px;
                font-style: italic;
            }}
        """)
        coord_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(coord_hint)
        
        return card
    
    def handle_login(self):
        """Handle login button click"""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            self.show_error("Please enter both email and password")
            return
        
        # Attempt login
        user = AuthService.login(email, password)
        
        if user:
            set_current_user(user)
            
            # Fade out and emit signal (disabled due to QPainter conflicts)
            # AnimationHelper.fade_out(self, 300, lambda: self.login_successful.emit(user))
            self.login_successful.emit(user)
        else:
            self.show_error("Invalid email or password")
            self.password_input.clear()
            # AnimationHelper.bounce(self.sender().parent() if hasattr(self.sender(), 'parent') else self)
    
    def show_error(self, message: str):
        """Show error message"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Login Error")
        msg.setText(message)
        msg.setStyleSheet(Styles.MESSAGE_BOX)
        msg.exec()
    
    def clear_form(self):
        """Clear login form"""
        self.email_input.clear()
        self.password_input.clear()

