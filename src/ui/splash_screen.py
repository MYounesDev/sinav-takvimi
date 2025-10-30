
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSequentialAnimationGroup, QParallelAnimationGroup
from PyQt6.QtGui import QFont, QColor, QLinearGradient, QPalette, QPixmap, QPainter
from PyQt6.QtCore import QSize
from config import COLORS

class SplashScreen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(600, 400)
        
        screen = self.screen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['white']};
                border-radius: 25px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.icon_label = QLabel("📚")
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 120px;
                background: none;
                color: transparent;
                text-shadow: 0 0 0 #27AE60;
            }
        """)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFixedHeight(140)
        layout.addWidget(self.icon_label)
        
        self.title = QLabel("Sınav Planlama Sistemi")
        self.title.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary']};
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 1px;
                background: none;
                margin: 10px 0px;
            }}
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)
        
        self.subtitle = QLabel("Kocaeli University")
        self.subtitle.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_light']};
                font-size: 14px;
                letter-spacing: 2px;
                background: none;
                margin-bottom: 20px;
            }}
        """)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.subtitle)
        
        self.progress = QProgressBar()
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 8px;
                text-align: center;
                height: 6px;
                background-color: #E8F8F5;
                margin: 10px 0px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['primary']},
                    stop:0.5 {COLORS['primary_light']},
                    stop:1 {COLORS['primary_dark']});
                border-radius: 7px;
            }}
        """)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary']};
                font-size: 13px;
                font-weight: 500;
                letter-spacing: 0.5px;
                background: none;
                margin-top: 15px;
            }}
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.loading_dots = QLabel("●")
        self.loading_dots.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary_light']};
                font-size: 16px;
                background: none;
            }}
        """)
        self.loading_dots.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_dots)
        
        self.progress_value = 0
        self.dot_count = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(25)
        
        self.dot_timer = QTimer()
        self.dot_timer.timeout.connect(self.update_loading_dots)
        self.dot_timer.start(500)
    
    def setup_animations(self):
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(600)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in_animation.start()
    
    def update_loading_dots(self):
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_count = 1
        self.loading_dots.setText("●" * self.dot_count)
    
    def update_progress(self):
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        
        if self.progress_value < 25:
            self.status_label.setText("🔄 Loading resources")
        elif self.progress_value < 50:
            self.status_label.setText("🔐 Initializing database")
        elif self.progress_value < 75:
            self.status_label.setText("🎨 Setting up interface")
        elif self.progress_value < 95:
            self.status_label.setText("✨ Final preparations")
        else:
            self.status_label.setText("🚀 Ready to launch")
        
        if self.progress_value >= 100:
            self.timer.stop()
            self.dot_timer.stop()
            self.close_splash()
    
    def close_splash(self):
        fade_out = QPropertyAnimation(self, b"windowOpacity")
        fade_out.setDuration(400)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        fade_out.finished.connect(self.close)
        fade_out.start()
        self._close_animation = fade_out

