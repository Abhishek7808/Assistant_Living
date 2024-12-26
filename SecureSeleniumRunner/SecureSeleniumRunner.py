"""
# Project Template Version = 0.0.0.1
# -------------------------------------------------------------------------------
# Name: SecureSeleniumRunner.py
# Purpose: To Initiate the framework process
# Author: Vivek Purohit (44454)
# -------------------------------------------------------------------------------
"""

import os
from os import path
import sys
import shutil
import winreg
sys.path[:0] = ['../../']
from datetime import datetime
from Assisted_Living.SecureSeleniumRunner.SecureSelenium import SecureSelenium
from configparser import ConfigParser
from pythonframework.FrameworkCore.TestResultReport.ColorPrint import ColorPrint

#Create a system variable and set the path of the frameworksettings.ini
ini_path = os.getcwd()+'\\'+'frameworksettings.ini'
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
winreg.SetValueEx(key, 'SECURE_SELENIUM_RUNNER', 0, winreg.REG_SZ, ini_path)
winreg.CloseKey(key)

#Read system variable
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_READ)
var_value, _ = winreg.QueryValueEx(key, 'SECURE_SELENIUM_RUNNER')
winreg.CloseKey(key)

now=datetime.now()
dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
print("[Info]: Framework Execution Started: " +str(dt_string))
config = ConfigParser()
config.read(var_value)
relative_path = config.get('DEFAULT', 'project_hirarchy')

shutil.copy(src = 'frameworksettings.ini',dst = relative_path)
print("[Info]: Config file copied to root folder")

if config.defaults().__len__() > 0:
  root = config.get('DEFAULT', 'AutomationFolderPath')

  if path.exists(root):
    #ColorPrint.PrintGreen(text="[Info]: Test starting, reading configuration file..")
    SecureSelenium = SecureSelenium(root)
    SecureSelenium.RunMainTest()
    now=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    print("[Info]: Test Automation ended: " +str(dt_string))

  else:
    ColorPrint.PrintRed("[Error]: Please check the test automation path!, enter path as "+root)

else:
  ColorPrint.PrintRed("[Error]: Please check the config file or its existence")
