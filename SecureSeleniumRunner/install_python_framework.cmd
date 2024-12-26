@echo off
python Setup.py
for /f "tokens=2 delims==" %%i in ('findstr /b "project_hirarchy=" frameworksettings.ini') do cd /d %%i
cd Deliverables\Framework\Python
echo ------------------------------------------ Installing python framework ----------------------------------------------------
pip install pythonframework.tar.gz
echo ------------------------------------------ Python framework Installed------------------------------------------------------
pause
exit