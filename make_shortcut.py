import os, subprocess

desktop_paths = [
    os.path.join(os.path.expanduser('~'), 'Desktop'),
    os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop'),
    os.path.join(os.path.expanduser('~'), 'OneDrive - Personal', 'Desktop'),
]
desktop = next((p for p in desktop_paths if os.path.isdir(p)), desktop_paths[0])

# Запускаем через pythonw.exe — без консоли, не триггерит антивирус
pythonw = r'C:\Scarlett\venv\Scripts\pythonw.exe'
script  = r'C:\Scarlett\scarlett.py'
workdir = r'C:\Scarlett'
ico     = r'C:\Scarlett\scarlett_icon.ico'
lnk_path = os.path.join(desktop, 'Scarlett.lnk')

try:
    import win32com.client
    sh  = win32com.client.Dispatch('WScript.Shell')
    lnk = sh.CreateShortCut(lnk_path)
    lnk.Targetpath      = pythonw
    lnk.Arguments       = f'"{script}"'
    lnk.WorkingDirectory = workdir
    if os.path.exists(ico):
        lnk.IconLocation = ico + ',0'
    lnk.Description = 'Scarlett AI Assistant'
    lnk.WindowStyle = 7   # 7 = minimized (скрывает консоль если есть)
    lnk.save()
    print('[OK] Shortcut created:', lnk_path)
except Exception as e:
    print('[!] win32com error:', e)
    vbs = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'mklink.vbs')
    with open(vbs, 'w') as f:
        f.write('Set sh=CreateObject("WScript.Shell")\n')
        f.write(f'Set lnk=sh.CreateShortcut("{lnk_path}")\n')
        f.write(f'lnk.TargetPath="{pythonw}"\n')
        f.write(f'lnk.Arguments=Chr(34) & "{script}" & Chr(34)\n')
        f.write(f'lnk.WorkingDirectory="{workdir}"\n')
        f.write('lnk.WindowStyle=7\n')
        f.write('lnk.Description="Scarlett AI"\n')
        f.write('lnk.Save\n')
    subprocess.run(['cscript', '//nologo', vbs], capture_output=True)
    if os.path.exists(lnk_path):
        print('[OK] Shortcut via VBS:', lnk_path)
    else:
        print('[!] Could not create shortcut')
