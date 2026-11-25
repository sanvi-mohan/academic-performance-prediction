@echo off
title AI-Based Academic Performance Prediction System
cd /d "%~dp0"

echo ============================================================
echo   AI-Based Academic Performance Prediction System
echo ============================================================
echo   Project Location: %CD%
echo ============================================================
echo.

set PYTHON_CMD=

:: 1. Check local python runtime in scratch tools first
if exist "%~dp0..\tools\python\python.exe" (
    set PYTHON_CMD="%~dp0..\tools\python\python.exe"
)

:: 2. Check system python if local not found
if "%PYTHON_CMD%"=="" (
    python --version >nul 2>nul && set PYTHON_CMD=python
)
if "%PYTHON_CMD%"=="" (
    py --version >nul 2>nul && set PYTHON_CMD=py
)
if "%PYTHON_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if "%PYTHON_CMD%"=="" if exist "C:\Python311\python.exe" set PYTHON_CMD="C:\Python311\python.exe"

if "%PYTHON_CMD%"=="" (
    echo [ERROR] A working Python runtime was not found.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo and ensure "Add Python to PATH" is checked during setup.
    echo.
    pause
    exit /b 1
)

echo [1/3] Using Python: %PYTHON_CMD%

echo [2/3] Checking dependencies (Flask)...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet --no-warn-script-location

echo [3/3] Starting Flask Application...
echo.
echo ============================================================
echo   Website running at: http://127.0.0.1:5000
echo   Opening in your default browser...
echo   Press Ctrl+C in this terminal window to stop the server.
echo ============================================================
echo.

set PYTHONPATH=%CD%
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000"

%PYTHON_CMD% app.py
pause
