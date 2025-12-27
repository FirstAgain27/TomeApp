<!-- src/views/CatalogView.vue -->
<template>
  <div class="pt-6 pb-16">
    <!-- Заголовок -->
    <div class="container mx-auto px-4 mb-8">
      <div class="text-center">
        <h1 class="text-3xl font-bold mb-2">Каталог книг</h1>
        <p class="text-gray-600 text-sm"></p>
      </div>
    </div>

    <!-- Сетка книг -->
    <div class="container mx-auto px-4">
      <!-- Загрузка -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-black"></div>
        <p class="mt-3 text-gray-600 text-sm">Загружаем каталог...</p>
      </div>

      <!-- Книги 4 в ряд -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
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
    const data = await catalogAPI.getBooks()
    
    // Получаем книги (массив или results)
    let allBooks: Book[] = []
    if (data && typeof data === 'object' && 'results' in data) {
      allBooks = data.results || []
    } else if (Array.isArray(data)) {
      allBooks = data
    }
    
    // Ограничиваем 12 книгами
    books.value = allBooks.slice(0, 12)
    
  } catch (error) {
    console.error('Ошибка загрузки книг:', error)
    books.value = []
  } finally {
    loading.value = false
  }
}
</script>