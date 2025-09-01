import axios from 'axios'
import Cookies from 'js-cookie'

// 创建axios实例
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  (config) => {
    const token = Cookies.get('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token过期或无效，清除本地存储并重定向到登录页
      Cookies.remove('auth_token')
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// API接口函数
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/login', { email, password }),
  
  register: (username: string, email: string, password: string) =>
    api.post('/register', { username, email, password }),
  
  logout: () =>
    api.post('/logout'),
  
  getProfile: () =>
    api.get('/profile'),
}

export const assessmentAPI = {
  calculate: (data: any) =>
    api.post('/api/calculate_freedom', data),
  
  getHistory: () =>
    api.get('/api/get_assessment_history'),
  
  test: (data: any) =>
    api.post('/api/test_assessment', data),
}

export const opportunityAPI = {
  discover: (data: any) =>
    api.post('/api/discover_opportunities', data),
  
  getRecommendations: () =>
    api.get('/api/opportunities'),
}

export const profileAPI = {
  update: (data: any) =>
    api.post('/api/update_profile', data),
  
  get: () =>
    api.get('/profile'),
}

export const learningAPI = {
  createPlan: (data: any) =>
    api.post('/api/create_learning_plan', data),
  
  getPlans: () =>
    api.get('/api/learning_plans'),
}

export const analyticsAPI = {
  getUserAnalytics: () =>
    api.get('/api/user_analytics'),
  
  exportData: () =>
    api.get('/api/export_data'),
}

// 工具函数
export const handleApiError = (error: any) => {
  if (error.response) {
    // 服务器响应了错误状态码
    const message = error.response.data?.error || error.response.data?.message || '请求失败'
    return { success: false, error: message }
  } else if (error.request) {
    // 请求已发出但没有收到响应
    return { success: false, error: '网络连接失败，请检查网络设置' }
  } else {
    // 其他错误
    return { success: false, error: '发生未知错误，请稍后重试' }
  }
}

// 上传文件
export const uploadFile = async (file: File, endpoint: string) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await api.post(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw handleApiError(error)
  }
}

// 下载文件
export const downloadFile = async (endpoint: string, filename: string) => {
  try {
    const response = await api.get(endpoint, {
      responseType: 'blob',
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    throw handleApiError(error)
  }
}

export default api
