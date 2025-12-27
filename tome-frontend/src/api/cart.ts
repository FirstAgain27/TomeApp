// src/api/cart.ts
import api from './index'

export interface CartBook {
  id: number
  title: string
  author_name: string
  cover_image: string | null
  current_price: string
  average_rating: number | null
  slug: string
}

export interface CartItem {
  id: number
  book: CartBook
  quantity: number
  item_total: string
  created_at: string
}

export interface Cart {
  id: number
  user: number
  items: CartItem[]
  total_items: number
  total_price: string
  created_at: string
  updated_at: string
}

export const cartAPI = {
  async getCart(): Promise<Cart> {
    const response = await api.get('/cart/')
    return response.data
  },

  async addToCart(bookId: number, quantity: number = 1): Promise<any> {
    const response = await api.post('/cart/items/', {
      book_id: bookId,
      quantity: quantity
    })
    return response.data
  },

  async updateCartItem(itemId: number, quantity: number): Promise<any> {
    const response = await api.patch(`/cart/items/${itemId}/`, {
      quantity: quantity
    })
    return response.data
  },

  async removeFromCart(itemId: number): Promise<void> {
    await api.delete(`/cart/items/${itemId}/`)
  },

  async clearCart(): Promise<void> {
    await api.delete('/cart/')
  }
}