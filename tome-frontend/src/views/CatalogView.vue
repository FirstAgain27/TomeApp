<template>
  <div class="catalog-page pt-6 pb-16 bg-gray-50">
    <!-- Заголовок и фильтры -->
    <div class="catalog-header mx-auto mb-8 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-10">
          <h1 class="text-3xl font-bold mb-2">Книжный каталог</h1>
          <p class="text-gray-600">Найдите редкие и коллекционные издания</p>
        </div>

        <div class="filters-container">
          <div class="flex flex-wrap justify-center gap-4 mb-8">
            <!-- Все ваши фильтры остаются без изменений -->
            <div class="relative group" @mouseenter="showAuthorFilter = true" @mouseleave="showAuthorFilter = false">
              <button class="btn-secondary !px-4 !py-2 text-sm flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                Автор
                <svg class="w-4 h-4 transition-transform" :class="{'rotate-180': showAuthorFilter}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
              
              <div v-if="showAuthorFilter" class="absolute top-full left-0 mt-1 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-10 max-h-64 overflow-y-auto">
                <div class="p-2">
                  <input
                    v-model="authorSearch"
                    type="text"
                    placeholder="Поиск автора..."
                    class="input-field !py-1.5 !text-sm mb-2"
                    @input="filterAuthors"
                  />
                  <div class="space-y-1">
                    <button
                      class="w-full text-left px-3 py-2 text-sm hover:bg-gray-100 rounded"
                      :class="{'bg-gray-100 font-medium': !filters.author}"
                      @click="selectAuthor('')"
                    >
                      Все авторы
                    </button>
                    <button
                      v-for="author in filteredAuthors"
                      :key="author.id"
                      class="w-full text-left px-3 py-2 text-sm hover:bg-gray-100 rounded"
                      :class="{'bg-gray-100 font-medium': filters.author === author.id.toString()}"
                      @click="selectAuthor(author.id)"
                    >
                      {{ author.full_name }}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Категория фильтр -->
            <div class="relative group" @mouseenter="showCategoryFilter = true" @mouseleave="showCategoryFilter = false">
              <button class="btn-secondary !px-4 !py-2 text-sm flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                </svg>
                Категория
                <svg class="w-4 h-4 transition-transform" :class="{'rotate-180': showCategoryFilter}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
              
              <div v-if="showCategoryFilter" class="absolute top-full left-0 mt-1 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-10 max-h-64 overflow-y-auto">
                <div class="p-2">
                  <input
                    v-model="categorySearch"
                    type="text"
                    placeholder="Поиск категории..."
                    class="input-field !py-1.5 !text-sm mb-2"
                    @input="filterCategories"
                  />
                  <div class="space-y-1">
                    <button
                      class="w-full text-left px-3 py-2 text-sm hover:bg-gray-100 rounded"
                      :class="{'bg-gray-100 font-medium': !filters.category}"
                      @click="selectCategory('')"
                    >
                      Все категории
                    </button>
                    <button
                      v-for="category in filteredCategories"
                      :key="category.id"
                      class="w-full text-left px-3 py-2 text-sm hover:bg-gray-100 rounded"
                      :class="{'bg-gray-100 font-medium': filters.category === category.id.toString()}"
                      @click="selectCategory(category.id)"
                    >
                      {{ category.name }}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Сортировка фильтр -->
            <div class="relative group" @mouseenter="showSortFilter = true" @mouseleave="showSortFilter = false">
              <button class="btn-secondary !px-4 !py-2 text-sm flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4"/>
                </svg>
                Сортировка
                <svg class="w-4 h-4 transition-transform" :class="{'rotate-180': showSortFilter}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
              
              <div v-if="showSortFilter" class="absolute top-full left-0 mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                <div class="p-2 space-y-1">
                  <button
                    v-for="option in sortOptions"
                    :key="option.value"
                    class="w-full text-left px-3 py-2 text-sm hover:bg-gray-100 rounded"
                    :class="{'bg-gray-100 font-medium': filters.ordering === option.value}"
                    @click="selectSort(option.value)"
                  >
                    {{ option.label }}
                  </button>
                </div>
              </div>
            </div>

            <button 
              v-if="hasActiveFilters"
              @click="resetFilters"
              class="btn-secondary !px-4 !py-2 text-sm flex items-center gap-2 text-gray-600 hover:text-black"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              Сбросить
            </button>
          </div>
        </div>

        <div v-if="hasActiveFilters" class="flex flex-wrap justify-center gap-2 mb-6">
          <div 
            v-if="selectedAuthorName"
            class="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 rounded-full text-sm"
          >
            <span>Автор: {{ selectedAuthorName }}</span>
            <button @click="selectAuthor('')" class="text-gray-500 hover:text-black">
              ×
            </button>
          </div>
          
          <div 
            v-if="selectedCategoryName"
            class="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 rounded-full text-sm"
          >
            <span>Категория: {{ selectedCategoryName }}</span>
            <button @click="selectCategory('')" class="text-gray-500 hover:text-black">
              ×
            </button>
          </div>
          
          <div 
            v-if="selectedSortLabel"
            class="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 rounded-full text-sm"
          >
            <span>Сортировка: {{ selectedSortLabel }}</span>
            <button @click="selectSort('')" class="text-gray-500 hover:text-black">
              ×
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Сетка книг -->
    <div class="books-container mx-auto px-4">
      <div class="max-w-6xl mx-auto">
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-black"></div>
          <p class="mt-3 text-gray-600 text-sm">Загружаем каталог...</p>
        </div>

        <div v-else-if="books.length === 0" class="text-center py-12">
          <div class="w-20 h-20 mx-auto mb-4 flex items-center justify-center rounded-full bg-gray-100">
            <span class="text-4xl">🔍</span>
          </div>
          <h2 class="text-xl font-bold mb-2">Книги не найдены</h2>
          <p class="text-gray-600 text-sm max-w-md mx-auto">
            Попробуйте изменить параметры фильтрации
          </p>
        </div>

        <div v-else class="books-grid">
          <BookCard v-for="book in books.slice(0, 12)" :key="book.id" :book="book" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import BookCard from '@/components/books/BookCard.vue'
import { catalogAPI, type Book, type Author, type Category } from '@/api/catalog'

const loading = ref(true)
const books = ref<Book[]>([])
const authors = ref<Author[]>([])
const categories = ref<Category[]>([])
const filteredAuthors = ref<Author[]>([])
const filteredCategories = ref<Category[]>([])
const showAuthorFilter = ref(false)
const showCategoryFilter = ref(false)
const showSortFilter = ref(false)
const authorSearch = ref('')
const categorySearch = ref('')

const filters = ref({
  author: '',
  category: '',
  ordering: ''
})

const sortOptions = [
  { value: '', label: 'По умолчанию' },
  { value: 'price', label: 'По возрастанию цены' },
  { value: '-price', label: 'По убыванию цены' },
  { value: '-created_at', label: 'Сначала новые' },
  { value: 'title', label: 'По названию (А-Я)' },
  { value: '-average_rating', label: 'По рейтингу' }
]

const hasActiveFilters = computed(() => {
  return !!filters.value.author || !!filters.value.category || !!filters.value.ordering
})

const selectedAuthorName = computed(() => {
  if (!filters.value.author) return ''
  const author = authors.value.find(a => a.id.toString() === filters.value.author)
  return author?.full_name || ''
})

const selectedCategoryName = computed(() => {
  if (!filters.value.category) return ''
  const category = categories.value.find(c => c.id.toString() === filters.value.category)
  return category?.name || ''
})

const selectedSortLabel = computed(() => {
  if (!filters.value.ordering) return ''
  const option = sortOptions.find(o => o.value === filters.value.ordering)
  return option?.label || ''
})

onMounted(async () => {
  await Promise.all([
    loadBooks(),
    loadAuthors(),
    loadCategories()
  ])
  filteredAuthors.value = authors.value
  filteredCategories.value = categories.value
})

const loadBooks = async () => {
  loading.value = true
  try {
    const params: any = {}
    
    if (filters.value.author) {
      params.author = filters.value.author
    }
    
    if (filters.value.category) {
      params.categories = filters.value.category
    }
    
    if (filters.value.ordering) {
      params.ordering = filters.value.ordering
    }
    
    const data = await catalogAPI.getBooks(params)
    
    let allBooks: Book[] = []
    if (data && typeof data === 'object' && 'results' in data) {
      allBooks = data.results || []
    } else if (Array.isArray(data)) {
      allBooks = data
    }
    
    books.value = allBooks
    
  } catch (error) {
    console.error('Ошибка загрузки книг:', error)
    books.value = []
  } finally {
    loading.value = false
  }
}

const loadAuthors = async () => {
  try {
    const data = await catalogAPI.getAuthors()
    authors.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Ошибка загрузки авторов:', error)
    authors.value = []
  }
}

const loadCategories = async () => {
  try {
    const data = await catalogAPI.getCategories()
    categories.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Ошибка загрузки категорий:', error)
    categories.value = []
  }
}

const selectAuthor = (authorId: number | string) => {
  filters.value.author = authorId.toString()
  showAuthorFilter.value = false
  authorSearch.value = ''
  filteredAuthors.value = authors.value
  loadBooks()
}

const selectCategory = (categoryId: number | string) => {
  filters.value.category = categoryId.toString()
  showCategoryFilter.value = false
  categorySearch.value = ''
  filteredCategories.value = categories.value
  loadBooks()
}

const selectSort = (sortValue: string) => {
  filters.value.ordering = sortValue
  showSortFilter.value = false
  loadBooks()
}

const filterAuthors = () => {
  if (!authorSearch.value.trim()) {
    filteredAuthors.value = authors.value
    return
  }
  
  const search = authorSearch.value.toLowerCase()
  filteredAuthors.value = authors.value.filter(author =>
    author.full_name.toLowerCase().includes(search)
  )
}

const filterCategories = () => {
  if (!categorySearch.value.trim()) {
    filteredCategories.value = categories.value
    return
  }
  
  const search = categorySearch.value.toLowerCase()
  filteredCategories.value = categories.value.filter(category =>
    category.name.toLowerCase().includes(search)
  )
}

const resetFilters = () => {
  filters.value = {
    author: '',
    category: '',
    ordering: ''
  }
  authorSearch.value = ''
  categorySearch.value = ''
  filteredAuthors.value = authors.value
  filteredCategories.value = categories.value
  loadBooks()
}
</script>

<style scoped>
.catalog-page {
  min-height: calc(100vh - 64px);
}

.books-container {
  width: 100%;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
  width: 100%;
}

@media (min-width: 640px) {
  .books-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .books-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1280px) {
  .books-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}
</style>