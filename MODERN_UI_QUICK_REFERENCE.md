# Modern UI Quick Reference Guide

## 🚀 Quick Start

### Using Modern UI Components

#### 1. Using ModernLineEdit (Login Page)
```python
from src.ui.login_view import ModernLineEdit

# Create input field
email_input = ModernLineEdit("placeholder text")
email_input.returnPressed.connect(on_submit)

# The component automatically handles:
# - Focus/unfocus styling
# - Smooth border transitions
# - Professional appearance
```

#### 2. Using ModernButton (Login Page)
```python
from src.ui.login_view import ModernButton

# Create button
login_btn = ModernButton("Sign In", is_primary=True)
login_btn.clicked.connect(on_click)

# Automatically has:
# - Gradient background
# - Hover effects with shadow
# - Smooth transitions
```

#### 3. Using ModernStatCard (Dashboard)
```python
from src.ui.dashboard_view import ModernStatCard

# Create stat card
card = ModernStatCard(
    title="Courses",
    value="24",
    icon="📚",
    color="#27AE60"
)

# Automatically has:
# - Hover effects
# - Color-coded design
# - Drop shadow
# - Interactive feedback
```

---

## 🎨 Styling Quick Reference

### Applying Styles
```python
from src.utils.styles import Styles, apply_shadow, apply_medium_shadow

# Apply predefined styles
button.setStyleSheet(Styles.PRIMARY_BUTTON)
input_field.setStyleSheet(Styles.LINE_EDIT)
card.setStyleSheet(Styles.CARD)

# Apply shadow effects
apply_shadow(widget)                    # Default: blur 16, offset 6
apply_light_shadow(widget)              # Subtle: blur 8, offset 2
apply_medium_shadow(widget)             # Standard: blur 12, offset 4
apply_strong_shadow(widget)             # Strong: blur 20, offset 8
```

### Available Styles
```python
# Buttons
Styles.PRIMARY_BUTTON
Styles.SECONDARY_BUTTON
Styles.DANGER_BUTTON
Styles.SUCCESS_BUTTON

# Inputs
Styles.LINE_EDIT
Styles.COMBO_BOX
Styles.SPIN_BOX

# Tables & Containers
Styles.TABLE_WIDGET
Styles.CARD
Styles.CARD_ELEVATED
Styles.SIDEBAR

# Text
Styles.TITLE_LABEL
Styles.SUBTITLE_LABEL
Styles.NORMAL_LABEL
Styles.INFO_LABEL

# Dialogs
Styles.MESSAGE_BOX
Styles.DIALOG
Styles.INPUT_DIALOG
```

---

## 🎬 Animation Quick Reference

### Using Animations
```python
from src.utils.animations import AnimationHelper
from config import ANIMATION_DURATION

# Fade animations
AnimationHelper.fade_in(widget, duration=300)
AnimationHelper.fade_out(widget, duration=300, callback=on_complete)

# Slide animations
AnimationHelper.slide_in_from_left(widget)
AnimationHelper.slide_in_from_right(widget)
AnimationHelper.slide_in_from_top(widget)
AnimationHelper.slide_in_from_bottom(widget)

# Scale animations
AnimationHelper.scale_in(widget)
AnimationHelper.scale_out(widget, callback=cleanup)
AnimationHelper.pulse_scale(widget)

# Effect animations
AnimationHelper.bounce(widget)
AnimationHelper.spring(widget)
AnimationHelper.shimmer_effect(widget)

# Composite animations
AnimationHelper.fade_and_slide_in_left(widget)
AnimationHelper.fade_and_scale_in(widget)

# Multiple widgets
widgets = [card1, card2, card3]
AnimationHelper.staggered_fade_in(widgets, delay=100)
AnimationHelper.sequential_animations(widgets, animation_type="fade_in")
```

### Animation Parameters
```python
# Duration (milliseconds)
ANIMATION_DURATION = 300  # From config.py
# Can override: AnimationHelper.fade_in(widget, duration=500)

# Easing Curves Used
QEasingCurve.Type.InOutQuad         # Smooth, natural
QEasingCurve.Type.OutCubic          # Professional, snappy
QEasingCurve.Type.OutBack           # Elastic, bouncy
QEasingCurve.Type.OutBounce         # Playful, energetic
QEasingCurve.Type.OutElastic        # Spring-like motion
```

---

## 🎨 Color System Quick Reference

### Using Colors
```python
from config import COLORS

# Primary colors
COLORS['primary']           # #27AE60 (Green)
COLORS['primary_light']     # #52BE80
COLORS['primary_dark']      # #229954

# Secondary colors
COLORS['secondary']         # #16A085 (Teal)
COLORS['success']           # #27AE60 (Green)
COLORS['warning']           # #F39C12 (Orange)
COLORS['danger']            # #E74C3C (Red)

# Neutral colors
COLORS['text']              # #2C3E50 (Dark text)
COLORS['text_light']        # #5D6D7B (Gray text)
COLORS['white']             # #FFFFFF
```

### In Stylesheets
```python
# Direct color usage
f"""
QLabel {{
    color: {COLORS['primary']};
    background-color: {COLORS['white']};
}}
"""

# Gradient usage
f"""
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['primary']},
        stop:1 {COLORS['primary_light']});
}}
"""
```

---

## 📐 Spacing & Layout Conventions

### Standard Spacing
```python
# Containers
layout.setContentsMargins(40, 40, 40, 40)  # Page margins
layout.setSpacing(30)                      # Between major sections

# Cards
layout.setContentsMargins(24, 24, 24, 24)  # Inside cards
layout.setSpacing(12)                      # Between card elements

# Buttons/Inputs
setMinimumHeight(48)                       # Input fields
setMinimumHeight(50)                       # Buttons
```

### Border Radius
```python
# Buttons: 10px
border-radius: 10px;

# Cards: 16px
border-radius: 16px;

# Inputs: 10-12px
border-radius: 10px;
```

### Font Sizes
```python
# Titles: 28-48px, bold
font-size: 32px;
font-weight: 700;

# Subtitles: 14-20px, light
font-size: 14px;
font-weight: 300;

# Body: 13px
font-size: 13px;
font-weight: 400;

# Labels: 12-13px
font-size: 12px;
font-weight: 600;
```

---

## 🔧 Common Implementation Patterns

### Pattern 1: Modern Card with Hover
```python
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from src.utils.styles import Styles, apply_shadow

card = QFrame()
card.setStyleSheet(Styles.CARD)
apply_medium_shadow(card)

layout = QVBoxLayout(card)
layout.setContentsMargins(24, 24, 24, 24)
layout.setSpacing(12)

# Add content
title = QLabel("Title")
title.setStyleSheet(Styles.TITLE_LABEL)
layout.addWidget(title)
```

### Pattern 2: Modern Button with Gradient
```python
from PyQt6.QtWidgets import QPushButton
from src.utils.styles import Styles
from config import COLORS

button = QPushButton("Click Me")
button.setStyleSheet(Styles.PRIMARY_BUTTON)
button.setCursor(Qt.CursorShape.PointingHandCursor)
button.setMinimumHeight(50)
button.clicked.connect(on_click)
```

### Pattern 3: Animated Widget Entrance
```python
from src.utils.animations import AnimationHelper

# Single widget
AnimationHelper.fade_in(widget, duration=600)

# Multiple widgets with stagger
cards = [card1, card2, card3, card4]
AnimationHelper.staggered_fade_in(cards, delay=100)
```

### Pattern 4: Input with Focus Styling
```python
from src.ui.login_view import ModernLineEdit

input_field = ModernLineEdit("Enter value...")
# Automatically handles:
# - Focus state: Green border
# - Unfocus state: Gray border
# - Disabled state: Light gray
# - Hover: Smooth transitions
```

---

## 📋 Component Checklist

### Splash Screen Features
- ✓ Modern gradient background
- ✓ Animated progress bar
- ✓ Loading status messages
- ✓ Smooth fade transitions
- ✓ Auto-close on completion

### Login Page Features
- ✓ Split-screen design
- ✓ Modern input components
- ✓ Gradient buttons
- ✓ Smooth animations
- ✓ Professional info section

### Dashboard Features
- ✓ Modern stat cards
- ✓ Interactive hover effects
- ✓ Staggered animations
- ✓ Color-coded categories
- ✓ Quick tips section

### General Styling
- ✓ Gradient backgrounds
- ✓ Smooth shadows
- ✓ Modern typography
- ✓ Professional spacing
- ✓ Consistent colors

---

## 🐛 Troubleshooting

### Animation Not Playing
```python
# Store animation reference to prevent garbage collection
self._animation = AnimationHelper.fade_in(widget)
```

### Styles Not Applied
```python
# Ensure stylesheet is set after creating widget
widget.setStyleSheet(Styles.CARD)

# For custom colors, use f-strings
widget.setStyleSheet(f"""
    QWidget {{
        color: {COLORS['primary']};
    }}
""")
```

### Shadow Not Visible
```python
from src.utils.styles import apply_medium_shadow

# Apply shadow after stylesheet is set
apply_medium_shadow(card)

# Ensure parent widget doesn't have conflicting effects
```

### Input Focus Not Showing
```python
# ModernLineEdit handles this automatically
# If using standard QLineEdit, apply stylesheet:
input_field.setStyleSheet(Styles.LINE_EDIT)
```

---

## 📚 File Reference

### UI Files
```
src/ui/splash_screen.py       # Splash screen with modern design
src/ui/login_view.py          # Login with ModernLineEdit & ModernButton
src/ui/dashboard_view.py      # Dashboard with ModernStatCard
src/ui/main_window.py         # Main application window
```

### Utility Files
```
src/utils/styles.py           # Styles class with predefined CSS
src/utils/animations.py       # AnimationHelper with animation methods
src/utils/auth.py             # Authentication utilities
config.py                     # Configuration and color definitions
```

---

## 🎯 Development Tips

1. **Always store animation references** to prevent garbage collection
2. **Use predefined styles** from Styles class for consistency
3. **Apply shadows after stylesheets** for best visual effect
4. **Use staggered animations** for multiple elements
5. **Test animations on target hardware** for smooth performance
6. **Use f-strings** for dynamic color values in stylesheets
7. **Set proper margins** for clean, professional layout
8. **Use rounded corners** for modern appearance

---

## 📞 Quick Command Reference

```python
# Import everything you need
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor
from src.ui.login_view import ModernLineEdit, ModernButton
from src.ui.dashboard_view import ModernStatCard
from src.utils.styles import Styles, apply_shadow, apply_medium_shadow
from src.utils.animations import AnimationHelper
from config import COLORS, ANIMATION_DURATION

# Create modern component
card = ModernStatCard("Courses", "24", "📚", COLORS['primary'])

# Apply styling
card.setStyleSheet(Styles.CARD)

# Apply shadow
apply_medium_shadow(card)

# Add animation
AnimationHelper.fade_in(card, duration=600)
```

---

## ✨ Best Practices

✅ **DO:**
- Use ModernLineEdit and ModernButton in login/forms
- Apply shadows with apply_*_shadow() functions
- Use staggered animations for multiple elements
- Set minimum heights for buttons (50px) and inputs (48px)
- Use f-strings for dynamic color values

❌ **DON'T:**
- Manually set complex stylesheets (use Styles class)
- Create animations without storing references
- Mix old and new UI components
- Use hardcoded colors (use COLORS dict)
- Apply shadows multiple times to same widget

---

**This guide covers 90% of common modern UI implementation tasks!** 🎉
