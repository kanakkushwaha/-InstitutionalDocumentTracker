@echo off
title Institutional Document Tracker

cd /d "%~dp0"

echo ========================================
echo Institutional Document Tracker Starting
echo ========================================
echo.

if not exist ".\venv\Scripts\python.exe" (
    echo Virtual environment not found at .\venv\Scripts\python.exe
    echo Please check that the project venv exists.
    pause
    exit /b 1
)

echo Opening project at: %cd%
echo.
echo Flask server will run at:
echo http://127.0.0.1:5000
echo.
echo Keep this window open while using the website.
echo Close this window or press Ctrl+C to stop the server.
echo.

start http://127.0.0.1:5000
.\venv\Scripts\python.exe run.py

pause
