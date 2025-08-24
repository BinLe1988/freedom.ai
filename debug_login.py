#!/usr/bin/env python3
"""
登录调试工具
Login Debug Tool
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

# 添加路径
sys.path.append(os.path.dirname(__file__))

def check_ports():
    """检查端口占用情况"""
    print("🔍 检查端口占用情况...")
    
    ports = [3000, 5000, 5001, 8000]
    
    for port in ports:
        try:
            result = subprocess.run(['lsof', '-i', f':{port}'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                print(f"❌ 端口 {port} 被占用:")
                lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                for line in lines[:2]:  # 只显示前2行
                    print(f"   {line}")
            else:
                print(f"✅ 端口 {port} 可用")
        except Exception as e:
            print(f"⚠️  检查端口 {port} 失败: {e}")

def start_backend_server():
    """启动后端服务器"""
    print("\n🚀 启动后端服务器...")
    
    # 寻找可用端口
    available_port = None
    for port in [5001, 5002, 8000, 8001]:
        try:
            result = subprocess.run(['lsof', '-i', f':{port}'], 
                                  capture_output=True, text=True)
            if result.returncode != 0 or not result.stdout.strip():
                available_port = port
                break
        except:
            continue
    
    if not available_port:
        print("❌ 没有找到可用端口")
        return None
    
    print(f"📡 使用端口: {available_port}")
    
    # 修改Flask应用端口
    try:
        # 启动Flask服务器
        env = os.environ.copy()
        env['FLASK_PORT'] = str(available_port)
        
        process = subprocess.Popen([
            sys.executable, 'web/app_with_auth.py', '--port', str(available_port)
        ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务器启动
        time.sleep(3)
        
        # 检查服务器是否启动成功
        if process.poll() is None:
            print(f"✅ 后端服务器启动成功: http://localhost:{available_port}")
            return available_port
        else:
            stdout, stderr = process.communicate()
            print(f"❌ 后端服务器启动失败")
            print(f"错误: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ 启动后端服务器失败: {e}")
        return None

def create_env_file(api_port):
    """创建环境变量文件"""
    print(f"\n⚙️ 创建环境变量文件...")
    
    frontend_dir = Path("frontend")
    env_file = frontend_dir / ".env.local"
    
    env_content = f"""# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:{api_port}
NEXT_PUBLIC_APP_URL=http://localhost:3000

# App Configuration
NEXT_PUBLIC_APP_NAME=Freedom.AI
NEXT_PUBLIC_APP_VERSION=1.0.0
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ 环境变量文件已创建: {env_file}")
        print(f"   API地址: http://localhost:{api_port}")
        return True
        
    except Exception as e:
        print(f"❌ 创建环境变量文件失败: {e}")
        return False

def test_api_connection(port):
    """测试API连接"""
    print(f"\n🌐 测试API连接: http://localhost:{port}")
    
    try:
        import urllib.request
        import urllib.parse
        
        # 测试基础连接
        try:
            response = urllib.request.urlopen(f"http://localhost:{port}/", timeout=5)
            print("✅ 基础连接成功")
        except Exception as e:
            print(f"❌ 基础连接失败: {e}")
            return False
        
        # 测试登录API
        login_data = {
            "username": "test@example.com",
            "password": "123456"
        }
        
        data = json.dumps(login_data).encode('utf-8')
        req = urllib.request.Request(
            f"http://localhost:{port}/login",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            response = urllib.request.urlopen(req, timeout=10)
            result = json.loads(response.read().decode())
            
            if result.get('success'):
                print("✅ 登录API测试成功")
                print(f"   用户ID: {result.get('user_id')}")
                print(f"   用户名: {result.get('username')}")
                return True
            else:
                print(f"❌ 登录API测试失败: {result.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ 登录API测试失败: {e}")
            return False
            
    except ImportError:
        print("⚠️  无法导入urllib，跳过API测试")
        return True

def create_simple_backend():
    """创建简单的后端服务器"""
    print("\n🔧 创建简单的后端服务器...")
    
    simple_server_code = '''#!/usr/bin/env python3
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
        print("\\n⏹️  服务器已停止")
        server.shutdown()

if __name__ == "__main__":
    main()
'''
    
    simple_server_file = Path("simple_login_server.py")
    
    try:
        with open(simple_server_file, 'w') as f:
            f.write(simple_server_code)
        
        print(f"✅ 简单服务器已创建: {simple_server_file}")
        return simple_server_file
        
    except Exception as e:
        print(f"❌ 创建简单服务器失败: {e}")
        return None

def show_debug_instructions():
    """显示调试说明"""
    print("\n" + "="*60)
    print("🔧 登录调试说明")
    print("="*60)
    
    print("\n📋 问题诊断步骤:")
    print("1. 检查端口占用情况")
    print("2. 启动后端API服务器")
    print("3. 创建前端环境变量文件")
    print("4. 测试API连接")
    print("5. 启动前端服务器")
    
    print("\n🚀 手动启动步骤:")
    print("1. 启动简单API服务器:")
    print("   python3 simple_login_server.py 5001")
    
    print("\n2. 启动前端服务器:")
    print("   cd frontend")
    print("   npm run dev")
    
    print("\n3. 测试登录:")
    print("   访问: http://localhost:3000/login")
    print("   邮箱: test@example.com")
    print("   密码: 123456")
    
    print("\n🔍 调试技巧:")
    print("- 打开浏览器开发者工具")
    print("- 查看Network标签页的API请求")
    print("- 查看Console标签页的错误信息")
    print("- 确认API请求地址是否正确")

def main():
    print("Freedom.AI 登录调试工具")
    print("="*50)
    
    # 检查端口
    check_ports()
    
    # 创建简单服务器
    server_file = create_simple_backend()
    
    if server_file:
        print(f"\n✅ 已创建简单API服务器: {server_file}")
        
        # 创建环境变量文件
        create_env_file(5001)
        
        print("\n🚀 现在可以手动启动服务器:")
        print("1. 启动API服务器: python3 simple_login_server.py 5001")
        print("2. 启动前端服务器: cd frontend && npm run dev")
        print("3. 访问登录页面: http://localhost:3000/login")
        
        # 询问是否自动启动
        choice = input("\n是否自动启动简单API服务器? (y/n): ").strip().lower()
        
        if choice == 'y':
            print("\n🚀 启动简单API服务器...")
            try:
                subprocess.run([sys.executable, str(server_file), '5001'])
            except KeyboardInterrupt:
                print("\n⏹️  服务器已停止")
    
    show_debug_instructions()

if __name__ == "__main__":
    main()
