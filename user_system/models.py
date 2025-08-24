#!/usr/bin/env python3
"""
用户系统数据模型
User System Data Models
"""

import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class ActionType(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    ASSESSMENT = "assessment"
    OPPORTUNITY_VIEW = "opportunity_view"
    OPPORTUNITY_APPLY = "opportunity_apply"
    LEARNING_PLAN = "learning_plan"
    SKILL_UPDATE = "skill_update"
    PREFERENCE_UPDATE = "preference_update"
    SEARCH = "search"
    FILTER = "filter"
    EXPORT = "export"
    SHARE = "share"

@dataclass
class User:
    """用户模型"""
    user_id: str
    username: str
    email: str
    password_hash: str
    created_at: datetime
    last_login: Optional[datetime] = None
    status: UserStatus = UserStatus.ACTIVE
    profile: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.profile is None:
            self.profile = {}
        if self.preferences is None:
            self.preferences = self._default_preferences()
    
    def _default_preferences(self) -> Dict[str, Any]:
        """默认用户偏好设置"""
        return {
            'language': 'zh-CN',
            'timezone': 'Asia/Shanghai',
            'email_notifications': True,
            'data_sharing': True,
            'theme': 'light',
            'dashboard_layout': 'default',
            'auto_save': True,
            'privacy_level': 'medium'
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_login'] = self.last_login.isoformat() if self.last_login else None
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """从字典创建用户对象"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_login'] = datetime.fromisoformat(data['last_login']) if data['last_login'] else None
        data['status'] = UserStatus(data['status'])
        return cls(**data)

@dataclass
class UserProfile:
    """用户档案"""
    user_id: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    experience_years: Optional[int] = None
    education_level: Optional[str] = None
    current_role: Optional[str] = None
    career_goals: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    social_links: Optional[Dict[str, str]] = None
    
    # 自由度评估结果
    last_assessment_score: Optional[float] = None
    last_assessment_date: Optional[datetime] = None
    assessment_history: Optional[List[Dict]] = None
    
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.career_goals is None:
            self.career_goals = []
        if self.skills is None:
            self.skills = []
        if self.interests is None:
            self.interests = []
        if self.social_links is None:
            self.social_links = {}
        if self.assessment_history is None:
            self.assessment_history = []

@dataclass
class UserAction:
    """用户行为记录"""
    action_id: str
    user_id: str
    action_type: ActionType
    timestamp: datetime
    details: Dict[str, Any]
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    def __post_init__(self):
        if self.action_id is None:
            self.action_id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['action_type'] = self.action_type.value
        return data

@dataclass
class UserSession:
    """用户会话"""
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True
    
    def __post_init__(self):
        if self.session_id is None:
            self.session_id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_activity is None:
            self.last_activity = datetime.now()
    
    def is_expired(self, timeout_hours: int = 24) -> bool:
        """检查会话是否过期"""
        return datetime.now() - self.last_activity > timedelta(hours=timeout_hours)
    
    def update_activity(self):
        """更新最后活动时间"""
        self.last_activity = datetime.now()

@dataclass
class UserPreferences:
    """用户偏好设置"""
    user_id: str
    # 职业偏好
    preferred_work_type: Optional[str] = None  # remote, hybrid, onsite
    preferred_job_types: Optional[List[str]] = None  # full-time, part-time, contract, freelance
    salary_expectations: Optional[Dict[str, int]] = None  # min, max, currency
    location_preferences: Optional[List[str]] = None
    industry_preferences: Optional[List[str]] = None
    company_size_preference: Optional[str] = None  # startup, small, medium, large
    
    # 学习偏好
    learning_style: Optional[str] = None  # visual, auditory, kinesthetic, mixed
    preferred_learning_time: Optional[str] = None  # morning, afternoon, evening, flexible
    learning_pace: Optional[str] = None  # slow, medium, fast
    
    # 通知偏好
    email_frequency: str = "weekly"  # daily, weekly, monthly, never
    notification_types: Optional[List[str]] = None
    
    # 隐私偏好
    data_sharing_level: str = "medium"  # low, medium, high
    profile_visibility: str = "private"  # public, private, connections
    
    # 界面偏好
    dashboard_widgets: Optional[List[str]] = None
    chart_preferences: Optional[Dict[str, str]] = None
    
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.preferred_job_types is None:
            self.preferred_job_types = []
        if self.location_preferences is None:
            self.location_preferences = []
        if self.industry_preferences is None:
            self.industry_preferences = []
        if self.notification_types is None:
            self.notification_types = ['opportunities', 'learning', 'trends']
        if self.dashboard_widgets is None:
            self.dashboard_widgets = ['freedom_score', 'opportunities', 'learning_progress']
        if self.chart_preferences is None:
            self.chart_preferences = {'type': 'radar', 'theme': 'default'}
        if self.salary_expectations is None:
            self.salary_expectations = {'min': 15000, 'max': 50000, 'currency': 'CNY'}

class UserBehaviorAnalyzer:
    """用户行为分析器"""
    
    def __init__(self):
        self.behavior_patterns = {}
    
    def analyze_user_patterns(self, user_id: str, actions: List[UserAction]) -> Dict[str, Any]:
        """分析用户行为模式"""
        if not actions:
            return {}
        
        # 活跃时间分析
        activity_hours = self._analyze_activity_hours(actions)
        
        # 功能使用频率
        feature_usage = self._analyze_feature_usage(actions)
        
        # 搜索偏好
        search_patterns = self._analyze_search_patterns(actions)
        
        # 职位偏好
        job_preferences = self._analyze_job_preferences(actions)
        
        # 学习偏好
        learning_patterns = self._analyze_learning_patterns(actions)
        
        return {
            'user_id': user_id,
            'activity_hours': activity_hours,
            'feature_usage': feature_usage,
            'search_patterns': search_patterns,
            'job_preferences': job_preferences,
            'learning_patterns': learning_patterns,
            'analysis_date': datetime.now().isoformat()
        }
    
    def _analyze_activity_hours(self, actions: List[UserAction]) -> Dict[str, Any]:
        """分析活跃时间"""
        hour_counts = {}
        for action in actions:
            hour = action.timestamp.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        if not hour_counts:
            return {}
        
        most_active_hour = max(hour_counts, key=hour_counts.get)
        
        # 分类时间段
        morning = sum(hour_counts.get(h, 0) for h in range(6, 12))
        afternoon = sum(hour_counts.get(h, 0) for h in range(12, 18))
        evening = sum(hour_counts.get(h, 0) for h in range(18, 24))
        night = sum(hour_counts.get(h, 0) for h in range(0, 6))
        
        total = morning + afternoon + evening + night
        
        return {
            'most_active_hour': most_active_hour,
            'time_distribution': {
                'morning': morning / total if total > 0 else 0,
                'afternoon': afternoon / total if total > 0 else 0,
                'evening': evening / total if total > 0 else 0,
                'night': night / total if total > 0 else 0
            }
        }
    
    def _analyze_feature_usage(self, actions: List[UserAction]) -> Dict[str, Any]:
        """分析功能使用频率"""
        feature_counts = {}
        for action in actions:
            action_type = action.action_type.value
            feature_counts[action_type] = feature_counts.get(action_type, 0) + 1
        
        total_actions = len(actions)
        feature_percentages = {
            feature: count / total_actions 
            for feature, count in feature_counts.items()
        }
        
        most_used_feature = max(feature_counts, key=feature_counts.get) if feature_counts else None
        
        return {
            'feature_counts': feature_counts,
            'feature_percentages': feature_percentages,
            'most_used_feature': most_used_feature,
            'total_actions': total_actions
        }
    
    def _analyze_search_patterns(self, actions: List[UserAction]) -> Dict[str, Any]:
        """分析搜索模式"""
        search_actions = [a for a in actions if a.action_type == ActionType.SEARCH]
        
        if not search_actions:
            return {}
        
        # 搜索关键词频率
        keywords = {}
        for action in search_actions:
            search_terms = action.details.get('keywords', [])
            for term in search_terms:
                keywords[term] = keywords.get(term, 0) + 1
        
        # 搜索频率
        search_frequency = len(search_actions) / len(actions) if actions else 0
        
        return {
            'search_frequency': search_frequency,
            'popular_keywords': dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]),
            'total_searches': len(search_actions)
        }
    
    def _analyze_job_preferences(self, actions: List[UserAction]) -> Dict[str, Any]:
        """分析职位偏好"""
        job_actions = [a for a in actions if a.action_type in [ActionType.OPPORTUNITY_VIEW, ActionType.OPPORTUNITY_APPLY]]
        
        if not job_actions:
            return {}
        
        # 工作类型偏好
        job_types = {}
        remote_preference = 0
        salary_ranges = []
        
        for action in job_actions:
            details = action.details
            
            # 工作类型
            job_type = details.get('job_type')
            if job_type:
                job_types[job_type] = job_types.get(job_type, 0) + 1
            
            # 远程工作偏好
            if details.get('remote_friendly'):
                remote_preference += 1
            
            # 薪资范围
            salary = details.get('salary_range')
            if salary:
                salary_ranges.append(salary)
        
        return {
            'preferred_job_types': job_types,
            'remote_preference': remote_preference / len(job_actions) if job_actions else 0,
            'viewed_jobs': len([a for a in job_actions if a.action_type == ActionType.OPPORTUNITY_VIEW]),
            'applied_jobs': len([a for a in job_actions if a.action_type == ActionType.OPPORTUNITY_APPLY])
        }
    
    def _analyze_learning_patterns(self, actions: List[UserAction]) -> Dict[str, Any]:
        """分析学习模式"""
        learning_actions = [a for a in actions if a.action_type == ActionType.LEARNING_PLAN]
        
        if not learning_actions:
            return {}
        
        # 学习技能偏好
        skills = {}
        for action in learning_actions:
            target_skills = action.details.get('target_skills', [])
            for skill in target_skills:
                skills[skill] = skills.get(skill, 0) + 1
        
        return {
            'learning_frequency': len(learning_actions) / len(actions) if actions else 0,
            'popular_skills': dict(sorted(skills.items(), key=lambda x: x[1], reverse=True)[:10]),
            'total_learning_plans': len(learning_actions)
        }

def create_password_hash(password: str) -> str:
    """创建密码哈希"""
    salt = uuid.uuid4().hex
    return hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt

def verify_password(password: str, password_hash: str) -> bool:
    """验证密码"""
    try:
        hash_part, salt = password_hash.split(':')
        return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
    except ValueError:
        return False

def generate_user_id() -> str:
    """生成用户ID"""
    return 'user_' + str(uuid.uuid4()).replace('-', '')[:12]

def generate_session_id() -> str:
    """生成会话ID"""
    return 'session_' + str(uuid.uuid4()).replace('-', '')[:16]

# 使用示例
if __name__ == "__main__":
    # 创建用户
    user = User(
        user_id=generate_user_id(),
        username="test_user",
        email="test@example.com",
        password_hash=create_password_hash("password123"),
        created_at=datetime.now()
    )
    
    print("用户创建成功:")
    print(f"用户ID: {user.user_id}")
    print(f"用户名: {user.username}")
    print(f"状态: {user.status.value}")
    
    # 创建用户行为记录
    action = UserAction(
        action_id=str(uuid.uuid4()),
        user_id=user.user_id,
        action_type=ActionType.ASSESSMENT,
        timestamp=datetime.now(),
        details={
            'assessment_type': 'freedom_score',
            'score': 0.65,
            'duration': 300
        }
    )
    
    print(f"\n行为记录: {action.action_type.value}")
    print(f"详情: {action.details}")
