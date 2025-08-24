'use client'

import { useEffect, useRef } from 'react'

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  size: number
  opacity: number
  element: HTMLDivElement
}

export function StarryEffects() {
  const containerRef = useRef<HTMLDivElement>(null)
  const particlesRef = useRef<Particle[]>([])
  const animationRef = useRef<number>()

  useEffect(() => {
    if (!containerRef.current) return

    const container = containerRef.current
    const particles: Particle[] = []
    const particleCount = 100

    // 创建粒子
    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div')
      particle.className = 'absolute w-0.5 h-0.5 bg-white rounded-full opacity-80'
      
      const x = Math.random() * window.innerWidth
      const y = Math.random() * window.innerHeight
      const size = Math.random() * 3 + 1
      const opacity = Math.random() * 0.8 + 0.2
      const delay = Math.random() * 4

      particle.style.left = x + 'px'
      particle.style.top = y + 'px'
      particle.style.width = size + 'px'
      particle.style.height = size + 'px'
      particle.style.opacity = opacity.toString()
      particle.style.animationDelay = delay + 's'
      particle.style.animation = 'twinkle 4s ease-in-out infinite alternate'

      container.appendChild(particle)

      particles.push({
        x,
        y,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size,
        opacity,
        element: particle
      })
    }

    particlesRef.current = particles

    // 动画循环
    const animate = () => {
      particles.forEach(particle => {
        particle.x += particle.vx
        particle.y += particle.vy

        // 边界检查
        if (particle.x < 0 || particle.x > window.innerWidth) {
          particle.vx *= -1
        }
        if (particle.y < 0 || particle.y > window.innerHeight) {
          particle.vy *= -1
        }

        // 更新位置
        particle.element.style.left = particle.x + 'px'
        particle.element.style.top = particle.y + 'px'
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    // 流星效果
    const createShootingStar = () => {
      if (Math.random() < 0.1) {
        const shootingStar = document.createElement('div')
        shootingStar.className = 'absolute w-0.5 h-0.5 bg-gradient-to-r from-white to-blue-400 rounded-full'
        shootingStar.style.boxShadow = '0 0 10px #74b9ff, 0 0 20px #74b9ff, 0 0 30px #74b9ff'

        const startX = Math.random() * window.innerWidth
        const startY = -10
        const endX = startX + (Math.random() - 0.5) * 400
        const endY = window.innerHeight + 10

        shootingStar.style.left = startX + 'px'
        shootingStar.style.top = startY + 'px'

        container.appendChild(shootingStar)

        const duration = 1000 + Math.random() * 2000
        shootingStar.animate([
          {
            left: startX + 'px',
            top: startY + 'px',
            opacity: '0'
          },
          {
            left: (startX + endX) / 2 + 'px',
            top: (startY + endY) / 2 + 'px',
            opacity: '1'
          },
          {
            left: endX + 'px',
            top: endY + 'px',
            opacity: '0'
          }
        ], {
          duration,
          easing: 'ease-out'
        }).onfinish = () => {
          container.removeChild(shootingStar)
        }
      }
    }

    const shootingStarInterval = setInterval(createShootingStar, 2000)

    // 鼠标轨迹效果
    const handleMouseMove = (e: MouseEvent) => {
      const trail = document.createElement('div')
      trail.className = 'absolute w-1 h-1 bg-starry-purple rounded-full pointer-events-none z-50'
      trail.style.left = e.clientX + 'px'
      trail.style.top = e.clientY + 'px'
      trail.style.background = 'radial-gradient(circle, #6c5ce7, transparent)'

      container.appendChild(trail)

      trail.animate([
        { opacity: '0.8', transform: 'scale(1)' },
        { opacity: '0', transform: 'scale(0)' }
      ], {
        duration: 800,
        easing: 'ease-out'
      }).onfinish = () => {
        if (container.contains(trail)) {
          container.removeChild(trail)
        }
      }
    }

    document.addEventListener('mousemove', handleMouseMove)

    // 窗口大小改变处理
    const handleResize = () => {
      particles.forEach(particle => {
        if (particle.x > window.innerWidth) particle.x = window.innerWidth
        if (particle.y > window.innerHeight) particle.y = window.innerHeight
      })
    }

    window.addEventListener('resize', handleResize)

    // 清理函数
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
      clearInterval(shootingStarInterval)
      document.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('resize', handleResize)
      
      particles.forEach(particle => {
        if (container.contains(particle.element)) {
          container.removeChild(particle.element)
        }
      })
    }
  }, [])

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ zIndex: -1 }}
    />
  )
}

// 星云爆炸效果组件
export function NebulaExplosion({ x, y, onComplete }: { x: number, y: number, onComplete: () => void }) {
  const nebulaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!nebulaRef.current) return

    const nebula = nebulaRef.current
    nebula.style.left = (x - 50) + 'px'
    nebula.style.top = (y - 50) + 'px'

    nebula.animate([
      { opacity: '0', transform: 'scale(0)' },
      { opacity: '0.6', transform: 'scale(1)' },
      { opacity: '0', transform: 'scale(1.5)' }
    ], {
      duration: 2000,
      easing: 'ease-out'
    }).onfinish = onComplete
  }, [x, y, onComplete])

  return (
    <div
      ref={nebulaRef}
      className="fixed w-24 h-24 rounded-full pointer-events-none z-50"
      style={{
        background: 'radial-gradient(circle, rgba(108, 92, 231, 0.3), transparent)',
        zIndex: 999
      }}
    />
  )
}
