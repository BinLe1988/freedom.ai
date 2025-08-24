#!/usr/bin/env python3
"""
命令行用户注册和登录工具
Command Line User Registration and Login Tool
"""

import sys
import os
import getpass
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase
from user_system.simple_auth import SimpleAuthManager
from user_system.models import ActionType

class CLIAuth:
    """命令行认证工具"""
    
    def __init__(self):
        self.db = UserDatabase("./data")
        self.auth = SimpleAuthManager(self.db)
        self.current_user = None
        self.current_token = None
    
    def register(self):
        """用户注册"""
        print("=== Freedom.AI 用户注册 ===\n")
        
        # 获取用户输入
        username = input("请输入用户名 (至少3个字符): ").strip()
        if len(username) < 3:
            print("❌ 用户名至少需要3个字符")
            return False
        
        email = input("请输入邮箱地址: ").strip()
        if '@' not in email:
            print("❌ 请输入有效的邮箱地址")
            return False
        
        password = getpass.getpass("请输入密码 (至少6个字符): ")
        if len(password) < 6:
            print("❌ 密码至少需要6个字符")
            return False
        
        confirm_password = getpass.getpass("请确认密码: ")
        if password != confirm_password:
            print("❌ 密码不匹配")
            return False
        
        # 可选信息
        print("\n--- 可选信息 ---")
        full_name = input("真实姓名 (可选): ").strip()
        industry = input("所在行业 (可选): ").strip()
        
        # 执行注册
        result = self.auth.register_user(
            username=username,
            email=email,
            password=password
        )
        
        if result['success']:
            print(f"✅ 注册成功！用户ID: {result['user_id']}")
            
            # 更新用户档案
            if full_name or industry:
                self.db.update_user_profile(
                    result['user_id'],
                    full_name=full_name if full_name else None,
                    industry=industry if industry else None
                )
                print("✅ 用户档案已更新")
            
            return True
        else:
            print(f"❌ 注册失败: {result['error']}")
            return False
    
    def login(self):
        """用户登录"""
        print("=== Freedom.AI 用户登录 ===\n")
        
        username = input("用户名: ").strip()
        password = getpass.getpass("密码: ")
        
        result = self.auth.login_user(
            username=username,
            password=password,
            ip_address="127.0.0.1",
            user_agent="CLI Tool"
        )
        
        if result['success']:
            self.current_user = {
                'user_id': result['user_id'],
                'username': result['username'],
                'session_id': result['session_id']
            }
            self.current_token = result['access_token']
            
            print(f"✅ 登录成功！欢迎回来，{result['username']}！")
            print(f"会话ID: {result['session_id']}")
            return True
        else:
            print(f"❌ 登录失败: {result['error']}")
            return False
    
    def logout(self):
        """用户登出"""
        if not self.current_user:
            print("❌ 您还没有登录")
            return False
        
        result = self.auth.logout_user(
            self.current_user['session_id'],
            self.current_user['user_id']
        )
        
        if result['success']:
            print(f"✅ 再见，{self.current_user['username']}！")
            self.current_user = None
            self.current_token = None
            return True
        else:
            print(f"❌ 登出失败: {result['error']}")
            return False
    
    def show_profile(self):
        """显示用户档案"""
        if not self.current_user:
            print("❌ 请先登录")
            return
        
        user_id = self.current_user['user_id']
        
        # 获取用户信息
        user = self.db.get_user(user_id)
        profile = self.db.get_user_profile(user_id)
        preferences = self.db.get_user_preferences(user_id)
        
        print(f"\n=== {user.username} 的档案信息 ===")
        print(f"用户ID: {user.user_id}")
        print(f"邮箱: {user.email}")
        print(f"注册时间: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"最后登录: {user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '首次登录'}")
        print(f"状态: {user.status.value}")
        
        if profile:
            print(f"\n--- 个人信息 ---")
            if profile.full_name:
                print(f"姓名: {profile.full_name}")
            if profile.industry:
                print(f"行业: {profile.industry}")
            if profile.bio:
                print(f"简介: {profile.bio}")
            if profile.skills:
                print(f"技能: {', '.join(profile.skills)}")
        
        if preferences:
            print(f"\n--- 偏好设置 ---")
            if preferences.preferred_work_type:
                print(f"工作类型偏好: {preferences.preferred_work_type}")
            if preferences.learning_style:
                print(f"学习风格: {preferences.learning_style}")
    
    def update_profile(self):
        """更新用户档案"""
        if not self.current_user:
            print("❌ 请先登录")
            return
        
        print("\n=== 更新用户档案 ===")
        print("(直接回车跳过不修改的项目)")
        
        user_id = self.current_user['user_id']
        profile = self.db.get_user_profile(user_id)
        
        # 获取更新信息
        updates = {}
        
        full_name = input(f"姓名 [{profile.full_name if profile and profile.full_name else ''}]: ").strip()
        if full_name:
            updates['full_name'] = full_name
        
        bio = input(f"个人简介 [{profile.bio if profile and profile.bio else ''}]: ").strip()
        if bio:
            updates['bio'] = bio
        
        industry = input(f"所在行业 [{profile.industry if profile and profile.industry else ''}]: ").strip()
        if industry:
            updates['industry'] = industry
        
        skills_input = input("技能列表 (用逗号分隔): ").strip()
        if skills_input:
            updates['skills'] = [s.strip() for s in skills_input.split(',') if s.strip()]
        
        # 更新档案
        if updates:
            self.db.update_user_profile(user_id, **updates)
            
            # 记录更新行为
            self.db.log_user_action(
                user_id,
                ActionType.PREFERENCE_UPDATE,
                {'updated_fields': list(updates.keys())}
            )
            
            print("✅ 档案更新成功！")
        else:
            print("ℹ️  没有更新任何信息")
    
    def show_stats(self):
        """显示用户统计"""
        if not self.current_user:
            print("❌ 请先登录")
            return
        
        user_id = self.current_user['user_id']
        stats = self.db.get_user_statistics(user_id)
        
        print(f"\n=== {stats['username']} 的使用统计 ===")
        print(f"总行为数: {stats['total_actions']}")
        print(f"最近7天行为: {stats['recent_actions_7d']}")
        print(f"账户状态: {stats['status']}")
        
        # 行为分析
        behavior = stats.get('behavior_analysis', {})
        if behavior:
            feature_usage = behavior.get('feature_usage', {})
            if feature_usage:
                print(f"\n--- 功能使用情况 ---")
                for feature, count in feature_usage.get('feature_counts', {}).items():
                    print(f"{feature}: {count} 次")
    
    def interactive_menu(self):
        """交互式菜单"""
        while True:
            print("\n" + "="*50)
            print("Freedom.AI 用户系统")
            print("="*50)
            
            if self.current_user:
                print(f"当前用户: {self.current_user['username']}")
                print("1. 查看档案")
                print("2. 更新档案")
                print("3. 使用统计")
                print("4. 登出")
                print("0. 退出")
            else:
                print("1. 用户注册")
                print("2. 用户登录")
                print("0. 退出")
            
            choice = input("\n请选择操作 (0-4): ").strip()
            
            if choice == '0':
                if self.current_user:
                    self.logout()
                print("👋 再见！")
                break
            elif choice == '1':
                if self.current_user:
                    self.show_profile()
                else:
                    self.register()
            elif choice == '2':
                if self.current_user:
                    self.update_profile()
                else:
                    self.login()
            elif choice == '3' and self.current_user:
                self.show_stats()
            elif choice == '4' and self.current_user:
                self.logout()
            else:
                print("❌ 无效选择，请重试")

def main():
    """主函数"""
    cli_auth = CLIAuth()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'register':
            cli_auth.register()
        elif command == 'login':
            if cli_auth.login():
                cli_auth.show_profile()
        elif command == 'menu':
            cli_auth.interactive_menu()
        else:
            print("用法:")
            print("  python3 cli_auth.py register  # 注册新用户")
            print("  python3 cli_auth.py login     # 用户登录")
            print("  python3 cli_auth.py menu      # 交互式菜单")
    else:
        # 默认启动交互式菜单
        cli_auth.interactive_menu()

if __name__ == "__main__":
    main()
