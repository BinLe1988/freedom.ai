#!/usr/bin/env python3
"""
测试登录功能
Test Login Functionality
"""

import os
import sys
import requests
import json

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase
from user_system.auth import AuthManager

def test_database_login():
    """测试数据库登录功能"""
    print("🔐 测试数据库登录功能...")
    
    db = UserDatabase("./data")
    
    # 测试账号
    test_accounts = [
        ("test@example.com", "123456"),
        ("admin@freedom.ai", "admin123"),
        ("demo@freedom.ai", "demo123"),
        ("test", "123456"),  # 用户名登录
        ("admin", "admin123")  # 用户名登录
    ]
    
    for username, password in test_accounts:
        print(f"\n测试登录: {username}")
        user = db.authenticate_user(username, password)
        
        if user:
            print(f"✅ 登录成功!")
            print(f"   用户ID: {user.user_id}")
            print(f"   用户名: {user.username}")
            print(f"   邮箱: {user.email}")
        else:
            print(f"❌ 登录失败")

def test_auth_manager():
    """测试认证管理器"""
    print("\n🔑 测试认证管理器...")
    
    auth_manager = AuthManager("./data")
    
    test_accounts = [
        ("test@example.com", "123456"),
        ("admin@freedom.ai", "admin123"),
        ("demo@freedom.ai", "demo123")
    ]
    
    for username, password in test_accounts:
        print(f"\n测试认证: {username}")
        result = auth_manager.login_user(username, password, "127.0.0.1", "Test-Agent")
        
        if result['success']:
            print(f"✅ 认证成功!")
            print(f"   用户ID: {result['user_id']}")
            print(f"   用户名: {result['username']}")
            print(f"   会话ID: {result['session_id']}")
            print(f"   访问令牌: {result['access_token'][:20]}...")
        else:
            print(f"❌ 认证失败: {result['error']}")

def test_api_login():
    """测试API登录"""
    print("\n🌐 测试API登录...")
    
    # 检查后端是否运行
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        print("✅ 后端服务器运行中")
    except:
        print("❌ 后端服务器未运行，请先启动: python3 web/app_with_auth.py")
        return
    
    test_accounts = [
        ("test@example.com", "123456"),
        ("admin@freedom.ai", "admin123"),
        ("demo@freedom.ai", "demo123")
    ]
    
    for email, password in test_accounts:
        print(f"\n测试API登录: {email}")
        
        try:
            response = requests.post(
                "http://localhost:5000/login",
                json={"username": email, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ API登录成功!")
                    print(f"   用户ID: {data.get('user_id')}")
                    print(f"   用户名: {data.get('username')}")
                    print(f"   会话ID: {data.get('session_id')}")
                else:
                    print(f"❌ API登录失败: {data.get('error')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")

def create_test_user_if_not_exists():
    """如果测试用户不存在则创建"""
    print("👤 检查测试用户...")
    
    db = UserDatabase("./data")
    
    # 检查test用户是否存在
    test_user = db.get_user_by_email("test@example.com")
    if not test_user:
        print("创建test用户...")
        from user_manager import UserManager
        manager = UserManager()
        manager.create_test_user("test", "test@example.com", "123456")
    else:
        print("✅ test用户已存在")
    
    # 检查admin用户是否存在
    admin_user = db.get_user_by_email("admin@freedom.ai")
    if not admin_user:
        print("创建admin用户...")
        from user_manager import UserManager
        manager = UserManager()
        manager.create_test_user("admin", "admin@freedom.ai", "admin123")
    else:
        print("✅ admin用户已存在")

def main():
    print("Freedom.AI 登录功能测试")
    print("=" * 50)
    
    # 检查数据目录
    if not os.path.exists("./data"):
        print("❌ 数据目录不存在")
        return
    
    # 确保测试用户存在
    create_test_user_if_not_exists()
    
    # 运行测试
    test_database_login()
    test_auth_manager()
    
    print("\n" + "=" * 50)
    print("📝 测试建议:")
    print("1. 如果数据库测试通过但API测试失败，请检查后端服务器")
    print("2. 如果所有测试都失败，请检查用户数据和密码")
    print("3. 前端登录应该使用邮箱地址作为用户名")
    
    # 询问是否测试API
    choice = input("\n是否测试API登录? (需要后端运行) (y/n): ").strip().lower()
    if choice == 'y':
        test_api_login()

if __name__ == "__main__":
    main()
