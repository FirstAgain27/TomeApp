<!-- src/components/layout/AppHeader.vue -->
<template>
  <header class="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50">
    <div class="container mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <!-- Логотип -->
        <router-link to="/" class="text-2xl font-bold tracking-tighter hover:opacity-80 transition-opacity">
          TOME
        </router-link>

        <!-- Навигация (скрыта на мобильных) -->
        <nav class="hidden md:flex space-x-10">
          <router-link to="/catalog" class="text-sm uppercase tracking-widest hover:text-gray-600 transition-colors">
            Каталог
          </router-link>
          <router-link to="/authors" class="text-sm uppercase tracking-widest hover:text-gray-600 transition-colors">
            Авторы
          </router-link>
          <router-link to="/categories" class="text-sm uppercase tracking-widest hover:text-gray-600 transition-colors">
            Коллекции
          </router-link>
          <a href="#" class="text-sm uppercase tracking-widest hover:text-gray-600 transition-colors">
            Контакты
          </a>
        </nav>

        <!-- Иконки действий -->
        <div class="flex items-center space-x-6">
          <button class="hover:text-gray-600 transition-colors" title="Поиск">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </button>
          
          <!-- Аутентификация -->
          <div v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="hover:text-gray-600 transition-colors flex items-center gap-1" title="Войти">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              <span class="text-sm hidden md:inline">Войти</span>
            </router-link>
          </div>
          <div v-else class="relative group">
            <button class="hover:text-gray-600 transition-colors flex items-center gap-2">
              <div class="w-8 h-8 bg-black text-white rounded-full flex items-center justify-center text-sm font-medium">
                {{ authStore.initials }}
              </div>
              <span class="text-sm hidden md:inline">{{ authStore.user?.first_name || authStore.user?.username }}</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            
            <!-- Dropdown меню -->
            <div class="absolute right-0 mt-2 w-48 bg-white border border-gray-200 shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
              <div class="p-4 border-b border-gray-100">
                <p class="font-medium">{{ authStore.user?.email }}</p>
                <p class="text-sm text-gray-500">Ваш аккаунт</p>
              </div>
              <div class="py-2">
                <router-link to="/profile" class="block px-4 py-2 hover:bg-gray-50">Профиль</router-link>
                <router-link to="/orders" class="block px-4 py-2 hover:bg-gray-50">Заказы</router-link>
                <router-link to="/wishlist" class="block px-4 py-2 hover:bg-gray-50">Избранное</router-link>
                <div class="border-t border-gray-100 my-2"></div>
                <button @click="handleLogout" class="block w-full text-left px-4 py-2 hover:bg-gray-50 text-red-600">
                  Выйти
                </button>
              </div>
            </div>
          </div>
          
          <!-- Иконка корзины -->
          <button 
            @click="cartStore.openCart" 
            class="hover:text-gray-600 transition-colors relative"
            title="Корзина"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
            <span 
              v-if="cartStore.totalItems > 0"
              class="absolute -top-2 -right-2 bg-black text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ cartStore.totalItems }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}
</script>