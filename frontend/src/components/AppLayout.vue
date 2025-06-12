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
            <router-link to="/dashboard" active-class="active-link" exact>
              <span v-if="!sidebarCollapsed">Главная</span>
            </router-link>
          </li>
          <li>
            <router-link to="/activity" active-class="active-link">
              <span v-if="!sidebarCollapsed">Активность</span>
            </router-link>
          </li>
          <li v-if="isAdminOrManager">
            <router-link to="/activity-stats" active-class="active-link">
              <span v-if="!sidebarCollapsed">Статистика</span>
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
          <li>
            <router-link to="/profile" active-class="active-link">
              <span v-if="!sidebarCollapsed">Профиль</span>
            </router-link>
          </li>
        </ul>
      </nav>

      <!-- Кнопка выхода и инфо -->
      <div v-if="!sidebarCollapsed" class="sidebar-footer">
        <div class="user-info-sidebar">
          <div class="user-avatar-small">
            {{ user?.name?.charAt(0) || 'U' }}
          </div>
          <div class="user-details">
            <p class="user-name">{{ user?.name || 'Пользователь' }}</p>
            <p class="user-email">{{ user?.email }}</p>
          </div>
          <button @click="handleLogout" class="logout-btn">Выйти</button>
        </div>
      </div>
      
      <!-- Компактная версия для collapsed состояния -->
      <div v-if="sidebarCollapsed" class="sidebar-footer-collapsed">
        <div class="user-avatar-small">
          {{ user?.name?.charAt(0) || 'U' }}
        </div>
        <button @click="handleLogout" class="logout-btn-small" title="Выйти">
          🚪
        </button>
      </div>
    </div>

    <!-- Основное содержимое -->
    <div class="main-content" :class="{ 'expanded': sidebarCollapsed }">
      <div class="header">
        <h1>{{ title }}</h1>
      </div>
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
    case '/activity-stats':
      return 'Статистика активности'
    case '/reports':
      return 'Отчёты'
    case '/employees':
      return 'Сотрудники'
    case '/profile':
      return 'Личный кабинет'
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
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.app-layout {
  display: flex;
  min-height: 100vh;
  font-family: 'Gabarito', sans-serif;
}

.sidebar {
  width: 220px;
  background: rgba(19, 24, 27, 1);
  color: rgba(243, 238, 232, 1);
  padding: 20px;
  transition: width 0.3s ease;
  position: fixed;
  height: 100vh;
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.sidebar-collapsed {
  width: 60px;
}

.toggle-btn {
  background: rgba(131, 21, 21, 1);
  border: none;
  color: rgba(243, 238, 232, 1);
  font-size: 1.5rem;
  cursor: pointer;
  margin-bottom: 20px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background: rgba(151, 31, 31, 1);
  transform: scale(1.05);
}

.sidebar-collapsed .toggle-btn {
  margin: 0 auto 20px auto;
  padding: 6px 10px;
  display: block;
}

nav {
  flex: 1;
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
  color: rgba(243, 238, 232, 1);
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.3s;
  font-weight: 500;
}

.sidebar-collapsed nav ul li a {
  justify-content: center;
  padding: 12px 8px;
}

.sidebar-collapsed nav ul li a span {
  display: none;
}

nav ul li a:hover {
  background-color: rgba(39, 44, 47, 1);
  transform: translateX(5px);
}

.sidebar-collapsed nav ul li a:hover {
  transform: scale(1.1);
}

.active-link {
  background-color: rgba(39, 44, 47, 1);
  font-weight: 600;
  border-left: 3px solid rgba(131, 21, 21, 1);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid rgba(243, 238, 232, 0.2);
}

.sidebar-footer-collapsed {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid rgba(243, 238, 232, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.user-info-sidebar {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.user-avatar-small {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(131, 21, 21, 1), rgba(151, 31, 31, 1));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: rgba(243, 238, 232, 1);
  margin: 0 auto;
}

.user-details {
  text-align: center;
}

.user-name {
  color: rgba(243, 238, 232, 1);
  margin: 0 0 5px 0;
  font-weight: 600;
  font-size: 14px;
}

.user-email {
  color: rgba(243, 238, 232, 0.7);
  margin: 0;
  font-size: 12px;
  word-break: break-word;
}

.logout-btn {
  padding: 8px 16px;
  background-color: rgba(131, 21, 21, 1);
  color: rgba(243, 238, 232, 1);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Gabarito', sans-serif;
  font-weight: 500;
  font-size: 14px;
  width: 100%;
}

.logout-btn:hover {
  background-color: rgba(151, 31, 31, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.logout-btn-small {
  padding: 8px;
  background-color: rgba(131, 21, 21, 1);
  color: rgba(243, 238, 232, 1);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
}

.logout-btn-small:hover {
  background-color: rgba(151, 31, 31, 1);
  transform: scale(1.1);
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-left: 220px;
  transition: margin-left 0.3s ease;
  background: rgba(58, 60, 65, 1);
  color: rgba(243, 238, 232, 1);
  min-height: 100vh;
}

.expanded {
  margin-left: 60px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(243, 238, 232, 0.2);
}

.header h1 {
  color: rgba(243, 238, 232, 1);
  font-weight: 600;
  margin: 0;
}

/* Адаптивность */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  .sidebar-collapsed {
    width: 100%;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .expanded {
    margin-left: 0;
  }
}
</style>
