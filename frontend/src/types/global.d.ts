// 全局类型定义
declare global {
  interface Window {
    gtag?: (...args: any[]) => void
  }
}

// React组件类型
export interface ComponentProps {
  children?: React.ReactNode
  className?: string
}

// 动画变体类型
export interface AnimationVariant {
  initial?: any
  animate?: any
  exit?: any
  whileHover?: any
  whileTap?: any
}

// API响应类型
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// 用户相关类型
export interface User {
  id: string
  username: string
  email: string
  full_name?: string
  created_at?: string
  last_login?: string
}

export interface UserProfile {
  user_id: string
  full_name?: string
  bio?: string
  location?: string
  current_role?: string
  experience_years?: number
  skills?: string[]
  interests?: string[]
}

export interface UserPreferences {
  user_id: string
  preferred_work_type?: string
  location_preferences?: string[]
  industry_preferences?: string[]
  company_size_preference?: string
  salary_expectations?: {
    min?: number
    max?: number
    currency?: string
  }
}

export {}
