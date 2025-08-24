#!/usr/bin/env python3
"""
Freedom.AI 简化演示脚本
不依赖外部API的核心功能展示
"""

import json
from tools.freedom_calculator import FreedomCalculator

def print_header(title):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    """打印章节"""
    print(f"\n--- {title} ---")

def demo_freedom_assessment():
    """演示自由度评估"""
    print_header("Freedom.AI 自由探索生活指南演示")
    
    calculator = FreedomCalculator()
    
    # 示例用户数据 - 一个想要更多自由的程序员
    user_data = {
        'financial': {
            'passive_income': 2000,    # 投资收益
            'active_income': 15000,    # 工资收入
            'monthly_expenses': 8000,   # 月支出
            'emergency_fund': 48000     # 应急基金
        },
        'time': {
            'work_hours_per_week': 50,  # 每周工作50小时
            'flexible_hours': 10,       # 10小时可灵活安排
            'vacation_days': 15,        # 年假15天
            'can_work_remotely': True   # 可以远程工作
        },
        'location': {
            'can_work_anywhere': False, # 不能在任何地方工作
            'travel_frequency': 2,      # 每年旅行2次
            'location_constraints': 1   # 1个地理限制
        },
        'skill': {
            'transferable_skills': ['Python编程', '数据分析', '项目管理', 'AI工具使用'],
            'learning_rate': 2,         # 每年学习2个新技能
            'market_demand_skills': ['AI', 'Python', '数据分析', '数字营销', '项目管理']
        }
    }
    
    print_section("1. 当前自由度评估")
    print("👤 用户画像: 30岁程序员，希望获得更多时间和地理自由")
    
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
        'relationship': 0.6  # 假设关系自由度为60%
    }
    
    overall_result = calculator.calculate_overall_freedom(individual_scores)
    
    print(f"\n📊 综合自由度: {overall_result['overall_score']:.1%} ({overall_result['level']})")
    print(f"🎯 下一个目标: {overall_result['next_milestone']}")
    print(f"💡 改进建议: {overall_result['improvement_priority']}")
    
    print("\n详细分析:")
    print(f"💰 财务自由度: {financial_result['score']:.1%}")
    print(f"   - 被动收入比例: {financial_result['basic_ratio']:.1%}")
    print(f"   - 应急基金: {financial_result['emergency_months']:.1f}个月")
    
    print(f"⏰ 时间自由度: {time_result['score']:.1%}")
    print(f"   - 时间灵活性: {time_result['time_flexibility']:.1%}")
    print(f"   - 远程工作: {'是' if time_result['remote_work'] else '否'}")
    
    print(f"🌍 地理自由度: {location_result['score']:.1%}")
    print(f"   - 工作地点自由: {location_result['work_location_freedom']:.1%}")
    print(f"   - 地理限制: {location_result['constraints']}个")
    
    print(f"🛠️ 技能自由度: {skill_result['score']:.1%}")
    print(f"   - 技能多样性: {skill_result['skill_diversity']:.1%}")
    print(f"   - 市场匹配度: {skill_result['market_match']:.1%}")
    
    return user_data, overall_result, individual_scores

def demo_improvement_suggestions(financial_result, time_result, location_result, skill_result):
    """演示改进建议"""
    print_section("2. AI智能改进建议")
    
    print("💰 财务自由度提升建议:")
    for rec in financial_result['recommendations']:
        print(f"   • {rec}")
    
    print("\n⏰时间自由度提升建议:")
    for rec in time_result['recommendations']:
        print(f"   • {rec}")
    
    print("\n🌍 地理自由度提升建议:")
    for rec in location_result['recommendations']:
        print(f"   • {rec}")
    
    print("\n🛠️ 技能自由度提升建议:")
    for rec in skill_result['recommendations']:
        print(f"   • {rec}")

def demo_opportunity_discovery():
    """演示机会发现"""
    print_section("3. 机会探索与发现")
    
    opportunities = [
        {
            "title": "AI内容创作服务",
            "description": "为企业提供AI辅助的内容创作和营销服务",
            "potential_income": 8000,
            "time_investment": 20,
            "risk_level": 3,
            "skills_required": ["AI工具使用", "内容策划", "客户沟通"],
            "market_trend": "AI工具应用热潮"
        },
        {
            "title": "在线编程教育",
            "description": "创建Python和数据分析在线课程",
            "potential_income": 5000,
            "time_investment": 25,
            "risk_level": 4,
            "skills_required": ["Python编程", "教学能力", "视频制作"],
            "market_trend": "在线教育需求增长"
        },
        {
            "title": "远程技术咨询",
            "description": "为中小企业提供技术咨询和解决方案",
            "potential_income": 12000,
            "time_investment": 30,
            "risk_level": 2,
            "skills_required": ["项目管理", "技术架构", "商务沟通"],
            "market_trend": "远程服务需求上升"
        }
    ]
    
    print("🔍 基于你的技能和市场趋势，发现以下机会:")
    
    for i, opp in enumerate(opportunities, 1):
        print(f"\n{i}. {opp['title']}")
        print(f"   📝 {opp['description']}")
        print(f"   💰 收入潜力: ¥{opp['potential_income']:,}/月")
        print(f"   ⏱️ 时间投入: {opp['time_investment']}小时/周")
        print(f"   ⚠️ 风险等级: {opp['risk_level']}/10")
        print(f"   🎯 所需技能: {', '.join(opp['skills_required'])}")
        print(f"   📈 市场趋势: {opp['market_trend']}")
    
    return opportunities

def demo_learning_path():
    """演示学习路径规划"""
    print_section("4. 个性化学习路径")
    
    current_skills = ['Python编程', '数据分析', '项目管理', 'AI工具使用']
    target_skills = ['AI提示工程', '内容创作', '数字营销', '自动化工具开发', '商务沟通']
    
    print("📚 基于技能差距分析，推荐学习路径:")
    
    learning_phases = [
        {
            "phase": 1,
            "skill": "AI提示工程",
            "duration": "4-6周",
            "method": "在线课程 + 实践项目",
            "resources": ["ChatGPT官方文档", "Prompt Engineering课程", "实际项目练习"],
            "milestone": "能够设计高效的AI提示词"
        },
        {
            "phase": 2,
            "skill": "内容创作",
            "duration": "6-8周",
            "method": "写作练习 + AI辅助创作",
            "resources": ["内容营销课程", "写作工具", "行业案例分析"],
            "milestone": "能够创作高质量的技术内容"
        },
        {
            "phase": 3,
            "skill": "数字营销",
            "duration": "8-10周",
            "method": "理论学习 + 实战操作",
            "resources": ["Google Analytics", "社交媒体营销", "SEO基础"],
            "milestone": "能够制定和执行营销策略"
        }
    ]
    
    for phase in learning_phases:
        print(f"\n阶段 {phase['phase']}: {phase['skill']}")
        print(f"   ⏰ 学习时长: {phase['duration']}")
        print(f"   📖 学习方法: {phase['method']}")
        print(f"   🎯 里程碑: {phase['milestone']}")
        print(f"   📚 推荐资源: {', '.join(phase['resources'][:2])}")

def demo_action_plan():
    """演示行动计划"""
    print_section("5. 30天行动计划")
    
    action_plan = {
        "第1周: 基础准备": [
            "完成详细的技能和资源盘点",
            "设置学习环境和工具",
            "制定每日学习计划(2小时/天)",
            "开始AI提示工程基础学习"
        ],
        "第2周: 技能建设": [
            "深入学习AI工具应用",
            "完成3个AI内容创作练习",
            "建立个人作品集网站",
            "开始建立专业社交网络"
        ],
        "第3周: 实践应用": [
            "寻找第一个潜在客户或项目",
            "制作服务介绍和案例展示",
            "在专业平台发布技能服务",
            "开始内容创作和个人品牌建设"
        ],
        "第4周: 优化迭代": [
            "收集反馈并优化服务",
            "扩大营销和推广渠道",
            "建立客户关系管理系统",
            "制定下个月的发展计划"
        ]
    }
    
    print("📅 基于你的目标，制定30天快速启动计划:")
    
    for week, tasks in action_plan.items():
        print(f"\n{week}:")
        for task in tasks:
            print(f"   ✓ {task}")

def demo_income_projection():
    """演示收入预测"""
    print_section("6. 收入增长预测")
    
    projections = [
        {"month": 1, "passive": 2000, "new_income": 0, "total": 2000, "freedom_increase": 0},
        {"month": 3, "passive": 2000, "new_income": 3000, "total": 5000, "freedom_increase": 15},
        {"month": 6, "passive": 2500, "new_income": 6000, "total": 8500, "freedom_increase": 25},
        {"month": 12, "passive": 3000, "new_income": 10000, "total": 13000, "freedom_increase": 40}
    ]
    
    print("📈 基于行动计划的收入增长预测:")
    print("月份 | 被动收入 | 新增收入 | 总收入 | 自由度提升")
    print("-" * 50)
    
    for proj in projections:
        print(f"{proj['month']:2d}月 | ¥{proj['passive']:,} | ¥{proj['new_income']:,} | ¥{proj['total']:,} | +{proj['freedom_increase']}%")
    
    print(f"\n🎯 12个月目标:")
    print(f"   • 被动收入增长: ¥2,000 → ¥3,000 (+50%)")
    print(f"   • 新增收入流: ¥0 → ¥10,000")
    print(f"   • 财务自由度: 25% → 65%")
    print(f"   • 综合自由度: 预计提升至75%+")

def demo_success_metrics():
    """演示成功指标"""
    print_section("7. 成功指标与里程碑")
    
    metrics = {
        "短期目标 (1-3个月)": {
            "财务指标": ["建立第一个副业收入流", "月收入增加¥3,000+"],
            "技能指标": ["掌握AI工具应用", "完成5个实践项目"],
            "自由度指标": ["时间自由度提升10%", "开始远程工作"]
        },
        "中期目标 (3-12个月)": {
            "财务指标": ["副业收入达到¥8,000/月", "被动收入增长50%"],
            "技能指标": ["建立个人品牌", "获得10+客户好评"],
            "自由度指标": ["实现地理位置灵活", "综合自由度达到70%"]
        },
        "长期目标 (12个月+)": {
            "财务指标": ["被动收入覆盖基本支出", "建立可扩展商业模式"],
            "技能指标": ["成为领域专家", "帮助他人实现自由"],
            "自由度指标": ["达到高度自由状态", "实现工作生活平衡"]
        }
    }
    
    for period, categories in metrics.items():
        print(f"\n🎯 {period}:")
        for category, goals in categories.items():
            print(f"   {category}:")
            for goal in goals:
                print(f"     • {goal}")

def main():
    """主演示函数"""
    try:
        # 1. 自由度评估
        user_data, freedom_result, individual_scores = demo_freedom_assessment()
        
        # 2. 改进建议
        calculator = FreedomCalculator()
        financial_result = calculator.calculate_financial_freedom(user_data['financial'])
        time_result = calculator.calculate_time_freedom(user_data['time'])
        location_result = calculator.calculate_location_freedom(user_data['location'])
        skill_result = calculator.calculate_skill_freedom(user_data['skill'])
        
        demo_improvement_suggestions(financial_result, time_result, location_result, skill_result)
        
        # 3. 机会发现
        opportunities = demo_opportunity_discovery()
        
        # 4. 学习路径
        demo_learning_path()
        
        # 5. 行动计划
        demo_action_plan()
        
        # 6. 收入预测
        demo_income_projection()
        
        # 7. 成功指标
        demo_success_metrics()
        
        # 总结
        print_header("Freedom.AI 系统总结")
        print("🎉 Freedom.AI 为你提供完整的自由探索解决方案:")
        print("   ✓ 科学的五维自由度评估体系")
        print("   ✓ 基于AI的智能机会发现")
        print("   ✓ 个性化的技能提升路径")
        print("   ✓ 详细的执行行动计划")
        print("   ✓ 可量化的成功指标体系")
        
        print("\n🚀 立即开始你的自由之旅:")
        print("   1. 交互式评估: python3 tools/freedom_calculator.py --interactive")
        print("   2. Web界面体验: python3 start.py --web")
        print("   3. 查看完整框架: cat life_guide_framework.md")
        print("   4. 环境初始化: python3 start.py --setup")
        
        print(f"\n💡 基于你当前{freedom_result['overall_score']:.1%}的自由度，")
        print("   建议优先关注时间和地理自由度的提升！")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        print("请确保所有文件都已正确创建")

if __name__ == "__main__":
    main()
