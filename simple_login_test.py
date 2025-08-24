#!/usr/bin/env python3
"""
简单登录测试
Simple Login Test
"""

import os
import sys

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase
from user_system.auth import AuthManager

def test_login():
    """测试登录功能"""
    print("🔐 测试登录功能...")
    
    db = UserDatabase("./data")
    auth_manager = AuthManager("./data")
    
    # 测试账号
    test_accounts = [
        ("test@example.com", "123456", "邮箱登录"),
        ("admin@freedom.ai", "admin123", "管理员邮箱"),
        ("demo@freedom.ai", "demo123", "演示邮箱"),
        ("test", "123456", "用户名登录"),
        ("admin", "admin123", "管理员用户名")
    ]
    
    print("\n=== 数据库认证测试 ===")
    for username, password, desc in test_accounts:
        print(f"\n测试 {desc}: {username}")
        user = db.authenticate_user(username, password)
        
        if user:
            print(f"✅ 数据库认证成功!")
            print(f"   用户ID: {user.user_id}")
            print(f"   用户名: {user.username}")
            print(f"   邮箱: {user.email}")
        else:
            print(f"❌ 数据库认证失败")
    
    print("\n=== 认证管理器测试 ===")
    for username, password, desc in test_accounts[:3]:  # 只测试邮箱登录
        print(f"\n测试 {desc}: {username}")
        result = auth_manager.login_user(username, password, "127.0.0.1", "Test-Agent")
        
        if result['success']:
            print(f"✅ 认证管理器成功!")
            print(f"   用户ID: {result['user_id']}")
            print(f"   用户名: {result['username']}")
            print(f"   会话ID: {result['session_id']}")
        else:
            print(f"❌ 认证管理器失败: {result['error']}")

def check_users():
    """检查用户数据"""
    print("\n👥 检查用户数据...")
    
    db = UserDatabase("./data")
    
    # 检查关键用户
    key_users = [
        ("test", "test@example.com"),
        ("admin", "admin@freedom.ai"),
        ("demo", "demo@freedom.ai")
    ]
    
    for username, email in key_users:
        print(f"\n检查用户: {username}")
        
        # 通过用户名查找
        user_by_name = db.get_user_by_username(username)
        if user_by_name:
            print(f"✅ 用户名查找成功: {user_by_name.username}")
        else:
            print(f"❌ 用户名查找失败")
        
        # 通过邮箱查找
        user_by_email = db.get_user_by_email(email)
        if user_by_email:
            print(f"✅ 邮箱查找成功: {user_by_email.email}")
        else:
            print(f"❌ 邮箱查找失败")

def show_login_info():
    """显示登录信息"""
    print("\n🔑 登录信息总结:")
    print("=" * 50)
    
    print("📧 推荐使用邮箱登录:")
    print("   邮箱: test@example.com")
    print("   密码: 123456")
    
    print("\n👤 或使用用户名登录:")
    print("   用户名: test")
    print("   密码: 123456")
    
    print("\n🌐 前端登录地址:")
    print("   http://localhost:3000/login")
    
    print("\n🔧 后端登录地址:")
    print("   http://localhost:5000/login")
    
    print("\n💡 如果登录失败:")
    print("1. 确保使用正确的邮箱地址")
    print("2. 确保后端服务器正在运行")
    print("3. 检查浏览器控制台的错误信息")
    print("4. 尝试清除浏览器缓存")

def main():
    print("Freedom.AI 简单登录测试")
    print("=" * 50)
    
    # 检查数据目录
    if not os.path.exists("./data"):
        print("❌ 数据目录不存在")
        return
    
    # 运行测试
    check_users()
    test_login()
    show_login_info()

if __name__ == "__main__":
    main()
