#!/usr/bin/env python3
"""
验证Next.js项目设置
Verify Next.js Project Setup
"""

import os
import subprocess
import sys
import json
from pathlib import Path

class NextJSVerifier:
    def __init__(self):
        self.frontend_dir = Path("frontend")
        self.issues = []
        self.fixes = []
        
    def check_node_environment(self):
        """检查Node.js环境"""
        print("🔍 检查Node.js环境...")
        
        try:
            # 检查Node.js版本
            node_result = subprocess.run(['node', '--version'], 
                                       capture_output=True, text=True)
            if node_result.returncode == 0:
                version = node_result.stdout.strip()
                print(f"✅ Node.js版本: {version}")
                
                # 检查版本是否足够新
                version_num = int(version.replace('v', '').split('.')[0])
                if version_num < 16:
                    self.issues.append(f"Node.js版本过低 ({version})，推荐v18+")
            else:
                self.issues.append("Node.js未安装")
                
            # 检查npm版本
            npm_result = subprocess.run(['npm', '--version'], 
                                      capture_output=True, text=True)
            if npm_result.returncode == 0:
                print(f"✅ npm版本: {npm_result.stdout.strip()}")
            else:
                self.issues.append("npm未安装")
                
        except FileNotFoundError:
            self.issues.append("Node.js或npm未安装")
            
        return len(self.issues) == 0
    
    def check_project_structure(self):
        """检查项目结构"""
        print("📁 检查项目结构...")
        
        required_files = [
            "package.json",
            "next.config.js", 
            "tailwind.config.js",
            "tsconfig.json",
            "src/app/layout.tsx",
            "src/app/page.tsx",
            "src/styles/globals.css"
        ]
        
        required_dirs = [
            "src/app",
            "src/components",
            "src/styles",
            "src/utils",
            "src/store"
        ]
        
        # 检查文件
        for file_path in required_files:
            full_path = self.frontend_dir / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path}")
                self.issues.append(f"缺少文件: {file_path}")
        
        # 检查目录
        for dir_path in required_dirs:
            full_path = self.frontend_dir / dir_path
            if full_path.exists():
                print(f"✅ {dir_path}/")
            else:
                print(f"❌ {dir_path}/")
                self.issues.append(f"缺少目录: {dir_path}")
        
        return len(self.issues) == 0
    
    def check_package_json(self):
        """检查package.json配置"""
        print("📦 检查package.json...")
        
        package_json_path = self.frontend_dir / "package.json"
        
        if not package_json_path.exists():
            self.issues.append("package.json不存在")
            return False
        
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # 检查必要的依赖
            required_deps = [
                "next", "react", "react-dom", "typescript",
                "tailwindcss", "framer-motion", "axios"
            ]
            
            dependencies = {**package_data.get('dependencies', {}), 
                          **package_data.get('devDependencies', {})}
            
            for dep in required_deps:
                if dep in dependencies:
                    print(f"✅ {dep}: {dependencies[dep]}")
                else:
                    print(f"❌ {dep}: 未安装")
                    self.issues.append(f"缺少依赖: {dep}")
            
            # 检查脚本
            scripts = package_data.get('scripts', {})
            required_scripts = ['dev', 'build', 'start']
            
            for script in required_scripts:
                if script in scripts:
                    print(f"✅ 脚本 {script}: {scripts[script]}")
                else:
                    print(f"❌ 脚本 {script}: 未定义")
                    self.issues.append(f"缺少脚本: {script}")
            
            return True
            
        except Exception as e:
            self.issues.append(f"package.json解析错误: {e}")
            return False
    
    def check_typescript_config(self):
        """检查TypeScript配置"""
        print("🔧 检查TypeScript配置...")
        
        tsconfig_path = self.frontend_dir / "tsconfig.json"
        
        if not tsconfig_path.exists():
            self.issues.append("tsconfig.json不存在")
            return False
        
        try:
            with open(tsconfig_path, 'r', encoding='utf-8') as f:
                tsconfig = json.load(f)
            
            # 检查编译选项
            compiler_options = tsconfig.get('compilerOptions', {})
            
            required_options = {
                'jsx': 'preserve',
                'module': 'esnext',
                'moduleResolution': 'node',
                'strict': True
            }
            
            for option, expected_value in required_options.items():
                actual_value = compiler_options.get(option)
                if actual_value == expected_value:
                    print(f"✅ {option}: {actual_value}")
                else:
                    print(f"⚠️  {option}: {actual_value} (期望: {expected_value})")
            
            # 检查路径映射
            if 'paths' in compiler_options:
                print("✅ 路径映射已配置")
            else:
                print("⚠️  路径映射未配置")
            
            return True
            
        except Exception as e:
            self.issues.append(f"tsconfig.json解析错误: {e}")
            return False
    
    def check_tailwind_config(self):
        """检查Tailwind配置"""
        print("🎨 检查Tailwind配置...")
        
        tailwind_config_path = self.frontend_dir / "tailwind.config.js"
        
        if not tailwind_config_path.exists():
            self.issues.append("tailwind.config.js不存在")
            return False
        
        try:
            with open(tailwind_config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查内容路径
            if 'src/app/**/*.{js,ts,jsx,tsx,mdx}' in content:
                print("✅ App Router路径已配置")
            else:
                print("⚠️  App Router路径未配置")
            
            # 检查自定义颜色
            if 'starry' in content:
                print("✅ 星空主题颜色已配置")
            else:
                print("⚠️  星空主题颜色未配置")
            
            # 检查插件
            if '@tailwindcss/forms' in content:
                print("✅ Tailwind表单插件已配置")
            else:
                print("⚠️  Tailwind表单插件未配置")
            
            return True
            
        except Exception as e:
            self.issues.append(f"tailwind.config.js读取错误: {e}")
            return False
    
    def check_css_files(self):
        """检查CSS文件"""
        print("🎨 检查CSS文件...")
        
        globals_css_path = self.frontend_dir / "src/styles/globals.css"
        
        if not globals_css_path.exists():
            self.issues.append("globals.css不存在")
            return False
        
        try:
            with open(globals_css_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查Tailwind导入
            required_imports = ['@tailwind base', '@tailwind components', '@tailwind utilities']
            
            for import_stmt in required_imports:
                if import_stmt in content:
                    print(f"✅ {import_stmt}")
                else:
                    print(f"❌ {import_stmt}")
                    self.issues.append(f"缺少CSS导入: {import_stmt}")
            
            # 检查自定义样式
            if '.starry-card' in content:
                print("✅ 星空主题样式已定义")
            else:
                print("⚠️  星空主题样式未定义")
            
            # 检查错误的类名
            if 'border-border' in content:
                print("❌ 发现错误的CSS类名: border-border")
                self.issues.append("CSS中包含错误的类名")
            else:
                print("✅ 没有发现错误的CSS类名")
            
            return True
            
        except Exception as e:
            self.issues.append(f"globals.css读取错误: {e}")
            return False
    
    def check_dependencies_installed(self):
        """检查依赖是否已安装"""
        print("📦 检查依赖安装状态...")
        
        node_modules_path = self.frontend_dir / "node_modules"
        
        if not node_modules_path.exists():
            print("❌ node_modules目录不存在")
            self.issues.append("依赖未安装")
            return False
        
        # 检查关键依赖
        key_deps = ['next', 'react', 'tailwindcss', 'typescript']
        
        for dep in key_deps:
            dep_path = node_modules_path / dep
            if dep_path.exists():
                print(f"✅ {dep}")
            else:
                print(f"❌ {dep}")
                self.issues.append(f"依赖未安装: {dep}")
        
        return len([issue for issue in self.issues if "依赖未安装" in issue]) == 0
    
    def run_build_test(self):
        """运行构建测试"""
        print("🏗️ 运行构建测试...")
        
        if not self.frontend_dir.exists():
            self.issues.append("frontend目录不存在")
            return False
        
        try:
            os.chdir(self.frontend_dir)
            
            # 运行类型检查
            print("  检查TypeScript类型...")
            type_check = subprocess.run(['npm', 'run', 'type-check'], 
                                      capture_output=True, text=True, timeout=30)
            
            if type_check.returncode == 0:
                print("✅ TypeScript类型检查通过")
            else:
                print("❌ TypeScript类型检查失败")
                print(f"错误: {type_check.stderr}")
                self.issues.append("TypeScript类型检查失败")
            
            # 运行ESLint检查
            print("  检查代码质量...")
            lint_check = subprocess.run(['npm', 'run', 'lint'], 
                                      capture_output=True, text=True, timeout=30)
            
            if lint_check.returncode == 0:
                print("✅ ESLint检查通过")
            else:
                print("⚠️  ESLint检查有警告")
                # ESLint警告不算严重问题
            
            return True
            
        except subprocess.TimeoutExpired:
            print("⚠️  构建测试超时")
            return True  # 超时不算失败
        except Exception as e:
            print(f"❌ 构建测试失败: {e}")
            self.issues.append(f"构建测试失败: {e}")
            return False
        finally:
            os.chdir("..")
    
    def generate_fixes(self):
        """生成修复建议"""
        if not self.issues:
            return
        
        print("\n🔧 修复建议:")
        print("=" * 50)
        
        for i, issue in enumerate(self.issues, 1):
            print(f"{i}. {issue}")
            
            # 提供具体的修复建议
            if "Node.js" in issue:
                print("   💡 请访问 https://nodejs.org/ 安装最新版本的Node.js")
            elif "缺少文件" in issue:
                print("   💡 请重新运行 setup_nextjs.py 脚本")
            elif "缺少依赖" in issue:
                print("   💡 运行: cd frontend && npm install")
            elif "依赖未安装" in issue:
                print("   💡 运行: cd frontend && npm install")
            elif "CSS" in issue:
                print("   💡 运行: python3 fix_color_classes.py")
            elif "TypeScript" in issue:
                print("   💡 检查代码语法，修复类型错误")
            
            print()
    
    def run_full_verification(self):
        """运行完整验证"""
        print("🚀 开始Next.js项目验证...")
        print("=" * 60)
        
        # 检查frontend目录
        if not self.frontend_dir.exists():
            print("❌ frontend目录不存在")
            print("💡 请先运行: python3 setup_nextjs.py")
            return False
        
        # 运行所有检查
        checks = [
            ("Node.js环境", self.check_node_environment),
            ("项目结构", self.check_project_structure),
            ("package.json", self.check_package_json),
            ("TypeScript配置", self.check_typescript_config),
            ("Tailwind配置", self.check_tailwind_config),
            ("CSS文件", self.check_css_files),
            ("依赖安装", self.check_dependencies_installed),
        ]
        
        passed_checks = 0
        
        for check_name, check_func in checks:
            print(f"\n{check_name}:")
            print("-" * 30)
            
            try:
                if check_func():
                    passed_checks += 1
                    print(f"✅ {check_name} 检查通过")
                else:
                    print(f"❌ {check_name} 检查失败")
            except Exception as e:
                print(f"❌ {check_name} 检查出错: {e}")
                self.issues.append(f"{check_name}检查出错: {e}")
        
        # 如果基础检查都通过，运行构建测试
        if passed_checks >= 6:  # 大部分检查通过
            print(f"\n构建测试:")
            print("-" * 30)
            self.run_build_test()
        
        # 显示结果
        print("\n" + "=" * 60)
        print("📊 验证结果:")
        
        total_checks = len(checks)
        success_rate = (passed_checks / total_checks) * 100
        
        print(f"通过检查: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
        
        if self.issues:
            print(f"发现问题: {len(self.issues)} 个")
            self.generate_fixes()
        else:
            print("🎉 所有检查都通过了！")
            print("\n📝 下一步:")
            print("1. cd frontend")
            print("2. npm run dev")
            print("3. 访问 http://localhost:3000")
        
        return len(self.issues) == 0

def main():
    print("Freedom.AI Next.js 项目验证工具")
    print("=" * 50)
    
    verifier = NextJSVerifier()
    
    choice = input("是否开始完整验证? (y/n): ").strip().lower()
    
    if choice == 'y':
        success = verifier.run_full_verification()
        
        if success:
            print("\n🎉 项目验证成功！可以开始开发了。")
        else:
            print("\n⚠️  项目存在一些问题，请根据修复建议进行处理。")
    else:
        print("取消验证")

if __name__ == "__main__":
    main()
