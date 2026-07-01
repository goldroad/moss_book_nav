@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
echo [DEBUG BUILD] Build EXE with console for error output.
pyinstaller --clean --onefile --console ^
    --name "苔藓名称导航_debug" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "img;img" ^
    --add-data "moss2026.json;." ^
    --add-data "moss2025.json;." ^
    --add-data "booknavi.db;." ^
    --hidden-import=flask ^
    --hidden-import=openpyxl ^
    --hidden-import=pypinyin ^
    desktop_app.py
echo.
echo [DONE] EXE is at: dist\苔藓名称导航_debug.exe
pause
