"""
Main Window - Application main window with navigation
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QStackedWidget, QPushButton, QLabel, QFrame, QStatusBar)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from src.ui.login_view import LoginView
from src.ui.dashboard_view import DashboardView
from src.ui.classrooms_view import ClassroomsView
from src.ui.courses_view import CoursesView
from src.ui.students_view import StudentsView
from src.ui.exam_schedule_view import ExamScheduleView
from src.ui.seating_plan_view import SeatingPlanView
from src.utils.auth import get_current_user, logout
from src.utils.styles import Styles
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.init_ui()
    
    def changeEvent(self, event):
        """Handle window state changes"""
        super().changeEvent(event)
        # Refresh data when window becomes active
        if event.type() == event.Type.ActivationChange and self.isActiveWindow():
            if self.stacked_widget.currentWidget() == self.app_view:
                current_index = self.content_stack.currentIndex()
                self.refresh_current_page(current_index)
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Exam Scheduler - Kocaeli University")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(Styles.MAIN_WINDOW)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {COLORS['white']};
                color: {COLORS['text_light']};
                border-top: 1px solid {COLORS['border']};
                padding: 5px;
            }}
        """)
        self.status_bar.showMessage("Ready | Press F5 to refresh")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget for switching between login and main app
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Create login view
        self.login_view = LoginView()
        self.login_view.login_successful.connect(self.on_login_successful)
        self.stacked_widget.addWidget(self.login_view)
        
        # Create main app view (will be shown after login)
        self.app_view = QWidget()
        self.setup_app_view()
        self.stacked_widget.addWidget(self.app_view)
        
        # Show login view initially
        self.stacked_widget.setCurrentWidget(self.login_view)
        
        # Add F5 shortcut for manual refresh
        self.refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        self.refresh_shortcut.activated.connect(self.manual_refresh)
    
    def setup_app_view(self):
        """Setup the main application view with sidebar navigation"""
        layout = QHBoxLayout(self.app_view)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self.create_sidebar()
        layout.addWidget(self.sidebar)
        
        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar
        self.top_bar = self.create_top_bar()
        content_layout.addWidget(self.top_bar)
        
        # Content stacked widget
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack)
        
        # Add pages
        self.dashboard_view = DashboardView()
        self.classrooms_view = ClassroomsView()
        self.courses_view = CoursesView()
        self.students_view = StudentsView()
        self.exam_schedule_view = ExamScheduleView()
        self.seating_plan_view = SeatingPlanView()
        
        self.content_stack.addWidget(self.dashboard_view)
        self.content_stack.addWidget(self.classrooms_view)
        self.content_stack.addWidget(self.courses_view)
        self.content_stack.addWidget(self.students_view)
        self.content_stack.addWidget(self.exam_schedule_view)
        self.content_stack.addWidget(self.seating_plan_view)
        
        layout.addWidget(content_widget)
    
    def create_sidebar(self) -> QFrame:
        """Create sidebar navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet(Styles.SIDEBAR)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        # Logo/Title
        title_label = QLabel("📚 Exam Scheduler")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['white']};
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
            }}
        """)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        self.nav_buttons = []
        
        self.add_nav_button("🏠 Dashboard", 0, layout)
        self.add_nav_button("🏫 Classrooms", 1, layout)
        self.add_nav_button("📖 Courses", 2, layout)
        self.add_nav_button("👨‍🎓 Students", 3, layout)
        self.add_nav_button("📅 Exam Schedule", 4, layout)
        self.add_nav_button("💺 Seating Plan", 5, layout)
        
        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet(Styles.SIDEBAR_BUTTON)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return sidebar
    
    def add_nav_button(self, text: str, index: int, layout: QVBoxLayout):
        """Add navigation button to sidebar"""
        btn = QPushButton(text)
        btn.setStyleSheet(Styles.SIDEBAR_BUTTON)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.switch_page(index))
        layout.addWidget(btn)
        self.nav_buttons.append(btn)
        
        # Set first button as checked
        if index == 0:
            btn.setChecked(True)
    
    def create_top_bar(self) -> QFrame:
        """Create top bar with user info"""
        top_bar = QFrame()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(30, 0, 30, 0)
        
        # Page title (will be updated dynamically)
        self.page_title = QLabel("Dashboard")
        self.page_title.setStyleSheet(Styles.TITLE_LABEL)
        layout.addWidget(self.page_title)
        
        layout.addStretch()
        
        # User info
        self.user_label = QLabel()
        self.user_label.setStyleSheet(Styles.NORMAL_LABEL)
        layout.addWidget(self.user_label)
        
        return top_bar
    
    def switch_page(self, index: int):
        """Switch to a different page"""
        self.content_stack.setCurrentIndex(index)
        
        # Update checked state of navigation buttons
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        
        # Update page title
        titles = ["Dashboard", "Classrooms", "Courses", "Students", "Exam Schedule", "Seating Plan"]
        self.page_title.setText(titles[index])
        
        # Refresh data for the selected page
        self.refresh_current_page(index)
    
    def manual_refresh(self):
        """Manually refresh current page (triggered by F5)"""
        if self.stacked_widget.currentWidget() == self.app_view:
            current_index = self.content_stack.currentIndex()
            self.status_bar.showMessage("🔄 Manual refresh (F5)...")
            self.refresh_current_page(current_index)
    
    def refresh_current_page(self, index: int):
        """Refresh data for the current page"""
        try:
            # Show refreshing message
            if not self.status_bar.currentMessage().startswith("🔄"):
                self.status_bar.showMessage("🔄 Refreshing data...")
            
            if index == 0:  # Dashboard
                self.dashboard_view.load_data()
                self.status_bar.showMessage("✅ Dashboard updated", 2000)
            elif index == 1:  # Classrooms
                self.classrooms_view.load_classrooms()
                self.status_bar.showMessage("✅ Classrooms updated", 2000)
            elif index == 2:  # Courses
                self.courses_view.load_courses()
                self.status_bar.showMessage("✅ Courses updated", 2000)
            elif index == 3:  # Students
                self.students_view.load_students()
                self.status_bar.showMessage("✅ Students updated", 2000)
            elif index == 4:  # Exam Schedule
                self.exam_schedule_view.load_schedule()
                self.status_bar.showMessage("✅ Exam schedule updated", 2000)
            elif index == 5:  # Seating Plan
                self.seating_plan_view.load_exams()
                if hasattr(self.seating_plan_view, 'current_exam_id') and self.seating_plan_view.current_exam_id:
                    self.seating_plan_view.load_seating()
                self.status_bar.showMessage("✅ Seating plan updated", 2000)
            
            # Clear status message after 2 seconds
            QTimer.singleShot(2000, lambda: self.status_bar.showMessage("Ready | Press F5 to refresh"))
        except Exception as e:
            error_msg = f"❌ Error refreshing data: {str(e)}"
            self.status_bar.showMessage(error_msg, 5000)
            print(f"Error refreshing page {index}: {e}")
    
    def on_login_successful(self, user: dict):
        """Handle successful login"""
        self.current_user = user
        
        # Update user label
        role_display = "Administrator" if user['role'] == 'admin' else "Coordinator"
        dept_display = f" - {user['department_name']}" if user['department_name'] else ""
        self.user_label.setText(f"👤 {user['name']} ({role_display}){dept_display}")
        
        # Switch to app view
        self.stacked_widget.setCurrentWidget(self.app_view)
        
        # Refresh dashboard
        self.dashboard_view.load_data()
    
    def handle_logout(self):
        """Handle logout"""
        logout()
        self.current_user = None
        
        # Clear login form
        self.login_view.clear_form()
        
        # Switch back to login view
        self.stacked_widget.setCurrentWidget(self.login_view)
        
        # Reset to dashboard
        self.switch_page(0)

