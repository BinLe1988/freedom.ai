'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { 
  RocketLaunchIcon, 
  CpuChipIcon, 
  CogIcon, 
  AcademicCapIcon, 
  MagnifyingGlassIcon,
  StarIcon,
  ChartBarIcon,
  ClockIcon,
  GlobeAltIcon,
  WrenchScrewdriverIcon,
  UsersIcon
} from '@heroicons/react/24/outline'
import { Navbar } from '@/components/layout/Navbar'
import { StatCard } from '@/components/ui/StatCard'
import { FeatureCard } from '@/components/ui/FeatureCard'
import { FloatingElements } from '@/components/effects/FloatingElements'

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

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* 英雄区域 */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <FloatingElements />
        
        <div className="container mx-auto px-4 relative z-10">
          <motion.div 
            className="text-center max-w-4xl mx-auto"
            initial="initial"
            animate="animate"
            variants={staggerChildren}
          >
            <motion.h1 
              className="text-6xl md:text-8xl font-bold mb-8 text-gradient"
              variants={fadeInUp}
              transition={{ duration: 0.6 }}
            >
              Freedom.AI
            </motion.h1>
            
            <motion.p 
              className="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              让AI成为你探索自由人生的得力助手<br />
              在寻找自由的路上，发现无限可能性
            </motion.p>
            
            <motion.div 
              className="flex flex-col sm:flex-row gap-6 justify-center"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              <Link href="/assessment" className="starry-button glow-effect text-lg px-8 py-4">
                <RocketLaunchIcon className="w-6 h-6 inline mr-2" />
                开始评估
              </Link>
              <Link href="/opportunities" className="starry-button-secondary text-lg px-8 py-4">
                <StarIcon className="w-6 h-6 inline mr-2" />
                探索机会
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* 功能特色 */}
      <section id="features" className="py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-16"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerChildren}
          >
            <motion.h2 
              className="text-4xl md:text-5xl font-bold text-white mb-6"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              四大AI智能体
            </motion.h2>
            <motion.p 
              className="text-xl text-gray-300 max-w-3xl mx-auto"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              通过AI驱动的智能分析，为你提供个性化的自由度评估和发展建议
            </motion.p>
          </motion.div>
          
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerChildren}
          >
            <FeatureCard
              icon={<CpuChipIcon className="w-12 h-12" />}
              title="决策支持AI"
              description="智能分析机会，提供数据驱动的决策建议，帮助你做出最优选择"
              href="/decision"
              delay={0}
            />
            <FeatureCard
              icon={<CogIcon className="w-12 h-12" />}
              title="执行助手AI"
              description="自动化任务执行，提高工作效率，让你专注于更重要的事情"
              href="/execution"
              delay={0.1}
            />
            <FeatureCard
              icon={<AcademicCapIcon className="w-12 h-12" />}
              title="学习伙伴AI"
              description="个性化学习路径，持续技能提升，助你在职场中保持竞争优势"
              href="/learning"
              delay={0.2}
            />
            <FeatureCard
              icon={<MagnifyingGlassIcon className="w-12 h-12" />}
              title="机会探索AI"
              description="发现市场机会，创造收入来源，开启多元化的财务自由之路"
              href="/opportunities"
              delay={0.3}
            />
          </motion.div>
        </div>
      </section>

      {/* 数据统计 */}
      <section id="stats" className="py-20 bg-starry-secondary/50 backdrop-blur-lg">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-16"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerChildren}
          >
            <motion.h2 
              className="text-4xl md:text-5xl font-bold text-white mb-6"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              平台数据
            </motion.h2>
            <motion.p 
              className="text-xl text-gray-300"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              用数据说话，见证每一个自由梦想的实现
            </motion.p>
          </motion.div>
          
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerChildren}
          >
            <StatCard number="1000+" label="活跃用户" delay={0} />
            <StatCard number="5000+" label="完成评估" delay={0.1} />
            <StatCard number="2500+" label="发现机会" delay={0.2} />
            <StatCard number="85%" label="满意度" delay={0.3} />
          </motion.div>
        </div>
      </section>

      {/* 五维自由度 */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-16"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerChildren}
          >
            <motion.h2 
              className="text-4xl md:text-5xl font-bold text-white mb-6"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              五维自由度评估
            </motion.h2>
            <motion.p 
              className="text-xl text-gray-300"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              全方位评估你的自由度，找到提升的方向
            </motion.p>
          </motion.div>
          
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerChildren}
          >
            <FeatureCard
              icon={<ChartBarIcon className="w-12 h-12" />}
              title="财务自由度"
              description="被动收入/支出比例、应急基金、收入多样性分析"
              delay={0}
            />
            <FeatureCard
              icon={<ClockIcon className="w-12 h-12" />}
              title="时间自由度"
              description="工作时间灵活性、假期自由、远程工作能力评估"
              delay={0.1}
            />
            <FeatureCard
              icon={<GlobeAltIcon className="w-12 h-12" />}
              title="地理自由度"
              description="工作地点限制、旅行频率、地理约束分析"
              delay={0.2}
            />
            <FeatureCard
              icon={<WrenchScrewdriverIcon className="w-12 h-12" />}
              title="技能自由度"
              description="可转移技能、学习能力、市场需求匹配度评估"
              delay={0.3}
            />
            <FeatureCard
              icon={<UsersIcon className="w-12 h-12" />}
              title="关系自由度"
              description="社交网络多样性、情感独立性、人际关系质量"
              delay={0.4}
            />
          </motion.div>
        </div>
      </section>

      {/* 行动号召 */}
      <section className="py-20 nebula-bg">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerChildren}
          >
            <motion.h2 
              className="text-4xl md:text-6xl font-bold text-white mb-8"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              开始你的自由之旅
            </motion.h2>
            <motion.p 
              className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              让AI成为你探索自由人生的得力助手，创造更多选择的可能性
            </motion.p>
            <motion.div 
              className="flex flex-col sm:flex-row gap-6 justify-center"
              variants={fadeInUp}
             transition={{ duration: 0.6 }}>
              <Link href="/assessment" className="starry-button glow-effect text-lg px-8 py-4">
                <RocketLaunchIcon className="w-6 h-6 inline mr-2" />
                开始评估
              </Link>
              <Link href="/learning" className="starry-button-secondary text-lg px-8 py-4">
                <AcademicCapIcon className="w-6 h-6 inline mr-2" />
                学习规划
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* 页脚 */}
      <footer className="py-12 bg-starry-secondary/80 backdrop-blur-lg border-t border-starry-purple/30">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4 flex items-center">
                <RocketLaunchIcon className="w-8 h-8 mr-2 text-starry-purple" />
                Freedom.AI
              </h3>
              <p className="text-gray-300 leading-relaxed">
                让AI成为你探索自由人生的得力助手。<br />
                自由不是想做什么就做什么，而是有能力选择不做什么。
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">快速链接</h4>
              <ul className="space-y-2">
                <li><Link href="/assessment" className="text-gray-300 hover:text-starry-cyan transition-colors">自由度评估</Link></li>
                <li><Link href="/opportunities" className="text-gray-300 hover:text-starry-cyan transition-colors">机会探索</Link></li>
                <li><Link href="/learning" className="text-gray-300 hover:text-starry-cyan transition-colors">学习规划</Link></li>
                <li><Link href="/profile" className="text-gray-300 hover:text-starry-cyan transition-colors">个人档案</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">联系我们</h4>
              <ul className="space-y-2 text-gray-300">
                <li>📧 support@freedom.ai</li>
                <li>🌐 www.freedom.ai</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-starry-purple/30 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400">&copy; 2024 Freedom.AI. All rights reserved.</p>
            <p className="text-gray-400 mt-4 md:mt-0">用AI的力量，创造更多选择的可能性</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
