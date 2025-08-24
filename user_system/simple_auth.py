#!/usr/bin/env python3
"""
简化版用户认证系统 (不依赖JWT)
Simplified User Authentication System (without JWT dependency)
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from functools import wraps
import os
import sys

# 导入数据库和模型
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.user_db import UserDatabase
from user_system.models import User, UserSession, ActionType

class SimpleAuthManager:
    """简化认证管理器"""
    
    def __init__(self, db: UserDatabase):
        self.db = db
        self.active_tokens = {}  # 内存中存储活跃令牌
        self.token_expiry_hours = 24
    
    def register_user(self, username: str, email: str, password: str, **kwargs) -> Dict[str, Any]:
        """用户注册"""
        try:
            # 验证输入
            if len(username) < 3:
                return {'success': False, 'error': '用户名至少需要3个字符'}
            
            if len(password) < 6:
                return {'success': False, 'error': '密码至少需要6个字符'}
            
            if '@' not in email:
                return {'success': False, 'error': '请输入有效的邮箱地址'}
            
            # 创建用户
            user = self.db.create_user(username, email, password, **kwargs)
            
            # 记录注册行为
            self.db.log_user_action(
                user.user_id,
                ActionType.LOGIN,
                {'action': 'register', 'method': 'email'}
            )
            
            return {
                'success': True,
                'user_id': user.user_id,
                'username': user.username,
                'message': '注册成功'
            }
            
        except ValueError as e:
            return {'success': False, 'error': str(e)}
        except Exception as e:
            return {'success': False, 'error': f'注册失败: {str(e)}'}
    
    def login_user(self, username: str, password: str, ip_address: str = None, 
                  user_agent: str = None) -> Dict[str, Any]:
        """用户登录"""
        try:
            # 认证用户
            user = self.db.authenticate_user(username, password)
            if not user:
                return {'success': False, 'error': '用户名或密码错误'}
            
            # 检查用户状态
            if user.status.value != 'active':
                return {'success': False, 'error': '账户已被禁用'}
            
            # 创建会话
            session = self.db.create_session(
                user.user_id,
                ip_address or 'unknown',
                user_agent or 'unknown'
            )
            
            # 生成简单令牌
            access_token = self._generate_simple_token(user.user_id, session.session_id)
            
            # 记录登录行为
            self.db.log_user_action(
                user.user_id,
                ActionType.LOGIN,
                {
                    'action': 'login',
                    'ip_address': ip_address,
                    'user_agent': user_agent,
                    'session_id': session.session_id
                },
                session_id=session.session_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            return {
                'success': True,
                'user_id': user.user_id,
                'username': user.username,
                'access_token': access_token,
                'session_id': session.session_id,
                'expires_in': self.token_expiry_hours * 3600,
                'message': '登录成功'
            }
            
        except Exception as e:
            return {'success': False, 'error': f'登录失败: {str(e)}'}
    
    def logout_user(self, session_id: str, user_id: str = None) -> Dict[str, Any]:
        """用户登出"""
        try:
            # 获取会话信息
            session = self.db.get_session(session_id)
            if not session:
                return {'success': False, 'error': '会话不存在'}
            
            # 记录登出行为
            self.db.log_user_action(
                session.user_id,
                ActionType.LOGOUT,
                {
                    'action': 'logout',
                    'session_id': session_id
                },
                session_id=session_id
            )
            
            # 标记会话为非活跃
            sessions_data = self.db._load_data(self.db.sessions_file)
            if session_id in sessions_data:
                sessions_data[session_id]['is_active'] = False
                self.db._save_data(self.db.sessions_file, sessions_data)
            
            # 从内存中移除令牌
            tokens_to_remove = [token for token, data in self.active_tokens.items() 
                              if data.get('session_id') == session_id]
            for token in tokens_to_remove:
                del self.active_tokens[token]
            
            return {'success': True, 'message': '登出成功'}
            
        except Exception as e:
            return {'success': False, 'error': f'登出失败: {str(e)}'}
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """验证访问令牌"""
        try:
            # 检查令牌是否存在
            if token not in self.active_tokens:
                return {'success': False, 'error': '无效的令牌'}
            
            token_data = self.active_tokens[token]
            
            # 检查令牌是否过期
            if datetime.now() > token_data['expires_at']:
                del self.active_tokens[token]
                return {'success': False, 'error': '令牌已过期'}
            
            user_id = token_data['user_id']
            session_id = token_data['session_id']
            
            # 检查用户是否存在
            user = self.db.get_user(user_id)
            if not user:
                return {'success': False, 'error': '用户不存在'}
            
            # 检查会话是否有效
            if session_id:
                session = self.db.get_session(session_id)
                if not session or not session.is_active:
                    return {'success': False, 'error': '会话已失效'}
                
                # 更新会话活动时间
                self.db.update_session_activity(session_id)
            
            return {
                'success': True,
                'user_id': user_id,
                'username': user.username,
                'session_id': session_id
            }
            
        except Exception as e:
            return {'success': False, 'error': f'令牌验证失败: {str(e)}'}
    
    def _generate_simple_token(self, user_id: str, session_id: str = None) -> str:
        """生成简单令牌"""
        # 生成随机令牌
        token = secrets.token_urlsafe(32)
        
        # 存储令牌信息
        self.active_tokens[token] = {
            'user_id': user_id,
            'session_id': session_id,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=self.token_expiry_hours)
        }
        
        return token
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> Dict[str, Any]:
        """修改密码"""
        try:
            user = self.db.get_user(user_id)
            if not user:
                return {'success': False, 'error': '用户不存在'}
            
            # 验证旧密码
            from user_system.models import verify_password
            if not verify_password(old_password, user.password_hash):
                return {'success': False, 'error': '原密码错误'}
            
            # 验证新密码
            if len(new_password) < 6:
                return {'success': False, 'error': '新密码至少需要6个字符'}
            
            # 更新密码
            from user_system.models import create_password_hash
            new_password_hash = create_password_hash(new_password)
            self.db.update_user(user_id, password_hash=new_password_hash)
            
            # 记录密码修改行为
            self.db.log_user_action(
                user_id,
                ActionType.PREFERENCE_UPDATE,
                {'action': 'change_password'}
            )
            
            return {'success': True, 'message': '密码修改成功'}
            
        except Exception as e:
            return {'success': False, 'error': f'密码修改失败: {str(e)}'}
    
    def cleanup_expired_tokens(self):
        """清理过期令牌"""
        current_time = datetime.now()
        expired_tokens = [
            token for token, data in self.active_tokens.items()
            if current_time > data['expires_at']
        ]
        
        for token in expired_tokens:
            del self.active_tokens[token]
        
        return len(expired_tokens)

def require_simple_auth(auth_manager: SimpleAuthManager):
    """简化认证装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 从请求中获取令牌 (这里需要根据具体框架调整)
            token = None
            
            # 尝试从不同来源获取令牌
            if len(args) > 0:
                request = args[0]
                
                # 从Authorization头获取
                if hasattr(request, 'headers'):
                    auth_header = request.headers.get('Authorization')
                    if auth_header and auth_header.startswith('Bearer '):
                        token = auth_header.split(' ')[1]
                
                # 从session获取 (Flask)
                if not token and hasattr(request, 'session'):
                    token = request.session.get('access_token')
            
            if not token:
                return {'success': False, 'error': '缺少认证令牌'}, 401
            
            # 验证令牌
            auth_result = auth_manager.verify_token(token)
            if not auth_result['success']:
                return auth_result, 401
            
            # 将用户信息添加到请求中
            kwargs['current_user'] = {
                'user_id': auth_result['user_id'],
                'username': auth_result['username'],
                'session_id': auth_result.get('session_id')
            }
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 使用示例
if __name__ == "__main__":
    # 初始化数据库和认证管理器
    db = UserDatabase("./test_data")
    auth = SimpleAuthManager(db)
    
    # 测试用户注册
    register_result = auth.register_user(
        username="simple_auth_user",
        email="simple@example.com",
        password="password123"
    )
    print(f"注册结果: {register_result}")
    
    if register_result['success']:
        # 测试用户登录
        login_result = auth.login_user(
            username="simple_auth_user",
            password="password123",
            ip_address="127.0.0.1",
            user_agent="Test Agent"
        )
        print(f"登录结果: {login_result}")
        
        if login_result['success']:
            # 测试令牌验证
            token = login_result['access_token']
            verify_result = auth.verify_token(token)
            print(f"令牌验证: {verify_result}")
            
            # 测试登出
            logout_result = auth.logout_user(
                login_result['session_id'],
                login_result['user_id']
            )
            print(f"登出结果: {logout_result}")
    
    print("简化认证系统测试完成")
