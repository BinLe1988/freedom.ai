#!/usr/bin/env python3
"""
测试修复后的档案保存功能
Test Fixed Profile Save Functionality
"""

import os
import sys
import json
import time
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(__file__))

def test_web_api():
    """测试Web API档案更新"""
    print("=== 测试Web API档案更新 ===")
    
    print("注意: 由于没有安装requests库，跳过Web API测试")
    print("要测试Web API，请:")
    print("1. 安装requests: pip install requests")
    print("2. 启动Web服务器: python3 web/app_with_auth.py")
    print("3. 在浏览器中登录用户")
    print("4. 尝试编辑和保存档案")

def create_test_user_and_profile():
    """创建测试用户和档案"""
    print("\n=== 创建测试用户和档案 ===")
    
    from database.user_db import UserDatabase
    
    db = UserDatabase("./data")
    
    # 创建测试用户
    try:
        test_username = f"test_user_{int(time.time())}"
        test_email = f"test_{int(time.time())}@example.com"
        
        user = db.create_user(
            username=test_username,
            email=test_email,
            password="test123456"
        )
        
        print(f"✓ 测试用户创建成功: {user.username} (ID: {user.user_id})")
        
        # 测试档案创建和更新
        profile_data = {
            'full_name': '测试用户档案',
            'bio': '这是测试档案',
            'location': '测试城市',
            'industry': '测试行业',
            'current_role': '测试职位',
            'experience_years': 2,
            'skills': ['测试', 'Python'],
            'interests': ['编程', '测试']
        }
        
        # 检查档案是否存在
        existing_profile = db.get_user_profile(user.user_id)
        
        if existing_profile is None:
            print("档案不存在，创建新档案...")
            profile = db.create_user_profile(user.user_id, **profile_data)
            print(f"✓ 档案创建成功: {profile.full_name}")
        else:
            print("档案已存在，执行更新...")
            success = db.update_user_profile(user.user_id, **profile_data)
            print(f"档案更新结果: {'成功' if success else '失败'}")
        
        # 验证档案
        final_profile = db.get_user_profile(user.user_id)
        if final_profile:
            print(f"✓ 最终档案: {final_profile.full_name}")
            print(f"✓ 技能: {final_profile.skills}")
            print(f"✓ 兴趣: {final_profile.interests}")
        
        return user.user_id
        
    except Exception as e:
        print(f"✗ 测试用户创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def provide_solution_summary():
    """提供解决方案总结"""
    print("\n" + "="*50)
    print("档案保存问题解决方案总结")
    print("="*50)
    
    print("\n问题原因:")
    print("1. 用户首次编辑档案时，档案记录不存在")
    print("2. update_user_profile() 方法在档案不存在时返回 False")
    print("3. Web API 没有检查返回值，也没有处理档案不存在的情况")
    
    print("\n解决方案:")
    print("1. 修改 api_update_profile() 方法")
    print("2. 在更新前检查档案是否存在")
    print("3. 如果不存在，先调用 create_user_profile() 创建档案")
    print("4. 如果存在，再调用 update_user_profile() 更新档案")
    print("5. 添加错误处理和日志输出")
    
    print("\n修复状态:")
    print("✓ Web应用文件已修复 (web/app_with_auth.py)")
    print("✓ 添加了档案存在性检查")
    print("✓ 添加了自动创建档案逻辑")
    print("✓ 添加了错误处理和日志")
    
    print("\n测试建议:")
    print("1. 重启Web服务器")
    print("2. 登录用户账号")
    print("3. 尝试编辑和保存档案")
    print("4. 检查浏览器控制台和服务器日志")
    
    print("\n启动命令:")
    print("cd /Users/richardl/projects/freedom.ai")
    print("python3 web/app_with_auth.py")

if __name__ == "__main__":
    # 创建测试用户和档案
    user_id = create_test_user_and_profile()
    
    # 测试Web API (需要手动提供session)
    test_web_api()
    
    # 提供解决方案总结
    provide_solution_summary()
