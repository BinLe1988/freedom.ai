#!/usr/bin/env python3
"""
用户认证和会话管理系统
User Authentication and Session Management
"""

# 简化JWT导入
import sys
import os

# 确保能正确导入PyJWT
try:
    # 清理可能的模块缓存问题
    if 'jwt' in sys.modules:
        del sys.modules['jwt']
    
    # 直接导入PyJWT
    import jwt
    # 验证是否是正确的PyJWT
    if not hasattr(jwt, 'encode') or not hasattr(jwt, 'decode'):
        raise ImportError("JWT模块不完整")
        
except ImportError:
    print("❌ JWT导入失败，请检查PyJWT安装")
    raise

import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from typing import List
from functools import wraps

# 导入数据库和模型
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.user_db import UserDatabase
from user_system.models import User, UserSession, ActionType

class AuthManager:
    """认证管理器"""
    
    def __init__(self, db: UserDatabase, secret_key: str = None):
        self.db = db
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.token_expiry_hours = 24
        self.refresh_token_expiry_days = 30
    
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
            
            # 生成JWT令牌
            access_token = self._generate_access_token(user.user_id, session.session_id)
            refresh_token = self._generate_refresh_token(user.user_id)
            
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
                'refresh_token': refresh_token,
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
            
            # 标记会话为非活跃 (软删除)
            sessions_data = self.db._load_data(self.db.sessions_file)
            if session_id in sessions_data:
                sessions_data[session_id]['is_active'] = False
                self.db._save_data(self.db.sessions_file, sessions_data)
            
            return {'success': True, 'message': '登出成功'}
            
        except Exception as e:
            return {'success': False, 'error': f'登出失败: {str(e)}'}
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """刷新访问令牌"""
        try:
            # 验证刷新令牌
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            token_type = payload.get('type')
            
            if token_type != 'refresh':
                return {'success': False, 'error': '无效的刷新令牌'}
            
            # 检查用户是否存在
            user = self.db.get_user(user_id)
            if not user:
                return {'success': False, 'error': '用户不存在'}
            
            # 生成新的访问令牌
            access_token = self._generate_access_token(user_id)
            
            return {
                'success': True,
                'access_token': access_token,
                'expires_in': self.token_expiry_hours * 3600
            }
            
        except jwt.ExpiredSignatureError:
            return {'success': False, 'error': '刷新令牌已过期'}
        except jwt.InvalidTokenError:
            return {'success': False, 'error': '无效的刷新令牌'}
        except Exception as e:
            return {'success': False, 'error': f'令牌刷新失败: {str(e)}'}
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """验证访问令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            session_id = payload.get('session_id')
            token_type = payload.get('type')
            
            if token_type != 'access':
                return {'success': False, 'error': '无效的令牌类型'}
            
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
            
        except jwt.ExpiredSignatureError:
            return {'success': False, 'error': '令牌已过期'}
        except jwt.InvalidTokenError:
            return {'success': False, 'error': '无效的令牌'}
        except Exception as e:
            return {'success': False, 'error': f'令牌验证失败: {str(e)}'}
    
    def _generate_access_token(self, user_id: str, session_id: str = None) -> str:
        """生成访问令牌"""
        payload = {
            'user_id': user_id,
            'session_id': session_id,
            'type': 'access',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def _generate_refresh_token(self, user_id: str) -> str:
        """生成刷新令牌"""
        payload = {
            'user_id': user_id,
            'type': 'refresh',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=self.refresh_token_expiry_days)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
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
    
    def reset_password(self, email: str) -> Dict[str, Any]:
        """重置密码 (发送重置链接)"""
        try:
            user = self.db.get_user_by_email(email)
            if not user:
                # 为了安全，不透露用户是否存在
                return {'success': True, 'message': '如果邮箱存在，重置链接已发送'}
            
            # 生成重置令牌
            reset_token = self._generate_reset_token(user.user_id)
            
            # 在实际应用中，这里应该发送邮件
            # 现在只是记录行为
            self.db.log_user_action(
                user.user_id,
                ActionType.PREFERENCE_UPDATE,
                {
                    'action': 'password_reset_request',
                    'reset_token': reset_token  # 实际应用中不应该记录令牌
                }
            )
            
            return {
                'success': True,
                'message': '重置链接已发送到您的邮箱',
                'reset_token': reset_token  # 仅用于演示
            }
            
        except Exception as e:
            return {'success': False, 'error': f'密码重置失败: {str(e)}'}
    
    def _generate_reset_token(self, user_id: str) -> str:
        """生成密码重置令牌"""
        payload = {
            'user_id': user_id,
            'type': 'reset',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=1)  # 1小时有效期
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def confirm_password_reset(self, reset_token: str, new_password: str) -> Dict[str, Any]:
        """确认密码重置"""
        try:
            # 验证重置令牌
            payload = jwt.decode(reset_token, self.secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            token_type = payload.get('type')
            
            if token_type != 'reset':
                return {'success': False, 'error': '无效的重置令牌'}
            
            # 验证新密码
            if len(new_password) < 6:
                return {'success': False, 'error': '密码至少需要6个字符'}
            
            # 更新密码
            from user_system.models import create_password_hash
            new_password_hash = create_password_hash(new_password)
            self.db.update_user(user_id, password_hash=new_password_hash)
            
            # 记录密码重置行为
            self.db.log_user_action(
                user_id,
                ActionType.PREFERENCE_UPDATE,
                {'action': 'password_reset_confirmed'}
            )
            
            return {'success': True, 'message': '密码重置成功'}
            
        except jwt.ExpiredSignatureError:
            return {'success': False, 'error': '重置链接已过期'}
        except jwt.InvalidTokenError:
            return {'success': False, 'error': '无效的重置链接'}
        except Exception as e:
            return {'success': False, 'error': f'密码重置失败: {str(e)}'}

def require_auth(auth_manager: AuthManager):
    """认证装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 这里需要根据具体的Web框架来实现
            # 以下是一个通用的示例
            
            # 从请求头获取令牌
            token = None
            if hasattr(args[0], 'headers'):  # Flask request对象
                auth_header = args[0].headers.get('Authorization')
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
            
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

class SessionManager:
    """会话管理器"""
    
    def __init__(self, db: UserDatabase):
        self.db = db
    
    def get_active_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户的活跃会话"""
        sessions_data = self.db._load_data(self.db.sessions_file)
        active_sessions = []
        
        for session_id, session_data in sessions_data.items():
            if (session_data['user_id'] == user_id and 
                session_data.get('is_active', True)):
                
                # 检查是否过期
                last_activity = datetime.fromisoformat(session_data['last_activity'])
                if datetime.now() - last_activity <= timedelta(hours=24):
                    active_sessions.append({
                        'session_id': session_id,
                        'created_at': session_data['created_at'],
                        'last_activity': session_data['last_activity'],
                        'ip_address': session_data['ip_address'],
                        'user_agent': session_data['user_agent']
                    })
        
        return active_sessions
    
    def terminate_session(self, session_id: str, user_id: str) -> bool:
        """终止指定会话"""
        session = self.db.get_session(session_id)
        if session and session.user_id == user_id:
            sessions_data = self.db._load_data(self.db.sessions_file)
            if session_id in sessions_data:
                sessions_data[session_id]['is_active'] = False
                self.db._save_data(self.db.sessions_file, sessions_data)
                return True
        return False
    
    def terminate_all_sessions(self, user_id: str, except_session: str = None) -> int:
        """终止用户的所有会话"""
        sessions_data = self.db._load_data(self.db.sessions_file)
        terminated_count = 0
        
        for session_id, session_data in sessions_data.items():
            if (session_data['user_id'] == user_id and 
                session_id != except_session and
                session_data.get('is_active', True)):
                
                sessions_data[session_id]['is_active'] = False
                terminated_count += 1
        
        if terminated_count > 0:
            self.db._save_data(self.db.sessions_file, sessions_data)
        
        return terminated_count

# 使用示例
if __name__ == "__main__":
    # 初始化数据库和认证管理器
    db = UserDatabase("./test_data")
    auth = AuthManager(db)
    
    # 测试用户注册
    register_result = auth.register_user(
        username="test_auth_user",
        email="auth@example.com",
        password="password123"
    )
    print(f"注册结果: {register_result}")
    
    if register_result['success']:
        # 测试用户登录
        login_result = auth.login_user(
            username="test_auth_user",
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
            
            # 测试会话管理
            session_manager = SessionManager(db)
            sessions = session_manager.get_active_sessions(login_result['user_id'])
            print(f"活跃会话: {len(sessions)} 个")
    
    print("认证系统测试完成")
