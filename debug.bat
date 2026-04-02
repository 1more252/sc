@echo off
cd /d "%~dp0"
echo ============================================
echo  Scarlett AI Upgrade - Debug mode
echo ============================================

python --version
if errorlevel 1 ( echo ERROR: Python not found & pause & exit /b 1 )

if exist venv\Scripts\python.exe (
    echo.
    echo Checking AI upgrades:
    venv\Scripts\python.exe -c "import chromadb;              print('  [OK] ChromaDB')"              2>nul || echo   [--] chromadb    -- pip install chromadb
    venv\Scripts\python.exe -c "import sentence_transformers; print('  [OK] sentence-transformers')" 2>nul || echo   [--] sent-trans  -- pip install sentence-transformers
    venv\Scripts\python.exe -c "import psutil;                print('  [OK] psutil')"                2>nul || echo   [--] psutil      -- pip install psutil
    venv\Scripts\python.exe -c "import win32gui;              print('  [OK] win32gui')"              2>nul || echo   [--] win32gui    -- pip install pywin32
    echo.
    echo Launching Scarlett with full output:
    echo ============================================
    venv\Scripts\python.exe scarlett.py
) else (
    echo venv not found - run install.bat first!
)

echo.
echo Exit code: %errorlevel%
pause
