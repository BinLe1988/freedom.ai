#!/usr/bin/env python3
"""
Freedom.AI 演示脚本
展示完整的自由探索生活指南功能
"""

import asyncio
import json
from datetime import datetime
from ai_agents_architecture import FreedomAIOrchestrator, Opportunity
from tools.freedom_calculator import FreedomCalculator

def print_header(title):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    """打印章节"""
    print(f"\n--- {title} ---")

async def demo_freedom_assessment():
    """演示自由度评估"""
    print_header("Freedom.AI 自由探索生活指南演示")
    
    calculator = FreedomCalculator()
    
    # 示例用户数据
    user_data = {
        'financial': {
            'passive_income': 3000,
            'active_income': 12000,
            'monthly_expenses': 8000,
            'emergency_fund': 50000
        },
        'time': {
            'work_hours_per_week': 50,
            'flexible_hours': 15,
            'vacation_days': 20,
            'can_work_remotely': True
        },
        'location': {
            'can_work_anywhere': False,
            'travel_frequency': 3,
            'location_constraints': 2
        },
        'skill': {
            'transferable_skills': ['Python编程', '数据分析', '项目管理', 'AI工具使用'],
            'learning_rate': 3,
            'market_demand_skills': ['AI', 'Python', '数据分析', '数字营销', '项目管理']
        }
    }
    
    print_section("1. 自由度评估")
    
    # 计算各维度自由度
    financial_result = calculator.calculate_financial_freedom(user_data['financial'])
    time_result = calculator.calculate_time_freedom(user_data['time'])
    location_result = calculator.calculate_location_freedom(user_data['location'])
    skill_result = calculator.calculate_skill_freedom(user_data['skill'])
    
    individual_scores = {
        'financial': financial_result['score'],
        'time': time_result['score'],
        'location': location_result['score'],
        'skill': skill_result['score'],
        'relationship': 0.7
    }
    
    overall_result = calculator.calculate_overall_freedom(individual_scores)
    
    print(f"📊 综合自由度: {overall_result['overall_score']:.1%} ({overall_result['level']})")
    print(f"🎯 下一个目标: {overall_result['next_milestone']}")
    print(f"💡 改进建议: {overall_result['improvement_priority']}")
    
    print("\n详细分析:")
    print(f"💰 财务自由度: {financial_result['score']:.1%}")
    print(f"⏰ 时间自由度: {time_result['score']:.1%}")
    print(f"🌍 地理自由度: {location_result['score']:.1%}")
    print(f"🛠️ 技能自由度: {skill_result['score']:.1%}")
    
    return user_data, overall_result

async def demo_ai_agents(user_data):
    """演示AI智能体功能"""
    print_section("2. AI智能体协同工作")
    
    orchestrator = FreedomAIOrchestrator()
    
    # 机会探索AI
    print("\n🔍 机会探索AI 正在分析市场...")
    opportunity_data = {
        'user_profile': {
            'skills': user_data['skill']['transferable_skills'],
            'freedom_level': 0.65,
            'preferences': ['远程工作', '技术相关', '创收潜力高']
        },
        'market_trends': ['AI工具应用', '远程工作服务', '在线教育', '数字营销']
    }
    
    opportunities_result = await orchestrator.process_user_request("discover_opportunities", opportunity_data)
    
    print("发现的机会:")
    for i, opp in enumerate(opportunities_result['new_opportunities'][:3], 1):
        print(f"  {i}. {opp.title}")
        print(f"     💰 收入潜力: ¥{opp.potential_income:,.0f}/月")
        print(f"     ⏱️ 时间投入: {opp.time_investment}小时/周")
        print(f"     ⚠️ 风险等级: {opp.risk_level}/10")
    
    # 决策支持AI
    print("\n🧠 决策支持AI 正在评估机会...")
    decision_data = {
        'opportunities': opportunities_result['new_opportunities'],
        'goals': [],
        'metrics': user_data
    }
    
    decision_result = await orchestrator.process_user_request("evaluate_opportunities", decision_data)
    
    print("AI推荐的最佳机会:")
    top_opportunity = decision_result['recommended_opportunities'][0]
    print(f"  🏆 {top_opportunity['opportunity'].title}")
    print(f"  📊 评分: {top_opportunity['score']:.2f}/1.0")
    print(f"  💭 推理: {top_opportunity['reasoning']}")
    
    # 学习伙伴AI
    print("\n🎓 学习伙伴AI 制定学习计划...")
    learning_data = {
        'current_skills': user_data['skill']['transferable_skills'],
        'target_skills': ['AI提示工程', '内容创作', '数字营销', '自动化工具开发'],
        'learning_style': 'mixed'
    }
    
    learning_result = await orchestrator.process_user_request("learning_guidance", learning_data)
    
    print("个性化学习路径:")
    for phase in learning_result['learning_path'][:2]:
        print(f"  阶段{phase['phase']}: {phase['skill']}")
        print(f"    方法: {phase['method']}")
        print(f"    时长: {phase['duration']}")
    
    # 执行助手AI
    print("\n⚙️ 执行助手AI 制定行动计划...")
    execution_data = {
        'task': top_opportunity['opportunity'].title,
        'context': {'deadline': '30天', 'resources': '有限'}
    }
    
    execution_result = await orchestrator.process_user_request("plan_execution", execution_data)
    
    print("执行计划:")
    print(f"  📅 预计时间: {execution_result['estimated_time']}小时")
    print(f"  🎯 里程碑: {len(execution_result['subtasks'])}个阶段")
    print("  自动化建议:")
    for suggestion in execution_result['automation_suggestions'][:2]:
        print(f"    • {suggestion}")
    
    return opportunities_result, decision_result, learning_result, execution_result

def demo_income_strategies():
    """演示收入策略"""
    print_section("3. 多元化收入策略")
    
    strategies = {
        "数字资产创建": {
            "在线课程": "AI工具使用教程 - 月收入潜力: ¥5,000-15,000",
            "数字产品": "自动化工具开发 - 月收入潜力: ¥3,000-10,000",
            "内容创作": "技术博客/视频 - 月收入潜力: ¥2,000-8,000"
        },
        "技能服务化": {
            "咨询服务": "AI应用咨询 - 时薪: ¥300-800",
            "自由职业": "数据分析项目 - 项目收入: ¥5,000-20,000",
            "远程工作": "技术顾问 - 月收入: ¥8,000-25,000"
        },
        "投资组合": {
            "股票基金": "指数基金定投 - 年化收益: 8-12%",
            "数字资产": "加密货币投资 - 高风险高收益",
            "房地产": "REITs投资 - 稳定分红收益"
        }
    }
    
    for category, items in strategies.items():
        print(f"\n📈 {category}:")
        for name, desc in items.items():
            print(f"  • {name}: {desc}")

def demo_freedom_roadmap():
    """演示自由实现路线图"""
    print_section("4. 自由实现路线图")
    
    roadmap = {
        "阶段1: 基础建设 (1-3个月)": [
            "完成详细的自由度评估",
            "建立第一个被动收入流",
            "优化时间管理和工作效率",
            "学习1-2个高需求技能"
        ],
        "阶段2: 扩展发展 (3-12个月)": [
            "建立2-3个收入来源",
            "实现25%的财务自由度",
            "获得远程工作能力",
            "建立个人品牌和网络"
        ],
        "阶段3: 自由实现 (12个月+)": [
            "被动收入覆盖基本生活成本",
            "实现地理位置独立",
            "建立可扩展的商业模式",
            "帮助他人实现自由"
        ]
    }
    
    for phase, tasks in roadmap.items():
        print(f"\n🚀 {phase}")
        for task in tasks:
            print(f"  ✓ {task}")

async def main():
    """主演示函数"""
    try:
        # 自由度评估
        user_data, freedom_result = await demo_freedom_assessment()
        
        # AI智能体演示
        await demo_ai_agents(user_data)
        
        # 收入策略
        demo_income_strategies()
        
        # 实现路线图
        demo_freedom_roadmap()
        
        print_header("演示总结")
        print("🎉 Freedom.AI 为你提供:")
        print("  • 科学的自由度评估体系")
        print("  • 智能的机会发现和分析")
        print("  • 个性化的学习和执行计划")
        print("  • 多元化的收入实现策略")
        print("  • 清晰的自由实现路线图")
        
        print("\n🚀 开始你的自由之旅:")
        print("  1. 运行: python3 start.py --calculator")
        print("  2. 或访问: python3 start.py --web")
        print("  3. 探索更多: 查看 life_guide_framework.md")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        print("这可能是因为缺少某些依赖包，请运行: python3 start.py --setup")

if __name__ == "__main__":
    asyncio.run(main())
