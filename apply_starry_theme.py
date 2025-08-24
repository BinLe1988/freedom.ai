#!/usr/bin/env python3
"""
应用星空主题到所有模板
Apply Starry Night Theme to All Templates
"""

import os
import re
from pathlib import Path

class StarryThemeApplier:
    def __init__(self):
        self.templates_dir = Path("web/templates")
        self.static_dir = Path("web/static")
        self.theme_files_created = []
        
    def apply_theme_to_all_templates(self):
        """应用主题到所有模板"""
        print("=== 应用星空主题到所有模板 ===")
        
        # 确保静态文件存在
        self.ensure_static_files()
        
        # 获取所有HTML模板
        template_files = list(self.templates_dir.glob("*.html"))
        
        print(f"找到 {len(template_files)} 个模板文件")
        
        for template_file in template_files:
            if template_file.name.endswith('_starry.html'):
                continue  # 跳过已经是星空主题的文件
                
            print(f"\n处理模板: {template_file.name}")
            self.apply_theme_to_template(template_file)
        
        print(f"\n✅ 主题应用完成!")
        print(f"✅ 创建的主题文件: {len(self.theme_files_created)} 个")
        
    def ensure_static_files(self):
        """确保静态文件存在"""
        static_files = [
            'starry-night-theme.css',
            'starry-effects.js', 
            'theme-config.js'
        ]
        
        missing_files = []
        for file in static_files:
            if not (self.static_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"⚠️  缺少静态文件: {missing_files}")
            print("请确保已创建所有必要的CSS和JS文件")
        else:
            print("✅ 所有静态文件都存在")
    
    def apply_theme_to_template(self, template_file):
        """应用主题到单个模板"""
        try:
            # 读取原始模板
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 创建备份
            backup_file = template_file.with_suffix('.html.backup_theme')
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ 创建备份: {backup_file.name}")
            
            # 应用主题修改
            modified_content = self.modify_template_content(content, template_file.name)
            
            # 写入修改后的内容
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            print(f"  ✓ 主题应用成功: {template_file.name}")
            self.theme_files_created.append(template_file.name)
            
        except Exception as e:
            print(f"  ✗ 处理失败: {e}")
    
    def modify_template_content(self, content, filename):
        """修改模板内容以应用主题"""
        
        # 1. 添加Google Fonts链接
        google_fonts = '''    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'''
        
        if 'fonts.googleapis.com' not in content:
            content = content.replace(
                '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">',
                '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">\n' + google_fonts
            )
        
        # 2. 添加星空主题CSS
        theme_css = '''    
    <!-- 星空主题CSS -->
    <link href="{{ url_for('static', filename='starry-night-theme.css') }}" rel="stylesheet">'''
        
        if 'starry-night-theme.css' not in content:
            # 在</head>之前添加
            content = content.replace('</head>', theme_css + '\n</head>')
        
        # 3. 添加主题配置JavaScript
        theme_js = '''    
    <!-- 主题配置 -->
    <script src="{{ url_for('static', filename='theme-config.js') }}"></script>'''
        
        if 'theme-config.js' not in content:
            # 在</body>之前添加
            content = content.replace('</body>', theme_js + '\n</body>')
        
        # 4. 修改特定页面的样式
        content = self.apply_page_specific_modifications(content, filename)
        
        return content
    
    def apply_page_specific_modifications(self, content, filename):
        """应用页面特定的修改"""
        
        if filename == 'login.html':
            return self.modify_login_page(content)
        elif filename == 'register.html':
            return self.modify_register_page(content)
        elif filename == 'dashboard.html':
            return self.modify_dashboard_page(content)
        elif filename == 'profile.html':
            return self.modify_profile_page(content)
        elif filename == 'assessment.html':
            return self.modify_assessment_page(content)
        elif filename == 'opportunities.html':
            return self.modify_opportunities_page(content)
        elif filename == 'learning.html':
            return self.modify_learning_page(content)
        
        return content
    
    def modify_login_page(self, content):
        """修改登录页面"""
        # 添加登录页面特殊样式
        login_styles = '''
    <style>
        .login-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        
        .login-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: var(--shadow-card);
            backdrop-filter: blur(10px);
            max-width: 400px;
            width: 100%;
            animation: fadeInUp 0.8s ease-out;
        }
        
        .login-title {
            text-align: center;
            color: var(--text-light);
            margin-bottom: 2rem;
            font-weight: 600;
        }
        
        .login-title i {
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            display: block;
            margin-bottom: 1rem;
        }
    </style>'''
        
        if '.login-container' not in content:
            content = content.replace('</head>', login_styles + '\n</head>')
        
        return content
    
    def modify_register_page(self, content):
        """修改注册页面"""
        # 添加注册页面特殊样式
        register_styles = '''
    <style>
        .register-container {
            min-height: 100vh;
            padding: 2rem 0;
            position: relative;
        }
        
        .register-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: var(--shadow-card);
            backdrop-filter: blur(10px);
            animation: fadeInUp 0.8s ease-out;
        }
        
        .register-title {
            text-align: center;
            color: var(--text-light);
            margin-bottom: 2rem;
            font-weight: 600;
        }
        
        .register-title i {
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            display: block;
            margin-bottom: 1rem;
        }
    </style>'''
        
        if '.register-container' not in content:
            content = content.replace('</head>', register_styles + '\n</head>')
        
        return content
    
    def modify_dashboard_page(self, content):
        """修改仪表板页面"""
        # 仪表板已经有很好的样式，主要添加动画效果
        dashboard_enhancements = '''
    <style>
        .dashboard-card {
            animation: fadeInUp 0.6s ease-out;
        }
        
        .dashboard-card:nth-child(2) { animation-delay: 0.1s; }
        .dashboard-card:nth-child(3) { animation-delay: 0.2s; }
        .dashboard-card:nth-child(4) { animation-delay: 0.3s; }
        
        .freedom-score {
            animation: pulse 2s ease-in-out infinite;
        }
    </style>'''
        
        if '.dashboard-card' not in content:
            content = content.replace('</head>', dashboard_enhancements + '\n</head>')
        
        return content
    
    def modify_profile_page(self, content):
        """修改档案页面"""
        # 档案页面增强
        profile_enhancements = '''
    <style>
        .profile-section {
            animation: fadeInUp 0.6s ease-out;
        }
        
        .profile-section:nth-child(2) { animation-delay: 0.1s; }
        .profile-section:nth-child(3) { animation-delay: 0.2s; }
        
        .edit-btn {
            transition: all 0.3s ease;
        }
        
        .edit-btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-glow);
        }
    </style>'''
        
        if '.profile-section' not in content:
            content = content.replace('</head>', profile_enhancements + '\n</head>')
        
        return content
    
    def modify_assessment_page(self, content):
        """修改评估页面"""
        return content
    
    def modify_opportunities_page(self, content):
        """修改机会页面"""
        return content
    
    def modify_learning_page(self, content):
        """修改学习页面"""
        return content
    
    def create_theme_demo_page(self):
        """创建主题演示页面"""
        demo_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>星空主题演示 - Freedom.AI</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- 星空主题CSS -->
    <link href="{{ url_for('static', filename='starry-night-theme.css') }}" rel="stylesheet">
</head>
<body>
    <div class="container py-5">
        <div class="row">
            <div class="col-12 text-center mb-5">
                <h1 class="display-3 fw-bold text-light">
                    <i class="fas fa-star me-3"></i>星空主题演示
                </h1>
                <p class="lead text-muted">体验Freedom.AI的炫酷暗夜星空主题</p>
            </div>
        </div>
        
        <!-- 按钮演示 -->
        <div class="row mb-5">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-mouse-pointer me-2"></i>按钮样式</h3>
                    </div>
                    <div class="card-body text-center">
                        <button class="btn btn-primary me-2 mb-2">主要按钮</button>
                        <button class="btn btn-success me-2 mb-2">成功按钮</button>
                        <button class="btn btn-warning me-2 mb-2">警告按钮</button>
                        <button class="btn btn-secondary me-2 mb-2">次要按钮</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 卡片演示 -->
        <div class="row mb-5">
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-header">
                        <i class="fas fa-rocket me-2"></i>功能卡片
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">AI智能助手</h5>
                        <p class="card-text">体验AI驱动的智能分析和个性化建议。</p>
                        <button class="btn btn-primary">了解更多</button>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-header">
                        <i class="fas fa-chart-line me-2"></i>数据分析
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">自由度评估</h5>
                        <p class="card-text">五维度全面评估你的自由度水平。</p>
                        <button class="btn btn-success">开始评估</button>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-header">
                        <i class="fas fa-lightbulb me-2"></i>机会发现
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">智能推荐</h5>
                        <p class="card-text">发现适合你的机会和发展方向。</p>
                        <button class="btn btn-warning">探索机会</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 表单演示 -->
        <div class="row mb-5">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-edit me-2"></i>表单样式</h3>
                    </div>
                    <div class="card-body">
                        <form>
                            <div class="mb-3">
                                <label class="form-label">用户名</label>
                                <input type="text" class="form-control" placeholder="请输入用户名">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">邮箱</label>
                                <input type="email" class="form-control" placeholder="请输入邮箱">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">选择类型</label>
                                <select class="form-select">
                                    <option>选项一</option>
                                    <option>选项二</option>
                                    <option>选项三</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">描述</label>
                                <textarea class="form-control" rows="3" placeholder="请输入描述"></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary">提交</button>
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-tags me-2"></i>技能标签</h3>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <span class="skill-tag">JavaScript</span>
                            <span class="skill-tag">Python</span>
                            <span class="skill-tag">React</span>
                            <span class="skill-tag">Node.js</span>
                            <span class="skill-tag">AI/ML</span>
                            <span class="skill-tag">数据分析</span>
                            <span class="skill-tag">项目管理</span>
                            <span class="skill-tag">UI/UX设计</span>
                        </div>
                        
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            这是一个信息提示框
                        </div>
                        
                        <div class="alert alert-success">
                            <i class="fas fa-check-circle me-2"></i>
                            这是一个成功提示框
                        </div>
                        
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            这是一个警告提示框
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 统计卡片 -->
        <div class="row">
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-number">1,234</div>
                    <div class="stat-label">注册用户</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-number">5,678</div>
                    <div class="stat-label">完成评估</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-number">2,345</div>
                    <div class="stat-label">发现机会</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-number">98%</div>
                    <div class="stat-label">满意度</div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- 主题配置 -->
    <script src="{{ url_for('static', filename='theme-config.js') }}"></script>
</body>
</html>'''
        
        demo_file = self.templates_dir / 'theme_demo.html'
        with open(demo_file, 'w', encoding='utf-8') as f:
            f.write(demo_content)
        
        print(f"✅ 创建主题演示页面: {demo_file}")
        return demo_file

def main():
    applier = StarryThemeApplier()
    
    print("Freedom.AI 星空主题应用工具")
    print("=" * 50)
    
    choice = input("选择操作:\n1. 应用主题到所有模板\n2. 创建主题演示页面\n3. 全部执行\n请输入选择 (1/2/3): ").strip()
    
    if choice == '1':
        applier.apply_theme_to_all_templates()
    elif choice == '2':
        applier.create_theme_demo_page()
    elif choice == '3':
        applier.apply_theme_to_all_templates()
        applier.create_theme_demo_page()
    else:
        print("无效选择")
        return
    
    print("\n🎉 操作完成!")
    print("\n📝 使用说明:")
    print("1. 启动Web服务器: python3 web/app_with_auth.py")
    print("2. 访问任意页面查看星空主题效果")
    print("3. 访问 /theme_demo 查看主题演示")
    print("4. 如需还原，使用备份文件 (*.backup_theme)")

if __name__ == "__main__":
    main()
