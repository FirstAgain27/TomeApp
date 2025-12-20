<!-- src/components/auth/ProtectedRoute.vue -->
<template>
  <slot v-if="isAuthenticated" />
  <div v-else class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <h2 class="text-2xl font-bold mb-4">Требуется авторизация</h2>
      <p class="text-gray-600 mb-8">Пожалуйста, войдите в систему чтобы получить доступ</p>
      <router-link to="/login" class="btn-primary">Войти</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)
</script>
