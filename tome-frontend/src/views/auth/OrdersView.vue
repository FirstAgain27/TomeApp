<!-- src/views/auth/OrdersView.vue -->
<template>
  <div class="pt-8 pb-20">
    <div class="container mx-auto px-6">
      <!-- Header -->
      <div class="mb-10">
        <h1 class="text-4xl font-bold mb-4">Мои заказы</h1>
        <div class="flex items-center text-sm text-gray-600">
          <router-link to="/profile" class="hover:text-black">← Назад в профиль</router-link>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="isLoading && orders.length === 0" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-black mb-4"></div>
        <p class="text-gray-600">Загружаем ваши заказы...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error && orders.length === 0" class="text-center py-20">
        <div class="text-red-600 mb-4">⚠️ {{ error }}</div>
        <button @click="fetchOrders" class="btn-primary">Попробовать снова</button>
      </div>

      <!-- Empty state -->
      <div v-else-if="orders.length === 0" class="text-center py-20">
        <div class="w-32 h-32 mx-auto mb-8 flex items-center justify-center rounded-full bg-gray-100">
          <span class="text-6xl">📦</span>
        </div>
        <h2 class="text-2xl font-bold mb-4">У вас еще нет заказов</h2>
        <p class="text-gray-600 mb-8 max-w-md mx-auto">
          Оформите первый заказ из корзины, чтобы он появился здесь
        </p>
        <router-link to="/cart" class="btn-primary">Перейти в корзину</router-link>
      </div>

      <!-- Orders list -->
      <div v-else class="space-y-6">
        <!-- Filter tabs -->
        <div class="border-b border-gray-200">
          <nav class="flex space-x-8">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'py-4 px-1 text-sm font-medium border-b-2 transition-colors',
                activeTab === tab.id
                  ? 'border-black text-black'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.name }}
              <span class="ml-2 bg-gray-100 px-2 py-0.5 rounded-full text-xs">
                {{ tab.count }}
              </span>
            </button>
          </nav>
        </div>

        <!-- Orders grid -->
        <div class="grid gap-6">
          <OrderCard
            v-for="order in filteredOrders"
            :key="order.id"
            :order="order"
            @cancel-order="handleCancelOrder"
            @add-note="handleAddNote"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useOrdersStore } from '@/stores/orders'
import OrderCard from '@/components/orders/OrderCard.vue'
import { storeToRefs } from 'pinia'

const ordersStore = useOrdersStore()
const { orders, isLoading, error, pendingOrders, completedOrders, cancelledOrders } = storeToRefs(ordersStore)
const { fetchOrders } = ordersStore

const activeTab = ref<'all' | 'pending' | 'completed' | 'cancelled'>('all')

const tabs = computed(() => [
  { id: 'all', name: 'Все заказы', count: orders.value.length },
  { id: 'pending', name: 'В обработке', count: pendingOrders.value.length },
  { id: 'completed', name: 'Завершенные', count: completedOrders.value.length },
  { id: 'cancelled', name: 'Отмененные', count: cancelledOrders.value.length }
])

const filteredOrders = computed(() => {
  switch (activeTab.value) {
    case 'pending': return pendingOrders.value
    case 'completed': return completedOrders.value
    case 'cancelled': return cancelledOrders.value
    default: return orders.value
  }
})

const handleCancelOrder = async (orderId: number, reason: string) => {
  try {
    await ordersStore.cancelOrder(orderId, reason)
    alert('Заказ успешно отменен')
  } catch (err) {
    alert('Ошибка при отмене заказа')
  }
}

const handleAddNote = async (orderId: number, note: string) => {
  try {
    await ordersStore.addNote(orderId, note)
    alert('Заметка добавлена')
  } catch (err) {
    alert('Ошибка при добавлении заметки')
  }
}

onMounted(() => {
  fetchOrders()
})
</script>