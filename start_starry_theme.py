#!/usr/bin/env python3
"""
Freedom.AI 星空主题快速启动
Quick Start for Starry Night Theme
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def show_theme_info():
    """显示主题信息"""
    print("🌟" * 25)
    print("   Freedom.AI 星空主题")
    print("   Starry Night Theme")
    print("🌟" * 25)
    
    print("\n✨ 主题特色:")
    print("🌌 动态星空背景")
    print("⭐ 粒子动画效果")
    print("🌠 流星划过动画")
    print("💫 鼠标轨迹光晕")
    print("🎨 渐变色彩设计")
    print("🎭 丰富交互动画")
    
    print("\n🎯 主要颜色:")
    print("🌑 主要暗色: #0a0a0f")
    print("🌌 次要暗色: #1a1a2e") 
    print("💜 强调紫色: #6c5ce7")
    print("💙 强调蓝色: #74b9ff")
    print("💚 强调青色: #00cec9")

def check_theme_files():
    """检查主题文件"""
    print("\n🔍 检查主题文件...")
    
    required_files = [
        "web/static/starry-night-theme.css",
        "web/static/starry-effects.js",
        "web/static/theme-config.js",
        "web/templates/theme_demo.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ 缺少文件: {missing_files}")
        print("请先运行 apply_starry_theme.py 来创建主题文件")
        return False
    
    print("\n✅ 所有主题文件都存在!")
    return True

def start_server():
    """启动Web服务器"""
    print("\n🚀 启动Web服务器...")
    
    try:
        # 启动服务器
        process = subprocess.Popen([
            sys.executable, "web/app_with_auth.py"
        ], cwd=os.getcwd())
        
        print("⏳ 等待服务器启动...")
        time.sleep(3)
        
        return process
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return None

def open_browser_tabs():
    """打开浏览器标签页"""
    print("\n🌐 打开浏览器...")
    
    urls = [
        ("主题演示", "http://localhost:5000/theme_demo"),
        ("首页", "http://localhost:5000/"),
        ("登录页面", "http://localhost:5000/login")
    ]
    
    for name, url in urls:
        try:
            webbrowser.open(url)
            print(f"✅ 打开 {name}: {url}")
            time.sleep(1)  # 避免同时打开太多标签
        except Exception as e:
            print(f"❌ 无法打开 {name}: {e}")

def show_usage_guide():
    """显示使用指南"""
    print("\n📖 使用指南:")
    print("=" * 50)
    
    print("\n🎮 页面导航:")
    print("• 主题演示: http://localhost:5000/theme_demo")
    print("• 首页: http://localhost:5000/")
    print("• 登录: http://localhost:5000/login")
    print("• 注册: http://localhost:5000/register")
    
    print("\n🎨 主题特效:")
    print("• 移动鼠标查看轨迹光晕效果")
    print("• 点击按钮查看星云爆炸效果")
    print("• 观察自动生成的流星动画")
    print("• 体验卡片悬停浮起效果")
    
    print("\n⚡ 交互功能:")
    print("• 按钮悬停: 发光和浮起")
    print("• 表单焦点: 发光边框")
    print("• 卡片动画: 浮动效果")
    print("• 滚动视差: 背景移动")
    
    print("\n🔧 调试工具:")
    print("• F12: 打开开发者工具")
    print("• Console: 查看动画日志")
    print("• Network: 检查资源加载")
    print("• Performance: 分析性能")

def show_customization_tips():
    """显示自定义提示"""
    print("\n🎨 自定义提示:")
    print("=" * 50)
    
    print("\n🌈 修改颜色:")
    print("编辑 web/static/starry-night-theme.css")
    print("修改 :root 中的 CSS 变量")
    
    print("\n⭐ 调整动画:")
    print("编辑 web/static/starry-effects.js")
    print("修改粒子数量和动画参数")
    
    print("\n🎭 主题配置:")
    print("编辑 web/static/theme-config.js")
    print("调整动画时长和缓动函数")

def main():
    """主函数"""
    show_theme_info()
    
    # 检查主题文件
    if not check_theme_files():
        return
    
    # 询问是否启动
    choice = input("\n🚀 是否启动Web服务器查看星空主题? (y/n): ").strip().lower()
    
    if choice != 'y':
        print("👋 再见!")
        return
    
    # 启动服务器
    process = start_server()
    if not process:
        return
    
    # 打开浏览器
    open_browser_tabs()
    
    # 显示使用指南
    show_usage_guide()
    show_customization_tips()
    
    print("\n" + "🌟" * 50)
    print("🎉 星空主题已启动!")
    print("🌌 享受你的星空之旅!")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("🌟" * 50)
    
    try:
        # 等待用户停止
        process.wait()
    except KeyboardInterrupt:
        print("\n\n⏹️  正在停止服务器...")
        process.terminate()
        process.wait()
        print("✅ 服务器已停止")
        print("👋 感谢使用 Freedom.AI 星空主题!")

if __name__ == "__main__":
    main()
