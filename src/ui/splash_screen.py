
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QParallelAnimationGroup, QRect, QSize
from PyQt6.QtGui import QFont, QColor, QLinearGradient, QPalette, QPixmap, QPainter
from config import COLORS

class SplashScreen(QWidget):
    """Modern futuristic splash screen with premium animations"""
    
    def __init__(self):
        super().__init__()
        self.progress_value = 0
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        """Initialize the UI with modern design"""
        # Window setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Modern size (16:9 aspect ratio)
        self.setFixedSize(900, 600)
        
        # Center on screen
        screen = self.screen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
        
        # Set gradient background
        self.setup_gradient_background()
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create content container with proper sizing
        content_widget = QWidget()
        content_widget.setObjectName("content")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Animated Logo Circle
        self.logo_container = QWidget()
        self.logo_container.setFixedSize(140, 140)
        self.logo_container.setObjectName("logoContainer")
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Outer animated ring
        self.outer_ring = QLabel("◯")
        self.outer_ring.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary']};
                font-size: 80px;
                background: none;
                font-weight: bold;
                text-align: center;
                line-height: 80px;
            }}
        """)
        self.outer_ring.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.outer_ring.setFixedHeight(80)
        logo_layout.addWidget(self.outer_ring)
        
        # Inner icon
        self.inner_icon = QLabel("📋")
        self.inner_icon.setStyleSheet("""
            QLabel {
                font-size: 60px;
                background: none;
                line-height: 60px;
            }
        """)
        self.inner_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inner_icon.setFixedHeight(60)
        logo_layout.addWidget(self.inner_icon)
        
        content_layout.addWidget(self.logo_container, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addSpacing(10)
        
        # Modern title with refined typography
        self.title = QLabel("Sınav Planlama")
        self.title.setStyleSheet(f"""
            QLabel {{
                color: #FFFFFF;
                font-size: 44px;
                font-weight: 700;
                letter-spacing: 1px;
                background: none;
                line-height: 50px;
            }}
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setMinimumHeight(50)
        content_layout.addWidget(self.title)
        
        # Subtitle
        self.subtitle = QLabel("Sistemesi")
        self.subtitle.setStyleSheet(f"""
            QLabel {{
                color: rgba(255, 255, 255, 0.9);
                font-size: 18px;
                font-weight: 300;
                letter-spacing: 1px;
                background: none;
                line-height: 24px;
            }}
        """)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setMinimumHeight(24)
        content_layout.addWidget(self.subtitle)
        
        content_layout.addSpacing(15)
        
        # Modern loading bar with gradient
        self.progress_container = QWidget()
        self.progress_container.setFixedHeight(12)
        self.progress_container.setMinimumWidth(300)
        progress_layout = QHBoxLayout(self.progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(0)
        
        self.progress_bar = QWidget()
        self.progress_bar.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['primary']},
                    stop:0.5 {COLORS['primary_light']},
                    stop:1 {COLORS['secondary']});
                border-radius: 6px;
            }}
        """)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setFixedWidth(0)
        progress_layout.addWidget(self.progress_bar)
        
        # Background track
        progress_track = QWidget()
        progress_track.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 6px;
            }}
        """)
        progress_track.setFixedHeight(12)
        progress_layout.addWidget(progress_track)
        
        content_layout.addWidget(self.progress_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Status text with smooth transitions
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: rgba(255, 255, 255, 0.85);
                font-size: 13px;
                font-weight: 400;
                letter-spacing: 0.5px;
                background: none;
                line-height: 18px;
            }}
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setMinimumHeight(18)
        content_layout.addWidget(self.status_label)
        
        # Animated loading dots
        self.loading_dots = QLabel("●")
        self.loading_dots.setStyleSheet(f"""
            QLabel {{
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
                background: none;
                letter-spacing: 3px;
                line-height: 16px;
            }}
        """)
        self.loading_dots.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_dots.setMinimumHeight(16)
        content_layout.addWidget(self.loading_dots)
        
        # Add content to main layout with proper spacing
        layout.addSpacing(20)
        layout.addWidget(content_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        
        # Setup timers
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(30)
        
        self.dot_timer = QTimer()
        self.dot_timer.timeout.connect(self.update_loading_dots)
        self.dot_timer.start(400)
        
        self.dot_count = 1
    
    def setup_gradient_background(self):
        """Create a modern gradient background"""
        # This will be handled via paintEvent
        pass
    
    def paintEvent(self, event):
        """Paint custom gradient background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create modern gradient (dark to accent)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(20, 33, 61))  # Dark blue
        gradient.setColorAt(0.5, QColor(32, 55, 95))  # Medium blue
        gradient.setColorAt(1, QColor(26, 72, 91))  # Teal-blue
        
        painter.fillRect(self.rect(), gradient)
        
        # Draw subtle accent lines
        painter.setPen(Qt.PenStyle.NoPen)
        
        super().paintEvent(event)
    
    def setup_animations(self):
        """Setup smooth fade-in animation"""
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(800)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Logo rotation animation
        self.rotation_angle = 0
        self.logo_timer = QTimer()
        self.logo_timer.timeout.connect(self.rotate_logo)
        self.logo_timer.start(30)
        
        self.fade_in_animation.start()
    
    def rotate_logo(self):
        """Rotate logo smoothly"""
        self.rotation_angle = (self.rotation_angle + 2) % 360
        # Update logo with rotation effect using transform
    
    def update_loading_dots(self):
        """Animate loading dots"""
        self.dot_count = (self.dot_count % 3) + 1
        self.loading_dots.setText("●" * self.dot_count)
    
    def update_progress(self):
        """Update progress bar and status"""
        self.progress_value += 1
        
        # Calculate progress bar width based on container width
        if self.progress_container.width() > 1:
            container_width = self.progress_container.width()
            new_width = int((self.progress_value / 100) * container_width)
            self.progress_bar.setFixedWidth(max(0, new_width))
        
        # Update status based on progress
        if self.progress_value < 20:
            self.status_label.setText("Loading resources...")
        elif self.progress_value < 40:
            self.status_label.setText("Initializing database...")
        elif self.progress_value < 60:
            self.status_label.setText("Setting up interface...")
        elif self.progress_value < 80:
            self.status_label.setText("Configuring system...")
        elif self.progress_value < 95:
            self.status_label.setText("Final preparations...")
        else:
            self.status_label.setText("Ready to launch...")
        
        if self.progress_value >= 100:
            self.progress_timer.stop()
            self.dot_timer.stop()
            self.logo_timer.stop()
            self.close_splash()
    
    def close_splash(self):
        """Smooth fade-out and close"""
        QTimer.singleShot(300, self.perform_fade_out)
    
    def perform_fade_out(self):
        """Execute fade out animation"""
        fade_out = QPropertyAnimation(self, b"windowOpacity")
        fade_out.setDuration(600)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        fade_out.finished.connect(self.close)
        fade_out.start()
        self._close_animation = fade_out

