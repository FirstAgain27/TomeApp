// src/api/catalog.ts
import api from './index'

export interface Book {
  id: number
  title: string
  slug: string
  author_name: string
  cover_image: string | null
  current_price: number | string
  price: number | string
  discount_price: number | string | null
  average_rating: number | null
  description: string
  isbn: string
  stock_quantity: number
  in_stock: boolean
  publisher: string
  publication_date: string
  pages: number
  language: string
  cover_type: string
  discount_percentage: number
  created_at: string
  updated_at: string
  rating_count?: number
  categories_info?: Array<{
    id: number
    name: string
    slug: string
    description: string
  }>
}

export const catalogAPI = {
  async getBooks(): Promise<{ results: Book[] } | Book[]> {
    const response = await api.get('/catalog/books/')
    return response.data
  },
  
  async getBook(slug: string): Promise<Book> {
    const response = await api.get(`/catalog/books/${slug}/`)
    return response.data
  },
  
  async getCategories() {
    const response = await api.get('/catalog/categories/')
    return response.data
  },
  
  async getAuthors() {
    const response = await api.get('/catalog/authors/')
    return response.data
  }
}