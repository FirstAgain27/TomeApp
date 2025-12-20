<!-- src/views/HomeView.vue -->
<template>
  <div>
    <!-- Герой-секция -->
    <section class="relative h-screen flex items-center justify-center overflow-hidden">
      <!-- Фон (позже можно заменить на видео или качественное изображение) -->
      <div class="absolute inset-0 bg-gradient-to-br from-gray-50 to-white z-0"></div>
      
      <!-- Декоративные элементы для стиля -->
      <div class="absolute top-20 left-10 w-64 h-64 border border-gray-300 rotate-12 opacity-30"></div>
      <div class="absolute bottom-20 right-10 w-80 h-80 border border-gray-300 -rotate-12 opacity-20"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="max-w-3xl mx-auto text-center">
          <!-- Заголовок -->
          <h1 class="text-5xl md:text-7xl font-bold tracking-tight mb-6 leading-tight">
            <span class="block">T O M E</span>
            <span class="block text-2xl md:text-3xl font-light tracking-widest mt-4 text-gray-600">BOOKSTORE</span>
          </h1>
          
          <!-- Подзаголовок -->
          <p class="text-lg md:text-xl text-gray-500 mb-10 max-w-2xl mx-auto tracking-wide leading-relaxed">
            Tome — пространство классики в её идеальной форме. Мы отбираем только значимые произведения русской и западной литературы, избавляя вас от шума современного книжного рынка. Здесь нет ничего лишнего — только текст, идеальный носитель и ваш диалог с автором.
          </p>
          
          <!-- Кнопки -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link 
              to="/catalog" 
              class="btn-primary inline-flex items-center justify-center group"
            >
              Исследовать каталог
              <svg class="ml-3 w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
              </svg>
            </router-link>
            <a 
              href="#" 
              class="btn-secondary inline-flex items-center justify-center"
            >
              О коллекции
              <svg class="ml-3 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 9l-7 7-7-7"/>
              </svg>
            </a>
          </div>
        </div>
      </div>

      <!-- Индикатор прокрутки -->
      <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
        </svg>
      </div>
    </section>

    <!-- Блок преимуществ -->
    <section class="py-20 bg-white">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold mb-4">Почему Tome</h2>
          <p class="text-gray-500 max-w-2xl mx-auto">Принципы, которые определяют наш подход к&nbsp;книгам</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div class="text-center p-8">
            <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center border border-gray-300 rounded-full">
              <span class="text-2xl">📜</span>
            </div>
            <h3 class="text-xl font-bold mb-4">Кураторство</h3>
            <p class="text-gray-600">Каждая книга проходит строгий отбор. Мы предлагаем только то, что заслуживает внимания.</p>
          </div>

          <div class="text-center p-8">
            <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center border border-gray-300 rounded-full">
              <span class="text-2xl">✒️</span>
            </div>
            <h3 class="text-xl font-bold mb-4">Архивные издания</h3>
            <p class="text-gray-600">Редкие тиражи, факсимиле первых изданий, книги с&nbsp;историей.</p>
          </div>

          <div class="text-center p-8">
            <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center border border-gray-300 rounded-full">
              <span class="text-2xl">📦</span>
            </div>
            <h3 class="text-xl font-bold mb-4">Музейная упаковка</h3>
            <p class="text-gray-600">Каждая книга упакована вручную с&nbsp;использованием архивных материалов.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Блок с избранной книгой -->
    <section class="py-20 border-t border-gray-100">
      <div class="container mx-auto px-6">
        <div class="flex flex-col lg:flex-row items-center gap-12">
          <!-- Изображение книги -->
          <div class="lg:w-1/2">
            <div class="relative">
              <div class="aspect-[3/4] bg-gradient-to-br from-gray-100 to-gray-200 shadow-2xl"></div>
              <div class="absolute -bottom-6 -right-6 w-48 h-64 bg-gradient-to-br from-gray-300 to-gray-400 opacity-20 -z-10"></div>
              <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
                <span class="text-6xl opacity-10">📖</span>
              </div>
            </div>
          </div>

          <!-- Описание -->
          <div class="lg:w-1/2">
            <span class="text-sm uppercase tracking-widest text-gray-400 mb-4 block">Книга месяца</span>
            <h2 class="text-3xl md:text-4xl font-bold mb-6">«Название редкой книги»</h2>
            <p class="text-gray-600 mb-8 leading-relaxed">
              Факсимильное издание 1927 года. Сохранён оригинальный переплёт, типографская бумага и&nbsp;все особенности первоисточника. Тираж 300 экземпляров.
            </p>
            <div class="space-y-4 mb-10">
              <div class="flex items-center">
                <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Оригинальный переплёт 1927 года</span>
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Тираж 300 пронумерованных экземпляров</span>
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span>Сопроводительное письмо от куратора</span>
              </div>
            </div>
            <div class="flex items-center gap-6">
              <span class="text-3xl font-bold">45 000 ₽</span>
              <button class="btn-primary">Предзаказ</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// Логику добавим позже
</script>
