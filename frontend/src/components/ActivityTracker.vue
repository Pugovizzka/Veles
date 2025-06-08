<template>
  <div class="activity-tracker-container">
    <div class="activity-tracker">
      <h2>Отслеживание активности</h2>

      <div v-if="currentActivity" class="activity-content">
        <p><strong>Приложение:</strong> {{ currentActivity.app }}</p>
        <p><strong>Окно:</strong> {{ currentActivity.title }}</p>
        <p><strong>Продолжительность:</strong> {{ formatDuration(currentActivity.duration) }}</p>
      </div>

      <div v-else class="activity-content">
        <p>Нет данных об активности</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const currentActivity = ref(null)
let trackingInterval = null

const getCurrentWindow = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/current-activity')
    currentActivity.value = response.data
  } catch (error) {
    console.error('Ошибка получения активности:', error)
  }
}

const formatDuration = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  return `${hours} ч ${minutes % 60} мин`
}

onMounted(() => {
  getCurrentWindow()
  trackingInterval = setInterval(getCurrentWindow, 5000)
})

onUnmounted(() => {
  if (trackingInterval) {
    clearInterval(trackingInterval)
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.activity-tracker-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  font-family: 'Gabarito', sans-serif;
}

.activity-tracker {
  text-align: center;
  padding: 40px;
  background: rgba(19, 24, 27, 1);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(243, 238, 232, 0.1);
  max-width: 600px;
  width: 100%;
}

.activity-tracker h2 {
  color: rgba(243, 238, 232, 1);
  margin-bottom: 20px;
  font-weight: 600;
}

.activity-content {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 20px;
  color: rgba(243, 238, 232, 1);
  text-align: left;
}

.activity-content p {
  margin: 10px 0;
  font-size: 16px;
  font-weight: 500;
}
</style>
