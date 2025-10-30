"""
Dashboard View - Modern, interactive statistics and overview
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QColor, QFont
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from config import COLORS


class ModernStatCard(QFrame):
    """Modern statistics card with hover effects and animations"""
    
    def __init__(self, title: str, value: str, icon: str, color: str):
        super().__init__()
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color
        self.init_ui()
        self.setup_shadow()
        
    def init_ui(self):
        """Initialize card UI"""
        self.setMinimumHeight(160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E8EEF5;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Top row with icon and accent line
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(12)
        
        # Icon - properly sized and centered
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 42px;
                background: none;
                line-height: 42px;
                min-width: 50px;
                min-height: 50px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(50, 50)
        top_layout.addWidget(icon_label)
        
        # Spacer
        top_layout.addStretch()
        
        # Accent bar
        accent_bar = QFrame()
        accent_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color};
                border-radius: 3px;
            }}
        """)
        accent_bar.setFixedSize(5, 45)
        top_layout.addWidget(accent_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(top_layout, 1)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.5px;
                background: none;
                line-height: 16px;
            }}
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                font-size: 36px;
                font-weight: 700;
                background: none;
                line-height: 42px;
            }}
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.value_label)
        
        layout.addStretch()
    
    def setup_shadow(self):
        """Add modern shadow effect"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)
    
    def enterEvent(self, event):
        """Handle mouse enter with animation"""
        super().enterEvent(event)
        self.animate_hover(True)
    
    def leaveEvent(self, event):
        """Handle mouse leave with animation"""
        super().leaveEvent(event)
        self.animate_hover(False)
    
    def animate_hover(self, is_hover):
        """Animate on hover"""
        if is_hover:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: #FFFFFF;
                    border-radius: 16px;
                    border: 1px solid {self.color}40;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: #FFFFFF;
                    border-radius: 16px;
                    border: 1px solid #E8EEF5;
                }}
            """)


class DashboardView(QWidget):
    """Modern dashboard with refined layout and smooth animations"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        """Initialize the dashboard UI"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)
        
        # Greeting title
        user = get_current_user()
        user_name = user['name'] if user else 'User'
        
        welcome_label = QLabel(f"Welcome back, {user_name}")
        welcome_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 28px;
                font-weight: 700;
                letter-spacing: 0.5px;
                line-height: 32px;
            }}
        """)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        welcome_label.setMinimumHeight(32)
        header_layout.addWidget(welcome_label)
        
        # Subtitle with date/status
        subtitle = QLabel("Here's your system overview")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 14px;
                font-weight: 300;
                letter-spacing: 0.3px;
                line-height: 18px;
            }}
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        subtitle.setMinimumHeight(18)
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)
        
        # Stats grid section
        stats_label = QLabel("System Statistics")
        stats_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.3px;
                line-height: 20px;
            }}
        """)
        stats_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        stats_label.setMinimumHeight(20)
        layout.addWidget(stats_label)
        
        # Create stats grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setColumnStretch(0, 1)
        stats_layout.setColumnStretch(1, 1)
        
        # Color palette for cards
        colors = [
            COLORS['primary'],      # Green
            COLORS['secondary'],    # Teal
            COLORS['warning'],      # Orange
            COLORS['danger'],       # Red
        ]
        
        icons = ["📚", "👨‍💼", "👨‍🎓", "📅"]
        titles = ["Courses", "Departments", "Students", "Scheduled Exams"]
        
        self.stat_cards = []
        
        for i, (title, icon, color) in enumerate(zip(titles, icons, colors)):
            card = ModernStatCard(title, "0", icon, color)
            self.stat_cards.append(card)
            row = i // 2
            col = i % 2
            stats_layout.addWidget(card, row, col)
        
        layout.addLayout(stats_layout)
        
        # Additional info section
        layout.addSpacing(10)
        
        info_section = QFrame()
        info_section.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['primary']}08,
                    stop:1 {COLORS['secondary']}08);
                border-radius: 14px;
                border: 1px solid {COLORS['primary']}20;
            }}
        """)
        info_section.setMinimumHeight(90)
        info_layout = QVBoxLayout(info_section)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(10)
        
        info_title = QLabel("Quick Tip")
        info_title.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary']};
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 0.5px;
                line-height: 16px;
            }}
        """)
        info_title.setMinimumHeight(16)
        info_layout.addWidget(info_title)
        
        info_text = QLabel(
            "Use the navigation menu on the left to manage courses, classrooms, students, and exam schedules."
        )
        info_text.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 13px;
                font-weight: 300;
                line-height: 1.5;
            }}
        """)
        info_text.setWordWrap(True)
        info_text.setMinimumHeight(50)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_section)
        
        layout.addStretch()
    
    def setup_animations(self):
        """Setup entrance animations"""
        # Stagger animation for cards
        for i, card in enumerate(self.stat_cards):
            QTimer.singleShot(i * 100, lambda c=card: self.animate_card_in(c))
    
    def animate_card_in(self, card):
        """Animate card entrance"""
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        effect = QGraphicsOpacityEffect()
        card.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(600)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        card._entrance_animation = animation
    
    def load_data(self):
        """Load and display statistics"""
        user = get_current_user()
        if not user:
            return
        
        dept_filter = "" if user['role'] == 'admin' else f"WHERE department_id = {user['department_id']}"
        
        # Load courses
        query = f"SELECT COUNT(*) as count FROM courses {dept_filter}"
        result = db_manager.execute_query(query)
        self.stat_cards[0].value_label.setText(str(result[0]['count']))
        
        # Load departments
        query = "SELECT COUNT(*) as count FROM departments"
        result = db_manager.execute_query(query)
        self.stat_cards[1].value_label.setText(str(result[0]['count']))
        
        # Load students
        query = f"SELECT COUNT(*) as count FROM students {dept_filter}"
        result = db_manager.execute_query(query)
        self.stat_cards[2].value_label.setText(str(result[0]['count']))
        
        # Load exams
        query = f"SELECT COUNT(*) as count FROM exams {dept_filter}"
        result = db_manager.execute_query(query)
        self.stat_cards[3].value_label.setText(str(result[0]['count']))

