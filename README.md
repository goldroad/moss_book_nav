# 作者信息
公众号：苔藓星球
作者：包子

# 苔藓名称导航系统

基于 Python + Flask + SQLite 的本地检索工具，用于按苔藓名称快速定位多本书籍中的页码，并集成苔藓名称数据库（来源：sp2000.org.cn）。无需安装额外服务，双击启动即可使用。

提供**桌面版(.exe)** 和 **网页版** 两种启动方式。

## 核心功能

- 模糊查询：输入苔藓名称的一个字或一个词即可检索，支持纲/目/科/属/种等层级名称。
- 多书籍聚合：同名在不同书籍的页码统一展示，可按所选书籍过滤。
- 按书籍浏览：选择某一本书，查看其下所有苔藓名称及页码。
- 苔藓名称数据库：浏览门→纲→目→科→属→物种级联结构，支持模糊匹配和分页。
- 系统树：苔藓名称脑图展示。
- 数据导入（书籍页码）：上传 xlsx，支持重复导入（可选择清空旧数据）。

## 启动方式

### 桌面版（.exe，推荐用于最终用户）

无需安装 Python，直接双击运行：

```
dist\苔藓名称导航.exe
```

运行后会自动：
1. 启动后台服务（Flask，内嵌 SQLite 数据库）
2. 弹出**原生桌面窗体**（内嵌 WebView2 浏览器引擎）
3. 在窗体中直接显示应用界面，无需打开外部浏览器
4. 关闭窗体即退出程序

技术特点：
- 体积约 29MB（单文件）
- 使用 WebView2 引擎（基于 Chromium，Win10 1803+ 自带）
- 无需外部浏览器，所有内容在窗口内显示
- 首次启动时自动将数据库（`booknavi.db`）复制到 .exe 同目录

系统要求：
- Windows 10 版本 1803 或更高（需 WebView2 Runtime）
- .NET Framework 4.8+（Windows 自带）

如需调试（显示控制台输出），可使用 `dist\苔藓名称导航_debug.exe`。

### 网页版（开发/调试用途）

- 双击 `start.bat`，或在命令行运行：`python app.py`
- 浏览器访问：`http://127.0.0.1:5000/`

如果修改代码以后没有生效，使用以下命令停止程序：
taskkill /f /t /im python.exe

注意：桌面版与网页版共用同一个后端服务（动态端口），同一时间各启动一个实例。

## 使用说明

- 数据导入（书籍页码）
  - 页面入口："查询"页右上角按钮"导入书籍页码表格"或直接访问 `/import`
  - 上传一个 `xlsx` 文件：每个 `sheet` 代表一本书；第1列为苔藓名称，第2列为页码（导入时自动去除左右空格，空行忽略）。
  - "导入前清空旧数据"可选，用于重复导入。

- 检索与浏览
  - "查询"页（`/`）：输入关键词检索；可勾选要显示的书籍；结果按书籍分组展示，并显示换算后的 PDF 页码（如配置）。
  - "按书籍浏览"（`/browse`）：选择一本书，浏览其下所有苔藓名称及页码。
  - "苔藓名称数据库"（`/taxonomy`）：浏览门→纲→目→科→属→物种级联结构，支持模糊匹配和分页。

- 苔藓名称脑图（`/mindmap`）：可视化展示苔藓名称的分类层级关系。

## 数据库结构

- `books(id, book_name, short_name, offset, has_pdf, region, publisher, publish_date, price, page, moss_count, author, cover_image, notes, has_txt, has_line, has_spec, has_env, has_micro, has_micro_section)`
  - `has_txt`: 文字描述（1有 0无）
  - `has_line`: 线条图（1有 0无 2部分有）
  - `has_spec`: 标本图（1有 0无 2部分有）
  - `has_env`: 生境图（1有 0无 2部分有）
  - `has_micro`: 显微图（1有 0无 2部分有）
  - `has_micro_section`: 显微剖面（1有 0无 2部分有）
  - `has_elec`: 电镜图（1有 0无 2部分有）
- `mosses(id, moss_name)`
- `moss_pages(id, book_id, moss_id, page_id)`
- `moss_data(门拉丁名, 门中文名, 纲拉丁名, 纲中文名, 目拉丁名, 目中文名, 科拉丁名, 科中文名, 属拉丁名, 属中文名, 物种拉丁名, 物种中文名)`

系统在启动/导入时确保必要索引与字段存在，并使用 SQLite 单机运行，无外部服务依赖。
可以使用Navicat等数据库工具查看和管理数据库，账号密码为空。

## 桌面版（.exe）打包说明

### 环境要求
- Python 3.12
- Windows 10+
- 依赖：`pip install -r requirements.txt`

### 打包命令
```
pyinstaller --clean 苔藓名称导航.spec
```

产物位于 `dist\苔藓名称导航.exe`（单文件，约 29MB）。

调试版本（带控制台输出）：
```
pyinstaller --clean 苔藓名称导航_debug.spec
```

## 桌面版技术栈
- **GUI**: pywebview 5.4（内嵌 WebView2 引擎）
- **WebView2 Runtime**: Windows 10 1803+ 自带 Chromium 引擎
- **.NET**: pythonnet + clr-loader 调用 WebView2 COM 接口
- **后端**: Flask
- **数据库**: SQLite 3
- **打包工具**: PyInstaller 6.x

## 项目文件说明
- `app.py` - Flask 后端主程序（含路由、数据库、业务逻辑）
- `desktop_app.py` - 桌面版启动器（pywebview + WebView2 + Flask 线程）
- `苔藓名称导航.spec` - 发布版 PyInstaller 打包配置（内嵌 WebView2 窗口，约 29MB）
- `苔藓名称导航_debug.spec` - 调试版 PyInstaller 打包配置（带控制台窗口）
- `start.bat` - 网页版启动脚本

## 反馈与更新
- 如需支持其他书籍或报错改进，请在公众号留言。
- 如果数据有错误或者遗漏，请在公众号留言。

## 许可协议
除另有说明外，本项目文档与页面内容采用 CC BY-NC-SA 4.0 国际许可协议进行许可：
https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh

---
版权所有：八方网域-无涯
最后更新：2026-07-01
