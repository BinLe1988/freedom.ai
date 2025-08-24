#!/usr/bin/env python3
"""
Freedom.AI 用户管理工具
User Management Tool
"""

import os
import sys
import json
import hashlib
import secrets
from datetime import datetime
from pathlib import Path

# 添加路径
sys.path.append(os.path.dirname(__file__))

try:
    from database.user_db import UserDatabase
    from user_system.models import User, UserStatus
except ImportError:
    print("⚠️  无法导入数据库模块，将使用简化版本")
    UserDatabase = None

class UserManager:
    def __init__(self, data_dir="./data"):
        self.data_dir = Path(data_dir)
        self.users_file = self.data_dir / "users.json"
        
        if UserDatabase:
            self.db = UserDatabase(data_dir)
        else:
            self.db = None
    
    def load_users(self):
        """加载用户数据"""
        if not self.users_file.exists():
            return {}
        
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载用户数据失败: {e}")
            return {}
    
    def save_users(self, users_data):
        """保存用户数据"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"❌ 保存用户数据失败: {e}")
            return False
    
    def hash_password(self, password):
        """密码哈希"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{password_hash}:{salt}"
    
    def verify_password(self, password, password_hash):
        """验证密码"""
        try:
            hash_part, salt = password_hash.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
        except:
            return False
    
    def list_users(self):
        """列出所有用户"""
        print("👥 用户列表:")
        print("=" * 80)
        
        users_data = self.load_users()
        
        if not users_data:
            print("❌ 没有找到用户数据")
            return
        
        print(f"{'序号':<4} {'用户名':<20} {'邮箱':<30} {'状态':<8} {'最后登录':<20}")
        print("-" * 80)
        
        for i, (user_id, user_info) in enumerate(users_data.items(), 1):
            username = user_info.get('username', 'N/A')
            email = user_info.get('email', 'N/A')
            status = user_info.get('status', 'unknown')
            last_login = user_info.get('last_login') or 'Never'
            
            if last_login and last_login != 'Never':
                try:
                    last_login = datetime.fromisoformat(last_login).strftime('%Y-%m-%d %H:%M')
                except:
                    last_login = 'Invalid'
            
            print(f"{i:<4} {username:<20} {email:<30} {status:<8} {last_login:<20}")
        
        print(f"\n📊 总用户数: {len(users_data)}")
    
    def create_test_user(self, username="test", email="test@example.com", password="123456"):
        """创建测试用户"""
        print(f"👤 创建测试用户: {username}")
        
        users_data = self.load_users()
        
        # 检查用户名是否已存在
        for user_info in users_data.values():
            if user_info.get('username') == username:
                print(f"❌ 用户名 '{username}' 已存在")
                return False
            if user_info.get('email') == email:
                print(f"❌ 邮箱 '{email}' 已存在")
                return False
        
        # 生成用户ID
        user_id = f"user_{secrets.token_hex(6)}"
        
        # 创建用户数据
        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "password_hash": self.hash_password(password),
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "status": "active",
            "profile": {},
            "preferences": {
                "language": "zh-CN",
                "timezone": "Asia/Shanghai",
                "email_notifications": True,
                "data_sharing": True,
                "theme": "dark",
                "dashboard_layout": "default",
                "auto_save": True,
                "privacy_level": "medium"
            }
        }
        
        users_data[user_id] = user_data
        
        if self.save_users(users_data):
            print(f"✅ 用户创建成功!")
            print(f"   用户ID: {user_id}")
            print(f"   用户名: {username}")
            print(f"   邮箱: {email}")
            print(f"   密码: {password}")
            return True
        else:
            return False
    
    def reset_password(self, username, new_password):
        """重置用户密码"""
        print(f"🔑 重置用户密码: {username}")
        
        users_data = self.load_users()
        
        # 查找用户
        target_user_id = None
        for user_id, user_info in users_data.items():
            if user_info.get('username') == username:
                target_user_id = user_id
                break
        
        if not target_user_id:
            print(f"❌ 用户 '{username}' 不存在")
            return False
        
        # 更新密码
        users_data[target_user_id]['password_hash'] = self.hash_password(new_password)
        
        if self.save_users(users_data):
            print(f"✅ 密码重置成功!")
            print(f"   用户名: {username}")
            print(f"   新密码: {new_password}")
            return True
        else:
            return False
    
    def verify_login(self, username, password):
        """验证登录"""
        print(f"🔐 验证登录: {username}")
        
        users_data = self.load_users()
        
        # 查找用户
        for user_id, user_info in users_data.items():
            if user_info.get('username') == username or user_info.get('email') == username:
                if self.verify_password(password, user_info.get('password_hash', '')):
                    print(f"✅ 登录验证成功!")
                    print(f"   用户ID: {user_id}")
                    print(f"   用户名: {user_info.get('username')}")
                    print(f"   邮箱: {user_info.get('email')}")
                    return True
                else:
                    print(f"❌ 密码错误")
                    return False
        
        print(f"❌ 用户不存在")
        return False
    
    def show_default_accounts(self):
        """显示默认测试账号"""
        print("🔑 默认测试账号:")
        print("=" * 50)
        
        default_accounts = [
            {
                "username": "admin",
                "email": "admin@freedom.ai",
                "password": "admin123",
                "description": "管理员账号"
            },
            {
                "username": "test",
                "email": "test@example.com", 
                "password": "123456",
                "description": "测试用户账号"
            },
            {
                "username": "demo",
                "email": "demo@freedom.ai",
                "password": "demo123",
                "description": "演示账号"
            }
        ]
        
        for account in default_accounts:
            print(f"👤 {account['description']}")
            print(f"   用户名: {account['username']}")
            print(f"   邮箱: {account['email']}")
            print(f"   密码: {account['password']}")
            print()
    
    def create_default_accounts(self):
        """创建默认测试账号"""
        print("🚀 创建默认测试账号...")
        
        accounts = [
            ("admin", "admin@freedom.ai", "admin123"),
            ("test", "test@example.com", "123456"),
            ("demo", "demo@freedom.ai", "demo123")
        ]
        
        success_count = 0
        
        for username, email, password in accounts:
            if self.create_test_user(username, email, password):
                success_count += 1
            print()
        
        print(f"✅ 成功创建 {success_count}/{len(accounts)} 个账号")
    
    def interactive_menu(self):
        """交互式菜单"""
        while True:
            print("\n" + "=" * 50)
            print("Freedom.AI 用户管理工具")
            print("=" * 50)
            
            print("1. 查看所有用户")
            print("2. 创建测试用户")
            print("3. 重置用户密码")
            print("4. 验证登录")
            print("5. 显示默认测试账号")
            print("6. 创建默认测试账号")
            print("7. 退出")
            
            choice = input("\n请选择操作 (1-7): ").strip()
            
            if choice == '1':
                self.list_users()
            elif choice == '2':
                username = input("输入用户名: ").strip()
                email = input("输入邮箱: ").strip()
                password = input("输入密码: ").strip()
                if username and email and password:
                    self.create_test_user(username, email, password)
                else:
                    print("❌ 请输入完整信息")
            elif choice == '3':
                username = input("输入用户名: ").strip()
                password = input("输入新密码: ").strip()
                if username and password:
                    self.reset_password(username, password)
                else:
                    print("❌ 请输入完整信息")
            elif choice == '4':
                username = input("输入用户名或邮箱: ").strip()
                password = input("输入密码: ").strip()
                if username and password:
                    self.verify_login(username, password)
                else:
                    print("❌ 请输入完整信息")
            elif choice == '5':
                self.show_default_accounts()
            elif choice == '6':
                self.create_default_accounts()
            elif choice == '7':
                print("👋 再见!")
                break
            else:
                print("❌ 无效选择")

def main():
    print("Freedom.AI 用户管理工具")
    print("=" * 50)
    
    # 检查数据目录
    if not Path("./data").exists():
        print("❌ 数据目录不存在，请确保在项目根目录运行")
        return
    
    manager = UserManager()
    
    # 显示现有用户
    manager.list_users()
    
    # 显示默认账号信息
    print("\n")
    manager.show_default_accounts()
    
    # 询问是否进入交互模式
    choice = input("\n是否进入交互式管理模式? (y/n): ").strip().lower()
    
    if choice == 'y':
        manager.interactive_menu()
    else:
        print("\n💡 快速创建测试账号:")
        print("python3 user_manager.py")

if __name__ == "__main__":
    main()
