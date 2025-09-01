'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { 
  RocketLaunchIcon, 
  HomeIcon, 
  ArrowLeftIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 }
}

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <motion.div
        className="text-center max-w-2xl mx-auto"
        initial="initial"
        animate="animate"
        variants={fadeInUp}
        transition={{ duration: 0.6 }}
      >
        {/* 404动画 */}
        <motion.div
          className="mb-8"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
        >
          <div className="relative">
            <div className="text-9xl font-bold text-gradient opacity-20">
              404
            </div>
            <div className="absolute inset-0 flex items-center justify-center">
              <ExclamationTriangleIcon className="w-24 h-24 text-starry-purple animate-pulse" />
            </div>
          </div>
        </motion.div>

        {/* 错误信息 */}
        <motion.div
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            页面未找到
          </h1>
          <p className="text-xl text-gray-300 mb-8 leading-relaxed">
            抱歉，你访问的页面不存在或正在开发中。<br />
            让我们帮你回到正确的轨道上！
          </p>
        </motion.div>

        {/* 导航按钮 */}
        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center"
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <Link href="/" className="starry-button text-lg px-8 py-4">
            <HomeIcon className="w-6 h-6 inline mr-2" />
            返回首页
          </Link>
          <Link href="/" className="starry-button-secondary text-lg px-8 py-4">
            <RocketLaunchIcon className="w-6 h-6 inline mr-2" />
            前往仪表板
          </Link>
        </motion.div>

        {/* 快速链接 */}
        <motion.div
          className="mt-12 p-6 starry-card"
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <h3 className="text-xl font-bold text-white mb-4">
            你可能在寻找：
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Link 
              href="/" 
              className="text-gray-300 hover:text-starry-cyan transition-colors p-2 rounded-lg hover:bg-gray-800"
            >
              📊 仪表板
            </Link>
            <Link 
              href="/profile" 
              className="text-gray-300 hover:text-starry-cyan transition-colors p-2 rounded-lg hover:bg-gray-800"
            >
              👤 个人档案
            </Link>
            <Link 
              href="/assessment" 
              className="text-gray-300 hover:text-starry-cyan transition-colors p-2 rounded-lg hover:bg-gray-800"
            >
              📈 自由度评估
            </Link>
            <Link 
              href="/opportunities" 
              className="text-gray-300 hover:text-starry-cyan transition-colors p-2 rounded-lg hover:bg-gray-800"
            >
              💼 机会探索
            </Link>
            <Link 
              href="/learning" 
              className="text-gray-300 hover:text-starry-cyan transition-colors p-2 rounded-lg hover:bg-gray-800"
            >
              🎓 学习规划
            </Link>
            <Link 
              href="/login" 
              className="text-gray-300 hover:text-starry-cyan transition-colors p-2 rounded-lg hover:bg-gray-800"
            >
              🔐 登录
            </Link>
            <Link 
              href="/register" 
              className="text-gray-300 hover:text-starry-cyan transition-colors p-2 rounded-lg hover:bg-gray-800"
            >
              📝 注册
            </Link>
            <Link 
              href="/" 
              className="text-gray-300 hover:text-starry-cyan transition-colors p-2 rounded-lg hover:bg-gray-800"
            >
              🏠 首页
            </Link>
          </div>
        </motion.div>

        {/* 返回按钮 */}
        <motion.div
          className="mt-8"
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <button 
            onClick={() => window.history.back()}
            className="text-gray-400 hover:text-starry-cyan transition-colors flex items-center mx-auto"
          >
            <ArrowLeftIcon className="w-5 h-5 mr-2" />
            返回上一页
          </button>
        </motion.div>
      </motion.div>
    </div>
  )
}
