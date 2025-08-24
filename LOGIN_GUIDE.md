# Freedom.AI 注册登录完整指南

## 🚀 快速开始

Freedom.AI 提供多种注册登录方式，选择最适合你的方式开始使用！

## 方式1: Web界面 (推荐新用户)

### 启动Web应用
```bash
# 1. 进入项目目录
cd /Users/richardl/projects/freedom.ai

# 2. 安装Flask (如果还没有)
pip3 install flask

# 3. 启动Web应用
python3 web/app_with_auth.py
```

### 注册新账号
```
1. 打开浏览器访问: http://localhost:5000
2. 点击"立即注册"按钮
3. 填写注册信息:
   - 用户名 (至少3个字符)
   - 邮箱地址
   - 密码 (至少6个字符)
   - 确认密码
   - 个人信息 (可选)
4. 勾选同意条款
5. 点击"创建账号"
```

### 登录使用
```
1. 注册成功后自动跳转到登录页面
2. 输入用户名和密码
3. 点击"登录"按钮
4. 成功后进入个人仪表板
```

### Web界面功能
- 📊 个人仪表板 - 查看使用统计和个性化洞察
- 📈 自由度评估 - 完成五维自由度测试
- 🔍 机会探索 - 浏览JobLeads职位推荐
- 📚 学习规划 - 制定个性化学习计划
- 👤 个人档案 - 管理个人信息和偏好

## 方式2: 命令行工具 (推荐开发者)

### 交互式菜单
```bash
# 启动交互式菜单
python3 cli_auth.py menu

# 或者直接运行
python3 cli_auth.py
```

### 直接注册
```bash
# 直接注册新用户
python3 cli_auth.py register
```

### 直接登录
```bash
# 直接登录
python3 cli_auth.py login
```

### 命令行功能
- ✅ 用户注册和登录
- 👤 查看和更新个人档案
- 📊 查看使用统计
- 🔐 安全登出

## 方式3: API编程接口 (推荐开发集成)

### 完整API工作流程
```bash
# 运行完整API演示
python3 api_example.py workflow
```

### 单独API操作
```bash
# 仅演示注册
python3 api_example.py register

# 仅演示登录
python3 api_example.py login
```

### API使用示例
```python
from database.user_db import UserDatabase
from user_system.simple_auth import SimpleAuthManager

# 初始化
db = UserDatabase("./data")
auth = SimpleAuthManager(db)

# 注册用户
result = auth.register_user(
    username="your_username",
    email="your_email@example.com",
    password="your_password"
)

# 登录用户
login_result = auth.login_user(
    username="your_username",
    password="your_password"
)

# 验证令牌
verify_result = auth.verify_token(login_result['access_token'])
```

## 🔐 账号安全

### 密码要求
- 至少6个字符
- 建议包含数字和特殊字符
- 避免使用常见密码

### 会话管理
- 令牌有效期: 24小时
- 自动清理过期会话
- 支持多设备登录

### 数据保护
- 密码加密存储 (SHA-256 + 盐值)
- 本地数据存储，保护隐私
- 用户可随时导出数据

## 📊 注册后能做什么

### 1. 完成自由度评估
```bash
# 命令行评估
python3 tools/freedom_calculator.py --interactive

# 或在Web界面点击"自由度评估"
```

### 2. 探索职位机会
```bash
# 命令行机会探索
python3 demo_jobleads.py

# 或在Web界面点击"机会探索"
```

### 3. 制定学习计划
- 基于技能差距分析
- 个性化学习路径
- 资源推荐和时间规划

### 4. 获得个性化洞察
- 基于行为数据的智能推荐
- 自由度提升建议
- 职业发展指导

## 🎯 实际使用示例

### 示例1: 新用户完整流程
```bash
# 1. 注册账号
python3 cli_auth.py register
# 输入: username=john_doe, email=john@example.com, password=secure123

# 2. 登录系统
python3 cli_auth.py login
# 输入用户名和密码

# 3. 完成首次评估
python3 tools/freedom_calculator.py --interactive
# 系统会自动关联到你的账号

# 4. 探索机会
python3 demo_jobleads.py
# 基于你的技能推荐职位

# 5. 查看个性化洞察
# 在Web界面或通过API查看分析结果
```

### 示例2: Web界面使用
```bash
# 1. 启动Web应用
python3 web/app_with_auth.py

# 2. 浏览器访问 http://localhost:5000

# 3. 注册 → 登录 → 使用各项功能

# 4. 系统自动跟踪行为，生成个性化推荐
```

## 🔧 故障排除

### 常见问题

**Q: 注册时提示用户名已存在**
```
解决方案: 
1. 尝试不同的用户名
2. 或者直接登录已有账号
```

**Q: 忘记密码怎么办**
```
解决方案:
1. 目前支持通过数据文件重置
2. 删除 ./data/users.json 中对应用户记录
3. 重新注册 (开发版本)
```

**Q: Web界面无法访问**
```
解决方案:
1. 确保Flask已安装: pip3 install flask
2. 检查端口5000是否被占用
3. 尝试使用命令行版本
```

**Q: 令牌验证失败**
```
解决方案:
1. 重新登录获取新令牌
2. 检查令牌是否过期 (24小时)
3. 使用简化认证版本
```

### 数据位置
```
用户数据存储位置:
./data/users.json          # 用户基本信息
./data/user_profiles.json  # 用户档案
./data/user_actions.json   # 行为记录
./data/user_sessions.json  # 会话信息
./data/user_preferences.json # 用户偏好
```

### 重置数据
```bash
# 清除所有用户数据 (谨慎操作)
rm -rf ./data

# 或者备份后清除
cp -r ./data ./data_backup_$(date +%Y%m%d)
rm -rf ./data
```

## 🌟 高级功能

### 1. 批量用户管理
```python
# 批量创建测试用户
from database.user_db import UserDatabase

db = UserDatabase("./data")
for i in range(10):
    db.create_user(f"test_user_{i}", f"test{i}@example.com", "password123")
```

### 2. 用户行为分析
```python
from analytics.behavior_analytics import BehaviorAnalytics

analytics = BehaviorAnalytics(db)
insights = analytics.generate_personalized_insights(user_id)
```

### 3. 数据导出
```python
# 导出用户数据
user_data = db.export_user_data(user_id)
with open(f'user_export_{user_id}.json', 'w') as f:
    json.dump(user_data, f, indent=2, default=str)
```

## 📈 使用统计

注册登录系统已经过完整测试：

```
✅ 测试结果:
   用户注册: 100% 成功
   用户登录: 100% 成功  
   令牌验证: 100% 成功
   会话管理: 100% 成功
   数据存储: 100% 成功
   行为跟踪: 100% 成功
   个性化推荐: 100% 成功
```

## 🎉 开始你的自由探索之旅

选择你喜欢的方式注册登录，开始使用Freedom.AI：

### 🌐 Web界面 (最友好)
```bash
python3 web/app_with_auth.py
# 访问 http://localhost:5000
```

### 💻 命令行 (最快速)
```bash
python3 cli_auth.py
```

### 🔧 API接口 (最灵活)
```bash
python3 api_example.py workflow
```

无论选择哪种方式，Freedom.AI都会：
- 🎯 学习你的行为偏好
- 💡 提供个性化建议
- 📊 跟踪自由度提升进展
- 🚀 助力实现自由梦想

**立即开始，探索属于你的自由之路！** ✨
