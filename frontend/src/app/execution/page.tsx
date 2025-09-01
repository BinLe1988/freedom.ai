'use client'

import { useState } from 'react'
import Link from 'next/link'

interface Task {
  id: string
  title: string
  description: string
  priority: 'high' | 'medium' | 'low'
  category: string
  estimatedTime: number
  status: 'pending' | 'in_progress' | 'completed' | 'automated'
  automationLevel: number // 0-100
  dependencies: string[]
}

interface AutomationSuggestion {
  taskId: string
  suggestion: string
  tools: string[]
  timesSaved: number
  difficulty: 'easy' | 'medium' | 'hard'
}

export default function ExecutionAssistantPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [suggestions, setSuggestions] = useState<AutomationSuggestion[]>([])
  const [showAddForm, setShowAddForm] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)

  const [newTask, setNewTask] = useState<Partial<Task>>({
    title: '',
    description: '',
    priority: 'medium',
    category: '',
    estimatedTime: 0,
    status: 'pending',
    automationLevel: 0,
    dependencies: []
  })

  const addTask = () => {
    if (newTask.title && newTask.description) {
      const task: Task = {
        id: Date.now().toString(),
        title: newTask.title!,
        description: newTask.description!,
        priority: newTask.priority!,
        category: newTask.category!,
        estimatedTime: newTask.estimatedTime!,
        status: 'pending',
        automationLevel: 0,
        dependencies: []
      }
      setTasks([...tasks, task])
      setNewTask({
        title: '',
        description: '',
        priority: 'medium',
        category: '',
        estimatedTime: 0,
        status: 'pending',
        automationLevel: 0,
        dependencies: []
      })
      setShowAddForm(false)
    }
  }

  const analyzeAutomation = () => {
    if (tasks.length === 0) {
      alert('请先添加一些任务')
      return
    }

    setAnalyzing(true)
    
    setTimeout(() => {
      const mockSuggestions: AutomationSuggestion[] = tasks.map(task => {
        const automationSuggestions = [
          {
            suggestion: '使用脚本自动化重复性操作',
            tools: ['Python脚本', '批处理文件', 'Shell脚本'],
            timesSaved: Math.floor(task.estimatedTime * 0.7),
            difficulty: 'medium' as const
          },
          {
            suggestion: '设置自动化工作流程',
            tools: ['Zapier', 'IFTTT', 'Microsoft Power Automate'],
            timesSaved: Math.floor(task.estimatedTime * 0.8),
            difficulty: 'easy' as const
          },
          {
            suggestion: '使用AI工具辅助完成',
            tools: ['ChatGPT', 'Claude', '专业AI工具'],
            timesSaved: Math.floor(task.estimatedTime * 0.6),
            difficulty: 'easy' as const
          }
        ]

        const randomSuggestion = automationSuggestions[Math.floor(Math.random() * automationSuggestions.length)]
        
        return {
          taskId: task.id,
          ...randomSuggestion
        }
      })

      setSuggestions(mockSuggestions)
      setAnalyzing(false)
    }, 2000)
  }

  const implementAutomation = (taskId: string) => {
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, status: 'automated', automationLevel: 80 }
        : task
    ))
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-400 bg-red-900/20 border-red-500/30'
      case 'medium': return 'text-yellow-400 bg-yellow-900/20 border-yellow-500/30'
      case 'low': return 'text-green-400 bg-green-900/20 border-green-500/30'
      default: return 'text-gray-400 bg-gray-900/20 border-gray-500/30'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-400'
      case 'automated': return 'text-blue-400'
      case 'in_progress': return 'text-yellow-400'
      default: return 'text-gray-400'
    }
  }

  const totalTimeSaved = suggestions.reduce((total, suggestion) => total + suggestion.timesSaved, 0)

  return (
    <div className="min-h-screen bg-gray-900">
      {/* 导航栏 */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-2xl">⚙️</span>
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
          <div className="text-6xl mb-4">⚙️</div>
          <h1 className="text-4xl font-bold text-white mb-4">执行助手AI</h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            自动化任务执行，提高工作效率，让你专注于最重要的事情
          </p>
        </div>

        {/* 统计面板 */}
        {suggestions.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-6 text-center">
              <div className="text-3xl font-bold text-blue-400">{tasks.length}</div>
              <div className="text-gray-300">总任务数</div>
            </div>
            <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-6 text-center">
              <div className="text-3xl font-bold text-green-400">{totalTimeSaved}h</div>
              <div className="text-gray-300">预计节省时间</div>
            </div>
            <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-6 text-center">
              <div className="text-3xl font-bold text-purple-400">{tasks.filter(t => t.status === 'automated').length}</div>
              <div className="text-gray-300">已自动化任务</div>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* 左侧：任务管理 */}
          <div className="space-y-6">
            <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">任务列表</h2>
                <button
                  onClick={() => setShowAddForm(!showAddForm)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  添加任务
                </button>
              </div>

              {/* 任务列表 */}
              <div className="space-y-4 mb-6">
                {tasks.map((task) => (
                  <div key={task.id} className="bg-gray-800 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-white">{task.title}</h3>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs border ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </span>
                        <span className={`text-sm ${getStatusColor(task.status)}`}>
                          {task.status === 'automated' ? '🤖 已自动化' : 
                           task.status === 'completed' ? '✅ 已完成' :
                           task.status === 'in_progress' ? '🔄 进行中' : '⏳ 待处理'}
                        </span>
                      </div>
                    </div>
                    <p className="text-gray-300 text-sm mb-3">{task.description}</p>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-blue-400">分类：</span>
                        <span className="text-white">{task.category || '未分类'}</span>
                      </div>
                      <div>
                        <span className="text-yellow-400">预计时间：</span>
                        <span className="text-white">{task.estimatedTime}小时</span>
                      </div>
                    </div>
                    {task.automationLevel > 0 && (
                      <div className="mt-3">
                        <div className="flex items-center justify-between text-sm mb-1">
                          <span className="text-purple-400">自动化程度</span>
                          <span className="text-white">{task.automationLevel}%</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div 
                            className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${task.automationLevel}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* 添加任务表单 */}
              {showAddForm && (
                <div className="bg-gray-800 rounded-lg p-4 space-y-4">
                  <input
                    type="text"
                    placeholder="任务标题"
                    value={newTask.title}
                    onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                    className="w-full bg-gray-700 text-white rounded px-3 py-2"
                  />
                  <textarea
                    placeholder="任务描述"
                    value={newTask.description}
                    onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                    className="w-full bg-gray-700 text-white rounded px-3 py-2 h-20"
                  />
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-gray-300 text-sm">分类</label>
                      <input
                        type="text"
                        placeholder="如：数据处理、文档整理"
                        value={newTask.category}
                        onChange={(e) => setNewTask({...newTask, category: e.target.value})}
                        className="w-full bg-gray-700 text-white rounded px-3 py-2"
                      />
                    </div>
                    <div>
                      <label className="text-gray-300 text-sm">预计时间（小时）</label>
                      <input
                        type="number"
                        value={newTask.estimatedTime}
                        onChange={(e) => setNewTask({...newTask, estimatedTime: Number(e.target.value)})}
                        className="w-full bg-gray-700 text-white rounded px-3 py-2"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-gray-300 text-sm">优先级</label>
                    <select
                      value={newTask.priority}
                      onChange={(e) => setNewTask({...newTask, priority: e.target.value as 'high' | 'medium' | 'low'})}
                      className="w-full bg-gray-700 text-white rounded px-3 py-2"
                    >
                      <option value="low">低</option>
                      <option value="medium">中</option>
                      <option value="high">高</option>
                    </select>
                  </div>

                  <div className="flex gap-4">
                    <button 
                      onClick={addTask} 
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
              {tasks.length > 0 && (
                <button
                  onClick={analyzeAutomation}
                  disabled={analyzing}
                  className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white py-3 rounded-lg text-lg font-semibold transition-colors"
                >
                  {analyzing ? '🔄 AI分析中...' : '🤖 分析自动化机会'}
                </button>
              )}
            </div>
          </div>

          {/* 右侧：自动化建议 */}
          <div className="space-y-6">
            {suggestions.length > 0 ? (
              <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6">
                <div className="flex items-center mb-6">
                  <span className="text-2xl mr-3">🤖</span>
                  <div>
                    <h2 className="text-2xl font-bold text-white">自动化建议</h2>
                    <p className="text-gray-300">AI为你找到了 {suggestions.length} 个自动化机会</p>
                  </div>
                </div>

                <div className="space-y-4">
                  {suggestions.map((suggestion, index) => {
                    const task = tasks.find(t => t.id === suggestion.taskId)
                    if (!task) return null

                    return (
                      <div key={index} className="bg-gray-800 rounded-lg p-4">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h3 className="text-lg font-semibold text-white mb-1">{task.title}</h3>
                            <p className="text-blue-400 text-sm">{suggestion.suggestion}</p>
                          </div>
                          <span className={`px-2 py-1 rounded text-xs ${
                            suggestion.difficulty === 'easy' ? 'bg-green-900/30 text-green-400' :
                            suggestion.difficulty === 'medium' ? 'bg-yellow-900/30 text-yellow-400' :
                            'bg-red-900/30 text-red-400'
                          }`}>
                            {suggestion.difficulty === 'easy' ? '简单' :
                             suggestion.difficulty === 'medium' ? '中等' : '困难'}
                          </span>
                        </div>

                        <div className="mb-4">
                          <p className="text-gray-300 text-sm mb-2">推荐工具：</p>
                          <div className="flex flex-wrap gap-2">
                            {suggestion.tools.map((tool, toolIndex) => (
                              <span key={toolIndex} className="bg-blue-900/30 text-blue-300 px-2 py-1 rounded text-xs">
                                {tool}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div className="flex items-center justify-between">
                          <div className="text-sm">
                            <span className="text-green-400">预计节省：</span>
                            <span className="text-white font-semibold">{suggestion.timesSaved}小时</span>
                          </div>
                          <button
                            onClick={() => implementAutomation(suggestion.taskId)}
                            disabled={task.status === 'automated'}
                            className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-colors"
                          >
                            {task.status === 'automated' ? '✅ 已实施' : '🚀 实施自动化'}
                          </button>
                        </div>
                      </div>
                    )
                  })}
                </div>

                {/* 总结 */}
                <div className="mt-6 bg-gradient-to-r from-purple-900/30 to-blue-900/30 border border-purple-500/30 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-white mb-2">💡 自动化收益总结</h3>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-300">总节省时间：</span>
                      <span className="text-green-400 font-semibold">{totalTimeSaved}小时</span>
                    </div>
                    <div>
                      <span className="text-gray-300">效率提升：</span>
                      <span className="text-blue-400 font-semibold">{Math.round((totalTimeSaved / tasks.reduce((sum, t) => sum + t.estimatedTime, 1)) * 100)}%</span>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-gray-700 p-6 text-center">
                <div className="text-6xl mb-4">🤖</div>
                <h3 className="text-xl font-semibold text-gray-400 mb-2">等待分析</h3>
                <p className="text-gray-500">添加任务后开始AI自动化分析</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
