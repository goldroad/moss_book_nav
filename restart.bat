@echo off
cd /d %~dp0
echo Restarting service...
taskkill /f /im python.exe >nul 2>nul
echo Stopping service...
ping -n 3 127.0.0.1 >nul
echo Starting service...
start python app.py
echo Restart complete.
pause