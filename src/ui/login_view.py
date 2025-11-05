"""
Login View - Modern, elegant user authentication screen
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QColor
from src.utils.auth import AuthService, set_current_user
from config import COLORS

class ModernLineEdit(QLineEdit):
    """Custom line edit with modern styling and animations"""
    
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.update_style(False)
        self.setMinimumHeight(48)
        self.setFont(QFont("Segoe UI", 11))
        
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.update_style(True)
        
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.update_style(False)
    
    def update_style(self, focused):
        if focused:
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    border: 2px solid """ + COLORS['primary'] + """;
                    border-radius: 12px;
                    padding: 12px 18px;
                    font-size: 14px;
                    color: """ + COLORS['text'] + """;
                    selection-background-color: """ + COLORS['primary'] + """;
                }
                QLineEdit::placeholder {
                    color: rgba(0, 0, 0, 0.25);
                }
            """)
        else:
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    border: 2px solid #E8E8E8;
                    border-radius: 12px;
                    padding: 12px 18px;
                    font-size: 14px;
                    color: """ + COLORS['text'] + """;
                }
                QLineEdit::placeholder {
                    color: rgba(0, 0, 0, 0.25);
                }
            """)


class ModernButton(QPushButton):
    """Custom button with modern hover effects"""
    
    def __init__(self, text="", is_primary=True):
        super().__init__(text)
        self.is_primary = is_primary
        self.setMinimumHeight(50)
        self.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_style()
        
    def update_style(self):
        if self.is_primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {COLORS['primary']},
                        stop:1 {COLORS['primary_light']});
                    color: #FFFFFF;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 13px;
                    font-weight: bold;
                    letter-spacing: 0.5px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {COLORS['primary_light']},
                        stop:1 {COLORS['primary']});
                    box-shadow: 0 8px 20px rgba(39, 174, 96, 0.3);
                }}
                QPushButton:pressed {{
                    background: {COLORS['primary_dark']};
                }}
            """)


class LoginView(QWidget):
    """Modern login screen with smooth animations"""
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        """Initialize the UI with modern design"""
        # Main background
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F0F4F8,
                    stop:0.5 #F8FAFB,
                    stop:1 #F0F4F8);
            }}
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left side - Decorative panel
        left_panel = QFrame()
        left_panel.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['primary']},
                    stop:1 {COLORS['secondary']});
                border: none;
            }}
        """)
        left_panel.setMinimumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(60, 60, 60, 60)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Decorative content on left
        left_title = QLabel("Welcome Back")
        left_title.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 42px;
                font-weight: 700;
                letter-spacing: 1px;
            }
        """)
        left_layout.addWidget(left_title)
        
        left_subtitle = QLabel("Exam Planning System")
        left_subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: 300;
                margin-top: 15px;
            }
        """)
        left_layout.addWidget(left_subtitle)
        
        left_description = QLabel(
            "Manage your exam scheduling efficiently with our modern platform"
        )
        left_description.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                font-weight: 300;
                margin-top: 30px;
                line-height: 1.6;
            }
        """)
        left_description.setWordWrap(True)
        left_layout.addWidget(left_description)
        left_layout.addStretch()
        
        main_layout.addWidget(left_panel)
        
        # Right side - Login form
        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { background-color: #FFFFFF; border: none; }")
        right_panel.setMinimumWidth(500)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setSpacing(30)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Form title
        form_title = QLabel("Sign In")
        form_title.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 32px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}
        """)
        right_layout.addWidget(form_title)
        
        # Form subtitle
        form_subtitle = QLabel("Enter your credentials to access the system")
        form_subtitle.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 14px;
                font-weight: 300;
                margin-top: -20px;
            }}
        """)
        right_layout.addWidget(form_subtitle)
        
        right_layout.addSpacing(10)
        
        # Email input
        email_label = QLabel("Email Address")
        email_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 0.3px;
            }}
        """)
        right_layout.addWidget(email_label)
        
        self.email_input = ModernLineEdit("admin@gmail.com")
        self.email_input.returnPressed.connect(self.handle_login)
        right_layout.addWidget(self.email_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 0.3px;
            }}
        """)
        right_layout.addWidget(password_label)
        
        self.password_input = ModernLineEdit("admin123")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.handle_login)
        right_layout.addWidget(self.password_input)
        
        right_layout.addSpacing(15)
        
        # Login button
        self.login_btn = ModernButton("Sign In", True)
        self.login_btn.clicked.connect(self.handle_login)
        right_layout.addWidget(self.login_btn)
        
        # Info section
        right_layout.addSpacing(20)
        
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #F0F9FF;
                border-radius: 12px;
                border: 1px solid """ + COLORS['primary'] + """22;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        info_layout.setSpacing(8)
        
        info_title = QLabel("Demo Credentials")
        info_title.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary']};
                font-size: 12px;
                font-weight: 600;
            }}
        """)
        info_layout.addWidget(info_title)
        
        admin_info = QLabel("Admin: admin@gmail.com / admin123")
        admin_info.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 11px;
            }}
        """)
        info_layout.addWidget(admin_info)
        
        coord_info = QLabel("Coordinators: bilgisayar@gmail.com (all use password: admin123)")
        coord_info.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 11px;
            }}
        """)
        info_layout.addWidget(coord_info)
        
        right_layout.addWidget(info_frame)
        right_layout.addStretch()
        
        main_layout.addWidget(right_panel)
    
    def setup_animations(self):
        """Setup entrance animations"""
        # Fade in animation
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(effect)
        
        fade_animation = QPropertyAnimation(effect, b"opacity")
        fade_animation.setDuration(800)
        fade_animation.setStartValue(0)
        fade_animation.setEndValue(1)
        fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        fade_animation.start()
        self._fade_animation = fade_animation
    
    def handle_login(self):
        """Handle login button click"""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            self.show_error("Please enter both email and password")
            return
        
        user = AuthService.login(email, password)
        
        if user:
            set_current_user(user)
            self.login_successful.emit(user)
        else:
            self.show_error("Invalid email or password")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def show_error(self, message: str):
        """Show error message with modern styling"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Login Error")
        msg.setText(message)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: #FFFFFF;
            }}
            QMessageBox QLabel {{
                color: {COLORS['text']};
                font-size: 13px;
            }}
            QMessageBox QPushButton {{
                background-color: {COLORS['primary']};
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                min-width: 60px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {COLORS['primary_light']};
            }}
        """)
        msg.exec()
    
    def clear_form(self):
        """Clear login form"""
        self.email_input.clear()
        self.password_input.clear()

