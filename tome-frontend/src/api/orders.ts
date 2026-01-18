// src/api/orders.ts
import api from './index'

export interface OrderItem {
  id: number
  book: number
  book_title: string
  book_author: string
  book_cover: string | null
  quantity: number
  price: string
  total: string
}

export interface Order {
  id: number
  order_number: string
  status: string
  formatted_date: string
  total_price: string
  items_count: number
  shipping_address: string
  phone_number: string
  payment_method: string
  payment_status: string
  created_at: string
  updated_at: string
  items: OrderItem[]
  note?: string
}

export interface CreateOrderData {
  shipping_address: string
  phone_number: string
  payment_method: 'CARD' | 'CASH' | 'ONLINE'
}

export interface CancelOrderData {
  reason: string
}

export interface AddNoteData {
  note: string
}

const orderApi = {
  // Получить список заказов
  getOrders() {
    return api.get<Order[]>('/orders/')
  },

  // Получить детали заказа
  getOrder(id: number) {
    return api.get<Order>(`/orders/${id}/`)
  },

  // Создать заказ
  createOrder(data: CreateOrderData) {
    return api.post<Order>('/orders/', data)
  },

  // Отменить заказ
  cancelOrder(id: number, data: CancelOrderData) {
    return api.post(`/orders/${id}/cancel/`, data)
  },

  // Добавить заметку к заказу
  addNote(id: number, data: AddNoteData) {
    return api.post(`/orders/${id}/add_note/`, data)
  },

  // Обновить заметку (если через PATCH)
  updateNote(id: number, data: AddNoteData) {
    return api.patch(`/orders/${id}/`, data)
  }
}

export default orderApi