#!/usr/bin/env python3
"""
Freedom.AI 项目启动脚本
快速启动和配置整个系统
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """检查依赖项"""
    required_packages = [
        'flask',
        'openai',
        'asyncio'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        
        install = input("是否自动安装? (y/n): ")
        if install.lower() == 'y':
            for package in missing_packages:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package])
        else:
            print("请手动安装依赖包后重试")
            sys.exit(1)

def create_config():
    """创建配置文件"""
    config_path = Path('config.json')
    
    if not config_path.exists():
        config = {
            "openai_api_key": "",
            "web_port": 5001,
            "debug_mode": True,
            "data_directory": "./data",
            "log_level": "INFO"
        }
        
        import json
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"已创建配置文件: {config_path}")
        print("请编辑配置文件设置你的API密钥等信息")

def setup_directories():
    """设置目录结构"""
    directories = [
        'data',
        'logs',
        'web/static/css',
        'web/static/js',
        'web/static/images',
        'web/templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("目录结构已创建")

def run_calculator():
    """运行自由度计算器"""
    print("启动自由度计算器...")
    subprocess.run([sys.executable, 'tools/freedom_calculator.py', '--interactive'])

def run_web_app():
    """运行Web应用"""
    print("启动Web应用...")
    os.chdir('web')
    subprocess.run([sys.executable, 'app.py'])

def run_ai_demo():
    """运行AI智能体演示"""
    print("启动AI智能体演示...")
    subprocess.run([sys.executable, 'ai_agents_architecture.py'])

def show_help():
    """显示帮助信息"""
    help_text = """
Freedom.AI - 自由探索人生可能性

使用方法:
  python start.py [选项]

选项:
  --setup          初始化项目环境
  --calculator     运行自由度计算器
  --web           启动Web应用
  --ai-demo       运行AI智能体演示
  --help          显示此帮助信息

示例:
  python start.py --setup        # 首次使用，初始化环境
  python start.py --calculator   # 命令行自由度评估
  python start.py --web         # 启动Web界面
  python start.py --ai-demo     # 测试AI智能体

项目结构:
  ├── ai_agents_architecture.py  # AI智能体核心架构
  ├── tools/freedom_calculator.py # 自由度计算工具
  ├── web/app.py                 # Web应用
  ├── life_guide_framework.md    # 生活指南框架
  └── start.py                   # 启动脚本

更多信息请查看 README.md
"""
    print(help_text)

def main():
    parser = argparse.ArgumentParser(description='Freedom.AI 启动脚本')
    parser.add_argument('--setup', action='store_true', help='初始化项目环境')
    parser.add_argument('--calculator', action='store_true', help='运行自由度计算器')
    parser.add_argument('--web', action='store_true', help='启动Web应用')
    parser.add_argument('--ai-demo', action='store_true', help='运行AI智能体演示')
    parser.add_argument('--help-detail', action='store_true', help='显示详细帮助')
    
    args = parser.parse_args()
    
    if args.help_detail:
        show_help()
        return
    
    if args.setup:
        print("=== Freedom.AI 环境初始化 ===")
        check_dependencies()
        setup_directories()
        create_config()
        print("\n初始化完成！")
        print("下一步:")
        print("1. 编辑 config.json 设置API密钥")
        print("2. 运行 python start.py --calculator 进行自由度评估")
        print("3. 运行 python start.py --web 启动Web界面")
        return
    
    if args.calculator:
        run_calculator()
        return
    
    if args.web:
        check_dependencies()
        run_web_app()
        return
    
    if args.ai_demo:
        check_dependencies()
        run_ai_demo()
        return
    
    # 默认显示菜单
    print("=== Freedom.AI 自由探索系统 ===")
    print("1. 自由度评估 (命令行)")
    print("2. Web界面")
    print("3. AI智能体演示")
    print("4. 初始化环境")
    print("5. 帮助信息")
    print("0. 退出")
    
    while True:
        choice = input("\n请选择 (0-5): ").strip()
        
        if choice == '0':
            print("再见！")
            break
        elif choice == '1':
            run_calculator()
            break
        elif choice == '2':
            check_dependencies()
            run_web_app()
            break
        elif choice == '3':
            check_dependencies()
            run_ai_demo()
            break
        elif choice == '4':
            print("=== 环境初始化 ===")
            check_dependencies()
            setup_directories()
            create_config()
            print("初始化完成！")
        elif choice == '5':
            show_help()
        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main()
