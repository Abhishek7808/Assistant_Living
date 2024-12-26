@echo off
echo Stopping any running Appium server instances...

:: Stop any running Appium instances
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :4723') do taskkill /F /PID %%a

:: Optional: Wait for a moment to ensure all processes are terminated
timeout /t 2 /nobreak >nul

echo Starting a new Appium server instance...

:: Start Appium on the default port (4723)
start appium

:: Optional: Wait for the server to start (adjust the time as needed)
timeout /t 20 /nobreak >nul  :: Sleep for 20 seconds (you can adjust this time)

echo Appium server restarted successfully.

:: Wait for a moment before running the next command
timeout /t 5 /nobreak >nul

:: Run your Selenium Runner
@echo off
cd /d D:\Automation Framework\Regression Cycle 2 SOS\Assisted_Living\SecureSeleniumRunner
start "" "D:\Automation Framework\Regression Cycle 2 SOS\Assisted_Living\SecureSeleniumRunner\Run.cmd"
