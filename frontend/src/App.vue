<template>
  <div id="app">
    <WorkTimer />
  </div>
</template>

<script>
import WorkTimer from './components/WorkTimer.vue'

export default {
  name: 'App',
  components: {
    WorkTimer
  }
}
</script>

<style>
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
}
</style>
