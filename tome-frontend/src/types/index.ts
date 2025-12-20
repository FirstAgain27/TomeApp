// src/types/index.ts

export interface CategoryInfo {
  id: number
  name: string
  slug: string
  description?: string
}


export interface Book {
  id: number
  title: string
  slug: string
  author_name: string
  cover_image?: string
  current_price: number
  price: number
  discount_price?: number | null
  average_rating: number
  description: string
  isbn: string
  stock_quantity: number
  in_stock: boolean
  publisher?: string
  publication_date?: string
  pages?: number
  language: string
  cover_type: string
  discount_percentage: number
  created_at: string
  updated_at: string
  // Добавляем информацию о категориях
  categories_info?: CategoryInfo[]
}

export interface User {
  id: number
  email: string
  username: string
  first_name?: string
  last_name?: string
  full_name?: string
  bio?: string
  avatar?: string
  is_staff?: boolean
  created_at?: string
  updated_at?: string
}
