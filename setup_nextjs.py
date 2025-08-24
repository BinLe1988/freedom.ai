#!/usr/bin/env python3
"""
Freedom.AI Next.js 前端重构初始化脚本
Setup Next.js Frontend Refactoring
"""

import os
import subprocess
import json
from pathlib import Path

class NextJSSetup:
    def __init__(self):
        self.project_root = Path(".")
        self.frontend_dir = self.project_root / "frontend"
        
    def create_nextjs_project(self):
        """创建Next.js项目"""
        print("🚀 创建Next.js项目...")
        
        # 创建frontend目录
        self.frontend_dir.mkdir(exist_ok=True)
        
        # 创建package.json
        package_json = {
            "name": "freedom-ai-frontend",
            "version": "1.0.0",
            "description": "Freedom.AI Next.js Frontend",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
                "type-check": "tsc --noEmit"
            },
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@types/node": "^20.0.0",
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "typescript": "^5.0.0",
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0",
                "@headlessui/react": "^1.7.0",
                "@heroicons/react": "^2.0.0",
                "framer-motion": "^10.16.0",
                "axios": "^1.6.0",
                "js-cookie": "^3.0.5",
                "@types/js-cookie": "^3.0.6",
                "react-hook-form": "^7.47.0",
                "react-query": "^3.39.0",
                "zustand": "^4.4.0",
                "chart.js": "^4.4.0",
                "react-chartjs-2": "^5.2.0",
                "date-fns": "^2.30.0",
                "clsx": "^2.0.0",
                "lucide-react": "^0.292.0"
            },
            "devDependencies": {
                "eslint": "^8.0.0",
                "eslint-config-next": "^14.0.0",
                "@tailwindcss/forms": "^0.5.0",
                "@tailwindcss/typography": "^0.5.0"
            }
        }
        
        with open(self.frontend_dir / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        print("✅ package.json 已创建")
    
    def create_nextjs_config(self):
        """创建Next.js配置文件"""
        print("⚙️ 创建Next.js配置...")
        
        # next.config.js
        next_config = '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:5000/api/:path*',
      },
    ]
  },
  images: {
    domains: ['localhost'],
  },
}

module.exports = nextConfig
'''
        
        with open(self.frontend_dir / "next.config.js", "w") as f:
            f.write(next_config)
        
        # tsconfig.json
        tsconfig = {
            "compilerOptions": {
                "target": "es5",
                "lib": ["dom", "dom.iterable", "es6"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "plugins": [
                    {
                        "name": "next"
                    }
                ],
                "baseUrl": ".",
                "paths": {
                    "@/*": ["./src/*"],
                    "@/components/*": ["./src/components/*"],
                    "@/pages/*": ["./src/pages/*"],
                    "@/styles/*": ["./src/styles/*"],
                    "@/utils/*": ["./src/utils/*"],
                    "@/hooks/*": ["./src/hooks/*"],
                    "@/types/*": ["./src/types/*"],
                    "@/store/*": ["./src/store/*"]
                }
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
            "exclude": ["node_modules"]
        }
        
        with open(self.frontend_dir / "tsconfig.json", "w") as f:
            json.dump(tsconfig, f, indent=2)
        
        print("✅ Next.js配置文件已创建")
    
    def create_tailwind_config(self):
        """创建Tailwind CSS配置"""
        print("🎨 创建Tailwind CSS配置...")
        
        # tailwind.config.js
        tailwind_config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        starry: {
          dark: '#0a0a0f',
          secondary: '#1a1a2e',
          purple: '#6c5ce7',
          blue: '#74b9ff',
          cyan: '#00cec9',
          gold: '#fdcb6e',
        }
      },
      backgroundImage: {
        'starry-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'starry-secondary': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'starry-accent': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      },
      animation: {
        'float': 'float 3s ease-in-out infinite',
        'twinkle': 'twinkle 4s ease-in-out infinite alternate',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'slide-in-left': 'slide-in-left 0.8s ease-out',
        'slide-in-right': 'slide-in-right 0.8s ease-out',
        'fade-in-up': 'fade-in-up 0.8s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        twinkle: {
          '0%, 100%': { opacity: '0.3', transform: 'scale(1)' },
          '50%': { opacity: '1', transform: 'scale(1.2)' },
        },
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(108, 92, 231, 0.3)' },
          '50%': { boxShadow: '0 0 30px rgba(108, 92, 231, 0.6)' },
        },
        'slide-in-left': {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        'slide-in-right': {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        'fade-in-up': {
          '0%': { transform: 'translateY(30px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
'''
        
        with open(self.frontend_dir / "tailwind.config.js", "w") as f:
            f.write(tailwind_config)
        
        # postcss.config.js
        postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''
        
        with open(self.frontend_dir / "postcss.config.js", "w") as f:
            f.write(postcss_config)
        
        print("✅ Tailwind CSS配置已创建")
    
    def create_directory_structure(self):
        """创建目录结构"""
        print("📁 创建目录结构...")
        
        directories = [
            "src",
            "src/app",
            "src/app/(auth)",
            "src/app/(auth)/login",
            "src/app/(auth)/register",
            "src/app/(dashboard)",
            "src/app/(dashboard)/dashboard",
            "src/app/(dashboard)/profile",
            "src/app/(dashboard)/assessment",
            "src/app/(dashboard)/opportunities",
            "src/app/(dashboard)/learning",
            "src/components",
            "src/components/ui",
            "src/components/layout",
            "src/components/forms",
            "src/components/charts",
            "src/components/effects",
            "src/hooks",
            "src/utils",
            "src/types",
            "src/store",
            "src/styles",
            "public",
            "public/images",
            "public/icons"
        ]
        
        for directory in directories:
            (self.frontend_dir / directory).mkdir(parents=True, exist_ok=True)
        
        print("✅ 目录结构已创建")
    
    def create_basic_files(self):
        """创建基础文件"""
        print("📄 创建基础文件...")
        
        # .gitignore
        gitignore = '''# Dependencies
/node_modules
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts
'''
        
        with open(self.frontend_dir / ".gitignore", "w") as f:
            f.write(gitignore)
        
        # .env.local.example
        env_example = '''# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# App Configuration
NEXT_PUBLIC_APP_NAME=Freedom.AI
NEXT_PUBLIC_APP_VERSION=1.0.0
'''
        
        with open(self.frontend_dir / ".env.local.example", "w") as f:
            f.write(env_example)
        
        # README.md
        readme = '''# Freedom.AI Frontend

Next.js frontend for Freedom.AI - 自由探索人生可能性

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🛠️ Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Headless UI
- **Icons**: Heroicons & Lucide React
- **Animations**: Framer Motion
- **State Management**: Zustand
- **Data Fetching**: React Query
- **Forms**: React Hook Form
- **Charts**: Chart.js with React Chart.js 2

## 📁 Project Structure

```
src/
├── app/                 # Next.js App Router
├── components/          # Reusable components
├── hooks/              # Custom hooks
├── store/              # State management
├── types/              # TypeScript types
├── utils/              # Utility functions
└── styles/             # Global styles
```

## 🎨 Features

- ✨ Starry night theme with animations
- 📱 Responsive design
- 🌙 Dark mode support
- ⚡ Server-side rendering
- 🔒 Authentication system
- 📊 Interactive charts and dashboards
- 🎭 Smooth animations and transitions
'''
        
        with open(self.frontend_dir / "README.md", "w") as f:
            f.write(readme)
        
        print("✅ 基础文件已创建")
    
    def show_next_steps(self):
        """显示下一步操作"""
        print("\n" + "="*60)
        print("🎉 Next.js 项目初始化完成!")
        print("="*60)
        
        print("\n📋 下一步操作:")
        print("1. 进入frontend目录:")
        print("   cd frontend")
        
        print("\n2. 安装依赖:")
        print("   npm install")
        
        print("\n3. 启动开发服务器:")
        print("   npm run dev")
        
        print("\n4. 访问应用:")
        print("   http://localhost:3000")
        
        print("\n🛠️ 开发工具:")
        print("- npm run dev     # 开发模式")
        print("- npm run build   # 构建生产版本")
        print("- npm run start   # 启动生产服务器")
        print("- npm run lint    # 代码检查")
        
        print("\n📁 项目结构已创建，包含:")
        print("- ✅ Next.js 14 配置")
        print("- ✅ TypeScript 支持")
        print("- ✅ Tailwind CSS 样式")
        print("- ✅ 星空主题配置")
        print("- ✅ 完整的目录结构")
        
        print("\n🎨 特色功能:")
        print("- 🌟 星空主题和动画效果")
        print("- 📱 响应式设计")
        print("- ⚡ 服务端渲染")
        print("- 🔒 身份验证系统")
        print("- 📊 交互式图表")
        print("- 🎭 流畅的动画过渡")

def main():
    print("Freedom.AI Next.js 前端重构")
    print("="*50)
    
    setup = NextJSSetup()
    
    try:
        setup.create_nextjs_project()
        setup.create_nextjs_config()
        setup.create_tailwind_config()
        setup.create_directory_structure()
        setup.create_basic_files()
        setup.show_next_steps()
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
