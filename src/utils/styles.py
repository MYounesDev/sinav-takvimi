"""
UI Styling Utilities - Modern Professional Design System
"""

from config import COLORS
from PyQt6.QtWidgets import QHeaderView, QTableWidget
from PyQt6.QtCore import Qt

class Styles:
    """Centralized styling definitions with modern design"""
    
    # ==================== MAIN WINDOW ====================
    MAIN_WINDOW = f"""
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #F8FAFB,
                stop:1 #F0F4F8);
        }}
    """
    
    # ==================== BUTTONS ====================
    PRIMARY_BUTTON = f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['primary']},
                stop:1 {COLORS['primary_light']});
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['primary_light']},
                stop:1 {COLORS['primary']});
        }}
        QPushButton:pressed {{
            background: {COLORS['primary_dark']};
        }}
        QPushButton:disabled {{
            background-color: #CCCCCC;
            color: #999999;
        }}
    """
    
    SECONDARY_BUTTON = f"""
        QPushButton {{
            background-color: #FFFFFF;
            color: {COLORS['primary']};
            border: 2px solid {COLORS['primary']};
            border-radius: 10px;
            padding: 10px 26px;
            font-size: 13px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']}10;
            border-color: {COLORS['primary_light']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary']};
            color: #FFFFFF;
        }}
    """
    
    DANGER_BUTTON = f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['danger']},
                stop:1 #E74C3C);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #E74C3C,
                stop:1 {COLORS['danger']});
        }}
        QPushButton:pressed {{
            background-color: #C0392B;
        }}
    """
    
    SUCCESS_BUTTON = f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['success']},
                stop:1 {COLORS['primary_light']});
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['primary_light']},
                stop:1 {COLORS['success']});
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
        }}
    """
    
    # ==================== TEXT INPUTS ====================
    LINE_EDIT = f"""
        QLineEdit {{
            background-color: #FFFFFF;
            border: 2px solid #E0E6EB;
            border-radius: 10px;
            padding: 12px 16px;
            font-size: 13px;
            color: {COLORS['text']};
            selection-background-color: {COLORS['primary']};
        }}
        QLineEdit:focus {{
            border-color: {COLORS['primary']};
            background-color: #FFFFFF;
        }}
        QLineEdit:disabled {{
            background-color: #F5F7FA;
            color: {COLORS['text_light']};
            border-color: #E0E6EB;
        }}
    """
    
    COMBO_BOX = f"""
        QComboBox {{
            background-color: #FFFFFF;
            border: 2px solid #E0E6EB;
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 13px;
            color: {COLORS['text']};
        }}
        QComboBox:focus {{
            border-color: {COLORS['primary']};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 28px;
        }}
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {COLORS['primary']};
            margin-right: 8px;
        }}
        QComboBox QAbstractItemView {{
            background-color: #FFFFFF;
            border: 1px solid #E0E6EB;
            selection-background-color: {COLORS['primary']}20;
        }}
    """
    
    SPIN_BOX = f"""
        QSpinBox {{
            background-color: #FFFFFF;
            border: 2px solid #E0E6EB;
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 13px;
            color: {COLORS['text']};
        }}
        QSpinBox:focus {{
            border-color: {COLORS['primary']};
        }}
        QSpinBox::up-button, QSpinBox::down-button {{
            width: 24px;
            background-color: transparent;
        }}
    """
    
    # ==================== TABLE ====================
    TABLE_WIDGET = f"""
        QTableWidget {{
            background-color: #FFFFFF;
            border: 1px solid #E0E6EB;
            border-radius: 12px;
            gridline-color: #E0E6EB;
            font-size: 13px;
        }}
        QTableWidget::item {{
            padding: 10px 8px;
            color: {COLORS['text']};
            border-right: 1px solid #E0E6EB;
        }}
        QTableWidget::item:selected {{
            background-color: {COLORS['primary']}20;
            color: {COLORS['text']};
        }}
        QTableWidget::item:alternate {{
            background-color: #F8FAFB;
        }}
        QHeaderView::section {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #F0F4F8,
                stop:1 #E8EEF5);
            color: {COLORS['text']};
            padding: 12px 8px;
            border-right: 1px solid #E0E6EB;
            border-bottom: 2px solid #E0E6EB;
            font-weight: 600;
            font-size: 12px;
        }}
    """
    
    # ==================== LABELS ====================
    TITLE_LABEL = f"""
        QLabel {{
            color: {COLORS['text']};
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }}
    """
    
    SUBTITLE_LABEL = f"""
        QLabel {{
            color: {COLORS['text']};
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.2px;
        }}
    """
    
    NORMAL_LABEL = f"""
        QLabel {{
            color: {COLORS['text']};
            font-size: 13px;
            font-weight: 500;
        }}
    """
    
    INFO_LABEL = f"""
        QLabel {{
            color: {COLORS['text_light']};
            font-size: 12px;
            font-weight: 400;
        }}
    """
    
    # ==================== CARDS & FRAMES ====================
    CARD = f"""
        QFrame {{
            background-color: #FFFFFF;
            border-radius: 12px;
            border: 1px solid #E0E6EB;
        }}
    """
    
    CARD_ELEVATED = f"""
        QFrame {{
            background-color: #FFFFFF;
            border-radius: 12px;
            border: none;
            background-color: white;
        }}
    """
    
    # ==================== SIDEBAR ====================
    SIDEBAR = f"""
        QFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {COLORS['primary']},
                stop:1 {COLORS['primary_dark']});
            border: none;
        }}
    """
    
    SIDEBAR_BUTTON = f"""
        QPushButton {{
            background-color: transparent;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 14px 18px;
            text-align: left;
            font-size: 13px;
            font-weight: 500;
            letter-spacing: 0.3px;
        }}
        QPushButton:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-left: 4px solid #FFFFFF;
            padding-left: 14px;
        }}
        QPushButton:checked {{
            background-color: rgba(255, 255, 255, 0.25);
            border-left: 4px solid #FFFFFF;
            padding-left: 14px;
        }}
    """
    
    # ==================== SCROLLBARS ====================
    SCROLL_AREA = f"""
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        QScrollBar:vertical {{
            background-color: #F0F4F8;
            width: 10px;
            border: none;
        }}
        QScrollBar::handle:vertical {{
            background-color: #C0C7D0;
            border-radius: 5px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: #B0B7C0;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
    """
    
    # ==================== DIALOGS & MESSAGE BOXES ====================
    MESSAGE_BOX = f"""
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
            border-radius: 8px;
            padding: 8px 18px;
            min-width: 70px;
            font-weight: 600;
        }}
        QMessageBox QPushButton:hover {{
            background-color: {COLORS['primary_light']};
        }}
        QMessageBox QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
        }}
    """
    
    # ==================== DIALOGS ====================
    DIALOG = f"""
        QDialog {{
            background-color: #FFFFFF;
            border: none;
        }}
    """
    
    # ==================== INPUT DIALOG ====================
    INPUT_DIALOG = f"""
        QInputDialog {{
            background-color: #FFFFFF;
        }}
        QInputDialog QLineEdit {{
            background-color: #FFFFFF;
            border: 2px solid #E0E6EB;
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 13px;
        }}
        QInputDialog QPushButton {{
            background-color: {COLORS['primary']};
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: 600;
        }}
    """

def apply_shadow(widget, blur_radius=16, offset_y=6, opacity=25):
    """
    Apply modern drop shadow effect to a widget
    
    Args:
        widget: QWidget to apply shadow to
        blur_radius: Blur radius of the shadow
        offset_y: Vertical offset of the shadow
        opacity: Opacity of the shadow (0-255)
    """
    from PyQt6.QtWidgets import QGraphicsDropShadowEffect
    from PyQt6.QtGui import QColor
    
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setXOffset(0)
    shadow.setYOffset(offset_y)
    shadow.setColor(QColor(0, 0, 0, opacity))
    widget.setGraphicsEffect(shadow)

def apply_light_shadow(widget):
    """Apply subtle light shadow"""
    apply_shadow(widget, blur_radius=8, offset_y=2, opacity=15)

def apply_medium_shadow(widget):
    """Apply medium shadow"""
    apply_shadow(widget, blur_radius=12, offset_y=4, opacity=20)

def apply_strong_shadow(widget):
    """Apply strong shadow"""
    apply_shadow(widget, blur_radius=20, offset_y=8, opacity=30)

def configure_table_widget(table_widget, min_row_height=35, min_total_height=400):
    """
    Configure a table widget with proper settings for visibility and scrolling
    
    Args:
        table_widget: QTableWidget to configure
        min_row_height: Minimum height for each row (default 35px)
        min_total_height: Minimum total table height (default 400px)
    """
    
    # Set row height
    table_widget.verticalHeader().setDefaultSectionSize(min_row_height)
    table_widget.verticalHeader().setStretchLastSection(False)
    
    # Set minimum heights
    table_widget.setMinimumHeight(min_total_height)
    
    # Enable scrolling
    table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    
    # Set column resize mode
    for i in range(table_widget.columnCount()):
        table_widget.horizontalHeader().setSectionResizeMode(
            i, QHeaderView.ResizeMode.Stretch
        )
    
    # Set selection and alternating row colors
    table_widget.setAlternatingRowColors(True)
    table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

