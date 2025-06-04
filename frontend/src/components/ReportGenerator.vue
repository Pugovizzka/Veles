<template>
  <div class="report-generator">
    <h2>Генерация отчета</h2>
    
    <div class="filters">
      <div class="filter-group">
        <label>Период:</label>
        <div class="date-inputs">
          <input 
            type="date" 
            v-model="filters.startDate"
            class="date-input"
          >
          <span>до</span>
          <input 
            type="date" 
            v-model="filters.endDate"
            class="date-input"
          >
        </div>
      </div>

      <div class="filter-group">
        <label>Отдел:</label>
        <select v-model="filters.department">
          <option value="">Все отделы</option>
          <option v-for="dept in departments" :key="dept" :value="dept">
            {{ dept }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label>Сотрудник:</label>
        <select v-model="filters.employeeId">
          <option value="">Все сотрудники</option>
          <option v-for="emp in employees" :key="emp.id" :value="emp.id">
            {{ emp.name }}
          </option>
        </select>
      </div>
    </div>

    <div class="buttons">
      <button @click="generateReport" :disabled="loading" class="generate-btn">
        {{ loading ? 'Формирование...' : 'Сформировать отчет' }}
      </button>
      
      <button 
        @click="downloadExcel" 
        :disabled="!report || loading" 
        class="download-btn"
      >
        Скачать Excel
      </button>
    </div>

    <div v-if="report" class="report-results">
      <h3>Результаты</h3>
      
      <table>
        <thead>
          <tr>
            <th>Сотрудник</th>
            <th>Отдел</th>
            <th>Общее время</th>
            <th>Активное время</th>
            <th>Приложения</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in report.items" :key="item.employeeId">
            <td>{{ item.employeeName }}</td>
            <td>{{ item.department }}</td>
            <td>{{ formatDuration(item.totalTime) }}</td>
            <td>{{ formatDuration(item.activeTime) }}</td>
            <td>
              <ul class="apps-list">
                <li v-for="(time, app) in item.apps" :key="app">
                  {{ app }}: {{ formatDuration(time) }}
                </li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="report-summary">
        <p>Общее время по отделу: {{ formatDuration(report.totalDepartmentTime) }}</p>
        <p>Среднее время на сотрудника: {{ formatDuration(report.averageEmployeeTime) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

const departments = ['Разработка', 'Маркетинг', 'Продажи']
const employees = ref([])
const report = ref(null)
const loading = ref(false)

const filters = reactive({
  startDate: '',
  endDate: '',
  department: '',
  employeeId: ''
})

const formatDuration = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return `${hours}ч ${mins}м`
}

const generateReport = async () => {
  loading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/report', {
      params: filters
    })
    report.value = response.data
  } catch (error) {
    console.error('Error generating report:', error)
  } finally {
    loading.value = false
  }
}

const downloadExcel = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/export-excel', {
      params: filters,
      responseType: 'blob'
    })
    
    // Создаем ссылку для скачивания
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `report_${filters.startDate}_${filters.endDate}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error downloading Excel:', error)
  }
}

// Загрузка списка сотрудников при монтировании компонента
const loadEmployees = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/employees')
    employees.value = response.data
  } catch (error) {
    console.error('Error loading employees:', error)
  }
}

loadEmployees()
</script>

<style scoped>
.report-generator {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filters {
  display: grid;
  gap: 20px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}

.buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.generate-btn, .download-btn {
  flex: 1;
  padding: 12px;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.generate-btn {
  background-color: #4CAF50;
}

.download-btn {
  background-color: #2196F3;
}

.generate-btn:disabled, .download-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
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

.apps-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.apps-list li {
  margin-bottom: 4px;
}

.report-summary {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}
</style>