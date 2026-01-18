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

          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium mb-2">Имя пользователя</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="input-field"
              placeholder="johndoe"
              :disabled="loading"
            />
          </div>

          <!-- First Name (optional) -->
          <div>
            <label for="first_name" class="block text-sm font-medium mb-2">Имя (необязательно)</label>
            <input
              id="first_name"
              v-model="form.first_name"
              type="text"
              class="input-field"
              placeholder="Иван"
              :disabled="loading"
            />
          </div>

          <!-- Last Name (optional) -->
          <div>
            <label for="last_name" class="block text-sm font-medium mb-2">Фамилия (необязательно)</label>
            <input
              id="last_name"
              v-model="form.last_name"
              type="text"
              class="input-field"
              placeholder="Иванов"
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

const form = reactive({
  email: '',
  username: '',
  password: '',
  password_confirm: '',
  first_name: '',
  last_name: '',
  agreeTerms: false
})

const handleRegister = async () => {
  // Валидация
  if (!form.email || !form.password || !form.password_confirm || !form.username) {
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

  try {
    // Реальная регистрация через authStore
    await authStore.register({
      email: form.email,
      username: form.username,
      password: form.password,
      password_confirm: form.password_confirm,
      first_name: form.first_name,
      last_name: form.last_name
    })
    
    // Перенаправление происходит внутри authStore
    // Если нужно показать сообщение о успехе:
    // router.push('/catalog') // authStore уже делает это
    
  } catch (err: any) {
    // Обработка ошибок от бэкенда
    if (err.response?.data) {
      // Парсим ошибки Django
      const errors = Object.entries(err.response.data)
        .map(([field, messages]) => {
          const fieldName = field === 'non_field_errors' ? '' : `${field}: `
          return `${fieldName}${Array.isArray(messages) ? messages[0] : messages}`
        })
        .join(', ')
      error.value = errors
    } else {
      error.value = err.message || 'Ошибка при регистрации'
    }
    console.error('Registration error:', err)
  } finally {
    loading.value = false
  }
}
</script>