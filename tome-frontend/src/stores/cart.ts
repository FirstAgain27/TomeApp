// src/stores/cart.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartAPI, type Cart, type CartItem } from '@/api/cart'

export const useCartStore = defineStore('cart', () => {
  const cart = ref<Cart | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const isOpen = ref(false) 

  const items = computed(() => cart.value?.items || [])
  
  const totalItems = computed(() => {
    if (!cart.value) return 0
    return cart.value.total_items || 0
  })

  const totalPrice = computed(() => {
    if (!cart.value) return 0
    return parseFloat(cart.value.total_price) || 0
  })

  const isEmpty = computed(() => items.value.length === 0)
  
  const groupedItems = computed(() => items.value)

  // ДОБАВИЛ методы для открытия/закрытия корзины
  const openCart = () => {
    isOpen.value = true
  }
  
  const closeCart = () => {
    isOpen.value = false
  }

  const fetchCart = async () => {
    if (!localStorage.getItem('access_token')) {
      cart.value = null
      return
    }
    
    isLoading.value = true
    error.value = null
    try {
      cart.value = await cartAPI.getCart()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Не удалось загрузить корзину'
      cart.value = null
    } finally {
      isLoading.value = false
    }
  }

  const loadFromLocalStorage = async () => {
    await fetchCart()
  }

  const addToCart = async (bookId: number, quantity: number = 1) => {
    isLoading.value = true
    error.value = null
    try {
      await cartAPI.addToCart(bookId, quantity)
      await fetchCart()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Не удалось добавить в корзину'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const removeItem = async (id: number) => {
    try {
      await cartAPI.removeFromCart(id)
      await fetchCart()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Не удалось удалить товар'
      throw err
    }
  }

  const updateQuantity = async (id: number, quantity: number) => {
    if (quantity < 1) {
      await removeItem(id)
      return
    }
    
    try {
      await cartAPI.updateCartItem(id, quantity)
      await fetchCart()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Не удалось обновить количество'
      throw err
    }
  }

  const clearCart = async () => {
    try {
      await cartAPI.clearCart()
      cart.value = null
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Не удалось очистить корзину'
      throw err
    }
  }

  return {
    // Состояние
    cart,
    isLoading,
    error,
    isOpen,
    
    // Геттеры
    items,
    totalItems,
    totalPrice,
    isEmpty,
    groupedItems,
    
    // Действия
    fetchCart,
    loadFromLocalStorage,
    addToCart,
    removeItem,
    updateQuantity,
    clearCart,
    openCart,
    closeCart 
  }
})