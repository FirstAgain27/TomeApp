<template>
  <div class="not-found">
    <h1>404 - Страница не найдена</h1>
    <p>Извините, запрашиваемая страница не существует.</p>
    <router-link to="/">Вернуться на главную</router-link>
  </div>
</template>

<script setup lang="ts">
// Можно добавить логику при необходимости
</script>

<style scoped>
.not-found {
  text-align: center;
  padding: 50px;
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
