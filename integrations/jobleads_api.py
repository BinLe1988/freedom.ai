#!/usr/bin/env python3
"""
JobLeads API集成模块
用于获取和分析JobLeads平台的职位数据
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re

class JobLeadsAPI:
    """JobLeads API客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.jobleads.com/v1"  # 假设的API端点
        
        # 由于演示环境可能没有requests库，我们主要使用模拟数据
        self.use_mock_data = True
    
    def search_jobs(self, 
                   keywords: List[str] = None,
                   location: str = None,
                   remote: bool = True,
                   salary_min: int = None,
                   job_type: str = None,
                   limit: int = 50) -> List[Dict[str, Any]]:
        """
        搜索JobLeads职位
        
        Args:
            keywords: 关键词列表
            location: 地理位置
            remote: 是否包含远程工作
            salary_min: 最低薪资
            job_type: 工作类型 (full-time, part-time, contract, freelance)
            limit: 返回结果数量限制
        
        Returns:
            职位列表
        """
        
        # 使用模拟数据（在实际环境中，这里会调用真实的JobLeads API）
        return self._get_mock_jobs(keywords, location, remote, salary_min, job_type, limit)
    
    def _get_mock_jobs(self, keywords, location, remote, salary_min, job_type, limit) -> List[Dict[str, Any]]:
        """获取模拟职位数据"""
        
        # 基于用户技能的模拟职位数据
        mock_jobs = [
            {
                'id': 'jl_001',
                'title': 'AI产品经理',
                'company': 'TechCorp',
                'location': '北京/远程',
                'salary_range': '25000-40000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '负责AI产品的规划、设计和推广，需要有技术背景和产品思维',
                'requirements': ['产品管理经验', 'AI/ML基础知识', '数据分析能力', '项目管理'],
                'benefits': ['弹性工作时间', '远程工作', '股权激励', '学习津贴'],
                'posted_date': '2024-01-15',
                'application_url': 'https://jobleads.com/jobs/jl_001',
                'freedom_score': 0.85,  # 自由度评分
                'match_score': 0.0  # 将在后续计算
            },
            {
                'id': 'jl_002',
                'title': '数据科学家',
                'company': 'DataTech Solutions',
                'location': '上海/远程',
                'salary_range': '30000-50000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '使用机器学习和统计方法分析大数据，为业务决策提供支持',
                'requirements': ['Python/R编程', '机器学习', '统计学基础', 'SQL数据库'],
                'benefits': ['100%远程工作', '灵活工作时间', '技术培训', '年终奖'],
                'posted_date': '2024-01-14',
                'application_url': 'https://jobleads.com/jobs/jl_002',
                'freedom_score': 0.90,
                'match_score': 0.0
            },
            {
                'id': 'jl_003',
                'title': 'AI内容创作专家',
                'company': 'ContentAI',
                'location': '深圳/远程',
                'salary_range': '20000-35000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '利用AI工具进行内容创作，包括文案、视频脚本、营销材料等',
                'requirements': ['内容创作经验', 'AI工具使用', '营销思维', '创意能力'],
                'benefits': ['远程优先', '创作自由度高', '作品署名权', '版权分成'],
                'posted_date': '2024-01-13',
                'application_url': 'https://jobleads.com/jobs/jl_003',
                'freedom_score': 0.88,
                'match_score': 0.0
            },
            {
                'id': 'jl_004',
                'title': '远程Python开发工程师',
                'company': 'RemoteFirst Tech',
                'location': '全球远程',
                'salary_range': '28000-45000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '开发和维护Python应用程序，参与开源项目，100%远程工作',
                'requirements': ['Python编程', 'Web框架经验', 'Git版本控制', '英语沟通'],
                'benefits': ['全球远程', '弹性工作时间', '开源贡献奖励', '设备津贴'],
                'posted_date': '2024-01-12',
                'application_url': 'https://jobleads.com/jobs/jl_004',
                'freedom_score': 0.95,
                'match_score': 0.0
            },
            {
                'id': 'jl_005',
                'title': '数字营销顾问',
                'company': 'Growth Marketing Co',
                'location': '广州/远程',
                'salary_range': '18000-30000',
                'job_type': 'contract',
                'remote_friendly': True,
                'description': '为客户提供数字营销策略咨询，包括SEO、SEM、社交媒体营销等',
                'requirements': ['数字营销经验', 'Google Analytics', 'SEO/SEM', '数据分析'],
                'benefits': ['项目制工作', '时间灵活', '客户资源共享', '业绩提成'],
                'posted_date': '2024-01-11',
                'application_url': 'https://jobleads.com/jobs/jl_005',
                'freedom_score': 0.82,
                'match_score': 0.0
            },
            {
                'id': 'jl_006',
                'title': '在线教育课程开发师',
                'company': 'EduTech Online',
                'location': '杭州/远程',
                'salary_range': '22000-38000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '设计和开发在线技术课程，包括课程大纲、视频制作、作业设计等',
                'requirements': ['教学设计经验', '视频制作', '技术背景', '沟通表达能力'],
                'benefits': ['远程工作', '创作版权', '学员反馈奖励', '技能培训'],
                'posted_date': '2024-01-10',
                'application_url': 'https://jobleads.com/jobs/jl_006',
                'freedom_score': 0.86,
                'match_score': 0.0
            },
            {
                'id': 'jl_007',
                'title': '自由职业项目经理',
                'company': 'FreelanceHub',
                'location': '全国远程',
                'salary_range': '15000-25000',
                'job_type': 'freelance',
                'remote_friendly': True,
                'description': '管理多个客户的项目，协调资源，确保项目按时交付',
                'requirements': ['项目管理经验', 'PMP认证优先', '多任务处理', '客户沟通'],
                'benefits': ['项目多样性', '时间自主', '客户网络', '技能提升'],
                'posted_date': '2024-01-09',
                'application_url': 'https://jobleads.com/jobs/jl_007',
                'freedom_score': 0.92,
                'match_score': 0.0
            },
            {
                'id': 'jl_008',
                'title': 'UI/UX设计师',
                'company': 'DesignStudio',
                'location': '成都/远程',
                'salary_range': '20000-35000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '负责产品界面设计和用户体验优化，与开发团队紧密合作',
                'requirements': ['UI/UX设计经验', 'Figma/Sketch', '用户研究', '原型设计'],
                'benefits': ['设计自由度', '远程协作', '作品集支持', '设计工具津贴'],
                'posted_date': '2024-01-08',
                'application_url': 'https://jobleads.com/jobs/jl_008',
                'freedom_score': 0.84,
                'match_score': 0.0
            },
            {
                'id': 'jl_009',
                'title': '区块链开发工程师',
                'company': 'BlockTech',
                'location': '深圳/远程',
                'salary_range': '35000-60000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '开发区块链应用和智能合约，参与DeFi项目开发',
                'requirements': ['Solidity编程', '区块链技术', 'Web3开发', 'JavaScript'],
                'benefits': ['高薪酬', '股权激励', '技术前沿', '远程工作'],
                'posted_date': '2024-01-07',
                'application_url': 'https://jobleads.com/jobs/jl_009',
                'freedom_score': 0.87,
                'match_score': 0.0
            },
            {
                'id': 'jl_010',
                'title': '技术写作专家',
                'company': 'TechDocs',
                'location': '北京/远程',
                'salary_range': '18000-28000',
                'job_type': 'part-time',
                'remote_friendly': True,
                'description': '为技术产品编写文档、教程和API说明，需要技术背景',
                'requirements': ['技术写作经验', '编程基础', '英语能力', '文档工具'],
                'benefits': ['兼职灵活', '远程工作', '技术学习', '作品署名'],
                'posted_date': '2024-01-06',
                'application_url': 'https://jobleads.com/jobs/jl_010',
                'freedom_score': 0.89,
                'match_score': 0.0
            }
        ]
        
        # 根据搜索条件过滤
        filtered_jobs = []
        for job in mock_jobs:
            # 关键词匹配
            if keywords:
                job_text = f"{job['title']} {job['description']} {' '.join(job['requirements'])}".lower()
                if not any(keyword.lower() in job_text for keyword in keywords):
                    continue
            
            # 远程工作过滤
            if remote and not job['remote_friendly']:
                continue
            
            # 薪资过滤
            if salary_min:
                salary_range = job['salary_range']
                min_salary = int(re.findall(r'\d+', salary_range)[0]) if re.findall(r'\d+', salary_range) else 0
                if min_salary < salary_min:
                    continue
            
            # 工作类型过滤
            if job_type and job['job_type'] != job_type:
                continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs[:limit]
    
    def _calculate_freedom_score(self, job: Dict) -> float:
        """计算职位的自由度评分"""
        score = 0.0
        
        # 远程工作加分
        if job.get('remote_friendly', False):
            score += 0.3
        
        # 工作类型加分
        job_type = job.get('job_type', '')
        if job_type in ['freelance', 'contract']:
            score += 0.25
        elif job_type == 'part-time':
            score += 0.15
        
        # 薪资水平加分
        salary_range = job.get('salary_range', '')
        if salary_range:
            try:
                max_salary = max([int(x) for x in re.findall(r'\d+', salary_range)])
                if max_salary >= 40000:
                    score += 0.2
                elif max_salary >= 25000:
                    score += 0.15
                elif max_salary >= 15000:
                    score += 0.1
            except:
                pass
        
        # 福利加分
        benefits = job.get('benefits', [])
        freedom_benefits = ['远程工作', '弹性工作时间', '时间自主', '全球远程', '项目制工作']
        for benefit in benefits:
            if any(fb in str(benefit) for fb in freedom_benefits):
                score += 0.05
        
        return min(score, 1.0)
    
    def calculate_job_match_score(self, job: Dict, user_skills: List[str]) -> float:
        """计算职位与用户技能的匹配度"""
        if not user_skills:
            return 0.0
        
        job_requirements = job.get('requirements', [])
        if not job_requirements:
            return 0.0
        
        # 技能匹配计算
        user_skills_lower = [skill.lower() for skill in user_skills]
        matched_skills = 0
        
        for requirement in job_requirements:
            requirement_lower = requirement.lower()
            for user_skill in user_skills_lower:
                if user_skill in requirement_lower or requirement_lower in user_skill:
                    matched_skills += 1
                    break
        
        match_score = matched_skills / len(job_requirements)
        return min(match_score, 1.0)
    
    def get_job_recommendations(self, 
                              user_skills: List[str],
                              preferences: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        基于用户技能和偏好获取职位推荐
        
        Args:
            user_skills: 用户技能列表
            preferences: 用户偏好设置
        
        Returns:
            推荐职位列表
        """
        preferences = preferences or {}
        
        # 搜索职位
        jobs = self.search_jobs(
            keywords=user_skills,
            remote=preferences.get('remote', True),
            salary_min=preferences.get('salary_min'),
            job_type=preferences.get('job_type'),
            limit=preferences.get('limit', 20)
        )
        
        # 计算匹配度
        for job in jobs:
            job['match_score'] = self.calculate_job_match_score(job, user_skills)
        
        # 计算综合评分
        for job in jobs:
            # 综合评分 = 技能匹配度 * 0.4 + 自由度评分 * 0.3 + 薪资评分 * 0.3
            salary_score = self._get_salary_score(job.get('salary_range', ''))
            job['overall_score'] = (
                job['match_score'] * 0.4 + 
                job['freedom_score'] * 0.3 + 
                salary_score * 0.3
            )
        
        # 按综合评分排序
        jobs.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return jobs
    
    def _get_salary_score(self, salary_range: str) -> float:
        """计算薪资评分"""
        if not salary_range:
            return 0.0
        
        try:
            salaries = [int(x) for x in re.findall(r'\d+', salary_range)]
            if not salaries:
                return 0.0
            
            avg_salary = sum(salaries) / len(salaries)
            
            # 薪资评分标准
            if avg_salary >= 50000:
                return 1.0
            elif avg_salary >= 35000:
                return 0.8
            elif avg_salary >= 25000:
                return 0.6
            elif avg_salary >= 15000:
                return 0.4
            else:
                return 0.2
        except:
            return 0.0
    
    def get_job_trends(self) -> Dict[str, Any]:
        """获取职位市场趋势"""
        return {
            'hot_skills': [
                'AI/机器学习', 'Python编程', '数据分析', 
                '云计算', '前端开发', 'UI/UX设计',
                '数字营销', '项目管理', '内容创作',
                '区块链', '技术写作'
            ],
            'remote_job_growth': '远程工作职位增长45%',
            'salary_trends': {
                'AI相关': '平均薪资上涨15%',
                '数据科学': '平均薪资上涨12%',
                '远程工作': '薪资溢价8%',
                '区块链': '平均薪资上涨20%'
            },
            'job_type_distribution': {
                'full-time': 60,
                'contract': 25,
                'freelance': 10,
                'part-time': 5
            },
            'top_companies_hiring': [
                'TechCorp', 'DataTech Solutions', 'RemoteFirst Tech',
                'ContentAI', 'Growth Marketing Co', 'EduTech Online',
                'BlockTech', 'DesignStudio'
            ]
        }

# 使用示例
def demo_jobleads_integration():
    """演示JobLeads集成功能"""
    print("=== JobLeads职位数据集成演示 ===\n")
    
    # 初始化API客户端
    jobleads = JobLeadsAPI()
    
    # 用户技能示例
    user_skills = ['Python编程', '数据分析', '项目管理', 'AI工具使用']
    
    # 用户偏好
    preferences = {
        'remote': True,
        'salary_min': 20000,
        'job_type': None,  # 不限制工作类型
        'limit': 10
    }
    
    print("👤 用户技能:", ', '.join(user_skills))
    print("⚙️ 搜索偏好:", preferences)
    print()
    
    # 获取职位推荐
    recommended_jobs = jobleads.get_job_recommendations(user_skills, preferences)
    
    print(f"🎯 为你推荐 {len(recommended_jobs)} 个职位:\n")
    
    for i, job in enumerate(recommended_jobs[:5], 1):
        print(f"{i}. {job['title']} - {job['company']}")
        print(f"   📍 地点: {job['location']}")
        print(f"   💰 薪资: {job['salary_range']}")
        print(f"   🏷️ 类型: {job['job_type']}")
        print(f"   🎯 技能匹配: {job['match_score']:.1%}")
        print(f"   🆓 自由度: {job['freedom_score']:.1%}")
        print(f"   ⭐ 综合评分: {job['overall_score']:.1%}")
        print(f"   🔗 申请链接: {job['application_url']}")
        print()
    
    # 获取市场趋势
    trends = jobleads.get_job_trends()
    print("📈 职位市场趋势:")
    print(f"   热门技能: {', '.join(trends['hot_skills'][:5])}")
    print(f"   远程工作: {trends['remote_job_growth']}")
    print(f"   薪资趋势: AI相关职位{trends['salary_trends']['AI相关']}")

if __name__ == "__main__":
    demo_jobleads_integration()
    
    def _get_mock_jobs(self, keywords, location, remote, salary_min, job_type, limit) -> List[Dict[str, Any]]:
        """获取模拟职位数据"""
        
        # 基于用户技能的模拟职位数据
        mock_jobs = [
            {
                'id': 'jl_001',
                'title': 'AI产品经理',
                'company': 'TechCorp',
                'location': '北京/远程',
                'salary_range': '25000-40000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '负责AI产品的规划、设计和推广，需要有技术背景和产品思维',
                'requirements': ['产品管理经验', 'AI/ML基础知识', '数据分析能力', '项目管理'],
                'benefits': ['弹性工作时间', '远程工作', '股权激励', '学习津贴'],
                'posted_date': '2024-01-15',
                'application_url': 'https://jobleads.com/jobs/jl_001',
                'freedom_score': 0.85,  # 自由度评分
                'match_score': 0.0  # 将在后续计算
            },
            {
                'id': 'jl_002',
                'title': '数据科学家',
                'company': 'DataTech Solutions',
                'location': '上海/远程',
                'salary_range': '30000-50000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '使用机器学习和统计方法分析大数据，为业务决策提供支持',
                'requirements': ['Python/R编程', '机器学习', '统计学基础', 'SQL数据库'],
                'benefits': ['100%远程工作', '灵活工作时间', '技术培训', '年终奖'],
                'posted_date': '2024-01-14',
                'application_url': 'https://jobleads.com/jobs/jl_002',
                'freedom_score': 0.90,
                'match_score': 0.0
            },
            {
                'id': 'jl_003',
                'title': 'AI内容创作专家',
                'company': 'ContentAI',
                'location': '深圳/远程',
                'salary_range': '20000-35000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '利用AI工具进行内容创作，包括文案、视频脚本、营销材料等',
                'requirements': ['内容创作经验', 'AI工具使用', '营销思维', '创意能力'],
                'benefits': ['远程优先', '创作自由度高', '作品署名权', '版权分成'],
                'posted_date': '2024-01-13',
                'application_url': 'https://jobleads.com/jobs/jl_003',
                'freedom_score': 0.88,
                'match_score': 0.0
            },
            {
                'id': 'jl_004',
                'title': '远程Python开发工程师',
                'company': 'RemoteFirst Tech',
                'location': '全球远程',
                'salary_range': '28000-45000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '开发和维护Python应用程序，参与开源项目，100%远程工作',
                'requirements': ['Python编程', 'Web框架经验', 'Git版本控制', '英语沟通'],
                'benefits': ['全球远程', '弹性工作时间', '开源贡献奖励', '设备津贴'],
                'posted_date': '2024-01-12',
                'application_url': 'https://jobleads.com/jobs/jl_004',
                'freedom_score': 0.95,
                'match_score': 0.0
            },
            {
                'id': 'jl_005',
                'title': '数字营销顾问',
                'company': 'Growth Marketing Co',
                'location': '广州/远程',
                'salary_range': '18000-30000',
                'job_type': 'contract',
                'remote_friendly': True,
                'description': '为客户提供数字营销策略咨询，包括SEO、SEM、社交媒体营销等',
                'requirements': ['数字营销经验', 'Google Analytics', 'SEO/SEM', '数据分析'],
                'benefits': ['项目制工作', '时间灵活', '客户资源共享', '业绩提成'],
                'posted_date': '2024-01-11',
                'application_url': 'https://jobleads.com/jobs/jl_005',
                'freedom_score': 0.82,
                'match_score': 0.0
            },
            {
                'id': 'jl_006',
                'title': '在线教育课程开发师',
                'company': 'EduTech Online',
                'location': '杭州/远程',
                'salary_range': '22000-38000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '设计和开发在线技术课程，包括课程大纲、视频制作、作业设计等',
                'requirements': ['教学设计经验', '视频制作', '技术背景', '沟通表达能力'],
                'benefits': ['远程工作', '创作版权', '学员反馈奖励', '技能培训'],
                'posted_date': '2024-01-10',
                'application_url': 'https://jobleads.com/jobs/jl_006',
                'freedom_score': 0.86,
                'match_score': 0.0
            },
            {
                'id': 'jl_007',
                'title': '自由职业项目经理',
                'company': 'FreelanceHub',
                'location': '全国远程',
                'salary_range': '15000-25000',
                'job_type': 'freelance',
                'remote_friendly': True,
                'description': '管理多个客户的项目，协调资源，确保项目按时交付',
                'requirements': ['项目管理经验', 'PMP认证优先', '多任务处理', '客户沟通'],
                'benefits': ['项目多样性', '时间自主', '客户网络', '技能提升'],
                'posted_date': '2024-01-09',
                'application_url': 'https://jobleads.com/jobs/jl_007',
                'freedom_score': 0.92,
                'match_score': 0.0
            },
            {
                'id': 'jl_008',
                'title': 'UI/UX设计师',
                'company': 'DesignStudio',
                'location': '成都/远程',
                'salary_range': '20000-35000',
                'job_type': 'full-time',
                'remote_friendly': True,
                'description': '负责产品界面设计和用户体验优化，与开发团队紧密合作',
                'requirements': ['UI/UX设计经验', 'Figma/Sketch', '用户研究', '原型设计'],
                'benefits': ['设计自由度', '远程协作', '作品集支持', '设计工具津贴'],
                'posted_date': '2024-01-08',
                'application_url': 'https://jobleads.com/jobs/jl_008',
                'freedom_score': 0.84,
                'match_score': 0.0
            }
        ]
        
        # 根据搜索条件过滤
        filtered_jobs = []
        for job in mock_jobs:
            # 关键词匹配
            if keywords:
                job_text = f"{job['title']} {job['description']} {' '.join(job['requirements'])}".lower()
                if not any(keyword.lower() in job_text for keyword in keywords):
                    continue
            
            # 远程工作过滤
            if remote and not job['remote_friendly']:
                continue
            
            # 薪资过滤
            if salary_min:
                salary_range = job['salary_range']
                min_salary = int(re.findall(r'\d+', salary_range)[0]) if re.findall(r'\d+', salary_range) else 0
                if min_salary < salary_min:
                    continue
            
            # 工作类型过滤
            if job_type and job['job_type'] != job_type:
                continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs[:limit]
    
    def _process_job_data(self, raw_jobs: List[Dict]) -> List[Dict[str, Any]]:
        """处理原始职位数据"""
        processed_jobs = []
        
        for job in raw_jobs:
            processed_job = {
                'id': job.get('id'),
                'title': job.get('title'),
                'company': job.get('company', {}).get('name'),
                'location': job.get('location'),
                'salary_range': job.get('salary_range'),
                'job_type': job.get('job_type'),
                'remote_friendly': job.get('remote_friendly', False),
                'description': job.get('description'),
                'requirements': job.get('requirements', []),
                'benefits': job.get('benefits', []),
                'posted_date': job.get('posted_date'),
                'application_url': job.get('application_url'),
                'freedom_score': self._calculate_freedom_score(job),
                'match_score': 0.0  # 将在后续计算
            }
            processed_jobs.append(processed_job)
        
        return processed_jobs
    
    def _calculate_freedom_score(self, job: Dict) -> float:
        """计算职位的自由度评分"""
        score = 0.0
        
        # 远程工作加分
        if job.get('remote_friendly', False):
            score += 0.3
        
        # 工作类型加分
        job_type = job.get('job_type', '')
        if job_type in ['freelance', 'contract']:
            score += 0.25
        elif job_type == 'part-time':
            score += 0.15
        
        # 薪资水平加分
        salary_range = job.get('salary_range', '')
        if salary_range:
            try:
                max_salary = max([int(x) for x in re.findall(r'\d+', salary_range)])
                if max_salary >= 40000:
                    score += 0.2
                elif max_salary >= 25000:
                    score += 0.15
                elif max_salary >= 15000:
                    score += 0.1
            except:
                pass
        
        # 福利加分
        benefits = job.get('benefits', [])
        freedom_benefits = ['远程工作', '弹性工作时间', '时间自主', '全球远程', '项目制工作']
        for benefit in benefits:
            if any(fb in str(benefit) for fb in freedom_benefits):
                score += 0.05
        
        return min(score, 1.0)
    
    def calculate_job_match_score(self, job: Dict, user_skills: List[str]) -> float:
        """计算职位与用户技能的匹配度"""
        if not user_skills:
            return 0.0
        
        job_requirements = job.get('requirements', [])
        if not job_requirements:
            return 0.0
        
        # 技能匹配计算
        user_skills_lower = [skill.lower() for skill in user_skills]
        matched_skills = 0
        
        for requirement in job_requirements:
            requirement_lower = requirement.lower()
            for user_skill in user_skills_lower:
                if user_skill in requirement_lower or requirement_lower in user_skill:
                    matched_skills += 1
                    break
        
        match_score = matched_skills / len(job_requirements)
        return min(match_score, 1.0)
    
    def get_job_recommendations(self, 
                              user_skills: List[str],
                              preferences: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        基于用户技能和偏好获取职位推荐
        
        Args:
            user_skills: 用户技能列表
            preferences: 用户偏好设置
        
        Returns:
            推荐职位列表
        """
        preferences = preferences or {}
        
        # 搜索职位
        jobs = self.search_jobs(
            keywords=user_skills,
            remote=preferences.get('remote', True),
            salary_min=preferences.get('salary_min'),
            job_type=preferences.get('job_type'),
            limit=preferences.get('limit', 20)
        )
        
        # 计算匹配度
        for job in jobs:
            job['match_score'] = self.calculate_job_match_score(job, user_skills)
        
        # 计算综合评分
        for job in jobs:
            # 综合评分 = 技能匹配度 * 0.4 + 自由度评分 * 0.3 + 薪资评分 * 0.3
            salary_score = self._get_salary_score(job.get('salary_range', ''))
            job['overall_score'] = (
                job['match_score'] * 0.4 + 
                job['freedom_score'] * 0.3 + 
                salary_score * 0.3
            )
        
        # 按综合评分排序
        jobs.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return jobs
    
    def _get_salary_score(self, salary_range: str) -> float:
        """计算薪资评分"""
        if not salary_range:
            return 0.0
        
        try:
            salaries = [int(x) for x in re.findall(r'\d+', salary_range)]
            if not salaries:
                return 0.0
            
            avg_salary = sum(salaries) / len(salaries)
            
            # 薪资评分标准
            if avg_salary >= 50000:
                return 1.0
            elif avg_salary >= 35000:
                return 0.8
            elif avg_salary >= 25000:
                return 0.6
            elif avg_salary >= 15000:
                return 0.4
            else:
                return 0.2
        except:
            return 0.0
    
    def get_job_trends(self) -> Dict[str, Any]:
        """获取职位市场趋势"""
        return {
            'hot_skills': [
                'AI/机器学习', 'Python编程', '数据分析', 
                '云计算', '前端开发', 'UI/UX设计',
                '数字营销', '项目管理', '内容创作'
            ],
            'remote_job_growth': '远程工作职位增长45%',
            'salary_trends': {
                'AI相关': '平均薪资上涨15%',
                '数据科学': '平均薪资上涨12%',
                '远程工作': '薪资溢价8%'
            },
            'job_type_distribution': {
                'full-time': 60,
                'contract': 25,
                'freelance': 10,
                'part-time': 5
            },
            'top_companies_hiring': [
                'TechCorp', 'DataTech Solutions', 'RemoteFirst Tech',
                'ContentAI', 'Growth Marketing Co', 'EduTech Online'
            ]
        }

# 使用示例
def demo_jobleads_integration():
    """演示JobLeads集成功能"""
    print("=== JobLeads职位数据集成演示 ===\n")
    
    # 初始化API客户端
    jobleads = JobLeadsAPI()
    
    # 用户技能示例
    user_skills = ['Python编程', '数据分析', '项目管理', 'AI工具使用']
    
    # 用户偏好
    preferences = {
        'remote': True,
        'salary_min': 20000,
        'job_type': None,  # 不限制工作类型
        'limit': 10
    }
    
    print("👤 用户技能:", ', '.join(user_skills))
    print("⚙️ 搜索偏好:", preferences)
    print()
    
    # 获取职位推荐
    recommended_jobs = jobleads.get_job_recommendations(user_skills, preferences)
    
    print(f"🎯 为你推荐 {len(recommended_jobs)} 个职位:\n")
    
    for i, job in enumerate(recommended_jobs[:5], 1):
        print(f"{i}. {job['title']} - {job['company']}")
        print(f"   📍 地点: {job['location']}")
        print(f"   💰 薪资: {job['salary_range']}")
        print(f"   🏷️ 类型: {job['job_type']}")
        print(f"   🎯 技能匹配: {job['match_score']:.1%}")
        print(f"   🆓 自由度: {job['freedom_score']:.1%}")
        print(f"   ⭐ 综合评分: {job['overall_score']:.1%}")
        print(f"   🔗 申请链接: {job['application_url']}")
        print()
    
    # 获取市场趋势
    trends = jobleads.get_job_trends()
    print("📈 职位市场趋势:")
    print(f"   热门技能: {', '.join(trends['hot_skills'][:5])}")
    print(f"   远程工作: {trends['remote_job_growth']}")
    print(f"   薪资趋势: AI相关职位{trends['salary_trends']['AI相关']}")

if __name__ == "__main__":
    demo_jobleads_integration()
