#!/usr/bin/env python3
"""
用户行为分析系统
User Behavior Analytics System
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter
import statistics

# 导入相关模块
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.user_db import UserDatabase
from user_system.models import ActionType, UserAction

class BehaviorAnalytics:
    """用户行为分析系统"""
    
    def __init__(self, db: UserDatabase):
        self.db = db
    
    def analyze_user_journey(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """分析用户旅程"""
        start_date = datetime.now() - timedelta(days=days)
        actions = self.db.get_user_actions(user_id, limit=1000, start_date=start_date)
        
        if not actions:
            return {'user_id': user_id, 'journey': [], 'insights': []}
        
        # 按时间排序
        actions.sort(key=lambda x: x.timestamp)
        
        # 构建用户旅程
        journey = []
        for action in actions:
            journey.append({
                'timestamp': action.timestamp.isoformat(),
                'action_type': action.action_type.value,
                'details': action.details,
                'session_id': action.session_id
            })
        
        # 生成洞察
        insights = self._generate_journey_insights(actions)
        
        return {
            'user_id': user_id,
            'analysis_period': f'{days} days',
            'total_actions': len(actions),
            'journey': journey,
            'insights': insights
        }
    
    def analyze_feature_adoption(self, user_id: str = None, days: int = 30) -> Dict[str, Any]:
        """分析功能采用情况"""
        start_date = datetime.now() - timedelta(days=days)
        
        if user_id:
            actions = self.db.get_user_actions(user_id, limit=1000, start_date=start_date)
            scope = f"user_{user_id}"
        else:
            # 分析所有用户
            actions_data = self.db._load_data(self.db.actions_file)
            all_actions = actions_data.get('actions', [])
            
            actions = []
            for action_data in all_actions:
                timestamp = datetime.fromisoformat(action_data['timestamp'])
                if timestamp >= start_date:
                    action_data['timestamp'] = timestamp
                    action_data['action_type'] = ActionType(action_data['action_type'])
                    actions.append(UserAction(**action_data))
            
            scope = "all_users"
        
        # 功能使用统计
        feature_stats = defaultdict(int)
        user_feature_usage = defaultdict(set)
        
        for action in actions:
            feature = action.action_type.value
            feature_stats[feature] += 1
            user_feature_usage[feature].add(action.user_id)
        
        # 计算采用率
        total_users = len(set(action.user_id for action in actions)) if actions else 1
        adoption_rates = {
            feature: len(users) / total_users 
            for feature, users in user_feature_usage.items()
        }
        
        # 功能流行度排序
        popular_features = sorted(feature_stats.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'scope': scope,
            'analysis_period': f'{days} days',
            'total_users': total_users,
            'total_actions': len(actions),
            'feature_usage': dict(feature_stats),
            'adoption_rates': adoption_rates,
            'popular_features': popular_features[:10],
            'insights': self._generate_adoption_insights(feature_stats, adoption_rates)
        }
    
    def analyze_user_segments(self, days: int = 30) -> Dict[str, Any]:
        """用户分群分析"""
        start_date = datetime.now() - timedelta(days=days)
        
        # 获取所有用户行为
        actions_data = self.db._load_data(self.db.actions_file)
        all_actions = actions_data.get('actions', [])
        
        user_metrics = defaultdict(lambda: {
            'total_actions': 0,
            'unique_features': set(),
            'assessment_count': 0,
            'opportunity_views': 0,
            'learning_plans': 0,
            'last_activity': None,
            'first_activity': None
        })
        
        # 计算用户指标
        for action_data in all_actions:
            timestamp = datetime.fromisoformat(action_data['timestamp'])
            if timestamp < start_date:
                continue
            
            user_id = action_data['user_id']
            action_type = ActionType(action_data['action_type'])
            
            metrics = user_metrics[user_id]
            metrics['total_actions'] += 1
            metrics['unique_features'].add(action_type.value)
            
            if not metrics['first_activity'] or timestamp < metrics['first_activity']:
                metrics['first_activity'] = timestamp
            if not metrics['last_activity'] or timestamp > metrics['last_activity']:
                metrics['last_activity'] = timestamp
            
            # 特定行为计数
            if action_type == ActionType.ASSESSMENT:
                metrics['assessment_count'] += 1
            elif action_type == ActionType.OPPORTUNITY_VIEW:
                metrics['opportunity_views'] += 1
            elif action_type == ActionType.LEARNING_PLAN:
                metrics['learning_plans'] += 1
        
        # 用户分群
        segments = {
            'power_users': [],      # 高活跃用户
            'regular_users': [],    # 常规用户
            'casual_users': [],     # 轻度用户
            'inactive_users': []    # 不活跃用户
        }
        
        for user_id, metrics in user_metrics.items():
            total_actions = metrics['total_actions']
            unique_features = len(metrics['unique_features'])
            
            if total_actions >= 50 and unique_features >= 5:
                segments['power_users'].append(user_id)
            elif total_actions >= 20 and unique_features >= 3:
                segments['regular_users'].append(user_id)
            elif total_actions >= 5:
                segments['casual_users'].append(user_id)
            else:
                segments['inactive_users'].append(user_id)
        
        # 计算分群统计
        segment_stats = {}
        for segment_name, user_list in segments.items():
            if user_list:
                segment_metrics = [user_metrics[uid] for uid in user_list]
                avg_actions = statistics.mean([m['total_actions'] for m in segment_metrics])
                avg_features = statistics.mean([len(m['unique_features']) for m in segment_metrics])
                
                segment_stats[segment_name] = {
                    'user_count': len(user_list),
                    'avg_actions': round(avg_actions, 2),
                    'avg_features': round(avg_features, 2),
                    'percentage': round(len(user_list) / len(user_metrics) * 100, 2)
                }
            else:
                segment_stats[segment_name] = {
                    'user_count': 0,
                    'avg_actions': 0,
                    'avg_features': 0,
                    'percentage': 0
                }
        
        return {
            'analysis_period': f'{days} days',
            'total_users': len(user_metrics),
            'segments': segments,
            'segment_stats': segment_stats,
            'insights': self._generate_segment_insights(segment_stats)
        }
    
    def analyze_conversion_funnel(self, days: int = 30) -> Dict[str, Any]:
        """转化漏斗分析"""
        start_date = datetime.now() - timedelta(days=days)
        
        # 定义转化漏斗步骤
        funnel_steps = [
            ('registration', ActionType.LOGIN),
            ('first_assessment', ActionType.ASSESSMENT),
            ('opportunity_exploration', ActionType.OPPORTUNITY_VIEW),
            ('learning_planning', ActionType.LEARNING_PLAN),
            ('job_application', ActionType.OPPORTUNITY_APPLY)
        ]
        
        # 获取所有用户行为
        actions_data = self.db._load_data(self.db.actions_file)
        all_actions = actions_data.get('actions', [])
        
        user_progress = defaultdict(set)
        
        # 跟踪用户在漏斗中的进展
        for action_data in all_actions:
            timestamp = datetime.fromisoformat(action_data['timestamp'])
            if timestamp < start_date:
                continue
            
            user_id = action_data['user_id']
            action_type = ActionType(action_data['action_type'])
            
            for step_name, step_action in funnel_steps:
                if action_type == step_action:
                    user_progress[user_id].add(step_name)
        
        # 计算每个步骤的用户数
        funnel_data = []
        total_users = len(user_progress)
        
        for i, (step_name, _) in enumerate(funnel_steps):
            users_at_step = len([uid for uid, steps in user_progress.items() if step_name in steps])
            conversion_rate = users_at_step / total_users if total_users > 0 else 0
            
            if i > 0:
                prev_step_users = funnel_data[i-1]['users']
                step_conversion = users_at_step / prev_step_users if prev_step_users > 0 else 0
            else:
                step_conversion = conversion_rate
            
            funnel_data.append({
                'step': step_name,
                'users': users_at_step,
                'conversion_rate': round(conversion_rate * 100, 2),
                'step_conversion': round(step_conversion * 100, 2)
            })
        
        return {
            'analysis_period': f'{days} days',
            'total_users': total_users,
            'funnel_data': funnel_data,
            'insights': self._generate_funnel_insights(funnel_data)
        }
    
    def analyze_user_retention(self, days: int = 30) -> Dict[str, Any]:
        """用户留存分析"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 按周分析留存
        weekly_cohorts = {}
        
        # 获取所有用户的首次活动时间
        users_data = self.db._load_data(self.db.users_file)
        actions_data = self.db._load_data(self.db.actions_file)
        all_actions = actions_data.get('actions', [])
        
        # 找到每个用户的首次活动时间
        user_first_activity = {}
        for action_data in all_actions:
            user_id = action_data['user_id']
            timestamp = datetime.fromisoformat(action_data['timestamp'])
            
            if user_id not in user_first_activity or timestamp < user_first_activity[user_id]:
                user_first_activity[user_id] = timestamp
        
        # 按周分组用户
        for user_id, first_activity in user_first_activity.items():
            if first_activity < start_date:
                continue
            
            # 计算是第几周
            week_number = (first_activity - start_date).days // 7
            if week_number not in weekly_cohorts:
                weekly_cohorts[week_number] = set()
            weekly_cohorts[week_number].add(user_id)
        
        # 计算每周的留存率
        retention_data = []
        for week, cohort_users in weekly_cohorts.items():
            cohort_size = len(cohort_users)
            week_start = start_date + timedelta(weeks=week)
            
            # 计算后续几周的留存
            weekly_retention = [100]  # 第0周留存率为100%
            
            for retention_week in range(1, min(5, (days // 7) - week)):  # 最多看4周留存
                retention_start = week_start + timedelta(weeks=retention_week)
                retention_end = retention_start + timedelta(weeks=1)
                
                # 统计在这一周有活动的用户
                active_users = set()
                for action_data in all_actions:
                    timestamp = datetime.fromisoformat(action_data['timestamp'])
                    if retention_start <= timestamp < retention_end:
                        user_id = action_data['user_id']
                        if user_id in cohort_users:
                            active_users.add(user_id)
                
                retention_rate = len(active_users) / cohort_size * 100 if cohort_size > 0 else 0
                weekly_retention.append(round(retention_rate, 2))
            
            retention_data.append({
                'cohort_week': week,
                'cohort_start': week_start.strftime('%Y-%m-%d'),
                'cohort_size': cohort_size,
                'retention_rates': weekly_retention
            })
        
        return {
            'analysis_period': f'{days} days',
            'cohort_analysis': retention_data,
            'insights': self._generate_retention_insights(retention_data)
        }
    
    def generate_personalized_insights(self, user_id: str) -> Dict[str, Any]:
        """生成个性化洞察"""
        # 获取用户基本信息
        user = self.db.get_user(user_id)
        profile = self.db.get_user_profile(user_id)
        preferences = self.db.get_user_preferences(user_id)
        
        if not user:
            return {'error': '用户不存在'}
        
        # 分析用户行为
        behavior_analysis = self.db.analyze_user_behavior(user_id, days=30)
        
        # 生成个性化建议
        recommendations = []
        
        # 基于活跃时间的建议
        if 'activity_hours' in behavior_analysis:
            most_active_hour = behavior_analysis['activity_hours'].get('most_active_hour')
            if most_active_hour:
                if 6 <= most_active_hour <= 11:
                    recommendations.append("您是晨型人，建议在上午安排重要的学习和规划活动")
                elif 18 <= most_active_hour <= 23:
                    recommendations.append("您习惯在晚上活跃，可以利用晚间时间进行技能提升")
        
        # 基于功能使用的建议
        if 'feature_usage' in behavior_analysis:
            feature_usage = behavior_analysis['feature_usage']
            most_used = feature_usage.get('most_used_feature')
            
            if most_used == 'assessment':
                recommendations.append("您经常进行自由度评估，建议制定具体的改进计划")
            elif most_used == 'opportunity_view':
                recommendations.append("您对机会探索很感兴趣，建议完善技能档案以获得更精准推荐")
            elif most_used == 'learning_plan':
                recommendations.append("您很注重学习成长，建议设置学习目标和进度跟踪")
        
        # 基于搜索模式的建议
        if 'search_patterns' in behavior_analysis:
            popular_keywords = behavior_analysis['search_patterns'].get('popular_keywords', {})
            if popular_keywords:
                top_keyword = max(popular_keywords, key=popular_keywords.get)
                recommendations.append(f"您经常搜索'{top_keyword}'相关内容，建议深入学习这个领域")
        
        # 基于职位偏好的建议
        if 'job_preferences' in behavior_analysis:
            job_prefs = behavior_analysis['job_preferences']
            if job_prefs.get('remote_preference', 0) > 0.7:
                recommendations.append("您偏好远程工作，建议发展远程协作和自我管理技能")
        
        return {
            'user_id': user_id,
            'username': user.username,
            'analysis_date': datetime.now().isoformat(),
            'behavior_summary': behavior_analysis,
            'personalized_recommendations': recommendations,
            'next_actions': self._suggest_next_actions(behavior_analysis)
        }
    
    def _generate_journey_insights(self, actions: List[UserAction]) -> List[str]:
        """生成用户旅程洞察"""
        insights = []
        
        if not actions:
            return insights
        
        # 分析活跃度
        total_days = (actions[-1].timestamp - actions[0].timestamp).days + 1
        avg_actions_per_day = len(actions) / total_days
        
        if avg_actions_per_day > 5:
            insights.append("用户活跃度很高，平均每天使用多次")
        elif avg_actions_per_day > 2:
            insights.append("用户活跃度中等，定期使用系统")
        else:
            insights.append("用户活跃度较低，使用频率不高")
        
        # 分析功能使用模式
        action_types = [action.action_type for action in actions]
        type_counts = Counter(action_types)
        
        if ActionType.ASSESSMENT in type_counts and type_counts[ActionType.ASSESSMENT] > 3:
            insights.append("用户经常进行自由度评估，关注个人发展状况")
        
        if ActionType.OPPORTUNITY_VIEW in type_counts:
            insights.append("用户积极探索机会，有明确的职业发展意向")
        
        return insights
    
    def _generate_adoption_insights(self, feature_stats: Dict, adoption_rates: Dict) -> List[str]:
        """生成功能采用洞察"""
        insights = []
        
        # 最受欢迎的功能
        if feature_stats:
            most_popular = max(feature_stats, key=feature_stats.get)
            insights.append(f"最受欢迎的功能是{most_popular}，使用次数占{feature_stats[most_popular]/sum(feature_stats.values())*100:.1f}%")
        
        # 采用率分析
        high_adoption = [f for f, rate in adoption_rates.items() if rate > 0.7]
        if high_adoption:
            insights.append(f"高采用率功能: {', '.join(high_adoption)}")
        
        low_adoption = [f for f, rate in adoption_rates.items() if rate < 0.3]
        if low_adoption:
            insights.append(f"需要推广的功能: {', '.join(low_adoption)}")
        
        return insights
    
    def _generate_segment_insights(self, segment_stats: Dict) -> List[str]:
        """生成用户分群洞察"""
        insights = []
        
        # 用户分布
        power_users_pct = segment_stats['power_users']['percentage']
        regular_users_pct = segment_stats['regular_users']['percentage']
        
        if power_users_pct > 20:
            insights.append(f"高活跃用户占比{power_users_pct}%，用户粘性良好")
        elif power_users_pct < 10:
            insights.append(f"高活跃用户占比仅{power_users_pct}%，需要提升用户参与度")
        
        if regular_users_pct > 40:
            insights.append("常规用户群体稳定，是产品的核心用户群")
        
        return insights
    
    def _generate_funnel_insights(self, funnel_data: List[Dict]) -> List[str]:
        """生成转化漏斗洞察"""
        insights = []
        
        if not funnel_data:
            return insights
        
        # 找到转化率最低的步骤
        min_conversion_step = min(funnel_data[1:], key=lambda x: x['step_conversion'])
        insights.append(f"转化瓶颈在{min_conversion_step['step']}步骤，转化率仅{min_conversion_step['step_conversion']}%")
        
        # 整体转化率
        final_conversion = funnel_data[-1]['conversion_rate']
        if final_conversion > 10:
            insights.append(f"整体转化率{final_conversion}%，表现良好")
        else:
            insights.append(f"整体转化率{final_conversion}%，有待提升")
        
        return insights
    
    def _generate_retention_insights(self, retention_data: List[Dict]) -> List[str]:
        """生成留存洞察"""
        insights = []
        
        if not retention_data:
            return insights
        
        # 计算平均留存率
        all_week1_retention = [cohort['retention_rates'][1] for cohort in retention_data if len(cohort['retention_rates']) > 1]
        if all_week1_retention:
            avg_week1_retention = statistics.mean(all_week1_retention)
            if avg_week1_retention > 50:
                insights.append(f"第1周留存率{avg_week1_retention:.1f}%，用户粘性良好")
            else:
                insights.append(f"第1周留存率{avg_week1_retention:.1f}%，需要改善新用户体验")
        
        return insights
    
    def _suggest_next_actions(self, behavior_analysis: Dict) -> List[str]:
        """建议下一步行动"""
        actions = []
        
        feature_usage = behavior_analysis.get('feature_usage', {})
        
        if 'assessment' not in feature_usage.get('feature_counts', {}):
            actions.append("完成首次自由度评估，了解当前状况")
        
        if 'opportunity_view' not in feature_usage.get('feature_counts', {}):
            actions.append("探索机会页面，发现适合的职位和项目")
        
        if 'learning_plan' not in feature_usage.get('feature_counts', {}):
            actions.append("制定学习计划，提升关键技能")
        
        return actions

# 使用示例
if __name__ == "__main__":
    # 初始化数据库和分析系统
    db = UserDatabase("./test_data")
    analytics = BehaviorAnalytics(db)
    
    # 创建测试用户和行为数据
    try:
        user = db.create_user("analytics_test", "analytics@test.com", "password123")
        user_id = user.user_id
        
        # 模拟用户行为
        test_actions = [
            (ActionType.ASSESSMENT, {'score': 0.6}),
            (ActionType.OPPORTUNITY_VIEW, {'job_type': 'remote', 'salary': 25000}),
            (ActionType.SEARCH, {'keywords': ['Python', 'remote']}),
            (ActionType.LEARNING_PLAN, {'target_skills': ['AI', 'Machine Learning']}),
        ]
        
        for action_type, details in test_actions:
            db.log_user_action(user_id, action_type, details)
        
        # 运行分析
        print("=== 用户旅程分析 ===")
        journey = analytics.analyze_user_journey(user_id)
        print(f"总行为数: {journey['total_actions']}")
        print(f"洞察: {journey['insights']}")
        
        print("\n=== 功能采用分析 ===")
        adoption = analytics.analyze_feature_adoption(user_id)
        print(f"功能使用: {adoption['feature_usage']}")
        
        print("\n=== 个性化洞察 ===")
        insights = analytics.generate_personalized_insights(user_id)
        print(f"推荐: {insights['personalized_recommendations']}")
        
    except ValueError as e:
        print(f"用户已存在，跳过创建: {e}")
        # 使用现有用户进行分析
        users_data = db._load_data(db.users_file)
        if users_data:
            user_id = list(users_data.keys())[0]
            insights = analytics.generate_personalized_insights(user_id)
            print(f"现有用户洞察: {insights.get('personalized_recommendations', [])}")
    
    print("\n行为分析系统测试完成")
