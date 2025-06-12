<template>
  <div class="activity-tracker-container">
    <div class="activity-tracker">
      <!-- Заголовок и статус -->
      <div class="tracker-header">
        <h2>Отслеживание активности</h2>
        <div class="tracking-status" :class="{ 'active': isTracking }">
          <span class="status-dot"></span>
          {{ isTracking ? 'Отслеживание активно' : 'Отслеживание остановлено' }}
        </div>
      </div>

      <!-- Управление отслеживанием -->
      <div class="tracking-controls">
        <button 
          @click="toggleTracking" 
          :class="['control-btn', isTracking ? 'stop' : 'start']"
        >
          {{ isTracking ? '⏹️ Остановить отслеживание' : '▶️ Начать отслеживание' }}
        </button>
        <button @click="refreshActivity" class="refresh-btn" :disabled="!isTracking">
          🔄 Обновить
        </button>
      </div>

      <!-- Текущая активность -->
      <div class="current-activity-section">
        <h3>Текущая активность</h3>
        <div v-if="currentActivity && isTracking" class="current-activity-card">
          <div class="activity-icon">
            {{ getAppIcon(currentActivity.app) }}
          </div>
          <div class="activity-details">
            <div class="activity-app">
              <strong>{{ currentActivity.app }}</strong>
              <span class="activity-pid" v-if="currentActivity.pid">
                (PID: {{ currentActivity.pid }})
              </span>
            </div>
            <div class="activity-title">{{ currentActivity.title }}</div>
            <div class="activity-duration">
              Активно: {{ formatDuration(currentSessionDuration) }}
            </div>
          </div>
          <div class="activity-status">
            <div class="pulse-indicator"></div>
          </div>
        </div>
        
        <div v-else-if="!isTracking" class="no-activity">
          <div class="no-activity-icon">⏸️</div>
          <p>Отслеживание приостановлено</p>
          <p class="no-activity-hint">Нажмите "Начать отслеживание" для мониторинга активности</p>
        </div>

        <div v-else class="loading-activity">
          <div class="loading-spinner"></div>
          <p>Получение данных об активности...</p>
        </div>
      </div>

      <!-- История активности за сегодня -->
      <div class="activity-history-section">
        <h3>История активности (сегодня)</h3>
        <div class="activity-timeline">
          <div 
            v-for="(activity, index) in todayActivities" 
            :key="index"
            class="timeline-item"
          >
            <div class="timeline-time">
              {{ formatTime(activity.startTime) }}
            </div>
            <div class="timeline-content">
              <div class="timeline-app">
                <span class="app-icon">{{ getAppIcon(activity.app) }}</span>
                <strong>{{ activity.app }}</strong>
              </div>
              <div class="timeline-title">{{ activity.title }}</div>
              <div class="timeline-duration">{{ activity.duration }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Статистика за день -->
      <div class="daily-stats-section">
        <h3>Статистика за сегодня</h3>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-content">
              <div class="stat-value">{{ dailyStats.totalTime }}</div>
              <div class="stat-label">Общее время</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">💻</div>
            <div class="stat-content">
              <div class="stat-value">{{ dailyStats.activeTime }}</div>
              <div class="stat-label">Активное время</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">📱</div>
            <div class="stat-content">
              <div class="stat-value">{{ dailyStats.appsCount }}</div>
              <div class="stat-label">Приложений</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
              <div class="stat-value">{{ dailyStats.productivity }}%</div>
              <div class="stat-label">Продуктивность</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Топ приложений -->
      <div class="top-apps-section">
        <h3>Топ приложений за сегодня</h3>
        <div class="apps-list">
          <div 
            v-for="(app, index) in topApps" 
            :key="app.name"
            class="app-item"
          >
            <div class="app-rank">#{{ index + 1 }}</div>
            <div class="app-icon-large">{{ getAppIcon(app.name) }}</div>
            <div class="app-details">
              <div class="app-name">{{ app.name }}</div>
              <div class="app-time">{{ app.time }}</div>
            </div>
            <div class="app-progress">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: app.percentage + '%' }"
                ></div>
              </div>
              <span class="progress-text">{{ app.percentage }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const currentActivity = ref(null)
const isTracking = ref(false)
const currentSessionDuration = ref(0)
const sessionStartTime = ref(null)

let trackingInterval = null
let durationInterval = null

// Демонстрационные данные для истории активности
const todayActivities = ref([
  {
    app: 'VS Code',
    title: 'main.py - employee-tracker',
    startTime: new Date(Date.now() - 3 * 60 * 60 * 1000), // 3 часа назад
    duration: '2ч 15м'
  },
  {
    app: 'Chrome',
    title: 'Vue.js Documentation',
    startTime: new Date(Date.now() - 2.5 * 60 * 60 * 1000),
    duration: '45м'
  },
  {
    app: 'Slack',
    title: 'Team Chat - Development',
    startTime: new Date(Date.now() - 2 * 60 * 60 * 1000),
    duration: '30м'
  },
  {
    app: 'Figma',
    title: 'UI Design - Dashboard',
    startTime: new Date(Date.now() - 1.5 * 60 * 60 * 1000),
    duration: '1ч 20м'
  },
  {
    app: 'Terminal',
    title: 'bash - project directory',
    startTime: new Date(Date.now() - 1 * 60 * 60 * 1000),
    duration: '25м'
  }
])

// Статистика за день
const dailyStats = ref({
  totalTime: '7ч 45м',
  activeTime: '6ч 30м',
  appsCount: 12,
  productivity: 84
})

// Топ приложений
const topApps = ref([
  { name: 'VS Code', time: '3ч 45м', percentage: 48 },
  { name: 'Chrome', time: '2ч 15м', percentage: 29 },
  { name: 'Figma', time: '1ч 20м', percentage: 17 },
  { name: 'Slack', time: '30м', percentage: 6 }
])

const getCurrentWindow = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/current-activity')
    currentActivity.value = response.data
    
    // Если это новая активность, сбрасываем таймер сессии
    if (!sessionStartTime.value) {
      sessionStartTime.value = Date.now()
      currentSessionDuration.value = 0
    }
  } catch (error) {
    console.error('Ошибка получения активности:', error)
    // В случае ошибки показываем демонстрационные данные
    currentActivity.value = {
      app: 'VS Code',
      title: 'ActivityTracker.vue - employee-tracker',
      pid: 1234
    }
    if (!sessionStartTime.value) {
      sessionStartTime.value = Date.now()
    }
  }
}

const toggleTracking = () => {
  if (isTracking.value) {
    stopTracking()
  } else {
    startTracking()
  }
}

const startTracking = () => {
  isTracking.value = true
  sessionStartTime.value = Date.now()
  currentSessionDuration.value = 0
  
  getCurrentWindow()
  trackingInterval = setInterval(getCurrentWindow, 5000)
  durationInterval = setInterval(() => {
    if (sessionStartTime.value) {
      currentSessionDuration.value = Math.floor((Date.now() - sessionStartTime.value) / 1000)
    }
  }, 1000)
}

const stopTracking = () => {
  isTracking.value = false
  currentActivity.value = null
  sessionStartTime.value = null
  currentSessionDuration.value = 0
  
  if (trackingInterval) {
    clearInterval(trackingInterval)
    trackingInterval = null
  }
  if (durationInterval) {
    clearInterval(durationInterval)
    durationInterval = null
  }
}

const refreshActivity = () => {
  if (isTracking.value) {
    getCurrentWindow()
  }
}

const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}ч ${minutes}м ${secs}с`
  } else if (minutes > 0) {
    return `${minutes}м ${secs}с`
  } else {
    return `${secs}с`
  }
}

const formatTime = (date) => {
  return date.toLocaleTimeString('ru-RU', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const getAppIcon = (appName) => {
  const icons = {
    'VS Code': '💻',
    'Chrome': '🌐',
    'Firefox': '🦊',
    'Slack': '💬',
    'Figma': '🎨',
    'Terminal': '⚡',
    'Photoshop': '🖼️',
    'Word': '📝',
    'Excel': '📊',
    'PowerPoint': '📈',
    'Zoom': '📹',
    'Teams': '👥',
    'Unknown': '❓'
  }
  return icons[appName] || icons['Unknown']
}

onMounted(() => {
  // Автоматически начинаем отслеживание при загрузке
  startTracking()
})

onUnmounted(() => {
  stopTracking()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.activity-tracker-container {
  font-family: 'Gabarito', sans-serif;
  color: rgba(243, 238, 232, 1);
}

.activity-tracker {
  background: rgba(19, 24, 27, 1);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(243, 238, 232, 0.1);
  max-width: 1000px;
  margin: 0 auto;
}

/* Заголовок */
.tracker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(243, 238, 232, 0.2);
}

.tracker-header h2 {
  margin: 0;
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
}

.tracking-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.tracking-status.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.tracking-status.active .status-dot {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Управление */
.tracking-controls {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.control-btn {
  flex: 1;
  padding: 15px 25px;
  border: none;
  border-radius: 8px;
  font-family: 'Gabarito', sans-serif;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-btn.start {
  background: rgba(76, 175, 80, 1);
  color: white;
}

.control-btn.start:hover {
  background: rgba(69, 160, 73, 1);
  transform: translateY(-2px);
}

.control-btn.stop {
  background: rgba(244, 67, 54, 1);
  color: white;
}

.control-btn.stop:hover {
  background: rgba(229, 57, 53, 1);
  transform: translateY(-2px);
}

.refresh-btn {
  padding: 15px 25px;
  border: none;
  border-radius: 8px;
  background: rgba(33, 150, 243, 1);
  color: white;
  font-family: 'Gabarito', sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(25, 118, 210, 1);
  transform: translateY(-2px);
}

.refresh-btn:disabled {
  background: rgba(33, 150, 243, 0.5);
  cursor: not-allowed;
}

/* Текущая активность */
.current-activity-section {
  margin-bottom: 40px;
}

.current-activity-section h3 {
  margin: 0 0 20px 0;
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
}

.current-activity-card {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 2px solid rgba(76, 175, 80, 0.3);
}

.activity-icon {
  font-size: 3rem;
  background: rgba(131, 21, 21, 0.2);
  border-radius: 50%;
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-details {
  flex: 1;
}

.activity-app {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: rgba(243, 238, 232, 1);
}

.activity-pid {
  font-size: 12px;
  color: rgba(243, 238, 232, 0.6);
  font-weight: normal;
}

.activity-title {
  font-size: 14px;
  color: rgba(243, 238, 232, 0.8);
  margin-bottom: 8px;
}

.activity-duration {
  font-size: 16px;
  font-weight: 600;
  color: rgba(76, 175, 80, 1);
}

.activity-status {
  display: flex;
  align-items: center;
}

.pulse-indicator {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(76, 175, 80, 1);
  animation: pulse-scale 2s infinite;
}

@keyframes pulse-scale {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}

.no-activity,
.loading-activity {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  color: rgba(243, 238, 232, 0.7);
}

.no-activity-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.no-activity-hint {
  font-size: 14px;
  color: rgba(243, 238, 232, 0.5);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(243, 238, 232, 0.3);
  border-top: 4px solid rgba(33, 150, 243, 1);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* История активности */
.activity-history-section {
  margin-bottom: 40px;
}

.activity-history-section h3 {
  margin: 0 0 20px 0;
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
}

.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: 300px;
  overflow-y: auto;
}

.timeline-item {
  background: rgba(58, 60, 65, 1);
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.timeline-time {
  font-weight: 600;
  color: rgba(243, 238, 232, 0.8);
  min-width: 60px;
  font-size: 14px;
}

.timeline-content {
  flex: 1;
}

.timeline-app {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}

.app-icon {
  font-size: 1.2rem;
}

.timeline-title {
  font-size: 14px;
  color: rgba(243, 238, 232, 0.7);
  margin-bottom: 5px;
}

.timeline-duration {
  font-size: 12px;
  color: rgba(243, 238, 232, 0.6);
}

/* Статистика */
.daily-stats-section {
  margin-bottom: 40px;
}

.daily-stats-section h3 {
  margin: 0 0 20px 0;
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
}

.stat-icon {
  font-size: 2rem;
  background: rgba(131, 21, 21, 0.2);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: rgba(243, 238, 232, 1);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: rgba(243, 238, 232, 0.6);
}

/* Топ приложений */
.top-apps-section h3 {
  margin: 0 0 20px 0;
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
}

.apps-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.app-item {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.app-rank {
  font-size: 18px;
  font-weight: 700;
  color: rgba(243, 238, 232, 0.8);
  min-width: 30px;
}

.app-icon-large {
  font-size: 2rem;
  background: rgba(131, 21, 21, 0.2);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-details {
  flex: 1;
}

.app-name {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 5px;
}

.app-time {
  color: rgba(243, 238, 232, 0.7);
  font-size: 14px;
}

.app-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 120px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: rgba(19, 24, 27, 1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, rgba(131, 21, 21, 1), rgba(151, 31, 31, 1));
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 12px;
  font-weight: 600;
  color: rgba(243, 238, 232, 0.8);
  min-width: 35px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .tracker-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .tracking-controls {
    flex-direction: column;
  }

  .current-activity-card {
    flex-direction: column;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .app-item {
    flex-direction: column;
    text-align: center;
  }

  .app-progress {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-tracker {
    padding: 20px;
  }
}
</style>