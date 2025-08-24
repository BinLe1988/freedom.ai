#!/usr/bin/env python3
"""
简化版调试应用
"""

from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.secret_key = 'debug-secret-key-12345'

@app.route('/')
def index():
    """首页"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"首页渲染错误: {str(e)}", 500

@app.route('/login')
def login():
    """登录页面"""
    try:
        return render_template('login.html')
    except Exception as e:
        return f"登录页面渲染错误: {str(e)}", 500

@app.route('/register')
def register():
    """注册页面"""
    try:
        return render_template('register.html')
    except Exception as e:
        return f"注册页面渲染错误: {str(e)}", 500

@app.route('/test')
def test():
    """测试页面"""
    return """
    <h1>Freedom.AI 调试页面</h1>
    <p>如果你能看到这个页面，说明Flask应用运行正常。</p>
    <ul>
        <li><a href="/">首页</a></li>
        <li><a href="/login">登录</a></li>
        <li><a href="/register">注册</a></li>
    </ul>
    """

@app.errorhandler(404)
def not_found(error):
    return f"""
    <h1>404 - 页面未找到</h1>
    <p>请求的URL: {request.url}</p>
    <p>可用路由:</p>
    <ul>
        <li><a href="/">首页</a></li>
        <li><a href="/test">测试页面</a></li>
        <li><a href="/login">登录</a></li>
        <li><a href="/register">注册</a></li>
    </ul>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    return f"""
    <h1>500 - 服务器内部错误</h1>
    <p>错误信息: {str(error)}</p>
    <p><a href="/">返回首页</a></p>
    """, 500

if __name__ == '__main__':
    print("🔧 Freedom.AI 调试模式启动")
    print("📍 访问 http://localhost:5002/test 进行测试")
    print("📍 访问 http://localhost:5002/ 查看首页")
    app.run(debug=True, host='0.0.0.0', port=5002)
