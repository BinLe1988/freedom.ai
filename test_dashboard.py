#!/usr/bin/env python3
"""
测试Dashboard功能
Test Dashboard Functionality
"""

import os
import sys
import subprocess
import time
import webbrowser
from datetime import datetime

def test_dashboard():
    """测试dashboard功能"""
    print("=== Dashboard功能测试 ===")
    
    print("\n修复内容:")
    print("✓ 添加了完整的错误处理")
    print("✓ 为user_stats和insights提供默认值")
    print("✓ 添加了详细的调试日志")
    print("✓ 检查用户存在性")
    print("✓ 优雅处理各种异常情况")
    
    print("\n测试步骤:")
    print("1. 启动Web服务器")
    print("2. 访问 http://localhost:5000")
    print("3. 登录用户账号")
    print("4. 访问 /dashboard 页面")
    print("5. 检查页面是否正常显示")
    
    # 检查必要文件
    required_files = [
        "web/app_with_auth.py",
        "web/templates/dashboard.html",
        "database/user_db.py",
        "analytics/behavior_analytics.py"
    ]
    
    print("\n文件检查:")
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} 不存在")
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ 缺少必要文件，无法启动测试")
        return
    
    print("\n✅ 所有必要文件都存在")
    
    # 询问是否启动服务器
    choice = input("\n是否启动Web服务器进行测试? (y/n): ").strip().lower()
    
    if choice == 'y':
        print("\n🚀 启动Web服务器...")
        print("📝 注意观察服务器日志中的调试信息")
        print("🌐 服务器启动后会自动打开浏览器")
        print("⏹️  按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        try:
            # 启动Web服务器
            process = subprocess.Popen([
                sys.executable, "web/app_with_auth.py"
            ], cwd=os.getcwd())
            
            # 等待服务器启动
            time.sleep(3)
            
            # 打开浏览器
            try:
                webbrowser.open('http://localhost:5000')
                print("✓ 浏览器已打开")
            except:
                print("⚠️  无法自动打开浏览器，请手动访问 http://localhost:5000")
            
            # 等待用户操作
            process.wait()
            
        except KeyboardInterrupt:
            print("\n\n⏹️  服务器已停止")
            if 'process' in locals():
                process.terminate()
        except Exception as e:
            print(f"\n❌ 启动失败: {e}")
    else:
        print("\n手动启动命令:")
        print("python3 web/app_with_auth.py")
        print("\n然后访问: http://localhost:5000/dashboard")

def show_troubleshooting():
    """显示故障排除指南"""
    print("\n" + "="*60)
    print("Dashboard访问故障排除指南")
    print("="*60)
    
    print("\n🔍 常见问题和解决方案:")
    
    print("\n1. 500内部服务器错误:")
    print("   - 检查服务器控制台日志")
    print("   - 查看具体的错误信息")
    print("   - 确保所有依赖模块正常")
    
    print("\n2. 模板渲染错误:")
    print("   - 检查dashboard.html模板文件")
    print("   - 确保模板语法正确")
    print("   - 检查传递给模板的数据格式")
    
    print("\n3. 数据库相关错误:")
    print("   - 检查用户数据文件是否存在")
    print("   - 确保用户ID有效")
    print("   - 检查数据文件权限")
    
    print("\n4. 分析模块错误:")
    print("   - 检查analytics模块导入")
    print("   - 确保行为分析数据完整")
    print("   - 检查依赖的计算方法")
    
    print("\n🛠️ 调试方法:")
    print("1. 查看服务器控制台输出")
    print("2. 检查浏览器开发者工具")
    print("3. 查看网络请求状态")
    print("4. 检查数据文件内容")
    
    print("\n📞 如果问题仍然存在:")
    print("1. 复制完整的错误信息")
    print("2. 检查服务器日志")
    print("3. 确认用户登录状态")
    print("4. 尝试重新启动服务器")

if __name__ == "__main__":
    test_dashboard()
    show_troubleshooting()
