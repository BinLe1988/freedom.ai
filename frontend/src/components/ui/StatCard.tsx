'use client'

import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

interface StatCardProps {
  number: string
  label: string
  delay?: number
}

export function StatCard({ number, label, delay = 0 }: StatCardProps) {
  const [displayNumber, setDisplayNumber] = useState('0')
  const [hasAnimated, setHasAnimated] = useState(false)

  // 提取数字进行动画
  const numericValue = parseInt(number.replace(/[^\d]/g, ''))
  const suffix = number.replace(/[\d]/g, '')

  useEffect(() => {
    if (!hasAnimated) return

    const duration = 2000
    const steps = 60
    const increment = numericValue / steps
    let current = 0

    const timer = setInterval(() => {
      current += increment
      if (current >= numericValue) {
        current = numericValue
        clearInterval(timer)
      }
      setDisplayNumber(Math.floor(current) + suffix)
    }, duration / steps)

    return () => clearInterval(timer)
  }, [hasAnimated, numericValue, suffix])

  return (
    <motion.div
      className="stat-card"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay }}
      onAnimationComplete={() => setHasAnimated(true)}
      whileHover={{ 
        y: -5,
        transition: { duration: 0.2 }
      }}
    >
      <div className="stat-number">
        {hasAnimated ? displayNumber : '0'}
      </div>
      <div className="stat-label">
        {label}
      </div>
    </motion.div>
  )
}
