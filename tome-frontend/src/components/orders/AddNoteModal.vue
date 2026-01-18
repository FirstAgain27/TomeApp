<!-- src/components/orders/AddNoteModal.vue -->
<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-8 max-w-md w-full mx-4">
      <h3 class="text-xl font-bold mb-4">
        {{ currentNote ? 'Изменить заметку' : 'Добавить заметку к заказу' }}
      </h3>
      
      <textarea
        v-model="note"
        :placeholder="currentNote ? 'Измените текст заметки...' : 'Напишите заметку для этого заказа...'"
        class="w-full h-32 p-3 border border-gray-300 rounded mb-6"
        maxlength="200"
      ></textarea>
      
      <div class="text-sm text-gray-500 mb-6">
        <div class="flex justify-between">
          <span>Максимальная длина: 200 символов</span>
          <span>{{ note.length }}/200</span>
        </div>
      </div>
      
      <div class="flex gap-4">
        <button
          @click="$emit('close')"
          class="btn-secondary flex-1"
        >
          Отмена
        </button>
        <button
          @click="saveNote"
          :disabled="note.trim().length === 0"
          :class="[
            'btn-primary flex-1',
            note.trim().length === 0 && 'opacity-50 cursor-not-allowed'
          ]"
        >
          Сохранить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{
  currentNote?: string
}>()

const emit = defineEmits<{
  save: [note: string]
  close: []
}>()

const note = ref('')

onMounted(() => {
  if (props.currentNote) {
    note.value = props.currentNote
  }
})

const saveNote = () => {
  if (note.value.trim()) {
    emit('save', note.value.trim())
  }
}
</script>