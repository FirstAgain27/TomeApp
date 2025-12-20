// src/stores/auth.ts
import { defineStore } from 'pinia'
import api from '@/api'
import type { User } from '@/types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  actions: {
    // Инициализация при запуске приложения
    initialize() {
      const token = localStorage.getItem('access_token')
      const userStr = localStorage.getItem('user')
      
      if (token && userStr) {
        try {
          this.user = JSON.parse(userStr)
          this.isAuthenticated = true
          
          // Устанавливаем токен в axios
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`
        } catch (error) {
          console.error('Ошибка при загрузке пользователя:', error)
          this.clearAuth()
        }
      }
    },

    // Логин
    async login(email: string, password: string) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/login/', { email, password })
        const { access, refresh, user } = response.data
        
        // Сохраняем токены и пользователя
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user', JSON.stringify(user))
        
        // Устанавливаем токен в axios
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`
        
        // Обновляем состояние
        this.user = user
        this.isAuthenticated = true
        
        return { success: true }
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'Ошибка при входе'
        return { success: false, error }
      } finally {
        this.loading = false
      }
    },

    // Регистрация
    async register(userData: {
      username: string
      email: string
      password: string
      password_confirm: string
      first_name?: string
      last_name?: string
    }) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/register/', userData)
        const { access, refresh, user } = response.data
        
        // Сохраняем токены и пользователя
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user', JSON.stringify(user))
        
        // Устанавливаем токен в axios
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`
        
        // Обновляем состояние
        this.user = user
        this.isAuthenticated = true
        
        return { success: true }
      } catch (error: any) {
        if (error.response?.data) {
          // Обработка ошибок валидации Django
          const errors = error.response.data
          if (errors.email) {
            this.error = `Email: ${errors.email[0]}`
          } else if (errors.username) {
            this.error = `Имя пользователя: ${errors.username[0]}`
          } else if (errors.password) {
            this.error = `Пароль: ${errors.password[0]}`
          } else {
            this.error = 'Ошибка при регистрации'
          }
        } else {
          this.error = 'Ошибка при регистрации'
        }
        return { success: false, error }
      } finally {
        this.loading = false
      }
    },

    // Выход
    async logout() {
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          await api.post('/logout/', { refresh_token: refreshToken })
        }
      } catch (error) {
        console.error('Ошибка при выходе:', error)
      } finally {
        this.clearAuth()
      }
    },

    // Обновление токена
    async refreshToken() {
      try {
        const refresh = localStorage.getItem('refresh_token')
        if (!refresh) throw new Error('No refresh token')
        
        const response = await api.post('/token/refresh/', { refresh })
        const newAccessToken = response.data.access
        
        localStorage.setItem('access_token', newAccessToken)
        api.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
        
        return newAccessToken
      } catch (error) {
        this.clearAuth()
        throw error
      }
    },

    // Очистка авторизации
    clearAuth() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      delete api.defaults.headers.common['Authorization']
      
      this.user = null
      this.isAuthenticated = false
      this.error = null
    },

    // Получение профиля
    async fetchProfile() {
      try {
        const response = await api.get('/profile/')
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
      } catch (error) {
        console.error('Ошибка при получении профиля:', error)
      }
    },

    // Обновление профиля
    async updateProfile(profileData: any) {
      try {
        const response = await api.put('/profile/', profileData)
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
        return { success: true }
      } catch (error: any) {
        return { success: false, error: error.response?.data }
      }
    },

    // Смена пароля
    async changePassword(passwordData: {
      old_password: string
      new_password: string
      new_password_confirm: string
    }) {
      try {
        await api.post('/change-password/', passwordData)
        return { success: true }
      } catch (error: any) {
        return { success: false, error: error.response?.data }
      }
    }
  },

  getters: {
    // Полное имя пользователя
    fullName: (state) => {
      if (!state.user) return ''
      return `${state.user.first_name || ''} ${state.user.last_name || ''}`.trim() || state.user.username
    },
    
    // Является ли пользователь админом
    isAdmin: (state) => state.user?.is_staff || false,
    
    // Инициалы для аватара
    initials: (state) => {
      if (!state.user) return 'U'
      const first = state.user.first_name?.charAt(0) || state.user.username?.charAt(0) || 'U'
      return first.toUpperCase()
    }
  }
})