<!-- src/views/CatalogView.vue -->
<template>
  <div class="pt-8 pb-20">
    <!-- Заголовок -->
    <div class="container mx-auto px-6 mb-10">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-10">
        <div>
          <h1 class="text-4xl font-bold mb-2">Каталог книг</h1>
          <p class="text-gray-600">Кураторская подборка эксклюзивных изданий</p>
        </div>
      </div>
    </div>

    <!-- Сетка книг -->
    <div class="container mx-auto px-6">
      <!-- Загрузка -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-black"></div>
        <p class="mt-4 text-gray-600">Загружаем каталог...</p>
      </div>

      <!-- Нет книг -->
      <div v-else-if="books.length === 0" class="text-center py-20">
        <div class="w-32 h-32 mx-auto mb-8 flex items-center justify-center rounded-full bg-gray-100">
          <span class="text-6xl">📚</span>
        </div>
        <h2 class="text-2xl font-bold mb-4">Каталог пуст</h2>
        <p class="text-gray-600 max-w-md mx-auto">
          В базе данных пока нет книг. Добавьте книги через админ-панель Django.
        </p>
      </div>

      <!-- Книги -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        <BookCard 
          v-for="book in books" 
          :key="book.id" 
          :book="book"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BookCard from '@/components/books/BookCard.vue'
import { catalogAPI } from '@/api/catalog'

interface Book {
  id: number
  title: string
  slug: string
  author_name: string
  cover_image: string | null
  current_price: string | number
  price: string | number
  discount_price: string | number | null
  average_rating: number | null
  stock_quantity: number
  in_stock: boolean
  discount_percentage: number
}

const loading = ref(true)
const books = ref<Book[]>([])

onMounted(async () => {
  await loadBooks()
})

const loadBooks = async () => {
  loading.value = true
  try {
    console.log('Загрузка книг...')
    const data = await catalogAPI.getBooks()
    console.log('Ответ от API:', data)
    
    // API возвращает массив напрямую
    books.value = Array.isArray(data) ? data : []
    
    console.log('Загружено книг:', books.value.length)
    console.log('Первая книга:', books.value[0])
  } catch (error) {
    console.error('Ошибка загрузки книг:', error)
    books.value = []
  } finally {
    loading.value = false
  }
}
</script>