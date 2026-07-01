@echo off
chcp 65001 >nul 2>&1
title 苔藓名称导航 - 打包工具
echo ============================================
echo  苔藓名称导航系统 - 桌面版打包工具
echo  八方网域-无涯
echo ============================================
echo.

REM === 第1步：检查 Python ===
echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请确保 Python 已安装并添加到 PATH
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo      检测到: %%i
echo.

REM === 第2步：安装依赖 ===
echo [2/4] 安装/更新依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查 requirements.txt
    pause
    exit /b 1
)
echo      依赖安装完成
echo.

REM === 第3步：清理旧构建 ===
echo [3/4] 清理旧构建文件...
if exist build rmdir /s /q build
if exist dist\苔藓名称导航.exe (
    del /f /q dist\苔藓名称导航.exe
    echo      已删除旧版 exe
) else (
    echo      无需清理
)
echo.

REM === 第4步：执行打包 ===
echo [4/4] 开始打包 release 版 EXE...
echo      执行命令: pyinstaller --clean 苔藓名称导航.spec
echo.
pyinstaller --clean 苔藓名称导航.spec
if errorlevel 1 (
    echo.
    echo [错误] 打包失败！请检查上方错误信息
    pause
    exit /b 1
)

REM === 验证产物 ===
echo.
echo ============================================
echo  验证构建产物...
echo ============================================
if exist "dist\苔藓名称导航.exe" (
    for %%A in ("dist\苔藓名称导航.exe") do (
        set size=%%~zA
    )
    echo.
    echo  ✓ 构建成功！
    echo.
    echo  文件路径: dist\苔藓名称导航.exe
    for /f "tokens=*" %%i in ('powershell -Command "[math]::Round((Get-Item 'dist\苔藓名称导航.exe').Length/1MB,2)"') do echo  文件大小: %%i MB
    echo.
    echo  双击 dist\苔藓名称导航.exe 即可运行
) else (
    echo.
    echo  ✗ 构建失败 - 未找到 EXE 文件
    echo  请检查上方错误信息
)
echo.
echo ============================================
pause
