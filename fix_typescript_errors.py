#!/usr/bin/env python3
"""
修复TypeScript错误
Fix TypeScript Errors
"""

import os
import re
from pathlib import Path

def fix_motion_variants():
    """修复Framer Motion variants类型问题"""
    print("🔧 修复Framer Motion variants...")
    
    frontend_dir = Path("frontend")
    tsx_files = list(frontend_dir.rglob("*.tsx"))
    
    fixes_applied = []
    
    for file_path in tsx_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 修复variants定义中的transition问题
            # 将transition从variants对象中移除，放到motion组件的props中
            pattern = r'const\s+(\w+)\s*=\s*{\s*initial:\s*{[^}]+},\s*animate:\s*{[^}]+},\s*transition:\s*{[^}]+}\s*}'
            
            def replace_variant(match):
                variant_name = match.group(1)
                variant_content = match.group(0)
                
                # 提取transition部分
                transition_match = re.search(r'transition:\s*({[^}]+})', variant_content)
                if transition_match:
                    # 移除transition部分
                    new_variant = re.sub(r',\s*transition:\s*{[^}]+}', '', variant_content)
                    fixes_applied.append(f"修复 {variant_name} variants in {file_path.name}")
                    return new_variant
                
                return variant_content
            
            content = re.sub(pattern, replace_variant, content)
            
            # 修复motion组件中缺少transition的问题
            # 查找使用variants但没有transition的motion组件
            motion_pattern = r'<motion\.\w+[^>]*variants={(\w+)}(?![^>]*transition=)[^>]*>'
            
            def add_transition(match):
                variant_name = match.group(1)
                motion_tag = match.group(0)
                
                # 如果variants是fadeInUp等常见动画，添加默认transition
                if variant_name in ['fadeInUp', 'slideInLeft', 'slideInRight']:
                    if 'transition=' not in motion_tag:
                        # 在>之前添加transition
                        new_tag = motion_tag[:-1] + ' transition={{ duration: 0.6 }}>'
                        fixes_applied.append(f"添加transition到 {variant_name} in {file_path.name}")
                        return new_tag
                
                return motion_tag
            
            content = re.sub(motion_pattern, add_transition, content)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
        except Exception as e:
            print(f"⚠️  处理文件失败 {file_path}: {e}")
    
    if fixes_applied:
        print(f"✅ 应用了 {len(fixes_applied)} 个Framer Motion修复")
        for fix in fixes_applied[:5]:  # 只显示前5个
            print(f"   • {fix}")
        if len(fixes_applied) > 5:
            print(f"   ... 还有 {len(fixes_applied) - 5} 个修复")
    else:
        print("✅ 没有发现需要修复的Framer Motion问题")

def fix_heroicons_imports():
    """修复Heroicons导入问题"""
    print("🔧 修复Heroicons导入...")
    
    frontend_dir = Path("frontend")
    tsx_files = list(frontend_dir.rglob("*.tsx"))
    
    # 不存在的图标映射到存在的图标
    icon_mappings = {
        'BrainIcon': 'CpuChipIcon',
        'CompassIcon': 'MapIcon',
        'BoltIcon': 'LightningBoltIcon',
        'DatabaseIcon': 'CircleStackIcon',
    }
    
    fixes_applied = []
    
    for file_path in tsx_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 修复导入语句
            for old_icon, new_icon in icon_mappings.items():
                if old_icon in content:
                    content = content.replace(old_icon, new_icon)
                    fixes_applied.append(f"修复图标 {old_icon} -> {new_icon} in {file_path.name}")
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
        except Exception as e:
            print(f"⚠️  处理文件失败 {file_path}: {e}")
    
    if fixes_applied:
        print(f"✅ 应用了 {len(fixes_applied)} 个图标修复")
        for fix in fixes_applied:
            print(f"   • {fix}")
    else:
        print("✅ 没有发现需要修复的图标问题")

def fix_missing_types():
    """修复缺失的类型定义"""
    print("🔧 修复缺失的类型定义...")
    
    frontend_dir = Path("frontend")
    
    # 创建类型定义文件
    types_dir = frontend_dir / "src/types"
    types_dir.mkdir(exist_ok=True)
    
    # 创建全局类型定义
    global_types = '''// 全局类型定义
declare global {
  interface Window {
    gtag?: (...args: any[]) => void
  }
}

// React组件类型
export interface ComponentProps {
  children?: React.ReactNode
  className?: string
}

// 动画变体类型
export interface AnimationVariant {
  initial?: any
  animate?: any
  exit?: any
  whileHover?: any
  whileTap?: any
}

// API响应类型
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// 用户相关类型
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

export {}
'''
    
    global_types_file = types_dir / "global.d.ts"
    
    try:
        with open(global_types_file, 'w', encoding='utf-8') as f:
            f.write(global_types)
        
        print("✅ 创建全局类型定义文件")
        
    except Exception as e:
        print(f"❌ 创建类型定义失败: {e}")

def fix_import_paths():
    """修复导入路径问题"""
    print("🔧 修复导入路径...")
    
    frontend_dir = Path("frontend")
    tsx_files = list(frontend_dir.rglob("*.tsx"))
    ts_files = list(frontend_dir.rglob("*.ts"))
    
    all_files = tsx_files + ts_files
    fixes_applied = []
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 修复相对路径导入
            # 将 '../../../components' 这样的路径替换为 '@/components'
            relative_import_pattern = r"from ['\"](\.\./.*)['\"]"
            
            def fix_relative_import(match):
                import_path = match.group(1)
                
                # 转换为绝对路径
                if import_path.startswith('../'):
                    # 简单的路径转换逻辑
                    if 'components' in import_path:
                        new_path = '@/components' + import_path.split('components')[1]
                    elif 'utils' in import_path:
                        new_path = '@/utils' + import_path.split('utils')[1]
                    elif 'store' in import_path:
                        new_path = '@/store' + import_path.split('store')[1]
                    elif 'types' in import_path:
                        new_path = '@/types' + import_path.split('types')[1]
                    else:
                        return match.group(0)  # 不修改
                    
                    fixes_applied.append(f"修复导入路径 {import_path} -> {new_path} in {file_path.name}")
                    return f"from '{new_path}'"
                
                return match.group(0)
            
            content = re.sub(relative_import_pattern, fix_relative_import, content)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
        except Exception as e:
            print(f"⚠️  处理文件失败 {file_path}: {e}")
    
    if fixes_applied:
        print(f"✅ 应用了 {len(fixes_applied)} 个导入路径修复")
        for fix in fixes_applied[:3]:  # 只显示前3个
            print(f"   • {fix}")
        if len(fixes_applied) > 3:
            print(f"   ... 还有 {len(fixes_applied) - 3} 个修复")
    else:
        print("✅ 没有发现需要修复的导入路径问题")

def run_type_check():
    """运行类型检查"""
    print("🔍 运行TypeScript类型检查...")
    
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ frontend目录不存在")
        return False
    
    try:
        os.chdir(frontend_dir)
        
        import subprocess
        result = subprocess.run(['npm', 'run', 'type-check'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ TypeScript类型检查通过")
            return True
        else:
            print("❌ TypeScript类型检查失败")
            print("错误详情:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  类型检查超时")
        return False
    except Exception as e:
        print(f"❌ 类型检查失败: {e}")
        return False
    finally:
        os.chdir("..")

def main():
    print("🔧 TypeScript错误修复工具")
    print("=" * 50)
    
    print("选择操作:")
    print("1. 修复Framer Motion variants问题")
    print("2. 修复Heroicons导入问题")
    print("3. 修复缺失的类型定义")
    print("4. 修复导入路径问题")
    print("5. 运行类型检查")
    print("6. 全部执行")
    
    choice = input("\n请输入选择 (1-6): ").strip()
    
    if choice == '1':
        fix_motion_variants()
    elif choice == '2':
        fix_heroicons_imports()
    elif choice == '3':
        fix_missing_types()
    elif choice == '4':
        fix_import_paths()
    elif choice == '5':
        run_type_check()
    elif choice == '6':
        print("🚀 执行所有修复...")
        fix_heroicons_imports()
        fix_motion_variants()
        fix_missing_types()
        fix_import_paths()
        print("\n" + "=" * 50)
        print("🎉 所有修复完成！")
        print("\n🔍 运行最终类型检查...")
        run_type_check()
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()
