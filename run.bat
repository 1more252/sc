@echo off
cd /d "%~dp0"

if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe scarlett.py
) else (
    python scarlett.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] Scarlett crashed. See error above.
    pause
)
