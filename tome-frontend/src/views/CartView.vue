<!-- src/views/CartView.vue -->
<template>
  <div class="pt-8 pb-20">
    <div class="container mx-auto px-6">
      <!-- Header -->
      <div class="mb-10">
        <h1 class="text-4xl font-bold mb-4">Корзина покупок</h1>
        <div class="flex items-center text-sm text-gray-600">
          <router-link to="/catalog" class="hover:text-black">← Вернуться к покупкам</router-link>
          <span class="mx-3">•</span>
          <span>Товаров в корзине: {{ totalItems }}</span>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="isEmpty" class="text-center py-20">
        <div class="w-32 h-32 mx-auto mb-8 flex items-center justify-center rounded-full bg-gray-100">
          <span class="text-6xl">🛒</span>
        </div>
        <h2 class="text-2xl font-bold mb-4">Корзина пуста</h2>
        <p class="text-gray-600 mb-8 max-w-md mx-auto">
          Добавьте книги из каталога, чтобы продолжить покупки
        </p>
        <router-link to="/catalog" class="btn-primary">Перейти в каталог</router-link>
      </div>

      <!-- Cart with items -->
      <div v-else class="flex flex-col lg:flex-row gap-12">
        <!-- Left column: Items -->
        <div class="lg:w-2/3">
          <!-- Items list -->
          <div class="space-y-6">
            <div 
              v-for="item in groupedItems" 
              :key="item.id"
              class="flex gap-6 p-6 border border-gray-200"
            >
              <!-- Book image -->
              <router-link 
                :to="`/books/${item.book.slug}`"
                class="flex-shrink-0 w-32 h-48 bg-gray-100 overflow-hidden"
              >
                <div v-if="!item.book.cover_image" class="w-full h-full flex items-center justify-center">
                  <span class="text-3xl text-gray-300">📖</span>
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
                <div class="flex justify-between items-start">
                  <div>
                    <router-link 
                      :to="`/books/${item.book.slug}`" 
                      class="text-xl font-bold hover:underline"
                    >
                      {{ item.book.title }}
                    </router-link>
                    <p class="text-gray-600 mt-1">{{ item.book.author_name }}</p>
                    
                    <!-- Book details -->
                    <div class="mt-4 text-sm text-gray-500 space-y-1">
                      <div v-if="item.book.publisher">Издательство: {{ item.book.publisher }}</div>
                      <div v-if="item.book.publication_date">Год издания: {{ item.book.publication_date }}</div>
                      <div v-if="item.book.pages">Страниц: {{ item.book.pages }}</div>
                    </div>
                  </div>
                  
                  <!-- Remove button -->
                  <button 
                    @click="removeItem(item.id)"
                    class="text-gray-400 hover:text-black"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>

                <!-- Quantity and price -->
                <div class="flex items-center justify-between mt-8">
                  <!-- Quantity selector -->
                  <div class="flex items-center">
                    <span class="text-sm text-gray-600 mr-4">Количество:</span>
                    <div class="flex items-center border border-gray-300">
                      <button 
                        @click="updateQuantity(item.id, item.quantity - 1)"
                        class="px-4 py-2 hover:bg-gray-100"
                        :disabled="item.quantity <= 1"
                      >
                        –
                      </button>
                      <span class="px-6 py-2 min-w-[60px] text-center">{{ item.quantity }}</span>
                      <button 
                        @click="updateQuantity(item.id, item.quantity + 1)"
                        class="px-4 py-2 hover:bg-gray-100"
                      >
                        +
                      </button>
                    </div>
                  </div>
                  
                  <!-- Price -->
                  <div class="text-right">
                    <div class="text-2xl font-bold">{{ (item.book.current_price * item.quantity).toLocaleString() }} ₽</div>
                    <div class="text-sm text-gray-500">{{ item.book.current_price.toLocaleString() }} ₽/шт</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Clear cart button -->
          <div class="mt-8 text-right">
            <button 
              @click="clearCart"
              class="text-sm text-gray-500 hover:text-black underline"
            >
              Очистить корзину
            </button>
          </div>
        </div>

        <!-- Right column: Order summary -->
        <div class="lg:w-1/3">
          <div class="border border-gray-200 p-6 sticky top-24">
            <h2 class="text-2xl font-bold mb-6">Ваш заказ</h2>
            
            <!-- Summary -->
            <div class="space-y-4 mb-8">
              <div class="flex justify-between">
                <span class="text-gray-600">Товары ({{ totalItems }})</span>
                <span>{{ totalPrice.toLocaleString() }} ₽</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Доставка</span>
                <span class="text-green-600 font-medium">Бесплатно</span>
              </div>
              <div class="flex justify-between pt-4 border-t border-gray-200 text-lg font-bold">
                <span>Итого</span>
                <span>{{ totalPrice.toLocaleString() }} ₽</span>
              </div>
            </div>

            <!-- Promo code -->
            <div class="mb-8">
              <label class="block text-sm font-medium mb-2">Промокод</label>
              <div class="flex gap-2">
                <input 
                  type="text" 
                  placeholder="Введите промокод"
                  class="input-field flex-grow"
                  v-model="promoCode"
                >
                <button class="btn-secondary whitespace-nowrap">Применить</button>
              </div>
            </div>

            <!-- Checkout button -->
            <button class="btn-primary w-full text-lg py-4 mb-4">
              Перейти к оформлению
            </button>
            
            <!-- Additional info -->
            <div class="text-sm text-gray-600 space-y-3">
              <div class="flex items-start">
                <svg class="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Бесплатная доставка по Москве от 3 000 ₽</span>
              </div>
              <div class="flex items-start">
                <svg class="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Возврат в течение 14 дней</span>
              </div>
              <div class="flex items-start">
                <svg class="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Безопасная оплата</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'

const cartStore = useCartStore()
const promoCode = ref('')

const {
  items,
  totalItems,
  totalPrice,
  isEmpty,
  groupedItems
} = storeToRefs(cartStore)

const { removeItem, updateQuantity, clearCart } = cartStore

onMounted(() => {
  // Загружаем корзину из localStorage
  cartStore.loadFromLocalStorage()
})
</script>