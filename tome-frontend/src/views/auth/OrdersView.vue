<!-- src/views/auth/OrdersView.vue -->
<template>
  <div class="pt-8 pb-20">
    <div class="container mx-auto px-6">
      <!-- Хлебные крошки -->
      <nav class="flex text-sm mb-10">
        <router-link to="/" class="text-gray-500 hover:text-black">Главная</router-link>
        <span class="mx-2">/</span>
        <router-link to="/profile" class="text-gray-500 hover:text-black">Профиль</router-link>
        <span class="mx-2">/</span>
        <span class="text-black">Заказы</span>
      </nav>

      <h1 class="text-3xl font-bold mb-8">Мои заказы</h1>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-black"></div>
        <p class="mt-4 text-gray-600">Загружаем заказы...</p>
      </div>

      <div v-else-if="orders.length === 0" class="text-center py-20 border border-gray-200">
        <div class="w-24 h-24 mx-auto mb-6 flex items-center justify-center rounded-full bg-gray-100">
          <span class="text-4xl">📦</span>
        </div>
        <h2 class="text-2xl font-bold mb-4">Заказов пока нет</h2>
        <p class="text-gray-600 mb-8">Как только вы сделаете заказ, он появится здесь</p>
        <router-link to="/catalog" class="btn-primary">Перейти в каталог</router-link>
      </div>

      <div v-else class="space-y-6">
        <div 
          v-for="order in orders" 
          :key="order.id"
          class="border border-gray-200 p-6 hover:shadow-md transition-shadow"
        >
          <div class="flex justify-between items-start mb-6">
            <div>
              <h3 class="text-xl font-bold">Заказ #{{ order.id }}</h3>
              <p class="text-gray-600 text-sm mt-1">{{ order.created_at }}</p>
            </div>
            <span class="px-4 py-1 bg-black text-white text-sm font-medium">
              {{ order.status }}
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Товары -->
            <div>
              <h4 class="font-bold mb-4">Товары</h4>
              <div class="space-y-4">
                <div 
                  v-for="item in order.items" 
                  :key="item.id"
                  class="flex gap-4"
                >
                  <div class="w-16 h-24 bg-gray-100 flex-shrink-0"></div>
                  <div>
                    <p class="font-medium">{{ item.book_title }}</p>
                    <p class="text-sm text-gray-600">{{ item.quantity }} × {{ item.price }} ₽</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Информация о заказе -->
            <div>
              <h4 class="font-bold mb-4">Информация</h4>
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-600">Товары</span>
                  <span>{{ order.items_total }} ₽</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Доставка</span>
                  <span>{{ order.shipping_cost }} ₽</span>
                </div>
                <div class="flex justify-between font-bold pt-3 border-t border-gray-200">
                  <span>Итого</span>
                  <span>{{ order.total }} ₽</span>
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-end mt-6">
            <button class="btn-secondary">Детали заказа</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const loading = ref(true)
const orders = ref<any[]>([])

onMounted(() => {
  // Имитация загрузки заказов
  setTimeout(() => {
    orders.value = [
      {
        id: 'ORD-2024-001',
        created_at: '15 декабря 2024',
        status: 'Доставлен',
        items: [
          { id: 1, book_title: 'Мастер и Маргарита', quantity: 1, price: 5600 },
          { id: 2, book_title: '1984', quantity: 2, price: 3200 }
        ],
        items_total: 12000,
        shipping_cost: 0,
        total: 12000
      }
    ]
    loading.value = false
  }, 1000)
})
</script>