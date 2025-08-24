'use client'

import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface FeatureCardProps {
  icon: ReactNode
  title: string
  description: string
  delay?: number
}

export function FeatureCard({ icon, title, description, delay = 0 }: FeatureCardProps) {
  return (
    <motion.div
      className="starry-card p-8 text-center h-full group cursor-pointer"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay }}
      whileHover={{ 
        y: -10,
        scale: 1.02,
        transition: { duration: 0.3 }
      }}
    >
      {/* 顶部装饰线 */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-starry" />
      
      {/* 图标 */}
      <motion.div 
        className="text-gradient mb-6 flex justify-center"
        whileHover={{ 
          scale: 1.1,
          rotate: 5,
          transition: { duration: 0.3 }
        }}
      >
        <div className="float-animation">
          {icon}
        </div>
      </motion.div>
      
      {/* 标题 */}
      <h3 className="text-xl font-semibold text-white mb-4 group-hover:text-starry-cyan transition-colors duration-300">
        {title}
      </h3>
      
      {/* 描述 */}
      <p className="text-gray-300 leading-relaxed">
        {description}
      </p>
      
      {/* 悬停效果 */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-starry-purple/10 to-starry-blue/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        initial={false}
      />
    </motion.div>
  )
}
