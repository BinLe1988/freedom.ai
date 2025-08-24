#!/usr/bin/env python3
"""
Freedom.AI Web应用
简单的Web界面用于自由度评估和AI智能体交互
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
import sys
from datetime import datetime

# 添加父目录到路径以导入我们的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.freedom_calculator import FreedomCalculator
from ai_agents_architecture import FreedomAIOrchestrator, Opportunity

app = Flask(__name__)
app.secret_key = 'freedom_ai_secret_key_2024'

# 初始化组件
calculator = FreedomCalculator()
orchestrator = FreedomAIOrchestrator()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/assessment')
def assessment():
    """自由度评估页面"""
    return render_template('assessment.html')

@app.route('/opportunities')
def opportunities():
    """机会探索页面"""
    return render_template('opportunities.html')

@app.route('/learning')
def learning():
    """学习规划页面"""
    return render_template('learning.html')

@app.route('/api/calculate_freedom', methods=['POST'])
def api_calculate_freedom():
    """API: 计算自由度"""
    try:
        data = request.json
        
        # 提取各维度数据
        financial_data = data.get('financial', {})
        time_data = data.get('time', {})
        location_data = data.get('location', {})
        skill_data = data.get('skill', {})
        
        # 计算各维度自由度
        financial_result = calculator.calculate_financial_freedom(financial_data)
        time_result = calculator.calculate_time_freedom(time_data)
        location_result = calculator.calculate_location_freedom(location_data)
        skill_result = calculator.calculate_skill_freedom(skill_data)
        
        # 综合评分
        individual_scores = {
            'financial': financial_result['score'],
            'time': time_result['score'],
            'location': location_result['score'],
            'skill': skill_result['score'],
            'relationship': data.get('relationship_score', 0.5)
        }
        
        overall_result = calculator.calculate_overall_freedom(individual_scores)
        
        # 保存到session
        session['last_assessment'] = {
            'timestamp': datetime.now().isoformat(),
            'results': {
                'financial': financial_result,
                'time': time_result,
                'location': location_result,
                'skill': skill_result,
                'overall': overall_result
            }
        }
        
        return jsonify({
            'success': True,
            'results': {
                'financial': financial_result,
                'time': time_result,
                'location': location_result,
                'skill': skill_result,
                'overall': overall_result
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/discover_opportunities', methods=['POST'])
def api_discover_opportunities():
    """API: 发现机会（集成JobLeads职位数据）"""
    try:
        data = request.json
        user_profile = data.get('user_profile', {})
        
        skills = user_profile.get('skills', [])
        include_jobs = data.get('include_jobs', True)  # 是否包含JobLeads职位
        
        # 导入JobLeads集成
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'integrations'))
        
        try:
            from jobleads_api import JobLeadsAPI
            jobleads_available = True
        except ImportError:
            jobleads_available = False
        
        # 传统机会数据
        traditional_opportunities = [
            {
                'title': 'AI内容创作服务',
                'description': '为企业提供AI辅助的内容创作和营销服务',
                'potential_income': 8000,
                'time_investment': 20,
                'risk_level': 3,
                'skills_required': ['AI工具使用', '内容策划', '客户沟通'],
                'source': '市场趋势分析',
                'type': 'business_opportunity'
            },
            {
                'title': '在线技能培训',
                'description': '创建和销售专业技能培训课程',
                'potential_income': 5000,
                'time_investment': 25,
                'risk_level': 4,
                'skills_required': ['教学能力', '视频制作', '营销推广'],
                'source': '技能变现分析',
                'type': 'business_opportunity'
            },
            {
                'title': '远程技术咨询',
                'description': '为中小企业提供技术咨询和解决方案',
                'potential_income': 12000,
                'time_investment': 30,
                'risk_level': 2,
                'skills_required': ['项目管理', '技术架构', '商务沟通'],
                'source': '远程工作趋势',
                'type': 'business_opportunity'
            }
        ]
        
        all_opportunities = []
        
        # 添加传统机会
        for opp in traditional_opportunities:
            # 计算技能匹配度
            user_skills_set = set([skill.lower() for skill in skills])
            required_skills_set = set([skill.lower() for skill in opp['skills_required']])
            match_score = len(user_skills_set.intersection(required_skills_set)) / len(required_skills_set) if required_skills_set else 0
            
            # 综合评分
            income_score = min(opp['potential_income'] / 10000, 1.0) * 0.4
            risk_score = (10 - opp['risk_level']) / 10 * 0.3
            skill_score = match_score * 0.3
            
            total_score = income_score + risk_score + skill_score
            
            all_opportunities.append({
                **opp,
                'match_score': match_score,
                'total_score': total_score
            })
        
        # 添加JobLeads职位数据
        job_opportunities = []
        if include_jobs and jobleads_available:
            try:
                jobleads = JobLeadsAPI()
                
                # 获取职位推荐
                preferences = {
                    'remote': user_profile.get('remote_preferred', True),
                    'salary_min': user_profile.get('salary_min', 15000),
                    'limit': 10
                }
                
                jobs = jobleads.get_job_recommendations(skills, preferences)
                
                # 转换JobLeads职位为机会格式
                for job in jobs[:5]:  # 取前5个职位
                    # 从薪资范围提取平均收入
                    salary_range = job.get('salary_range', '0-0')
                    try:
                        import re
                        salaries = [int(x) for x in re.findall(r'\d+', salary_range)]
                        avg_income = sum(salaries) / len(salaries) if salaries else 0
                    except:
                        avg_income = 0
                    
                    # 根据工作类型估算时间投入
                    job_type = job.get('job_type', 'full-time')
                    if job_type == 'full-time':
                        time_investment = 40
                    elif job_type == 'part-time':
                        time_investment = 20
                    elif job_type in ['contract', 'freelance']:
                        time_investment = 30
                    else:
                        time_investment = 35
                    
                    # 根据自由度评分估算风险等级
                    freedom_score = job.get('freedom_score', 0.5)
                    risk_level = max(1, min(10, int((1 - freedom_score) * 8 + 2)))
                    
                    job_opportunity = {
                        'title': f"{job['title']} - {job['company']}",
                        'description': job.get('description', ''),
                        'potential_income': avg_income,
                        'time_investment': time_investment,
                        'risk_level': risk_level,
                        'skills_required': job.get('requirements', []),
                        'source': 'JobLeads职位推荐',
                        'type': 'job_opportunity',
                        'match_score': job.get('match_score', 0),
                        'total_score': job.get('overall_score', 0),
                        'job_details': {
                            'company': job.get('company'),
                            'location': job.get('location'),
                            'job_type': job.get('job_type'),
                            'remote_friendly': job.get('remote_friendly'),
                            'benefits': job.get('benefits', []),
                            'application_url': job.get('application_url'),
                            'posted_date': job.get('posted_date'),
                            'freedom_score': job.get('freedom_score')
                        }
                    }
                    
                    job_opportunities.append(job_opportunity)
                    all_opportunities.append(job_opportunity)
                
            except Exception as e:
                print(f"JobLeads集成错误: {e}")
        
        # 按评分排序所有机会
        all_opportunities.sort(key=lambda x: x['total_score'], reverse=True)
        
        # 获取市场趋势（包含JobLeads数据）
        trend_analysis = {
            'hot_sectors': ['AI/ML', '远程工作工具', '个人品牌建设'],
            'emerging_skills': ['AI提示工程', '数字营销', '内容创作'],
            'market_gaps': ['中小企业AI应用', '个人效率工具', '在线教育'],
            'timing_advice': '现在是进入AI辅助服务领域的好时机'
        }
        
        # 如果有JobLeads数据，更新趋势分析
        if jobleads_available:
            try:
                jobleads = JobLeadsAPI()
                job_trends = jobleads.get_job_trends()
                trend_analysis.update({
                    'hot_skills_jobs': job_trends.get('hot_skills', []),
                    'remote_job_growth': job_trends.get('remote_job_growth'),
                    'salary_trends': job_trends.get('salary_trends', {}),
                    'top_hiring_companies': job_trends.get('top_companies_hiring', [])
                })
            except:
                pass
        
        recommendations = [
            '优先关注低风险、高收益的机会',
            '建立个人品牌和专业网络',
            '持续学习和技能提升',
            '多元化收入来源，降低风险'
        ]
        
        # 如果有职位机会，添加相关建议
        if job_opportunities:
            recommendations.extend([
                '考虑远程工作职位，提升地理自由度',
                '关注自由职业和合同工作机会',
                '利用职位要求指导技能学习方向'
            ])
        
        return jsonify({
            'success': True,
            'opportunities': all_opportunities,
            'job_opportunities': job_opportunities,
            'business_opportunities': [opp for opp in all_opportunities if opp.get('type') == 'business_opportunity'],
            'trend_analysis': trend_analysis,
            'recommendations': recommendations,
            'jobleads_integrated': jobleads_available
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/evaluate_opportunities', methods=['POST'])
def api_evaluate_opportunities():
    """API: 评估机会"""
    try:
        data = request.json
        opportunities_data = data.get('opportunities', [])
        
        if not opportunities_data:
            return jsonify({'success': False, 'error': '没有提供机会数据'}), 400
        
        # 简化的机会评估逻辑
        evaluated_opportunities = []
        
        for opp_data in opportunities_data:
            # 计算机会评分
            income_score = min(float(opp_data.get('potential_income', 0)) / 10000, 1.0) * 0.3
            efficiency_score = (float(opp_data.get('potential_income', 0)) / max(int(opp_data.get('time_investment', 1)), 1)) / 100 * 0.2
            risk_score = (10 - int(opp_data.get('risk_level', 5))) / 10 * 0.2
            skill_score = 0.7 * 0.3  # 假设70%技能匹配度
            
            total_score = income_score + efficiency_score + risk_score + skill_score
            
            # 生成推理说明
            reasoning = f"基于收入潜力(¥{opp_data.get('potential_income', 0)})、时间投资({opp_data.get('time_investment', 0)}h)和风险水平({opp_data.get('risk_level', 0)})的综合评估"
            
            evaluated_opportunities.append({
                'opportunity': opp_data,
                'score': total_score,
                'reasoning': reasoning
            })
        
        # 按分数排序
        evaluated_opportunities.sort(key=lambda x: x['score'], reverse=True)
        
        # 决策因素
        decision_factors = [
            "收入潜力与时间投资比",
            "技能匹配度",
            "风险承受能力",
            "长期发展价值",
            "个人兴趣契合度"
        ]
        
        # 风险评估
        high_risk_count = len([o for o in opportunities_data if int(o.get('risk_level', 0)) > 7])
        risk_assessment = {
            'high_risk_count': high_risk_count,
            'diversification_advice': "建议同时追求2-3个不同风险级别的机会",
            'risk_mitigation': "设置止损点，分阶段投入资源"
        }
        
        return jsonify({
            'success': True,
            'evaluation': {
                'recommended_opportunities': evaluated_opportunities[:3],
                'decision_factors': decision_factors,
                'risk_assessment': risk_assessment
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create_learning_plan', methods=['POST'])
def api_create_learning_plan():
    """API: 创建学习计划"""
    try:
        data = request.json
        
        current_skills = data.get('current_skills', [])
        target_skills = data.get('target_skills', [])
        learning_style = data.get('learning_style', 'mixed')
        
        # 技能差距分析
        skill_gaps = []
        for skill in target_skills:
            if skill not in current_skills:
                skill_gaps.append({
                    'skill': skill,
                    'priority': 'high',
                    'difficulty': 'medium',
                    'market_demand': 'high'
                })
        
        # 学习路径规划
        learning_path = []
        for i, gap in enumerate(skill_gaps):
            # 根据学习风格推荐方法
            methods = {
                'visual': '视频教程 + 图表总结',
                'hands_on': '项目实践 + 代码练习',
                'mixed': '在线课程 + 实际项目 + 社区交流'
            }
            method = methods.get(learning_style, methods['mixed'])
            
            learning_path.append({
                'phase': i + 1,
                'skill': gap['skill'],
                'method': method,
                'duration': '4-6周',
                'milestones': ['基础理解', '实践应用', '熟练掌握']
            })
        
        # 推荐学习资源
        resources = [
            {'type': '在线课程', 'platform': 'Coursera/Udemy', 'cost': '免费-$100'},
            {'type': '实践项目', 'platform': 'GitHub', 'cost': '免费'},
            {'type': '社区学习', 'platform': 'Discord/Reddit', 'cost': '免费'},
            {'type': '导师指导', 'platform': '专业网络', 'cost': '$50-200/小时'}
        ]
        
        # 估算学习时间
        weeks = len(skill_gaps) * 6  # 每个技能6周
        estimated_timeline = f"{weeks}周 (每周投入10-15小时)"
        
        return jsonify({
            'success': True,
            'learning_plan': {
                'skill_gaps': skill_gaps,
                'learning_path': learning_path,
                'recommended_resources': resources,
                'estimated_timeline': estimated_timeline
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_dashboard_data')
def api_get_dashboard_data():
    """API: 获取仪表板数据"""
    try:
        last_assessment = session.get('last_assessment')
        
        if not last_assessment:
            return jsonify({
                'success': False,
                'message': '请先完成自由度评估'
            })
        
        results = last_assessment['results']
        
        # 准备图表数据
        chart_data = {
            'freedom_scores': {
                'labels': ['财务自由', '时间自由', '地理自由', '技能自由'],
                'values': [
                    results['financial']['score'] * 100,
                    results['time']['score'] * 100,
                    results['location']['score'] * 100,
                    results['skill']['score'] * 100
                ]
            },
            'overall_score': results['overall']['overall_score'] * 100,
            'level': results['overall']['level'],
            'next_milestone': results['overall']['next_milestone'],
            'improvement_priority': results['overall']['improvement_priority']
        }
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'timestamp': last_assessment['timestamp']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # 创建模板目录
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("Freedom.AI Web应用启动中...")
    print("访问 http://localhost:5001 开始使用")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
