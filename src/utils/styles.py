"""
UI Styling Utilities
"""

from config import COLORS

class Styles:
    """Centralized styling definitions"""
    
    MAIN_WINDOW = f"""
        QMainWindow {{
            background-color: {COLORS['light']};
        }}
    """
    
    PRIMARY_BUTTON = f"""
        QPushButton {{
            background-color: {COLORS['primary']};
            color: {COLORS['white']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary_light']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
        }}
        QPushButton:disabled {{
            background-color: #CCCCCC;
            color: #666666;
        }}
    """
    
    SECONDARY_BUTTON = f"""
        QPushButton {{
            background-color: {COLORS['white']};
            color: {COLORS['primary']};
            border: 2px solid {COLORS['primary']};
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']};
            color: {COLORS['white']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
            color: {COLORS['white']};
        }}
    """
    
    DANGER_BUTTON = f"""
        QPushButton {{
            background-color: {COLORS['danger']};
            color: {COLORS['white']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #C0392B;
        }}
        QPushButton:pressed {{
            background-color: #A93226;
        }}
    """
    
    SUCCESS_BUTTON = f"""
        QPushButton {{
            background-color: {COLORS['primary']};
            color: {COLORS['white']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary_light']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
        }}
    """
    
    LINE_EDIT = f"""
        QLineEdit {{
            background-color: {COLORS['white']};
            border: 2px solid {COLORS['border']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {COLORS['text']};
        }}
        QLineEdit:focus {{
            border-color: {COLORS['primary']};
            background-color: {COLORS['white']};
        }}
        QLineEdit:disabled {{
            background-color: {COLORS['light']};
            color: {COLORS['text_light']};
        }}
    """
    
    COMBO_BOX = f"""
        QComboBox {{
            background-color: {COLORS['white']};
            border: 2px solid {COLORS['border']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {COLORS['text']};
        }}
        QComboBox:focus {{
            border-color: {COLORS['primary']};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {COLORS['primary']};
            margin-right: 10px;
        }}
    """
    
    SPIN_BOX = f"""
        QSpinBox {{
            background-color: {COLORS['white']};
            border: 2px solid {COLORS['border']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {COLORS['text']};
        }}
        QSpinBox:focus {{
            border-color: {COLORS['primary']};
        }}
    """
    
    TABLE_WIDGET = f"""
        QTableWidget {{
            background-color: {COLORS['white']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            gridline-color: {COLORS['border']};
            font-size: 13px;
        }}
        QTableWidget::item {{
            padding: 8px;
            color: {COLORS['text']};
        }}
        QTableWidget::item:selected {{
            background-color: {COLORS['primary']};
            color: {COLORS['white']};
        }}
        QHeaderView::section {{
            background-color: {COLORS['primary']};
            color: {COLORS['white']};
            padding: 10px;
            border: none;
            font-weight: bold;
        }}
    """
    
    TITLE_LABEL = f"""
        QLabel {{
            color: {COLORS['primary']};
            font-size: 24px;
            font-weight: bold;
        }}
    """
    
    SUBTITLE_LABEL = f"""
        QLabel {{
            color: {COLORS['text']};
            font-size: 16px;
            font-weight: 600;
        }}
    """
    
    NORMAL_LABEL = f"""
        QLabel {{
            color: {COLORS['text']};
            font-size: 14px;
        }}
    """
    
    CARD = f"""
        QFrame {{
            background-color: {COLORS['white']};
            border-radius: 12px;
            border: 1px solid {COLORS['border']};
        }}
    """
    
    SIDEBAR = f"""
        QFrame {{
            background-color: {COLORS['primary']};
            border: none;
        }}
    """
    
    SIDEBAR_BUTTON = f"""
        QPushButton {{
            background-color: transparent;
            color: {COLORS['white']};
            border: none;
            border-radius: 8px;
            padding: 15px 20px;
            text-align: left;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-left: 4px solid {COLORS['white']};
        }}
        QPushButton:checked {{
            background-color: {COLORS['primary_light']};
            border-left: 4px solid {COLORS['white']};
        }}
    """
    
    SCROLL_AREA = f"""
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
    """
    
    MESSAGE_BOX = f"""
        QMessageBox {{
            background-color: {COLORS['white']};
        }}
        QMessageBox QLabel {{
            color: {COLORS['text']};
            font-size: 14px;
        }}
        QMessageBox QPushButton {{
            background-color: {COLORS['primary']};
            color: {COLORS['white']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 80px;
        }}
        QMessageBox QPushButton:hover {{
            background-color: {COLORS['primary_light']};
        }}
    """

def apply_shadow(widget):
    """
    Apply drop shadow effect to a widget
    
    Args:
        widget: QWidget to apply shadow to
    """
    from PyQt6.QtWidgets import QGraphicsDropShadowEffect
    from PyQt6.QtGui import QColor
    
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(0, 0, 0, 30))
    widget.setGraphicsEffect(shadow)

