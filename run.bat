@echo off
title Face Recognition Attendance System
color 0b

echo ========================================================
echo   Face Recognition Attendance System - Setup & Launcher
echo ========================================================
echo.

:: 1. Check Python installation
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not added to PATH!
    echo Please install Python 3.8 - 3.12 from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Python detected:
python --version
echo.

:: 2. Check and install dependencies if missing
echo [2/3] Checking required libraries...
python -c "import flask, cv2, PIL, pandas" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing missing requirements from requirements.txt...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install dependencies. Check your internet connection.
        pause
        exit /b 1
    )
) else (
    echo [OK] All required libraries are already installed!
)
echo.

:: 3. Launch application
echo [3/3] Starting Server at http://localhost:5000 ...
start "" http://localhost:5000
python app.py

pause
