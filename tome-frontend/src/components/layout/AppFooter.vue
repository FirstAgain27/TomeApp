<!-- src/components/layout/AppFooter.vue -->
<template>
  <footer class="bg-black text-white mt-20">
    <div class="container mx-auto px-6 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Колонка 1: О магазине -->
        <div>
          <h3 class="text-2xl font-bold tracking-tighter mb-4">TOME</h3>
          <p class="text-gray-400 text-sm">
            Премиальный книжный магазин. Эксклюзивные издания, редкие авторы, коллекционные книги.
          </p>
        </div>

        <!-- Колонка 2: Навигация -->
        <div>
          <h4 class="font-bold mb-4 uppercase tracking-widest text-sm">Навигация</h4>
          <ul class="space-y-2">
            <li><a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">Каталог</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">Новинки</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">Бестселлеры</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">Акции</a></li>
          </ul>
        </div>

        <!-- Колонка 3: Помощь -->
        <div>
          <h4 class="font-bold mb-4 uppercase tracking-widest text-sm">Помощь</h4>
          <ul class="space-y-2">
            <li><a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">Доставка и оплата</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">Возврат</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">Контакты</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">FAQ</a></li>
          </ul>
        </div>

        <!-- Колонка 4: Контакты -->
        <div>
          <h4 class="font-bold mb-4 uppercase tracking-widest text-sm">Контакты</h4>
          <p class="text-gray-400 text-sm mb-2">+7 (XXX) XXX-XX-XX</p>
          <p class="text-gray-400 text-sm mb-4">contact@tome-books.ru</p>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-400 hover:text-white">Instagram</a>
            <a href="#" class="text-gray-400 hover:text-white">Telegram</a>
          </div>
        </div>
      </div>

      <!-- Копирайт -->
      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-500 text-sm">
        <p>© 2025 TOME BOOKSTORE. Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Логику добавим позже
</script>
