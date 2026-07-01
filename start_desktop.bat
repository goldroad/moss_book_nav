@echo off
chcp 65001 >nul 2>&1

cd /d "%~dp0"

echo ============================================
echo   苔藓名称导航系统 - 桌面版
echo ============================================
echo.

REM 检查 Python 安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERR] Python not found. Please install Python 3.9+ and add to PATH.
    pause
    exit /b 1
)

REM 自动安装依赖
echo [INFO] Checking dependencies...
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERR] Dependency install failed. Please run manually:
    echo        pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Dependencies ready.

REM 启动桌面版
echo [INFO] Starting desktop app...
echo ============================================
python desktop_app.py

pause
