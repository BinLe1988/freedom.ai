'use client'

import { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  RocketLaunchIcon, 
  StarIcon, 
  ChartBarIcon,
  Bars3Icon,
  XMarkIcon,
  UserIcon,
  AcademicCapIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline'

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  const navItems = [
    { href: '/assessment', label: '自由度评估', icon: ChartBarIcon },
    { href: '/opportunities', label: '机会探索', icon: MagnifyingGlassIcon },
    { href: '/learning', label: '学习规划', icon: AcademicCapIcon },
  ]

  return (
    <motion.nav 
      className="starry-navbar fixed top-0 left-0 right-0 z-50"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 group">
            <RocketLaunchIcon className="w-8 h-8 text-starry-cyan group-hover:animate-pulse" />
            <span className="text-2xl font-bold text-gradient">Freedom.AI</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center space-x-1 text-gray-300 hover:text-starry-cyan transition-colors duration-300 relative group"
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
                <div className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-starry group-hover:w-full transition-all duration-300" />
              </Link>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-white hover:text-starry-cyan transition-colors"
          >
            {isOpen ? (
              <XMarkIcon className="w-6 h-6" />
            ) : (
              <Bars3Icon className="w-6 h-6" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <motion.div
            className="md:hidden py-4 border-t border-starry-purple/30"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="flex flex-col space-y-4">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="flex items-center space-x-2 text-gray-300 hover:text-starry-cyan transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  <item.icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </motion.nav>
  )
}
