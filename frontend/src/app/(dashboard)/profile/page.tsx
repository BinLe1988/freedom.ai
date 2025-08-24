'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { 
  UserIcon, 
  PencilIcon,
  MapPinIcon,
  BriefcaseIcon,
  AcademicCapIcon,
  StarIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import { useAuth, withAuth } from '@/store/auth'
import Link from 'next/link'

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 }
}

function ProfilePage() {
  const { user } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [profile, setProfile] = useState({
    fullName: '张三',
    bio: '一个热爱自由的探索者，正在寻找人生的更多可能性。',
    location: '北京',
    currentRole: '软件工程师',
    experienceYears: 5,
    skills: ['JavaScript', 'Python', 'React', 'Node.js', 'AI/ML'],
    interests: ['编程', '旅行', '摄影', '读书', '创业']
  })

  const handleSave = () => {
    // TODO: 保存到后端
    setIsEditing(false)
  }

  const handleCancel = () => {
    // TODO: 恢复原始数据
    setIsEditing(false)
  }

  const addSkill = (skill: string) => {
    if (skill && !profile.skills.includes(skill)) {
      setProfile(prev => ({
        ...prev,
        skills: [...prev.skills, skill]
      }))
    }
  }

  const removeSkill = (skillToRemove: string) => {
    setProfile(prev => ({
      ...prev,
      skills: prev.skills.filter(skill => skill !== skillToRemove)
    }))
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* 导航栏 */}
      <nav className="starry-navbar">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/dashboard" className="text-gray-300 hover:text-starry-cyan transition-colors">
              ← 返回仪表板
            </Link>
            <h1 className="text-xl font-bold text-white">个人档案</h1>
            <div></div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        {/* 头部信息 */}
        <motion.div
          className="starry-card p-8 mb-8"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center space-x-6">
              <div className="w-24 h-24 bg-gradient-starry rounded-full flex items-center justify-center">
                <UserIcon className="w-12 h-12 text-white" />
              </div>
              <div>
                <h2 className="text-3xl font-bold text-white mb-2">
                  {profile.fullName}
                </h2>
                <p className="text-gray-300 text-lg mb-2">
                  @{user?.username}
                </p>
                <div className="flex items-center text-gray-400">
                  <MapPinIcon className="w-5 h-5 mr-2" />
                  {profile.location}
                </div>
              </div>
            </div>
            
            <button
              onClick={() => setIsEditing(!isEditing)}
              className={`starry-button ${isEditing ? 'opacity-50' : ''}`}
              disabled={isEditing}
            >
              <PencilIcon className="w-5 h-5 inline mr-2" />
              编辑档案
            </button>
          </div>
          
          <p className="text-gray-300 text-lg leading-relaxed">
            {profile.bio}
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* 基本信息 */}
          <motion.div
            className="starry-card p-6"
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
              <BriefcaseIcon className="w-6 h-6 mr-2 text-gradient" />
              职业信息
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-gray-400 text-sm mb-2">当前职位</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={profile.currentRole}
                    onChange={(e) => setProfile(prev => ({ ...prev, currentRole: e.target.value }))}
                    className="starry-input w-full"
                  />
                ) : (
                  <p className="text-white text-lg">{profile.currentRole}</p>
                )}
              </div>
              
              <div>
                <label className="block text-gray-400 text-sm mb-2">工作经验</label>
                {isEditing ? (
                  <input
                    type="number"
                    value={profile.experienceYears}
                    onChange={(e) => setProfile(prev => ({ ...prev, experienceYears: parseInt(e.target.value) }))}
                    className="starry-input w-full"
                  />
                ) : (
                  <p className="text-white text-lg">{profile.experienceYears} 年</p>
                )}
              </div>
              
              <div>
                <label className="block text-gray-400 text-sm mb-2">所在地区</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={profile.location}
                    onChange={(e) => setProfile(prev => ({ ...prev, location: e.target.value }))}
                    className="starry-input w-full"
                  />
                ) : (
                  <p className="text-white text-lg">{profile.location}</p>
                )}
              </div>
            </div>
          </motion.div>

          {/* 技能标签 */}
          <motion.div
            className="starry-card p-6"
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
              <AcademicCapIcon className="w-6 h-6 mr-2 text-gradient" />
              技能标签
            </h3>
            
            <div className="flex flex-wrap gap-2 mb-4">
              {profile.skills.map((skill, index) => (
                <motion.span
                  key={skill}
                  className="skill-tag relative group"
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                >
                  {skill}
                  {isEditing && (
                    <button
                      onClick={() => removeSkill(skill)}
                      className="ml-2 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <XMarkIcon className="w-4 h-4" />
                    </button>
                  )}
                </motion.span>
              ))}
            </div>
            
            {isEditing && (
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="添加新技能"
                  className="starry-input flex-1"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      addSkill(e.currentTarget.value)
                      e.currentTarget.value = ''
                    }
                  }}
                />
                <button
                  onClick={(e) => {
                    const input = e.currentTarget.previousElementSibling as HTMLInputElement
                    addSkill(input.value)
                    input.value = ''
                  }}
                  className="starry-button px-4"
                >
                  添加
                </button>
              </div>
            )}
          </motion.div>

          {/* 兴趣爱好 */}
          <motion.div
            className="starry-card p-6"
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
              <StarIcon className="w-6 h-6 mr-2 text-gradient" />
              兴趣爱好
            </h3>
            
            <div className="flex flex-wrap gap-2">
              {profile.interests.map((interest, index) => (
                <motion.span
                  key={interest}
                  className="px-4 py-2 bg-gray-800 text-gray-300 rounded-full text-sm border border-gray-600 hover:border-starry-purple transition-colors"
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                >
                  {interest}
                </motion.span>
              ))}
            </div>
          </motion.div>

          {/* 个人简介 */}
          <motion.div
            className="starry-card p-6"
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <h3 className="text-2xl font-bold text-white mb-6">个人简介</h3>
            
            {isEditing ? (
              <textarea
                value={profile.bio}
                onChange={(e) => setProfile(prev => ({ ...prev, bio: e.target.value }))}
                className="starry-input w-full h-32 resize-none"
                placeholder="介绍一下你自己..."
              />
            ) : (
              <p className="text-gray-300 leading-relaxed">
                {profile.bio}
              </p>
            )}
          </motion.div>
        </div>

        {/* 编辑模式的操作按钮 */}
        {isEditing && (
          <motion.div
            className="fixed bottom-8 right-8 flex space-x-4"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <button
              onClick={handleCancel}
              className="starry-button bg-gray-600 hover:bg-gray-700"
            >
              <XMarkIcon className="w-5 h-5 inline mr-2" />
              取消
            </button>
            <button
              onClick={handleSave}
              className="starry-button"
            >
              <CheckIcon className="w-5 h-5 inline mr-2" />
              保存
            </button>
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default withAuth(ProfilePage)
