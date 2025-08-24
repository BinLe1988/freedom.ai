#!/usr/bin/env python3
"""
检查运行中应用的路由
"""

import requests
import json

def check_live_routes():
    """检查运行中应用的路由"""
    
    print("🔍 检查运行中应用的路由...")
    
    # 尝试访问一些常见路由
    test_routes = [
        '/',
        '/login',
        '/register', 
        '/dashboard',
        '/assessment',
        '/opportunities',
        '/learning',
        '/profile',
        '/logout',
        '/api/calculate_freedom',
        '/admin/analytics'
    ]
    
    base_url = "http://localhost:5001"
    
    print(f"基础URL: {base_url}")
    print("=" * 60)
    
    for route in test_routes:
        url = base_url + route
        try:
            # 对于API路由使用POST，其他使用GET
            if route.startswith('/api/') and route != '/api/export_data':
                response = requests.post(url, timeout=3, json={})
            else:
                response = requests.get(url, timeout=3)
            
            status = response.status_code
            
            if status == 200:
                print(f"✅ {route:<25} - {status} (正常)")
            elif status == 302:
                location = response.headers.get('Location', '未知')
                print(f"🔄 {route:<25} - {status} (重定向到: {location})")
            elif status == 401:
                print(f"🔒 {route:<25} - {status} (需要认证)")
            elif status == 404:
                print(f"❌ {route:<25} - {status} (未找到)")
            elif status == 405:
                print(f"⚠️  {route:<25} - {status} (方法不允许)")
            else:
                print(f"❓ {route:<25} - {status} (其他)")
                
        except requests.exceptions.ConnectionError:
            print(f"💥 {route:<25} - 连接失败")
        except requests.exceptions.Timeout:
            print(f"⏰ {route:<25} - 超时")
        except Exception as e:
            print(f"❌ {route:<25} - 错误: {e}")
    
    print("\n" + "=" * 60)
    
    # 尝试获取首页内容，看看是否有线索
    try:
        response = requests.get(base_url + "/", timeout=5)
        if response.status_code == 200:
            content = response.text
            print("📄 首页内容分析:")
            
            # 检查是否包含注册链接
            if 'href="/register"' in content:
                print("  ✅ 首页包含注册链接")
            else:
                print("  ❌ 首页不包含注册链接")
            
            # 检查是否包含登录链接  
            if 'href="/login"' in content:
                print("  ✅ 首页包含登录链接")
            else:
                print("  ❌ 首页不包含登录链接")
                
            # 查找所有链接
            import re
            links = re.findall(r'href="([^"]*)"', content)
            internal_links = [link for link in links if link.startswith('/') and not link.startswith('//')]
            
            if internal_links:
                print(f"  📎 发现的内部链接: {', '.join(set(internal_links))}")
            
    except Exception as e:
        print(f"❌ 无法分析首页内容: {e}")

if __name__ == '__main__':
    check_live_routes()
