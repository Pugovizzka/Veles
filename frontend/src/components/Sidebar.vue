<template>
  <div class="sidebar" :class="{ 'sidebar-collapsed': isCollapsed }">
    <button class="toggle-btn" @click="toggleSidebar">
      {{ isCollapsed ? '☰' : '✕' }}
    </button>
    <nav>
      <ul>
        <li>
          <router-link to="/dashboard" active-class="active-link">
            <span v-if="!isCollapsed">Главная</span>
          </router-link>
        </li>
        <li>
          <router-link to="/employees" active-class="active-link">
            <span v-if="!isCollapsed">Список сотрудников</span>
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isCollapsed = ref(false)

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.sidebar {
  width: 200px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
  transition: width 0.3s ease;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
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
  transition: background-color 0.3s;
}

nav ul li a:hover {
  background-color: #34495e;
}

.active-link {
  background-color: #34495e;
  font-weight: bold;
}
</style>