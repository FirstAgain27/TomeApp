<!-- src/views/CatalogView.vue -->
<template>
  <div class="pt-8 pb-20">
    <!-- Заголовок и фильтры -->
    <div class="container mx-auto px-6 mb-10">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-10">
        <div>
          <h1 class="text-4xl font-bold mb-2">Каталог книг</h1>
          <p class="text-gray-600">Кураторская подборка эксклюзивных изданий</p>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-4">
          <!-- Выбор сортировки -->
          <select class="input-field !py-2.5 !text-sm w-full sm:w-auto">
            <option>Сначала новые</option>
            <option>По популярности</option>
            <option>По возрастанию цены</option>
            <option>По убыванию цены</option>
          </select>
          
          <!-- Кнопка фильтров (для мобильных) -->
          <button class="btn-secondary !px-4 !py-2.5 text-sm flex items-center justify-center sm:hidden">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
            </svg>
            Фильтры
          </button>
        </div>
      </div>

      <!-- Панель фильтров (десктоп) -->
      <div class="hidden lg:block border-t border-b border-gray-200 py-6">
        <div class="flex flex-wrap gap-8 items-center">
          <div>
            <span class="text-sm font-medium mr-4">Категории:</span>
            <div class="inline-flex flex-wrap gap-2">
              <button class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors">Все</button>
              <button class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors">Художественная</button>
              <button class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors">Фантастика</button>
              <button class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors">Философия</button>
              <button class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors">Архивные</button>
            </div>
          </div>
          
          <div>
            <span class="text-sm font-medium mr-4">Цена:</span>
            <div class="inline-flex items-center gap-4">
              <input type="number" placeholder="от 0" class="input-field !py-1.5 !w-24 !text-sm">
              <span class="text-gray-400">—</span>
              <input type="number" placeholder="до 100 000" class="input-field !py-1.5 !w-24 !text-sm">
              <button class="text-sm underline hover:no-underline">Применить</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Сетка книг -->
    <div class="container mx-auto px-6">
      <!-- Состояние загрузки (пока используем мок-данные) -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-black"></div>
        <p class="mt-4 text-gray-600">Загружаем каталог...</p>
      </div>

      <!-- Сетка книг -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        <BookCard 
          v-for="book in books" 
          :key="book.id" 
          :book="book"
          @quick-view="handleQuickView"
          @add-to-cart="handleAddToCart"
        />
      </div>

      <!-- Пагинация -->
      <div v-if="!loading" class="flex justify-center mt-20">
        <nav class="flex items-center space-x-2">
          <button class="w-10 h-10 flex items-center justify-center border border-gray-300 hover:border-black disabled:opacity-30" disabled>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          
          <button class="w-10 h-10 flex items-center justify-center border border-black bg-black text-white">1</button>
          <button class="w-10 h-10 flex items-center justify-center border border-gray-300 hover:border-black">2</button>
          <button class="w-10 h-10 flex items-center justify-center border border-gray-300 hover:border-black">3</button>
          
          <button class="w-10 h-10 flex items-center justify-center border border-gray-300 hover:border-black">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BookCard from '@/components/books/BookCard.vue'
import type { Book } from '@/types'

const loading = ref(true)
const books = ref<Book[]>([])

// Временные мок-данные (потом заменим на запрос к API)
const mockBooks: Book[] = [
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
  },
  {
    id: 3,
    title: 'Маленький принц',
    slug: 'malenkiy-prints',
    author_name: 'Антуан де Сент-Экзюпери',
    cover_image: '',
    current_price: 2800,
    price: 2800,
    discount_price: null,
    average_rating: 4.9,
    description: '',
    isbn: '',
    stock_quantity: 0,
    in_stock: false,
    publisher: '',
    publication_date: '',
    pages: 0,
    language: '',
    cover_type: '',
    discount_percentage: 0,
    created_at: '',
    updated_at: ''
  },
  // Добавь ещё книг для теста...
]

onMounted(() => {
  // Имитация загрузки данных
  setTimeout(() => {
    books.value = [...mockBooks, ...mockBooks, ...mockBooks, ...mockBooks] // 12 книг для сетки
    loading.value = false
  }, 800)
})

const handleQuickView = (book: Book) => {
  console.log('Быстрый просмотр:', book)
  // TODO: Открыть модальное окно
}

const handleAddToCart = (book: Book) => {
  console.log('Добавить в корзину:', book)
  // TODO: Добавить в корзину
}
</script>
