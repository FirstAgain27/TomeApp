<!-- src/components/orders/StatusBadge.vue -->
<template>
  <span :class="badgeClasses">
    {{ statusText }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string
}>()

const statusText = computed(() => {
  const statuses: Record<string, string> = {
    'PENDING': 'В обработке',
    'PAID': 'Оплачен',
    'PROCESSING': 'В сборке',
    'SHIPPED': 'Отправлен',
    'DELIVERED': 'Доставлен',
    'COMPLETED': 'Завершен',
    'CANCELLED': 'Отменен'
  }
  return statuses[props.status] || props.status
})

const badgeClasses = computed(() => {
  const base = 'px-3 py-1 text-xs font-medium rounded-full'
  
  const colors: Record<string, string> = {
    'PENDING': 'bg-yellow-100 text-yellow-800',
    'PAID': 'bg-blue-100 text-blue-800',
    'PROCESSING': 'bg-purple-100 text-purple-800',
    'SHIPPED': 'bg-indigo-100 text-indigo-800',
    'DELIVERED': 'bg-green-100 text-green-800',
    'COMPLETED': 'bg-green-100 text-green-800',
    'CANCELLED': 'bg-red-100 text-red-800'
  }
  
  return `${base} ${colors[props.status] || 'bg-gray-100 text-gray-800'}`
})
</script>
