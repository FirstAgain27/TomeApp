<!-- src/components/orders/CancelOrderModal.vue -->
<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-8 max-w-md w-full mx-4">
      <h3 class="text-xl font-bold mb-4">Отмена заказа {{ orderNumber }}</h3>
      
      <p class="text-gray-600 mb-6">
        Пожалуйста, укажите причину отмены. Отмена доступна только для заказов в статусе "В обработке" или "Оплачен".
      </p>
      
      <textarea
        v-model="reason"
        placeholder="Например: передумал, нашел дешевле, изменились обстоятельства..."
        class="w-full h-32 p-3 border border-gray-300 rounded mb-6"
      ></textarea>
      
      <div class="flex gap-4">
        <button
          @click="$emit('close')"
          class="btn-secondary flex-1"
        >
          Отмена
        </button>
        <button
          @click="confirmCancel"
          :disabled="!reason.trim()"
          :class="[
            'btn-primary flex-1',
            !reason.trim() && 'opacity-50 cursor-not-allowed'
          ]"
        >
          Подтвердить отмену
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  orderNumber: string
}>()

const emit = defineEmits<{
  confirm: [reason: string]
  close: []
}>()

const reason = ref('')

const confirmCancel = () => {
  if (reason.value.trim()) {
    emit('confirm', reason.value.trim())
  }
}
</script>