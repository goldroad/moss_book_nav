# -*- mode: python ; coding: utf-8 -*-
"""
苔藓名称导航 - 发布版打包配置
八方网域-无涯

桌面方案：pywebview + WebView2 (edgechromium)
- 原生桌面窗体内嵌 WebView2 浏览器
- 需要系统安装 WebView2 Runtime（Win10 1803+ 自带）
- .NET Framework 4.8+ 已内置配置（desktop_app.py 中自动指定）
"""

a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static'), ('img', 'img'), ('moss2026.json', '.'), ('moss2025.json', '.'), ('booknavi.db', '.')],
    hiddenimports=[
        'flask', 'openpyxl', 'pypinyin', 'app',
        'pywebview', 'webview',
        'clr', 'clr_loader', 'pythonnet',
        'clr_loader.netfx', 'clr_loader.types',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'cefpython3',
        'numpy', 'pandas', 'scipy', 'matplotlib',
        'PIL', 'pillow',
        'setuptools', 'pip', 'wheel',
        'pytest', '_pytest', 'unittest',
        'pydoc', 'doctest',
        'IPython', 'jupyter', 'notebook',
        'requests', 'urllib3', 'certifi',
    ],
    noarchive=False,
    optimize=0,  # optimize=2 导致 pywebview/pythonnet 异常
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='苔藓名称导航',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        'vcruntime140.dll', 'vcruntime1_40_1.dll', 'msvcp140.dll',
        'python3.dll', 'python312.dll',
        'WebView2Loader.dll',
    ],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
