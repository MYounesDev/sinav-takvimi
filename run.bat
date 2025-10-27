@echo off
REM Windows Batch Script to run Exam Scheduler

echo ====================================
echo   Exam Scheduler
echo   Kocaeli University
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.12+ from https://www.python.org/
    pause
    exit /b 1
)

REM Run the application
echo Starting Exam Scheduler...
echo.
python main.py

REM If the program crashes, pause to see the error
if errorlevel 1 (
    echo.
    echo The application encountered an error.
    pause
)



