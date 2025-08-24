#!/usr/bin/env python3
"""
JobLeads集成演示脚本
展示如何在Freedom.AI中集成JobLeads职位数据
"""

import sys
import os

# 添加路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'integrations'))

def demo_jobleads_integration():
    """演示JobLeads集成功能"""
    print("=== Freedom.AI × JobLeads 职位集成演示 ===\n")
    
    try:
        from jobleads_api import JobLeadsAPI
        
        # 初始化JobLeads API客户端
        jobleads = JobLeadsAPI()
        print("✅ JobLeads API客户端初始化成功")
        
        # 模拟用户技能
        user_skills = ['Python编程', '数据分析', '项目管理', 'AI工具使用']
        print(f"👤 用户技能: {', '.join(user_skills)}")
        
        # 用户偏好设置
        preferences = {
            'remote': True,
            'salary_min': 20000,
            'job_type': None,
            'limit': 8
        }
        print(f"⚙️ 搜索偏好: 远程工作={preferences['remote']}, 最低薪资={preferences['salary_min']}")
        print()
        
        # 获取职位推荐
        print("🔍 正在搜索匹配的职位...")
        jobs = jobleads.get_job_recommendations(user_skills, preferences)
        
        print(f"📋 找到 {len(jobs)} 个匹配职位:\n")
        
        # 显示推荐职位
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job['title']}")
            print(f"   🏢 公司: {job['company']}")
            print(f"   📍 地点: {job['location']}")
            print(f"   💰 薪资: {job['salary_range']}")
            print(f"   🏷️ 类型: {job['job_type']}")
            print(f"   🌐 远程: {'支持' if job['remote_friendly'] else '不支持'}")
            print(f"   🎯 技能匹配: {job['match_score']:.1%}")
            print(f"   🆓 自由度: {job['freedom_score']:.1%}")
            print(f"   ⭐ 综合评分: {job['overall_score']:.1%}")
            
            # 显示技能要求
            if job.get('requirements'):
                print(f"   📚 技能要求: {', '.join(job['requirements'][:3])}...")
            
            # 显示福利
            if job.get('benefits'):
                print(f"   🎁 福利: {', '.join(job['benefits'][:2])}...")
            
            print(f"   🔗 申请: {job['application_url']}")
            print()
        
        # 获取市场趋势
        print("📈 JobLeads市场趋势分析:")
        trends = jobleads.get_job_trends()
        
        print(f"   🔥 热门技能: {', '.join(trends['hot_skills'][:5])}")
        print(f"   📊 远程工作: {trends['remote_job_growth']}")
        print(f"   💹 薪资趋势:")
        for category, trend in trends['salary_trends'].items():
            print(f"      • {category}: {trend}")
        print(f"   🏆 热门招聘公司: {', '.join(trends['top_companies_hiring'][:3])}")
        print()
        
        # 演示与Freedom.AI的集成
        print("🤖 与Freedom.AI自由度评估集成:")
        
        # 计算职位对自由度的影响
        high_freedom_jobs = [job for job in jobs if job['freedom_score'] > 0.8]
        remote_jobs = [job for job in jobs if job['remote_friendly']]
        
        print(f"   • 高自由度职位 (>80%): {len(high_freedom_jobs)} 个")
        print(f"   • 支持远程工作: {len(remote_jobs)} 个")
        print(f"   • 平均自由度评分: {sum(job['freedom_score'] for job in jobs) / len(jobs):.1%}")
        
        # 推荐最佳职位
        if jobs:
            best_job = max(jobs, key=lambda x: x['overall_score'])
            print(f"\n🏆 最佳推荐职位: {best_job['title']} - {best_job['company']}")
            print(f"   综合评分: {best_job['overall_score']:.1%}")
            print(f"   推荐理由: 技能匹配度高({best_job['match_score']:.1%})，自由度优秀({best_job['freedom_score']:.1%})")
        
        print("\n" + "="*60)
        print("✅ JobLeads集成演示完成！")
        print("\n💡 集成优势:")
        print("   • 实时职位数据，机会更新及时")
        print("   • 智能匹配算法，推荐更精准")
        print("   • 自由度评分，助力职业选择")
        print("   • 市场趋势分析，把握发展方向")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入JobLeads模块失败: {e}")
        print("请确保 integrations/jobleads_api.py 文件存在")
        return False
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        return False

def demo_web_integration():
    """演示Web界面集成"""
    print("\n=== Web界面集成演示 ===")
    
    print("🌐 在Web界面中使用JobLeads集成:")
    print("   1. 访问机会探索页面: /opportunities")
    print("   2. 输入你的技能和偏好")
    print("   3. 勾选 '包含JobLeads职位推荐'")
    print("   4. 点击 '发现机会' 按钮")
    print("   5. 查看混合的创业机会和职位推荐")
    
    print("\n📊 Web界面新功能:")
    print("   • 职位/创业机会分类筛选")
    print("   • JobLeads集成状态显示")
    print("   • 职位详细信息展示")
    print("   • 一键申请职位功能")
    print("   • 薪资趋势数据展示")

def main():
    """主函数"""
    success = demo_jobleads_integration()
    
    if success:
        demo_web_integration()
        
        print("\n🚀 下一步操作:")
        print("   1. 启动Web应用: python3 web/app.py")
        print("   2. 访问: http://localhost:5000/opportunities")
        print("   3. 体验JobLeads职位推荐功能")
        print("   4. 如需真实API，请配置JobLeads API密钥")
    else:
        print("\n🔧 故障排除:")
        print("   1. 确保所有文件已正确创建")
        print("   2. 检查Python路径设置")
        print("   3. 运行: python3 test_api.py 测试基础功能")

if __name__ == "__main__":
    main()
