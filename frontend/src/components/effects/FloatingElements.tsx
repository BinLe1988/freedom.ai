'use client'

import { motion } from 'framer-motion'
import { 
  StarIcon, 
  RocketLaunchIcon, 
  LightBulbIcon, 
  MapIcon 
} from '@heroicons/react/24/outline'

const floatingVariants = {
  animate: {
    y: [-10, 10, -10],
    rotate: [0, 5, -5, 0],
    transition: {
      duration: 6,
      repeat: Infinity,
      ease: "easeInOut"
    }
  }
}

export function FloatingElements() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* 星星 */}
      <motion.div
        className="absolute top-1/4 left-1/10 text-white/20"
        variants={floatingVariants}
        animate="animate"
        style={{ animationDelay: '0s' }}
      >
        <StarIcon className="w-8 h-8" />
      </motion.div>

      {/* 火箭 */}
      <motion.div
        className="absolute top-1/3 right-1/6 text-white/20"
        variants={floatingVariants}
        animate="animate"
        style={{ animationDelay: '2s' }}
      >
        <RocketLaunchIcon className="w-6 h-6" />
      </motion.div>

      {/* 灯泡 */}
      <motion.div
        className="absolute bottom-2/5 left-1/5 text-white/20"
        variants={floatingVariants}
        animate="animate"
        style={{ animationDelay: '4s' }}
      >
        <LightBulbIcon className="w-7 h-7" />
      </motion.div>

      {/* 地图 */}
      <motion.div
        className="absolute bottom-1/5 right-1/10 text-white/20"
        variants={floatingVariants}
        animate="animate"
        style={{ animationDelay: '1s' }}
      >
        <MapIcon className="w-9 h-9" />
      </motion.div>

      {/* 额外的装饰性元素 */}
      <motion.div
        className="absolute top-1/2 left-1/12 w-2 h-2 bg-starry-purple/30 rounded-full"
        animate={{
          scale: [1, 1.5, 1],
          opacity: [0.3, 0.8, 0.3],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />

      <motion.div
        className="absolute top-3/4 right-1/8 w-1 h-1 bg-starry-cyan/40 rounded-full"
        animate={{
          scale: [1, 2, 1],
          opacity: [0.4, 1, 0.4],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1.5
        }}
      />

      <motion.div
        className="absolute top-1/6 right-1/4 w-3 h-3 bg-starry-blue/20 rounded-full"
        animate={{
          y: [0, -20, 0],
          x: [0, 10, 0],
          opacity: [0.2, 0.6, 0.2],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2
        }}
      />
    </div>
  )
}
