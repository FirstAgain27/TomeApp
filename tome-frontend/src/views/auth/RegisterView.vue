<!-- src/views/auth/RegisterView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <router-link to="/" class="text-3xl font-bold tracking-tighter inline-block mb-2">
          TOME
        </router-link>
        <h2 class="mt-6 text-2xl font-bold">Создание аккаунта</h2>
        <p class="mt-2 text-sm text-gray-600">
          Или
          <router-link to="/login" class="font-medium hover:text-black">
            войдите в существующий
          </router-link>
        </p>
      </div>

      <!-- Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium mb-2">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="input-field"
              placeholder="you@example.com"
              :disabled="loading"
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium mb-2">Пароль</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="input-field"
              placeholder="••••••••"
              :disabled="loading"
            />
            <p class="mt-1 text-xs text-gray-500">Минимум 8 символов</p>
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="password_confirm" class="block text-sm font-medium mb-2">Подтверждение пароля</label>
            <input
              id="password_confirm"
              v-model="form.password_confirm"
              type="password"
              required
              class="input-field"
              placeholder="••••••••"
              :disabled="loading"
            />
          </div>
        </div>

        <!-- Error message -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded text-sm">
          {{ error }}
        </div>

        <!-- Success message -->
        <div v-if="success" class="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded text-sm">
          {{ success }}
        </div>

        <!-- Terms -->
        <div class="flex items-center">
          <input
            id="terms"
            v-model="form.agreeTerms"
            type="checkbox"
            required
            class="h-4 w-4 text-black focus:ring-black border-gray-300 rounded"
            :disabled="loading"
          />
          <label for="terms" class="ml-2 block text-sm text-gray-600">
            Я согласен с условиями использования
          </label>
        </div>

        <!-- Submit button -->
        <div>
          <button
            type="submit"
            class="btn-primary w-full flex justify-center items-center"
            :disabled="loading"
            :class="{ 'opacity-50 cursor-not-allowed': loading }"
          >
            <svg
              v-if="loading"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            {{ loading ? 'Регистрация...' : 'Создать аккаунт' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')
const success = ref('')

const form = reactive({
  email: '',
  password: '',
  password_confirm: '',
  agreeTerms: false
})

const handleRegister = async () => {
  // Валидация
  if (!form.email || !form.password || !form.password_confirm) {
    error.value = 'Пожалуйста, заполните все обязательные поля'
    return
  }

  if (form.password !== form.password_confirm) {
    error.value = 'Пароли не совпадают'
    return
  }

  if (form.password.length < 8) {
    error.value = 'Пароль должен содержать минимум 8 символов'
    return
  }

  if (!form.agreeTerms) {
    error.value = 'Необходимо согласиться с условиями'
    return
  }

  loading.value = true
  error.value = ''
  success.value = ''

  try {
    // Пока используем моковую регистрацию (без API)
    console.log('Моковая регистрация с:', form.email)
    
    // Имитация успешной регистрации
    setTimeout(() => {
      // Создаём мокового пользователя
      const mockUser = {
        id: Date.now(),
        email: form.email,
        username: form.email.split('@')[0],
        first_name: '',
        last_name: '',
        is_staff: false,
        bio: '',
        avatar: null
      }
      
      // Сохраняем в localStorage для теста
      localStorage.setItem('access_token', 'mock-token-' + Date.now())
      localStorage.setItem('refresh_token', 'mock-refresh-' + Date.now())
      localStorage.setItem('user', JSON.stringify(mockUser))
      
      // Обновляем store
      authStore.user = mockUser
      authStore.isAuthenticated = true
      
      success.value = 'Аккаунт успешно создан! Перенаправляем...'
      
      // Автоматический вход после регистрации
      setTimeout(() => {
        router.push('/')
      }, 1500)
    }, 1000)
    
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при регистрации. Попробуйте позже.'
  } finally {
    loading.value = false
  }
}
</script>