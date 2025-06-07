<template>
  <div class="employee-list">
    <h2>Список сотрудников</h2>
    
    <div class="filters">
      <select v-model="departmentFilter" class="filter-select">
        <option value="">Все отделы</option>
        <option v-for="dept in departments" :key="dept" :value="dept">
          {{ dept }}
        </option>
      </select>
    </div>

    <table>
      <thead>
        <tr>
          <th>Имя</th>
          <th>Отдел</th>
          <th>Статус</th>
          <th>Время работы сегодня</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="employee in filteredEmployees" :key="employee.id">
          <td>{{ employee.name }}</td>
          <td>{{ employee.department }}</td>
          <td>
            <span :class="['status', employee.isActive ? 'active' : 'inactive']">
              {{ employee.isActive ? 'Активен' : 'Неактивен' }}
            </span>
          </td>
          <td>{{ employee.workTime }}</td>
          <td>
            <button @click="viewDetails(employee.id)" class="btn-details">
              Подробнее
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Временные данные для демонстрации
const employees = ref([
  { 
    id: 1, 
    name: 'Иван Петров', 
    department: 'Разработка', 
    isActive: true,
    workTime: '6ч 30м' 
  },
  { 
    id: 2, 
    name: 'Анна Сидорова', 
    department: 'Маркетинг', 
    isActive: false,
    workTime: '4ч 15м' 
  }
])

const departments = ['Разработка', 'Маркетинг', 'Продажи']
const departmentFilter = ref('')

const filteredEmployees = computed(() => {
  if (!departmentFilter.value) return employees.value
  return employees.value.filter(emp => emp.department === departmentFilter.value)
})

const viewDetails = (employeeId) => {
  router.push(`/employee/${employeeId}`)
}
</script>

<style scoped>
.employee-list {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
}

.filter-select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
}

.status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.9em;
}

.active {
  background-color: #e6f4ea;
  color: #1e7e34;
}

.inactive {
  background-color: #fbe9e7;
  color: #d32f2f;
}

.btn-details {
  padding: 6px 12px;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-details:hover {
  background-color: #1565c0;
}
</style>