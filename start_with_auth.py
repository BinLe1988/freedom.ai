#!/usr/bin/env python3
"""
启动带有用户认证系统的Freedom.AI Web应用
"""

import os
import sys
import subprocess

def main():
    """启动带认证的Web应用"""
    print("=== Freedom.AI 用户认证系统启动 ===")
    print("启动带有登录/注册功能的Web应用...")
    
    # 切换到web目录并运行app_with_auth.py
    try:
        os.chdir('web')
        subprocess.run([sys.executable, 'app_with_auth.py'])
    except KeyboardInterrupt:
        print("\n应用已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        print("请确保所有依赖已安装:")
        print("pip install flask")

if __name__ == "__main__":
    main()
