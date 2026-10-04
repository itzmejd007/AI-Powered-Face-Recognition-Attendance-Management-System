#!/usr/bin/env bash
# Face Recognition Attendance System - Setup & Launcher for Linux & macOS

echo "========================================================"
echo "  Face Recognition Attendance System - Setup & Launcher"
echo "========================================================"
echo ""

# 1. Check Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python is not installed!"
    echo "Please install Python 3.8+ using your package manager or from https://www.python.org/"
    exit 1
fi

echo "[1/3] Python detected: $($PYTHON_CMD --version)"
echo ""

# 2. Check and install dependencies
echo "[2/3] Checking dependencies..."
$PYTHON_CMD -c "import flask, cv2, PIL, pandas" &>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing missing requirements from requirements.txt..."
    pip install -r requirements.txt || pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies. Check your internet connection."
        exit 1
    fi
else
    echo "[OK] All required libraries are installed!"
fi
echo ""

# 3. Launch application
echo "[3/3] Starting Server at http://localhost:5000 ..."
if command -v xdg-open &>/dev/null; then
    xdg-open "http://localhost:5000" &
elif command -v open &>/dev/null; then
    open "http://localhost:5000" &
fi

$PYTHON_CMD app.py
