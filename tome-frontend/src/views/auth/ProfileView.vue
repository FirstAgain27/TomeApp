<!-- src/views/auth/ProfileView.vue -->
<template>
  <div class="pt-8 pb-20">
    <div class="container mx-auto px-6">
      <!-- Хлебные крошки -->
      <nav class="flex text-sm mb-10">
        <router-link to="/" class="text-gray-500 hover:text-black">Главная</router-link>
        <span class="mx-2">/</span>
        <span class="text-black">Профиль</span>
      </nav>

      <div class="flex flex-col lg:flex-row gap-12">
        <!-- Боковая навигация -->
        <div class="lg:w-1/4">
          <div class="border border-gray-200 p-6 sticky top-24">
            <!-- Аватар -->
            <div class="flex items-center mb-8">
              <div class="w-16 h-16 bg-black text-white rounded-full flex items-center justify-center text-2xl font-bold mr-4">
                {{ authStore.initials }}
              </div>
              <div>
                <h2 class="font-bold text-xl">{{ authStore.fullName }}</h2>
                <p class="text-gray-600 text-sm">{{ authStore.user?.email }}</p>
              </div>
            </div>

            <!-- Меню -->
            <nav class="space-y-2">
              <router-link 
                to="/profile" 
                class="block px-4 py-3 hover:bg-gray-50 rounded transition-colors"
                :class="{ 'bg-black text-white hover:bg-gray-800': $route.name === 'profile' }"
              >
                Личные данные
              </router-link>
              <router-link 
                to="/orders" 
                class="block px-4 py-3 hover:bg-gray-50 rounded transition-colors"
              >
                Мои заказы
              </router-link>
              <router-link 
                to="/wishlist" 
                class="block px-4 py-3 hover:bg-gray-50 rounded transition-colors"
              >
                Избранное
              </router-link>
              <button 
                @click="handleLogout"
                class="block w-full text-left px-4 py-3 hover:bg-gray-50 rounded transition-colors text-red-600"
              >
                Выйти
              </button>
            </nav>
          </div>
        </div>

        <!-- Основной контент -->
        <div class="lg:w-3/4">
          <div class="border border-gray-200 p-8">
            <h1 class="text-3xl font-bold mb-8">Личные данные</h1>

            <!-- Форма профиля -->
            <form @submit.prevent="updateProfile" class="space-y-6">
              <!-- Имя пользователя -->
              <div>
                <label class="block text-sm font-medium mb-2">Имя пользователя</label>
                <input
                  v-model="profileForm.username"
                  type="text"
                  class="input-field"
                  disabled
                />
                <p class="text-xs text-gray-500 mt-1">Имя пользователя нельзя изменить</p>
              </div>

              <!-- Email -->
              <div>
                <label class="block text-sm font-medium mb-2">Email</label>
                <input
                  v-model="profileForm.email"
                  type="email"
                  class="input-field"
                  disabled
                />
                <p class="text-xs text-gray-500 mt-1">Email нельзя изменить</p>
              </div>

              <!-- Имя -->
              <div>
                <label class="block text-sm font-medium mb-2">Имя</label>
                <input
                  v-model="profileForm.first_name"
                  type="text"
                  class="input-field"
                  placeholder="Иван"
                />
              </div>

              <!-- Фамилия -->
              <div>
                <label class="block text-sm font-medium mb-2">Фамилия</label>
                <input
                  v-model="profileForm.last_name"
                  type="text"
                  class="input-field"
                  placeholder="Иванов"
                />
              </div>

              <!-- Биография -->
              <div>
                <label class="block text-sm font-medium mb-2">О себе</label>
                <textarea
                  v-model="profileForm.bio"
                  rows="4"
                  class="input-field"
                  placeholder="Расскажите немного о себе..."
                ></textarea>
              </div>

              <!-- Кнопки -->
              <div class="flex gap-4 pt-6 border-t border-gray-200">
                <button
                  type="submit"
                  class="btn-primary"
                  :disabled="loading"
                >
                  {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
                </button>
                <button
                  type="button"
                  @click="resetForm"
                  class="btn-secondary"
                >
                  Отмена
                </button>
              </div>
            </form>

            <!-- Смена пароля -->
            <div class="mt-12 pt-12 border-t border-gray-200">
              <h2 class="text-2xl font-bold mb-6">Смена пароля</h2>
              
              <form @submit.prevent="changePassword" class="space-y-6">
                <!-- Старый пароль -->
                <div>
                  <label class="block text-sm font-medium mb-2">Текущий пароль</label>
                  <input
                    v-model="passwordForm.old_password"
                    type="password"
                    class="input-field"
                    required
                  />
                </div>

                <!-- Новый пароль -->
                <div>
                  <label class="block text-sm font-medium mb-2">Новый пароль</label>
                  <input
                    v-model="passwordForm.new_password"
                    type="password"
                    class="input-field"
                    required
                  />
                </div>

                <!-- Подтверждение пароля -->
                <div>
                  <label class="block text-sm font-medium mb-2">Подтверждение пароля</label>
                  <input
                    v-model="passwordForm.new_password_confirm"
                    type="password"
                    class="input-field"
                    required
                  />
                </div>

                <!-- Сообщения -->
                <div v-if="passwordError" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded text-sm">
                  {{ passwordError }}
                </div>
                <div v-if="passwordSuccess" class="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded text-sm">
                  {{ passwordSuccess }}
                </div>

                <!-- Кнопка -->
                <button
                  type="submit"
                  class="btn-primary"
                  :disabled="passwordLoading"
                >
                  {{ passwordLoading ? 'Изменение...' : 'Изменить пароль' }}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const passwordLoading = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

// Форма профиля
const profileForm = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  bio: ''
})

// Форма смены пароля
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
})

// Инициализация формы
const initForm = () => {
  if (authStore.user) {
    profileForm.username = authStore.user.username || ''
    profileForm.email = authStore.user.email || ''
    profileForm.first_name = authStore.user.first_name || ''
    profileForm.last_name = authStore.user.last_name || ''
    profileForm.bio = authStore.user.bio || ''
  }
}

// Обновление профиля
const updateProfile = async () => {
  loading.value = true
  const result = await authStore.updateProfile(profileForm)
  loading.value = false
  
  if (result.success) {
    alert('Профиль успешно обновлён')
  } else {
    alert('Ошибка при обновлении профиля')
  }
}

// Смена пароля
const changePassword = async () => {
  if (passwordForm.new_password !== passwordForm.new_password_confirm) {
    passwordError.value = 'Пароли не совпадают'
    return
  }
  
  passwordLoading.value = true
  passwordError.value = ''
  passwordSuccess.value = ''
  
  const result = await authStore.changePassword(passwordForm)
  passwordLoading.value = false
  
  if (result.success) {
    passwordSuccess.value = 'Пароль успешно изменён'
    // Очищаем форму
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.new_password_confirm = ''
  } else {
    if (result.error?.old_password) {
      passwordError.value = `Текущий пароль: ${result.error.old_password[0]}`
    } else if (result.error?.new_password) {
      passwordError.value = `Новый пароль: ${result.error.new_password[0]}`
    } else {
      passwordError.value = 'Ошибка при смене пароля'
    }
  }
}

// Сброс формы
const resetForm = () => {
  initForm()
}

// Выход
const handleLogout = async () => {
  if (confirm('Вы уверены, что хотите выйти?')) {
    await authStore.logout()
    router.push('/login')
  }
}

// Инициализация при загрузке
onMounted(() => {
  initForm()
})
</script>