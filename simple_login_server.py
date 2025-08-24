#!/usr/bin/env python3
"""
简单的登录API服务器
Simple Login API Server
"""

import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 添加路径
sys.path.append(os.path.dirname(__file__))

try:
    from database.user_db import UserDatabase
    db = UserDatabase("./data")
    print("✅ 数据库连接成功")
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")
    db = None

class LoginHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "ok", "message": "Freedom.AI API Server"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/login':
            self.handle_login()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_login(self):
        """处理登录请求"""
        try:
            # 读取请求数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            username = data.get('username')
            password = data.get('password')
            
            print(f"登录请求: {username}")
            
            if not username or not password:
                self.send_error_response("请输入用户名和密码")
                return
            
            # 验证用户
            if db:
                user = db.authenticate_user(username, password)
                if user:
                    response = {
                        "success": True,
                        "user_id": user.user_id,
                        "username": user.username,
                        "session_id": f"session_{user.user_id}",
                        "message": "登录成功"
                    }
                    self.send_success_response(response)
                    print(f"✅ 用户 {username} 登录成功")
                else:
                    self.send_error_response("用户名或密码错误")
                    print(f"❌ 用户 {username} 登录失败")
            else:
                # 数据库不可用时的测试模式
                if username in ["test@example.com", "test"] and password == "123456":
                    response = {
                        "success": True,
                        "user_id": "test_user_id",
                        "username": "test",
                        "session_id": "test_session",
                        "message": "登录成功 (测试模式)"
                    }
                    self.send_success_response(response)
                    print(f"✅ 测试用户 {username} 登录成功")
                else:
                    self.send_error_response("用户名或密码错误")
                    print(f"❌ 测试用户 {username} 登录失败")
                    
        except Exception as e:
            print(f"❌ 登录处理错误: {e}")
            self.send_error_response(f"服务器错误: {str(e)}")
    
    def send_success_response(self, data):
        """发送成功响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, error_message):
        """发送错误响应"""
        self.send_response(200)  # 仍然返回200，错误信息在JSON中
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"success": False, "error": error_message}
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.address_string()}] {format % args}")

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    
    server = HTTPServer(('localhost', port), LoginHandler)
    print(f"🚀 简单API服务器启动: http://localhost:{port}")
    print("📝 支持的端点:")
    print("   GET  / - 服务器状态")
    print("   POST /login - 用户登录")
    print("⏹️  按 Ctrl+C 停止服务器")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  服务器已停止")
        server.shutdown()

if __name__ == "__main__":
    main()
