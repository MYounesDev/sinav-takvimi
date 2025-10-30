"""
Animation Utilities - Modern, smooth animation effects
"""

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QSize, QSequentialAnimationGroup, QParallelAnimationGroup
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from config import ANIMATION_DURATION


class AnimationHelper:
    """Helper class for creating smooth, modern animations"""
    
    # ==================== FADE ANIMATIONS ====================
    @staticmethod
    def fade_in(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Smooth fade in animation
        
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
        
        widget._fade_animation = animation
        return animation
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = ANIMATION_DURATION, callback=None):
        """
        Smooth fade out animation
        
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
        
        widget._fade_animation = animation
        return animation
    
    # ==================== SLIDE ANIMATIONS ====================
    @staticmethod
    def slide_in_from_left(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Slide in from left animation with smooth easing
        
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
        return animation
    
    @staticmethod
    def slide_in_from_right(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Slide in from right animation with smooth easing
        
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
        return animation
    
    @staticmethod
    def slide_in_from_top(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Slide in from top animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        start_pos = widget.pos()
        start_pos.setY(-widget.height())
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(QPoint(start_pos.x(), 0))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        
        widget._slide_animation = animation
        return animation
    
    @staticmethod
    def slide_in_from_bottom(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Slide in from bottom animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        parent_height = widget.parent().height() if widget.parent() else 0
        start_pos = widget.pos()
        start_pos.setY(parent_height)
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(QPoint(start_pos.x(), 0))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        
        widget._slide_animation = animation
        return animation
    
    # ==================== SCALE ANIMATIONS ====================
    @staticmethod
    def scale_in(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Scale in animation from 0 to full size
        
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
        return animation
    
    @staticmethod
    def scale_out(widget: QWidget, duration: int = ANIMATION_DURATION, callback=None):
        """
        Scale out animation from full size to 0
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
            callback: Function to call when animation finishes
        """
        start_size = widget.size()
        
        animation = QPropertyAnimation(widget, b"size")
        animation.setDuration(duration)
        animation.setStartValue(start_size)
        animation.setEndValue(QSize(0, 0))
        animation.setEasingCurve(QEasingCurve.Type.InBack)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.start()
        
        widget._scale_animation = animation
        return animation
    
    @staticmethod
    def pulse_scale(widget: QWidget, duration: int = 500):
        """
        Pulse scale animation (grow and shrink)
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        original_size = widget.size()
        
        animation = QPropertyAnimation(widget, b"size")
        animation.setDuration(duration)
        animation.setStartValue(original_size)
        animation.setKeyValueAt(0.5, QSize(
            int(original_size.width() * 1.05),
            int(original_size.height() * 1.05)
        ))
        animation.setEndValue(original_size)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        
        widget._pulse_animation = animation
        return animation
    
    # ==================== BOUNCE & SPRING ANIMATIONS ====================
    @staticmethod
    def bounce(widget: QWidget, duration: int = 500):
        """
        Bounce animation with elastic effect
        
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
        return animation
    
    @staticmethod
    def spring(widget: QWidget, duration: int = 600):
        """
        Spring animation with elastic overshoot
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        original_pos = widget.pos()
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(original_pos)
        animation.setKeyValueAt(0.3, QPoint(original_pos.x(), original_pos.y() - 30))
        animation.setKeyValueAt(0.6, QPoint(original_pos.x(), original_pos.y() + 10))
        animation.setEndValue(original_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutElastic)
        animation.start()
        
        widget._spring_animation = animation
        return animation
    
    # ==================== COMPOSITE ANIMATIONS ====================
    @staticmethod
    def fade_and_slide_in_left(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Combined fade and slide animation from left
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        # Parallel animation group
        parallel_group = QParallelAnimationGroup()
        
        # Fade animation
        fade_anim = QPropertyAnimation(effect, b"opacity")
        fade_anim.setDuration(duration)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Slide animation
        start_pos = widget.pos()
        start_pos.setX(-widget.width())
        slide_anim = QPropertyAnimation(widget, b"pos")
        slide_anim.setDuration(duration)
        slide_anim.setStartValue(start_pos)
        slide_anim.setEndValue(QPoint(0, start_pos.y()))
        slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        parallel_group.addAnimation(fade_anim)
        parallel_group.addAnimation(slide_anim)
        parallel_group.start()
        
        widget._composite_animation = parallel_group
        return parallel_group
    
    @staticmethod
    def fade_and_scale_in(widget: QWidget, duration: int = ANIMATION_DURATION):
        """
        Combined fade and scale animation
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        final_size = widget.size()
        
        # Parallel animation group
        parallel_group = QParallelAnimationGroup()
        
        # Fade animation
        fade_anim = QPropertyAnimation(effect, b"opacity")
        fade_anim.setDuration(duration)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Scale animation
        scale_anim = QPropertyAnimation(widget, b"size")
        scale_anim.setDuration(duration)
        scale_anim.setStartValue(QSize(0, 0))
        scale_anim.setEndValue(final_size)
        scale_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        
        parallel_group.addAnimation(fade_anim)
        parallel_group.addAnimation(scale_anim)
        parallel_group.start()
        
        widget._composite_animation = parallel_group
        return parallel_group
    
    @staticmethod
    def staggered_fade_in(widgets: list, duration: int = ANIMATION_DURATION, delay: int = 100):
        """
        Staggered fade in for multiple widgets
        
        Args:
            widgets: List of widgets to animate
            duration: Animation duration in milliseconds
            delay: Delay between each animation in milliseconds
        """
        animations = []
        for i, widget in enumerate(widgets):
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
            
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            # Delay each animation
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(i * delay, animation.start)
            
            animations.append(animation)
            widget._fade_animation = animation
        
        return animations
    
    @staticmethod
    def sequential_animations(widgets: list, animation_type: str = "fade_in", duration: int = ANIMATION_DURATION):
        """
        Sequential animations on multiple widgets
        
        Args:
            widgets: List of widgets to animate
            animation_type: Type of animation ('fade_in', 'scale_in', 'slide_left')
            duration: Animation duration in milliseconds
        """
        seq_group = QSequentialAnimationGroup()
        
        for widget in widgets:
            if animation_type == "fade_in":
                anim = AnimationHelper.fade_in(widget, duration)
            elif animation_type == "scale_in":
                anim = AnimationHelper.scale_in(widget, duration)
            elif animation_type == "slide_left":
                anim = AnimationHelper.slide_in_from_left(widget, duration)
            else:
                continue
            
            seq_group.addAnimation(anim)
        
        seq_group.start()
        return seq_group
    
    # ==================== UTILITY ANIMATIONS ====================
    @staticmethod
    def rotate_smooth(widget: QWidget, duration: int = 1000, start_angle: float = 0, end_angle: float = 360):
        """
        Smooth rotation animation using property animation
        Note: Requires custom implementation with QTransform
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
            start_angle: Starting angle in degrees
            end_angle: Ending angle in degrees
        """
        # This would require custom implementation with QTransform
        # For now, this is a placeholder
        pass
    
    @staticmethod
    def color_transition(widget: QWidget, start_color: str, end_color: str, duration: int = ANIMATION_DURATION):
        """
        Smooth color transition animation
        
        Args:
            widget: Widget to animate
            start_color: Starting color as hex string
            end_color: Ending color as hex string
            duration: Animation duration in milliseconds
        """
        # This would require custom property animation for colors
        pass
    
    @staticmethod
    def shimmer_effect(widget: QWidget, duration: int = 2000):
        """
        Shimmer/pulse effect for loading states
        
        Args:
            widget: Widget to animate
            duration: Animation duration in milliseconds
        """
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.6)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.setLoopCount(-1)  # Infinite loop
        animation.start()
        
        widget._shimmer_animation = animation
        return animation

