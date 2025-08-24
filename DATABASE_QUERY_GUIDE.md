# 📊 Freedom.AI 数据库查询指南

## 🗄️ 数据库结构

Freedom.AI 使用基于JSON文件的数据存储系统，包含以下主要数据文件：

### 📁 数据文件结构
```
data/
├── users.json              # 用户基本信息
├── user_profiles.json      # 用户档案信息  
├── user_preferences.json   # 用户偏好设置
├── user_actions.json       # 用户行为记录
└── user_sessions.json      # 用户会话信息
```

## 🔍 查询方法

### 1. 使用Python API查询

#### 初始化数据库连接
```python
from database.user_db import UserDatabase

# 初始化数据库
db = UserDatabase("./data")
```

#### 用户查询
```python
# 根据用户ID查询
user = db.get_user("user_049273837421")
print(f"用户名: {user.username}")
print(f"邮箱: {user.email}")

# 根据用户名查询
user = db.get_user_by_username("test_cli_user")

# 根据邮箱查询
user = db.get_user_by_email("test@example.com")
```

#### 档案查询
```python
# 获取用户档案
profile = db.get_user_profile("user_049273837421")
if profile:
    print(f"姓名: {profile.full_name}")
    print(f"简介: {profile.bio}")
    print(f"技能: {profile.skills}")
    print(f"兴趣: {profile.interests}")
```

#### 偏好查询
```python
# 获取用户偏好
preferences = db.get_user_preferences("user_049273837421")
if preferences:
    print(f"工作类型: {preferences.preferred_work_type}")
    print(f"地点偏好: {preferences.location_preferences}")
    print(f"行业偏好: {preferences.industry_preferences}")
    print(f"薪资期望: {preferences.salary_expectations}")
```

#### 行为查询
```python
# 获取用户行为记录
actions = db.get_user_actions("user_049273837421", limit=10)
for action in actions:
    print(f"{action.timestamp}: {action.action_type.value}")
    print(f"详情: {action.details}")

# 按类型查询行为
from user_system.models import ActionType
login_actions = db.get_user_actions(
    "user_049273837421", 
    action_type=ActionType.LOGIN
)

# 按时间范围查询
from datetime import datetime, timedelta
recent_actions = db.get_user_actions(
    "user_049273837421",
    start_date=datetime.now() - timedelta(days=7)
)
```

#### 统计查询
```python
# 获取用户统计信息
stats = db.get_user_statistics("user_049273837421")
print(f"总操作数: {stats['total_actions']}")
print(f"7天内操作: {stats['recent_actions_7d']}")
print(f"行为分析: {stats['behavior_analysis']}")
```

### 2. 直接JSON文件查询

#### 查询所有用户
```python
import json

# 读取用户数据
with open("./data/users.json", 'r', encoding='utf-8') as f:
    users_data = json.load(f)

print(f"总用户数: {len(users_data)}")

# 遍历用户
for user_id, user_info in users_data.items():
    print(f"用户: {user_info['username']} ({user_id})")
    print(f"邮箱: {user_info['email']}")
    print(f"状态: {user_info['status']}")
```

#### 查询用户档案
```python
# 读取档案数据
with open("./data/user_profiles.json", 'r', encoding='utf-8') as f:
    profiles_data = json.load(f)

# 查询特定用户档案
user_id = "user_049273837421"
if user_id in profiles_data:
    profile = profiles_data[user_id]
    print(f"姓名: {profile.get('full_name', 'N/A')}")
    print(f"简介: {profile.get('bio', 'N/A')}")
    print(f"技能: {profile.get('skills', [])}")
```

#### 查询用户偏好
```python
# 读取偏好数据
with open("./data/user_preferences.json", 'r', encoding='utf-8') as f:
    preferences_data = json.load(f)

# 查询特定用户偏好
user_id = "user_049273837421"
if user_id in preferences_data:
    prefs = preferences_data[user_id]
    print(f"地点偏好: {prefs.get('location_preferences', [])}")
    print(f"行业偏好: {prefs.get('industry_preferences', [])}")
```

#### 查询用户行为
```python
# 读取行为数据
with open("./data/user_actions.json", 'r', encoding='utf-8') as f:
    actions_data = json.load(f)

# 用户行为统计
user_actions = {}
for action in actions_data['actions']:
    user_id = action['user_id']
    if user_id not in user_actions:
        user_actions[user_id] = []
    user_actions[user_id].append(action)

# 查询特定用户行为
user_id = "user_049273837421"
if user_id in user_actions:
    actions = user_actions[user_id]
    print(f"用户 {user_id} 的行为记录:")
    for action in actions[-5:]:  # 最近5条
        print(f"  {action['timestamp']}: {action['action_type']}")
```

## 🛠️ 查询工具

### 使用查询工具脚本

我们提供了几个查询工具脚本：

#### 1. 简单查询工具
```bash
python3 simple_db_query.py
```

#### 2. 完整查询工具
```bash
python3 database_query_guide.py
```

#### 3. 交互式查询
```bash
python3 database_query_guide.py
# 选择 "1. 交互式查询"
```

### 交互式查询命令

在交互式模式下，可以使用以下命令：

| 命令 | 说明 | 示例 |
|------|------|------|
| `users [数量]` | 查询用户列表 | `users 10` |
| `user <用户ID>` | 查询用户详情 | `user user_049273837421` |
| `actions <用户ID> [数量]` | 查询用户行为 | `actions user_049273837421 20` |
| `search <关键词>` | 搜索用户 | `search test` |
| `stats` | 整体统计 | `stats` |
| `export <用户ID> [文件]` | 导出数据 | `export user_049273837421 user_data.json` |

## 📊 常用查询示例

### 1. 用户统计查询
```python
import json
from collections import Counter

# 用户状态统计
with open("./data/users.json", 'r') as f:
    users = json.load(f)

status_count = Counter(user['status'] for user in users.values())
print("用户状态分布:", dict(status_count))

# 注册时间分布
from datetime import datetime
registration_dates = []
for user in users.values():
    if user.get('created_at'):
        date = datetime.fromisoformat(user['created_at']).date()
        registration_dates.append(date)

# 按月统计
monthly_registrations = Counter(date.strftime('%Y-%m') for date in registration_dates)
print("月度注册统计:", dict(monthly_registrations))
```

### 2. 档案完成度分析
```python
# 档案完成度统计
with open("./data/user_profiles.json", 'r') as f:
    profiles = json.load(f)

completion_stats = {
    'total': len(profiles),
    'has_name': sum(1 for p in profiles.values() if p.get('full_name')),
    'has_bio': sum(1 for p in profiles.values() if p.get('bio')),
    'has_skills': sum(1 for p in profiles.values() if p.get('skills')),
    'complete': sum(1 for p in profiles.values() 
                   if p.get('full_name') and p.get('bio') and p.get('skills'))
}

print("档案完成度统计:")
for key, value in completion_stats.items():
    if key != 'total':
        percentage = (value / completion_stats['total']) * 100
        print(f"  {key}: {value} ({percentage:.1f}%)")
```

### 3. 用户行为分析
```python
# 行为类型统计
with open("./data/user_actions.json", 'r') as f:
    actions_data = json.load(f)

action_types = Counter(action['action_type'] for action in actions_data['actions'])
print("行为类型分布:")
for action_type, count in action_types.most_common():
    print(f"  {action_type}: {count}")

# 活跃用户分析
from datetime import datetime, timedelta
recent_date = datetime.now() - timedelta(days=7)

active_users = set()
for action in actions_data['actions']:
    action_time = datetime.fromisoformat(action['timestamp'])
    if action_time > recent_date:
        active_users.add(action['user_id'])

print(f"7天内活跃用户数: {len(active_users)}")
```

### 4. 偏好分析
```python
# 地点偏好统计
with open("./data/user_preferences.json", 'r') as f:
    preferences = json.load(f)

location_prefs = []
industry_prefs = []

for prefs in preferences.values():
    if prefs.get('location_preferences'):
        location_prefs.extend(prefs['location_preferences'])
    if prefs.get('industry_preferences'):
        industry_prefs.extend(prefs['industry_preferences'])

location_count = Counter(location_prefs)
industry_count = Counter(industry_prefs)

print("热门地点偏好:")
for location, count in location_count.most_common(10):
    print(f"  {location}: {count}")

print("热门行业偏好:")
for industry, count in industry_count.most_common(10):
    print(f"  {industry}: {count}")
```

## 🔧 高级查询

### 1. 复合条件查询
```python
# 查询活跃且档案完整的用户
def find_active_complete_users():
    # 获取活跃用户
    with open("./data/users.json", 'r') as f:
        users = json.load(f)
    
    active_users = {uid for uid, user in users.items() 
                   if user['status'] == 'active'}
    
    # 获取档案完整的用户
    with open("./data/user_profiles.json", 'r') as f:
        profiles = json.load(f)
    
    complete_users = {uid for uid, profile in profiles.items()
                     if profile.get('full_name') and profile.get('bio')}
    
    # 交集
    target_users = active_users & complete_users
    
    return target_users

result = find_active_complete_users()
print(f"活跃且档案完整的用户: {len(result)} 个")
```

### 2. 时间序列分析
```python
# 用户注册趋势分析
from datetime import datetime
import matplotlib.pyplot as plt  # 需要安装: pip install matplotlib

def analyze_registration_trend():
    with open("./data/users.json", 'r') as f:
        users = json.load(f)
    
    # 提取注册日期
    dates = []
    for user in users.values():
        if user.get('created_at'):
            date = datetime.fromisoformat(user['created_at']).date()
            dates.append(date)
    
    # 按日统计
    from collections import defaultdict
    daily_count = defaultdict(int)
    for date in dates:
        daily_count[date] += 1
    
    # 排序
    sorted_dates = sorted(daily_count.items())
    
    return sorted_dates

# 使用示例
trend_data = analyze_registration_trend()
print("注册趋势数据:")
for date, count in trend_data[-10:]:  # 最近10天
    print(f"  {date}: {count} 人")
```

## 📈 数据导出

### 1. 导出用户数据
```python
def export_user_data(user_id, output_file):
    """导出单个用户的完整数据"""
    db = UserDatabase("./data")
    
    # 获取所有相关数据
    user = db.get_user(user_id)
    profile = db.get_user_profile(user_id)
    preferences = db.get_user_preferences(user_id)
    actions = db.get_user_actions(user_id, limit=1000)
    
    # 组织数据
    export_data = {
        'user_info': user.to_dict() if user else None,
        'profile': profile.__dict__ if profile else None,
        'preferences': preferences.__dict__ if preferences else None,
        'actions': [action.to_dict() for action in actions],
        'export_time': datetime.now().isoformat()
    }
    
    # 保存到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"用户数据已导出到: {output_file}")

# 使用示例
export_user_data("user_049273837421", "user_export.json")
```

### 2. 导出统计报告
```python
def generate_statistics_report():
    """生成统计报告"""
    report = {
        'generated_at': datetime.now().isoformat(),
        'user_statistics': {},
        'profile_statistics': {},
        'behavior_statistics': {},
        'preference_statistics': {}
    }
    
    # 用户统计
    with open("./data/users.json", 'r') as f:
        users = json.load(f)
    
    report['user_statistics'] = {
        'total_users': len(users),
        'active_users': sum(1 for u in users.values() if u['status'] == 'active'),
        'status_distribution': dict(Counter(u['status'] for u in users.values()))
    }
    
    # 档案统计
    with open("./data/user_profiles.json", 'r') as f:
        profiles = json.load(f)
    
    report['profile_statistics'] = {
        'total_profiles': len(profiles),
        'complete_profiles': sum(1 for p in profiles.values() 
                               if p.get('full_name') and p.get('bio')),
        'completion_rate': sum(1 for p in profiles.values() 
                             if p.get('full_name') and p.get('bio')) / len(profiles) * 100
    }
    
    # 保存报告
    with open("statistics_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    return report

# 生成报告
report = generate_statistics_report()
print("统计报告已生成: statistics_report.json")
```

## 🚀 快速开始

### 1. 基础查询
```bash
# 运行简单查询示例
python3 simple_db_query.py

# 运行完整查询工具
python3 database_query_guide.py
```

### 2. 交互式查询
```bash
python3 database_query_guide.py
# 选择 "1. 交互式查询"
# 输入命令如: users 10, user user_049273837421, stats
```

### 3. 自定义查询
```python
# 创建自己的查询脚本
from database.user_db import UserDatabase

db = UserDatabase("./data")

# 你的查询逻辑
user = db.get_user("your_user_id")
print(f"用户: {user.username}")
```

---

## 📞 技术支持

如果在数据库查询过程中遇到问题：

1. **检查数据文件**: 确保 `./data/` 目录下的JSON文件存在
2. **检查权限**: 确保有读取数据文件的权限
3. **查看日志**: 检查控制台输出的错误信息
4. **使用调试**: 在查询代码中添加 `print()` 语句调试

**数据库查询现在变得简单了！** 🎉📊
