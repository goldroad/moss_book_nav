# 项目构建规则

## 构建命令

**Tauri 项目必须使用 `build.bat` 构建，不要直接运行 `npm run tauri build`！**

`build.bat` 包含以下关键步骤：
1. 设置 MSVC 环境（vcvarsall.bat x64）
2. 安装前端依赖（npm install）
3. 构建前端（npm run build）
4. 构建 Tauri 桌面应用（npm run tauri build）
5. 复制 exe 到根目录（API-Key-Manager.exe）

## 构建后检查

构建完成后，**必须确认 .exe 文件已生成**：
- 检查 `src-tauri\target\release\key_manager_new.exe` 是否存在
- 检查根目录的 `API-Key-Manager.exe` 是否已更新
- 如果没有生成 .exe，不能告诉用户"构建完成"

## 启动方式

- 开发模式：`npm run tauri dev`
- 生产构建：`build.bat`（双击或在终端运行）
- 构建产物：`API-Key-Manager.exe`（根目录）

## 常见问题

### Windows SDK 头文件缺失

**错误**：`Cannot open include file: 'windows.h'`

**原因**：PowerShell 环境下 Windows SDK include 路径未正确设置

**解决方案**：手动设置 INCLUDE 环境变量后构建：
```powershell
$env:INCLUDE = "C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\ucrt;C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\shared;C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\um;C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\winrt;" + $env:INCLUDE
npm run tauri build
```

如果路径不存在，先确定 Windows SDK 版本：`dir "C:\Program Files (x86)\Windows Kits\10\Include\"`

构建完成后记得复制 exe：
```powershell
Copy-Item "src-tauri\target\release\key_manager_new.exe" "API-Key-Manager.exe" -Force
```
