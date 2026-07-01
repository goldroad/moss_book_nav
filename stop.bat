@echo off
setlocal

chcp 65001 >nul
title 停止苔藓名称导航

echo.
echo 将停止本地服务（python.exe）。请保存工作。
echo.
choice /C 12 /M "是否继续停止？按 1 继续，2 取消"
if errorlevel 2 (
  echo 已取消停止操作。
  goto :end
)

echo 正在停止程序...
taskkill /f /t /im python.exe
if %errorlevel%==0 (
  echo 程序已停止。
) else (
  echo 未检测到正在运行的程序或停止失败。
)

:end
echo.
echo 操作完成。按任意键关闭窗口。
pause >nul
endlocal