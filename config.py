"""
Application Configuration
"""

import os

DATABASE_DIR = "database"
DATABASE_PATH = os.path.join(DATABASE_DIR, "exam_scheduler.db")

os.makedirs(DATABASE_DIR, exist_ok=True)

DEFAULT_ADMIN = {
    "name": "Admin",
    "email": "admin@gmail.com",
    "password": "admin123",  
    "role": "admin"
}

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
ANIMATION_DURATION = 300  

DEFAULT_EXAM_DURATION = 75  
DEFAULT_BREAK_TIME = 15  

COLORS = {
    "primary": "#27AE60",
    "primary_dark": "#229954",
    "primary_light": "#52BE80",
    "secondary": "#16A085",
    "success": "#27AE60",
    "danger": "#E74C3C",
    "warning": "#F39C12",
    "dark": "#1C2833",
    "light": "#EBF5FB",
    "border": "#D5DBDB",
    "text": "#2C3E50",
    "text_light": "#5D6D7B",
    "white": "#FFFFFF",
    "green_50": "#F0F9FF",
    "green_100": "#E8F8F5",
    "green_600": "#1E8449"
}

MAX_FILE_SIZE_MB = 10
ALLOWED_EXCEL_EXTENSIONS = [".xlsx", ".xls"]

