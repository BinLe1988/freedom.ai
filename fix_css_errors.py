#!/usr/bin/env python3
"""
修复Next.js项目中的CSS错误
Fix CSS Errors in Next.js Project
"""

import os
import re
from pathlib import Path

class CSSErrorFixer:
    def __init__(self):
        self.frontend_dir = Path("frontend")
        self.fixes_applied = []
        
    def fix_globals_css(self):
        """修复globals.css中的错误"""
        print("🔧 修复globals.css...")
        
        globals_css = self.frontend_dir / "src/styles/globals.css"
        
        if not globals_css.exists():
            print("❌ globals.css文件不存在")
            return False
        
        try:
            with open(globals_css, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修复border-border错误
            if 'border-border' in content:
                content = content.replace('@apply border-border;', '@apply border-gray-600;')
                self.fixes_applied.append("修复border-border类")
            
            # 确保所有自定义颜色都在Tailwind配置中定义
            custom_colors = [
                'starry-dark', 'starry-secondary', 'starry-purple', 
                'starry-blue', 'starry-cyan', 'starry-gold'
            ]
            
            for color in custom_colors:
                if f'bg-{color}' in content or f'text-{color}' in content or f'border-{color}' in content:
                    # 这些颜色需要在tailwind.config.js中定义
                    pass
            
            # 写回文件
            with open(globals_css, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ globals.css修复完成")
            return True
            
        except Exception as e:
            print(f"❌ 修复globals.css失败: {e}")
            return False
    
    def check_tailwind_config(self):
        """检查并修复tailwind.config.js"""
        print("🔧 检查tailwind.config.js...")
        
        tailwind_config = self.frontend_dir / "tailwind.config.js"
        
        if not tailwind_config.exists():
            print("❌ tailwind.config.js文件不存在")
            return False
        
        try:
            with open(tailwind_config, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含自定义颜色
            required_colors = ['starry-dark', 'starry-secondary', 'starry-purple']
            
            for color in required_colors:
                if color not in content:
                    print(f"⚠️  缺少自定义颜色: {color}")
            
            print("✅ tailwind.config.js检查完成")
            return True
            
        except Exception as e:
            print(f"❌ 检查tailwind.config.js失败: {e}")
            return False
    
    def fix_component_imports(self):
        """修复组件导入错误"""
        print("🔧 检查组件导入...")
        
        # 检查所有TypeScript文件
        tsx_files = list(self.frontend_dir.rglob("*.tsx"))
        ts_files = list(self.frontend_dir.rglob("*.ts"))
        
        all_files = tsx_files + ts_files
        
        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查常见的导入错误
                if "from 'next/font/google'" in content and "import { Inter }" not in content:
                    # 修复字体导入
                    content = re.sub(
                        r"from 'next/font/google'",
                        "from 'next/font/google'\nconst inter = Inter({ subsets: ['latin'] })",
                        content
                    )
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    self.fixes_applied.append(f"修复字体导入: {file_path.name}")
                
            except Exception as e:
                print(f"⚠️  检查文件失败 {file_path}: {e}")
        
        print("✅ 组件导入检查完成")
    
    def create_missing_components(self):
        """创建缺失的组件"""
        print("🔧 创建缺失的组件...")
        
        # 检查是否需要创建TypeScript类型文件
        types_dir = self.frontend_dir / "src/types"
        if not types_dir.exists():
            types_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建基础类型文件
            types_content = '''// 基础类型定义
export interface User {
  id: string
  username: string
  email: string
  full_name?: string
  created_at?: string
  last_login?: string
}

export interface UserProfile {
  user_id: string
  full_name?: string
  bio?: string
  location?: string
  current_role?: string
  experience_years?: number
  skills?: string[]
  interests?: string[]
}

export interface UserPreferences {
  user_id: string
  preferred_work_type?: string
  location_preferences?: string[]
  industry_preferences?: string[]
  company_size_preference?: string
  salary_expectations?: {
    min?: number
    max?: number
    currency?: string
  }
}

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}
'''
            
            with open(types_dir / "index.ts", 'w', encoding='utf-8') as f:
                f.write(types_content)
            
            self.fixes_applied.append("创建基础类型文件")
        
        print("✅ 组件创建完成")
    
    def fix_css_classes(self):
        """修复CSS类名错误"""
        print("🔧 修复CSS类名...")
        
        # 常见的CSS类名修复映射
        css_fixes = {
            'border-border': 'border-gray-600',
            'text-border': 'text-gray-600',
            'bg-border': 'bg-gray-600',
        }
        
        # 查找所有CSS和样式文件
        css_files = list(self.frontend_dir.rglob("*.css"))
        tsx_files = list(self.frontend_dir.rglob("*.tsx"))
        
        all_files = css_files + tsx_files
        
        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 应用修复
                for old_class, new_class in css_fixes.items():
                    if old_class in content:
                        content = content.replace(old_class, new_class)
                        self.fixes_applied.append(f"修复{old_class} -> {new_class} in {file_path.name}")
                
                # 如果内容有变化，写回文件
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                
            except Exception as e:
                print(f"⚠️  修复文件失败 {file_path}: {e}")
        
        print("✅ CSS类名修复完成")
    
    def validate_project_structure(self):
        """验证项目结构"""
        print("🔍 验证项目结构...")
        
        required_files = [
            "package.json",
            "next.config.js",
            "tailwind.config.js",
            "tsconfig.json",
            "src/app/layout.tsx",
            "src/app/page.tsx",
            "src/styles/globals.css"
        ]
        
        missing_files = []
        
        for file_path in required_files:
            full_path = self.frontend_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
            else:
                print(f"✅ {file_path}")
        
        if missing_files:
            print("❌ 缺失文件:")
            for file_path in missing_files:
                print(f"   - {file_path}")
            return False
        
        print("✅ 项目结构验证完成")
        return True
    
    def run_all_fixes(self):
        """运行所有修复"""
        print("🚀 开始修复CSS错误...")
        print("=" * 50)
        
        # 检查frontend目录是否存在
        if not self.frontend_dir.exists():
            print("❌ frontend目录不存在，请先运行setup_nextjs.py")
            return False
        
        # 运行所有修复
        self.fix_globals_css()
        self.check_tailwind_config()
        self.fix_component_imports()
        self.create_missing_components()
        self.fix_css_classes()
        self.validate_project_structure()
        
        # 显示修复总结
        print("\n" + "=" * 50)
        print("🎉 修复完成!")
        
        if self.fixes_applied:
            print(f"\n✅ 应用的修复 ({len(self.fixes_applied)}个):")
            for fix in self.fixes_applied:
                print(f"   • {fix}")
        else:
            print("\n✅ 没有发现需要修复的问题")
        
        print("\n📝 下一步:")
        print("1. cd frontend")
        print("2. npm install")
        print("3. npm run dev")
        
        return True

def main():
    print("Freedom.AI CSS错误修复工具")
    print("=" * 50)
    
    fixer = CSSErrorFixer()
    
    choice = input("是否开始修复CSS错误? (y/n): ").strip().lower()
    
    if choice == 'y':
        fixer.run_all_fixes()
    else:
        print("取消修复")

if __name__ == "__main__":
    main()
