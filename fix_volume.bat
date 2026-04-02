@echo off
echo.
echo === Fix pycaw (volume control) ===
echo.

if exist "venv\Scripts\pip.exe" (
    set PIP=venv\Scripts\pip.exe
    set PY=venv\Scripts\python.exe
    echo Using venv Python
) else (
    set PIP=pip
    set PY=python
    echo Using system Python
)

echo Step 1: Remove old pycaw and comtypes...
%PIP% uninstall pycaw comtypes -y 2>nul

echo Step 2: Install correct versions...
%PIP% install comtypes==1.2.0
%PIP% install pycaw==20181226

echo Step 3: Testing...
%PY% -c "from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume; from comtypes import CLSCTX_ALL; from ctypes import cast, POINTER; d=AudioUtilities.GetSpeakers(); i=d.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None); v=cast(i,POINTER(IAudioEndpointVolume)); print('OK! Level:', int(v.GetMasterVolumeLevelScalar()*100))"

if errorlevel 1 (
    echo.
    echo [ERROR] pycaw still fails
    echo Try manually: %PIP% install --upgrade pycaw comtypes
) else (
    echo.
    echo SUCCESS! Restart run.bat now.
)
echo.
pause
