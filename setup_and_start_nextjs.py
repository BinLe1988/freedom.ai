#!/usr/bin/env python3
"""
Freedom.AI Next.js 完整设置和启动脚本
Complete Next.js Setup and Start Script
"""

import os
import subprocess
import sys
import time
from pathlib import Path

class NextJSManager:
    def __init__(self):
        self.project_root = Path(".")
        self.frontend_dir = self.project_root / "frontend"
        
    def check_node_npm(self):
        """检查Node.js和npm是否安装"""
        print("🔍 检查Node.js和npm...")
        
        try:
            # 检查Node.js
            node_result = subprocess.run(['node', '--version'], 
                                       capture_output=True, text=True)
            if node_result.returncode == 0:
                print(f"✅ Node.js版本: {node_result.stdout.strip()}")
            else:
                print("❌ Node.js未安装")
                return False
            
            # 检查npm
            npm_result = subprocess.run(['npm', '--version'], 
                                      capture_output=True, text=True)
            if npm_result.returncode == 0:
                print(f"✅ npm版本: {npm_result.stdout.strip()}")
            else:
                print("❌ npm未安装")
                return False
                
            return True
            
        except FileNotFoundError:
            print("❌ Node.js或npm未安装")
            print("请先安装Node.js: https://nodejs.org/")
            return False
    
    def install_dependencies(self):
        """安装依赖"""
        print("\n📦 安装依赖包...")
        
        if not self.frontend_dir.exists():
            print("❌ frontend目录不存在，请先运行setup_nextjs.py")
            return False
        
        try:
            os.chdir(self.frontend_dir)
            
            # 安装依赖
            result = subprocess.run(['npm', 'install'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 依赖安装成功")
                return True
            else:
                print(f"❌ 依赖安装失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 安装过程出错: {e}")
            return False
        finally:
            os.chdir(self.project_root)
    
    def create_env_file(self):
        """创建环境变量文件"""
        print("\n⚙️ 创建环境变量文件...")
        
        env_content = """# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# App Configuration
NEXT_PUBLIC_APP_NAME=Freedom.AI
NEXT_PUBLIC_APP_VERSION=1.0.0

# Development
NODE_ENV=development
"""
        
        env_file = self.frontend_dir / ".env.local"
        with open(env_file, "w") as f:
            f.write(env_content)
        
        print("✅ 环境变量文件已创建")
    
    def start_development_server(self):
        """启动开发服务器"""
        print("\n🚀 启动Next.js开发服务器...")
        
        try:
            os.chdir(self.frontend_dir)
            
            print("📝 开发服务器启动中...")
            print("🌐 前端地址: http://localhost:3000")
            print("⚡ 后端地址: http://localhost:5000")
            print("⏹️  按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            # 启动开发服务器
            subprocess.run(['npm', 'run', 'dev'])
            
        except KeyboardInterrupt:
            print("\n\n⏹️  开发服务器已停止")
        except Exception as e:
            print(f"\n❌ 启动失败: {e}")
        finally:
            os.chdir(self.project_root)
    
    def build_production(self):
        """构建生产版本"""
        print("\n🏗️ 构建生产版本...")
        
        try:
            os.chdir(self.frontend_dir)
            
            # 构建
            result = subprocess.run(['npm', 'run', 'build'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 生产版本构建成功")
                return True
            else:
                print(f"❌ 构建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 构建过程出错: {e}")
            return False
        finally:
            os.chdir(self.project_root)
    
    def start_production_server(self):
        """启动生产服务器"""
        print("\n🚀 启动生产服务器...")
        
        try:
            os.chdir(self.frontend_dir)
            
            print("📝 生产服务器启动中...")
            print("🌐 访问地址: http://localhost:3000")
            print("⏹️  按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            # 启动生产服务器
            subprocess.run(['npm', 'start'])
            
        except KeyboardInterrupt:
            print("\n\n⏹️  生产服务器已停止")
        except Exception as e:
            print(f"\n❌ 启动失败: {e}")
        finally:
            os.chdir(self.project_root)
    
    def show_project_status(self):
        """显示项目状态"""
        print("\n📊 项目状态检查:")
        
        # 检查目录结构
        directories = [
            "frontend/src/app",
            "frontend/src/components",
            "frontend/src/styles",
            "frontend/src/utils",
            "frontend/src/store"
        ]
        
        for directory in directories:
            path = self.project_root / directory
            if path.exists():
                print(f"✅ {directory}")
            else:
                print(f"❌ {directory}")
        
        # 检查关键文件
        files = [
            "frontend/package.json",
            "frontend/next.config.js",
            "frontend/tailwind.config.js",
            "frontend/tsconfig.json",
            "frontend/src/app/layout.tsx",
            "frontend/src/app/page.tsx"
        ]
        
        for file in files:
            path = self.project_root / file
            if path.exists():
                print(f"✅ {file}")
            else:
                print(f"❌ {file}")
    
    def show_help(self):
        """显示帮助信息"""
        print("\n📖 Next.js项目管理帮助:")
        print("=" * 50)
        
        commands = [
            ("开发模式", "npm run dev", "启动开发服务器"),
            ("构建项目", "npm run build", "构建生产版本"),
            ("启动生产", "npm start", "启动生产服务器"),
            ("代码检查", "npm run lint", "运行ESLint检查"),
            ("类型检查", "npm run type-check", "运行TypeScript检查")
        ]
        
        for name, command, description in commands:
            print(f"{name:<10} {command:<20} - {description}")
        
        print("\n🌐 访问地址:")
        print("- 前端开发: http://localhost:3000")
        print("- 后端API: http://localhost:5000")
        
        print("\n📁 项目结构:")
        print("frontend/")
        print("├── src/")
        print("│   ├── app/          # Next.js App Router")
        print("│   ├── components/   # React组件")
        print("│   ├── styles/       # 样式文件")
        print("│   ├── utils/        # 工具函数")
        print("│   └── store/        # 状态管理")
        print("├── public/           # 静态资源")
        print("└── package.json      # 项目配置")

def main():
    print("Freedom.AI Next.js 项目管理器")
    print("=" * 50)
    
    manager = NextJSManager()
    
    # 检查Node.js环境
    if not manager.check_node_npm():
        return
    
    # 显示菜单
    while True:
        print("\n选择操作:")
        print("1. 安装依赖")
        print("2. 启动开发服务器")
        print("3. 构建生产版本")
        print("4. 启动生产服务器")
        print("5. 项目状态检查")
        print("6. 显示帮助")
        print("7. 退出")
        
        choice = input("\n请输入选择 (1-7): ").strip()
        
        if choice == '1':
            manager.install_dependencies()
            manager.create_env_file()
        elif choice == '2':
            manager.start_development_server()
        elif choice == '3':
            manager.build_production()
        elif choice == '4':
            manager.start_production_server()
        elif choice == '5':
            manager.show_project_status()
        elif choice == '6':
            manager.show_help()
        elif choice == '7':
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()
