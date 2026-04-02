# -*- coding: utf-8 -*-
"""
Scarlett Launcher — запуск без консольного окна.
Файл .pyw запускается pythonw.exe и не показывает консоль.
"""
import os, sys

# Добавляем папку скрипта в PATH чтобы найти scarlett.py
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

# Скрываем консоль на случай если всё же появилась
try:
    import ctypes
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
except:
    pass

# Запускаем основное приложение
exec(open(os.path.join(script_dir, 'scarlett.py'), encoding='utf-8').read())
