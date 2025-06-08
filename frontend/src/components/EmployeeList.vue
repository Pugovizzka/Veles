<template>
  <div class="employee-list-container">
    <div class="employee-list">
      <div class="employee-header">
        <h2>Список сотрудников</h2>
        <button class="btn-add" @click="showCreateModal = true">+</button>
      </div>

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

      <!-- Модальное окно создания сотрудника -->
      <div v-if="showCreateModal" class="modal-overlay">
        <div class="modal">
          <h3>Создание пользователя</h3>
          <label>ФИО</label>
          <input v-model="form.name" type="text" />

          <label>Email (логин)</label>
          <input v-model="form.email" type="email" />

          <label>Пароль</label>
          <input v-model="form.password" type="password" />

          <label>Роль</label>
          <select v-model="form.role">
            <option value="EMPLOYEE">Сотрудник</option>
            <option value="MANAGER">Менеджер</option>
          </select>

          <label>Отдел</label>
          <select v-model="form.department">
            <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
          </select>

          <div class="modal-actions">
            <button class="btn-details" @click="createUser">Создать</button>
            <button class="btn-cancel" @click="showCreateModal = false">Отменить</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const employees = ref([
  { id: 1, name: 'Иван Петров', department: 'Разработка', isActive: true, workTime: '6ч 30м' },
  { id: 2, name: 'Анна Сидорова', department: 'Маркетинг', isActive: false, workTime: '4ч 15м' }
])

const departments = ['Разработка', 'Маркетинг', 'Продажи']
const departmentFilter = ref('')
const showCreateModal = ref(false)
const form = ref({
  name: '',
  email: '',
  password: '',
  role: 'EMPLOYEE',
  department: ''
})

const filteredEmployees = computed(() => {
  if (!departmentFilter.value) return employees.value
  return employees.value.filter(emp => emp.department === departmentFilter.value)
})

const viewDetails = (employeeId) => {
  router.push(`/employee/${employeeId}`)
}

const createUser = async () => {
  try {
    await axios.post(`${process.env.VUE_APP_BACKEND_API_URL}/users`, form.value)
    alert('Пользователь создан')
    showCreateModal.value = false
    // Обновляем список сотрудников
    const response = await axios.get(`${process.env.VUE_APP_BACKEND_API_URL}/employees`)
    employees.value = response.data
  } catch (e) {
    alert('Ошибка создания пользователя: ' + (e.response?.data?.detail || e.response?.data?.error || e.message))
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.employee-list-container {
  display: flex;
  justify-content: center;
  font-family: 'Gabarito', sans-serif;
}

.employee-list {
  background: rgba(19, 24, 27, 1);
  padding: 40px;
  border-radius: 16px;
  max-width: 1000px;
  width: 100%;
  color: rgba(243, 238, 232, 1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(243, 238, 232, 0.1);
}

.employee-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-add {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
}

.filters {
  margin-bottom: 20px;
}

.filter-select {
  padding: 10px;
  border-radius: 6px;
  border: none;
  width: 100%;
  background-color: #2a2e35;
  color: rgba(243, 238, 232, 1);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  background-color: #2a2e35;
  border-radius: 12px;
  overflow: hidden;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid rgba(243, 238, 232, 0.1);
}

th {
  background-color: #343a40;
  font-weight: 700;
}

.status {
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.9em;
  font-weight: 600;
}

.active {
  background-color: rgba(76, 175, 80, 0.15);
  color: #4CAF50;
}

.inactive {
  background-color: rgba(244, 67, 54, 0.15);
  color: #f44336;
}

.btn-details {
  padding: 8px 16px;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.btn-details:hover {
  background-color: #4CAF50;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal {
  background: #2a2e35;
  padding: 30px;
  border-radius: 12px;
  color: white;
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal input, .modal select {
  padding: 8px;
  border-radius: 6px;
  border: none;
  background: #444;
  color: white;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn-cancel {
  background-color: rgba(131, 21, 21, 1);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}
</style>
