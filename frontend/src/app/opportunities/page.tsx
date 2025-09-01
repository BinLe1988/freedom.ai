'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { 
  BriefcaseIcon, 
  MapPinIcon,
  CurrencyDollarIcon,
  ClockIcon,
  StarIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  GlobeAltIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 }
}

const opportunities = [
  {
    id: 1,
    title: '高级前端工程师',
    company: 'TechCorp',
    location: '远程',
    salary: '25-35K',
    type: '全职',
    tags: ['React', 'TypeScript', '远程工作'],
    description: '负责开发现代化的Web应用，使用最新的前端技术栈。',
    match: 95,
    posted: '2天前'
  },
  {
    id: 2,
    title: 'AI产品经理',
    company: 'AI Startup',
    location: '北京/远程',
    salary: '30-50K',
    type: '全职',
    tags: ['AI', '产品管理', '创业公司'],
    description: '领导AI产品的规划和开发，与技术团队紧密合作。',
    match: 88,
    posted: '1天前'
  },
  {
    id: 3,
    title: '自由职业开发者',
    company: '多个客户',
    location: '全球远程',
    salary: '500-1000/天',
    type: '自由职业',
    tags: ['自由职业', '全栈开发', '灵活时间'],
    description: '为多个客户提供定制化的软件开发服务。',
    match: 92,
    posted: '3天前'
  },
  {
    id: 4,
    title: '技术博主/内容创作者',
    company: '自媒体',
    location: '任意地点',
    salary: '被动收入',
    type: '创业',
    tags: ['内容创作', '技术分享', '被动收入'],
    description: '通过技术博客、视频课程等方式分享知识并获得收入。',
    match: 85,
    posted: '5天前'
  },
  {
    id: 5,
    title: 'SaaS产品创始人',
    company: '自主创业',
    location: '任意地点',
    salary: '股权收益',
    type: '创业',
    tags: ['SaaS', '创业', '产品开发'],
    description: '开发和运营自己的SaaS产品，实现财务自由。',
    match: 78,
    posted: '1周前'
  },
  {
    id: 6,
    title: '远程技术顾问',
    company: '咨询公司',
    location: '全球远程',
    salary: '1000-2000/天',
    type: '咨询',
    tags: ['技术咨询', '高薪', '灵活时间'],
    description: '为企业提供技术架构和数字化转型咨询服务。',
    match: 90,
    posted: '4天前'
  }
]

function OpportunitiesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedType, setSelectedType] = useState('all')
  const [selectedLocation, setSelectedLocation] = useState('all')

  const filteredOpportunities = opportunities.filter(opp => {
    const matchesSearch = opp.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         opp.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         opp.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
    
    const matchesType = selectedType === 'all' || opp.type === selectedType
    const matchesLocation = selectedLocation === 'all' || 
                           opp.location.toLowerCase().includes(selectedLocation.toLowerCase())
    
    return matchesSearch && matchesType && matchesLocation
  })

  const getMatchColor = (match: number) => {
    if (match >= 90) return 'text-green-400'
    if (match >= 80) return 'text-yellow-400'
    return 'text-orange-400'
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="starry-navbar">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="text-gray-300 hover:text-starry-cyan transition-colors">
              ← 返回首页
            </Link>
            <h1 className="text-xl font-bold text-white">机会探索</h1>
            <div></div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        {/* 搜索和筛选 */}
        <motion.div
          className="starry-card p-6 mb-8"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6 }}
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <div className="relative">
                <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="搜索职位、公司或技能..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="starry-input pl-10 w-full"
                />
              </div>
            </div>
            
            <div>
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="starry-input w-full"
              >
                <option value="all">所有类型</option>
                <option value="全职">全职</option>
                <option value="自由职业">自由职业</option>
                <option value="创业">创业</option>
                <option value="咨询">咨询</option>
              </select>
            </div>
            
            <div>
              <select
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                className="starry-input w-full"
              >
                <option value="all">所有地点</option>
                <option value="远程">远程</option>
                <option value="北京">北京</option>
                <option value="上海">上海</option>
                <option value="深圳">深圳</option>
              </select>
            </div>
          </div>
        </motion.div>

        {/* 推荐机会 */}
        <motion.div
          className="mb-8"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <StarIcon className="w-6 h-6 mr-2 text-gradient" />
            为你推荐 ({filteredOpportunities.length})
          </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {filteredOpportunities.map((opportunity, index) => (
              <motion.div
                key={opportunity.id}
                className="starry-card p-6 hover:scale-105 transition-transform cursor-pointer"
                initial="initial"
                animate="animate"
                variants={fadeInUp}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-2">
                      {opportunity.title}
                    </h3>
                    <div className="flex items-center text-gray-300 mb-2">
                      <BuildingOfficeIcon className="w-4 h-4 mr-2" />
                      {opportunity.company}
                    </div>
                    <div className="flex items-center text-gray-400 text-sm">
                      <MapPinIcon className="w-4 h-4 mr-1" />
                      {opportunity.location}
                      <span className="mx-2">•</span>
                      <CurrencyDollarIcon className="w-4 h-4 mr-1" />
                      {opportunity.salary}
                      <span className="mx-2">•</span>
                      <ClockIcon className="w-4 h-4 mr-1" />
                      {opportunity.type}
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className={`text-2xl font-bold ${getMatchColor(opportunity.match)}`}>
                      {opportunity.match}%
                    </div>
                    <div className="text-gray-400 text-sm">匹配度</div>
                  </div>
                </div>
                
                <p className="text-gray-300 mb-4 leading-relaxed">
                  {opportunity.description}
                </p>
                
                <div className="flex flex-wrap gap-2 mb-4">
                  {opportunity.tags.map(tag => (
                    <span
                      key={tag}
                      className="px-3 py-1 bg-gray-800 text-gray-300 rounded-full text-sm border border-gray-600"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">
                    发布于 {opportunity.posted}
                  </span>
                  <button className="starry-button px-4 py-2 text-sm">
                    查看详情
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* 机会类型统计 */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-4 gap-6"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <div className="starry-card p-6 text-center">
            <BriefcaseIcon className="w-12 h-12 text-gradient mx-auto mb-4" />
            <div className="text-2xl font-bold text-white mb-2">12</div>
            <div className="text-gray-400">全职机会</div>
          </div>
          
          <div className="starry-card p-6 text-center">
            <GlobeAltIcon className="w-12 h-12 text-gradient mx-auto mb-4" />
            <div className="text-2xl font-bold text-white mb-2">8</div>
            <div className="text-gray-400">远程工作</div>
          </div>
          
          <div className="starry-card p-6 text-center">
            <StarIcon className="w-12 h-12 text-gradient mx-auto mb-4" />
            <div className="text-2xl font-bold text-white mb-2">5</div>
            <div className="text-gray-400">创业项目</div>
          </div>
          
          <div className="starry-card p-6 text-center">
            <CurrencyDollarIcon className="w-12 h-12 text-gradient mx-auto mb-4" />
            <div className="text-2xl font-bold text-white mb-2">15</div>
            <div className="text-gray-400">高薪职位</div>
          </div>
        </motion.div>

        {/* 行动建议 */}
        <motion.div
          className="starry-card p-8 mt-8 text-center"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <h3 className="text-2xl font-bold text-white mb-4">
            提升机会匹配度
          </h3>
          <p className="text-gray-300 mb-6">
            完善你的技能档案和偏好设置，获得更精准的机会推荐
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/profile" className="starry-button">
              完善档案
            </Link>
            <Link href="/learning" className="starry-button-secondary">
              技能提升
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default OpportunitiesPage
