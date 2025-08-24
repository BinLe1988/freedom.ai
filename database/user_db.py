#!/usr/bin/env python3
"""
用户数据库管理器
User Database Manager
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading
from dataclasses import asdict

# 导入用户模型
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from user_system.models import (
    User, UserProfile, UserAction, UserSession, UserPreferences,
    UserStatus, ActionType, UserBehaviorAnalyzer,
    generate_user_id, generate_session_id, create_password_hash, verify_password
)

class UserDatabase:
    """用户数据库管理器 (基于JSON文件存储)"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # 数据文件路径
        self.users_file = self.data_dir / "users.json"
        self.profiles_file = self.data_dir / "user_profiles.json"
        self.actions_file = self.data_dir / "user_actions.json"
        self.sessions_file = self.data_dir / "user_sessions.json"
        self.preferences_file = self.data_dir / "user_preferences.json"
        
        # 线程锁
        self._lock = threading.Lock()
        
        # 初始化数据文件
        self._init_data_files()
        
        # 行为分析器
        self.behavior_analyzer = UserBehaviorAnalyzer()
    
    def _init_data_files(self):
        """初始化数据文件"""
        files = [
            self.users_file,
            self.profiles_file,
            self.actions_file,
            self.sessions_file,
            self.preferences_file
        ]
        
        for file_path in files:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
    
    def _load_data(self, file_path: Path) -> Dict[str, Any]:
        """加载数据文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self, file_path: Path, data: Dict[str, Any]):
        """保存数据到文件"""
        with self._lock:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 用户管理
    def create_user(self, username: str, email: str, password: str, **kwargs) -> User:
        """创建新用户"""
        users_data = self._load_data(self.users_file)
        
        # 检查用户名和邮箱是否已存在
        for user_data in users_data.values():
            if user_data['username'] == username:
                raise ValueError(f"用户名 '{username}' 已存在")
            if user_data['email'] == email:
                raise ValueError(f"邮箱 '{email}' 已存在")
        
        # 创建用户
        user = User(
            user_id=generate_user_id(),
            username=username,
            email=email,
            password_hash=create_password_hash(password),
            created_at=datetime.now(),
            **kwargs
        )
        
        # 保存用户数据
        users_data[user.user_id] = user.to_dict()
        self._save_data(self.users_file, users_data)
        
        # 创建默认用户档案和偏好
        self.create_user_profile(user.user_id)
        self.create_user_preferences(user.user_id)
        
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户信息"""
        users_data = self._load_data(self.users_file)
        user_data = users_data.get(user_id)
        
        if user_data:
            return User.from_dict(user_data)
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """通过用户名获取用户"""
        users_data = self._load_data(self.users_file)
        
        for user_data in users_data.values():
            if user_data['username'] == username:
                return User.from_dict(user_data)
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """通过邮箱获取用户"""
        users_data = self._load_data(self.users_file)
        
        for user_data in users_data.values():
            if user_data['email'] == email:
                return User.from_dict(user_data)
        return None
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """更新用户信息"""
        users_data = self._load_data(self.users_file)
        
        if user_id not in users_data:
            return False
        
        # 更新用户数据
        for key, value in kwargs.items():
            if hasattr(User, key):
                users_data[user_id][key] = value
        
        self._save_data(self.users_file, users_data)
        return True
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """用户认证 - 支持用户名或邮箱登录"""
        # 首先尝试用户名登录
        user = self.get_user_by_username(username)
        
        # 如果用户名不存在，尝试邮箱登录
        if not user:
            user = self.get_user_by_email(username)
        
        if user and verify_password(password, user.password_hash):
            # 更新最后登录时间
            self.update_user(user.user_id, last_login=datetime.now().isoformat())
            return user
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户 (软删除)"""
        return self.update_user(user_id, status=UserStatus.DELETED.value)
    
    # 用户档案管理
    def create_user_profile(self, user_id: str, **kwargs) -> UserProfile:
        """创建用户档案"""
        profiles_data = self._load_data(self.profiles_file)
        
        profile = UserProfile(user_id=user_id, **kwargs)
        profiles_data[user_id] = asdict(profile)
        profiles_data[user_id]['updated_at'] = profile.updated_at.isoformat()
        
        self._save_data(self.profiles_file, profiles_data)
        return profile
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """获取用户档案"""
        profiles_data = self._load_data(self.profiles_file)
        profile_data = profiles_data.get(user_id)
        
        if profile_data:
            profile_data['updated_at'] = datetime.fromisoformat(profile_data['updated_at'])
            return UserProfile(**profile_data)
        return None
    
    def update_user_profile(self, user_id: str, **kwargs) -> bool:
        """更新用户档案"""
        profiles_data = self._load_data(self.profiles_file)
        
        if user_id not in profiles_data:
            return False
        
        # 更新档案数据
        for key, value in kwargs.items():
            if hasattr(UserProfile, key):
                # 处理datetime对象
                if isinstance(value, datetime):
                    profiles_data[user_id][key] = value.isoformat()
                else:
                    profiles_data[user_id][key] = value
        
        profiles_data[user_id]['updated_at'] = datetime.now().isoformat()
        self._save_data(self.profiles_file, profiles_data)
        return True
    
    # 用户偏好管理
    def create_user_preferences(self, user_id: str, **kwargs) -> UserPreferences:
        """创建用户偏好"""
        preferences_data = self._load_data(self.preferences_file)
        
        preferences = UserPreferences(user_id=user_id, **kwargs)
        pref_dict = asdict(preferences)
        pref_dict['updated_at'] = preferences.updated_at.isoformat()
        
        preferences_data[user_id] = pref_dict
        self._save_data(self.preferences_file, preferences_data)
        return preferences
    
    def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """获取用户偏好"""
        preferences_data = self._load_data(self.preferences_file)
        pref_data = preferences_data.get(user_id)
        
        if pref_data:
            pref_data['updated_at'] = datetime.fromisoformat(pref_data['updated_at'])
            return UserPreferences(**pref_data)
        return None
    
    def update_user_preferences(self, user_id: str, **kwargs) -> bool:
        """更新用户偏好"""
        preferences_data = self._load_data(self.preferences_file)
        
        if user_id not in preferences_data:
            return False
        
        # 更新偏好数据
        for key, value in kwargs.items():
            if hasattr(UserPreferences, key):
                preferences_data[user_id][key] = value
        
        preferences_data[user_id]['updated_at'] = datetime.now().isoformat()
        self._save_data(self.preferences_file, preferences_data)
        return True
    
    # 用户行为记录
    def log_user_action(self, user_id: str, action_type: ActionType, details: Dict[str, Any], 
                       session_id: str = None, ip_address: str = None, user_agent: str = None) -> UserAction:
        """记录用户行为"""
        actions_data = self._load_data(self.actions_file)
        
        action = UserAction(
            action_id=None,  # 将自动生成
            user_id=user_id,
            action_type=action_type,
            timestamp=datetime.now(),
            details=details,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # 保存行为记录
        if 'actions' not in actions_data:
            actions_data['actions'] = []
        
        actions_data['actions'].append(action.to_dict())
        
        # 限制记录数量，保留最近10000条
        if len(actions_data['actions']) > 10000:
            actions_data['actions'] = actions_data['actions'][-10000:]
        
        self._save_data(self.actions_file, actions_data)
        return action
    
    def get_user_actions(self, user_id: str, limit: int = 100, 
                        action_type: ActionType = None, 
                        start_date: datetime = None, 
                        end_date: datetime = None) -> List[UserAction]:
        """获取用户行为记录"""
        actions_data = self._load_data(self.actions_file)
        all_actions = actions_data.get('actions', [])
        
        # 过滤用户行为
        user_actions = []
        for action_data in all_actions:
            if action_data['user_id'] != user_id:
                continue
            
            # 转换时间戳
            timestamp = datetime.fromisoformat(action_data['timestamp'])
            
            # 时间范围过滤
            if start_date and timestamp < start_date:
                continue
            if end_date and timestamp > end_date:
                continue
            
            # 行为类型过滤
            if action_type and ActionType(action_data['action_type']) != action_type:
                continue
            
            # 创建UserAction对象
            action_data['timestamp'] = timestamp
            action_data['action_type'] = ActionType(action_data['action_type'])
            user_actions.append(UserAction(**action_data))
        
        # 按时间倒序排列，返回最近的记录
        user_actions.sort(key=lambda x: x.timestamp, reverse=True)
        return user_actions[:limit]
    
    # 会话管理
    def create_session(self, user_id: str, ip_address: str, user_agent: str) -> UserSession:
        """创建用户会话"""
        sessions_data = self._load_data(self.sessions_file)
        
        session = UserSession(
            session_id=generate_session_id(),
            user_id=user_id,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        sessions_data[session.session_id] = asdict(session)
        sessions_data[session.session_id]['created_at'] = session.created_at.isoformat()
        sessions_data[session.session_id]['last_activity'] = session.last_activity.isoformat()
        
        self._save_data(self.sessions_file, sessions_data)
        return session
    
    def get_session(self, session_id: str) -> Optional[UserSession]:
        """获取会话信息"""
        sessions_data = self._load_data(self.sessions_file)
        session_data = sessions_data.get(session_id)
        
        if session_data:
            session_data['created_at'] = datetime.fromisoformat(session_data['created_at'])
            session_data['last_activity'] = datetime.fromisoformat(session_data['last_activity'])
            return UserSession(**session_data)
        return None
    
    def update_session_activity(self, session_id: str) -> bool:
        """更新会话活动时间"""
        sessions_data = self._load_data(self.sessions_file)
        
        if session_id not in sessions_data:
            return False
        
        sessions_data[session_id]['last_activity'] = datetime.now().isoformat()
        self._save_data(self.sessions_file, sessions_data)
        return True
    
    def cleanup_expired_sessions(self, timeout_hours: int = 24):
        """清理过期会话"""
        sessions_data = self._load_data(self.sessions_file)
        current_time = datetime.now()
        
        expired_sessions = []
        for session_id, session_data in sessions_data.items():
            last_activity = datetime.fromisoformat(session_data['last_activity'])
            if current_time - last_activity > timedelta(hours=timeout_hours):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del sessions_data[session_id]
        
        if expired_sessions:
            self._save_data(self.sessions_file, sessions_data)
        
        return len(expired_sessions)
    
    # 用户行为分析
    def analyze_user_behavior(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """分析用户行为模式"""
        start_date = datetime.now() - timedelta(days=days)
        actions = self.get_user_actions(user_id, limit=1000, start_date=start_date)
        
        return self.behavior_analyzer.analyze_user_patterns(user_id, actions)
    
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """获取用户统计信息"""
        user = self.get_user(user_id)
        if not user:
            return {}
        
        # 基本统计
        total_actions = len(self.get_user_actions(user_id, limit=10000))
        recent_actions = len(self.get_user_actions(user_id, limit=100, 
                                                 start_date=datetime.now() - timedelta(days=7)))
        
        # 行为分析
        behavior_analysis = self.analyze_user_behavior(user_id)
        
        return {
            'user_id': user_id,
            'username': user.username,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'status': user.status.value,
            'total_actions': total_actions,
            'recent_actions_7d': recent_actions,
            'behavior_analysis': behavior_analysis
        }
    
    # 数据导出
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """导出用户数据"""
        user = self.get_user(user_id)
        profile = self.get_user_profile(user_id)
        preferences = self.get_user_preferences(user_id)
        actions = self.get_user_actions(user_id, limit=1000)
        
        return {
            'user': user.to_dict() if user else None,
            'profile': asdict(profile) if profile else None,
            'preferences': asdict(preferences) if preferences else None,
            'actions': [action.to_dict() for action in actions],
            'export_date': datetime.now().isoformat()
        }

# 使用示例
if __name__ == "__main__":
    # 初始化数据库
    db = UserDatabase("./test_data")
    
    try:
        # 创建测试用户
        user = db.create_user(
            username="test_user",
            email="test@example.com",
            password="password123"
        )
        print(f"创建用户成功: {user.username} ({user.user_id})")
        
        # 更新用户档案
        db.update_user_profile(
            user.user_id,
            full_name="测试用户",
            bio="这是一个测试用户",
            skills=["Python", "数据分析", "机器学习"]
        )
        
        # 记录用户行为
        db.log_user_action(
            user.user_id,
            ActionType.ASSESSMENT,
            {
                'assessment_type': 'freedom_score',
                'score': 0.75,
                'duration': 300
            }
        )
        
        # 获取用户统计
        stats = db.get_user_statistics(user.user_id)
        print(f"用户统计: {stats}")
        
    except ValueError as e:
        print(f"错误: {e}")
    
    print("用户系统测试完成")
