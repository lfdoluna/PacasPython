#!/usr/bin/env python
# -*- coding: utf-8 -*-
from win32api import (GetModuleFileName, RegCloseKey, RegDeleteValue,
                      RegOpenKeyEx, RegSetValueEx)
from win32con import HKEY_LOCAL_MACHINE, KEY_WRITE, REG_SZ
SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
def run_at_startup_set(appname, path):
    """
    Sets the registry key to run at startup.
    """
    key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, SUBKEY, 0, KEY_WRITE)
    RegSetValueEx(key, appname, 0, REG_SZ, path)
    RegCloseKey(key)
def run_script_at_startup_set(appname, script):
    path = "%s %s" % (GetModuleFileName(0), script)
    run_at_startup_set(appname, path)

def run_script_at_startup_setw(appname, script):
    path = "C:\Users\lfdlu\AppData\Local\Programs\Python\Python27\pythonw.exe c:\PacasPython\runSerPacas.pyw"
    run_at_startup_set(appname, path)
def run_at_startup_remove(appname):
    """
    Removes the run-at-startup registry key.
    """
    key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, SUBKEY, 0, KEY_WRITE)
    RegDeleteValue(key, appname)
    RegCloseKey(key)

run_script_at_startup_setw("IniciaPython", "c:\PacasPython\runSerPacas.pyw")
#run_script_at_startup_set("IniciaPython", "c:\PacasPython\initP.py")
