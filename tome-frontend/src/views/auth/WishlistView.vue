<!-- src/views/auth/WishlistView.vue -->
<template>
  <div class="pt-8 pb-20">
    <div class="container mx-auto px-6">
      <!-- Хлебные крошки -->
      <nav class="flex text-sm mb-10">
        <router-link to="/" class="text-gray-500 hover:text-black">Главная</router-link>
        <span class="mx-2">/</span>
        <router-link to="/profile" class="text-gray-500 hover:text-black">Профиль</router-link>
        <span class="mx-2">/</span>
        <span class="text-black">Избранное</span>
      </nav>

      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold">Избранное</h1>
        <button 
          v-if="wishlist.length > 0"
          @click="clearWishlist"
          class="text-sm text-gray-500 hover:text-black underline"
        >
          Очистить избранное
        </button>
      </div>

      <div v-if="wishlist.length === 0" class="text-center py-20 border border-gray-200">
        <div class="w-24 h-24 mx-auto mb-6 flex items-center justify-center rounded-full bg-gray-100">
          <span class="text-4xl">❤️</span>
        </div>
        <h2 class="text-2xl font-bold mb-4">Избранное пусто</h2>
        <p class="text-gray-600 mb-8">Добавляйте книги, чтобы вернуться к ним позже</p>
        <router-link to="/catalog" class="btn-primary">Перейти в каталог</router-link>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        <!-- Карточки книг из избранного -->
        <div 
          v-for="book in wishlist" 
          :key="book.id"
          class="border border-gray-200 p-4 group relative"
        >
          <button 
            @click="removeFromWishlist(book.id)"
            class="absolute top-4 right-4 text-gray-400 hover:text-black z-10"
            title="Удалить из избранного"
          >
            ❌
          </button>
          
          <router-link :to="`/books/${book.slug}`" class="block">
            <div class="aspect-[3/4] bg-gray-100 mb-4 flex items-center justify-center">
              <span class="text-3xl text-gray-300">📖</span>
            </div>
            <h3 class="font-bold mb-2 line-clamp-2">{{ book.title }}</h3>
            <p class="text-sm text-gray-600 mb-2">{{ book.author_name }}</p>
            <div class="font-bold">{{ book.current_price.toLocaleString() }} ₽</div>
          </router-link>
          
          <button 
            @click="addToCart(book)"
            class="btn-secondary w-full mt-4"
          >
            В корзину
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import type { Book } from '@/types'

const cartStore = useCartStore()

// Моковые данные для избранного
const wishlist = ref<Book[]>([
  {
    id: 1,
    title: 'Мастер и Маргарита',
    slug: 'master-i-margarita',
    author_name: 'Михаил Булгаков',
    cover_image: '',
    current_price: 5600,
    price: 5600,
    discount_price: null,
    average_rating: 4.8,
    description: '',
    isbn: '',
    stock_quantity: 5,
    in_stock: true,
    publisher: '',
    publication_date: '',
    pages: 0,
    language: '',
    cover_type: '',
    discount_percentage: 0,
    created_at: '',
    updated_at: ''
  },
  {
    id: 2,
    title: '1984',
    slug: '1984',
    author_name: 'Джордж Оруэлл',
    cover_image: '',
    current_price: 3200,
    price: 4000,
    discount_price: 3200,
    average_rating: 4.6,
    description: '',
    isbn: '',
    stock_quantity: 10,
    in_stock: true,
    publisher: '',
    publication_date: '',
    pages: 0,
    language: '',
    cover_type: '',
    discount_percentage: 20,
    created_at: '',
    updated_at: ''
  }
])

const removeFromWishlist = (bookId: number) => {
  wishlist.value = wishlist.value.filter(book => book.id !== bookId)
}

const clearWishlist = () => {
  if (confirm('Очистить избранное?')) {
    wishlist.value = []
  }
}

const addToCart = (book: Book) => {
  cartStore.addItem(book, 1)
}
</script>