<!-- src/views/BookDetailView.vue -->
<template>
  <div v-if="loading" class="pt-20 pb-20 text-center">
    <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-black"></div>
    <p class="mt-4 text-gray-600">Загружаем информацию о книге...</p>
  </div>

  <div v-else-if="book" class="pt-8 pb-20">
    <!-- Хлебные крошки -->
    <div class="container mx-auto px-6 mb-10">
      <nav class="flex text-sm">
        <router-link to="/" class="text-gray-500 hover:text-black">Главная</router-link>
        <span class="mx-2">/</span>
        <router-link to="/catalog" class="text-gray-500 hover:text-black">Каталог</router-link>
        <span class="mx-2">/</span>
        <span class="text-black">{{ book.title }}</span>
      </nav>
    </div>

    <div class="container mx-auto px-6">
      <div class="flex flex-col lg:flex-row gap-12">
        <!-- Левая колонка: Изображение -->
        <div class="lg:w-1/2">
          <!-- Основное изображение -->
          <div class="relative aspect-[3/4] bg-gradient-to-br from-gray-50 to-gray-100 mb-6 shadow-xl overflow-hidden">
            <div v-if="!book.cover_image" class="w-full h-full flex items-center justify-center">
              <span class="text-7xl text-gray-300 opacity-50">📖</span>
            </div>
            <img 
              v-else 
              :src="book.cover_image" 
              :alt="book.title"
              class="w-full h-full object-cover"
            >
            
            <!-- Бейдж скидки -->
            <div v-if="hasDiscount" class="absolute top-6 left-6 bg-black text-white text-lg font-bold px-4 py-2 tracking-widest">
              -{{ book.discount_percentage }}%
            </div>
            
            <!-- Бейдж нового поступления -->
            <div v-if="isNewBook" class="absolute top-6 right-6 bg-white text-black text-sm font-medium px-3 py-1 border border-black tracking-widest">
              НОВИНКА
            </div>
          </div>

          <!-- Миниатюры (галерея) -->
          <div class="grid grid-cols-4 gap-4">
            <div 
              v-for="n in 4" 
              :key="n" 
              class="aspect-square border border-gray-200 hover:border-black cursor-pointer transition-colors bg-gradient-to-br from-gray-50 to-gray-100"
            >
              <div class="w-full h-full flex items-center justify-center">
                <span class="text-2xl text-gray-300">📖</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Правая колонка: Информация -->
        <div class="lg:w-1/2">
          <!-- Название и автор -->
          <h1 class="text-4xl font-bold mb-4">{{ book.title }}</h1>
          <div class="flex items-center mb-8">
            <span class="text-xl text-gray-600">Автор:</span>
            <span class="text-xl ml-3">
              {{ book.author_name }}
            </span>
          </div>

          <!-- Рейтинг и отзывы -->
          <div class="flex items-center mb-8">
            <div class="flex">
              <svg v-for="n in 5" :key="n" class="w-6 h-6" :class="{'text-yellow-400': n <= Math.round(book.average_rating || 0), 'text-gray-300': n > Math.round(book.average_rating || 0)}" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <span class="text-gray-600 ml-3">{{ (book.average_rating || 0).toFixed(1) }} ({{ book.rating_count || 0 }} отзывов)</span>
            <span class="mx-3 text-gray-300">•</span>
            <span class="text-gray-600">ISBN: {{ book.isbn || 'Не указан' }}</span>
          </div>

          <!-- Цена и наличие -->
          <div class="mb-10">
            <div v-if="hasDiscount" class="flex items-baseline mb-2">
              <span class="text-5xl font-bold">{{ formatPrice(book.discount_price!) }}</span>
              <span class="text-2xl text-gray-400 line-through ml-4">{{ formatPrice(book.price) }}</span>
            </div>
            <div v-else>
              <span class="text-5xl font-bold">{{ formatPrice(book.current_price) }}</span>
            </div>
            
            <div class="mt-4">
              <span class="text-lg" :class="{'text-green-600': book.in_stock, 'text-red-600': !book.in_stock}">
                {{ book.in_stock ? '✅ В наличии' : '❌ Нет в наличии' }}
              </span>
              <span v-if="book.in_stock && book.stock_quantity" class="text-gray-600 ml-4">Осталось {{ book.stock_quantity }} экз.</span>
            </div>
          </div>

          <!-- Описание -->
          <div class="mb-10" v-if="book.description">
            <h2 class="text-2xl font-bold mb-4">Описание</h2>
            <p class="text-gray-700 leading-relaxed whitespace-pre-line">
              {{ book.description }}
            </p>
          </div>

          <!-- Детали -->
          <div class="grid grid-cols-2 gap-6 mb-10">
            <div>
              <h3 class="font-bold mb-2">Детали издания</h3>
              <ul class="space-y-2 text-gray-600">
                <li class="flex justify-between">
                  <span>Издательство:</span>
                  <span class="font-medium">{{ book.publisher || 'Не указано' }}</span>
                </li>
                <li class="flex justify-between">
                  <span>Год издания:</span>
                  <span class="font-medium">{{ book.publication_date || 'Не указан' }}</span>
                </li>
                <li class="flex justify-between">
                  <span>Страниц:</span>
                  <span class="font-medium">{{ book.pages || 'Не указано' }}</span>
                </li>
                <li class="flex justify-between">
                  <span>Обложка:</span>
                  <span class="font-medium">{{ getCoverType(book.cover_type) }}</span>
                </li>
                <li class="flex justify-between">
                  <span>Язык:</span>
                  <span class="font-medium">{{ book.language || 'Русский' }}</span>
                </li>
              </ul>
            </div>
            
            <div v-if="book.categories_info && book.categories_info.length > 0">
              <h3 class="font-bold mb-2">Категории</h3>
              <div class="flex flex-wrap gap-2">
                <span v-for="category in book.categories_info" :key="category.id" class="px-3 py-1 border border-gray-300 text-sm hover:border-black transition-colors cursor-pointer">
                  {{ category.name }}
                </span>
              </div>
            </div>
          </div>

          <!-- Кнопки действий -->
          <div class="flex flex-col sm:flex-row gap-4">
            <button 
              class="btn-primary flex-1 text-center text-lg py-4"
              :disabled="!book.in_stock"
              :class="{'opacity-50 cursor-not-allowed': !book.in_stock}"
              @click="addToCart"
            >
              {{ book.in_stock ? 'Добавить в корзину' : 'Нет в наличии' }}
            </button>
            <button class="btn-secondary flex-1 text-center text-lg py-4">
              Добавить в избранное
            </button>
          </div>

          <!-- Дополнительная информация -->
          <div class="mt-10 pt-10 border-t border-gray-200">
            <h3 class="font-bold mb-4">Информация о доставке</h3>
            <ul class="space-y-3 text-gray-600">
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Бесплатная доставка по Москве от 5 000 ₽</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Доставка по России от 2 дней</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Архивная упаковка включена в стоимость</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Вкладки -->
      <div class="mt-20">
        <div class="border-b border-gray-200">
          <nav class="flex space-x-10">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              class="pb-4 text-lg font-medium border-b-2 transition-colors"
              :class="activeTab === tab.id ? 'border-black text-black' : 'border-transparent text-gray-500 hover:text-black'"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <!-- Контент вкладок -->
        <div class="py-10">
          <div v-if="activeTab === 'description' && book.description">
            <h3 class="text-2xl font-bold mb-6">Подробное описание</h3>
            <div class="prose max-w-none text-gray-700 whitespace-pre-line">
              {{ book.description }}
            </div>
          </div>

          <div v-else-if="activeTab === 'reviews'">
            <h3 class="text-2xl font-bold mb-6">Отзывы покупателей</h3>
            <div v-if="book.rating_count === 0" class="text-center py-10">
              <p class="text-gray-600">Пока нет отзывов о этой книге.</p>
              <button class="btn-secondary mt-4">Написать первый отзыв</button>
            </div>
            <div v-else class="space-y-8">
              <div class="border-b border-gray-100 pb-8">
                <div class="flex justify-between items-start mb-4">
                  <div>
                    <h4 class="font-bold">Александр Петров</h4>
                    <div class="flex items-center mt-1">
                      <div class="flex">
                        <svg v-for="n in 5" :key="n" class="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                      </div>
                      <span class="text-sm text-gray-500 ml-2">2 недели назад</span>
                    </div>
                  </div>
                </div>
                <p class="text-gray-700">
                  Потрясающее издание! Качество печати на высоте, упаковка — произведение искусства. Рекомендую всем ценителям.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="pt-20 pb-20 text-center">
    <h2 class="text-2xl font-bold mb-4">Книга не найдена</h2>
    <p class="text-gray-600 mb-8">Запрошенная вами книга не существует или была удалена.</p>
    <router-link to="/catalog" class="btn-primary">Вернуться в каталог</router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { catalogAPI } from '@/api/catalog'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import type { Book } from '@/api/catalog'

const route = useRoute()
const cartStore = useCartStore()
const authStore = useAuthStore()

const loading = ref(true)
const book = ref<Book | null>(null)
const activeTab = ref('description')

const tabs = computed(() => [
  { id: 'description', label: 'Описание' },
  { id: 'reviews', label: `Отзывы (${book.value?.rating_count || 0})` },
])

const hasDiscount = computed(() => {
  if (!book.value?.discount_price) return false
  const discountPrice = parseFloat(book.value.discount_price as string)
  const regularPrice = parseFloat(book.value.price as string)
  return discountPrice > 0 && discountPrice < regularPrice
})

const isNewBook = computed(() => {
  if (!book.value?.created_at) return false
  const bookDate = new Date(book.value.created_at)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - bookDate.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays < 30
})

onMounted(async () => {
  await loadBook()
})

const loadBook = async () => {
  loading.value = true
  try {
    const slug = route.params.slug as string
    book.value = await catalogAPI.getBook(slug)
  } catch (error) {
    console.error('Ошибка загрузки книги:', error)
    book.value = null
  } finally {
    loading.value = false
  }
}

const formatPrice = (price: number | string) => {
  const num = typeof price === 'string' ? parseFloat(price) : price
  return num.toLocaleString('ru-RU') + ' ₽'
}

const getCoverType = (type: string) => {
  const types: Record<string, string> = {
    'hard': 'Твёрдая',
    'soft': 'Мягкая',
    'electronic': 'Электронная',
  }
  return types[type] || type
}

const addToCart = async () => {
  if (!book.value?.in_stock) {
    alert('Товара нет в наличии')
    return
  }
  
  if (!authStore.isAuthenticated) {
    if (confirm('Чтобы добавить товар в корзину, нужно войти в аккаунт. Перейти на страницу входа?')) {
      // router.push('/login') // Добавь useRouter если нужно
    }
    return
  }
  
  try {
    await cartStore.addToCart(book.value.id, 1)
    console.log('Добавлено в корзину:', book.value.title)
  } catch (error: any) {
    console.error('Ошибка при добавлении в корзину:', error)
    alert(error.message || 'Не удалось добавить товар в корзину')
  }
}
</script>