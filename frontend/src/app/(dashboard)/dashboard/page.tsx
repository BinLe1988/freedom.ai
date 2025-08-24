'use client'

import { motion } from 'framer-motion'
import { 
  ChartBarIcon, 
  UserIcon, 
  CogIcon, 
  RocketLaunchIcon,
  StarIcon,
  TrophyIcon,
  ClockIcon,
  GlobeAltIcon,
  AcademicCapIcon,
  BriefcaseIcon
} from '@heroicons/react/24/outline'
import { useAuth, withAuth } from '@/store/auth'
import { StatCard } from '@/components/ui/StatCard'
import { FeatureCard } from '@/components/ui/FeatureCard'
import Link from 'next/link'

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 }
}

const staggerChildren = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
}

function DashboardPage() {
  const { user } = useAuth()

  return (
    <div className="min-h-screen bg-gray-900">
      {/* 导航栏 */}
      <nav className="starry-navbar">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <RocketLaunchIcon className="w-8 h-8 text-starry-cyan" />
              <span className="text-2xl font-bold text-gradient">Freedom.AI</span>
            </Link>
            
            <div className="flex items-center space-x-6">
              <Link href="/profile" className="text-gray-300 hover:text-starry-cyan transition-colors">
                <UserIcon className="w-6 h-6" />
              </Link>
              <Link href="/assessment" className="text-gray-300 hover:text-starry-cyan transition-colors">
                <ChartBarIcon className="w-6 h-6" />
              </Link>
              <Link href="/opportunities" className="text-gray-300 hover:text-starry-cyan transition-colors">
                <BriefcaseIcon className="w-6 h-6" />
              </Link>
              <Link href="/learning" className="text-gray-300 hover:text-starry-cyan transition-colors">
                <AcademicCapIcon className="w-6 h-6" />
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        {/* 欢迎区域 */}
        <motion.div
          className="mb-12"
          initial="initial"
          animate="animate"
          variants={staggerChildren}
        >
          <motion.div
            className="text-center mb-8"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-6xl font-bold text-gradient mb-4">
              欢迎回来，{user?.username || '探索者'}！
            </h1>
            <p className="text-xl text-gray-300">
              继续你的自由探索之旅，发现更多可能性
            </p>
          </motion.div>
        </motion.div>

        {/* 自由度概览 */}
        <motion.section
          className="mb-12"
          initial="initial"
          animate="animate"
          variants={staggerChildren}
        >
          <motion.h2
            className="text-3xl font-bold text-white mb-8 text-center"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            你的自由度概览
          </motion.h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.1 }}>
              <StatCard number="75%" label="财务自由度" delay={0} />
            </motion.div>
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.2 }}>
              <StatCard number="60%" label="时间自由度" delay={0.1} />
            </motion.div>
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.3 }}>
              <StatCard number="85%" label="地理自由度" delay={0.2} />
            </motion.div>
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.4 }}>
              <StatCard number="70%" label="技能自由度" delay={0.3} />
            </motion.div>
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.5 }}>
              <StatCard number="65%" label="关系自由度" delay={0.4} />
            </motion.div>
          </div>
        </motion.section>

        {/* 综合自由度分数 */}
        <motion.section
          className="mb-12"
          initial="initial"
          animate="animate"
          variants={staggerChildren}
        >
          <motion.div
            className="starry-card p-8 text-center"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            <div className="flex items-center justify-center mb-6">
              <TrophyIcon className="w-16 h-16 text-gradient" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-4">综合自由度分数</h3>
            <div className="text-6xl font-bold text-gradient mb-4 freedom-score">
              71
            </div>
            <p className="text-gray-300 text-lg">
              你已经在自由的道路上取得了不错的进展！
            </p>
            <div className="mt-6">
              <Link href="/assessment" className="starry-button">
                <ChartBarIcon className="w-5 h-5 inline mr-2" />
                重新评估
              </Link>
            </div>
          </motion.div>
        </motion.section>

        {/* 快速操作 */}
        <motion.section
          className="mb-12"
          initial="initial"
          animate="animate"
          variants={staggerChildren}
        >
          <motion.h2
            className="text-3xl font-bold text-white mb-8 text-center"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            快速操作
          </motion.h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.1 }}>
              <Link href="/assessment">
                <FeatureCard
                  icon={<ChartBarIcon className="w-12 h-12" />}
                  title="自由度评估"
                  description="全面评估你的五维自由度，发现提升空间"
                  delay={0}
                />
              </Link>
            </motion.div>
            
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.2 }}>
              <Link href="/opportunities">
                <FeatureCard
                  icon={<BriefcaseIcon className="w-12 h-12" />}
                  title="机会探索"
                  description="发现适合你的工作机会和创业项目"
                  delay={0.1}
                />
              </Link>
            </motion.div>
            
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.3 }}>
              <Link href="/learning">
                <FeatureCard
                  icon={<AcademicCapIcon className="w-12 h-12" />}
                  title="学习规划"
                  description="制定个性化的技能提升和学习计划"
                  delay={0.2}
                />
              </Link>
            </motion.div>
            
            <motion.div variants={fadeInUp} transition={{ duration: 0.6, delay: 0.4 }}>
              <Link href="/profile">
                <FeatureCard
                  icon={<UserIcon className="w-12 h-12" />}
                  title="个人档案"
                  description="完善你的个人信息和技能档案"
                  delay={0.3}
                />
              </Link>
            </motion.div>
          </div>
        </motion.section>

        {/* 最近活动 */}
        <motion.section
          className="mb-12"
          initial="initial"
          animate="animate"
          variants={staggerChildren}
        >
          <motion.h2
            className="text-3xl font-bold text-white mb-8 text-center"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            最近活动
          </motion.h2>
          
          <motion.div
            className="starry-card p-6"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            <div className="space-y-4">
              <div className="flex items-center space-x-4 p-4 bg-gray-800/50 rounded-lg">
                <div className="w-10 h-10 bg-gradient-starry rounded-full flex items-center justify-center">
                  <StarIcon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h4 className="text-white font-semibold">完成了自由度评估</h4>
                  <p className="text-gray-400 text-sm">获得了71分的综合自由度分数</p>
                </div>
                <div className="text-gray-400 text-sm">
                  2小时前
                </div>
              </div>
              
              <div className="flex items-center space-x-4 p-4 bg-gray-800/50 rounded-lg">
                <div className="w-10 h-10 bg-gradient-starry-secondary rounded-full flex items-center justify-center">
                  <UserIcon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h4 className="text-white font-semibold">更新了个人档案</h4>
                  <p className="text-gray-400 text-sm">添加了新的技能和经验信息</p>
                </div>
                <div className="text-gray-400 text-sm">
                  1天前
                </div>
              </div>
              
              <div className="flex items-center space-x-4 p-4 bg-gray-800/50 rounded-lg">
                <div className="w-10 h-10 bg-gradient-starry-accent rounded-full flex items-center justify-center">
                  <RocketLaunchIcon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h4 className="text-white font-semibold">加入了Freedom.AI</h4>
                  <p className="text-gray-400 text-sm">开始了自由探索之旅</p>
                </div>
                <div className="text-gray-400 text-sm">
                  3天前
                </div>
              </div>
            </div>
          </motion.div>
        </motion.section>

        {/* 推荐行动 */}
        <motion.section
          initial="initial"
          animate="animate"
          variants={staggerChildren}
        >
          <motion.h2
            className="text-3xl font-bold text-white mb-8 text-center"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            推荐行动
          </motion.h2>
          
          <motion.div
            className="starry-card p-8 text-center"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            <div className="mb-6">
              <ClockIcon className="w-16 h-16 text-gradient mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-white mb-4">提升时间自由度</h3>
              <p className="text-gray-300 text-lg mb-6">
                你的时间自由度相对较低，建议探索远程工作机会或提升工作效率
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/opportunities" className="starry-button">
                <BriefcaseIcon className="w-5 h-5 inline mr-2" />
                探索远程工作
              </Link>
              <Link href="/learning" className="starry-button-secondary">
                <AcademicCapIcon className="w-5 h-5 inline mr-2" />
                学习时间管理
              </Link>
            </div>
          </motion.div>
        </motion.section>
      </div>
    </div>
  )
}

export default withAuth(DashboardPage)
