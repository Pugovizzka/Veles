<template>
  <div class="dashboard">
    <h1>Панель управления</h1>
    <div class="user-info">
      <p>Добро пожаловать, {{ user?.email }}</p>
      <button @click="handleLogout">Выйти</button>
    </div>
    <WorkTimer />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import WorkTimer from '@/components/WorkTimer.vue'

const store = useStore()
const router = useRouter()

const user = computed(() => store.getters['auth/currentUser'])

const handleLogout = async () => {
  await store.dispatch('auth/logout')
  router.push('/login')
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #cc0000;
}
</style>