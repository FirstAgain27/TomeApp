<!-- src/views/auth/LoginView.vue -->
<template>
  <div class="pt-8 pb-20">
    <div class="container mx-auto max-w-md px-6">
      <div class="text-center mb-10">
        <h1 class="text-4xl font-bold mb-4">Вход в аккаунт</h1>
        <p class="text-gray-600">
          Нет аккаунта?
          <router-link to="/register" class="text-black font-medium hover:underline">
            Зарегистрироваться
          </router-link>
        </p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium mb-2">Email</label>
          <input
            v-model="form.email"
            type="email"
            required
            class="input-field"
            placeholder="your@email.com"
          >
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium mb-2">Пароль</label>
          <input
            v-model="form.password"
            type="password"
            required
            class="input-field"
            placeholder="••••••••"
          >
        </div>

        <!-- Ошибка -->
        <div v-if="error" class="text-red-600 text-sm p-3 bg-red-50 rounded">
          {{ error }}
        </div>

        <!-- Кнопка -->
        <button
          type="submit"
          :disabled="isLoading"
          class="btn-primary w-full py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading">
            <svg class="animate-spin h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Вход...
          </span>
          <span v-else>Войти</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  email: '',
  password: ''
})

const isLoading = ref(false)
const error = ref('')

const handleLogin = async () => {
  if (!form.value.email || !form.value.password) {
    error.value = 'Заполните все поля'
    return
  }

  isLoading.value = true
  error.value = ''
  
  try {
    await authStore.login(form.value.email, form.value.password)
    router.push('/catalog')
  } catch (err: any) {
    error.value = err.response?.data?.non_field_errors?.[0] || 'Неверный email или пароль'
    console.error('Login error:', err)
  } finally {
    isLoading.value = false
  }
}
</script>