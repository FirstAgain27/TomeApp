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
  author?: number
  categories?: number[]
  categories_info?: Array<{
    id: number
    name: string
    slug: string
    description: string
  }>
}

export interface Author {
  id: number
  first_name: string
  second_name: string
  full_name: string
  slug: string
  bio?: string
  photo?: string
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  parent?: number
}

export const catalogAPI = {
  // Получить все книги с фильтрами
  async getBooks(params?: {
    author?: string
    categories?: string
    ordering?: string
    search?: string
    page?: number
  }): Promise<{ results: Book[] } | Book[]> {
    const response = await api.get('/catalog/books/', { params })
    return response.data
  },
  
  // Получить книгу по slug
  async getBook(slug: string): Promise<Book> {
    const response = await api.get(`/catalog/books/${slug}/`)
    return response.data
  },
  
  // Получить категории
  async getCategories(): Promise<Category[]> {
    const response = await api.get('/catalog/categories/')
    return response.data
  },
  
  // Получить авторов
  async getAuthors(): Promise<Author[]> {
    const response = await api.get('/catalog/authors/')
    return response.data
  }
}