# 📁 Freedom.AI 项目结构

## 🏗️ 核心架构

```
freedom.ai/
├── 📄 README.md                    # 项目说明文档
├── 📄 LICENSE                      # 开源许可证
├── ⚙️ config.json                  # 项目配置文件
├── 📄 life_guide_framework.md      # 生活指南框架文档
├── 🤖 ai_agents_architecture.py    # AI智能体核心架构
├── 👤 user_manager.py              # 用户管理模块
│
├── 🗄️ database/                    # 数据库模块
│   └── user_db.py                  # 用户数据库操作
│
├── 👥 user_system/                 # 用户系统
│   ├── auth.py                     # 用户认证
│   ├── models.py                   # 数据模型
│   └── simple_auth.py              # 简单认证
│
├── 🛠️ tools/                       # 工具模块
│   └── freedom_calculator.py       # 自由度计算器
│
├── 🔗 integrations/                # 第三方集成
│   └── jobleads_api.py             # 工作机会API
│
├── 📊 analytics/                   # 数据分析
│   └── behavior_analytics.py       # 行为分析
│
├── 🌐 web/                         # Flask Web应用
│   ├── app.py                      # 基础Web应用
│   ├── app_with_auth.py            # 带认证的Web应用
│   ├── templates/                  # HTML模板
│   └── static/                     # 静态资源
│
├── ⚛️ frontend/                    # Next.js前端应用
│   ├── src/                        # 源代码
│   ├── public/                     # 公共资源
│   ├── package.json                # 依赖配置
│   ├── next.config.js              # Next.js配置
│   ├── tailwind.config.js          # Tailwind CSS配置
│   └── tsconfig.json               # TypeScript配置
│
├── 💾 data/                        # 数据存储
│   ├── users.json                  # 用户数据
│   ├── user_profiles.json          # 用户档案
│   ├── user_preferences.json       # 用户偏好
│   ├── user_sessions.json          # 用户会话
│   └── user_actions.json           # 用户行为
│
└── 🐍 venv/                        # Python虚拟环境
```

## 🎯 主要功能模块

### 🤖 AI智能体系统
- **决策支持AI**: 智能分析和决策建议
- **执行助手AI**: 任务自动化执行
- **学习伙伴AI**: 个性化学习路径
- **机会探索AI**: 市场机会发现

### 📊 自由度评估系统
- **财务自由度**: 被动收入/支出比例分析
- **时间自由度**: 工作时间灵活性评估
- **地理自由度**: 地点限制分析
- **技能自由度**: 技能可转移性评估
- **关系自由度**: 社交网络多样性

### 🌐 双端架构
- **Flask后端**: 提供API服务和数据处理
- **Next.js前端**: 现代化用户界面和交互体验

## 🚀 快速启动

### 后端服务
```bash
# 激活虚拟环境
source venv/bin/activate

# 启动Flask应用
python web/app_with_auth.py
```

### 前端应用
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📝 开发说明

- **Python版本**: 3.8+
- **Node.js版本**: 18+
- **主要技术栈**: Flask, Next.js, TypeScript, Tailwind CSS
- **数据存储**: JSON文件 (可扩展至数据库)
- **AI服务**: OpenAI API集成

## 🔧 配置文件

主要配置在 `config.json` 中：
- OpenAI API密钥
- Web服务端口
- 调试模式设置
- 数据目录路径
