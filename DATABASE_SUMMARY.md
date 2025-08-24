# 📊 Freedom.AI 数据库查询总结

## 🎯 数据库概览

Freedom.AI 使用基于JSON文件的数据存储系统，当前包含：

### 📈 数据统计
- **👥 总用户数**: 40 个用户
- **✅ 活跃用户**: 40 个 (100% 活跃率)
- **📋 用户档案**: 11 个档案，7 个完整 (63.6% 完成率)
- **📊 行为记录**: 大量用户行为数据 (159KB)
- **⚙️ 偏好设置**: 丰富的用户偏好数据 (35KB)

## 🗄️ 数据文件结构

| 文件 | 大小 | 描述 | 状态 |
|------|------|------|------|
| `users.json` | 27KB | 用户基本信息 | ✅ |
| `user_profiles.json` | 12KB | 用户档案信息 | ✅ |
| `user_preferences.json` | 36KB | 用户偏好设置 | ✅ |
| `user_actions.json` | 159KB | 用户行为记录 | ✅ |
| `user_sessions.json` | 14KB | 用户会话信息 | ✅ |

## 🔍 查询方法

### 1. Python API 查询

#### 基础用户查询
```python
from database.user_db import UserDatabase

db = UserDatabase("./data")

# 查询用户
user = db.get_user("user_049273837421")
print(f"用户名: {user.username}")
print(f"邮箱: {user.email}")
print(f"状态: {user.status.value}")
```

#### 档案和偏好查询
```python
# 用户档案
profile = db.get_user_profile("user_049273837421")
if profile:
    print(f"姓名: {profile.full_name}")
    print(f"技能: {profile.skills}")

# 用户偏好
preferences = db.get_user_preferences("user_049273837421")
if preferences:
    print(f"地点偏好: {preferences.location_preferences}")
    print(f"行业偏好: {preferences.industry_preferences}")
```

#### 行为和统计查询
```python
# 用户行为
actions = db.get_user_actions("user_049273837421", limit=10)
for action in actions:
    print(f"{action.timestamp}: {action.action_type.value}")

# 用户统计
stats = db.get_user_statistics("user_049273837421")
print(f"总操作数: {stats['total_actions']}")
print(f"7天内操作: {stats['recent_actions_7d']}")
```

### 2. 直接JSON查询

#### 快速统计查询
```python
import json

# 用户总数
with open("./data/users.json", 'r') as f:
    users = json.load(f)
print(f"总用户数: {len(users)}")

# 档案完成率
with open("./data/user_profiles.json", 'r') as f:
    profiles = json.load(f)
completed = sum(1 for p in profiles.values() 
               if p.get('full_name') and p.get('bio'))
print(f"档案完成率: {completed/len(profiles)*100:.1f}%")
```

## 🛠️ 查询工具

### 可用的查询脚本

1. **简单查询工具**
   ```bash
   python3 simple_db_query.py
   ```
   - 显示基本统计信息
   - 查询示例用户数据
   - 展示数据结构

2. **完整查询工具**
   ```bash
   python3 database_query_guide.py
   ```
   - 交互式查询界面
   - 完整的查询功能
   - 数据导出功能

3. **交互式查询命令**
   - `users 10` - 查询前10个用户
   - `user user_049273837421` - 查询特定用户
   - `actions user_049273837421 20` - 查询用户行为
   - `search test` - 搜索用户
   - `stats` - 整体统计
   - `export user_049273837421` - 导出用户数据

## 📊 实际数据示例

### 示例用户数据
```
👤 用户ID: user_049273837421
   用户名: test_cli_user
   邮箱: test_cli@example.com
   状态: active
   注册时间: 2025-08-17 19:43:37

📋 档案信息:
   姓名: 更新测试
   简介: 测试更新
   位置: 更新后的城市
   技能: ['Python', 'AI', 'Web开发']

⚙️ 偏好设置:
   工作类型: remote
   地点偏好: ['北京', '上海']
   行业偏好: ['科技', 'AI']

📊 统计信息:
   总操作数: 1
   7天内操作: 1
```

## 🚀 快速开始

### 1. 基础查询
```bash
# 查看数据库概览
python3 simple_db_query.py

# 输出示例:
# 总用户数: 40
# 活跃用户: 40 (100%)
# 档案完成率: 63.6%
```

### 2. 交互式查询
```bash
python3 database_query_guide.py
# 选择 "1. 交互式查询"
# 输入命令进行查询
```

### 3. 自定义查询
```python
# 创建自定义查询脚本
from database.user_db import UserDatabase
import json

db = UserDatabase("./data")

# 查询所有活跃用户
with open("./data/users.json", 'r') as f:
    users = json.load(f)

active_users = [uid for uid, user in users.items() 
               if user['status'] == 'active']

print(f"活跃用户数: {len(active_users)}")

# 查询每个用户的详细信息
for user_id in active_users[:5]:  # 前5个
    user = db.get_user(user_id)
    print(f"用户: {user.username}")
```

## 📈 常用查询场景

### 1. 用户管理查询
- 查询所有用户列表
- 搜索特定用户
- 查看用户详细信息
- 分析用户活跃度

### 2. 档案分析查询
- 统计档案完成情况
- 分析用户技能分布
- 查看用户兴趣偏好
- 地理位置分析

### 3. 行为分析查询
- 用户行为轨迹分析
- 功能使用统计
- 活跃时间分析
- 用户留存分析

### 4. 偏好分析查询
- 工作类型偏好统计
- 地点偏好热力图
- 行业偏好分布
- 薪资期望分析

## 🔧 高级功能

### 数据导出
```python
# 导出单个用户完整数据
db.export_user_data("user_049273837421")

# 导出统计报告
# 生成包含所有统计信息的JSON报告
```

### 批量查询
```python
# 批量查询多个用户
user_ids = ["user_049273837421", "user_304...", "user_031..."]
for user_id in user_ids:
    user = db.get_user(user_id)
    profile = db.get_user_profile(user_id)
    print(f"{user.username}: {profile.full_name if profile else 'N/A'}")
```

### 条件筛选
```python
# 筛选满足条件的用户
def find_users_by_criteria():
    with open("./data/users.json", 'r') as f:
        users = json.load(f)
    
    # 筛选活跃用户
    active_users = {uid: user for uid, user in users.items() 
                   if user['status'] == 'active'}
    
    return active_users

result = find_users_by_criteria()
print(f"找到 {len(result)} 个活跃用户")
```

## 📞 技术支持

### 常见问题
1. **数据文件不存在**: 确保在项目根目录运行
2. **权限问题**: 检查文件读取权限
3. **编码问题**: 确保使用UTF-8编码
4. **内存问题**: 大数据量时考虑分批处理

### 调试技巧
- 使用 `print()` 输出中间结果
- 检查JSON文件格式是否正确
- 验证用户ID是否存在
- 查看错误堆栈信息

---

## 🎉 总结

Freedom.AI 的数据库查询系统提供了：

- 🔍 **灵活的查询接口** - 支持多种查询方式
- 📊 **丰富的数据统计** - 全面的用户和行为分析
- 🛠️ **便捷的查询工具** - 交互式和脚本化查询
- 📈 **实时数据洞察** - 用户行为和偏好分析
- 🚀 **高性能查询** - 基于JSON的快速数据访问

**现在你可以轻松查询和分析Freedom.AI的所有数据了！** 📊✨
