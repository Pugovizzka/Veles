<template>
  <div class="activity-stats-container">
    <div class="activity-stats">
      <div class="stats-header">
        <h2>Статистика активности сотрудников</h2>
        <div class="filters">
          <select v-model="selectedPeriod" @change="loadActivityData" class="period-select">
            <option value="today">Сегодня</option>
            <option value="yesterday">Вчера</option>
            <option value="week">Эта неделя</option>
            <option value="month">Этот месяц</option>
            <option value="custom">Выбрать период</option>
          </select>
          <div v-if="selectedPeriod === 'custom'" class="date-range">
            <input 
              type="date" 
              v-model="customStartDate" 
              @change="loadActivityData"
              class="date-input"
            />
            <span>—</span>
            <input 
              type="date" 
              v-model="customEndDate" 
              @change="loadActivityData"
              class="date-input"
            />
          </div>
        </div>
      </div>

      <!-- Общая статистика -->
      <div class="summary-cards">
        <div class="summary-card">
          <div class="card-icon">👥</div>
          <div class="card-content">
            <h3>Активных сотрудников</h3>
            <p class="card-value">{{ activeEmployees }}</p>
          </div>
        </div>
        <div class="summary-card">
          <div class="card-icon">⏱️</div>
          <div class="card-content">
            <h3>Общее время работы</h3>
            <p class="card-value">{{ totalWorkTime }}</p>
          </div>
        </div>
        <div class="summary-card">
          <div class="card-icon">📊</div>
          <div class="card-content">
            <h3>Средняя продуктивность</h3>
            <p class="card-value">{{ averageProductivity }}%</p>
          </div>
        </div>
      </div>

      <!-- Временная диаграмма активности (горизонтальная) -->
      <div class="chart-section">
        <h3>Активность по времени ({{ getPeriodLabel() }})</h3>
        <div class="time-chart">
          <div class="chart-container">
            <!-- Горизонтальная шкала времени -->
            <div class="time-scale">
              <div 
                v-for="hour in 24" 
                :key="hour"
                class="time-marker"
                :style="{ left: ((hour - 1) / 24 * 100) + '%' }"
              >
                {{ String(hour - 1).padStart(2, '0') }}:00
              </div>
            </div>
            
            <!-- Сотрудники и их временные линии -->
            <div class="employees-timeline">
              <div 
                v-for="employee in employeeStats" 
                :key="employee.id" 
                class="employee-row"
              >
                <div class="employee-label">
                  <div class="employee-avatar">
                    {{ employee.name.charAt(0) }}
                  </div>
                  <div class="employee-details">
                    <span class="employee-name">{{ employee.name }}</span>
                    <span class="employee-dept">{{ employee.department }}</span>
                  </div>
                </div>
                <div class="timeline-container">
                  <div class="timeline-background"></div>
                  <div 
                    v-for="(activity, index) in employee.timeline" 
                    :key="index"
                    class="activity-segment"
                    :class="activity.type"
                    :style="getActivityStyle(activity)"
                    :title="`${activity.app} (${activity.startTime} - ${activity.endTime})`"
                  >
                    <span class="activity-label">{{ activity.app }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Легенда -->
        <div class="chart-legend">
          <div class="legend-item">
            <div class="legend-color work"></div>
            <span>Рабочее время</span>
          </div>
          <div class="legend-item">
            <div class="legend-color break"></div>
            <span>Перерывы</span>
          </div>
          <div class="legend-item">
            <div class="legend-color meeting"></div>
            <span>Встречи</span>
          </div>
        </div>
      </div>

      <!-- Детальная статистика по сотрудникам -->
      <div class="detailed-stats">
        <h3>Детальная статистика</h3>
        <div class="employee-cards">
          <div 
            v-for="employee in employeeStats" 
            :key="employee.id" 
            class="employee-card"
          >
            <div class="employee-header">
              <div class="employee-avatar large">
                {{ employee.name.charAt(0) }}
              </div>
              <div class="employee-info">
                <h4>{{ employee.name }}</h4>
                <p>{{ employee.department }}</p>
              </div>
              <div class="employee-status" :class="employee.status">
                {{ employee.status === 'active' ? 'Активен' : 'Неактивен' }}
              </div>
            </div>
            
            <div class="employee-metrics">
              <div class="metric">
                <span class="metric-label">Время работы:</span>
                <span class="metric-value">{{ employee.workTime }}</span>
              </div>
              <div class="metric">
                <span class="metric-label">Продуктивность:</span>
                <span class="metric-value">{{ employee.productivity }}%</span>
              </div>
              <div class="metric">
                <span class="metric-label">Перерывы:</span>
                <span class="metric-value">{{ employee.breaks }}</span>
              </div>
            </div>

            <!-- Мини-диаграмма приложений -->
            <div class="app-usage">
              <h5>Использование приложений</h5>
              <div class="app-bars">
                <div 
                  v-for="app in employee.topApps" 
                  :key="app.name" 
                  class="app-bar"
                >
                  <span class="app-name">{{ app.name }}</span>
                  <div class="app-progress">
                    <div 
                      class="app-fill" 
                      :style="{ width: app.percentage + '%' }"
                    ></div>
                  </div>
                  <span class="app-time">{{ app.time }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Статистика по отделам -->
      <div class="department-stats">
        <h3>Статистика по отделам</h3>
        <div class="department-chart">
          <div 
            v-for="dept in departmentStats" 
            :key="dept.name" 
            class="department-bar"
          >
            <div class="dept-info">
              <span class="dept-name">{{ dept.name }}</span>
              <span class="dept-time">{{ dept.totalTime }}</span>
            </div>
            <div class="dept-progress">
              <div 
                class="dept-fill" 
                :style="{ width: dept.percentage + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const selectedPeriod = ref('today')
const customStartDate = ref('')
const customEndDate = ref('')

// Демонстрационные данные - 3 активных сотрудника
const employeeStats = ref([
  {
    id: 1,
    name: 'Иван Петров',
    department: 'Разработка',
    status: 'active',
    workTime: '7ч 45м',
    productivity: 85,
    breaks: '45м',
    timeline: [
      { type: 'work', app: 'VS Code', startTime: '09:00', endTime: '10:30', start: 9, duration: 1.5 },
      { type: 'break', app: 'Перерыв', startTime: '10:30', endTime: '10:45', start: 10.5, duration: 0.25 },
      { type: 'work', app: 'Chrome', startTime: '10:45', endTime: '12:00', start: 10.75, duration: 1.25 },
      { type: 'break', app: 'Обед', startTime: '12:00', endTime: '13:00', start: 12, duration: 1 },
      { type: 'work', app: 'VS Code', startTime: '13:00', endTime: '15:30', start: 13, duration: 2.5 },
      { type: 'meeting', app: 'Zoom', startTime: '15:30', endTime: '16:30', start: 15.5, duration: 1 },
      { type: 'work', app: 'VS Code', startTime: '16:30', endTime: '18:00', start: 16.5, duration: 1.5 }
    ],
    topApps: [
      { name: 'VS Code', time: '5ч 30м', percentage: 70 },
      { name: 'Chrome', time: '1ч 15м', percentage: 16 },
      { name: 'Zoom', time: '1ч', percentage: 14 }
    ]
  },
  {
    id: 2,
    name: 'Анна Сидорова',
    department: 'Дизайн',
    status: 'active',
    workTime: '8ч 15м',
    productivity: 92,
    breaks: '30м',
    timeline: [
      { type: 'work', app: 'Figma', startTime: '09:00', endTime: '11:00', start: 9, duration: 2 },
      { type: 'break', app: 'Перерыв', startTime: '11:00', endTime: '11:15', start: 11, duration: 0.25 },
      { type: 'work', app: 'Photoshop', startTime: '11:15', endTime: '12:30', start: 11.25, duration: 1.25 },
      { type: 'break', app: 'Обед', startTime: '12:30', endTime: '13:30', start: 12.5, duration: 1 },
      { type: 'work', app: 'Figma', startTime: '13:30', endTime: '16:00', start: 13.5, duration: 2.5 },
      { type: 'meeting', app: 'Teams', startTime: '16:00', endTime: '16:45', start: 16, duration: 0.75 },
      { type: 'work', app: 'Figma', startTime: '16:45', endTime: '18:00', start: 16.75, duration: 1.25 }
    ],
    topApps: [
      { name: 'Figma', time: '5ч 45м', percentage: 75 },
      { name: 'Photoshop', time: '1ч 15м', percentage: 15 },
      { name: 'Teams', time: '45м', percentage: 10 }
    ]
  },
  {
    id: 3,
    name: 'Михаил Козлов',
    department: 'Маркетинг',
    status: 'active',
    workTime: '6ч 30м',
    productivity: 78,
    breaks: '1ч 15м',
    timeline: [
      { type: 'work', app: 'Excel', startTime: '09:30', endTime: '11:00', start: 9.5, duration: 1.5 },
      { type: 'break', app: 'Перерыв', startTime: '11:00', endTime: '11:30', start: 11, duration: 0.5 },
      { type: 'work', app: 'PowerPoint', startTime: '11:30', endTime: '12:30', start: 11.5, duration: 1 },
      { type: 'break', app: 'Обед', startTime: '12:30', endTime: '14:00', start: 12.5, duration: 1.5 },
      { type: 'work', app: 'Chrome', startTime: '14:00', endTime: '16:00', start: 14, duration: 2 },
      { type: 'meeting', app: 'Zoom', startTime: '16:00', endTime: '17:00', start: 16, duration: 1 }
    ],
    topApps: [
      { name: 'Excel', time: '2ч 30м', percentage: 40 },
      { name: 'Chrome', time: '2ч', percentage: 32 },
      { name: 'PowerPoint', time: '1ч', percentage: 16 },
      { name: 'Zoom', time: '1ч', percentage: 12 }
    ]
  }
])

const departmentStats = ref([
  { name: 'Разработка', totalTime: '15ч 30м', percentage: 45 },
  { name: 'Дизайн', totalTime: '12ч 15м', percentage: 35 },
  { name: 'Маркетинг', totalTime: '8ч 45м', percentage: 25 },
  { name: 'Продажи', totalTime: '6ч 30м', percentage: 20 }
])

// Вычисляемые свойства для общей статистики
const activeEmployees = computed(() => 
  employeeStats.value.filter(emp => emp.status === 'active').length
)

const totalWorkTime = computed(() => {
  const total = employeeStats.value.reduce((sum, emp) => {
    const [hours, minutes] = emp.workTime.split('ч ').map(t => parseInt(t))
    return sum + hours + (minutes || 0) / 60
  }, 0)
  return `${Math.floor(total)}ч ${Math.round((total % 1) * 60)}м`
})

const averageProductivity = computed(() => {
  const avg = employeeStats.value.reduce((sum, emp) => sum + emp.productivity, 0) / employeeStats.value.length
  return Math.round(avg)
})

// Функция для стилизации блоков активности (горизонтальная)
const getActivityStyle = (activity) => {
  const startPercent = (activity.start / 24) * 100
  const widthPercent = (activity.duration / 24) * 100
  
  return {
    left: `${startPercent}%`,
    width: `${widthPercent}%`
  }
}

const getPeriodLabel = () => {
  switch (selectedPeriod.value) {
    case 'today': return 'Сегодня'
    case 'yesterday': return 'Вчера'
    case 'week': return 'Эта неделя'
    case 'month': return 'Этот месяц'
    case 'custom': return `${customStartDate.value} — ${customEndDate.value}`
    default: return 'Сегодня'
  }
}

const loadActivityData = () => {
  // Здесь будет загрузка данных с сервера в зависимости от выбранного периода
  console.log('Загрузка данных за период:', selectedPeriod.value)
  if (selectedPeriod.value === 'custom') {
    console.log('Период:', customStartDate.value, 'до', customEndDate.value)
  }
}

onMounted(() => {
  // Устанавливаем даты по умолчанию для custom периода
  const today = new Date()
  const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)
  
  customStartDate.value = weekAgo.toISOString().split('T')[0]
  customEndDate.value = today.toISOString().split('T')[0]
  
  loadActivityData()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.activity-stats-container {
  font-family: 'Gabarito', sans-serif;
  color: rgba(243, 238, 232, 1);
}

.activity-stats {
  background: rgba(19, 24, 27, 1);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(243, 238, 232, 0.1);
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(243, 238, 232, 0.2);
  flex-wrap: wrap;
  gap: 20px;
}

.stats-header h2 {
  margin: 0;
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
}

.filters {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.period-select,
.date-input {
  padding: 10px 15px;
  border: 1px solid rgba(243, 238, 232, 0.3);
  border-radius: 8px;
  background: rgba(58, 60, 65, 1);
  color: rgba(243, 238, 232, 1);
  font-family: 'Gabarito', sans-serif;
  font-size: 14px;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-range span {
  color: rgba(243, 238, 232, 0.7);
}

/* Карточки общей статистики */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.summary-card {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-5px);
}

.card-icon {
  font-size: 2.5rem;
  background: rgba(131, 21, 21, 0.2);
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-content h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 500;
  color: rgba(243, 238, 232, 0.8);
}

.card-value {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: rgba(243, 238, 232, 1);
}

/* Временная диаграмма (горизонтальная) */
.chart-section {
  margin-bottom: 40px;
}

.chart-section h3 {
  margin-bottom: 20px;
  font-weight: 600;
}

.time-chart {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 25px;
  overflow-x: auto;
}

.chart-container {
  position: relative;
  min-width: 900px;
}

/* Горизонтальная шкала времени */
.time-scale {
  position: relative;
  height: 30px;
  margin-bottom: 20px;
  border-bottom: 2px solid rgba(243, 238, 232, 0.2);
}

.time-marker {
  position: absolute;
  font-size: 12px;
  color: rgba(243, 238, 232, 0.6);
  transform: translateX(-50%);
  white-space: nowrap;
}

.time-marker::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 1px;
  height: 10px;
  background: rgba(243, 238, 232, 0.3);
}

/* Временные линии сотрудников */
.employees-timeline {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.employee-row {
  display: flex;
  align-items: center;
  gap: 20px;
}

.employee-label {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 200px;
  flex-shrink: 0;
}

.employee-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(131, 21, 21, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: rgba(243, 238, 232, 1);
}

.employee-avatar.large {
  width: 50px;
  height: 50px;
  font-size: 18px;
}

.employee-details {
  display: flex;
  flex-direction: column;
}

.employee-name {
  font-weight: 600;
  font-size: 14px;
  line-height: 1.2;
}

.employee-dept {
  font-size: 12px;
  color: rgba(243, 238, 232, 0.7);
  line-height: 1.2;
}

.timeline-container {
  flex: 1;
  position: relative;
  height: 50px;
}

.timeline-background {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 30px;
  transform: translateY(-50%);
  background: rgba(19, 24, 27, 1);
  border-radius: 15px;
  border: 1px solid rgba(243, 238, 232, 0.1);
}

.activity-segment {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  height: 30px;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.activity-segment:hover {
  transform: translateY(-50%) scale(1.05);
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.activity-label {
  font-size: 11px;
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 0 8px;
}

.activity-segment.work {
  background: linear-gradient(135deg, #4CAF50, #45a049);
}

.activity-segment.break {
  background: linear-gradient(135deg, #FF9800, #F57C00);
}

.activity-segment.meeting {
  background: linear-gradient(135deg, #2196F3, #1976D2);
}

/* Легенда */
.chart-legend {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(243, 238, 232, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 8px;
}

.legend-color.work {
  background: linear-gradient(135deg, #4CAF50, #45a049);
}

.legend-color.break {
  background: linear-gradient(135deg, #FF9800, #F57C00);
}

.legend-color.meeting {
  background: linear-gradient(135deg, #2196F3, #1976D2);
}

/* Детальная статистика */
.detailed-stats {
  margin-bottom: 40px;
}

.detailed-stats h3 {
  margin-bottom: 20px;
  font-weight: 600;
}

.employee-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.employee-card {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 25px;
  transition: transform 0.3s ease;
}

.employee-card:hover {
  transform: translateY(-3px);
}

.employee-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.employee-info h4 {
  margin: 0 0 5px 0;
  font-weight: 600;
}

.employee-info p {
  margin: 0;
  color: rgba(243, 238, 232, 0.7);
  font-size: 14px;
}

.employee-status {
  margin-left: auto;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.employee-status.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
}

.employee-status.inactive {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.employee-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.metric-label {
  font-size: 12px;
  color: rgba(243, 238, 232, 0.7);
}

.metric-value {
  font-weight: 600;
  font-size: 16px;
}

/* Использование приложений */
.app-usage h5 {
  margin: 0 0 15px 0;
  font-weight: 600;
  font-size: 14px;
}

.app-bars {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.app-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}

.app-name {
  width: 80px;
  font-weight: 500;
}

.app-progress {
  flex: 1;
  height: 6px;
  background: rgba(19, 24, 27, 1);
  border-radius: 3px;
  overflow: hidden;
}

.app-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #45a049);
  transition: width 0.3s ease;
}

.app-time {
  width: 50px;
  text-align: right;
  color: rgba(243, 238, 232, 0.8);
}

/* Статистика по отделам */
.department-stats h3 {
  margin-bottom: 20px;
  font-weight: 600;
}

.department-chart {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 25px;
}

.department-bar {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.department-bar:last-child {
  margin-bottom: 0;
}

.dept-info {
  display: flex;
  justify-content: space-between;
  width: 200px;
}

.dept-name {
  font-weight: 600;
}

.dept-time {
  color: rgba(243, 238, 232, 0.8);
}

.dept-progress {
  flex: 1;
  height: 12px;
  background: rgba(19, 24, 27, 1);
  border-radius: 6px;
  overflow: hidden;
}

.dept-fill {
  height: 100%;
  background: linear-gradient(90deg, rgba(131, 21, 21, 1), rgba(151, 31, 31, 1));
  transition: width 0.3s ease;
}

/* Адаптивность */
@media (max-width: 1200px) {
  .chart-container {
    min-width: 800px;
  }
  
  .employee-label {
    width: 160px;
  }
  
  .employee-name {
    font-size: 13px;
  }
  
  .employee-dept {
    font-size: 11px;
  }
}

@media (max-width: 768px) {
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .employee-cards {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    min-width: 600px;
  }
  
  .employee-label {
    width: 120px;
  }
  
  .employee-name {
    font-size: 12px;
  }
  
  .employee-dept {
    font-size: 10px;
  }
  
  .stats-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters {
    justify-content: center;
  }
  
  .chart-legend {
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }
}
</style>