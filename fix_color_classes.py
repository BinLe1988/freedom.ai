#!/usr/bin/env python3
"""
修复颜色类名以匹配Tailwind配置
Fix Color Class Names to Match Tailwind Config
"""

import os
import re
from pathlib import Path

def fix_color_classes():
    """修复颜色类名"""
    print("🎨 修复颜色类名...")
    
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ frontend目录不存在")
        return False
    
    # 颜色映射：从错误的类名到正确的类名
    color_mappings = {
        # 背景色
        'bg-starry-dark': 'bg-gray-900',  # 使用标准颜色
        'bg-starry-secondary': 'bg-gray-800',
        'bg-starry-purple': 'bg-purple-600',
        'bg-starry-blue': 'bg-blue-500',
        'bg-starry-cyan': 'bg-cyan-500',
        'bg-starry-gold': 'bg-yellow-500',
        
        # 文本色
        'text-starry-dark': 'text-gray-900',
        'text-starry-secondary': 'text-gray-800',
        'text-starry-purple': 'text-purple-600',
        'text-starry-blue': 'text-blue-500',
        'text-starry-cyan': 'text-cyan-500',
        'text-starry-gold': 'text-yellow-500',
        
        # 边框色
        'border-starry-dark': 'border-gray-900',
        'border-starry-secondary': 'border-gray-800',
        'border-starry-purple': 'border-purple-600',
        'border-starry-blue': 'border-blue-500',
        'border-starry-cyan': 'border-cyan-500',
        'border-starry-gold': 'border-yellow-500',
    }
    
    # 查找所有相关文件
    file_patterns = ['**/*.css', '**/*.tsx', '**/*.ts', '**/*.js']
    all_files = []
    
    for pattern in file_patterns:
        all_files.extend(frontend_dir.rglob(pattern))
    
    fixes_applied = []
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 应用颜色映射
            for old_class, new_class in color_mappings.items():
                if old_class in content:
                    content = content.replace(old_class, new_class)
                    fixes_applied.append(f"{old_class} -> {new_class} in {file_path.name}")
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
        except Exception as e:
            print(f"⚠️  处理文件失败 {file_path}: {e}")
    
    if fixes_applied:
        print(f"✅ 应用了 {len(fixes_applied)} 个颜色修复:")
        for fix in fixes_applied[:10]:  # 只显示前10个
            print(f"   • {fix}")
        if len(fixes_applied) > 10:
            print(f"   ... 还有 {len(fixes_applied) - 10} 个修复")
    else:
        print("✅ 没有发现需要修复的颜色类名")
    
    return True

def create_simplified_globals_css():
    """创建简化的globals.css"""
    print("📝 创建简化的globals.css...")
    
    simplified_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

/* 星空主题全局样式 */
@layer base {
  :root {
    --starry-dark: #0a0a0f;
    --starry-secondary: #1a1a2e;
    --starry-purple: #6c5ce7;
    --starry-blue: #74b9ff;
    --starry-cyan: #00cec9;
    --starry-gold: #fdcb6e;
  }

  * {
    @apply border-gray-600;
  }

  body {
    @apply bg-gray-900 text-white font-sans;
    background: radial-gradient(ellipse at top, #1a1a2e 0%, #0a0a0f 100%);
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
  }

  /* 星空背景效果 */
  body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
      radial-gradient(2px 2px at 20px 30px, #fff, transparent),
      radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
      radial-gradient(1px 1px at 90px 40px, #fff, transparent),
      radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
      radial-gradient(2px 2px at 160px 30px, #fff, transparent);
    background-repeat: repeat;
    background-size: 200px 100px;
    animation: twinkle 4s ease-in-out infinite alternate;
    z-index: -1;
    opacity: 0.8;
    pointer-events: none;
  }

  /* 自定义滚动条 */
  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    @apply bg-gray-900;
  }

  ::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    @apply bg-purple-600;
  }

  /* 文本选择样式 */
  ::selection {
    background: rgba(108, 92, 231, 0.3);
    color: #ddd6fe;
  }
}

@layer components {
  /* 卡片组件 */
  .starry-card {
    @apply bg-gray-800/80 border border-purple-600/30 rounded-2xl backdrop-blur-lg;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
  }

  .starry-card:hover {
    @apply -translate-y-1 border-purple-600/50;
    box-shadow: 0 12px 40px rgba(108, 92, 231, 0.4);
  }

  /* 按钮组件 */
  .starry-button {
    @apply px-6 py-3 rounded-full font-semibold text-white transition-all duration-300;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);
    position: relative;
    overflow: hidden;
  }

  .starry-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
  }

  .starry-button:hover::before {
    left: 100%;
  }

  .starry-button:hover {
    @apply -translate-y-0.5;
    box-shadow: 0 8px 25px rgba(108, 92, 231, 0.6);
  }

  .starry-button-secondary {
    @apply starry-button;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
  }

  .starry-button-secondary:hover {
    box-shadow: 0 8px 25px rgba(79, 172, 254, 0.6);
  }

  /* 输入框组件 */
  .starry-input {
    @apply bg-gray-800/80 border border-purple-600/30 rounded-lg px-4 py-3 text-white placeholder-gray-400 backdrop-blur-lg;
    transition: all 0.3s ease;
  }

  .starry-input:focus {
    @apply border-purple-600 outline-none;
    box-shadow: 0 0 0 0.2rem rgba(108, 92, 231, 0.25);
  }

  /* 导航栏 */
  .starry-navbar {
    @apply bg-gray-800/95 backdrop-blur-lg border-b border-purple-600/30;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }

  /* 加载动画 */
  .loading-spinner {
    @apply w-10 h-10 border-4 border-purple-600/30 border-t-purple-600 rounded-full;
    animation: spin 1s linear infinite;
  }

  /* 发光效果 */
  .glow-effect {
    box-shadow: 0 0 20px rgba(108, 92, 231, 0.5);
    animation: pulse-glow 2s ease-in-out infinite;
  }

  /* 统计卡片 */
  .stat-card {
    @apply starry-card p-6 text-center;
    position: relative;
    overflow: hidden;
  }

  .stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  .stat-number {
    @apply text-4xl font-bold mb-2;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .stat-label {
    @apply text-gray-400 text-lg font-medium;
  }
}

@layer utilities {
  /* 文本渐变 */
  .text-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .text-gradient-secondary {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* 星云背景效果 */
  .nebula-bg {
    background: radial-gradient(ellipse at center, rgba(108, 92, 231, 0.3) 0%, transparent 70%);
    position: relative;
  }

  .nebula-bg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(ellipse at 30% 70%, rgba(116, 185, 255, 0.2) 0%, transparent 50%);
    pointer-events: none;
  }
}

/* 动画关键帧 */
@keyframes twinkle {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(108, 92, 231, 0.3); }
  50% { box-shadow: 0 0 30px rgba(108, 92, 231, 0.6); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .starry-card {
    @apply mx-2 rounded-xl;
  }
  
  .starry-button {
    @apply px-4 py-2 text-sm;
  }
  
  .stat-number {
    @apply text-2xl;
  }
}
'''
    
    globals_css_path = Path("frontend/src/styles/globals.css")
    
    try:
        with open(globals_css_path, 'w', encoding='utf-8') as f:
            f.write(simplified_css)
        
        print("✅ 简化的globals.css已创建")
        return True
        
    except Exception as e:
        print(f"❌ 创建globals.css失败: {e}")
        return False

def main():
    print("🎨 颜色类名修复工具")
    print("=" * 50)
    
    print("选择操作:")
    print("1. 修复现有颜色类名")
    print("2. 创建简化的globals.css")
    print("3. 全部执行")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == '1':
        fix_color_classes()
    elif choice == '2':
        create_simplified_globals_css()
    elif choice == '3':
        fix_color_classes()
        create_simplified_globals_css()
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()
