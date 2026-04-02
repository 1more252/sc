@echo off
cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Download from https://python.org
    pause & exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 ( echo [ERROR] venv failed & pause & exit /b 1 )

echo [2/5] Activating...
call venv\Scripts\activate.bat

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo [4/5] Installing core dependencies...
pip install speechrecognition pyaudio pyttsx3 requests psutil pywin32 comtypes pycaw pillow pygame pystray edge-tts

echo [5/5] Installing AI upgrades (vector memory + embeddings)...
pip install chromadb sentence-transformers

echo.
echo ============================================
echo  Scarlett AI Upgrade installed!
echo ============================================
echo.
echo Checking AI upgrades:
venv\Scripts\python.exe -c "import chromadb;              print('  [OK] ChromaDB - vector memory')"          2>nul || echo   [--] chromadb not installed
venv\Scripts\python.exe -c "import sentence_transformers; print('  [OK] sentence-transformers - embeddings')" 2>nul || echo   [--] sentence-transformers not installed
venv\Scripts\python.exe -c "import psutil;                print('  [OK] psutil - system context')"            2>nul || echo   [--] psutil not installed
venv\Scripts\python.exe -c "import win32gui;              print('  [OK] win32gui - active window')"           2>nul || echo   [--] win32gui not installed (part of pywin32)
echo.
echo Tool Calling: set groq_key or mistral_key in Settings to enable
echo.
pause
