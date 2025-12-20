<!-- src/components/books/BookCard.vue -->
<template>
  <article class="group relative flex flex-col h-full bg-white border border-gray-200 hover:border-gray-300 transition-all duration-300 card-hover">
    <!-- Бейдж скидки (если есть) -->
    <div 
      v-if="book.discount_percentage" 
      class="absolute top-4 left-4 z-10 bg-black text-white text-xs font-bold px-3 py-1 tracking-widest"
    >
      -{{ book.discount_percentage }}%
    </div>

    <!-- Изображение обложки - кликабельно -->
    <router-link :to="`/books/${book.slug}`" class="block relative aspect-[3/4] overflow-hidden bg-gradient-to-br from-gray-50 to-gray-100">
      <!-- Заглушка, если нет изображения -->
      <div v-if="!book.cover_image" class="w-full h-full flex items-center justify-center group-hover:scale-105 transition-transform duration-500">
        <span class="text-4xl text-gray-300">📖</span>
      </div>
      <img 
        v-else 
        :src="book.cover_image" 
        :alt="book.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
      >
    </router-link>

    <!-- Информация о книге -->
    <div class="flex flex-col flex-grow p-5">
      <!-- Автор -->
      <p class="text-sm text-gray-500 mb-1 truncate">
        {{ book.author_name }}
      </p>
      
      <!-- Название - тоже кликабельно -->
      <h3 class="font-bold text-lg mb-3 line-clamp-2 flex-grow group-hover:text-gray-700 transition-colors">
        <router-link :to="`/books/${book.slug}`" class="hover:underline">
          {{ book.title }}
        </router-link>
      </h3>

      <!-- Рейтинг -->
      <div class="flex items-center mb-4">
        <div class="flex text-gray-300">
          <svg v-for="n in 5" :key="n" class="w-4 h-4" :class="{'text-yellow-400': n <= Math.round(book.average_rating)}" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
        </div>
        <span class="text-xs text-gray-500 ml-2">{{ book.average_rating.toFixed(1) }}</span>
      </div>

      <!-- Цена и кнопка -->
      <div class="mt-auto flex items-center justify-between">
        <div>
          <div v-if="book.discount_price" class="flex items-baseline">
            <span class="text-2xl font-bold">{{ book.discount_price.toLocaleString() }} ₽</span>
            <span class="text-sm text-gray-400 line-through ml-2">{{ book.price.toLocaleString() }} ₽</span>
          </div>
          <div v-else>
            <span class="text-2xl font-bold">{{ book.current_price.toLocaleString() }} ₽</span>
          </div>
        </div>
        <button 
          class="btn-secondary !px-4 !py-2 text-sm"
          @click="addToCart"
          :disabled="!book.in_stock"
          :class="{'opacity-50 cursor-not-allowed': !book.in_stock}"
        >
          {{ book.in_stock ? '+ В корзину' : 'Нет в наличии' }}
        </button>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { Book } from '@/types'
import { useCartStore } from '@/stores/cart'

const props = defineProps<{
  book: Book
}>()

const cartStore = useCartStore()

const addToCart = () => {
  console.log('Нажата кнопка В корзину для книги:', props.book.title)
  cartStore.addItem(props.book, 1)
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Убираем стандартные стили ссылки для картинки */
.router-link {
  text-decoration: none;
  color: inherit;
}
</style>