"""
Application Configuration
"""

import os

# Database Configuration
DATABASE_DIR = "database"
DATABASE_PATH = os.path.join(DATABASE_DIR, "exam_scheduler.db")

# Ensure database directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

# Default Admin Credentials
DEFAULT_ADMIN = {
    "name": "Admin",
    "email": "admin@gmail.com",
    "password": "admin123",  # Will be hashed
    "role": "admin"
}

# UI Configuration
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
ANIMATION_DURATION = 300  # milliseconds

# Exam Scheduling Defaults
DEFAULT_EXAM_DURATION = 75  # minutes
DEFAULT_BREAK_TIME = 15  # minutes

# Colors (Modern Design)
COLORS = {
    "primary": "#4A90E2",
    "secondary": "#7B68EE",
    "success": "#52C41A",
    "danger": "#FF4D4F",
    "warning": "#FAAD14",
    "dark": "#2C3E50",
    "light": "#F5F7FA",
    "border": "#E8ECF0",
    "text": "#333333",
    "text_light": "#666666",
    "white": "#FFFFFF"
}

# File Upload Limits
MAX_FILE_SIZE_MB = 10
ALLOWED_EXCEL_EXTENSIONS = ['.xlsx', '.xls']


