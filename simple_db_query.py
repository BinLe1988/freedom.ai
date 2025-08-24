#!/usr/bin/env python3
"""
简单的数据库查询示例
Simple Database Query Examples
"""

import os
import sys
import json
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase

def simple_queries():
    """简单查询示例"""
    print("=== Freedom.AI 数据库查询示例 ===")
    
    # 初始化数据库
    db = UserDatabase("./data")
    
    # 1. 查询所有用户
    print("\n1. 查询用户列表:")
    try:
        with open("./data/users.json", 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        print(f"总用户数: {len(users_data)}")
        
        # 显示前5个用户
        count = 0
        for user_id, user_info in users_data.items():
            if count >= 5:
                break
            print(f"  • {user_info['username']} ({user_id[:8]}...)")
            count += 1
            
    except Exception as e:
        print(f"查询失败: {e}")
    
    # 2. 查询特定用户
    print("\n2. 查询特定用户:")
    try:
        # 获取第一个用户ID
        with open("./data/users.json", 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        if users_data:
            user_id = list(users_data.keys())[0]
            user = db.get_user(user_id)
            
            if user:
                print(f"用户ID: {user.user_id}")
                print(f"用户名: {user.username}")
                print(f"邮箱: {user.email}")
                print(f"状态: {user.status.value}")
                print(f"注册时间: {user.created_at}")
        
    except Exception as e:
        print(f"查询失败: {e}")
    
    # 3. 查询用户档案
    print("\n3. 查询用户档案:")
    try:
        if users_data:
            user_id = list(users_data.keys())[0]
            profile = db.get_user_profile(user_id)
            
            if profile:
                print(f"姓名: {profile.full_name or '未设置'}")
                print(f"简介: {profile.bio or '未设置'}")
                print(f"位置: {profile.location or '未设置'}")
                print(f"技能: {profile.skills or []}")
            else:
                print("该用户没有档案信息")
        
    except Exception as e:
        print(f"查询失败: {e}")
    
    # 4. 查询用户偏好
    print("\n4. 查询用户偏好:")
    try:
        if users_data:
            user_id = list(users_data.keys())[0]
            preferences = db.get_user_preferences(user_id)
            
            if preferences:
                print(f"工作类型偏好: {preferences.preferred_work_type or '未设置'}")
                print(f"地点偏好: {preferences.location_preferences or []}")
                print(f"行业偏好: {preferences.industry_preferences or []}")
            else:
                print("该用户没有偏好设置")
        
    except Exception as e:
        print(f"查询失败: {e}")
    
    # 5. 查询用户行为
    print("\n5. 查询用户行为 (最近5条):")
    try:
        if users_data:
            user_id = list(users_data.keys())[0]
            actions = db.get_user_actions(user_id, limit=5)
            
            if actions:
                for i, action in enumerate(actions, 1):
                    print(f"  {i}. {action.action_type.value} - {action.timestamp}")
            else:
                print("该用户没有行为记录")
        
    except Exception as e:
        print(f"查询失败: {e}")
    
    # 6. 统计信息
    print("\n6. 统计信息:")
    try:
        if users_data:
            user_id = list(users_data.keys())[0]
            stats = db.get_user_statistics(user_id)
            
            if stats:
                print(f"总操作数: {stats.get('total_actions', 0)}")
                print(f"7天内操作: {stats.get('recent_actions_7d', 0)}")
        
    except Exception as e:
        print(f"查询失败: {e}")

def direct_json_queries():
    """直接JSON文件查询示例"""
    print("\n=== 直接JSON文件查询 ===")
    
    # 查询用户数据
    print("\n📊 用户数据统计:")
    try:
        with open("./data/users.json", 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        total = len(users)
        active = sum(1 for u in users.values() if u.get('status') == 'active')
        
        print(f"总用户数: {total}")
        print(f"活跃用户: {active}")
        print(f"活跃率: {active/total*100:.1f}%")
        
    except Exception as e:
        print(f"查询失败: {e}")
    
    # 查询档案完成情况
    print("\n📋 档案完成情况:")
    try:
        with open("./data/user_profiles.json", 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        
        total = len(profiles)
        completed = sum(1 for p in profiles.values() 
                       if p.get('full_name') and p.get('bio'))
        
        print(f"总档案数: {total}")
        print(f"完整档案: {completed}")
        print(f"完成率: {completed/total*100:.1f}%")
        
    except Exception as e:
        print(f"查询失败: {e}")
    
    # 查询行为类型分布
    print("\n📈 行为类型分布:")
    try:
        with open("./data/user_actions.json", 'r', encoding='utf-8') as f:
            actions = json.load(f)
        
        action_types = {}
        for action in actions.values():
            action_type = action.get('action_type', 'unknown')
            action_types[action_type] = action_types.get(action_type, 0) + 1
        
        # 按数量排序
        for action_type, count in sorted(action_types.items(), 
                                       key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {action_type}: {count}")
        
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    simple_queries()
    direct_json_queries()
