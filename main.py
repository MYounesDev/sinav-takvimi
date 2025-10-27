"""
Dynamic Exam Scheduler System - Main Entry Point
Kocaeli University - Yazlab-1 Project

This is the main entry point for the application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from src.ui.splash_screen import SplashScreen
from src.ui.main_window import MainWindow
from src.database.db_manager import DatabaseManager


def main():
    """Initialize and run the application"""
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Exam Scheduler")
    app.setOrganizationName("Kocaeli University")
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Process events to show splash
    app.processEvents()
    
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Create main window (but don't show yet)
    window = MainWindow()
    
    # Show main window after splash closes
    def show_main_window():
        window.show()
    
    # Close splash and show main window after it finishes
    QTimer.singleShot(2100, show_main_window)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

