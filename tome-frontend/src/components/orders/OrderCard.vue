<!-- src/components/orders/OrderCard.vue -->
<template>
  <div class="border border-gray-200 p-6 hover:border-black transition-colors">
    <!-- Order header -->
    <div class="flex justify-between items-start mb-6">
      <div>
        <h3 class="text-xl font-bold mb-2">{{ order.order_number }}</h3>
        <div class="flex items-center gap-4 text-sm text-gray-600">
          <span>{{ order.formatted_date }}</span>
          <span>•</span>
          <span>{{ order.items_count }} товар{{ itemsCountText }}</span>
          <span>•</span>
          <span>{{ parseFloat(order.total_price).toLocaleString() }} ₽</span>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <StatusBadge :status="order.status" />
        
        <!-- Actions dropdown -->
        <div class="relative">
          <button
            @click="showActions = !showActions"
            class="p-2 hover:bg-gray-100 rounded"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
            </svg>
          </button>
          
          <!-- Dropdown menu -->
          <div
            v-if="showActions"
            class="absolute right-0 mt-2 w-48 bg-white border border-gray-200 shadow-lg z-10"
            @click="showActions = false"
          >
            <button
              @click="viewDetails"
              class="block w-full text-left px-4 py-3 hover:bg-gray-50"
            >
              Просмотреть детали
            </button>
            
            <button
              v-if="canCancel"
              @click="showCancelModal = true"
              class="block w-full text-left px-4 py-3 hover:bg-gray-50 text-red-600"
            >
              Отменить заказ
            </button>
            
            <button
              @click="showNoteModal = true"
              class="block w-full text-left px-4 py-3 hover:bg-gray-50"
            >
              {{ order.note ? 'Изменить заметку' : 'Добавить заметку' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Items preview -->
    <div class="mb-6">
      <div class="flex gap-4 overflow-x-auto pb-4">
        <div
          v-for="item in order.items?.slice(0, 3)"
          :key="item.id"
          class="flex-shrink-0 w-24"
        >
          <div class="w-24 h-36 bg-gray-100 overflow-hidden mb-2">
            <img
              v-if="item.book_cover"
              :src="item.book_cover"
              :alt="item.book_title"
              class="w-full h-full object-cover"
            >
            <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
              <span class="text-2xl">📖</span>
            </div>
          </div>
          <p class="text-xs truncate">{{ item.book_title }}</p>
        </div>
        
        <div v-if="order.items && order.items.length > 3" class="flex-shrink-0 w-24">
          <div class="w-24 h-36 bg-gray-100 flex items-center justify-center">
            <span class="text-2xl text-gray-400">+{{ order.items.length - 3 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Shipping info -->
    <div class="text-sm text-gray-600 space-y-2">
      <div class="flex justify-between">
        <span>Адрес доставки:</span>
        <span class="text-black">{{ order.shipping_address }}</span>
      </div>
      <div class="flex justify-between">
        <span>Телефон:</span>
        <span class="text-black">{{ order.phone_number }}</span>
      </div>
      <div class="flex justify-between">
        <span>Способ оплаты:</span>
        <span class="text-black">{{ paymentMethodText }}</span>
      </div>
      
      <!-- Note preview -->
      <div v-if="order.note" class="mt-4 p-3 bg-yellow-50 border border-yellow-100 rounded">
        <div class="flex items-start">
          <span class="text-yellow-600 mr-2">📝</span>
          <span class="text-sm">{{ order.note }}</span>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <CancelOrderModal
      v-if="showCancelModal"
      :order-number="order.order_number"
      @confirm="handleCancel"
      @close="showCancelModal = false"
    />
    
    <AddNoteModal
      v-if="showNoteModal"
      :current-note="order.note"
      @save="handleAddNote"
      @close="showNoteModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import StatusBadge from './StatusBadge.vue'
import CancelOrderModal from './CancelOrderModal.vue'
import AddNoteModal from './AddNoteModal.vue'

const props = defineProps<{
  order: any // Можно заменить на конкретный тип Order
}>()

const emit = defineEmits<{
  cancelOrder: [id: number, reason: string]
  addNote: [id: number, note: string]
}>()

const router = useRouter()
const showActions = ref(false)
const showCancelModal = ref(false)
const showNoteModal = ref(false)

const itemsCountText = computed(() => {
  const lastDigit = props.order.items_count % 10
  const lastTwoDigits = props.order.items_count % 100
  
  if (lastTwoDigits >= 11 && lastTwoDigits <= 19) return 'ов'
  if (lastDigit === 1) return ''
  if (lastDigit >= 2 && lastDigit <= 4) return 'а'
  return 'ов'
})

const paymentMethodText = computed(() => {
  const methods: Record<string, string> = {
    'CARD': 'Банковская карта',
    'CASH': 'Наличные при получении',
    'ONLINE': 'Онлайн оплата'
  }
  return methods[props.order.payment_method] || props.order.payment_method
})

const canCancel = computed(() => {
  return ['PENDING', 'PAID'].includes(props.order.status)
})

const viewDetails = () => {
  router.push(`/orders/${props.order.id}`)
}

const handleCancel = (reason: string) => {
  emit('cancelOrder', props.order.id, reason)
  showCancelModal.value = false
}

const handleAddNote = (note: string) => {
  emit('addNote', props.order.id, note)
  showNoteModal.value = false
}
</script>
