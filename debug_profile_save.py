#!/usr/bin/env python3
"""
调试档案保存功能
Debug Profile Save Functionality
"""

import os
import sys
import json
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase

def test_profile_save():
    """测试档案保存功能"""
    print("=== 档案保存功能调试 ===")
    
    # 初始化数据库
    db = UserDatabase("./data")
    
    # 检查数据文件
    print("\n1. 检查数据文件:")
    data_files = [
        "./data/users.json",
        "./data/user_profiles.json", 
        "./data/user_preferences.json"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} 存在 (大小: {size} bytes)")
        else:
            print(f"✗ {file_path} 不存在")
    
    # 获取第一个用户进行测试
    print("\n2. 获取测试用户:")
    try:
        with open("./data/users.json", 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        if not users_data:
            print("✗ 没有找到用户数据")
            return
        
        user_id = list(users_data.keys())[0]
        user_info = users_data[user_id]
        print(f"✓ 找到测试用户: {user_info['username']} (ID: {user_id})")
        
    except Exception as e:
        print(f"✗ 读取用户数据失败: {e}")
        return
    
    # 测试档案更新
    print("\n3. 测试档案更新:")
    try:
        # 获取当前档案
        current_profile = db.get_user_profile(user_id)
        print(f"✓ 当前档案: {current_profile.full_name if current_profile else '无档案'}")
        
        # 更新档案
        test_data = {
            'full_name': f'测试用户_{datetime.now().strftime("%H%M%S")}',
            'bio': '这是一个测试更新',
            'location': '测试城市',
            'industry': '测试行业',
            'current_role': '测试职位',
            'experience_years': 5,
            'skills': ['Python', 'JavaScript', 'AI'],
            'interests': ['编程', '人工智能', '自由职业']
        }
        
        print(f"准备更新数据: {test_data}")
        
        # 执行更新
        success = db.update_user_profile(user_id, **test_data)
        print(f"更新结果: {'成功' if success else '失败'}")
        
        if success:
            # 验证更新
            updated_profile = db.get_user_profile(user_id)
            print(f"✓ 更新后档案: {updated_profile.full_name}")
            print(f"✓ 更新时间: {updated_profile.updated_at}")
        
    except Exception as e:
        print(f"✗ 档案更新失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试偏好更新
    print("\n4. 测试偏好更新:")
    try:
        # 获取当前偏好
        current_preferences = db.get_user_preferences(user_id)
        print(f"✓ 当前偏好: {current_preferences.preferred_work_type if current_preferences else '无偏好'}")
        
        # 更新偏好
        pref_data = {
            'preferred_work_type': 'remote',
            'company_size_preference': 'startup',
            'salary_expectations': {'min': 10000, 'max': 20000, 'currency': 'CNY'},
            'location_preferences': ['北京', '上海'],
            'industry_preferences': ['科技', 'AI']
        }
        
        print(f"准备更新偏好: {pref_data}")
        
        # 执行更新
        success = db.update_user_preferences(user_id, **pref_data)
        print(f"偏好更新结果: {'成功' if success else '失败'}")
        
        if success:
            # 验证更新
            updated_preferences = db.get_user_preferences(user_id)
            print(f"✓ 更新后偏好: {updated_preferences.preferred_work_type}")
            print(f"✓ 更新时间: {updated_preferences.updated_at}")
        
    except Exception as e:
        print(f"✗ 偏好更新失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 检查文件权限
    print("\n5. 检查文件权限:")
    for file_path in data_files:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            permissions = oct(stat.st_mode)[-3:]
            print(f"✓ {file_path} 权限: {permissions}")
            
            # 测试写入权限
            try:
                with open(file_path, 'a') as f:
                    pass
                print(f"✓ {file_path} 可写")
            except Exception as e:
                print(f"✗ {file_path} 不可写: {e}")

def check_web_api():
    """检查Web API"""
    print("\n=== Web API 检查 ===")
    
    try:
        import requests
        
        # 测试API端点
        test_url = "http://localhost:5000/api/update_profile"
        print(f"测试URL: {test_url}")
        
        # 注意：这需要服务器运行和用户登录
        print("注意: 需要启动Web服务器并登录用户才能测试API")
        
    except ImportError:
        print("requests库未安装，跳过API测试")

if __name__ == "__main__":
    test_profile_save()
    check_web_api()
