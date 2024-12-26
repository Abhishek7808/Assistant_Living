@echo off
mkdir ..\..\logs
::python SecureSeleniumRunner.py > ..\..\logs\output_%time::=-%.txt
python SecureSeleniumRunner.py
pause
exit