"""
苔藓名称导航系统 - 桌面版启动器
八方网域-无涯

使用 pywebview (edgechromium引擎) 将 Flask 网页应用包装为原生桌面窗体。
支持 PyInstaller 打包为单文件 .exe。

打包命令（在项目根目录执行）：
    pyinstaller --clean 苔藓名称导航.spec
"""

import os
import sys

# ========== 必须在 import webview 之前配置 .NET Runtime ==========
# pywebview 5.4 在 Windows 上通过 pythonnet 调用 WebView2 COM 接口
# pythonnet 默认按 coreclr -> mono -> netfx 顺序查找运行时
# 但自动查找在某些系统上会失败，需手动指定 netfx
try:
    import clr_loader
    import pythonnet
    netfx = clr_loader.get_netfx()
    print(f"[DEBUG] clr_loader OK, netfx: {netfx is not None}")
    if netfx is not None:
        pythonnet.set_runtime(netfx)
        print(f"[DEBUG] pythonnet.set_runtime OK")
except Exception as e:
    # 如果设置失败，webview 会回退到自动查找
    print(f"[DEBUG] .NET Runtime init failed: {e}")

# 指定 WebView2 渲染器（edgechromium 需要 Win10 1803+ 自带 WebView2 Runtime）
os.environ.setdefault("PYWEBVIEW_GUI", "edgechromium")

import socket
import threading
import time
import webview

# ========== 路径兼容层 ==========
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def find_free_port() -> int:
    """动态寻找一个可用的 TCP 端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_port(port: int, timeout: int = 15) -> bool:
    """等待端口真正开始监听"""
    start_ts = time.time()
    while time.time() - start_ts < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(0.2)
    return False


def _setup_error_log():
    """设置错误日志文件（用于 release 版调试）"""
    try:
        if getattr(sys, "frozen", False):
            log_dir = os.path.dirname(sys.executable)
        else:
            log_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(log_dir, "error.log")

        class Logger:
            def __init__(self, path):
                self.path = path
                # windowed 模式下 sys.__stdout__ 可能为 None
                self.terminal = sys.__stdout__ or None
            def write(self, msg):
                if msg.strip():
                    try:
                        with open(self.path, "a", encoding="utf-8") as f:
                            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}")
                    except Exception:
                        pass
                if self.terminal is not None:
                    try: 
                        self.terminal.write(msg)
                    except Exception: 
                        pass
            def flush(self):
                if self.terminal is not None:
                    try: 
                        self.terminal.flush()
                    except Exception: 
                        pass

        sys.stdout = Logger(log_path)
        sys.stderr = Logger(log_path)
    except Exception:
        pass


def start_flask_in_thread(port: int, ready_event: threading.Event):
    """在后台线程中运行 Flask 应用"""
    if getattr(sys, "frozen", False):
        user_dir = os.path.dirname(sys.executable)
        os.chdir(user_dir)

    sys.path.insert(0, BASE_DIR)
    import app as flask_app

    print(f"[DEBUG] Flask module: {flask_app}")
    print(f"[DEBUG] Routes: {[rule.rule for rule in flask_app.app.url_map.iter_rules()]}")
    print(f"[DEBUG] DB_PATH: {flask_app.DB_PATH}")
    sys.stdout.flush()

    try:
        ready_event.set()
        flask_app.app.run(
            host="127.0.0.1",
            port=port,
            debug=False,
            use_reloader=False,
        )
    except Exception as e:
        print(f"[ERROR] Flask failed: {e}", flush=True)


def main():
    _setup_error_log()

    # 动态选择端口
    port = find_free_port()
    print(f"[启动] 选定端口 {port}")
    sys.stdout.flush()

    # 启动 Flask 后台线程
    ready_event = threading.Event()
    flask_thread = threading.Thread(
        target=start_flask_in_thread,
        args=(port, ready_event),
        daemon=True,
    )
    flask_thread.start()

    # 等待服务就绪
    if not ready_event.wait(timeout=5):
        print("[错误] Flask 服务未在 5 秒内初始化")
        sys.exit(1)

    if not wait_for_port(port, timeout=15):
        print(f"[错误] 端口 {port} 未响应，Flask 启动失败")
        sys.exit(1)

    print(f"[就绪] Flask 服务已启动，端口 {port}")
    sys.stdout.flush()

    # 创建原生桌面窗体（WebView2 内嵌浏览器）
    window = webview.create_window(
        title="苔藓名称导航系统",
        url=f"http://127.0.0.1:{port}/",
        width=1280,
        height=800,
        min_size=(1024, 600),
        text_select=True,
    )

    # 启动 pywebview 事件循环
    try:
        webview.start(debug=False)
    except Exception as e:
        print(f"[错误] 窗体启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
