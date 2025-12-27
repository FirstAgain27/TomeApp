// src/api/auth.ts
import api from './index'

export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  full_name?: string
}

export interface LoginResponse {
  user: User
  refresh: string
  access: string
  message: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name?: string
  last_name?: string
}

export const authAPI = {
  // Логин
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await api.post('/auth/login/', { email, password })
    return response.data
  },

  // Регистрация
  async register(data: RegisterData): Promise<LoginResponse> {
    const response = await api.post('/auth/register/', data)
    return response.data
  },

  // Выход
  async logout(refreshToken: string): Promise<void> {
    await api.post('/auth/logout/', { refresh_token: refreshToken })
  },

  // Профиль
  async getProfile(): Promise<User> {
    const response = await api.get('/auth/profile/')
    return response.data
  }
}