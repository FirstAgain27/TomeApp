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
            <div v-if="book.discount_percentage" class="absolute top-6 left-6 bg-black text-white text-lg font-bold px-4 py-2 tracking-widest">
              -{{ book.discount_percentage }}%
            </div>
            
            <!-- Бейдж нового поступления -->
            <div class="absolute top-6 right-6 bg-white text-black text-sm font-medium px-3 py-1 border border-black tracking-widest">
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
            <router-link to="/authors/author-slug" class="text-xl ml-3 hover:underline">
              {{ book.author_name }}
            </router-link>
          </div>

          <!-- Рейтинг и отзывы -->
          <div class="flex items-center mb-8">
            <div class="flex">
              <svg v-for="n in 5" :key="n" class="w-6 h-6" :class="{'text-yellow-400': n <= Math.round(book.average_rating), 'text-gray-300': n > Math.round(book.average_rating)}" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <span class="text-gray-600 ml-3">{{ book.average_rating.toFixed(1) }} (128 отзывов)</span>
            <span class="mx-3 text-gray-300">•</span>
            <span class="text-gray-600">ISBN: {{ book.isbn }}</span>
          </div>

          <!-- Цена и наличие -->
          <div class="mb-10">
            <div v-if="book.discount_price" class="flex items-baseline mb-2">
              <span class="text-5xl font-bold">{{ book.discount_price.toLocaleString() }} ₽</span>
              <span class="text-2xl text-gray-400 line-through ml-4">{{ book.price.toLocaleString() }} ₽</span>
            </div>
            <div v-else>
              <span class="text-5xl font-bold">{{ book.current_price.toLocaleString() }} ₽</span>
            </div>
            
            <div class="mt-4">
              <span class="text-lg" :class="{'text-green-600': book.in_stock, 'text-red-600': !book.in_stock}">
                {{ book.in_stock ? '✅ В наличии' : '❌ Нет в наличии' }}
              </span>
              <span v-if="book.in_stock" class="text-gray-600 ml-4">Осталось {{ book.stock_quantity }} экз.</span>
            </div>
          </div>

          <!-- Описание -->
          <div class="mb-10">
            <h2 class="text-2xl font-bold mb-4">Описание</h2>
            <p class="text-gray-700 leading-relaxed">
              {{ book.description || 'Эксклюзивное коллекционное издание. Книга в идеальном состоянии, сохранены все элементы оригинального оформления. Ограниченный тираж.' }}
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
                  <span class="font-medium">{{ book.language }}</span>
                </li>
              </ul>
            </div>
            
            <div>
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

      <!-- Вкладки (Описание/Отзывы) -->
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
          <div v-if="activeTab === 'description'">
            <h3 class="text-2xl font-bold mb-6">Подробное описание</h3>
            <div class="prose max-w-none text-gray-700">
              <p class="mb-4">
                Это эксклюзивное коллекционное издание представляет собой факсимильное воспроизведение оригинала с сохранением всех особенностей: типографской бумаги, переплёта, иллюстраций и даже мельчайших деталей вёрстки.
              </p>
              <p class="mb-4">
                Каждый экземпляр пронумерован и сопровождается сертификатом подлинности, подписанным куратором коллекции. Книга упакована в архивный футляр из переработанного картона с тиснением золотой фольгой.
              </p>
              <ul class="list-disc pl-5 mb-4 space-y-2">
                <li>Ограниченный тираж: 300 экземпляров</li>
                <li>Факсимильное воспроизведение оригинала</li>
                <li>Архивная упаковка с сертификатом</li>
                <li>Тиснение золотой фольгой</li>
              </ul>
            </div>
          </div>

          <div v-else-if="activeTab === 'reviews'">
            <h3 class="text-2xl font-bold mb-6">Отзывы покупателей</h3>
            <div class="space-y-8">
              <!-- Пример отзыва -->
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
import type { Book } from '@/types'

const route = useRoute()
const loading = ref(true)
const book = ref<Book | null>(null)
const activeTab = ref('description')

const tabs = [
  { id: 'description', label: 'Описание' },
  { id: 'reviews', label: 'Отзывы (128)' },
]

// Мок-данные для книги (потом заменим на запрос к API)
const mockBook: Book = {
  id: 1,
  title: 'Мастер и Маргарита',
  slug: 'master-i-margarita',
  author_name: 'Михаил Булгаков',
  cover_image: '',
  current_price: 5600,
  price: 5600,
  discount_price: null,
  average_rating: 4.8,
  description: 'Эксклюзивное коллекционное издание романа Михаила Булгакова. Факсимильное воспроизведение первого издания с комментариями и иллюстрациями.',
  isbn: '978-5-699-12345-6',
  stock_quantity: 5,
  in_stock: true,
  publisher: 'Издательство «Редкая книга»',
  publication_date: '2023',
  pages: 480,
  language: 'Русский',
  cover_type: 'hard',
  discount_percentage: 0,
  created_at: '2023-10-15T10:30:00Z',
  updated_at: '2023-10-15T10:30:00Z'
}

// Добавляем информацию о категориях для этой книги
const bookWithCategories = {
  ...mockBook,
  categories_info: [
    { id: 1, name: 'Русская классика', slug: 'russkaya-klassika' },
    { id: 2, name: 'Художественная литература', slug: 'hudozhestvennaya' },
    { id: 3, name: 'Коллекционные издания', slug: 'kollekcionnye' },
  ]
}

onMounted(() => {
  // Имитация загрузки данных с API
  setTimeout(() => {
    book.value = bookWithCategories as Book
    loading.value = false
  }, 500)
})

const getCoverType = (type: string) => {
  const types: Record<string, string> = {
    'hard': 'Твёрдая',
    'soft': 'Мягкая',
    'electronic': 'Электронная',
  }
  return types[type] || type
}

const addToCart = () => {
  if (book.value?.in_stock) {
    console.log('Добавлено в корзину:', book.value)
    // TODO: Реализовать добавление в корзину
  }
}
</script>