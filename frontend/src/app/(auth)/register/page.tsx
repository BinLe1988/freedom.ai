'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  UserIcon,
  EnvelopeIcon, 
  LockClosedIcon, 
  EyeIcon, 
  EyeSlashIcon,
  RocketLaunchIcon,
  CheckIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '@/store/auth'
import { useNotification } from '@/components/ui/Notification'

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [agreedToTerms, setAgreedToTerms] = useState(false)
  
  const { register } = useAuth()
  const { success, error } = useNotification()
  const router = useRouter()

  // 密码强度检查
  const getPasswordStrength = (password: string) => {
    let strength = 0
    const checks = {
      length: password.length >= 8,
      lowercase: /[a-z]/.test(password),
      uppercase: /[A-Z]/.test(password),
      number: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    }
    
    Object.values(checks).forEach(check => {
      if (check) strength++
    })
    
    return { strength, checks }
  }

  const passwordStrength = getPasswordStrength(formData.password)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!agreedToTerms) {
      error('注册失败', '请同意服务条款和隐私政策')
      return
    }

    if (formData.password !== formData.confirmPassword) {
      error('注册失败', '两次输入的密码不一致')
      return
    }

    if (passwordStrength.strength < 3) {
      error('注册失败', '密码强度不够，请设置更安全的密码')
      return
    }

    setLoading(true)

    try {
      const result = await register(formData.username, formData.email, formData.password)
      
      if (result) {
        success('注册成功', '欢迎加入Freedom.AI!')
        router.push('/dashboard')
      } else {
        error('注册失败', '用户名或邮箱已存在，请重试')
      }
    } catch (err) {
      error('注册失败', '网络错误，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const getStrengthColor = (strength: number) => {
    if (strength < 2) return 'bg-red-500'
    if (strength < 4) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  const getStrengthText = (strength: number) => {
    if (strength < 2) return '弱'
    if (strength < 4) return '中等'
    return '强'
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        className="max-w-md w-full space-y-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* 头部 */}
        <div className="text-center">
          <motion.div
            className="flex justify-center mb-6"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          >
            <div className="w-20 h-20 bg-gradient-starry rounded-full flex items-center justify-center glow-effect">
              <RocketLaunchIcon className="w-10 h-10 text-white" />
            </div>
          </motion.div>
          
          <motion.h2
            className="text-3xl font-bold text-white mb-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            开始你的自由之旅
          </motion.h2>
          
          <motion.p
            className="text-gray-400"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            创建你的Freedom.AI账户
          </motion.p>
        </div>

        {/* 注册表单 */}
        <motion.div
          className="starry-card p-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* 用户名输入 */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
                用户名
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <UserIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  className="starry-input pl-10 w-full"
                  placeholder="输入用户名"
                  value={formData.username}
                  onChange={handleChange}
                />
              </div>
            </div>

            {/* 邮箱输入 */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                邮箱地址
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <EnvelopeIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  className="starry-input pl-10 w-full"
                  placeholder="输入邮箱地址"
                  value={formData.email}
                  onChange={handleChange}
                />
              </div>
            </div>

            {/* 密码输入 */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                密码
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  className="starry-input pl-10 pr-10 w-full"
                  placeholder="设置密码"
                  value={formData.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-300" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-300" />
                  )}
                </button>
              </div>
              
              {/* 密码强度指示器 */}
              {formData.password && (
                <div className="mt-2">
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-700 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full transition-all duration-300 ${getStrengthColor(passwordStrength.strength)}`}
                        style={{ width: `${(passwordStrength.strength / 5) * 100}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-400">
                      {getStrengthText(passwordStrength.strength)}
                    </span>
                  </div>
                  
                  <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
                    {Object.entries(passwordStrength.checks).map(([key, passed]) => (
                      <div key={key} className={`flex items-center ${passed ? 'text-green-400' : 'text-gray-500'}`}>
                        <CheckIcon className={`w-3 h-3 mr-1 ${passed ? 'opacity-100' : 'opacity-30'}`} />
                        {key === 'length' && '8位以上'}
                        {key === 'lowercase' && '小写字母'}
                        {key === 'uppercase' && '大写字母'}
                        {key === 'number' && '数字'}
                        {key === 'special' && '特殊字符'}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* 确认密码输入 */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-2">
                确认密码
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  required
                  className="starry-input pl-10 pr-10 w-full"
                  placeholder="再次输入密码"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-300" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-300" />
                  )}
                </button>
              </div>
              
              {/* 密码匹配指示 */}
              {formData.confirmPassword && (
                <div className="mt-1">
                  {formData.password === formData.confirmPassword ? (
                    <p className="text-xs text-green-400 flex items-center">
                      <CheckIcon className="w-3 h-3 mr-1" />
                      密码匹配
                    </p>
                  ) : (
                    <p className="text-xs text-red-400">
                      密码不匹配
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* 服务条款 */}
            <div className="flex items-center">
              <input
                id="terms"
                name="terms"
                type="checkbox"
                className="h-4 w-4 text-starry-purple focus:ring-starry-purple border-gray-600 rounded bg-starry-secondary"
                checked={agreedToTerms}
                onChange={(e) => setAgreedToTerms(e.target.checked)}
              />
              <label htmlFor="terms" className="ml-2 block text-sm text-gray-300">
                我同意{' '}
                <Link href="/terms" className="text-starry-cyan hover:text-starry-blue">
                  服务条款
                </Link>
                {' '}和{' '}
                <Link href="/privacy" className="text-starry-cyan hover:text-starry-blue">
                  隐私政策
                </Link>
              </label>
            </div>

            {/* 注册按钮 */}
            <motion.button
              type="submit"
              disabled={loading || !agreedToTerms}
              className="starry-button w-full py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              whileHover={{ scale: loading ? 1 : 1.02 }}
              whileTap={{ scale: loading ? 1 : 0.98 }}
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="loading-spinner w-5 h-5 mr-2" />
                  注册中...
                </div>
              ) : (
                '创建账户'
              )}
            </motion.button>
          </form>

          {/* 分割线 */}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-600" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-starry-secondary text-gray-400">或者</span>
              </div>
            </div>
          </div>

          {/* 登录链接 */}
          <div className="mt-6 text-center">
            <p className="text-gray-400">
              已有账户？{' '}
              <Link href="/login" className="text-starry-cyan hover:text-starry-blue transition-colors font-medium">
                立即登录
              </Link>
            </p>
          </div>
        </motion.div>

        {/* 返回首页 */}
        <motion.div
          className="text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
        >
          <Link href="/" className="text-gray-400 hover:text-starry-cyan transition-colors">
            ← 返回首页
          </Link>
        </motion.div>
      </motion.div>
    </div>
  )
}
