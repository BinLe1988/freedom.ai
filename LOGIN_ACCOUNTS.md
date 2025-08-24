# 🔑 Freedom.AI 登录账号信息

## 🎯 推荐使用的测试账号

### 1. 管理员账号
- **用户名**: `admin`
- **邮箱**: `admin@freedom.ai`
- **密码**: `admin123`
- **用途**: 管理员功能测试

### 2. 普通测试账号
- **用户名**: `test`
- **邮箱**: `test@example.com`
- **密码**: `123456`
- **用途**: 日常功能测试

### 3. 演示账号
- **用户名**: `demo`
- **邮箱**: `demo@freedom.ai`
- **密码**: `demo123`
- **用途**: 演示和展示

## 🌐 登录方式

### Next.js 前端登录
1. 启动前端服务器:
   ```bash
   cd frontend
   npm run dev
   ```

2. 访问登录页面: http://localhost:3000/login

3. 使用上述任一账号登录

### Flask 后端登录
1. 启动后端服务器:
   ```bash
   python3 web/app_with_auth.py
   ```

2. 访问登录页面: http://localhost:5000/login

3. 使用上述任一账号登录

## 📊 现有用户统计

- **总用户数**: 43个用户
- **活跃用户**: 43个 (100%)
- **最新创建**: admin, test, demo (刚刚创建)

## 🔧 用户管理

### 查看所有用户
```bash
python3 user_manager.py
```

### 创建新用户
```bash
python3 user_manager.py
# 选择 "2. 创建测试用户"
```

### 重置密码
```bash
python3 user_manager.py
# 选择 "3. 重置用户密码"
```

### 验证登录
```bash
python3 user_manager.py
# 选择 "4. 验证登录"
```

## 🚀 快速测试

### 测试Next.js登录
```bash
# 1. 启动前端
cd frontend && npm run dev

# 2. 访问 http://localhost:3000/login

# 3. 使用以下账号登录:
用户名: test
密码: 123456
```

### 测试Flask登录
```bash
# 1. 启动后端
python3 web/app_with_auth.py

# 2. 访问 http://localhost:5000/login

# 3. 使用以下账号登录:
用户名: admin
密码: admin123
```

## 🔐 密码安全

- 所有密码都经过SHA256+盐值加密存储
- 测试环境使用简单密码便于测试
- 生产环境请使用强密码

## 📝 注意事项

1. **测试账号**: 这些是测试账号，仅用于开发和测试
2. **数据持久化**: 用户数据存储在 `data/users.json` 文件中
3. **会话管理**: 登录后会创建会话，存储在 `data/user_sessions.json`
4. **权限控制**: 目前所有用户都有相同权限

## 🛠️ 开发建议

### 前端开发
- 使用 `test` 账号进行日常开发测试
- 使用 `admin` 账号测试管理功能
- 使用 `demo` 账号进行演示

### 后端开发
- 可以通过用户管理工具创建更多测试用户
- 支持用户名或邮箱登录
- 密码验证使用安全的哈希算法

## 🎯 下一步

1. **启动应用**: 选择前端或后端进行测试
2. **登录测试**: 使用推荐的测试账号
3. **功能测试**: 测试各种功能模块
4. **用户管理**: 根据需要创建更多测试用户

---

**快速登录测试账号**: `test` / `123456` 🚀
