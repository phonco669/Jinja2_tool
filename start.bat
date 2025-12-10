@echo off
title Jinja2 Real-time Renderer Tool
echo Starting Jinja2 Tool...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b
)

:: Install dependencies
echo Installing/Updating dependencies...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo.
    echo -------------------------------------------------------
    echo Error: Failed to install dependencies.
    echo Please check your internet connection.
    echo You can try manually running: pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo -------------------------------------------------------
    pause
    exit /b
)

:: Run the application
echo Starting Flask Server...
python app.py

pause
