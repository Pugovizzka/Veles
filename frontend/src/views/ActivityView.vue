<template>
  <div class="activity-view">
    <h2>Активность сотрудников</h2>
    <ActivityTracker />
  </div>
</template>

<script setup>
import ActivityTracker from '@/components/ActivityTracker.vue'
</script>

<style scoped>
.activity-view {
  padding: 20px;
}
</style>
