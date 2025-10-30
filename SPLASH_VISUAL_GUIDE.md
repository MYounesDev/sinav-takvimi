# Splash Screen Visual Guide

## 📱 Splash Screen Layout

```
╔════════════════════════════════════════════════╗
║                                                ║
║                     📚                         ║
║                                                ║
║        Sınav Planlama Sistemi                 ║
║                                                ║
║        Kocaeli University                      ║
║                                                ║
║    ████████████░░░░░░░░░░░░░░                ║  (Gradient: Green)
║                                                ║
║      🔄 Loading resources                     ║  (Status Message)
║                                                ║
║              ●●●                              ║  (Loading Dots)
║                                                ║
╚════════════════════════════════════════════════╝
```

## 🎬 Animation Sequence

### Stage 1: Fade In (0-600ms)
```
Opacity: 0% ━━━━━━━━━━━━━━━━━━━━━━ 100%
Time:    0ms ━━━━━━━━━━━━━━━━━━ 600ms
Status:  Splash appears with smooth fade
```

### Stage 2: Loading Resources (0-25%)
```
Progress: ████░░░░░░░░░░░░░░░░░
Status:   🔄 Loading resources
Dots:     ●
Time:     0-625ms
```

### Stage 3: Initializing Database (25-50%)
```
Progress: ████████░░░░░░░░░░░░
Status:   🔐 Initializing database
Dots:     ●●●
Time:     625-1250ms
```

### Stage 4: Setting Up Interface (50-75%)
```
Progress: ████████████░░░░░░░░
Status:   🎨 Setting up interface
Dots:     ●●
Time:     1250-1875ms
```

### Stage 5: Final Preparations (75-95%)
```
Progress: ████████████████░░░░
Status:   ✨ Final preparations
Dots:     ●
Time:     1875-2375ms
```

### Stage 6: Ready to Launch (95-100%)
```
Progress: ████████████████████
Status:   🚀 Ready to launch
Dots:     ●●●
Time:     2375-2500ms
```

### Stage 7: Fade Out (2500-2900ms)
```
Opacity: 100% ━━━━━━━━━━━━━━━━━━━ 0%
Time:    2500ms ━━━━━━━━━ 2900ms
Status:  Splash fades out
Action:  Main window appears
```

## 🎨 Color Zones

```
         ┌─────────────────────┐
         │   📚 Icon Zone      │  Size: 120px
         │   (Green #27AE60)   │
         └─────────────────────┘
         ┌─────────────────────┐
         │  Title & Subtitle   │  Colors: Green
         │  Typography Zone    │  Spacing: Optimal
         └─────────────────────┘
         ┌─────────────────────┐
         │ Progress Bar Zone   │  Gradient: Green Spectrum
         │ ████░░░░░░░░       │  Height: 6px (Sleek)
         └─────────────────────┘
         ┌─────────────────────┐
         │ Status & Dots Zone  │  Colors: Primary Green
         │ 🔄 Loading ●●●     │  Dynamic Updates
         └─────────────────────┘
```

## 📊 Loading Progress Timeline

```
0%       25%        50%        75%        95%      100%
│────────│──────────│──────────│──────────│────────│
🔄       🔐        🎨         ✨         🚀       ✓
│←─────────────────────────────────────────────────→|
                    2500ms Total
```

## 🎯 Typography Hierarchy

```
TITLE LEVEL
┌──────────────────────────┐
│ Sınav Planlama Sistemi   │  Font: 36px Bold
│ Letter Spacing: 1px      │  Color: #27AE60
│ Weight: Bold             │
└──────────────────────────┘

SUBTITLE LEVEL
┌──────────────────────────┐
│ Kocaeli University       │  Font: 14px Regular
│ Letter Spacing: 2px      │  Color: #5D6D7B
│ Weight: Normal           │
└──────────────────────────┘

STATUS LEVEL
┌──────────────────────────┐
│ 🔄 Loading resources     │  Font: 13px Medium
│ Letter Spacing: 0.5px    │  Color: #27AE60
│ Weight: 500              │
└──────────────────────────┘
```

## 💫 Animation Easing Curves

### Fade In/Out
```
Start ─╮
       │  Smooth InOutQuad curve
       │  (Accelerates then decelerates)
       └─ End
```

### Progress Fill
```
Start ─────────────────────► End
      Linear progression
      Smooth and steady
```

### Loading Dots
```
●  ──→  ●●  ──→  ●●●  ──→  (repeat)
Time: 500ms intervals
```

## 📐 Dimensions

```
Window Size:        600 x 400 px
Border Radius:      25px (Premium look)
Content Margins:    50px all sides
Icon Size:          120px height
Progress Height:    6px (Sleek)
Spacing Between:    20px (Optimal)
```

## 🎨 Color Palette

### Main Colors
```
Primary Green:       #27AE60  ████
Primary Dark:        #229954  ████
Primary Light:       #52BE80  ████
```

### Supporting Colors
```
Background:          #E8F8F5  ████
Text Dark:           #2C3E50  ████
Text Light:          #5D6D7B  ████
White:               #FFFFFF  ████
```

## ✨ Animation Presets

### Fade In
- **Type**: Opacity Animation
- **Duration**: 600ms
- **Easing**: InOutQuad
- **From**: 0.0 → **To**: 1.0

### Fade Out
- **Type**: Opacity Animation
- **Duration**: 400ms
- **Easing**: InOutQuad
- **From**: 1.0 → **To**: 0.0

### Progress Bar
- **Type**: Linear Fill
- **Duration**: 2500ms
- **Gradient**: Green Spectrum
- **Easing**: Linear

### Loading Dots
- **Type**: Text Update
- **Duration**: 500ms per cycle
- **Pattern**: ● → ●● → ●●●
- **Easing**: Instant

## 🔄 Loading Dot Animation Cycle

```
Stage 1:  ●
          ▼ (500ms)
Stage 2:  ●●
          ▼ (500ms)
Stage 3:  ●●●
          ▼ (500ms)
Stage 1:  ● (repeat)
```

## 🚀 App Launch Sequence

```
1. Database Initialization
   ├─ Load from disk
   ├─ Setup connections
   └─ Prepare tables

2. Splash Screen Appears
   ├─ Fade in (600ms)
   ├─ Show loading animation
   └─ Update status messages

3. Main Window Initialization
   ├─ Create UI components
   ├─ Load views
   └─ Prepare widgets

4. Progress Completion
   ├─ Reach 100%
   ├─ Fade out splash (400ms)
   └─ Show main window

5. User Can Interact
   └─ Application ready
```

## 📱 Responsive Design

The splash screen is centered on screen:
```
┌─────────────────────────────────────┐
│                                     │
│    ┌─────────────────────────┐    │
│    │   Splash Screen         │    │
│    │   600 x 400px          │    │
│    │   Centered              │    │
│    └─────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

---

## 🎬 Complete Animation Sequence

```
TIME    EVENT                           VISUAL
─────────────────────────────────────────────────
0ms     App starts                      (background)
0ms     Splash appears                  Opacity: 0%
50ms    Fade in begins                  Opacity: ↑
600ms   Splash fully visible            Opacity: 100%
        Progress: 0%
        Status: 🔄 Loading resources
        
625ms   Status update                   🔐 Initializing database
1250ms  Progress: 50%                   

1875ms  Status update                   🎨 Setting up interface
        Progress: 75%

2375ms  Status update                   ✨ Final preparations
2500ms  Status update                   🚀 Ready to launch
        Progress: 100%
        Fade out begins                 Opacity: ↓

2900ms  Splash invisible                Opacity: 0%
        Main window appears             Window shows

USER    Application ready
        Can interact with main window
```

---

**Design Status**: ✨ **PREMIUM, MODERN & PROFESSIONAL**

Perfect for a first impression! 🎉
