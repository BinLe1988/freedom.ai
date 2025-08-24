#!/usr/bin/env python3
"""
Freedom.AI 数据库查询指南和工具
Database Query Guide and Tools
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase
from user_system.models import User, UserProfile, UserPreferences, ActionType

class DatabaseQueryTool:
    def __init__(self, data_dir="./data"):
        self.db = UserDatabase(data_dir)
        self.data_dir = data_dir
    
    def show_database_structure(self):
        """显示数据库结构"""
        print("=== Freedom.AI 数据库结构 ===")
        
        print("\n📁 数据文件:")
        files = [
            ("users.json", "用户基本信息"),
            ("user_profiles.json", "用户档案信息"),
            ("user_preferences.json", "用户偏好设置"),
            ("user_actions.json", "用户行为记录"),
            ("user_sessions.json", "用户会话信息")
        ]
        
        for filename, description in files:
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"✅ {filename:<20} - {description} ({size:,} bytes)")
            else:
                print(f"❌ {filename:<20} - {description} (不存在)")
    
    def show_query_methods(self):
        """显示查询方法"""
        print("\n=== 数据库查询方法 ===")
        
        methods = [
            ("用户查询", [
                "get_user(user_id) - 根据用户ID获取用户",
                "get_user_by_username(username) - 根据用户名获取用户",
                "get_user_by_email(email) - 根据邮箱获取用户"
            ]),
            ("档案查询", [
                "get_user_profile(user_id) - 获取用户档案",
                "get_user_preferences(user_id) - 获取用户偏好"
            ]),
            ("行为查询", [
                "get_user_actions(user_id, limit, action_type, start_date) - 获取用户行为",
                "analyze_user_behavior(user_id, days) - 分析用户行为"
            ]),
            ("统计查询", [
                "get_user_statistics(user_id) - 获取用户统计",
                "get_session(session_id) - 获取会话信息"
            ])
        ]
        
        for category, method_list in methods:
            print(f"\n📊 {category}:")
            for method in method_list:
                print(f"  • {method}")
    
    def query_users(self, limit=10):
        """查询用户列表"""
        print(f"\n=== 用户列表 (前{limit}个) ===")
        
        try:
            with open(os.path.join(self.data_dir, "users.json"), 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            count = 0
            for user_id, user_info in users_data.items():
                if count >= limit:
                    break
                
                print(f"\n👤 用户ID: {user_id}")
                print(f"   用户名: {user_info.get('username', 'N/A')}")
                print(f"   邮箱: {user_info.get('email', 'N/A')}")
                print(f"   状态: {user_info.get('status', 'N/A')}")
                print(f"   注册时间: {user_info.get('created_at', 'N/A')}")
                print(f"   最后登录: {user_info.get('last_login', 'N/A')}")
                
                count += 1
            
            print(f"\n📊 总用户数: {len(users_data)}")
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")
    
    def query_user_by_id(self, user_id: str):
        """根据ID查询用户详细信息"""
        print(f"\n=== 用户详细信息: {user_id} ===")
        
        try:
            # 基本信息
            user = self.db.get_user(user_id)
            if user:
                print(f"👤 基本信息:")
                print(f"   用户ID: {user.user_id}")
                print(f"   用户名: {user.username}")
                print(f"   邮箱: {user.email}")
                print(f"   状态: {user.status.value}")
                print(f"   注册时间: {user.created_at}")
                print(f"   最后登录: {user.last_login}")
            else:
                print("❌ 用户不存在")
                return
            
            # 档案信息
            profile = self.db.get_user_profile(user_id)
            if profile:
                print(f"\n📋 档案信息:")
                print(f"   姓名: {profile.full_name or 'N/A'}")
                print(f"   简介: {profile.bio or 'N/A'}")
                print(f"   位置: {profile.location or 'N/A'}")
                print(f"   职业: {profile.current_role or 'N/A'}")
                print(f"   经验: {profile.experience_years or 'N/A'} 年")
                print(f"   技能: {profile.skills or []}")
                print(f"   兴趣: {profile.interests or []}")
            
            # 偏好信息
            preferences = self.db.get_user_preferences(user_id)
            if preferences:
                print(f"\n⚙️ 偏好设置:")
                print(f"   工作类型: {preferences.preferred_work_type or 'N/A'}")
                print(f"   地点偏好: {preferences.location_preferences or []}")
                print(f"   行业偏好: {preferences.industry_preferences or []}")
                print(f"   公司规模: {preferences.company_size_preference or 'N/A'}")
                print(f"   薪资期望: {preferences.salary_expectations or 'N/A'}")
            
            # 统计信息
            stats = self.db.get_user_statistics(user_id)
            if stats:
                print(f"\n📊 统计信息:")
                print(f"   总操作数: {stats.get('total_actions', 0)}")
                print(f"   7天内操作: {stats.get('recent_actions_7d', 0)}")
                print(f"   行为分析: {len(stats.get('behavior_analysis', {}))}")
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")
    
    def query_user_actions(self, user_id: str, limit=20):
        """查询用户行为记录"""
        print(f"\n=== 用户行为记录: {user_id} (最近{limit}条) ===")
        
        try:
            actions = self.db.get_user_actions(user_id, limit=limit)
            
            if not actions:
                print("❌ 没有找到行为记录")
                return
            
            for i, action in enumerate(actions, 1):
                print(f"\n📝 行为 {i}:")
                print(f"   类型: {action.action_type.value}")
                print(f"   时间: {action.timestamp}")
                print(f"   详情: {action.details}")
                if action.session_id:
                    print(f"   会话: {action.session_id[:8]}...")
                if action.ip_address:
                    print(f"   IP: {action.ip_address}")
            
            print(f"\n📊 总记录数: {len(actions)}")
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")
    
    def query_statistics(self):
        """查询整体统计信息"""
        print("\n=== 整体统计信息 ===")
        
        try:
            # 用户统计
            with open(os.path.join(self.data_dir, "users.json"), 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            total_users = len(users_data)
            active_users = sum(1 for u in users_data.values() if u.get('status') == 'active')
            
            print(f"👥 用户统计:")
            print(f"   总用户数: {total_users}")
            print(f"   活跃用户: {active_users}")
            print(f"   活跃率: {active_users/total_users*100:.1f}%")
            
            # 档案统计
            with open(os.path.join(self.data_dir, "user_profiles.json"), 'r', encoding='utf-8') as f:
                profiles_data = json.load(f)
            
            total_profiles = len(profiles_data)
            completed_profiles = sum(1 for p in profiles_data.values() 
                                   if p.get('full_name') and p.get('bio'))
            
            print(f"\n📋 档案统计:")
            print(f"   总档案数: {total_profiles}")
            print(f"   完整档案: {completed_profiles}")
            print(f"   完成率: {completed_profiles/total_profiles*100:.1f}%")
            
            # 行为统计
            with open(os.path.join(self.data_dir, "user_actions.json"), 'r', encoding='utf-8') as f:
                actions_data = json.load(f)
            
            total_actions = len(actions_data)
            recent_actions = sum(1 for a in actions_data.values() 
                               if datetime.fromisoformat(a['timestamp']) > datetime.now() - timedelta(days=7))
            
            print(f"\n📊 行为统计:")
            print(f"   总行为数: {total_actions}")
            print(f"   7天内行为: {recent_actions}")
            
            # 行为类型统计
            action_types = {}
            for action in actions_data.values():
                action_type = action.get('action_type', 'unknown')
                action_types[action_type] = action_types.get(action_type, 0) + 1
            
            print(f"\n📈 行为类型分布:")
            for action_type, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True):
                print(f"   {action_type}: {count}")
            
        except Exception as e:
            print(f"❌ 统计失败: {e}")
    
    def search_users(self, keyword: str):
        """搜索用户"""
        print(f"\n=== 搜索用户: '{keyword}' ===")
        
        try:
            with open(os.path.join(self.data_dir, "users.json"), 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            results = []
            for user_id, user_info in users_data.items():
                if (keyword.lower() in user_info.get('username', '').lower() or
                    keyword.lower() in user_info.get('email', '').lower() or
                    keyword in user_id):
                    results.append((user_id, user_info))
            
            if results:
                print(f"找到 {len(results)} 个匹配结果:")
                for user_id, user_info in results:
                    print(f"\n👤 {user_info.get('username', 'N/A')} ({user_id[:8]}...)")
                    print(f"   邮箱: {user_info.get('email', 'N/A')}")
                    print(f"   状态: {user_info.get('status', 'N/A')}")
            else:
                print("❌ 没有找到匹配的用户")
                
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
    
    def export_data(self, user_id: str = None, output_file: str = None):
        """导出数据"""
        if user_id:
            print(f"\n=== 导出用户数据: {user_id} ===")
            try:
                data = self.db.export_user_data(user_id)
                
                if output_file:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                    print(f"✅ 数据已导出到: {output_file}")
                else:
                    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
                    
            except Exception as e:
                print(f"❌ 导出失败: {e}")
        else:
            print("❌ 请提供用户ID")
    
    def interactive_query(self):
        """交互式查询"""
        print("\n=== 交互式数据库查询 ===")
        print("输入 'help' 查看帮助，输入 'quit' 退出")
        
        while True:
            try:
                command = input("\n🔍 请输入查询命令: ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见!")
                    break
                elif command.lower() == 'help':
                    self.show_help()
                elif command.startswith('users'):
                    parts = command.split()
                    limit = int(parts[1]) if len(parts) > 1 else 10
                    self.query_users(limit)
                elif command.startswith('user '):
                    user_id = command.split(' ', 1)[1]
                    self.query_user_by_id(user_id)
                elif command.startswith('actions '):
                    parts = command.split()
                    user_id = parts[1]
                    limit = int(parts[2]) if len(parts) > 2 else 20
                    self.query_user_actions(user_id, limit)
                elif command.startswith('search '):
                    keyword = command.split(' ', 1)[1]
                    self.search_users(keyword)
                elif command == 'stats':
                    self.query_statistics()
                elif command.startswith('export '):
                    parts = command.split()
                    user_id = parts[1]
                    output_file = parts[2] if len(parts) > 2 else None
                    self.export_data(user_id, output_file)
                else:
                    print("❌ 未知命令，输入 'help' 查看帮助")
                    
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                print(f"❌ 执行错误: {e}")
    
    def show_help(self):
        """显示帮助信息"""
        print("\n📖 查询命令帮助:")
        print("=" * 50)
        
        commands = [
            ("users [数量]", "查询用户列表，可指定数量"),
            ("user <用户ID>", "查询指定用户的详细信息"),
            ("actions <用户ID> [数量]", "查询用户行为记录"),
            ("search <关键词>", "搜索用户"),
            ("stats", "查询整体统计信息"),
            ("export <用户ID> [文件名]", "导出用户数据"),
            ("help", "显示帮助信息"),
            ("quit", "退出程序")
        ]
        
        for command, description in commands:
            print(f"  {command:<25} - {description}")

def main():
    """主函数"""
    print("Freedom.AI 数据库查询工具")
    print("=" * 50)
    
    # 检查数据目录
    if not os.path.exists("./data"):
        print("❌ 数据目录不存在，请确保在项目根目录运行")
        return
    
    # 初始化查询工具
    query_tool = DatabaseQueryTool()
    
    # 显示数据库结构
    query_tool.show_database_structure()
    
    # 显示查询方法
    query_tool.show_query_methods()
    
    # 询问操作模式
    print("\n选择操作模式:")
    print("1. 交互式查询")
    print("2. 快速统计")
    print("3. 查看用户列表")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == '1':
        query_tool.interactive_query()
    elif choice == '2':
        query_tool.query_statistics()
    elif choice == '3':
        query_tool.query_users()
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()
