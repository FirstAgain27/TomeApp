<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <router-link to="/" class="text-3xl font-bold tracking-tighter inline-block mb-2">
          TOME
        </router-link>
        <h2 class="mt-6 text-2xl font-bold">Вход в аккаунт</h2>
        <p class="mt-2 text-sm text-gray-600">
          Или
          <router-link to="/register" class="font-medium hover:text-black">
            создайте новый аккаунт
          </router-link>
        </p>
      </div>

      <!-- Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
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
            <div class="flex justify-between items-center mb-2">
              <label for="password" class="block text-sm font-medium">Пароль</label>
              <router-link to="/forgot-password" class="text-sm hover:text-black">
                Забыли пароль?
              </router-link>
            </div>
            <input
              id="password"
              v-model="form.password"
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
            {{ loading ? 'Вход...' : 'Войти' }}
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

const form = reactive({
  email: '',
  password: ''
})

const handleLogin = async () => {
  if (!form.email || !form.password) {
    error.value = 'Пожалуйста, заполните все поля'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // Пока используем моковый вход (без API)
    // TODO: Заменить на реальный API вызов
    console.log('Моковый вход с:', form.email)
    
    // Имитация успешного входа
    setTimeout(() => {
      // Создаём мокового пользователя
      const mockUser = {
        id: 1,
        email: form.email,
        username: form.email.split('@')[0],
        first_name: 'Тест',
        last_name: 'Пользователь',
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
      
      // Редирект на главную
      const redirect = router.currentRoute.value.query.redirect as string || '/'
      router.push(redirect)
    }, 1000)
    
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка при входе. Попробуйте позже.'
  } finally {
    loading.value = false
  }
}
</script>