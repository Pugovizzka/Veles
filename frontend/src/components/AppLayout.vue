<template>
  <div class="app-layout">
    <!-- Боковая панель -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <button class="toggle-btn" @click="toggleSidebar">
        {{ sidebarCollapsed ? '☰' : '✕' }}
      </button>
      <nav>
        <ul>
          <li>
            <router-link to="/dashboard" active-class="active-link">
              <span v-if="!sidebarCollapsed">Главная</span>
            </router-link>
          </li>
          <li>
            <router-link to="/activity" active-class="active-link">
              <span v-if="!sidebarCollapsed">Активность</span>
            </router-link>
          </li>
          <li>
            <router-link to="/reports" active-class="active-link">
              <span v-if="!sidebarCollapsed">Отчёты</span>
            </router-link>
          </li>
          <li v-if="isAdminOrManager">
            <router-link to="/employees" active-class="active-link">
              <span v-if="!sidebarCollapsed">Сотрудники</span>
            </router-link>
          </li>
        </ul>
      </nav>
    </div>

    <!-- Основное содержимое -->
    <div class="main-content" :class="{ 'expanded': sidebarCollapsed }">
      <div class="header">
        <h1>{{ title }}</h1>
        <div class="user-info">
          <p>Добро пожаловать, {{ user?.email }}</p>
          <button @click="handleLogout">Выйти</button>
        </div>
      </div>

      <!-- Здесь будет отображаться содержимое маршрута -->
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

const store = useStore()
const router = useRouter()
const route = useRoute()

const sidebarCollapsed = ref(false)

const user = computed(() => store.getters['auth/currentUser'])
const isAdminOrManager = computed(() => 
  store.getters['auth/isAdmin'] || store.getters['auth/isManager']
)

const title = computed(() => {
  switch (route.path) {
    case '/dashboard':
      return 'Панель управления'
    case '/activity':
      return 'Активность'
    case '/reports':
      return 'Отчёты'
    case '/employees':
      return 'Сотрудники'
    default:
      return ''
  }
})

const handleLogout = async () => {
  await store.dispatch('auth/logout')
  router.push('/login')
}

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
  transition: width 0.3s ease;
  position: fixed;
  height: 100vh;
  z-index: 100;
}

.sidebar-collapsed {
  width: 50px;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  margin-bottom: 20px;
}

nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

nav ul li {
  margin-bottom: 15px;
}

nav ul li a {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 4px;
  transition: all 0.3s;
}

nav ul li a:hover {
  background-color: #34495e;
}

.active-link {
  background-color: #34495e;
  font-weight: bold;
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-left: 250px;
  transition: margin-left 0.3s ease;
}

.expanded {
  margin-left: 60px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

button {
  padding: 8px 16px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #cc0000;
}
</style>
