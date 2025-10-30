"""
Main Window - Application main window with navigation
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QStackedWidget, QPushButton, QLabel, QFrame, QStatusBar, QMenu)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from src.ui.login_view import LoginView
from src.ui.dashboard_view import DashboardView
from src.ui.classrooms_view import ClassroomsView
from src.ui.courses_view import CoursesView
from src.ui.students_view import StudentsView
from src.ui.exam_schedule_view import ExamScheduleView
from src.ui.seating_plan_view import SeatingPlanView
from src.ui.users_view import UsersView
from src.ui.departments_view import DepartmentsView
from src.utils.auth import get_current_user, logout
from src.utils.styles import Styles
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.sidebar_expanded = True
        self.init_ui()
    
    def changeEvent(self, event):
        """Handle window state changes"""
        super().changeEvent(event)
        if event.type() == event.Type.ActivationChange and self.isActiveWindow():
            if self.stacked_widget.currentWidget() == self.app_view:
                current_index = self.content_stack.currentIndex()
                self.refresh_current_page(current_index)
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Sınav Planlama Sistemi - Kocaeli Üniversitesi")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(Styles.MAIN_WINDOW)
        
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
        self.status_bar.showMessage("Hazır | F5 ile yenile")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        self.login_view = LoginView()
        self.login_view.login_successful.connect(self.on_login_successful)
        self.stacked_widget.addWidget(self.login_view)
        
        self.app_view = QWidget()
        self.setup_app_view()
        self.stacked_widget.addWidget(self.app_view)
        
        self.stacked_widget.setCurrentWidget(self.login_view)
        
        self.refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        self.refresh_shortcut.activated.connect(self.manual_refresh)
    
    def setup_app_view(self):
        """Setup the main application view with sidebar navigation"""
        layout = QHBoxLayout(self.app_view)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.sidebar = self.create_sidebar()
        self.sidebar.setMinimumWidth(250)
        self.sidebar.setMaximumWidth(250)
        layout.addWidget(self.sidebar)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        self.top_bar = self.create_top_bar()
        content_layout.addWidget(self.top_bar)
        
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack)
        
        self.dashboard_view = DashboardView()
        self.classrooms_view = ClassroomsView()
        self.courses_view = CoursesView()
        self.students_view = StudentsView()
        self.exam_schedule_view = ExamScheduleView()
        self.seating_plan_view = SeatingPlanView()
        self.users_view = UsersView()
        self.departments_view = DepartmentsView()
        
        self.content_stack.addWidget(self.dashboard_view)
        self.content_stack.addWidget(self.classrooms_view)
        self.content_stack.addWidget(self.courses_view)
        self.content_stack.addWidget(self.students_view)
        self.content_stack.addWidget(self.exam_schedule_view)
        self.content_stack.addWidget(self.seating_plan_view)
        self.content_stack.addWidget(self.users_view)
        self.content_stack.addWidget(self.departments_view)
        
        layout.addWidget(content_widget)
    
    def create_sidebar(self) -> QFrame:
        """Create sidebar navigation"""
        sidebar = QFrame()
        sidebar.setStyleSheet(Styles.SIDEBAR)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        header_layout = QHBoxLayout()
        
        toggle_btn = QPushButton("☰")
        toggle_btn.setMaximumWidth(40)
        toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['white']};
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_light']};
            }}
        """)
        toggle_btn.clicked.connect(self.toggle_sidebar)
        header_layout.addWidget(toggle_btn)
        
        title_label = QLabel("📚 Sınav Planlama")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['white']};
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
            }}
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addSpacing(20)
        
        self.nav_buttons = []
        
        self.add_nav_button("🏠 Gösterge Paneli", 0, layout)
        self.add_nav_button("🏫 Sınıflar", 1, layout)
        self.add_nav_button("📖 Dersler", 2, layout)
        self.add_nav_button("👨‍🎓 Öğrenciler", 3, layout)
        self.add_nav_button("📅 Sınav Programı", 4, layout)
        self.add_nav_button("💺 Oturma Düzeni", 5, layout)
        
        self.admin_users_btn = None
        self.admin_depts_btn = None
        
        layout.addStretch()
        
        logout_btn = QPushButton("🚪 Çıkış")
        logout_btn.setStyleSheet(Styles.SIDEBAR_BUTTON)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return sidebar
    
    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.setMinimumWidth(60)
            self.sidebar.setMaximumWidth(60)
            self.sidebar_expanded = False
            for btn in self.nav_buttons:
                btn.setText("  " + btn.text().split()[-1])
        else:
            self.sidebar.setMinimumWidth(250)
            self.sidebar.setMaximumWidth(250)
            self.sidebar_expanded = True
            titles = ["🏠 Gösterge Paneli", "🏫 Sınıflar", "📖 Dersler", "👨‍🎓 Öğrenciler", "📅 Sınav Programı", "💺 Oturma Düzeni"]
            for i, btn in enumerate(self.nav_buttons):
                if i < len(titles):
                    btn.setText(titles[i])
    
    def add_nav_button(self, text: str, index: int, layout: QVBoxLayout):
        """Add navigation button to sidebar"""
        btn = QPushButton(text)
        btn.setStyleSheet(Styles.SIDEBAR_BUTTON)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.switch_page(index))
        layout.addWidget(btn)
        self.nav_buttons.append(btn)
        
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
        
        self.page_title = QLabel("Gösterge Paneli")
        self.page_title.setStyleSheet(Styles.TITLE_LABEL)
        layout.addWidget(self.page_title)
        
        layout.addStretch()
        
        self.admin_menu_btn = QPushButton("⚙️ Yönetim")
        self.admin_menu_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['white']};
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_light']};
            }}
        """)
        self.admin_menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.admin_menu_btn.hide()
        self.admin_menu = QMenu(self.admin_menu_btn)
        self.admin_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['white']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['primary_light']};
            }}
        """)
        self.admin_menu_btn.setMenu(self.admin_menu)
        layout.addWidget(self.admin_menu_btn)
        
        self.user_label = QLabel()
        self.user_label.setStyleSheet(Styles.NORMAL_LABEL)
        layout.addWidget(self.user_label)
        
        return top_bar
    
    def switch_page(self, index: int):
        """Switch to a different page"""
        self.content_stack.setCurrentIndex(index)
        
        for i, btn in enumerate(self.nav_buttons):
            try:
                btn.setChecked(i == index)
            except RuntimeError:
                continue
        
        user = get_current_user()
        titles = ["Gösterge Paneli", "Sınıflar", "Dersler", "Öğrenciler", "Sınav Programı", "Oturma Düzeni"]
        if user and user['role'] == 'admin':
            titles.extend(["Kullanıcılar", "Bölümler"])
        if index < len(titles):
            self.page_title.setText(titles[index])
        
        self.refresh_current_page(index)
    
    def manual_refresh(self):
        """Manually refresh current page (triggered by F5)"""
        if self.stacked_widget.currentWidget() == self.app_view:
            current_index = self.content_stack.currentIndex()
            self.status_bar.showMessage("🔄 El ile yenileme (F5)...")
            self.refresh_current_page(current_index)
    
    def refresh_current_page(self, index: int):
        """Refresh data for the current page"""
        try:
            if not self.status_bar.currentMessage().startswith("🔄"):
                self.status_bar.showMessage("🔄 Veriler yenileniyor...")
            
            if index == 0:  
                self.dashboard_view.load_data()
                self.status_bar.showMessage("✅ Gösterge paneli güncellendi", 2000)
            elif index == 1:  
                self.classrooms_view.load_classrooms()
                self.status_bar.showMessage("✅ Sınıflar güncellendi", 2000)
            elif index == 2:  
                self.courses_view.load_courses()
                self.status_bar.showMessage("✅ Dersler güncellendi", 2000)
            elif index == 3:  
                self.students_view.load_students()
                self.status_bar.showMessage("✅ Öğrenciler güncellendi", 2000)
            elif index == 4:  
                self.exam_schedule_view.load_schedule()
                self.status_bar.showMessage("✅ Sınav programı güncellendi", 2000)
            elif index == 5:  
                self.seating_plan_view.load_exams()
                if hasattr(self.seating_plan_view, 'current_exam_id') and self.seating_plan_view.current_exam_id:
                    self.seating_plan_view.load_seating()
                self.status_bar.showMessage("✅ Oturma düzeni güncellendi", 2000)
            elif index == 6:  
                self.users_view.load_users()
                self.status_bar.showMessage("✅ Kullanıcılar güncellendi", 2000)
            elif index == 7:  
                self.departments_view.load_departments()
                self.status_bar.showMessage("✅ Bölümler güncellendi", 2000)
            
            QTimer.singleShot(2000, lambda: self.status_bar.showMessage("Hazır | F5 ile yenile"))
        except Exception as e:
            error_msg = f"❌ Hata: {str(e)}"
            self.status_bar.showMessage(error_msg, 5000)
            print(f"Sayfa {index} yenilenemedi: {e}")
    
    def on_login_successful(self, user: dict):
        """Handle successful login"""
        self.current_user = user
        
        if user['role'] == 'admin':
            self.admin_menu.clear()
            users_action = self.admin_menu.addAction("👥 Kullanıcılar")
            users_action.triggered.connect(lambda: self.switch_page(6))
            
            depts_action = self.admin_menu.addAction("🏢 Bölümler")
            depts_action.triggered.connect(lambda: self.switch_page(7))
            
            self.admin_menu_btn.show()
        
        role_display = "Yönetici" if user['role'] == 'admin' else "Koordinatör"
        dept_display = f" - {user['department_name']}" if user.get('department_name') else ""
        self.user_label.setText(f"👤 {user['name']} ({role_display}){dept_display}")
        
        self.stacked_widget.setCurrentWidget(self.app_view)
        
        self.dashboard_view.load_data()
    
    def handle_logout(self):
        """Handle logout"""
        logout()
        self.current_user = None
        
        self.admin_menu.clear()
        self.admin_menu_btn.hide()
        
        self.login_view.clear_form()
        
        self.stacked_widget.setCurrentWidget(self.login_view)
        
        self.switch_page(0)

