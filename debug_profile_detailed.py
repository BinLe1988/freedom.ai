#!/usr/bin/env python3
"""
详细调试档案更新问题
Detailed Debug for Profile Update Issues
"""

import os
import sys
import json
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase

def debug_profile_update():
    """详细调试档案更新"""
    print("=== 详细档案更新调试 ===")
    
    # 初始化数据库
    db = UserDatabase("./data")
    
    # 获取测试用户
    with open("./data/users.json", 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    user_id = list(users_data.keys())[0]
    print(f"测试用户ID: {user_id}")
    
    # 检查档案文件内容
    print("\n1. 检查档案文件内容:")
    try:
        with open("./data/user_profiles.json", 'r', encoding='utf-8') as f:
            profiles_data = json.load(f)
        
        print(f"档案文件中的用户数量: {len(profiles_data)}")
        print(f"用户ID {user_id} 是否存在: {user_id in profiles_data}")
        
        if user_id in profiles_data:
            print(f"现有档案数据: {profiles_data[user_id]}")
        else:
            print("用户档案不存在，需要先创建")
            
    except Exception as e:
        print(f"读取档案文件失败: {e}")
    
    # 测试创建档案
    print("\n2. 测试创建档案:")
    try:
        # 先创建档案
        profile = db.create_user_profile(
            user_id=user_id,
            full_name="测试用户档案",
            bio="初始档案",
            location="测试地点"
        )
        print(f"✓ 档案创建成功: {profile.full_name}")
        
    except Exception as e:
        print(f"档案创建失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 再次测试更新
    print("\n3. 测试档案更新:")
    try:
        test_data = {
            'full_name': f'更新用户_{datetime.now().strftime("%H%M%S")}',
            'bio': '这是更新后的简介',
            'location': '更新后的城市',
            'industry': '更新后的行业',
            'current_role': '更新后的职位',
            'experience_years': 8,
            'skills': ['Python', 'AI', 'Web开发'],
            'interests': ['技术', '创业', '旅行']
        }
        
        print(f"准备更新数据: {test_data}")
        
        # 执行更新
        success = db.update_user_profile(user_id, **test_data)
        print(f"更新结果: {'成功' if success else '失败'}")
        
        if success:
            # 验证更新
            updated_profile = db.get_user_profile(user_id)
            print(f"✓ 更新后档案: {updated_profile.full_name}")
            print(f"✓ 技能: {updated_profile.skills}")
            print(f"✓ 兴趣: {updated_profile.interests}")
        
    except Exception as e:
        print(f"档案更新失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 检查更新后的文件内容
    print("\n4. 检查更新后的文件内容:")
    try:
        with open("./data/user_profiles.json", 'r', encoding='utf-8') as f:
            profiles_data = json.load(f)
        
        if user_id in profiles_data:
            print(f"更新后的档案数据: {json.dumps(profiles_data[user_id], indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"读取更新后文件失败: {e}")

def debug_update_method():
    """调试更新方法本身"""
    print("\n=== 调试更新方法 ===")
    
    # 直接测试数据库方法
    db = UserDatabase("./data")
    
    # 获取用户ID
    with open("./data/users.json", 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    user_id = list(users_data.keys())[0]
    
    print(f"测试用户ID: {user_id}")
    
    # 检查update_user_profile方法的逻辑
    print("\n检查update_user_profile方法:")
    
    # 加载档案数据
    profiles_data = db._load_data(db.profiles_file)
    print(f"档案文件路径: {db.profiles_file}")
    print(f"用户是否在档案中: {user_id in profiles_data}")
    
    if user_id not in profiles_data:
        print("用户不在档案中，update_user_profile会返回False")
        print("需要先调用create_user_profile创建档案")
        
        # 创建档案
        try:
            profile = db.create_user_profile(user_id, full_name="测试档案")
            print(f"✓ 档案创建成功: {profile}")
        except Exception as e:
            print(f"✗ 档案创建失败: {e}")
    
    # 现在测试更新
    try:
        success = db.update_user_profile(user_id, full_name="更新测试", bio="测试更新")
        print(f"更新结果: {success}")
        
        if success:
            profile = db.get_user_profile(user_id)
            print(f"更新后档案: {profile.full_name}")
    except Exception as e:
        print(f"更新失败: {e}")

if __name__ == "__main__":
    debug_profile_update()
    debug_update_method()
