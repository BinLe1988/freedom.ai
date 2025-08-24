#!/usr/bin/env python3
"""
检查主应用的路由配置
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

try:
    # 导入主应用
    from web.app_with_auth import app
    
    print("🔍 Freedom.AI 应用路由检查")
    print("=" * 50)
    
    # 显示所有路由
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': sorted(list(rule.methods - {'HEAD', 'OPTIONS'})),
            'rule': rule.rule
        })
    
    # 按路径排序
    routes.sort(key=lambda x: x['rule'])
    
    print(f"总共找到 {len(routes)} 个路由:")
    print()
    
    for route in routes:
        methods_str = ', '.join(route['methods'])
        print(f"  {route['rule']:<25} [{methods_str:<15}] -> {route['endpoint']}")
    
    print()
    print("🎯 关键路由检查:")
    key_routes = ['/', '/login', '/register', '/dashboard', '/assessment']
    for path in key_routes:
        found = any(route['rule'] == path for route in routes)
        status = "✅" if found else "❌"
        print(f"  {status} {path}")
    
    print()
    print("📝 模板文件检查:")
    template_dir = "web/templates"
    if os.path.exists(template_dir):
        templates = [f for f in os.listdir(template_dir) if f.endswith('.html')]
        for template in sorted(templates):
            print(f"  ✅ {template}")
    else:
        print("  ❌ 模板目录不存在")

except Exception as e:
    print(f"❌ 导入应用失败: {e}")
    print("💡 可能的原因:")
    print("  - 缺少依赖包")
    print("  - 配置文件问题")
    print("  - 模块导入错误")
    
    # 尝试简单导入测试
    try:
        from flask import Flask
        print("  ✅ Flask 可用")
    except ImportError:
        print("  ❌ Flask 未安装")
    
    try:
        from user_system.auth import AuthManager
        print("  ✅ 认证模块可用")
    except ImportError as e2:
        print(f"  ❌ 认证模块问题: {e2}")
