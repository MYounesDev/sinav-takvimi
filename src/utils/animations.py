"""
Animation Utilities
"""

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from config import ANIMATION_DURATION


class AnimationHelper:
    """Helper class for creating smooth animations"""
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Fade in animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        
        # Store animation reference to prevent garbage collection
        widget._fade_animation = animation
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = ANIMATION_DURATION, callback=None):
        """
        Fade out animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
            callback: Function to call when animation finishes
        """
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.start()
        
        # Store animation reference
        widget._fade_animation = animation
    
    @staticmethod
    def slide_in_from_left(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Slide in from left animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        start_pos = widget.pos()
        start_pos.setX(-widget.width())
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(QPoint(0, start_pos.y()))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        
        widget._slide_animation = animation
    
    @staticmethod
    def slide_in_from_right(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Slide in from right animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        parent_width = widget.parent().width() if widget.parent() else 0
        start_pos = widget.pos()
        start_pos.setX(parent_width)
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(QPoint(0, start_pos.y()))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        
        widget._slide_animation = animation
    
    @staticmethod
    def scale_in(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Scale in animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        final_size = widget.size()
        
        animation = QPropertyAnimation(widget, b"size")
        animation.setDuration(duration)
        animation.setStartValue(QSize(0, 0))
        animation.setEndValue(final_size)
        animation.setEasingCurve(QEasingCurve.Type.OutBack)
        animation.start()
        
        widget._scale_animation = animation
    
    @staticmethod
    def bounce(widget: QWidget, duration: int = 500):
        """
        Bounce animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        original_pos = widget.pos()
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(original_pos)
        animation.setKeyValueAt(0.5, QPoint(original_pos.x(), original_pos.y() - 20))
        animation.setEndValue(original_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        animation.start()
        
        widget._bounce_animation = animation


