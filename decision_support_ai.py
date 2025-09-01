#!/usr/bin/env python3
"""
决策支持AI - 智能分析机会，提供数据驱动的决策建议
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai

@dataclass
class DecisionOption:
    """决策选项"""
    name: str
    description: str
    pros: List[str]
    cons: List[str]
    risk_score: float  # 0-1
    potential_return: float
    time_investment: int  # hours
    required_resources: List[str]
    success_probability: float  # 0-1

@dataclass
class DecisionContext:
    """决策上下文"""
    goal: str
    current_situation: Dict[str, Any]
    constraints: List[str]
    priorities: List[str]
    timeline: str

@dataclass
class DecisionRecommendation:
    """决策建议"""
    recommended_option: str
    confidence_score: float  # 0-1
    reasoning: str
    risk_analysis: str
    action_plan: List[str]
    success_metrics: List[str]
    fallback_plan: str

class DecisionSupportAI:
    """决策支持AI智能体"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
    
    def analyze_decision(self, context: DecisionContext, options: List[DecisionOption]) -> DecisionRecommendation:
        """分析决策选项并提供建议"""
        
        # 计算每个选项的综合得分
        scored_options = []
        for option in options:
            score = self._calculate_option_score(option, context)
            scored_options.append((option, score))
        
        # 按得分排序
        scored_options.sort(key=lambda x: x[1], reverse=True)
        best_option = scored_options[0][0]
        
        # 生成详细分析
        recommendation = self._generate_recommendation(best_option, scored_options, context)
        
        return recommendation
    
    def _calculate_option_score(self, option: DecisionOption, context: DecisionContext) -> float:
        """计算选项综合得分"""
        
        # 基础得分计算
        return_score = min(option.potential_return / 100000, 1.0)  # 标准化收益
        risk_score = 1 - option.risk_score  # 风险越低得分越高
        probability_score = option.success_probability
        
        # 时间投资评分（考虑效率）
        time_efficiency = option.potential_return / max(option.time_investment, 1)
        time_score = min(time_efficiency / 1000, 1.0)
        
        # 综合得分（可根据用户偏好调整权重）
        total_score = (
            return_score * 0.3 +
            risk_score * 0.25 +
            probability_score * 0.25 +
            time_score * 0.2
        )
        
        return total_score
    
    def _generate_recommendation(self, best_option: DecisionOption, 
                               all_options: List[tuple], context: DecisionContext) -> DecisionRecommendation:
        """生成详细的决策建议"""
        
        # 风险分析
        risk_analysis = self._analyze_risks(best_option, context)
        
        # 行动计划
        action_plan = self._create_action_plan(best_option)
        
        # 成功指标
        success_metrics = self._define_success_metrics(best_option)
        
        # 备选方案
        fallback_plan = self._create_fallback_plan(all_options[1][0] if len(all_options) > 1 else None)
        
        # 推理过程
        reasoning = f"""
基于数据分析，推荐选择"{best_option.name}"，原因如下：

1. 潜在收益: {best_option.potential_return:,.0f}元
2. 成功概率: {best_option.success_probability*100:.1f}%
3. 风险等级: {best_option.risk_score*10:.1f}/10
4. 时间投资: {best_option.time_investment}小时

优势分析:
{chr(10).join(f"• {pro}" for pro in best_option.pros)}

需要注意的风险:
{chr(10).join(f"• {con}" for con in best_option.cons)}
        """.strip()
        
        return DecisionRecommendation(
            recommended_option=best_option.name,
            confidence_score=all_options[0][1],
            reasoning=reasoning,
            risk_analysis=risk_analysis,
            action_plan=action_plan,
            success_metrics=success_metrics,
            fallback_plan=fallback_plan
        )
    
    def _analyze_risks(self, option: DecisionOption, context: DecisionContext) -> str:
        """分析风险"""
        risk_level = "低" if option.risk_score < 0.3 else "中" if option.risk_score < 0.7 else "高"
        
        return f"""
风险等级: {risk_level} ({option.risk_score*10:.1f}/10)

主要风险因素:
{chr(10).join(f"• {con}" for con in option.cons)}

风险缓解建议:
• 制定详细的执行计划
• 设置阶段性检查点
• 准备应急预案
• 控制资源投入节奏
        """.strip()
    
    def _create_action_plan(self, option: DecisionOption) -> List[str]:
        """创建行动计划"""
        plan = [
            "第一阶段：准备和规划",
            f"• 准备所需资源: {', '.join(option.required_resources)}",
            "• 制定详细时间表",
            "• 设定阶段性目标",
            "",
            "第二阶段：执行和监控",
            "• 按计划开始执行",
            "• 定期评估进展",
            "• 及时调整策略",
            "",
            "第三阶段：优化和扩展",
            "• 总结经验教训",
            "• 优化执行流程",
            "• 寻找扩展机会"
        ]
        return plan
    
    def _define_success_metrics(self, option: DecisionOption) -> List[str]:
        """定义成功指标"""
        return [
            f"收益目标: {option.potential_return:,.0f}元",
            f"时间效率: 每小时产出 {option.potential_return/option.time_investment:,.0f}元",
            f"成功概率: 达到{option.success_probability*100:.0f}%预期",
            "风险控制: 实际风险不超过预期",
            "资源利用: 按计划使用资源"
        ]
    
    def _create_fallback_plan(self, backup_option: Optional[DecisionOption]) -> str:
        """创建备选方案"""
        if not backup_option:
            return "如果主方案失败，建议重新评估现有选项或寻找新的机会。"
        
        return f"""
备选方案: {backup_option.name}

如果主方案遇到以下情况，可考虑切换到备选方案:
• 风险超出预期
• 资源不足
• 外部环境变化
• 预期收益大幅下降

备选方案优势:
{chr(10).join(f"• {pro}" for pro in backup_option.pros)}
        """.strip()
    
    def compare_opportunities(self, opportunities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """比较多个机会"""
        
        # 转换为DecisionOption对象
        options = []
        for opp in opportunities:
            option = DecisionOption(
                name=opp.get('title', '未知机会'),
                description=opp.get('description', ''),
                pros=opp.get('pros', []),
                cons=opp.get('cons', []),
                risk_score=opp.get('risk_level', 5) / 10,
                potential_return=opp.get('potential_income', 0),
                time_investment=opp.get('time_investment', 1),
                required_resources=opp.get('skills_required', []),
                success_probability=opp.get('success_probability', 0.5)
            )
            options.append(option)
        
        # 创建决策上下文
        context = DecisionContext(
            goal="寻找最佳收入机会",
            current_situation={},
            constraints=[],
            priorities=["收益最大化", "风险控制"],
            timeline="短期到中期"
        )
        
        # 分析决策
        recommendation = self.analyze_decision(context, options)
        
        return {
            'recommended_option': recommendation.recommended_option,
            'confidence_score': recommendation.confidence_score,
            'reasoning': recommendation.reasoning,
            'risk_analysis': recommendation.risk_analysis,
            'action_plan': recommendation.action_plan,
            'success_metrics': recommendation.success_metrics,
            'fallback_plan': recommendation.fallback_plan
        }

# 使用示例
if __name__ == "__main__":
    # 创建决策支持AI
    decision_ai = DecisionSupportAI()
    
    # 示例机会数据
    opportunities = [
        {
            'title': '自由职业写作',
            'description': '为企业提供内容创作服务',
            'pros': ['时间灵活', '技能可积累', '市场需求大'],
            'cons': ['收入不稳定', '需要持续营销', '竞争激烈'],
            'risk_level': 4,
            'potential_income': 50000,
            'time_investment': 500,
            'skills_required': ['写作', '营销', '客户沟通'],
            'success_probability': 0.7
        },
        {
            'title': '在线课程制作',
            'description': '制作并销售专业技能课程',
            'pros': ['被动收入', '影响力大', '可扩展性强'],
            'cons': ['前期投入大', '制作周期长', '需要专业技能'],
            'risk_level': 6,
            'potential_income': 100000,
            'time_investment': 800,
            'skills_required': ['专业技能', '视频制作', '在线营销'],
            'success_probability': 0.5
        }
    ]
    
    # 获取决策建议
    result = decision_ai.compare_opportunities(opportunities)
    
    print("=== 决策支持AI分析结果 ===")
    print(f"推荐选项: {result['recommended_option']}")
    print(f"置信度: {result['confidence_score']:.2f}")
    print(f"\n推理过程:\n{result['reasoning']}")
    print(f"\n风险分析:\n{result['risk_analysis']}")
