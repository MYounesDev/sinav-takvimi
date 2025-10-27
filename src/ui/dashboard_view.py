"""
Dashboard View - Overview and statistics
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout)
from PyQt6.QtCore import Qt
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from src.utils.styles import Styles, apply_shadow
from config import COLORS


class DashboardView(QWidget):
    """Dashboard with statistics and overview"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Welcome message
        welcome_label = QLabel("Welcome to Exam Scheduler")
        welcome_label.setStyleSheet(Styles.TITLE_LABEL)
        layout.addWidget(welcome_label)
        
        # Statistics cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)
        
        self.classrooms_card = self.create_stat_card("Classrooms", "0", "🏫", COLORS['primary'])
        self.courses_card = self.create_stat_card("Courses", "0", "📖", COLORS['secondary'])
        self.students_card = self.create_stat_card("Students", "0", "👨‍🎓", COLORS['success'])
        self.exams_card = self.create_stat_card("Scheduled Exams", "0", "📅", COLORS['warning'])
        
        stats_layout.addWidget(self.classrooms_card, 0, 0)
        stats_layout.addWidget(self.courses_card, 0, 1)
        stats_layout.addWidget(self.students_card, 0, 2)
        stats_layout.addWidget(self.exams_card, 0, 3)
        
        layout.addLayout(stats_layout)
        
        layout.addStretch()
    
    def create_stat_card(self, title: str, value: str, icon: str, color: str) -> QFrame:
        """Create a statistics card"""
        card = QFrame()
        card.setFixedHeight(150)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 12px;
                border-left: 5px solid {color};
                border: 1px solid {COLORS['border']};
            }}
        """)
        # apply_shadow(card)  # Temporarily disabled due to QPainter conflicts
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Icon and value
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 40px;")
        top_layout.addWidget(icon_label)
        
        top_layout.addStretch()
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 36px;
                font-weight: bold;
            }}
        """)
        top_layout.addWidget(value_label)
        
        layout.addLayout(top_layout)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 16px;
            }}
        """)
        layout.addWidget(title_label)
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def load_data(self):
        """Load and display statistics"""
        user = get_current_user()
        if not user:
            return
        
        dept_filter = "" if user['role'] == 'admin' else f"WHERE department_id = {user['department_id']}"
        
        # Count classrooms
        query = f"SELECT COUNT(*) as count FROM classrooms {dept_filter}"
        result = db_manager.execute_query(query)
        self.classrooms_card.value_label.setText(str(result[0]['count']))
        
        # Count courses
        query = f"SELECT COUNT(*) as count FROM courses {dept_filter}"
        result = db_manager.execute_query(query)
        self.courses_card.value_label.setText(str(result[0]['count']))
        
        # Count students
        query = f"SELECT COUNT(*) as count FROM students {dept_filter}"
        result = db_manager.execute_query(query)
        self.students_card.value_label.setText(str(result[0]['count']))
        
        # Count exams
        query = f"SELECT COUNT(*) as count FROM exams {dept_filter}"
        result = db_manager.execute_query(query)
        self.exams_card.value_label.setText(str(result[0]['count']))

