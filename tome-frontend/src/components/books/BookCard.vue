<!-- src/components/books/BookCard.vue -->
<template>
  <article class="group relative flex flex-col h-full bg-white border border-gray-200 hover:border-gray-300 transition-all duration-200 rounded-lg overflow-hidden max-w-[280px] mx-auto">
    <!-- Бейдж скидки -->
    <div 
      v-if="book.discount_percentage && book.discount_percentage > 0" 
      class="absolute top-2 left-2 z-10 bg-black text-white text-xs font-bold px-2 py-1 tracking-tight"
    >
      -{{ book.discount_percentage }}%
    </div>

    <!-- Изображение -->
    <router-link :to="`/books/${book.slug}`" class="block relative aspect-[3/4] overflow-hidden bg-gradient-to-br from-gray-50 to-gray-100">
      <div v-if="!book.cover_image" class="w-full h-full flex items-center justify-center">
        <span class="text-3xl text-gray-300">📖</span>
      </div>
      <img 
        v-else 
        :src="book.cover_image" 
        :alt="book.title"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
      >
    </router-link>

    <!-- Информация -->
    <div class="flex flex-col flex-grow p-3">
      <!-- Автор -->
      <p class="text-xs text-gray-500 mb-1 truncate">
        {{ book.author_name }}
      </p>
      
      <!-- Название -->
      <h3 class="font-bold text-sm mb-2 line-clamp-2 flex-grow leading-tight">
        <router-link :to="`/books/${book.slug}`" class="hover:underline">
          {{ book.title }}
        </router-link>
      </h3>

      <!-- Рейтинг -->
      <div class="flex items-center mb-3">
        <div class="flex">
          <svg v-for="n in 5" :key="n" class="w-3 h-3" :class="{'text-yellow-400': n <= Math.round(book.average_rating || 0), 'text-gray-300': n > Math.round(book.average_rating || 0)}" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
        </div>
        <span class="text-xs text-gray-500 ml-1">{{ (book.average_rating || 0).toFixed(1) }}</span>
      </div>

      <!-- Цена и кнопка -->
      <div class="mt-auto flex items-center justify-between">
        <div>
          <div v-if="book.discount_price && parseFloat(book.discount_price as string) > 0" class="flex items-baseline">
            <span class="text-lg font-bold">{{ formatPrice(book.discount_price) }}</span>
            <span class="text-xs text-gray-400 line-through ml-1">{{ formatPrice(book.price) }}</span>
          </div>
          <div v-else>
            <span class="text-lg font-bold">{{ formatPrice(book.current_price) }}</span>
          </div>
        </div>
        <button 
          class="btn-secondary !px-3 !py-1.5 text-xs"
          @click="addToCart"
          :disabled="!book.in_stock"
          :class="{'opacity-50 cursor-not-allowed': !book.in_stock}"
        >
          {{ book.in_stock ? '+ Корзина' : 'Нет' }}
        </button>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const props = defineProps<{
  book: any
}>()

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()
const isLoading = ref(false)

const formatPrice = (price: number | string) => {
  const num = typeof price === 'string' ? parseFloat(price) : price
  return num.toLocaleString('ru-RU') + ' ₽'
}

const addToCart = async () => {
  if (!props.book.in_stock) {
    alert('Товара нет в наличии')
    return
  }
  
  if (!authStore.isAuthenticated) {
    if (confirm('Чтобы добавить товар в корзину, нужно войти в аккаунт. Перейти на страницу входа?')) {
      router.push('/login')
    }
    return
  }
  
  isLoading.value = true
  try {
    await cartStore.addToCart(props.book.id, 1)
    console.log('Товар добавлен в корзину:', props.book.title)
  } catch (error: any) {
    console.error('Ошибка при добавлении в корзину:', error)
    alert(error.message || 'Не удалось добавить товар в корзину')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>