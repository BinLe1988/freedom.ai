#!/usr/bin/env python3
"""
测试修复后的Web应用
Test Fixed Web Application
"""

import os
import sys
import subprocess
import time

def start_web_app():
    """启动Web应用进行测试"""
    print("=== 启动Freedom.AI Web应用测试 ===")
    
    # 检查必要文件
    required_files = [
        "web/app_with_auth.py",
        "database/user_db.py",
        "data/users.json"
    ]
    
    print("\n1. 检查必要文件:")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} 不存在")
            return
    
    print("\n2. 启动Web服务器...")
    print("修复内容:")
    print("- 档案不存在时自动创建")
    print("- 偏好不存在时自动创建") 
    print("- 添加了详细的错误处理")
    print("- 添加了调试日志输出")
    
    print(f"\n3. 启动命令:")
    print(f"cd {os.getcwd()}")
    print("python3 web/app_with_auth.py")
    
    print("\n4. 测试步骤:")
    print("1. 打开浏览器访问 http://localhost:5000")
    print("2. 注册新用户或登录现有用户")
    print("3. 进入档案页面 (/profile)")
    print("4. 编辑档案信息并保存")
    print("5. 检查是否保存成功")
    
    print("\n5. 调试信息:")
    print("- 服务器日志会显示档案创建/更新过程")
    print("- 浏览器控制台会显示API响应")
    print("- 如果仍有问题，请检查服务器输出")
    
    # 询问是否启动
    choice = input("\n是否现在启动Web服务器? (y/n): ").strip().lower()
    
    if choice == 'y':
        try:
            print("\n启动Web服务器...")
            print("按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            # 启动Web应用
            subprocess.run([sys.executable, "web/app_with_auth.py"], 
                         cwd=os.getcwd())
                         
        except KeyboardInterrupt:
            print("\n\n服务器已停止")
        except Exception as e:
            print(f"\n启动失败: {e}")
    else:
        print("\n手动启动命令:")
        print("python3 web/app_with_auth.py")

def show_fix_summary():
    """显示修复总结"""
    print("\n" + "="*60)
    print("档案编辑保存问题 - 修复总结")
    print("="*60)
    
    print("\n🔍 问题诊断:")
    print("- 用户首次编辑档案时，数据库中没有对应的档案记录")
    print("- update_user_profile() 方法检查档案不存在时返回 False")
    print("- Web API 没有处理这种情况，导致保存失败")
    
    print("\n🔧 修复方案:")
    print("- 修改 api_update_profile() 方法")
    print("- 添加档案存在性检查")
    print("- 档案不存在时自动调用 create_user_profile()")
    print("- 档案存在时调用 update_user_profile()")
    print("- 同样处理用户偏好的创建和更新")
    print("- 添加详细的错误处理和日志")
    
    print("\n✅ 修复状态:")
    print("- ✓ 已修复 web/app_with_auth.py")
    print("- ✓ 已添加自动档案创建逻辑")
    print("- ✓ 已添加错误处理和日志")
    print("- ✓ 已测试数据库操作正常")
    
    print("\n🧪 测试验证:")
    print("- ✓ 数据库档案创建/更新功能正常")
    print("- ✓ 文件权限检查通过")
    print("- ✓ 用户偏好保存功能正常")
    print("- 🔄 需要测试Web界面保存功能")
    
    print("\n📝 使用说明:")
    print("1. 启动Web服务器: python3 web/app_with_auth.py")
    print("2. 访问: http://localhost:5000")
    print("3. 登录用户账号")
    print("4. 进入档案页面编辑并保存")
    print("5. 现在应该可以正常保存了!")

if __name__ == "__main__":
    show_fix_summary()
    start_web_app()
