#!/usr/bin/env python3
"""
快速测试注册页面
"""

import requests
import time
import subprocess
import sys
import os

def test_register_page():
    """测试注册页面是否可访问"""
    
    print("🧪 开始测试注册页面...")
    
    # 测试不同的URL
    test_urls = [
        "http://localhost:5001/register",
        "http://127.0.0.1:5001/register",
        "http://localhost:5001/",
        "http://127.0.0.1:5001/"
    ]
    
    for url in test_urls:
        try:
            print(f"📡 测试 {url}")
            response = requests.get(url, timeout=5)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ 成功访问")
                if "注册" in response.text or "register" in response.text.lower():
                    print(f"   ✅ 包含注册相关内容")
                else:
                    print(f"   ⚠️  未找到注册相关内容")
            elif response.status_code == 404:
                print(f"   ❌ 404 - 页面未找到")
            else:
                print(f"   ⚠️  其他状态码: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ 连接失败 - 服务器可能未启动")
        except requests.exceptions.Timeout:
            print(f"   ❌ 请求超时")
        except Exception as e:
            print(f"   ❌ 其他错误: {e}")
        
        print()

def check_app_status():
    """检查应用状态"""
    print("🔍 检查应用状态...")
    
    # 检查端口占用
    try:
        result = subprocess.run(['lsof', '-i', ':5001'], 
                              capture_output=True, text=True)
        if result.stdout:
            print("📍 端口5001占用情况:")
            print(result.stdout)
        else:
            print("❌ 端口5001未被占用 - 应用可能未启动")
    except Exception as e:
        print(f"❌ 检查端口失败: {e}")

if __name__ == '__main__':
    print("🚀 Freedom.AI 注册页面测试")
    print("=" * 50)
    
    check_app_status()
    print()
    test_register_page()
    
    print("💡 解决建议:")
    print("1. 确保应用已启动: python web/app_with_auth.py")
    print("2. 检查控制台是否有错误信息")
    print("3. 尝试访问首页: http://localhost:5001/")
    print("4. 检查浏览器网络面板的具体错误")
