<!-- src/components/cart/CartDrawer.vue -->
<template>
  <!-- Overlay -->
  <div 
    v-if="isOpen"
    class="fixed inset-0 bg-black bg-opacity-50 z-50 transition-opacity duration-300"
    @click="closeCart"
  ></div>

  <!-- Drawer -->
  <div 
    class="fixed top-0 right-0 h-full w-full md:w-96 bg-white z-50 transform transition-transform duration-300 shadow-2xl"
    :class="isOpen ? 'translate-x-0' : 'translate-x-full'"
  >
    <!-- Header -->
    <div class="flex items-center justify-between p-6 border-b border-gray-200">
      <h2 class="text-xl font-bold">Корзина покупок</h2>
      <button @click="closeCart" class="p-2 hover:bg-gray-100 rounded-full">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Content -->
    <div class="flex flex-col h-full">
      <!-- Items -->
      <div class="flex-grow overflow-y-auto p-6" v-if="!isEmpty">
        <div class="space-y-6">
          <div 
            v-for="item in groupedItems" 
            :key="item.id"
            class="flex gap-4 pb-6 border-b border-gray-100 last:border-0"
          >
            <!-- Book image -->
            <router-link 
              :to="`/books/${item.book.slug}`"
              class="flex-shrink-0 w-20 h-28 bg-gray-100 overflow-hidden"
              @click="closeCart"
            >
              <div v-if="!item.book.cover_image" class="w-full h-full flex items-center justify-center">
                <span class="text-2xl text-gray-300">📖</span>
              </div>
              <img 
                v-else 
                :src="item.book.cover_image" 
                :alt="item.book.title"
                class="w-full h-full object-cover"
              >
            </router-link>

            <!-- Book info -->
            <div class="flex-grow">
              <div class="flex justify-between">
                <router-link 
                  :to="`/books/${item.book.slug}`" 
                  class="font-medium hover:underline line-clamp-2"
                  @click="closeCart"
                >
                  {{ item.book.title }}
                </router-link>
                <button 
                  @click="removeItem(item.id)"
                  class="text-gray-400 hover:text-black ml-2"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
              
              <p class="text-sm text-gray-500 mt-1">{{ item.book.author_name }}</p>
              
              <div class="flex items-center justify-between mt-4">
                <!-- Quantity selector -->
                <div class="flex items-center border border-gray-300">
                  <button 
                    @click="updateQuantity(item.id, item.quantity - 1)"
                    class="px-3 py-1 hover:bg-gray-100"
                    :disabled="item.quantity <= 1"
                  >
                    –
                  </button>
                  <span class="px-4 py-1 min-w-[40px] text-center">{{ item.quantity }}</span>
                  <button 
                    @click="updateQuantity(item.id, item.quantity + 1)"
                    class="px-3 py-1 hover:bg-gray-100"
                  >
                    +
                  </button>
                </div>
                
                <!-- Price -->
                <div class="text-right">
                  <div class="font-bold">{{ (item.book.current_price * item.quantity).toLocaleString() }} ₽</div>
                  <div class="text-sm text-gray-500">{{ item.book.current_price.toLocaleString() }} ₽/шт</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="flex-grow flex flex-col items-center justify-center p-6 text-center">
        <div class="w-24 h-24 mb-6 flex items-center justify-center rounded-full bg-gray-100">
          <span class="text-4xl">🛒</span>
        </div>
        <h3 class="text-xl font-bold mb-2">Корзина пуста</h3>
        <p class="text-gray-600 mb-8">Добавьте книги из каталога</p>
        <button @click="closeCart" class="btn-primary">Продолжить покупки</button>
      </div>

      <!-- Footer -->
      <div class="border-t border-gray-200 p-6 space-y-4" v-if="!isEmpty">
        <!-- Summary -->
        <div class="space-y-2">
          <div class="flex justify-between">
            <span class="text-gray-600">Товары ({{ totalItems }})</span>
            <span>{{ totalPrice.toLocaleString() }} ₽</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Доставка</span>
            <span class="text-green-600">Бесплатно</span>
          </div>
          <div class="flex justify-between text-lg font-bold pt-2 border-t border-gray-200">
            <span>Итого</span>
            <span>{{ totalPrice.toLocaleString() }} ₽</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="space-y-3">
          <router-link 
            to="/cart" 
            class="btn-primary block text-center"
            @click="closeCart"
          >
            Перейти к оформлению
          </router-link>
          <button 
            @click="clearCart"
            class="text-sm text-gray-500 hover:text-black underline block mx-auto"
          >
            Очистить корзину
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'

const cartStore = useCartStore()

const {
  isOpen,
  items,
  totalItems,
  totalPrice,
  isEmpty,
  groupedItems
} = storeToRefs(cartStore)

const { 
  closeCart, 
  removeItem, 
  updateQuantity, 
  clearCart 
} = cartStore
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>