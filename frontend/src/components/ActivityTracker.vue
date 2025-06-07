<template>
  <div class="activity-tracker">
    <h3>Отслеживание активности</h3>
    <div v-if="currentActivity" class="current-activity">
      <p>Текущее приложение: {{ currentActivity.app }}</p>
      <p>Название окна: {{ currentActivity.title }}</p>
      <p>Продолжительность: {{ formatDuration(currentActivity.duration) }}</p>
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
    console.error('Error fetching activity:', error)
  }
}

const formatDuration = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  return `${hours}h ${minutes % 60}m`
}

onMounted(() => {
  getCurrentWindow()
  trackingInterval = setInterval(getCurrentWindow, 5000) // Poll every 5 seconds
})

onUnmounted(() => {
  if (trackingInterval) {
    clearInterval(trackingInterval)
  }
})
</script>

<style scoped>
.activity-tracker {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.current-activity {
  margin-top: 1rem;
}

.current-activity p {
  margin: 0.5rem 0;
}
</style>