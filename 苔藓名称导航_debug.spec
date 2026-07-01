# -*- mode: python ; coding: utf-8 -*-
"""
苔藓名称导航 - 调试版打包配置（带控制台输出）
八方网域-无涯
"""

a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static'), ('img', 'img'), ('moss2026.json', '.'), ('moss2025.json', '.'), ('booknavi.db', '.')],
    hiddenimports=[
        'flask', 'openpyxl', 'pypinyin', 'app',
        'pywebview', 'webview', 'clr', 'clr_loader', 'pythonnet',
        'clr_loader.netfx', 'clr_loader.types',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Qt 系列 (edgechromium 引擎不需要，改用 WebView2)
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        # CEF 浏览器引擎 (edgechromium 不需要)
        'cefpython3',
        # 数据处理
        'numpy', 'pandas', 'scipy', 'matplotlib',
        # 图像处理
        'PIL', 'pillow',
        # 其他不必要的大型库
        'setuptools', 'pip', 'wheel',
        'pytest', '_pytest', 'unittest',
        'pydoc', 'doctest',
        'IPython', 'jupyter', 'notebook',
        'requests', 'urllib3', 'certifi',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='苔藓名称导航_debug',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        'vcruntime140.dll', 'vcruntime1_40_1.dll', 'msvcp140.dll',
        'python3.dll', 'python312.dll',
    ],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
