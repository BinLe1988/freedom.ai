'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { 
  AcademicCapIcon, 
  BookOpenIcon,
  PlayIcon,
  CheckCircleIcon,
  ClockIcon,
  StarIcon,
  TrophyIcon,
  ChartBarIcon,
  PlusIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 }
}

const learningPaths = [
  {
    id: 1,
    title: '全栈开发进阶',
    description: '从前端到后端，掌握现代Web开发的完整技能栈',
    level: '中级',
    duration: '3个月',
    progress: 65,
    modules: 12,
    completedModules: 8,
    skills: ['React', 'Node.js', 'MongoDB', 'TypeScript'],
    nextLesson: 'GraphQL API设计'
  },
  {
    id: 2,
    title: 'AI/机器学习入门',
    description: '学习人工智能和机器学习的基础知识和实践应用',
    level: '初级',
    duration: '4个月',
    progress: 25,
    modules: 16,
    completedModules: 4,
    skills: ['Python', 'TensorFlow', '数据分析', '深度学习'],
    nextLesson: '神经网络基础'
  },
  {
    id: 3,
    title: '产品管理实战',
    description: '从0到1学习产品管理，掌握产品规划和团队协作',
    level: '中级',
    duration: '2个月',
    progress: 80,
    modules: 8,
    completedModules: 6,
    skills: ['产品设计', '用户研究', '数据分析', '团队管理'],
    nextLesson: '产品上线策略'
  }
]

const recommendedCourses = [
  {
    id: 1,
    title: '区块链开发实战',
    provider: 'TechEdu',
    rating: 4.8,
    students: 1200,
    duration: '6周',
    price: '¥299',
    image: '🔗',
    tags: ['区块链', 'Web3', 'Solidity']
  },
  {
    id: 2,
    title: '数字营销策略',
    provider: 'MarketPro',
    rating: 4.6,
    students: 800,
    duration: '4周',
    price: '¥199',
    image: '📱',
    tags: ['营销', 'SEO', '社交媒体']
  },
  {
    id: 3,
    title: '创业财务管理',
    provider: 'BizSchool',
    rating: 4.9,
    students: 600,
    duration: '8周',
    price: '¥399',
    image: '💰',
    tags: ['财务', '创业', '投资']
  }
]

function LearningPage() {
  const [activeTab, setActiveTab] = useState('paths')

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="starry-navbar">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="text-gray-300 hover:text-starry-cyan transition-colors">
              ← 返回首页
            </Link>
            <h1 className="text-xl font-bold text-white">学习规划</h1>
            <div></div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        {/* 学习统计 */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6 }}
        >
          <div className="starry-card p-6 text-center">
            <TrophyIcon className="w-12 h-12 text-gradient mx-auto mb-4" />
            <div className="text-2xl font-bold text-white mb-2">3</div>
            <div className="text-gray-400">学习路径</div>
          </div>
          
          <div className="starry-card p-6 text-center">
            <BookOpenIcon className="w-12 h-12 text-gradient mx-auto mb-4" />
            <div className="text-2xl font-bold text-white mb-2">18</div>
            <div className="text-gray-400">已完成课程</div>
          </div>
          
          <div className="starry-card p-6 text-center">
            <ClockIcon className="w-12 h-12 text-gradient mx-auto mb-4" />
            <div className="text-2xl font-bold text-white mb-2">120</div>
            <div className="text-gray-400">学习小时</div>
          </div>
          
          <div className="starry-card p-6 text-center">
            <StarIcon className="w-12 h-12 text-gradient mx-auto mb-4" />
            <div className="text-2xl font-bold text-white mb-2">15</div>
            <div className="text-gray-400">获得技能</div>
          </div>
        </motion.div>

        {/* 标签页导航 */}
        <motion.div
          className="starry-card p-2 mb-8"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab('paths')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === 'paths'
                  ? 'bg-gradient-starry text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              我的学习路径
            </button>
            <button
              onClick={() => setActiveTab('recommended')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === 'recommended'
                  ? 'bg-gradient-starry text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              推荐课程
            </button>
            <button
              onClick={() => setActiveTab('skills')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === 'skills'
                  ? 'bg-gradient-starry text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              技能地图
            </button>
          </div>
        </motion.div>

        {/* 我的学习路径 */}
        {activeTab === 'paths' && (
          <motion.div
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white">我的学习路径</h2>
              <button className="starry-button">
                <PlusIcon className="w-5 h-5 inline mr-2" />
                添加路径
              </button>
            </div>
            
            <div className="space-y-6">
              {learningPaths.map((path, index) => (
                <motion.div
                  key={path.id}
                  className="starry-card p-6"
                  initial="initial"
                  animate="animate"
                  variants={fadeInUp}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-white mb-2">
                        {path.title}
                      </h3>
                      <p className="text-gray-300 mb-4">
                        {path.description}
                      </p>
                      
                      <div className="flex items-center space-x-4 text-sm text-gray-400 mb-4">
                        <span className="flex items-center">
                          <ChartBarIcon className="w-4 h-4 mr-1" />
                          {path.level}
                        </span>
                        <span className="flex items-center">
                          <ClockIcon className="w-4 h-4 mr-1" />
                          {path.duration}
                        </span>
                        <span className="flex items-center">
                          <BookOpenIcon className="w-4 h-4 mr-1" />
                          {path.completedModules}/{path.modules} 模块
                        </span>
                      </div>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        {path.skills.map(skill => (
                          <span
                            key={skill}
                            className="px-3 py-1 bg-gray-800 text-gray-300 rounded-full text-sm"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    <div className="text-right ml-6">
                      <div className="text-3xl font-bold text-gradient mb-2">
                        {path.progress}%
                      </div>
                      <div className="starry-progress w-24 mb-4">
                        <div 
                          className="starry-progress-bar"
                          style={{ width: `${path.progress}%` }}
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <div className="text-gray-400">
                      下一课: {path.nextLesson}
                    </div>
                    <button className="starry-button">
                      <PlayIcon className="w-5 h-5 inline mr-2" />
                      继续学习
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* 推荐课程 */}
        {activeTab === 'recommended' && (
          <motion.div
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h2 className="text-2xl font-bold text-white mb-6">推荐课程</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendedCourses.map((course, index) => (
                <motion.div
                  key={course.id}
                  className="starry-card p-6 hover:scale-105 transition-transform"
                  initial="initial"
                  animate="animate"
                  variants={fadeInUp}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <div className="text-4xl mb-4 text-center">
                    {course.image}
                  </div>
                  
                  <h3 className="text-xl font-bold text-white mb-2">
                    {course.title}
                  </h3>
                  
                  <div className="text-gray-400 mb-4">
                    by {course.provider}
                  </div>
                  
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <StarIcon className="w-4 h-4 text-yellow-400 mr-1" />
                      <span className="text-white">{course.rating}</span>
                      <span className="text-gray-400 ml-2">
                        ({course.students})
                      </span>
                    </div>
                    <div className="text-gray-400">
                      {course.duration}
                    </div>
                  </div>
                  
                  <div className="flex flex-wrap gap-2 mb-4">
                    {course.tags.map(tag => (
                      <span
                        key={tag}
                        className="px-2 py-1 bg-gray-800 text-gray-300 rounded text-xs"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <div className="text-2xl font-bold text-gradient">
                      {course.price}
                    </div>
                    <button className="starry-button px-4 py-2">
                      立即学习
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* 技能地图 */}
        {activeTab === 'skills' && (
          <motion.div
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h2 className="text-2xl font-bold text-white mb-6">技能发展地图</h2>
            
            <div className="starry-card p-8">
              <div className="text-center mb-8">
                <AcademicCapIcon className="w-16 h-16 text-gradient mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-white mb-4">
                  个性化技能发展路径
                </h3>
                <p className="text-gray-300 text-lg">
                  基于你的目标和当前技能水平，我们为你规划了最优的学习路径
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-starry rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-white font-bold">1</span>
                  </div>
                  <h4 className="text-lg font-semibold text-white mb-2">
                    基础技能强化
                  </h4>
                  <p className="text-gray-400">
                    巩固现有技能，填补知识空白
                  </p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-starry-secondary rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-white font-bold">2</span>
                  </div>
                  <h4 className="text-lg font-semibold text-white mb-2">
                    进阶技能学习
                  </h4>
                  <p className="text-gray-400">
                    学习市场需求的新兴技术
                  </p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-starry-accent rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-white font-bold">3</span>
                  </div>
                  <h4 className="text-lg font-semibold text-white mb-2">
                    专业认证获取
                  </h4>
                  <p className="text-gray-400">
                    获得行业认可的专业证书
                  </p>
                </div>
              </div>
              
              <div className="text-center mt-8">
                <button className="starry-button mr-4">
                  开始技能评估
                </button>
                <button className="starry-button-secondary">
                  查看详细路径
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default LearningPage
