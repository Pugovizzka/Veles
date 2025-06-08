<template>
  <div class="report-generator-container">
    <div class="report-generator">
      <h2>Генерация отчета</h2>

      <div class="filters">
        <div class="filter-group">
          <label>Период:</label>
          <div class="date-inputs">
            <input type="date" v-model="filters.startDate" class="date-input" />
            <span>до</span>
            <input type="date" v-model="filters.endDate" class="date-input" />
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
        <button @click="downloadExcel" :disabled="!report || loading" class="download-btn">
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
    const response = await axios.get('http://127.0.0.1:8000/report', { params: filters })
    report.value = response.data
  } catch (error) {
    console.error('Ошибка при формировании отчета:', error)
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

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `report_${filters.startDate}_${filters.endDate}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Ошибка при загрузке Excel:', error)
  }
}

const loadEmployees = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/employees')
    employees.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки сотрудников:', error)
  }
}

loadEmployees()
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.report-generator-container {
  display: flex;
  justify-content: center;
  font-family: 'Gabarito', sans-serif;
}

.report-generator {
  background: rgba(19, 24, 27, 1);
  padding: 40px;
  border-radius: 16px;
  max-width: 1000px;
  width: 100%;
  color: rgba(243, 238, 232, 1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(243, 238, 232, 0.1);
}

.report-generator h2 {
  font-weight: 600;
  margin-bottom: 30px;
  color: rgba(243, 238, 232, 1);
}

.filters {
  display: grid;
  gap: 20px;
  margin-bottom: 30px;
}

.filter-group label {
  font-weight: 600;
  margin-bottom: 8px;
  display: block;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-input,
select {
  padding: 10px;
  border: none;
  border-radius: 6px;
  width: 100%;
  font-size: 15px;
  background: #2a2e35;
  color: rgba(243, 238, 232, 1);
}

.buttons {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.generate-btn,
.download-btn {
  flex: 1;
  padding: 15px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Gabarito', sans-serif;
}

.generate-btn {
  background-color: #4CAF50;
  color: rgba(243, 238, 232, 1);
}

.generate-btn:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.download-btn {
  background-color: #2196F3;
  color: rgba(243, 238, 232, 1);
}

.download-btn:hover {
  background-color: #1976D2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.4);
}

.report-results h3 {
  margin-top: 30px;
  font-weight: 600;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
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
  padding: 20px;
  background: rgba(58, 60, 65, 1);
  border-radius: 8px;
  font-weight: 500;
}
</style>
