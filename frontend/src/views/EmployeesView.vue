<template>
  <div class="employees-page">
    <div class="header">
      <h1>Управление сотрудниками</h1>
      <div class="user-info">
        <p>{{ user?.email }}</p>
        <button @click="handleLogout" class="btn-logout">Выйти</button>
      </div>
    </div>
    <EmployeeList />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import EmployeeList from '@/components/EmployeeList.vue'

const store = useStore()
const router = useRouter()

const user = computed(() => store.getters['auth/currentUser'])

const handleLogout = async () => {
  await store.dispatch('auth/logout')
  router.push('/login')
}
</script>

<style scoped>
.employees-page {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.btn-logout {
  padding: 8px 16px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-logout:hover {
  background-color: #cc0000;
}
</style>