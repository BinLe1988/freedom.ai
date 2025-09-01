'use client'

import { useState } from 'react'
import Link from 'next/link'

interface DecisionOption {
  name: string
  description: string
  riskLevel: number
  potentialReturn: number
  timeInvestment: number
  successProbability: number
}

export default function DecisionSupportPage() {
  const [options, setOptions] = useState<DecisionOption[]>([])
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [showAddForm, setShowAddForm] = useState(false)

  const [newOption, setNewOption] = useState<DecisionOption>({
    name: '',
    description: '',
    riskLevel: 5,
    potentialReturn: 0,
    timeInvestment: 0,
    successProbability: 0.5
  })

  const addOption = () => {
    if (newOption.name && newOption.description) {
      setOptions([...options, { ...newOption }])
      setNewOption({
        name: '',
        description: '',
        riskLevel: 5,
        potentialReturn: 0,
        timeInvestment: 0,
        successProbability: 0.5
      })
      setShowAddForm(false)
    }
  }

  const analyzeDecision = async () => {
    if (options.length < 2) {
      alert('请至少添加2个选项进行比较')
      return
    }

    setLoading(true)
    
    setTimeout(() => {
      const bestOption = options.reduce((best, current) => {
        const bestScore = (best.potentialReturn / best.timeInvestment) * best.successProbability * (1 - best.riskLevel/10)
        const currentScore = (current.potentialReturn / current.timeInvestment) * current.successProbability * (1 - current.riskLevel/10)
        return currentScore > bestScore ? current : best
      })

      const mockResult = {
        recommendedOption: bestOption.name,
        confidenceScore: 0.85,
        reasoning: `基于数据分析，推荐选择"${bestOption.name}"。该选项在收益潜力、成功概率和风险控制方面表现最佳。预期收益为${bestOption.potentialReturn.toLocaleString()}元，成功概率${(bestOption.successProbability*100).toFixed(0)}%，风险等级${bestOption.riskLevel}/10。`,
        riskAnalysis: `风险等级：${bestOption.riskLevel < 4 ? '低' : bestOption.riskLevel < 7 ? '中' : '高'} (${bestOption.riskLevel}/10)。建议制定详细执行计划并设置风险控制措施。`,
        actionPlan: [
          '第一阶段：准备和规划',
          '• 制定详细时间表',
          '• 设定阶段性目标',
          '第二阶段：执行和监控',
          '• 按计划开始执行',
          '• 定期评估进展'
        ],
        successMetrics: [
          `收益目标：${bestOption.potentialReturn.toLocaleString()}元`,
          `成功概率：达到${(bestOption.successProbability*100).toFixed(0)}%预期`,
          '风险控制：实际风险不超过预期'
        ]
      }

      setResult(mockResult)
      setLoading(false)
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* 导航栏 */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-2xl">🧠</span>
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
          <div className="text-6xl mb-4">🧠</div>
          <h1 className="text-4xl font-bold text-white mb-4">决策支持AI</h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            智能分析机会，提供数据驱动的决策建议，帮助你做出最优选择
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* 左侧：选项管理 */}
          <div className="space-y-6">
            <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">决策选项</h2>
                <button
                  onClick={() => setShowAddForm(!showAddForm)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  添加选项
                </button>
              </div>

              {/* 现有选项列表 */}
              <div className="space-y-4 mb-6">
                {options.map((option, index) => (
                  <div key={index} className="bg-gray-800 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-white mb-2">{option.name}</h3>
                    <p className="text-gray-300 text-sm mb-3">{option.description}</p>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-green-400">收益：</span>
                        <span className="text-white">{option.potentialReturn.toLocaleString()}元</span>
                      </div>
                      <div>
                        <span className="text-blue-400">时间：</span>
                        <span className="text-white">{option.timeInvestment}小时</span>
                      </div>
                      <div>
                        <span className="text-yellow-400">成功率：</span>
                        <span className="text-white">{(option.successProbability*100).toFixed(0)}%</span>
                      </div>
                      <div>
                        <span className="text-red-400">风险：</span>
                        <span className="text-white">{option.riskLevel}/10</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* 添加选项表单 */}
              {showAddForm && (
                <div className="bg-gray-800 rounded-lg p-4 space-y-4">
                  <input
                    type="text"
                    placeholder="选项名称"
                    value={newOption.name}
                    onChange={(e) => setNewOption({...newOption, name: e.target.value})}
                    className="w-full bg-gray-700 text-white rounded px-3 py-2"
                  />
                  <textarea
                    placeholder="选项描述"
                    value={newOption.description}
                    onChange={(e) => setNewOption({...newOption, description: e.target.value})}
                    className="w-full bg-gray-700 text-white rounded px-3 py-2 h-20"
                  />
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-gray-300 text-sm">潜在收益（元）</label>
                      <input
                        type="number"
                        value={newOption.potentialReturn}
                        onChange={(e) => setNewOption({...newOption, potentialReturn: Number(e.target.value)})}
                        className="w-full bg-gray-700 text-white rounded px-3 py-2"
                      />
                    </div>
                    <div>
                      <label className="text-gray-300 text-sm">时间投资（小时）</label>
                      <input
                        type="number"
                        value={newOption.timeInvestment}
                        onChange={(e) => setNewOption({...newOption, timeInvestment: Number(e.target.value)})}
                        className="w-full bg-gray-700 text-white rounded px-3 py-2"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-gray-300 text-sm">成功概率: {(newOption.successProbability*100).toFixed(0)}%</label>
                      <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.1"
                        value={newOption.successProbability}
                        onChange={(e) => setNewOption({...newOption, successProbability: Number(e.target.value)})}
                        className="w-full"
                      />
                    </div>
                    <div>
                      <label className="text-gray-300 text-sm">风险等级: {newOption.riskLevel}/10</label>
                      <input
                        type="range"
                        min="1"
                        max="10"
                        value={newOption.riskLevel}
                        onChange={(e) => setNewOption({...newOption, riskLevel: Number(e.target.value)})}
                        className="w-full"
                      />
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <button 
                      onClick={addOption} 
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

              {/* 分析按钮 */}
              {options.length >= 2 && (
                <button
                  onClick={analyzeDecision}
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white py-3 rounded-lg text-lg font-semibold transition-colors"
                >
                  {loading ? '🔄 AI分析中...' : '🧠 开始AI分析'}
                </button>
              )}
            </div>
          </div>

          {/* 右侧：分析结果 */}
          <div className="space-y-6">
            {result ? (
              <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
                <div className="flex items-center mb-6">
                  <span className="text-2xl mr-3">✅</span>
                  <div>
                    <h2 className="text-2xl font-bold text-white">AI分析结果</h2>
                    <p className="text-gray-300">置信度: {(result.confidenceScore*100).toFixed(0)}%</p>
                  </div>
                </div>

                <div className="space-y-6">
                  {/* 推荐选项 */}
                  <div>
                    <h3 className="text-lg font-semibold text-blue-400 mb-2">🎯 推荐选项</h3>
                    <div className="bg-green-900/30 border border-green-500/30 rounded-lg p-4">
                      <p className="text-white font-semibold text-xl">{result.recommendedOption}</p>
                    </div>
                  </div>

                  {/* 推理过程 */}
                  <div>
                    <h3 className="text-lg font-semibold text-blue-400 mb-2">💭 推理过程</h3>
                    <div className="bg-gray-800 rounded-lg p-4">
                      <p className="text-gray-300 whitespace-pre-line">{result.reasoning}</p>
                    </div>
                  </div>

                  {/* 风险分析 */}
                  <div>
                    <h3 className="text-lg font-semibold text-yellow-400 mb-2">⚠️ 风险分析</h3>
                    <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-4">
                      <p className="text-gray-300 whitespace-pre-line">{result.riskAnalysis}</p>
                    </div>
                  </div>

                  {/* 行动计划 */}
                  <div>
                    <h3 className="text-lg font-semibold text-blue-400 mb-2">📋 行动计划</h3>
                    <div className="bg-gray-800 rounded-lg p-4">
                      <ul className="text-gray-300 space-y-1">
                        {result.actionPlan.map((step: string, index: number) => (
                          <li key={index} className={step.startsWith('•') ? 'ml-4' : 'font-semibold mt-2'}>
                            {step}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* 成功指标 */}
                  <div>
                    <h3 className="text-lg font-semibold text-green-400 mb-2">📊 成功指标</h3>
                    <div className="bg-gray-800 rounded-lg p-4">
                      <ul className="text-gray-300 space-y-2">
                        {result.successMetrics.map((metric: string, index: number) => (
                          <li key={index} className="flex items-center">
                            <span className="text-green-400 mr-2">✓</span>
                            {metric}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6 text-center">
                <div className="text-6xl mb-4">📊</div>
                <h3 className="text-xl font-semibold text-gray-400 mb-2">等待分析</h3>
                <p className="text-gray-500">添加至少2个选项后开始AI分析</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
