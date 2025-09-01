'use client'

import { useState } from 'react'
import Link from 'next/link'

interface Skill {
  name: string
  category: string
  currentLevel: number // 1-10
  targetLevel: number // 1-10
  priority: 'high' | 'medium' | 'low'
  marketDemand: number // 1-10
}

interface LearningPath {
  skillName: string
  totalWeeks: number
  weeklyHours: number
  phases: LearningPhase[]
  resources: Resource[]
  milestones: Milestone[]
  careerImpact: string
}

interface LearningPhase {
  phase: string
  weeks: number
  description: string
  goals: string[]
}

interface Resource {
  type: 'course' | 'book' | 'practice' | 'project'
  title: string
  provider: string
  duration: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  cost: 'free' | 'paid'
}

interface Milestone {
  week: number
  title: string
  description: string
  assessment: string
}

export default function LearningPartnerPage() {
  const [skills, setSkills] = useState<Skill[]>([])
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([])
  const [showAddForm, setShowAddForm] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)

  const [newSkill, setNewSkill] = useState<Skill>({
    name: '',
    category: '',
    currentLevel: 1,
    targetLevel: 5,
    priority: 'medium',
    marketDemand: 5
  })

  const skillCategories = [
    '编程开发', '数据分析', '人工智能', '产品管理', '市场营销', 
    '设计创意', '项目管理', '语言能力', '金融投资', '创业技能'
  ]

  const addSkill = () => {
    if (newSkill.name && newSkill.category) {
      setSkills([...skills, { ...newSkill }])
      setNewSkill({
        name: '',
        category: '',
        currentLevel: 1,
        targetLevel: 5,
        priority: 'medium',
        marketDemand: 5
      })
      setShowAddForm(false)
    }
  }

  const generateLearningPaths = () => {
    if (skills.length === 0) {
      alert('请先添加一些技能目标')
      return
    }

    setAnalyzing(true)
    
    setTimeout(() => {
      const mockPaths: LearningPath[] = skills.map(skill => {
        const levelGap = skill.targetLevel - skill.currentLevel
        const baseWeeks = Math.max(levelGap * 4, 8)
        const weeklyHours = skill.priority === 'high' ? 10 : skill.priority === 'medium' ? 6 : 4

        const phases: LearningPhase[] = [
          {
            phase: '基础建立',
            weeks: Math.ceil(baseWeeks * 0.3),
            description: '掌握核心概念和基础知识',
            goals: ['理解基本概念', '熟悉基础工具', '建立知识框架']
          },
          {
            phase: '实践应用',
            weeks: Math.ceil(baseWeeks * 0.4),
            description: '通过项目实践巩固技能',
            goals: ['完成实际项目', '解决实际问题', '积累实战经验']
          },
          {
            phase: '深度提升',
            weeks: Math.ceil(baseWeeks * 0.3),
            description: '深入学习高级技能和最佳实践',
            goals: ['掌握高级技巧', '优化工作流程', '形成个人方法论']
          }
        ]

        const resources: Resource[] = [
          {
            type: 'course',
            title: `${skill.name}完整教程`,
            provider: '在线教育平台',
            duration: `${baseWeeks}周`,
            difficulty: skill.currentLevel < 3 ? 'beginner' : skill.currentLevel < 7 ? 'intermediate' : 'advanced',
            cost: 'paid'
          },
          {
            type: 'book',
            title: `${skill.name}权威指南`,
            provider: '技术出版社',
            duration: '4-6周',
            difficulty: 'intermediate',
            cost: 'paid'
          },
          {
            type: 'practice',
            title: '实战练习平台',
            provider: '编程练习网站',
            duration: '持续',
            difficulty: 'beginner',
            cost: 'free'
          },
          {
            type: 'project',
            title: '个人项目实践',
            provider: '自主学习',
            duration: `${Math.ceil(baseWeeks * 0.4)}周`,
            difficulty: 'intermediate',
            cost: 'free'
          }
        ]

        const milestones: Milestone[] = [
          {
            week: Math.ceil(baseWeeks * 0.3),
            title: '基础知识掌握',
            description: '完成基础概念学习和工具熟悉',
            assessment: '基础知识测试 + 简单练习'
          },
          {
            week: Math.ceil(baseWeeks * 0.7),
            title: '项目实践完成',
            description: '独立完成一个完整的实践项目',
            assessment: '项目展示 + 代码审查'
          },
          {
            week: baseWeeks,
            title: '技能目标达成',
            description: '达到预设的技能水平目标',
            assessment: '综合能力评估 + 同行评议'
          }
        ]

        const careerImpacts = [
          '提升职场竞争力，获得更好的职业机会',
          '增加薪资谈判筹码，预期薪资提升15-30%',
          '扩展职业发展路径，开启新的可能性',
          '建立专业声誉，成为领域内的专家',
          '提高工作效率，在现有岗位上表现更出色'
        ]

        return {
          skillName: skill.name,
          totalWeeks: baseWeeks,
          weeklyHours,
          phases,
          resources,
          milestones,
          careerImpact: careerImpacts[Math.floor(Math.random() * careerImpacts.length)]
        }
      })

      setLearningPaths(mockPaths)
      setAnalyzing(false)
    }, 2500)
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-400 bg-red-900/20 border-red-500/30'
      case 'medium': return 'text-yellow-400 bg-yellow-900/20 border-yellow-500/30'
      case 'low': return 'text-green-400 bg-green-900/20 border-green-500/30'
      default: return 'text-gray-400 bg-gray-900/20 border-gray-500/30'
    }
  }

  const getResourceIcon = (type: string) => {
    switch (type) {
      case 'course': return '🎓'
      case 'book': return '📚'
      case 'practice': return '💻'
      case 'project': return '🚀'
      default: return '📖'
    }
  }

  const totalLearningTime = learningPaths.reduce((total, path) => total + (path.totalWeeks * path.weeklyHours), 0)

  return (
    <div className="min-h-screen bg-gray-900">
      {/* 导航栏 */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-2xl">🎓</span>
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
          <div className="text-6xl mb-4">🎓</div>
          <h1 className="text-4xl font-bold text-white mb-4">学习伙伴AI</h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            个性化学习路径，持续技能提升，助你在职场中保持竞争优势
          </p>
        </div>

        {/* 统计面板 */}
        {learningPaths.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-6 text-center">
              <div className="text-3xl font-bold text-blue-400">{skills.length}</div>
              <div className="text-gray-300">学习目标</div>
            </div>
            <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-6 text-center">
              <div className="text-3xl font-bold text-green-400">{totalLearningTime}h</div>
              <div className="text-gray-300">总学习时间</div>
            </div>
            <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-6 text-center">
              <div className="text-3xl font-bold text-purple-400">{learningPaths.reduce((sum, p) => sum + p.resources.length, 0)}</div>
              <div className="text-gray-300">学习资源</div>
            </div>
            <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-6 text-center">
              <div className="text-3xl font-bold text-yellow-400">{Math.max(...learningPaths.map(p => p.totalWeeks))}</div>
              <div className="text-gray-300">最长周期(周)</div>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* 左侧：技能目标管理 */}
          <div className="space-y-6">
            <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">技能目标</h2>
                <button
                  onClick={() => setShowAddForm(!showAddForm)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  添加技能
                </button>
              </div>

              {/* 技能列表 */}
              <div className="space-y-4 mb-6">
                {skills.map((skill, index) => (
                  <div key={index} className="bg-gray-800 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-white">{skill.name}</h3>
                      <span className={`px-2 py-1 rounded text-xs border ${getPriorityColor(skill.priority)}`}>
                        {skill.priority === 'high' ? '高优先级' : skill.priority === 'medium' ? '中优先级' : '低优先级'}
                      </span>
                    </div>
                    <p className="text-blue-400 text-sm mb-3">{skill.category}</p>
                    
                    <div className="grid grid-cols-2 gap-4 mb-3">
                      <div>
                        <div className="flex items-center justify-between text-sm mb-1">
                          <span className="text-gray-300">当前水平</span>
                          <span className="text-white">{skill.currentLevel}/10</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full"
                            style={{ width: `${skill.currentLevel * 10}%` }}
                          ></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex items-center justify-between text-sm mb-1">
                          <span className="text-gray-300">目标水平</span>
                          <span className="text-white">{skill.targetLevel}/10</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div 
                            className="bg-green-500 h-2 rounded-full"
                            style={{ width: `${skill.targetLevel * 10}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>

                    <div className="text-sm">
                      <span className="text-yellow-400">市场需求：</span>
                      <span className="text-white">{skill.marketDemand}/10</span>
                      <span className="ml-4 text-purple-400">提升空间：</span>
                      <span className="text-white">{skill.targetLevel - skill.currentLevel} 级</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* 添加技能表单 */}
              {showAddForm && (
                <div className="bg-gray-800 rounded-lg p-4 space-y-4">
                  <input
                    type="text"
                    placeholder="技能名称（如：Python编程、数据分析）"
                    value={newSkill.name}
                    onChange={(e) => setNewSkill({...newSkill, name: e.target.value})}
                    className="w-full bg-gray-700 text-white rounded px-3 py-2"
                  />
                  
                  <select
                    value={newSkill.category}
                    onChange={(e) => setNewSkill({...newSkill, category: e.target.value})}
                    className="w-full bg-gray-700 text-white rounded px-3 py-2"
                  >
                    <option value="">选择技能分类</option>
                    {skillCategories.map(category => (
                      <option key={category} value={category}>{category}</option>
                    ))}
                  </select>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-gray-300 text-sm">当前水平: {newSkill.currentLevel}/10</label>
                      <input
                        type="range"
                        min="1"
                        max="10"
                        value={newSkill.currentLevel}
                        onChange={(e) => setNewSkill({...newSkill, currentLevel: Number(e.target.value)})}
                        className="w-full"
                      />
                    </div>
                    <div>
                      <label className="text-gray-300 text-sm">目标水平: {newSkill.targetLevel}/10</label>
                      <input
                        type="range"
                        min="1"
                        max="10"
                        value={newSkill.targetLevel}
                        onChange={(e) => setNewSkill({...newSkill, targetLevel: Number(e.target.value)})}
                        className="w-full"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-gray-300 text-sm">优先级</label>
                      <select
                        value={newSkill.priority}
                        onChange={(e) => setNewSkill({...newSkill, priority: e.target.value as 'high' | 'medium' | 'low'})}
                        className="w-full bg-gray-700 text-white rounded px-3 py-2"
                      >
                        <option value="low">低</option>
                        <option value="medium">中</option>
                        <option value="high">高</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-gray-300 text-sm">市场需求: {newSkill.marketDemand}/10</label>
                      <input
                        type="range"
                        min="1"
                        max="10"
                        value={newSkill.marketDemand}
                        onChange={(e) => setNewSkill({...newSkill, marketDemand: Number(e.target.value)})}
                        className="w-full"
                      />
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <button 
                      onClick={addSkill} 
                      className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      确认添加
                    </button>
                    <button 
                      onClick={() => setShowAddForm(false)}
                      className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      取消
                    </button>
                  </div>
                </div>
              )}

              {/* 生成学习路径按钮 */}
              {skills.length > 0 && (
                <button
                  onClick={generateLearningPaths}
                  disabled={analyzing}
                  className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white py-3 rounded-lg text-lg font-semibold transition-colors"
                >
                  {analyzing ? '🔄 AI规划中...' : '🎓 生成学习路径'}
                </button>
              )}
            </div>
          </div>

          {/* 右侧：学习路径 */}
          <div className="space-y-6">
            {learningPaths.length > 0 ? (
              <div className="space-y-6">
                {learningPaths.map((path, index) => (
                  <div key={index} className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
                    <div className="flex items-center mb-4">
                      <span className="text-2xl mr-3">🎯</span>
                      <div>
                        <h3 className="text-xl font-bold text-white">{path.skillName} 学习路径</h3>
                        <p className="text-gray-300 text-sm">{path.totalWeeks}周 · 每周{path.weeklyHours}小时</p>
                      </div>
                    </div>

                    {/* 学习阶段 */}
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-blue-400 mb-3">📚 学习阶段</h4>
                      <div className="space-y-3">
                        {path.phases.map((phase, phaseIndex) => (
                          <div key={phaseIndex} className="bg-gray-800 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <h5 className="font-semibold text-white">{phase.phase}</h5>
                              <span className="text-sm text-gray-400">{phase.weeks}周</span>
                            </div>
                            <p className="text-gray-300 text-sm mb-2">{phase.description}</p>
                            <div className="flex flex-wrap gap-1">
                              {phase.goals.map((goal, goalIndex) => (
                                <span key={goalIndex} className="bg-blue-900/30 text-blue-300 px-2 py-1 rounded text-xs">
                                  {goal}
                                </span>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* 学习资源 */}
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-green-400 mb-3">📖 推荐资源</h4>
                      <div className="grid grid-cols-1 gap-3">
                        {path.resources.map((resource, resourceIndex) => (
                          <div key={resourceIndex} className="bg-gray-800 rounded-lg p-3 flex items-center justify-between">
                            <div className="flex items-center">
                              <span className="text-xl mr-3">{getResourceIcon(resource.type)}</span>
                              <div>
                                <h6 className="font-semibold text-white text-sm">{resource.title}</h6>
                                <p className="text-gray-400 text-xs">{resource.provider} · {resource.duration}</p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <span className={`px-2 py-1 rounded text-xs ${
                                resource.difficulty === 'beginner' ? 'bg-green-900/30 text-green-400' :
                                resource.difficulty === 'intermediate' ? 'bg-yellow-900/30 text-yellow-400' :
                                'bg-red-900/30 text-red-400'
                              }`}>
                                {resource.difficulty === 'beginner' ? '初级' :
                                 resource.difficulty === 'intermediate' ? '中级' : '高级'}
                              </span>
                              <span className={`px-2 py-1 rounded text-xs ${
                                resource.cost === 'free' ? 'bg-green-900/30 text-green-400' : 'bg-blue-900/30 text-blue-400'
                              }`}>
                                {resource.cost === 'free' ? '免费' : '付费'}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* 里程碑 */}
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-yellow-400 mb-3">🏆 学习里程碑</h4>
                      <div className="space-y-3">
                        {path.milestones.map((milestone, milestoneIndex) => (
                          <div key={milestoneIndex} className="bg-gray-800 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <h6 className="font-semibold text-white">第{milestone.week}周: {milestone.title}</h6>
                            </div>
                            <p className="text-gray-300 text-sm mb-2">{milestone.description}</p>
                            <p className="text-yellow-400 text-xs">评估方式: {milestone.assessment}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* 职业影响 */}
                    <div className="bg-gradient-to-r from-purple-900/30 to-blue-900/30 border border-purple-500/30 rounded-lg p-4">
                      <h4 className="text-lg font-semibold text-purple-400 mb-2">💼 职业发展影响</h4>
                      <p className="text-gray-300 text-sm">{path.careerImpact}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6 text-center">
                <div className="text-6xl mb-4">🎓</div>
                <h3 className="text-xl font-semibold text-gray-400 mb-2">等待规划</h3>
                <p className="text-gray-500">添加技能目标后开始AI学习路径规划</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
