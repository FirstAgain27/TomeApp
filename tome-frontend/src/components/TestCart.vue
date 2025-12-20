<!-- src/components/TestCart.vue -->
<template>
  <div class="fixed bottom-4 right-4 bg-black text-white p-4 rounded z-50">
    <p>Корзина работает!</p>
    <p>Товаров: {{ cartStore.totalItems }}</p>
    <button @click="testAdd" class="bg-white text-black px-3 py-1 mt-2">
      Тест добавить
    </button>
  </div>
</template>

<script setup lang="ts">
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()

const testAdd = () => {
  cartStore.addItem({
    id: 999,
    title: 'Тестовая книга',
    slug: 'test-book',
    author_name: 'Тест Автор',
    current_price: 1000,
    price: 1000,
    average_rating: 4.5,
    description: '',
    isbn: '',
    stock_quantity: 10,
    in_stock: true,
    publisher: '',
    publication_date: '',
    pages: 0,
    language: '',
    cover_type: '',
    discount_percentage: 0,
    created_at: '',
    updated_at: ''
  }, 1)
}
</script>
