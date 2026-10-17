"""
图书管理系统 - 后端服务入口
"""

import sys

# Windows 控制台默认 GBK，重设为 UTF-8 避免中文/emoji 打印崩溃
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from app.models import init_database
from app.routes import start_server

if __name__ == "__main__":
    print("=" * 50)
    print("  图书管理系统 - 原子能力API服务")
    print("=" * 50)

    # 初始化数据库
    print("\n[init] 正在初始化数据库...")
    init_database()
    print("[init] 数据库初始化完成\n")

    # 启动服务（端口 8001，避开被外部服务占用的 8000）
    start_server(port=8001)
