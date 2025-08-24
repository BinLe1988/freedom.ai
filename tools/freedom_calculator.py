#!/usr/bin/env python3
"""
自由度计算器 - 实用工具
Freedom Calculator - Practical Tools
"""

import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any

class FreedomCalculator:
    """自由度计算器"""
    
    def __init__(self):
        self.weights = {
            'financial': 0.35,  # 财务自由权重最高
            'time': 0.25,
            'location': 0.20,
            'skill': 0.15,
            'relationship': 0.05
        }
    
    def calculate_financial_freedom(self, data: Dict[str, float]) -> Dict[str, Any]:
        """计算财务自由度"""
        passive_income = data.get('passive_income', 0)
        active_income = data.get('active_income', 0)
        monthly_expenses = data.get('monthly_expenses', 0)
        emergency_fund = data.get('emergency_fund', 0)
        
        # 基础财务自由度 = 被动收入 / 月支出
        basic_ratio = passive_income / monthly_expenses if monthly_expenses > 0 else 0
        
        # 应急基金覆盖月数
        emergency_months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
        
        # 收入多样性 (简化计算)
        income_diversity = min(len([i for i in [passive_income, active_income] if i > 0]) / 2, 1.0)
        
        # 综合财务自由度
        financial_score = min((basic_ratio * 0.6 + min(emergency_months / 6, 1.0) * 0.3 + income_diversity * 0.1), 1.0)
        
        return {
            'score': financial_score,
            'basic_ratio': basic_ratio,
            'emergency_months': emergency_months,
            'income_diversity': income_diversity,
            'recommendations': self._get_financial_recommendations(financial_score, basic_ratio, emergency_months)
        }
    
    def calculate_time_freedom(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算时间自由度"""
        work_hours_per_week = data.get('work_hours_per_week', 40)
        flexible_hours = data.get('flexible_hours', 0)
        vacation_days = data.get('vacation_days', 0)
        can_work_remotely = data.get('can_work_remotely', False)
        
        # 工作时间灵活性
        time_flexibility = flexible_hours / work_hours_per_week if work_hours_per_week > 0 else 0
        
        # 假期自由度
        vacation_freedom = min(vacation_days / 30, 1.0)  # 30天为满分
        
        # 远程工作加分
        remote_bonus = 0.2 if can_work_remotely else 0
        
        # 综合时间自由度
        time_score = min(time_flexibility * 0.5 + vacation_freedom * 0.3 + remote_bonus, 1.0)
        
        return {
            'score': time_score,
            'time_flexibility': time_flexibility,
            'vacation_freedom': vacation_freedom,
            'remote_work': can_work_remotely,
            'recommendations': self._get_time_recommendations(time_score, work_hours_per_week)
        }
    
    def calculate_location_freedom(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算地理位置自由度"""
        can_work_anywhere = data.get('can_work_anywhere', False)
        travel_frequency = data.get('travel_frequency', 0)  # 每年旅行次数
        location_constraints = data.get('location_constraints', 0)  # 地理限制数量
        
        # 工作地点自由度
        work_location_freedom = 1.0 if can_work_anywhere else 0.3
        
        # 旅行自由度
        travel_freedom = min(travel_frequency / 4, 1.0)  # 每年4次旅行为满分
        
        # 地理限制惩罚
        constraint_penalty = location_constraints * 0.1
        
        # 综合地理自由度
        location_score = max(work_location_freedom * 0.6 + travel_freedom * 0.4 - constraint_penalty, 0)
        
        return {
            'score': location_score,
            'work_location_freedom': work_location_freedom,
            'travel_freedom': travel_freedom,
            'constraints': location_constraints,
            'recommendations': self._get_location_recommendations(location_score, can_work_anywhere)
        }
    
    def calculate_skill_freedom(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算技能自由度"""
        transferable_skills = data.get('transferable_skills', [])
        learning_rate = data.get('learning_rate', 0)  # 每年学习新技能数量
        market_demand_skills = data.get('market_demand_skills', [])
        
        # 可转移技能数量
        skill_count = len(transferable_skills)
        skill_diversity = min(skill_count / 10, 1.0)  # 10个技能为满分
        
        # 学习能力
        learning_ability = min(learning_rate / 3, 1.0)  # 每年3个新技能为满分
        
        # 市场需求匹配度
        demand_match = len(set(transferable_skills) & set(market_demand_skills)) / max(len(transferable_skills), 1)
        
        # 综合技能自由度
        skill_score = skill_diversity * 0.4 + learning_ability * 0.3 + demand_match * 0.3
        
        return {
            'score': skill_score,
            'skill_diversity': skill_diversity,
            'learning_ability': learning_ability,
            'market_match': demand_match,
            'recommendations': self._get_skill_recommendations(skill_score, skill_count)
        }
    
    def calculate_overall_freedom(self, individual_scores: Dict[str, float]) -> Dict[str, Any]:
        """计算综合自由度"""
        weighted_score = sum(
            individual_scores.get(category, 0) * weight 
            for category, weight in self.weights.items()
        )
        
        # 自由度等级
        if weighted_score >= 0.8:
            level = "高度自由"
            color = "green"
        elif weighted_score >= 0.6:
            level = "相对自由"
            color = "yellow"
        elif weighted_score >= 0.4:
            level = "部分自由"
            color = "orange"
        else:
            level = "受限状态"
            color = "red"
        
        return {
            'overall_score': weighted_score,
            'level': level,
            'color': color,
            'breakdown': individual_scores,
            'next_milestone': self._get_next_milestone(weighted_score),
            'improvement_priority': self._get_improvement_priority(individual_scores)
        }
    
    def _get_financial_recommendations(self, score: float, ratio: float, emergency_months: float) -> List[str]:
        """财务自由建议"""
        recommendations = []
        
        if ratio < 0.25:
            recommendations.append("优先建立被动收入流，目标是覆盖25%的月支出")
        if emergency_months < 3:
            recommendations.append("建立至少3个月的应急基金")
        if score < 0.5:
            recommendations.append("考虑投资理财产品，如指数基金或房地产投资信托")
            recommendations.append("探索副业机会，增加收入来源")
        
        return recommendations
    
    def _get_time_recommendations(self, score: float, work_hours: int) -> List[str]:
        """时间自由建议"""
        recommendations = []
        
        if work_hours > 50:
            recommendations.append("寻找工作效率提升方法，减少工作时间")
        if score < 0.4:
            recommendations.append("与雇主协商灵活工作安排")
            recommendations.append("考虑转向自由职业或远程工作")
        
        return recommendations
    
    def _get_location_recommendations(self, score: float, can_work_anywhere: bool) -> List[str]:
        """地理自由建议"""
        recommendations = []
        
        if not can_work_anywhere:
            recommendations.append("发展可远程工作的技能")
            recommendations.append("寻找支持远程工作的雇主或客户")
        if score < 0.5:
            recommendations.append("计划更多的旅行和探索")
            recommendations.append("考虑数字游民生活方式")
        
        return recommendations
    
    def _get_skill_recommendations(self, score: float, skill_count: int) -> List[str]:
        """技能自由建议"""
        recommendations = []
        
        if skill_count < 5:
            recommendations.append("学习更多可转移的技能")
        if score < 0.6:
            recommendations.append("关注市场需求高的技能")
            recommendations.append("建立持续学习的习惯")
        
        return recommendations
    
    def _get_next_milestone(self, score: float) -> str:
        """获取下一个里程碑"""
        if score < 0.4:
            return "达到部分自由状态 (40%)"
        elif score < 0.6:
            return "达到相对自由状态 (60%)"
        elif score < 0.8:
            return "达到高度自由状态 (80%)"
        else:
            return "维持并优化当前自由状态"
    
    def _get_improvement_priority(self, scores: Dict[str, float]) -> str:
        """获取改进优先级"""
        # 找到得分最低的维度
        min_category = min(scores.items(), key=lambda x: x[1])
        return f"优先提升{min_category[0]}自由度 (当前: {min_category[1]:.1%})"

def main():
    """命令行工具主函数"""
    parser = argparse.ArgumentParser(description='自由度计算器')
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--interactive', action='store_true', help='交互式模式')
    
    args = parser.parse_args()
    
    calculator = FreedomCalculator()
    
    if args.interactive:
        # 交互式输入
        print("=== 自由度评估工具 ===\n")
        
        # 财务数据
        print("1. 财务信息:")
        passive_income = float(input("被动收入 (月): ") or "0")
        active_income = float(input("主动收入 (月): ") or "0")
        monthly_expenses = float(input("月支出: ") or "0")
        emergency_fund = float(input("应急基金: ") or "0")
        
        # 时间数据
        print("\n2. 时间信息:")
        work_hours = int(input("每周工作时间: ") or "40")
        flexible_hours = int(input("灵活工作时间: ") or "0")
        vacation_days = int(input("年假天数: ") or "0")
        remote_work = input("可以远程工作? (y/n): ").lower() == 'y'
        
        # 地理数据
        print("\n3. 地理信息:")
        work_anywhere = input("可以在任何地方工作? (y/n): ").lower() == 'y'
        travel_freq = int(input("每年旅行次数: ") or "0")
        constraints = int(input("地理限制数量: ") or "0")
        
        # 技能数据
        print("\n4. 技能信息:")
        skills_input = input("可转移技能 (用逗号分隔): ")
        skills = [s.strip() for s in skills_input.split(',') if s.strip()]
        learning_rate = int(input("每年学习新技能数量: ") or "0")
        
        # 计算各维度自由度
        financial_data = {
            'passive_income': passive_income,
            'active_income': active_income,
            'monthly_expenses': monthly_expenses,
            'emergency_fund': emergency_fund
        }
        
        time_data = {
            'work_hours_per_week': work_hours,
            'flexible_hours': flexible_hours,
            'vacation_days': vacation_days,
            'can_work_remotely': remote_work
        }
        
        location_data = {
            'can_work_anywhere': work_anywhere,
            'travel_frequency': travel_freq,
            'location_constraints': constraints
        }
        
        skill_data = {
            'transferable_skills': skills,
            'learning_rate': learning_rate,
            'market_demand_skills': ['AI', 'Python', '数据分析', '数字营销', '项目管理']
        }
        
        # 计算结果
        financial_result = calculator.calculate_financial_freedom(financial_data)
        time_result = calculator.calculate_time_freedom(time_data)
        location_result = calculator.calculate_location_freedom(location_data)
        skill_result = calculator.calculate_skill_freedom(skill_data)
        
        individual_scores = {
            'financial': financial_result['score'],
            'time': time_result['score'],
            'location': location_result['score'],
            'skill': skill_result['score'],
            'relationship': 0.5  # 简化处理
        }
        
        overall_result = calculator.calculate_overall_freedom(individual_scores)
        
        # 输出结果
        print("\n" + "="*50)
        print("自由度评估结果")
        print("="*50)
        print(f"综合自由度: {overall_result['overall_score']:.1%} ({overall_result['level']})")
        print(f"下一个目标: {overall_result['next_milestone']}")
        print(f"改进建议: {overall_result['improvement_priority']}")
        
        print("\n详细分析:")
        print(f"财务自由度: {financial_result['score']:.1%}")
        for rec in financial_result['recommendations']:
            print(f"  • {rec}")
        
        print(f"\n时间自由度: {time_result['score']:.1%}")
        for rec in time_result['recommendations']:
            print(f"  • {rec}")
        
        print(f"\n地理自由度: {location_result['score']:.1%}")
        for rec in location_result['recommendations']:
            print(f"  • {rec}")
        
        print(f"\n技能自由度: {skill_result['score']:.1%}")
        for rec in skill_result['recommendations']:
            print(f"  • {rec}")
    
    elif args.config:
        # 从配置文件读取
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 处理配置文件数据...
        print("从配置文件计算自由度...")
    
    else:
        print("请使用 --interactive 进行交互式评估，或 --config 指定配置文件")

if __name__ == "__main__":
    main()
