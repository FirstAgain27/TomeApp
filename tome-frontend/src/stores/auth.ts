// src/stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI, type User, type LoginResponse } from '@/api/auth'
import { useCartStore } from './cart'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      const data: LoginResponse = await authAPI.login(email, password)
      
      // Сохраняем токены
      accessToken.value = data.access
      refreshToken.value = data.refresh
      user.value = data.user
      
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      // Загружаем корзину после логина
      const cartStore = useCartStore()
      await cartStore.fetchCart()
      
      return data
    } catch (err: any) {
      error.value = err.response?.data?.non_field_errors?.[0] || 'Ошибка входа'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const register = async (data: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authAPI.register(data)
      
      // После регистрации автоматически логинимся
      await login(data.email, data.password)
      
      return response
    } catch (err: any) {
      // Обработка ошибок валидации
      if (err.response?.data) {
        const errors = Object.entries(err.response.data)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages[0] : messages}`)
          .join(', ')
        error.value = errors
      } else {
        error.value = 'Ошибка регистрации'
      }
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      if (refreshToken.value) {
        await authAPI.logout(refreshToken.value)
      }
    } finally {
      // Всегда очищаем
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      
      // Очищаем корзину
      const cartStore = useCartStore()
      cartStore.clearCart()
    }
  }

  const fetchProfile = async () => {
    try {
      const profile = await authAPI.getProfile()
      user.value = profile
      localStorage.setItem('user', JSON.stringify(profile))
    } catch (err) {
      console.error('Failed to fetch profile:', err)
      await logout()
    }
  }

  const initialize = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = JSON.parse(savedUser)
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    fetchProfile,
    initialize
  }
})