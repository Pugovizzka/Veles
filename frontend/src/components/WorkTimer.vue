<template>
  <div class="timer-container">
    <div class="timer">
      <h2>Учёт рабочего времени</h2>
      <div class="display">{{ formattedTime }}</div>

      <div class="button-container">
        <button v-if="!isRunning" @click="startWork" class="start-btn">
          Начать рабочий день
        </button>
        <button v-if="isRunning" @click="stopWork" class="stop-btn">
          Закончить рабочий день
        </button>
      </div>

      <div v-if="duration" class="duration-result">
        Вы отработали: {{ duration }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const isRunning = ref(false)
const startTime = ref(null)
const endTime = ref(null)
const elapsed = ref(0)
const duration = ref(null)

let intervalId = null

const updateTimer = () => {
  if (isRunning.value && startTime.value) {
    elapsed.value = Math.floor((Date.now() - startTime.value) / 1000)
  }
}

const formattedTime = computed(() => {
  const hours = Math.floor(elapsed.value / 3600).toString().padStart(2, '0')
  const minutes = Math.floor((elapsed.value % 3600) / 60).toString().padStart(2, '0')
  const seconds = (elapsed.value % 60).toString().padStart(2, '0')
  return `${hours}:${minutes}:${seconds}`
})

const startWork = () => {
  startTime.value = Date.now()
  isRunning.value = true
  duration.value = null
  intervalId = setInterval(updateTimer, 1000)
}

const stopWork = async () => {
  clearInterval(intervalId)
  isRunning.value = false
  endTime.value = Date.now()
  elapsed.value = Math.floor((endTime.value - startTime.value) / 1000)

  try {
    const response = await axios.post(`${process.env.VUE_APP_BACKEND_API_URL}/stop`, {
      start_time: new Date(startTime.value).toISOString(),
      end_time: new Date(endTime.value).toISOString()
    })
    duration.value = response.data.duration_human
    console.log('Время успешно отправлено')
  } catch (error) {
    console.error('Ошибка отправки времени', error)
  }
}

onMounted(() => {
  if (isRunning.value) {
    intervalId = setInterval(updateTimer, 1000)
  }
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.timer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  font-family: 'Gabarito', sans-serif;
}

.timer {
  text-align: center;
  padding: 40px;
  background: rgba(19, 24, 27, 1);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(243, 238, 232, 0.1);
  max-width: 500px;
  width: 100%;
}

.timer h2 {
  color: rgba(243, 238, 232, 1);
  margin-bottom: 30px;
  font-weight: 600;
}

.display {
  font-size: 3em;
  margin: 30px 0;
  color: rgba(243, 238, 232, 1);
  font-weight: 700;
  font-family: 'Gabarito', monospace;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.button-container {
  margin: 30px 0;
}

.start-btn, .stop-btn {
  margin: 10px;
  padding: 15px 30px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Gabarito', sans-serif;
}

.start-btn {
  background-color: #4CAF50;
  color: rgba(243, 238, 232, 1);
}

.start-btn:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.stop-btn {
  background-color: rgba(131, 21, 21, 1);
  color: rgba(243, 238, 232, 1);
}

.stop-btn:hover {
  background-color: rgba(151, 31, 31, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(131, 21, 21, 0.4);
}

.duration-result {
  margin-top: 20px;
  padding: 15px;
  background: rgba(58, 60, 65, 1);
  border-radius: 8px;
  color: rgba(243, 238, 232, 1);
  font-weight: 600;
  font-size: 18px;
}
</style>