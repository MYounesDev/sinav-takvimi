"""
Dynamic Exam Scheduler System - Main Entry Point
Kocamanuali University - Yazlab-1 Project

This is the main entry point for the application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from src.ui.splash_screen import SplashScreen
from src.ui.main_window import MainWindow
from src.database.db_manager import DatabaseManager

def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Exam Planning System")
    app.setOrganizationName("Kocamanuali University")
    
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    window = MainWindow()
    
    splash = SplashScreen()
    splash.show()
    app.processEvents()
    
    def show_main_window():
        splash.close()
        window.showMaximized()
        window.raise_()
        window.activateWindow()
    
    QTimer.singleShot(2500, show_main_window)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

