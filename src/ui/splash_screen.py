"""
Splash Screen - Animated startup screen
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from config import COLORS


class SplashScreen(QWidget):
    """Animated splash screen shown during startup"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        # Window settings
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(500, 350)
        
        # Center on screen
        screen = self.screen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Background
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['white']};
                border-radius: 20px;
                border: 3px solid {COLORS['primary']};
            }}
        """)
        
        # Logo/Icon
        icon_label = QLabel("📚")
        icon_label.setStyleSheet("font-size: 80px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title = QLabel("Exam Scheduler")
        title.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary']};
                font-size: 32px;
                font-weight: bold;
                margin-top: 20px;
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
                margin-bottom: 30px;
            }}
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {COLORS['border']};
                border-radius: 10px;
                text-align: center;
                height: 20px;
                background-color: {COLORS['light']};
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['primary']};
                border-radius: 8px;
            }}
        """)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        
        # Status label
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 12px;
                margin-top: 10px;
            }}
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Start progress animation
        self.progress_value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(20)
    
    def update_progress(self):
        """Update progress bar"""
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        
        # Update status text
        if self.progress_value < 30:
            self.status_label.setText("Loading resources...")
        elif self.progress_value < 60:
            self.status_label.setText("Initializing database...")
        elif self.progress_value < 90:
            self.status_label.setText("Setting up UI...")
        else:
            self.status_label.setText("Almost ready...")
        
        # Close when done
        if self.progress_value >= 100:
            self.timer.stop()
            QTimer.singleShot(300, self.close)



