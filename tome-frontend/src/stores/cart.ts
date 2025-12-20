// src/stores/cart.ts
import { defineStore } from 'pinia'
import type { Book } from '@/types'

export interface CartItem {
  id: number
  book: Book
  quantity: number
  addedAt: string
}

interface CartState {
  items: CartItem[]
  isOpen: boolean
}

export const useCartStore = defineStore('cart', {
  state: (): CartState => ({
    items: [],
    isOpen: false
  }),

  getters: {
    // Количество товаров в корзине
    totalItems: (state) => {
      return state.items.reduce((total, item) => total + item.quantity, 0)
    },
    
    // Общая стоимость
    totalPrice: (state) => {
      return state.items.reduce((total, item) => {
        return total + (item.book.current_price * item.quantity)
      }, 0)
    },
    
    // Проверка на пустоту
    isEmpty: (state) => state.items.length === 0,
    
    // Сгруппированные товары (для отображения)
    groupedItems: (state) => state.items
  },

  actions: {
    // Добавить товар в корзину
    addItem(book: Book, quantity: number = 1) {
      console.log('Добавляем книгу в корзину:', book.title) // Для отладки
      
      const existingItem = this.items.find(item => item.book.id === book.id)
      
      if (existingItem) {
        existingItem.quantity += quantity
        console.log('Увеличили количество до:', existingItem.quantity)
      } else {
        this.items.push({
          id: Date.now(),
          book,
          quantity,
          addedAt: new Date().toISOString()
        })
        console.log('Добавили новую книгу в корзину')
      }
      
      // Показываем корзину при добавлении
      this.isOpen = true
      
      // Сохраняем в localStorage
      this.saveToLocalStorage()
      
      console.log('Товаров в корзине теперь:', this.totalItems)
    },

    // Удалить товар из корзины
    removeItem(itemId: number) {
      this.items = this.items.filter(item => item.id !== itemId)
      this.saveToLocalStorage()
    },

    // Изменить количество товара
    updateQuantity(itemId: number, quantity: number) {
      const item = this.items.find(item => item.id === itemId)
      if (item) {
        if (quantity <= 0) {
          this.removeItem(itemId)
        } else {
          item.quantity = quantity
        }
        this.saveToLocalStorage()
      }
    },

    // Очистить корзину
    clearCart() {
      this.items = []
      this.saveToLocalStorage()
    },

    // Переключить видимость корзины (для модального окна/сайдбара)
    toggleCart() {
      this.isOpen = !this.isOpen
    },

    // Открыть корзину
    openCart() {
      this.isOpen = true
    },

    // Закрыть корзину
    closeCart() {
      this.isOpen = false
    },

    // Сохранение в localStorage
    saveToLocalStorage() {
      localStorage.setItem('cart_items', JSON.stringify(this.items))
    },

    // Загрузка из localStorage
    loadFromLocalStorage() {
      const saved = localStorage.getItem('cart_items')
      if (saved) {
        try {
          this.items = JSON.parse(saved)
          console.log('Загружена корзина из localStorage:', this.items.length, 'товаров')
        } catch (e) {
          console.error('Failed to load cart from localStorage:', e)
          this.items = []
        }
      }
    }
  }
})