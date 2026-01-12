<template>
  <div class="min-h-screen bg-white flex flex-col">
    <AppHeader />
    <main class="flex-grow pt-16">
      <router-view />
    </main>
    <AppFooter />
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
  authStore.initialize()
})
</script>