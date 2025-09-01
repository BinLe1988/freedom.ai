'use client'

import { useState } from 'react'
import Link from 'next/link'

interface UserProfile {
  skills: string[]
  interests: string[]
  experience: string
  timeAvailable: number // hours per week
  riskTolerance: 'low' | 'medium' | 'high'
  investmentCapacity: number // in yuan
}

interface Opportunity {
  id: string
  title: string
  category: string
  description: string
  potentialIncome: {
    min: number
    max: number
    timeframe: string
  }
  requirements: {
    skills: string[]
    timeCommitment: number
    initialInvestment: number
  }
  riskLevel: number // 1-10
  marketTrend: 'rising' | 'stable' | 'declining'
  difficulty: 'easy' | 'medium' | 'hard'
  successRate: number // 0-100
  steps: string[]
  pros: string[]
  cons: string[]
  realExamples: string[]
}

export default function OpportunitiesPage() {
  const [profile, setProfile] = useState<UserProfile>({
    skills: [],
    interests: [],
    experience: 'beginner',
    timeAvailable: 10,
    riskTolerance: 'medium',
    investmentCapacity: 10000
  })
  
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [showProfileForm, setShowProfileForm] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  const skillOptions = [
    '编程开发', '设计创意', '写作文案', '数据分析', '市场营销', '销售技巧',
    '语言翻译', '视频制作', '摄影拍照', '教学培训', '咨询顾问', '项目管理',
    '财务会计', '法律服务', '医疗健康', '手工制作', '音乐艺术', '运动健身'
  ]

  const interestOptions = [
    '科技创新', '金融投资', '电商零售', '内容创作', '教育培训', '健康养生',
    '旅游出行', '美食餐饮', '时尚潮流', '家居生活', '宠物服务', '环保公益',
    '游戏娱乐', '社交网络', '文化艺术', '体育运动', '汽车交通', '房产建筑'
  ]

  const categories = [
    'all', '在线业务', '自由职业', '投资理财', '创业项目', '技能变现', '内容创作', '服务咨询'
  ]

  const updateProfile = (field: keyof UserProfile, value: any) => {
    setProfile({ ...profile, [field]: value })
  }

  const toggleSkill = (skill: string) => {
    const newSkills = profile.skills.includes(skill)
      ? profile.skills.filter(s => s !== skill)
      : [...profile.skills, skill]
    updateProfile('skills', newSkills)
  }

  const toggleInterest = (interest: string) => {
    const newInterests = profile.interests.includes(interest)
      ? profile.interests.filter(i => i !== interest)
      : [...profile.interests, interest]
    updateProfile('interests', newInterests)
  }

  const discoverOpportunities = () => {
    if (profile.skills.length === 0 || profile.interests.length === 0) {
      alert('请至少选择一项技能和兴趣')
      return
    }

    setAnalyzing(true)
    setShowProfileForm(false)

    setTimeout(() => {
      const mockOpportunities: Opportunity[] = [
        {
          id: '1',
          title: '在线课程制作',
          category: '内容创作',
          description: '基于你的专业技能制作在线教学课程，通过知识付费平台销售',
          potentialIncome: { min: 5000, max: 50000, timeframe: '月' },
          requirements: {
            skills: ['教学培训', '视频制作'],
            timeCommitment: 15,
            initialInvestment: 3000
          },
          riskLevel: 3,
          marketTrend: 'rising',
          difficulty: 'medium',
          successRate: 70,
          steps: [
            '确定课程主题和目标受众',
            '制作课程大纲和内容',
            '录制高质量视频课程',
            '选择合适的销售平台',
            '制定营销推广策略',
            '持续优化和更新内容'
          ],
          pros: ['被动收入', '可扩展性强', '建立个人品牌'],
          cons: ['前期投入大', '竞争激烈', '需要持续更新'],
          realExamples: ['某程序员年收入100万', '设计师月入3万', '英语老师年入50万']
        },
        {
          id: '2',
          title: '自由职业服务',
          category: '自由职业',
          description: '利用专业技能为企业和个人提供项目制服务',
          potentialIncome: { min: 3000, max: 30000, timeframe: '月' },
          requirements: {
            skills: ['编程开发', '设计创意', '写作文案'],
            timeCommitment: 20,
            initialInvestment: 1000
          },
          riskLevel: 2,
          marketTrend: 'stable',
          difficulty: 'easy',
          successRate: 85,
          steps: [
            '完善个人作品集',
            '注册自由职业平台',
            '设定合理的服务价格',
            '积极投标和沟通',
            '按时交付高质量作品',
            '维护客户关系和口碑'
          ],
          pros: ['时间灵活', '技能提升', '收入稳定'],
          cons: ['收入波动', '需要营销', '客户管理'],
          realExamples: ['设计师月入2万', '程序员年入40万', '文案师月入1.5万']
        },
        {
          id: '3',
          title: '电商店铺运营',
          category: '在线业务',
          description: '开设网店销售产品，通过电商平台实现销售收入',
          potentialIncome: { min: 2000, max: 100000, timeframe: '月' },
          requirements: {
            skills: ['市场营销', '数据分析'],
            timeCommitment: 25,
            initialInvestment: 20000
          },
          riskLevel: 6,
          marketTrend: 'stable',
          difficulty: 'hard',
          successRate: 45,
          steps: [
            '市场调研和产品选择',
            '寻找可靠的供应商',
            '开设店铺和产品上架',
            '制定营销推广策略',
            '优化客户服务体验',
            '数据分析和持续优化'
          ],
          pros: ['收入潜力大', '可规模化', '市场广阔'],
          cons: ['竞争激烈', '资金需求大', '库存风险'],
          realExamples: ['服装店年入200万', '数码产品月入10万', '美妆店年入80万']
        },
        {
          id: '4',
          title: '投资理财组合',
          category: '投资理财',
          description: '通过多元化投资组合实现财富增值',
          potentialIncome: { min: 500, max: 20000, timeframe: '月' },
          requirements: {
            skills: ['数据分析', '财务会计'],
            timeCommitment: 5,
            initialInvestment: 50000
          },
          riskLevel: 5,
          marketTrend: 'rising',
          difficulty: 'medium',
          successRate: 60,
          steps: [
            '学习投资理财知识',
            '评估个人风险承受能力',
            '制定投资策略和目标',
            '选择合适的投资产品',
            '定期监控和调整组合',
            '长期坚持价值投资'
          ],
          pros: ['被动收入', '财富增值', '抗通胀'],
          cons: ['市场风险', '需要专业知识', '收益波动'],
          realExamples: ['基金投资年化15%', '股票投资年入30万', '债券稳定收益8%']
        },
        {
          id: '5',
          title: '内容创作变现',
          category: '内容创作',
          description: '通过短视频、直播、写作等内容创作获得收入',
          potentialIncome: { min: 1000, max: 80000, timeframe: '月' },
          requirements: {
            skills: ['写作文案', '视频制作', '市场营销'],
            timeCommitment: 30,
            initialInvestment: 5000
          },
          riskLevel: 4,
          marketTrend: 'rising',
          difficulty: 'medium',
          successRate: 55,
          steps: [
            '确定内容定位和风格',
            '选择合适的平台渠道',
            '制作高质量原创内容',
            '建立粉丝社群',
            '探索多元化变现方式',
            '持续创新和优化内容'
          ],
          pros: ['创意自由', '影响力大', '多种变现方式'],
          cons: ['竞争激烈', '收入不稳定', '需要持续创作'],
          realExamples: ['知识博主年入100万', '美食UP主月入5万', '财经作者年入60万']
        }
      ]

      // 根据用户画像筛选和排序机会
      const filteredOpportunities = mockOpportunities.filter(opp => {
        const skillMatch = opp.requirements.skills.some(skill => profile.skills.includes(skill))
        const timeMatch = opp.requirements.timeCommitment <= profile.timeAvailable
        const investmentMatch = opp.requirements.initialInvestment <= profile.investmentCapacity
        const riskMatch = 
          (profile.riskTolerance === 'low' && opp.riskLevel <= 3) ||
          (profile.riskTolerance === 'medium' && opp.riskLevel <= 6) ||
          (profile.riskTolerance === 'high')
        
        return skillMatch && timeMatch && investmentMatch && riskMatch
      }).sort((a, b) => b.successRate - a.successRate)

      setOpportunities(filteredOpportunities)
      setAnalyzing(false)
    }, 3000)
  }

  const getRiskColor = (level: number) => {
    if (level <= 3) return 'text-green-400 bg-green-900/20'
    if (level <= 6) return 'text-yellow-400 bg-yellow-900/20'
    return 'text-red-400 bg-red-900/20'
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'rising': return '📈'
      case 'stable': return '➡️'
      case 'declining': return '📉'
      default: return '➡️'
    }
  }

  const filteredOpportunities = selectedCategory === 'all' 
    ? opportunities 
    : opportunities.filter(opp => opp.category === selectedCategory)

  return (
    <div className="min-h-screen bg-gray-900">
      {/* 导航栏 */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-2xl">🔍</span>
              <span className="text-2xl font-bold text-white">Freedom.AI</span>
            </Link>
            <Link href="/" className="text-gray-300 hover:text-blue-400 transition-colors">
              ← 返回首页
            </Link>
          </div>
        </div>
      </nav>
      
      <div className="container mx-auto px-4 pt-24 pb-12">
        {/* 页面标题 */}
        <div className="text-center mb-12">
          <div className="text-6xl mb-4">🔍</div>
          <h1 className="text-4xl font-bold text-white mb-4">机会探索AI</h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            发现市场机会，创造收入来源，开启多元化的财务自由之路
          </p>
        </div>

        {/* 用户画像表单 */}
        {showProfileForm && (
          <div className="max-w-4xl mx-auto mb-8">
            <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
              <h2 className="text-2xl font-bold text-white mb-6">📋 个人画像分析</h2>
              
              <div className="space-y-6">
                {/* 技能选择 */}
                <div>
                  <label className="text-lg font-semibold text-blue-400 mb-3 block">你的技能 (选择3-5项)</label>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                    {skillOptions.map(skill => (
                      <button
                        key={skill}
                        onClick={() => toggleSkill(skill)}
                        className={`px-3 py-2 rounded-lg text-sm transition-colors ${
                          profile.skills.includes(skill)
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                        }`}
                      >
                        {skill}
                      </button>
                    ))}
                  </div>
                </div>

                {/* 兴趣选择 */}
                <div>
                  <label className="text-lg font-semibold text-green-400 mb-3 block">兴趣领域 (选择2-4项)</label>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                    {interestOptions.map(interest => (
                      <button
                        key={interest}
                        onClick={() => toggleInterest(interest)}
                        className={`px-3 py-2 rounded-lg text-sm transition-colors ${
                          profile.interests.includes(interest)
                            ? 'bg-green-600 text-white'
                            : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                        }`}
                      >
                        {interest}
                      </button>
                    ))}
                  </div>
                </div>

                {/* 其他参数 */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div>
                    <label className="text-gray-300 text-sm mb-2 block">经验水平</label>
                    <select
                      value={profile.experience}
                      onChange={(e) => updateProfile('experience', e.target.value)}
                      className="w-full bg-gray-800 text-white rounded-lg px-3 py-2"
                    >
                      <option value="beginner">初学者</option>
                      <option value="intermediate">有经验</option>
                      <option value="expert">专家级</option>
                    </select>
                  </div>

                  <div>
                    <label className="text-gray-300 text-sm mb-2 block">每周可投入时间: {profile.timeAvailable}小时</label>
                    <input
                      type="range"
                      min="5"
                      max="40"
                      value={profile.timeAvailable}
                      onChange={(e) => updateProfile('timeAvailable', Number(e.target.value))}
                      className="w-full"
                    />
                  </div>

                  <div>
                    <label className="text-gray-300 text-sm mb-2 block">风险承受能力</label>
                    <select
                      value={profile.riskTolerance}
                      onChange={(e) => updateProfile('riskTolerance', e.target.value)}
                      className="w-full bg-gray-800 text-white rounded-lg px-3 py-2"
                    >
                      <option value="low">保守型</option>
                      <option value="medium">平衡型</option>
                      <option value="high">激进型</option>
                    </select>
                  </div>

                  <div>
                    <label className="text-gray-300 text-sm mb-2 block">初始投资能力: ¥{profile.investmentCapacity.toLocaleString()}</label>
                    <input
                      type="range"
                      min="1000"
                      max="100000"
                      step="1000"
                      value={profile.investmentCapacity}
                      onChange={(e) => updateProfile('investmentCapacity', Number(e.target.value))}
                      className="w-full"
                    />
                  </div>
                </div>

                <button
                  onClick={discoverOpportunities}
                  disabled={analyzing}
                  className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white py-3 rounded-lg text-lg font-semibold transition-colors"
                >
                  {analyzing ? '🔄 AI分析中...' : '🔍 发现机会'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* 机会列表 */}
        {opportunities.length > 0 && (
          <div>
            {/* 分类筛选 */}
            <div className="flex flex-wrap gap-2 mb-6 justify-center">
              {categories.map(category => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                    selectedCategory === category
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  {category === 'all' ? '全部' : category}
                </button>
              ))}
            </div>

            {/* 统计信息 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-6 text-center">
                <div className="text-3xl font-bold text-blue-400">{filteredOpportunities.length}</div>
                <div className="text-gray-300">匹配机会</div>
              </div>
              <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-6 text-center">
                <div className="text-3xl font-bold text-green-400">
                  ¥{Math.max(...filteredOpportunities.map(o => o.potentialIncome.max)).toLocaleString()}
                </div>
                <div className="text-gray-300">最高月收入</div>
              </div>
              <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-6 text-center">
                <div className="text-3xl font-bold text-purple-400">
                  {Math.round(filteredOpportunities.reduce((sum, o) => sum + o.successRate, 0) / filteredOpportunities.length)}%
                </div>
                <div className="text-gray-300">平均成功率</div>
              </div>
            </div>

            {/* 机会卡片 */}
            <div className="grid lg:grid-cols-2 gap-6">
              {filteredOpportunities.map(opportunity => (
                <div key={opportunity.id} className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-white mb-2">{opportunity.title}</h3>
                      <p className="text-blue-400 text-sm">{opportunity.category}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xl">{getTrendIcon(opportunity.marketTrend)}</span>
                      <span className={`px-2 py-1 rounded text-xs ${getRiskColor(opportunity.riskLevel)}`}>
                        风险{opportunity.riskLevel}/10
                      </span>
                    </div>
                  </div>

                  <p className="text-gray-300 text-sm mb-4">{opportunity.description}</p>

                  {/* 收入潜力 */}
                  <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-3 mb-4">
                    <div className="flex items-center justify-between">
                      <span className="text-green-400 font-semibold">收入潜力</span>
                      <span className="text-white font-bold">
                        ¥{opportunity.potentialIncome.min.toLocaleString()} - ¥{opportunity.potentialIncome.max.toLocaleString()}/{opportunity.potentialIncome.timeframe}
                      </span>
                    </div>
                    <div className="flex items-center justify-between mt-2 text-sm">
                      <span className="text-gray-300">成功率</span>
                      <span className="text-green-400">{opportunity.successRate}%</span>
                    </div>
                  </div>

                  {/* 要求 */}
                  <div className="mb-4">
                    <h4 className="text-gray-300 font-semibold mb-2">📋 基本要求</h4>
                    <div className="grid grid-cols-1 gap-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">时间投入:</span>
                        <span className="text-white">{opportunity.requirements.timeCommitment}小时/周</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">初始投资:</span>
                        <span className="text-white">¥{opportunity.requirements.initialInvestment.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">难度等级:</span>
                        <span className={`${
                          opportunity.difficulty === 'easy' ? 'text-green-400' :
                          opportunity.difficulty === 'medium' ? 'text-yellow-400' : 'text-red-400'
                        }`}>
                          {opportunity.difficulty === 'easy' ? '简单' :
                           opportunity.difficulty === 'medium' ? '中等' : '困难'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* 所需技能 */}
                  <div className="mb-4">
                    <h4 className="text-gray-300 font-semibold mb-2">🛠️ 所需技能</h4>
                    <div className="flex flex-wrap gap-2">
                      {opportunity.requirements.skills.map(skill => (
                        <span key={skill} className="bg-blue-900/30 text-blue-300 px-2 py-1 rounded text-xs">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* 优缺点 */}
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <h4 className="text-green-400 font-semibold mb-2 text-sm">✅ 优势</h4>
                      <ul className="text-xs text-gray-300 space-y-1">
                        {opportunity.pros.map((pro, index) => (
                          <li key={index}>• {pro}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="text-red-400 font-semibold mb-2 text-sm">⚠️ 挑战</h4>
                      <ul className="text-xs text-gray-300 space-y-1">
                        {opportunity.cons.map((con, index) => (
                          <li key={index}>• {con}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* 成功案例 */}
                  <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-3">
                    <h4 className="text-purple-400 font-semibold mb-2 text-sm">🏆 成功案例</h4>
                    <div className="text-xs text-gray-300 space-y-1">
                      {opportunity.realExamples.map((example, index) => (
                        <div key={index}>• {example}</div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {filteredOpportunities.length === 0 && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-xl font-semibold text-gray-400 mb-2">暂无匹配机会</h3>
                <p className="text-gray-500">尝试调整筛选条件或个人画像设置</p>
              </div>
            )}
          </div>
        )}

        {!showProfileForm && opportunities.length === 0 && !analyzing && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">😔</div>
            <h3 className="text-xl font-semibold text-gray-400 mb-2">未找到匹配的机会</h3>
            <p className="text-gray-500 mb-4">根据你的条件，暂时没有找到合适的机会</p>
            <button
              onClick={() => setShowProfileForm(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
            >
              重新设置条件
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
