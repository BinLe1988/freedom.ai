#!/usr/bin/env python3
"""
简化的Web服务器 (不依赖Flask)
Simple Web Server without Flask dependency
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(__file__))

from database.user_db import UserDatabase
from user_system.simple_auth import SimpleAuthManager
from analytics.behavior_analytics import BehaviorAnalytics
from tools.freedom_calculator import FreedomCalculator

class FreedomAIHandler(http.server.SimpleHTTPRequestHandler):
    """Freedom.AI HTTP请求处理器"""
    
    def __init__(self, *args, **kwargs):
        # 初始化系统组件
        self.db = UserDatabase("./data")
        self.auth = SimpleAuthManager(self.db)
        self.analytics = BehaviorAnalytics(self.db)
        self.calculator = FreedomCalculator()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_html_page('index')
        elif self.path == '/register':
            self.serve_html_page('register')
        elif self.path == '/login':
            self.serve_html_page('login')
        elif self.path == '/dashboard':
            self.serve_html_page('dashboard')
        elif self.path.startswith('/static/'):
            self.serve_static_file()
        else:
            self.send_error(404, "Page not found")
    
    def do_POST(self):
        """处理POST请求"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            if self.path == '/api/register':
                self.handle_register(post_data)
            elif self.path == '/api/login':
                self.handle_login(post_data)
            elif self.path == '/api/calculate_freedom':
                self.handle_calculate_freedom(post_data)
            else:
                self.send_error(404, "API endpoint not found")
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_html_page(self, page_name):
        """提供HTML页面"""
        html_content = self.get_html_content(page_name)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def get_html_content(self, page_name):
        """获取HTML内容"""
        if page_name == 'index':
            return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Freedom.AI - 自由探索人生可能性</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 0;
        }
    </style>
</head>
<body>
    <div class="hero-section text-center">
        <div class="container">
            <h1 class="display-4 fw-bold mb-4">🚀 Freedom.AI</h1>
            <p class="lead mb-5">探索自由人生的无限可能</p>
            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                <a href="/register" class="btn btn-light btn-lg me-md-2">立即注册</a>
                <a href="/login" class="btn btn-outline-light btn-lg">用户登录</a>
            </div>
        </div>
    </div>
    
    <div class="container my-5">
        <div class="row text-center">
            <div class="col-md-3">
                <h5>🧠 决策支持AI</h5>
                <p>智能分析机会，提供数据驱动的决策建议</p>
            </div>
            <div class="col-md-3">
                <h5>⚙️ 执行助手AI</h5>
                <p>自动化任务执行，提高工作效率</p>
            </div>
            <div class="col-md-3">
                <h5>🎓 学习伙伴AI</h5>
                <p>个性化学习路径，持续技能提升</p>
            </div>
            <div class="col-md-3">
                <h5>🔍 机会探索AI</h5>
                <p>发现市场机会，创造收入来源</p>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
            """
        
        elif page_name == 'register':
            return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>注册 - Freedom.AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .register-container {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .register-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="register-container d-flex align-items-center justify-content-center py-4">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card register-card">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <h2>🚀 Freedom.AI</h2>
                                <h4>开始你的自由之旅</h4>
                            </div>
                            
                            <div id="message"></div>
                            
                            <form id="registerForm">
                                <div class="mb-3">
                                    <label class="form-label">用户名 *</label>
                                    <input type="text" class="form-control" id="username" required>
                                    <small class="text-muted">至少3个字符</small>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">邮箱地址 *</label>
                                    <input type="email" class="form-control" id="email" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">密码 *</label>
                                    <input type="password" class="form-control" id="password" required>
                                    <small class="text-muted">至少6个字符</small>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">确认密码 *</label>
                                    <input type="password" class="form-control" id="confirmPassword" required>
                                </div>
                                
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary btn-lg">创建账号</button>
                                </div>
                            </form>
                            
                            <div class="text-center mt-3">
                                <p>已有账号？<a href="/login">立即登录</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('registerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (password !== confirmPassword) {
                showMessage('密码不匹配', 'danger');
                return;
            }
            
            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, email, password})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage('注册成功！正在跳转...', 'success');
                    setTimeout(() => window.location.href = '/login', 2000);
                } else {
                    showMessage(result.error, 'danger');
                }
            } catch (error) {
                showMessage('网络错误，请稍后重试', 'danger');
            }
        });
        
        function showMessage(message, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
        }
    </script>
</body>
</html>
            """
        
        elif page_name == 'login':
            return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 - Freedom.AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .login-container {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="login-container d-flex align-items-center justify-content-center">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-4">
                    <div class="card login-card">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <h2>🚀 Freedom.AI</h2>
                                <h4>欢迎回来</h4>
                            </div>
                            
                            <div id="message"></div>
                            
                            <form id="loginForm">
                                <div class="mb-3">
                                    <label class="form-label">用户名</label>
                                    <input type="text" class="form-control" id="username" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">密码</label>
                                    <input type="password" class="form-control" id="password" required>
                                </div>
                                
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary btn-lg">登录</button>
                                </div>
                            </form>
                            
                            <div class="text-center mt-3">
                                <p>还没有账号？<a href="/register">立即注册</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage('登录成功！正在跳转...', 'success');
                    localStorage.setItem('access_token', result.access_token);
                    localStorage.setItem('username', result.username);
                    setTimeout(() => window.location.href = '/dashboard', 2000);
                } else {
                    showMessage(result.error, 'danger');
                }
            } catch (error) {
                showMessage('网络错误，请稍后重试', 'danger');
            }
        });
        
        function showMessage(message, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
        }
    </script>
</body>
</html>
            """
        
        elif page_name == 'dashboard':
            return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>仪表板 - Freedom.AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">🚀 Freedom.AI</a>
            <div class="navbar-nav ms-auto">
                <span class="navbar-text me-3">欢迎，<span id="username"></span>！</span>
                <button class="btn btn-outline-light btn-sm" onclick="logout()">登出</button>
            </div>
        </div>
    </nav>
    
    <div class="container my-5">
        <div class="row">
            <div class="col-md-8">
                <h2>🎯 个人仪表板</h2>
                <p class="text-muted">欢迎使用Freedom.AI！这里是你的个性化控制中心。</p>
                
                <div class="row g-4 mt-3">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5>📊 自由度评估</h5>
                                <p>评估你的五维自由度</p>
                                <button class="btn btn-primary" onclick="startAssessment()">开始评估</button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5>🔍 机会探索</h5>
                                <p>发现适合你的机会</p>
                                <button class="btn btn-success" onclick="exploreOpportunities()">探索机会</button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5>📚 学习规划</h5>
                                <p>制定个性化学习计划</p>
                                <button class="btn btn-warning" onclick="createLearningPlan()">学习规划</button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5>👤 个人档案</h5>
                                <p>管理你的个人信息</p>
                                <button class="btn btn-info" onclick="manageProfile()">管理档案</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h6>💡 个性化建议</h6>
                    </div>
                    <div class="card-body">
                        <p class="small">完成更多操作以获得个性化洞察和建议。</p>
                        <ul class="small">
                            <li>完成首次自由度评估</li>
                            <li>浏览机会探索页面</li>
                            <li>制定学习计划</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // 检查登录状态
        const token = localStorage.getItem('access_token');
        const username = localStorage.getItem('username');
        
        if (!token || !username) {
            window.location.href = '/login';
        } else {
            document.getElementById('username').textContent = username;
        }
        
        function logout() {
            localStorage.removeItem('access_token');
            localStorage.removeItem('username');
            window.location.href = '/login';
        }
        
        function startAssessment() {
            alert('自由度评估功能：\\n请使用命令行工具：python3 tools/freedom_calculator.py --interactive');
        }
        
        function exploreOpportunities() {
            alert('机会探索功能：\\n请使用命令行工具：python3 demo_jobleads.py');
        }
        
        function createLearningPlan() {
            alert('学习规划功能：\\n请查看完整Web版本或使用API接口');
        }
        
        function manageProfile() {
            alert('档案管理功能：\\n请使用命令行工具：python3 cli_auth.py');
        }
    </script>
</body>
</html>
            """
        
        return "<html><body><h1>Page not found</h1></body></html>"
    
    def handle_register(self, post_data):
        """处理注册请求"""
        try:
            data = json.loads(post_data.decode('utf-8'))
            result = self.auth.register_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            self.send_json_response(result)
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_login(self, post_data):
        """处理登录请求"""
        try:
            data = json.loads(post_data.decode('utf-8'))
            result = self.auth.login_user(
                username=data['username'],
                password=data['password'],
                ip_address=self.client_address[0],
                user_agent=self.headers.get('User-Agent', 'Unknown')
            )
            self.send_json_response(result)
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_calculate_freedom(self, post_data):
        """处理自由度计算请求"""
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # 这里可以集成自由度计算逻辑
            result = {
                'success': True,
                'message': '请使用命令行工具进行详细评估：python3 tools/freedom_calculator.py --interactive'
            }
            
            self.send_json_response(result)
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def send_json_response(self, data, status_code=200):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))

def start_server(port=8000):
    """启动简化Web服务器"""
    try:
        with socketserver.TCPServer(("", port), FreedomAIHandler) as httpd:
            print(f"🚀 Freedom.AI 简化Web服务器启动成功！")
            print(f"📱 访问地址: http://localhost:{port}")
            print(f"✨ 功能特性:")
            print(f"   • 用户注册和登录")
            print(f"   • 个人仪表板")
            print(f"   • 无需Flask依赖")
            print(f"   • 集成用户系统")
            print(f"\n💡 使用说明:")
            print(f"   1. 点击'立即注册'创建账号")
            print(f"   2. 登录后进入个人仪表板")
            print(f"   3. 使用命令行工具体验完整功能")
            print(f"\n按 Ctrl+C 停止服务器")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n👋 服务器已停止")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {port} 已被占用，尝试使用端口 {port+1}")
            start_server(port+1)
        else:
            print(f"❌ 启动服务器失败: {e}")

if __name__ == "__main__":
    import sys
    
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("端口号必须是数字")
            sys.exit(1)
    
    start_server(port)
