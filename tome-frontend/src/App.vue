<!-- src/App.vue -->
<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- Шапка сайта -->
    <AppHeader />

    <!-- Основное содержимое страницы -->
    <main class="flex-grow pt-16">
      <router-view />
    </main>

    <!-- Подвал сайта -->
    <AppFooter />

    <!-- Боковая панель корзины -->
    <CartDrawer />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import CartDrawer from '@/components/cart/CartDrawer.vue'

const authStore = useAuthStore()

onMounted(() => {
  // Инициализируем авторизацию при загрузке приложения
  authStore.initialize()
})
</script>