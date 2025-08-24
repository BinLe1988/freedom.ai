#!/usr/bin/env python3
"""
基础登录测试
Basic Login Test
"""

import os
import sys
import json

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase

def test_basic_login():
    """测试基础登录功能"""
    print("🔐 测试基础登录功能...")
    
    db = UserDatabase("./data")
    
    # 测试账号
    test_accounts = [
        ("test@example.com", "123456", "测试邮箱"),
        ("admin@freedom.ai", "admin123", "管理员邮箱"),
        ("demo@freedom.ai", "demo123", "演示邮箱"),
        ("test", "123456", "测试用户名"),
        ("admin", "admin123", "管理员用户名")
    ]
    
    success_count = 0
    
    for username, password, desc in test_accounts:
        print(f"\n测试 {desc}: {username}")
        user = db.authenticate_user(username, password)
        
        if user:
            print(f"✅ 认证成功!")
            print(f"   用户ID: {user.user_id}")
            print(f"   用户名: {user.username}")
            print(f"   邮箱: {user.email}")
            success_count += 1
        else:
            print(f"❌ 认证失败")
    
    print(f"\n📊 测试结果: {success_count}/{len(test_accounts)} 成功")
    
    if success_count > 0:
        print("✅ 基础登录功能正常")
    else:
        print("❌ 基础登录功能异常")
    
    return success_count > 0

def check_user_data():
    """检查用户数据"""
    print("\n👥 检查用户数据...")
    
    try:
        with open("./data/users.json", 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        print(f"📊 总用户数: {len(users_data)}")
        
        # 查找关键用户
        key_emails = ["test@example.com", "admin@freedom.ai", "demo@freedom.ai"]
        found_users = []
        
        for user_id, user_info in users_data.items():
            email = user_info.get('email')
            username = user_info.get('username')
            
            if email in key_emails:
                found_users.append((username, email))
                print(f"✅ 找到用户: {username} ({email})")
        
        if len(found_users) >= 2:
            print("✅ 关键测试用户存在")
            return True
        else:
            print("❌ 缺少关键测试用户")
            return False
            
    except Exception as e:
        print(f"❌ 读取用户数据失败: {e}")
        return False

def create_missing_users():
    """创建缺失的用户"""
    print("\n👤 创建缺失的测试用户...")
    
    try:
        from user_manager import UserManager
        manager = UserManager()
        
        # 检查并创建关键用户
        test_accounts = [
            ("test", "test@example.com", "123456"),
            ("admin", "admin@freedom.ai", "admin123"),
            ("demo", "demo@freedom.ai", "demo123")
        ]
        
        created_count = 0
        
        for username, email, password in test_accounts:
            # 检查用户是否已存在
            db = UserDatabase("./data")
            existing_user = db.get_user_by_email(email)
            
            if not existing_user:
                print(f"创建用户: {username}")
                if manager.create_test_user(username, email, password):
                    created_count += 1
            else:
                print(f"✅ 用户已存在: {username}")
        
        if created_count > 0:
            print(f"✅ 创建了 {created_count} 个用户")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return False

def show_frontend_fix():
    """显示前端修复信息"""
    print("\n🔧 前端登录修复信息:")
    print("=" * 50)
    
    print("✅ 已修复的问题:")
    print("1. 前端API路径: /auth/login → /login")
    print("2. 参数格式: {email, password} → {username: email, password}")
    print("3. 后端支持邮箱登录")
    print("4. 响应数据格式匹配")
    
    print("\n📝 使用说明:")
    print("1. 在登录页面的邮箱字段输入: test@example.com")
    print("2. 在密码字段输入: 123456")
    print("3. 点击登录按钮")
    
    print("\n🌐 测试地址:")
    print("- Next.js前端: http://localhost:3000/login")
    print("- Flask后端: http://localhost:5000/login")
    
    print("\n🔍 调试方法:")
    print("1. 打开浏览器开发者工具")
    print("2. 查看Network标签页的API请求")
    print("3. 查看Console标签页的错误信息")

def main():
    print("Freedom.AI 基础登录测试")
    print("=" * 50)
    
    # 检查数据目录
    if not os.path.exists("./data"):
        print("❌ 数据目录不存在")
        return
    
    # 检查用户数据
    if not check_user_data():
        print("\n尝试创建测试用户...")
        create_missing_users()
    
    # 测试登录
    if test_basic_login():
        print("\n🎉 登录功能测试通过!")
        show_frontend_fix()
    else:
        print("\n❌ 登录功能测试失败")
        print("请检查用户数据和密码设置")

if __name__ == "__main__":
    main()
