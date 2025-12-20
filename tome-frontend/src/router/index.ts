import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { title: 'Tome — Премиальный книжный магазин' }
    },
    {
      path: '/catalog',
      name: 'catalog',
      component: () => import('@/views/CatalogView.vue'),
      meta: { title: 'Каталог книг | Tome' }
    },
    {
      path: '/books/:slug',
      name: 'book-detail',
      component: () => import('@/views/BookDetailView.vue'),
      meta: { title: 'Книга | Tome' }
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('@/views/CartView.vue'),
      meta: { title: 'Корзина | Tome' }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { 
        title: 'Вход | Tome',
        requiresGuest: true
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { 
        title: 'Регистрация | Tome',
        requiresGuest: true
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/auth/ProfileView.vue'),
      meta: { 
        title: 'Профиль | Tome',
        requiresAuth: true
      }
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('@/views/auth/OrdersView.vue'),
      meta: { 
        title: 'Заказы | Tome',
        requiresAuth: true
      }
    },
    {
      path: '/wishlist',
      name: 'wishlist',
      component: () => import('@/views/auth/WishlistView.vue'),
      meta: { 
        title: 'Избранное | Tome',
        requiresAuth: true
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
      meta: { title: 'Страница не найдена | Tome' }
    }
  ],
})

// Навигационные хуки
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Устанавливаем заголовок страницы
  if (to.meta.title) {
    document.title = to.meta.title as string
  }

  // Проверка аутентификации
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router