# Freedom.AI - 自由探索人生可能性

在寻找自由的路上能够做的事情 - 结合AI智能体实现自由生活指南

## 🎯 项目愿景

Freedom.AI 是一个AI驱动的生活指南系统，帮助用户在探索人生可能性的过程中实现经济独立和生活自由。通过四大AI智能体的协同工作，为用户提供个性化的自由度评估、机会发现、学习规划和执行指导。

## ✨ 核心特性

### 🤖 四大AI智能体

1. **决策支持AI** - 智能分析机会，提供数据驱动的决策建议
2. **执行助手AI** - 自动化任务执行，提高工作效率
3. **学习伙伴AI** - 个性化学习路径，持续技能提升
4. **机会探索AI** - 发现市场机会，创造收入来源

### 📊 五维自由度评估

- **财务自由度**: 被动收入/支出比例、应急基金、收入多样性
- **时间自由度**: 工作时间灵活性、假期自由、远程工作能力
- **地理自由度**: 工作地点限制、旅行频率、地理约束
- **技能自由度**: 可转移技能、学习能力、市场需求匹配
- **关系自由度**: 社交网络多样性、情感独立性

### 🎨 多种使用方式

- **命令行工具**: 快速自由度评估和计算
- **Web界面**: 直观的图表展示和交互体验
- **API接口**: 集成到其他应用和工具中

## 🚀 快速开始

### 1. 环境初始化

```bash
# 克隆项目
git clone <repository-url>
cd freedom.ai

# 初始化环境
python start.py --setup
```

### 2. 配置设置

编辑 `config.json` 文件：

```json
{
  "openai_api_key": "your-api-key-here",
  "web_port": 1,
  "debug_mode": true,
  "data_directory": "./data",
  "log_level": "INFO"
}
```

### 3. 开始使用

```bash
# 命令行自由度评估
python start.py --calculator

# 启动Web界面
python start.py --web

# AI智能体演示
python start.py --ai-demo
```

## 📁 项目结构

```
freedom.ai/
├── README.md                      # 项目说明
├── start.py                       # 启动脚本
├── config.json                    # 配置文件
├── life_guide_framework.md        # 生活指南框架
├── ai_agents_architecture.py      # AI智能体核心架构
├── tools/
│   └── freedom_calculator.py      # 自由度计算工具
├── web/
│   ├── app.py                     # Web应用
│   ├── templates/                 # HTML模板
│   │   ├── index.html            # 主页
│   │   └── assessment.html       # 评估页面
│   └── static/                    # 静态资源
├── data/                          # 数据存储
└── logs/                          # 日志文件
```

## 🎯 使用场景

### 场景1: 职场人士转型

**背景**: 30岁程序员，想要更多时间自由和地理自由

**使用流程**:
1. 完成自由度评估，发现时间和地理自由度较低
2. AI分析推荐远程工作和自由职业机会
3. 制定技能提升计划，学习高需求的远程工作技能
4. 逐步建立副业收入，最终实现工作方式转型

### 场景2: 创业者机会探索

**背景**: 有一定积蓄，寻找创业机会

**使用流程**:
1. 评估当前财务和技能状况
2. AI探索市场机会和趋势分析
3. 获得项目评估和风险分析
4. 制定执行计划和里程碑

### 场景3: 学生职业规划

**背景**: 大学生，规划未来职业发展

**使用流程**:
1. 评估当前技能和学习能力
2. AI推荐市场需求技能和学习路径
3. 发现实习和项目机会
4. 建立个人品牌和网络

## 🛠️ 技术架构

### 后端技术栈
- **Python 3.8+**: 核心开发语言
- **Flask**: Web框架
- **OpenAI API**: AI智能体实现
- **asyncio**: 异步处理

### 前端技术栈
- **Bootstrap 5**: UI框架
- **Chart.js**: 数据可视化
- **Font Awesome**: 图标库
- **原生JavaScript**: 交互逻辑

### 数据存储
- **JSON文件**: 配置和用户数据
- **Session**: 临时数据存储
- **可扩展**: 支持数据库集成

## 📈 自由度计算算法

### 财务自由度计算
```python
# 基础财务自由度 = 被动收入 / 月支出
basic_ratio = passive_income / monthly_expenses

# 应急基金覆盖月数
emergency_months = emergency_fund / monthly_expenses

# 收入多样性
income_diversity = active_income_sources / total_sources

# 综合财务自由度
financial_score = basic_ratio * 0.6 + emergency_months/6 * 0.3 + income_diversity * 0.1
```

### 综合自由度权重
- 财务自由: 35%
- 时间自由: 25%
- 地理自由: 20%
- 技能自由: 15%
- 关系自由: 5%

## 🤝 贡献指南

### 开发环境设置

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest tests/

# 代码格式化
black .
flake8 .
```

### 贡献流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📋 开发路线图

### v1.0 (当前版本)
- [x] 基础自由度评估系统
- [x] 四大AI智能体架构
- [x] Web界面和命令行工具
- [x] 基础机会发现和评估

### v1.1 (计划中)
- [ ] 用户数据持久化
- [ ] 历史趋势分析
- [ ] 社区功能和经验分享
- [ ] 移动端适配

### v2.0 (未来版本)
- [ ] 高级AI模型集成
- [ ] 实时市场数据接入
- [ ] 个性化推荐算法优化
- [ ] 多语言支持

## 🔒 隐私和安全

- **数据本地化**: 用户数据存储在本地，保护隐私
- **API安全**: OpenAI API密钥本地配置，不上传服务器
- **开源透明**: 所有代码开源，算法透明可审计
- **用户控制**: 用户完全控制自己的数据和评估结果

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- OpenAI 提供的强大AI能力
- Bootstrap 和 Chart.js 等开源项目
- 所有为自由生活理念贡献想法的朋友们

## 📞 联系方式

- 项目主页: [GitHub Repository]
- 问题反馈: [Issues]
- 讨论交流: [Discussions]

---

**Freedom.AI** - 让AI成为你探索自由人生的得力助手 🚀

> "自由不是想做什么就做什么，而是有能力选择不做什么。" - 让我们一起用AI的力量，创造更多选择的可能性。
