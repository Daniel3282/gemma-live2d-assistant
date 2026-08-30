@echo off
setlocal enabledelayedexpansion
title Live2D Assistant Setup and Startup

echo ===================================================
echo   Live2D Assistant - Automated Setup ^& Launcher
echo ===================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found on your system PATH.
    echo Please install Python 3.10 or newer and make sure to check "Add Python to PATH" during installation.
    pause
    exit /b
)

:: Create Virtual Environment if it does not exist
if not exist .venv (
    echo [INFO] Creating local virtual environment venv...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
)

:: Activate Virtual Environment
call .venv\Scripts\activate.bat

:: Upgrade pip first
echo [INFO] Checking package manager dependencies...
python -m pip install --upgrade pip >nul 2>&1

:: Install 'uv' inside the virtual environment
echo [INFO] Installing 'uv' package installer to ensure fast and reliable dependencies setup...
pip install uv

if %errorlevel% equ 0 (
    echo [INFO] Installing required libraries via 'uv' - this is extremely fast...
    uv pip install -r requirements.txt
) else (
    echo [WARNING] Failed to install 'uv'. Falling back to standard 'pip' package installer...
    pip install -r requirements.txt
)

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install required packages. Please check your internet connection.
    pause
    exit /b
)

echo [INFO] All dependencies are ready. Starting the Live2D Assistant...
python main.py

pause