#!/bin/bash
# Linux/Mac Shell Script to run Exam Scheduler

echo "===================================="
echo "  Exam Scheduler"
echo "  Kocaeli University"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.12+ from https://www.python.org/"
    exit 1
fi

# Run the application
echo "Starting Exam Scheduler..."
echo ""
python3 main.py

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "The application encountered an error."
    read -p "Press Enter to exit..."
fi



