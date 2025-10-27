"""
UI Styling Utilities
"""

from config import COLORS


class Styles:
    """Centralized styling definitions"""
    
    # Main Window Styles
    MAIN_WINDOW = f"""
        QMainWindow {{
            background-color: {COLORS['light']};
        }}
    """
    
    # Button Styles
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
            background-color: #3A7BC8;
        }}
        QPushButton:pressed {{
            background-color: #2A6BB8;
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
            background-color: #2A6BB8;
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
            background-color: #E63E40;
        }}
        QPushButton:pressed {{
            background-color: #D62E30;
        }}
    """
    
    SUCCESS_BUTTON = f"""
        QPushButton {{
            background-color: {COLORS['success']};
            color: {COLORS['white']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #42A310;
        }}
        QPushButton:pressed {{
            background-color: #329300;
        }}
    """
    
    # Input Styles
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
            border-top: 5px solid {COLORS['text']};
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
    
    # Table Styles
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
            background-color: {COLORS['dark']};
            color: {COLORS['white']};
            padding: 10px;
            border: none;
            font-weight: bold;
        }}
    """
    
    # Label Styles
    TITLE_LABEL = f"""
        QLabel {{
            color: {COLORS['dark']};
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
    
    # Card/Panel Styles
    CARD = f"""
        QFrame {{
            background-color: {COLORS['white']};
            border-radius: 12px;
            border: 1px solid {COLORS['border']};
        }}
    """
    
    # Sidebar Styles
    SIDEBAR = f"""
        QFrame {{
            background-color: {COLORS['dark']};
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
            background-color: rgba(255, 255, 255, 0.1);
        }}
        QPushButton:checked {{
            background-color: {COLORS['primary']};
        }}
    """
    
    # Scroll Area
    SCROLL_AREA = f"""
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
    """
    
    # Message Box
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
            background-color: #3A7BC8;
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


