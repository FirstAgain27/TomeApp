// src/stores/orders.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import orderApi, { type Order, type CreateOrderData, type CancelOrderData } from '@/api/orders'

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref<Order[]>([])
  const currentOrder = ref<Order | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Вычисляемые свойства
  const pendingOrders = computed(() => 
    orders.value.filter(order => order.status === 'PENDING')
  )
  
  const completedOrders = computed(() => 
    orders.value.filter(order => ['DELIVERED', 'COMPLETED'].includes(order.status))
  )
  
  const cancelledOrders = computed(() => 
    orders.value.filter(order => order.status === 'CANCELLED')
  )

  // Действия
  const fetchOrders = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await orderApi.getOrders()
      orders.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Ошибка при загрузке заказов'
      console.error('Error fetching orders:', err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchOrder = async (id: number) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await orderApi.getOrder(id)
      currentOrder.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Ошибка при загрузке заказа'
      console.error('Error fetching order:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createOrder = async (data: CreateOrderData) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await orderApi.createOrder(data)
      orders.value.unshift(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Ошибка при создании заказа'
      console.error('Error creating order:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const cancelOrder = async (id: number, reason: string) => {
    isLoading.value = true
    error.value = null
    try {
      await orderApi.cancelOrder(id, { reason })
      
      // Обновляем статус в локальном списке
      const orderIndex = orders.value.findIndex(order => order.id === id)
      if (orderIndex !== -1) {
        orders.value[orderIndex].status = 'CANCELLED'
      }
      
      // Обновляем текущий заказ если он открыт
      if (currentOrder.value && currentOrder.value.id === id) {
        currentOrder.value.status = 'CANCELLED'
      }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Ошибка при отмене заказа'
      console.error('Error cancelling order:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const addNote = async (id: number, note: string) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await orderApi.addNote(id, { note })
      
      // Обновляем заметку в локальном списке
      const orderIndex = orders.value.findIndex(order => order.id === id)
      if (orderIndex !== -1) {
        orders.value[orderIndex].note = note
      }
      
      // Обновляем текущий заказ если он открыт
      if (currentOrder.value && currentOrder.value.id === id) {
        currentOrder.value.note = note
      }
      
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Ошибка при добавлении заметки'
      console.error('Error adding note:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    // Состояние
    orders,
    currentOrder,
    isLoading,
    error,
    
    // Геттеры
    pendingOrders,
    completedOrders,
    cancelledOrders,
    
    // Действия
    fetchOrders,
    fetchOrder,
    createOrder,
    cancelOrder,
    addNote
  }
})