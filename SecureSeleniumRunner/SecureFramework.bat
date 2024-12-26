@echo off
echo *********** Secure Test Automation Framework Installation ***********
echo.
call :checkPython
pause
exit

:: Function to check if python exists.
:checkPython
where python 3.8.5 > nul 2>&1
if %errorlevel% equ 0 (
    echo [Info] Python is installed.
	goto clonedeliverables
) else (
    echo [Info] Python is not installed.
	goto downloadPython	
)

:: Function to download python 3.8.5
:downloadPython
D:
mkdir PythonDownloads
cd PythonDownloads
::curl https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe --output python-3.8.5-amd64.exe
start python-3.8.5-amd64.exe
echo [Info] Please install the python and set the environment varible and re run the script.
pause
exit

::Function to clone deliverables
:clonedeliverables
IF EXIST "pythonframework\" (
  echo [Info] The directory exists, deleting the existing folder.
  rmdir /s /q pythonframework
) ELSE (.
  echo [Info] The directory does not exist, cloning to the pythonframework.
)
git clone --branch TestAutomationframework_dev https://git.securemeters.com:8443/scm/aswautomationplatform/pythonframework.git
goto installLib

:: Function to install required libraries to execute function.
:installLib
echo Inside Lib function
cd pythonframework
pip install -r requirements.txt
echo framework is installed successfully
pause

