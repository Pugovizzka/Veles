<template>
  <div class="timer">
    <h2>Учёт рабочего времени</h2>
    <div class="display">{{ formattedTime }}</div>

    <button v-if="!isRunning" @click="startWork">Начать рабочий день</button>
    <button v-if="isRunning" @click="stopWork">Закончить рабочий день</button>

    <div v-if="duration">Вы отработали: {{ duration }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const isRunning = ref(false)
const startTime = ref(null)
const endTime = ref(null)
const elapsed = ref(0)
const duration = ref(null)  // Новая переменная для вывода времени

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
  duration.value = null  // Сбросим предыдущий результат
  intervalId = setInterval(updateTimer, 1000)
}

const stopWork = async () => {
  clearInterval(intervalId)
  isRunning.value = false
  endTime.value = Date.now()
  elapsed.value = Math.floor((endTime.value - startTime.value) / 1000)

  try {
    const response = await axios.post('http://127.0.0.1:8000/stop', {
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
.timer {
  text-align: center;
  padding: 20px;
}
.display {
  font-size: 2em;
  margin: 10px 0;
}
button {
  margin: 5px;
  padding: 10px 20px;
}
</style>
