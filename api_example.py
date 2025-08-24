#!/usr/bin/env python3
"""
Freedom.AI API使用示例
API Usage Examples
"""

import sys
import os

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase
from user_system.simple_auth import SimpleAuthManager
from analytics.behavior_analytics import BehaviorAnalytics
from user_system.models import ActionType

def api_register_example():
    """API注册示例"""
    print("=== API注册示例 ===")
    
    # 初始化系统
    db = UserDatabase("./data")
    auth = SimpleAuthManager(db)
    
    # 注册用户
    result = auth.register_user(
        username="api_user_demo",
        email="api_demo@example.com",
        password="password123"
    )
    
    if result['success']:
        print(f"✅ 注册成功: {result['username']}")
        print(f"用户ID: {result['user_id']}")
        
        # 更新用户档案
        db.update_user_profile(
            result['user_id'],
            full_name="API演示用户",
            bio="通过API创建的演示用户",
            skills=["Python", "API开发", "数据分析"],
            industry="technology"
        )
        print("✅ 用户档案已更新")
        
        return result['user_id']
    else:
        print(f"❌ 注册失败: {result['error']}")
        return None

def api_login_example(username="api_user_demo", password="password123"):
    """API登录示例"""
    print("\n=== API登录示例 ===")
    
    # 初始化系统
    db = UserDatabase("./data")
    auth = SimpleAuthManager(db)
    
    # 用户登录
    result = auth.login_user(
        username=username,
        password=password,
        ip_address="192.168.1.100",
        user_agent="API Client v1.0"
    )
    
    if result['success']:
        print(f"✅ 登录成功: {result['username']}")
        print(f"访问令牌: {result['access_token'][:20]}...")
        print(f"会话ID: {result['session_id']}")
        print(f"令牌有效期: {result['expires_in']} 秒")
        
        return {
            'user_id': result['user_id'],
            'token': result['access_token'],
            'session_id': result['session_id']
        }
    else:
        print(f"❌ 登录失败: {result['error']}")
        return None

def api_user_behavior_example(user_id):
    """API用户行为记录示例"""
    print("\n=== API用户行为记录示例 ===")
    
    db = UserDatabase("./data")
    
    # 模拟用户行为
    behaviors = [
        (ActionType.ASSESSMENT, {
            "assessment_type": "freedom_score",
            "score": 0.72,
            "duration": 280,
            "dimensions": ["financial", "time", "location", "skill"]
        }),
        (ActionType.SEARCH, {
            "keywords": ["remote work", "python developer", "AI"],
            "results_count": 15,
            "search_duration": 45
        }),
        (ActionType.OPPORTUNITY_VIEW, {
            "opportunity_id": "job_remote_001",
            "job_title": "远程Python开发工程师",
            "company": "TechCorp",
            "salary_range": "25000-40000",
            "remote_friendly": True,
            "view_duration": 120
        }),
        (ActionType.LEARNING_PLAN, {
            "target_skills": ["机器学习", "深度学习", "AI工程"],
            "learning_style": "hands_on",
            "estimated_duration": "3 months"
        })
    ]
    
    for action_type, details in behaviors:
        db.log_user_action(
            user_id=user_id,
            action_type=action_type,
            details=details,
            ip_address="192.168.1.100",
            user_agent="API Client v1.0"
        )
    
    print(f"✅ 记录了 {len(behaviors)} 个用户行为")

def api_analytics_example(user_id):
    """API分析功能示例"""
    print("\n=== API分析功能示例 ===")
    
    db = UserDatabase("./data")
    analytics = BehaviorAnalytics(db)
    
    # 获取用户统计
    stats = db.get_user_statistics(user_id)
    print(f"📊 用户统计:")
    print(f"   总行为数: {stats['total_actions']}")
    print(f"   最近7天: {stats['recent_actions_7d']}")
    
    # 生成个性化洞察
    insights = analytics.generate_personalized_insights(user_id)
    print(f"\n💡 个性化洞察:")
    for rec in insights['personalized_recommendations']:
        print(f"   • {rec}")
    
    # 用户旅程分析
    journey = analytics.analyze_user_journey(user_id, days=7)
    print(f"\n🗺️ 用户旅程:")
    print(f"   行为总数: {journey['total_actions']}")
    print(f"   洞察数量: {len(journey['insights'])}")
    
    return insights

def api_token_verification_example(token):
    """API令牌验证示例"""
    print("\n=== API令牌验证示例 ===")
    
    auth = SimpleAuthManager(UserDatabase("./data"))
    
    # 验证令牌
    result = auth.verify_token(token)
    
    if result['success']:
        print(f"✅ 令牌有效")
        print(f"用户: {result['username']}")
        print(f"用户ID: {result['user_id']}")
        print(f"会话ID: {result['session_id']}")
        return True
    else:
        print(f"❌ 令牌验证失败: {result['error']}")
        return False

def api_logout_example(session_id, user_id):
    """API登出示例"""
    print("\n=== API登出示例 ===")
    
    auth = SimpleAuthManager(UserDatabase("./data"))
    
    result = auth.logout_user(session_id, user_id)
    
    if result['success']:
        print("✅ 登出成功")
        return True
    else:
        print(f"❌ 登出失败: {result['error']}")
        return False

def complete_api_workflow():
    """完整的API工作流程示例"""
    print("Freedom.AI API完整工作流程演示")
    print("="*50)
    
    # 1. 注册用户
    user_id = api_register_example()
    if not user_id:
        return
    
    # 2. 用户登录
    login_info = api_login_example()
    if not login_info:
        return
    
    # 3. 验证令牌
    if not api_token_verification_example(login_info['token']):
        return
    
    # 4. 记录用户行为
    api_user_behavior_example(user_id)
    
    # 5. 分析用户数据
    insights = api_analytics_example(user_id)
    
    # 6. 用户登出
    api_logout_example(login_info['session_id'], user_id)
    
    print("\n🎉 API工作流程演示完成！")
    return insights

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'register':
            api_register_example()
        elif command == 'login':
            api_login_example()
        elif command == 'workflow':
            complete_api_workflow()
        else:
            print("用法:")
            print("  python3 api_example.py register   # 注册示例")
            print("  python3 api_example.py login      # 登录示例")
            print("  python3 api_example.py workflow   # 完整工作流程")
    else:
        # 默认运行完整工作流程
        complete_api_workflow()
