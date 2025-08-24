#!/usr/bin/env python3
"""
调试dashboard路由问题
Debug Dashboard Route Issues
"""

import os
import sys
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(__file__))

def test_dashboard_dependencies():
    """测试dashboard路由的依赖"""
    print("=== Dashboard路由依赖测试 ===")
    
    try:
        # 测试数据库导入
        from database.user_db import UserDatabase
        print("✓ 数据库模块导入成功")
        
        # 测试分析模块导入
        from analytics.behavior_analytics import BehaviorAnalytics
        print("✓ 分析模块导入成功")
        
        # 初始化组件
        db = UserDatabase("./data")
        analytics = BehaviorAnalytics(db)
        print("✓ 组件初始化成功")
        
        # 获取测试用户
        import json
        with open("./data/users.json", 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        if not users_data:
            print("✗ 没有用户数据")
            return
        
        user_id = list(users_data.keys())[0]
        print(f"✓ 测试用户ID: {user_id}")
        
        # 测试get_user_statistics
        print("\n1. 测试 get_user_statistics:")
        try:
            user_stats = db.get_user_statistics(user_id)
            print(f"✓ 用户统计获取成功")
            print(f"  - 用户名: {user_stats.get('username')}")
            print(f"  - 总操作数: {user_stats.get('total_actions')}")
            print(f"  - 7天内操作: {user_stats.get('recent_actions_7d')}")
        except Exception as e:
            print(f"✗ 用户统计获取失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 测试generate_personalized_insights
        print("\n2. 测试 generate_personalized_insights:")
        try:
            insights = analytics.generate_personalized_insights(user_id)
            print(f"✓ 个性化洞察生成成功")
            print(f"  - 推荐数量: {len(insights.get('personalized_recommendations', []))}")
            print(f"  - 推荐内容: {insights.get('personalized_recommendations', [])[:2]}")
        except Exception as e:
            print(f"✗ 个性化洞察生成失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 测试模板文件
        print("\n3. 测试模板文件:")
        template_path = "./web/templates/dashboard.html"
        if os.path.exists(template_path):
            print(f"✓ 模板文件存在: {template_path}")
        else:
            print(f"✗ 模板文件不存在: {template_path}")
        
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def create_minimal_dashboard_route():
    """创建最小化的dashboard路由"""
    print("\n=== 创建最小化Dashboard路由 ===")
    
    minimal_route = '''
    @app.route('/dashboard')
    @require_login
    def dashboard():
        """用户仪表板 - 简化版本"""
        try:
            user_id = session['user_id']
            
            # 记录访问行为
            log_user_action(ActionType.LOGIN, {'page': 'dashboard'})
            
            # 获取基本用户信息
            user = db.get_user(user_id)
            if not user:
                return redirect(url_for('login'))
            
            # 尝试获取用户统计，如果失败则使用默认值
            try:
                user_stats = db.get_user_statistics(user_id)
            except Exception as e:
                print(f"获取用户统计失败: {e}")
                user_stats = {
                    'user_id': user_id,
                    'username': user.username,
                    'total_actions': 0,
                    'recent_actions_7d': 0,
                    'behavior_analysis': {}
                }
            
            # 尝试获取个性化洞察，如果失败则使用默认值
            try:
                insights = analytics.generate_personalized_insights(user_id)
            except Exception as e:
                print(f"生成个性化洞察失败: {e}")
                insights = {
                    'user_id': user_id,
                    'username': user.username,
                    'analysis_date': datetime.now().isoformat(),
                    'personalized_recommendations': ['欢迎使用Freedom.AI！', '开始探索您的自由度评估'],
                    'next_actions': []
                }
            
            return render_template('dashboard.html', 
                                 user_stats=user_stats, 
                                 insights=insights)
                                 
        except Exception as e:
            print(f"Dashboard路由错误: {e}")
            import traceback
            traceback.print_exc()
            # 返回错误页面或重定向
            return render_template('500.html', error=str(e)), 500
    '''
    
    print("建议的最小化dashboard路由代码:")
    print(minimal_route)
    
    return minimal_route

def fix_dashboard_route():
    """修复dashboard路由"""
    print("\n=== 修复Dashboard路由 ===")
    
    # 读取当前的app文件
    app_file = "./web/app_with_auth.py"
    
    try:
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找dashboard路由
        if '@app.route(\'/dashboard\')' in content:
            print("✓ 找到dashboard路由")
            
            # 创建备份
            backup_file = f"{app_file}.backup_{int(datetime.now().timestamp())}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 创建备份: {backup_file}")
            
            # 提供修复建议
            print("\n修复建议:")
            print("1. 在dashboard路由中添加try-catch错误处理")
            print("2. 为user_stats和insights提供默认值")
            print("3. 添加调试日志输出")
            print("4. 检查模板文件是否存在")
            
        else:
            print("✗ 未找到dashboard路由")
            
    except Exception as e:
        print(f"✗ 读取文件失败: {e}")

if __name__ == "__main__":
    test_dashboard_dependencies()
    create_minimal_dashboard_route()
    fix_dashboard_route()
