#!/usr/bin/env python3
"""
详细调试应用
"""

import os
import sys
import traceback
sys.path.append(os.path.dirname(__file__))

from flask import Flask, request, session

# 创建应用
app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.secret_key = 'debug-key'

# 添加请求日志
@app.before_request
def log_request():
    print(f"📥 请求: {request.method} {request.url}")
    print(f"   路径: {request.path}")
    print(f"   参数: {request.args}")
    if request.form:
        print(f"   表单: {dict(request.form)}")

@app.after_request
def log_response(response):
    print(f"📤 响应: {response.status_code}")
    return response

# 基础路由
@app.route('/')
def index():
    try:
        from flask import render_template
        return render_template('index.html')
    except Exception as e:
        print(f"❌ 首页错误: {e}")
        traceback.print_exc()
        return f"首页错误: {str(e)}", 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        print(f"🔧 注册路由被调用: {request.method}")
        from flask import render_template
        
        if request.method == 'POST':
            print("📝 处理注册表单")
            return "注册处理逻辑（调试版）"
        else:
            print("📄 显示注册页面")
            return render_template('register.html')
            
    except Exception as e:
        print(f"❌ 注册页面错误: {e}")
        traceback.print_exc()
        return f"注册页面错误: {str(e)}", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        print(f"🔧 登录路由被调用: {request.method}")
        from flask import render_template
        
        if request.method == 'POST':
            print("📝 处理登录表单")
            return "登录处理逻辑（调试版）"
        else:
            print("📄 显示登录页面")
            return render_template('login.html')
            
    except Exception as e:
        print(f"❌ 登录页面错误: {e}")
        traceback.print_exc()
        return f"登录页面错误: {str(e)}", 500

@app.route('/debug')
def debug_info():
    """调试信息页面"""
    info = {
        'routes': [],
        'templates': [],
        'static_files': []
    }
    
    # 路由信息
    for rule in app.url_map.iter_rules():
        info['routes'].append({
            'rule': rule.rule,
            'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
            'endpoint': rule.endpoint
        })
    
    # 模板文件
    template_dir = 'web/templates'
    if os.path.exists(template_dir):
        info['templates'] = [f for f in os.listdir(template_dir) if f.endswith('.html')]
    
    # 静态文件
    static_dir = 'web/static'
    if os.path.exists(static_dir):
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), static_dir)
                info['static_files'].append(rel_path)
    
    html = "<h1>调试信息</h1>"
    
    html += "<h2>路由列表</h2><ul>"
    for route in sorted(info['routes'], key=lambda x: x['rule']):
        html += f"<li><strong>{route['rule']}</strong> [{', '.join(route['methods'])}] -> {route['endpoint']}</li>"
    html += "</ul>"
    
    html += "<h2>模板文件</h2><ul>"
    for template in sorted(info['templates']):
        html += f"<li>{template}</li>"
    html += "</ul>"
    
    html += "<h2>测试链接</h2><ul>"
    html += '<li><a href="/">首页</a></li>'
    html += '<li><a href="/login">登录</a></li>'
    html += '<li><a href="/register">注册</a></li>'
    html += "</ul>"
    
    return html

# 错误处理
@app.errorhandler(404)
def not_found(error):
    print(f"❌ 404错误: {request.url}")
    return f"""
    <h1>404 - 页面未找到</h1>
    <p>请求的URL: {request.url}</p>
    <p>请求路径: {request.path}</p>
    <p><a href="/debug">查看调试信息</a></p>
    <p><a href="/">返回首页</a></p>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    print(f"❌ 500错误: {error}")
    traceback.print_exc()
    return f"""
    <h1>500 - 服务器内部错误</h1>
    <p>错误信息: {str(error)}</p>
    <p><a href="/debug">查看调试信息</a></p>
    <p><a href="/">返回首页</a></p>
    """, 500

if __name__ == '__main__':
    print("🔧 详细调试应用启动")
    print("📍 访问 http://localhost:5004/debug 查看调试信息")
    print("📍 访问 http://localhost:5004/register 测试注册页面")
    print("📍 所有请求都会在控制台显示详细日志")
    app.run(debug=True, host='0.0.0.0', port=5004)
