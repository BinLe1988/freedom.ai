# 个人档案地点偏好和行业偏好保存问题调试指南

## 问题描述
用户反馈在个人档案页面中，地点偏好和行业偏好无法保存。

## 调试步骤

### 1. 检查后端API功能
后端API功能已经验证正常，可以正确保存和读取偏好数据。

### 2. 检查前端JavaScript功能
已添加详细的调试日志，请按以下步骤操作：

#### 步骤A: 访问个人档案页面
1. 登录系统
2. 访问 http://localhost:5001/profile
3. 打开浏览器开发者工具 (F12)
4. 切换到 Console 标签页

#### 步骤B: 测试添加偏好标签
1. 点击"编辑档案"按钮
2. 在"地点偏好"输入框中输入城市名称（如"北京"）
3. 按回车键添加
4. 重复添加几个地点
5. 在"行业偏好"输入框中输入行业名称（如"互联网"）
6. 按回车键添加
7. 重复添加几个行业

#### 步骤C: 检查控制台输出
在添加标签时，控制台应该没有错误信息。

#### 步骤D: 测试保存功能
1. 点击"保存"按钮
2. 观察控制台输出，应该看到以下调试信息：
   - "开始保存档案..."
   - "开始获取地点偏好..."
   - "找到的地点标签数量: X"
   - "开始获取行业偏好..."
   - "找到的行业标签数量: X"
   - "准备发送的数据: {...}"
   - "API响应状态: 200"
   - "API响应数据: {...}"

### 3. 常见问题排查

#### 问题1: 标签没有正确添加
**症状**: 按回车后没有出现标签
**可能原因**: 
- JavaScript事件监听器没有正确绑定
- 输入框ID不匹配

**解决方案**: 
检查控制台是否有JavaScript错误

#### 问题2: 标签添加了但获取不到
**症状**: 能看到标签，但保存时获取到空数组
**可能原因**: 
- CSS选择器不匹配
- DOM结构问题

**解决方案**: 
在控制台中手动执行：
```javascript
document.querySelectorAll('#locationPreferencesContainer .location-tag')
document.querySelectorAll('#industryPreferencesContainer .industry-tag')
```

#### 问题3: 数据发送了但没有保存
**症状**: API调用成功但数据没有持久化
**可能原因**: 
- 后端保存逻辑问题
- 数据格式问题

**解决方案**: 
检查API响应和数据导出功能

### 4. 手动验证步骤

如果自动保存有问题，可以手动验证：

1. 在控制台中执行：
```javascript
// 手动获取偏好
const locations = getCurrentLocationPreferences();
const industries = getCurrentIndustryPreferences();
console.log('地点偏好:', locations);
console.log('行业偏好:', industries);

// 手动发送保存请求
const testData = {
    full_name: '测试用户',
    location_preferences: ['北京', '上海'],
    industry_preferences: ['互联网', '人工智能']
};

fetch('/api/update_profile', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(testData)
}).then(r => r.json()).then(console.log);
```

### 5. 验证保存结果

保存后，可以通过以下方式验证：

1. 刷新页面，检查偏好是否显示
2. 访问 http://localhost:5001/api/export_data 查看导出数据
3. 再次进入编辑模式，检查标签是否正确加载

## 已知正常情况

- 后端API `/api/update_profile` 功能正常
- 数据库保存和读取功能正常
- 数据导出功能包含偏好数据
- JavaScript函数逻辑正确

## 需要用户反馈的信息

1. 浏览器控制台是否有错误信息？
2. 添加标签时是否能看到标签出现？
3. 点击保存时控制台输出了什么？
4. 保存后刷新页面，偏好是否显示？
5. 使用的是什么浏览器和版本？

## 临时解决方案

如果前端有问题，可以直接使用API：

```bash
curl -X POST http://localhost:5001/api/update_profile \
  -H "Content-Type: application/json" \
  -d '{
    "location_preferences": ["北京", "上海", "深圳"],
    "industry_preferences": ["互联网", "人工智能", "金融科技"]
  }'
```

## 联系支持

如果问题仍然存在，请提供：
1. 浏览器控制台的完整输出
2. 具体的操作步骤
3. 期望的结果和实际结果
